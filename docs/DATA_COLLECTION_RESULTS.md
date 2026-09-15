# Data Collection Results — SIH MVP

**Run date:** 2026-09-14
**Phase:** First real data collection (discovery phase has finished)
**Scope:** Five MVP data categories only
**Short inventory:** [`data/interim/collection_summary.md`](../data/interim/collection_summary.md)

> **Nothing in this collection is `VERIFIED`.** Facts observed by scripts are `MACHINE_OBSERVED`. Facts taken from search engines are `UNVERIFIED_SECONDHAND`. Every item has an empty `human_verification` block for a reviewer. Only a human may set `VERIFIED` (see `STATUS_VOCABULARY.md`).

---

## 1. Outcome

| # | MVP category | Result | Headline |
|---|---|---|---|
| 1 | NSSTA training programmes & offerings | ✅ Collected | 6 official PDFs; **99 distinct programmes** parsed from the FY 2025-26 calendar |
| 2 | NSSTA TPAC-related documents | ⚠️ Partial | No standalone TPAC document is public. **16 TPAC references** found inside 3 collected documents. 1 candidate link held back for privacy |
| 3 | MoSPI learning / reference documents | ✅ Collected | **12 documents** across all 7 priority topics |
| 4 | Competency framework (CSCD) | ✅ Located and structured | Official DoPT URL confirmed; **4 clusters / 25 competencies**; definitions **not** extracted (DoPT copyright policy) |
| 5 | iGOT API status + mock | ✅ Confirmed | Real API `UNKNOWN`; mock client only; 14/14 tests pass |

**Totals:** 22 items, of which 19 were downloaded (29.4 MB) and 3 were recorded as links only. No personal data was collected. No credentials were used. No undocumented endpoint was called.

---

## 2. How collection was controlled

| Control | Implementation |
|---|---|
| Explicit item lists | Every download is listed in a reviewed manifest: `scripts/collectors/manifests/{nssta,mospi,cscd}.json`. No link-following, no crawling. |
| Host allow-list | Only `mospi.gov.in`, `www.mospi.gov.in` and `dopt.gov.in`. |
| File checks | Content type must be PDF, the body must start with `%PDF-`, and files are capped at 25 MB (10 MB for DoPT). |
| Politeness | 2 s between requests, and an identifying User-Agent. |
| Provenance | Every file has a `.meta.json` sidecar: URL, retrieval time (UTC), HTTP headers, SHA-256, byte count, access method, licence notes, authorisation. |
| Idempotence | Re-running skips files whose sidecar checksum matches, so nothing is downloaded twice. |
| Source control | PDFs and extracted text are git-ignored. Sidecars and interim metadata are tracked. `.gitignore` was fixed so that the exceptions for sidecar files work inside subdirectories. |

Tooling:
- `scripts/collectors/fetch_documents.py`
- `scripts/utils/extract_pdf_metadata.py`
- `scripts/utils/parse_nssta_calendar.py`
- `scripts/utils/extract_cscd_structure.py`
- `scripts/utils/build_interim_metadata.py`

The `pypdf` library was installed for text extraction.

---

## 3. NSSTA

### 3.1 Documents and Offerings pages

`https://nssta.gov.in/offerings` and `https://nssta.gov.in/documents` were checked again on 2026-09-14. Both return HTTP 200 with a 1,048-byte JavaScript page shell: the title is `NSSTA`, the only text is *"You need to enable JavaScript to run this app"*, and there are **no links**. Status: `MACHINE_OBSERVED`.

The site's hidden JSON backend was **not** probed. That would mean calling an undocumented endpoint (`API_REQUIREMENTS.md` §3). The programme metadata therefore comes from NSSTA's official training calendars, which are published as PDFs on `mospi.gov.in`.

### 3.2 Collected

