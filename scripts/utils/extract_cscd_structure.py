"""Extract the structure of the DoPT Civil Services Competency Dictionary.

Deliberately limited by the DoPT Copyright Policy ("Contents of this website
may not be reproduced partially or fully, without due permission"): this
records only competency identifiers, names, cluster membership, page
references and proficiency-level labels. It does NOT store definitions or
behavioural indicators; those stay in the official PDF, referenced by page.

Usage:
    python scripts/utils/extract_cscd_structure.py TEXT_FILE SIDECAR_JSON OUT_JSON
"""

import json
import re
import sys
from pathlib import Path

CONTENTS_PAGE = 7      # 1-based page holding the table of contents
FRAMEWORK_PAGE = 11    # 1-based page holding the framework diagram
CLUSTER_RE = re.compile(r"^\s*([1-4])\.\s+(ethos|ethics|equity|efficiency)\s*\|\s*(\d+)", re.I | re.M)
ITEM_RE = re.compile(r"^\s*([1-4]\.\d{1,2})\s+(.+?)\s*\|\s*(\d+)\s*$", re.M)
FRAMEWORK_ITEM_RE = re.compile(r"([1-4]\.\d{1,2})\s+(.+?)(?=\s+[1-4]\.\d{1,2}\s|\s+(?:ethics|equity|efficiency)\b|\s+1 2 3 4|$)", re.I)
LEVEL_RE = re.compile(r"\bLevel\s+([1-9])\s*:")
# A descriptive level name counts only if printed beside a level label
# (a bare "expert" elsewhere in prose is unrelated).
LEVEL_NAME_RE = re.compile(r"(?i)\bLevel\s*[1-9]\s*[:\-–]?\s*\(?\s*(beginner|basic|intermediate|advanced|expert|master)\b")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main(text_file, sidecar_json, out_json):
    pages = Path(text_file).read_text(encoding="utf-8").split("\f")
    sidecar = json.loads(Path(sidecar_json).read_text(encoding="utf-8"))
    contents = pages[CONTENTS_PAGE - 1]
    framework = norm(pages[FRAMEWORK_PAGE - 1])

    clusters = {m.group(1): {"cluster_id": m.group(1), "cluster_name": m.group(2).capitalize(),
                             "start_page": int(m.group(3)), "competencies": []}
                for m in CLUSTER_RE.finditer(contents)}
    framework_names = {m.group(1): norm(m.group(2)) for m in FRAMEWORK_ITEM_RE.finditer(framework)}

    items = sorted(ITEM_RE.finditer(contents), key=lambda m: [int(x) for x in m.group(1).split(".")])
    issues = []
    for m in items:
        cid, name, page_no = m.group(1), norm(m.group(2)), int(m.group(3))
        page_text = pages[page_no - 1] if page_no <= len(pages) else ""
        heading_found = cid in page_text
        levels = sorted({int(x) for x in LEVEL_RE.findall(page_text)})
        if not heading_found:
            issues.append(f"{cid}: identifier not found on page {page_no}")
        if levels != [1, 2, 3, 4, 5]:
            issues.append(f"{cid}: proficiency level labels in the PDF text layer on page {page_no} = {levels}; "
                          "whether the page itself omits a level is UNKNOWN - check the rendered page")
        entry = {
            "competency_id": cid,
            "competency_name": name,
            "name_as_printed_in_framework_page": framework_names.get(cid, "UNKNOWN"),
            "definition": "NOT EXTRACTED - DoPT copyright policy; see definition_reference",
            "definition_reference": {"page": 12 if cid.startswith(("1.", "2.", "3.")) else 13,
                                     "note": "Competency Definitions table (pages 12-13)"},
            "detail_page": page_no,
            "proficiency_levels_observed": [f"Level {n}" for n in levels],
            "behavioural_indicators": f"NOT EXTRACTED - DoPT copyright policy; see page {page_no}",
        }
        clusters[cid.split(".")[0]]["competencies"].append(entry)

    all_text = "\n".join(pages)
    out = {
        "dataset": "Civil Services Competency Dictionary - structure only",
        "source_doc_id": sidecar["doc_id"],
        "document_title": "Civil Services Competency Dictionary (GoI-UNDP Project: Strengthening Human Resource Management of Civil Service)",
        "document_title_status": "MACHINE_OBSERVED (cover page text)",
        "source_url": sidecar["source_url"],
        "discovery_page": "https://dopt.gov.in/tool-kit-competency-dictionary-civil-services-officers",
        "source_organisation": sidecar["source_organisation"],
        "collaborator_named_in_document": "United Nations Development Programme (UNDP)",
        "publication_date": "2014-02-26",
        "publication_date_status": "MACHINE_OBSERVED (date on the foreword message, page 4; formal imprint date UNKNOWN)",
        "retrieval_date": sidecar["retrieval_date"],
        "local_file_path": sidecar["local_file_path"],
        "source_sha256": sidecar["sha256"],
        "access_method": sidecar["access_method"],
        "status": "MACHINE_OBSERVED",
        "licence_usage_notes": sidecar["licence_usage_notes"],
        "extraction_scope": "Names, identifiers, clusters, page references and proficiency-level labels only. No definitions, behavioural indicators, or other prose were copied.",
        "counts": {
            "clusters": len(clusters),
            "competencies": sum(len(c["competencies"]) for c in clusters.values()),
            "detail_pages_with_levels_1_to_5_in_text": sum(
                len(c["proficiency_levels_observed"]) == 5 for cl in clusters.values() for c in cl["competencies"]),
        },
        "proficiency_level_names": ("Only numeric labels 'Level 1'..'Level 5' appear in the document; "
                                     "descriptive names (e.g. 'Beginner'..'Expert') reported by third-party summaries "
                                     + ("were NOT found next to any level label." if not LEVEL_NAME_RE.search(all_text)
                                        else "appear next to level labels - check manually.")),
        "clusters": list(clusters.values()),
        "extraction_issues": issues,
        "personal_data": "None extracted. Foreword signatories' names were not recorded.",
        "human_verification": {
            "verified": False, "verified_by": None, "verified_on": None,
            "names_checked_against_pdf": None,
            "permission_from_dopt_for_reuse_of_definitions": None,
            "notes": None,
        },
    }
    Path(out_json).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"clusters={out['counts']['clusters']} competencies={out['counts']['competencies']} issues={len(issues)}")
    for i in issues:
        print("  ISSUE", i)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
