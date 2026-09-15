"""Assessment and attempt routes (API_INTEGRATION_SPEC.md §2.6).

Response models declare only key-free fields for delivery endpoints, so an
answer key cannot be serialised by accident (T-07).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.modules.assessment import service
from app.modules.competency.api import CompetencyRef
from app.modules.identity.dependencies import SELF_LEARNING_ROLES, CurrentUser, require_any_role

router = APIRouter(prefix="/api/v1", tags=["assessment"])

learner = require_any_role(SELF_LEARNING_ROLES)
learner_write = require_any_role(SELF_LEARNING_ROLES, csrf=True)

_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "CSRF or permission failure"},
           404: {"description": "Not found or not yours"}}


class LatestAttempt(BaseModel):
    id: uuid.UUID
    status: str


class AssessmentSummary(BaseModel):
    id: uuid.UUID
    title: str
    purpose: str
    feedback_policy: str
    question_count: int
    is_demo: bool
    latest_attempt: LatestAttempt | None


class AssessmentRef(BaseModel):
    id: uuid.UUID
    title: str
    purpose: str
    feedback_policy: str
    is_demo: bool


class DeliveredOption(BaseModel):
    id: uuid.UUID
    label: str
    text: str


class DeliveredQuestion(BaseModel):
    question_version_id: uuid.UUID
    position: int
    stem: str
    difficulty: str
    competency: CompetencyRef
    is_demo: bool
    options: list[DeliveredOption]
    selected_option_id: uuid.UUID | None


class AttemptResponse(BaseModel):
    id: uuid.UUID
    status: str
    started_at: datetime
    submitted_at: datetime | None
    assessment: AssessmentRef
    questions: list[DeliveredQuestion]
    answered_count: int
    question_count: int


class AnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    selected_option_id: uuid.UUID | None


class AnswerSaved(BaseModel):
    question_version_id: uuid.UUID
    selected_option_id: uuid.UUID | None
    saved_at: datetime


class SubmitResponse(BaseModel):
    attempt_id: uuid.UUID
    status: str
    score_total: Decimal
    is_baseline: bool
    result_url: str


class CompetencyResult(BaseModel):
    competency: CompetencyRef
    score: Decimal | None
    level_number: int | None
    evidence_band: str
    evidence_count: int
    thresholds_status: str
    method_version: str


class QuestionFeedback(BaseModel):
    question_version_id: uuid.UUID
    position: int
    stem: str
    competency_id: uuid.UUID
    selected_option_id: uuid.UUID | None
    is_correct: bool | None = None
    correct_option_id: uuid.UUID | None = None
    explanation: str | None = None


class ResultAssessmentRef(BaseModel):
    id: uuid.UUID
    title: str
    is_demo: bool


class AttemptResult(BaseModel):
    attempt_id: uuid.UUID
    status: str
    scored_at: datetime
    score_total: Decimal
    is_baseline: bool
    feedback_policy: str
    assessment: ResultAssessmentRef
    competencies: list[CompetencyResult]
    questions: list[QuestionFeedback]
    notice: str


class HistoryAssessmentRef(BaseModel):
    id: uuid.UUID
    title: str
    purpose: str
    is_demo: bool


class AttemptHistoryItem(BaseModel):
    id: uuid.UUID
    status: str
    started_at: datetime
    submitted_at: datetime | None
    scored_at: datetime | None
    score_total: Decimal | None
    is_baseline: bool
    assessment: HistoryAssessmentRef


@router.get("/me/attempts", operation_id="assessment_list_my_attempts", response_model=list[AttemptHistoryItem],
            responses=_ERRORS)
def my_attempts(current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> list[AttemptHistoryItem]:
    return [AttemptHistoryItem(**a) for a in service.attempt_history(db, current.user)]


@router.get("/assessments", operation_id="assessment_list_assessments", response_model=list[AssessmentSummary],
            responses=_ERRORS)
def list_assessments(current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> list[AssessmentSummary]:
    return [AssessmentSummary(**a) for a in service.available_assessments(db, current.user)]


@router.post(
    "/assessments/{assessment_id}/attempts", operation_id="assessment_start_attempt", response_model=AttemptResponse,
    status_code=201,
    responses={**_ERRORS, 200: {"description": "Existing in-progress attempt resumed"},
               409: {"description": "Notice, job role or completion precondition not met"}},
)
def start_attempt(
    assessment_id: uuid.UUID, response: Response, current: CurrentUser = Depends(learner_write),
    db: DbSession = Depends(get_db),
) -> AttemptResponse:
    attempt, created = service.start_or_resume(db, current.user, assessment_id)
    response.status_code = 201 if created else 200
    return AttemptResponse(**service.attempt_view(db, current.user, attempt.id))


@router.get("/attempts/{attempt_id}", operation_id="assessment_get_attempt", response_model=AttemptResponse,
            responses=_ERRORS)
def get_attempt(attempt_id: uuid.UUID, current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> AttemptResponse:
    return AttemptResponse(**service.attempt_view(db, current.user, attempt_id))


@router.put(
    "/attempts/{attempt_id}/answers/{question_version_id}", operation_id="assessment_save_answer",
    response_model=AnswerSaved,
    responses={**_ERRORS, 409: {"description": "Attempt already submitted"}, 422: {"description": "Invalid option"}},
)
def save_answer(
    attempt_id: uuid.UUID, question_version_id: uuid.UUID, body: AnswerRequest,
    current: CurrentUser = Depends(learner_write), db: DbSession = Depends(get_db),
) -> AnswerSaved:
    return AnswerSaved(**service.save_answer(db, current.user, attempt_id, question_version_id, body.selected_option_id))


@router.post(
    "/attempts/{attempt_id}/submit", operation_id="assessment_submit_attempt", response_model=SubmitResponse,
    responses={**_ERRORS, 409: {"description": "Attempt already submitted"}},
)
def submit_attempt(
    attempt_id: uuid.UUID, current: CurrentUser = Depends(learner_write), db: DbSession = Depends(get_db)
) -> SubmitResponse:
    attempt = service.submit(db, current.user, attempt_id, sorted(current.roles))
    return SubmitResponse(attempt_id=attempt.id, status=attempt.status, score_total=attempt.score_total,
                          is_baseline=attempt.is_baseline, result_url=f"/api/v1/attempts/{attempt.id}/result")


@router.get(
    "/attempts/{attempt_id}/result", operation_id="assessment_get_attempt_result", response_model=AttemptResult,
    responses={**_ERRORS, 409: {"description": "Attempt not scored yet"}},
)
def get_result(attempt_id: uuid.UUID, current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> AttemptResult:
    return AttemptResult(**service.result_view(db, current.user, attempt_id))
