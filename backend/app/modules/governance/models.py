"""Governance module tables: AuditLog (DATA_MODEL.md §9).

Append-only: a database trigger (migration 0002) rejects UPDATE and DELETE.
Review tasks, approvals and correction requests arrive in Phase 4.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    ARRAY,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    SmallInteger,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in

AUDIT_OUTCOMES = ("success", "denied", "failure")


class AuditLog(TenantMixin, Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    actor_roles: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, server_default=text("'{}'"))
    action: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_id: Mapped[str | None] = mapped_column(Text)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)
    before: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    after: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    reason: Mapped[str | None] = mapped_column(Text)
    ip_hash: Mapped[str | None] = mapped_column(Text)
    correlation_id: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint(check_in("outcome", AUDIT_OUTCOMES), name="outcome"),
        CheckConstraint("action ~ '^[a-z_]+(\\.[a-z_]+)+$'", name="action_format"),
        Index("ix_audit_logs_org_occurred", "organization_id", "occurred_at"),
        Index("ix_audit_logs_actor_occurred", "actor_user_id", "occurred_at"),
        Index("ix_audit_logs_target", "target_type", "target_id"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_correlation", "correlation_id"),
    )


REVIEW_TASK_TYPES = ("question_version_review", "course_review")
REVIEW_TASK_STATUSES = ("open", "decided", "cancelled")
REVIEW_DECISIONS = ("approve", "reject", "request_changes")


class ReviewTask(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    """A unit of human review work (Phase 4C; DATA_MODEL.md ReviewTask). One open task per target."""

    __tablename__ = "review_tasks"

    task_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_type: Mapped[str] = mapped_column(Text, nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    target_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    title_snapshot: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'open'"))
    submitted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    eligible_capability: Mapped[str] = mapped_column(Text, nullable=False)
    required_decisions: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text("1"))
    policy_snapshot: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    submission_note: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(check_in("task_type", REVIEW_TASK_TYPES), name="task_type"),
        CheckConstraint(check_in("status", REVIEW_TASK_STATUSES), name="status"),
        CheckConstraint("required_decisions IN (1, 2)", name="required_decisions"),
        CheckConstraint("status <> 'decided' OR decided_at IS NOT NULL", name="decided_has_time"),
        Index("ix_review_tasks_org_status_type", "organization_id", "status", "task_type"),
        Index("uq_review_tasks_open_target", "target_type", "target_id", unique=True,
              postgresql_where=text("status = 'open'")),
    )


class Approval(TenantMixin, Base):
    """A human decision on a review task. Append-only (trigger). Authors cannot decide their own work (A-5)."""

    __tablename__ = "approvals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    review_task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("review_tasks.id"), nullable=False)
    sequence: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    reason_text: Mapped[str | None] = mapped_column(Text)
    decided_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    target_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    __table_args__ = (
        CheckConstraint(check_in("decision", REVIEW_DECISIONS), name="decision"),
        CheckConstraint("sequence IN (1, 2)", name="sequence"),
        CheckConstraint("decision = 'approve' OR reason_text IS NOT NULL", name="reason_required"),
        UniqueConstraint("review_task_id", "sequence"),
    )
