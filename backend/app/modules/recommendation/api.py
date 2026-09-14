"""Learner recommendations (API_INTEGRATION_SPEC.md §2.3)."""

from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.modules.competency.api import JobRoleItem
from app.modules.identity.dependencies import SELF_LEARNING_ROLES, CurrentUser, require_any_role
from app.modules.recommendation import service

router = APIRouter(prefix="/api/v1", tags=["recommendation"])


class CourseRef(BaseModel):
    id: uuid.UUID
    title: str
    course_type: str
    provider_organisation: str
    duration_days: int | None
    description: str | None
    is_demo: bool


class RecommendationItem(BaseModel):
    rank: int
    course: CourseRef
    score: Decimal
    reasons: list[dict]
    provenance: dict


class RecommendationsResponse(BaseModel):
    rule_version: str
    rule: str
    job_role: JobRoleItem
    items: list[RecommendationItem]
    gaps_without_approved_content: list[str]
    igot: dict


@router.get(
    "/me/recommendations", operation_id="recommendation_get_my_recommendations", response_model=RecommendationsResponse,
    responses={401: {"description": "Not signed in"}, 403: {"description": "Not permitted"},
               409: {"description": "No job role selected"}},
)
def my_recommendations(
    current: CurrentUser = Depends(require_any_role(SELF_LEARNING_ROLES)), db: DbSession = Depends(get_db)
) -> RecommendationsResponse:
    return RecommendationsResponse(**service.recommendations(db, current.user))
