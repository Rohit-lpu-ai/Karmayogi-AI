# data/processed — canonical datasets

Application-ready JSON built from `data/interim/` by
`scripts/processing/build_canonical_datasets.py` and checked by
`scripts/validators/validate_canonical_datasets.py` against
[`docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md`](../../docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md).

**Current verdict:** `VALID_FOR_DEVELOPMENT_NOT_RELEASABLE`. The data can be used to build and test features. **No record may be shown to learners yet.** See [`docs/DATASET_VALIDATION_REPORT.md`](../../docs/DATASET_VALIDATION_REPORT.md).

---

## Datasets

| File | Records | What it is |
|---|---|---|
| `training_programmes.json` | 99 | NSSTA programmes for FY 2025-26, parsed from the Advance Training Calendar. Fields: family, cohort, target group, topic, duration, batch size, venue, topic tags. |
| `documents.json` | 22 | Reference library of NSSTA, MoSPI, and DoPT documents (19 collected, 3 link-only), with type, topics, pages, text availability, detected language, and series/base year. |
| `competency_framework.json` | 25 | DoPT Civil Services Competency Dictionary: 4 clusters and 25 competencies, **names and structure only**. |
| `tpac_references.json` | 16 | TPAC mentions inside NSSTA documents: page number and context of up to 220 characters. |
| `topics.json` | 23 | Shared topic taxonomy used by programmes and documents. The taxonomy is `ASSUMED`. |
| `validation_report.json` | — | Machine-readable validation result. Generated; do not edit. |

Every dataset uses the same envelope: `schema_version`, `dataset_id`, `generated_at_utc`, `generator`, `inputs` (path and SHA-256), `record_count`, `records`. The schema is at `schemas/canonical_datasets.schema.json`.

## Every record carries

| Field | Meaning |
|---|---|
| `id` | Stable ID derived from content. Rebuilding produces the same IDs. |
| `data_status` | Value from `STATUS_VOCABULARY.md`. Nothing here is `VERIFIED`. |
| `provenance` | Source ID, URL, organisation, retrieval date, access method, local raw file, SHA-256. |
| `licence` | Status, usage notes, attribution text, `permits_learner_display` (`null` means not yet established). |
| `review` | Human-verification fields. All currently unset. |
| `learner_visible` | `true` only when review is complete **and** the licence is `VERIFIED` and permits display. Currently `false` everywhere. |
| `release_blockers` | Why the record cannot be shown yet. |

## Rules for application code

1. **Filter on `learner_visible === true`** before showing anything to a learner. Today that returns nothing, which is correct.
2. **Show `licence.attribution_text`** wherever a record is displayed.
3. **Never display competency definitions.** They are not in the data. Link to the official DoPT PDF using `source_pages`.
4. **Treat `topic_tags` as suggestions.** They are keyword-derived (`ASSUMED`) until reviewed.
5. **Programme dates are unknown** (`schedule.dates = null`). The calendar is marked "Tentative". Do not invent dates.
6. **Codes stay as printed** (`ISS (P)`, `MCTP`, `DSTP`, `DBTP`, `UN SIAP`, `ISEC`). Expansions have not been confirmed.
7. **Data from iGOT is not here.** The platform's iGOT integration is mock-only (`clients/mock_igot_client.py`), and mock data is prohibited in this directory.

## Rebuild and validate

```
python scripts/processing/build_canonical_datasets.py
python scripts/validators/validate_canonical_datasets.py     # exit 1 on any ERROR
python -m unittest discover -s tests -t .
```

**Reproducibility note:** language detection reads the extracted PDF text in `data/interim/*/text/`, which is git-ignored and local only. In a fresh clone without those files, `languages_detected` falls back to `UNKNOWN` and the validator warns that inputs are missing. All IDs and other fields are unaffected.
