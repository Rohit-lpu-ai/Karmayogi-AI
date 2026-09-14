# Data Dictionary

**Phase:** Discovery
**Status of this document:** Proposed canonical schema. Not yet validated against
any real source, because no real source has been inspected.
**Last updated:** 2026-09-14

Every field marked `PROPOSED` is our design intent. Every field marked `UNKNOWN`
is something we cannot define until a real source is examined. Nothing here is
`VERIFIED` yet.

---

## 1. Scope

This dictionary defines the shape of files in `data/processed/`. It covers:

- the canonical **observation** record (one number, fully described),
- the **dataset** wrapper and its provenance block,
- the **sidecar metadata** written next to every raw file,
- controlled vocabularies,
- missing-value and status conventions.

It explicitly does **not** define any person-level record, because the project
does not collect personal data. See §7.

---

## 2. Canonical observation record

One row = one number. This is the atomic unit the platform teaches with.

| Field | Type | Required | Status | Definition |
|---|---|---|---|---|
| `observation_id` | string | Yes | PROPOSED | Deterministic hash of indicator + geography + period + vintage + disaggregation. Stable across re-runs. |
| `indicator_id` | string | Yes | PROPOSED | Our internal stable ID. Not the source's ID. |
| `indicator_name_en` | string | Yes | PROPOSED | Indicator name in English, as published by the source. Not reworded. |
| `indicator_name_hi` | string | No | UNKNOWN | Hindi name. Availability unknown for every source. |
| `source_indicator_code` | string | No | UNKNOWN | The source's own identifier, verbatim, if one exists. |
| `value` | number \| null | Yes | PROPOSED | The figure. `null` only with a `missing_reason`. |
| `value_type` | enum | Yes | PROPOSED | `count`, `rate`, `ratio`, `percentage`, `index`, `currency`, `mean`, `median`. |
| `unit` | string | Yes | PROPOSED | Verbatim unit, e.g. `persons`, `per 1000 live births`, `INR crore`. Never inferred. |
| `unit_multiplier` | number | No | PROPOSED | Multiplier to reach the base unit, where the source publishes in thousands, lakh, crore, etc. |
| `base_year` | string | Cond. | PROPOSED | Required when `value_type` is `index`. Format `YYYY` or `YYYY-YY`. |
| `currency_year` | string | Cond. | PROPOSED | Required for constant-price currency values. |
| `price_basis` | enum | Cond. | PROPOSED | `current`, `constant`. Required for currency values. |
| `geo_level` | enum | Yes | PROPOSED | `national`, `state`, `district`, `subdistrict`, `urban_rural`, `other`. |
| `geo_code` | string | Yes | PROPOSED | Code in the vocabulary named by `geo_code_system`. |
| `geo_code_system` | string | Yes | UNKNOWN | Which coding system. Cannot be fixed until sources are inspected. See §5.1. |
| `geo_name` | string | Yes | PROPOSED | Name as published by the source, verbatim. |
| `period_start` | string | Yes | PROPOSED | ISO 8601 date, inclusive. |
| `period_end` | string | Yes | PROPOSED | ISO 8601 date, inclusive. |
| `period_type` | enum | Yes | PROPOSED | `annual`, `financial_year`, `quarterly`, `monthly`, `point_in_time`, `multi_year`. |
| `period_label` | string | Yes | PROPOSED | Human label as published, e.g. `2023-24`. Kept because Indian financial years are routinely mislabelled when normalised. |
| `estimate_vintage` | enum | Yes | PROPOSED | `provisional`, `first_revised`, `second_revised`, `third_revised`, `final`, `projected`, `unknown`. |
| `vintage_published_on` | date | No | PROPOSED | Publication date of this particular estimate. |
| `supersedes_observation_id` | string | No | PROPOSED | Prior vintage of the same figure, if known. Makes revisions teachable. |
| `disaggregation` | object | No | PROPOSED | Key-value map, e.g. `{"sex":"female","sector":"rural"}`. Keys from §5.2. |
| `missing_reason` | enum | Cond. | PROPOSED | Required when `value` is `null`. See §4. |
| `confidence_interval_low` | number | No | UNKNOWN | Availability unknown for every source. |
| `confidence_interval_high` | number | No | UNKNOWN | As above. |
| `relative_standard_error` | number | No | UNKNOWN | As above. |
| `sample_size` | number | No | UNKNOWN | As above. |
| `footnote_refs` | array[string] | No | PROPOSED | References into the dataset-level footnotes. |
| `data_status` | enum | Yes | PROPOSED | `VERIFIED`, `UNKNOWN`, `UNAVAILABLE`, `MOCK`, `ASSUMED`. Per `STATUS_VOCABULARY.md`. |
| `source_id` | string | Yes | PROPOSED | Foreign key to `registry/source_registry.csv`. |

