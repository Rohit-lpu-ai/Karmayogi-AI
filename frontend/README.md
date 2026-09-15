# Frontend

React 18 + TypeScript + Vite 8 + React Router 7, styled with Tailwind CSS 4 and shadcn/ui-style components on Radix
primitives (DEC-050). Every screen calls the real API; authorisation is enforced by the backend.

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173 - proxies /api to 127.0.0.1:8000 (override with API_PROXY_TARGET)
npm test           # Vitest + Testing Library (API mocked)
npm run typecheck  # app (tsconfig.json) and vite.config.ts (tsconfig.node.json)
npm run build
```

On Windows, `start-dev.bat` in the repository root starts the database, backend and this dev server together.
If the backend is not running, API calls return a 503 `BACKEND_UNAVAILABLE` problem that the UI shows as a message.

## Structure

| Path | Contents |
|---|---|
| `src/styles/globals.css` | Design tokens (colour roles, level scale, radius, shadows, fonts) and Tailwind theme mapping |
| `src/styles/legacy.css` | Vertical-slice styles scoped under `.legacy`, only for screens not yet migrated |
| `src/components/ui/` | Base components: button, card, badge, alert, form, tabs, progress, skeleton, dialog/sheet, dropdown menu, collapsible, toaster |
| `src/components/layout/` | `AppShell` (sidebar, top bar, mobile drawer, user menu, skip link), `PageHeader`, `Breadcrumbs` |
| `src/components/product/` | `DemoDataNotice`, `ConfirmationDialog`, `StatCard` |
| `src/components/States.tsx` | `LoadingState`, `EmptyState`, `ErrorState`, `StatusBadge`, `EvidenceBadge`, `DemoBadge` |
| `src/config/product.ts` | Product name (working name, DEC-053) - change it only here |
| `src/config/navigation.ts` | Primary navigation; add an entry when a screen ships (no placeholder routes) |
| `src/pages/dev/DesignSystemPage.tsx` | Component gallery at `/dev/design-system`, dev server only (excluded from production builds) |

## Migration status (DEC-050)

| Screen | Status |
|---|---|
| App shell, signed-out layout | Migrated |
| Login, get started, dashboard, assessment, result | Legacy styles inside the new shell (wrapped in `.legacy`); migrated one at a time |

Rules: one primary action per view; status always in words (colour supports text); no official government branding;
every synthetic item carries a DEMO label; developer details (rule versions, formulas) only inside disclosures.

## Local sign-in

Synthetic accounts such as `learner01@example.invalid` with `DEMO_USER_PASSWORD` from the repository `.env`
(created by `python -m app.seed ... --demo-users --demo-content`). Each account can complete the baseline once;
reset accounts with `reset-demo.bat` or `python -m app.seed.demo_reset` (see `backend/README.md`).
