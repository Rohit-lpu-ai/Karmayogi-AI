"""Review workflow (Phase 4C; DATA_MODEL.md ReviewTask and Approval; plan assumption A-5).

Policy ``single-reviewer-v1``: one human decision closes a task; the person who submitted the work (or authored the
version under review) cannot decide it; deciders need the review capability for the task type. Every submission and
decision is written to the audit log, and approvals are append-only. Nothing is ever approved automatically.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as DbSession

from app.core.errors import ProblemError
from app.modules.governance.models import Approval, ReviewTask
from app.modules.governance.service import record_audit
from app.modules.identity.dependencies import CurrentUser
from app.modules.identity.models import User
from app.modules.identity.policy import has_capability

POLICY = {"policy": "single-reviewer-v1", "required_decisions": 1, "self_approval": "blocked"}
TASK_CAPABILITY = {"question_version_review": "questions.review", "course_review": "courses.review"}

# Called when a task is decided: (db, task, decision, current) -> None. Registered by the content services.
DecisionHandler = Callable[[DbSession, ReviewTask, str, CurrentUser], None]
_HANDLERS: dict[str, DecisionHandler] = {}


def register_handler(task_type: str, handler: DecisionHandler) -> None:
    _HANDLERS[task_type] = handler


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def open_task(db: DbSession, target_type: str, target_id: uuid.UUID) -> ReviewTask | None:
    return db.scalar(select(ReviewTask).where(ReviewTask.target_type == target_type, ReviewTask.target_id == target_id,
                                              ReviewTask.status == "open"))


def submit(db: DbSession, current: CurrentUser, *, task_type: str, target_type: str, target_id: uuid.UUID,
           target_version_id: uuid.UUID | None, title: str, note: str | None) -> ReviewTask:
    if open_task(db, target_type, target_id) is not None:
        raise ProblemError(409, "REVIEW_ALREADY_OPEN", "Already in review", "This item is already waiting for review.")
    task = ReviewTask(organization_id=current.user.organization_id, task_type=task_type, target_type=target_type,
                      target_id=target_id, target_version_id=target_version_id, title_snapshot=title[:300], status="open",
                      submitted_by=current.user.id, submitted_at=utcnow(), eligible_capability=TASK_CAPABILITY[task_type],
                      required_decisions=1, policy_snapshot=POLICY, submission_note=(note or "").strip() or None,
                      created_by=current.user.id)
    try:
        with db.begin_nested():
            db.add(task)
            db.flush()
    except IntegrityError:
        raise ProblemError(409, "REVIEW_ALREADY_OPEN", "Already in review", "This item is already waiting for review.") from None
    record_audit(db, organization_id=current.user.organization_id, action="review.submit", target_type=target_type,
                 target_id=str(target_id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"task_id": str(task.id), "task_type": task_type, "version_id": str(target_version_id) if target_version_id else None})
    return task


def cancel_open(db: DbSession, current: CurrentUser, target_type: str, target_id: uuid.UUID, reason: str) -> None:
    task = open_task(db, target_type, target_id)
    if task is None:
        return
    task.status, task.updated_by = "cancelled", current.user.id
    record_audit(db, organization_id=current.user.organization_id, action="review.cancel", target_type=target_type,
                 target_id=str(target_id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"task_id": str(task.id)}, reason=reason)


def list_tasks(db: DbSession, current: CurrentUser, *, status: str) -> list[dict]:
    caps = [cap for cap in set(TASK_CAPABILITY.values()) if has_capability(current.roles, cap)]
    query = select(ReviewTask).where(ReviewTask.organization_id == current.user.organization_id,
                                     ReviewTask.eligible_capability.in_(caps))
    if status != "all":
        query = query.where(ReviewTask.status == status)
    tasks = list(db.scalars(query.order_by(ReviewTask.submitted_at.desc()).limit(200)))
    people = {u.id: u for u in db.scalars(select(User).where(User.id.in_({t.submitted_by for t in tasks})))} if tasks else {}
    decisions = {}
    if tasks:
        for approval in db.scalars(select(Approval).where(Approval.review_task_id.in_([t.id for t in tasks]))):
            decisions[approval.review_task_id] = approval
    deciders = {u.id: u for u in db.scalars(select(User).where(User.id.in_({a.decided_by for a in decisions.values()})))} \
        if decisions else {}
    return [task_out(t, people.get(t.submitted_by), decisions.get(t.id), deciders, current) for t in tasks]


def task_out(task: ReviewTask, submitter: User | None, approval: Approval | None, deciders: dict, current: CurrentUser) -> dict:
    own = task.submitted_by == current.user.id
    return {
        "id": task.id, "task_type": task.task_type, "target_type": task.target_type, "target_id": task.target_id,
        "target_version_id": task.target_version_id, "title": task.title_snapshot, "status": task.status,
        "submitted_by": {"id": submitter.id, "display_name": submitter.display_name} if submitter else None,
        "submitted_at": task.submitted_at, "submission_note": task.submission_note, "decided_at": task.decided_at,
        "decision": {"decision": approval.decision, "reason": approval.reason_text, "decided_at": approval.created_at,
                     "decided_by": deciders[approval.decided_by].display_name if approval.decided_by in deciders else None}
        if approval else None,
        "can_decide": task.status == "open" and not own and has_capability(current.roles, task.eligible_capability),
        "blocked_reason": "You submitted this item, so another reviewer must decide it." if own and task.status == "open" else None,
        "policy": task.policy_snapshot, "row_version": task.row_version,
    }


def decide(db: DbSession, current: CurrentUser, task_id: uuid.UUID, decision: str, reason: str | None,
           row_version: int) -> ReviewTask:
    task = db.scalar(select(ReviewTask).where(ReviewTask.id == task_id, ReviewTask.organization_id == current.user.organization_id)
                     .with_for_update())
    if task is None or not has_capability(current.roles, task.eligible_capability):
        raise ProblemError(404, "NOT_FOUND", "Not found", "Review task not found.")
    if task.row_version != row_version:
        raise ProblemError(409, "STALE_VERSION", "Changed by someone else", "This task changed since you opened it. Reload.")
    if task.status != "open":
        raise ProblemError(409, "TASK_CLOSED", "Already decided", "This review task is no longer open.")
    if task.submitted_by == current.user.id:
        record_audit(db, organization_id=current.user.organization_id, action="review.decide", target_type=task.target_type,
                     target_id=str(task.target_id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                     outcome="denied", reason="self_approval_blocked")
        db.commit()
        raise ProblemError(403, "SELF_REVIEW_BLOCKED", "Another reviewer is needed",
                           "You submitted this item for review, so you cannot decide it. Ask another reviewer.")
    reason = (reason or "").strip() or None
    if decision != "approve" and not reason:
        raise ProblemError(422, "VALIDATION_FAILED", "Validation failed", "Give a reason so the author knows what to change.",
                           errors=[{"field": "reason", "code": "REASON_REQUIRED", "message": "Reason required."}])
    handler = _HANDLERS.get(task.task_type)
    if handler is None:
        raise ProblemError(500, "NO_HANDLER", "Review cannot be completed", "This review type is not configured.")
    handler(db, task, decision, current)  # may raise a guard error; nothing is written in that case
    db.add(Approval(organization_id=task.organization_id, review_task_id=task.id, sequence=1, decision=decision,
                    reason_text=reason, decided_by=current.user.id, target_version_id=task.target_version_id))
    task.status, task.decided_at, task.updated_by = "decided", utcnow(), current.user.id
    record_audit(db, organization_id=current.user.organization_id, action="review.decide", target_type=task.target_type,
                 target_id=str(task.target_id), actor_user_id=current.user.id, actor_roles=sorted(current.roles),
                 after={"task_id": str(task.id), "decision": decision}, reason=reason)
    db.commit()
    return task


def history(db: DbSession, target_type: str, target_id: uuid.UUID) -> list[dict]:
    tasks = list(db.scalars(select(ReviewTask).where(ReviewTask.target_type == target_type, ReviewTask.target_id == target_id)
                            .order_by(ReviewTask.submitted_at.desc())))
    if not tasks:
        return []
    approvals = {a.review_task_id: a for a in db.scalars(select(Approval).where(Approval.review_task_id.in_([t.id for t in tasks])))}
    user_ids = {t.submitted_by for t in tasks} | {a.decided_by for a in approvals.values()}
    people = {u.id: u.display_name for u in db.scalars(select(User).where(User.id.in_(user_ids)))}
    return [{
        "task_id": t.id, "status": t.status, "version_id": t.target_version_id, "submitted_at": t.submitted_at,
        "submitted_by": people.get(t.submitted_by), "note": t.submission_note,
        "decision": approvals[t.id].decision if t.id in approvals else None,
        "reason": approvals[t.id].reason_text if t.id in approvals else None,
        "decided_by": people.get(approvals[t.id].decided_by) if t.id in approvals else None,
        "decided_at": t.decided_at,
    } for t in tasks]
