"""Migrations apply cleanly, round-trip, and match the SQLAlchemy models."""

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

import app.models  # noqa: F401
from app.core.db import Base
from app.main import create_app
from tests.conftest import alembic_config, is_test_database, make_settings

pytestmark = pytest.mark.db


def test_single_migration_head(test_database_url):
    assert len(ScriptDirectory.from_config(alembic_config(test_database_url)).get_heads()) == 1


def test_upgrade_creates_required_extensions(migrated_engine):
    with migrated_engine.connect() as conn:
        extensions = set(conn.execute(text("SELECT extname FROM pg_extension")).scalars())
        assert {"pgcrypto", "citext"} <= extensions
        assert "vector" not in extensions  # DEC-038: not before Phase 5
        assert conn.execute(text("SELECT gen_random_uuid() IS NOT NULL")).scalar()


def test_models_and_migrations_in_sync(migrated_engine):
    with migrated_engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn, opts={"compare_type": True}), Base.metadata)
    assert diff == [], f"Models differ from migrations: {diff}"


def test_downgrade_to_base_then_upgrade_again(test_database_url, migrated_engine):
    config = alembic_config(test_database_url)
    command.downgrade(config, "base")
    with migrated_engine.connect() as conn:
        tables = set(conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")).scalars())
    assert tables <= {"alembic_version"}
    command.upgrade(config, "head")


def test_readyz_ok_with_database(test_database_url):
    engine = create_engine(test_database_url)
    try:
        app = create_app(make_settings(database_url=test_database_url), engine_factory=lambda: engine)
        with TestClient(app) as client:
            response = client.get("/readyz")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}
    finally:
        engine.dispose()


def test_destructive_fixture_guard():
    assert is_test_database("postgresql+psycopg://u:p@h/platform_test")
    assert not is_test_database("postgresql+psycopg://u:p@h/platform")
