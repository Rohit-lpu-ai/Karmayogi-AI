# Data Collection Checklist

**Phase:** Discovery (data and API discovery only)
**Status of this document:** Draft procedure. Not yet exercised against any real source.
**Last updated:** 2026-09-14

This checklist governs how a source moves from "someone mentioned it" to "we are
allowed to collect from it". **No collection has happened yet and none may happen
until a source has cleared Gate C below.**

Read `STATUS_VOCABULARY.md` first. Every answer recorded here is `VERIFIED`,
`UNKNOWN`, `UNAVAILABLE`, `MOCK`, or `ASSUMED` — never blank.

---

## Standing rules for this phase

| # | Rule | Rationale |
|---|---|---|
| R1 | Do not scrape, crawl, or bulk-download anything. | This phase is discovery. Access decisions are not yet made. |
| R2 | Do not write an API endpoint into any file unless a human has read it in official documentation and marked it `VERIFIED`. | Invented endpoints propagate silently and are extremely hard to unpick later. |
| R3 | Do not collect personal data, unit-level records about identifiable individuals, or any microdata, in this phase or the next, without a separate written decision. | The platform teaches statistics; it does not need person-level data to do so. |
| R4 | Manual, human-driven browsing of a public page to read its terms is allowed and expected. Automated fetching is not. | Reading a licence is not collection. |
| R5 | Anything synthetic lives under `data/samples/mock/` and is marked `MOCK` inside the file itself. | Prevents mock numbers being mistaken for official statistics. |
| R6 | Every claim gets a date and a name. An undated claim is `UNKNOWN`. | Portals change. A fact without a date is not a fact. |

---

## Gate A — Identification

Complete for every candidate source before spending any further effort.

- [ ] Source has a row in `registry/source_registry.csv` with a `source_id`.
- [ ] Publishing organisation named (the body legally responsible, not the portal brand).
- [ ] Tier assigned (1 = core official statistics, 2 = important, 3 = supplementary, 4 = internal fixture).
- [ ] Domain / topic assigned.
- [ ] Stated in one sentence: what this source would teach a learner that no other source would.
- [ ] Priority assigned (P1 / P2 / P3).
- [ ] A named human owner assigned. `UNASSIGNED` blocks Gate B.

**Exit condition:** the row exists and has an owner. Every other field may still be `UNKNOWN`.

---

## Gate B — Access assessment (desk research, human, manual)

Performed by opening the site in a browser and reading. No automation.

### B1. Existence and identity
- [ ] Canonical homepage URL observed first-hand and recorded, with date. Until then: `UNKNOWN`.
- [ ] Confirmed the site is the official one (government domain, or a body the ministry names).
- [ ] Recorded whether the source appears to be actively maintained or dormant.

### B2. Access route
Record which of these exist. Mark each `VERIFIED` / `UNAVAILABLE` / `UNKNOWN`:
- [ ] Documented public API.
- [ ] Bulk download (CSV / XLSX / ZIP).
- [ ] Per-table download behind a form or query builder.
- [ ] PDF-only publication.
- [ ] No programmatic access at all.

### B3. Documentation
- [ ] Located official API or data documentation, or confirmed none exists.
- [ ] Saved a copy / screenshot of the documentation under `docs/evidence/<source_id>/`.
- [ ] Recorded the documentation URL and the date it was read.

### B4. Terms, licence, and robots
- [ ] Terms of use / data policy located and read in full by a human.
- [ ] Licence identified and recorded verbatim (do not paraphrase a licence).
- [ ] Attribution requirement recorded.
- [ ] Redistribution permitted? Yes / No / `UNKNOWN`.
- [ ] Derivative works permitted? Yes / No / `UNKNOWN`.
- [ ] Commercial or hosted use permitted? Yes / No / `UNKNOWN`.
- [ ] `robots.txt` read and its relevant directives recorded.
- [ ] Any rate limit or fair-use clause recorded.

### B5. Privacy screen (mandatory, blocking)
- [ ] Confirmed the target data is **aggregate** — no rows about identifiable individuals.
- [ ] Confirmed no direct identifiers (name, address, phone, Aadhaar or any ID number, GPS point location).
- [ ] Confirmed no indirect identifiers that could re-identify a person in combination.
- [ ] If the source contains microdata: the specific tables we want are named, and the microdata is explicitly excluded.
- [ ] If any doubt remains: mark `UNKNOWN` and escalate. Do not proceed.

**Exit condition:** B1–B5 answered, B5 clean, evidence saved.

---

## Gate C — Collection authorisation

A source may only be collected from after **all** of the following are true and
recorded in the registry.