| ID | Document | Category | Pages | Notes |
|---|---|---|---|---|
| NSSTA-DOC-001 | Advance Training Calendar FY 2025-26 | training_calendar | 9 | The calendar marks itself "(Tentative)" |
| NSSTA-DOC-002 | Training Calendar FY 2021-22 | training_calendar | 29 | Mentions TPAC |
| NSSTA-DOC-003 | Training Calendar FY 2020-21 | training_calendar | 26 | Mentions TPAC |
| NSSTA-DOC-004 | About NSSTA | institutional_profile | 2 | **Scanned; no text layer** |
| NSSTA-DOC-005 | Reference Manual for ISS Probationary Training | curriculum_reference | 56 | TPAC terms of reference; Annexure IV TPAC recommendations |
| NSSTA-DOC-006 | NSSTA Office Memorandum 29.09.2025 with metadata sheet | office_memorandum | 3 | **Scanned.** Now served from `mospi.gov.in/uploads/…`; the old `new.mospi.gov.in` host no longer resolves |

### 3.3 Programme-level metadata

`data/interim/nssta/programmes_fy2025_26.json` holds **99 distinct programmes**. They come from 178 calendar rows; the same programme often repeats across weeks, so repeats were merged and counted.

| Programme type | Distinct programmes |
|---|---|
| ISS probationers (46th and 47th batches) | 49 |
| SSS in-Service Training Programme | 13 |
| DSTP | 6 |
| MCTP (phases 1–3) | 5 |
| UN SIAP | 5 |
| DES Training Programme | 4 |
| DBTP, Webinar | 3 each |
| SSS Induction, Workshop, PG & UG University Exposure | 2 each |
| Awareness Programme (HOD/Faculty, two variants), ISEC Five-day Workshop, ISEC 77th Term, Seminar (Foundation Day) | 1 each |

Fields per programme:
- programme type
- topic
- participant group
- duration in days per occurrence
- batch size
- venue
- occurrences listed and total days
- parse confidence

Quality checks:
- 178 rows parsed, equal to the 178 row starts in the text.
- 0 rows unparsed and 0 low-confidence splits.
- 0 honorific or name matches.

**Personal data:** none. The participant fields are cadre groups (for example "SSOs", "ISS (P)-47th Batch (2025)") and venues are institutions.

**Known limitations:**
- **Week and date are not assigned** to programmes. In the extracted text, the week labels are detached from the rows.
- Rows are anchored on the 15 programme-type patterns seen in this document. A row with an unseen type would be merged into the row before it, and the row-count check cannot detect that.
- Programme codes such as DSTP, DBTP, MCTP, ISEC and UN SIAP are **not expanded**. Their expansions are `UNKNOWN` until read from an official source.
- The older calendars (FY 2020-21, 2021-22) were collected but **not parsed** into programmes.

### 3.4 TPAC

No standalone TPAC minutes, orders, or TPAC-issued document was found online. What exists (`data/interim/nssta/tpac_references.json`, 16 mentions):

| Document | What it says about TPAC (paraphrased) |
|---|---|
| NSSTA-DOC-005 (8 mentions) | TPAC was constituted after NSSTA was established, with terms of reference per an OM dated 2 January 2012. It meets before each financial year to approve the training programmes. Annexure IV lists TPAC recommendations for 2015-16 and 2016-17. |
| NSSTA-DOC-002 (4) | Programmes are designed within TPAC's recommendations. TPAC authorised demand-based programmes and approved Training of Trainers (TOT) programmes for FY 2021-22. |
| NSSTA-DOC-003 (4) | The same approvals for FY 2020-21. The TPAC chair is named by designation. |

**Held back:** `NSSTA-LINK-001`, the MoSPI RTI proactive-disclosure compendium (28.06.2024), was confirmed live (1.1 MB). A search summary says it refers to TPAC minutes. It was **not downloaded**. My reason (`ASSUMED`) is that RTI s.4(1)(b) disclosures must include officer directories and pay, which is personal information. A human should review it in a browser and record only the TPAC references.

---

## 4. MoSPI

