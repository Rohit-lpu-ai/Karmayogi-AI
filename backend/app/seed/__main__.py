"""Seed command.

Usage (from ``backend/``, after ``alembic upgrade head``):

    python -m app.seed --org-code local-demo --org-name "Local development organisation" [--demo-users [--demo-content]]

Runs the canonical dataset validator first and refuses an INVALID verdict.
Idempotent: running it again creates nothing. All writes share one transaction.

``--demo-content`` applies every registered, versioned DEMO pack that is missing or outdated
(``app/seed/demo_packs.py``, DEC-052). Reset synthetic accounts with ``python -m app.seed.demo_reset``.
"""

from __future__ import annotations

import argparse
import json
import sys

from app.core.config import get_settings
from app.core.db import get_sessionmaker
from app.core.logging import configure_logging
from app.seed.canonical import SeedRefused, load_canonical_bundle
from app.seed.demo_packs import apply_demo_packs
from app.seed.demo_users import seed_demo_users
from app.seed.importer import get_or_create_organization, import_canonical_datasets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import canonical seed datasets")
    parser.add_argument("--org-code", required=True, help="Organisation slug, e.g. local-demo")
    parser.add_argument("--org-name", required=True)
    parser.add_argument("--demo-users", action="store_true", help="Create synthetic demo accounts (local/ci/staging only)")
    parser.add_argument("--demo-content", action="store_true",
                        help="Apply the versioned DEMO content packs (local/ci only; needs --demo-users)")
    args = parser.parse_args(argv)

    settings = get_settings()
    configure_logging(settings.log_level)
    session = get_sessionmaker()()
    try:
        bundle = load_canonical_bundle()
        org, org_created = get_or_create_organization(session, args.org_code, args.org_name)
        report = import_canonical_datasets(session, org, bundle)
        summary = {"organization_created": org_created, "validator_verdict": bundle.verdict, **report.as_dict()}
        if args.demo_content and not args.demo_users:
            raise SeedRefused("--demo-content requires --demo-users")
        if args.demo_users:
            password = settings.demo_user_password.get_secret_value() if settings.demo_user_password else None
            summary["demo_users_created"] = dict(seed_demo_users(session, org, settings.app_env, password))
        if args.demo_content:
            summary["demo_packs"] = apply_demo_packs(session, org, settings.app_env)
        session.commit()
    except SeedRefused as exc:
        session.rollback()
        print(json.dumps({"refused": str(exc)}), file=sys.stderr)
        return 2
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
