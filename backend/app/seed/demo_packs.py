"""Versioned DEMO seed packs (DEC-052). Local and ci only.

Why: the original demo seed (DEC-045) is idempotent *as a unit* - it returns as soon as its
framework exists - so richer synthetic content could never reach a database that already ran it.

How it works:
- every pack has a ``code`` (``demo-1``, later ``demo-2`` ...) and an integer ``version``;
- ``seed_pack_applications`` stores, per organisation, the version of each pack already applied;
- a pack runs when it has never been applied or its registered version is lower than the pack's version;
  its ``apply`` function must therefore be additive and safe to re-run (create what is missing only);
- a database that ran the pre-registry demo seed is *adopted*: the pack's ``detect`` finds its content,
  the application row is written and nothing is re-created.

Packs never touch imported official records, and every pack application is audited.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.modules.competency.models import CompetencyFramework
from app.modules.governance.service import record_audit
from app.modules.organization.models import Organization
from app.modules.platform.models import SeedPackApplication
from app.seed import demo_content, demo_pack_2, demo_pack_3, demo_pack_4
from app.seed.canonical import SeedRefused

DEMO_PACK_ENVS = {AppEnv.local, AppEnv.ci}


@dataclass(frozen=True)
class DemoPack:
    code: str
    version: int
    title: str
    apply: Callable[[Session, Organization, AppEnv], Counter]
    detect: Callable[[Session, Organization], bool]


def _demo_1_present(session: Session, org: Organization) -> bool:
    return session.scalar(select(CompetencyFramework.id).where(
        CompetencyFramework.organization_id == org.id, CompetencyFramework.code == demo_content.FRAMEWORK_CODE,
    )) is not None


# Ordered: later packs may rely on earlier ones.
PACKS: tuple[DemoPack, ...] = (
    DemoPack(
        code="demo-1", version=1,
        title="Vertical slice 1: DEMO framework, 1 job role, 2 competencies, 10 arithmetic items, 3 courses",
        apply=demo_content.seed_demo_content, detect=_demo_1_present,
    ),
    DemoPack(
        code="demo-2", version=1,
        title="Statistical practice: 8 competencies, 3 job roles, 40 scenario items, 3 assessments, 12 courses",
        apply=demo_pack_2.seed_demo_pack_2, detect=lambda session, org: False,  # never seeded before the registry
    ),
    DemoPack(
        code="demo-3", version=1,
        title="Learning content: 2 modules and 4 lessons for each demo-2 course, completion criteria, prerequisites",
        apply=demo_pack_3.seed_demo_pack_3, detect=lambda session, org: False,
    ),
    DemoPack(
        code="demo-4", version=1,
        title="Synthetic cohort: 38 learners in 3 departments with scored baselines and some lesson progress (aggregates only)",
        apply=demo_pack_4.seed_demo_pack_4, detect=lambda session, org: False,
    ),
)


def pack_status(session: Session, org: Organization) -> list[dict]:
    applied = {row.pack_code: row for row in session.scalars(
        select(SeedPackApplication).where(SeedPackApplication.organization_id == org.id))}
    out = []
    for pack in PACKS:
        row = applied.get(pack.code)
        out.append({
            "code": pack.code, "version": pack.version, "title": pack.title,
            "applied_version": row.pack_version if row else None,
            "state": "not_applied" if row is None else ("up_to_date" if row.pack_version >= pack.version else "outdated"),
        })
    return out


CONTENT_PACKS = frozenset({"demo-1", "demo-2", "demo-3"})  # everything except the insight cohort


def apply_demo_packs(session: Session, org: Organization, app_env: AppEnv,
                     codes: frozenset[str] | set[str] | None = None) -> dict[str, dict]:
    """Apply every registered pack (or only ``codes``) that is missing or outdated. Returns a per-pack report."""
    if app_env not in DEMO_PACK_ENVS:
        raise SeedRefused(f"DEMO packs are not allowed in {app_env.value}")
    report: dict[str, dict] = {}
    for pack in PACKS:
        if codes is not None and pack.code not in codes:
            continue
        row = session.scalar(select(SeedPackApplication).where(
            SeedPackApplication.organization_id == org.id, SeedPackApplication.pack_code == pack.code))
        if row is not None and row.pack_version >= pack.version:
            report[pack.code] = {"action": "up_to_date", "version": row.pack_version}
            continue
        if row is None and pack.detect(session, org):
            action, created = "adopted", Counter()  # content from the pre-registry seed; nothing re-created
        else:
            action, created = ("upgraded" if row else "applied"), pack.apply(session, org, app_env)
        summary = {"action": action, "version": pack.version, "created": dict(created)}
        if row is None:
            session.add(SeedPackApplication(organization_id=org.id, pack_code=pack.code, pack_version=pack.version,
                                            summary=summary))
        else:
            row.pack_version, row.summary = pack.version, summary
        record_audit(session, organization_id=org.id, action="seed.demo_pack.apply", target_type="seed_pack",
                     target_id=f"{pack.code}@{pack.version}", after=summary,
                     reason="DEMO pack: synthetic content for local development, not official data (DEC-045, DEC-052)")
        session.flush()
        report[pack.code] = summary
    return report
