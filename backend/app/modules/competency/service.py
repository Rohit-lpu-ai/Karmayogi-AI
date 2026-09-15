"""Competency service: role requirements, evidence ledger, deterministic estimates and gaps."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.core.errors import ProblemError
from app.modules.competency import scoring
from app.modules.competency.models import (
    Competency,
    CompetencyEvidence,
    CompetencyFramework,
    CompetencyLevel,
    RoleCompetency,
    UserCompetency,
)
from app.modules.identity.models import User
from app.modules.organization.models import JobRole


@dataclass(frozen=True)
class Requirement:
    mapping: RoleCompetency
    competency: Competency
    framework: CompetencyFramework
    levels: tuple[scoring.LevelThreshold, ...]

    @property
    def max_level_span(self) -> int:
        numbers = [lvl.level_number for lvl in self.levels]
        return max(numbers) - min(numbers) if numbers else 0


def job_role_in_org(db: DbSession, organization_id: uuid.UUID, job_role_id: uuid.UUID) -> JobRole:
    role = db.scalar(select(JobRole).where(JobRole.id == job_role_id, JobRole.organization_id == organization_id))
    if role is None:
        raise ProblemError(404, "NOT_FOUND", "Not found", "Job role not found.")
    return role


def framework_levels(db: DbSession, framework_id: uuid.UUID) -> tuple[scoring.LevelThreshold, ...]:
    rows = db.scalars(select(CompetencyLevel).where(CompetencyLevel.framework_id == framework_id)
                      .order_by(CompetencyLevel.level_number)).all()
    return tuple(scoring.LevelThreshold(r.level_number, r.label, r.min_score, r.threshold_status, r.description) for r in rows)


def role_requirements(db: DbSession, organization_id: uuid.UUID, job_role_id: uuid.UUID) -> list[Requirement]:
    """Approved mappings only: draft or retired mappings never drive assessments or gaps (MVP-05)."""
    rows = db.execute(
        select(RoleCompetency, Competency, CompetencyFramework)
        .join(Competency, Competency.id == RoleCompetency.competency_id)
        .join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
        .where(RoleCompetency.organization_id == organization_id, RoleCompetency.job_role_id == job_role_id,
               RoleCompetency.status == "approved", Competency.status == "active")
        .order_by(Competency.code)
    ).all()
    levels_cache: dict[uuid.UUID, tuple[scoring.LevelThreshold, ...]] = {}
    out = []
    for mapping, competency, framework in rows:
        if framework.id not in levels_cache:
            levels_cache[framework.id] = framework_levels(db, framework.id)
        out.append(Requirement(mapping, competency, framework, levels_cache[framework.id]))
    return out


def record_answer_evidence(
    db: DbSession, *, user: User, attempt_id: uuid.UUID, answer_id: uuid.UUID, question_version_id: uuid.UUID,
    competency_id: uuid.UUID, difficulty: str, is_correct: bool,
) -> None:
    db.add(CompetencyEvidence(
        organization_id=user.organization_id, user_id=user.id, competency_id=competency_id,
        evidence_type="assessment_answer", attempt_id=attempt_id, answer_id=answer_id,
        question_version_id=question_version_id, difficulty_weight=scoring.weight_for(difficulty), is_correct=is_correct,
    ))


def _weight_to_difficulty(weight: Decimal) -> str:
    for difficulty, value in scoring.DIFFICULTY_WEIGHTS.items():
        if value == weight:
            return difficulty
    raise ValueError(f"unknown difficulty weight {weight}")


def recompute_from_attempt(db: DbSession, user: User, attempt_id: uuid.UUID, competency_ids: set[uuid.UUID]) -> None:
    """Recompute estimates from the just-scored attempt, which is the most recent scored attempt (score-v1 step 1)."""
    now = datetime.now(timezone.utc)
    requirements = {r.competency.id: r for r in role_requirements(db, user.organization_id, user.job_role_id)} \
        if user.job_role_id else {}
    for competency_id in sorted(competency_ids, key=str):
        competency = db.get(Competency, competency_id)
        rows = db.scalars(select(CompetencyEvidence).where(
            CompetencyEvidence.user_id == user.id, CompetencyEvidence.competency_id == competency_id,
            CompetencyEvidence.attempt_id == attempt_id, CompetencyEvidence.evidence_type == "assessment_answer",
            CompetencyEvidence.voided_at.is_(None),
        )).all()
        items = [scoring.EvidenceItem(str(r.question_version_id), _weight_to_difficulty(r.difficulty_weight),
                                      bool(r.is_correct)) for r in rows]
        estimate = scoring.compute_estimate(items, framework_levels(db, competency.framework_id))
        requirement = requirements.get(competency_id)
        values = dict(
            job_role_id=user.job_role_id,
            role_mapping_version=requirement.mapping.mapping_version if requirement else None,
            score=estimate.score, level_number=estimate.level_number, evidence_band=estimate.evidence_band,
            evidence_count=estimate.evidence_count, method_version=estimate.method_version,
            explanation=scoring.explanation(estimate, str(attempt_id)), is_stale=False, computed_at=now,
        )
        current = db.scalar(select(UserCompetency).where(UserCompetency.user_id == user.id,
                                                         UserCompetency.competency_id == competency_id))
        if current is None:
            db.add(UserCompetency(organization_id=user.organization_id, user_id=user.id, competency_id=competency_id,
                                  **values))
        else:
            for key, value in values.items():
                setattr(current, key, value)
    db.flush()


def competency_ref(competency: Competency, framework: CompetencyFramework) -> dict:
    return {
        "id": competency.id, "code": competency.code, "name": competency.name,
        "framework_code": framework.code, "framework_status": framework.status,
        # Restricted frameworks (CSCD) never store a description, so this is null for them by construction.
        "description": competency.description,
        "is_demo": is_demo_code(competency.code) or is_demo_code(framework.code),
    }


def _estimates_by_competency(db: DbSession, user: User) -> dict[uuid.UUID, UserCompetency]:
    return {uc.competency_id: uc for uc in db.scalars(select(UserCompetency).where(UserCompetency.user_id == user.id))}


def require_job_role(db: DbSession, user: User) -> JobRole:
    if user.job_role_id is None:
        raise ProblemError(409, "JOB_ROLE_REQUIRED", "Select a job role first",
                           "Choose your job role to see requirements, results and recommendations.")
    return job_role_in_org(db, user.organization_id, user.job_role_id)


def competency_gaps(db: DbSession, user: User) -> dict:
    job_role = require_job_role(db, user)
    estimates = _estimates_by_competency(db, user)
    items = []
    for requirement in role_requirements(db, user.organization_id, job_role.id):
        estimate = estimates.get(requirement.competency.id)
        result = scoring.classify_gap(
            requirement.mapping.required_level_number,
            estimate.level_number if estimate else None,
            estimate.evidence_band if estimate else None,
        )
        items.append({
            "competency": competency_ref(requirement.competency, requirement.framework),
            "required_level": requirement.mapping.required_level_number,
            "estimated_level": estimate.level_number if estimate else None,
            "score": estimate.score if estimate else None,
            "evidence_band": estimate.evidence_band if estimate else None,
            "evidence_count": estimate.evidence_count if estimate else 0,
            "status": result.status,
            "gap": result.gap,
            "max_level_span": requirement.max_level_span,
        })
    order = {"gap": 0, "insufficient_evidence": 1, "level_unavailable": 2, "not_assessed": 3, "meets_requirement": 4}
    items.sort(key=lambda i: (order[i["status"]], -(i["gap"] or 0), i["competency"]["code"]))
    summary = {status: sum(1 for i in items if i["status"] == status) for status in order}
    return {
        "job_role": {"id": job_role.id, "name": job_role.name, "code": job_role.code, "description": job_role.description,
                     "is_demo": is_demo_code(job_role.code)},
        "method_version": scoring.METHOD_VERSION,
        "gap_rule": "gap = required level - estimated level, shown only when evidence band is medium or high",
        "items": items,
        "summary": summary,
    }


def competency_profile(db: DbSession, user: User) -> dict:
    estimates = _estimates_by_competency(db, user)
    items = []
    for estimate in estimates.values():
        competency = db.get(Competency, estimate.competency_id)
        framework = db.get(CompetencyFramework, competency.framework_id)
        items.append({
            "competency": competency_ref(competency, framework),
            "score": estimate.score,
            "level_number": estimate.level_number,
            "evidence_band": estimate.evidence_band,
            "evidence_count": estimate.evidence_count,
            "method_version": estimate.method_version,
            "computed_at": estimate.computed_at,
            "explanation": estimate.explanation,
        })
    items.sort(key=lambda i: i["competency"]["code"])
    return {"method_version": scoring.METHOD_VERSION, "items": items}
