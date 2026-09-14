# Status Vocabulary (normative)

Every fact recorded anywhere in this repository — in Markdown tables, in
`registry/source_registry.csv`, in JSON metadata blocks — MUST carry exactly one
of these five status values. Nothing is left blank and nothing is implied.

| Status | Meaning | Who may set it | Allowed uses |
|---|---|---|---|
| `VERIFIED` | A human opened the source, confirmed the fact first-hand, and recorded the date and evidence path. | Human only. Never set by an AI assistant, a script, or an inference. | Safe to build on. |
| `UNKNOWN` | Not yet investigated, or investigated and inconclusive. This is the default for every new row. | Anyone. | Must not be built on. Blocks downstream work. |
| `UNAVAILABLE` | Investigated and confirmed to not exist, to be inaccessible to us, or to be blocked by licence/auth/cost. Requires a stated reason. | Human only. | Closes the line of enquiry; record the reason. |
| `MOCK` | Synthetic, hand-written, or placeholder content created by us so that downstream code has something to run against. | Anyone. | Never leaves `data/samples/mock/`. Never merged into `data/processed/`. |
| `ASSUMED` | A working assumption we are proceeding on, with no evidence yet. Must name the person who assumed it and what would falsify it. | Anyone. | Temporary only. Must resolve to `VERIFIED` or `UNAVAILABLE` before the build phase. |
| `MACHINE_OBSERVED` | Directly observed by an automated request, with the method, URL and timestamp recorded. Stronger than `UNKNOWN`, weaker than `VERIFIED`. | Anyone, including an AI assistant. | May be acted on provisionally. Must be human-confirmed to become `VERIFIED`. |
| `UNVERIFIED_SECONDHAND` | Reported by a third party — a search-engine summary, a news article, someone's recollection — and not observed at the source. | Anyone. | A lead to check. Must never be built on or shown to a learner. |
| `EXCLUDED_BY_POLICY` | Discovered, but deliberately not collected, on privacy or licence grounds. Requires a stated reason. | Anyone. | Closes the line of enquiry permanently. Record the reason. |

## Rules

1. `VERIFIED` requires three things together: a date (`YYYY-MM-DD`), the name of
   the person who checked, and a pointer to evidence (a saved file under
   `data/raw/`, or a screenshot under `docs/evidence/`). Without all three the
   status is `UNKNOWN`.
2. An AI assistant may draft rows but may only ever write `UNKNOWN`, `MOCK`,
   `ASSUMED`, `MACHINE_OBSERVED`, `UNVERIFIED_SECONDHAND`, or
   `EXCLUDED_BY_POLICY`. Promotion to `VERIFIED` or `UNAVAILABLE` is a human
   action.
2a. `MACHINE_OBSERVED` requires the request method, the exact URL, and the
   timestamp. Without all three it is `UNKNOWN`. It is never a synonym for
   `VERIFIED`, however reliable the observation felt.
3. `MOCK` data must be visibly marked inside the file itself (a `"_status":
   "MOCK"` key in JSON, a `# MOCK` header comment in CSV), not only by its
   directory.
4. Anything recorded before this vocabulary existed is `UNKNOWN` until re-checked.
