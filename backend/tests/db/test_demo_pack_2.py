"""DEMO pack demo-2: synthetic statistical-practice content (DEC-045, DEC-051, DEC-052)."""

from __future__ import annotations

import uuid
from collections import Counter

import pytest
from sqlalchemy import func, select

from app.core.config import AppEnv
from app.modules.assessment.models import Assessment, AssessmentQuestion, QuestionOption, QuestionVersion
from app.modules.competency.models import Competency, CompetencyFramework, CompetencyLevel
from app.modules.organization.models import JobRole, Organization
from app.modules.recommendation.models import Course, CourseCompetency
from app.seed import demo_pack_2
from app.seed.canonical import SeedRefused
from app.seed.demo_packs import CONTENT_PACKS, apply_demo_packs
from app.seed.demo_users import seed_demo_users
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, correct_options, factory, login, make_user, problem,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def pack_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"pack2-{uuid.uuid4().hex[:10]}", name=f"Pack 2 {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        apply_demo_packs(db, org, AppEnv.ci, CONTENT_PACKS)
        db.commit()
        return org.id


def test_pack_creates_the_documented_content_once(factory, pack_org):
    with factory() as db:
        framework = db.scalar(select(CompetencyFramework).where(CompetencyFramework.organization_id == pack_org,
                                                                CompetencyFramework.code == demo_pack_2.FRAMEWORK_CODE))
        assert framework.status == "draft" and not framework.definitions_restricted
        levels = db.scalars(select(CompetencyLevel).where(CompetencyLevel.framework_id == framework.id)).all()
        assert len(levels) == 4 and all(lvl.description and lvl.threshold_status == "provisional" for lvl in levels)
        competencies = db.scalars(select(Competency).where(Competency.framework_id == framework.id)).all()
        assert len(competencies) == 8
        assert all(c.code.startswith("DEMO-") and c.name.startswith("DEMO") and "synthetic" in c.name for c in competencies)
        assert all(c.description and c.data_status == "ASSUMED" for c in competencies)
        roles = db.scalars(select(JobRole).where(JobRole.organization_id == pack_org, JobRole.code.like("DEMO-ROLE-%"))).all()
        assert {r.code for r in roles} >= {"DEMO-ROLE-JSO", "DEMO-ROLE-SURVEY", "DEMO-ROLE-PRICES"}
        org = db.get(Organization, pack_org)
        assert demo_pack_2.seed_demo_pack_2(db, org, AppEnv.ci) == Counter()  # additive: nothing missing
        db.rollback()


def test_every_item_has_one_correct_option_and_a_demo_explanation(factory, pack_org):
    with factory() as db:
        framework_id = db.scalar(select(CompetencyFramework.id).where(CompetencyFramework.organization_id == pack_org,
                                                                      CompetencyFramework.code == demo_pack_2.FRAMEWORK_CODE))
        versions = db.scalars(select(QuestionVersion).join(Competency, Competency.id == QuestionVersion.competency_id)
                              .where(Competency.framework_id == framework_id)).all()
        assert len(versions) == 40
        for version in versions:
            options = db.scalars(select(QuestionOption).where(QuestionOption.question_version_id == version.id)).all()
            assert len(options) == 4 and sum(o.is_correct for o in options) == 1
            assert "DEMO item" in version.explanation


def test_each_role_assessment_has_five_items_per_required_competency(factory, pack_org):
    with factory() as db:
        for code, _, _, requirements in demo_pack_2.ROLES:
            role = db.scalar(select(JobRole).where(JobRole.organization_id == pack_org, JobRole.code == code))
            assessment = db.scalar(select(Assessment).where(Assessment.job_role_id == role.id))
            assert assessment.status == "published" and assessment.blueprint["demo_seed"] is True
            rows = db.execute(select(Competency.code, func.count())
                              .join(QuestionVersion, QuestionVersion.competency_id == Competency.id)
                              .join(AssessmentQuestion, AssessmentQuestion.question_version_id == QuestionVersion.id)
                              .where(AssessmentQuestion.assessment_id == assessment.id).group_by(Competency.code)).all()
            assert dict(rows) == {competency: 5 for competency, _ in requirements}


def test_courses_have_descriptive_difficulty_objectives_and_approved_mappings(factory, pack_org):
    with factory() as db:
        courses = db.scalars(select(Course).where(Course.organization_id == pack_org, Course.external_ref.like("DEMO-C2-%"))).all()
        assert len(courses) == 12
        for course in courses:
            assert course.title.startswith("DEMO") and "synthetic" in course.title
            assert course.difficulty in ("foundational", "intermediate", "advanced")
            assert len(course.learning_objectives) >= 3
            assert course.review_status == "approved" and course.data_status == "ASSUMED"
            mappings = db.scalars(select(CourseCompetency).where(CourseCompetency.course_id == course.id)).all()
            assert mappings and all(m.status == "approved" and m.method == "demo_seed" for m in mappings)


