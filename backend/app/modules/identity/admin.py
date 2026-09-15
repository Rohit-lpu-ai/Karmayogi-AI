"""User and department administration (Phase 4A, SECURITY_RESPONSIBLE_AI.md §3-4).

Rules enforced here, on the server:
- Everything is scoped to the caller's organisation.
- A caller who holds ``users.*`` only through ``department_admin`` sees and manages users in the departments they
  are scoped to, may create learners only, and may not manage accounts that hold any administrative role.
- Role changes need ``roles.assign``. Only a platform_admin may grant, remove or manage platform_admin accounts.
- Administrators cannot change their own roles or deactivate themselves (use another administrator).
- Accounts are never deleted; deactivation revokes every session. New accounts start ``invited`` with a one-time
  account-setup token instead of an administrator-chosen password.
"""

from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession
from sqlalchemy.orm.exc import StaleDataError

from app.core.config import Settings
from app.core.errors import ProblemError
from app.core.vocab import ACCESS_ROLES
from app.modules.governance.service import record_audit
from app.modules.identity import accounts, service
from app.modules.identity.admin_schemas import (
    AdminDepartment,
    AdminRole,
    AdminUser,
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
    NamedRef,
    RoleAssignment,
    RoleAssignmentRequest,
)
from app.modules.identity.dependencies import CurrentUser
from app.modules.identity.models import User, UserAccessRole
from app.modules.identity.policy import ADMIN_ROLES, ROLE_DESCRIPTIONS, capabilities_for, has_capability, only_department_scoped
from app.modules.identity.schemas import DepartmentRef
from app.modules.organization.models import Department, JobRole

SCOPED_ROLES = frozenset({"department_admin", "trainer", "training_manager"})


def _not_found() -> ProblemError:
    return ProblemError(404, "NOT_FOUND", "Not found", "User not found.")


def _forbidden(detail: str) -> ProblemError:
    return ProblemError(403, "FORBIDDEN", "Forbidden", detail)


def department_scope(db: DbSession, current: CurrentUser, capability: str) -> set[uuid.UUID] | None:
    """None when the caller is organisation-wide for this capability; otherwise their department scope ids."""
    if not only_department_scoped(current.roles, capability):
        return None
    return set(db.scalars(select(UserAccessRole.department_scope_id).where(
        UserAccessRole.user_id == current.user.id, UserAccessRole.role == "department_admin",
        UserAccessRole.department_scope_id.is_not(None))))


def _roles_of(db: DbSession, user_ids: list[uuid.UUID]) -> dict[uuid.UUID, list[RoleAssignment]]:
    out: dict[uuid.UUID, list[RoleAssignment]] = {uid: [] for uid in user_ids}
    if not user_ids:
        return out
    for row in db.scalars(select(UserAccessRole).where(UserAccessRole.user_id.in_(user_ids))
                          .order_by(UserAccessRole.role)):
        out[row.user_id].append(RoleAssignment(role=row.role, department_scope_id=row.department_scope_id))
    return out


def to_admin_users(db: DbSession, users: list[User]) -> list[AdminUser]:
    roles = _roles_of(db, [u.id for u in users])
    dept_ids = {u.department_id for u in users if u.department_id}
    role_ids = {u.job_role_id for u in users if u.job_role_id}
    departments = {d.id: d for d in db.scalars(select(Department).where(Department.id.in_(dept_ids)))} if dept_ids else {}
    job_roles = {r.id: r for r in db.scalars(select(JobRole).where(JobRole.id.in_(role_ids)))} if role_ids else {}
    items = []
    for u in users:
        d = departments.get(u.department_id)
        r = job_roles.get(u.job_role_id)
        items.append(AdminUser(
            id=u.id, display_name=u.display_name, email=u.email, registration_id=u.registration_id,
            designation=u.designation, status=u.status,
            department=DepartmentRef(id=d.id, name=d.name, code=d.code) if d else None,
            job_role=NamedRef(id=r.id, name=r.name) if r else None,
            roles=roles[u.id], is_synthetic=u.is_synthetic, has_password=u.password_hash is not None,
            last_login_at=u.last_login_at, created_at=u.created_at, row_version=u.row_version,
        ))
    return items


