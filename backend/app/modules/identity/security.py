"""Credential and token primitives (SECURITY_RESPONSIBLE_AI.md §3).

- Passwords: Argon2id (argon2-cffi defaults, RFC 9106 low-memory profile).
- Session tokens: 256-bit random; only their SHA-256 is stored.
- CSRF tokens: HMAC-SHA256(SESSION_SECRET, raw session token) - bound to the session, never stored (DEC-047).
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

_hasher = PasswordHasher()
# Verified against when the account does not exist, so response time does not reveal whether it exists.
_DUMMY_HASH = _hasher.hash(secrets.token_urlsafe(32))

MIN_PASSWORD_LENGTH = 12


def hash_password(password: str) -> str:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def session_id_for(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def csrf_token_for(secret: str, session_token: str) -> str:
    return hmac.new(secret.encode("utf-8"), session_token.encode("utf-8"), hashlib.sha256).hexdigest()


def csrf_matches(secret: str, session_token: str, presented: str | None) -> bool:
    if not presented:
        return False
    return hmac.compare_digest(csrf_token_for(secret, session_token), presented)
