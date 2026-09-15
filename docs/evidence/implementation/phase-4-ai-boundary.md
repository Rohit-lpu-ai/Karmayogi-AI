# Phase 4 - AI capability boundary and external-provider analysis

Status: **No external AI is connected.** No API keys are used or requested. This document is the analysis the Phase 4 brief asked for before any provider decision. It records what each capability would need; it is not a decision.

## 1. What exists now

`backend/app/modules/ai/interfaces.py` defines six narrow interfaces. `backend/app/modules/ai/local.py` implements each one with fixed rules. Every result carries a `method` so that nothing rule-based can be shown as AI.

| Interface | Local implementation (`method`) | Where it is used today |
|---|---|---|
| `CompetencyInterpreter` | `TemplateCompetencyInterpreter` (`template-v1`): fills a sentence from the competency name and level description | Not wired into screens yet |
| `RecommendationExplainer` | `TemplateRecommendationExplainer` (`template-v1`): restates the `rec-v1` inputs (estimated level, required level, relevance) | Not wired; screens already build the same sentence from API data |
| `LearningContentRetriever` | `KeywordContentRetriever` (`keyword-v1`): term overlap over published lesson titles and bodies, title matches weighted double | Not wired |
| `QuestionGenerator` | `NoQuestionGenerator` (`not-available`): returns nothing | Not wired; authoring is fully human |
| `QuestionValidator` | `StructuralQuestionValidator` (`structure-v1`): option count, one correct answer, duplicates, "all/none of the above", negative wording, give-away option length, short explanation | Question detail screen ("Wording and structure checks - fixed rules, not AI") |
| `LearningTutor` | `RetrievalOnlyTutor` (`retrieval-only-v1`): points to matching lessons, never writes an answer; declines when nothing matches | Not wired |

Tests: `backend/tests/unit/test_ai_local.py` (interface conformance, determinism, method labelling).

## 2. What an external provider would add, and what it would need

"Provider" below means a hosted large-language-model API (for example Google Gemini, OpenAI, Anthropic, or an Azure/Google Cloud-hosted equivalent) or a self-hosted open-weights model. No provider has been chosen.

| Capability | Needs an external model? | Data that would be sent | What stays local | Main privacy and quality implications |
|---|---|---|---|---|
| Competency interpretation | Optional. Templates are adequate for synthetic content | Competency name, level label and description (no personal data) | Frameworks, requirements, scoring | Licence-restricted frameworks (CSCD) must never be sent: their definitions may not be reproduced. Output must be reviewed before learners see it |
| Recommendation explanation | No. The rule is deterministic; a model adds fluency only | Competency, levels, course title | The ranking itself (`rec-v1`) | Risk of the model inventing reasons that the rule did not use. If used, the explanation must be checked against the rule's reasons |
| Content retrieval (RAG) | Yes for semantic search (embedding model); keyword search works without | Lesson text and the learner's query; embeddings of published lessons | Lesson storage, access control, the list of passages a learner may see | pgvector is already in the database image, so embeddings can be stored locally. Queries can contain personal context; retention and logging at the provider must be contractually controlled |
| Question generation | Yes | Competency description, difficulty, possibly source excerpts | Review workflow, approval, publication | Drafts only, always through the human review in Phase 4C. Source excerpts from restricted or unverified documents must not be sent. Generated questions need the source metadata rules like human ones |
| Question validation (semantic) | Optional. Structural checks work locally | Question text and options | The decision (humans approve) | Findings must stay advisory. Must not see the answer key unless the provider's data handling is approved |
| Learning tutor | Yes | Learner question, retrieved lesson passages, possibly conversation history | Identity, progress, estimates | Highest risk: personal data in free text, hallucinated statistics, over-reliance. Needs grounding-only answers with citations to lessons, refusal rules, moderation, age/role checks, and logging without content |

## 3. What a provider integration would require before it is switched on

1. A recorded decision (DECISIONS.md) per capability: provider, model, region, retention, cost limit.
2. A data-processing agreement covering Indian public-sector data handling, no training on submitted data, and deletion.
3. Configuration through environment variables only, for example `AI_PROVIDER` (`local` default), `AI_API_KEY` (secret, never logged), `AI_MODEL`, `AI_REGION`, `AI_MAX_TOKENS_PER_DAY`. Keys are read once at startup, excluded from logs by the existing redaction, and never sent to the browser.
4. A redaction step before any call: strip names, emails, registration IDs and free-text personal data.
5. An evaluation set (synthetic) with pass criteria per capability, run in CI with the local implementation as the fallback.
6. A kill switch that reverts every capability to the local implementation.
7. UI labelling: any generated text marked as AI-assisted and reviewable; nothing generated reaches learners without human review, except tutor answers, which must quote lesson passages.

## 4. Question for the product owner

External AI is out of scope until you decide. Please confirm, per capability, whether to plan a provider integration, and which provider constraints apply (for example "Government-hosted only", "no personal data leaves India"). Until then the platform stays fully local.
