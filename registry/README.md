# registry/

`source_registry.csv` is the single source of truth for what sources exist and
what we know about each one. Every other document indexes into it by `source_id`.

- 27 columns, 24 rows (23 candidate external sources + 1 internal mock fixture).
- Every unknown field reads `UNKNOWN`, never blank.
- Status values are defined in `../STATUS_VOCABULARY.md`.
- Only a human may change a field to `VERIFIED` or `UNAVAILABLE`, and only with
  a date, a name, and an evidence path.

Collection scripts read this file to decide whether they are permitted to run.
