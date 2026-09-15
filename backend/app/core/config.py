"""Typed application settings, validated at startup.

Values come from environment variables, or from the repository-root ``.env``
file in local development. Secrets are held as ``SecretStr`` so they never
appear in reprs, logs or error messages.
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class AppEnv(str, Enum):
    local = "local"
    ci = "ci"
    staging = "staging"
    pilot = "pilot"
    production = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: AppEnv = AppEnv.local
    log_level: str = "INFO"
    database_url: SecretStr = Field(..., description="SQLAlchemy URL, e.g. postgresql+psycopg://user:pass@host:5433/db")
    database_connect_timeout_s: int = Field(default=3, ge=1, le=30)
    database_pool_size: int = Field(default=5, ge=1, le=50)

    # Existing variable from Phase 1 (.env.example). "live" is refused by the iGOT client factory.
    igot_client_mode: str = "mock"

    # Sessions (SECURITY_RESPONSIBLE_AI.md §3; DEC-007, DEC-047).
    session_secret: SecretStr = Field(..., description="Random secret (>= 32 chars) used to derive CSRF tokens")
    session_cookie_name: str = "platform_session"
    session_cookie_secure: bool = True
    session_idle_timeout_minutes: int = Field(default=30, ge=5, le=240)
    session_absolute_timeout_hours: int = Field(default=12, ge=1, le=24)
    login_lockout_threshold: int = Field(default=5, ge=3, le=20)
    login_lockout_minutes: int = Field(default=15, ge=1, le=240)

    # Only used by the seed command for synthetic demo users (local/ci/staging).
    demo_user_password: SecretStr | None = None

    # Learner self-registration (Phase 4, assumption A-1 / D4-1). MVP-01 excludes self-registration, so it is
    # allowed only in local and ci; unset means "on in local/ci, off elsewhere".
    learner_self_registration_enabled: bool | None = None
    password_token_ttl_hours: int = Field(default=24, ge=1, le=168)

    @field_validator("session_secret")
    @classmethod
    def _strong_session_secret(cls, value: SecretStr) -> SecretStr:
        if len(value.get_secret_value()) < 32:
            raise ValueError("SESSION_SECRET must be at least 32 characters")
        return value

    @model_validator(mode="after")
    def _secure_cookies_outside_development(self) -> "Settings":
        if not self.session_cookie_secure and self.app_env not in (AppEnv.local, AppEnv.ci):
            raise ValueError("SESSION_COOKIE_SECURE=false is only allowed in local and ci")
        return self

    @model_validator(mode="after")
    def _self_registration_only_in_development(self) -> "Settings":
        if self.learner_self_registration_enabled and self.app_env not in (AppEnv.local, AppEnv.ci):
            raise ValueError("LEARNER_SELF_REGISTRATION_ENABLED=true is only allowed in local and ci (D4-1)")
        return self

    @property
    def self_registration_enabled(self) -> bool:
        if self.learner_self_registration_enabled is None:
            return self.app_env in (AppEnv.local, AppEnv.ci)
        return self.learner_self_registration_enabled

    @field_validator("log_level")
    @classmethod
    def _valid_log_level(cls, value: str) -> str:
        level = value.upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError(f"invalid log level {value!r}")
        return level

    @field_validator("database_url")
    @classmethod
    def _postgres_only(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().startswith("postgresql"):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL")
        return value

    @field_validator("igot_client_mode")
    @classmethod
    def _valid_igot_mode(cls, value: str) -> str:
        mode = value.strip().lower()
        if mode not in {"mock", "live"}:
            raise ValueError("IGOT_CLIENT_MODE must be 'mock' or 'live'")
        return mode

    @property
    def openapi_public(self) -> bool:
        """DEC-030: the OpenAPI document is public only in local development."""
        return self.app_env in (AppEnv.local, AppEnv.ci)


@lru_cache
def get_settings() -> Settings:
    return Settings()
