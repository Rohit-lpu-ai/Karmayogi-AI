"""Shared vocabulary for the feature registry used to generate docs/FEATURE_CATALOG.md.

Documentation tooling only (see docs/DECISIONS.md, DEC-018). No application code.
"""

# Implementation-status vocabulary (docs/DOCUMENTATION_INDEX.md, "Status vocabularies").
IMPL = "Implemented"
PART = "Partially implemented"
MOCK = "Mocked"
PLAN = "Planned"
UNK = "Unknown"
BLOCK = "Blocked by external access"
HUMAN = "Requires human confirmation"
STATUSES = [IMPL, PART, MOCK, PLAN, UNK, BLOCK, HUMAN]

PRIORITIES = ["P0", "P1", "P2"]

CATEGORIES = {}
FEATURES = []


def category(letter, prefix, title, area, primary, secondary, deps, human_review, security, accessibility):
    CATEGORIES[prefix] = {
        "letter": letter, "prefix": prefix, "title": title, "area": area,
        "primary": primary, "secondary": secondary, "deps": deps,
        "human_review": human_review, "security": security, "accessibility": accessibility,
    }


def F(fid, name, priority, description, value, data, ai, api, ui, failure, acceptance, future,
      status=PLAN, status_note="No application code exists yet.", **overrides):
    prefix = fid.split("-")[0]
    cat = CATEGORIES[prefix]
    assert priority in PRIORITIES, fid
    assert status in STATUSES, fid
    mvp = {
        "P0": "In MVP",
        "P1": "Excluded from MVP (P1 - post-MVP)",
        "P2": "Excluded from MVP (P2 - future)",
    }[priority]
    feature = {
        "id": fid,
        "name": name,
        "category": cat["letter"],
        "description": description,
        "primary_user": overrides.pop("primary", cat["primary"]),
        "secondary_users": overrides.pop("secondary", cat["secondary"]),
        "business_value": value,
        "priority": priority,
        "product_area": cat["area"],
        "dependencies": overrides.pop("deps", cat["deps"]),
        "data_required": data,
        "ai_involvement": ai,
        "human_review_required": overrides.pop("human_review", cat["human_review"]),
        "mvp_status": overrides.pop("mvp", mvp),
        "implementation_status": f"{status} - {status_note}",
        "implementation_status_code": status,
        "api_requirements": api,
        "ui_requirements": ui,
        "security_considerations": overrides.pop("security", cat["security"]),
        "accessibility_considerations": overrides.pop("accessibility", cat["accessibility"]),
        "failure_cases": failure,
        "acceptance_criteria": acceptance,
        "future_extensions": future,
        "alias_of": overrides.pop("alias_of", None),
    }
    assert not overrides, (fid, overrides)
    FEATURES.append(feature)
    return feature
