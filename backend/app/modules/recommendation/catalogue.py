"""Learner course catalogue and course detail (API_INTEGRATION_SPEC.md §2.9, UI_UX_SPEC.md S-09, MVP-17).

Learners see approved, active courses only; unreviewed NSSTA programme listings stay hidden. Difficulty and learning
objectives are descriptive (DEC-051): they filter and display, and rec-v1 never reads them. Recommendation context
comes from the same deterministic service the dashboard uses, so a course shows exactly why it was recommended.
"""

from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.core.errors import ProblemError
from app.modules.competency import service as competency_service
from app.modules.competency.models import Competency, CompetencyFramework
from app.modules.identity.models import User
from app.modules.recommendation import service as recommendation_service
from app.modules.recommendation.models import COURSE_DIFFICULTIES, Course, CourseCompetency

SORTS = ("recommended", "title", "duration_asc", "duration_desc")


def _learner_visible(user: User):
    return select(Course).where(Course.organization_id == user.organization_id, Course.status == "active",
                                Course.review_status == "approved")


def _learning_context(db: DbSession, user: User, can_learn: bool) -> tuple[dict[str, dict], dict[str, dict]]:
    """(recommendations by course id, gaps by competency id) for the caller; empty when unavailable."""
    if not can_learn or user.job_role_id is None:
        return {}, {}
    try:
        recs = recommendation_service.recommendations(db, user)
        gaps = competency_service.competency_gaps(db, user)
    except ProblemError:
        return {}, {}
    return ({str(item["course"]["id"]): item for item in recs["items"]},
            {str(item["competency"]["id"]): item for item in gaps["items"]})


def _mappings(db: DbSession, course_ids: list[uuid.UUID]) -> dict[uuid.UUID, list[dict]]:
    if not course_ids:
        return {}
    rows = db.execute(
        select(CourseCompetency, Competency, CompetencyFramework)
        .join(Competency, Competency.id == CourseCompetency.competency_id)
        .join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
        .where(CourseCompetency.course_id.in_(course_ids), CourseCompetency.status == "approved")
        .order_by(CourseCompetency.relevance, Competency.code)
    ).all()
    out: dict[uuid.UUID, list[dict]] = {}
    for mapping, competency, framework in rows:
        out.setdefault(mapping.course_id, []).append({
            "competency": competency_service.competency_ref(competency, framework), "relevance": mapping.relevance})
    return out


def _summary(course: Course, mappings: list[dict], rec: dict | None, gaps: dict[str, dict]) -> dict:
    addressed_gaps = [
        {"competency_id": m["competency"]["id"], "competency_name": m["competency"]["name"],
         "required_level": gaps[str(m["competency"]["id"])]["required_level"],
         "estimated_level": gaps[str(m["competency"]["id"])]["estimated_level"],
         "gap": gaps[str(m["competency"]["id"])]["gap"]}
        for m in mappings
        if str(m["competency"]["id"]) in gaps and gaps[str(m["competency"]["id"])]["status"] == "gap"
    ]
    return {
        "id": course.id, "title": course.title, "description": course.description,
        "provider_organisation": course.provider_organisation, "course_type": course.course_type,
        "duration_days": course.duration_days, "difficulty": course.difficulty,
        "learning_objectives": list(course.learning_objectives or []),
        "competencies": mappings,
        "recommendation": {"rank": rec["rank"], "reasons": rec["reasons"]} if rec else None,
        "addresses_your_gaps": addressed_gaps,
        "is_demo": is_demo_code(course.external_ref),
        "_content_origin": course.content_origin,
        "provenance": {"data_status": course.data_status, "review_status": course.review_status,
                       "is_demo": is_demo_code(course.external_ref)},
    }


def _attach_learning(db: DbSession, user: User, items: list[dict], can_learn: bool) -> None:
    """Lesson counts for everyone; the caller's own progress for learning roles (Phase 4B)."""
    from app.modules.learning import service as learning_service  # local import: learning depends on this module

    summaries = learning_service.course_progress_summaries(db, user, [i["id"] for i in items])
    for item in items:
        summary = summaries[item["id"]]
        item["content_origin"] = item.pop("_content_origin")
        item["lessons"] = {"lesson_count": summary["lesson_count"], "module_count": summary["module_count"],
                           "total_minutes": summary["total_minutes"]}
        item["your_progress"] = {k: summary[k] for k in ("status", "completed_lessons", "percent", "resume_lesson")}             if can_learn else None


