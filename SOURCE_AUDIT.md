# Source Audit

**Phase:** Discovery
**Status of this document:** Audit framework and empty record. **No source has
been audited.**
**Last updated:** 2026-09-14

---

## 1. Summary of current state

| Metric | Count |
|---|---|
| Sources registered | 24 (23 external + 1 internal mock fixture) |
| Sources audited (`VERIFIED`) | **0** |
| Sources confirmed `UNAVAILABLE` | 0 |
| Sources with a licence confirmed | 0 |
| Sources with an API confirmed to exist | 0 |
| Sources cleared for collection (Gate C) | **0** |
| Bytes collected from any source | **0** |
| Mock fixture sets | 1 (`SRC-024`, marked `MOCK`) |

**Nothing in this repository is derived from a government source.** The source
list was assembled from general knowledge of India's statistical system and
represents *candidates to investigate*, not confirmed facts. Organisation names
and source names are drawn from common usage and are themselves `UNKNOWN` until
a human confirms the current official naming.

---

## 2. Why this audit exists

An AI-enabled learning platform for India's Official Statistical System has an
unusual failure mode: a plausible wrong number is worse than no number. Officials
being trained on this platform will carry what they learn into real statistical
work. So the audit exists to answer four questions before a single byte is
collected:

1. **Does the source exist and is it official?**
2. **Are we permitted to use it, and on what terms?**
3. **Does it contain personal data we must not touch?**
4. **Is the data good enough to teach from, and do we understand its caveats?**

A source that fails (2) or (3) is dropped regardless of how useful it would be.

---

## 3. Audit template

Copy this block into §5 for each source as it is audited. Do not shorten it.

```
### <SRC-0XX> — <Source name>

Auditor:            <name>
Audit date:         <YYYY-MM-DD>
Reviewer:           <name>
Review date:        <YYYY-MM-DD>
Overall status:     UNKNOWN | VERIFIED | UNAVAILABLE

A. IDENTITY
  Publishing body:              UNKNOWN
  Official homepage:            UNKNOWN
  Confirmed official? :         UNKNOWN     (how confirmed: )
  Actively maintained? :        UNKNOWN     (evidence: )
  Last observed update:         UNKNOWN

B. ACCESS
  Documented API:               UNKNOWN
  Bulk download:                UNKNOWN
  Query/form download:          UNKNOWN
  PDF only:                     UNKNOWN
  Chosen access method:         UNKNOWN
  Justification:                UNKNOWN

C. LEGAL
  Terms of use URL:             UNKNOWN
  Licence (verbatim):           UNKNOWN
  Attribution required:         UNKNOWN
  Attribution string:           UNKNOWN
  Redistribution allowed:       UNKNOWN
  Derivatives allowed:          UNKNOWN
  Caching / re-serving allowed: UNKNOWN
  robots.txt directives:        UNKNOWN
  Rate limit / fair use:        UNKNOWN
  Legal risk assessment:        UNKNOWN

D. PRIVACY  (blocking — must be clean to proceed)
  Contains microdata:           UNKNOWN
  Contains direct identifiers:  UNKNOWN
  Re-identification risk:       UNKNOWN
  Tables we intend to use:      UNKNOWN
  Personal data excluded? :     UNKNOWN
  Screen outcome:               UNKNOWN   (PASS / FAIL / UNKNOWN)

E. QUALITY AND FITNESS
  Formats offered:              UNKNOWN
  Metadata completeness:        UNKNOWN
  Methodology documented:       UNKNOWN
  Revision policy documented:   UNKNOWN
  Temporal coverage:            UNKNOWN
  Geographic granularity:       UNKNOWN
  Publication lag:              UNKNOWN
  Known breaks in series:       UNKNOWN
  Known caveats:                UNKNOWN
  Teaching value (1-5):         UNKNOWN
  Collection effort (1-5):      UNKNOWN

F. EVIDENCE
  Evidence directory:           docs/evidence/<SRC-0XX>/
  Files saved:                  none
  Screenshots:                  none

G. DECISION
  Recommendation:               UNKNOWN   (PROCEED / DEFER / DROP)
  Rationale:                    UNKNOWN
  Gate C sign-off (owner):      UNSIGNED
  Gate C sign-off (reviewer):   UNSIGNED
```

---

## 4. Risk register

Risks identified from the shape of the problem, before any source contact.
All are `ASSUMED` — reasoned expectations, not observed facts.

