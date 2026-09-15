"""Read-only administration views (Phase 4C): competency structure, assessment coverage and guards, audit trail.

Licence-restricted frameworks show names and codes only (no definitions), as everywhere else.
The audit view is organisation-scoped and paginated; entries never contain passwords, tokens or answer keys.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.modules.assessment.models import Assessment, AssessmentQuestion, Question, QuestionSourceReference, QuestionVersion
from app.modules.competency.models import Competency, CompetencyFramework, CompetencyLevel, RoleCompetency
from app.modules.governance.models import AuditLog
from app.modules.identity.dependencies import CurrentUser
from app.modules.identity.models import User
from app.modules.organization.models import JobRole

MIN_ITEMS_PER_COMPETENCY = 5  # evidence reaches the "medium" band (score-v1)


def competency_structure(db: DbSession, current: CurrentUser) -> dict:
    org_id = current.user.organization_id
    frameworks = list(db.scalars(select(CompetencyFramework).where(CompetencyFramework.organization_id == org_id)
                                 .order_by(CompetencyFramework.code)))
    competencies = list(db.scalars(select(Competency).where(Competency.organization_id == org_id).order_by(Competency.code)))
    levels = dict(db.execute(select(CompetencyLevel.framework_id, func.count()).group_by(CompetencyLevel.framework_id)).all())
    question_counts = dict(db.execute(
        select(QuestionVersion.competency_id, func.count(func.distinct(Question.id)))
        .join(Question, Question.approved_version_id == QuestionVersion.id)
        .where(Question.organization_id == org_id, Question.status == "approved").group_by(QuestionVersion.competency_id)).all())
    roles = list(db.scalars(select(JobRole).where(JobRole.organization_id == org_id).order_by(JobRole.name)))
    requirements = db.execute(select(RoleCompetency, Competency).join(Competency, Competency.id == RoleCompetency.competency_id)
                              .where(RoleCompetency.organization_id == org_id).order_by(Competency.code)).all()
    by_role: dict[uuid.UUID, list[dict]] = {}
    for req, comp in requirements:
        by_role.setdefault(req.job_role_id, []).append({"competency": {"id": comp.id, "code": comp.code, "name": comp.name},
                                                        "required_level": req.required_level_number, "status": req.status,
                                                        "mapping_version": req.mapping_version})
    return {
        "frameworks": [{
            "id": f.id, "code": f.code, "name": f.name, "status": f.status, "version_label": f.version_label,
            "definitions_restricted": f.definitions_restricted, "is_demo": is_demo_code(f.code), "level_count": levels.get(f.id, 0),
            "competencies": [{"id": c.id, "code": c.code, "name": c.name, "status": c.status,
                              "description": None if f.definitions_restricted else c.description,
                              "approved_questions": question_counts.get(c.id, 0)}
                             for c in competencies if c.framework_id == f.id],
        } for f in frameworks],
        "job_roles": [{"id": r.id, "code": r.code, "name": r.name, "status": r.status, "is_demo": is_demo_code(r.code),
                       "requirements": by_role.get(r.id, [])} for r in roles],
    }


def assessments_overview(db: DbSession, current: CurrentUser) -> list[dict]:
    org_id = current.user.organization_id
    out = []
    for assessment in db.scalars(select(Assessment).where(Assessment.organization_id == org_id).order_by(Assessment.title)):
        rows = db.execute(select(QuestionVersion, Question, Competency)
                          .join(AssessmentQuestion, AssessmentQuestion.question_version_id == QuestionVersion.id)
                          .join(Question, Question.id == QuestionVersion.question_id)
                          .join(Competency, Competency.id == QuestionVersion.competency_id)
                          .where(AssessmentQuestion.assessment_id == assessment.id)).all()
        with_sources = set(db.scalars(select(QuestionSourceReference.question_version_id).where(
            QuestionSourceReference.question_version_id.in_([v.id for v, _, _ in rows])))) if rows else set()
        role = db.get(JobRole, assessment.job_role_id) if assessment.job_role_id else None
        required = [comp for _, comp in db.execute(select(RoleCompetency, Competency).join(Competency, Competency.id == RoleCompetency.competency_id)
                                                    .where(RoleCompetency.job_role_id == assessment.job_role_id))] if role else []
        coverage = {}
        for version, _, comp in rows:
            coverage.setdefault(comp.id, {"competency": {"id": comp.id, "code": comp.code, "name": comp.name}, "items": 0})["items"] += 1
        for comp in required:
            coverage.setdefault(comp.id, {"competency": {"id": comp.id, "code": comp.code, "name": comp.name}, "items": 0})
        not_approved = sum(1 for v, q, _ in rows if not (q.status == "approved" and q.approved_version_id == v.id))
        seeded = sum(1 for _, q, _ in rows if q.origin == "demo_seed")
        missing_sources = sum(1 for v, q, _ in rows if v.id not in with_sources and q.origin != "demo_seed")
        checks = [
            {"id": "approved_items", "label": "Every item is an approved question version", "passed": not_approved == 0,
             "detail": f"{not_approved} not approved" if not_approved else None},
            {"id": "coverage", "label": f"At least {MIN_ITEMS_PER_COMPETENCY} items for each required competency",
             "passed": all(c["items"] >= MIN_ITEMS_PER_COMPETENCY for c in coverage.values()) if coverage else False, "detail": None},
            {"id": "sources", "label": "Every authored item has source metadata", "passed": missing_sources == 0,
             "detail": f"{missing_sources} missing" if missing_sources else None},
        ]
        out.append({
            "id": assessment.id, "title": assessment.title, "purpose": assessment.purpose, "status": assessment.status,
            "published_at": assessment.published_at, "feedback_policy": assessment.feedback_policy,
            "job_role": {"id": role.id, "name": role.name} if role else None, "item_count": len(rows),
            "demo_seed_items": seeded, "coverage": sorted(coverage.values(), key=lambda c: c["competency"]["code"]),
            "checks": checks, "publishable": all(c["passed"] for c in checks),
            "is_demo": bool((assessment.blueprint or {}).get("demo_seed")),
        })
    return out


def audit_log(db: DbSession, current: CurrentUser, *, action: str | None, target_type: str | None, outcome: str | None,
              since: datetime | None, before_id: int | None, limit: int) -> dict:
    query = select(AuditLog).where(AuditLog.organization_id == current.user.organization_id)
    if action:
        query = query.where(AuditLog.action.like(f"{action}%"))
    if target_type:
        query = query.where(AuditLog.target_type == target_type)
    if outcome:
        query = query.where(AuditLog.outcome == outcome)
    if since:
        query = query.where(AuditLog.occurred_at >= since)
    if before_id:
        query = query.where(AuditLog.id < before_id)
    rows = list(db.scalars(query.order_by(AuditLog.id.desc()).limit(limit + 1)))
    more = len(rows) > limit
    rows = rows[:limit]
    actors = {u.id: u.display_name for u in db.scalars(select(User).where(User.id.in_({r.actor_user_id for r in rows if r.actor_user_id})))}
    actions = sorted({a.split(".")[0] for a in db.scalars(select(AuditLog.action).where(
        AuditLog.organization_id == current.user.organization_id).distinct())})
    return {
        "items": [{"id": r.id, "occurred_at": r.occurred_at, "actor": actors.get(r.actor_user_id) if r.actor_user_id else "System",
                   "actor_roles": list(r.actor_roles or []), "action": r.action, "target_type": r.target_type, "target_id": r.target_id,
                   "outcome": r.outcome, "before": r.before, "after": r.after, "reason": r.reason,
                   "correlation_id": r.correlation_id} for r in rows],
        "next_before_id": rows[-1].id if more and rows else None,
        "action_groups": actions,
    }
