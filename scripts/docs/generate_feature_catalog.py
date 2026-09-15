"""Generate docs/FEATURE_CATALOG.md and docs/feature_registry.json from the feature registry.

Documentation tooling only (docs/DECISIONS.md DEC-018). Validates that feature IDs are
unique, sequential within each category, that every referenced feature ID exists, and
that alias targets exist.

Usage:
    python scripts/docs/generate_feature_catalog.py
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import registry_common as rc  # noqa: E402
import registry_a_c  # noqa: E402,F401
import registry_d_h  # noqa: E402,F401
import registry_i_n  # noqa: E402,F401
import registry_o_t  # noqa: E402,F401

ID_RE = re.compile(r"\b(?:AI|MAT|ASM|CMP|ROLE|PER|TUT|IGOT|ADM|ANA|TRN|ACC|GAM|PRO|REP|SEC|RAI|AUT|UX|FUT)-\d{3}\b")

FIELDS = [
    ("description", "Description"),
    ("primary_user", "Primary user"),
    ("secondary_users", "Secondary users"),
    ("business_value", "Business value"),
    ("priority", "Priority"),
    ("product_area", "Product area"),
    ("dependencies", "Dependencies"),
    ("data_required", "Data required"),
    ("ai_involvement", "AI involvement"),
    ("human_review_required", "Human review required"),
    ("mvp_status", "MVP status"),
    ("implementation_status", "Implementation status"),
    ("api_requirements", "API requirements"),
    ("ui_requirements", "UI requirements"),
    ("security_considerations", "Security considerations"),
    ("accessibility_considerations", "Accessibility considerations"),
    ("failure_cases", "Failure cases"),
    ("acceptance_criteria", "Acceptance criteria"),
    ("future_extensions", "Future extensions"),
]


def validate(features):
    errors = []
    ids = [f["id"] for f in features]
    for fid, n in Counter(ids).items():
        if n > 1:
            errors.append(f"duplicate id {fid}")
    known = set(ids)
    by_prefix = {}
    for f in features:
        prefix, num = f["id"].rsplit("-", 1)
        by_prefix.setdefault(prefix, []).append(int(num))
    for prefix, nums in by_prefix.items():
        if nums != list(range(1, len(nums) + 1)):
            errors.append(f"{prefix} ids not sequential: {nums}")
    for f in features:
        text = " ".join(str(v) for k, v in f.items() if isinstance(v, str))
        for ref in set(ID_RE.findall(text)):
            if ref not in known:
                errors.append(f"{f['id']} references unknown feature {ref}")
        if f["alias_of"] and f["alias_of"] not in known:
            errors.append(f"{f['id']} alias_of unknown {f['alias_of']}")
    return errors


def anchor(fid, name):
    return (fid + " " + name).lower().replace(" ", "-").translate(str.maketrans("", "", "/(),.'&:"))


def render(features):
    cats = rc.CATEGORIES
    pri = Counter(f["priority"] for f in features)
    status = Counter(f["implementation_status_code"] for f in features)
    lines = [
        "# Feature Catalog",
        "",
        "| | |",
        "|---|---|",
        "| **Product** | Competency intelligence and personalized learning platform for India's official statistical system (working name: Decision required, [DECISIONS.md](DECISIONS.md) DEC-001) |",
        "| **Document version** | 1.0.0-draft |",
        "| **Status** | Draft for approval - no implementation authorised |",
        "| **Owner** | Product owner: Decision required |",
        "| **Last updated** | 2026-09-14 |",
        "| **Generated from** | `scripts/docs/registry_*.py` via `scripts/docs/generate_feature_catalog.py` (do not hand-edit; edit the registry and regenerate) |",
        "| **Machine-readable copy** | [feature_registry.json](feature_registry.json) |",
        "| **Related** | [PRD.md](PRD.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) · [UI_UX_SPEC.md](UI_UX_SPEC.md) |",
        "",
        "## How to read this catalog",
        "",
        "- **Priority:** P0 = MVP (first usable product); P1 = post-MVP; P2 = future. P1 and P2 features must not be implemented during MVP ([MVP_SCOPE.md](MVP_SCOPE.md) §Forbidden).",
        "- **Implementation status** uses the implementation vocabulary in [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md): Implemented, Partially implemented, Mocked, Planned, Unknown, Blocked by external access, Requires human confirmation. Every status cites repository evidence.",
        "- **API requirements** name *planned internal* endpoints of this platform. They are not implemented and are **not** external or iGOT endpoints.",
        "- **Alias entries** (\"Alias of\") keep the inventory complete where the brief lists the same capability in more than one category; the canonical entry holds the full specification.",
        "- One feature (`UX-021 User profile and account settings`) was added because the P0 list requires a user profile but the inventory had no matching item ([DOCUMENTATION_VALIDATION_REPORT.md](DOCUMENTATION_VALIDATION_REPORT.md)).",
        "",
        "## Summary",
        "",
        f"**{len(features)} features** - P0: {pri['P0']} · P1: {pri['P1']} · P2: {pri['P2']}",
        "",
        "| Implementation status | Features |",
        "|---|---|",
    ]
    for s in rc.STATUSES:
        lines.append(f"| {s} | {status.get(s, 0)} |")
    lines += ["", "| Category | Prefix | Features | P0 | P1 | P2 |", "|---|---|---|---|---|---|"]
    for prefix, c in cats.items():
        fs = [f for f in features if f["id"].startswith(prefix + "-")]
        cp = Counter(f["priority"] for f in fs)
        lines.append(f"| [{c['letter']}. {c['title']}](#{c['letter'].lower()}-{c['title'].lower().replace(' ', '-').replace('/', '')}) | {prefix} | {len(fs)} | {cp['P0']} | {cp['P1']} | {cp['P2']} |")

    lines += ["", "## P0 feature index", "", "| ID | Feature | Implementation status | Alias of |", "|---|---|---|---|"]
    for f in features:
        if f["priority"] == "P0":
            lines.append(f"| {f['id']} | {f['name']} | {f['implementation_status_code']} | {f['alias_of'] or ''} |")

    lines += ["", "## Table of contents", ""]
    for prefix, c in cats.items():
        lines.append(f"- [{c['letter']}. {c['title']}](#{c['letter'].lower()}-{c['title'].lower().replace(' ', '-').replace('/', '')})")

    for prefix, c in cats.items():
        lines += ["", "---", "", f"# {c['letter']}. {c['title']}", ""]
        for f in (x for x in features if x["id"].startswith(prefix + "-")):
            lines += ["", f"## [{f['id']}] {f['name']}", ""]
            if f["alias_of"]:
                lines.append(f"> Alias of **{f['alias_of']}** - see that entry for the full specification.")
                lines.append("")
            for key, label in FIELDS:
                lines.append(f"- {label}: {f[key]}")
    return "\n".join(lines) + "\n"


def main():
    features = rc.FEATURES
    errors = validate(features)
    if errors:
        print("REGISTRY ERRORS:")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    (ROOT / "docs" / "FEATURE_CATALOG.md").write_text(render(features), encoding="utf-8")
    registry = {
        "generated_from": "scripts/docs/generate_feature_catalog.py",
        "implementation_statuses": rc.STATUSES,
        "categories": list(rc.CATEGORIES.values()),
        "features": features,
    }
    (ROOT / "docs" / "feature_registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pri = Counter(f["priority"] for f in features)
    print(f"features={len(features)} P0={pri['P0']} P1={pri['P1']} P2={pri['P2']}")
    print("status:", dict(Counter(f["implementation_status_code"] for f in features)))


if __name__ == "__main__":
    main()
