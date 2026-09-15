"""Create a fresh synthetic learner for browser journeys (local/ci only).

Usage (from ``backend/``):

    .venv/Scripts/python scripts/e2e_learner.py --org-code local-demo

Prints ``{"email": "..."}``. The account is ``is_synthetic``, has the ``learner`` role, uses ``DEMO_USER_PASSWORD``
and has no notice acknowledgement or job role, so a journey can walk the whole onboarding. Notice
acknowledgements are append-only, which is why a new account is created per run instead of reusing one.
Accounts are named ``e2e-<timestamp>-<random>@example.invalid`` and are kept (audit history references them).
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # run as a script from backend/

from sqlalchemy import select  # noqa: E402

from app.core.config import AppEnv, get_settings  # noqa: E402
from app.core.db import get_sessionmaker  # noqa: E402
from app.modules.identity.models import User, UserAccessRole  # noqa: E402
from app.modules.identity.security import hash_password  # noqa: E402
from app.modules.organization.models import Organization  # noqa: E402

ALLOWED = {AppEnv.local, AppEnv.ci}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--org-code", default="local-demo")
    args = parser.parse_args(argv)
    settings = get_settings()
    if settings.app_env not in ALLOWED:
        print(json.dumps({"refused": f"not allowed in {settings.app_env.value}"}), file=sys.stderr)
        return 2
    if settings.demo_user_password is None:
        print(json.dumps({"refused": "DEMO_USER_PASSWORD is not set"}), file=sys.stderr)
        return 2
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    email = f"e2e-{stamp}-{secrets.token_hex(3)}@example.invalid"
    with get_sessionmaker()() as db:
        org = db.scalar(select(Organization).where(Organization.code == args.org_code))
        if org is None:
            print(json.dumps({"refused": f"unknown organisation {args.org_code}"}), file=sys.stderr)
            return 2
        user = User(organization_id=org.id, email=email, display_name="E2E Learner (synthetic)", status="active",
                    registration_id=f"E2E-{stamp}-{secrets.token_hex(3)}",
                    password_hash=hash_password(settings.demo_user_password.get_secret_value()), is_synthetic=True)
        db.add(user)
        db.flush()
        db.add(UserAccessRole(organization_id=org.id, user_id=user.id, role="learner"))
        db.commit()
    print(json.dumps({"email": email}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
