"""Validate data/processed/ canonical datasets against the learning-platform requirements.

Every check maps to a requirement in docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md
(LP-01 .. LP-21) with its severity:
  ERROR            -> dataset invalid; exit code 1
  RELEASE_BLOCKER  -> valid for development, not showable to learners
  WARNING          -> tracked quality gap

Usage:
    python scripts/validators/validate_canonical_datasets.py            # validate + write reports
    python scripts/validators/validate_canonical_datasets.py --no-write # validate only
"""

import copy
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
SCHEMA_PATH = ROOT / "schemas" / "canonical_datasets.schema.json"
REGISTRY_PATH = ROOT / "registry" / "source_registry.csv"
CSCD_TEXT = ROOT / "data" / "interim" / "cscd" / "text" / "CSCD-DOC-001.txt"
DATASETS = ["topics", "documents", "training_programmes", "competency_framework", "tpac_references"]

REQUIREMENTS = {
    "LP-01": ("ERROR", "Dataset envelope complete; record_count matches"),
    "LP-02": ("ERROR", "Validates against canonical JSON Schema"),
    "LP-03": ("ERROR", "Record IDs unique and deterministic"),
    "LP-04": ("ERROR", "Cross-references resolve"),
    "LP-05": ("ERROR", "Status values from STATUS_VOCABULARY.md"),
    "LP-06": ("ERROR", "Provenance complete for every record"),
    "LP-07": ("ERROR", "Raw source checksums match (missing local raw file = WARNING)"),
    "LP-08": ("ERROR", "Licence status and usage notes present"),
    "LP-09": ("ERROR", "No personal data"),
    "LP-10": ("ERROR", "No MOCK data in data/processed"),
    "LP-11": ("ERROR", "No reproduction of restricted content"),
    "LP-12": ("ERROR", "No automated verification"),
    "LP-13": ("ERROR", "Programme catalogue fields usable"),
    "LP-14": ("ERROR", "Reference library fields usable"),
    "LP-15": ("ERROR", "Competency framework fields usable"),
    "LP-16": ("WARNING", "Topic-tag linkability coverage"),
    "LP-17": ("ERROR", "Schedule status recorded; unknown dates not guessed"),
    "LP-18": ("ERROR", "learner_visible only when review + VERIFIED licence"),
    "LP-19": ("RELEASE_BLOCKER", "Outstanding release blockers listed"),
    "LP-20": ("RELEASE_BLOCKER", "Methodology documents record series/base year"),
    "LP-21": ("RELEASE_BLOCKER", "Search-index titles confirmed before release"),
}
VOCAB = {"VERIFIED", "UNKNOWN", "UNAVAILABLE", "MOCK", "ASSUMED", "MACHINE_OBSERVED",
         "UNVERIFIED_SECONDHAND", "EXCLUDED_BY_POLICY", "NOT_APPLICABLE"}
PERSONAL_PATTERNS = {
    "honorific_name": re.compile(r"\b(?:Shri|Smt|Kumari|Mr|Mrs|Ms|Dr)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "indian_mobile": re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"),
    "twelve_digit_id": re.compile(r"(?<![\d_])\d{4}\s?\d{4}\s?\d{4}(?![\d_])"),
}
PROGRAMME_COVERAGE_TARGET = 0.80
QUOTE_LIMIT = 220
SHINGLE_WORDS = 12


class Findings:
    def __init__(self):
        self.items = defaultdict(list)

    def add(self, req, dataset, record_id, message, severity=None):
        self.items[req].append({"severity": severity or REQUIREMENTS[req][0], "dataset": dataset,
                                "record_id": record_id, "message": message})


def sha256_file(path, cache={}):
    key = str(path)
    if key not in cache:
        cache[key] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return cache[key]


def short_hash(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:10]


def load_datasets(processed_dir=PROCESSED):
    return {name: json.loads((Path(processed_dir) / f"{name}.json").read_text(encoding="utf-8")) for name in DATASETS}


def registry_ids():
    with open(REGISTRY_PATH, newline="", encoding="utf-8") as f:
        return {row["source_id"] for row in csv.DictReader(f)}