def list_users(db: DbSession, current: CurrentUser, *, q: str | None, status: str | None, role: str | None,
               department_id: uuid.UUID | None, page: int, page_size: int) -> tuple[list[AdminUser], int]:
    query = select(User).where(User.organization_id == current.user.organization_id)
    scope = department_scope(db, current, "users.view")
    if scope is not None:
        query = query.where(User.department_id.in_(scope or {uuid.UUID(int=0)}))
    if q:
        like = f"%{q.strip()}%"
        query = query.where(or_(User.display_name.ilike(like), User.email.ilike(like), User.registration_id.ilike(like)))
    if status:
        query = query.where(User.status == status)
    if department_id:
        query = query.where(User.department_id == department_id)
    if role:
        query = query.where(User.id.in_(select(UserAccessRole.user_id).where(UserAccessRole.role == role)))
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    users = db.scalars(query.order_by(User.display_name, User.id).offset((page - 1) * page_size).limit(page_size)).all()
    return to_admin_users(db, list(users)), total


def _load_manageable(db: DbSession, current: CurrentUser, user_id: uuid.UUID, capability: str) -> User:
    user = db.scalar(select(User).where(User.id == user_id, User.organization_id == current.user.organization_id))
    if user is None:
        raise _not_found()
    scope = department_scope(db, current, capability)
    if scope is not None and user.department_id not in scope:
        raise _not_found()  # outside the caller's scope: indistinguishable from absent
    return user


def get_user(db: DbSession, current: CurrentUser, user_id: uuid.UUID) -> AdminUser:
    return to_admin_users(db, [_load_manageable(db, current, user_id, "users.view")])[0]


def _check_target_manageable(db: DbSession, current: CurrentUser, target: User) -> None:
    target_roles = set(service.access_roles(db, target))
    if department_scope(db, current, "users.manage") is not None and target_roles & ADMIN_ROLES:
        raise _forbidden("Department administrators can manage learner accounts only.")
    if "platform_admin" in target_roles and "platform_admin" not in current.roles:
        raise _forbidden("Only a platform administrator can manage this account.")


def _validated_roles(db: DbSession, current: CurrentUser, requested: list[RoleAssignmentRequest],
                     department_id: uuid.UUID | None) -> list[RoleAssignmentRequest]:
    seen: dict[tuple[str, uuid.UUID | None], RoleAssignmentRequest] = {}
    for item in requested:
        if item.role not in ACCESS_ROLES:
            raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Unknown access role.",
                               errors=[{"field": "roles", "code": "UNKNOWN_ROLE", "message": f"Unknown role {item.role}."}])
        scope_id = item.department_scope_id
        if item.role in SCOPED_ROLES and scope_id is None:
            scope_id = department_id
        if item.role == "department_admin" and scope_id is None:
            raise ProblemError(422, "VALIDATION_FAILED", "Validation failed",
                               "A department administrator needs a department.",
                               errors=[{"field": "roles", "code": "DEPARTMENT_SCOPE_REQUIRED",
                                        "message": "Choose a department for the department administrator role."}])
        if item.role not in SCOPED_ROLES:
            scope_id = None
        if scope_id is not None:
            accounts._department_in_org(db, current.user.organization_id, scope_id)
        seen[(item.role, scope_id)] = RoleAssignmentRequest(role=item.role, department_scope_id=scope_id)
    roles = list(seen.values())
    names = {r.role for r in roles}
    if names != {"learner"} and not has_capability(current.roles, "roles.assign"):
        raise _forbidden("Your access role can create learner accounts only.")
    if "platform_admin" in names and "platform_admin" not in current.roles:
        raise _forbidden("Only a platform administrator can grant the platform administrator role.")
    return roles


def _department_allowed(db: DbSession, current: CurrentUser, department_id: uuid.UUID | None) -> None:
    scope = department_scope(db, current, "users.manage")
    if scope is not None and department_id not in scope:
        raise _forbidden("Choose a department you administer.")
    if department_id is not None:
        accounts._department_in_org(db, current.user.organization_id, department_id)


def create_user(db: DbSession, settings: Settings, current: CurrentUser, body: AdminUserCreateRequest):
    org_id = current.user.organization_id
    _department_allowed(db, current, body.department_id)
    roles = _validated_roles(db, current, body.roles, body.department_id)
    email = body.email.strip()
    registration_id = body.registration_id.strip() if body.registration_id else None
    accounts.ensure_unique_identity(db, org_id, email, registration_id)
    job_role = service.active_job_role(db, org_id, body.job_role_id) if body.job_role_id else None
    user = User(organization_id=org_id, email=email, display_name=body.display_name.strip(),
                registration_id=registration_id, designation=(body.designation or "").strip() or None,
                department_id=body.department_id, job_role_id=job_role.id if job_role else None,
                status="invited", is_synthetic=False, created_by=current.user.id)
    db.add(user)
    db.flush()
    for r in roles:
        db.add(UserAccessRole(organization_id=org_id, user_id=user.id, role=r.role, department_scope_id=r.department_scope_id,
                              created_by=current.user.id))
    record_audit(db, organization_id=org_id, action="user.create", target_type="user", target_id=str(user.id),
                 actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"roles": sorted(r.role for r in roles), "status": "invited", "source": "administrator"})
    token, expires_at = accounts.issue_password_token(db, settings, user, current.user, "account_setup")
    db.commit()
    return to_admin_users(db, [user])[0], token, expires_at


