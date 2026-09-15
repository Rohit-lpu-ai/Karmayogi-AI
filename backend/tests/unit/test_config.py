import pytest
from pydantic import ValidationError

from app.core.config import AppEnv, Settings
from tests.conftest import make_settings


def test_database_url_is_secret():
    settings = make_settings(database_url="postgresql+psycopg://u:s3cr3t-value@h:5433/db")
    assert "s3cr3t-value" not in repr(settings)
    assert "s3cr3t-value" not in str(settings.model_dump())


def test_non_postgres_database_rejected():
    with pytest.raises(ValidationError):
        make_settings(database_url="sqlite:///x.db")


def test_invalid_app_env_rejected():
    with pytest.raises(ValidationError):
        make_settings(app_env="dev")


def test_invalid_log_level_rejected():
    with pytest.raises(ValidationError):
        make_settings(log_level="LOUD")


def test_igot_mode_validated():
    assert make_settings(igot_client_mode=" MOCK ").igot_client_mode == "mock"
    with pytest.raises(ValidationError):
        make_settings(igot_client_mode="real")


@pytest.mark.parametrize(
    "env,public",
    [(AppEnv.local, True), (AppEnv.ci, True), (AppEnv.staging, False), (AppEnv.pilot, False), (AppEnv.production, False)],
)
def test_openapi_public_only_in_local_and_ci(env, public):
    assert make_settings(app_env=env).openapi_public is public


def test_database_url_required(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
