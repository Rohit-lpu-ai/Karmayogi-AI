"""Question authoring (Phase 4C): drafts, immutable versions, source references and review.

Lifecycle for human-authored questions: ``draft`` -> submit -> ``in_review`` -> approve (``approved``) | reject
(``rejected``) | request changes (back to ``draft``). Approved questions can be ``retired`` unless a published
assessment uses them. Every edit creates a new append-only version, so a decision always refers to exact content.

Guards: a question cannot be submitted without exactly one correct answer among 3-5 options, an explanation, and at
least one source reference. A ``synthetic`` reference must say the scenario is invented. External references are the
author's claim and are always shown as "author-provided, not verified" - they are never presented as citations.
"""

from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app.core.demo import is_demo_code
from app.core.errors import ProblemError
from app.modules.ai.local import StructuralQuestionValidator
from app.modules.assessment.models import (
    Assessment,
    AssessmentQuestion,
    Question,
    QuestionOption,
    QuestionSourceReference,
    QuestionVersion,
)
from app.modules.competency.models import Competency, CompetencyFramework
from app.modules.content.models import SourceRecord
from app.modules.content_admin import reviews
from app.modules.governance.models import ReviewTask
from app.modules.governance.service import record_audit
from app.modules.identity.dependencies import CurrentUser
from app.modules.identity.models import User
from app.seed.demo_content import content_hash

EDITABLE = ("draft", "rejected")
LETTERS = "ABCDE"


def _not_found() -> ProblemError:
    return ProblemError(404, "NOT_FOUND", "Not found", "Question not found.")


def _question(db: DbSession, current: CurrentUser, question_id: uuid.UUID, *, lock: bool = False) -> Question:
    query = select(Question).where(Question.id == question_id, Question.organization_id == current.user.organization_id)
    question = db.scalar(query.with_for_update() if lock else query)
    if question is None:
        raise _not_found()
    return question


def _competency(db: DbSession, current: CurrentUser, competency_id: uuid.UUID) -> tuple[Competency, CompetencyFramework]:
    row = db.execute(select(Competency, CompetencyFramework).join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
                     .where(Competency.id == competency_id, Competency.organization_id == current.user.organization_id)).first()
    if row is None:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Choose a competency from your organisation.",
                           errors=[{"field": "competency_id", "code": "UNKNOWN_COMPETENCY", "message": "Unknown competency."}])
    competency, framework = row
    if framework.definitions_restricted:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed",
                           "This competency's framework is licence-restricted; questions cannot quote or target it yet.",
                           errors=[{"field": "competency_id", "code": "RESTRICTED_FRAMEWORK", "message": "Restricted framework."}])
    return competency, framework


def _validate_content(body) -> None:
    errors = []
    options = [o for o in body.options]
    if not 3 <= len(options) <= 5:
        errors.append({"field": "options", "code": "OPTION_COUNT", "message": "Give 3 to 5 answer options."})
    if sum(1 for o in options if o.is_correct) != 1:
        errors.append({"field": "options", "code": "ONE_CORRECT", "message": "Mark exactly one option as correct."})
    texts = [" ".join(o.text.lower().split()) for o in options]
    if len(set(texts)) != len(texts):
        errors.append({"field": "options", "code": "DUPLICATE_OPTIONS", "message": "Options must be different."})
    if errors:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Check the answer options.", errors=errors)


def _validate_sources(db: DbSession, current: CurrentUser, sources) -> None:
    for index, source in enumerate(sources):
        field = f"sources.{index}"
        if source.source_kind == "source_record":
            record = db.scalar(select(SourceRecord.id).where(SourceRecord.id == source.source_record_id,
                                                             SourceRecord.organization_id == current.user.organization_id))
            if record is None:
                raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Choose a source record from the list.",
                                   errors=[{"field": field, "code": "UNKNOWN_SOURCE", "message": "Unknown source record."}])
        if source.source_kind == "external_reference" and not (source.title and source.publisher):
            raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "An external reference needs a title and publisher.",
                               errors=[{"field": field, "code": "REFERENCE_INCOMPLETE", "message": "Title and publisher required."}])
        if source.source_kind == "synthetic" and not (source.note or "").strip():
            raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Say that the scenario and figures are invented.",
                               errors=[{"field": field, "code": "SYNTHETIC_NOTE_REQUIRED", "message": "Note required."}])


