# MoSPI Document Audit — Starter Corpus

**Audit ID:** AUDIT-MOSPI-001
**Source ID:** SRC-001 (MoSPI main portal)
**Collection date:** 2026-09-14
**Scope:** A small, high-value starter corpus of official methodology documents across 11 topics. This is not a full inventory of the site.
**Method:** Candidate URLs came from search engine indexes restricted to `mospi.gov.in`. Each one was checked with a HEAD request (1.5 s apart, identifying User-Agent, TLS verified), and no document contents were downloaded.
**Personal data collected:** None. No microdata or unit-level files were selected.

---

## 1. Bottom line

| | |
|---|---|
| Candidates selected | 33 |
| **Confirmed live PDFs** | **31** |
| Dead (HTTP 404) | 1 |
| Unreachable host | 1 |
| Topics covered | 11 of 11 |
| Combined size of live corpus | ~154 MB (161,660,595 bytes) |
| Documents downloaded | **0** |
| Items marked `VERIFIED` | **0** |

All 11 topics have at least one confirmed document. **Sampling** has no document that is mainly about sampling, but four live documents cover it as a secondary topic. The strongest of these is the NSS 76th Round sample design note (DOC-001).

---

## 2. What each field is based on

Each field has its own status, because the evidence behind the fields differs. See `STATUS_VOCABULARY.md`.

| Field | Status | Basis |
|---|---|---|
| URL, HTTP status, content type, size | `MACHINE_OBSERVED` | HEAD request, timestamped |
| Download status | `MACHINE_OBSERVED` | Derived from the status code and content type |
| Server Last-Modified | `MACHINE_OBSERVED` | HTTP header. **This is not a publication date** (see §6) |
| Title | `UNVERIFIED_SECONDHAND` | Search index. Not read from the PDF |
| Organization | `UNVERIFIED_SECONDHAND` | The domain was observed. The issuing unit comes from the indexed title |
| Publication date | `UNVERIFIED_SECONDHAND` or `UNKNOWN` | Only filled in where the filename or title states one. Otherwise `UNKNOWN` |
| Language | `UNVERIFIED_SECONDHAND` | Script of the indexed title. PDF not opened |
| Document type | `ASSUMED` | The auditor's classification from the title |
| Copyright / usage | `UNKNOWN` | No licence information in headers, and PDFs not opened |

Nothing was read from inside a PDF. As a result, **title, language, publication date and copyright are all unconfirmed for every item.** A human opening each PDF can close these gaps quickly.

---

## 3. The corpus

Sizes are rounded. Full URLs are in `mospi_document_urls.txt`, and all fields are in `mospi_document_corpus.json` / `.csv`.

### Survey design & sampling
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-001 | Note on Sample Design and Estimation Procedure: NSS 76th Round | Methodology note | NSS 76th Round | 1.1 MB | ✅ Live |
| DOC-002 | Instructions to Field Staff (HCES) Vol I | Instruction manual | — | 2.0 MB | ✅ Live |
| DOC-003 | Schedule 33.1 Instructions to Field Staff, Vol-1, NSS 77th Round | Instruction manual | NSS 77th Round | 1.5 MB | ✅ Live* |

\* Only works with the commas percent-encoded (`%2C`). The URL as indexed returns 404.

### National accounts
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-004 | National Accounts Statistics: Sources and Methods | Methodology manual | 2012 | 5.0 MB | ✅ Live |
| DOC-005 | Manual on Estimation of State and District Income | Methodology manual | — | 2.4 MB | ✅ Live |
| DOC-006 | FAQ on GDP | FAQ / definitions | 2026-02-26 | 0.1 MB | ✅ Live |
| DOC-007 | National Accounts — Compliance of Metadata | Metadata sheet | — | 0.5 MB | ✅ Live |

### Price statistics
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-008 | FAQs on CPI 2024 Series | FAQ / definitions | — | 0.3 MB | ✅ Live |
| DOC-009 | CPI: Changes in the Revised Series (Base 2012=100) | Methodology note | — | — | ❌ Host unreachable |
| DOC-010 | Manual on Consumer Price Index 2010 | Methodology manual | 2010 | 5.2 MB | ✅ Live |
| DOC-011 | Report of the Committee on Price Statistics | Committee report | — | 0.3 MB | ✅ Live |
| DOC-012 | Expert Group Report on Comprehensive Updation of CPI | Committee report | — | 4.8 MB | ✅ Live |

### Labour statistics
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-013 | PLFS — changes in 2025 | Methodology note | 2025 | 3.4 MB | ✅ Live |
| DOC-014 | PLFS Annual Report 2021-22 | Report | 2021-22 | 32.7 MB | ✅ Live |
| DOC-015 | NMDS 2.0 metadata — PLFS | Metadata sheet | — | 0.2 MB | ✅ Live |
| DOC-016 | Report of the NSC Committee on PLFS | Committee report | — | 2.3 MB | ✅ Live |

