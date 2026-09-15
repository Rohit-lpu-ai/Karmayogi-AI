"""Identity service: login, sessions, profile, notice acknowledgement, job-role selection."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.core.config import Settings
from app.core.errors import ProblemError
from app.modules.governance.service import record_audit
from app.modules.identity.models import NoticeAcknowledgement, Session, User, UserAccessRole
from app.modules.identity.security import new_session_token, session_id_for, verify_password
from app.modules.organization.models import JobRole, Organization

logger = logging.getLogger("app.identity")

NOTICE_TYPE = "privacy_ai_use"
# DEC-027: the notice text is not legally approved. Version and text are labelled draft.
NOTICE_VERSION = "privacy-ai-use-draft-0"
NOTICE_TEXT = (
    "DRAFT NOTICE - not legally reviewed. This platform records your assessment answers to estimate your "
    "competency levels for learning and development only. Estimates are calculated by fixed rules, not by AI, "
    "and are not an appraisal, promotion or eligibility decision. AI features (not used in this demo) answer only "
    "from cited documents. Your trainer and authorised administrators may see your results. You can ask for a "
    "result to be reviewed."
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def invalid_credentials() -> ProblemError:
    return ProblemError(401, "INVALID_CREDENTIALS", "Sign-in failed", "Email or password is incorrect.")


@dataclass(frozen=True)
class LoginResult:
    user: User
    session: Session
    token: str


def _find_login_user(db: DbSession, email: str, organization_code: str | None) -> User | None:
    query = select(User).join(Organization, Organization.id == User.organization_id).where(
        User.email == email, Organization.status == "active"
    )
    if organization_code:
        query = query.where(Organization.code == organization_code)
    users = db.scalars(query.limit(2)).all()
    # Without an organisation code, an email present in several organisations is ambiguous (DEC-047).
    return users[0] if len(users) == 1 else None


def login(db: DbSession, settings: Settings, email: str, password: str, organization_code: str | None) -> LoginResult:
    now = utcnow()
    user = _find_login_user(db, email, organization_code)
    if user is None:
        verify_password(None, password)  # equalise timing
        logger.warning("login_failed", extra={"reason": "unknown_or_ambiguous_account"})
        raise invalid_credentials()

    if user.locked_until is not None and user.locked_until > now:
        record_audit(db, organization_id=user.organization_id, action="auth.login.failure", target_type="user",
                     target_id=str(user.id), outcome="denied", reason="account_locked")
        db.commit()
        raise ProblemError(
            423, "ACCOUNT_LOCKED", "Account temporarily locked",
            "Too many failed sign-in attempts. Try again later or contact your administrator.",
            headers={"Retry-After": str(max(1, int((user.locked_until - now).total_seconds())))},
        )

    if not verify_password(user.password_hash, password) or user.status != "active":
        user.failed_login_count += 1
        record_audit(db, organization_id=user.organization_id, action="auth.login.failure", target_type="user",
                     target_id=str(user.id), outcome="failure")
        if user.failed_login_count >= settings.login_lockout_threshold:
            user.locked_until = now + timedelta(minutes=settings.login_lockout_minutes)
            user.failed_login_count = 0
            record_audit(db, organization_id=user.organization_id, action="auth.lockout", target_type="user",
                         target_id=str(user.id), outcome="success")
        db.commit()
        raise invalid_credentials()

    result = start_session(db, settings, user)
    record_audit(db, organization_id=user.organization_id, action="auth.login.success", target_type="user",
                 target_id=str(user.id), actor_user_id=user.id, actor_roles=access_roles(db, user))
    db.commit()
    return result


def start_session(db: DbSession, settings: Settings, user: User) -> LoginResult:
    """New server-side session for an authenticated user (login and registration). The caller commits."""
    now = utcnow()
    token = new_session_token()
    session = Session(
        id=session_id_for(token),
        organization_id=user.organization_id,
        user_id=user.id,
        last_seen_at=now,
        idle_expires_at=now + timedelta(minutes=settings.session_idle_timeout_minutes),
        absolute_expires_at=now + timedelta(hours=settings.session_absolute_timeout_hours),
    )
    session.idle_expires_at = min(session.idle_expires_at, session.absolute_expires_at)
    user.failed_login_count = 0
    user.locked_until = None
    user.last_login_at = now
    db.add(session)
    return LoginResult(user=user, session=session, token=token)


def resolve_session(db: DbSession, settings: Settings, token: str) -> tuple[Session, User] | None:
    now = utcnow()
    session = db.get(Session, session_id_for(token))
    if session is None or session.revoked_at is not None:
        return None
    if session.idle_expires_at <= now or session.absolute_expires_at <= now:
        return None
    user = db.get(User, session.user_id)
    if user is None or user.status != "active" or user.organization_id != session.organization_id:
        return None
    session.last_seen_at = now
    session.idle_expires_at = min(now + timedelta(minutes=settings.session_idle_timeout_minutes),
                                  session.absolute_expires_at)
    db.commit()
    return session, user


def logout(db: DbSession, session: Session, user: User) -> None:
    session.revoked_at = utcnow()
    record_audit(db, organization_id=user.organization_id, action="auth.logout", target_type="user",
                 target_id=str(user.id), actor_user_id=user.id, actor_roles=access_roles(db, user))
    db.commit()


def access_roles(db: DbSession, user: User) -> list[str]:
    return sorted(set(db.scalars(select(UserAccessRole.role).where(UserAccessRole.user_id == user.id))))


def notice_acknowledged(db: DbSession, user: User) -> datetime | None:
    return db.scalar(select(NoticeAcknowledgement.acknowledged_at).where(
        NoticeAcknowledgement.user_id == user.id,
        NoticeAcknowledgement.notice_type == NOTICE_TYPE,
        NoticeAcknowledgement.notice_version == NOTICE_VERSION,
    ))


def acknowledge_notice(db: DbSession, user: User, notice_version: str) -> datetime:
    if notice_version != NOTICE_VERSION:
        raise ProblemError(409, "NOTICE_VERSION_OUTDATED", "Notice version outdated",
                           "Reload the page to read the current notice.")
    existing = notice_acknowledged(db, user)
    if existing is not None:
        return existing
    now = utcnow()
    db.add(NoticeAcknowledgement(organization_id=user.organization_id, user_id=user.id, notice_type=NOTICE_TYPE,
                                 notice_version=NOTICE_VERSION, acknowledged_at=now))
    db.commit()
    return now


def active_job_role(db: DbSession, organization_id: uuid.UUID, job_role_id: uuid.UUID) -> JobRole:
    role = db.scalar(select(JobRole).where(JobRole.id == job_role_id, JobRole.organization_id == organization_id))
    if role is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Job role not found.")
    if role.status != "active":
        raise ProblemError(409, "JOB_ROLE_INACTIVE", "Job role unavailable", "This job role is no longer active.")
    return role


def select_job_role(db: DbSession, user: User, job_role_id: uuid.UUID) -> JobRole:
    role = active_job_role(db, user.organization_id, job_role_id)
    previous = user.job_role_id
    if previous != role.id:
        user.job_role_id = role.id
        record_audit(db, organization_id=user.organization_id, action="user.job_role.change", target_type="user",
                     target_id=str(user.id), actor_user_id=user.id, actor_roles=access_roles(db, user),
                     before={"job_role_id": str(previous) if previous else None}, after={"job_role_id": str(role.id)})
        db.commit()
    return role
