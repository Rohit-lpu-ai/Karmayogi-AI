# Dataset Validation Report

**Generated:** 2026-09-14T12:37:25+00:00  
**Requirements:** [`docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md`](LEARNING_PLATFORM_DATA_REQUIREMENTS.md)  
**Schema:** `schemas/canonical_datasets.schema.json`  
**Validator:** `scripts/validators/validate_canonical_datasets.py` (this file is generated; do not edit)

## Verdict: `VALID_FOR_DEVELOPMENT_NOT_RELEASABLE`

| Errors | Warnings | Release-blocker findings |
|---|---|---|
| 0 | 10 | 724 |

## Datasets

| Dataset | Records | Human-verified | Learner-visible |
|---|---|---|---|
| `topics` | 23 | 0 | 0 |
| `documents` | 22 | 0 | 0 |
| `training_programmes` | 99 | 0 | 0 |
| `competency_framework` | 25 | 0 | 0 |
| `tpac_references` | 16 | 0 | 0 |

## Requirements

| ID | Requirement | Severity | Outcome | Findings |
|---|---|---|---|---|
| LP-01 | Dataset envelope complete; record_count matches | ERROR | **PASS** | — |
| LP-02 | Validates against canonical JSON Schema | ERROR | **PASS** | — |
| LP-03 | Record IDs unique and deterministic | ERROR | **PASS** | — |
| LP-04 | Cross-references resolve | ERROR | **PASS** | — |
| LP-05 | Status values from STATUS_VOCABULARY.md | ERROR | **PASS** | — |
| LP-06 | Provenance complete for every record | ERROR | **PASS** | — |
| LP-07 | Raw source checksums match (missing local raw file = WARNING) | ERROR | **PASS** | — |
| LP-08 | Licence status and usage notes present | ERROR | **PASS** | — |
| LP-09 | No personal data | ERROR | **PASS** | — |
| LP-10 | No MOCK data in data/processed | ERROR | **PASS** | — |
| LP-11 | No reproduction of restricted content | ERROR | **PASS** | — |
| LP-12 | No automated verification | ERROR | **PASS** | — |
| LP-13 | Programme catalogue fields usable | ERROR | **PASS** | — |
| LP-14 | Reference library fields usable | ERROR | **PASS** | — |
| LP-15 | Competency framework fields usable | ERROR | **WARN** | warning: 1 |
| LP-16 | Topic-tag linkability coverage | WARNING | **WARN** | warning: 9 |
| LP-17 | Schedule status recorded; unknown dates not guessed | ERROR | **PASS** | — |
| LP-18 | learner_visible only when review + VERIFIED licence | ERROR | **PASS** | — |
| LP-19 | Outstanding release blockers listed | RELEASE_BLOCKER | **BLOCKED** | release_blocker: 696 |
| LP-20 | Methodology documents record series/base year | RELEASE_BLOCKER | **BLOCKED** | release_blocker: 7 |
| LP-21 | Search-index titles confirmed before release | RELEASE_BLOCKER | **BLOCKED** | release_blocker: 21 |

## Release blockers (per record)

| Blocker | Records |
|---|---|
| `human_review_pending` | 162 |
| `licence_not_verified` | 162 |
| `topic_tags_unreviewed` | 112 |
| `parse_needs_spot_check` | 99 |
| `schedule_dates_unknown` | 99 |
| `licence_restricts_reproduction` | 28 |
| `title_unverified` | 21 |
| `series_base_year_unknown` | 7 |
| `link_only_not_collected` | 3 |
| `scanned_no_text_layer` | 2 |
| `extraction_issue` | 1 |

## Findings other than per-record release blockers

### LP-15 — Competency framework fields usable (1 total)
- **WARNING** `competency_framework` `CSCD-2014-4.8`: levels ['Level 1', 'Level 2', 'Level 3', 'Level 4'] differ from framework scale ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']

### LP-16 — Topic-tag linkability coverage (9 total)
- **WARNING** `training_programmes` `NSSTA-PRG-5e2a1a8c54`: untagged: 'DBTP for UT of Ladakh'
- **WARNING** `training_programmes` `NSSTA-PRG-aa0504f895`: untagged: 'DBTP for UT of Ladakh'
- **WARNING** `training_programmes` `NSSTA-PRG-10da2e7afe`: untagged: 'TBD'
- **WARNING** `training_programmes` `NSSTA-PRG-8b1a8a8a5e`: untagged: 'TBD'
- **WARNING** `training_programmes` `NSSTA-PRG-963861005c`: untagged: 'Special Foundation Course (SFC) With AIS and CCS Officers'
- **WARNING** `training_programmes` `NSSTA-PRG-f3feead5d8`: untagged: 'TBD'
- **WARNING** `training_programmes` `NSSTA-PRG-2a0679aea1`: untagged: 'TBD'
- **WARNING** `training_programmes` `NSSTA-PRG-0f81a64034`: untagged: 'One Day Workshop on University Campus'
- **WARNING** `training_programmes` `NSSTA-PRG-2a1c1f2a0f`: untagged: 'NSSTA Foundation Day'

### LP-20 — Methodology documents record series/base year (7 total)
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-002`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-004`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-006`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-012`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-013`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-015`: series/base year unknown
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-016`: series/base year unknown

### LP-21 — Search-index titles confirmed before release (21 total)
- **RELEASE_BLOCKER** `documents` `CSCD-LINK-001`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `CSCD-LINK-002`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-001`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-002`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-004`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-006`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-008`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-012`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-013`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-015`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-016`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-026`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-029`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `MOSPI-DOC-031`: title taken from search index; confirm against document
- **RELEASE_BLOCKER** `documents` `NSSTA-DOC-001`: title taken from search index; confirm against document
- … 6 more in `data/processed/validation_report.json`

