"""Phase 4B learning experience API: outline, lessons, progress, resume, completion, learning path, isolation."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

from app.core.config import AppEnv
from app.modules.competency.models import UserCompetency
from app.modules.identity.models import User
from app.modules.learning.models import LearningActivity, LearningPath, Lesson, ProgressRecord
from app.modules.organization.models import Organization
from app.modules.recommendation.models import Course
from app.seed.demo_packs import CONTENT_PACKS, apply_demo_packs
from app.seed.demo_reset import reset_demo_users
from app.seed.demo_users import seed_demo_users
from tests.db.test_catalogue_api import _learner_with_baseline
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, factory, login, make_user, problem,
)

pytestmark = pytest.mark.db

TABLES_COURSE = "DEMO - Reading statistical tables critically (synthetic course)"


@pytest.fixture(scope="module")
def learn_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"learn-{uuid.uuid4().hex[:10]}", name=f"Learning {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        apply_demo_packs(db, org, AppEnv.ci, CONTENT_PACKS)
        db.add(Course(organization_id=org.id, course_type="internal", title="Unreviewed draft course",
                      provider_organisation="Somewhere", data_status="ASSUMED", review_status="unreviewed", status="active"))
        db.commit()
        return org.id


def _course_id(client, title=TABLES_COURSE) -> str:
    return next(i["id"] for i in client.get("/api/v1/courses").json()["items"] if i["title"] == title)


def _csrf(client) -> dict:
    return {"X-CSRF-Token": client.get("/api/v1/auth/session").json()["csrf_token"]}


def test_learning_routes_require_a_learning_role(client, factory, learn_org):
    problem(client.get("/api/v1/me/progress"), 401, "UNAUTHENTICATED")
    email = make_user(factory, learn_org, "auditor")
    login(client, email)
    problem(client.get("/api/v1/me/learning-path"), 403, "FORBIDDEN")
    problem(client.get("/api/v1/me/progress"), 403, "FORBIDDEN")


def test_outline_lists_modules_lessons_and_starts_at_zero(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    outline = client.get(f"/api/v1/courses/{_course_id(client)}/outline").json()
    assert [m["position"] for m in outline["modules"]] == [1, 2]
    lessons = [lesson for m in outline["modules"] for lesson in m["lessons"]]
    assert len(lessons) == 4 and {lesson["status"] for lesson in lessons} == {"not_started"}
    assert {lesson["lesson_type"] for lesson in lessons} == {"reading", "worked_example", "practice_check"}
    assert outline["progress"]["status"] == "not_started"
    assert outline["progress"]["resume_lesson"]["id"] == lessons[0]["id"]
    assert outline["course"]["content_origin"] == "synthetic"


def test_prerequisites_are_listed_on_the_outline(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org, role_code="DEMO-ROLE-SURVEY")
    title = "DEMO - Planning and running a sample survey (synthetic course)"
    outline = client.get(f"/api/v1/courses/{_course_id(client, title)}/outline").json()
    assert [p["title"] for p in outline["prerequisites"]] == ["DEMO - Survey sampling essentials (synthetic course)"]


def test_full_course_journey_resume_and_completion(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    headers = _csrf(client)
    course_id = _course_id(client)
    start = client.post(f"/api/v1/courses/{course_id}/start", headers=headers)
    assert start.status_code == 200 and start.json()["progress"]["status"] == "in_progress"
    lessons = [lesson["id"] for m in start.json()["modules"] for lesson in m["lessons"]]

    first = client.get(f"/api/v1/lessons/{lessons[0]}").json()
    assert first["position"] == 1 and first["lesson_count"] == 4 and first["previous"] is None
    assert first["next"]["id"] == lessons[1] and first["body_markdown"].strip()
    assert "invented" in first["content_notice"]

    # Open lesson 2 without completing: resume points to it
    opened = client.put(f"/api/v1/me/lessons/{lessons[1]}/progress", json={"status": "in_progress"}, headers=headers).json()
    assert opened["lesson_status"] == "in_progress" and opened["course_progress"]["resume_lesson"]["id"] == lessons[1]

    for index, lesson_id in enumerate(lessons):
        body = client.put(f"/api/v1/me/lessons/{lesson_id}/progress", json={"status": "completed"}, headers=headers).json()
        assert body["lesson_status"] == "completed"
        assert body["course_progress"]["completed_lessons"] == index + 1
    assert body["course_progress"]["status"] == "completed" and body["course_progress"]["percent"] == 100
    assert body["next"] is None

    # Re-opening a completed lesson never downgrades it
    again = client.put(f"/api/v1/me/lessons/{lessons[0]}/progress", json={"status": "in_progress"}, headers=headers).json()
    assert again["lesson_status"] == "completed" and again["course_progress"]["status"] == "completed"

    progress = client.get("/api/v1/me/progress").json()
    assert [i["course"]["id"] for i in progress["completed"]] == [course_id]
    assert progress["totals"] == {"courses_started": 1, "courses_completed": 1, "lessons_completed": 4}
    catalogue = client.get("/api/v1/courses", params={"progress": "completed"}).json()
    assert [i["id"] for i in catalogue["items"]] == [course_id]


def test_completion_never_changes_competency_estimates(client, factory, learn_org):
    email, _ = _learner_with_baseline(client, factory, learn_org)
    with factory() as db:
        before = {(u.competency_id, u.score, u.level_number) for u in db.scalars(
            select(UserCompetency).join(User, User.id == UserCompetency.user_id).where(User.email == email))}
    headers = _csrf(client)
    course_id = _course_id(client)
    outline = client.post(f"/api/v1/courses/{course_id}/start", headers=headers).json()
    for lesson in [lesson for m in outline["modules"] for lesson in m["lessons"]]:
        client.put(f"/api/v1/me/lessons/{lesson['id']}/progress", json={"status": "completed"}, headers=headers)
    with factory() as db:
        after = {(u.competency_id, u.score, u.level_number) for u in db.scalars(
            select(UserCompetency).join(User, User.id == UserCompetency.user_id).where(User.email == email))}
    assert before == after and before
    assessments = client.get("/api/v1/assessments").json()
    assert assessments[0]["latest_attempt"]["status"] == "scored"  # no reassessment is opened


def test_lesson_progress_validation_csrf_and_visibility(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    outline = client.get(f"/api/v1/courses/{_course_id(client)}/outline").json()
    lesson_id = outline["modules"][0]["lessons"][0]["id"]
    assert client.put(f"/api/v1/me/lessons/{lesson_id}/progress", json={"status": "completed"}).status_code == 403
    headers = _csrf(client)
    assert client.put(f"/api/v1/me/lessons/{lesson_id}/progress", json={"status": "done"}, headers=headers).status_code == 422
    assert client.put(f"/api/v1/me/lessons/{lesson_id}/progress", json={"status": "completed", "user_id": str(uuid.uuid4())},
                      headers=headers).status_code == 422
    problem(client.get(f"/api/v1/lessons/{uuid.uuid4()}"), 404, "NOT_FOUND")
    with factory() as db:
        hidden = db.scalar(select(Course).where(Course.organization_id == learn_org, Course.title == "Unreviewed draft course"))
    problem(client.get(f"/api/v1/courses/{hidden.id}/outline"), 404, "NOT_FOUND")
    problem(client.post(f"/api/v1/courses/{hidden.id}/start", headers=headers), 404, "NOT_FOUND")


def test_lessons_of_other_organisations_are_not_found(client, factory, learn_org):
    with factory() as db:
        other = Organization(code=f"lo-{uuid.uuid4().hex[:8]}", name=f"Other learning {uuid.uuid4().hex[:8]}")
        db.add(other)
        db.flush()
        seed_demo_users(db, other, AppEnv.ci, PASSWORD)
        apply_demo_packs(db, other, AppEnv.ci, CONTENT_PACKS)
        db.commit()
        foreign_lesson = db.scalar(select(Lesson.id).where(Lesson.organization_id == other.id).limit(1))
    _learner_with_baseline(client, factory, learn_org)
    problem(client.get(f"/api/v1/lessons/{foreign_lesson}"), 404, "NOT_FOUND")
    problem(client.put(f"/api/v1/me/lessons/{foreign_lesson}/progress", json={"status": "completed"}, headers=_csrf(client)),
            404, "NOT_FOUND")


def test_progress_is_private_to_each_learner(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    headers = _csrf(client)
    course_id = _course_id(client)
    outline = client.post(f"/api/v1/courses/{course_id}/start", headers=headers).json()
    client.put(f"/api/v1/me/lessons/{outline['modules'][0]['lessons'][0]['id']}/progress", json={"status": "completed"},
               headers=headers)
    client.cookies.clear()
    _learner_with_baseline(client, factory, learn_org)
    assert client.get("/api/v1/me/progress").json()["totals"] == {"courses_started": 0, "courses_completed": 0, "lessons_completed": 0}
    other_outline = client.get(f"/api/v1/courses/{course_id}/outline").json()
    assert other_outline["progress"]["completed_lessons"] == 0


def test_learning_path_orders_gaps_and_tracks_progress(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    path = client.get("/api/v1/me/learning-path").json()
    assert path["state"] == "ready" and path["rule_version"] == "path-v1"
    gaps = [g["gap"] for g in path["groups"]]
    assert gaps == sorted(gaps, reverse=True)
    for group in path["groups"]:
        difficulties = [{"foundational": 0, "intermediate": 1, "advanced": 2}.get(i["course"]["difficulty"], 1)
                        for i in group["items"] if i["course"] and i["reasons"][0]["rule"] != "prerequisite"]
        assert difficulties == sorted(difficulties)
    course_ids = [i["course"]["id"] for g in path["groups"] for i in g["items"] if i["course"]]
    assert len(course_ids) == len(set(course_ids)) == path["summary"]["courses"]

    # Same inputs: same path, not regenerated
    again = client.get("/api/v1/me/learning-path").json()
    assert again["id"] == path["id"]

    headers = _csrf(client)
    first_course = course_ids[0]
    outline = client.post(f"/api/v1/courses/{first_course}/start", headers=headers).json()
    for lesson in [lesson for m in outline["modules"] for lesson in m["lessons"]]:
        client.put(f"/api/v1/me/lessons/{lesson['id']}/progress", json={"status": "completed"}, headers=headers)
    tracked = client.get("/api/v1/me/learning-path").json()
    item = next(i for g in tracked["groups"] for i in g["items"] if i["course"] and i["course"]["id"] == first_course)
    assert item["status"] == "completed" and tracked["summary"]["completed"] == 1

    regenerated = client.post("/api/v1/me/learning-path/regenerate", headers=headers).json()
    assert regenerated["id"] != path["id"] and regenerated["summary"]["completed"] == 1  # completion carried over
    with factory() as db:
        statuses = [p.status for p in db.scalars(select(LearningPath).where(LearningPath.id.in_([path["id"], regenerated["id"]])))]
        assert sorted(statuses) == ["active", "superseded"]


def test_learning_path_before_assessment_explains_what_to_do(client, factory, learn_org):
    email = make_user(factory, learn_org)
    csrf = login(client, email)
    headers = {"X-CSRF-Token": csrf}
    problem(client.get("/api/v1/me/learning-path"), 409, "JOB_ROLE_REQUIRED")
    me = client.get("/api/v1/me").json()
    client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": me["notice"]["version"]}, headers=headers)
    role = next(r for r in client.get("/api/v1/job-roles").json() if r["code"] == "DEMO-ROLE-JSO")
    client.put("/api/v1/me/job-role", json={"job_role_id": role["id"]}, headers=headers)
    path = client.get("/api/v1/me/learning-path").json()
    assert path["state"] == "assessment_needed" and path["groups"] == []


def test_activity_log_is_append_only_and_holds_no_text(client, factory, learn_org):
    _learner_with_baseline(client, factory, learn_org)
    headers = _csrf(client)
    outline = client.post(f"/api/v1/courses/{_course_id(client)}/start", headers=headers).json()
    client.put(f"/api/v1/me/lessons/{outline['modules'][0]['lessons'][0]['id']}/progress", json={"status": "completed"},
               headers=headers)
    with factory() as db:
        activity = db.scalars(select(LearningActivity).order_by(LearningActivity.occurred_at.desc()).limit(3)).all()
        assert {a.activity_type for a in activity} >= {"lesson_completed"}
        for a in activity:
            assert all(isinstance(v, (int, str)) and (not isinstance(v, str) or len(v) <= 40) for v in a.activity_metadata.values())
        with pytest.raises(DBAPIError):
            db.execute(text("UPDATE learning_activities SET activity_type = 'lesson_opened' WHERE id = :id"), {"id": activity[0].id})
        db.rollback()


def test_demo_reset_clears_learning_progress(client, factory, learn_org):
    email, _ = _learner_with_baseline(client, factory, learn_org)
    headers = _csrf(client)
    outline = client.post(f"/api/v1/courses/{_course_id(client)}/start", headers=headers).json()
    client.put(f"/api/v1/me/lessons/{outline['modules'][0]['lessons'][0]['id']}/progress", json={"status": "completed"},
               headers=headers)
    client.get("/api/v1/me/learning-path")
    with factory() as db:
        report = reset_demo_users(db, db.get(Organization, learn_org), AppEnv.ci, emails=[email])
        db.commit()
        assert report["totals"]["progress_records_removed"] == 2 and report["totals"]["learning_paths_removed"] == 1
        user_id = db.execute(text("SELECT id FROM users WHERE email = :e"), {"e": email}).scalar()
        assert db.scalar(select(ProgressRecord.id).where(ProgressRecord.user_id == user_id)) is None


def test_concurrent_open_and_complete_do_not_conflict(client, factory, learn_org):
    """Opening a lesson and completing it at the same moment must both succeed (no unique-constraint error)."""
    from concurrent.futures import ThreadPoolExecutor

    _learner_with_baseline(client, factory, learn_org)
    headers = _csrf(client)
    outline = client.get(f"/api/v1/courses/{_course_id(client)}/outline").json()
    lesson_ids = [lesson["id"] for m in outline["modules"] for lesson in m["lessons"]]

    def put(args):
        lesson_id, status = args
        return client.put(f"/api/v1/me/lessons/{lesson_id}/progress", json={"status": status}, headers=headers).status_code

    jobs = [(lid, s) for lid in lesson_ids for s in ("in_progress", "completed")]
    with ThreadPoolExecutor(max_workers=8) as pool:
        codes = list(pool.map(put, jobs))
    assert set(codes) == {200}, codes
    final = client.get(f"/api/v1/courses/{_course_id(client)}/outline").json()
    assert final["progress"]["status"] == "completed" and final["progress"]["completed_lessons"] == len(lesson_ids)
