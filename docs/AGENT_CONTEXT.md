# Agent Context

| Field | Value |
|---|---|
| **Version** | 1.0.0 |
| **Audience** | Human contributors and AI coding agents working in this repository |
| **Last updated** | 2026-09-14 |
| **Related** | [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [DECISIONS.md](DECISIONS.md) · [../STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md) |

This file was **missing** when implementation started, although PRD, MVP_SCOPE, TECH_STACK, DATA_MODEL and DECISIONS cite it ("agent rule 1", "rule 14", "rule 19", "§5"). It was generated on 2026-09-14 so those references resolve (DEC-032). Rule numbers are fixed; new rules are appended, never renumbered.

## 1. What this product is

An AI-assisted competency intelligence and personalised learning platform for India's official statistical system. It helps officials see what their job role requires, estimate where they stand from assessment evidence, get relevant learning, and use source-grounded AI for document Q&A and draft assessment questions.

**AI is assistive.** It never makes employment decisions, never assigns competency scores, and never publishes content without human approval.

## 2. Sources of truth

| Question | Authoritative document |
|---|---|
| What the product must do | [PRD.md](PRD.md) |
| What may be built now | [MVP_SCOPE.md](MVP_SCOPE.md) (P0 only) |
| Feature details and IDs | [FEATURE_CATALOG.md](FEATURE_CATALOG.md) (generated; edit `scripts/docs/registry_*.py`) |
| Order of work and exit criteria | [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) |
| What exists today, with evidence | [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) |
| Module boundaries and flows | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) |
| Database schema | [DATA_MODEL.md](DATA_MODEL.md) |
| Platform API | [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) |
| AI behaviour | [AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) |
| Security, RBAC, responsible AI | [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) |
| Screens | [UI_UX_SPEC.md](UI_UX_SPEC.md) |
| Decisions and conflicts | [DECISIONS.md](DECISIONS.md) |
| Dataset status labels | [../STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md) |
| External sources and iGOT access | [../API_REQUIREMENTS.md](../API_REQUIREMENTS.md), [../IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md) |

When documents disagree with each other or with the repository, **stop and record the conflict in DECISIONS.md**. Do not silently pick one.

## 3. Rules

### Scope

1. **Build only P0 features** listed in MVP_SCOPE.md. No P1/P2 feature may be implemented, stubbed into production routes, or exposed in the UI without an explicit recorded approval.
2. Do not implement predictive workforce intelligence, skill-demand forecasting, knowledge tracing, BKT, IRT, voice, offline mode, a mobile app, career-path prediction, a real iGOT integration, autonomous evaluation, or any promotion or appraisal logic.
3. Do not add a dependency without a stated purpose mapped to a feature ID and a record in TECH_STACK.md (§18 admission rules).

### Architecture

4. The backend is a **modular monolith** (`backend/app/modules/<module>/`). A module calls another module only through its `service.py`, never its models or repository.
5. **Authorisation is enforced on the server** on every route through the policy dependency. The frontend only hides controls.
6. All LLM access goes through `LLMProvider`; all embedding access through `EmbeddingProvider`. No provider SDK is imported outside `ai/providers/`.
7. iGOT access goes only through `IGotClient`. The mock is labelled MOCK everywhere, never persisted as application data, and never reports `connected`.
8. Never invent government or iGOT endpoints, URLs, or deep-link patterns.

### Security and privacy

9. Never hardcode secrets. Configuration comes from environment variables through the settings module; `.env` stays git-ignored.
10. Never log passwords, tokens, cookies, session IDs, raw document text, answer content or personal data. Use the redacting logger.
11. Every tenant-scoped query filters by `organization_id`.
12. Uploaded files and extracted text are **untrusted**: validate before storage, never execute, and wrap as data in prompts.
13. Do not reproduce licence-restricted content (for example CSCD definitions or behavioural indicators).

### Change discipline

14. **Do not delete working code or tests merely to match the documentation.** Move and adapt them; record the change in DECISIONS.md.
15. Work in small, reviewable increments. No uncontrolled rewrites.
16. Before each phase: state intended changes, affected files, database changes, API changes and risks.
17. After each phase: run all tests, report failures honestly, update documentation, summarise.
18. Never claim a feature is implemented without evidence (file path and a passing test).

### Data

19. **Alembic migrations are the only way to change the schema.** Applied migrations are never edited; fixes are new revisions. DATA_MODEL.md is updated in the same change.
20. Never build a model from documentation alone: compare it with the canonical datasets and record naming or type differences.
21. Preserve provenance: source URL, organisation, retrieval date, SHA-256 and `data_status` survive every import.
22. Never mark anything `VERIFIED`. Only humans do that ([../STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md)).
23. Seed imports run the canonical dataset validator first and refuse an `INVALID` verdict. Mock fixtures are never imported into tables.

### AI

24. Every AI operation: validate inputs, use structured outputs, re-validate output schemas, store model and prompt-version metadata, store source references, store validation status, log the interaction before returning output, apply timeouts and bounded retries.
25. Grounded outputs carry verified citations or the system abstains. Page numbers are never fabricated.
26. Every AI-generated question carries source metadata and needs human approval before any learner sees it.
27. Competency scores, gaps, recommendations and learning paths are **deterministic**. No LLM participates.
28. Language about people is development-oriented ("developing", "reassess to confirm"), never evaluative ("weak", "failed").

### Testing

29. Every module adds unit, API, validation, authorisation and failure-path tests; database tests where it touches the schema; AI output-schema tests where it calls a provider.
30. Tests use deterministic fake AI providers. No test sends data to an external provider.
31. A phase is not complete until its exit criteria in IMPLEMENTATION_ROADMAP.md hold and its tests pass.

## 4. Documentation rules

- Update [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) at the end of every phase, citing file paths and test commands.
- API changes update [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md); schema changes update [DATA_MODEL.md](DATA_MODEL.md).
- Feature implementation status lives in `scripts/docs/registry_*.py`; regenerate FEATURE_CATALOG.md with `python scripts/docs/generate_feature_catalog.py` rather than editing it by hand.
- Record every new decision or conflict in [DECISIONS.md](DECISIONS.md) with the next free number.

## 5. Current implementation status (summary)

Detail and evidence: [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).

| Area | Status |
|---|---|
| Canonical datasets, validator, collectors | Implemented (Phase 1, offline tooling) |
| iGOT client interface | Implemented (`clients/igot_client.py`) |
| iGOT client | Mocked (`clients/mock_igot_client.py`) |
| Backend application | Phase 2 complete (local); vertical slice 1 implemented |
| Frontend application | Partially implemented (vertical slice 1: login, onboarding, assessment, result, dashboard) |
| Authentication, RBAC, audit | Partially implemented (sessions, CSRF, lockout, role guard for slice endpoints) |
| Competency engine, assessments | Partially implemented (deterministic `score-v1`, gaps; DEMO content only) |
| Content pipeline, RAG, AI providers | Missing |
| Recommendations, learning paths | Recommendations partially implemented (`rec-v1`, computed on read); learning paths missing |

## 6. How to run things

| Task | Command |
|---|---|
| Existing dataset and mock tests | `python -m unittest discover -s tests -t .` |
| Validate canonical datasets | `python scripts/validators/validate_canonical_datasets.py` |
| Backend tests | `cd backend && python -m pytest` (see `backend/README.md`) |
| Apply migrations | `cd backend && alembic upgrade head` |
| Seed with demo content (local) | `cd backend && .venv/Scripts/python -m app.seed --org-code local-demo --org-name "Local development organisation" --demo-users --demo-content` |
| Frontend tests and build | `cd frontend && npm test && npm run build` |
