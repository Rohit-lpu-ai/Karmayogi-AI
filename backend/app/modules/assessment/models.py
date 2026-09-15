"""Assessment module tables (DATA_MODEL.md §6), added in vertical slice 1 (migration 0003).

Columns that reference tables from later phases are omitted until then (DEC-046):
``questions.generation_job_id``; ``question_versions.ai_interaction_id``,
``prompt_template_version_id``, ``model_id``, ``generation_parameters``, ``stem_embedding``.
Append-only tables (question versions, options, delivered questions) are protected by triggers.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    ARRAY,
    BigInteger,
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
    text as sql_text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in

# 'demo_seed' marks synthetic items created by the local demo seed (DEC-046); never reviewed content.
QUESTION_ORIGINS = ("ai_generated", "human_authored", "demo_seed")
# "draft": a human author's unsubmitted work (Phase 4C, migration 0008).
QUESTION_STATUSES = (
    "draft", "pending_validation", "failed_validation", "validation_incomplete", "in_review",
    "approved", "rejected", "suspended", "retired",
)
DIFFICULTIES = ("foundational", "intermediate", "advanced")
ASSESSMENT_PURPOSES = ("pre", "practice", "topic", "competency")  # 'post' is P1, 'certification' P2
FEEDBACK_POLICIES = ("score_only", "correctness", "correctness_and_explanations")
ASSESSMENT_STATUSES = ("draft", "published", "retired")
# "voided": withdrawn by a local/ci demo reset (DEC-052); the row and its evidence are kept, never deleted.
ATTEMPT_STATUSES = ("in_progress", "submitted", "scored", "scoring_failed", "expired", "voided")


class Question(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "questions"

    origin: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=sql_text("'pending_validation'"))
    current_version_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id", use_alter=True)
    )
    approved_version_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id", use_alter=True)
    )

    __table_args__ = (
        CheckConstraint(check_in("origin", QUESTION_ORIGINS), name="origin"),
        CheckConstraint(check_in("status", QUESTION_STATUSES), name="status"),
        CheckConstraint("status <> 'approved' OR approved_version_id IS NOT NULL", name="approved_has_version"),
        Index("ix_questions_org_status", "organization_id", "status"),
    )


class QuestionVersion(TenantMixin, Base):
    """Immutable question content."""

    __tablename__ = "question_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=sql_text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    question_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_type: Mapped[str] = mapped_column(Text, nullable=False, server_default=sql_text("'mcq_single'"))
    stem: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sql_text("false"))
    competency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    topic_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"))
    content_hash: Mapped[str] = mapped_column(Text, nullable=False)
    edited_from_version_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id"))
    human_edited_fields: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False, server_default=sql_text("'{}'"))
    language: Mapped[str] = mapped_column(Text, nullable=False, server_default=sql_text("'en'"))

    __table_args__ = (
        UniqueConstraint("question_id", "version_number"),
        CheckConstraint("question_type = 'mcq_single'", name="question_type"),
        CheckConstraint(check_in("difficulty", DIFFICULTIES), name="difficulty"),
        CheckConstraint("language = 'en'", name="language"),
        CheckConstraint("content_hash ~ '^[0-9a-f]{64}$'", name="content_hash_format"),
        Index("ix_question_versions_org_content_hash", "organization_id", "content_hash"),
        Index("ix_question_versions_competency_difficulty", "competency_id", "difficulty"),
    )


class QuestionOption(TenantMixin, Base):
    __tablename__ = "question_options"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=sql_text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    question_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id"), nullable=False
    )
    label: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)  # never serialised to learners before submission
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint("question_version_id", "label"),
        CheckConstraint(check_in("label", ("A", "B", "C", "D")), name="label"),
        Index("uq_question_options_one_correct", "question_version_id", unique=True, postgresql_where=sql_text("is_correct")),
    )


class Assessment(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "assessments"

    title: Mapped[str] = mapped_column(Text, nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    job_role_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("job_roles.id"))
    blueprint: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    feedback_policy: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=sql_text("'draft'"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))

    __table_args__ = (
        CheckConstraint(check_in("purpose", ASSESSMENT_PURPOSES), name="purpose"),
        CheckConstraint(check_in("feedback_policy", FEEDBACK_POLICIES), name="feedback_policy"),
        CheckConstraint(check_in("status", ASSESSMENT_STATUSES), name="status"),
        CheckConstraint("purpose <> 'pre' OR job_role_id IS NOT NULL", name="pre_requires_job_role"),
        CheckConstraint("status <> 'published' OR published_at IS NOT NULL", name="published_has_time"),
        Index("ix_assessments_org_status", "organization_id", "status"),
        Index(
            "uq_assessments_one_published_pre_per_role", "job_role_id", unique=True,
            postgresql_where=sql_text("purpose = 'pre' AND status = 'published'"),
        ),
    )


class AssessmentQuestion(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "assessment_questions"

    assessment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    question_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id"), nullable=False
    )

    __table_args__ = (UniqueConstraint("assessment_id", "question_version_id"),)


class AssessmentAttempt(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "assessment_attempts"

    assessment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=sql_text("'in_progress'"))
    seed: Mapped[int] = mapped_column(BigInteger, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    score_total: Mapped[Decimal | None] = mapped_column(Numeric(6, 5))
    is_baseline: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=sql_text("false"))
    rescored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    voided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    void_reason: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(check_in("status", ATTEMPT_STATUSES), name="status"),
        CheckConstraint("(status = 'voided') = (voided_at IS NOT NULL AND void_reason IS NOT NULL)", name="voided_complete"),
        CheckConstraint("score_total IS NULL OR (score_total >= 0 AND score_total <= 1)", name="score_total_range"),
        CheckConstraint("status <> 'scored' OR (scored_at IS NOT NULL AND score_total IS NOT NULL)", name="scored_complete"),
        Index("ix_assessment_attempts_user_assessment", "user_id", "assessment_id"),
        Index(
            "uq_assessment_attempts_one_baseline", "user_id", unique=True,
            postgresql_where=sql_text("is_baseline AND status <> 'voided'"),
        ),
        Index(
            "uq_assessment_attempts_one_open", "user_id", "assessment_id", unique=True,
            postgresql_where=sql_text("status = 'in_progress'"),
        ),
    )


class AttemptQuestion(TenantMixin, Base):
    """Exact questions, order and option order delivered in an attempt (append-only)."""

    __tablename__ = "attempt_questions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=sql_text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assessment_attempts.id"), nullable=False)
    question_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id"), nullable=False
    )
    position: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    option_order: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)

    __table_args__ = (
        UniqueConstraint("attempt_id", "position"),
        UniqueConstraint("attempt_id", "question_version_id"),
    )


class Answer(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "answers"

    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assessment_attempts.id"), nullable=False)
    question_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("question_versions.id"), nullable=False
    )
    selected_option_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("question_options.id"))
    answered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_correct: Mapped[bool | None] = mapped_column(Boolean)
    scored_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rescore_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=sql_text("0"))

    __table_args__ = (UniqueConstraint("attempt_id", "question_version_id"),)


SOURCE_KINDS = ("synthetic", "source_record", "external_reference")


class QuestionSourceReference(TenantMixin, Base):
    """Where a question version's content comes from (Phase 4C, plan K-6). Append-only with its version.

    - ``synthetic``: invented for practice; ``note`` must say so. Never presented as a citation.
    - ``source_record``: points to an imported source record (reference only until its review is verified).
    - ``external_reference``: title and publisher given by the author; shown as "author-provided, not verified".
    """

    __tablename__ = "question_source_references"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=sql_text("gen_random_uuid()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    question_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question_versions.id"),
                                                           nullable=False, index=True)
    source_kind: Mapped[str] = mapped_column(Text, nullable=False)
    source_record_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("source_records.id"))
    title: Mapped[str | None] = mapped_column(Text)
    publisher: Mapped[str | None] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(Text)
    locator: Mapped[str | None] = mapped_column(Text)
    note: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(check_in("source_kind", SOURCE_KINDS), name="source_kind"),
        CheckConstraint("source_kind <> 'source_record' OR source_record_id IS NOT NULL", name="record_has_id"),
        CheckConstraint("source_kind <> 'external_reference' OR (title IS NOT NULL AND publisher IS NOT NULL)",
                        name="external_has_title_publisher"),
        CheckConstraint("source_kind <> 'synthetic' OR note IS NOT NULL", name="synthetic_has_note"),
        CheckConstraint("url IS NULL OR url ~ '^https?://'", name="url_scheme"),
    )