def list_courses(db: DbSession, user: User, *, can_learn: bool, q: str | None, competency_id: uuid.UUID | None,
                 difficulty: str | None, max_days: int | None, sort: str, progress: str | None = None) -> dict:
    query = _learner_visible(user)
    if q:
        pattern = f"%{q.strip()}%"
        query = query.where(or_(Course.title.ilike(pattern), Course.description.ilike(pattern),
                                func.array_to_string(Course.learning_objectives, " ").ilike(pattern)))
    if competency_id:
        query = query.where(Course.id.in_(select(CourseCompetency.course_id).where(
            CourseCompetency.competency_id == competency_id, CourseCompetency.status == "approved")))
    if difficulty:
        query = query.where(Course.difficulty == difficulty)
    if max_days:
        query = query.where(Course.duration_days.is_not(None), Course.duration_days <= max_days)
    courses = list(db.scalars(query))
    recs, gaps = _learning_context(db, user, can_learn)
    mappings = _mappings(db, [c.id for c in courses])
    items = [_summary(c, mappings.get(c.id, []), recs.get(str(c.id)), gaps) for c in courses]
    _attach_learning(db, user, items, can_learn)
    if progress and can_learn:
        items = [i for i in items if i["your_progress"]["status"] == progress]

    if sort == "title":
        items.sort(key=lambda i: i["title"])
    elif sort in ("duration_asc", "duration_desc"):
        items.sort(key=lambda i: (i["duration_days"] is None, i["duration_days"] or 0, i["title"]),
                   reverse=sort == "duration_desc")
    else:  # recommended first (in rec-v1 order), then the rest by title
        items.sort(key=lambda i: (i["recommendation"] is None, (i["recommendation"] or {}).get("rank", 0), i["title"]))

    # Filter options come from the whole visible catalogue, not the filtered result.
    all_ids = [c.id for c in db.scalars(_learner_visible(user))]
    facet_rows = db.execute(
        select(Competency, CompetencyFramework, func.count(func.distinct(CourseCompetency.course_id)))
        .join(CourseCompetency, CourseCompetency.competency_id == Competency.id)
        .join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
        .where(CourseCompetency.course_id.in_(all_ids), CourseCompetency.status == "approved")
        .group_by(Competency.id, CompetencyFramework.id).order_by(Competency.name)
    ).all() if all_ids else []
    return {
        "items": items,
        "total": len(items),
        "filters": {
            "competencies": [{**competency_service.competency_ref(c, f), "course_count": n} for c, f, n in facet_rows],
            "difficulties": list(COURSE_DIFFICULTIES),
            "sorts": list(SORTS),
        },
        "has_learning_context": bool(recs or gaps),
    }


def course_detail(db: DbSession, user: User, course_id: uuid.UUID, *, can_learn: bool) -> dict:
    course = db.scalar(_learner_visible(user).where(Course.id == course_id))
    if course is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "This course is not available.")
    recs, gaps = _learning_context(db, user, can_learn)
    mappings = _mappings(db, [course.id]).get(course.id, [])
    detail = _summary(course, mappings, recs.get(str(course.id)), gaps)
    _attach_learning(db, user, [detail], can_learn)
    for mapping in detail["competencies"]:
        gap = gaps.get(str(mapping["competency"]["id"]))
        mapping["your_status"] = None if gap is None else {
            "status": gap["status"], "required_level": gap["required_level"],
            "estimated_level": gap["estimated_level"], "gap": gap["gap"], "evidence_band": gap["evidence_band"]}

    competency_ids = [m["competency"]["id"] for m in mappings]
    related_ids = [cid for cid in db.scalars(
        select(CourseCompetency.course_id).where(CourseCompetency.competency_id.in_(competency_ids),
                                                 CourseCompetency.status == "approved",
                                                 CourseCompetency.course_id != course.id).distinct())] if competency_ids else []
    related = list(db.scalars(_learner_visible(user).where(Course.id.in_(related_ids)).order_by(Course.title))) if related_ids else []
    detail["related_courses"] = [
        {"id": c.id, "title": c.title, "difficulty": c.difficulty, "duration_days": c.duration_days,
         "is_demo": is_demo_code(c.external_ref), "is_recommended": str(c.id) in recs}
        for c in related[:4]
    ]
    from app.modules.learning.models import CoursePrerequisite

    prerequisites = list(db.scalars(_learner_visible(user).join(
        CoursePrerequisite, CoursePrerequisite.prerequisite_course_id == Course.id).where(
        CoursePrerequisite.course_id == course.id).order_by(Course.title)))
    detail["prerequisites"] = [{"id": c.id, "title": c.title} for c in prerequisites]
    detail["completion_criteria"] = course.completion_criteria
    available = detail["lessons"]["lesson_count"] > 0
    detail["learning_content"] = {"available": available,
                                  "reason": None if available else "This course has no lessons in the platform yet."}
    return detail
