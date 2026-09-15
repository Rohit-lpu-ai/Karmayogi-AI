"""Parse programme-level metadata from the NSSTA Advance Training Calendar FY 2025-26.

Input is the pypdf text extracted by extract_pdf_metadata.py. The calendar is
a table (Week | Training Programme | Duration (days) | Topic | Participants |
Batch size | Venue) whose cells wrap across lines and whose week labels are
detached from rows, so:
- rows are anchored on the programme types observed in this document,
- week/date is NOT assigned to rows (not reliably recoverable),
- repeated weekly rows are collapsed into one programme with an occurrence count,
- anything that does not parse cleanly is kept verbatim for human review.

Only programme-level fields are produced. Participants are cadre groups
(e.g. "SSOs", "ISS (P)- 47th Batch (2025)"), not individuals.

Usage:
    python scripts/utils/parse_nssta_calendar.py TEXT_FILE SIDECAR_JSON OUT_JSON
"""

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

PROGRAMME_TYPES = [
    r"ISS \(P\)\s*-\s*\d+th Batch \(\d{4}\)",
    r"SSS Induction Training Programme",
    r"SSS in-Service Training Programme",
    r"DES Training Programme",
    r"MCTP Phase \d+ Stage\s*-\s*I{1,3}",
    r"ISEC, \d+th Term",
    r"ISEC Five-day Workshop",
    r"UN SIAP",
    r"Webinar",
    r"Workshop",
    r"DSTP",
    r"DBTP",
    r"Awareness Progamme for HOD/ Faculty of [A-Za-z/ ]+? Dept",  # sic: "Progamme" as printed
    r"PG & UG University Exposure Training Programme",
    r"Seminar \(Foundation day\)",
]
TYPE_RE = "(?:" + "|".join(PROGRAMME_TYPES) + ")"
WEEK_PREFIX = r"(?:\d+ \([^)]*\) )?"
START_RE = re.compile(rf"^{WEEK_PREFIX}({TYPE_RE}) \d{{1,3}} ")
# Programme-type cells that wrap: their first line alone starts a new row.
WRAPPED_TYPE_START_RE = re.compile(r"^(Awareness Progamme for HOD/ Faculty|PG & UG University Exposure Training)$")
ROW_RE = re.compile(rf"^{WEEK_PREFIX}(?P<ptype>{TYPE_RE}) (?P<days>\d{{1,3}}) (?P<rest>.+) (?P<batch>\d{{1,3}}(?:-\d{{1,3}})?|TBD)(?: (?P<venue>.*))?$")

PARTICIPANT_GROUPS = [
    r"ISS \(P\)\s*-\s*\d+th Batch \(\d{4}\)",
    r"In-Service ISS Officers",
    r"ISS officers with [\d\s-]+years(?: of service)?",
    r"ISS/SSS Officers",
    r"State DES Officers / International",
    r"DES Officers / International",
    r"DES Officers",
    r"SSOs",
    r"JSOs",
    r"University Students",
    r"International Participants",
    r"HOD/ Faculty of [A-Za-z/ ]+ dept",
    r"PG/ UG Students of [A-Za-z/ ]+",
    r"MoSPI/Line Ministries/State.*",
    r"Others",
]
PARTICIPANT_RE = re.compile(r"^(?P<topic>.+?) (?P<participants>" + "|".join(PARTICIPANT_GROUPS) + r")$")

# Week labels such as "29 (Oct 13 - Oct 17)" sometimes land inside a row.
WEEK_LABEL_RE = re.compile(r"(?<=\s)\d{1,2} \([A-Za-z]{3,4}\s*\d{1,2}\s*-\s*(?:[A-Za-z]{3,4}\s*)?\d{1,2}\)")

SKIP_RE = re.compile(
    r"^(Week Training Programme Duration|\(In Days\) Topic Participants Batch|Size Venue / Institute|"
    r"\(Tentative\)|\d+ \([^)]*\)$|\d+ \([A-Za-z]+\s*\d*\s*$|-\s*[A-Za-z]+\s*\d+\)$)"
)