def walk_status_values(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            here = f"{path}.{k}" if path else k
            if isinstance(v, str) and (k == "status" or k.endswith("_status")):
                yield here, v
            else:
                yield from walk_status_values(v, here)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_status_values(v, f"{path}[{i}]")


# Status-like fields that intentionally carry non-vocabulary values.
NON_VOCAB_STATUS_FIELDS = {"collection.status", "schedule.status_in_source", "framework.publication_date_status"}


def content_without_provenance(record):
    r = {k: v for k, v in record.items() if k not in ("provenance", "licence")}
    return json.dumps(r, ensure_ascii=False)


def validate_datasets(datasets):
    f = Findings()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    known_sources = registry_ids()
    checked_raw = {}

    for name in DATASETS:
        data = datasets.get(name)
        if data is None:
            f.add("LP-01", name, None, "dataset file missing")
            continue

        # LP-01 envelope
        if data.get("record_count") != len(data.get("records", [])):
            f.add("LP-01", name, None, f"record_count {data.get('record_count')} != {len(data.get('records', []))} records")
        for inp in data.get("inputs", []):
            p = ROOT / inp["path"]
            if not p.exists():
                f.add("LP-01", name, None, f"input not present locally: {inp['path']}", "WARNING")
            elif sha256_file(p) != inp["sha256"]:
                f.add("LP-01", name, None, f"input changed since build (rebuild needed): {inp['path']}", "WARNING")

        # LP-02 schema
        validator = Draft202012Validator({"$ref": f"#/$defs/{name}_dataset", "$defs": schema["$defs"]})
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))[:50]:
            loc = "/".join(str(x) for x in err.absolute_path)
            f.add("LP-02", name, loc, err.message[:300])

        records = data.get("records", [])

        # LP-03 unique ids
        for rid, n in Counter(r.get("id") for r in records).items():
            if n > 1:
                f.add("LP-03", name, rid, f"duplicate id ({n} records)")

        for r in records:
            rid = r.get("id")
            prov = r.get("provenance", {})

            # LP-05 statuses
            for field, value in walk_status_values(r):
                if field not in NON_VOCAB_STATUS_FIELDS and value not in VOCAB:
                    f.add("LP-05", name, rid, f"{field}={value!r} not in vocabulary")

            # LP-06 / LP-07 provenance and checksums (topics carry no provenance)
            if name != "topics":
                if prov.get("source_id") not in known_sources:
                    f.add("LP-04", name, rid, f"source_id {prov.get('source_id')!r} not in registry")
                collected = name != "documents" or r.get("collection", {}).get("status") == "DOWNLOADED"
                if collected:
                    for key in ("local_file_path", "source_sha256", "retrieval_date"):
                        if not prov.get(key):
                            f.add("LP-06", name, rid, f"collected record missing provenance.{key}")
                path = prov.get("local_file_path")
                if path and prov.get("source_sha256"):
                    raw = ROOT / path
                    if path not in checked_raw:
                        checked_raw[path] = None if not raw.exists() else sha256_file(raw) == prov["source_sha256"]
                    if checked_raw[path] is None:
                        f.add("LP-07", name, rid, f"raw file not present locally, checksum not checked: {path}", "WARNING")
                    elif checked_raw[path] is False:
                        f.add("LP-07", name, rid, f"checksum mismatch for {path}")

                # LP-08 licence
                lic = r.get("licence", {})
                if not lic.get("status") or not lic.get("usage_notes"):
                    f.add("LP-08", name, rid, "licence status or usage notes missing")

                # LP-09 personal data
                content = content_without_provenance(r)
                for label, pat in PERSONAL_PATTERNS.items():
                    m = pat.search(content)
                    if m:
                        f.add("LP-09", name, rid, f"possible personal data ({label}): {m.group(0)!r}")

                # LP-12 verification integrity
                rev = r.get("review", {})
                if rev.get("verified") and not (rev.get("verified_by") and rev.get("verified_on")):
                    f.add("LP-12", name, rid, "review.verified is true without verified_by and verified_on")
                if not rev.get("verified"):
                    for field, value in walk_status_values(r):
                        if value == "VERIFIED":
                            f.add("LP-12", name, rid, f"{field} is VERIFIED but the record has no completed human review")

                # LP-18 learner visibility gate
                gate = bool(rev.get("verified") and lic.get("status") == "VERIFIED" and lic.get("permits_learner_display") is True)
                if r.get("learner_visible") and not gate:
                    f.add("LP-18", name, rid, "learner_visible=true without completed review and VERIFIED licence permitting display")

                # LP-19 blockers consistency
                blockers = r.get("release_blockers", [])
                if r.get("learner_visible") and blockers:
                    f.add("LP-18", name, rid, f"learner_visible=true while release blockers remain: {blockers}")
                if not r.get("learner_visible") and not blockers:
                    f.add("LP-19", name, rid, "not learner-visible but no release blocker explains why", "WARNING")
                if not rev.get("verified") and "human_review_pending" not in blockers:
                    f.add("LP-19", name, rid, "human review pending but blocker not listed", "ERROR")
                for b in blockers:
                    f.add("LP-19", name, rid, b)

            # LP-10 mock
            if "MOCK" in json.dumps(r) and re.search(r'"MOCK"|MOCK-', json.dumps(r)):
                f.add("LP-10", name, rid, "MOCK content in processed dataset")

    # Cross-dataset checks
    topics = {t["id"] for t in datasets.get("topics", {}).get("records", [])}
    docs = {d["id"]: d for d in datasets.get("documents", {}).get("records", [])}
    fw = datasets.get("competency_framework", {}).get("framework", {})
    clusters = {c["id"] for c in fw.get("clusters", [])}

    for d in docs.values():
        for t in d.get("topics", []):
            if t["topic_id"] not in topics:
                f.add("LP-04", "documents", d["id"], f"unknown topic {t['topic_id']!r}")
        if d.get("id") != d.get("provenance", {}).get("source_document_id"):
            f.add("LP-03", "documents", d["id"], "id does not equal provenance.source_document_id")
        coll = d.get("collection", {})
        if coll.get("status") == "DOWNLOADED" and (coll.get("page_count") is None or coll.get("text_available") is None):
            f.add("LP-14", "documents", d["id"], "downloaded document lacks page_count or text_available")
        sb = d.get("series_base_year", {})
        if sb.get("applicable") and sb.get("value") is None:
            if "series_base_year_unknown" not in d.get("release_blockers", []):
                f.add("LP-20", "documents", d["id"], "series/base year unknown but blocker not listed", "ERROR")
            f.add("LP-20", "documents", d["id"], "series/base year unknown")
        if d.get("title_status") == "UNVERIFIED_SECONDHAND":
            if "title_unverified" not in d.get("release_blockers", []):
                f.add("LP-21", "documents", d["id"], "secondhand title but blocker not listed", "ERROR")
            f.add("LP-21", "documents", d["id"], "title taken from search index; confirm against document")

    progs = datasets.get("training_programmes", {}).get("records", [])
    for p in progs:
        expected = "NSSTA-PRG-" + short_hash(p["schedule"]["fiscal_year"], p["programme_type_as_printed"],
                                             p["topic_as_printed"], p["target_group"], p["delivery"]["venue_as_printed"])
        if p["id"] != expected:
            f.add("LP-03", "training_programmes", p["id"], f"id not reproducible from content (expected {expected})")
        for t in p.get("topic_tags", []):
            if t["topic_id"] not in topics:
                f.add("LP-04", "training_programmes", p["id"], f"unknown topic {t['topic_id']!r}")
        if p.get("target_group") in (None, "", "UNKNOWN"):
            f.add("LP-13", "training_programmes", p["id"], "target group unknown", "WARNING")
        if p["schedule"].get("dates") is not None and p["schedule"].get("dates_status") != "MACHINE_OBSERVED":
            f.add("LP-17", "training_programmes", p["id"], "dates present without an observed source")
        if not p["schedule"].get("status_in_source"):
            f.add("LP-17", "training_programmes", p["id"], "schedule status missing")
    if progs:
        tagged = sum(1 for p in progs if p.get("topic_tags"))
        share = tagged / len(progs)
        if share < PROGRAMME_COVERAGE_TARGET:
            f.add("LP-16", "training_programmes", None, f"topic-tag coverage {tagged}/{len(progs)} ({share:.0%}) below {PROGRAMME_COVERAGE_TARGET:.0%}")
        for p in progs:
            if not p.get("topic_tags"):
                f.add("LP-16", "training_programmes", p["id"], f"untagged: {p['topic_as_printed']!r}")

    for c in datasets.get("competency_framework", {}).get("records", []):
        if c.get("cluster_id") not in clusters:
            f.add("LP-04", "competency_framework", c.get("id"), f"unknown cluster {c.get('cluster_id')!r}")
        if c.get("id") != f"{c.get('framework_id')}-{c.get('code')}":
            f.add("LP-03", "competency_framework", c.get("id"), "id not reproducible from framework_id and code")
        if c.get("definition") is not None:
            f.add("LP-11", "competency_framework", c.get("id"), "definition text present (DoPT copyright policy)")
        if c.get("proficiency_levels") != fw.get("proficiency_scale"):
            f.add("LP-15", "competency_framework", c.get("id"),
                  f"levels {c.get('proficiency_levels')} differ from framework scale {fw.get('proficiency_scale')}", "WARNING")

    # LP-11: no 12-word run from the CSCD text layer anywhere in the competency dataset
    if CSCD_TEXT.exists():
        words = re.findall(r"[A-Za-z']+", CSCD_TEXT.read_text(encoding="utf-8").lower())
        shingles = {" ".join(words[i:i + SHINGLE_WORDS]) for i in range(len(words) - SHINGLE_WORDS + 1)}
        # Scan content fields only. Bibliographic fields (framework name/publisher,
        # provenance, licence/attribution) cite the document by title, which the
        # DoPT policy requires, and are not reproduction of its content.
        cf = datasets.get("competency_framework", {})
        content = {
            "clusters": cf.get("framework", {}).get("clusters", []),
            "proficiency_scale": cf.get("framework", {}).get("proficiency_scale", []),
            "records": [{k: v for k, v in r.items() if k not in ("provenance", "licence")} for r in cf.get("records", [])],
        }
        dataset_words = re.findall(r"[A-Za-z']+", json.dumps(content).lower())
        for i in range(len(dataset_words) - SHINGLE_WORDS + 1):
            run = " ".join(dataset_words[i:i + SHINGLE_WORDS])
            if run in shingles:
                f.add("LP-11", "competency_framework", None, f"{SHINGLE_WORDS}-word passage copied from CSCD: {run!r}")
                break
    else:
        f.add("LP-11", "competency_framework", None, "CSCD text layer not present locally; copy check skipped", "WARNING")

    for t in datasets.get("tpac_references", {}).get("records", []):
        if t.get("document_id") not in docs:
            f.add("LP-04", "tpac_references", t.get("id"), f"unknown document {t.get('document_id')!r}")
        if len(t.get("context", "")) > QUOTE_LIMIT:
            f.add("LP-11", "tpac_references", t.get("id"), f"context exceeds {QUOTE_LIMIT} characters")
        expected = "TPAC-REF-" + short_hash(t["document_id"], str(t["page"]), t["context"])
        if t.get("id") != expected:
            f.add("LP-03", "tpac_references", t.get("id"), "id not reproducible from content")

    return build_report(f, datasets)