### Agricultural statistics
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-017 | Manual on Area and Crop Production Statistics | Methodology manual | 2008-07-23 | 1.4 MB | ✅ Live |
| DOC-018 | Situation Assessment Survey of Agricultural Households | Report | — | **57.7 MB** | ✅ Live |
| DOC-019 | Tabulation Plan, Schedule 33.1, NSS 77th Round | Tabulation plan | 2019-09-26 | 2.0 MB | ✅ Live |

### Industrial statistics
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-020 | Index of Industrial Production with Base 2011-12 — An Overview | Methodology manual | 2018-04-03 | 1.2 MB | ✅ Live |
| DOC-021 | Report of the Working Group for IIP | Committee report | — | 2.8 MB | ✅ Live |
| DOC-022 | IIP Metadata, Base 2011-12 | Metadata sheet | 2017-08-01 | 0.3 MB | ✅ Live |
| DOC-023 | ASI Instruction Manual 2023-24 | Instruction manual | 2023-24 | 3.0 MB | ✅ Live |
| DOC-024 | ASI Instruction Manual 2023-24 (Hindi-titled) | Instruction manual | 2023-24 | 3.0 MB | ✅ Live — see §5 |
| DOC-025 | Know Your Survey — User Guide to the ASI | User guide | — | 0.8 MB | ✅ Live |

### SDG indicators
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-026 | SDG National Indicator Framework, 2026 (with metadata) | Indicator framework | 2026 | 3.2 MB | ✅ Live |
| DOC-027 | SDG NIF Progress Report, 2025 | Report | 2025 | — | ❌ HTTP 404 |
| DOC-028 | SDG National Indicator Framework (Baseline Report) | Report | — | 6.2 MB | ✅ Live |

### Metadata
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-029 | National Metadata Structure NMDS 2.0 | Standard | 2024-12-05 | 0.7 MB | ✅ Live |
| DOC-030 | Data Dissemination: National Metadata Structure (NMDS) | Standard | 2023-12-06 | 0.7 MB | ✅ Live |

### Data quality
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-031 | Statistical Quality Assessment Framework (SQAF) Guidelines | Framework | — | 0.7 MB | ✅ Live |

### Official statistical methodology
| ID | Title (indexed) | Type | Date hint | Size | Status |
|---|---|---|---|---|---|
| DOC-032 | Draft Revised National Policy on Official Statistics | **Policy — DRAFT** | — | 0.3 MB | ✅ Live |
| DOC-033 | Report of the Sub-Committee on Methodological Improvement for the Base [title truncated] | Committee report | — | 8.3 MB | ✅ Live |

---

## 4. Where to start

If a human reads only six of these, this set covers the most ground:

1. **DOC-029 NMDS 2.0.** This is India's national metadata standard, and it applies directly to this project's `DATA_DICTIONARY.md`. We should align with it rather than create our own.
2. **DOC-031 SQAF.** The official data-quality framework, which is the basis for any "data quality" module.
3. **DOC-026 SDG NIF 2026.** The newest document in the corpus (Last-Modified 2026-06-29). It comes with indicator metadata.
4. **DOC-001 NSS 76th Round sample design note.** A short, concrete worked example of stratified two-stage sampling.
5. **DOC-004 NAS Sources and Methods.** The main reference for national accounts methodology.
6. **DOC-023 ASI Instruction Manual 2023-24.** Current concepts and definitions for industrial statistics.

---

## 5. Issues to flag

**Superseded methodology.** DOC-010 (CPI manual 2010) and DOC-009 (CPI 2012 base changes) describe older CPI series. Search results mention a CPI 2024 base series, and DOC-008 is its FAQ. DOC-020/022 describe the IIP 2011-12 base. Whether a newer IIP base exists is `UNKNOWN`. **If older documents are presented as current practice, learners will be taught outdated methods.** Every methodology document needs a "series / base year" tag and a check against the current series before it is taught.

**Draft policy.** DOC-032 is a draft and must never be presented as settled policy.

**Probable duplicate.** DOC-023 and DOC-024 are exactly the same size (3,188,716 bytes) but have different ETags and upload dates. They may be the same file uploaded twice, or a bilingual document indexed under two titles. Whether they are identical is `UNKNOWN` without a content hash. The language of DOC-024 is also `UNKNOWN`: its indexed title is in Devanagari, but that does not show the contents are in Hindi.

**Fragile URLs.** DOC-003 only works when the commas are percent-encoded. DOC-031's filename has a trailing space before `.pdf`. DOC-012 is stored under `/uploads/Marquee/`, a homepage-banner path that may not be kept. Two URL patterns are in use at the same time (`/sites/default/files/…` and `/uploads/…`), which suggests a CMS migration is under way. **Record URLs exactly as observed and recheck them before any retrieval.**

**Large files.** DOC-018 (57.7 MB) and DOC-014 (32.7 MB) make up 59% of the corpus by size. Consider leaving them out of a first retrieval.

**Two failures:**
- DOC-027 returned HTTP 404 for the indexed URL and for an en-dash title variant. The server returned a real 404 page, not the SPA shell, so the file is actually missing. DOC-026 covers the same need.
- DOC-009 is on `cpi.mospi.gov.in`, which refused connections on port 443 (two attempts, with and without `www`). It is `UNAVAILABLE` from this environment and may be reachable from Indian networks.