def norm(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    return re.sub(r"ISS \(P\)\s*-\s*(\d+th)", r"ISS (P)-\1", s)


def blocks(text):
    current = None
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or SKIP_RE.match(line) or "NSSTA - Advance Training Calendar" in line:
            continue
        if START_RE.match(line) or WRAPPED_TYPE_START_RE.match(line):
            if current:
                yield current
            current = [line]
        elif current is not None:
            current.append(line)
    if current:
        yield current


def parse(text):
    programmes = OrderedDict()
    unparsed = []
    for block in blocks(text):
        joined = norm(WEEK_LABEL_RE.sub(" ", " ".join(block)))
        m = ROW_RE.match(joined)
        if not m:
            unparsed.append(joined)
            continue
        rest = m.group("rest")
        pm = PARTICIPANT_RE.match(rest)
        topic = norm(pm.group("topic")) if pm else rest
        participants = norm(pm.group("participants")) if pm else "UNKNOWN"
        row = {
            "programme_type": norm(m.group("ptype")),
            "topic": topic,
            "participant_group": participants,
            "duration_days_per_occurrence": int(m.group("days")),
            "batch_size": m.group("batch"),
            "venue": norm(m.group("venue")) or "UNKNOWN",
            "parse_confidence": "medium" if pm else "low",
        }
        key = tuple(row[k] for k in ("programme_type", "topic", "participant_group", "venue"))
        if key in programmes:
            programmes[key]["occurrences_listed"] += 1
            programmes[key]["total_days_listed"] += row["duration_days_per_occurrence"]
        else:
            programmes[key] = {**row, "occurrences_listed": 1,
                               "total_days_listed": row["duration_days_per_occurrence"]}
    return list(programmes.values()), unparsed


def main(text_file, sidecar_json, out_json):
    text = Path(text_file).read_text(encoding="utf-8")
    sidecar = json.loads(Path(sidecar_json).read_text(encoding="utf-8"))
    programmes, unparsed = parse(text)
    for i, p in enumerate(programmes, 1):
        p["programme_id"] = f"NSSTA-FY2526-P{i:03d}"

    by_type = OrderedDict()
    for p in programmes:
        by_type.setdefault(p["programme_type"], 0)
        by_type[p["programme_type"]] += 1

    out = {
        "dataset": "NSSTA programme-level metadata - Advance Training Calendar FY 2025-26",
        "source_doc_id": sidecar["doc_id"],
        "source_url": sidecar["source_url"],
        "source_organisation": sidecar["source_organisation"],
        "retrieval_date": sidecar["retrieval_date"],
        "local_file_path": sidecar["local_file_path"],
        "source_sha256": sidecar["sha256"],
        "access_method": sidecar["access_method"],
        "extraction_method": "pypdf text extraction + rule-based table parsing (scripts/utils/parse_nssta_calendar.py)",
        "status": "MACHINE_OBSERVED",
        "calendar_status_in_source": "Tentative (the calendar marks itself '(Tentative)')",
        "licence_usage_notes": sidecar["licence_usage_notes"],
        "personal_data": "None extracted. Participant fields are cadre/group names, not individuals.",
        "known_limitations": [
            "Week/date per programme is not assigned: week labels are detached from rows in the extracted text.",
            "Topic/participant split is rule-based; parse_confidence 'low' means the split failed and topic holds both.",
            "Rows whose text did not match the table pattern are listed in unparsed_rows for human review.",
            "Programme-type codes (DSTP, DBTP, MCTP, ISEC, UN SIAP) are not expanded here; expansions are UNKNOWN until read from an official source.",
        ],
        "counts": {
            "distinct_programmes": len(programmes),
            "unparsed_rows": len(unparsed),
            "programmes_by_type": by_type,
        },
        "programmes": programmes,
        "unparsed_rows": unparsed,
        "human_verification": {
            "verified": False, "verified_by": None, "verified_on": None,
            "sample_rows_checked_against_pdf": None, "notes": None,
        },
    }
    Path(out_json).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"programmes={len(programmes)} unparsed={len(unparsed)}")
    for t, n in by_type.items():
        print(f"  {n:3} {t}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
