"""Phase 4C content administration: question authoring and review, course publishing, audit trail, authorisation."""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

from app.core.config import AppEnv
from app.modules.assessment.models import Question
from app.modules.competency.models import Competency
from app.modules.governance.models import Approval, AuditLog
from app.modules.organization.models import Organization
from app.seed.demo_packs import CONTENT_PACKS, apply_demo_packs
from app.seed.demo_users import seed_demo_users
from tests.db.test_catalogue_api import _learner_with_baseline
from tests.db.test_vertical_slice_api import (  # noqa: F401 - fixtures are reused
    PASSWORD, client, factory, login, make_user, problem,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def content_org(factory) -> uuid.UUID:
    with factory() as db:
        org = Organization(code=f"content-{uuid.uuid4().hex[:10]}", name=f"Content {uuid.uuid4().hex[:10]}")
        db.add(org)
        db.flush()
        seed_demo_users(db, org, AppEnv.ci, PASSWORD)
        apply_demo_packs(db, org, AppEnv.ci, CONTENT_PACKS)
        db.commit()
        return org.id


def as_role(client, factory, org_id, role) -> dict:
    client.cookies.clear()
    csrf = login(client, make_user(factory, org_id, role))
    return {"X-CSRF-Token": csrf}


def competency_id(factory, org_id, code="DEMO-SP-TABLES") -> str:
    with factory() as db:
        return str(db.scalar(select(Competency.id).where(Competency.organization_id == org_id, Competency.code == code)))


def question_body(factory, org_id, **over) -> dict:
    body = {
        "competency_id": competency_id(factory, org_id), "difficulty": "foundational",
        "stem": "A table reports enrolment in thousands. What does the value 12.5 represent?",
        "explanation": "The unit is thousands, so 12.5 represents 12,500 people.",
        "options": [{"text": "12.5 people", "is_correct": False}, {"text": "12,500 people", "is_correct": True},
                    {"text": "1,25,000 people", "is_correct": False}, {"text": "125 people", "is_correct": False}],
        "sources": [],
    }
    body.update(over)
    return body


SYNTHETIC = [{"source_kind": "synthetic", "note": "Invented scenario and figures written for practice."}]


# --- Authorisation ------------------------------------------------------------------------------------------

READS = ["/api/v1/admin/questions", "/api/v1/admin/reviews", "/api/v1/admin/courses", "/api/v1/admin/competencies",
         "/api/v1/admin/assessments", "/api/v1/admin/audit"]


@pytest.mark.parametrize("path", READS)
def test_learners_cannot_reach_content_administration(client, factory, content_org, path):
    as_role(client, factory, content_org, "learner")
    problem(client.get(path), 403, "FORBIDDEN")


def test_capabilities_separate_authoring_courses_and_audit(client, factory, content_org):
    as_role(client, factory, content_org, "trainer")
    assert client.get("/api/v1/admin/questions").status_code == 200
    problem(client.get("/api/v1/admin/courses"), 403, "FORBIDDEN")
    problem(client.get("/api/v1/admin/audit"), 403, "FORBIDDEN")
    as_role(client, factory, content_org, "training_manager")
    assert client.get("/api/v1/admin/courses").status_code == 200
    problem(client.get("/api/v1/admin/questions"), 403, "FORBIDDEN")
    auditor = as_role(client, factory, content_org, "auditor")
    assert client.get("/api/v1/admin/audit").status_code == 200
    assert client.get("/api/v1/admin/competencies").status_code == 200
    problem(client.post("/api/v1/admin/courses", json={"title": "Nope", "provider_organisation": "Nowhere"}, headers=auditor),
            403, "FORBIDDEN")  # auditors are read-only


def test_writes_require_csrf(client, factory, content_org):
    as_role(client, factory, content_org, "trainer")
    problem(client.post("/api/v1/admin/questions", json=question_body(factory, content_org)), 403, "CSRF_FAILED")


# --- Question authoring and review -------------------------------------------------------------------------


def test_question_review_workflow_with_self_approval_block(client, factory, content_org):
    author = as_role(client, factory, content_org, "trainer")
    created = client.post("/api/v1/admin/questions", json=question_body(factory, content_org), headers=author)
    assert created.status_code == 201, created.text
    q = created.json()
    assert q["status"] == "draft" and q["current_version"]["version_number"] == 1

    # No source metadata: cannot be submitted
    problem(client.post(f"/api/v1/admin/questions/{q['id']}/submit", json={}, headers=author), 422, "SOURCE_REQUIRED")
    updated = client.put(f"/api/v1/admin/questions/{q['id']}", headers=author,
                         json={**question_body(factory, content_org, sources=SYNTHETIC), "row_version": q["row_version"]}).json()
    assert updated["current_version"]["version_number"] == 2
    assert updated["current_version"]["sources"][0]["status"] == "Invented for practice - not a citation"
    submitted = client.post(f"/api/v1/admin/questions/{q['id']}/submit", json={"note": "Ready"}, headers=author).json()
    assert submitted["status"] == "in_review" and not submitted["actions"]["can_edit"]
    problem(client.put(f"/api/v1/admin/questions/{q['id']}", headers=author,
                       json={**question_body(factory, content_org, sources=SYNTHETIC), "row_version": submitted["row_version"]}),
            409, "NOT_EDITABLE")

    task = next(t for t in client.get("/api/v1/admin/reviews").json() if t["target_id"] == q["id"])
    assert task["can_decide"] is False and "another reviewer" in task["blocked_reason"]
    problem(client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=author,
                        json={"decision": "approve", "row_version": 1}), 403, "SELF_REVIEW_BLOCKED")

    reviewer = as_role(client, factory, content_org, "competency_admin")
    task = next(t for t in client.get("/api/v1/admin/reviews").json() if t["target_id"] == q["id"])
    assert task["can_decide"] is True
    problem(client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                        json={"decision": "reject", "row_version": 1}), 422, "VALIDATION_FAILED")
    assert client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                       json={"decision": "request_changes", "reason": "Say the unit in the stem.", "row_version": 1}).status_code == 200
    detail = client.get(f"/api/v1/admin/questions/{q['id']}").json()
    assert detail["status"] == "draft" and detail["reviews"][0]["decision"] == "request_changes"
    problem(client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                        json={"decision": "approve", "row_version": 2}), 409, "TASK_CLOSED")

    # The original author revises and resubmits; a different reviewer approves the exact version
    client.cookies.clear()
    with factory() as db:
        creator = db.scalar(select(Question.created_by).where(Question.id == uuid.UUID(q["id"])))
        email = db.execute(text("SELECT email FROM users WHERE id = :id"), {"id": creator}).scalar()
    author = {"X-CSRF-Token": login(client, email)}
    detail = client.get(f"/api/v1/admin/questions/{q['id']}").json()
    client.put(f"/api/v1/admin/questions/{q['id']}", headers=author,
               json={**question_body(factory, content_org, sources=SYNTHETIC, stem="A table reports enrolment in thousands (unit shown in the title). What does 12.5 represent?"),
                     "row_version": detail["row_version"]})
    submitted = client.post(f"/api/v1/admin/questions/{q['id']}/submit", json={}, headers=author).json()
    reviewer = as_role(client, factory, content_org, "competency_admin")
    task = next(t for t in client.get("/api/v1/admin/reviews").json() if t["target_id"] == q["id"])
    assert client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                       json={"decision": "approve", "row_version": 1}).status_code == 200
    final = client.get(f"/api/v1/admin/questions/{q['id']}").json()
    assert final["status"] == "approved" and final["approved_version_id"] == submitted["current_version"]["id"]
    assert [v["version_number"] for v in final["versions"]] == [3, 2, 1]

    with factory() as db:
        actions = {a.action for a in db.scalars(select(AuditLog).where(AuditLog.target_id == q["id"]))}
        assert {"question.create", "question.update", "review.submit", "review.decide"} <= actions
        denied = db.scalar(select(AuditLog).where(AuditLog.target_id == q["id"], AuditLog.outcome == "denied"))
        assert denied.reason == "self_approval_blocked"
        approval = db.scalar(select(Approval).where(Approval.review_task_id == uuid.UUID(task["id"])))
        with pytest.raises(DBAPIError):
            db.execute(text("UPDATE approvals SET decision = 'reject' WHERE id = :id"), {"id": approval.id})
        db.rollback()


