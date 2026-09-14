"""Organisation module tables: Organization, Department, JobRole (DATA_MODEL.md §4-5)."""

from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import ACTIVE_INACTIVE


class Organization(StandardColumnsMixin, Base):
    """Tenant root."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    settings_row_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))

    __table_args__ = (
        CheckConstraint(check_in("status", ACTIVE_INACTIVE), name="status"),
        CheckConstraint("code ~ '^[a-z0-9][a-z0-9-]{1,62}$'", name="code_slug"),
        Index("uq_organizations_lower_name", func.lower(text("name")), unique=True),
    )


class Department(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))

    __table_args__ = (
        CheckConstraint(check_in("status", ACTIVE_INACTIVE), name="status"),
        Index("uq_departments_org_lower_name", "organization_id", func.lower(text("name")), unique=True),
    )


class JobRole(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    """A statistical job role ("Role" in the product brief; DEC-012)."""

    __tablename__ = "job_roles"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    department_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("departments.id"))
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))

    __table_args__ = (
        CheckConstraint(check_in("status", ACTIVE_INACTIVE), name="status"),
        Index("uq_job_roles_org_lower_name", "organization_id", func.lower(text("name")), unique=True),
    )
