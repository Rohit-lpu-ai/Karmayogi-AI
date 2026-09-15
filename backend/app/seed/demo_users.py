"""Synthetic demo accounts for local development (DATA_MODEL.md §15).

Only allowed in local, ci and staging. Every account is ``is_synthetic=true``,
uses the reserved ``example.invalid`` domain. When a demo password is supplied
(``DEMO_USER_PASSWORD``, never hardcoded) accounts without a password receive its
Argon2id hash and become ``active``. Demo job roles and content live in
``demo_content.py`` (DEC-045).
"""

from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.core.vocab import ACCESS_ROLES
from app.modules.governance.service import record_audit
from app.modules.identity.models import User, UserAccessRole
from app.modules.identity.security import hash_password
from app.modules.organization.models import Department, Organization
from app.seed.canonical import SeedRefused

SYNTHETIC_ALLOWED_ENVS = {AppEnv.local, AppEnv.ci, AppEnv.staging}
DEMO_DEPARTMENT_NAME = "Demo Department (synthetic)"
DEMO_EMAIL_DOMAIN = "example.invalid"


def demo_email(role: str) -> str:
    return f"{role.replace('_', '-')}01@{DEMO_EMAIL_DOMAIN}"


def demo_registration_id(role: str) -> str:
    """Synthetic registration ID (Phase 4A). The DEMO- prefix keeps it visibly non-official."""
    return f"DEMO-{role.replace('_', '-').upper()}-01"


def seed_demo_users(session: Session, org: Organization, app_env: AppEnv, password: str | None = None) -> Counter:
    if app_env not in SYNTHETIC_ALLOWED_ENVS:
        raise SeedRefused(f"Synthetic demo users are not allowed in {app_env.value}")
    created: Counter = Counter()

    department = session.scalar(
        select(Department).where(Department.organization_id == org.id, Department.name == DEMO_DEPARTMENT_NAME)
    )
    if department is None:
        department = Department(organization_id=org.id, name=DEMO_DEPARTMENT_NAME, code="demo", status="active")
        session.add(department)
        session.flush()
        created["departments"] += 1

    for role in ACCESS_ROLES:
        email = demo_email(role)
        user = session.scalar(select(User).where(User.organization_id == org.id, User.email == email))
        if user is not None:
            if user.is_synthetic and user.registration_id is None:
                user.registration_id = demo_registration_id(role)  # backfill accounts seeded before migration 0006
                created["registration_ids_backfilled"] += 1
            continue
        user = User(
            organization_id=org.id,
            email=email,
            display_name=f"Demo {role.replace('_', ' ').title()} 01",
            registration_id=demo_registration_id(role),
            department_id=department.id,
            status="invited",
            is_synthetic=True,
        )
        session.add(user)
        session.flush()
        session.add(UserAccessRole(
            organization_id=org.id,
            user_id=user.id,
            role=role,
            department_scope_id=department.id if role in ("department_admin", "trainer", "training_manager") else None,
        ))
        created["users"] += 1
        created["user_access_roles"] += 1

    if password is not None:
        hash_password(password)  # validate length once before touching any account (raises if < 12 chars)
        for user in session.scalars(select(User).where(User.organization_id == org.id, User.is_synthetic,
                                                       User.password_hash.is_(None))):
            user.password_hash = hash_password(password)  # unique salt per account
            user.status = "active"
            created["passwords_set"] += 1

    if created:
        record_audit(
            session, organization_id=org.id, action="seed.import", target_type="synthetic_demo_users",
            after={"created": dict(created)},
        )
    session.flush()
    return created
