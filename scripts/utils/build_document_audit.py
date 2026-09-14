"""Merge a candidates CSV, URL-check results and annotations into audit outputs.

Every field carries a status per STATUS_VOCABULARY.md. Nothing is inferred
beyond what the inputs state: document titles, languages and date hints come
from search indexes and stay UNVERIFIED_SECONDHAND; HTTP facts are
MACHINE_OBSERVED; anything absent is UNKNOWN.

Usage:
    python scripts/utils/build_document_audit.py EVIDENCE_DIR PREFIX
e.g.
    python scripts/utils/build_document_audit.py docs/evidence/MoSPI mospi

Reads  <PREFIX>_candidates.csv, <PREFIX>_url_checks.json, <PREFIX>_annotations.json
Writes <PREFIX>_document_corpus.json, <PREFIX>_document_corpus.csv, <PREFIX>_document_urls.txt
"""

import csv
import json
import sys
from pathlib import Path

COPYRIGHT_NOT_VISIBLE = (
    "Not visible: no copyright or licence information in HTTP response headers, "
    "and the document was not opened."
)


def build_item(cand, chk, note):
    live = chk.get("download_status") == "DOWNLOADABLE_PDF"
    date_hint = cand["pub_date_hint"]
    has_date_hint = date_hint and date_hint != "UNKNOWN"
    return {
        "doc_id": cand["doc_id"],
        "title": cand["indexed_title"],
        "title_status": "UNVERIFIED_SECONDHAND",
        "title_source": "search engine index; not read from the document",
        "url": chk.get("url", cand["url"]),
        "document_type": cand["document_type"],
        "document_type_status": "ASSUMED",
        "document_type_source": "classified by the auditor from the indexed title",
        "topic": cand["topic"],
        "secondary_topics": [t for t in cand["secondary_topics"].split(";") if t],
        "organization": cand["organization_hint"],
        "organization_status": "UNVERIFIED_SECONDHAND",
        "organization_source": "hosted on a mospi.gov.in domain (observed); attribution to a specific unit taken from the indexed title",
        "publication_date": date_hint if has_date_hint else "UNKNOWN",
        "publication_date_status": "UNVERIFIED_SECONDHAND" if has_date_hint else "UNKNOWN",
        "publication_date_source": cand["pub_date_hint_source"] if has_date_hint else "none available",
        "server_last_modified": chk.get("server_last_modified") or "UNKNOWN",
        "server_last_modified_status": "MACHINE_OBSERVED" if chk.get("server_last_modified") else "UNKNOWN",
        "server_last_modified_caveat": "HTTP Last-Modified is the file's upload time on the server, not its publication date.",
        "language": cand["language_hint"],
        "language_status": "UNVERIFIED_SECONDHAND",
        "language_source": "script of the indexed title; document not opened",
        "download_status": chk.get("download_status", "UNKNOWN"),
        "download_status_status": "MACHINE_OBSERVED",
        "http_status": chk.get("http_status"),
        "content_type": chk.get("content_type") or "UNKNOWN",
        "content_length_bytes": chk.get("content_length_bytes"),
        "check_method": chk.get("method"),
        "observed_at_utc": chk.get("observed_at_utc"),
        "check_error": chk.get("error"),
        "copyright_usage_notes": COPYRIGHT_NOT_VISIBLE,
        "copyright_usage_status": "UNKNOWN",
        "content_downloaded": False,
        "notes": note or "",
        "_live": live,
    }


def main(evidence_dir, prefix):
    base = Path(evidence_dir)
    with open(base / f"{prefix}_candidates.csv", newline="", encoding="utf-8") as f:
        candidates = list(csv.DictReader(f))
    checks = {c["doc_id"]: c for c in json.loads((base / f"{prefix}_url_checks.json").read_text(encoding="utf-8"))}
    notes = json.loads((base / f"{prefix}_annotations.json").read_text(encoding="utf-8"))

    missing = [c["doc_id"] for c in candidates if c["doc_id"] not in checks]
    if missing:
        sys.exit(f"No URL check result for: {missing}")

    items = [build_item(c, checks[c["doc_id"]], notes.get(c["doc_id"])) for c in candidates]
    live = [i for i in items if i["_live"]]
    for i in items:
        del i["_live"]

    (base / f"{prefix}_document_corpus.json").write_text(
        json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    columns = [
        "doc_id", "title", "title_status", "url", "document_type", "topic", "secondary_topics",
        "organization", "organization_status", "publication_date", "publication_date_status",
        "server_last_modified", "language", "language_status", "download_status", "http_status",
        "content_type", "content_length_bytes", "copyright_usage_status", "notes",
    ]
    with open(base / f"{prefix}_document_corpus.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for i in items:
            writer.writerow({**i, "secondary_topics": ";".join(i["secondary_topics"])})

    lines = [
        f"# {prefix} - downloadable document URLs",
        "# Each URL returned HTTP 200 with a PDF content type to a metadata-only check.",
        "# Status: MACHINE_OBSERVED. Content NOT downloaded. Licence per document: UNKNOWN.",
        "",
    ]
    for topic in sorted({i["topic"] for i in live}):
        lines.append(f"# --- {topic}")
        for i in (x for x in live if x["topic"] == topic):
            lines.append(f"# {i['doc_id']} | {i['document_type']} | {i['content_length_bytes']} bytes | {i['title']}")
            lines.append(i["url"])
        lines.append("")
    (base / f"{prefix}_document_urls.txt").write_text("\n".join(lines), encoding="utf-8")

    print(f"items: {len(items)}  live: {len(live)}  not live: {len(items) - len(live)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
