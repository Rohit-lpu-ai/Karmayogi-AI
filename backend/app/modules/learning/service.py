"""Learning experience service (Phase 4B): course outline, start and resume, lessons, progress and the learning path.

Rules:
- Learners only ever read and write their own progress; every query filters on the caller's user id.
- Lessons are available only inside courses the learner can see in the catalogue (approved and active).
- Lesson completion is self-reported ("Mark as complete"). It updates course progress and the learning path, never a
  competency estimate: only assessment evidence changes estimates (no reassessment is added, K-4).
- A completed lesson is never downgraded by opening it again.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.core.errors import ProblemError
from app.modules.competency import service as competency_service
from app.modules.identity.models import User
from app.modules.learning import path_rules
from app.modules.learning.models import (
    CourseModule,
    CoursePrerequisite,
    LearningActivity,
    LearningPath,
    LearningPathItem,
    Lesson,
    ProgressRecord,
)
from app.modules.recommendation import service as recommendation_service
from app.modules.recommendation.models import Course


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _not_found(what: str = "course") -> ProblemError:
    return ProblemError(404, "NOT_FOUND", "Not found", f"This {what} is not available.")


def visible_course(db: DbSession, user: User, course_id: uuid.UUID) -> Course:
    course = db.scalar(select(Course).where(Course.id == course_id, Course.organization_id == user.organization_id,
                                            Course.status == "active", Course.review_status == "approved"))
    if course is None:
        raise _not_found()
    return course


def _active_lessons(db: DbSession, course_ids: list[uuid.UUID]) -> dict[uuid.UUID, list[tuple[CourseModule, Lesson]]]:
    """Active lessons per course in reading order (module position, lesson position)."""
    if not course_ids:
        return {}
    rows = db.execute(
        select(CourseModule, Lesson).join(Lesson, Lesson.module_id == CourseModule.id)
        .where(CourseModule.course_id.in_(course_ids), CourseModule.status == "active", Lesson.status == "active")
        .order_by(CourseModule.course_id, CourseModule.position, Lesson.position)
    ).all()
    out: dict[uuid.UUID, list[tuple[CourseModule, Lesson]]] = {cid: [] for cid in course_ids}
    for module, lesson in rows:
        out[module.course_id].append((module, lesson))
    return out


def _record(db: DbSession, user: User, target_type: str, target_id: uuid.UUID) -> ProgressRecord | None:
    return db.scalar(select(ProgressRecord).where(ProgressRecord.user_id == user.id, ProgressRecord.target_type == target_type,
                                                  ProgressRecord.target_id == target_id))


def _lesson_statuses(db: DbSession, user: User, course_ids: list[uuid.UUID]) -> dict[uuid.UUID, str]:
    if not course_ids:
        return {}
    return dict(db.execute(select(ProgressRecord.target_id, ProgressRecord.status).where(
        ProgressRecord.user_id == user.id, ProgressRecord.target_type == "lesson", ProgressRecord.course_id.in_(course_ids))).all())


def _activity(db: DbSession, user: User, activity_type: str, target_type: str, target_id: uuid.UUID | None, **metadata) -> None:
    db.add(LearningActivity(organization_id=user.organization_id, user_id=user.id, activity_type=activity_type,
                            target_type=target_type, target_id=target_id,
                            activity_metadata={k: (str(v) if isinstance(v, uuid.UUID) else v) for k, v in metadata.items()}))


def course_progress_summaries(db: DbSession, user: User, course_ids: list[uuid.UUID]) -> dict[uuid.UUID, dict]:
    """Per course: lesson counts, minutes, the caller's status, and the lesson to resume."""
    lessons = _active_lessons(db, course_ids)
    statuses = _lesson_statuses(db, user, course_ids)
    records = {r.target_id: r for r in db.scalars(select(ProgressRecord).where(
        ProgressRecord.user_id == user.id, ProgressRecord.target_type == "course", ProgressRecord.target_id.in_(course_ids)))} \
        if course_ids else {}
    out = {}
    for course_id in course_ids:
        rows = lessons.get(course_id, [])
        completed = sum(1 for _, lesson in rows if statuses.get(lesson.id) == "completed")
        record = records.get(course_id)
        next_lesson = next((lesson for _, lesson in rows if statuses.get(lesson.id) != "completed"), None)
        resume = record.resume_lesson_id if record and record.resume_lesson_id else (next_lesson.id if next_lesson else None)
        resume_lesson = next((lesson for _, lesson in rows if lesson.id == resume), None)
        out[course_id] = {
            "lesson_count": len(rows),
            "total_minutes": sum(lesson.estimated_minutes for _, lesson in rows),
            "module_count": len({module.id for module, _ in rows}),
            "completed_lessons": completed,
            "percent": round(100 * completed / len(rows)) if rows else 0,
            "status": record.status if record else "not_started",
            "started_at": record.started_at if record else None,
            "completed_at": record.completed_at if record else None,
            "resume_lesson": {"id": resume_lesson.id, "title": resume_lesson.title} if resume_lesson else None,
        }
    return out


