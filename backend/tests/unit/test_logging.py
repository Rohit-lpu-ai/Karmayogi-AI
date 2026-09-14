import json
import logging
import sys

from app.core.logging import REDACTED, JsonFormatter, correlation_id_var, redact


def _format(message, exc_info=None, **extra):
    record = logging.LogRecord("t", logging.INFO, __file__, 1, message, None, exc_info)
    for key, value in extra.items():
        setattr(record, key, value)
    return json.loads(JsonFormatter().format(record))


def test_sensitive_keys_redacted():
    out = _format("login", password="hunter2hunter2", session_token="abc", authorization="Bearer x", user_count=3)
    assert out["password"] == REDACTED
    assert out["session_token"] == REDACTED
    assert out["authorization"] == REDACTED
    assert out["user_count"] == 3


def test_personal_data_patterns_redacted_in_message():
    out = _format("contact learner01@example.invalid or 9876543210, id 1234 5678 9012")
    assert "example.invalid" not in out["message"]
    assert "9876543210" not in out["message"]
    assert "1234 5678 9012" not in out["message"]


def test_url_credentials_redacted():
    assert "pw123" not in redact("postgresql+psycopg://user:pw123@host:5433/db")


def test_nested_structures_redacted():
    out = redact({"meta": {"api_key": "k", "items": ["a@b.co"]}})
    assert out["meta"]["api_key"] == REDACTED
    assert out["meta"]["items"] == ["[EMAIL]"]


def test_correlation_id_included():
    token = correlation_id_var.set("corr-12345678")
    try:
        assert _format("x")["correlation_id"] == "corr-12345678"
    finally:
        correlation_id_var.reset(token)


def test_exception_text_redacted():
    try:
        raise ValueError("bad value for someone@example.invalid")
    except ValueError:
        out = _format("boom", exc_info=sys.exc_info())
    assert "someone@example.invalid" not in out["exception"]
