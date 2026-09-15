# API Requirements

**Phase:** Discovery
**Status of this document:** Requirements definition. **Contains no endpoints.**
**Last updated:** 2026-09-14

---

## 0. Non-negotiable rule for this file

> **No API endpoint, path, parameter name, header, or base URL appears in this
> repository unless a named human has read it in official documentation, recorded
> the documentation URL and the date, and marked it `VERIFIED`.**

Every endpoint column below is deliberately empty and reads `UNKNOWN`. That is
not an oversight — it is the accurate state of our knowledge on 2026-09-14. An
assistant, a teammate, or a future contributor filling these in from memory or
from a plausible-looking guess is the single most damaging thing that can happen
to this project, because a wrong endpoint that returns *something* is worse than
one that returns nothing.

This document instead defines **what we need an API to do**, so that when someone
does open the real documentation, they know exactly what to look for.

---

## 1. What this platform needs from a data source

The learning platform teaches India's official statistics. It needs to show
learners real indicators, real revisions, real metadata, and real caveats.

### 1.1 Functional requirements

| ID | Requirement | Priority | Why the platform needs it |
|---|---|---|---|
| FR-01 | Retrieve a named indicator as a time series | Must | The core teaching object is a series over time. |
| FR-02 | Filter by time period (from / to) | Must | Lessons target specific windows. |
| FR-03 | Filter by geography (national / state / district) | Must | Sub-national comparison is a core skill being taught. |
| FR-04 | Retrieve the unit of measurement with the value | Must | A number without a unit is not teachable. |
| FR-05 | Retrieve the base year / reference period where the indicator is an index | Must | Index rebasing is itself a lesson. |
| FR-06 | Distinguish provisional, revised, and final estimates | Must | Revision practice is a core curriculum topic. |
| FR-07 | Retrieve the publication date of the figure | Must | Needed to explain lags and to cache correctly. |
| FR-08 | Machine-readable listing of available indicators (a catalogue) | Must | We cannot hand-maintain a catalogue of hundreds of series. |
| FR-09 | Distinguish missing-value reasons (not collected / not applicable / suppressed / not yet published) | Should | Teaching learners to read missing data correctly. |
| FR-10 | Retrieve methodology notes or a link to them | Should | Every indicator page should carry its caveats. |
| FR-11 | Retrieve disaggregations (sex, rural/urban, sector) | Should | Disaggregation is a key statistical literacy topic. |
| FR-12 | Stable identifiers for indicators across releases | Should | Otherwise our lesson content silently breaks. |
| FR-13 | Notification or changelog of new releases | Could | Would let content stay current automatically. |
| FR-14 | Bulk export of a whole dataset | Could | Cheaper than paginating for static course content. |

### 1.2 Non-functional requirements

| ID | Requirement | Target | Notes |
|---|---|---|---|
| NFR-01 | Response format | JSON preferred; CSV acceptable; XML tolerable | HTML-only means scraping, which we are not authorising in this phase. |
| NFR-02 | Character encoding | UTF-8, declared | Devanagari and other Indic scripts must round-trip intact. |
| NFR-03 | Multilingual labels | Hindi and English at minimum | The platform serves officials across states. |
| NFR-04 | Authentication | Documented, obtainable by a legitimate project | Method `UNKNOWN` for every source. |
| NFR-05 | Rate limits | Documented and honoured with margin | We will run well below any stated limit. |
| NFR-06 | Pagination | Deterministic and stable under concurrent updates | Otherwise bulk pulls silently skip rows. |
| NFR-07 | Versioning | API version in the contract | Protects us from silent breaking changes. |
| NFR-08 | HTTPS with a valid certificate | Required | No exceptions, no verification disabling. |
| NFR-09 | Availability | Best effort; we must cache | Public portals have maintenance windows. |
| NFR-10 | Licence permits caching and re-serving to learners | Required | Determines whether the platform is viable at all. |

### 1.3 Metadata requirements

Any source we build on must let us populate, for every value we display:
indicator name, indicator ID, unit, geography, geography code, time period,
period type, estimate vintage, source organisation, publication date,
retrieval date, licence, and attribution string. See `DATA_DICTIONARY.md`.

If a source cannot supply these, we may still use it, but the gap is recorded as
`UNKNOWN` and shown to the learner as unknown. We do not fill gaps with guesses.

---

## 2. Per-source capability matrix — CURRENT STATE

