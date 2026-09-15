# Vertical slice 1 - command evidence (2026-09-15)

Output captured with `tee` while the commands ran. Secrets are never printed (the demo password is read from `.env`).

| File | Content |
|---|---|
| 01-repository-inventory.txt | `git status`, `git log`, backend/deploy file list, frontend absence (before work) |
| 02-database-verification.txt | Alembic head, tables, triggers, seed counts, restricted content checks (before work) |
| 03-existing-tests.txt | 73 backend tests, 35 Phase 1 tests, `alembic check` (before work) |
| 04-document-claim-checks.txt | Stale-claim grep, implemented routes, lock file, ignore rules (before work) |
| 05-install-argon2.txt | Installing `argon2-cffi` |
| 06-autogenerate-0003.txt | Autogeneration of migration 0003 |
| 07-backend-tests.txt | Full verbose backend test run: 167 passed |
| 08-dev-migrate-and-seed.txt | Upgrade to 0003, `alembic check`, demo seed run twice |
| 09-live-api-smoke.txt | Live HTTP journey against uvicorn |
| 10-npm-audit.txt | Frontend dependency versions and audit (0 vulnerabilities) |
| 11-frontend-typecheck-test-build.txt | `npm run typecheck`, `npm test` (12 passed), `npm run build` |
| 12-frontend-proxy-smoke.txt | Journey through the Vite dev-server proxy |
| 13-log-hygiene.txt | API log checked for password, session cookie, email addresses |
| 14-final-regression.txt | Final run of all suites, build and `alembic check` |
