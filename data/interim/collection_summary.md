# Collection Summary — MVP Data Collection

**Run date:** 2026-09-14
**Scope:** The five MVP data categories only. The 24-source statistical audit and broad statistical APIs were explicitly out of scope.
**Authorisation:** Controlled collection directed by the project owner on 2026-09-14. Public file URLs only. No authentication, no crawling, no undocumented endpoints.
**Verification:** **Nothing is `VERIFIED`.** Every item has an empty `human_verification` block awaiting review.

Full report: [`docs/DATA_COLLECTION_RESULTS.md`](../../docs/DATA_COLLECTION_RESULTS.md)

---

## At a glance

| Category | Items | Downloaded | Link only | Size | Structured output |
|---|---|---|---|---|---|
| 1. NSSTA programmes & offerings | 6 docs + 1 link | 6 | 1 | 3.6 MB | 99 programmes (FY 2025-26) |
| 2. NSSTA TPAC-related | (within NSSTA docs) | — | — | — | 16 page-referenced mentions |
| 3. MoSPI learning / reference | 12 | 12 | 0 | 23.8 MB | Document metadata |
| 4. Competency framework (CSCD) | 1 doc + 2 links | 1 | 2 | 2.0 MB | 4 clusters, 25 competencies (names only) |
| 5. iGOT | — | — | — | — | Mock client only; real API `UNKNOWN` |
| **Total** | **22** | **19** | **3** | **29.4 MB** | |

---

## Files

| File | Contents |
|---|---|
| `nssta_metadata.json` | 7 NSSTA items with all required fields |
| `mospi_metadata.json` | 12 MoSPI items with all required fields |
| `cscd_metadata.json` | 3 CSCD items (1 downloaded, 2 links) |
| `nssta/programmes_fy2025_26.json` | Programme-level metadata parsed from the FY 2025-26 calendar |
| `nssta/tpac_references.json` | TPAC mentions: document, page, ≤220-character context |
| `nssta/collection_log.json`, `mospi/…`, `cscd/…` | Download run logs |
| `*/<doc_id>.pdf_metadata.json` | Page count, PDF info, keyword pages, usage-notice scan |
| `cscd/competency_structure.json` | CSCD clusters, names, page references, level labels. **No definitions.** |
| `*/text/*.txt` | Extracted text. **Git-ignored and local only**, never committed. |

Raw PDFs are in `data/raw/{nssta,mospi,cscd}/`. The PDFs are **git-ignored**. Their `.meta.json` provenance sidecars are tracked.

---

## Status of every item

### NSSTA (`SRC-025`)
| ID | Title | Status | Pages | Text layer |
|---|---|---|---|---|
| NSSTA-DOC-001 | Advance Training Calendar FY 2025-26 | DOWNLOADED | 9 | yes |
| NSSTA-DOC-002 | Training Calendar FY 2021-22 | DOWNLOADED | 29 | yes |
| NSSTA-DOC-003 | Training Calendar FY 2020-21 | DOWNLOADED | 26 | yes |
| NSSTA-DOC-004 | About NSSTA | DOWNLOADED | 2 | **no (scanned)** |
| NSSTA-DOC-005 | Reference Manual for ISS Probationary Training | DOWNLOADED | 56 | yes |
| NSSTA-DOC-006 | NSSTA Office Memorandum dated 29.09.2025 with metadata sheet | DOWNLOADED | 3 | **no (scanned)** |
| NSSTA-LINK-001 | MoSPI RTI proactive disclosure compendium (28.06.2024) | LINK ONLY | — | — |

### MoSPI (`SRC-001`)
| ID | Title | Topic | Pages |
|---|---|---|---|
| MOSPI-DOC-001 | Note on Sample Design and Estimation Procedure: NSS 76th Round | survey design, sampling | 125 |
| MOSPI-DOC-002 | Instructions to Field Staff (HCES) Vol I | survey design | 234 |
| MOSPI-DOC-004 | National Accounts Statistics: Sources and Methods (2012) | national accounts | 353 |
| MOSPI-DOC-006 | FAQ on GDP (26 Feb 2026) | national accounts | 11 |
| MOSPI-DOC-008 | FAQs on CPI 2024 Series | price statistics | 7 |
| MOSPI-DOC-012 | Expert Group Report on Comprehensive Updation of CPI | price statistics | 258 |
| MOSPI-DOC-013 | PLFS — changes in 2025 | labour statistics, sampling | 51 |
| MOSPI-DOC-015 | NMDS 2.0 metadata — PLFS | labour statistics, data quality | 11 |
| MOSPI-DOC-016 | Report of the NSC Committee on PLFS | labour statistics, survey design | 82 |
| MOSPI-DOC-026 | SDG National Indicator Framework, 2026 (with metadata) | SDG indicators | 166 |
| MOSPI-DOC-029 | National Metadata Structure NMDS 2.0 | data quality, metadata | 31 |
| MOSPI-DOC-031 | Statistical Quality Assessment Framework (SQAF) Guidelines | data quality | 30 |

All 12 downloaded and all have a text layer.

### CSCD (`SRC-026`)
| ID | Title | Status |
|---|---|---|
| CSCD-DOC-001 | Civil Services Competency Dictionary (DoPT, GoI-UNDP) | DOWNLOADED — local reference copy only |
| CSCD-LINK-001 | Implementation Tool-kit | LINK ONLY (live) |
| CSCD-LINK-002 | DoPT Training Division FRAC page | LINK ONLY (**host unreachable**) |

### iGOT
No collection. The real API stays **`UNKNOWN`** (no documented public or partner API) and its portals are **`UNAVAILABLE`** from this environment. `clients/mock_igot_client.py` is the only client, and every record it returns is `MOCK`. Tests pass (14/14). See `IGOT_ACCESS_STATUS.md`.

---

## Needs a human

1. **Licences.**
   - DoPT prohibits reproduction without permission (read first-hand).
   - MoSPI/NSSTA terms are still only secondhand.
   - None of the 17 PDFs with a text layer contains a usage notice.
2. **Two scanned PDFs** (NSSTA-DOC-004, -006) need OCR or a human read.
3. **Spot-check the programmes parse** against the calendar PDF.
4. **CSCD page 34** ("Problem Solving"): only Levels 1–4 are in the text layer. Check the rendered page.
5. **NSSTA-LINK-001:** a human reviews it in a browser and notes TPAC references only.
