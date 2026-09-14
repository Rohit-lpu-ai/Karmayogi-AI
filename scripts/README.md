# scripts/

Collection, validation, and utility scripts.

**Nothing here performs collection yet, and nothing may be run against a live
government source during the discovery phase.**

| Directory | Purpose | Status |
|---|---|---|
| `collectors/` | One module per source. Retrieves and writes raw bytes to `data/raw/`. | Empty. Blocked until Gate C sign-off exists for a source. |
| `validators/` | Schema checks, provenance checks, and the blocking personal-data check. | Empty. Write these before the first collector. |
| `utils/` | Checksums, metadata sidecar writing, registry loading, logging. | Empty. |

## Rules for anything added here

1. A collector refuses to run unless its source row in
   `registry/source_registry.csv` is `VERIFIED` and Gate C is signed.
2. Raw responses are written unmodified, with a `.meta.json` sidecar and a
   SHA-256 checksum, before any parsing.
3. No endpoint is hard-coded. Configuration comes from the registry and the
   environment.
4. No collector requests, stores, or logs personal data. On encountering
   person-level fields it aborts and raises.
5. Validators fail the build. They do not warn.

See `../API_REQUIREMENTS.md` section 4 for the full client constraint list.
