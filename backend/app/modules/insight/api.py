"""Aggregated insight routes (Phase 4D). Capability ``insight.view``; aggregates only, small groups withheld."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.modules.identity.dependencies import CurrentUser, require_capability
from app.modules.insight import service

router = APIRouter(prefix="/api/v1/admin/insight", tags=["insight"])
_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "Not permitted"}}
viewer = require_capability("insight.view")


@router.get("/summary", operation_id="insight_summary", responses=_ERRORS)
def summary(current: CurrentUser = Depends(viewer), db: DbSession = Depends(get_db)) -> dict:
    return service.summary(db, current)


@router.get("/skill-gaps", operation_id="insight_skill_gaps", responses=_ERRORS)
def skill_gaps(job_role_id: uuid.UUID | None = None, current: CurrentUser = Depends(viewer), db: DbSession = Depends(get_db)) -> dict:
    return service.skill_gaps(db, current, job_role_id)


@router.get("/training-needs", operation_id="insight_training_needs", responses=_ERRORS)
def training_needs(current: CurrentUser = Depends(viewer), db: DbSession = Depends(get_db)) -> dict:
    return service.training_needs(db, current)
