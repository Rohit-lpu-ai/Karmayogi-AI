"""Check candidate document URLs without downloading them.

Discovery-phase tool. For each row in a candidates CSV it sends a HEAD request
(falling back to a 1-byte ranged GET if HEAD is refused) and records only
response metadata: status, content type, size, Last-Modified, final URL.
No document bodies are saved. TLS verification is never disabled.

Usage:
    python scripts/validators/check_document_urls.py CANDIDATES.csv OUT.json
"""

import csv
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER_AGENT = "KaramYogiAI-discovery/0.1 (SIH project; metadata-only source audit)"
DELAY_SECONDS = 1.5
TIMEOUT_SECONDS = 30


def _request(url, method, extra_headers=None):
    headers = {"User-Agent": USER_AGENT}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        if method == "GET":
            resp.read(1)
        return resp.status, resp.geturl(), dict(resp.headers)


def _size(headers):
    content_range = headers.get("Content-Range", "")
    if "/" in content_range:
        total = content_range.rsplit("/", 1)[1]
        return int(total) if total.isdigit() else None
    length = headers.get("Content-Length")
    return int(length) if length and length.isdigit() else None


def classify(status, content_type):
    if status is None:
        return "NETWORK_ERROR"
    if status in (200, 206):
        if "pdf" in content_type:
            return "DOWNLOADABLE_PDF"
        if "html" in content_type:
            return "SPA_SHELL_NOT_A_DOCUMENT"
        return "DOWNLOADABLE_OTHER"
    return f"HTTP_{status}"


def check(url):
    observed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    method_used = "HEAD"
    try:
        try:
            status, final_url, headers = _request(url, "HEAD")
        except urllib.error.HTTPError as err:
            if err.code not in (403, 405, 501):
                raise
            method_used = "GET Range: bytes=0-0"
            status, final_url, headers = _request(url, "GET", {"Range": "bytes=0-0"})
    except urllib.error.HTTPError as err:
        return {
            "observed_at_utc": observed_at, "method": method_used,
            "http_status": err.code, "download_status": f"HTTP_{err.code}",
            "error": str(err),
        }
    except Exception as err:  # network, DNS, TLS, timeout
        return {
            "observed_at_utc": observed_at, "method": method_used,
            "http_status": None, "download_status": "NETWORK_ERROR",
            "error": f"{type(err).__name__}: {err}",
        }

    content_type = headers.get("Content-Type", "")
    return {
        "observed_at_utc": observed_at,
        "method": method_used,
        "http_status": status,
        "final_url": final_url,
        "redirected": final_url != url,
        "content_type": content_type,
        "content_length_bytes": _size(headers),
        "server_last_modified": headers.get("Last-Modified"),
        "content_disposition": headers.get("Content-Disposition"),
        "download_status": classify(status, content_type.lower()),
    }


def main(candidates_path, out_path):
    with open(candidates_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    results = []
    for i, row in enumerate(rows):
        if i:
            time.sleep(DELAY_SECONDS)
        result = check(row["url"])
        results.append({"doc_id": row["doc_id"], "url": row["url"], **result})
        print(f'{row["doc_id"]}  {result["download_status"]}  {result.get("content_length_bytes")}')

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
