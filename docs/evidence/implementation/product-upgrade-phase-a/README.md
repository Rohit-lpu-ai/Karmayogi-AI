# Product upgrade phase A - evidence (2026-09-15)

Critical fixes, design foundation and app shell. Summary: [../../../IMPLEMENTATION_STATUS.md](../../../IMPLEMENTATION_STATUS.md) §1c.

| File | Content |
|---|---|
| `01-port-detection.txt` | `deploy/local/dev-port.ps1` against this project's API and Vite, the wrong kind, a stale `uvicorn --reload`, a free port |
| `02-smoke-through-vite-proxy.txt` | Live API journey through the Vite proxy with `API_PROXY_TARGET` (backend on port 8001), after a demo reset |
| `03-backend-pytest.txt` | Backend test suite |
| `04-alembic.txt` | Migration `0004` current, drift check, downgrade and upgrade |
| `05-phase1-unittest.txt` | Phase 1 dataset and mock iGOT tests |
| `06-frontend.txt` | Type-check, Vitest (verbose), production build, `npm audit` |
| `screenshots/` | Headless Microsoft Edge captures of login, dashboard (desktop and 360 px), demo notice, account menu, mobile menu, assessment and the dev-only design system page. Signed-in captures use the synthetic account `learner01@example.invalid`; dashboard content is still the legacy vertical-slice layout inside the new shell |

Not performed: axe automated accessibility checks, Playwright journeys, manual screen-reader test.
