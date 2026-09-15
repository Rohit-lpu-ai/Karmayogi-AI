"""Learner recommendations (API_INTEGRATION_SPEC.md §2.3)."""

from __future__ import annotations

import uuid
from decimal import Decimal

from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.modules.competency.api import JobRoleItem
from app.modules.competency.api import CompetencyRef
from app.modules.identity.dependencies import SELF_LEARNING_ROLES, CurrentUser, get_current_user, require_any_role
from app.modules.recommendation import catalogue, service

router = APIRouter(prefix="/api/v1", tags=["recommendation"])


class CourseRef(BaseModel):
    id: uuid.UUID
    title: str
    course_type: str
    provider_organisation: str
    duration_days: int | None
    description: str | None
    difficulty: str | None = None
    learning_objectives: list[str] = []
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


# --- Catalogue (S-09) and course detail -----------------------------------------------------------------


class CourseCompetencyItem(BaseModel):
    competency: CompetencyRef
    relevance: str
    your_status: dict | None = None


class AddressedGap(BaseModel):
    competency_id: uuid.UUID
    competency_name: str
    required_level: int
    estimated_level: int | None
    gap: int | None


class CourseRecommendation(BaseModel):
    rank: int
    reasons: list[dict]


class CourseSummary(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    provider_organisation: str
    course_type: str
    duration_days: int | None
    difficulty: str | None
    learning_objectives: list[str]
    competencies: list[CourseCompetencyItem]
    recommendation: CourseRecommendation | None
    addresses_your_gaps: list[AddressedGap]
    is_demo: bool
    provenance: dict
    content_origin: str = "synthetic"
    lessons: dict = {}
    your_progress: dict | None = None


class CatalogueFilters(BaseModel):
    competencies: list[dict]
    difficulties: list[str]
    sorts: list[str]


class CatalogueResponse(BaseModel):
    items: list[CourseSummary]
    total: int
    filters: CatalogueFilters
    has_learning_context: bool


class RelatedCourse(BaseModel):
    id: uuid.UUID
    title: str
    difficulty: str | None
    duration_days: int | None
    is_demo: bool
    is_recommended: bool


class CourseDetail(CourseSummary):
    related_courses: list[RelatedCourse]
    learning_content: dict
    prerequisites: list[dict] = []
    completion_criteria: str | None = None


@router.get("/courses", operation_id="recommendation_list_courses", response_model=CatalogueResponse,
            responses={401: {"description": "Not signed in"}, 422: {"description": "Invalid filter"}})
def list_courses(
    q: str | None = Query(default=None, max_length=100),
    competency_id: uuid.UUID | None = None,
    difficulty: Literal["foundational", "intermediate", "advanced"] | None = None,
    max_days: int | None = Query(default=None, ge=1, le=365),
    sort: Literal["recommended", "title", "duration_asc", "duration_desc"] = "recommended",
    progress: Literal["not_started", "in_progress", "completed"] | None = None,
    current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db),
) -> CatalogueResponse:
    can_learn = bool(set(current.roles) & SELF_LEARNING_ROLES)
    return CatalogueResponse(**catalogue.list_courses(db, current.user, can_learn=can_learn, q=q, competency_id=competency_id,
                                                      difficulty=difficulty, max_days=max_days, sort=sort,
                                                      progress=progress))


@router.get("/courses/{course_id}", operation_id="recommendation_get_course", response_model=CourseDetail,
            responses={401: {"description": "Not signed in"}, 404: {"description": "Not available"}})
def get_course(course_id: uuid.UUID, current: CurrentUser = Depends(get_current_user),
               db: DbSession = Depends(get_db)) -> CourseDetail:
    can_learn = bool(set(current.roles) & SELF_LEARNING_ROLES)
    return CourseDetail(**catalogue.course_detail(db, current.user, course_id, can_learn=can_learn))