def _new_version(db: DbSession, current: CurrentUser, question: Question, body, previous: QuestionVersion | None) -> QuestionVersion:
    competency, _ = _competency(db, current, body.competency_id)
    _validate_content(body)
    _validate_sources(db, current, body.sources)
    number = (db.scalar(select(func.max(QuestionVersion.version_number)).where(QuestionVersion.question_id == question.id)) or 0) + 1
    version = QuestionVersion(organization_id=question.organization_id, question_id=question.id, version_number=number,
                              stem=body.stem.strip(), explanation=body.explanation.strip(), difficulty=body.difficulty,
                              difficulty_confirmed=True, competency_id=competency.id,
                              content_hash=content_hash(body.stem, [o.text for o in body.options]),
                              edited_from_version_id=previous.id if previous else None,
                              human_edited_fields=["stem", "options", "explanation"] if previous else [],
                              created_by=current.user.id)
    db.add(version)
    db.flush()
    for position, option in enumerate(body.options):
        db.add(QuestionOption(organization_id=question.organization_id, question_version_id=version.id,
                              label=LETTERS[position], text=option.text.strip(), is_correct=option.is_correct, position=position + 1))
    for source in body.sources:
        db.add(QuestionSourceReference(organization_id=question.organization_id, question_version_id=version.id,
                                       source_kind=source.source_kind,
                                       source_record_id=source.source_record_id if source.source_kind == "source_record" else None,
                                       title=(source.title or "").strip() or None, publisher=(source.publisher or "").strip() or None,
                                       url=(source.url or "").strip() or None, locator=(source.locator or "").strip() or None,
                                       note=(source.note or "").strip() or None, created_by=current.user.id))
    question.current_version_id = version.id
    db.flush()
    return version


def create(db: DbSession, current: CurrentUser, body) -> dict:
    question = Question(organization_id=current.user.organization_id, origin="human_authored", status="draft", created_by=current.user.id)
    db.add(question)
    db.flush()
    version = _new_version(db, current, question, body, None)
    record_audit(db, organization_id=current.user.organization_id, action="question.create", target_type="question",
                 target_id=str(question.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"version": version.version_number, "sources": len(body.sources)})
    db.commit()
    return detail(db, current, question.id)


def update(db: DbSession, current: CurrentUser, question_id: uuid.UUID, body) -> dict:
    question = _question(db, current, question_id, lock=True)
    if question.row_version != body.row_version:
        raise ProblemError(409, "STALE_VERSION", "Changed by someone else", "This question changed since you opened it. Reload.")
    if question.status not in EDITABLE:
        raise ProblemError(409, "NOT_EDITABLE", "Cannot edit now",
                           "Only draft or rejected questions can be edited. Approved questions keep their reviewed content.")
    previous = db.get(QuestionVersion, question.current_version_id) if question.current_version_id else None
    version = _new_version(db, current, question, body, previous)
    if question.status == "rejected":
        question.status = "draft"
    question.updated_by = current.user.id
    record_audit(db, organization_id=current.user.organization_id, action="question.update", target_type="question",
                 target_id=str(question.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"version": version.version_number})
    db.commit()
    return detail(db, current, question.id)


def submit(db: DbSession, current: CurrentUser, question_id: uuid.UUID, note: str | None) -> dict:
    question = _question(db, current, question_id, lock=True)
    if question.status not in EDITABLE:
        raise ProblemError(409, "NOT_SUBMITTABLE", "Cannot submit", "Only draft or rejected questions can be sent for review.")
    version = db.get(QuestionVersion, question.current_version_id)
    sources = db.scalar(select(func.count()).select_from(QuestionSourceReference)
                        .where(QuestionSourceReference.question_version_id == version.id)) or 0
    if sources == 0:
        raise ProblemError(422, "SOURCE_REQUIRED", "Source metadata required",
                           "Add at least one source reference before sending this question for review.",
                           errors=[{"field": "sources", "code": "SOURCE_REQUIRED", "message": "At least one source is required."}])
    reviews.submit(db, current, task_type="question_version_review", target_type="question", target_id=question.id,
                   target_version_id=version.id, title=version.stem, note=note)
    question.status, question.updated_by = "in_review", current.user.id
    db.commit()
    return detail(db, current, question.id)


def withdraw(db: DbSession, current: CurrentUser, question_id: uuid.UUID) -> dict:
    question = _question(db, current, question_id, lock=True)
    if question.status != "in_review":
        raise ProblemError(409, "NOT_IN_REVIEW", "Not in review", "This question is not waiting for review.")
    reviews.cancel_open(db, current, "question", question.id, "withdrawn_by_author")
    question.status, question.updated_by = "draft", current.user.id
    db.commit()
    return detail(db, current, question.id)


