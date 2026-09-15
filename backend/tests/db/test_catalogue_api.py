"""Course catalogue, course detail and attempt history APIs (MVP-17, S-09, GET /me/attempts)."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select

from app.core.config import AppEnv
from app.modules.identity.models import User
from app.modules.organization.models import Organization
from app.modules.recommendation.models import Course
from app.seed.demo_packs import CONTENT_PACKS, apply_demo_packs
from app.seed.demo_reset import reset_demo_users
from app.seed.demo_users import seed_demo_users
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, factory, login, make_user, problem,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def cat_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"cat-{uuid.uuid4().hex[:10]}", name=f"Catalogue {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        apply_demo_packs(db, org, AppEnv.ci, CONTENT_PACKS)
        db.add(Course(organization_id=org.id, course_type="internal", title="Unreviewed draft course",
                      provider_organisation="Somewhere", data_status="ASSUMED", review_status="unreviewed", status="active"))
        db.add(Course(organization_id=org.id, course_type="internal", title="Inactive approved course",
                      provider_organisation="Somewhere", data_status="ASSUMED", review_status="approved", status="inactive"))
        db.commit()
        return org.id


def _learner_with_baseline(client, factory, org_id, role_code="DEMO-ROLE-JSO") -> tuple[str, str]:
    """A learner on a demo-2 role who submitted the baseline with no answers (every competency has a gap)."""
    email = make_user(factory, org_id)
    csrf = login(client, email)
    headers = {"X-CSRF-Token": csrf}
    me = client.get("/api/v1/me").json()
    client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": me["notice"]["version"]}, headers=headers)
    role = next(r for r in client.get("/api/v1/job-roles").json() if r["code"] == role_code)
    client.put("/api/v1/me/job-role", json={"job_role_id": role["id"]}, headers=headers)
    assessment = client.get("/api/v1/assessments").json()[0]
    attempt = client.post(f"/api/v1/assessments/{assessment['id']}/attempts", headers=headers).json()
    client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers=headers).raise_for_status()
    return email, attempt["id"]


def test_catalogue_requires_a_session(client):
    problem(client.get("/api/v1/courses"), 401, "UNAUTHENTICATED")
    problem(client.get(f"/api/v1/courses/{uuid.uuid4()}"), 401, "UNAUTHENTICATED")
    problem(client.get("/api/v1/me/attempts"), 401, "UNAUTHENTICATED")


def test_learners_see_approved_active_courses_with_filters_and_facets(client, factory, cat_org):
    login(client, make_user(factory, cat_org))
    body = client.get("/api/v1/courses").json()
    titles = [i["title"] for i in body["items"]]
    assert body["total"] == 15  # 3 demo-1 + 12 demo-2
    assert "Unreviewed draft course" not in titles and "Inactive approved course" not in titles
    assert all(i["is_demo"] for i in body["items"])
    assert body["has_learning_context"] is False  # no job role yet
    assert body["filters"]["difficulties"] == ["foundational", "intermediate", "advanced"]
    assert any(c["code"] == "DEMO-SP-SAMPLING" and c["course_count"] == 3 for c in body["filters"]["competencies"])

    sampling = next(c["id"] for c in body["filters"]["competencies"] if c["code"] == "DEMO-SP-SAMPLING")
    by_competency = client.get("/api/v1/courses", params={"competency_id": sampling}).json()["items"]
    assert {i["title"] for i in by_competency} == {
        "DEMO - Survey sampling essentials (synthetic course)",
        "DEMO - Planning and running a sample survey (synthetic course)",
        "DEMO - Data validation and quality checks (synthetic course)",
    }
    advanced = client.get("/api/v1/courses", params={"difficulty": "advanced"}).json()["items"]
    assert advanced and all(i["difficulty"] == "advanced" for i in advanced)
    short = client.get("/api/v1/courses", params={"max_days": 1}).json()["items"]
    assert short and all(i["duration_days"] == 1 for i in short)
    searched = client.get("/api/v1/courses", params={"q": "rebase"}).json()["items"]  # matches a learning objective
    assert [i["title"] for i in searched] == ["DEMO - Price statistics: weights, rebasing and linking (synthetic course)"]
    by_duration = [i["duration_days"] for i in client.get("/api/v1/courses", params={"sort": "duration_desc"}).json()["items"]]
    assert by_duration == sorted(by_duration, reverse=True)
    problem(client.get("/api/v1/courses", params={"difficulty": "expert"}), 422, "VALIDATION_FAILED")
    problem(client.get("/api/v1/courses", params={"max_days": 0}), 422, "VALIDATION_FAILED")


def test_recommended_courses_come_first_with_reasons_and_gaps(client, factory, cat_org):
    _learner_with_baseline(client, factory, cat_org)
    body = client.get("/api/v1/courses").json()
    assert body["has_learning_context"] is True
    recommended = [i for i in body["items"] if i["recommendation"]]
    assert recommended and body["items"][: len(recommended)] == recommended
    assert [i["recommendation"]["rank"] for i in recommended] == sorted(i["recommendation"]["rank"] for i in recommended)
    first = recommended[0]
    assert any(r["rule"] == "gap_match" for r in first["recommendation"]["reasons"])
    assert first["addresses_your_gaps"] and all(g["gap"] >= 1 for g in first["addresses_your_gaps"])


def test_course_detail_shows_personal_context_related_courses_and_honest_content_state(client, factory, cat_org):
    _learner_with_baseline(client, factory, cat_org)
    course = next(i for i in client.get("/api/v1/courses").json()["items"]
                  if i["title"] == "DEMO - Reading statistical tables critically (synthetic course)")
    detail = client.get(f"/api/v1/courses/{course['id']}").json()
    assert detail["learning_objectives"] and detail["difficulty"] == "foundational"
    tables = next(m for m in detail["competencies"] if m["competency"]["code"] == "DEMO-SP-TABLES")
    assert tables["relevance"] == "primary" and tables["competency"]["description"]
    assert tables["your_status"]["status"] == "gap" and tables["your_status"]["required_level"] == 3
    assert detail["recommendation"] is not None
    assert detail["related_courses"] and all(r["id"] != course["id"] for r in detail["related_courses"])
    assert detail["learning_content"] == {"available": True, "reason": None}
    assert detail["lessons"]["lesson_count"] == 4 and detail["your_progress"]["status"] == "not_started"
    assert detail["content_origin"] == "synthetic" and "does not change your competency estimate" in detail["completion_criteria"]


def test_course_detail_hides_unapproved_and_other_organisations_courses(client, factory, cat_org):
    login(client, make_user(factory, cat_org))
    with factory() as db:
        hidden = db.scalar(select(Course.id).where(Course.organization_id == cat_org, Course.title == "Unreviewed draft course"))
        other_org = Organization(code=f"other-{uuid.uuid4().hex[:8]}", name=f"Other {uuid.uuid4().hex[:8]}")
        db.add(other_org)
        db.flush()
        foreign = Course(organization_id=other_org.id, course_type="internal", title="Foreign course",
                         provider_organisation="X", data_status="ASSUMED", review_status="approved", status="active")
        db.add(foreign)
        db.commit()
        foreign_id = foreign.id
    problem(client.get(f"/api/v1/courses/{hidden}"), 404, "NOT_FOUND")
    problem(client.get(f"/api/v1/courses/{foreign_id}"), 404, "NOT_FOUND")
    problem(client.get("/api/v1/courses/not-a-uuid"), 422, "VALIDATION_FAILED")


def test_non_learning_roles_browse_without_personal_context(client, factory, cat_org):
    login(client, make_user(factory, cat_org, role="auditor"))
    body = client.get("/api/v1/courses").json()
    assert body["total"] == 15 and body["has_learning_context"] is False
    assert all(i["recommendation"] is None and i["addresses_your_gaps"] == [] for i in body["items"])


def test_attempt_history_is_own_newest_first_and_skips_voided(client, factory, cat_org):
    email, attempt_id = _learner_with_baseline(client, factory, cat_org)
    history = client.get("/api/v1/me/attempts").json()
    assert [h["id"] for h in history] == [attempt_id]
    assert history[0]["status"] == "scored" and history[0]["is_baseline"] is True and history[0]["assessment"]["is_demo"]

    with factory() as db:
        reset_demo_users(db, db.get(Organization, cat_org), AppEnv.ci, emails=[email])
        db.commit()
    assert client.get("/api/v1/me/attempts").json() == []

    login(client, make_user(factory, cat_org))  # another learner sees nothing of the first
    assert client.get("/api/v1/me/attempts").json() == []
    with factory() as db:
        assert db.scalar(select(User).where(User.email == email)) is not None
