"""Learning experience routes (Phase 4B). Learning roles only; every route acts on the caller's own progress."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session as DbSession

from app.core.db import get_db
from app.modules.identity.dependencies import SELF_LEARNING_ROLES, CurrentUser, require_any_role
from app.modules.identity.schemas import RequestModel
from app.modules.learning import service

router = APIRouter(prefix="/api/v1", tags=["learning"])

_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "CSRF or permission failure"},
           404: {"description": "Not available"}}
learner = require_any_role(SELF_LEARNING_ROLES)
learner_write = require_any_role(SELF_LEARNING_ROLES, csrf=True)


class LessonRef(BaseModel):
    id: uuid.UUID
    title: str


class CourseProgress(BaseModel):
    lesson_count: int
    total_minutes: int
    module_count: int
    completed_lessons: int
    percent: int
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    resume_lesson: LessonRef | None


class LearningCourseRef(BaseModel):
    id: uuid.UUID
    title: str
    difficulty: str | None
    duration_days: int | None
    content_origin: str
    completion_criteria: str | None
    is_demo: bool
    description: str | None = None


class OutlineLesson(BaseModel):
    id: uuid.UUID
    position: int
    title: str
    lesson_type: str
    estimated_minutes: int
    status: str


class OutlineModule(BaseModel):
    id: uuid.UUID
    position: int
    title: str
    summary: str | None
    lessons: list[OutlineLesson]


class PrerequisiteRef(BaseModel):
    id: uuid.UUID
    title: str
    status: str


class CourseOutline(BaseModel):
    course: LearningCourseRef
    modules: list[OutlineModule]
    progress: CourseProgress
    prerequisites: list[PrerequisiteRef]


class LessonModuleRef(BaseModel):
    id: uuid.UUID
    title: str
    position: int


class LessonDetail(BaseModel):
    id: uuid.UUID
    title: str
    lesson_type: str
    estimated_minutes: int
    content_kind: str
    body_markdown: str | None
    module: LessonModuleRef
    position: int
    lesson_count: int
    status: str
    previous: LessonRef | None
    next: LessonRef | None
    course: LearningCourseRef
    content_notice: str | None


class LessonProgressRequest(RequestModel):
    status: Literal["in_progress", "completed"]


class LessonProgressResponse(BaseModel):
    lesson_id: uuid.UUID
    lesson_status: str
    course_progress: CourseProgress
    next: LessonRef | None


class ProgressItem(BaseModel):
    course: LearningCourseRef
    progress: CourseProgress
    last_activity_at: datetime


class MyProgress(BaseModel):
    in_progress: list[ProgressItem]
    completed: list[ProgressItem]
    totals: dict[str, int]
    note: str


class PathItem(BaseModel):
    id: uuid.UUID
    position: int
    item_type: str
    course: LearningCourseRef | None
    progress: CourseProgress | None
    status: str
    reasons: list[dict]


class PathGroup(BaseModel):
    competency: dict
    required_level: int | None
    estimated_level: int | None
    gap: int | None
    items: list[PathItem]


class LearningPathResponse(BaseModel):
    id: uuid.UUID
    rule_version: str
    rule: str
    generated_at: datetime
    job_role: dict
    state: Literal["ready", "assessment_needed", "no_gaps"]
    summary: dict[str, int]
    groups: list[PathGroup]
    completed_earlier: list[PathItem]
    note: str


@router.get("/courses/{course_id}/outline", operation_id="learning_get_course_outline", response_model=CourseOutline,
            responses=_ERRORS)
def course_outline(course_id: uuid.UUID, current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> CourseOutline:
    return CourseOutline(**service.course_outline(db, current.user, course_id))


@router.post("/courses/{course_id}/start", operation_id="learning_start_course", response_model=CourseOutline,
             responses={**_ERRORS, 409: {"description": "Course has no lessons"}})
def start_course(course_id: uuid.UUID, current: CurrentUser = Depends(learner_write), db: DbSession = Depends(get_db)) -> CourseOutline:
    return CourseOutline(**service.start_course(db, current.user, course_id))


@router.get("/lessons/{lesson_id}", operation_id="learning_get_lesson", response_model=LessonDetail, responses=_ERRORS)
def get_lesson(lesson_id: uuid.UUID, current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> LessonDetail:
    return LessonDetail(**service.lesson_detail(db, current.user, lesson_id))


@router.put("/me/lessons/{lesson_id}/progress", operation_id="learning_put_lesson_progress",
            response_model=LessonProgressResponse, responses={**_ERRORS, 422: {"description": "Invalid status"}})
def put_lesson_progress(lesson_id: uuid.UUID, body: LessonProgressRequest, current: CurrentUser = Depends(learner_write),
                        db: DbSession = Depends(get_db)) -> LessonProgressResponse:
    return LessonProgressResponse(**service.set_lesson_progress(db, current.user, lesson_id, body.status))


@router.get("/me/progress", operation_id="learning_get_my_progress", response_model=MyProgress, responses=_ERRORS)
def my_progress(current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> MyProgress:
    return MyProgress(**service.my_progress(db, current.user))


@router.get("/me/learning-path", operation_id="learning_get_my_learning_path", response_model=LearningPathResponse,
            responses={**_ERRORS, 409: {"description": "No job role selected"}})
def my_learning_path(current: CurrentUser = Depends(learner), db: DbSession = Depends(get_db)) -> LearningPathResponse:
    return LearningPathResponse(**service.learning_path(db, current.user))


@router.post("/me/learning-path/regenerate", operation_id="learning_regenerate_my_learning_path",
             response_model=LearningPathResponse, responses={**_ERRORS, 409: {"description": "No job role selected"}})
def regenerate_learning_path(current: CurrentUser = Depends(learner_write), db: DbSession = Depends(get_db)) -> LearningPathResponse:
    return LearningPathResponse(**service.learning_path(db, current.user, regenerate=True))