@pytest.mark.parametrize("override,code", [
    ({"options": [{"text": "A", "is_correct": True}, {"text": "B", "is_correct": True}, {"text": "C", "is_correct": False}]}, "ONE_CORRECT"),
    ({"options": [{"text": "Same", "is_correct": True}, {"text": "same", "is_correct": False}, {"text": "C", "is_correct": False}]}, "DUPLICATE_OPTIONS"),
    ({"sources": [{"source_kind": "external_reference", "title": "Some manual"}]}, "REFERENCE_INCOMPLETE"),
    ({"sources": [{"source_kind": "source_record", "source_record_id": str(uuid.uuid4())}]}, "UNKNOWN_SOURCE"),
    ({"sources": [{"source_kind": "synthetic", "note": "  "}]}, "SYNTHETIC_NOTE_REQUIRED"),
])
def test_question_validation(client, factory, content_org, override, code):
    headers = as_role(client, factory, content_org, "trainer")
    response = client.post("/api/v1/admin/questions", json=question_body(factory, content_org, **override), headers=headers)
    assert response.status_code == 422, response.text
    assert code in response.text


def test_questions_of_other_organisations_are_not_found(client, factory, content_org):
    with factory() as db:
        foreign = db.scalar(select(Question.id).where(Question.organization_id != content_org).limit(1))
    as_role(client, factory, content_org, "competency_admin")
    if foreign:
        problem(client.get(f"/api/v1/admin/questions/{foreign}"), 404, "NOT_FOUND")


