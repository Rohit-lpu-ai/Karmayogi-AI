# NSSTA Source Audit

**Audit ID:** AUDIT-NSSTA-001
**Source ID:** SRC-025
**Subject:** National Statistical Systems Training Academy (NSSTA), MoSPI — Documents and Offerings pages
**Collection date:** 2026-09-14
**Method:** Targeted HTTP GET/HEAD against named public pages and candidate document URLs. No crawling, no bulk download.
**Personal data collected:** **None.**

---

## 1. Bottom line

Six NSSTA PDFs are confirmed live and downloadable. **Everything else the audit was
asked to find is `UNKNOWN`**, for one structural reason:

> **Both `nssta.gov.in` and `mospi.gov.in` are client-side-rendered single-page
> applications.** They return a 1–2.7 KB HTML shell with no content and no links
> to any client that does not execute JavaScript.

So the Offerings page and the Documents page both *exist* and both return HTTP 200 —
and both are empty as far as any non-browser client is concerned. Training
categories, programme names, and subject areas could not be read. They have been
recorded as `UNKNOWN` rather than guessed.

### Goals scorecard

| Goal | Result | Status |
|---|---|---|
| Training categories | None readable | `UNKNOWN` |
| Programme names | None readable first-hand | `UNKNOWN` (3 secondhand leads) |
| Subject areas | None readable | `UNKNOWN` |
| TPAC-related documents | No TPAC-titled document found | `UNKNOWN` |
| Downloadable PDFs | **6 confirmed live** | `MACHINE_OBSERVED` |
| Structured APIs | None documented | `UNKNOWN` |

---

## 2. Status vocabulary used

This audit needed two statuses the project did not yet have, because "an AI made an
HTTP request and read the response header" is genuinely stronger than `UNKNOWN` and
genuinely weaker than `VERIFIED`.

| Status | Meaning |
|---|---|
| `MACHINE_OBSERVED` | Directly observed by an automated request here, with method and timestamp. **Not** `VERIFIED` — a human has not confirmed it. |
| `UNVERIFIED_SECONDHAND` | Reported by a search-engine summary, not seen at the source. A lead, not a fact. |
| `UNKNOWN` | Not established. Not guessed. |
| `UNAVAILABLE` | Confirmed not retrievable, reason recorded. |
| `EXCLUDED_BY_POLICY` | Found, deliberately not collected, on privacy grounds. |

**Nothing in this audit is `VERIFIED`.** Per `STATUS_VOCABULARY.md`, only a human
may set that, and no human has reviewed these findings yet.

---

## 3. Privacy finding — requires action

`https://nssta.attendance.gov.in/` is live and, unlike the other hosts, is **fully
server-rendered** (32,879 bytes of real HTML).

Page title: `Dashboard | Attendance | National Statistical System Training Academy  - MoSPI`

This is an attendance system. It concerns identifiable individuals. **The audit
stopped at the page title** — no content was read, stored, or transcribed, and no
links from it were followed.

**Action required:** add this host, and any other attendance or participant-facing
system, to a permanent exclusion list. It is exactly the kind of host that a broad
crawl of `*.gov.in` would hoover up without anyone noticing.

---

## 4. Pages audited

| Source URL | Page title | HTTP | Bytes | Access status | Links found |
|---|---|---|---|---|---|
| `https://nssta.gov.in/` | NSSTA | 200 | 1,048 | Reachable but empty | 0 |
| `https://nssta.gov.in/offerings` | NSSTA | 200 | — | Reachable but empty | 0 |
| `https://nssta.gov.in/documents` | NSSTA | 200 | — | Reachable but empty | 0 |
| `https://mospi.gov.in/training` | Ministry of Statistics and Program Implementation \| Government Of India | 200 | 2,657 | Reachable but empty | 3 (assets only) |
| `https://www.mospi.gov.in/NSSTA` | Ministry of Statistics and Program Implementation \| Government Of India | 200 | 2,657 | Reachable but empty | 0 |
| `https://datainnovation.mospi.gov.in/mospi-mcp` | DI Lab | 200 | 745 | Reachable but empty | 0 |
| `https://nssta.attendance.gov.in/` | Dashboard \| Attendance \| NSSTA - MoSPI | 200 | 32,879 | **Excluded by policy** | not examined |

