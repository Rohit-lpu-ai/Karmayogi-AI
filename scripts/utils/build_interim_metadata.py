"""Build data/interim/<name>_metadata.json from a collection manifest.

Combines, per item: the manifest entry, the raw provenance sidecar written by
fetch_documents.py, and the PDF metadata written by extract_pdf_metadata.py.
Links that were recorded but deliberately not downloaded are included with
their reason. Nothing is marked VERIFIED; each item has an empty
human_verification block.

Usage:
    python scripts/utils/build_interim_metadata.py MANIFEST.json OUT_JSON [DERIVED_FILE ...]
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def human_verification():
    return {"verified": False, "verified_by": None, "verified_on": None,
            "title_confirmed": None, "organisation_confirmed": None,
            "publication_date_confirmed": None, "licence_confirmed": None,
            "personal_data_absent_confirmed": None, "notes": None}


def downloaded_item(item, manifest):
    raw_dir = REPO_ROOT / manifest["raw_dir"]
    sidecars = list(raw_dir.glob(f"{item['doc_id']}__*.meta.json"))
    if not sidecars:
        return {
            "item_id": item["doc_id"], "source_url": item["url"],
            "source_organisation": item.get("organisation", manifest["organisation"]),
            "document_title": item["title"], "document_title_status": "UNVERIFIED_SECONDHAND",
            "category": item["category"], "topic": item["topic"].split(";"),
            "retrieval_date": None, "access_method": None,
            "status": "NOT_COLLECTED", "verification_status": "UNKNOWN",
            "local_file_path": None,
            "licence_usage_notes": manifest.get("licence_usage_notes", "UNKNOWN"),
            "licence_status": manifest.get("licence_status", "UNKNOWN"),
            "human_verification": human_verification(),
        }
    meta = load(sidecars[0])
    pdf_meta_path = REPO_ROOT / manifest["interim_dir"] / f"{item['doc_id']}.pdf_metadata.json"
    pdf = load(pdf_meta_path) if pdf_meta_path.exists() else {}
    notices = pdf.get("usage_notice_snippets", [])
    return {
        "item_id": item["doc_id"],
        "source_url": meta["source_url"],
        "source_organisation": meta["source_organisation"],
        "retrieval_date": meta["retrieval_date"],
        "retrieved_at_utc": meta["retrieved_at_utc"],
        "document_title": meta["document_title"],
        "document_title_status": meta["document_title_status"],
        "first_page_lines_for_title_check": pdf.get("first_page_lines", []),
        "category": meta["category"],
        "topic": meta["topic"].split(";"),
        "access_method": meta["access_method"],
        "status": meta["collection_status"],
        "verification_status": meta["verification_status"],
        "local_file_path": meta["local_file_path"],
        "provenance_sidecar": sidecars[0].relative_to(REPO_ROOT).as_posix(),
        "sha256": meta["sha256"],
        "bytes": meta["bytes"],
        "server_last_modified": meta["server_last_modified"],
        "server_last_modified_caveat": "Upload time on the server, not a publication date.",
        "pdf_creation_date": pdf.get("pdf_info", {}).get("CreationDate", "UNKNOWN"),
        "page_count": pdf.get("page_count"),
        "text_extractable": pdf.get("text_extractable"),
        "licence_usage_notes": meta["licence_usage_notes"],
        "licence_status": meta["licence_status"],
        "usage_notice_in_document_text": (
            "Found - see usage_notice_snippets" if notices else
            "None found by keyword scan of extracted text" if pdf.get("text_extractable") else
            "UNKNOWN - no text layer (scanned); not scanned for notices"),
        "usage_notice_snippets": notices,
        "authorisation": meta["authorisation"],
        "human_verification": human_verification(),
    }


def link_item(link, manifest):
    return {
        "item_id": link["doc_id"],
        "source_url": link["url"],
        "source_organisation": link.get("organisation", manifest["organisation"]),
        "retrieval_date": None,
        "document_title": link["title"],
        "document_title_status": "UNVERIFIED_SECONDHAND",
        "category": link["category"],
        "topic": link["topic"].split(";"),
        "access_method": "Link recorded only; not downloaded",
        "status": "LINK_RECORDED_NOT_DOWNLOADED",
        "verification_status": "MACHINE_OBSERVED" if "HTTP 200" in link.get("observed", "") else "UNKNOWN",
        "observation": link.get("observed"),
        "reason_not_downloaded": link["reason_not_downloaded"],
        "local_file_path": None,
        "licence_usage_notes": manifest.get("licence_usage_notes", "UNKNOWN"),
        "licence_status": manifest.get("licence_status", "UNKNOWN"),
        "human_verification": human_verification(),
    }


def main(manifest_path, out_path, derived):
    manifest = load(manifest_path)
    items = [downloaded_item(i, manifest) for i in manifest["items"]]
    items += [link_item(l, manifest) for l in manifest.get("links_recorded_not_downloaded", [])]
    statuses = {}
    for it in items:
        statuses[it["status"]] = statuses.get(it["status"], 0) + 1
    out = {
        "source_id": manifest["source_id"],
        "source_organisation": manifest["organisation"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "manifest": Path(manifest_path).as_posix(),
        "authorisation": manifest["authorisation"],
        "verification_note": "Nothing in this file is VERIFIED. All human_verification blocks await review.",
        "counts": {"items": len(items), "by_status": statuses,
                   "bytes_downloaded": sum(i.get("bytes") or 0 for i in items)},
        "derived_datasets": [Path(d).as_posix() for d in derived],
        "items": items,
    }
    Path(out_path).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{out_path}: {out['counts']}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
