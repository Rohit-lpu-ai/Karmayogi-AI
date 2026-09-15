"""Database constraints and triggers of the reference schema (migration 0002)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm.exc import StaleDataError

import app.models  # noqa: F401
from app.core.db import Base, TenantMixin
from app.modules.competency.models import Competency, CompetencyFramework, CompetencyLevel, RoleCompetency
from app.modules.content.models import SourceRecord
from app.modules.governance.service import record_audit
from app.modules.identity.models import User, UserAccessRole
from app.modules.organization.models import Department, JobRole, Organization
from app.modules.platform.models import Topic
from app.modules.recommendation.models import Course

pytestmark = pytest.mark.db


def _fails(session, *objects, error=IntegrityError):
    with pytest.raises(error):
        with session.begin_nested():
            session.add_all(objects)
            session.flush()


def _framework(org, restricted=False, **kw):
    return CompetencyFramework(
        organization_id=org.id, name="F", code=f"F-{uuid.uuid4().hex[:6]}", framework_type="functional",
        version_label="v1", definitions_restricted=restricted, **kw,
    )


def _source(org, **kw):
    values = dict(
        organization_id=org.id, registry_source_id="SRC-025", source_url="https://example.invalid/doc.pdf",
        source_organisation="Test", access_method="test", data_status="MACHINE_OBSERVED",
        licence_status="UNVERIFIED_SECONDHAND", licence_notes="n/a", attribution_text="Source: test",
        canonical_dataset="test", canonical_record_id=uuid.uuid4().hex,
    )
    values.update(kw)
    return SourceRecord(**values)


def test_every_tenant_table_has_non_null_organization_fk():
    tenant_tables = [m.local_table for m in Base.registry.mappers if issubclass(m.class_, TenantMixin)]
    assert len(tenant_tables) >= 15
    for table in tenant_tables:
        column = table.c.organization_id
        assert not column.nullable, table.name
        assert {fk.column.table.name for fk in column.foreign_keys} == {"organizations"}, table.name


def test_primary_keys_generated_by_database(db_session, organization):
    assert isinstance(organization.id, uuid.UUID)


def test_organization_code_and_name_unique(db_session, organization):
    _fails(db_session, Organization(code=organization.code, name="Other name"))
    _fails(db_session, Organization(code=f"x-{uuid.uuid4().hex[:6]}", name=organization.name.upper()))


def test_organization_code_must_be_slug(db_session):
    _fails(db_session, Organization(code="Not A Slug", name="Slug test"))


def test_department_name_unique_per_org_case_insensitive(db_session, organization):
    db_session.add(Department(organization_id=organization.id, name="Survey Design"))
    db_session.flush()
    _fails(db_session, Department(organization_id=organization.id, name="survey design"))
    other = Organization(code=f"o-{uuid.uuid4().hex[:6]}", name=f"Other {uuid.uuid4().hex[:6]}")
    db_session.add(other)
    db_session.flush()
    db_session.add(Department(organization_id=other.id, name="Survey Design"))
    db_session.flush()


def test_user_email_unique_per_org_case_insensitive(db_session, organization):
    db_session.add(User(organization_id=organization.id, email="learner@example.invalid", display_name="A"))
    db_session.flush()
    _fails(db_session, User(organization_id=organization.id, email="LEARNER@example.invalid", display_name="B"))


@pytest.mark.parametrize("field,value", [("status", "suspended"), ("locale", "fr")])
def test_user_enumerations_checked(db_session, organization, field, value):
    _fails(db_session, User(organization_id=organization.id, email=f"{uuid.uuid4().hex}@example.invalid",
                            display_name="A", **{field: value}))


def test_access_role_enumeration_and_department_admin_scope(db_session, organization):
    user = User(organization_id=organization.id, email="u@example.invalid", display_name="U")
    db_session.add(user)
    db_session.flush()
    _fails(db_session, UserAccessRole(organization_id=organization.id, user_id=user.id, role="superuser"))
    _fails(db_session, UserAccessRole(organization_id=organization.id, user_id=user.id, role="department_admin"))


def test_access_role_unique_when_scope_is_null(db_session, organization):
    user = User(organization_id=organization.id, email="r@example.invalid", display_name="R")
    db_session.add(user)
    db_session.flush()
    db_session.add(UserAccessRole(organization_id=organization.id, user_id=user.id, role="learner"))
    db_session.flush()
    _fails(db_session, UserAccessRole(organization_id=organization.id, user_id=user.id, role="learner"))


def test_restricted_framework_rejects_description(db_session, organization):
    framework = _framework(organization, restricted=True)
    db_session.add(framework)
    db_session.flush()
    _fails(db_session, Competency(organization_id=organization.id, framework_id=framework.id, code="1.1",
                                  name="People First", description="Definition text", data_status="MACHINE_OBSERVED"),
           error=DBAPIError)
    db_session.add(Competency(organization_id=organization.id, framework_id=framework.id, code="1.2",
                              name="Named only", data_status="MACHINE_OBSERVED"))
    db_session.flush()


def test_cannot_restrict_framework_that_has_descriptions(db_session, organization):
    framework = _framework(organization)
    db_session.add(framework)
    db_session.flush()
    db_session.add(Competency(organization_id=organization.id, framework_id=framework.id, code="S1",
                              name="Sampling", description="Authored", data_status="ASSUMED"))
    db_session.flush()
    with pytest.raises(DBAPIError):
        with db_session.begin_nested():
            db_session.execute(text("UPDATE competency_frameworks SET definitions_restricted = true WHERE id = :id"),
                               {"id": framework.id})


def test_min_score_must_increase_with_level(db_session, organization):
    framework = _framework(organization)
    db_session.add(framework)
    db_session.flush()
    with pytest.raises(DBAPIError):
        with db_session.begin_nested():
            db_session.add_all([
                CompetencyLevel(organization_id=organization.id, framework_id=framework.id, level_number=1,
                                label="Level 1", min_score=Decimal("0.60")),
                CompetencyLevel(organization_id=organization.id, framework_id=framework.id, level_number=2,
                                label="Level 2", min_score=Decimal("0.40")),
            ])
            db_session.flush()
            db_session.execute(text("SET CONSTRAINTS ALL IMMEDIATE"))


def test_min_score_range_checked(db_session, organization):
    framework = _framework(organization)
    db_session.add(framework)
    db_session.flush()
    _fails(db_session, CompetencyLevel(organization_id=organization.id, framework_id=framework.id, level_number=1,
                                       label="L1", min_score=Decimal("1.5")))


def test_role_mapping_level_must_exist_in_scale(db_session, organization):
    framework = _framework(organization)
    db_session.add(framework)
    db_session.flush()
    competency = Competency(organization_id=organization.id, framework_id=framework.id, code="S1", name="Sampling",
                            data_status="ASSUMED")
    level = CompetencyLevel(organization_id=organization.id, framework_id=framework.id, level_number=1, label="L1")
    role = JobRole(organization_id=organization.id, name="Statistical Officer")
    db_session.add_all([competency, level, role])
    db_session.flush()
    _fails(db_session, RoleCompetency(organization_id=organization.id, job_role_id=role.id,
                                      competency_id=competency.id, required_level_number=3), error=DBAPIError)
    db_session.add(RoleCompetency(organization_id=organization.id, job_role_id=role.id, competency_id=competency.id,
                                  required_level_number=1))
    db_session.flush()


def test_approval_requires_approver_and_time(db_session, organization):
    _fails(db_session, _framework(organization, status="approved"))


def test_only_one_approved_mapping_per_role_and_competency(db_session, organization):
    framework = _framework(organization)
    approver = User(organization_id=organization.id, email="ca@example.invalid", display_name="CA")
    db_session.add_all([framework, approver])
    db_session.flush()
    competency = Competency(organization_id=organization.id, framework_id=framework.id, code="S1", name="S",
                            data_status="ASSUMED")
    level = CompetencyLevel(organization_id=organization.id, framework_id=framework.id, level_number=1, label="L1")
    role = JobRole(organization_id=organization.id, name="Role A")
    db_session.add_all([competency, level, role])
    db_session.flush()
    now = datetime.now(timezone.utc)
    approved = dict(organization_id=organization.id, job_role_id=role.id, competency_id=competency.id,
                    required_level_number=1, status="approved", approved_by=approver.id, approved_at=now)
    db_session.add(RoleCompetency(mapping_version=1, **approved))
    db_session.flush()
    _fails(db_session, RoleCompetency(mapping_version=2, **approved))


def test_mock_data_rejected_everywhere(db_session, organization):
    _fails(db_session, _source(organization, data_status="MOCK"))
    _fails(db_session, Topic(organization_id=organization.id, code="t", label="T", taxonomy_version="1", data_status="MOCK"))
    _fails(db_session, Course(organization_id=organization.id, course_type="internal", title="C",
                              provider_organisation="P", data_status="MOCK"))


def test_external_igot_course_type_not_allowed_in_mvp(db_session, organization):
    _fails(db_session, Course(organization_id=organization.id, course_type="external_igot", title="C",
                              provider_organisation="P", data_status="UNKNOWN"))


def test_programme_listing_requires_provenance(db_session, organization):
    _fails(db_session, Course(organization_id=organization.id, course_type="nssta_programme_listing", title="C",
                              provider_organisation="NSSTA", data_status="MACHINE_OBSERVED"))


def test_audit_log_is_append_only(db_session, organization):
    entry = record_audit(db_session, organization_id=organization.id, action="test.event", target_type="test")
    db_session.flush()
    for statement in ("UPDATE audit_logs SET reason = 'x' WHERE id = :id", "DELETE FROM audit_logs WHERE id = :id"):
        with pytest.raises(DBAPIError):
            with db_session.begin_nested():
                db_session.execute(text(statement), {"id": entry.id})
    with pytest.raises(DBAPIError):
        with db_session.begin_nested():
            db_session.execute(text("TRUNCATE audit_logs"))


def test_audit_action_format_checked(db_session, organization):
    with pytest.raises(IntegrityError):
        with db_session.begin_nested():
            record_audit(db_session, organization_id=organization.id, action="Not An Action", target_type="t")
            db_session.flush()


def test_audit_before_after_are_redacted(db_session, organization):
    entry = record_audit(db_session, organization_id=organization.id, action="user.update", target_type="user",
                         before={"password_hash": "argon2..."}, after={"email": "person@example.invalid"})
    db_session.flush()
    assert entry.before == {"password_hash": "[REDACTED]"}
    assert entry.after == {"email": "[EMAIL]"}
    assert entry.correlation_id


def test_optimistic_locking(db_session, organization):
    role = JobRole(organization_id=organization.id, name="Versioned role")
    db_session.add(role)
    db_session.flush()
    assert role.row_version == 1
    role.description = "changed"
    db_session.flush()
    assert role.row_version == 2
    db_session.execute(text("UPDATE job_roles SET row_version = 9 WHERE id = :id"), {"id": role.id})
    role.description = "stale write"
    with pytest.raises(StaleDataError):
        db_session.flush()
