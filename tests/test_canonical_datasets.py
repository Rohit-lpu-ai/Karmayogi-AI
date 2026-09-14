"""The canonical datasets are valid, and the validator rejects each class of defect.

Each negative test corrupts one thing in an in-memory copy of the real
datasets and asserts that the matching requirement fails with ERROR.
"""

import copy
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "validators"))

import validate_canonical_datasets as v  # noqa: E402

BASELINE = v.load_datasets()


def errors(report, req):
    return [i for r in report["requirements"] if r["id"] == req
            for i in r["findings"] if i["severity"] == "ERROR"]


class CurrentDatasetsTest(unittest.TestCase):
    def test_no_errors(self):
        report = v.validate_datasets(copy.deepcopy(BASELINE))
        failing = {r["id"]: r["findings"][:3] for r in report["requirements"] if r["outcome"] == "FAIL"}
        self.assertEqual(failing, {})
        self.assertEqual(report["totals"]["errors"], 0)

    def test_not_releasable_until_human_review(self):
        report = v.validate_datasets(copy.deepcopy(BASELINE))
        self.assertEqual(report["verdict"], "VALID_FOR_DEVELOPMENT_NOT_RELEASABLE")


class ValidatorRejectsDefectsTest(unittest.TestCase):
    def setUp(self):
        self.d = copy.deepcopy(BASELINE)
        self.prog = self.d["training_programmes"]["records"][0]
        self.comp = self.d["competency_framework"]["records"][0]
        self.doc = self.d["documents"]["records"][0]

    def assertFails(self, req):
        report = v.validate_datasets(self.d)
        self.assertTrue(errors(report, req), f"{req} did not report an ERROR in its findings")
        self.assertEqual(next(r["outcome"] for r in report["requirements"] if r["id"] == req), "FAIL")
        self.assertEqual(report["verdict"], "INVALID")

    def test_record_count_mismatch(self):
        self.d["documents"]["record_count"] += 1
        self.assertFails("LP-01")

    def test_schema_violation(self):
        self.prog["delivery"]["duration_days_per_occurrence"] = "five"
        self.assertFails("LP-02")

    def test_duplicate_id(self):
        self.d["tpac_references"]["records"].append(copy.deepcopy(self.d["tpac_references"]["records"][0]))
        self.d["tpac_references"]["record_count"] += 1
        self.assertFails("LP-03")

    def test_non_reproducible_programme_id(self):
        self.prog["topic_as_printed"] += " (edited)"
        self.assertFails("LP-03")

    def test_unknown_topic_reference(self):
        self.doc["topics"].append({"topic_id": "not_a_topic", "status": "ASSUMED", "method": "test"})
        self.assertFails("LP-04")

    def test_unknown_source_id(self):
        self.prog["provenance"]["source_id"] = "SRC-999"
        self.assertFails("LP-04")

    def test_collected_record_without_checksum(self):
        self.prog["provenance"]["source_sha256"] = None
        self.assertFails("LP-06")

    def test_personal_data(self):
        self.prog["title"] = "Contact Shri Ramesh Kumar at officer@example.gov.in"
        self.assertFails("LP-09")

    def test_mock_data(self):
        self.prog["data_status"] = "MOCK"
        self.assertFails("LP-10")

    def test_competency_definition_reproduced(self):
        self.comp["definition"] = "Some definition text"
        self.assertFails("LP-11")

    @unittest.skipUnless(v.CSCD_TEXT.exists(), "CSCD text layer is local-only")
    def test_passage_copied_from_cscd(self):
        words = re.findall(r"[A-Za-z']+", v.CSCD_TEXT.read_text(encoding="utf-8"))
        passage = " ".join(words[2000:2000 + v.SHINGLE_WORDS])
        self.comp["extraction_issues"].append(passage)
        self.assertFails("LP-11")

    def test_quote_too_long(self):
        self.d["tpac_references"]["records"][0]["context"] = "x " * 200
        self.assertFails("LP-11")

    def test_automated_verified_status(self):
        self.doc["data_status"] = "VERIFIED"
        self.assertFails("LP-12")

    def test_verified_without_reviewer(self):
        self.doc["review"]["verified"] = True
        self.assertFails("LP-12")

    def test_learner_visible_without_gates(self):
        self.prog["learner_visible"] = True
        self.assertFails("LP-18")

    def test_missing_review_blocker(self):
        self.prog["release_blockers"].remove("human_review_pending")
        self.assertFails("LP-19")

    def test_missing_series_blocker(self):
        target = next(r for r in self.d["documents"]["records"]
                      if r["series_base_year"]["applicable"] and r["series_base_year"]["value"] is None)
        target["release_blockers"].remove("series_base_year_unknown")
        self.assertFails("LP-20")

    def test_guessed_dates(self):
        self.prog["schedule"]["dates"] = {"start": "2025-04-01"}
        self.assertFails("LP-02")


class ReleaseGateAllowsReviewedRecordsTest(unittest.TestCase):
    def test_fully_reviewed_record_may_be_visible(self):
        d = copy.deepcopy(BASELINE)
        rec = d["training_programmes"]["records"][0]
        rec["review"].update({"verified": True, "verified_by": "reviewer", "verified_on": "2026-09-15"})
        rec["licence"].update({"status": "VERIFIED", "permits_learner_display": True})
        rec["release_blockers"] = []
        rec["learner_visible"] = True
        report = v.validate_datasets(d)
        self.assertEqual(errors(report, "LP-18"), [])
        self.assertEqual(errors(report, "LP-12"), [])
        self.assertEqual(report["totals"]["errors"], 0)


if __name__ == "__main__":
    unittest.main()