def _course_ref(course: Course) -> dict:
    return {"id": course.id, "title": course.title, "difficulty": course.difficulty, "duration_days": course.duration_days,
            "content_origin": course.content_origin, "completion_criteria": course.completion_criteria,
            "is_demo": is_demo_code(course.external_ref)}


def course_outline(db: DbSession, user: User, course_id: uuid.UUID) -> dict:
    course = visible_course(db, user, course_id)
    rows = _active_lessons(db, [course.id])[course.id]
    statuses = _lesson_statuses(db, user, [course.id])
    modules: list[dict] = []
    for module, lesson in rows:
        if not modules or modules[-1]["id"] != module.id:
            modules.append({"id": module.id, "position": module.position, "title": module.title, "summary": module.summary,
                            "lessons": []})
        modules[-1]["lessons"].append({"id": lesson.id, "position": lesson.position, "title": lesson.title,
                                       "lesson_type": lesson.lesson_type, "estimated_minutes": lesson.estimated_minutes,
                                       "status": statuses.get(lesson.id, "not_started")})
    prereq_rows = db.execute(select(Course).join(CoursePrerequisite, CoursePrerequisite.prerequisite_course_id == Course.id)
                             .where(CoursePrerequisite.course_id == course.id, Course.status == "active",
                                    Course.review_status == "approved").order_by(Course.title)).scalars().all()
    prereq_progress = course_progress_summaries(db, user, [c.id for c in prereq_rows])
    return {
        "course": _course_ref(course),
        "modules": modules,
        "progress": course_progress_summaries(db, user, [course.id])[course.id],
        "prerequisites": [{"id": c.id, "title": c.title, "status": prereq_progress[c.id]["status"]} for c in prereq_rows],
    }


def start_course(db: DbSession, user: User, course_id: uuid.UUID) -> dict:
    course = visible_course(db, user, course_id)
    rows = _active_lessons(db, [course.id])[course.id]
    if not rows:
        raise ProblemError(409, "NO_LESSONS", "No lessons yet", "This course has no lessons to start yet.")
    _ensure_course_started(db, user, course, rows)
    db.commit()
    return course_outline(db, user, course.id)


def _claim_record(db: DbSession, user: User, target_type: str, target_id: uuid.UUID, **values) -> tuple[ProgressRecord, bool]:
    """Insert the progress row if absent, then lock it. Concurrent requests (a lesson opened and completed in quick
    succession) serialise on the row lock instead of failing on the unique constraint. Returns (row, created)."""
    inserted = db.execute(
        insert(ProgressRecord)
        .values(organization_id=user.organization_id, user_id=user.id, target_type=target_type, target_id=target_id,
                created_by=user.id, **values)
        .on_conflict_do_nothing(index_elements=["user_id", "target_type", "target_id"])
        .returning(ProgressRecord.id)
    ).scalar()
    record = db.scalar(select(ProgressRecord).where(ProgressRecord.user_id == user.id, ProgressRecord.target_type == target_type,
                                                    ProgressRecord.target_id == target_id)
                       .with_for_update().execution_options(populate_existing=True))
    return record, inserted is not None


def _ensure_course_started(db: DbSession, user: User, course: Course, rows: list[tuple[CourseModule, Lesson]]) -> ProgressRecord:
    statuses = _lesson_statuses(db, user, [course.id])
    first_open = next((lesson for _, lesson in rows if statuses.get(lesson.id) != "completed"), rows[0][1])
    record, created = _claim_record(db, user, "course", course.id, course_id=course.id, title_snapshot=course.title,
                                    status="in_progress", status_source="system", started_at=utcnow(),
                                    resume_lesson_id=first_open.id)
    if created:
        _activity(db, user, "course_started", "course", course.id, lesson_count=len(rows))
    return record