def update_user(db: DbSession, current: CurrentUser, user_id: uuid.UUID, body: AdminUserUpdateRequest) -> AdminUser:
    user = _load_manageable(db, current, user_id, "users.manage")
    _check_target_manageable(db, current, user)
    if user.row_version != body.row_version:
        raise ProblemError(409, "STALE_VERSION", "Changed by someone else", "This account changed since you opened it. Reload and try again.")
    fields = body.model_dump(exclude_unset=True)
    fields.pop("row_version")
    before, after = {}, {}
    is_self = user.id == current.user.id

    if "display_name" in fields and fields["display_name"]:
        user.display_name = fields["display_name"].strip()
        after["display_name"] = "changed"
    if "designation" in fields:
        user.designation = (fields["designation"] or "").strip() or None
        after["designation"] = "changed"
    if "registration_id" in fields:
        new_id = (fields["registration_id"] or "").strip() or None
        accounts.ensure_unique_identity(db, user.organization_id, None, new_id, exclude_user_id=user.id)
        user.registration_id = new_id
        after["registration_id"] = "changed"
    if "department_id" in fields:
        _department_allowed(db, current, fields["department_id"])
        before["department_id"] = str(user.department_id) if user.department_id else None
        user.department_id = fields["department_id"]
        after["department_id"] = str(user.department_id) if user.department_id else None
    if "job_role_id" in fields:
        role = service.active_job_role(db, user.organization_id, fields["job_role_id"]) if fields["job_role_id"] else None
        before["job_role_id"] = str(user.job_role_id) if user.job_role_id else None
        user.job_role_id = role.id if role else None
        after["job_role_id"] = str(user.job_role_id) if user.job_role_id else None
    if fields.get("status") and fields["status"] != user.status:
        if is_self:
            raise _forbidden("You cannot change the status of your own account.")
        if fields["status"] == "active" and user.password_hash is None:
            raise ProblemError(409, "PASSWORD_NOT_SET", "Account not set up",
                               "This account has no password yet. Issue an account setup link instead.")
        before["status"], after["status"] = user.status, fields["status"]
        user.status = fields["status"]
        if user.status == "inactive":
            after["sessions_revoked"] = accounts.revoke_sessions(db, user)
        else:
            user.failed_login_count = 0
            user.locked_until = None
    if fields.get("roles") is not None:
        if not has_capability(current.roles, "roles.assign"):
            raise _forbidden("Your access role cannot change access roles.")
        if is_self:
            raise _forbidden("You cannot change your own access roles.")
        requested = [RoleAssignmentRequest(**r) for r in fields["roles"]]
        roles = _validated_roles(db, current, requested, user.department_id)
        existing = list(db.scalars(select(UserAccessRole).where(UserAccessRole.user_id == user.id)))
        before["roles"] = sorted(r.role for r in existing)
        wanted = {(r.role, r.department_scope_id) for r in roles}
        have = {(r.role, r.department_scope_id): r for r in existing}
        for key, row in have.items():
            if key not in wanted:
                db.delete(row)
        db.flush()
        for role_name, scope_id in wanted - set(have):
            db.add(UserAccessRole(organization_id=user.organization_id, user_id=user.id, role=role_name,
                                  department_scope_id=scope_id, created_by=current.user.id))
        after["roles"] = sorted(r.role for r in roles)
        if before["roles"] != after["roles"]:
            after["sessions_revoked"] = accounts.revoke_sessions(db, user)  # role change takes effect on next sign-in
    if not after:
        return to_admin_users(db, [user])[0]
    user.updated_by = current.user.id
    record_audit(db, organization_id=user.organization_id, action="user.update", target_type="user", target_id=str(user.id),
                 actor_user_id=current.user.id, actor_roles=sorted(current.roles), before=before or None, after=after)
    try:
        db.commit()
    except StaleDataError:
        db.rollback()
        raise ProblemError(409, "STALE_VERSION", "Changed by someone else", "This account changed since you opened it. Reload and try again.")
    return to_admin_users(db, [user])[0]