def build_report(f, datasets):
    requirements = []
    totals = Counter()
    blockers = Counter()
    severity_order = {"ERROR": 0, "WARNING": 1, "RELEASE_BLOCKER": 2}
    for req, (severity, title) in REQUIREMENTS.items():
        # Most severe first, so truncation below can never hide an ERROR behind
        # hundreds of per-record release blockers.
        items = sorted(f.items.get(req, []), key=lambda i: severity_order[i["severity"]])
        by_sev = Counter(i["severity"] for i in items)
        totals.update(by_sev)
        if req == "LP-19":
            blockers.update(i["message"] for i in items if i["severity"] == "RELEASE_BLOCKER")
        if by_sev.get("ERROR"):
            outcome = "FAIL"
        elif by_sev.get("RELEASE_BLOCKER"):
            outcome = "BLOCKED"
        elif by_sev.get("WARNING"):
            outcome = "WARN"
        else:
            outcome = "PASS"
        requirements.append({"id": req, "title": title, "severity": severity, "outcome": outcome,
                             "counts": dict(by_sev), "findings": items[:25], "findings_total": len(items)})

    per_dataset = {}
    for name, data in datasets.items():
        recs = data.get("records", [])
        per_dataset[name] = {
            "records": len(recs),
            "learner_visible": sum(1 for r in recs if r.get("learner_visible")),
            "verified": sum(1 for r in recs if r.get("review", {}).get("verified")),
        }
    errors = totals.get("ERROR", 0)
    all_visible = all(d["learner_visible"] == d["records"] for n, d in per_dataset.items() if n != "topics")
    if errors:
        verdict = "INVALID"
    elif totals.get("RELEASE_BLOCKER", 0) or not all_visible:
        verdict = "VALID_FOR_DEVELOPMENT_NOT_RELEASABLE"
    else:
        verdict = "RELEASE_READY"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "requirements_document": "docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md",
        "schema": SCHEMA_PATH.relative_to(ROOT).as_posix(),
        "verdict": verdict,
        "totals": {"errors": errors, "warnings": totals.get("WARNING", 0),
                   "release_blocker_findings": totals.get("RELEASE_BLOCKER", 0)},
        "release_blockers_by_type": dict(blockers.most_common()),
        "datasets": per_dataset,
        "requirements": requirements,
    }


