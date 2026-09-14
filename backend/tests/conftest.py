"""Shared fixtures.

Unit tests build settings explicitly and never read the developer's .env.
Database tests need TEST_DATABASE_URL (environment or repository .env) and
refuse to run against a database whose name does not end in ``_test``.
"""

from __future__ import annotations

import os
import uuid
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session

from app.core.config import REPO_ROOT, AppEnv, Settings
from app.main import create_app

BACKEND_ROOT = REPO_ROOT / "backend"
UNREACHABLE_DB = "postgresql+psycopg://nobody:nothing@127.0.0.1:1/none"


def make_settings(**overrides) -> Settings:
    values = {
        "app_env": AppEnv.ci,
        "database_url": UNREACHABLE_DB,
        "database_connect_timeout_s": 1,
        "session_secret": "test-session-secret-0123456789abcdef",
        "session_cookie_secure": False,
    }
    values.update(overrides)
    if values["app_env"] not in (AppEnv.local, AppEnv.ci, "local", "ci") and "session_cookie_secure" not in overrides:
        values["session_cookie_secure"] = True  # insecure cookies are refused outside local/ci
    return Settings(_env_file=None, **values)


@pytest.fixture
def settings() -> Settings:
    return make_settings()


@pytest.fixture
def unreachable_engine() -> Iterator[Engine]:
    engine = create_engine(UNREACHABLE_DB, connect_args={"connect_timeout": 1})
    yield engine
    engine.dispose()


@pytest.fixture
def client(settings: Settings, unreachable_engine: Engine) -> Iterator[TestClient]:
    app = create_app(settings, engine_factory=lambda: unreachable_engine)
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


# --- Database fixtures -------------------------------------------------------


def is_test_database(url: str) -> bool:
    return (make_url(url).database or "").endswith("_test")


@pytest.fixture(scope="session")
def test_database_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL") or dotenv_values(REPO_ROOT / ".env").get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not configured")
    if not is_test_database(url):
        pytest.fail("Refusing to run destructive tests: the test database name must end in '_test'")
    return url


def alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "migrations"))
    config.attributes["database_url"] = database_url
    config.attributes["configure_logger"] = False
    return config


def reset_schema(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))


@pytest.fixture(scope="session")
def migrated_engine(test_database_url: str) -> Iterator[Engine]:
    """The test database reset to an empty schema and migrated to head once per session."""
    engine = create_engine(test_database_url)
    reset_schema(engine)
    command.upgrade(alembic_config(test_database_url), "head")
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(migrated_engine: Engine) -> Iterator[Session]:
    """A session inside an outer transaction that is always rolled back.

    Code under test may call ``commit()``; with ``create_savepoint`` that only releases a savepoint.
    """
    connection = migrated_engine.connect()
    outer = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()
        outer.rollback()
        connection.close()


@pytest.fixture
def organization(db_session: Session):
    from app.modules.organization.models import Organization

    org = Organization(code=f"test-{uuid.uuid4().hex[:12]}", name=f"Test Organisation {uuid.uuid4().hex[:8]}")
    db_session.add(org)
    db_session.flush()
    return org