def issue_reset(db: DbSession, settings: Settings, current: CurrentUser, user_id: uuid.UUID):
    user = _load_manageable(db, current, user_id, "users.manage")
    _check_target_manageable(db, current, user)
    if user.id == current.user.id:
        raise _forbidden("Change your own password from your profile.")
    if user.status == "inactive":
        raise ProblemError(409, "USER_INACTIVE", "Account inactive", "Reactivate the account before issuing a link.")
    purpose = "password_reset" if user.password_hash else "account_setup"
    token, expires_at = accounts.issue_password_token(db, settings, user, current.user, purpose)
    db.commit()
    return purpose, token, expires_at


def list_roles(db: DbSession, current: CurrentUser) -> list[AdminRole]:
    counts = dict(db.execute(select(UserAccessRole.role, func.count(func.distinct(UserAccessRole.user_id)))
                             .where(UserAccessRole.organization_id == current.user.organization_id)
                             .group_by(UserAccessRole.role)).all())
    return [AdminRole(role=role, label=ROLE_DESCRIPTIONS[role][0], description=ROLE_DESCRIPTIONS[role][1],
                      capabilities=capabilities_for([role]), user_count=counts.get(role, 0),
                      department_scoped=role in SCOPED_ROLES)
            for role in ACCESS_ROLES]


# --- Departments --------------------------------------------------------------------------------------------


def list_departments(db: DbSession, current: CurrentUser) -> list[AdminDepartment]:
    org_id = current.user.organization_id
    counts = dict(db.execute(select(User.department_id, func.count()).where(User.organization_id == org_id)
                             .group_by(User.department_id)).all())
    query = select(Department).where(Department.organization_id == org_id)
    scope = department_scope(db, current, "users.view")
    if scope is not None:
        query = query.where(Department.id.in_(scope or {uuid.UUID(int=0)}))
    return [AdminDepartment(id=d.id, name=d.name, code=d.code, status=d.status, user_count=counts.get(d.id, 0))
            for d in db.scalars(query.order_by(Department.name))]


def _unique_department_name(db: DbSession, org_id: uuid.UUID, name: str, exclude: uuid.UUID | None = None) -> None:
    query = select(Department.id).where(Department.organization_id == org_id, func.lower(Department.name) == name.lower())
    if exclude:
        query = query.where(Department.id != exclude)
    if db.scalar(query) is not None:
        raise ProblemError(409, "DEPARTMENT_EXISTS", "Department exists", "A department with this name already exists.",
                           errors=[{"field": "name", "code": "DEPARTMENT_EXISTS", "message": "Name already used."}])


def create_department(db: DbSession, current: CurrentUser, name: str, code: str | None) -> AdminDepartment:
    org_id = current.user.organization_id
    name = name.strip()
    _unique_department_name(db, org_id, name)
    department = Department(organization_id=org_id, name=name, code=code, status="active", created_by=current.user.id)
    db.add(department)
    db.flush()
    record_audit(db, organization_id=org_id, action="department.create", target_type="department",
                 target_id=str(department.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"name": name, "code": code})
    db.commit()
    return AdminDepartment(id=department.id, name=department.name, code=department.code, status=department.status, user_count=0)


def update_department(db: DbSession, current: CurrentUser, department_id: uuid.UUID, fields: dict) -> AdminDepartment:
    org_id = current.user.organization_id
    department = db.scalar(select(Department).where(Department.id == department_id, Department.organization_id == org_id))
    if department is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Department not found.")
    before = {"name": department.name, "code": department.code, "status": department.status}
    if fields.get("name"):
        _unique_department_name(db, org_id, fields["name"].strip(), exclude=department.id)
        department.name = fields["name"].strip()
    if "code" in fields:
        department.code = fields["code"]
    if fields.get("status"):
        department.status = fields["status"]
    department.updated_by = current.user.id
    after = {"name": department.name, "code": department.code, "status": department.status}
    if after != before:
        record_audit(db, organization_id=org_id, action="department.update", target_type="department",
                     target_id=str(department.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                     before=before, after=after)
    db.commit()
    count = db.scalar(select(func.count()).select_from(User).where(User.department_id == department.id)) or 0
    return AdminDepartment(id=department.id, name=department.name, code=department.code, status=department.status,
                           user_count=count)