def retire(db: DbSession, current: CurrentUser, question_id: uuid.UUID) -> dict:
    question = _question(db, current, question_id, lock=True)
    if question.status != "approved":
        raise ProblemError(409, "NOT_RETIRABLE", "Cannot retire", "Only approved questions can be retired.")
    in_published = db.scalar(select(func.count()).select_from(AssessmentQuestion)
                             .join(Assessment, Assessment.id == AssessmentQuestion.assessment_id)
                             .join(QuestionVersion, QuestionVersion.id == AssessmentQuestion.question_version_id)
                             .where(QuestionVersion.question_id == question.id, Assessment.status == "published")) or 0
    if in_published:
        raise ProblemError(409, "USED_IN_PUBLISHED_ASSESSMENT", "Question in use",
                           "A published assessment uses this question. It stays available until that assessment is retired.")
    question.status, question.updated_by = "retired", current.user.id
    record_audit(db, organization_id=current.user.organization_id, action="question.retire", target_type="question",
                 target_id=str(question.id), actor_user_id=current.user.id, actor_roles=sorted(current.roles))
    db.commit()
    return detail(db, current, question.id)


def _on_decision(db: DbSession, task: ReviewTask, decision: str, current: CurrentUser) -> None:
    question = db.scalar(select(Question).where(Question.id == task.target_id).with_for_update())
    version = db.get(QuestionVersion, task.target_version_id)
    if question is None or version is None or question.status != "in_review" or question.current_version_id != version.id:
        raise ProblemError(409, "TARGET_CHANGED", "Question changed", "The question changed after it was submitted. Reload.")
    if version.created_by == current.user.id:
        raise ProblemError(403, "SELF_REVIEW_BLOCKED", "Another reviewer is needed",
                           "You wrote this version of the question, so you cannot decide it. Ask another reviewer.")
    if decision == "approve":
        question.status, question.approved_version_id = "approved", version.id
    elif decision == "reject":
        question.status = "rejected"
    else:
        question.status = "draft"
    question.updated_by = current.user.id


reviews.register_handler("question_version_review", _on_decision)


# --- Reading ------------------------------------------------------------------------------------------------


def _sources_out(db: DbSession, version_ids: list[uuid.UUID]) -> dict[uuid.UUID, list[dict]]:
    if not version_ids:
        return {}
    rows = db.execute(select(QuestionSourceReference, SourceRecord)
                      .outerjoin(SourceRecord, SourceRecord.id == QuestionSourceReference.source_record_id)
                      .where(QuestionSourceReference.question_version_id.in_(version_ids))
                      .order_by(QuestionSourceReference.created_at)).all()
    out: dict[uuid.UUID, list[dict]] = {}
    for ref, record in rows:
        if ref.source_kind == "source_record" and record is not None:
            label, verified = record.attribution_text, record.review_verified
            status = "Imported source record, verified by a reviewer" if verified else "Imported source record, not yet verified"
        elif ref.source_kind == "external_reference":
            label, status = f"{ref.title} - {ref.publisher}", "Author-provided, not verified"
        else:
            label, status = "Synthetic scenario", "Invented for practice - not a citation"
        out.setdefault(ref.question_version_id, []).append({
            "id": ref.id, "source_kind": ref.source_kind, "label": label, "status": status,
            "source_record_id": ref.source_record_id, "title": ref.title, "publisher": ref.publisher, "url": ref.url,
            "locator": ref.locator, "note": ref.note,
        })
    return out


def list_questions(db: DbSession, current: CurrentUser, *, status: str | None, competency_id: uuid.UUID | None,
                   origin: str | None, q: str | None, page: int, page_size: int) -> dict:
    query = (select(Question, QuestionVersion, Competency)
             .join(QuestionVersion, QuestionVersion.id == Question.current_version_id)
             .join(Competency, Competency.id == QuestionVersion.competency_id)
             .where(Question.organization_id == current.user.organization_id))
    if status:
        query = query.where(Question.status == status)
    if competency_id:
        query = query.where(QuestionVersion.competency_id == competency_id)
    if origin:
        query = query.where(Question.origin == origin)
    if q:
        query = query.where(or_(QuestionVersion.stem.ilike(f"%{q.strip()}%"), Competency.name.ilike(f"%{q.strip()}%")))
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.execute(query.order_by(Question.updated_at.desc(), Question.id).offset((page - 1) * page_size).limit(page_size)).all()
    source_counts = dict(db.execute(select(QuestionSourceReference.question_version_id, func.count())
                                    .where(QuestionSourceReference.question_version_id.in_([v.id for _, v, _ in rows]))
                                    .group_by(QuestionSourceReference.question_version_id)).all()) if rows else {}
    status_counts = dict(db.execute(select(Question.status, func.count()).where(Question.organization_id == current.user.organization_id)
                                    .group_by(Question.status)).all())
    return {
        "items": [{"id": qn.id, "status": qn.status, "origin": qn.origin, "stem": v.stem, "difficulty": v.difficulty,
                   "version_number": v.version_number, "competency": {"id": c.id, "code": c.code, "name": c.name},
                   "source_count": source_counts.get(v.id, 0), "is_demo": qn.origin == "demo_seed" or is_demo_code(c.code),
                   "updated_at": qn.updated_at} for qn, v, c in rows],
        "total": total, "page": page, "page_size": page_size, "status_counts": status_counts,
    }