def test_seeded_questions_used_by_published_assessments_cannot_be_retired(client, factory, content_org):
    headers = as_role(client, factory, content_org, "competency_admin")
    listing = client.get("/api/v1/admin/questions", params={"origin": "demo_seed", "status": "approved", "page_size": 1}).json()
    qid = listing["items"][0]["id"]
    assert client.get(f"/api/v1/admin/questions/{qid}").json()["actions"]["can_retire"] is False
    problem(client.post(f"/api/v1/admin/questions/{qid}/retire", headers=headers), 409, "USED_IN_PUBLISHED_ASSESSMENT")


# --- Courses ------------------------------------------------------------------------------------------------


LESSON = {"title": "Reading a unit", "lesson_type": "reading", "estimated_minutes": 6,
          "body_markdown": "Always read the **unit** before quoting a figure from a table."}


def test_course_publishing_guards_review_and_learner_visibility(client, factory, content_org):
    manager = as_role(client, factory, content_org, "training_manager")
    course = client.post("/api/v1/admin/courses", headers=manager, json={
        "title": "Units and footnotes clinic", "provider_organisation": "Internal training team (synthetic)", "difficulty": "foundational"}).json()
    cid = course["id"]
    assert course["state"] == "draft" and course["actions"]["can_submit"] is False

    # Not visible to learners while draft
    _learner_with_baseline(client, factory, content_org)
    problem(client.get(f"/api/v1/courses/{cid}"), 404, "NOT_FOUND")
    manager = as_role(client, factory, content_org, "training_manager")

    problem(client.post(f"/api/v1/admin/courses/{cid}/submit", json={}, headers=manager), 422, "SUBMIT_GUARDS_FAILED")
    detail = client.patch(f"/api/v1/admin/courses/{cid}", headers=manager,
                          json={"row_version": course["row_version"], "description": "A short clinic on units."}).json()
    detail = client.post(f"/api/v1/admin/courses/{cid}/modules", headers=manager, json={"title": "Units"}).json()
    module_id = detail["modules"][0]["id"]
    detail = client.post(f"/api/v1/admin/courses/{cid}/modules/{module_id}/lessons", headers=manager, json=LESSON).json()
    detail = client.put(f"/api/v1/admin/courses/{cid}/competencies", headers=manager,
                        json={"competency_id": competency_id(factory, content_org), "relevance": "primary"}).json()
    assert detail["competencies"][0]["status"] == "suggested" and detail["actions"]["can_submit"]
    problem(client.post(f"/api/v1/admin/courses/{cid}/publish", headers=manager), 409, "NOT_APPROVED")
    detail = client.post(f"/api/v1/admin/courses/{cid}/submit", json={}, headers=manager).json()
    assert detail["state"] == "in_review"
    problem(client.post(f"/api/v1/admin/courses/{cid}/modules", headers=manager, json={"title": "Sneaky"}), 409, "IN_REVIEW")

    task = next(t for t in client.get("/api/v1/admin/reviews").json() if t["target_id"] == cid)
    problem(client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=manager,
                        json={"decision": "approve", "row_version": 1}), 403, "SELF_REVIEW_BLOCKED")
    reviewer = as_role(client, factory, content_org, "org_admin")
    assert client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                       json={"decision": "approve", "row_version": 1}).status_code == 200
    approved = client.get(f"/api/v1/admin/courses/{cid}").json()
    assert approved["state"] == "approved" and approved["competencies"][0]["status"] == "approved"

    # Approved is not yet live
    _learner_with_baseline(client, factory, content_org)
    problem(client.get(f"/api/v1/courses/{cid}"), 404, "NOT_FOUND")

    reviewer = as_role(client, factory, content_org, "org_admin")
    published = client.post(f"/api/v1/admin/courses/{cid}/publish", headers=reviewer).json()
    assert published["state"] == "published" and published["published_at"]
    problem(client.patch(f"/api/v1/admin/courses/{cid}", headers=reviewer, json={"row_version": published["row_version"], "title": "Changed"}),
            409, "PUBLISHED")

    _learner_with_baseline(client, factory, content_org)
    learner_view = client.get(f"/api/v1/courses/{cid}").json()
    assert learner_view["learning_content"]["available"] is True
    outline = client.get(f"/api/v1/courses/{cid}/outline").json()
    assert outline["modules"][0]["lessons"][0]["title"] == "Reading a unit"

    reviewer = as_role(client, factory, content_org, "org_admin")
    assert client.post(f"/api/v1/admin/courses/{cid}/unpublish", headers=reviewer, json={"reason": "x"}).status_code == 422
    unpublished = client.post(f"/api/v1/admin/courses/{cid}/unpublish", headers=reviewer, json={"reason": "Content refresh"}).json()
    assert unpublished["state"] == "approved"
    edited = client.patch(f"/api/v1/admin/courses/{cid}", headers=reviewer,
                          json={"row_version": unpublished["row_version"], "title": "Units and footnotes clinic (revised)"}).json()
    assert edited["state"] == "draft" and edited["review_status"] == "unreviewed"  # approval does not carry over edits

    _learner_with_baseline(client, factory, content_org)
    problem(client.get(f"/api/v1/courses/{cid}"), 404, "NOT_FOUND")
    with factory() as db:
        actions = {a.action for a in db.scalars(select(AuditLog).where(AuditLog.target_id == cid))}
        assert {"course.create", "course.publish", "course.unpublish", "course.approval_reset", "review.decide"} <= actions