The only links present anywhere in served HTML were on `/training`:
`/assets/index-DpcmNdVB.css`, `/favicon.ico`, and a Google Fonts stylesheet. That
Vite-style asset hash is what confirms the SPA diagnosis.

---

## 5. Unreachable or superseded

| URL / host | Status | Reason |
|---|---|---|
| `training.niip.gov.in` | `UNAVAILABLE` | DNS failure (`ENOTFOUND`). Indexed by search engines but does not resolve. |
| `mospi.nic.in` | `UNAVAILABLE` | DNS failure (`ENOTFOUND`). Legacy domain, superseded by `mospi.gov.in`. |
| `new.mospi.gov.in/.../OM_dated_29.09.2025_...pdf` | `UNAVAILABLE` | No HTTP response at all. Indexed as an NSSTA Office Memorandum with a metadata sheet — worth a human retry from another network. |
| `mospi.gov.in/documents/213904/0/Training+Calendar...` | `UNAVAILABLE` | Returns the SPA shell (`text/html`, 2,657 bytes), not a PDF. Legacy Liferay URL. Same document is live at the `/sites/default/files/` path. |
| `www.mospi.gov.in/robots.txt` | `UNKNOWN` | Connection timed out after 25s. **Blocking gap.** |

---

## 6. Downloadable documents — 6 confirmed

All six returned HTTP 200 with `Content-Type: application/pdf`. Sizes and
modification dates are as reported by the server on 2026-09-14.

| ID | Document | Type | Size | Last modified |
|---|---|---|---|---|
| NSSTA-DOC-001 | Advance Training Calendar FY 2025-26 | Training calendar / circular | 317 KB | 2025-04-24 |
| NSSTA-DOC-002 | Training Calendar FY 2021-22 | Training calendar | 508 KB | 2022-10-17 |
| NSSTA-DOC-003 | Training Calendar FY 2020-21 | Training calendar | 1,197 KB | 2020-06-18 |
| NSSTA-DOC-004 | About NSSTA | Institutional profile | 351 KB | 2016-11-09 |
| NSSTA-DOC-005 | Reference Manual for ISS Probationary Training | Reference manual / curriculum | 1,246 KB | 2018-08-08 |
| NSSTA-DOC-006 | Draft Revised National Policy on Official Statistics | Policy (draft) | 366 KB | 2023-08-10 |

Full URLs: see `nssta_document_urls.txt`.

**Document titles are `UNVERIFIED_SECONDHAND`** — they come from search-engine
result titles, not from the PDFs themselves. Filenames, sizes, dates, and content
types are `MACHINE_OBSERVED`.

Two documents matter most for the platform:

- **NSSTA-DOC-001** is the most recent and should carry the current programme list.
- **NSSTA-DOC-005** is a probationary training reference manual — the closest thing
  found to a formal syllabus, and the best candidate for curriculum structure.

**NSSTA-DOC-006 is a DRAFT** policy. It must never be taught as settled policy.

---

## 7. Why content could not be extracted

NSSTA-DOC-001 was downloaded to a scratch directory (not into the repository) and
an extraction was attempted. It failed:

- The PDF uses **embedded subset fonts with no recoverable ToUnicode mapping**, so
  raw stream decoding yields glyph indices, not text. The only readable ASCII in
  130 KB of decoded streams was font and certificate boilerplate.
- **No PDF tooling is installed** — `poppler` (pdftoppm), `pypdf`, `PyPDF2`, and
  `PyMuPDF` are all absent.
- `WebFetch` against `mospi.gov.in` fails consistently with `Socket is closed`,
  across five attempts and three URLs, while `curl` against the same host succeeds.
  The host appears to reject that particular fetcher.

This is a tooling gap, not a dead end. A human opening the PDF in any browser
resolves it in minutes.

---

## 8. Structured APIs

**No documented public API was found** for NSSTA training data, programmes, or documents.

Two things follow:

