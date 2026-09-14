"""Password hashing, session/CSRF tokens, delivery order reproducibility and new settings validation."""

import pytest
from pydantic import ValidationError

from app.core.config import AppEnv
from app.core.demo import is_demo_code
from app.modules.assessment.service import delivery_plan
from app.modules.identity.security import (
    csrf_matches,
    csrf_token_for,
    hash_password,
    new_session_token,
    session_id_for,
    verify_password,
)
from tests.conftest import make_settings


def test_password_hash_is_argon2id_and_verifies():
    hashed = hash_password("correct horse battery")
    assert hashed.startswith("$argon2id$")
    assert "correct horse battery" not in hashed
    assert verify_password(hashed, "correct horse battery")
    assert not verify_password(hashed, "wrong password!!")


def test_short_password_rejected():
    with pytest.raises(ValueError):
        hash_password("short")


def test_missing_or_corrupt_hash_never_verifies():
    assert not verify_password(None, "anything at all")
    assert not verify_password("not-a-hash", "anything at all")


def test_session_token_stored_only_as_hash():
    token = new_session_token()
    assert len(token) >= 43
    session_id = session_id_for(token)
    assert len(session_id) == 64 and token not in session_id


def test_csrf_token_bound_to_session_and_secret():
    token_a, token_b = new_session_token(), new_session_token()
    csrf = csrf_token_for("s" * 40, token_a)
    assert csrf_matches("s" * 40, token_a, csrf)
    assert not csrf_matches("s" * 40, token_b, csrf)
    assert not csrf_matches("t" * 40, token_a, csrf)
    assert not csrf_matches("s" * 40, token_a, None)


def test_delivery_plan_reproducible_from_seed():
    ids = [f"v{i}" for i in range(10)]
    first = delivery_plan(123456789, ids)
    assert delivery_plan(123456789, list(reversed(ids))) == first
    assert sorted(p.question_version_id for p in first) == sorted(ids)
    assert [p.position for p in first] == list(range(1, 11))
    assert all(sorted(p.option_order) == ["A", "B", "C", "D"] for p in first)
    assert delivery_plan(987654321, ids) != first


def test_demo_code_detection():
    assert is_demo_code("DEMO-C1")
    assert not is_demo_code("1.1")
    assert not is_demo_code(None)


def test_short_session_secret_rejected():
    with pytest.raises(ValidationError):
        make_settings(session_secret="too-short")


@pytest.mark.parametrize("env", [AppEnv.staging, AppEnv.pilot, AppEnv.production])
def test_insecure_cookie_refused_outside_development(env):
    with pytest.raises(ValidationError):
        make_settings(app_env=env, session_cookie_secure=False)