@pytest.mark.parametrize("env", [AppEnv.staging, AppEnv.pilot, AppEnv.production])
def test_pack_refused_outside_local_and_ci(factory, pack_org, env):
    with factory() as db:
        with pytest.raises(SeedRefused):
            demo_pack_2.seed_demo_pack_2(db, db.get(Organization, pack_org), env)


def test_learner_journey_on_a_demo_2_role_yields_gaps_and_recommendations(client, factory, pack_org):
    email = make_user(factory, pack_org)
    csrf = login(client, email)
    headers = {"X-CSRF-Token": csrf}
    me = client.get("/api/v1/me").json()
    client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": me["notice"]["version"]}, headers=headers)
    role = next(r for r in client.get("/api/v1/job-roles").json() if r["code"] == "DEMO-ROLE-JSO")
    assert client.put("/api/v1/me/job-role", json={"job_role_id": role["id"]}, headers=headers).status_code == 200

    requirements = client.get(f"/api/v1/job-roles/{role['id']}/competencies").json()["requirements"]
    assert len(requirements) == 4
    assert all(r["competency"]["description"] and all(lvl["description"] for lvl in r["levels"]) for r in requirements)

    assessment = client.get("/api/v1/assessments").json()[0]
    assert assessment["question_count"] == 20
    attempt = client.post(f"/api/v1/assessments/{assessment['id']}/attempts", headers=headers).json()
    keys = correct_options(factory, attempt)
    # Answer the descriptive-statistics items correctly and everything else incorrectly.
    for question in attempt["questions"]:
        competency_code, correct_id, _ = keys[question["question_version_id"]]
        wrong_id = next(o["id"] for o in question["options"] if o["id"] != correct_id)
        chosen = correct_id if competency_code == "DEMO-SP-DESC" else wrong_id
        client.put(f"/api/v1/attempts/{attempt['id']}/answers/{question['question_version_id']}",
                   json={"selected_option_id": chosen}, headers=headers).raise_for_status()
    assert client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers=headers).status_code == 200

    gaps = {g["competency"]["code"]: g for g in client.get("/api/v1/me/competency-gaps").json()["items"]}
    assert gaps["DEMO-SP-DESC"]["status"] == "meets_requirement" and gaps["DEMO-SP-DESC"]["evidence_band"] == "medium"
    assert gaps["DEMO-SP-TABLES"]["status"] == "gap" and gaps["DEMO-SP-TABLES"]["gap"] == 2
    recommendations = client.get("/api/v1/me/recommendations").json()["items"]
    assert recommendations and all(r["course"]["is_demo"] for r in recommendations)
    assert all(r["course"]["difficulty"] and r["course"]["learning_objectives"] for r in recommendations)
    titles = [r["course"]["title"] for r in recommendations]
    assert "DEMO - Reading statistical tables critically (synthetic course)" in titles


def test_course_difficulty_never_changes_recommendation_order(client, factory, pack_org):
    """DEC-051: difficulty is descriptive only."""
    email = make_user(factory, pack_org)
    csrf = login(client, email)
    headers = {"X-CSRF-Token": csrf}
    me = client.get("/api/v1/me").json()
    client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": me["notice"]["version"]}, headers=headers)
    role = next(r for r in client.get("/api/v1/job-roles").json() if r["code"] == "DEMO-ROLE-PRICES")
    client.put("/api/v1/me/job-role", json={"job_role_id": role["id"]}, headers=headers)
    assessment = client.get("/api/v1/assessments").json()[0]
    attempt = client.post(f"/api/v1/assessments/{assessment['id']}/attempts", headers=headers).json()
    client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers=headers).raise_for_status()  # all unanswered

    before = [r["course"]["id"] for r in client.get("/api/v1/me/recommendations").json()["items"]]
    assert len(before) > 1
    with factory() as db:
        courses = db.scalars(select(Course).where(Course.id.in_([uuid.UUID(i) for i in before]))).all()
        original = {c.id: c.difficulty for c in courses}
        for c in courses:
            c.difficulty = "advanced" if c.difficulty != "advanced" else "foundational"
        db.commit()
    try:
        after = [r["course"]["id"] for r in client.get("/api/v1/me/recommendations").json()["items"]]
        assert after == before
    finally:
        with factory() as db:
            for c in db.scalars(select(Course).where(Course.id.in_(list(original)))).all():
                c.difficulty = original[c.id]
            db.commit()