def detail(db: DbSession, current: CurrentUser, question_id: uuid.UUID) -> dict:
    question = _question(db, current, question_id)
    versions = list(db.scalars(select(QuestionVersion).where(QuestionVersion.question_id == question.id)
                               .order_by(QuestionVersion.version_number.desc())))
    current_version = next(v for v in versions if v.id == question.current_version_id)
    options = list(db.scalars(select(QuestionOption).where(QuestionOption.question_version_id == current_version.id)
                              .order_by(QuestionOption.position)))
    competency, framework = db.execute(select(Competency, CompetencyFramework)
                                       .join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
                                       .where(Competency.id == current_version.competency_id)).one()
    authors = {u.id: u.display_name for u in db.scalars(select(User).where(User.id.in_({v.created_by for v in versions if v.created_by})))}
    sources = _sources_out(db, [current_version.id])
    used_in = [{"id": a.id, "title": a.title, "status": a.status} for a in db.scalars(
        select(Assessment).join(AssessmentQuestion, AssessmentQuestion.assessment_id == Assessment.id)
        .join(QuestionVersion, QuestionVersion.id == AssessmentQuestion.question_version_id)
        .where(QuestionVersion.question_id == question.id).distinct())]
    task = reviews.open_task(db, "question", question.id)
    correct = next((i for i, o in enumerate(options) if o.is_correct), None)
    findings = StructuralQuestionValidator().validate(current_version.stem, [o.text for o in options], correct,
                                                      current_version.explanation)
    is_author = current_version.created_by == current.user.id or question.created_by == current.user.id
    return {
        "id": question.id, "status": question.status, "origin": question.origin, "row_version": question.row_version,
        "is_demo": question.origin == "demo_seed",
        "current_version": {
            "id": current_version.id, "version_number": current_version.version_number, "stem": current_version.stem,
            "explanation": current_version.explanation, "difficulty": current_version.difficulty,
            "competency": {"id": competency.id, "code": competency.code, "name": competency.name, "framework_code": framework.code},
            "options": [{"label": o.label, "text": o.text, "is_correct": o.is_correct} for o in options],
            "sources": sources.get(current_version.id, []),
            "created_at": current_version.created_at, "created_by": authors.get(current_version.created_by),
        },
        "approved_version_id": question.approved_version_id,
        "versions": [{"id": v.id, "version_number": v.version_number, "created_at": v.created_at,
                      "created_by": authors.get(v.created_by), "is_approved": v.id == question.approved_version_id} for v in versions],
        "reviews": reviews.history(db, "question", question.id),
        "open_task_id": task.id if task else None,
        "used_in_assessments": used_in,
        "quality_checks": {"method": StructuralQuestionValidator.method,
                           "findings": [{"code": f.code, "severity": f.severity, "message": f.message} for f in findings]},
        "actions": {
            "can_edit": question.status in EDITABLE and question.origin == "human_authored",
            "can_submit": question.status in EDITABLE and question.origin == "human_authored",
            "can_withdraw": question.status == "in_review" and is_author,
            "can_retire": question.status == "approved" and not any(a["status"] == "published" for a in used_in),
        },
    }


def authoring_options(db: DbSession, current: CurrentUser) -> dict:
    rows = db.execute(select(Competency, CompetencyFramework).join(CompetencyFramework, CompetencyFramework.id == Competency.framework_id)
                      .where(Competency.organization_id == current.user.organization_id, Competency.status == "active")
                      .order_by(CompetencyFramework.code, Competency.name)).all()
    records = db.scalars(select(SourceRecord).where(SourceRecord.organization_id == current.user.organization_id,
                                                    SourceRecord.canonical_dataset.in_(["documents", "competency_framework"]))
                         .order_by(SourceRecord.canonical_record_id))
    return {
        "competencies": [{"id": c.id, "code": c.code, "name": c.name, "framework_code": f.code,
                          "restricted": f.definitions_restricted} for c, f in rows],
        "source_records": [{"id": r.id, "label": r.attribution_text, "organisation": r.source_organisation,
                            "record_id": r.canonical_record_id, "verified": r.review_verified,
                            "licence_notes": r.licence_notes} for r in records],
        "difficulties": ["foundational", "intermediate", "advanced"],
    }
