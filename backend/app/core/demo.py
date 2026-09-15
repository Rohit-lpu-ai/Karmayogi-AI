"""Labelling of synthetic demo content (DEC-045).

Demo content exists only in local and ci databases and is recognised by a
``DEMO-`` code prefix. Every API object built from it carries ``is_demo: true``
so the UI can label it; nothing here is official data.
"""

from __future__ import annotations

DEMO_CODE_PREFIX = "DEMO-"
DEMO_NOTICE = "DEMO - synthetic content for local testing. Not official data, not a real assessment."


def is_demo_code(code: str | None) -> bool:
    return bool(code) and code.startswith(DEMO_CODE_PREFIX)
