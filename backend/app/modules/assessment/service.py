"""Assessment service: delivery, answers, deterministic scoring on submit, results (MVP-06, MVP-07).

Answer keys never leave this module before an attempt is scored. Scoring is
server-side, uses the exact delivered question versions, and writes the evidence
ledger and recomputed estimates in the same transaction as the submission.
"""

from __future__ import annotations

import random
import secrets
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession

from app.core.errors import ProblemError
from app.modules.assessment.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    AttemptQuestion,
    Question,
    QuestionOption,
    QuestionVersion,
)
from app.modules.competency import scoring
from app.modules.competency import service as competency_service
from app.modules.competency.models import Competency, CompetencyFramework
from app.modules.governance.service import record_audit
from app.modules.identity import service as identity_service
from app.modules.identity.models import User

OPTION_LABELS = ("A", "B", "C", "D")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def not_found(what: str) -> ProblemError:
    return ProblemError(404, "NOT_FOUND", "Not found", f"{what} not found.")


# --- Pure delivery plan -------------------------------------------------------


@dataclass(frozen=True)
class PlannedQuestion:
    question_version_id: str
    position: int
    option_order: tuple[str, ...]


def delivery_plan(seed: int, question_version_ids: Sequence[str], labels: Sequence[str] = OPTION_LABELS) -> list[PlannedQuestion]:
    """Question and option order reconstructible from the stored seed (ASM-014)."""
    rng = random.Random(seed)
    ordered = sorted(question_version_ids)
    rng.shuffle(ordered)
    plan = []
    for position, version_id in enumerate(ordered, start=1):
        option_order = list(labels)
        rng.shuffle(option_order)
        plan.append(PlannedQuestion(version_id, position, tuple(option_order)))
    return plan


# --- Queries -------------------------------------------------------------------


def is_demo_assessment(assessment: Assessment) -> bool:
    return bool((assessment.blueprint or {}).get("demo_seed"))


def _assessment_in_org(db: DbSession, user: User, assessment_id: uuid.UUID) -> Assessment:
    assessment = db.scalar(select(Assessment).where(Assessment.id == assessment_id,
                                                    Assessment.organization_id == user.organization_id))
    if assessment is None or assessment.status != "published":
        raise not_found("Assessment")
    return assessment


def _owned_attempt(db: DbSession, user: User, attempt_id: uuid.UUID, *, lock: bool = False) -> AssessmentAttempt:
    query = select(AssessmentAttempt).where(AssessmentAttempt.id == attempt_id,
                                            AssessmentAttempt.organization_id == user.organization_id,
                                            AssessmentAttempt.user_id == user.id)
    if lock:
        query = query.with_for_update()
    attempt = db.scalar(query)
    if attempt is None:  # other users' attempts are indistinguishable from missing ones
        raise not_found("Attempt")
    return attempt


def _approved_pool(db: DbSession, assessment: Assessment) -> list[QuestionVersion]:
    """Only a question's currently approved version is deliverable (M-11 guard at delivery time)."""
    return list(db.scalars(
        select(QuestionVersion)
        .join(AssessmentQuestion, AssessmentQuestion.question_version_id == QuestionVersion.id)
        .join(Question, Question.id == QuestionVersion.question_id)
        .where(AssessmentQuestion.assessment_id == assessment.id, Question.status == "approved",
               Question.approved_version_id == QuestionVersion.id)
    ))


def available_assessments(db: DbSession, user: User) -> list[dict]:
    if user.job_role_id is None:
        return []
    assessments = db.scalars(select(Assessment).where(
        Assessment.organization_id == user.organization_id, Assessment.status == "published",
        Assessment.purpose == "pre", Assessment.job_role_id == user.job_role_id,
    ).order_by(Assessment.title)).all()
    out = []
    for assessment in assessments:
        attempts = db.scalars(select(AssessmentAttempt).where(AssessmentAttempt.assessment_id == assessment.id,
                                                              AssessmentAttempt.user_id == user.id)
                              .order_by(AssessmentAttempt.started_at.desc())).all()
        latest = attempts[0] if attempts else None
        out.append({
            "id": assessment.id, "title": assessment.title, "purpose": assessment.purpose,
            "feedback_policy": assessment.feedback_policy, "question_count": len(_approved_pool(db, assessment)),
            "is_demo": is_demo_assessment(assessment),
            "latest_attempt": {"id": latest.id, "status": latest.status} if latest else None,
        })
    return out