| # | Risk | Status | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| RK-01 | No usable API exists for most P1 sources; data is PDF or portal-only | ASSUMED | Medium | High | Budget for manual curation of a small, high-value indicator set rather than broad automated coverage |
| RK-02 | Licences do not clearly permit caching and re-serving inside a platform | ASSUMED | Medium | Critical | Resolve early (Q3 in API_REQUIREMENTS). If unclear, seek written permission before building |
| RK-03 | Geography codes are inconsistent across sources and across time | ASSUMED | High | High | Keep source codes verbatim; build a dated crosswalk; never silently map |
| RK-04 | Financial-year and survey-round periods get mangled by naive date normalisation | ASSUMED | High | Medium | `period_label` retains the source's own label (DATA_DICTIONARY §5.3) |
| RK-05 | Revisions overwrite earlier figures, so the platform shows a number that contradicts a published report | ASSUMED | Medium | High | Model `estimate_vintage` and `supersedes_observation_id` from the start |
| RK-06 | A contributor or an AI assistant invents an endpoint or a figure that looks plausible | ASSUMED | **High** | **Critical** | The `VERIFIED`-only rule; AI assistants may never set `VERIFIED`; endpoint columns stay `UNKNOWN` until a human reads official docs |
| RK-07 | Microdata is downloaded "just to look" and personal data enters the repository | ASSUMED | Medium | Critical | Gate B5 is blocking; validators fail the build on person-level fields |
| RK-08 | Portal URLs change and break the pipeline silently | ASSUMED | High | Medium | Record retrieval dates; re-verify on a schedule; fail loudly, never fall back to stale data silently |
| RK-09 | Automated requests are read as abusive by a government portal | ASSUMED | Low | Critical | No scraping this phase; identify ourselves; stay well under documented limits |
| RK-10 | Mock data leaks into learner-facing content | ASSUMED | Medium | Critical | Mock data is directory-isolated, self-labelled, implausible by construction, and blocked from `data/processed/` |
| RK-11 | Under SIH time pressure, gates are skipped to demo something | ASSUMED | **High** | High | Demo on `MOCK` data, clearly labelled. A labelled mock demo is honest; an unlabelled real-looking one is not |
| RK-12 | The platform teaches a figure without its caveat and an official repeats it | ASSUMED | Medium | High | Caveats and methodology links are required fields, not optional decoration |

---

## 5. Audit records

*No audits completed. Each source below is at Gate A with every substantive
field `UNKNOWN`. Records are added here using the §3 template as audits are
performed.*

| source_id | Source | Auditor | Audit date | Privacy screen | Licence | Recommendation | Overall |
|---|---|---|---|---|---|---|---|
| SRC-001 | MoSPI portal | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-002 | NSS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-003 | PLFS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-004 | CPI | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-005 | IIP | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-006 | National Accounts | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-007 | ASI | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-008 | eSankhyiki | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-009 | NDAP | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-010 | OGD Platform | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-011 | RBI / DBIE | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-012 | Census of India | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-013 | SRS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-014 | CRS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-015 | NFHS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-016 | UDISE+ | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-017 | AISHE | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-018 | Agri statistics | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-019 | Trade statistics | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-020 | Labour Bureau | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-021 | NSC reports | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-022 | NIC / NCO / NPCMS | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-023 | SDG NIF | — | — | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| SRC-024 | Mock fixtures | — | 2026-09-14 | NOT_APPLICABLE | INTERNAL | Internal use only | MOCK |

---

## 6. Suggested audit order

Rationale, not instruction. Adjust once real findings arrive.

1. **Aggregator portals first** — SRC-009 (NDAP), SRC-010 (OGD), SRC-008
   (eSankhyiki). If one of these covers enough P1 indicators under a workable
   licence, the integration surface shrinks dramatically. This is the highest
   information-gain move available.
2. **Then the flagship indicators** — SRC-004 (CPI), SRC-005 (IIP), SRC-006 (NAS).
   High teaching value, monthly or annual cadence, well-documented revision
   practice.
3. **Then the structural references** — SRC-012 (Census), SRC-022
   (classifications). Needed as denominators and vocabularies for everything else.
4. **Then the remainder** by priority.

Audit SRC-002 (NSS) and SRC-007 (ASI) only after the microdata boundary is
settled in writing, because that is where the privacy risk concentrates.

---

## 7. Sign-off

This document is unsigned. It becomes meaningful only when real auditors put
real names and real dates against real sources.

| Role | Name | Date | Signature |
|---|---|---|---|
| Data lead | UNASSIGNED | — | — |
| Privacy reviewer | UNASSIGNED | — | — |
| Project lead | UNASSIGNED | — | — |
