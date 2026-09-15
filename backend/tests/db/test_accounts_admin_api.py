"""Phase 4A: learner registration, password flows, profile and user/department administration.

Runs against the real PostgreSQL test database. Each module gets its own organisation; tests create the users they need.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.core.db import get_db
from app.main import create_app
from app.modules.governance.models import AuditLog
from app.modules.identity.models import PasswordResetToken, Session as SessionRow, User, UserAccessRole
from app.modules.identity.security import hash_password
from app.modules.organization.models import Department, Organization
from tests.conftest import make_settings

pytestmark = pytest.mark.db

PASSWORD = "Test-demo-password-123"
NEW_PASSWORD = "Another-strong-pass-456"


@pytest.fixture(scope="module")
def factory(migrated_engine) -> sessionmaker[Session]:
    return sessionmaker(bind=migrated_engine, expire_on_commit=False)


@pytest.fixture(scope="module")
def org(factory) -> dict:
    with factory() as db:
        org = Organization(code=f"acct-{uuid.uuid4().hex[:10]}", name=f"Accounts test {uuid.uuid4().hex[:8]}")
        db.add(org)
        db.flush()
        north = Department(organization_id=org.id, name="North Division", code="north")
        south = Department(organization_id=org.id, name="South Division", code="south")
        db.add_all([north, south])
        db.commit()
        return {"id": org.id, "code": org.code, "north": north.id, "south": south.id}


def _client(factory, test_database_url, **settings) -> Iterator[TestClient]:
    app = create_app(make_settings(database_url=test_database_url, **settings))

    def override_db():
        db = factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def client(factory, test_database_url) -> Iterator[TestClient]:
    yield from _client(factory, test_database_url)


def make_user(factory, org, roles=("learner",), *, department="north", scope=None, status="active") -> tuple[uuid.UUID, str]:
    email = f"{roles[0]}-{uuid.uuid4().hex[:8]}@example.invalid"
    with factory() as db:
        user = User(organization_id=org["id"], email=email, display_name=f"Test {roles[0]}", status=status,
                    department_id=org[department] if department else None,
                    password_hash=hash_password(PASSWORD), is_synthetic=True)
        db.add(user)
        db.flush()
        for role in roles:
            scope_id = org[scope or department] if role in ("department_admin", "trainer", "training_manager") else None
            db.add(UserAccessRole(organization_id=org["id"], user_id=user.id, role=role, department_scope_id=scope_id))
        db.commit()
        return user.id, email


def login(client, email, password=PASSWORD) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["csrf_token"]


def problem(response, status, code):
    assert response.status_code == status, response.text
    assert response.json()["code"] == code, response.text
    return response.json()


def registration(org, **overrides) -> dict:
    body = {"display_name": "New Learner", "email": f"new-{uuid.uuid4().hex[:8]}@example.invalid",
            "password": PASSWORD, "registration_id": f"REG-{uuid.uuid4().hex[:8]}", "organization_code": org["code"],
            "department_id": str(org["north"])}
    body.update(overrides)
    return body


# --- Registration ------------------------------------------------------------------------------------------


def test_registration_creates_active_learner_and_signs_in(client, factory, org):
    body = registration(org)
    options = client.get("/api/v1/auth/registration-options", params={"organization_code": org["code"]}).json()
    assert options["enabled"] is True
    assert {d["name"] for d in options["departments"]} >= {"North Division", "South Division"}

    response = client.post("/api/v1/auth/register", json=body)
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["user"]["access_roles"] == ["learner"]
    assert payload["user"]["admin_capabilities"] == []
    assert payload["user"]["registration_id"] == body["registration_id"]
    assert payload["user"]["department"]["name"] == "North Division"
    assert "password_hash" not in response.text and body["password"] not in response.text
    cookie = response.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie
    assert client.get("/api/v1/me").status_code == 200  # session cookie works

    with factory() as db:
        user = db.scalar(select(User).where(User.email == body["email"]))
        assert user.status == "active" and not user.is_synthetic
        assert user.password_hash.startswith("$argon2id$")
        assert db.scalar(select(AuditLog).where(AuditLog.action == "user.create", AuditLog.target_id == str(user.id)))


def test_registration_disabled_by_setting(factory, test_database_url, org):
    for client in _client(factory, test_database_url, learner_self_registration_enabled=False):
        assert client.get("/api/v1/auth/registration-options").json() == {
            "enabled": False, "organization_name": None, "departments": [], "job_roles": []}
        problem(client.post("/api/v1/auth/register", json=registration(org)), 403, "REGISTRATION_DISABLED")


def test_registration_cannot_be_enabled_outside_local_and_ci():
    with pytest.raises(ValueError):
        make_settings(app_env="production", learner_self_registration_enabled=True, session_cookie_secure=True)


def test_registration_rejects_duplicates_case_insensitively(client, org):
    body = registration(org)
    assert client.post("/api/v1/auth/register", json=body).status_code == 201
    client.cookies.clear()
    problem(client.post("/api/v1/auth/register", json=registration(org, email=body["email"].upper())), 409, "EMAIL_IN_USE")
    problem(client.post("/api/v1/auth/register", json=registration(org, registration_id=body["registration_id"].lower())),
            409, "REGISTRATION_ID_IN_USE")


@pytest.mark.parametrize("override", [
    {"password": "short"},
    {"email": "not-an-email"},
    {"registration_id": "a"},
    {"registration_id": "has space"},
    {"display_name": "x"},
    {"roles": ["org_admin"]},  # no mass assignment of roles
    {"department_id": str(uuid.uuid4())},
])
def test_registration_validation(client, org, override):
    response = client.post("/api/v1/auth/register", json=registration(org, **override))
    assert response.status_code == 422, response.text


def test_registration_rejects_other_organisations_department(client, factory, org):
    with factory() as db:
        other = Organization(code=f"other-{uuid.uuid4().hex[:8]}", name=f"Other {uuid.uuid4().hex[:8]}")
        db.add(other)
        db.flush()
        dept = Department(organization_id=other.id, name="Elsewhere")
        db.add(dept)
        db.commit()
        dept_id = dept.id
    problem(client.post("/api/v1/auth/register", json=registration(org, department_id=str(dept_id))), 422, "VALIDATION_FAILED")


def test_registration_does_not_log_password(client, org, capfd):
    body = registration(org)
    capfd.readouterr()
    assert client.post("/api/v1/auth/register", json=body).status_code == 201
    out, err = capfd.readouterr()
    assert body["password"] not in out + err
    assert body["registration_id"] not in out + err


# --- Password flows and profile ----------------------------------------------------------------------------


def test_password_change_revokes_other_sessions(client, factory, test_database_url, org):
    user_id, email = make_user(factory, org)
    for other in _client(factory, test_database_url):
        login(other, email)
        csrf = login(client, email)
        problem(client.post("/api/v1/auth/password/change", json={"current_password": "wrong-password-1", "new_password": NEW_PASSWORD},
                            headers={"X-CSRF-Token": csrf}), 422, "CURRENT_PASSWORD_INCORRECT")
        assert client.post("/api/v1/auth/password/change", json={"current_password": PASSWORD, "new_password": NEW_PASSWORD}).status_code == 403
        response = client.post("/api/v1/auth/password/change", json={"current_password": PASSWORD, "new_password": NEW_PASSWORD},
                               headers={"X-CSRF-Token": csrf})
        assert response.status_code == 204, response.text
        assert client.get("/api/v1/me").status_code == 200  # this session stays
        assert other.get("/api/v1/me").status_code == 401  # the other session is revoked
    client.cookies.clear()
    assert client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD}).status_code == 401
    login(client, email, NEW_PASSWORD)


def test_profile_update(client, factory, org):
    _, email = make_user(factory, org)
    csrf = login(client, email)
    response = client.patch("/api/v1/me", json={"display_name": "Renamed Person", "department_id": str(org["south"])},
                            headers={"X-CSRF-Token": csrf})
    assert response.status_code == 200, response.text
    assert response.json()["display_name"] == "Renamed Person"
    assert response.json()["department"]["name"] == "South Division"
    assert client.patch("/api/v1/me", json={"email": "x@example.invalid"}, headers={"X-CSRF-Token": csrf}).status_code == 422
    assert client.patch("/api/v1/me", json={"status": "active"}, headers={"X-CSRF-Token": csrf}).status_code == 422


# --- Administration: authorisation -------------------------------------------------------------------------


ADMIN_READS = ["/api/v1/admin/users", "/api/v1/admin/departments", "/api/v1/admin/roles"]


@pytest.mark.parametrize("path", ADMIN_READS)
def test_admin_reads_require_session(client, path):
    problem(client.get(path), 401, "UNAUTHENTICATED")


@pytest.mark.parametrize("role", ["learner", "auditor", "trainer", "competency_admin", "training_manager"])
def test_roles_without_user_capability_are_forbidden(client, factory, org, role):
    _, email = make_user(factory, org, (role,))
    csrf = login(client, email)
    for path in ADMIN_READS:
        problem(client.get(path), 403, "FORBIDDEN")
    problem(client.post("/api/v1/admin/users", json={"display_name": "X Y", "email": "xy@example.invalid"},
                        headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")


def test_me_reports_admin_capabilities(client, factory, org):
    _, email = make_user(factory, org, ("org_admin",))
    login(client, email)
    caps = client.get("/api/v1/me").json()["admin_capabilities"]
    assert {"users.manage", "roles.assign", "departments.manage", "audit.view"} <= set(caps)


def test_admin_writes_require_csrf(client, factory, org):
    _, email = make_user(factory, org, ("org_admin",))
    login(client, email)
    problem(client.post("/api/v1/admin/users", json={"display_name": "X Y", "email": "xy@example.invalid"}), 403, "CSRF_FAILED")


# --- Administration: user lifecycle ------------------------------------------------------------------------


def test_org_admin_invites_user_who_sets_password_once(client, factory, org):
    _, admin_email = make_user(factory, org, ("org_admin",))
    csrf = login(client, admin_email)
    email = f"invitee-{uuid.uuid4().hex[:8]}@example.invalid"
    response = client.post("/api/v1/admin/users", headers={"X-CSRF-Token": csrf}, json={
        "display_name": "Invited Trainer", "email": email, "department_id": str(org["north"]),
        "roles": [{"role": "trainer"}, {"role": "learner"}]})
    assert response.status_code == 201, response.text
    created = response.json()
    assert created["user"]["status"] == "invited" and created["user"]["has_password"] is False
    assert {r["role"] for r in created["user"]["roles"]} == {"trainer", "learner"}
    assert "password_hash" not in response.text and "token_hash" not in response.text
    token = created["setup"]["token"]

    with factory() as db:
        stored = db.scalar(select(PasswordResetToken).where(PasswordResetToken.user_id == uuid.UUID(created["user"]["id"])))
        assert stored.token_hash != token and len(stored.token_hash) == 64

    client.cookies.clear()
    assert client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD}).status_code == 401
    assert client.post("/api/v1/auth/password/set", json={"token": token, "new_password": NEW_PASSWORD}).status_code == 204
    problem(client.post("/api/v1/auth/password/set", json={"token": token, "new_password": NEW_PASSWORD}), 400, "TOKEN_INVALID")
    login(client, email, NEW_PASSWORD)


def test_expired_and_superseded_tokens_are_rejected(client, factory, org):
    user_id, _ = make_user(factory, org)
    _, admin_email = make_user(factory, org, ("org_admin",))
    csrf = login(client, admin_email)
    first = client.post(f"/api/v1/admin/users/{user_id}/password-link", headers={"X-CSRF-Token": csrf}).json()
    second = client.post(f"/api/v1/admin/users/{user_id}/password-link", headers={"X-CSRF-Token": csrf}).json()
    assert second["purpose"] == "password_reset"
    problem(client.post("/api/v1/auth/password/set", json={"token": first["token"], "new_password": NEW_PASSWORD}), 400, "TOKEN_INVALID")
    with factory() as db:
        for row in db.scalars(select(PasswordResetToken).where(PasswordResetToken.user_id == user_id, PasswordResetToken.used_at.is_(None))):
            row.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db.commit()
    problem(client.post("/api/v1/auth/password/set", json={"token": second["token"], "new_password": NEW_PASSWORD}), 400, "TOKEN_INVALID")


def test_deactivation_revokes_sessions_and_blocks_login(client, factory, test_database_url, org):
    user_id, email = make_user(factory, org)
    _, admin_email = make_user(factory, org, ("org_admin",))
    for learner in _client(factory, test_database_url):
        login(learner, email)
        csrf = login(client, admin_email)
        version = client.get(f"/api/v1/admin/users/{user_id}").json()["row_version"]
        response = client.patch(f"/api/v1/admin/users/{user_id}", json={"row_version": version, "status": "inactive"},
                                headers={"X-CSRF-Token": csrf})
        assert response.status_code == 200, response.text
        assert learner.get("/api/v1/me").status_code == 401
        learner.cookies.clear()
        assert learner.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD}).status_code == 401
        problem(client.patch(f"/api/v1/admin/users/{user_id}", json={"row_version": version, "status": "active"},
                             headers={"X-CSRF-Token": csrf}), 409, "STALE_VERSION")


def test_admin_cannot_change_own_roles_or_status(client, factory, org):
    admin_id, admin_email = make_user(factory, org, ("org_admin",))
    csrf = login(client, admin_email)
    version = client.get(f"/api/v1/admin/users/{admin_id}").json()["row_version"]
    problem(client.patch(f"/api/v1/admin/users/{admin_id}", json={"row_version": version, "status": "inactive"},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")
    problem(client.patch(f"/api/v1/admin/users/{admin_id}", json={"row_version": version, "roles": [{"role": "learner"}]},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")


def test_org_admin_cannot_grant_or_manage_platform_admin(client, factory, org):
    user_id, _ = make_user(factory, org)
    platform_id, _ = make_user(factory, org, ("platform_admin",))
    _, admin_email = make_user(factory, org, ("org_admin",))
    csrf = login(client, admin_email)
    version = client.get(f"/api/v1/admin/users/{user_id}").json()["row_version"]
    problem(client.patch(f"/api/v1/admin/users/{user_id}", json={"row_version": version, "roles": [{"role": "platform_admin"}]},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")
    version = client.get(f"/api/v1/admin/users/{platform_id}").json()["row_version"]
    problem(client.patch(f"/api/v1/admin/users/{platform_id}", json={"row_version": version, "status": "inactive"},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")


def test_role_change_is_audited_and_revokes_sessions(client, factory, test_database_url, org):
    user_id, email = make_user(factory, org)
    _, admin_email = make_user(factory, org, ("org_admin",))
    for learner in _client(factory, test_database_url):
        login(learner, email)
        csrf = login(client, admin_email)
        version = client.get(f"/api/v1/admin/users/{user_id}").json()["row_version"]
        response = client.patch(f"/api/v1/admin/users/{user_id}", headers={"X-CSRF-Token": csrf}, json={
            "row_version": version, "roles": [{"role": "learner"}, {"role": "department_admin"}]})
        assert response.status_code == 200, response.text
        roles = {(r["role"], r["department_scope_id"]) for r in response.json()["roles"]}
        assert roles == {("learner", None), ("department_admin", str(org["north"]))}
        assert learner.get("/api/v1/me").status_code == 401
    with factory() as db:
        entry = db.scalar(select(AuditLog).where(AuditLog.action == "user.update", AuditLog.target_id == str(user_id)))
        assert entry.before["roles"] == ["learner"] and entry.after["roles"] == ["department_admin", "learner"]


def test_department_admin_is_scoped_to_own_department(client, factory, org):
    north_learner, _ = make_user(factory, org, department="north")
    south_learner, _ = make_user(factory, org, department="south")
    north_trainer, _ = make_user(factory, org, ("trainer",), department="north")
    _, email = make_user(factory, org, ("department_admin",), department="north")
    csrf = login(client, email)

    listed = {u["id"] for u in client.get("/api/v1/admin/users", params={"page_size": 100}).json()["items"]}
    assert str(north_learner) in listed and str(south_learner) not in listed
    assert {d["name"] for d in client.get("/api/v1/admin/departments").json()} == {"North Division"}
    problem(client.get(f"/api/v1/admin/users/{south_learner}"), 404, "NOT_FOUND")

    # Learners in own department only; no admin roles; cannot manage admin accounts.
    ok = client.post("/api/v1/admin/users", headers={"X-CSRF-Token": csrf}, json={
        "display_name": "North Learner", "email": f"n-{uuid.uuid4().hex[:6]}@example.invalid", "department_id": str(org["north"])})
    assert ok.status_code == 201, ok.text
    problem(client.post("/api/v1/admin/users", headers={"X-CSRF-Token": csrf}, json={
        "display_name": "South Learner", "email": f"s-{uuid.uuid4().hex[:6]}@example.invalid", "department_id": str(org["south"])}),
        403, "FORBIDDEN")
    problem(client.post("/api/v1/admin/users", headers={"X-CSRF-Token": csrf}, json={
        "display_name": "Sneaky", "email": f"x-{uuid.uuid4().hex[:6]}@example.invalid", "department_id": str(org["north"]),
        "roles": [{"role": "org_admin"}]}), 403, "FORBIDDEN")
    version = client.get(f"/api/v1/admin/users/{north_trainer}").json()["row_version"]
    problem(client.patch(f"/api/v1/admin/users/{north_trainer}", json={"row_version": version, "status": "inactive"},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")
    version = client.get(f"/api/v1/admin/users/{north_learner}").json()["row_version"]
    problem(client.patch(f"/api/v1/admin/users/{north_learner}", json={"row_version": version, "department_id": str(org["south"])},
                         headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")
    problem(client.post("/api/v1/admin/departments", json={"name": "Rogue"}, headers={"X-CSRF-Token": csrf}), 403, "FORBIDDEN")


def test_other_organisation_users_are_not_found(client, factory, org):
    with factory() as db:
        other = Organization(code=f"iso-{uuid.uuid4().hex[:8]}", name=f"Isolated {uuid.uuid4().hex[:8]}")
        db.add(other)
        db.flush()
        stranger = User(organization_id=other.id, email=f"s-{uuid.uuid4().hex[:6]}@example.invalid", display_name="Stranger",
                        status="active", is_synthetic=True)
        db.add(stranger)
        db.commit()
        stranger_id = stranger.id
    _, email = make_user(factory, org, ("org_admin",))
    login(client, email)
    problem(client.get(f"/api/v1/admin/users/{stranger_id}"), 404, "NOT_FOUND")
    assert str(stranger_id) not in client.get("/api/v1/admin/users", params={"page_size": 100}).text


def test_admin_user_list_filters_and_never_exposes_hashes(client, factory, org):
    _, email = make_user(factory, org, ("org_admin",))
    login(client, email)
    response = client.get("/api/v1/admin/users", params={"role": "org_admin", "status": "active", "page_size": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1 and len(body["items"]) <= 5
    assert all(any(r["role"] == "org_admin" for r in u["roles"]) for u in body["items"])
    assert "argon2" not in response.text and "password_hash" not in response.text


def test_departments_create_and_rename(client, factory, org):
    _, email = make_user(factory, org, ("org_admin",))
    csrf = login(client, email)
    name = f"Dept {uuid.uuid4().hex[:6]}"
    created = client.post("/api/v1/admin/departments", json={"name": name}, headers={"X-CSRF-Token": csrf})
    assert created.status_code == 201, created.text
    problem(client.post("/api/v1/admin/departments", json={"name": name.upper()}, headers={"X-CSRF-Token": csrf}), 409, "DEPARTMENT_EXISTS")
    dept_id = created.json()["id"]
    renamed = client.patch(f"/api/v1/admin/departments/{dept_id}", json={"name": name + " East", "status": "inactive"},
                           headers={"X-CSRF-Token": csrf})
    assert renamed.status_code == 200 and renamed.json()["status"] == "inactive"


def test_roles_matrix_lists_every_role_with_counts(client, factory, org):
    _, email = make_user(factory, org, ("org_admin",))
    login(client, email)
    roles = {r["role"]: r for r in client.get("/api/v1/admin/roles").json()}
    assert set(roles) == {"learner", "trainer", "department_admin", "org_admin", "competency_admin", "training_manager",
                          "auditor", "platform_admin"}
    assert roles["org_admin"]["user_count"] >= 1
    assert roles["learner"]["capabilities"] == []
    assert roles["auditor"]["capabilities"] == ["audit.view", "frameworks.view"]


def test_environment_flags_are_public_and_minimal(client):
    body = client.get("/api/v1/environment").json()
    assert body == {"synthetic_data": True, "self_registration_enabled": True}


def test_signed_in_users_list_active_departments_of_their_organisation(client, factory, org):
    problem(client.get("/api/v1/departments"), 401, "UNAUTHENTICATED")
    _, email = make_user(factory, org)
    login(client, email)
    names = {d["name"] for d in client.get("/api/v1/departments").json()}
    assert {"North Division", "South Division"} <= names and "Elsewhere" not in names