1. Both portals are SPAs, which means **an undocumented JSON backend almost
   certainly exists** behind them. It was **deliberately not probed.** Per
   `API_REQUIREMENTS.md` §3, an undocumented endpoint is not a contract, and using
   one is not authorised. Reverse-engineering a government portal's internal API is
   a decision for a human to take explicitly, not a shortcut for an audit to take
   quietly.
2. `https://datainnovation.mospi.gov.in/mospi-mcp` surfaced during the API search.
   The name suggests a MoSPI Model Context Protocol offering. Its page is also an
   empty shell, so **what it actually is remains `UNKNOWN`** — but if MoSPI
   publishes a documented MCP server or API, it changes the integration strategy
   for this whole project. **Highest-value follow-up in this audit.**

---

## 9. Blocking gaps

| Gap | Status | Blocks |
|---|---|---|
| Licence / terms of use for NSSTA and MoSPI content never located | `UNKNOWN` | Gate B4, Gate C, and the entire question of whether we may re-serve this material to learners |
| `robots.txt` not read | `UNKNOWN` | Any further automated access |
| PDF content unread | `UNAVAILABLE` | Categories, programme names, subject areas, TPAC |

The licence gap is the serious one. Six confirmed PDF URLs are worth very little
until someone establishes we are permitted to use their contents in a platform.

---

## 10. Next actions

| Priority | Action | Owner |
|---|---|---|
| **P1** | A human opens NSSTA-DOC-001 in a browser and transcribes programme names, categories, and target groups. Unblocks three of six goals. | UNASSIGNED |
| **P1** | Read `mospi.gov.in` robots.txt and terms of use. Blocking for Gate B4/C. | UNASSIGNED |
| **P1** | Add `nssta.attendance.gov.in` to a permanent exclusion list. | UNASSIGNED |
| P2 | Investigate `datainnovation.mospi.gov.in/mospi-mcp` with a browser. | UNASSIGNED |
| P2 | Install PDF tooling so document audits become reproducible. | UNASSIGNED |
| P2 | Retry the 29.09.2025 Office Memorandum from another network. | UNASSIGNED |
| P3 | Decide explicitly whether JS-rendered fetching of the Offerings and Documents pages is acceptable. It is a materially different access posture and deserves a decision, not a default. | UNASSIGNED |

---

## 11. Sign-off

| Role | Name | Date |
|---|---|---|
| Auditor | AI assistant — findings are `MACHINE_OBSERVED`, **not** `VERIFIED` | 2026-09-14 |
| Human reviewer | UNASSIGNED | — |

Gate B complete: **No.** Gate C signed: **No.**

---

## Sources

- [NSSTA](https://nssta.gov.in/)
- [NSSTA — Offerings](https://nssta.gov.in/offerings)
- [MoSPI — Training](https://mospi.gov.in/training)
- [MoSPI — NSSTA](https://www.mospi.gov.in/NSSTA)
- [MoSPI DI Lab — MCP](https://datainnovation.mospi.gov.in/mospi-mcp)
- [NSSTA Attendance portal](https://nssta.attendance.gov.in/) — excluded on privacy grounds
- [NSSTA Advance Training Calendar FY 2025-26](https://mospi.gov.in/sites/default/files/announcements/Circular_NSSTA_Advance_Training_Calander_FY\(25-26\).pdf)
- [Training Calendar FY 2021-22](https://mospi.gov.in/sites/default/files/main_menu/training/Training%20Calendar%20of%20NSSTA%20for%20FY%202021-22.pdf)
- [Training Calendar FY 2020-21](https://mospi.gov.in/sites/default/files/main_menu/training/TrainingCalenderNSSTA2020-21.pdf)
- [About NSSTA](https://mospi.gov.in/sites/default/files/content_image/\(1\)%20About%20NSSTA.pdf)
- [Reference Manual for ISS Probationary Training](https://mospi.gov.in/sites/default/files/announcements/refdoc_nsc_nssta_final_8aug18.pdf)
- [Draft Revised National Policy on Official Statistics](https://mospi.gov.in/sites/default/files/announcements/Draft_Revised_NPOS.pdf)
