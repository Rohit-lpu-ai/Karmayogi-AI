"""Content administration routes (Phase 4C). Every route checks a policy capability on the server."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.core.errors import ProblemError
from app.modules.content_admin import courses, questions, reviews, views
from app.modules.identity.dependencies import CurrentUser, get_current_user, require_capability, require_csrf
from app.modules.identity.policy import has_capability
from app.modules.identity.schemas import RequestModel

router = APIRouter(prefix="/api/v1/admin", tags=["content administration"])
_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "CSRF or permission failure"},
           404: {"description": "Not found"}, 409: {"description": "Conflict or guard"}, 422: {"description": "Validation failed"}}

Difficulty = Literal["foundational", "intermediate", "advanced"]


# --- Schemas ------------------------------------------------------------------------------------------------


class OptionIn(RequestModel):
    text: str = Field(min_length=1, max_length=500)
    is_correct: bool


class SourceIn(RequestModel):
    source_kind: Literal["synthetic", "source_record", "external_reference"]
    source_record_id: uuid.UUID | None = None
    title: str | None = Field(default=None, max_length=300)
    publisher: str | None = Field(default=None, max_length=200)
    url: str | None = Field(default=None, max_length=500, pattern=r"^https?://\S+$")
    locator: str | None = Field(default=None, max_length=120)
    note: str | None = Field(default=None, max_length=500)


class QuestionIn(RequestModel):
    competency_id: uuid.UUID
    difficulty: Difficulty
    stem: str = Field(min_length=10, max_length=2000)
    explanation: str = Field(min_length=10, max_length=2000)
    options: list[OptionIn] = Field(min_length=2, max_length=6)
    sources: list[SourceIn] = Field(default_factory=list, max_length=5)


class QuestionUpdate(QuestionIn):
    row_version: int = Field(ge=1)


class NoteIn(RequestModel):
    note: str | None = Field(default=None, max_length=1000)


class DecisionIn(RequestModel):
    decision: Literal["approve", "reject", "request_changes"]
    reason: str | None = Field(default=None, max_length=2000)
    row_version: int = Field(ge=1)


class CourseIn(RequestModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    provider_organisation: str = Field(min_length=2, max_length=200)
    duration_days: int | None = Field(default=None, ge=1, le=365)
    difficulty: Difficulty | None = None
    learning_objectives: list[str] = Field(default_factory=list, max_length=12)
    completion_criteria: str | None = Field(default=None, max_length=500)
    content_origin: Literal["synthetic", "provider"] = "synthetic"


class CourseUpdate(RequestModel):
    row_version: int = Field(ge=1)
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    provider_organisation: str | None = Field(default=None, min_length=2, max_length=200)
    duration_days: int | None = Field(default=None, ge=1, le=365)
    difficulty: Difficulty | None = None
    learning_objectives: list[str] | None = Field(default=None, max_length=12)
    completion_criteria: str | None = Field(default=None, max_length=500)
    content_origin: Literal["synthetic", "provider"] | None = None


class ModuleIn(RequestModel):
    title: str = Field(min_length=2, max_length=200)
    summary: str | None = Field(default=None, max_length=500)


class LessonIn(RequestModel):
    title: str = Field(min_length=2, max_length=200)
    lesson_type: Literal["reading", "worked_example", "practice_check"]
    estimated_minutes: int = Field(ge=1, le=240)
    body_markdown: str = Field(min_length=20, max_length=20000)


class LessonUpdate(RequestModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    lesson_type: Literal["reading", "worked_example", "practice_check"] | None = None
    estimated_minutes: int | None = Field(default=None, ge=1, le=240)
    body_markdown: str | None = Field(default=None, min_length=20, max_length=20000)
    status: Literal["active", "inactive"] | None = None


class LinkIn(RequestModel):
    competency_id: uuid.UUID
    relevance: Literal["primary", "secondary"] | None  # null removes the link


class UnpublishIn(RequestModel):
    reason: str = Field(min_length=5, max_length=500)


# --- Questions ----------------------------------------------------------------------------------------------

author = require_capability("questions.author")
author_write = require_capability("questions.author", csrf=True)


@router.get("/questions", operation_id="admin_list_questions", responses=_ERRORS)
def list_questions(status: str | None = Query(default=None, max_length=40), competency_id: uuid.UUID | None = None,
                   origin: Literal["human_authored", "demo_seed", "ai_generated"] | None = None,
                   q: str | None = Query(default=None, max_length=100), page: int = Query(default=1, ge=1),
                   page_size: int = Query(default=25, ge=1, le=100),
                   current: CurrentUser = Depends(author), db: DbSession = Depends(get_db)) -> dict:
    return questions.list_questions(db, current, status=status, competency_id=competency_id, origin=origin, q=q,
                                    page=page, page_size=page_size)


@router.get("/questions/options", operation_id="admin_question_authoring_options", responses=_ERRORS)
def question_options(current: CurrentUser = Depends(author), db: DbSession = Depends(get_db)) -> dict:
    return questions.authoring_options(db, current)


@router.post("/questions", operation_id="admin_create_question", status_code=201, responses=_ERRORS)
def create_question(body: QuestionIn, current: CurrentUser = Depends(author_write), db: DbSession = Depends(get_db)) -> dict:
    return questions.create(db, current, body)


def _question_reader(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not (has_capability(current.roles, "questions.author") or has_capability(current.roles, "questions.review")):
        raise ProblemError(403, "FORBIDDEN", "Forbidden", "Your access role does not permit this action.")
    return current


@router.get("/questions/{question_id}", operation_id="admin_get_question", responses=_ERRORS)
def get_question(question_id: uuid.UUID, current: CurrentUser = Depends(_question_reader), db: DbSession = Depends(get_db)) -> dict:
    return questions.detail(db, current, question_id)


@router.put("/questions/{question_id}", operation_id="admin_update_question", responses=_ERRORS)
def update_question(question_id: uuid.UUID, body: QuestionUpdate, current: CurrentUser = Depends(author_write),
                    db: DbSession = Depends(get_db)) -> dict:
    return questions.update(db, current, question_id, body)


@router.post("/questions/{question_id}/submit", operation_id="admin_submit_question", responses=_ERRORS)
def submit_question(question_id: uuid.UUID, body: NoteIn, current: CurrentUser = Depends(author_write),
                    db: DbSession = Depends(get_db)) -> dict:
    return questions.submit(db, current, question_id, body.note)


@router.post("/questions/{question_id}/withdraw", operation_id="admin_withdraw_question", responses=_ERRORS)
def withdraw_question(question_id: uuid.UUID, current: CurrentUser = Depends(author_write), db: DbSession = Depends(get_db)) -> dict:
    return questions.withdraw(db, current, question_id)


@router.post("/questions/{question_id}/retire", operation_id="admin_retire_question", responses=_ERRORS)
def retire_question(question_id: uuid.UUID, current: CurrentUser = Depends(author_write), db: DbSession = Depends(get_db)) -> dict:
    return questions.retire(db, current, question_id)


# --- Reviews ------------------------------------------------------------------------------------------------


def _reviewer(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not (has_capability(current.roles, "questions.review") or has_capability(current.roles, "courses.review")):
        raise ProblemError(403, "FORBIDDEN", "Forbidden", "Your access role does not permit reviewing content.")
    return current


@router.get("/reviews", operation_id="admin_list_reviews", responses=_ERRORS)
def list_reviews(status: Literal["open", "decided", "cancelled", "all"] = "open", current: CurrentUser = Depends(_reviewer),
                 db: DbSession = Depends(get_db)) -> list[dict]:
    return reviews.list_tasks(db, current, status=status)


def _reviewer_write(current: CurrentUser = Depends(require_csrf)) -> CurrentUser:
    return _reviewer(current)


@router.post("/reviews/{task_id}/decision", operation_id="admin_decide_review", responses=_ERRORS)
def decide_review(task_id: uuid.UUID, body: DecisionIn, current: CurrentUser = Depends(_reviewer_write),
                  db: DbSession = Depends(get_db)) -> dict:
    """The capability for the task type and the self-review block are checked in the service."""
    return {"status": reviews.decide(db, current, task_id, body.decision, body.reason, body.row_version).status}


# --- Courses ------------------------------------------------------------------------------------------------

manager = require_capability("courses.manage")
manager_write = require_capability("courses.manage", csrf=True)


@router.get("/courses", operation_id="admin_list_courses", responses=_ERRORS)
def list_courses(state: Literal["draft", "in_review", "approved", "published"] | None = None,
                 origin: Literal["synthetic", "official_source", "provider"] | None = None,
                 q: str | None = Query(default=None, max_length=100),
                 current: CurrentUser = Depends(manager), db: DbSession = Depends(get_db)) -> dict:
    return courses.list_courses(db, current, state=state, origin=origin, q=q)


@router.get("/courses/options", operation_id="admin_course_authoring_options", responses=_ERRORS)
def course_options(current: CurrentUser = Depends(manager), db: DbSession = Depends(get_db)) -> dict:
    return courses.authoring_options(db, current)


@router.post("/courses", operation_id="admin_create_course", status_code=201, responses=_ERRORS)
def create_course(body: CourseIn, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.create(db, current, body)


def _course_reader(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not (has_capability(current.roles, "courses.manage") or has_capability(current.roles, "courses.review")):
        raise ProblemError(403, "FORBIDDEN", "Forbidden", "Your access role does not permit this action.")
    return current


@router.get("/courses/{course_id}", operation_id="admin_get_course", responses=_ERRORS)
def get_course(course_id: uuid.UUID, current: CurrentUser = Depends(_course_reader), db: DbSession = Depends(get_db)) -> dict:
    return courses.detail(db, current, course_id)


@router.patch("/courses/{course_id}", operation_id="admin_update_course", responses=_ERRORS)
def update_course(course_id: uuid.UUID, body: CourseUpdate, current: CurrentUser = Depends(manager_write),
                  db: DbSession = Depends(get_db)) -> dict:
    return courses.update(db, current, course_id, body)


@router.post("/courses/{course_id}/modules", operation_id="admin_add_course_module", responses=_ERRORS)
def add_module(course_id: uuid.UUID, body: ModuleIn, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.add_module(db, current, course_id, body.title, body.summary)


@router.post("/courses/{course_id}/modules/{module_id}/lessons", operation_id="admin_add_lesson", responses=_ERRORS)
def add_lesson(course_id: uuid.UUID, module_id: uuid.UUID, body: LessonIn, current: CurrentUser = Depends(manager_write),
               db: DbSession = Depends(get_db)) -> dict:
    return courses.add_lesson(db, current, course_id, module_id, body)


@router.patch("/courses/{course_id}/lessons/{lesson_id}", operation_id="admin_update_lesson", responses=_ERRORS)
def update_lesson(course_id: uuid.UUID, lesson_id: uuid.UUID, body: LessonUpdate, current: CurrentUser = Depends(manager_write),
                  db: DbSession = Depends(get_db)) -> dict:
    return courses.update_lesson(db, current, course_id, lesson_id, body)


@router.put("/courses/{course_id}/competencies", operation_id="admin_set_course_competency", responses=_ERRORS)
def set_competency(course_id: uuid.UUID, body: LinkIn, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.set_competency_link(db, current, course_id, body.competency_id, body.relevance)


@router.post("/courses/{course_id}/submit", operation_id="admin_submit_course", responses=_ERRORS)
def submit_course(course_id: uuid.UUID, body: NoteIn, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.submit(db, current, course_id, body.note)


@router.post("/courses/{course_id}/withdraw", operation_id="admin_withdraw_course", responses=_ERRORS)
def withdraw_course(course_id: uuid.UUID, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.withdraw(db, current, course_id)


@router.post("/courses/{course_id}/publish", operation_id="admin_publish_course", responses=_ERRORS)
def publish_course(course_id: uuid.UUID, current: CurrentUser = Depends(manager_write), db: DbSession = Depends(get_db)) -> dict:
    return courses.publish(db, current, course_id)


@router.post("/courses/{course_id}/unpublish", operation_id="admin_unpublish_course", responses=_ERRORS)
def unpublish_course(course_id: uuid.UUID, body: UnpublishIn, current: CurrentUser = Depends(manager_write),
                     db: DbSession = Depends(get_db)) -> dict:
    return courses.unpublish(db, current, course_id, body.reason)


# --- Read-only views ----------------------------------------------------------------------------------------


@router.get("/competencies", operation_id="admin_competency_structure", responses=_ERRORS)
def competency_structure(current: CurrentUser = Depends(require_capability("frameworks.view")), db: DbSession = Depends(get_db)) -> dict:
    return views.competency_structure(db, current)


@router.get("/assessments", operation_id="admin_assessments_overview", responses=_ERRORS)
def assessments_overview(current: CurrentUser = Depends(require_capability("assessments.manage")), db: DbSession = Depends(get_db)) -> list[dict]:
    return views.assessments_overview(db, current)


@router.get("/audit", operation_id="admin_audit_log", responses=_ERRORS)
def audit_log(action: str | None = Query(default=None, max_length=60, pattern=r"^[a-z_.]+$"),
              target_type: str | None = Query(default=None, max_length=60, pattern=r"^[a-z_]+$"),
              outcome: Literal["success", "denied", "failure"] | None = None, since: datetime | None = None,
              before_id: int | None = Query(default=None, ge=1), limit: int = Query(default=50, ge=1, le=200),
              current: CurrentUser = Depends(require_capability("audit.view")), db: DbSession = Depends(get_db)) -> dict:
    return views.audit_log(db, current, action=action, target_type=target_type, outcome=outcome, since=since,
                           before_id=before_id, limit=limit)
