"""Catalogue tables: Course, CourseTopic, CourseCompetency (DATA_MODEL.md §8).

Recommendations and learning paths arrive in Phase 7. Mock iGOT courses are
served by the adapter at request time and are never stored here (DEC-014).
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, RowVersionMixin, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import ACTIVE_INACTIVE, DATA_STATUSES

# DEC-043: 'external_igot' (P1, real adapter only) is not allowed by the MVP schema.
COURSE_TYPES = ("internal", "nssta_programme_listing")
COURSE_REVIEW_STATUSES = ("unreviewed", "approved", "rejected")
MAPPING_STATUSES = ("suggested", "approved", "rejected")


class Course(StandardColumnsMixin, TenantMixin, RowVersionMixin, Base):
    __tablename__ = "courses"

    course_type: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    provider_organisation: Mapped[str] = mapped_column(Text, nullable=False)
    programme_family: Mapped[str | None] = mapped_column(Text)
    cohort: Mapped[str | None] = mapped_column(Text)
    target_group: Mapped[str | None] = mapped_column(Text)
    duration_days: Mapped[int | None] = mapped_column(Integer)
    batch_size_min: Mapped[int | None] = mapped_column(Integer)
    batch_size_max: Mapped[int | None] = mapped_column(Integer)
    venue: Mapped[str | None] = mapped_column(Text)
    fiscal_year: Mapped[str | None] = mapped_column(Text)
    schedule_status: Mapped[str | None] = mapped_column(Text)
    external_ref: Mapped[str | None] = mapped_column(Text)
    external_url: Mapped[str | None] = mapped_column(Text)  # only if verified; never fabricated
    source_record_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("source_records.id"))
    data_status: Mapped[str] = mapped_column(Text, nullable=False)
    review_status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'unreviewed'"))
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'active'"))

    __table_args__ = (
        CheckConstraint(check_in("course_type", COURSE_TYPES), name="course_type"),
        CheckConstraint(check_in("data_status", DATA_STATUSES), name="data_status"),
        CheckConstraint("data_status <> 'MOCK'", name="not_mock"),
        CheckConstraint(check_in("review_status", COURSE_REVIEW_STATUSES), name="review_status"),
        CheckConstraint(check_in("status", ACTIVE_INACTIVE), name="status"),
        CheckConstraint(
            "course_type <> 'nssta_programme_listing' OR source_record_id IS NOT NULL", name="listing_has_provenance"
        ),
        CheckConstraint("duration_days IS NULL OR duration_days > 0", name="duration_positive"),
        CheckConstraint(
            "batch_size_min IS NULL OR batch_size_max IS NULL OR batch_size_min <= batch_size_max",
            name="batch_size_order",
        ),
        Index("ix_courses_org_type_status", "organization_id", "course_type", "status"),
        UniqueConstraint("organization_id", "source_record_id"),
    )


class CourseTopic(StandardColumnsMixin, TenantMixin, Base):
    __tablename__ = "course_topics"

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    method: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'suggested'"))

    __table_args__ = (
        UniqueConstraint("course_id", "topic_id"),
        CheckConstraint(check_in("method", ("keyword_rule", "human")), name="method"),
        CheckConstraint(check_in("status", MAPPING_STATUSES), name="status"),
    )


class CourseCompetency(StandardColumnsMixin, TenantMixin, Base):
    """Human-approved course-to-competency mapping; only approved rows drive recommendations."""

    __tablename__ = "course_competencies"

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    competency_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("competencies.id"), nullable=False)
    relevance: Mapped[str] = mapped_column(Text, nullable=False)
    method: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'suggested'"))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("course_id", "competency_id"),
        CheckConstraint(check_in("relevance", ("primary", "secondary")), name="relevance"),
        CheckConstraint(check_in("method", ("human", "keyword_rule", "demo_seed")), name="method"),  # demo_seed: DEC-045
        CheckConstraint(check_in("status", MAPPING_STATUSES), name="status"),
        CheckConstraint(
            "status <> 'approved' OR (approved_by IS NOT NULL AND approved_at IS NOT NULL)", name="approval_recorded"
        ),
    )
