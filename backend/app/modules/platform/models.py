"""Platform module tables: Topic (DATA_MODEL.md §5). Settings and flags arrive later."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, Text, UniqueConstraint, text
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