def _lesson_in_visible_course(db: DbSession, user: User, lesson_id: uuid.UUID) -> tuple[Lesson, Course, list[tuple[CourseModule, Lesson]]]:
    lesson = db.scalar(select(Lesson).where(Lesson.id == lesson_id, Lesson.organization_id == user.organization_id,
                                            Lesson.status == "active"))
    if lesson is None:
        raise _not_found("lesson")
    try:
        course = visible_course(db, user, lesson.course_id)
    except ProblemError:
        raise _not_found("lesson") from None
    rows = _active_lessons(db, [course.id])[course.id]
    if not any(l.id == lesson.id for _, l in rows):  # lesson inside an inactive module
        raise _not_found("lesson")
    return lesson, course, rows


def lesson_detail(db: DbSession, user: User, lesson_id: uuid.UUID) -> dict:
    lesson, course, rows = _lesson_in_visible_course(db, user, lesson_id)
    index = next(i for i, (_, l) in enumerate(rows) if l.id == lesson.id)
    module = rows[index][0]
    statuses = _lesson_statuses(db, user, [course.id])

    def ref(i: int) -> dict | None:
        return {"id": rows[i][1].id, "title": rows[i][1].title} if 0 <= i < len(rows) else None

    return {
        "id": lesson.id, "title": lesson.title, "lesson_type": lesson.lesson_type,
        "estimated_minutes": lesson.estimated_minutes, "content_kind": lesson.content_kind,
        "body_markdown": lesson.body_markdown,
        "module": {"id": module.id, "title": module.title, "position": module.position},
        "position": index + 1, "lesson_count": len(rows),
        "status": statuses.get(lesson.id, "not_started"),
        "previous": ref(index - 1), "next": ref(index + 1),
        "course": _course_ref(course),
        "content_notice": "Synthetic lesson written for product evaluation. Figures are invented."
        if course.content_origin == "synthetic" else None,
    }


def set_lesson_progress(db: DbSession, user: User, lesson_id: uuid.UUID, status: str) -> dict:
    lesson, course, rows = _lesson_in_visible_course(db, user, lesson_id)
    now = utcnow()
    course_record = _ensure_course_started(db, user, course, rows)  # locks the course row for this request
    record, created = _claim_record(db, user, "lesson", lesson.id, course_id=course.id, title_snapshot=lesson.title,
                                    status="in_progress", status_source="self_reported", started_at=now)
    if created:
        _activity(db, user, "lesson_opened", "lesson", lesson.id, course_id=course.id)
    if status == "completed" and record.status != "completed":
        record.status, record.completed_at, record.status_source = "completed", now, "self_reported"
        record.updated_by = user.id
        _activity(db, user, "lesson_completed", "lesson", lesson.id, course_id=course.id)
    db.flush()

    statuses = _lesson_statuses(db, user, [course.id])
    remaining = [l for _, l in rows if statuses.get(l.id) != "completed"]
    if status == "in_progress" and record.status != "completed":
        course_record.resume_lesson_id = lesson.id
    else:
        position = [l.id for _, l in rows].index(lesson.id)
        following = [l for _, l in rows[position + 1:] if statuses.get(l.id) != "completed"]
        upcoming = following or remaining
        course_record.resume_lesson_id = upcoming[0].id if upcoming else None
    if not remaining and course_record.status != "completed":
        course_record.status, course_record.completed_at, course_record.status_source = "completed", now, "self_reported"
        course_record.resume_lesson_id = None
        _activity(db, user, "course_completed", "course", course.id, lesson_count=len(rows))
    elif remaining and course_record.status == "completed":
        course_record.status, course_record.completed_at = "in_progress", None  # a lesson was added after completion
    course_record.updated_by = user.id
    _sync_path_items(db, user)
    db.commit()
    return {"lesson_id": lesson.id, "lesson_status": record.status,
            "course_progress": course_progress_summaries(db, user, [course.id])[course.id],
            "next": ({"id": remaining[0].id, "title": remaining[0].title} if remaining else None)}


def my_progress(db: DbSession, user: User) -> dict:
    records = list(db.scalars(select(ProgressRecord).where(ProgressRecord.user_id == user.id,
                                                           ProgressRecord.target_type == "course")
                              .order_by(ProgressRecord.updated_at.desc())))
    courses = {c.id: c for c in db.scalars(select(Course).where(Course.id.in_([r.target_id for r in records]),
                                                                Course.status == "active", Course.review_status == "approved"))} \
        if records else {}
    summaries = course_progress_summaries(db, user, list(courses))
    items = [{"course": _course_ref(courses[r.target_id]), "progress": summaries[r.target_id],
              "last_activity_at": r.updated_at} for r in records if r.target_id in courses]
    completed_lessons = db.scalar(select(func.count()).select_from(ProgressRecord).where(
        ProgressRecord.user_id == user.id, ProgressRecord.target_type == "lesson", ProgressRecord.status == "completed")) or 0
    return {
        "in_progress": [i for i in items if i["progress"]["status"] == "in_progress"],
        "completed": [i for i in items if i["progress"]["status"] == "completed"],
        "totals": {"courses_started": len(items), "courses_completed": sum(1 for i in items if i["progress"]["status"] == "completed"),
                   "lessons_completed": completed_lessons},
        "note": "Completion is recorded by you. It does not change your competency estimate; assessment evidence does.",
    }


