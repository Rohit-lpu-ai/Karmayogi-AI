"""Canonical dataset import: counts, provenance, licence guards, idempotency and refusals."""

from __future__ import annotations

import copy
import json
import uuid

import pytest
from sqlalchemy import func, select

from app.core.config import AppEnv
from app.modules.competency.models import Competency, CompetencyCluster, CompetencyFramework, CompetencyLevel
from app.modules.content.models import SourceRecord
from app.modules.governance.models import AuditLog
from app.modules.identity.models import User, UserAccessRole
from app.modules.platform.models import Topic
from app.modules.recommendation.models import Course, CourseTopic
from app.seed.canonical import CanonicalBundle, SeedRefused, load_canonical_bundle
from app.seed.demo_users import seed_demo_users
from app.seed.importer import import_canonical_datasets

pytestmark = pytest.mark.db

TABLES = (Topic, CompetencyFramework, CompetencyCluster, Competency, CompetencyLevel, SourceRecord, Course, CourseTopic,
          AuditLog)


@pytest.fixture(scope="module")
def bundle() -> CanonicalBundle:
    return load_canonical_bundle()


def _counts(session, org):
    return {m.__tablename__: session.scalar(select(func.count()).select_from(m).where(m.organization_id == org.id))
            for m in TABLES}


def test_validator_gate_passes_for_current_datasets(bundle):
    assert bundle.verdict == "VALID_FOR_DEVELOPMENT_NOT_RELEASABLE"


def test_import_counts(db_session, organization, bundle):
    report = import_canonical_datasets(db_session, organization, bundle)
    programmes = bundle.datasets["training_programmes"]["records"]
    expected_tags = sum(len(p.get("topic_tags") or []) for p in programmes)
    counts = _counts(db_session, organization)
    assert counts["topics"] == 23
    assert counts["competency_frameworks"] == 1
    assert counts["competency_clusters"] == 4
    assert counts["competencies"] == 25
    assert counts["competency_levels"] == 5
    assert counts["courses"] == 99
    assert counts["course_topics"] == expected_tags
    assert counts["source_records"] == 100  # 99 programmes + the CSCD framework
    assert counts["audit_logs"] == 3
    assert any("CSCD-2014-4.8" in w for w in report.warnings)


def test_restricted_content_and_review_state(db_session, organization, bundle):
    import_canonical_datasets(db_session, organization, bundle)
    framework = db_session.scalar(select(CompetencyFramework).where(CompetencyFramework.organization_id == organization.id))
    assert framework.definitions_restricted and framework.status == "draft"
    assert framework.approved_by is None
    competencies = db_session.scalars(select(Competency).where(Competency.framework_id == framework.id)).all()
    assert all(c.description is None for c in competencies)
    levels = db_session.scalars(select(CompetencyLevel).where(CompetencyLevel.framework_id == framework.id)).all()
    assert all(lvl.min_score is None and lvl.threshold_status == "provisional" for lvl in levels)
    courses = db_session.scalars(select(Course).where(Course.organization_id == organization.id)).all()
    assert all(c.review_status == "unreviewed" and c.external_url is None for c in courses)
    assert {c.schedule_status for c in courses} == {"Tentative"}
    topics = db_session.scalars(select(Topic).where(Topic.organization_id == organization.id)).all()
    assert all(t.review_status == "unreviewed" and t.data_status == "ASSUMED" for t in topics)
    tags = db_session.scalars(select(CourseTopic).where(CourseTopic.organization_id == organization.id)).all()
    assert {(t.method, t.status) for t in tags} == {("keyword_rule", "suggested")}
    statuses = set(db_session.scalars(select(SourceRecord.data_status).where(SourceRecord.organization_id == organization.id)))
    assert "VERIFIED" not in statuses and "MOCK" not in statuses


def test_provenance_preserved(db_session, organization, bundle):
    import_canonical_datasets(db_session, organization, bundle)
    record = bundle.datasets["training_programmes"]["records"][0]
    course = db_session.scalar(select(Course).where(Course.organization_id == organization.id,
                                                    Course.external_ref == record["id"]))
    source = db_session.get(SourceRecord, course.source_record_id)
    assert source.canonical_record_id == record["id"]
    assert source.source_url == record["provenance"]["source_url"]
    assert source.source_sha256 == record["provenance"]["source_sha256"]
    assert source.retrieval_date.isoformat() == record["provenance"]["retrieval_date"]
    assert source.licence_status == record["licence"]["status"]
    assert source.attribution_text == record["licence"]["attribution_text"]
    assert source.canonical_dataset_sha256 == bundle.file_sha256["training_programmes"]
    assert source.review_verified is False
    assert course.title == record["title"]
    assert course.duration_days == record["delivery"]["duration_days_per_occurrence"]


def test_import_is_idempotent(db_session, organization, bundle):
    import_canonical_datasets(db_session, organization, bundle)
    first = _counts(db_session, organization)
    report = import_canonical_datasets(db_session, organization, bundle)
    assert sum(report.created.values()) == 0
    assert _counts(db_session, organization) == first


