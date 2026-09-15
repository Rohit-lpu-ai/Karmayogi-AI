"""score-v1 and the gap rule are deterministic, reproducible and match AI_SYSTEM_SPEC.md §25."""

import itertools
import random
from decimal import Decimal

import pytest

from app.modules.competency.scoring import (
    METHOD_VERSION,
    EvidenceItem,
    LevelThreshold,
    classify_gap,
    compute_estimate,
    evidence_band,
    explanation,
    level_for,
    weight_for,
)

LEVELS = (
    LevelThreshold(1, "Level 1", Decimal("0"), "provisional"),
    LevelThreshold(2, "Level 2", Decimal("0.4"), "provisional"),
    LevelThreshold(3, "Level 3", Decimal("0.6"), "provisional"),
    LevelThreshold(4, "Level 4", Decimal("0.8"), "provisional"),
)


def items(*spec):
    return [EvidenceItem(f"q{i:02d}", difficulty, correct) for i, (difficulty, correct) in enumerate(spec)]


def test_weights():
    assert weight_for("foundational") == Decimal("1.0")
    assert weight_for("intermediate") == Decimal("1.5")
    assert weight_for("advanced") == Decimal("2.0")
    with pytest.raises(ValueError):
        weight_for("expert")


@pytest.mark.parametrize("count,band", [(0, "insufficient"), (2, "insufficient"), (3, "low"), (4, "low"),
                                        (5, "medium"), (9, "medium"), (10, "high"), (40, "high")])
def test_evidence_bands(count, band):
    assert evidence_band(count) == band


def test_negative_count_rejected():
    with pytest.raises(ValueError):
        evidence_band(-1)


def test_difficulty_weighted_score_and_level():
    # correct: foundational(1.0) + foundational(1.0) of total 1+1+1.5+1.5+2 = 7 -> 2/7
    estimate = compute_estimate(items(("foundational", True), ("foundational", True), ("intermediate", False),
                                      ("intermediate", False), ("advanced", False)), LEVELS)
    assert estimate.score == Decimal("0.28571")
    assert estimate.level_number == 1
    assert estimate.evidence_band == "medium"
    assert estimate.evidence_count == 5
    assert estimate.thresholds_status == "provisional"
    assert estimate.method_version == METHOD_VERSION


def test_all_correct_and_all_wrong():
    all_right = compute_estimate(items(*[("advanced", True)] * 5), LEVELS)
    all_wrong = compute_estimate(items(*[("advanced", False)] * 5), LEVELS)
    assert (all_right.score, all_right.level_number) == (Decimal("1.00000"), 4)
    assert (all_wrong.score, all_wrong.level_number) == (Decimal("0.00000"), 1)


def test_threshold_boundaries_are_inclusive():
    assert level_for(Decimal("0.6"), LEVELS) == 3
    assert level_for(Decimal("0.59999"), LEVELS) == 2


def test_no_evidence_gives_no_score():
    estimate = compute_estimate([], LEVELS)
    assert estimate.score is None and estimate.level_number is None and estimate.evidence_band == "insufficient"


def test_unconfigured_thresholds_give_score_without_level():
    unconfigured = (LevelThreshold(1, "Level 1", None, "provisional"), LevelThreshold(2, "Level 2", None, "provisional"))
    estimate = compute_estimate(items(("foundational", True)), unconfigured)
    assert estimate.score == Decimal("1.00000")
    assert estimate.level_number is None
    assert estimate.thresholds_status == "not_configured"


def test_deterministic_and_order_independent():
    rng = random.Random(20260915)
    spec = [(rng.choice(["foundational", "intermediate", "advanced"]), rng.random() < 0.5) for _ in range(12)]
    base = items(*spec)
    first = compute_estimate(base, LEVELS)
    for _ in range(20):
        shuffled = base[:]
        rng.shuffle(shuffled)
        assert compute_estimate(shuffled, LEVELS) == first


def test_exhaustive_small_cases_match_formula():
    difficulties = ["foundational", "intermediate", "advanced"]
    for combo in itertools.product(difficulties, [True, False], repeat=2):
        spec = [(combo[0], combo[1]), (combo[2], combo[3])]
        total = sum(weight_for(d) for d, _ in spec)
        earned = sum(weight_for(d) for d, c in spec if c)
        assert compute_estimate(items(*spec), LEVELS).score == (earned / total).quantize(Decimal("0.00001"))


def test_explanation_block_lists_evidence_and_limitations():
    estimate = compute_estimate(items(("foundational", True), ("advanced", False)), LEVELS)
    block = explanation(estimate, "attempt-1")
    assert block["method_version"] == "score-v1"
    assert block["attempt_id"] == "attempt-1"
    assert len(block["items"]) == 2
    assert any("provisional" in line for line in block["limitations"])
    assert any("reassess to confirm" in line for line in block["limitations"])
    assert any("not an appraisal" in line for line in block["limitations"])


@pytest.mark.parametrize("required,level,band,status,gap", [
    (3, 1, "medium", "gap", 2),
    (3, 3, "high", "meets_requirement", 0),
    (3, 4, "medium", "meets_requirement", 0),
    (3, 1, "low", "insufficient_evidence", None),
    (3, 1, "insufficient", "insufficient_evidence", None),
    (3, None, "medium", "level_unavailable", None),
    (3, None, None, "not_assessed", None),
])
def test_gap_rule(required, level, band, status, gap):
    result = classify_gap(required, level, band)
    assert (result.status, result.gap) == (status, gap)
