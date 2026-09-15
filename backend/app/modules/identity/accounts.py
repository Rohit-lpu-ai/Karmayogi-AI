"""Account lifecycle: learner self-registration, profile updates, password change and one-time set-password tokens.

SECURITY_RESPONSIBLE_AI.md §3: Argon2id hashing, minimum length 12, change requires the current password,
administrator-initiated reset issues a one-time token with expiry, all sessions are revoked on change or reset.
Self-registration is an explicit Phase 4 assumption (A-1): learner role only, and only when the settings allow it.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession

from app.core.config import Settings
from app.core.errors import ProblemError
from app.modules.governance.service import record_audit
from app.modules.identity import service
from app.modules.identity.models import PasswordResetToken, Session, User, UserAccessRole
from app.modules.identity.security import hash_password, verify_password
from app.modules.organization.models import Department, JobRole, Organization

logger = logging.getLogger("app.identity.accounts")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def resolve_registration_org(db: DbSession, organization_code: str | None) -> Organization | None:
    query = select(Organization).where(Organization.status == "active")
    if organization_code:
        query = query.where(Organization.code == organization_code)
    orgs = db.scalars(query.limit(2)).all()
    return orgs[0] if len(orgs) == 1 else None


def registration_options(db: DbSession, settings: Settings, organization_code: str | None = None) -> dict:
    if not settings.self_registration_enabled:
        return {"enabled": False}
    org = resolve_registration_org(db, organization_code)
    if org is None:
        return {"enabled": False}
    departments = db.scalars(select(Department).where(Department.organization_id == org.id, Department.status == "active")
                             .order_by(Department.name)).all()
    roles = db.scalars(select(JobRole).where(JobRole.organization_id == org.id, JobRole.status == "active")
                       .order_by(JobRole.name)).all()
    return {"enabled": True, "organization_name": org.name,
            "departments": [{"id": d.id, "name": d.name} for d in departments],
            "job_roles": [{"id": r.id, "name": r.name} for r in roles]}


def _department_in_org(db: DbSession, organization_id: uuid.UUID, department_id: uuid.UUID) -> Department:
    department = db.scalar(select(Department).where(Department.id == department_id, Department.organization_id == organization_id,
                                                     Department.status == "active"))
    if department is None:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Choose an active department.",
                           errors=[{"field": "department_id", "code": "UNKNOWN_DEPARTMENT", "message": "Unknown department."}])
    return department


def ensure_unique_identity(db: DbSession, organization_id: uuid.UUID, email: str | None, registration_id: str | None,
                           exclude_user_id: uuid.UUID | None = None) -> None:
    query = select(User.id).where(User.organization_id == organization_id, User.email == email)
    if exclude_user_id:
        query = query.where(User.id != exclude_user_id)
    if email is not None and db.scalar(query) is not None:
        raise ProblemError(409, "EMAIL_IN_USE", "Email already registered",
                           "An account with this email already exists. Sign in, or ask your administrator to reset access.",
                           errors=[{"field": "email", "code": "EMAIL_IN_USE", "message": "Email already registered."}])
    if registration_id:
        query = select(User.id).where(User.organization_id == organization_id, User.registration_id == registration_id)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        if db.scalar(query) is not None:
            raise ProblemError(409, "REGISTRATION_ID_IN_USE", "Registration ID already in use",
                               "This registration ID is already linked to an account. Check the ID or contact your administrator.",
                               errors=[{"field": "registration_id", "code": "REGISTRATION_ID_IN_USE",
                                        "message": "Registration ID already in use."}])


def register_learner(db: DbSession, settings: Settings, *, display_name: str, email: str, password: str,
                     registration_id: str, department_id: uuid.UUID | None, job_role_id: uuid.UUID | None,
                     organization_code: str | None) -> User:
    if not settings.self_registration_enabled:
        raise ProblemError(403, "REGISTRATION_DISABLED", "Registration is not available",
                           "Accounts are created by your administrator. Contact them for access.")
    org = resolve_registration_org(db, organization_code)
    if org is None:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Enter your organisation code.",
                           errors=[{"field": "organization_code", "code": "ORGANIZATION_REQUIRED", "message": "Organisation code required."}])
    email = email.strip()
    registration_id = registration_id.strip()
    ensure_unique_identity(db, org.id, email, registration_id)
    department = _department_in_org(db, org.id, department_id) if department_id else None
    job_role = service.active_job_role(db, org.id, job_role_id) if job_role_id else None

    user = User(organization_id=org.id, email=email, display_name=display_name.strip(), registration_id=registration_id,
                department_id=department.id if department else None, job_role_id=job_role.id if job_role else None,
                password_hash=hash_password(password), status="active", is_synthetic=False)
    try:
        with db.begin_nested():
            db.add(user)
            db.flush()
    except IntegrityError:
        # A concurrent registration won the unique index; report it the same way as the pre-check.
        db.expire_all()
        ensure_unique_identity(db, org.id, email, registration_id)
        raise
    db.add(UserAccessRole(organization_id=org.id, user_id=user.id, role="learner"))
    record_audit(db, organization_id=org.id, action="user.create", target_type="user", target_id=str(user.id),
                 actor_user_id=user.id, actor_roles=["learner"], after={"roles": ["learner"], "source": "self_registration"},
                 reason="Learner self-registration (assumption A-1)")
    db.flush()
    return user


def update_profile(db: DbSession, user: User, *, fields: dict) -> User:
    before, after = {}, {}
    if "display_name" in fields and fields["display_name"] is not None:
        before["display_name"], after["display_name"] = "changed", "changed"  # personal data is not copied into audit
        user.display_name = fields["display_name"].strip()
    if "designation" in fields:
        user.designation = (fields["designation"] or "").strip() or None
        after["designation"] = "changed"
    if "department_id" in fields:
        department = _department_in_org(db, user.organization_id, fields["department_id"]) if fields["department_id"] else None
        before["department_id"] = str(user.department_id) if user.department_id else None
        user.department_id = department.id if department else None
        after["department_id"] = str(user.department_id) if user.department_id else None
    if after:
        record_audit(db, organization_id=user.organization_id, action="user.update", target_type="user",
                     target_id=str(user.id), actor_user_id=user.id, actor_roles=service.access_roles(db, user),
                     before=before or None, after=after)
    db.commit()
    return user


def revoke_sessions(db: DbSession, user: User, *, keep_session_id: str | None = None) -> int:
    query = update(Session).where(Session.user_id == user.id, Session.revoked_at.is_(None))
    if keep_session_id:
        query = query.where(Session.id != keep_session_id)
    return db.execute(query.values(revoked_at=utcnow())).rowcount or 0


def change_password(db: DbSession, user: User, current_session: Session, current_password: str, new_password: str) -> None:
    if not verify_password(user.password_hash, current_password):
        record_audit(db, organization_id=user.organization_id, action="auth.password.change", target_type="user",
                     target_id=str(user.id), actor_user_id=user.id, outcome="failure", reason="current_password_mismatch")
        db.commit()
        raise ProblemError(422, "CURRENT_PASSWORD_INCORRECT", "Password not changed", "Your current password is incorrect.",
                           errors=[{"field": "current_password", "code": "CURRENT_PASSWORD_INCORRECT", "message": "Incorrect password."}])
    if current_password == new_password:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Choose a password different from your current one.",
                           errors=[{"field": "new_password", "code": "PASSWORD_UNCHANGED", "message": "Same as current password."}])
    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    revoked = revoke_sessions(db, user, keep_session_id=current_session.id)
    record_audit(db, organization_id=user.organization_id, action="auth.password.change", target_type="user",
                 target_id=str(user.id), actor_user_id=user.id, actor_roles=service.access_roles(db, user),
                 after={"other_sessions_revoked": revoked})
    db.commit()


def issue_password_token(db: DbSession, settings: Settings, user: User, issued_by: User, purpose: str) -> tuple[str, datetime]:
    now = utcnow()
    # Only the newest token works: earlier unused tokens are closed.
    db.execute(update(PasswordResetToken).where(PasswordResetToken.user_id == user.id, PasswordResetToken.used_at.is_(None))
               .values(used_at=now))
    token = secrets.token_urlsafe(32)
    expires_at = now + timedelta(hours=settings.password_token_ttl_hours)
    db.add(PasswordResetToken(organization_id=user.organization_id, user_id=user.id, token_hash=_token_hash(token),
                              issued_by=issued_by.id, purpose=purpose, expires_at=expires_at))
    record_audit(db, organization_id=user.organization_id, action="auth.password.reset_issued", target_type="user",
                 target_id=str(user.id), actor_user_id=issued_by.id, actor_roles=service.access_roles(db, issued_by),
                 after={"purpose": purpose, "expires_at": expires_at.isoformat()})
    return token, expires_at


def set_password_with_token(db: DbSession, token: str, new_password: str) -> None:
    now = utcnow()
    record = db.scalar(select(PasswordResetToken).where(PasswordResetToken.token_hash == _token_hash(token)).with_for_update())
    if record is None or record.used_at is not None or record.expires_at <= now:
        logger.warning("password_token_rejected")
        raise ProblemError(400, "TOKEN_INVALID", "Link not valid",
                           "This set-password link is invalid, already used or expired. Ask your administrator for a new one.")
    user = db.get(User, record.user_id)
    if user is None or user.status not in ("active", "invited"):
        raise ProblemError(400, "TOKEN_INVALID", "Link not valid",
                           "This set-password link is invalid, already used or expired. Ask your administrator for a new one.")
    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    user.failed_login_count = 0
    user.locked_until = None
    if user.status == "invited":
        user.status = "active"
    record.used_at = now
    revoke_sessions(db, user)
    record_audit(db, organization_id=user.organization_id, action="auth.password.change", target_type="user",
                 target_id=str(user.id), actor_user_id=user.id, after={"via": record.purpose, "all_sessions_revoked": True})
    db.commit()
