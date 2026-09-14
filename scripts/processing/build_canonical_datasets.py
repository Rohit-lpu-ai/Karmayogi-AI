"""Convert interim collection outputs into canonical datasets in data/processed/.

Outputs (schema: schemas/canonical_datasets.schema.json):
    topics.json, documents.json, training_programmes.json,
    competency_framework.json, tpac_references.json

Principles:
- Deterministic: IDs derive from content; same inputs give the same records.
- No guessing: unknown values stay null with status UNKNOWN; codes such as
  "ISS (P)" or "MCTP" are not expanded.
- Nothing is VERIFIED and nothing is learner_visible: learner visibility is
  computed from human review + a VERIFIED licence, neither of which exists yet.

Usage:
    python scripts/processing/build_canonical_datasets.py
"""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTERIM = ROOT / "data" / "interim"
OUT = ROOT / "data" / "processed"
TAXONOMY_PATH = ROOT / "scripts" / "processing" / "topic_taxonomy.json"
SCHEMA_VERSION = "0.2.0"
GENERATOR = "scripts/processing/build_canonical_datasets.py"

SOURCE_METADATA = {
    "SRC-025": INTERIM / "nssta_metadata.json",
    "SRC-001": INTERIM / "mospi_metadata.json",
    "SRC-026": INTERIM / "cscd_metadata.json",
}
TEXT_DIRS = {"SRC-025": INTERIM / "nssta" / "text", "SRC-001": INTERIM / "mospi" / "text", "SRC-026": INTERIM / "cscd" / "text"}
PROGRAMMES_PATH = INTERIM / "nssta" / "programmes_fy2025_26.json"
TPAC_PATH = INTERIM / "nssta" / "tpac_references.json"
CSCD_STRUCTURE_PATH = INTERIM / "cscd" / "competency_structure.json"

ATTRIBUTION = {
    "SRC-025": "Source: National Statistical Systems Training Academy (NSSTA), Ministry of Statistics and Programme Implementation, Government of India",
    "SRC-001": "Source: Ministry of Statistics and Programme Implementation (MoSPI), Government of India",
    "SRC-026": "Source: Department of Personnel and Training (DoPT), Government of India - Civil Services Competency Dictionary",
}
BASE_YEAR_APPLICABLE_SOURCES = {"SRC-001"}
# Series/base year is meaningful only for documents about statistical series,
# not for cross-cutting standards (e.g. metadata or quality frameworks).
SERIES_DOMAIN_TOPICS = {"survey_design", "sampling", "national_accounts", "price_statistics",
                        "labour_statistics", "sdg_indicators"}
# Series identifiers are taken only from text printed on the document's first page.
SERIES_PATTERNS = [
    (re.compile(r"NSS\s*(\d+)\s*th\s+Round", re.I), "NSS {}th Round"),
    (re.compile(r"CPI\s*(\d{4})\s*Series", re.I), "CPI {} Series"),
    (re.compile(r"National Indicator Framework,?\s*(\d{4})", re.I), "SDG NIF {}"),
]

# --- helpers ------------------------------------------------------------------


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def input_ref(path):
    path = Path(path)
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256_file(path)}


def load(path, inputs):
    """Read JSON and record it as an input of the dataset being built."""
    ref = input_ref(path)
    if ref not in inputs:
        inputs.append(ref)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def short_hash(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:10]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def review(check_names):
    return {"verified": False, "verified_by": None, "verified_on": None,
            "checks": {name: None for name in check_names}, "notes": None}


def learner_visible(record):
    lic, rev = record["licence"], record["review"]
    return bool(rev["verified"] and lic["status"] == "VERIFIED" and lic["permits_learner_display"] is True)


def licence_for(source_id, status, notes):
    return {"status": status, "usage_notes": notes, "attribution_text": ATTRIBUTION[source_id],
            "permits_learner_display": None}