---

## 3. Dataset wrapper

```json
{
  "schema_version": "0.1.0-draft",
  "dataset_id": "UNKNOWN",
  "dataset_title_en": "UNKNOWN",
  "source_id": "UNKNOWN",
  "data_status": "UNKNOWN",
  "provenance": {
    "source_organisation": "UNKNOWN",
    "source_publication_title": "UNKNOWN",
    "source_url": "UNKNOWN",
    "access_method": "UNKNOWN",
    "retrieved_at_utc": "UNKNOWN",
    "retrieved_by": "UNKNOWN",
    "raw_file_path": "UNKNOWN",
    "raw_file_sha256": "UNKNOWN",
    "transform_script": "UNKNOWN",
    "transform_script_git_sha": "UNKNOWN",
    "licence": "UNKNOWN",
    "licence_url": "UNKNOWN",
    "attribution_text": "UNKNOWN",
    "gate_c_signed_by": "UNKNOWN",
    "gate_c_signed_on": "UNKNOWN"
  },
  "coverage": {
    "temporal_from": "UNKNOWN",
    "temporal_to": "UNKNOWN",
    "geo_levels": ["UNKNOWN"],
    "geo_code_system": "UNKNOWN"
  },
  "quality": {
    "row_count": 0,
    "null_value_count": 0,
    "reconciled_against_source": false,
    "known_caveats": ["No source has been inspected as of 2026-09-14."]
  },
  "footnotes": {},
  "observations": []
}
```

**Rule:** a processed file whose `provenance` contains any `UNKNOWN` cannot be
served to a learner. It may exist in the repository as work in progress.

---

## 4. Missing-value conventions

`value: null` alone is never acceptable. It must be paired with `missing_reason`.

| `missing_reason` | Meaning | Display guidance |
|---|---|---|
| `not_collected` | The survey or system did not collect it. | "Not collected" |
| `not_applicable` | The category does not apply to this unit. | "—" |
| `suppressed_confidentiality` | Withheld to protect confidentiality. | "Suppressed" |
| `suppressed_reliability` | Withheld because the estimate is too unreliable to publish. | "Not reliable enough to publish" |
| `not_yet_published` | Expected but not released at retrieval time. | "Not yet published" |
| `source_blank` | The source left it blank without saying why. | "Not stated by source" |
| `parse_failure` | Our pipeline could not read it. Defect on our side. | Never displayed; raises an alert. |
| `unknown` | We genuinely do not know. | "Unknown" |

Never impute, interpolate, carry forward, or zero-fill. A gap in official
statistics is information, and this platform exists to teach people to read it.

---

## 5. Controlled vocabularies

### 5.1 Geography — `UNKNOWN`, blocking

We cannot pick a geography coding system yet. Candidates to evaluate during
Gate B, all currently `UNKNOWN`:

- Census / ORGI codes
- LGD (Local Government Directory) codes
- ISO 3166-2:IN subdivision codes
- Source-specific internal codes

**Decision required before any processing.** Until then, `geo_code_system` is
`UNKNOWN` and `geo_code` holds the source's verbatim code. Do not silently map
between systems — state and district boundaries and codes have changed over
time, and an undocumented crosswalk would corrupt every sub-national series.