def test_request_changes_needs_a_reason_and_reopens_the_draft(client, factory, content_org):
    manager = as_role(client, factory, content_org, "training_manager")
    c = client.post("/api/v1/admin/courses", headers=manager, json={
        "title": "Footnotes clinic", "description": "Short.", "provider_organisation": "Internal (synthetic)"}).json()
    m = client.post(f"/api/v1/admin/courses/{c['id']}/modules", headers=manager, json={"title": "One"}).json()["modules"][0]["id"]
    client.post(f"/api/v1/admin/courses/{c['id']}/modules/{m}/lessons", headers=manager, json=LESSON)
    client.put(f"/api/v1/admin/courses/{c['id']}/competencies", headers=manager,
               json={"competency_id": competency_id(factory, content_org), "relevance": "secondary"})
    client.post(f"/api/v1/admin/courses/{c['id']}/submit", json={}, headers=manager)
    reviewer = as_role(client, factory, content_org, "competency_admin")
    task = next(t for t in client.get("/api/v1/admin/reviews").json() if t["target_id"] == c["id"])
    problem(client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                        json={"decision": "request_changes", "row_version": 1}), 422, "VALIDATION_FAILED")
    client.post(f"/api/v1/admin/reviews/{task['id']}/decision", headers=reviewer,
                json={"decision": "request_changes", "reason": "Add a practice check.", "row_version": 1})
    detail = client.get(f"/api/v1/admin/courses/{c['id']}").json()
    assert detail["state"] == "draft" and detail["reviews"][0]["reason"] == "Add a practice check."


# --- Read-only views ----------------------------------------------------------------------------------------


def test_competency_structure_and_assessment_guards(client, factory, content_org):
    as_role(client, factory, content_org, "competency_admin")
    structure = client.get("/api/v1/admin/competencies").json()
    stat = next(f for f in structure["frameworks"] if f["code"] == "DEMO-STAT-PRACTICE")
    assert len(stat["competencies"]) == 8 and all(c["approved_questions"] >= 5 for c in stat["competencies"])
    jso = next(r for r in structure["job_roles"] if r["code"] == "DEMO-ROLE-JSO")
    assert len(jso["requirements"]) == 4
    assessments = client.get("/api/v1/admin/assessments").json()
    jso_assessment = next(a for a in assessments if a["job_role"] and a["job_role"]["name"] == jso["name"])
    assert jso_assessment["item_count"] == 20
    assert {c["id"]: c["passed"] for c in jso_assessment["checks"]} == {"approved_items": True, "coverage": True, "sources": True}


def test_audit_trail_is_filterable_and_paginated(client, factory, content_org):
    as_role(client, factory, content_org, "auditor")
    first = client.get("/api/v1/admin/audit", params={"limit": 5}).json()
    assert len(first["items"]) == 5 and first["next_before_id"]
    second = client.get("/api/v1/admin/audit", params={"limit": 5, "before_id": first["next_before_id"]}).json()
    assert all(i["id"] < first["next_before_id"] for i in second["items"])
    seeds = client.get("/api/v1/admin/audit", params={"action": "seed."}).json()
    assert seeds["items"] and all(i["action"].startswith("seed.") for i in seeds["items"])
    everything = client.get("/api/v1/admin/audit", params={"limit": 200}).text.lower()
    assert "argon2" not in everything and "token_hash" not in everything and "is_correct" not in everything
    problem(client.get("/api/v1/admin/audit", params={"action": "DROP TABLE"}), 422, "VALIDATION_FAILED")