# --- Commands ------------------------------------------------------------------


def start_or_resume(db: DbSession, user: User, assessment_id: uuid.UUID) -> tuple[AssessmentAttempt, bool]:
    assessment = _assessment_in_org(db, user, assessment_id)
    if identity_service.notice_acknowledged(db, user) is None:
        raise ProblemError(409, "NOTICE_NOT_ACKNOWLEDGED", "Notice not acknowledged",
                           "Read and acknowledge the privacy and AI-use notice before starting an assessment.")
    if user.job_role_id is None:
        raise ProblemError(409, "JOB_ROLE_REQUIRED", "Select a job role first",
                           "Choose your job role before starting the baseline assessment.")
    if assessment.purpose == "pre" and assessment.job_role_id != user.job_role_id:
        raise ProblemError(409, "ASSESSMENT_NOT_FOR_JOB_ROLE", "Assessment not for your job role",
                           "This baseline assessment belongs to a different job role.")

    existing = db.scalars(select(AssessmentAttempt).where(AssessmentAttempt.assessment_id == assessment.id,
                                                          AssessmentAttempt.user_id == user.id)).all()
    open_attempt = next((a for a in existing if a.status == "in_progress"), None)
    if open_attempt is not None:
        return open_attempt, False
    if any(a.status in ("submitted", "scored") for a in existing):
        # Reassessment and post-assessments are P1 (MVP_SCOPE.md MVP-06).
        raise ProblemError(409, "ASSESSMENT_ALREADY_COMPLETED", "Assessment already completed",
                           "You have already completed this assessment. Reassessment is not available yet.")

    pool = _approved_pool(db, assessment)
    if not pool:
        raise ProblemError(409, "ASSESSMENT_HAS_NO_QUESTIONS", "Assessment unavailable",
                           "This assessment has no approved questions yet.")
    attempt = AssessmentAttempt(organization_id=user.organization_id, assessment_id=assessment.id, user_id=user.id,
                                status="in_progress", seed=secrets.randbits(62), started_at=utcnow(),
                                created_by=user.id, updated_by=user.id)
    try:
        with db.begin_nested():
            db.add(attempt)
            db.flush()
    except IntegrityError:
        # A concurrent request created the open attempt first.
        db.expire_all()
        return next(a for a in db.scalars(select(AssessmentAttempt).where(
            AssessmentAttempt.assessment_id == assessment.id, AssessmentAttempt.user_id == user.id,
            AssessmentAttempt.status == "in_progress"))), False
    for planned in delivery_plan(attempt.seed, [str(v.id) for v in pool]):
        db.add(AttemptQuestion(organization_id=user.organization_id, attempt_id=attempt.id,
                               question_version_id=uuid.UUID(planned.question_version_id),
                               position=planned.position, option_order=list(planned.option_order)))
    db.commit()
    return attempt, True


def _delivered(db: DbSession, attempt: AssessmentAttempt) -> list[AttemptQuestion]:
    return list(db.scalars(select(AttemptQuestion).where(AttemptQuestion.attempt_id == attempt.id)
                           .order_by(AttemptQuestion.position)))


def _options(db: DbSession, version_id: uuid.UUID) -> dict[str, QuestionOption]:
    return {o.label: o for o in db.scalars(select(QuestionOption).where(QuestionOption.question_version_id == version_id))}


def _answers(db: DbSession, attempt: AssessmentAttempt) -> dict[uuid.UUID, Answer]:
    return {a.question_version_id: a for a in db.scalars(select(Answer).where(Answer.attempt_id == attempt.id))}


def _competency_ref(db: DbSession, competency_id: uuid.UUID) -> dict:
    competency = db.get(Competency, competency_id)
    framework = db.get(CompetencyFramework, competency.framework_id)
    return competency_service.competency_ref(competency, framework)