Required once decided: a documented crosswalk with effective dates, handling
state reorganisations and district splits and merges.

### 5.2 Disaggregation keys — PROPOSED

| Key | Allowed values | Status |
|---|---|---|
| `sex` | `male`, `female`, `transgender`, `all` | PROPOSED — source categories may differ and are not to be forced into these |
| `sector` | `rural`, `urban`, `combined` | PROPOSED |
| `age_group` | Verbatim source label, e.g. `15-59` | PROPOSED |
| `social_group` | Verbatim source label | PROPOSED — treat as sensitive; aggregate only |
| `industry` | NIC code | UNKNOWN — NIC version unconfirmed |
| `occupation` | NCO code | UNKNOWN — NCO version unconfirmed |

Where a source's categories do not match these, keep the source's categories
verbatim and record the mismatch. Never coerce.

### 5.3 Period types — PROPOSED

Indian statistics mix calendar years, financial years (April to March), agricultural
years, and survey rounds spanning months. `period_label` always keeps the source's
own label so this is never lost in normalisation.

---

## 6. Raw sidecar metadata

Every file in `data/raw/` gets `<filename>.meta.json` beside it:

```json
{
  "source_id": "UNKNOWN",
  "retrieved_at_utc": "UNKNOWN",
  "retrieved_by": "UNKNOWN",
  "access_method": "UNKNOWN",
  "request_url": "UNKNOWN",
  "request_params": {},
  "response_status": "UNKNOWN",
  "response_content_type": "UNKNOWN",
  "file_sha256": "UNKNOWN",
  "file_size_bytes": 0,
  "licence_at_time_of_retrieval": "UNKNOWN",
  "data_status": "UNKNOWN",
  "notes": "No raw files exist yet. Discovery phase."
}
```

Raw files are immutable. Corrections happen in processing, never by editing raw.

---

## 7. Personal data — excluded by design

This project collects **aggregate official statistics only**.

The following are **out of scope** and must not appear anywhere in this
repository, in any file, in any phase, unless a separate written decision with a
documented lawful basis is taken first:

- Names, addresses, phone numbers, email addresses
- Aadhaar, PAN, voter ID, ration card, or any government identifier
- Exact geographic coordinates of a household or individual
- Household or individual survey records (microdata), whether or not anonymised
- Any combination of fields sufficient to single out an individual
- Learner personal data, which is a separate system with a separate assessment

Any field in a processed file describing a person is a defect. The validators in
`scripts/validators/` are to fail the build on detection, not warn.

---

## 8. Mock data

`MOCK` data exists so that pipeline code can be developed before any real
collection is authorised.

Rules:
1. Lives only under `data/samples/mock/`.
2. Every mock file carries `"data_status": "MOCK"` at the top level.
3. Mock values are obviously synthetic — round, implausible, or flagged — never
   a plausible-looking real figure.
4. `source_id` is `SRC-024`.
5. Mock data never enters `data/processed/` and is never shown to a learner.
6. Any mock series is prefixed `MOCK — NOT OFFICIAL DATA` in its title.

---

## 9. Schema versioning

`schema_version` follows semantic versioning. Current: `0.1.0-draft`.

It stays below `1.0.0` until at least one real source has been inspected and the
schema has survived contact with real data. Expect breaking changes — in
particular to §5.1, which is unresolved.

---

## 10. Known gaps

| # | Gap | Status | Blocks |
|---|---|---|---|
| G1 | Geography coding system undecided | UNKNOWN | All sub-national data |
| G2 | NIC / NCO versions unconfirmed | UNKNOWN | Industry and occupation breakdowns |
| G3 | Sampling error field availability unknown | UNKNOWN | Teaching uncertainty |
| G4 | Hindi metadata availability unknown | UNKNOWN | NFR-03 |
| G5 | Revision vintage exposure unknown | UNKNOWN | FR-06, a core curriculum topic |
| G6 | No real source inspected, so this schema is untested | UNKNOWN | Schema 1.0.0 |