Twelve documents were chosen from the 31 confirmed in AUDIT-MOSPI-001. The choice follows the MVP priorities and leaves out the very large files (57.7 MB and 32.7 MB).

| Priority topic | Documents |
|---|---|
| Survey design | DOC-001 NSS 76 sample design note; DOC-002 HCES field instructions; DOC-016 NSC committee report on PLFS |
| Sampling | DOC-001; DOC-013 PLFS changes 2025 |
| National accounts | DOC-004 NAS Sources & Methods; DOC-006 FAQ on GDP (Feb 2026) |
| Price statistics | DOC-008 FAQs on CPI 2024; DOC-012 Expert Group Report on CPI updation |
| Labour statistics | DOC-013; DOC-015 NMDS 2.0 PLFS metadata; DOC-016 |
| Data quality | DOC-031 SQAF Guidelines; DOC-029 NMDS 2.0; DOC-015 |
| SDG indicators | DOC-026 SDG NIF 2026 with metadata |

All 12 were downloaded, and all have extractable text: 1,359 pages in total. The PDF creation dates run from 2010 (the NSC PLFS report) to June 2026 (SDG NIF 2026).

**Teaching caveat:** DOC-004 (2012) describes an older national accounts base. DOC-006 (Feb 2026) is an FAQ on a new GDP series. Tag each document with its series or base year before teaching from it.

**Deferred:** Draft Revised NPOS (a draft), the older CPI 2010 manual (superseded), and the industrial and agricultural documents (not MVP priorities).

---

## 5. CSCD — Civil Services Competency Dictionary

| Field | Value | Status |
|---|---|---|
| Official URL | `https://dopt.gov.in/sites/default/files/Competency%20Dictionary%20for%20the%20Civil%20Services.pdf` | `MACHINE_OBSERVED` |
| Official discovery page | `https://dopt.gov.in/tool-kit-competency-dictionary-civil-services-officers` (server-rendered; links the PDF) | `MACHINE_OBSERVED` |
| Availability | HTTP 200, `application/pdf`, 2,056,035 bytes, Last-Modified 2018-02-19 | `MACHINE_OBSERVED` |
| Cover title | *Civil Services Competency Dictionary — GoI-UNDP Project: Strengthening Human Resource Management of Civil Service* | `MACHINE_OBSERVED` |
| Date | Foreword dated 26 February 2014 (formal imprint date `UNKNOWN`) | `MACHINE_OBSERVED` |
| Usage terms | **DoPT Copyright Policy:** *"Contents of this website may not be reproduced partially or fully, without due permission from the Department of Personnel & Training."* Content referred to must acknowledge its source. | `MACHINE_OBSERVED` (read at `https://dopt.gov.in/website-policies`) |

**Extraction decision.** You asked to extract names, definitions and proficiency information "if permitted". The copyright policy **does not permit** reproduction without permission. So:
- **Extracted:** competency IDs, names, cluster membership, page references, and proficiency-level labels.
- **Not extracted:** definitions and behavioural indicators. Each entry points to the PDF page instead.
- **Not stored:** the foreword signatories' names.
- The PDF is kept **locally only** (git-ignored) as a reference copy.

**Structure (`data/interim/cscd/competency_structure.json`):**

| Cluster | Competencies |
|---|---|
| 1. Ethos (p.14) | People First · Strategic Thinking · Organisational Awareness · Commitment to the Organisation · Leading Others |
| 2. Ethics (p.19) | Integrity · Self-Confidence · Attention to Detail · Taking Accountability |
| 3. Equity (p.23) | Consultation and Consensus Building · Decision Making · Empathy · Delegation |
| 4. Efficiency (p.27) | Result Orientation · Conceptual Thinking · Initiative and Drive · Seeking Information · Planning and Coordination · Desire for Knowledge · Innovative Thinking · Problem Solving · Developing Others · Self-Awareness and Self-Control · Communication Skills · Team-Working |

