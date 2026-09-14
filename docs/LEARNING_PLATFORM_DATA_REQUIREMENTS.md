# Learning-Platform Data Requirements

**Applies to:** the canonical datasets in `data/processed/`
**Enforced by:** `scripts/validators/validate_canonical_datasets.py`
**Last updated:** 2026-09-14

No product specification existed for the MVP data categories (programmes, reference documents, competencies, TPAC). This document collects the binding rules already in the repository and adds the minimum needed to make the data usable by the platform.

Each requirement has an **origin**:
- **Existing**: already stated in a repository document, which is cited.
- **ASSUMED**: introduced here. The product team should confirm, change, or drop it.

Each requirement also has a **severity**:

| Severity | Meaning |
|---|---|
| `ERROR` | The dataset is invalid. The validator exits non-zero and the data must not be used. |
| `RELEASE_BLOCKER` | The data is valid for development, but the affected records **must not be shown to learners** until the blocker is cleared. |
| `WARNING` | A quality gap. Report it and track it. It does not block anything. |

---

## A. Structure and integrity

| ID | Requirement | Severity | Origin |
|---|---|---|---|
| LP-01 | Every dataset file has an envelope: `schema_version`, `dataset_id`, `generated_at_utc`, `inputs` (path and SHA-256), `record_count` equal to the actual number of records, and `records`. | ERROR | Existing: `DATA_DICTIONARY.md` §3 (dataset wrapper) |
| LP-02 | Every dataset validates against `schemas/canonical_datasets.schema.json`. | ERROR | ASSUMED |
| LP-03 | Record IDs are unique within a dataset and **deterministic**: rebuilding from the same inputs yields the same IDs. | ERROR | ASSUMED (lesson content links to IDs, so they must be stable) |
| LP-04 | Every cross-reference resolves: topic tags → `topics`, competencies → clusters, TPAC references → `documents`, `source_id` → `registry/source_registry.csv`. | ERROR | ASSUMED |
| LP-05 | Only status values defined in `STATUS_VOCABULARY.md` are used. | ERROR | Existing: `STATUS_VOCABULARY.md` |

## B. Provenance

| ID | Requirement | Severity | Origin |
|---|---|---|---|
| LP-06 | Every record carries provenance: source ID, source URL, source organisation, retrieval date, access method. Collected records also carry the local file path and the source file's SHA-256. | ERROR | Existing: `DATA_DICTIONARY.md` §3, §6; collection instruction of 2026-09-14 |
| LP-07 | Where the raw source file is present locally, its SHA-256 matches the value recorded in the record. A missing raw file is reported but is not an error, because raw PDFs are git-ignored. | ERROR / WARNING | Existing: `DATA_COLLECTION_CHECKLIST.md` Gate D |
| LP-08 | Every record states its licence status and usage notes. | ERROR | Existing: collection instruction of 2026-09-14 |

## C. Safety

| ID | Requirement | Severity | Origin |
|---|---|---|---|
| LP-09 | No personal data: no honorific-plus-name patterns, email addresses, phone numbers, or 12-digit ID-like numbers. | ERROR | Existing: `DATA_DICTIONARY.md` §7; `DATA_COLLECTION_CHECKLIST.md` R3 |
| LP-10 | No `MOCK` data in `data/processed/`. | ERROR | Existing: `DATA_DICTIONARY.md` §8 |
| LP-11 | No reproduction of restricted content. CSCD definitions and behavioural indicators are absent. Quoted context from any source is ≤ 220 characters. | ERROR | Existing: DoPT Copyright Policy (recorded in `docs/DATA_COLLECTION_RESULTS.md` §5) |
| LP-12 | Nothing is marked `VERIFIED` and no human-review field is pre-filled by automation. | ERROR | Existing: `STATUS_VOCABULARY.md` rule 2 |

## D. Fitness for platform features

| ID | Requirement | Severity | Origin |
|---|---|---|---|
| LP-13 | **Programme catalogue.** Each programme has a display title, programme family, target group, duration, and fiscal year, so learners can browse and filter by family, target group, and topic. | ERROR | ASSUMED (mirrors IG-FR-01/06 in `API_REQUIREMENTS.md` §6.2) |
| LP-14 | **Reference library.** Each document has a title, document type, organisation, at least one topic, page count, and a text-availability flag (needed for later search and retrieval). | ERROR | ASSUMED |
| LP-15 | **Competency framework.** Each competency has an ID, name, cluster, and proficiency levels; the framework lists its level scale. | ERROR | ASSUMED (IG-FR-06 filter by competency) |
| LP-16 | **Linkability.** Programmes and documents carry topic tags from the shared taxonomy, so a programme can link to its reference reading. Coverage is reported: all documents should be tagged, and ≥ 80% of programmes. | WARNING | ASSUMED |
| LP-17 | Each programme records its schedule status (for example, tentative). Dates that are not known are stated as unknown, never guessed. | ERROR | Existing: "Do not guess missing fields" (instruction of 2026-09-14) |

## E. Learner-release gates

| ID | Requirement | Severity | Origin |
|---|---|---|---|
| LP-18 | `learner_visible` may be `true` only when the record's human review is complete (`review.verified = true`) **and** its licence status is `VERIFIED` with learner display permitted. The validator fails any record that claims visibility without meeting both. | ERROR | Existing: `DATA_DICTIONARY.md` §3 ("provenance containing UNKNOWN cannot be served to a learner"); `STATUS_VOCABULARY.md` |
| LP-19 | Every record lists its outstanding `release_blockers`. | RELEASE_BLOCKER | ASSUMED |
| LP-20 | Methodology documents record the statistical series or base year they describe, so superseded methods are not taught as current. | RELEASE_BLOCKER | Existing: recommendation in `docs/evidence/MoSPI/mospi_document_audit.md` §5 and `docs/DATA_COLLECTION_RESULTS.md` §4 |
| LP-21 | Titles taken from search indexes are confirmed against the document before release. | RELEASE_BLOCKER | Existing: `docs/DATA_COLLECTION_RESULTS.md` §8 |

---

## Out of scope for these datasets

- **iGOT course, enrolment, and completion data.** There is no real data. `clients/mock_igot_client.py` returns `MOCK` records, which LP-10 keeps out of `data/processed/`.
- **Statistical observations** (the `DATA_DICTIONARY.md` §2 observation record). No indicator series have been collected.
- **Mapping programmes to competencies.** No source states this mapping, so it is not inferred.