def render_markdown(report):
    lines = [
        "# Dataset Validation Report", "",
        f"**Generated:** {report['generated_at_utc']}  ",
        f"**Requirements:** [`{report['requirements_document']}`](LEARNING_PLATFORM_DATA_REQUIREMENTS.md)  ",
        f"**Schema:** `{report['schema']}`  ",
        "**Validator:** `scripts/validators/validate_canonical_datasets.py` (this file is generated; do not edit)", "",
        f"## Verdict: `{report['verdict']}`", "",
        f"| Errors | Warnings | Release-blocker findings |", "|---|---|---|",
        f"| {report['totals']['errors']} | {report['totals']['warnings']} | {report['totals']['release_blocker_findings']} |", "",
        "## Datasets", "", "| Dataset | Records | Human-verified | Learner-visible |", "|---|---|---|---|",
    ]
    for name, d in report["datasets"].items():
        lines.append(f"| `{name}` | {d['records']} | {d['verified']} | {d['learner_visible']} |")
    lines += ["", "## Requirements", "", "| ID | Requirement | Severity | Outcome | Findings |", "|---|---|---|---|---|"]
    for r in report["requirements"]:
        counts = ", ".join(f"{k.lower()}: {v}" for k, v in r["counts"].items()) or "—"
        lines.append(f"| {r['id']} | {r['title']} | {r['severity']} | **{r['outcome']}** | {counts} |")
    lines += ["", "## Release blockers (per record)", "", "| Blocker | Records |", "|---|---|"]
    for b, n in report["release_blockers_by_type"].items():
        lines.append(f"| `{b}` | {n} |")
    lines += ["", "## Findings other than per-record release blockers", ""]
    for r in report["requirements"]:
        shown = [i for i in r["findings"] if not (r["id"] == "LP-19" and i["severity"] == "RELEASE_BLOCKER")]
        if not shown:
            continue
        lines.append(f"### {r['id']} — {r['title']} ({r['findings_total']} total)")
        for i in shown[:15]:
            rid = f" `{i['record_id']}`" if i["record_id"] else ""
            lines.append(f"- **{i['severity']}** `{i['dataset']}`{rid}: {i['message']}")
        if r["findings_total"] > 15:
            lines.append(f"- … {r['findings_total'] - 15} more in `data/processed/validation_report.json`")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv):
    report = validate_datasets(load_datasets())
    if "--no-write" not in argv:
        (PROCESSED / "validation_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ROOT / "docs" / "DATASET_VALIDATION_REPORT.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"verdict={report['verdict']} errors={report['totals']['errors']} warnings={report['totals']['warnings']} "
          f"release_blocker_findings={report['totals']['release_blocker_findings']}")
    for r in report["requirements"]:
        print(f"  {r['id']} {r['outcome']:8} {r['counts']}")
    return 1 if report["totals"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
