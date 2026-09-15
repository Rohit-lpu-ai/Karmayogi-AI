"""Request middleware: correlation IDs, security headers, request logging.

Implemented as plain ASGI so the correlation-ID context variable is visible
to route handlers, exception handlers and log records of the same request.
"""

from __future__ import annotations

import json
import logging
import re
import time
import uuid

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.errors import PROBLEM_CONTENT_TYPE, internal_error_body
from app.core.logging import correlation_id_var

CORRELATION_HEADER = "x-correlation-id"
_VALID_CORRELATION_ID = re.compile(r"^[A-Za-z0-9-]{8,64}$")

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Cache-Control": "no-store",
}

logger = logging.getLogger("app.request")


def resolve_correlation_id(incoming: str | None) -> str:
    if incoming and _VALID_CORRELATION_ID.match(incoming):
        return incoming
    return uuid.uuid4().hex


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        incoming = None
        for name, value in scope.get("headers", []):
            if name == CORRELATION_HEADER.encode():
                incoming = value.decode("latin-1")
                break
        correlation_id = resolve_correlation_id(incoming)
        token = correlation_id_var.set(correlation_id)
        started = time.perf_counter()
        status_holder = {"status": 500}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
                headers = MutableHeaders(scope=message)
                headers[CORRELATION_HEADER] = correlation_id
                for key, value in SECURITY_HEADERS.items():
                    headers.setdefault(key, value)
            await send(message)

        response_started = False

        async def tracking_send(message: Message) -> None:
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send_wrapper(message)

        try:
            await self.app(scope, receive, tracking_send)
        except Exception as exc:  # noqa: BLE001 - last-resort conversion to a problem response
            logger.error("unhandled_exception", exc_info=exc, extra={"route": getattr(scope.get("route"), "path", None)})
            if response_started:
                raise
            body = json.dumps(internal_error_body(scope.get("path", ""))).encode()
            await tracking_send({
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    (b"content-type", PROBLEM_CONTENT_TYPE.encode()),
                    (b"content-length", str(len(body)).encode()),
                ],
            })
            await send({"type": "http.response.body", "body": body})
        finally:
            route = scope.get("route")
            # Log the route template, never the raw path or query string (may carry identifiers).
            path = getattr(route, "path", None) or "unmatched"
            logger.info(
                "request",
                extra={
                    "method": scope.get("method"),
                    "route": path,
                    "status": status_holder["status"],
                    "duration_ms": round((time.perf_counter() - started) * 1000, 1),
                },
            )
            correlation_id_var.reset(token)
