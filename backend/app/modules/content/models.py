"""Content module tables: SourceRecord (DATA_MODEL.md §7).

LearningMaterial, Document and the processing tables arrive in Phase 5.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, CheckConstraint, Date, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import DATA_STATUSES


class SourceRecord(StandardColumnsMixin, TenantMixin, Base):
    """Provenance of anything imported from a canonical dataset. Mock data is never imported."""

    __tablename__ = "source_records"

    registry_source_id: Mapped[str] = mapped_column(Text, nullable=False)
    source_document_id: Mapped[str | None] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_organisation: Mapped[str] = mapped_column(Text, nullable=False)
    retrieval_date: Mapped[date | None] = mapped_column(Date)
    access_method: Mapped[str] = mapped_column(Text, nullable=False)
    source_sha256: Mapped[str | None] = mapped_column(Text)
    raw_local_path: Mapped[str | None] = mapped_column(Text)
    canonical_dataset: Mapped[str | None] = mapped_column(Text)
    canonical_record_id: Mapped[str | None] = mapped_column(Text)
    canonical_dataset_sha256: Mapped[str | None] = mapped_column(Text)
    data_status: Mapped[str] = mapped_column(Text, nullable=False)
    licence_status: Mapped[str] = mapped_column(Text, nullable=False)
    licence_notes: Mapped[str] = mapped_column(Text, nullable=False)
    attribution_text: Mapped[str] = mapped_column(Text, nullable=False)
    review_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))

    __table_args__ = (
        UniqueConstraint("organization_id", "canonical_dataset", "canonical_record_id"),
        CheckConstraint(check_in("data_status", DATA_STATUSES), name="data_status"),
        CheckConstraint(check_in("licence_status", DATA_STATUSES), name="licence_status"),
        CheckConstraint("data_status <> 'MOCK' AND licence_status <> 'MOCK'", name="not_mock"),
        CheckConstraint("source_sha256 IS NULL OR source_sha256 ~ '^[0-9a-f]{64}$'", name="source_sha256_format"),
        CheckConstraint(
            "canonical_dataset_sha256 IS NULL OR canonical_dataset_sha256 ~ '^[0-9a-f]{64}$'",
            name="canonical_dataset_sha256_format",
        ),
    )