def test_audit_event_records_dataset_fingerprint(db_session, organization, bundle):
    import_canonical_datasets(db_session, organization, bundle)
    events = db_session.scalars(select(AuditLog).where(AuditLog.organization_id == organization.id,
                                                       AuditLog.action == "seed.import")).all()
    by_target = {e.target_id: e for e in events}
    assert set(by_target) == {"topics", "competency_framework", "training_programmes"}
    assert by_target["training_programmes"].after["dataset_sha256"] == bundle.file_sha256["training_programmes"]
    assert by_target["training_programmes"].after["created"]["courses"] == 99


def test_refuses_invalid_verdict(db_session, organization, bundle):
    invalid = CanonicalBundle(datasets=bundle.datasets, file_sha256=bundle.file_sha256, verdict="INVALID")
    with pytest.raises(SeedRefused):
        import_canonical_datasets(db_session, organization, invalid)
    assert sum(_counts(db_session, organization).values()) == 0


def _mutated(bundle, dataset, mutate):
    datasets = copy.deepcopy(bundle.datasets)
    mutate(datasets[dataset]["records"])
    return CanonicalBundle(datasets=datasets, file_sha256=bundle.file_sha256, verdict=bundle.verdict)


def test_refuses_definition_text(db_session, organization, bundle):
    def add_definition(records):
        records[3]["definition"] = "Reproduced definition text"
    with pytest.raises(SeedRefused, match="definition"):
        with db_session.begin_nested():
            import_canonical_datasets(db_session, organization, _mutated(bundle, "competency_framework", add_definition))


def test_refuses_mock_records(db_session, organization, bundle):
    def mark_mock(records):
        records[5]["data_status"] = "MOCK"
    with pytest.raises(SeedRefused, match="MOCK"):
        with db_session.begin_nested():
            import_canonical_datasets(db_session, organization, _mutated(bundle, "training_programmes", mark_mock))


def test_refuses_human_only_statuses(db_session, organization, bundle):
    def mark_verified(records):
        records[0]["data_status"] = "VERIFIED"
    with pytest.raises(SeedRefused, match="VERIFIED"):
        import_canonical_datasets(db_session, organization, _mutated(bundle, "topics", mark_verified))


def test_demo_users_are_synthetic_and_idempotent(db_session, organization):
    created = seed_demo_users(db_session, organization, AppEnv.local)
    assert created["users"] == 8
    users = db_session.scalars(select(User).where(User.organization_id == organization.id)).all()
    assert all(u.is_synthetic and u.email.endswith("@example.invalid") and u.password_hash is None for u in users)
    dept_admin = db_session.scalar(select(UserAccessRole).where(UserAccessRole.organization_id == organization.id,
                                                                UserAccessRole.role == "department_admin"))
    assert dept_admin.department_scope_id is not None
    assert seed_demo_users(db_session, organization, AppEnv.local) == {}


@pytest.mark.parametrize("env", [AppEnv.pilot, AppEnv.production])
def test_demo_users_refused_outside_development(db_session, organization, env):
    with pytest.raises(SeedRefused):
        seed_demo_users(db_session, organization, env)


def test_seed_cli_runs_twice_without_changes(test_database_url, migrated_engine, monkeypatch, capsys):
    from app.core import config, db
    from app.seed.__main__ import main

    monkeypatch.setenv("DATABASE_URL", test_database_url)
    monkeypatch.setenv("APP_ENV", "ci")
    config.get_settings.cache_clear()
    db.get_engine.cache_clear()
    db.get_sessionmaker.cache_clear()
    code = f"cli-{uuid.uuid4().hex[:10]}"
    try:
        assert main(["--org-code", code, "--org-name", f"CLI {code}", "--demo-users"]) == 0
        first = json.loads(capsys.readouterr().out)
        assert first["created"]["courses"] == 99 and first["demo_users_created"]["users"] == 8
        assert main(["--org-code", code, "--org-name", f"CLI {code}", "--demo-users"]) == 0
        second = json.loads(capsys.readouterr().out)
        assert second["created"] == {} and second["demo_users_created"] == {}
        assert second["organization_created"] is False
    finally:
        db.get_engine().dispose()
        config.get_settings.cache_clear()
        db.get_engine.cache_clear()
        db.get_sessionmaker.cache_clear()


def test_seed_cli_refuses_demo_content_without_demo_users(test_database_url, migrated_engine, monkeypatch, capsys):
    from app.core import config, db
    from app.seed.__main__ import main

    monkeypatch.setenv("DATABASE_URL", test_database_url)
    monkeypatch.setenv("APP_ENV", "ci")
    config.get_settings.cache_clear()
    db.get_engine.cache_clear()
    db.get_sessionmaker.cache_clear()
    try:
        code = f"cli-{uuid.uuid4().hex[:10]}"
        assert main(["--org-code", code, "--org-name", f"CLI {code}", "--demo-content"]) == 2
        assert "requires --demo-users" in capsys.readouterr().err
    finally:
        db.get_engine().dispose()
        config.get_settings.cache_clear()
        db.get_engine.cache_clear()
        db.get_sessionmaker.cache_clear()