# --- Learning path (path-v1) ---------------------------------------------------------------------------------


def _path_inputs(db: DbSession, user: User):
    gaps_payload = competency_service.competency_gaps(db, user)  # 409 JOB_ROLE_REQUIRED without a job role
    recs = recommendation_service.recommendations(db, user)
    gaps = [path_rules.PathGap(str(i["competency"]["id"]), i["competency"]["code"], i["competency"]["name"],
                               i["required_level"], i["estimated_level"], i["gap"])
            for i in gaps_payload["items"] if i["status"] == "gap"]
    recommended = []
    for item in recs["items"]:
        per_gap: dict[str, list[dict]] = {}
        current: str | None = None
        for reason in item["reasons"]:
            if reason["rule"] == "gap_match":
                current = str(reason["competency_id"])
                per_gap.setdefault(current, [])
            if current is not None:
                per_gap[current].append(reason)
        recommended.append(path_rules.PathCourse(str(item["course"]["id"]), item["course"]["title"],
                                                 item["course"]["difficulty"], item["rank"],
                                                 {k: tuple(v) for k, v in per_gap.items()}))
    visible = {str(c.id): path_rules.PathCourse(str(c.id), c.title, c.difficulty, 0) for c in db.scalars(
        select(Course).where(Course.organization_id == user.organization_id, Course.status == "active",
                             Course.review_status == "approved"))}
    prerequisites: dict[str, list[str]] = {}
    for row in db.scalars(select(CoursePrerequisite).where(CoursePrerequisite.organization_id == user.organization_id)):
        prerequisites.setdefault(str(row.course_id), []).append(str(row.prerequisite_course_id))
    return gaps_payload, gaps, recommended, visible, prerequisites


def _active_path(db: DbSession, user: User) -> LearningPath | None:
    return db.scalar(select(LearningPath).where(LearningPath.user_id == user.id, LearningPath.status == "active"))


def _completed_course_ids(db: DbSession, user: User) -> set[str]:
    return {str(i) for i in db.scalars(select(ProgressRecord.target_id).where(
        ProgressRecord.user_id == user.id, ProgressRecord.target_type == "course", ProgressRecord.status == "completed"))}


def _generate(db: DbSession, user: User, gaps, recommended, visible, prerequisites, digest: str, reason: str) -> LearningPath:
    previous = _active_path(db, user)
    completed = _completed_course_ids(db, user)
    earlier: list[str] = []
    if previous is not None:
        earlier = [str(i.target_id) for i in db.scalars(select(LearningPathItem).where(
            LearningPathItem.learning_path_id == previous.id, LearningPathItem.item_type == "course")) if str(i.target_id) in completed]
        previous.status = "superseded"
        db.flush()
    now = utcnow()
    path = LearningPath(organization_id=user.organization_id, user_id=user.id, job_role_id=user.job_role_id, status="active",
                        rule_version=path_rules.RULE_VERSION, input_snapshot_hash=digest, generated_at=now, created_by=user.id)
    db.add(path)
    db.flush()
    items = path_rules.build_path(gaps, recommended, prerequisites, visible, earlier)
    for position, item in enumerate(items, start=1):
        course = db.get(Course, uuid.UUID(item.course_id)) if item.course_id else None
        is_demo = is_demo_code(course.external_ref) if course else False
        db.add(LearningPathItem(
            organization_id=user.organization_id, learning_path_id=path.id, position=position, item_type=item.item_type,
            target_id=uuid.UUID(item.course_id) if item.course_id else None,
            gap_competency_id=uuid.UUID(item.gap_competency_id) if item.gap_competency_id else None,
            reasons=list(item.reasons),
            provenance={"rule_version": path_rules.RULE_VERSION, "recommendation_rule": "rec-v1",
                        "source": "internal_catalogue", "is_demo": is_demo},
            status="completed" if item.course_id in completed else "not_started", status_source="system",
            completed_at=now if item.course_id in completed else None, created_by=user.id))
    _activity(db, user, "path_generated", "learning_path", path.id, item_count=len(items), trigger=reason)
    db.flush()
    _sync_path_items(db, user)
    return path


