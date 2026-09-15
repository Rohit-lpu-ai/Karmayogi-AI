"""Download an explicit, reviewed list of public documents.

Controlled collection only: this fetches exactly the items in a manifest,
never follows links, never crawls. Each file is checked (allowed host, PDF
content type and %PDF- signature, size cap), written atomically, and given a
provenance sidecar ``<file>.meta.json``. Files already collected (sidecar
present with a matching checksum) are not downloaded again.

Nothing is ever marked VERIFIED: sidecars carry verification_status
MACHINE_OBSERVED and an empty human_verification block for a reviewer.

Usage:
    python scripts/collectors/fetch_documents.py MANIFEST.json
"""

import hashlib
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
USER_AGENT = "KaramYogiAI-collector/0.1 (SIH project; controlled document collection)"
DELAY_SECONDS = 2.0
TIMEOUT_SECONDS = 60
DEFAULT_MAX_BYTES = 25 * 1024 * 1024
CHUNK = 64 * 1024


def safe_filename(doc_id, url):
    name = unquote(Path(urlparse(url).path).name) or "document.pdf"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "document.pdf"
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    return f"{doc_id}__{name}"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def human_verification_block():
    return {
        "verified": False,
        "verified_by": None,
        "verified_on": None,
        "title_confirmed": None,
        "organisation_confirmed": None,
        "publication_date_confirmed": None,
        "licence_confirmed": None,
        "personal_data_absent_confirmed": None,
        "notes": None,
    }


def download(item, manifest, out_dir):
    url = item["url"]
    host = urlparse(url).hostname or ""
    if host not in manifest["allowed_hosts"]:
        return {"status": "REFUSED_HOST_NOT_ALLOWED", "error": host}

    target = out_dir / safe_filename(item["doc_id"], url)
    sidecar = target.with_name(target.name + ".meta.json")
    if target.exists() and sidecar.exists():
        recorded = json.loads(sidecar.read_text(encoding="utf-8")).get("sha256")
        if recorded and recorded == sha256_of(target):
            return {"status": "SKIPPED_ALREADY_COLLECTED", "local_path": target, "sidecar": sidecar}

    max_bytes = item.get("max_bytes", manifest.get("max_bytes", DEFAULT_MAX_BYTES))
    retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    partial = target.with_name(target.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            headers = dict(resp.headers)
            content_type = headers.get("Content-Type", "")
            declared = headers.get("Content-Length")
            if "pdf" not in content_type.lower():
                return {"status": "FAILED_NOT_PDF", "error": content_type, "http_status": resp.status}
            if declared and declared.isdigit() and int(declared) > max_bytes:
                return {"status": "SKIPPED_TOO_LARGE", "error": f"{declared} > {max_bytes}", "http_status": resp.status}
            size = 0
            with open(partial, "wb") as f:
                first = resp.read(CHUNK)
                if not first.startswith(b"%PDF-"):
                    raise ValueError("response body does not start with %PDF-")
                while first:
                    size += len(first)
                    if size > max_bytes:
                        raise ValueError(f"body exceeded {max_bytes} bytes")
                    f.write(first)
                    first = resp.read(CHUNK)
            status_code, final_url = resp.status, resp.geturl()
    except Exception as err:
        partial.unlink(missing_ok=True)
        return {"status": "FAILED", "error": f"{type(err).__name__}: {err}"}

    partial.replace(target)
    meta = {
        "doc_id": item["doc_id"],
        "source_id": manifest["source_id"],
        "source_url": url,
        "final_url": final_url,
        "source_organisation": item.get("organisation", manifest["organisation"]),
        "document_title": item["title"],
        "document_title_status": item.get("title_status", "UNVERIFIED_SECONDHAND"),
        "category": item["category"],
        "topic": item["topic"],
        "retrieval_date": retrieved_at[:10],
        "retrieved_at_utc": retrieved_at,
        "access_method": "HTTPS GET of a direct public file URL (no authentication, no crawling)",
        "user_agent": USER_AGENT,
        "http_status": status_code,
        "content_type": content_type,
        "server_last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
        "bytes": size,
        "sha256": sha256_of(target),
        "local_file_path": target.relative_to(REPO_ROOT).as_posix(),
        "collection_status": "DOWNLOADED",
        "verification_status": "MACHINE_OBSERVED",
        "licence_usage_notes": manifest.get("licence_usage_notes", "UNKNOWN"),
        "licence_status": manifest.get("licence_status", "UNKNOWN"),
        "authorisation": manifest["authorisation"],
        "human_verification": human_verification_block(),
    }
    sidecar.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": "DOWNLOADED", "local_path": target, "sidecar": sidecar}


def main(manifest_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    out_dir = REPO_ROOT / manifest["raw_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    log = []
    for i, item in enumerate(manifest["items"]):
        if i:
            time.sleep(DELAY_SECONDS)
        result = download(item, manifest, out_dir)
        entry = {"doc_id": item["doc_id"], "url": item["url"], "attempted_at_utc":
                 datetime.now(timezone.utc).isoformat(timespec="seconds"), **result}
        for key in ("local_path", "sidecar"):
            if key in entry:
                entry[key] = Path(entry[key]).relative_to(REPO_ROOT).as_posix()
        log.append(entry)
        print(f'{item["doc_id"]:16} {result["status"]:28} {result.get("error", "")}')

    log_path = REPO_ROOT / manifest["interim_dir"] / "collection_log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
