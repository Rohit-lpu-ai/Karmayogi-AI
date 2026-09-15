# iGOT Karmayogi — Access Status

**Audit ID:** AUDIT-IGOT-001
**Date:** 2026-09-14
**Subject:** Public resources and integration documentation for iGOT Karmayogi (operated by Karmayogi Bharat)
**Method:** Web search; HTTP checks of the public portals; reading **public open-source code** in the `KB-iGOT` and `sunbird-cb` GitHub organisations via the GitHub API.
**Not done:** No iGOT API endpoint was called, public or private. No credentials were obtained, used, or stored. No personal data was accessed.

Status values follow `STATUS_VOCABULARY.md`. This audit adds one qualifier: **`MACHINE_OBSERVED (source)`** means the fact was read from public source code at a pinned commit. **Source code shows what the software *can* do. It does not show what the production deployment exposes, to whom, or under what terms.**

---

## 1. Answers

| Question | Answer | Status |
|---|---|---|
| Are public APIs documented? | **No official public or partner API documentation was found.** | `UNKNOWN` — not found ≠ does not exist |
| Which functions appear to exist? | Course discovery, enrolment, progress state, completion and certificates, org hierarchy, public assessments (see §3) | `MACHINE_OBSERVED (source)`; deployment `UNKNOWN` |
| Is authentication required? | **Yes, for everything learner-related.** Protected routes use Keycloak. Even the "public" routes call the upstream gateway with a server-held API key. | `MACHINE_OBSERVED (source)` |
| Are sandbox credentials mentioned? | **No.** No sandbox or credentials were found anywhere public. One internal service guide refers to a UAT environment and uses placeholder credentials only. | `MACHINE_OBSERVED (source)` |
| Is course catalogue access public? | **Only a narrow slice.** The one public content-search route is hard-filtered to Live items tagged `Public Course` in the `Case Study` category. No open full-catalogue access was found. | `MACHINE_OBSERVED (source)` |
| Do enrolment and completion data require authorization? | **Yes.** All learner, course, and enrolment routes sit behind Keycloak protection. These are also personal data. | `MACHINE_OBSERVED (source)` |

**Bottom line:** there is no documented route for a third party to integrate with iGOT. Building on the platform's real data would require a formal arrangement with Karmayogi Bharat. Until then, this project builds against `MockIGotClient`.

---

## 2. Official public resources

| Resource | Observed | Status |
|---|---|---|
| `https://www.igotkarmayogi.gov.in/` | Connection timed out from this environment (30 s). | `UNAVAILABLE` from here |
| `https://portal.igotkarmayogi.gov.in/public/faq` | `curl` timed out. Through WebFetch the page is an **empty app shell** titled `iGot`, with no readable content. | `MACHINE_OBSERVED` |
| `https://portal.igotkarmayogi.gov.in/robots.txt` | Connection timed out. | `UNKNOWN` |
| DoPT *Karmayogi Portal User Manual* v1.1 (`trgdiv.dopt.gov.in`, PDF) | HTTP 200, `application/pdf`, 5,549,857 bytes, Last-Modified 2022-11-19. Not opened. It is an end-user manual, not integration documentation. | `MACHINE_OBSERVED` |
| GitHub org **`KB-iGOT`** | 100+ public repositories. Actively maintained (pushes on 2026-09-14). Mixed licences: many MIT, many with no licence declared. | `MACHINE_OBSERVED` |
| GitHub org **`sunbird-cb`** | 74 public repositories. Latest push 2024-09. Appears to be the predecessor of `KB-iGOT`. | `MACHINE_OBSERVED` |

**Other SIH repositories.** Several GitHub repositories from other hackathon teams (for example "StatKarmayogi") came up in search. They are **not official**, were not used as evidence, and must not be mistaken for Karmayogi Bharat documentation.

---

## 3. Functions that appear to exist

Everything below was read from source code. The route strings are what that code defines internally. **They are not a documented public API. They have not been verified as deployed or reachable, and they must not be called.** `clients/` contains no real client for this reason.

Pinned commits:
- `KB-iGOT/sunbird-cb-uiproxy` @ `a75b72277f47962c57d3dd27e58622bdbef43f2b` — the web portal's API proxy
- `KB-iGOT/sunbird-course-service` @ `1be851de8c7e2115f8fa0648868776e233a05694` — course and enrolment backend

### 3.1 How the proxy splits access

`src/server.ts`:

| Line | Mount | Guard |
|---|---|---|
| 190 | `/public/v8` → `publicApiV8` | **none at proxy level** |
| 195 | `/protected/v8` → `protectedApiV8` | `keycloak.protect` |
| 200 | `/proxies/v8` → `proxiesV8` | `keycloak.protect` |

### 3.2 Public-router functions (`src/publicApi_v8/publicApiV8.ts`)

| Function | Notes |
|---|---|
| Public content search | Lines 299–338. Forces `additionalTags: ['Public Course']`, category `Case Study`, and `status: ['Live']` (lines 308–311). **This is a narrow public showcase, not the catalogue.** |
| Organisation list / read / hierarchy search (ministry, state) | Proxied to the upstream gateway |
| Public assessments: question list, read, submit, result (several versions) | Proxied |
| Forms: get form, save submission | Proxied |
| Careers list, tenders list, designation search | |
| Platform consumption counters | Read from cache: live course count, user count, completion counts |
| Hall of fame / wall of fame read | Leaderboards. Likely to contain officer names — **personal data; out of scope** |
| Certificate download (mobile) | |
| SSO flows: Parichay, OIL, NTPC, Google | Login integrations, not data APIs |

Even these "public" handlers call upstream with `Authorization: CONSTANTS.SB_API_KEY` (lines 151, 193, 284, 324). So the upstream gateway expects an API key, which the proxy adds on the server side. The key is read from the environment (`src/utils/env.ts:167`), and the committed default is a placeholder. **An unauthenticated caller cannot reach the upstream gateway directly.**

### 3.3 Protected functions (Keycloak-guarded)

From `src/proxies_v8/proxies_v8.ts`: learner services (`/learner/*`, line 543), course services (`/course/*`, line 1204), CIOS enrolment (`/cios-enroll/*`, line 1378), karma points, course recommendations, and batch participant lists (line 1145). **Batch participant lists return other people's personal data.**

### 3.4 Backend course-service functions (`service/conf/routes`)

| Line | Function | Controller |
|---|---|---|
| 16 | List a user's enrolled courses | `CourseEnrollmentController.getEnrolledCourses` |
| 17 | List a user's enrolled courses (v2) | `CourseEnrollmentController.getUserEnrolledCourses` |
| 18 | Enrol in a course | `CourseEnrollmentController.enrollCourse` |
| 22 | Read content progress state | `LearnerController.getContentState` |
| 24 | Update content progress state | `LearnerController.updateContentState` |
| 60 | Issue course certificate | `CertificateController.issueCertificate` |

The same routes file also defines unenrol, bulk enrol and unenrol, batch read, certificate template add and remove, and collection summary.

**Mapping to what this project needs.** Enrolments come from the enrolled-courses functions. Completions and learning history are most likely *derived* from enrolment status plus content state, because no dedicated "completions" or "learning history" backend function was identified in these routes. The proxy's `learningHistory.model.ts` suggests a history concept exists in the UI layer. Its data source is `UNKNOWN`.

---

## 4. Authentication model (as seen in source)

| Layer | Mechanism | Status |
|---|---|---|
| End user → portal proxy | Keycloak session (cookie) | `MACHINE_OBSERVED (source)` |
| Server → upstream gateway | API key in the `Authorization` header, plus the user's Keycloak token in `x-authenticated-user-token` | `MACHINE_OBSERVED (source)` — see the internal service docs below |
| Government SSO | Parichay integration present | `MACHINE_OBSERVED (source)` |
| Third-party / partner credentials | No issuance process found | `UNKNOWN` |

Corroborating internal documentation in public repositories. These are **per-microservice developer docs, not partner documentation**:

- `KB-iGOT/cb-ext-config-service` @ `4a4915eb5078c1c498f80614115505aa23a43dfc`, `docs/API_DOCUMENTATION.md` and `docs/openapi.json`. The base URL is `localhost`. Endpoints require `x-authenticated-user-token`.
- `KB-iGOT/ai-assessment-service` @ `49d066d37fde89a7676da9a129f91e52ee8a25dd`, `integration/API_INTEGRATION_GUIDE.md`. Server-to-server calls need a Keycloak user JWT **and** a Kong JWT credential. The guide lists **UAT** and Local environments. **All credentials in it are placeholders** (for example `<kong_jwt_credential>`). The UAT hostnames were deliberately not recorded in this repository.

---

## 5. Sandbox credentials

