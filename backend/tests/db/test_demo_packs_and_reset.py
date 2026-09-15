"""Versioned DEMO packs and the local demo reset (DEC-052)."""

from __future__ import annotations

import json
import uuid
from collections import Counter

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.config import AppEnv
from app.modules.assessment.models import AssessmentAttempt
from app.modules.competency.models import CompetencyEvidence, UserCompetency
from app.modules.governance.models import AuditLog
from app.modules.identity.models import User
from app.modules.organization.models import Organization
from app.modules.platform.models import SeedPackApplication
from app.seed import demo_packs
from app.seed.canonical import SeedRefused
from app.seed.demo_content import seed_demo_content
from app.seed.demo_reset import reset_demo_users
from app.seed.demo_users import seed_demo_users
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, correct_options, factory, login, make_user, onboard, org_id, problem, start,
)

pytestmark = pytest.mark.db


def _new_org(db) -> Organization:
    org = Organization(code=f"packs-{uuid.uuid4().hex[:10]}", name=f"Packs test {uuid.uuid4().hex[:10]}")
    db.add(org)
    db.flush()
    seed_demo_users(db, org, AppEnv.ci, PASSWORD)
    return org


# --- Demo packs ----------------------------------------------------------------


def test_packs_apply_once_and_are_recorded(db_session):
    org = _new_org(db_session)
    first = demo_packs.apply_demo_packs(db_session, org, AppEnv.ci)
    assert first["demo-1"]["action"] == "applied" and first["demo-1"]["created"]["questions"] == 10
    row = db_session.scalar(select(SeedPackApplication).where(SeedPackApplication.organization_id == org.id))
    assert (row.pack_code, row.pack_version) == ("demo-1", 1)

    second = demo_packs.apply_demo_packs(db_session, org, AppEnv.ci)
    assert second == {"demo-1": {"action": "up_to_date", "version": 1}}
    assert demo_packs.pack_status(db_session, org)[0]["state"] == "up_to_date"
    audits = db_session.scalars(select(AuditLog).where(AuditLog.organization_id == org.id,
                                                       AuditLog.action == "seed.demo_pack.apply")).all()
    assert [a.target_id for a in audits] == ["demo-1@1"]


def test_pre_registry_demo_content_is_adopted_without_recreating(db_session):
    org = _new_org(db_session)
    seed_demo_content(db_session, org, AppEnv.ci)  # the seed as it ran before DEC-052
    report = demo_packs.apply_demo_packs(db_session, org, AppEnv.ci)
    assert report["demo-1"] == {"action": "adopted", "version": 1, "created": {}}


def test_newer_pack_version_is_applied_additively(db_session, monkeypatch):
    org = _new_org(db_session)
    demo_packs.apply_demo_packs(db_session, org, AppEnv.ci)
    calls = []

    def additive(session, organization, env):
        calls.append(organization.id)
        return Counter(new_items=2)

    bumped = demo_packs.DemoPack(code="demo-1", version=2, title="bumped", apply=additive,
                                 detect=lambda session, organization: True)
    monkeypatch.setattr(demo_packs, "PACKS", (bumped,))
    assert demo_packs.pack_status(db_session, org)[0]["state"] == "outdated"
    report = demo_packs.apply_demo_packs(db_session, org, AppEnv.ci)
    assert report["demo-1"] == {"action": "upgraded", "version": 2, "created": {"new_items": 2}}
    assert calls == [org.id]
    row = db_session.scalar(select(SeedPackApplication).where(SeedPackApplication.organization_id == org.id))
    assert row.pack_version == 2


@pytest.mark.parametrize("env", [AppEnv.staging, AppEnv.pilot, AppEnv.production])
def test_packs_refused_outside_local_and_ci(db_session, env):
    org = _new_org(db_session)
    with pytest.raises(SeedRefused):
        demo_packs.apply_demo_packs(db_session, org, env)


def test_pack_code_format_is_enforced(db_session):
    org = _new_org(db_session)
    db_session.add(SeedPackApplication(organization_id=org.id, pack_code="Bad Code", pack_version=1))
    with pytest.raises(IntegrityError):
        with db_session.begin_nested():
            db_session.flush()


# --- Demo reset -----------------------------------------------------------------


def _complete_baseline(client, factory, email) -> str:
    csrf = login(client, email)
    onboard(client, csrf)
    attempt = start(client, csrf)
    keys = correct_options(factory, attempt)
    for qv, (_, option_id, _) in keys.items():
        client.put(f"/api/v1/attempts/{attempt['id']}/answers/{qv}", json={"selected_option_id": option_id},
                   headers={"X-CSRF-Token": csrf}).raise_for_status()
    submitted = client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers={"X-CSRF-Token": csrf}).json()
    assert submitted["is_baseline"] is True
    return attempt["id"]