def attempt_view(db: DbSession, user: User, attempt_id: uuid.UUID) -> dict:
    attempt = _owned_attempt(db, user, attempt_id)
    assessment = db.get(Assessment, attempt.assessment_id)
    answers = _answers(db, attempt)
    questions = []
    for delivered in _delivered(db, attempt):
        version = db.get(QuestionVersion, delivered.question_version_id)
        question = db.get(Question, version.question_id)
        options = _options(db, version.id)
        answer = answers.get(version.id)
        questions.append({
            "question_version_id": version.id,
            "position": delivered.position,
            "stem": version.stem,
            "difficulty": version.difficulty,
            "competency": _competency_ref(db, version.competency_id),
            "is_demo": question.origin == "demo_seed",
            # Only id, label and text: is_correct is never serialised before scoring.
            "options": [{"id": options[label].id, "label": label, "text": options[label].text}
                        for label in delivered.option_order],
            "selected_option_id": answer.selected_option_id if answer else None,
        })
    return {
        "id": attempt.id, "status": attempt.status, "started_at": attempt.started_at,
        "submitted_at": attempt.submitted_at,
        "assessment": {"id": assessment.id, "title": assessment.title, "purpose": assessment.purpose,
                       "feedback_policy": assessment.feedback_policy, "is_demo": is_demo_assessment(assessment)},
        "questions": questions,
        "answered_count": sum(1 for q in questions if q["selected_option_id"] is not None),
        "question_count": len(questions),
    }


def save_answer(db: DbSession, user: User, attempt_id: uuid.UUID, question_version_id: uuid.UUID,
                selected_option_id: uuid.UUID | None) -> dict:
    attempt = _owned_attempt(db, user, attempt_id, lock=True)
    if attempt.status != "in_progress":
        raise ProblemError(409, "ATTEMPT_NOT_IN_PROGRESS", "Attempt closed", "This attempt has already been submitted.")
    delivered = db.scalar(select(AttemptQuestion).where(AttemptQuestion.attempt_id == attempt.id,
                                                        AttemptQuestion.question_version_id == question_version_id))
    if delivered is None:
        raise not_found("Question in this attempt")
    if selected_option_id is not None:
        option = db.get(QuestionOption, selected_option_id)
        if option is None or option.question_version_id != question_version_id:
            raise ProblemError(422, "INVALID_OPTION", "Validation failed", "The selected option does not belong to this question.",
                               errors=[{"field": "selected_option_id", "code": "INVALID_OPTION",
                                        "message": "Option does not belong to this question."}])
    answer = db.scalar(select(Answer).where(Answer.attempt_id == attempt.id, Answer.question_version_id == question_version_id))
    now = utcnow()
    if answer is None:
        answer = Answer(organization_id=user.organization_id, attempt_id=attempt.id,
                        question_version_id=question_version_id, created_by=user.id)
        db.add(answer)
    answer.selected_option_id = selected_option_id
    answer.answered_at = now if selected_option_id is not None else None
    answer.updated_by = user.id
    db.commit()
    return {"question_version_id": question_version_id, "selected_option_id": selected_option_id, "saved_at": now}


