"""Aggregated insight for administrators (Phase 4D; plan assumption A-3, SECURITY_RESPONSIBLE_AI.md §12).

Rules:
- Aggregates only. No learner names, emails, identifiers or individual rows ever leave this module.
- Minimum group size: any figure describing fewer than ``MIN_GROUP_SIZE`` learners is withheld (``suppressed``),
  including zero counts inside small groups, so small departments cannot be singled out.
- A gap counts only where ``score-v1`` evidence is at least "medium" (the same rule learners see).
- ``department_admin`` sees their own departments only; other insight roles see the organisation.
- Development guidance only: figures describe learning needs, never performance, appraisal or eligibility.
"""

from __future__ import annotations

import uuid
from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.modules.assessment.models import AssessmentAttempt
from app.modules.competency import scoring
from app.modules.competency.models import Competency, RoleCompetency, UserCompetency
from app.modules.identity.dependencies import CurrentUser
from app.modules.identity.models import User, UserAccessRole
from app.modules.identity.policy import only_department_scoped
from app.modules.learning.models import ProgressRecord
from app.modules.organization.models import Department, JobRole
from app.modules.recommendation.models import Course, CourseCompetency

MIN_GROUP_SIZE = 5
NOTE = ("Aggregated development insight. Figures for fewer than 5 learners are withheld. Gaps count only where assessment "
        "evidence is at least medium. Not a measure of performance and not for appraisal or selection decisions.")


@dataclass(frozen=True)
class LearnerGaps:
    department_id: uuid.UUID | None
    job_role_id: uuid.UUID | None
    assessed: set[uuid.UUID]  # competencies with any estimate
    gaps: dict[uuid.UUID, int]  # competency -> gap size (confirmed gaps only)
    required: dict[uuid.UUID, int]


def _count(value: int) -> dict:
    return {"value": value, "suppressed": False} if value >= MIN_GROUP_SIZE else {"value": None, "suppressed": True}


def _scope(db: DbSession, current: CurrentUser) -> set[uuid.UUID] | None:
    if not only_department_scoped(current.roles, "insight.view"):
        return None
    return set(db.scalars(select(UserAccessRole.department_scope_id).where(
        UserAccessRole.user_id == current.user.id, UserAccessRole.role == "department_admin",
        UserAccessRole.department_scope_id.is_not(None))))


def _learners(db: DbSession, current: CurrentUser, job_role_id: uuid.UUID | None = None) -> dict[uuid.UUID, LearnerGaps]:
    org_id = current.user.organization_id
    query = (select(User).join(UserAccessRole, UserAccessRole.user_id == User.id)
             .where(User.organization_id == org_id, UserAccessRole.role == "learner", User.status.in_(["active", "invited"]))
             .distinct())
    scope = _scope(db, current)
    if scope is not None:
        query = query.where(User.department_id.in_(scope or {uuid.UUID(int=0)}))
    if job_role_id:
        query = query.where(User.job_role_id == job_role_id)
    users = {u.id: u for u in db.scalars(query)}
    if not users:
        return {}
    requirements: dict[uuid.UUID, dict[uuid.UUID, int]] = defaultdict(dict)
    for req in db.scalars(select(RoleCompetency).where(RoleCompetency.organization_id == org_id)):
        requirements[req.job_role_id][req.competency_id] = req.required_level_number
    estimates: dict[uuid.UUID, list[UserCompetency]] = defaultdict(list)
    for estimate in db.scalars(select(UserCompetency).where(UserCompetency.user_id.in_(list(users)))):
        estimates[estimate.user_id].append(estimate)
    out = {}
    for user_id, user in users.items():
        required = requirements.get(user.job_role_id, {}) if user.job_role_id else {}
        assessed, gaps = set(), {}
        for estimate in estimates.get(user_id, []):
            if estimate.competency_id not in required:
                continue
            assessed.add(estimate.competency_id)
            result = scoring.classify_gap(required[estimate.competency_id], estimate.level_number, estimate.evidence_band)
            if result.status == "gap":
                gaps[estimate.competency_id] = result.gap
        out[user_id] = LearnerGaps(user.department_id, user.job_role_id, assessed, gaps, required)
    return out


def summary(db: DbSession, current: CurrentUser) -> dict:
    learners = _learners(db, current)
    ids = list(learners)
    baselines = db.scalar(select(func.count(func.distinct(AssessmentAttempt.user_id))).where(
        AssessmentAttempt.user_id.in_(ids), AssessmentAttempt.is_baseline, AssessmentAttempt.status == "scored")) if ids else 0
    completed = db.scalar(select(func.count(func.distinct(ProgressRecord.user_id))).where(
        ProgressRecord.user_id.in_(ids), ProgressRecord.target_type == "course", ProgressRecord.status == "completed")) if ids else 0
    started = db.scalar(select(func.count(func.distinct(ProgressRecord.user_id))).where(
        ProgressRecord.user_id.in_(ids), ProgressRecord.target_type == "course")) if ids else 0
    return {
        "learners": _count(len(learners)),
        "baseline_completed": _count(baselines or 0),
        "learners_with_confirmed_gaps": _count(sum(1 for lg in learners.values() if lg.gaps)),
        "learners_started_learning": _count(started or 0),
        "learners_completed_a_course": _count(completed or 0),
        "min_group_size": MIN_GROUP_SIZE,
        "scope": "department" if _scope(db, current) is not None else "organisation",
        "note": NOTE,
    }