def test_reset_lets_a_synthetic_learner_take_a_new_baseline(client, factory, org_id):
    email = make_user(factory, org_id)
    old_attempt = _complete_baseline(client, factory, email)
    csrf = client.get("/api/v1/auth/session").json()["csrf_token"]
    problem(client.post(f"/api/v1/assessments/{client.get('/api/v1/assessments').json()[0]['id']}/attempts",
                        headers={"X-CSRF-Token": csrf}), 409, "ASSESSMENT_ALREADY_COMPLETED")

    with factory() as db:
        report = reset_demo_users(db, db.get(Organization, org_id), AppEnv.ci, emails=[email])
        db.commit()
    assert report["totals"] == {"attempts_voided": 1, "evidence_voided": 10, "estimates_removed": 2}

    with factory() as db:
        attempt = db.get(AssessmentAttempt, uuid.UUID(old_attempt))
        assert attempt.status == "voided" and attempt.voided_at and attempt.is_baseline  # history kept, not rewritten
        evidence = db.scalars(select(CompetencyEvidence).where(CompetencyEvidence.attempt_id == attempt.id)).all()
        assert len(evidence) == 10 and all(e.voided_at and e.void_reason for e in evidence)
        user = db.scalar(select(User).where(User.email == email))
        assert db.scalars(select(UserCompetency).where(UserCompetency.user_id == user.id)).all() == []
        assert db.scalar(select(AuditLog).where(AuditLog.action == "seed.demo_reset", AuditLog.target_id == str(user.id)))

    assert client.get("/api/v1/assessments").json()[0]["latest_attempt"] is None
    gaps = client.get("/api/v1/me/competency-gaps").json()
    assert {i["status"] for i in gaps["items"]} == {"not_assessed"}
    problem(client.get(f"/api/v1/attempts/{old_attempt}/result"), 409, "ATTEMPT_VOIDED")
    problem(client.get(f"/api/v1/attempts/{old_attempt}"), 409, "ATTEMPT_VOIDED")
    problem(client.post(f"/api/v1/attempts/{old_attempt}/submit", headers={"X-CSRF-Token": csrf}), 409, "ATTEMPT_VOIDED")

    new_attempt = start(client, csrf)
    assert new_attempt["id"] != old_attempt
    submitted = client.post(f"/api/v1/attempts/{new_attempt['id']}/submit", headers={"X-CSRF-Token": csrf}).json()
    assert submitted["is_baseline"] is True  # the voided baseline does not block a new one


def test_reset_can_clear_the_job_role(client, factory, org_id):
    email = make_user(factory, org_id)
    _complete_baseline(client, factory, email)
    with factory() as db:
        reset_demo_users(db, db.get(Organization, org_id), AppEnv.ci, emails=[email], clear_job_role=True)
        db.commit()
    me = client.get("/api/v1/me").json()
    assert me["job_role"] is None and me["notice"]["acknowledged_at"] is not None


def test_reset_refuses_real_accounts_unknown_emails_and_bad_options(factory, org_id):
    real = f"real-{uuid.uuid4().hex[:8]}@example.invalid"
    with factory() as db:
        db.add(User(organization_id=org_id, email=real, display_name="Real person", status="active", is_synthetic=False))
        db.commit()
        org = db.get(Organization, org_id)
        with pytest.raises(SeedRefused, match="non-synthetic"):
            reset_demo_users(db, org, AppEnv.ci, emails=[real])
        with pytest.raises(SeedRefused, match="No account"):
            reset_demo_users(db, org, AppEnv.ci, emails=["nobody@example.invalid"])
        with pytest.raises(SeedRefused, match="either"):
            reset_demo_users(db, org, AppEnv.ci)
        with pytest.raises(SeedRefused, match="either"):
            reset_demo_users(db, org, AppEnv.ci, emails=[real], all_synthetic=True)
        for env in (AppEnv.staging, AppEnv.pilot, AppEnv.production):
            with pytest.raises(SeedRefused, match="not allowed"):
                reset_demo_users(db, org, env, all_synthetic=True)
        db.rollback()


def test_all_synthetic_reset_skips_real_accounts(factory):
    with factory() as db:
        org = _new_org(db)
        db.add(User(organization_id=org.id, email="person@example.invalid", display_name="Real", status="active",
                    is_synthetic=False))
        db.flush()
        report = reset_demo_users(db, org, AppEnv.ci, all_synthetic=True)
        assert len(report["users"]) == 8 and all(u["email"] != "person@example.invalid" for u in report["users"])
        db.rollback()


def test_voided_attempt_requires_time_and_reason(factory, org_id):
    email = make_user(factory, org_id)
    with factory() as db:
        user = db.scalar(select(User).where(User.email == email))
        assessment_id = db.execute(text("SELECT id FROM assessments WHERE organization_id = :o"), {"o": org_id}).scalar()
        db.add(AssessmentAttempt(organization_id=org_id, assessment_id=assessment_id, user_id=user.id, status="voided",
                                 seed=1, started_at=user.created_at))
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()


def test_seed_cli_applies_packs_and_reset_cli_runs(test_database_url, migrated_engine, monkeypatch, capsys):
    from app.core import config, db
    from app.seed.__main__ import main as seed_main
    from app.seed.demo_reset import main as reset_main

    monkeypatch.setenv("DATABASE_URL", test_database_url)
    monkeypatch.setenv("APP_ENV", "ci")
    config.get_settings.cache_clear()
    db.get_engine.cache_clear()
    db.get_sessionmaker.cache_clear()
    code = f"cli-{uuid.uuid4().hex[:10]}"
    args = ["--org-code", code, "--org-name", f"CLI {code}", "--demo-users", "--demo-content"]
    try:
        assert seed_main(args) == 0
        assert json.loads(capsys.readouterr().out)["demo_packs"]["demo-1"]["action"] == "applied"
        assert seed_main(args) == 0
        assert json.loads(capsys.readouterr().out)["demo_packs"]["demo-1"]["action"] == "up_to_date"
        assert reset_main(["--org-code", code, "--all-synthetic"]) == 0
        assert len(json.loads(capsys.readouterr().out)["users"]) == 8
        assert reset_main(["--org-code", "no-such-org", "--all-synthetic"]) == 2
        assert "Unknown organisation" in capsys.readouterr().err
    finally:
        db.get_engine().dispose()
        config.get_settings.cache_clear()
        db.get_engine.cache_clear()
        db.get_sessionmaker.cache_clear()
