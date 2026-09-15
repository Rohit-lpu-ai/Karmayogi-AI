"""Job roles, role requirements, competency profile and gaps (API_INTEGRATION_SPEC.md §2.3-2.5)."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.core.demo import is_demo_code
from app.modules.competency import service
from app.modules.identity.dependencies import SELF_LEARNING_ROLES, CurrentUser, get_current_user, require_any_role
from app.modules.organization.models import JobRole

router = APIRouter(prefix="/api/v1", tags=["competency"])
_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "Not permitted"}}


class CompetencyRef(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    framework_code: str
    framework_status: str
    description: str | None = None
    is_demo: bool


class JobRoleItem(BaseModel):
    id: uuid.UUID
    name: str
    code: str | None
    description: str | None
    is_demo: bool


class LevelItem(BaseModel):
    level_number: int
    label: str
    description: str | None = None
    min_score: Decimal | None
    threshold_status: str


class RequirementItem(BaseModel):
    competency: CompetencyRef
    required_level: int
    mapping_version: int
    levels: list[LevelItem]


class JobRoleCompetencies(BaseModel):
    job_role: JobRoleItem
    requirements: list[RequirementItem]


class GapItem(BaseModel):
    competency: CompetencyRef
    required_level: int
    estimated_level: int | None
    score: Decimal | None
    evidence_band: str | None
    evidence_count: int
    status: str
    gap: int | None
    max_level_span: int


class GapsResponse(BaseModel):
    job_role: JobRoleItem
    method_version: str
    gap_rule: str
    items: list[GapItem]
    summary: dict[str, int]


class ProfileItem(BaseModel):
    competency: CompetencyRef
    score: Decimal | None
    level_number: int | None
    evidence_band: str
    evidence_count: int
    method_version: str
    computed_at: datetime
    explanation: dict


class ProfileResponse(BaseModel):
    method_version: str
    items: list[ProfileItem]


def _job_role_item(role: JobRole) -> JobRoleItem:
    return JobRoleItem(id=role.id, name=role.name, code=role.code, description=role.description,
                       is_demo=is_demo_code(role.code))


@router.get("/job-roles", operation_id="organization_list_job_roles", response_model=list[JobRoleItem], responses=_ERRORS)
def list_job_roles(current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db)) -> list[JobRoleItem]:
    roles = db.scalars(select(JobRole).where(JobRole.organization_id == current.user.organization_id,
                                             JobRole.status == "active").order_by(JobRole.name)).all()
    return [_job_role_item(r) for r in roles]


@router.get(
    "/job-roles/{job_role_id}/competencies", operation_id="organization_get_job_role_competencies",
    response_model=JobRoleCompetencies, responses={**_ERRORS, 404: {"description": "Job role not found"}},
)
def job_role_competencies(
    job_role_id: uuid.UUID, current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db)
) -> JobRoleCompetencies:
    role = service.job_role_in_org(db, current.user.organization_id, job_role_id)
    requirements = service.role_requirements(db, current.user.organization_id, role.id)
    return JobRoleCompetencies(
        job_role=_job_role_item(role),
        requirements=[
            RequirementItem(
                competency=CompetencyRef(**service.competency_ref(r.competency, r.framework)),
                required_level=r.mapping.required_level_number,
                mapping_version=r.mapping.mapping_version,
                levels=[LevelItem(level_number=lvl.level_number, label=lvl.label, description=lvl.description,
                                  min_score=lvl.min_score, threshold_status=lvl.threshold_status) for lvl in r.levels],
            )
            for r in requirements
        ],
    )


@router.get("/me/competency-profile", operation_id="competency_get_my_profile", response_model=ProfileResponse,
            responses=_ERRORS)
def my_profile(
    current: CurrentUser = Depends(require_any_role(SELF_LEARNING_ROLES)), db: DbSession = Depends(get_db)
) -> ProfileResponse:
    return ProfileResponse(**service.competency_profile(db, current.user))


@router.get("/me/competency-gaps", operation_id="competency_get_my_gaps", response_model=GapsResponse,
            responses={**_ERRORS, 409: {"description": "No job role selected"}})
def my_gaps(
    current: CurrentUser = Depends(require_any_role(SELF_LEARNING_ROLES)), db: DbSession = Depends(get_db)
) -> GapsResponse:
    return GapsResponse(**service.competency_gaps(db, current.user))
