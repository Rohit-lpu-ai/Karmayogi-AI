"""Health, problem responses, correlation IDs, security headers and OpenAPI exposure."""

from fastapi import APIRouter
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.config import AppEnv
from app.core.errors import PROBLEM_CONTENT_TYPE, ProblemError
from app.core.middleware import SECURITY_HEADERS
from app.main import create_app
from tests.conftest import make_settings


def _client_with_test_routes(engine) -> TestClient:
    app = create_app(make_settings(), engine_factory=lambda: engine)
    router = APIRouter()

    class Body(BaseModel):
        name: str = Field(min_length=3)

    @router.post("/_test/validate")
    def validate(body: Body):
        return {"ok": True}

    @router.get("/_test/problem")
    def problem():
        raise ProblemError(409, "CONFLICT", "Conflict", "Already exists.")

    @router.get("/_test/boom")
    def boom():
        raise RuntimeError("internal detail with secret sk-live-123")

    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


def _assert_problem(response, status, code):
    assert response.status_code == status
    assert response.headers["content-type"].startswith(PROBLEM_CONTENT_TYPE)
    body = response.json()
    assert body["status"] == status
    assert body["code"] == code
    assert body["correlation_id"] == response.headers["x-correlation-id"]
    return body


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz_unavailable_without_database(client):
    body = _assert_problem(client.get("/readyz"), 503, "SERVICE_UNAVAILABLE")
    assert "127.0.0.1" not in str(body)
    assert "psycopg" not in str(body)


def test_unknown_route_is_problem_json(client):
    _assert_problem(client.get("/api/v1/does-not-exist"), 404, "NOT_FOUND")


def test_method_not_allowed_is_problem_json(client):
    _assert_problem(client.post("/healthz"), 405, "METHOD_NOT_ALLOWED")


def test_validation_error_lists_fields_without_echoing_input(unreachable_engine):
    response = _client_with_test_routes(unreachable_engine).post("/_test/validate", json={"name": "pw"})
    body = _assert_problem(response, 422, "VALIDATION_FAILED")
    assert body["errors"][0]["field"] == "name"
    assert "input" not in body["errors"][0]
    assert '"pw"' not in response.text


def test_problem_error_raised_by_route(unreachable_engine):
    body = _assert_problem(_client_with_test_routes(unreachable_engine).get("/_test/problem"), 409, "CONFLICT")
    assert body["detail"] == "Already exists."


def test_unhandled_exception_hides_details(unreachable_engine):
    response = _client_with_test_routes(unreachable_engine).get("/_test/boom")
    body = _assert_problem(response, 500, "INTERNAL_ERROR")
    assert "sk-live-123" not in response.text
    assert "RuntimeError" not in response.text
    for header in SECURITY_HEADERS:
        assert header in response.headers
    assert body["instance"] == "/_test/boom"


def test_valid_correlation_id_is_propagated(client):
    response = client.get("/healthz", headers={"X-Correlation-ID": "abc-12345678"})
    assert response.headers["x-correlation-id"] == "abc-12345678"


def test_invalid_correlation_id_is_replaced(client):
    response = client.get("/healthz", headers={"X-Correlation-ID": "bad id<script>"})
    assert response.headers["x-correlation-id"] != "bad id<script>"
    assert len(response.headers["x-correlation-id"]) == 32


def test_security_headers_present(client):
    response = client.get("/healthz")
    for header, value in SECURITY_HEADERS.items():
        assert response.headers[header] == value


def test_openapi_served_in_ci(client):
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    operation_ids = {op["operationId"] for path in response.json()["paths"].values() for op in path.values()}
    assert {"platform_get_healthz", "platform_get_readyz"} <= operation_ids


def test_openapi_hidden_outside_local(unreachable_engine):
    app = create_app(make_settings(app_env=AppEnv.pilot), engine_factory=lambda: unreachable_engine)
    with TestClient(app) as client:
        assert client.get("/api/v1/openapi.json").status_code == 404
        assert client.get("/docs").status_code == 404


def test_app_import_registers_every_model_table():
    """The running app (not only the test suite) must know every table, or flushes fail on cross-module foreign keys."""
    import subprocess
    import sys

    code = "import app.main; from app.core.db import Base; print(sorted(Base.metadata.tables))"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    for table in ("topics", "question_versions", "lessons", "review_tasks", "source_records"):
        assert f"'{table}'" in out
