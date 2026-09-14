"""Governance service: audit log writes (SECURITY_RESPONSIBLE_AI.md §11).

Audit rows are added to the caller's session so they commit or roll back with
the action they describe (fail closed).
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import correlation_id_var, redact
from app.modules.governance.models import AuditLog


def current_correlation_id() -> str:
    return correlation_id_var.get() or f"system-{uuid.uuid4().hex}"


def record_audit(
    session: Session,
    *,
    organization_id: uuid.UUID,
    action: str,
    target_type: str,
    outcome: str = "success",
    target_id: str | None = None,
    actor_user_id: uuid.UUID | None = None,
    actor_roles: Sequence[str] = (),
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    reason: str | None = None,
) -> AuditLog:
    entry = AuditLog(
        organization_id=organization_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        outcome=outcome,
        actor_user_id=actor_user_id,
        actor_roles=list(actor_roles),
        before=redact(before) if before is not None else None,
        after=redact(after) if after is not None else None,
        reason=reason,
        correlation_id=current_correlation_id(),
    )
    session.add(entry)
    return entry
