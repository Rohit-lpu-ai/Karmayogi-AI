"""Vertical slice 1 API: journey, validation, authorisation, key leakage and demo labelling.

Runs against the real PostgreSQL test database. Each module gets its own
organisation with synthetic demo users and DEMO content; each test creates the
learners it needs so tests do not share attempt state.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import AppEnv
from app.core.db import get_db
from app.main import create_app
from app.modules.assessment.models import AssessmentAttempt, QuestionOption, QuestionVersion
from app.modules.competency.models import Competency
from app.modules.governance.models import AuditLog
from app.modules.identity.models import NoticeAcknowledgement, Session as SessionRow, User, UserAccessRole
from app.modules.identity.security import hash_password
from app.modules.organization.models import Organization
from app.seed.canonical import SeedRefused
from app.seed.demo_content import JOB_ROLE_CODE, seed_demo_content
from app.seed.demo_users import seed_demo_users
from tests.conftest import make_settings

pytestmark = pytest.mark.db

PASSWORD = "Test-demo-password-123"


@pytest.fixture(scope="module")
def factory(migrated_engine) -> sessionmaker[Session]:
    return sessionmaker(bind=migrated_engine, expire_on_commit=False)


def _make_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"slice-{uuid.uuid4().hex[:10]}", name=f"Slice test {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        seed_demo_content(db, org, AppEnv.ci)
        db.commit()
        return org.id


@pytest.fixture(scope="module")
def org_id(factory) -> uuid.UUID:
    return _make_org(factory)


@pytest.fixture
def client(factory, test_database_url) -> Iterator[TestClient]:
    app = create_app(make_settings(database_url=test_database_url))

    def override_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def make_user(factory, org_id, role="learner", *, status="active") -> str:
    email = f"{role}-{uuid.uuid4().hex[:8]}@example.invalid"
    with factory() as db:
        user = User(organization_id=org_id, email=email, display_name=f"Test {role}", status=status,
                    password_hash=hash_password(PASSWORD), is_synthetic=True)
        db.add(user)
        db.flush()
        db.add(UserAccessRole(organization_id=org_id, user_id=user.id, role=role))
        db.commit()
    return email


def login(client, email, password=PASSWORD) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["csrf_token"]


def problem(response, status, code):
    assert response.status_code == status, response.text
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["code"] == code
    return response.json()


def onboard(client, csrf) -> dict:
    me = client.get("/api/v1/me").json()
    assert client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": me["notice"]["version"]},
                       headers={"X-CSRF-Token": csrf}).status_code == 200
    role = next(r for r in client.get("/api/v1/job-roles").json() if r["code"] == JOB_ROLE_CODE)
    response = client.put("/api/v1/me/job-role", json={"job_role_id": role["id"]}, headers={"X-CSRF-Token": csrf})
    assert response.status_code == 200, response.text
    return role


def start(client, csrf) -> dict:
    assessment = client.get("/api/v1/assessments").json()[0]
    response = client.post(f"/api/v1/assessments/{assessment['id']}/attempts", headers={"X-CSRF-Token": csrf})
    assert response.status_code in (200, 201), response.text
    return response.json()


def correct_options(factory, attempt) -> dict[str, tuple[str, str]]:
    """question_version_id -> (competency code, correct option id), read from the database (never from the API)."""
    out = {}
    with factory() as db:
        for q in attempt["questions"]:
            version = db.get(QuestionVersion, uuid.UUID(q["question_version_id"]))
            option = db.scalar(select(QuestionOption).where(QuestionOption.question_version_id == version.id,
                                                            QuestionOption.is_correct))
            out[q["question_version_id"]] = (db.get(Competency, version.competency_id).code, str(option.id), version.difficulty)
    return out


# --- Journey -----------------------------------------------------------------


def test_full_learner_journey(client, factory, org_id):
    email = make_user(factory, org_id)
    csrf = login(client, email)

    session = client.get("/api/v1/auth/session").json()
    assert session["csrf_token"] == csrf
    me = session["user"]
    assert me["job_role"] is None and me["notice"]["acknowledged_at"] is None and me["notice"]["status"] == "draft"
    assert me["can_take_assessments"] is True

    roles = client.get("/api/v1/job-roles").json()
    demo_role = next(r for r in roles if r["code"] == JOB_ROLE_CODE)
    assert demo_role["is_demo"] is True

    requirements = client.get(f"/api/v1/job-roles/{demo_role['id']}/competencies").json()
    assert [r["competency"]["code"] for r in requirements["requirements"]] == ["DEMO-C1", "DEMO-C2"]
    assert all(r["required_level"] == 3 and len(r["levels"]) == 4 and r["competency"]["is_demo"]
               for r in requirements["requirements"])
    assert {lvl["threshold_status"] for r in requirements["requirements"] for lvl in r["levels"]} == {"provisional"}

    onboard(client, csrf)
    assessments = client.get("/api/v1/assessments").json()
    assert len(assessments) == 1 and assessments[0]["question_count"] == 10 and assessments[0]["is_demo"]

    attempt = start(client, csrf)
    assert attempt["question_count"] == 10 and attempt["status"] == "in_progress"
    resumed = start(client, csrf)
    assert resumed["id"] == attempt["id"]

    # Answer: all DEMO-C1 correct; DEMO-C2 only the two foundational items correct.
    keys = correct_options(factory, attempt)
    for q in attempt["questions"]:
        code, correct_id, difficulty = keys[q["question_version_id"]]
        wrong_id = next(o["id"] for o in q["options"] if o["id"] != correct_id)
        choice = correct_id if code == "DEMO-C1" or difficulty == "foundational" else wrong_id
        saved = client.put(f"/api/v1/attempts/{attempt['id']}/answers/{q['question_version_id']}",
                           json={"selected_option_id": choice}, headers={"X-CSRF-Token": csrf})
        assert saved.status_code == 200, saved.text
    assert client.get(f"/api/v1/attempts/{attempt['id']}").json()["answered_count"] == 10

    submitted = client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers={"X-CSRF-Token": csrf})
    assert submitted.status_code == 200, submitted.text
    body = submitted.json()
    # (7 + 2) / 14 weighted points
    assert body["status"] == "scored" and Decimal(body["score_total"]) == Decimal("0.64286") and body["is_baseline"]

    result = client.get(f"/api/v1/attempts/{attempt['id']}/result").json()
    by_code = {c["competency"]["code"]: c for c in result["competencies"]}
    assert Decimal(by_code["DEMO-C1"]["score"]) == Decimal("1.00000") and by_code["DEMO-C1"]["level_number"] == 4
    assert Decimal(by_code["DEMO-C2"]["score"]) == Decimal("0.28571") and by_code["DEMO-C2"]["level_number"] == 1
    assert all(c["evidence_band"] == "medium" for c in result["competencies"])
    assert all("explanation" in q and "correct_option_id" in q for q in result["questions"])

    profile = client.get("/api/v1/me/competency-profile").json()
    assert {i["competency"]["code"]: Decimal(i["score"]) for i in profile["items"]} == {
        "DEMO-C1": Decimal("1.00000"), "DEMO-C2": Decimal("0.28571")}
    assert all(i["explanation"]["method_version"] == "score-v1" and i["explanation"]["limitations"] for i in profile["items"])

    gaps = client.get("/api/v1/me/competency-gaps").json()
    statuses = {i["competency"]["code"]: (i["status"], i["gap"]) for i in gaps["items"]}
    assert statuses == {"DEMO-C2": ("gap", 2), "DEMO-C1": ("meets_requirement", 0)}
    assert gaps["summary"]["gap"] == 1

    recs = client.get("/api/v1/me/recommendations").json()
    assert recs["rule_version"] == "rec-v1" and recs["igot"]["included"] is False
    assert [(r["rank"], r["course"]["title"], Decimal(r["score"])) for r in recs["items"]] == [
        (1, "DEMO - Percentages refresher (synthetic course)", Decimal("0.66667")),
        (2, "DEMO - Reading simple data tables (synthetic course)", Decimal("0.33333")),
    ]
    assert all(r["course"]["is_demo"] and r["provenance"]["is_demo"] and r["reasons"] for r in recs["items"])
    # Recommendations are deterministic
    assert client.get("/api/v1/me/recommendations").json()["items"] == recs["items"]

    with factory() as db:
        user = db.scalar(select(User).where(User.email == email))
        actions = [a for a in db.scalars(select(AuditLog.action).where(AuditLog.actor_user_id == user.id).order_by(AuditLog.id))]
    assert actions == ["auth.login.success", "user.job_role.change", "attempt.submit"]


def test_answer_keys_never_in_delivery_responses(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    onboard(client, csrf)
    attempt = start(client, csrf)
    leaked_keys = {"is_correct", "correct_option_id", "explanation"}

    def keys(value):
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(v) for v in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(v) for v in value)) if value else set()
        return set()

    assert not keys(attempt) & leaked_keys
    assert not keys(client.get(f"/api/v1/attempts/{attempt['id']}").json()) & leaked_keys
    q = attempt["questions"][0]
    saved = client.put(f"/api/v1/attempts/{attempt['id']}/answers/{q['question_version_id']}",
                       json={"selected_option_id": q["options"][0]["id"]}, headers={"X-CSRF-Token": csrf})
    assert not keys(saved.json()) & leaked_keys
    # No option text or explanation text from the key leaks either: explanations are only in the scored result.
    assert "DEMO item" not in client.get(f"/api/v1/attempts/{attempt['id']}").text
    problem(client.get(f"/api/v1/attempts/{attempt['id']}/result"), 409, "ATTEMPT_NOT_SCORED")


def test_unanswered_questions_score_as_incorrect_with_insufficient_gaps_hidden(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    onboard(client, csrf)
    attempt = start(client, csrf)
    submitted = client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers={"X-CSRF-Token": csrf}).json()
    assert Decimal(submitted["score_total"]) == Decimal("0")
    gaps = client.get("/api/v1/me/competency-gaps").json()
    assert {(i["status"], i["gap"]) for i in gaps["items"]} == {("gap", 2)}  # level 1 vs required 3, band medium


# --- Invalid input -----------------------------------------------------------


@pytest.mark.parametrize("payload", [
    {"email": "not-an-email", "password": "x"},
    {"email": "a@example.invalid"},
    {"email": "a@example.invalid", "password": ""},
    {"email": "a@example.invalid", "password": "x", "role": "org_admin"},
])
def test_login_validation(client, payload):
    body = problem(client.post("/api/v1/auth/login", json=payload), 422, "VALIDATION_FAILED")
    assert body["errors"]


def test_wrong_password_and_unknown_email_are_indistinguishable(client, factory, org_id):
    email = make_user(factory, org_id)
    wrong = problem(client.post("/api/v1/auth/login", json={"email": email, "password": "wrong-password"}), 401,
                    "INVALID_CREDENTIALS")
    unknown = problem(client.post("/api/v1/auth/login", json={"email": "nobody@example.invalid", "password": "x"}), 401,
                      "INVALID_CREDENTIALS")
    assert wrong["detail"] == unknown["detail"]
    assert "platform_session" not in client.cookies


def test_inactive_user_cannot_login(client, factory, org_id):
    problem(client.post("/api/v1/auth/login", json={"email": make_user(factory, org_id, status="inactive"),
                                                    "password": PASSWORD}), 401, "INVALID_CREDENTIALS")


def test_lockout_after_threshold(client, factory, org_id):
    email = make_user(factory, org_id)
    for _ in range(5):
        problem(client.post("/api/v1/auth/login", json={"email": email, "password": "wrong-password"}), 401,
                "INVALID_CREDENTIALS")
    locked = client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    problem(locked, 423, "ACCOUNT_LOCKED")
    assert int(locked.headers["retry-after"]) > 0
    with factory() as db:
        user = db.scalar(select(User).where(User.email == email))
        assert db.scalar(select(AuditLog).where(AuditLog.target_id == str(user.id), AuditLog.action == "auth.lockout"))


def test_notice_version_must_match(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    problem(client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": "old"},
                        headers={"X-CSRF-Token": csrf}), 409, "NOTICE_VERSION_OUTDATED")


def test_job_role_selection_errors(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    headers = {"X-CSRF-Token": csrf}
    problem(client.put("/api/v1/me/job-role", json={"job_role_id": str(uuid.uuid4())}, headers=headers), 404, "NOT_FOUND")
    problem(client.put("/api/v1/me/job-role", json={"job_role_id": "not-a-uuid"}, headers=headers), 422, "VALIDATION_FAILED")
    problem(client.put("/api/v1/me/job-role", json={}, headers=headers), 422, "VALIDATION_FAILED")


def test_other_organisation_job_role_is_not_found(client, factory, org_id):
    other_org = _make_org(factory)
    with factory() as db:
        from app.modules.organization.models import JobRole
        foreign_role = db.scalar(select(JobRole).where(JobRole.organization_id == other_org, JobRole.code == JOB_ROLE_CODE))
    csrf = login(client, make_user(factory, org_id))
    problem(client.get(f"/api/v1/job-roles/{foreign_role.id}/competencies"), 404, "NOT_FOUND")
    problem(client.put("/api/v1/me/job-role", json={"job_role_id": str(foreign_role.id)},
                       headers={"X-CSRF-Token": csrf}), 404, "NOT_FOUND")


def test_start_requires_notice_then_job_role(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    headers = {"X-CSRF-Token": csrf}
    with factory() as db:
        from app.modules.assessment.models import Assessment
        assessment = db.scalar(select(Assessment).where(Assessment.organization_id == org_id))
    problem(client.post(f"/api/v1/assessments/{assessment.id}/attempts", headers=headers), 409, "NOTICE_NOT_ACKNOWLEDGED")
    version = client.get("/api/v1/me").json()["notice"]["version"]
    client.post("/api/v1/me/notice-acknowledgements", json={"notice_version": version}, headers=headers)
    problem(client.post(f"/api/v1/assessments/{assessment.id}/attempts", headers=headers), 409, "JOB_ROLE_REQUIRED")
    problem(client.get("/api/v1/me/competency-gaps"), 409, "JOB_ROLE_REQUIRED")
    problem(client.get("/api/v1/me/recommendations"), 409, "JOB_ROLE_REQUIRED")
    assert client.get("/api/v1/assessments").json() == []


def test_answer_and_submit_errors(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    headers = {"X-CSRF-Token": csrf}
    onboard(client, csrf)
    attempt = start(client, csrf)
    q1, q2 = attempt["questions"][0], attempt["questions"][1]
    base = f"/api/v1/attempts/{attempt['id']}"
    problem(client.put(f"{base}/answers/{q1['question_version_id']}", json={"selected_option_id": q2["options"][0]["id"]},
                       headers=headers), 422, "INVALID_OPTION")
    problem(client.put(f"{base}/answers/{uuid.uuid4()}", json={"selected_option_id": None}, headers=headers), 404, "NOT_FOUND")
    problem(client.put(f"{base}/answers/{q1['question_version_id']}", json={"selected_option_id": None, "is_correct": True},
                       headers=headers), 422, "VALIDATION_FAILED")
    assert client.put(f"{base}/answers/{q1['question_version_id']}", json={"selected_option_id": None},
                      headers=headers).status_code == 200
    assert client.post(f"{base}/submit", headers=headers).status_code == 200
    problem(client.post(f"{base}/submit", headers=headers), 409, "ATTEMPT_NOT_IN_PROGRESS")
    problem(client.put(f"{base}/answers/{q1['question_version_id']}", json={"selected_option_id": q1["options"][0]["id"]},
                       headers=headers), 409, "ATTEMPT_NOT_IN_PROGRESS")
    problem(client.post(f"/api/v1/assessments/{attempt['assessment']['id']}/attempts", headers=headers), 409,
            "ASSESSMENT_ALREADY_COMPLETED")
    problem(client.get("/api/v1/attempts/not-a-uuid"), 422, "VALIDATION_FAILED")


# --- Authorisation -----------------------------------------------------------

READ_ENDPOINTS = ["/api/v1/auth/session", "/api/v1/me", "/api/v1/job-roles", f"/api/v1/job-roles/{uuid.uuid4()}/competencies",
                  "/api/v1/assessments", f"/api/v1/attempts/{uuid.uuid4()}", f"/api/v1/attempts/{uuid.uuid4()}/result",
                  "/api/v1/me/competency-profile", "/api/v1/me/competency-gaps", "/api/v1/me/recommendations"]
WRITE_ENDPOINTS = [("post", "/api/v1/auth/logout", None), ("post", "/api/v1/me/notice-acknowledgements", {"notice_version": "x"}),
                   ("put", "/api/v1/me/job-role", {"job_role_id": str(uuid.uuid4())}),
                   ("post", f"/api/v1/assessments/{uuid.uuid4()}/attempts", None),
                   ("put", f"/api/v1/attempts/{uuid.uuid4()}/answers/{uuid.uuid4()}", {"selected_option_id": None}),
                   ("post", f"/api/v1/attempts/{uuid.uuid4()}/submit", None)]


@pytest.mark.parametrize("path", READ_ENDPOINTS)
def test_read_endpoints_require_session(client, path):
    problem(client.get(path), 401, "UNAUTHENTICATED")


@pytest.mark.parametrize("method,path,body", WRITE_ENDPOINTS)
def test_write_endpoints_require_session(client, method, path, body):
    problem(getattr(client, method)(path, json=body), 401, "UNAUTHENTICATED")


@pytest.mark.parametrize("method,path,body", WRITE_ENDPOINTS)
def test_write_endpoints_require_csrf(client, factory, org_id, method, path, body):
    login(client, make_user(factory, org_id))
    problem(getattr(client, method)(path, json=body), 403, "CSRF_FAILED")
    problem(getattr(client, method)(path, json=body, headers={"X-CSRF-Token": "0" * 64}), 403, "CSRF_FAILED")


def test_logout_revokes_session(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    assert client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": csrf}).status_code == 204
    problem(client.get("/api/v1/me"), 401, "UNAUTHENTICATED")


def test_expired_session_rejected(client, factory, org_id):
    email = make_user(factory, org_id)
    login(client, email)
    with factory() as db:
        user = db.scalar(select(User).where(User.email == email))
        db.execute(text("UPDATE sessions SET idle_expires_at = :t WHERE user_id = :u"),
                   {"t": datetime.now(timezone.utc) - timedelta(minutes=1), "u": user.id})
        db.commit()
    problem(client.get("/api/v1/me"), 401, "UNAUTHENTICATED")


def test_cookie_flags(client, factory, org_id):
    response = client.post("/api/v1/auth/login", json={"email": make_user(factory, org_id), "password": PASSWORD})
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie and "path=/" in cookie
    with factory() as db:
        rows = db.scalars(select(SessionRow.id)).all()
    token = response.cookies.get("platform_session")
    assert token not in rows  # only the hash is stored


def test_other_users_attempt_is_not_found(client, factory, org_id):
    csrf = login(client, make_user(factory, org_id))
    onboard(client, csrf)
    attempt = start(client, csrf)
    client.cookies.clear()
    other_csrf = login(client, make_user(factory, org_id))
    problem(client.get(f"/api/v1/attempts/{attempt['id']}"), 404, "NOT_FOUND")
    problem(client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers={"X-CSRF-Token": other_csrf}), 404, "NOT_FOUND")


@pytest.mark.parametrize("role", ["auditor", "platform_admin"])
def test_non_learning_roles_cannot_take_assessments(client, factory, org_id, role):
    csrf = login(client, make_user(factory, org_id, role=role))
    assert client.get("/api/v1/me").json()["can_take_assessments"] is False
    problem(client.get("/api/v1/assessments"), 403, "FORBIDDEN")
    problem(client.get("/api/v1/me/competency-gaps"), 403, "FORBIDDEN")
    problem(client.post(f"/api/v1/assessments/{uuid.uuid4()}/attempts", headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")


# --- Demo seed and ledger integrity ------------------------------------------


def test_demo_content_refused_outside_local_and_ci(factory, org_id):
    with factory() as db:
        org = db.get(Organization, org_id)
        for env in (AppEnv.staging, AppEnv.pilot, AppEnv.production):
            with pytest.raises(SeedRefused):
                seed_demo_content(db, org, env)
        assert seed_demo_content(db, org, AppEnv.ci) == {}  # idempotent


def test_every_demo_question_has_exactly_one_correct_option(factory, org_id):
    with factory() as db:
        versions = db.scalars(select(QuestionVersion).where(QuestionVersion.organization_id == org_id)).all()
        assert len(versions) == 10
        for version in versions:
            options = db.scalars(select(QuestionOption).where(QuestionOption.question_version_id == version.id)).all()
            assert len(options) == 4 and sum(o.is_correct for o in options) == 1
            assert "DEMO item" in version.explanation


def test_append_only_tables_reject_updates(factory, org_id):
    with factory() as db:
        version = db.scalar(select(QuestionVersion).where(QuestionVersion.organization_id == org_id))
        for statement in ("UPDATE question_versions SET stem = 'changed' WHERE id = :id",
                          "UPDATE question_options SET is_correct = NOT is_correct WHERE question_version_id = :id"):
            with pytest.raises(Exception, match="append_only"):
                db.execute(text(statement), {"id": version.id})
            db.rollback()


def test_evidence_only_void_columns_settable_once(client, factory, org_id):
    email = make_user(factory, org_id)
    csrf = login(client, email)
    onboard(client, csrf)
    attempt = start(client, csrf)
    client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers={"X-CSRF-Token": csrf})
    with factory() as db:
        evidence_id = db.execute(text("SELECT id FROM competency_evidence WHERE attempt_id = :a LIMIT 1"),
                                 {"a": attempt["id"]}).scalar()
        with pytest.raises(Exception, match="append_only"):
            db.execute(text("UPDATE competency_evidence SET is_correct = true WHERE id = :id"), {"id": evidence_id})
        db.rollback()
        db.execute(text("UPDATE competency_evidence SET voided_at = now(), void_reason = 'test' WHERE id = :id"),
                   {"id": evidence_id})
        db.commit()
        with pytest.raises(Exception, match="append_only"):
            db.execute(text("UPDATE competency_evidence SET void_reason = 'again' WHERE id = :id"), {"id": evidence_id})
        db.rollback()
        with pytest.raises(Exception, match="append_only"):
            db.execute(text("DELETE FROM competency_evidence WHERE id = :id"), {"id": evidence_id})
        db.rollback()
        with pytest.raises(Exception, match="append_only"):
            db.execute(text("UPDATE notice_acknowledgements SET notice_version = 'x' WHERE user_id = "
                            "(SELECT id FROM users WHERE email = :e)"), {"e": email})
        db.rollback()


def test_single_baseline_and_single_open_attempt_constraints(factory, org_id):
    with factory() as db:
        attempts = db.scalars(select(AssessmentAttempt).where(AssessmentAttempt.organization_id == org_id,
                                                              AssessmentAttempt.is_baseline)).all()
        assert len({a.user_id for a in attempts}) == len(attempts)
        assert db.scalar(select(NoticeAcknowledgement.id).limit(1)) is not None
