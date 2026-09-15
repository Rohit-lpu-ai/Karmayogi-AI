"""Application factory for the api process (SYSTEM_ARCHITECTURE.md §3)."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI
from sqlalchemy.engine import Engine

from app.core.config import Settings, get_settings
from app.core.errors import install_error_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.modules.assessment import api as assessment_api
from app.modules.competency import api as competency_api
import app.models  # noqa: F401 - register every mapper so cross-module foreign keys resolve at runtime
from app.modules.identity import admin_api as identity_admin_api
from app.modules.identity import api as identity_api
from app.modules.learning import api as learning_api
from app.modules.content_admin import api as content_admin_api
from app.modules.insight import api as insight_api
from app.modules.platform import api as platform_api
from app.modules.recommendation import api as recommendation_api

API_PREFIX = "/api/v1"


def create_app(settings: Settings | None = None, engine_factory: Callable[[], Engine] | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Competency intelligence and learning platform API",
        version="0.1.0",
        # DEC-030: OpenAPI public only in local/ci. Interactive docs UIs are not served (CSP default-src 'none').
        openapi_url=f"{API_PREFIX}/openapi.json" if settings.openapi_public else None,
        docs_url=None,
        redoc_url=None,
    )
    app.state.settings = settings
    app.state.engine_factory = engine_factory or platform_api.default_engine_factory

    install_error_handlers(app)
    app.add_middleware(RequestContextMiddleware)
    app.include_router(platform_api.router)
    app.include_router(identity_api.router)
    app.include_router(identity_admin_api.router)
    app.include_router(competency_api.router)
    app.include_router(assessment_api.router)
    app.include_router(recommendation_api.router)
    app.include_router(learning_api.router)
    app.include_router(content_admin_api.router)
    app.include_router(insight_api.router)
    return app


def app_factory() -> FastAPI:
    """Entry point for ``uvicorn --factory app.main:app_factory``."""
    return create_app()