Every cell below is `UNKNOWN` because no source has been investigated yet.
Fill in only from official documentation, following `DATA_COLLECTION_CHECKLIST.md`
Gate B3.

| source_id | Source | API exists? | Docs URL | Base URL | Auth | Formats | Rate limit | Meets FR-01..08? | Status |
|---|---|---|---|---|---|---|---|---|---|
| SRC-001 | MoSPI portal | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-002 | NSS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-003 | PLFS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-004 | CPI | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-005 | IIP | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-006 | National Accounts | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-007 | ASI | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-008 | eSankhyiki | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-009 | NDAP | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-010 | OGD Platform | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-011 | RBI / DBIE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-012 | Census of India | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-013 | SRS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-014 | CRS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-015 | NFHS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-016 | UDISE+ | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-017 | AISHE | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-018 | Agri statistics | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-019 | Trade statistics | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-020 | Labour Bureau | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-021 | NSC reports | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-022 | NIC / NCO / NPCMS | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-023 | SDG NIF | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-024 | Mock fixtures | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | JSON | NOT_APPLICABLE | Partially, by construction | MOCK |

---

## 3. How to fill in a row (procedure)

1. Open the source's official site by hand in a browser.
2. Find a page that *the site itself* labels as API documentation, developer
   documentation, or data access.
3. Save a copy or screenshot to `docs/evidence/<source_id>/`.
4. Record, verbatim: base URL, auth mechanism, formats, rate limit, version.
5. Record the documentation URL and today's date.
6. Assess FR-01 to FR-08 against what the documentation actually states — not
   what it implies, and not what a similar portal does.
7. Set the row status to `VERIFIED`, and add your name in `SOURCE_AUDIT.md`.
8. If there is no API: set `API exists?` to `UNAVAILABLE`, state what access does
   exist, and stop. Do not go looking for undocumented endpoints in network
   traffic — an undocumented endpoint is not a contract and using one is not
   authorised.

---

## 4. Client design constraints (applies to `clients/`)

These apply to any client we eventually write, and are fixed now so that the
code cannot quietly drift into bad practice.

| ID | Constraint |
|---|---|
| C-01 | All base URLs, keys, and paths come from configuration, never hard-coded in a module. |
| C-02 | Configuration is read from `registry/source_registry.csv` plus environment variables. A client with no `VERIFIED` config refuses to run. |
| C-03 | Secrets live in environment variables or a local `.env` that is git-ignored. No key is ever committed. |
| C-04 | Every client sends a descriptive User-Agent identifying the project and a contact address. |
| C-05 | Every client honours the documented rate limit with a safety margin, and backs off exponentially on 429 and 5xx. |
| C-06 | Every client caches responses locally and prefers the cache during development. |
| C-07 | Every client writes the raw response to `data/raw/` unmodified before any parsing. |
| C-08 | Clients are read-only. No client ever issues a write method against a government system. |
| C-09 | TLS verification is never disabled. |
| C-10 | A client refuses to run against a source whose registry `record_status` is not `VERIFIED` and whose Gate C sign-off is absent. |
| C-11 | No client requests, parses, stores, or logs personal data. If a response unexpectedly contains person-level fields, the client aborts and raises. |
| C-12 | `MOCK` clients are named with a `mock_` prefix and can never be selected by a production code path. |

---

## 5. Open questions

Tracked here until answered. All currently `UNKNOWN`.

| # | Question | Status | Blocks |
|---|---|---|---|
| Q1 | Does any single portal cover enough P1 indicators to be our primary source? | UNKNOWN | Architecture |
| Q2 | Do any of the sources require an API key, and can this project legitimately obtain one? | UNKNOWN | Everything downstream |
| Q3 | Do the licences permit us to cache official figures and re-serve them inside a learning platform? | UNKNOWN | Project viability |
| Q4 | Are geography codes consistent across sources, or do we need a crosswalk? | UNKNOWN | Data model |
| Q5 | How are revisions and estimate vintages exposed, if at all? | UNKNOWN | FR-06 |
| Q6 | Is Hindi-language metadata available, or must we translate? | UNKNOWN | NFR-03 |
| Q7 | What is the realistic publication lag per indicator? | UNKNOWN | Content freshness claims |
| Q8 | Is there an official contact route for a data access request? | UNKNOWN | Fallback if no API exists |

---

## 6. iGOT Karmayogi integration requirements

**Added:** 2026-09-14. **Evidence:** `IGOT_ACCESS_STATUS.md` (AUDIT-IGOT-001).

