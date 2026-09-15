"""Competency module reference tables (DATA_MODEL.md §5).

CompetencyFramework, CompetencyCluster, Competency, CompetencyLevel and
RoleCompetency. Estimates, snapshots and evidence arrive in Phase 4.

Cross-row rules enforced by database triggers (see migration 0002):
- a competency in a framework with restricted definitions has no description;
- ``min_score`` increases with ``level_number`` within a framework;
- a role mapping's required level exists in the competency's framework scale.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import ACTIVE_INACTIVE, DATA_STATUSES

FRAMEWORK_TYPES = ("reference_behavioural", "functional")
APPROVAL_STATUSES = ("draft", "approved", "retired")
THRESHOLD_STATUSES = ("provisional", "approved")


class CompetencyFramework(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "competency_frameworks"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    framework_type: Mapped[str] = mapped_column(Text, nullable=False)
    publisher: Mapped[str | None] = mapped_column(Text)
    version_label: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'draft'"))
    definitions_restricted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    source_record_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("source_records.id"))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(check_in("framework_type", FRAMEWORK_TYPES), name="framework_type"),
        CheckConstraint(check_in("status", APPROVAL_STATUSES), name="status"),
        CheckConstraint(
            "status <> 'approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)", name="approval_recorded"
        ),
        UniqueConstraint("organization_id", "code", "version_label"),
    )


class CompetencyCluster(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "competency_clusters"

    framework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("competency_frameworks.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    source_page: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("framework_id", "code"),
        CheckConstraint("source_page IS NULL OR source_page >= 1", name="source_page_positive"),
    )


class Competency(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "competencies"

    framework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("competency_frameworks.id"), nullable=False
    )
    cluster_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("competency_clusters.id"))
    code: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    name_variants: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, server_default=text("'{}'"))
    description: Mapped[str | None] = mapped_column(Text)
    definition_source_page: Mapped[int | None] = mapped_column(Integer)
    detail_source_page: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))
    data_status: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("framework_id", "code"),
        CheckConstraint(check_in("status", ACTIVE_INACTIVE), name="status"),
        CheckConstraint(check_in("data_status", DATA_STATUSES), name="data_status"),
        CheckConstraint("data_status <> 'MOCK'", name="not_mock"),
    )


class CompetencyLevel(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "competency_levels"

    framework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("competency_frameworks.id"), nullable=False
    )
    level_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    min_score: Mapped[Decimal | None] = mapped_column(Numeric(6, 5))
    threshold_status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'provisional'"))

    __table_args__ = (
        UniqueConstraint("framework_id", "level_number"),
        CheckConstraint("level_number >= 1", name="level_number_positive"),
        CheckConstraint("min_score IS NULL OR (min_score >= 0 AND min_score <= 1)", name="min_score_range"),
        CheckConstraint(check_in("threshold_status", THRESHOLD_STATUSES), name="threshold_status"),
    )


class RoleCompetency(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    """Required level of a competency for a job role. Unapproved mappings are never used."""

    __tablename__ = "role_competencies"

    job_role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("job_roles.id"), nullable=False)
    competency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    required_level_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    mapping_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'draft'"))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_critical: Mapped[bool | None] = mapped_column(Boolean)  # P1 column (CMP-005); no MVP behaviour

    __table_args__ = (
        UniqueConstraint("job_role_id", "competency_id", "mapping_version"),
        CheckConstraint(check_in("status", APPROVAL_STATUSES), name="status"),
        CheckConstraint(
            "status <> 'approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)", name="approval_recorded"
        ),
        Index(
            "uq_role_competencies_one_approved",
            "job_role_id",
            "competency_id",
            unique=True,
            postgresql_where=text("status = 'approved'"),
        ),
    )


EVIDENCE_BANDS = ("insufficient", "low", "medium", "high")
EVIDENCE_TYPES = ("assessment_answer", "human_adjustment")  # 'learning_activity' is P1


class UserCompetency(StandardColumnsMixin, TenantMixin, Base):
    """Current deterministic estimate for a user and competency (AI_SYSTEM_SPEC.md §25). No LLM is involved."""

    __tablename__ = "user_competencies"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    job_role_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("job_roles.id"))
    role_mapping_version: Mapped[int | None] = mapped_column(Integer)
    score: Mapped[Decimal | None] = mapped_column(Numeric(6, 5))
    level_number: Mapped[int | None] = mapped_column(SmallInteger)
    evidence_band: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_count: Mapped[int] = mapped_column(Integer, nullable=False)
    method_version: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    is_stale: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "competency_id"),
        CheckConstraint(check_in("evidence_band", EVIDENCE_BANDS), name="evidence_band"),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 1)", name="score_range"),
        CheckConstraint("evidence_count > 0 OR score IS NULL", name="no_score_without_evidence"),
        CheckConstraint("evidence_count >= 0", name="evidence_count_non_negative"),
    )


class CompetencyEvidence(TenantMixin, Base):
    """Append-only evidence ledger. Only the void columns may be set, once (trigger in migration 0003)."""

    __tablename__ = "competency_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    competency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(Text, nullable=False)
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("assessment_attempts.id"))
    answer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("answers.id"))
    question_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id"))
    difficulty_weight: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    adjusted_level_number: Mapped[int | None] = mapped_column(SmallInteger)
    reason: Mapped[str | None] = mapped_column(Text)
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    voided_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    void_reason: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(check_in("evidence_type", EVIDENCE_TYPES), name="evidence_type"),
        CheckConstraint(
            "evidence_type <> 'assessment_answer' OR (attempt_id IS NOT NULL AND answer_id IS NOT NULL "
            "AND question_version_id IS NOT NULL AND difficulty_weight IS NOT NULL AND is_correct IS NOT NULL)",
            name="answer_evidence_fields",
        ),
        CheckConstraint(
            "evidence_type <> 'human_adjustment' OR (adjusted_level_number IS NOT NULL AND reason IS NOT NULL "
            "AND created_by IS NOT NULL AND created_by <> user_id)",
            name="adjustment_fields",
        ),
        CheckConstraint("(voided_at IS NULL) = (void_reason IS NULL)", name="void_reason_with_void"),
        Index("ix_competency_evidence_active", "user_id", "competency_id", postgresql_where=text("voided_at IS NULL")),
        Index("ix_competency_evidence_answer", "answer_id"),
    )
