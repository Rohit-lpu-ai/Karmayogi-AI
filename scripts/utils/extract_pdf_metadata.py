"""Extract document-level metadata from collected PDFs.

For each ``*.pdf`` in a raw directory this records page count, the PDF info
dictionary, whether text is extractable, the pages on which given keywords
occur, and short snippets around any copyright / reproduction notice. It
does not store document content in tracked files: full extracted text goes to
``<interim_dir>/text/`` which is git-ignored, for local analysis only.

Usage:
    python scripts/utils/extract_pdf_metadata.py RAW_DIR INTERIM_DIR [KEYWORD ...]
"""

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

# Usage-notice wording only; bare "licence"/"reproduc" matched unrelated text
# ("licence fee", "reproductive health") in practice.
NOTICE_PATTERNS = [
    r"©",
    r"all rights reserved",
    r"copyright\s*(?:©|\(c\)|reserved|notice|policy|\d{4})",
    r"reproduc\w*\s+(?:is\s+|are\s+)?(?:permitted|allowed|prohibited)",
    r"may\s+(?:not\s+)?be\s+(?:freely\s+)?reproduced",
    r"acknowledg\w*\s+(?:of\s+)?the\s+source",
    r"creative\s+commons|open\s+government\s+data\s+licen[cs]e",
]
SNIPPET_CHARS = 160
MAX_SNIPPETS = 5


def _clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def _info(reader):
    try:
        meta = reader.metadata or {}
    except Exception:
        return {}
    return {k.lstrip("/"): str(v) for k, v in meta.items() if v not in (None, "")}


def extract(pdf_path, text_dir, keywords):
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")

    text_dir.mkdir(parents=True, exist_ok=True)
    doc_id = pdf_path.name.split("__", 1)[0]
    (text_dir / f"{doc_id}.txt").write_text(
        "\n\f\n".join(pages), encoding="utf-8")

    chars = [len(_clean(p)) for p in pages]
    first_lines = [ln.strip() for ln in (pages[0] if pages else "").splitlines() if ln.strip()][:6]

    keyword_pages = {}
    for kw in keywords:
        hits = [i + 1 for i, p in enumerate(pages) if re.search(re.escape(kw), p, re.I)]
        keyword_pages[kw] = hits

    notices = []
    for i, p in enumerate(pages):
        flat = _clean(p)
        for pat in NOTICE_PATTERNS:
            for m in re.finditer(pat, flat, re.I):
                start = max(0, m.start() - SNIPPET_CHARS // 2)
                notices.append({"page": i + 1, "pattern": pat,
                                "snippet": flat[start:start + SNIPPET_CHARS]})
                if len(notices) >= MAX_SNIPPETS:
                    break
            if len(notices) >= MAX_SNIPPETS:
                break
        if len(notices) >= MAX_SNIPPETS:
            break

    return {
        "doc_id": doc_id,
        "local_file_path": pdf_path.as_posix(),
        "page_count": len(pages),
        "pdf_info": _info(reader),
        "text_extractable": sum(chars) > 50 * max(1, len(pages)) // 10,
        "extracted_chars_total": sum(chars),
        "pages_without_text": [i + 1 for i, c in enumerate(chars) if c < 20],
        "first_page_lines": [ln[:120] for ln in first_lines],
        "keyword_pages": keyword_pages,
        "usage_notice_snippets": notices,
        "extraction_tool": "pypdf",
        "verification_status": "MACHINE_OBSERVED",
    }


def main(raw_dir, interim_dir, keywords):
    raw, interim = Path(raw_dir), Path(interim_dir)
    interim.mkdir(parents=True, exist_ok=True)
    for pdf in sorted(raw.glob("*.pdf")):
        try:
            result = extract(pdf, interim / "text", keywords)
        except Exception as err:
            result = {"doc_id": pdf.name.split("__", 1)[0], "local_file_path": pdf.as_posix(),
                      "extraction_error": f"{type(err).__name__}: {err}"}
        out = interim / f"{result['doc_id']}.pdf_metadata.json"
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{result['doc_id']:16} pages={result.get('page_count')} chars={result.get('extracted_chars_total')} "
              f"kw={ {k: len(v) for k, v in result.get('keyword_pages', {}).items()} } "
              f"notices={len(result.get('usage_notice_snippets', []))} {result.get('extraction_error', '')}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
