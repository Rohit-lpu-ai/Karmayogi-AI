"""Local demo reset for synthetic accounts (DEC-052). Local and ci only.

Usage (from ``backend/``):

    python -m app.seed.demo_reset --org-code local-demo --email learner01@example.invalid [--email ...]
    python -m app.seed.demo_reset --org-code local-demo --all-synthetic [--clear-job-role]

Why: each account may take the baseline once (reassessment is P1), so a demo could only be shown once
per synthetic account.

What it does, for synthetic users only (``users.is_synthetic``):
- every non-voided assessment attempt becomes ``voided`` with a reason (rows are kept);
- the competency evidence of those attempts is voided through its existing void columns (append-only ledger);
- current estimates (``user_competencies``, a derived read model) are removed so the profile shows "not assessed";
- with ``--clear-job-role`` the job role is cleared so onboarding can be shown again
  (notice acknowledgements are append-only and stay);
- one audit record per user.

It is not a product feature, is refused outside local/ci and never touches non-synthetic accounts.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import AppEnv, get_settings
from app.core.db import get_sessionmaker
from app.core.logging import configure_logging
from app.modules.assessment.models import AssessmentAttempt
from app.modules.competency.models import CompetencyEvidence, UserCompetency
from app.modules.governance.service import record_audit
from app.modules.identity.models import User
from app.modules.learning.models import LearningPath, LearningPathItem, ProgressRecord
from app.modules.organization.models import Organization
from app.seed.canonical import SeedRefused

RESET_ENVS = {AppEnv.local, AppEnv.ci}
VOID_REASON = "Local demo reset of a synthetic account (DEC-052); not a correction of a real result."


def reset_demo_users(session: Session, org: Organization, app_env: AppEnv, *, emails: list[str] | None = None,
                     all_synthetic: bool = False, clear_job_role: bool = False) -> dict:
    if app_env not in RESET_ENVS:
        raise SeedRefused(f"Demo reset is not allowed in {app_env.value}")
    if bool(emails) == all_synthetic:
        raise SeedRefused("Give either --email (one or more) or --all-synthetic")

    query = select(User).where(User.organization_id == org.id)
    if emails:
        users = list(session.scalars(query.where(User.email.in_(emails))))
        found = {u.email.lower() for u in users}
        missing = sorted(e for e in emails if e.lower() not in found)
        if missing:
            raise SeedRefused(f"No account in this organisation for: {', '.join(missing)}")
        real = sorted(u.email for u in users if not u.is_synthetic)
        if real:
            raise SeedRefused(f"Refusing to reset non-synthetic accounts: {', '.join(real)}")
    else:
        # The insight cohort (pack demo-4) is not a demo account set and would empty the aggregate views.
        users = [u for u in session.scalars(query.where(User.is_synthetic)) if not u.email.lower().startswith("cohort-")]

    now = datetime.now(timezone.utc)
    totals: Counter = Counter()
    per_user = []
    for user in sorted(users, key=lambda u: u.email):
        counts: Counter = Counter()
        attempts = list(session.scalars(select(AssessmentAttempt).where(
            AssessmentAttempt.user_id == user.id, AssessmentAttempt.status != "voided")))
        for attempt in attempts:
            attempt.status, attempt.voided_at, attempt.void_reason = "voided", now, VOID_REASON
            counts["attempts_voided"] += 1
        session.flush()
        if attempts:
            for evidence in session.scalars(select(CompetencyEvidence).where(
                    CompetencyEvidence.attempt_id.in_([a.id for a in attempts]), CompetencyEvidence.voided_at.is_(None))):
                evidence.voided_at, evidence.void_reason = now, VOID_REASON
                counts["evidence_voided"] += 1
        counts["estimates_removed"] = session.execute(
            delete(UserCompetency).where(UserCompetency.user_id == user.id)).rowcount or 0
        # Learning progress and paths restart too; the append-only activity log keeps its history.
        path_ids = list(session.scalars(select(LearningPath.id).where(LearningPath.user_id == user.id)))
        if path_ids:
            session.execute(delete(LearningPathItem).where(LearningPathItem.learning_path_id.in_(path_ids)))
            counts["learning_paths_removed"] = session.execute(
                delete(LearningPath).where(LearningPath.id.in_(path_ids))).rowcount or 0
        progress_removed = session.execute(delete(ProgressRecord).where(ProgressRecord.user_id == user.id)).rowcount or 0
        if progress_removed:
            counts["progress_records_removed"] = progress_removed
        if clear_job_role and user.job_role_id is not None:
            user.job_role_id = None
            counts["job_role_cleared"] = 1
        session.flush()
        record_audit(session, organization_id=org.id, action="seed.demo_reset", target_type="user",
                     target_id=str(user.id), after=dict(counts), reason=VOID_REASON)
        totals.update(counts)
        per_user.append({"email": user.email, **dict(counts)})
    session.flush()
    return {"users": per_user, "totals": dict(totals)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reset synthetic demo accounts (local/ci only)")
    parser.add_argument("--org-code", required=True)
    parser.add_argument("--email", action="append", help="Synthetic account to reset (repeatable)")
    parser.add_argument("--all-synthetic", action="store_true", help="Reset every synthetic account in the organisation")
    parser.add_argument("--clear-job-role", action="store_true", help="Also clear the job role to replay onboarding")
    args = parser.parse_args(argv)

    settings = get_settings()
    configure_logging(settings.log_level)
    session = get_sessionmaker()()
    try:
        org = session.scalar(select(Organization).where(Organization.code == args.org_code))
        if org is None:
            raise SeedRefused(f"Unknown organisation code: {args.org_code}")
        report = reset_demo_users(session, org, settings.app_env, emails=args.email, all_synthetic=args.all_synthetic,
                                  clear_job_role=args.clear_job_role)
        session.commit()
    except SeedRefused as exc:
        session.rollback()
        print(json.dumps({"refused": str(exc)}), file=sys.stderr)
        return 2
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
