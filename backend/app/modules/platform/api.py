"""Liveness and readiness probes (API_INTEGRATION_SPEC.md §2.1).

Both are unauthenticated and reveal no configuration or dependency details.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.core.db import check_database, get_engine
from app.core.errors import ProblemError

router = APIRouter(tags=["platform"])
logger = logging.getLogger("app.platform.health")


@router.get("/healthz", operation_id="platform_get_healthz", summary="Liveness probe")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/readyz",
    operation_id="platform_get_readyz",
    summary="Readiness probe (database reachable)",
    responses={503: {"description": "A required dependency is unavailable"}},
)
async def readyz(request: Request) -> JSONResponse:
    engine = request.app.state.engine_factory()
    if not await run_in_threadpool(check_database, engine):
        logger.warning("readiness_failed", extra={"dependency": "database"})
        raise ProblemError(503, "SERVICE_UNAVAILABLE", "Service unavailable", "The service is not ready.")
    return JSONResponse({"status": "ready"})


def default_engine_factory():
    return get_engine()
