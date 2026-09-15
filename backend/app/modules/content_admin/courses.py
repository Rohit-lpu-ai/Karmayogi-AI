"""Course administration (Phase 4C): details, modules, lessons, competency links, review and publishing.

States (derived, so learner visibility keeps using ``review_status`` and ``status``):
- ``draft``: not approved (``review_status`` unreviewed or rejected) and no open review;
- ``in_review``: an open review task;
- ``approved``: approved by a reviewer but not live (``status='inactive'``);
- ``published``: approved and ``status='active'`` - the only state learners see.

Guards: submitting needs a description, at least one active lesson and at least one competency link. Publishing needs
reviewer approval, at least one active lesson and at least one approved competency link. Editing an approved course
that is not live sends it back to draft; a published course must be unpublished before it can be edited. Programme
listings imported from official source documents can be viewed here but not edited or published (they have no lessons
and their review is a separate, pending human check).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.core.errors import ProblemError
from app.modules.competency.models import Competency, CompetencyFramework
from app.modules.content.models import SourceRecord
from app.modules.content_admin import reviews
from app.modules.governance.models import ReviewTask
from app.modules.governance.service import record_audit
from app.modules.identity.dependencies import CurrentUser
from app.modules.learning.models import CourseModule, Lesson
from app.modules.recommendation.models import Course, CourseCompetency


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def state_of(db: DbSession, course: Course) -> str:
    if reviews.open_task(db, "course", course.id) is not None:
        return "in_review"
    if course.review_status == "approved":
        return "published" if course.status == "active" else "approved"
    return "draft"


def _course(db: DbSession, current: CurrentUser, course_id: uuid.UUID, *, lock: bool = False) -> Course:
    query = select(Course).where(Course.id == course_id, Course.organization_id == current.user.organization_id)
    course = db.scalar(query.with_for_update() if lock else query)
    if course is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Course not found.")
    return course


def _audit(db: DbSession, current: CurrentUser, action: str, course: Course, **after) -> None:
    record_audit(db, organization_id=current.user.organization_id, action=action, target_type="course", target_id=str(course.id),
                 actor_user_id=current.user.id, actor_roles=sorted(current.roles), after=after or None)


def _editable(db: DbSession, current: CurrentUser, course: Course) -> None:
    if course.course_type != "internal":
        raise ProblemError(409, "READ_ONLY_LISTING", "Imported listing",
                           "Programme listings imported from source documents cannot be edited here.")
    state = state_of(db, course)
    if state == "in_review":
        raise ProblemError(409, "IN_REVIEW", "Waiting for review", "Withdraw the review request before editing.")
    if state == "published":
        raise ProblemError(409, "PUBLISHED", "Course is live", "Unpublish the course before editing it.")
    if state == "approved":
        course.review_status = "unreviewed"  # approval covered the previous content
        _audit(db, current, "course.approval_reset", course, reason="edited_after_approval")


def _lessons(db: DbSession, course_id: uuid.UUID) -> list[tuple[CourseModule, Lesson | None]]:
    return db.execute(select(CourseModule, Lesson).outerjoin(Lesson, Lesson.module_id == CourseModule.id)
                      .where(CourseModule.course_id == course_id)
                      .order_by(CourseModule.position, Lesson.position)).all()


def guard_report(db: DbSession, course: Course) -> dict:
    active_lessons = db.scalar(select(func.count()).select_from(Lesson).join(CourseModule, CourseModule.id == Lesson.module_id)
                               .where(Lesson.course_id == course.id, Lesson.status == "active", CourseModule.status == "active")) or 0
    links = dict(db.execute(select(CourseCompetency.status, func.count()).where(CourseCompetency.course_id == course.id)
                            .group_by(CourseCompetency.status)).all())
    checks = [
        {"id": "internal", "label": "Course is managed in this platform (not an imported listing)", "passed": course.course_type == "internal"},
        {"id": "description", "label": "Has a description", "passed": bool((course.description or "").strip())},
        {"id": "lessons", "label": "Has at least one active lesson", "passed": active_lessons > 0},
        {"id": "competency_link", "label": "Linked to at least one competency", "passed": sum(links.values()) > 0},
        {"id": "approved", "label": "Approved by a reviewer", "passed": course.review_status == "approved"},
        {"id": "approved_link", "label": "At least one approved competency link", "passed": links.get("approved", 0) > 0},
    ]
    submit_ids, publish_ids = {"internal", "description", "lessons", "competency_link"}, {"internal", "lessons", "approved", "approved_link"}
    return {"checks": checks,
            "can_submit": all(c["passed"] for c in checks if c["id"] in submit_ids),
            "can_publish": all(c["passed"] for c in checks if c["id"] in publish_ids)}


def list_courses(db: DbSession, current: CurrentUser, *, state: str | None, origin: str | None, q: str | None) -> dict:
    query = select(Course).where(Course.organization_id == current.user.organization_id)
    if origin:
        query = query.where(Course.content_origin == origin)
    if q:
        query = query.where(or_(Course.title.ilike(f"%{q.strip()}%"), Course.provider_organisation.ilike(f"%{q.strip()}%")))
    courses = list(db.scalars(query.order_by(Course.course_type, Course.title)))
    open_ids = set(db.scalars(select(ReviewTask.target_id).where(ReviewTask.target_type == "course", ReviewTask.status == "open",
                                                                 ReviewTask.organization_id == current.user.organization_id)))
    lesson_counts = dict(db.execute(select(Lesson.course_id, func.count()).where(Lesson.status == "active",
                                                                                 Lesson.course_id.in_([c.id for c in courses]))
                                    .group_by(Lesson.course_id)).all()) if courses else {}
    items = []
    for c in courses:
        s = "in_review" if c.id in open_ids else ("published" if c.review_status == "approved" and c.status == "active"
                                                  else "approved" if c.review_status == "approved" else "draft")
        items.append({"id": c.id, "title": c.title, "course_type": c.course_type, "content_origin": c.content_origin,
                      "provider_organisation": c.provider_organisation, "difficulty": c.difficulty, "state": s,
                      "review_status": c.review_status, "lesson_count": lesson_counts.get(c.id, 0),
                      "is_demo": is_demo_code(c.external_ref), "published_at": c.published_at, "updated_at": c.updated_at})
    counts = {k: sum(1 for i in items if i["state"] == k) for k in ("draft", "in_review", "approved", "published")}
    if state:
        items = [i for i in items if i["state"] == state]
    return {"items": items, "total": len(items), "state_counts": counts}


def detail(db: DbSession, current: CurrentUser, course_id: uuid.UUID) -> dict:
    course = _course(db, current, course_id)
    modules: list[dict] = []
    for module, lesson in _lessons(db, course.id):
        if not modules or modules[-1]["id"] != module.id:
            modules.append({"id": module.id, "position": module.position, "title": module.title, "summary": module.summary,
                            "status": module.status, "lessons": []})
        if lesson is not None:
            modules[-1]["lessons"].append({"id": lesson.id, "position": lesson.position, "title": lesson.title,
                                           "lesson_type": lesson.lesson_type, "estimated_minutes": lesson.estimated_minutes,
                                           "status": lesson.status, "body_markdown": lesson.body_markdown})
    links = db.execute(select(CourseCompetency, Competency).join(Competency, Competency.id == CourseCompetency.competency_id)
                       .where(CourseCompetency.course_id == course.id).order_by(CourseCompetency.relevance, Competency.code)).all()
    source = db.get(SourceRecord, course.source_record_id) if course.source_record_id else None
    state = state_of(db, course)
    task = reviews.open_task(db, "course", course.id)
    guards = guard_report(db, course)
    return {
        "id": course.id, "row_version": course.row_version, "title": course.title, "description": course.description,
        "course_type": course.course_type, "content_origin": course.content_origin, "provider_organisation": course.provider_organisation,
        "duration_days": course.duration_days, "difficulty": course.difficulty, "learning_objectives": list(course.learning_objectives or []),
        "completion_criteria": course.completion_criteria, "state": state, "review_status": course.review_status,
        "status": course.status, "published_at": course.published_at, "is_demo": is_demo_code(course.external_ref),
        "source": {"attribution": source.attribution_text, "url": source.source_url, "verified": source.review_verified,
                   "licence_notes": source.licence_notes} if source else None,
        "modules": modules,
        "competencies": [{"id": link.id, "competency": {"id": comp.id, "code": comp.code, "name": comp.name},
                          "relevance": link.relevance, "status": link.status} for link, comp in links],
        "guards": guards,
        "reviews": reviews.history(db, "course", course.id),
        "open_task_id": task.id if task else None,
        "actions": {
            "can_edit": course.course_type == "internal" and state in ("draft", "approved"),
            "can_submit": state == "draft" and guards["can_submit"],
            "can_withdraw": state == "in_review",
            "can_publish": state == "approved" and guards["can_publish"],
            "can_unpublish": state == "published",
        },
    }


def create(db: DbSession, current: CurrentUser, body) -> dict:
    course = Course(organization_id=current.user.organization_id, course_type="internal", title=body.title.strip(),
                    description=(body.description or "").strip() or None, provider_organisation=body.provider_organisation.strip(),
                    duration_days=body.duration_days, difficulty=body.difficulty,
                    learning_objectives=[o.strip() for o in body.learning_objectives if o.strip()],
                    completion_criteria=(body.completion_criteria or "").strip() or None, content_origin=body.content_origin,
                    data_status="ASSUMED", review_status="unreviewed", status="inactive", created_by=current.user.id)
    db.add(course)
    db.flush()
    _audit(db, current, "course.create", course, content_origin=course.content_origin)
    db.commit()
    return detail(db, current, course.id)


def update(db: DbSession, current: CurrentUser, course_id: uuid.UUID, body) -> dict:
    course = _course(db, current, course_id, lock=True)
    if course.row_version != body.row_version:
        raise ProblemError(409, "STALE_VERSION", "Changed by someone else", "This course changed since you opened it. Reload.")
    _editable(db, current, course)
    fields = body.model_dump(exclude_unset=True, exclude={"row_version"})
    for key in ("title", "description", "provider_organisation", "completion_criteria"):
        if key in fields:
            value = (fields[key] or "").strip() or None
            if key in ("title", "provider_organisation") and not value:
                continue
            setattr(course, key, value)
    for key in ("duration_days", "difficulty", "content_origin"):
        if key in fields:
            setattr(course, key, fields[key])
    if "learning_objectives" in fields:
        course.learning_objectives = [o.strip() for o in fields["learning_objectives"] if o.strip()]
    course.updated_by = current.user.id
    _audit(db, current, "course.update", course, fields=sorted(fields))
    db.commit()
    return detail(db, current, course.id)


def add_module(db: DbSession, current: CurrentUser, course_id: uuid.UUID, title: str, summary: str | None) -> dict:
    course = _course(db, current, course_id, lock=True)
    _editable(db, current, course)
    position = (db.scalar(select(func.max(CourseModule.position)).where(CourseModule.course_id == course.id)) or 0) + 1
    db.add(CourseModule(organization_id=course.organization_id, course_id=course.id, position=position, title=title.strip(),
                        summary=(summary or "").strip() or None, created_by=current.user.id))
    _audit(db, current, "course.module_add", course, position=position)
    db.commit()
    return detail(db, current, course.id)


def _module(db: DbSession, course: Course, module_id: uuid.UUID) -> CourseModule:
    module = db.scalar(select(CourseModule).where(CourseModule.id == module_id, CourseModule.course_id == course.id))
    if module is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Module not found.")
    return module


def add_lesson(db: DbSession, current: CurrentUser, course_id: uuid.UUID, module_id: uuid.UUID, body) -> dict:
    course = _course(db, current, course_id, lock=True)
    _editable(db, current, course)
    module = _module(db, course, module_id)
    position = (db.scalar(select(func.max(Lesson.position)).where(Lesson.module_id == module.id)) or 0) + 1
    db.add(Lesson(organization_id=course.organization_id, module_id=module.id, course_id=course.id, position=position,
                  title=body.title.strip(), lesson_type=body.lesson_type, estimated_minutes=body.estimated_minutes,
                  content_kind="inline_markdown", body_markdown=body.body_markdown.strip() + "\n", created_by=current.user.id))
    _audit(db, current, "course.lesson_add", course, module_id=str(module.id), position=position)
    db.commit()
    return detail(db, current, course.id)


def update_lesson(db: DbSession, current: CurrentUser, course_id: uuid.UUID, lesson_id: uuid.UUID, body) -> dict:
    course = _course(db, current, course_id, lock=True)
    _editable(db, current, course)
    lesson = db.scalar(select(Lesson).where(Lesson.id == lesson_id, Lesson.course_id == course.id))
    if lesson is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Lesson not found.")
    fields = body.model_dump(exclude_unset=True)
    for key in ("title", "lesson_type", "estimated_minutes", "status"):
        if key in fields and fields[key] is not None:
            setattr(lesson, key, fields[key].strip() if isinstance(fields[key], str) and key == "title" else fields[key])
    if fields.get("body_markdown"):
        lesson.body_markdown = fields["body_markdown"].strip() + "\n"
    lesson.updated_by = current.user.id
    _audit(db, current, "course.lesson_update", course, lesson_id=str(lesson.id), fields=sorted(fields))
    db.commit()
    return detail(db, current, course.id)


def set_competency_link(db: DbSession, current: CurrentUser, course_id: uuid.UUID, competency_id: uuid.UUID, relevance: str | None) -> dict:
    course = _course(db, current, course_id, lock=True)
    _editable(db, current, course)
    competency = db.scalar(select(Competency).join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
                           .where(Competency.id == competency_id, Competency.organization_id == course.organization_id))
    if competency is None:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Choose a competency from your organisation.")
    link = db.scalar(select(CourseCompetency).where(CourseCompetency.course_id == course.id, CourseCompetency.competency_id == competency.id))
    if relevance is None:
        if link is not None:
            db.delete(link)
            _audit(db, current, "course.competency_unlink", course, competency_id=str(competency.id))
    elif link is None:
        db.add(CourseCompetency(organization_id=course.organization_id, course_id=course.id, competency_id=competency.id,
                                relevance=relevance, method="human", status="suggested", created_by=current.user.id))
        _audit(db, current, "course.competency_link", course, competency_id=str(competency.id), relevance=relevance)
    else:
        link.relevance, link.status, link.approved_by, link.approved_at = relevance, "suggested", None, None
        _audit(db, current, "course.competency_link", course, competency_id=str(competency.id), relevance=relevance)
    db.commit()
    return detail(db, current, course.id)


def submit(db: DbSession, current: CurrentUser, course_id: uuid.UUID, note: str | None) -> dict:
    course = _course(db, current, course_id, lock=True)
    if state_of(db, course) != "draft":
        raise ProblemError(409, "NOT_SUBMITTABLE", "Cannot submit", "Only draft courses can be sent for review.")
    guards = guard_report(db, course)
    if not guards["can_submit"]:
        failed = [c["label"] for c in guards["checks"] if not c["passed"] and c["id"] in {"internal", "description", "lessons", "competency_link"}]
        raise ProblemError(422, "SUBMIT_GUARDS_FAILED", "Not ready for review", "Before review: " + "; ".join(failed) + ".")
    reviews.submit(db, current, task_type="course_review", target_type="course", target_id=course.id, target_version_id=None,
                   title=course.title, note=note)
    db.commit()
    return detail(db, current, course.id)


def withdraw(db: DbSession, current: CurrentUser, course_id: uuid.UUID) -> dict:
    course = _course(db, current, course_id, lock=True)
    reviews.cancel_open(db, current, "course", course.id, "withdrawn_by_manager")
    db.commit()
    return detail(db, current, course.id)


def publish(db: DbSession, current: CurrentUser, course_id: uuid.UUID) -> dict:
    course = _course(db, current, course_id, lock=True)
    if state_of(db, course) != "approved":
        raise ProblemError(409, "NOT_APPROVED", "Not approved", "Only courses approved by a reviewer can be published.")
    guards = guard_report(db, course)
    if not guards["can_publish"]:
        failed = [c["label"] for c in guards["checks"] if not c["passed"] and c["id"] in {"internal", "lessons", "approved", "approved_link"}]
        raise ProblemError(422, "PUBLISH_GUARDS_FAILED", "Cannot publish", "Before publishing: " + "; ".join(failed) + ".")
    course.status, course.published_at, course.published_by, course.updated_by = "active", utcnow(), current.user.id, current.user.id
    _audit(db, current, "course.publish", course)
    db.commit()
    return detail(db, current, course.id)


def unpublish(db: DbSession, current: CurrentUser, course_id: uuid.UUID, reason: str) -> dict:
    course = _course(db, current, course_id, lock=True)
    if state_of(db, course) != "published":
        raise ProblemError(409, "NOT_PUBLISHED", "Not published", "This course is not live.")
    course.status, course.updated_by = "inactive", current.user.id
    record_audit(db, organization_id=current.user.organization_id, action="course.unpublish", target_type="course",
                 target_id=str(course.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles), reason=reason)
    db.commit()
    return detail(db, current, course.id)


def _on_decision(db: DbSession, task: ReviewTask, decision: str, current: CurrentUser) -> None:
    course = db.scalar(select(Course).where(Course.id == task.target_id).with_for_update())
    if course is None:
        raise ProblemError(409, "TARGET_CHANGED", "Course changed", "The course is no longer available.")
    if decision == "approve":
        guards = guard_report(db, course)
        if not guards["can_submit"]:
            raise ProblemError(409, "TARGET_CHANGED", "Course changed", "The course no longer meets the review requirements.")
        now = utcnow()
        course.review_status = "approved"
        for link in db.scalars(select(CourseCompetency).where(CourseCompetency.course_id == course.id)):
            link.status, link.approved_by, link.approved_at = "approved", current.user.id, now
    elif decision == "reject":
        course.review_status = "rejected"
    else:
        course.review_status = "unreviewed"
    course.updated_by = current.user.id


reviews.register_handler("course_review", _on_decision)


def authoring_options(db: DbSession, current: CurrentUser) -> dict:
    rows = db.execute(select(Competency, CompetencyFramework).join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
                      .where(Competency.organization_id == current.user.organization_id, Competency.status == "active")
                      .order_by(CompetencyFramework.code, Competency.name)).all()
    return {"competencies": [{"id": c.id, "code": c.code, "name": c.name, "framework_code": f.code} for c, f in rows]}
