"""Platform module tables: Topic (DATA_MODEL.md §5) and SeedPackApplication (DEC-052). Settings and flags arrive later."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, StandardColumnsMixin, TenantMixin, check_in
from app.core.vocab import DATA_STATUSES

TOPIC_REVIEW_STATUSES = ("unreviewed", "approved", "retired")


class Topic(StandardColumnsMixin, TenantMixin, Base):
    """Taxonomy term. Seeded terms are ASSUMED and unreviewed until a human reviews them."""

    __tablename__ = "topics"

    code: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    taxonomy_version: Mapped[str] = mapped_column(Text, nullable=False)
    data_status: Mapped[str] = mapped_column(Text, nullable=False)
    review_status: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'unreviewed'"))

    __table_args__ = (
        UniqueConstraint("organization_id", "code"),
        CheckConstraint(check_in("data_status", DATA_STATUSES), name="data_status"),
        CheckConstraint("data_status <> 'MOCK'", name="not_mock"),
        CheckConstraint(check_in("review_status", TOPIC_REVIEW_STATUSES), name="review_status"),
    )


class SeedPackApplication(StandardColumnsMixin, TenantMixin, Base):
    """Which versioned seed pack has been applied to an organisation (DEC-052).

    One row per (organisation, pack code). Applying a newer version of the same pack updates
    ``pack_version``; different packs (``demo-1``, ``demo-2``) are independent rows.
    """

    __tablename__ = "seed_pack_applications"

    pack_code: Mapped[str] = mapped_column(Text, nullable=False)
    pack_version: Mapped[int] = mapped_column(nullable=False)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    summary: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))

    __table_args__ = (
        UniqueConstraint("organization_id", "pack_code"),
        CheckConstraint("pack_code ~ '^[a-z0-9][a-z0-9-]*$'", name="pack_code_format"),
        CheckConstraint("pack_version >= 1", name="pack_version_positive"),
    )
