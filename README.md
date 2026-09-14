# KaramYogiAI — AI-Enabled Learning Platform for India's Official Statistical System

**Current phase: MVP implementation, roadmap Phase 2 (backend foundation and reference schema).** Discovery and data collection (Phase 1) are complete. See [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) and [`docs/IMPLEMENTATION_ROADMAP.md`](docs/IMPLEMENTATION_ROADMAP.md). The discovery notes below are kept for provenance and describe the state before collection (DEC-042).

This repository currently holds the discovery scaffold only: a registry of
candidate sources, the procedure for assessing them, the schema we intend to
normalise into, and the audit record. It contains **no collected data**, **no API
endpoints**, and **no personal data**.

---

## What has and has not happened

| | |
|---|---|
| Sources registered as candidates | 24 |
| Sources actually investigated | **0** |
| Data collected | **none** |
| API endpoints recorded | **none — deliberately** |
| Personal data | **none, and excluded by design** |
| Mock fixtures | 1, clearly labelled `MOCK` |

The source list was assembled from general knowledge of India's statistical
system. It is a list of things *to investigate*, not a list of confirmed facts.
Even the organisation names are `UNKNOWN` until a human confirms current
official naming.

---

## Core documents

| Document | Purpose |
|---|---|
| [`STATUS_VOCABULARY.md`](STATUS_VOCABULARY.md) | Defines `VERIFIED` / `UNKNOWN` / `UNAVAILABLE` / `MOCK` / `ASSUMED`. **Read first.** |
| [`DATA_COLLECTION_CHECKLIST.md`](DATA_COLLECTION_CHECKLIST.md) | Gates A–E. How a source becomes collectable. |
| [`API_REQUIREMENTS.md`](API_REQUIREMENTS.md) | What we need an API to do, and the empty capability matrix. |
| [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | Canonical schema for statistical observations (none collected yet). |
| [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) | Audit template, risk register, and (empty) audit record. |
| [`registry/source_registry.csv`](registry/source_registry.csv) | Single source of truth. 27 columns × 27 rows. |
| [`docs/DATA_COLLECTION_RESULTS.md`](docs/DATA_COLLECTION_RESULTS.md) | What the MVP collection gathered (NSSTA, MoSPI, CSCD, iGOT status). |
| [`docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md`](docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md) | Requirements LP-01–LP-21 for application-ready datasets. |
| [`data/processed/README.md`](data/processed/README.md) | The canonical datasets and the rules for consuming them. |
| [`docs/DATASET_VALIDATION_REPORT.md`](docs/DATASET_VALIDATION_REPORT.md) | Generated validation result. Current verdict: valid for development, not releasable. |

---

## Layout

```
KaramYogiAI/
├── data/
│   ├── raw/              Unmodified source files, one dir per source. EMPTY.
│   │   ├── mospi/  ndap/  data_gov_in/  rbi/  census/  misc/
│   ├── interim/          Scratch space between raw and processed. EMPTY.
│   ├── processed/        Canonical JSON per DATA_DICTIONARY.md. EMPTY.
│   └── samples/mock/     Synthetic fixtures. Labelled MOCK. Never served.
├── scripts/
│   ├── collectors/       One per source. Blocked until Gate C. EMPTY.
│   ├── validators/       Schema, provenance, and personal-data checks. EMPTY.
│   └── utils/            Checksums, sidecars, registry loading. EMPTY.
├── clients/              Read-only API clients. EMPTY — no API is VERIFIED yet.
├── registry/             source_registry.csv — the source of truth.
├── schemas/              JSON Schema files, once the dictionary stabilises. EMPTY.
├── docs/
│   └── evidence/         Saved docs and screenshots proving VERIFIED claims. EMPTY.
├── logs/collection/      Collection run logs. EMPTY.
└── notebooks/            Exploration notebooks. EMPTY.
```

---

## Ground rules for this phase

1. **Do not scrape anything.** Manual browsing to read terms is fine; automated
   fetching is not.
2. **Do not invent API endpoints.** No base URL, path, or parameter enters this
   repository unless a human read it in official documentation and recorded the
   URL and date.
3. **Do not collect personal data.** No microdata, no identifiers. This is
   blocking, not advisory — see `DATA_DICTIONARY.md` §7.
4. **Mark every claim.** `UNKNOWN`, `UNAVAILABLE`, `MOCK`, and `ASSUMED` are
   distinct from `VERIFIED` and are never blurred together.
5. **Only humans mark things `VERIFIED`.** An AI assistant may draft rows, but
   may only ever write `UNKNOWN`, `MOCK`, or `ASSUMED`.

The reason rule 2 and rule 5 are stated this bluntly: officials trained on this
platform will carry what they learn into real statistical work. A plausible
wrong number is worse here than no number at all.

---

## Next steps

1. Assign a named owner to each P1 source in the registry.
2. Audit the three aggregator portals first (SRC-009, SRC-010, SRC-008) — highest
   information gain, since one of them may cover many indicators at once.
3. Resolve the blocking geography-coding decision (`DATA_DICTIONARY.md` §5.1).
4. Resolve Q3 in `API_REQUIREMENTS.md` — whether licences permit caching and
   re-serving official figures inside a learning platform. This one determines
   project viability and should not wait.
