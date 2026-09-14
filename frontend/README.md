# Frontend (vertical slice 1)

React 18 + TypeScript + Vite 8 + React Router 7 (DEC-048). Pages: login, get started (notice + job role),
baseline assessment, result, dashboard (competency gaps, recommendations, estimate explanations).
Every screen calls the real API; authorisation is enforced by the backend.

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173 - proxies /api to the backend on 127.0.0.1:8000
npm test           # Vitest + Testing Library (API mocked)
npm run typecheck
npm run build
```

Local sign-in: synthetic accounts such as `learner01@example.invalid` with the `DEMO_USER_PASSWORD` from the
repository `.env` (created by `python -m app.seed ... --demo-users --demo-content`). All demo content is labelled DEMO.
Each account can complete the baseline assessment once (reassessment is not available yet).
