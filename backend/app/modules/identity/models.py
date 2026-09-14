"""Identity module tables: User, UserAccessRole (DATA_MODEL.md §4).

Session and NoticeAcknowledgement were added in vertical slice 1 (migration 0003).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import CITEXT, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import ACCESS_ROLES

USER_STATUSES = ("invited", "active", "locked", "inactive")
LOCALES = ("en", "hi")  # "hi" is P1; the API accepts only "en" in MVP (MVP-03).


class User(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(CITEXT, nullable=False)  # PD
    display_name: Mapped[str] = mapped_column(Text, nullable=False)  # PD
    designation: Mapped[str | None] = mapped_column(Text)  # PD
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))
    job_role_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("job_roles.id"))
    locale: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'en'"))
    password_hash: Mapped[str | None] = mapped_column(Text)  # Argon2id (Phase 3); never serialised
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'invited'"))
    failed_login_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    onboarding_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))

    __table_args__ = (
        CheckConstraint(check_in("status", USER_STATUSES), name="status"),
        CheckConstraint(check_in("locale", LOCALES), name="locale"),
        CheckConstraint("failed_login_count >= 0", name="failed_login_count_non_negative"),
        Index("uq_users_org_email", "organization_id", "email", unique=True),
        Index("ix_users_org_department", "organization_id", "department_id"),
        Index("ix_users_org_job_role", "organization_id", "job_role_id"),
    )


class UserAccessRole(StandardColumnsMixin, TenantMixin, Base):
    """RBAC assignment. Access roles, not job roles (DEC-012)."""

    __tablename__ = "user_access_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    department_scope_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))

    __table_args__ = (
        CheckConstraint(check_in("role", ACCESS_ROLES), name="role"),
        CheckConstraint(
            "role <> 'department_admin' OR department_scope_id IS NOT NULL", name="department_admin_requires_scope"
        ),
        Index(
            "uq_user_access_roles_user_role_scope",
            "user_id",
            "role",
            text("coalesce(department_scope_id, '00000000-0000-0000-0000-000000000000'::uuid)"),
            unique=True,
        ),
    )


class Session(TenantMixin, Base):
    """Server-side session (DEC-007). The primary key is the SHA-256 of the raw token; the token is never stored."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    idle_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    absolute_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reauthenticated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ip_hash: Mapped[str | None] = mapped_column(Text)  # PD; not collected in this slice
    user_agent: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("id ~ '^[0-9a-f]{64}$'", name="id_is_sha256"),
        CheckConstraint("idle_expires_at <= absolute_expires_at", name="idle_within_absolute"),
    )


NOTICE_TYPES = ("privacy_ai_use",)


class NoticeAcknowledgement(TenantMixin, Base):
    """Append-only record that a user acknowledged a notice version (MVP-03)."""

    __tablename__ = "notice_acknowledgements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    notice_type: Mapped[str] = mapped_column(Text, nullable=False)
    notice_version: Mapped[str] = mapped_column(Text, nullable=False)
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        CheckConstraint(check_in("notice_type", NOTICE_TYPES), name="notice_type"),
        UniqueConstraint("user_id", "notice_type", "notice_version"),
    )