- **25 competencies in total.** Third-party summaries variously said "12 core" or "25". The document confirms 25.
- **Proficiency levels:** labelled only "Level 1" to "Level 5". The "Beginner to Expert" names from third-party summaries **do not appear** next to any level label.
- 24 of the 25 detail pages have all five level labels in the text layer. **Page 34 (4.8 Problem Solving) shows only Levels 1–4.** Whether the page itself leaves out Level 5 is `UNKNOWN`; check the rendered page.
- Small name variants between the contents page and the framework page are recorded (for example "Result Orientation" and "Results Orientation").

**Related links recorded:**
- *Implementation Tool-kit* PDF: live, 551,841 bytes. Not downloaded (outside scope).
- DoPT Training Division **FRAC** page (`dopttrg.nic.in`): host **unreachable** (`UNAVAILABLE`). FRAC is Mission Karmayogi's Framework of Roles, Activities and Competencies. It is likely more directly relevant to iGOT competency mapping than CSCD, so it is worth a human follow-up.

---

## 6. iGOT

| Item | Status |
|---|---|
| Documented public or partner API | `UNKNOWN`: none found (AUDIT-IGOT-001) |
| iGOT portals from this environment | `UNAVAILABLE`: connections time out |
| Undocumented endpoints called | None |
| Credentials used or stored | None |
| Client in use | `clients/mock_igot_client.py`, `MOCK` only. `IGOT_CLIENT_MODE=live` is refused |
| Mock tests | 14/14 pass (re-run 2026-09-14) |

**Official access information still required** (from `API_REQUIREMENTS.md` §6.4–6.5):
1. Written authorisation or agreement from Karmayogi Bharat.
2. Official API documentation: base URL, authentication flow, rate limits, terms of use.
3. Credentials issued through an official process, stored outside source control.
4. Whether non-personal **course catalogue metadata** can be shared as an API or an export. This is the recommended first request.
5. Whether a UAT or test environment is available to approved partners.
6. The consent model for learner enrolment and completion data, and a documented lawful basis under the DPDP Act, 2023.
7. Whether courses can be filtered by provider (NSSTA/MoSPI) and by competency framework (CSCD/FRAC).

---

## 7. Licence and usage position

| Source | Terms | Status | Consequence |
|---|---|---|---|
| DoPT (CSCD) | Reproduction prohibited without permission; acknowledge the source | `MACHINE_OBSERVED` | Reference and link only. **Ask DoPT for permission** before showing definitions or indicators in the platform. |
| MoSPI / NSSTA | "Reproduction is permitted provided an acknowledgment of the source is made" | `UNVERIFIED_SECONDHAND` | The MoSPI copyright page cannot be read by a script. **A human must read it** before any content is shown to learners. |
| Per-document notices | None found in the 17 PDFs with a text layer. The 2 scanned PDFs could not be checked. | `MACHINE_OBSERVED` | Site-level terms decide the position. |

Until these are confirmed, keep collected PDFs out of source control and do not re-serve their content.

---

## 8. Human review checklist

Set the relevant `human_verification` fields in `data/interim/*_metadata.json` as each check is done:

- [ ] Read the MoSPI copyright policy in a browser and record its exact wording
- [ ] Decide whether to request DoPT permission to reuse CSCD definitions
- [ ] Confirm document titles against `first_page_lines_for_title_check` (titles are currently secondhand for NSSTA and MoSPI)
- [ ] Spot-check ≥10 programmes in `programmes_fy2025_26.json` against the calendar PDF
- [ ] Confirm the expansions of DSTP, DBTP, MCTP, ISEC and UN SIAP from an official source
- [ ] Read NSSTA-DOC-004 and NSSTA-DOC-006 (scanned) and record their key metadata
- [ ] Check CSCD page 34 for Level 5
- [ ] Review NSSTA-LINK-001 in a browser and note TPAC references only
- [ ] Retry the FRAC page from another network
- [ ] Confirm that no personal data is present in any collected file
