"""Phase 4D aggregated insight: authorisation, minimum group size, department scoping, no personal data."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select

from app.core.config import AppEnv
from app.modules.identity.models import User, UserAccessRole
from app.modules.identity.security import hash_password
from app.modules.organization.models import Department, Organization
from app.seed.demo_packs import apply_demo_packs
from app.seed.demo_users import seed_demo_users
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, factory, login, make_user, problem,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def insight_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"insight-{uuid.uuid4().hex[:10]}", name=f"Insight {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        report = apply_demo_packs(db, org, AppEnv.ci)  # includes the demo-4 cohort
        assert report["demo-4"]["created"]["learners"] == 38
        db.commit()
        return org.id


PATHS = ["/api/v1/admin/insight/summary", "/api/v1/admin/insight/skill-gaps", "/api/v1/admin/insight/training-needs"]


@pytest.mark.parametrize("role", ["learner", "trainer", "auditor", "platform_admin"])
def test_insight_needs_the_insight_capability(client, factory, insight_org, role):
    login(client, make_user(factory, insight_org, role))
    for path in PATHS:
        problem(client.get(path), 403, "FORBIDDEN")


def test_figures_are_aggregated_and_small_groups_withheld(client, factory, insight_org):
    login(client, make_user(factory, insight_org, "training_manager"))
    summary = client.get(PATHS[0]).json()
    assert summary["baseline_completed"]["value"] >= 38 and summary["min_group_size"] == 5
    gaps = client.get(PATHS[1]).json()
    rows = {r["department"]["name"]: r for r in gaps["rows"]}
    small = rows["DEMO Data Services Unit (synthetic)"]
    assert small["learners"] == {"value": None, "suppressed": True}
    assert all(c["assessed"] is None and c["with_gap"] is None for c in small["cells"].values())
    survey = rows["DEMO Survey Operations Division (synthetic)"]
    assert survey["learners"]["value"] == 18
    shown = [c for c in survey["cells"].values() if not c["suppressed"] and c["assessed"] is not None]
    assert shown and all(c["assessed"] >= 5 and 0 <= c["share"] <= 1 for c in shown)
    for cell in [c for r in gaps["rows"] for c in r["cells"].values()] + list(gaps["totals"].values()):
        for key in ("assessed", "required_for"):
            assert cell[key] is None or cell[key] >= 5

    needs = client.get(PATHS[2]).json()
    assert needs["items"] and all(i["learners_with_gap"] >= 5 for i in needs["items"])
    counts = [i["learners_with_gap"] for i in needs["items"]]
    assert counts == sorted(counts, reverse=True)
    for item in needs["items"]:
        for key in ("learners_started_linked_course", "learners_completed_linked_course"):
            assert item[key]["suppressed"] or item[key]["value"] >= 5


def test_responses_contain_no_personal_data(client, factory, insight_org):
    login(client, make_user(factory, insight_org, "org_admin"))
    blob = " ".join(client.get(p).text for p in PATHS + ["/api/v1/admin/insight/skill-gaps?job_role_id=" + str(uuid.uuid4())])
    assert "@example.invalid" not in blob and "Cohort Learner" not in blob and "DEMO-COHORT" not in blob


def test_department_admin_sees_only_their_department(client, factory, insight_org):
    with factory() as db:
        survey = db.scalar(select(Department).where(Department.organization_id == insight_org, Department.code == "demo-survey"))
        user = User(organization_id=insight_org, email=f"dept-{uuid.uuid4().hex[:6]}@example.invalid", display_name="Scoped admin",
                    status="active", password_hash=hash_password(PASSWORD), is_synthetic=True, department_id=survey.id)
        db.add(user)
        db.flush()
        db.add(UserAccessRole(organization_id=insight_org, user_id=user.id, role="department_admin", department_scope_id=survey.id))
        db.commit()
        email = user.email
    login(client, email)
    summary = client.get(PATHS[0]).json()
    assert summary["scope"] == "department" and summary["learners"]["value"] == 18
    names = {r["department"]["name"] for r in client.get(PATHS[1]).json()["rows"]}
    assert names == {"DEMO Survey Operations Division (synthetic)"}


def test_job_role_filter_limits_learners(client, factory, insight_org):
    login(client, make_user(factory, insight_org, "competency_admin"))
    everything = client.get(PATHS[1]).json()
    prices = next(r for r in everything["job_roles"] if "Price" in r["name"])
    filtered = client.get(PATHS[1], params={"job_role_id": prices["id"]}).json()
    assert {r["department"]["name"] for r in filtered["rows"]} == {"DEMO Price Statistics Division (synthetic)"}