**None found.** Every code-search hit for "sandbox" in `KB-iGOT` was unrelated to credentials. For example, `cbp-ai-service/src/utils/common.py:35` launches Chromium with `--no-sandbox`, and `deterministic-chatbot` refers to expression sandboxing.

A UAT environment exists for internal teams. Nothing public says that third parties can get UAT access or credentials. **Do not look for, request through unofficial channels, or use UAT credentials.** Access has to be granted formally.

---

## 6. Personal data and legal position

Enrolments, completions, progress, and learning history are **personal data** about identifiable civil servants.

- The project's standing rule R3 (`DATA_COLLECTION_CHECKLIST.md`) and `DATA_DICTIONARY.md` §7 exclude personal data. Learner data needs its own separate assessment.
- Any real integration needs a **lawful basis** (for example the Digital Personal Data Protection Act, 2023), **authorization from Karmayogi Bharat**, and either user consent or an institutional mandate.
- The mock client exists so the platform can be designed and demonstrated **without touching any real learner record**.

---

## 7. Evidence that is only secondhand

| Claim | Source | Status |
|---|---|---|
| Platform built on Sunbird; Sunbird RC used for verifiable certificates | Sunbird RC adopters page (search result) | `UNVERIFIED_SECONDHAND` (consistent with the observed repositories) |
| ~2,400 courses in 16 languages; 1 crore+ registered users | News and search summaries | `UNVERIFIED_SECONDHAND` |
| "No back-end sync of the existing LMS onto iGOT; content must be re-created; bulk upload exists" | Third-party webinar page (CEGIS C-LOP) | `UNVERIFIED_SECONDHAND` |
| An integration with SPARROW APAR exists | YouTube video title | `UNVERIFIED_SECONDHAND` — shows government-to-government integrations exist; says nothing about third-party access |
| MDO subscription of INR 432 per employee for the first year | Third-party glossary site | `UNVERIFIED_SECONDHAND` |

---

## 8. Recommended path

| Priority | Action |
|---|---|
| **P1** | Build and demo entirely on `MockIGotClient`. Label it as mock in the UI. |
| **P1** | Write to Karmayogi Bharat asking whether a partner API, data-sharing agreement, or course catalogue feed exists for approved projects, and on what terms. |
| P2 | Ask specifically whether a **course catalogue export** (non-personal metadata) can be shared. This is the lowest-risk integration and the most useful. |
| P2 | Have a human open the portal in a browser and record whether catalogue browsing works without logging in. |
| P3 | Only after written authorization: implement a real `IGotClient` against *documented* endpoints, with credentials from environment variables. |

**Do not** reverse-engineer the portal, replay browser session tokens, scrape the logged-in portal, or call any route listed in §3.

---

## Sources

- [iGOT Karmayogi](https://www.igotkarmayogi.gov.in/)
- [iGOT portal FAQ](https://portal.igotkarmayogi.gov.in/public/faq)
- [Karmayogi Portal User Manual (DoPT)](https://trgdiv.dopt.gov.in/igotmk/ImportantDocuments/User%20manual%20docs%202022Nov/User_Manual%20-%20Karmayogi_Bharat.pdf)
- [KB-iGOT on GitHub](https://github.com/KB-iGOT)
- [KB-iGOT/sunbird-cb-portal](https://github.com/KB-iGOT/sunbird-cb-portal)
- [KB-iGOT/sunbird-cb-uiproxy](https://github.com/KB-iGOT/sunbird-cb-uiproxy)
- [KB-iGOT/sunbird-cb-orgportal](https://github.com/KB-iGOT/sunbird-cb-orgportal)
- [sunbird-cb/sunbird-cb-ext-kb-igot](https://github.com/sunbird-cb/sunbird-cb-ext-kb-igot)
- [Sunbird RC adopters](https://rc.sunbird.org/learn/adopters)
- [Mission Karmayogi — Digital India](https://www.digitalindia.gov.in/initiative/mission-karmayogi/)
- [CEGIS C-LOP webinar: Content development and user onboarding](https://clop.cegis.org/webinars/content-development-and-user-onboarding)
- [iGOT Karmayogi Platform glossary (Model Diplomat)](https://modeldiplomat.com/learn/glossary/igot-karmayogi-platform)
- [SPARROW APAR integration video](https://www.youtube.com/watch?v=gSMSuFib2n8)
- [iGOT crosses 1 crore users (News on AIR)](https://www.newsonair.gov.in/igot-karmayogi-platform-crosses-mark-of-1-cr-registered-civil-servants)