def submit(db: DbSession, user: User, attempt_id: uuid.UUID, actor_roles: Sequence[str]) -> AssessmentAttempt:
    attempt = _owned_attempt(db, user, attempt_id, lock=True)
    if attempt.status != "in_progress":
        raise ProblemError(409, "ATTEMPT_NOT_IN_PROGRESS", "Attempt already submitted",
                           "This attempt has already been submitted.")
    assessment = db.get(Assessment, attempt.assessment_id)
    now = utcnow()
    answers = _answers(db, attempt)
    total_weight = Decimal("0")
    earned = Decimal("0")
    competencies: set[uuid.UUID] = set()

    for delivered in _delivered(db, attempt):
        version = db.get(QuestionVersion, delivered.question_version_id)
        correct_ids = {o.id for o in _options(db, version.id).values() if o.is_correct}
        answer = answers.get(version.id)
        if answer is None:  # unanswered questions are scored as incorrect
            answer = Answer(organization_id=user.organization_id, attempt_id=attempt.id,
                            question_version_id=version.id, created_by=user.id)
            db.add(answer)
        answer.is_correct = answer.selected_option_id in correct_ids
        answer.scored_at = now
        db.flush()
        weight = scoring.weight_for(version.difficulty)
        total_weight += weight
        earned += weight if answer.is_correct else Decimal("0")
        competency_service.record_answer_evidence(
            db, user=user, attempt_id=attempt.id, answer_id=answer.id, question_version_id=version.id,
            competency_id=version.competency_id, difficulty=version.difficulty, is_correct=answer.is_correct,
        )
        competencies.add(version.competency_id)

    has_baseline = db.scalar(select(AssessmentAttempt.id).where(AssessmentAttempt.user_id == user.id,
                                                                AssessmentAttempt.is_baseline))
    attempt.status = "scored"
    attempt.submitted_at = now
    attempt.scored_at = now
    attempt.score_total = (earned / total_weight).quantize(scoring.SCORE_QUANTUM, ROUND_HALF_EVEN) if total_weight else Decimal("0")
    attempt.is_baseline = assessment.purpose == "pre" and has_baseline is None
    attempt.updated_by = user.id
    db.flush()
    competency_service.recompute_from_attempt(db, user, attempt.id, competencies)
    record_audit(db, organization_id=user.organization_id, action="attempt.submit", target_type="assessment_attempt",
                 target_id=str(attempt.id), actor_user_id=user.id, actor_roles=actor_roles,
                 after={"status": "scored", "score_total": str(attempt.score_total), "is_baseline": attempt.is_baseline,
                        "method_version": scoring.METHOD_VERSION})
    db.commit()
    return attempt


def result_view(db: DbSession, user: User, attempt_id: uuid.UUID) -> dict:
    attempt = _owned_attempt(db, user, attempt_id)
    if attempt.status != "scored":
        raise ProblemError(409, "ATTEMPT_NOT_SCORED", "Result not available", "Submit the attempt to see its result.")
    assessment = db.get(Assessment, attempt.assessment_id)
    policy = assessment.feedback_policy
    answers = _answers(db, attempt)
    by_competency: dict[uuid.UUID, list[scoring.EvidenceItem]] = {}
    questions = []
    for delivered in _delivered(db, attempt):
        version = db.get(QuestionVersion, delivered.question_version_id)
        options = _options(db, version.id)
        answer = answers[version.id]
        by_competency.setdefault(version.competency_id, []).append(
            scoring.EvidenceItem(str(version.id), version.difficulty, bool(answer.is_correct)))
        item = {"question_version_id": version.id, "position": delivered.position, "stem": version.stem,
                "competency_id": version.competency_id, "selected_option_id": answer.selected_option_id}
        if policy in ("correctness", "correctness_and_explanations"):
            item["is_correct"] = answer.is_correct
        if policy == "correctness_and_explanations":
            correct = next(o for o in options.values() if o.is_correct)
            item["correct_option_id"] = correct.id
            item["explanation"] = version.explanation
        questions.append(item)

    competencies = []
    for competency_id, items in sorted(by_competency.items(), key=lambda kv: str(kv[0])):
        competency = db.get(Competency, competency_id)
        estimate = scoring.compute_estimate(items, competency_service.framework_levels(db, competency.framework_id))
        competencies.append({
            "competency": _competency_ref(db, competency_id), "score": estimate.score,
            "level_number": estimate.level_number, "evidence_band": estimate.evidence_band,
            "evidence_count": estimate.evidence_count, "thresholds_status": estimate.thresholds_status,
            "method_version": estimate.method_version,
        })
    competencies.sort(key=lambda c: c["competency"]["code"])
    return {
        "attempt_id": attempt.id, "status": attempt.status, "scored_at": attempt.scored_at,
        "score_total": attempt.score_total, "is_baseline": attempt.is_baseline, "feedback_policy": policy,
        "assessment": {"id": assessment.id, "title": assessment.title, "is_demo": is_demo_assessment(assessment)},
        "competencies": competencies, "questions": questions,
        "notice": "Development guidance only - not an appraisal or eligibility decision.",
    }
