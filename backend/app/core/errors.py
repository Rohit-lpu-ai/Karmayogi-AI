"""RFC 9457 problem responses (API_INTEGRATION_SPEC.md §1.4).

Error bodies never contain stack traces, SQL, provider errors or secrets.
Until ERROR_HANDLING_SPEC.md exists (DEC-039), the codes defined here are the
catalogue.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import StaleDataError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import correlation_id_var

PROBLEM_CONTENT_TYPE = "application/problem+json"

_HTTP_CODES = {
    400: ("BAD_REQUEST", "Bad request"),
    401: ("UNAUTHENTICATED", "Authentication required"),
    403: ("FORBIDDEN", "Forbidden"),
    404: ("NOT_FOUND", "Not found"),
    405: ("METHOD_NOT_ALLOWED", "Method not allowed"),
    409: ("CONFLICT", "Conflict"),
    423: ("ACCOUNT_LOCKED", "Account temporarily locked"),
    413: ("PAYLOAD_TOO_LARGE", "Payload too large"),
    415: ("UNSUPPORTED_MEDIA_TYPE", "Unsupported media type"),
    429: ("RATE_LIMITED", "Too many requests"),
    503: ("SERVICE_UNAVAILABLE", "Service unavailable"),
}


class ProblemError(Exception):
    """Raise from services or routes to return a problem response."""

    def __init__(
        self,
        status: int,
        code: str,
        title: str,
        detail: str | None = None,
        errors: list[dict[str, str]] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(detail or title)
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail
        self.errors = errors
        self.headers = headers


def problem_response(
    request: Request,
    status: int,
    code: str,
    title: str,
    detail: str | None = None,
    errors: list[dict[str, str]] | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    body: dict[str, Any] = {
        "type": f"urn:platform:problem:{code.lower().replace('_', '-')}",
        "title": title,
        "status": status,
        "code": code,
        "instance": request.url.path,
        "correlation_id": correlation_id_var.get(),
    }
    if detail:
        body["detail"] = detail
    if errors:
        body["errors"] = errors
    return JSONResponse(body, status_code=status, media_type=PROBLEM_CONTENT_TYPE, headers=headers)


def _field_errors(exc: RequestValidationError) -> list[dict[str, str]]:
    out = []
    for err in exc.errors():
        location = [str(p) for p in err.get("loc", ()) if p not in ("body", "query", "path", "header")]
        # The input value is deliberately omitted: it may contain personal data or secrets.
        out.append({
            "field": ".".join(location) or "request",
            "code": str(err.get("type", "invalid")).upper(),
            "message": str(err.get("msg", "Invalid value")),
        })
    return out


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProblemError)
    async def _problem(request: Request, exc: ProblemError) -> JSONResponse:
        return problem_response(request, exc.status, exc.code, exc.title, exc.detail, exc.errors, exc.headers)

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        return problem_response(
            request, 422, "VALIDATION_FAILED", "Validation failed",
            "One or more fields are invalid.", _field_errors(exc),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code, title = _HTTP_CODES.get(exc.status_code, ("HTTP_ERROR", "Request failed"))
        return problem_response(request, exc.status_code, code, title, headers=getattr(exc, "headers", None))

    @app.exception_handler(StaleDataError)
    async def _stale(request: Request, exc: StaleDataError) -> JSONResponse:
        return problem_response(request, 409, "CONFLICT", "Conflict", "This record was changed by someone else. Reload and try again.")

    # Unexpected exceptions are converted in RequestContextMiddleware, which runs inside the
    # correlation-ID context; Starlette's own catch-all handler runs outside it.


def internal_error_body(path: str) -> dict[str, Any]:
    return {
        "type": "urn:platform:problem:internal-error",
        "title": "Internal server error",
        "status": 500,
        "code": "INTERNAL_ERROR",
        "detail": "Something went wrong. Quote the correlation ID if you contact support.",
        "instance": path,
        "correlation_id": correlation_id_var.get(),
    }
