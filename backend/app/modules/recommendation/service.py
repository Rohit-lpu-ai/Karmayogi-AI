"""Recommendation service: applies ``rec-v1`` to the learner's own gaps and the reviewed catalogue."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.modules.competency import service as competency_service
from app.modules.identity.models import User
from app.modules.recommendation import rules
from app.modules.recommendation.models import Course, CourseCompetency


def _approved_mappings(db: DbSession, user: User, competency_ids: list) -> list[rules.CourseMapping]:
    if not competency_ids:
        return []
    rows = db.execute(
        select(Course, CourseCompetency)
        .join(CourseCompetency, CourseCompetency.course_id == Course.id)
        .where(Course.organization_id == user.organization_id, Course.status == "active",
               Course.review_status == "approved", CourseCompetency.status == "approved",
               CourseCompetency.competency_id.in_(competency_ids))
    ).all()
    return [rules.CourseMapping(str(course.id), course.title, course.course_type, course.duration_days,
                                str(mapping.competency_id), mapping.relevance) for course, mapping in rows]


def recommendations(db: DbSession, user: User) -> dict:
    gaps = competency_service.competency_gaps(db, user)  # raises JOB_ROLE_REQUIRED without a job role
    gap_inputs = [
        rules.GapInput(str(i["competency"]["id"]), i["competency"]["code"], i["competency"]["name"],
                       i["required_level"], i["estimated_level"], i["gap"], i["max_level_span"])
        for i in gaps["items"] if i["status"] == "gap"
    ]
    ranked = rules.rank_courses(gap_inputs, _approved_mappings(db, user, [g.competency_id for g in gap_inputs]))
    courses = {str(c.id): c for c in db.scalars(select(Course).where(Course.id.in_([r.course_id for r in ranked])))} \
        if ranked else {}
    items = []
    for rank, rec in enumerate(ranked, start=1):
        course = courses[rec.course_id]
        is_demo = is_demo_code(course.external_ref)
        items.append({
            "rank": rank,
            "course": {
                "id": course.id, "title": course.title, "course_type": course.course_type,
                "provider_organisation": course.provider_organisation, "duration_days": course.duration_days,
                "description": course.description, "is_demo": is_demo,
            },
            "score": rec.score,
            "reasons": list(rec.reasons),
            "provenance": {"source": "internal_catalogue", "data_status": course.data_status,
                           "review_status": course.review_status, "is_demo": is_demo},
        })
    unmatched = [g.competency_code for g in gap_inputs
                 if not any(r["rule"] == "gap_match" and r["competency_code"] == g.competency_code
                            for rec in ranked for r in rec.reasons)]
    return {
        "rule_version": rules.RULE_VERSION,
        "rule": "score = (gap / level span) x relevance weight (primary 1.0, secondary 0.5); "
                "only reviewed courses with approved competency mappings; ties: internal first, shorter, title",
        "job_role": gaps["job_role"],
        "items": items,
        "gaps_without_approved_content": unmatched,
        "igot": {"included": False, "reason": "No iGOT integration: mock source not enabled in this slice"},
    }
