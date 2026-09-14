"""Enable PostgreSQL extensions required by the data model.

pgcrypto provides gen_random_uuid() for UUID primary keys; citext provides
case-insensitive email columns (DATA_MODEL.md §12). The vector extension is
added in Phase 5 with the first embedding table (DEC-038).

Revision ID: 0001
Revises:
Create Date: 2026-09-14
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS citext")
    op.execute("DROP EXTENSION IF EXISTS pgcrypto")