def skill_gaps(db: DbSession, current: CurrentUser, job_role_id: uuid.UUID | None) -> dict:
    org_id = current.user.organization_id
    learners = _learners(db, current, job_role_id)
    competency_ids = sorted({c for lg in learners.values() for c in lg.required}, key=str)
    competencies = {c.id: c for c in db.scalars(select(Competency).where(Competency.id.in_(competency_ids)))} if competency_ids else {}
    departments = {d.id: d for d in db.scalars(select(Department).where(Department.organization_id == org_id))}

    by_department: dict[uuid.UUID | None, list[LearnerGaps]] = defaultdict(list)
    for lg in learners.values():
        by_department[lg.department_id].append(lg)

    def cell(group: list[LearnerGaps], competency_id: uuid.UUID) -> dict:
        required = [lg for lg in group if competency_id in lg.required]
        assessed = [lg for lg in required if competency_id in lg.assessed]
        with_gap = [lg for lg in assessed if competency_id in lg.gaps]
        if len(assessed) < MIN_GROUP_SIZE:
            return {"required_for": len(required) if len(required) >= MIN_GROUP_SIZE else None, "assessed": None,
                    "with_gap": None, "share": None, "average_gap": None, "suppressed": bool(required)}
        return {"required_for": len(required), "assessed": len(assessed), "with_gap": len(with_gap),
                "share": round(len(with_gap) / len(assessed), 3),
                "average_gap": round(sum(lg.gaps[competency_id] for lg in with_gap) / len(with_gap), 2) if with_gap else None,
                "suppressed": False}

    rows = []
    for dept_id, group in sorted(by_department.items(), key=lambda kv: departments[kv[0]].name if kv[0] in departments else "~"):
        dept = departments.get(dept_id)
        rows.append({
            "department": {"id": dept.id, "name": dept.name, "is_demo": is_demo_code((dept.code or "").upper())} if dept else
                          {"id": None, "name": "No department recorded", "is_demo": False},
            "learners": _count(len(group)),
            "cells": {str(c): cell(group, c) for c in competency_ids},
        })
    everyone = list(learners.values())
    roles = db.scalars(select(JobRole).where(JobRole.organization_id == org_id, JobRole.status == "active").order_by(JobRole.name))
    return {
        "competencies": [{"id": c, "code": competencies[c].code, "name": competencies[c].name} for c in competency_ids if c in competencies],
        "rows": rows,
        "totals": {str(c): cell(everyone, c) for c in competency_ids},
        "job_roles": [{"id": r.id, "name": r.name} for r in roles],
        "job_role_id": job_role_id,
        "min_group_size": MIN_GROUP_SIZE,
        "note": NOTE,
    }


def training_needs(db: DbSession, current: CurrentUser) -> dict:
    learners = _learners(db, current)
    need: dict[uuid.UUID, list[tuple[uuid.UUID, int]]] = defaultdict(list)
    for user_id, lg in learners.items():
        for competency_id, gap in lg.gaps.items():
            need[competency_id].append((user_id, gap))
    if not need:
        return {"items": [], "min_group_size": MIN_GROUP_SIZE, "note": NOTE, "withheld_competencies": 0}
    competencies = {c.id: c for c in db.scalars(select(Competency).where(Competency.id.in_(list(need))))}
    links = db.execute(select(CourseCompetency.competency_id, Course.id).join(Course, Course.id == CourseCompetency.course_id)
                       .where(CourseCompetency.competency_id.in_(list(need)), CourseCompetency.status == "approved",
                              Course.status == "active", Course.review_status == "approved")).all()
    courses_for: dict[uuid.UUID, set[uuid.UUID]] = defaultdict(set)
    for competency_id, course_id in links:
        courses_for[competency_id].add(course_id)
    progress = db.execute(select(ProgressRecord.user_id, ProgressRecord.target_id, ProgressRecord.status).where(
        ProgressRecord.user_id.in_(list(learners)), ProgressRecord.target_type == "course")).all()
    items, withheld = [], 0
    for competency_id, entries in need.items():
        if len(entries) < MIN_GROUP_SIZE:
            withheld += 1
            continue
        user_ids = {u for u, _ in entries}
        linked = courses_for.get(competency_id, set())
        started = {u for u, course, _ in progress if u in user_ids and course in linked}
        finished = {u for u, course, status in progress if u in user_ids and course in linked and status == "completed"}
        departments = {learners[u].department_id for u in user_ids}
        competency = competencies[competency_id]
        items.append({
            "competency": {"id": competency.id, "code": competency.code, "name": competency.name},
            "learners_with_gap": len(entries),
            "average_gap": round(sum(g for _, g in entries) / len(entries), 2),
            "departments_affected": len(departments),
            "published_courses": len(linked),
            "learners_started_linked_course": _count(len(started)),
            "learners_completed_linked_course": _count(len(finished)),
            "content_gap": len(linked) == 0,
        })
    items.sort(key=lambda i: (-i["learners_with_gap"], -i["average_gap"], i["competency"]["code"]))
    return {"items": items, "min_group_size": MIN_GROUP_SIZE, "note": NOTE, "withheld_competencies": withheld}