def _sync_path_items(db: DbSession, user: User) -> None:
    path = _active_path(db, user)
    if path is None:
        return
    records = {r.target_id: r for r in db.scalars(select(ProgressRecord).where(
        ProgressRecord.user_id == user.id, ProgressRecord.target_type == "course"))}
    for item in db.scalars(select(LearningPathItem).where(LearningPathItem.learning_path_id == path.id,
                                                          LearningPathItem.item_type == "course")):
        record = records.get(item.target_id)
        status = record.status if record else "not_started"
        if item.status != status:
            item.status, item.status_source = status, "system"
            item.completed_at = record.completed_at if record and status == "completed" else None


def learning_path(db: DbSession, user: User, *, regenerate: bool = False) -> dict:
    gaps_payload, gaps, recommended, visible, prerequisites = _path_inputs(db, user)
    digest = path_rules.input_hash(str(user.job_role_id) if user.job_role_id else None, gaps, recommended, prerequisites)
    path = _active_path(db, user)
    if path is None or regenerate or path.input_snapshot_hash != digest:
        reason = "requested" if regenerate else ("first_view" if path is None else "inputs_changed")
        try:
            path = _generate(db, user, gaps, recommended, visible, prerequisites, digest, reason)
            db.commit()
        except IntegrityError:  # a concurrent request generated the path first
            db.rollback()
            path = _active_path(db, user)
            if path is None:
                raise
    else:
        _sync_path_items(db, user)
        db.commit()
    return _path_response(db, user, path, gaps_payload)


def _path_response(db: DbSession, user: User, path: LearningPath, gaps_payload: dict) -> dict:
    items = list(db.scalars(select(LearningPathItem).where(LearningPathItem.learning_path_id == path.id)
                            .order_by(LearningPathItem.position)))
    course_ids = [i.target_id for i in items if i.target_id]
    courses = {c.id: c for c in db.scalars(select(Course).where(Course.id.in_(course_ids)))} if course_ids else {}
    progress = course_progress_summaries(db, user, course_ids)
    gap_items = {str(i["competency"]["id"]): i for i in gaps_payload["items"]}

    def item_out(item: LearningPathItem) -> dict:
        course = courses.get(item.target_id) if item.target_id else None
        visible = bool(course and course.status == "active" and course.review_status == "approved")
        return {
            "id": item.id, "position": item.position, "item_type": item.item_type,
            "course": {**_course_ref(course), "description": course.description} if visible else None,
            "progress": progress.get(item.target_id) if visible else None,
            "status": item.status, "reasons": item.reasons,
        }

    groups: list[dict] = []
    earlier: list[dict] = []
    for item in items:
        if item.gap_competency_id is None:
            earlier.append(item_out(item))
            continue
        key = str(item.gap_competency_id)
        if not groups or groups[-1]["competency"]["id"] != key:
            gap = gap_items.get(key)
            groups.append({"competency": {"id": key, "code": gap["competency"]["code"] if gap else None,
                                          "name": gap["competency"]["name"] if gap else None},
                           "required_level": gap["required_level"] if gap else None,
                           "estimated_level": gap["estimated_level"] if gap else None,
                           "gap": gap["gap"] if gap else None, "items": []})
        groups[-1]["items"].append(item_out(item))

    course_items = [i for g in groups for i in g["items"] if i["course"]] + [i for i in earlier if i["course"]]
    summary = gaps_payload["summary"]
    if groups:
        state = "ready"
    elif summary.get("not_assessed") or summary.get("insufficient_evidence"):
        state = "assessment_needed"
    else:
        state = "no_gaps"
    return {
        "id": path.id, "rule_version": path.rule_version, "rule": path_rules.RULE_TEXT, "generated_at": path.generated_at,
        "job_role": gaps_payload["job_role"], "state": state,
        "summary": {"courses": len(course_items),
                    "completed": sum(1 for i in course_items if i["status"] == "completed"),
                    "in_progress": sum(1 for i in course_items if i["status"] == "in_progress"),
                    "total_minutes": sum((i["progress"] or {}).get("total_minutes", 0) for i in course_items),
                    "gaps_without_content": sum(1 for g in groups for i in g["items"] if i["item_type"] == "no_content_placeholder")},
        "groups": groups,
        "completed_earlier": earlier,
        "note": "Your path is ordered by rule path-v1 from your assessed gaps. Completing courses does not change your "
                "competency estimates.",
    }