iGOT is a different kind of source from sections 1–5. It is not official statistics. It is a **learning platform holding personal learner records**. The requirements below stand apart from the statistical-data requirements above.

### 6.1 Current state

| Item | State | Status |
|---|---|---|
| Documented public or partner API | None found | `UNKNOWN` |
| Documented base URL | None | `UNKNOWN` — **none may be recorded** |
| Authentication | Keycloak user token plus server-side gateway API key (seen in source code) | `MACHINE_OBSERVED (source)` |
| Sandbox / test credentials for third parties | None found | `UNKNOWN` |
| Public course catalogue | Only a filtered "Public Course / Case Study" search exists in source | `MACHINE_OBSERVED (source)` |
| Enrolment and completion data | Behind Keycloak; personal data | `MACHINE_OBSERVED (source)` |
| **Integration mode in use** | **`MockIGotClient` only** | `MOCK` |

### 6.2 Functional requirements

What the platform needs from iGOT. The capabilities listed are what we would *request* from Karmayogi Bharat. They are not endpoints known to exist.

| ID | Capability | Interface method | Data class | Priority |
|---|---|---|---|---|
| IG-FR-01 | List courses with metadata (title, provider, competencies, duration, language) | `list_courses()` | Non-personal | Must |
| IG-FR-02 | Read one course's detail | `get_course(course_id)` | Non-personal | Must |
| IG-FR-03 | List one user's enrolments with progress | `get_user_enrollments(user_id)` | **Personal** | Should |
| IG-FR-04 | List one user's completions with completion date and certificate reference | `get_user_completions(user_id)` | **Personal** | Should |
| IG-FR-05 | Read one user's learning history (enrol / progress / complete events) | `get_learning_history(user_id)` | **Personal** | Could |
| IG-FR-06 | Filter courses by competency and by provider (for example NSSTA / MoSPI) | `list_courses(...)` filters | Non-personal | Should |

**Sequencing:** IG-FR-01, 02 and 06 (catalogue, non-personal) come first and are the only ones worth asking for initially. IG-FR-03 to 05 need everything in 6.4 first.

### 6.3 Non-functional requirements

| ID | Requirement |
|---|---|
| IG-NFR-01 | Endpoints, auth flow and rate limits must come from **documentation issued by Karmayogi Bharat**, never from reading portal source code or network traffic. |
| IG-NFR-02 | Credentials are supplied only through environment variables (`IGOT_*`, see `.env.example`). They are never committed, logged, or written to `data/`. |
| IG-NFR-03 | User-scoped methods act only **on behalf of the authenticated user themself** (delegated token), or under a written institutional mandate. No bulk export of other users' records. |
| IG-NFR-04 | The client interface is fixed now (`clients/igot_client.py`). Mock and real implementations are interchangeable without changes to calling code. |
| IG-NFR-05 | Selecting a real client requires an explicit `IGOT_CLIENT_MODE=live` together with verified configuration. The default is `mock`. |
| IG-NFR-06 | Every returned record carries `data_status`. Mock records are `MOCK` and must be visibly labelled anywhere they are displayed. |
| IG-NFR-07 | Learner data received from a real integration is minimised (only the fields listed in 6.2), is not copied into `data/processed/`, and has a documented retention period. |

### 6.4 Preconditions for any live integration

All must be `VERIFIED` by a human before a real client is written:

- [ ] Written authorization or agreement from Karmayogi Bharat
- [ ] Official API documentation received (base URL, auth, rate limits, terms)
- [ ] Credentials issued through an official process, stored outside source control
- [ ] Lawful basis for processing learner personal data documented (DPDP Act, 2023)
- [ ] Consent or mandate model defined for IG-FR-03 to IG-FR-05
- [ ] Privacy review signed (separate from the statistical-data Gate C)

### 6.5 Open questions for Karmayogi Bharat

| # | Question | Status |
|---|---|---|
| IQ1 | Is there a partner or third-party API programme, and how does an approved project apply? | UNKNOWN |
| IQ2 | Can non-personal course catalogue metadata be shared as an API or a periodic export? | UNKNOWN |
| IQ3 | Is a test / UAT environment available to approved partners? | UNKNOWN |
| IQ4 | What consent model applies to a learner sharing their own iGOT records with another platform? | UNKNOWN |
| IQ5 | Can courses be filtered by provider (NSSTA / MoSPI) and by competency framework? | UNKNOWN |