---

## 6. Publication dates: be careful

**HTTP Last-Modified is not a publication date.** The data shows this directly. Four documents (DOC-004, 005, 010, 017) have Last-Modified values between `2016-07-01 05:40` and `05:43` UTC. That is a bulk upload during a site migration, not four publications within three minutes. DOC-010 is a 2010 manual and DOC-017's filename says 2008, yet both show 2016.

This audit records the two separately:
- `publication_date` is filled in only when the filename or title states a date (`UNVERIFIED_SECONDHAND`). Otherwise it is `UNKNOWN`.
- `server_last_modified` is `MACHINE_OBSERVED` and carries an explicit caveat.

A real publication date needs someone to open the PDF and read its imprint page.

---

## 7. Copyright and usage

| Item | Finding | Status |
|---|---|---|
| Per-document licence | Not in any HTTP response header, including `Content-Disposition`, for any of the 31 files | `UNKNOWN` |
| MoSPI copyright policy page | `https://www.mospi.gov.in/copyrights-policy` exists in the search index, but the site is an SPA and the page content cannot be read by a non-browser client | `UNKNOWN` |
| Reproduction notice | A search summary quotes MoSPI publications as saying: *"Reproduction is permitted provided an acknowledgment of the source is made. Material contained in this publication attributed to third parties are subject to third party copyright and are also subject to separate terms of use."* | `UNVERIFIED_SECONDHAND` |
| robots.txt | `https://mospi.gov.in/robots.txt` returns HTTP 200 **with the SPA's HTML shell**, so no robots.txt file is served. `sitemap.xml` behaves the same way | `MACHINE_OBSERVED` |

**If the reproduction notice is confirmed, it is good news for this project:** reuse with attribution is exactly what a learning platform needs. It is still secondhand. A human needs to (a) read the copyright policy page in a browser and (b) check the imprint page of at least the six priority documents. Some reports carry third-party material under separate terms, so the check has to be done per document.

The absence of a robots.txt file does not mean permission to crawl. It only means no machine-readable restriction is published. This audit's limits (targeted HEAD requests, 1.5 s spacing, no crawling) stay the right approach.

---

## 8. Next actions

| Priority | Action |
|---|---|
| **P1** | A human opens the copyright policy page in a browser and records its text word for word. This unblocks the licence question for the whole corpus. |
| **P1** | A human opens the six priority documents (§4) and confirms title, publication date, language and imprint copyright notice. |
| **P1** | Add a `series_base_year` / `supersedes` field to the corpus schema before any document is used for teaching (see §5). |
| P2 | Install PDF tooling (poppler or pypdf) so title, date and language can be read reproducibly from the PDF metadata. |
| P2 | After licence confirmation and Gate C sign-off, retrieve the six priority documents into `data/raw/mospi/`, with SHA-256 checksums. Then resolve the DOC-023/024 duplicate question by hash. |
| P3 | Retry `cpi.mospi.gov.in` from an Indian network. |
| P3 | Extend the corpus: HCES 2023-24 methodology, NIC 2008 / NCO classifications, WPI (issued by DPIIT/OEA, not MoSPI), and a current IIP base document if one exists. |

---

## 9. Reproducing this audit

```
python scripts/validators/check_document_urls.py docs/evidence/MoSPI/mospi_candidates.csv docs/evidence/MoSPI/mospi_url_checks.json
python scripts/utils/build_document_audit.py docs/evidence/MoSPI mospi
```

The first command sends one HEAD request per candidate and saves no document contents. The second combines candidates, check results and `mospi_annotations.json` into the corpus files.

| File | Contents |
|---|---|
| `mospi_candidates.csv` | Candidate list and search-index hints (input) |
| `mospi_url_checks.json` | Raw HTTP observations (input) |
| `mospi_annotations.json` | Per-document auditor notes (input) |
| `mospi_document_corpus.json` | Full record for every item, with per-field status |
| `mospi_document_corpus.csv` | Same data, flattened |
| `mospi_document_urls.txt` | The 31 live URLs, grouped by topic |

---

## 10. Sign-off

| Role | Name | Date |
|---|---|---|
| Auditor | AI assistant. Findings are `MACHINE_OBSERVED` / `UNVERIFIED_SECONDHAND`, **not** `VERIFIED` | 2026-09-14 |
| Human reviewer | UNASSIGNED | — |

Gate B complete: **No** (licence unconfirmed). Gate C signed: **No.**

---

## Sources

Search index queries were restricted to `mospi.gov.in`. Policy pages referenced:
- [MoSPI Copyrights Policy](https://www.mospi.gov.in/copyrights-policy)
- [MoSPI Privacy Policy](https://www.mospi.gov.in/privacy-policy)
- [MoSPI Meta Data Standards](https://www.mospi.gov.in/meta-data-standards)

The document URLs listed in §3 and in `mospi_document_urls.txt` are the primary sources.