def pdf_date(raw):
    m = re.match(r"^D:(\d{4})(\d{2})(\d{2})", raw or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def envelope(dataset_id, title, records, inputs, **extra):
    return {"schema_version": SCHEMA_VERSION, "dataset_id": dataset_id, "title": title,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "generator": GENERATOR, "inputs": inputs, "record_count": len(records),
            **extra, "records": records}


class Tagger:
    def __init__(self, taxonomy):
        self.rules = [(t["id"], [re.compile(r, re.I) for r in t["rules"]]) for t in taxonomy["topics"]]
        self.aliases = taxonomy["document_topic_aliases"]
        self.ids = {t["id"] for t in taxonomy["topics"]}

    def tag(self, text):
        return [tid for tid, pats in self.rules if any(p.search(text) for p in pats)]


def detect_languages(text_path, inputs):
    if not text_path.exists():
        return {"values": [], "status": "UNKNOWN", "method": "no extracted text available"}
    inputs.append(input_ref(text_path))
    text = text_path.read_text(encoding="utf-8")
    deva = len(re.findall(r"[ऀ-ॿ]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    total = deva + latin
    if total < 200:
        return {"values": [], "status": "UNKNOWN", "method": "too little text in PDF text layer to detect script"}
    values = [code for code, n in (("en", latin), ("hi", deva)) if n / total >= 0.05]
    return {"values": values, "status": "MACHINE_OBSERVED",
            "method": "character-script share in PDF text layer (script >= 5% of letters); Devanagari counted as hi"}


# --- datasets -----------------------------------------------------------------


def build_topics(taxonomy, taxonomy_ref):
    records = [{"id": t["id"], "label": t["label"], "data_status": taxonomy["status"], "rule_count": len(t["rules"])}
               for t in taxonomy["topics"]]
    return envelope("topics", "Topic taxonomy for linking programmes, documents and competencies",
                    records, [taxonomy_ref], taxonomy_version=taxonomy["version"], note=taxonomy["note"])


def build_documents(tagger, tpac_counts, shared_refs):
    inputs = list(shared_refs)
    cscd = load(CSCD_STRUCTURE_PATH, inputs)
    records = []
    for source_id, path in SOURCE_METADATA.items():
        meta = load(path, inputs)
        for item in meta["items"]:
            downloaded = item["status"] == "DOWNLOADED"
            doc_id = item["item_id"]
            title, title_status = item["document_title"], item["document_title_status"]
            publication_date, publication_status = None, "UNKNOWN"
            if doc_id == cscd["source_doc_id"]:
                title, title_status = cscd["document_title"], "MACHINE_OBSERVED"
                publication_date, publication_status = cscd["publication_date"], "MACHINE_OBSERVED"

            topics = []
            for t in item["topic"]:
                tid = tagger.aliases.get(t, t)
                topics.append({"topic_id": tid, "status": "ASSUMED", "method": "assigned by auditor in collection manifest"})

            series = {"applicable": False, "value": None, "status": "NOT_APPLICABLE"}
            if source_id in BASE_YEAR_APPLICABLE_SOURCES and SERIES_DOMAIN_TOPICS & {t["topic_id"] for t in topics}:
                series = {"applicable": True, "value": None, "status": "UNKNOWN"}
                first_page = " ".join(item.get("first_page_lines_for_title_check", []))
                for pattern, template in SERIES_PATTERNS:
                    m = pattern.search(first_page)
                    if m:
                        series = {"applicable": True, "value": template.format(m.group(1)), "status": "MACHINE_OBSERVED"}
                        break

            text_available = item.get("text_extractable") if downloaded else None
            record = {
                "id": doc_id,
                "title": title,
                "title_status": title_status,
                "document_type": item["category"],
                "organisation": item["source_organisation"],
                "topics": topics,
                "collection": {
                    "status": item["status"],
                    "bytes": item.get("bytes"),
                    "page_count": item.get("page_count"),
                    "text_available": text_available,
                    "scanned": (not text_available) if downloaded else None,
                },
                "languages_detected": (detect_languages(TEXT_DIRS[source_id] / f"{doc_id}.txt", inputs) if downloaded
                                       else {"values": [], "status": "UNKNOWN", "method": "not downloaded"}),
                "dates": {
                    "publication_date": publication_date,
                    "publication_date_status": publication_status,
                    "pdf_creation_date": pdf_date(item.get("pdf_creation_date")),
                    "server_last_modified": item.get("server_last_modified"),
                },
                "series_base_year": series,
                "tpac_reference_count": tpac_counts.get(doc_id, 0),
                "data_status": item["verification_status"],
                "provenance": {
                    "source_id": source_id,
                    "source_document_id": doc_id,
                    "source_url": item["source_url"],
                    "source_organisation": item["source_organisation"],
                    "retrieval_date": item.get("retrieval_date"),
                    "access_method": item["access_method"],
                    "local_file_path": item.get("local_file_path"),
                    "source_sha256": item.get("sha256"),
                },
                "licence": licence_for(source_id, item["licence_status"], item["licence_usage_notes"]),
                "review": review(["title_confirmed", "organisation_confirmed", "publication_date_confirmed",
                                  "topics_confirmed", "series_base_year_confirmed", "licence_confirmed",
                                  "personal_data_absent_confirmed"]),
            }
            if not downloaded:
                record["collection"]["reason_not_downloaded"] = item.get("reason_not_downloaded", "")

            blockers = ["human_review_pending", "topic_tags_unreviewed"]
            if record["licence"]["status"] != "VERIFIED":
                blockers.append("licence_not_verified")
            if source_id == "SRC-026":
                blockers.append("licence_restricts_reproduction")
            if title_status == "UNVERIFIED_SECONDHAND":
                blockers.append("title_unverified")
            if series["applicable"] and series["value"] is None:
                blockers.append("series_base_year_unknown")
            if downloaded and not text_available:
                blockers.append("scanned_no_text_layer")
            if not downloaded:
                blockers.append("link_only_not_collected")
            record["release_blockers"] = blockers
            record["learner_visible"] = learner_visible(record)
            records.append(record)

    records.sort(key=lambda r: r["id"])
    return envelope("documents", "Reference library: NSSTA, MoSPI and DoPT documents",
                    records, inputs)


def programme_family(ptype):
    ptype = norm(ptype)
    m = re.match(r"^ISS \(P\)\s*-\s*(\d+th Batch \(\d{4}\))$", ptype)
    if m:
        return "ISS (P)", m.group(1)
    m = re.match(r"^MCTP (Phase \d+) Stage\s*-\s*(I{1,3})$", ptype)
    if m:
        return "MCTP", f"{m.group(1)} Stage-{m.group(2)}"
    m = re.match(r"^ISEC, (\d+th Term)$", ptype)
    if m:
        return "ISEC", m.group(1)
    return ptype, None


def batch_size(raw):
    raw = norm(raw)
    m = re.match(r"^(\d+)(?:\s*-\s*(\d+))?$", raw)
    if not m:
        return {"min": None, "max": None, "as_printed": raw}
    lo = int(m.group(1))
    return {"min": lo, "max": int(m.group(2)) if m.group(2) else lo, "as_printed": raw}


def venue_options(raw):
    parts = [norm(p) for p in raw.split("/") if norm(p)]
    return parts if parts and all(len(p) <= 40 for p in parts) else [norm(raw)]


def build_programmes(tagger, shared_refs):
    inputs = list(shared_refs)
    data = load(PROGRAMMES_PATH, inputs)
    nssta_items = {i["item_id"]: i for i in load(SOURCE_METADATA["SRC-025"], inputs)["items"]}
    fy_match = re.search(r"FY\s*(\d{4})-(\d{2})", data["dataset"])
    fiscal_year = f"{fy_match.group(1)}-{fy_match.group(2)}"
    status_in_source = "Tentative" if data["calendar_status_in_source"].lower().startswith("tentative") else data["calendar_status_in_source"]
    source_item = nssta_items[data["source_doc_id"]]

    records = []
    for p in data["programmes"]:
        family, cohort = programme_family(p["programme_type"])
        topic = norm(p["topic"])
        tags = [{"topic_id": t, "status": "ASSUMED", "method": "keyword rule (scripts/processing/topic_taxonomy.json)"}
                for t in tagger.tag(topic)]
        record = {
            "id": "NSSTA-PRG-" + short_hash(fiscal_year, norm(p["programme_type"]), topic, norm(p["participant_group"]), norm(p["venue"])),
            "title": topic if topic.upper() != "TBD" else f"{family} (topic to be decided)",
            "provider": data["source_organisation"],
            "programme_family": family,
            "programme_type_as_printed": norm(p["programme_type"]),
            "cohort": cohort,
            "target_group": norm(p["participant_group"]),
            "topic_as_printed": topic,
            "topic_tags": tags,
            "delivery": {
                "duration_days_per_occurrence": p["duration_days_per_occurrence"],
                "occurrences_listed": p["occurrences_listed"],
                "total_days_listed": p["total_days_listed"],
                "batch_size": batch_size(p["batch_size"]),
                "venue_as_printed": norm(p["venue"]),
                "venue_options": venue_options(p["venue"]),
            },
            "schedule": {"fiscal_year": fiscal_year, "status_in_source": status_in_source,
                         "dates": None, "dates_status": "UNKNOWN"},
            "parse": {"method": data["extraction_method"], "confidence": p["parse_confidence"], "interim_id": p["programme_id"]},
            "data_status": data["status"],
            "provenance": {
                "source_id": "SRC-025",
                "source_document_id": data["source_doc_id"],
                "source_url": data["source_url"],
                "source_organisation": data["source_organisation"],
                "retrieval_date": data["retrieval_date"],
                "access_method": data["access_method"],
                "local_file_path": data["local_file_path"],
                "source_sha256": data["source_sha256"],
            },
            "licence": licence_for("SRC-025", source_item["licence_status"], data["licence_usage_notes"]),
            "review": review(["row_matches_pdf", "topic_tags_confirmed", "target_group_confirmed", "licence_confirmed"]),
        }
        blockers = ["human_review_pending", "parse_needs_spot_check", "schedule_dates_unknown"]
        if record["licence"]["status"] != "VERIFIED":
            blockers.append("licence_not_verified")
        if tags:
            blockers.append("topic_tags_unreviewed")
        record["release_blockers"] = blockers
        record["learner_visible"] = learner_visible(record)
        records.append(record)

    return envelope("training_programmes", f"NSSTA training programmes, FY {fiscal_year} (from the Advance Training Calendar)",
                    records, inputs)


def build_competencies():
    inputs = []
    cscd = load(CSCD_STRUCTURE_PATH, inputs)
    fw_id = "CSCD-2014"
    clusters = [{"id": f"{fw_id}-C{c['cluster_id']}", "code": c["cluster_id"], "name": c["cluster_name"],
                 "source_page": c["start_page"]} for c in cscd["clusters"]]
    scale = sorted({lvl for c in cscd["clusters"] for comp in c["competencies"] for lvl in comp["proficiency_levels_observed"]},
                   key=lambda s: int(s.split()[-1]))
    records = []
    for c in cscd["clusters"]:
        for comp in c["competencies"]:
            code = comp["competency_id"]
            variant = comp["name_as_printed_in_framework_page"]
            issues = [i for i in cscd["extraction_issues"] if i.startswith(f"{code}:")]
            record = {
                "id": f"{fw_id}-{code}",
                "framework_id": fw_id,
                "code": code,
                "name": comp["competency_name"],
                "name_variants": [variant] if variant not in ("UNKNOWN", comp["competency_name"]) else [],
                "cluster_id": f"{fw_id}-C{c['cluster_id']}",
                "proficiency_levels": comp["proficiency_levels_observed"],
                "definition": None,
                "definition_availability": (f"In the official document only (definitions p.{comp['definition_reference']['page']}, "
                                            f"proficiency indicators p.{comp['detail_page']}); not reproduced under the DoPT copyright policy"),
                "source_pages": {"definition": comp["definition_reference"]["page"], "detail": comp["detail_page"]},
                "extraction_issues": issues,
                "data_status": cscd["status"],
                "provenance": {
                    "source_id": "SRC-026",
                    "source_document_id": cscd["source_doc_id"],
                    "source_url": cscd["source_url"],
                    "source_organisation": cscd["source_organisation"],
                    "retrieval_date": cscd["retrieval_date"],
                    "access_method": cscd["access_method"],
                    "local_file_path": cscd["local_file_path"],
                    "source_sha256": cscd["source_sha256"],
                    "source_pages": sorted({comp["definition_reference"]["page"], comp["detail_page"]}),
                },
                "licence": licence_for("SRC-026", "MACHINE_OBSERVED", cscd["licence_usage_notes"]),
                "review": review(["name_matches_pdf", "cluster_confirmed", "proficiency_levels_confirmed",
                                  "dopt_permission_for_display"]),
            }
            blockers = ["human_review_pending", "licence_not_verified", "licence_restricts_reproduction"]
            if issues:
                blockers.append("extraction_issue")
            record["release_blockers"] = blockers
            record["learner_visible"] = learner_visible(record)
            records.append(record)

    framework = {
        "id": fw_id,
        "name": cscd["document_title"],
        "publisher": cscd["source_organisation"],
        "publication_date": cscd["publication_date"],
        "publication_date_status": cscd["publication_date_status"],
        "source_document_id": cscd["source_doc_id"],
        "proficiency_scale": scale,
        "clusters": clusters,
    }
    return envelope("competency_framework", "Civil Services Competency Dictionary (DoPT) - structure only",
                    records, inputs, framework=framework)


def build_tpac():
    inputs = []
    tpac = load(TPAC_PATH, inputs)
    nssta_items = {i["item_id"]: i for i in load(SOURCE_METADATA["SRC-025"], inputs)["items"]}
    records = []
    for ref in tpac["references"]:
        item = nssta_items[ref["doc_id"]]
        context = norm(ref["context"])
        record = {
            "id": "TPAC-REF-" + short_hash(ref["doc_id"], str(ref["page"]), context),
            "document_id": ref["doc_id"],
            "page": ref["page"],
            "context": context,
            "data_status": tpac["status"],
            "provenance": {
                "source_id": "SRC-025",
                "source_document_id": ref["doc_id"],
                "source_url": item["source_url"],
                "source_organisation": item["source_organisation"],
                "retrieval_date": item["retrieval_date"],
                "access_method": item["access_method"],
                "local_file_path": item["local_file_path"],
                "source_sha256": item["sha256"],
                "source_pages": [ref["page"]],
            },
            "licence": licence_for("SRC-025", item["licence_status"], item["licence_usage_notes"]),
            "review": review(["context_matches_pdf", "licence_confirmed"]),
        }
        blockers = ["human_review_pending"]
        if record["licence"]["status"] != "VERIFIED":
            blockers.append("licence_not_verified")
        record["release_blockers"] = blockers
        record["learner_visible"] = learner_visible(record)
        records.append(record)
    return envelope("tpac_references", "TPAC references found in collected NSSTA documents",
                    records, inputs, note=tpac["note"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    taxonomy_ref = input_ref(TAXONOMY_PATH)
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    tagger = Tagger(taxonomy)

    tpac_ref = input_ref(TPAC_PATH)
    tpac_counts = {}
    for ref in json.loads(TPAC_PATH.read_text(encoding="utf-8"))["references"]:
        tpac_counts[ref["doc_id"]] = tpac_counts.get(ref["doc_id"], 0) + 1

    datasets = {
        "topics": build_topics(taxonomy, taxonomy_ref),
        "documents": build_documents(tagger, tpac_counts, [taxonomy_ref, tpac_ref]),
        "training_programmes": build_programmes(tagger, [taxonomy_ref]),
        "competency_framework": build_competencies(),
        "tpac_references": build_tpac(),
    }
    for name, data in datasets.items():
        path = OUT / f"{name}.json"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{path.relative_to(ROOT).as_posix():45} records={data['record_count']} inputs={len(data['inputs'])}")


if __name__ == "__main__":
    main()