- [ ] Gate B complete, with evidence paths present.
- [ ] Licence permits our intended use, or written permission obtained.
- [ ] Attribution string drafted and stored with the source.
- [ ] Access method chosen and justified (API > bulk download > form download > PDF extraction).
- [ ] Rate limit and politeness policy written down.
- [ ] Two named humans have signed off: the source owner and one reviewer.
- [ ] Sign-off date recorded.

**Until Gate C is signed, the collection scripts in `scripts/collectors/` must
refuse to run against that source.**

---

## Gate D — Collection run (future phase — not active)

Recorded here so the design is fixed in advance.

- [ ] Raw response saved byte-for-byte and unmodified under `data/raw/<source>/`.
- [ ] Accompanying `.meta.json` written alongside it (see `DATA_DICTIONARY.md`).
- [ ] SHA-256 checksum of the raw file recorded.
- [ ] Retrieval timestamp in ISO 8601 with timezone recorded.
- [ ] Request parameters recorded.
- [ ] Run logged to `logs/collection/`.
- [ ] Raw file never edited in place. Corrections happen downstream only.

---

## Gate E — Processing (future phase — not active)

- [ ] Transformation script committed and referenced from the output metadata.
- [ ] Output conforms to the canonical schema in `DATA_DICTIONARY.md`.
- [ ] Units, base year, and currency-year recorded explicitly.
- [ ] Geography codes mapped to a single controlled vocabulary.
- [ ] Missing values distinguished: not collected / not applicable / suppressed / not yet published.
- [ ] Provenance block present and complete in every processed file.
- [ ] Validation script passes.
- [ ] Row counts and totals reconciled against the published source figures.

---

## Per-source progress board

Update as work proceeds. Every source starts at Gate A, `UNKNOWN`.

| source_id | Source | Owner | Gate A | Gate B | Gate C | Notes |
|---|---|---|---|---|---|---|
| SRC-001 | MoSPI main portal | UNASSIGNED | Not started | Not started | Not started | |
| SRC-002 | NSS | UNASSIGNED | Not started | Not started | Not started | Microdata concern — see B5 |
| SRC-003 | PLFS | UNASSIGNED | Not started | Not started | Not started | |
| SRC-004 | CPI | UNASSIGNED | Not started | Not started | Not started | |
| SRC-005 | IIP | UNASSIGNED | Not started | Not started | Not started | |
| SRC-006 | National Accounts | UNASSIGNED | Not started | Not started | Not started | |
| SRC-007 | ASI | UNASSIGNED | Not started | Not started | Not started | |
| SRC-008 | eSankhyiki | UNASSIGNED | Not started | Not started | Not started | Existence unconfirmed |
| SRC-009 | NDAP | UNASSIGNED | Not started | Not started | Not started | |
| SRC-010 | OGD Platform | UNASSIGNED | Not started | Not started | Not started | |
| SRC-011 | RBI / DBIE | UNASSIGNED | Not started | Not started | Not started | |
| SRC-012 | Census of India | UNASSIGNED | Not started | Not started | Not started | |
| SRC-013 | SRS | UNASSIGNED | Not started | Not started | Not started | |
| SRC-014 | CRS | UNASSIGNED | Not started | Not started | Not started | |
| SRC-015 | NFHS | UNASSIGNED | Not started | Not started | Not started | Likely restricted access |
| SRC-016 | UDISE+ | UNASSIGNED | Not started | Not started | Not started | |
| SRC-017 | AISHE | UNASSIGNED | Not started | Not started | Not started | |
| SRC-018 | Agri statistics | UNASSIGNED | Not started | Not started | Not started | |
| SRC-019 | Trade statistics | UNASSIGNED | Not started | Not started | Not started | |
| SRC-020 | Labour Bureau | UNASSIGNED | Not started | Not started | Not started | |
| SRC-021 | NSC reports | UNASSIGNED | Not started | Not started | Not started | Text corpus |
| SRC-022 | NIC / NCO / NPCMS | UNASSIGNED | Not started | Not started | Not started | Needed as vocabularies |
| SRC-023 | SDG NIF | UNASSIGNED | Not started | Not started | Not started | |
| SRC-024 | Mock fixtures | UNASSIGNED | Complete | Not applicable | Not applicable | `MOCK` — internal only |

---

## Phase exit criteria

Discovery is finished when, for every P1 source:

1. Gate B is complete with saved evidence.
2. The registry has no `UNKNOWN` in the licence, access-method, or privacy columns.
3. `API_REQUIREMENTS.md` records, per source, whether our requirements are met,
   partially met, or `UNAVAILABLE`.
4. `SOURCE_AUDIT.md` carries a signed assessment.
5. A written recommendation exists on which sources to build on first.
