"""Feature registry: O (Reporting), P (Security), Q (Responsible AI), R (Automation), S (UX), T (Future)."""

from registry_common import F, category, IMPL, PART, MOCK, PLAN, BLOCK, HUMAN

API = "Planned internal API (docs/API_INTEGRATION_SPEC.md): "


def batch(rows):
    for r in rows:
        fid, name, p, d, v, data, ai, api, ui, fail, acc, fut, *extra = r
        kwargs = extra[0] if extra else {}
        F(fid, name, p, d, v, data, ai, API + api, ui, fail, acc, fut, **kwargs)


# ------------------------------------------------------------ O. REPORTING
category(
    "O", "REP", "Reporting", "Reporting",
    "Training manager", "Department administrator; Learner (own reports); System auditor",
    "SEC-002 (RBAC); AUT-012 (background jobs)",
    "Reports are decision support; any report about an individual is visible to that individual on request.",
    "Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.",
    "Reports available as accessible HTML views before export; exports include headers and units.",
)

batch([
    ("REP-001", "Employee report", "P0", "Individual development report: role, estimates with bands, gaps, path progress, assessment history.", "Structured view for learner and trainer conversations.", "Profile; gaps; progress; attempts.", "None.", "POST /api/v1/reports (type=learner_development); GET /api/v1/reports/{id}", "Reports screen; 'Download my report' on profile.", "Generation failure -> job retry and error state.", "Report shows evidence bands and limitations; learners can always generate their own report; access by others is scoped and audited.", "PDF export (REP-010).", {"primary": "Learner", "secondary": "Trainer; Training manager", "security": "Titled 'Learner development report'; carries a notice that it is not an appraisal instrument (SECURITY_RESPONSIBLE_AI.md §HID)."}),
    ("REP-002", "Department report", "P1", "Aggregated department capability and progress report.", "Department-level planning.", "Aggregates.", "None.", "POST /api/v1/reports (type=department, P1)", "Reports screen.", "Small groups -> suppressed.", "Minimum group-size suppression applied.", "Scheduled reports (REP-013).", {"primary": "Department administrator"}),
    ("REP-003", "Competency-gap report", "P0", "Gap list for a learner (own) or scoped learners, with evidence bands.", "Actionable gap export.", "Gaps.", "None.", "POST /api/v1/reports (type=competency_gaps)", "Reports screen.", "No gaps data -> empty report with explanation.", "Only gaps with sufficient evidence included; insufficient-evidence competencies listed separately.", "Department gap report (P1)."),
    ("REP-004", "Assessment report", "P0", "Results of an assessment for a learner, or aggregate for an assessment (scoped).", "Assessment follow-up.", "Attempts.", "None.", "POST /api/v1/reports (type=assessment)", "Reports screen.", "Aggregate below minimum size -> suppressed.", "Individual results visible only within scope; aggregates suppressed below minimum size.", "Item analysis (ANA-015).", {"primary": "Trainer"}),
    ("REP-005", "Quiz report", "P1", "Practice quiz outcomes.", "Practice insight.", "Attempts.", "None.", "POST /api/v1/reports (type=quiz, P1)", "Reports screen.", "As REP-004.", "As REP-004.", "None."),
    ("REP-006", "Course-effectiveness report", "P1", "See ANA-008.", "See ANA-008.", "See ANA-008.", "See ANA-008.", "POST /api/v1/reports (type=course_effectiveness, P1)", "Reports screen.", "See ANA-008.", "See ANA-008.", "See ANA-008.", {"alias_of": "ANA-008"}),
    ("REP-007", "Progress report", "P0", "Learning path and item progress for a learner or scoped group.", "Tracks development activity.", "Progress records.", "None.", "POST /api/v1/reports (type=progress)", "Reports screen.", "As REP-001.", "Self-reported completions labelled.", "Scheduled delivery."),
    ("REP-008", "Improvement report", "P1", "Before-vs-after report (see PRO-008).", "See PRO-008.", "See PRO-008.", "See PRO-008.", "POST /api/v1/reports (type=improvement, P1)", "Reports screen.", "See PRO-008.", "See PRO-008.", "See PRO-008."),
    ("REP-009", "Training recommendation report", "P1", "Aggregated recommended training needs.", "Programme planning.", "Aggregated gaps; recommendations.", "None.", "POST /api/v1/reports (type=training_needs, P1)", "Reports screen.", "Low data -> caveat.", "Aggregate-only with caveats.", "TRN-015."),
    ("REP-010", "PDF export", "P1", "PDF rendering of reports.", "Shareable formal documents.", "Report data.", "None.", "GET /api/v1/reports/{id}/download?format=pdf (P1)", "Download menu.", "Rendering failure -> CSV offered.", "PDFs are tagged for accessibility.", "Watermarking."),
    ("REP-011", "Excel export", "P1", "XLSX exports.", "Analysis in spreadsheets.", "Report data.", "None.", "GET /api/v1/reports/{id}/download?format=xlsx (P1)", "Download menu.", "Formula injection -> values escaped.", "Cell values escaped against formula injection.", "Templates."),
    ("REP-012", "CSV export", "P0", "CSV download of report tables.", "Interoperability with minimal dependencies.", "Report data.", "None.", "GET /api/v1/reports/{id}/download?format=csv", "Download button.", "Formula injection risk -> leading =,+,-,@ escaped.", "CSV is UTF-8 with header row; cells escaped against formula injection; download audited.", "Excel (REP-011)."),
    ("REP-013", "Scheduled reports", "P2", "Recurring report generation and delivery.", "Routine oversight.", "Schedules.", "None.", "Not defined until P2 design.", "Schedule editor.", "Delivery failure -> retry.", "Recipients limited to authorised roles.", "Subscriptions."),
    ("REP-014", "Report access control", "P0", "Enforces who may generate and download each report type and scope.", "Protects personal data in reports.", "Permissions; report scope.", "None.", "Enforced on all /api/v1/reports routes", "Unavailable report types hidden and disabled server-side.", "Unauthorised download -> 403 and audit.", "Authorisation tests cover every report type and role.", "Signed download URLs (P1).", {"deps": "SEC-002"}),
    ("REP-015", "Report audit trail", "P0", "Audits report generation and downloads.", "Accountability for personal data exports.", "AuditLog.", "None.", "Audit entries for report events", "Visible in Audit logs.", "Audit write failure -> download refused.", "No report download occurs without an audit record.", "Access reviews.", {"deps": "SEC-009"}),
])

# ------------------------------------------------------------ P. SECURITY
category(
    "P", "SEC", "Security", "Security",
    "Platform administrator", "System auditor; all users",
    "None (foundational)",
    "Security-relevant configuration changes require an authorised administrator and are audited.",
    "See SECURITY_RESPONSIBLE_AI.md for controls and threat model.",
    "Authentication and security prompts accessible (no CAPTCHA without accessible alternative).",
)

batch([
    ("SEC-001", "Authentication", "P0", "Email/username and password authentication with secure hashing for MVP; SSO-ready adapter.", "Only known users access the platform.", "User credentials (hashed).", "None.", "POST /api/v1/auth/login; POST /api/v1/auth/logout; GET /api/v1/auth/session; POST /api/v1/auth/password/change", "Login screen.", "Brute force -> rate limiting and lockout policy; unknown user -> generic error.", "Passwords hashed with a modern adaptive algorithm; generic login errors; lockout/rate limits enforced; all events audited.", "SSO/OIDC (SEC-004).", {"deps": "SEC-013; SEC-014"}),
    ("SEC-002", "Role-based access control", "P0", "Server-side permission checks for eight access roles scoped by organisation and department.", "Least-privilege access to personal and restricted data.", "Access role assignments; permission matrix.", "None.", "Enforced in every endpoint via dependency-injected policy checks", "UI hides unavailable actions (never relied on for security).", "Missing permission -> 403; ambiguous scope -> deny.", "Every endpoint has an authorisation test per role in the permission matrix (SECURITY_RESPONSIBLE_AI.md §RBAC).", "Permission management (ADM-016)."),
    ("SEC-003", "JWT or secure session architecture", "P0", "Server-side sessions with HttpOnly, Secure, SameSite cookies and CSRF protection (recommended; DEC-007).", "Revocable sessions for a browser application.", "Session store.", "None.", "Session cookie; CSRF token header", "Session expiry prompts.", "Stolen session -> revocation on logout/password change.", "Sessions revocable server-side; cookies HttpOnly/Secure/SameSite; CSRF protection on state-changing requests.", "Token-based API clients (P1)."),
    ("SEC-004", "OAuth/SSO readiness", "P1", "Authentication adapter supporting OIDC providers when authorised.", "Integration with government identity providers.", "Provider metadata.", "None.", "Auth adapter (API_INTEGRATION_SPEC.md)", "SSO button when configured.", "Provider unavailable -> local login policy.", "No provider enabled without verified configuration.", "Parichay or other SSO (Decision required)."),
    ("SEC-005", "Admin authentication", "P0", "Stronger requirements for administrative roles (shorter sessions; re-authentication for sensitive actions; MFA when available).", "Protects high-privilege accounts.", "Session metadata.", "None.", "Re-auth endpoint POST /api/v1/auth/reauthenticate", "Re-authentication dialog.", "Re-auth failure -> action blocked.", "Sensitive admin actions require recent authentication; MFA requirement recorded as Decision required.", "MFA (P1)."),
    ("SEC-006", "Encryption in transit", "P0", "TLS for all external traffic; internal traffic encrypted where crossing hosts.", "Confidentiality of personal data.", "Certificates.", "None.", "HTTPS only; HSTS", "None.", "Plain HTTP -> redirect/deny.", "No production endpoint accepts plain HTTP.", "mTLS internal (P2)."),
    ("SEC-007", "Encryption at rest", "P0", "Database, backups and object storage encrypted at rest by the hosting platform or disk encryption.", "Protection against media theft.", "Storage configuration.", "None.", "N/A", "None.", "Unencrypted volume -> deployment check fails.", "Deployment checklist verifies encryption at rest (hosting decision pending).", "Field-level encryption for sensitive fields (P1)."),
    ("SEC-008", "Secure APIs", "P0", "Validated, authenticated, authorised, rate-limited APIs following OWASP API Security guidance.", "Reduces API abuse risk.", "OpenAPI schema.", "None.", "All /api/v1 routes", "None.", "Mass assignment -> explicit schemas prevent it.", "Request/response schemas explicit; no unauthenticated routes except login, health and readiness.", "API gateway (P2)."),
    ("SEC-009", "Audit logs", "P0", "Append-only audit records for security, administrative, review and data-access events.", "Accountability and investigation.", "AuditLog.", "None.", "GET /api/v1/audit-logs", "Audit logs screen.", "Audit write failure for critical events -> operation fails closed.", "Critical events (login, role change, approval, adjustment, export) always produce audit records with actor, action, target, time and correlation ID.", "Tamper-evident hashing (P1)."),
    ("SEC-010", "Activity logs", "P0", "Operational application logs (structured, redacted).", "Troubleshooting.", "Log stream.", "None.", "N/A", "None.", "Secrets in logs -> redaction filter.", "Logs are structured JSON with correlation IDs and redaction of secrets and personal fields.", "Central log platform (OBSERVABILITY_SPEC.md)."),
    ("SEC-011", "AI interaction logs", "P0", "Records every AI provider call: purpose, model, prompt version, input references, output, validation, tokens, latency, user and correlation ID.", "Traceability of AI behaviour.", "AIInteractionLog.", "None.", "GET /api/v1/ai-interactions; GET /api/v1/ai-interactions/{id}", "Audit logs screen (AI tab).", "Log write failure -> AI response not shown.", "No AI output is shown to a user without an AIInteractionLog record; stored content follows retention and redaction rules.", "Evaluation sampling.", {"deps": "RAI-019"}),
    ("SEC-012", "Document-level access control", "P0", "Access scopes on materials enforced across storage, retrieval, AI context and downloads (see MAT-028).", "See MAT-028.", "See MAT-028.", "See MAT-028.", "See MAT-028", "See MAT-028.", "See MAT-028.", "See MAT-028.", "See MAT-028.", {"alias_of": "MAT-028"}),
    ("SEC-013", "Session management", "P0", "Idle and absolute timeouts, logout everywhere, session rotation on privilege change.", "Limits session hijacking impact.", "Sessions.", "None.", "POST /api/v1/auth/logout; POST /api/v1/auth/sessions/revoke-all", "Timeout warning dialog.", "Timeout during form -> draft preserved where safe.", "Session ID rotates on login and privilege change; timeouts configurable.", "Device list (P1)."),
    ("SEC-014", "Rate limiting", "P0", "Per-user and per-IP limits, stricter on login and AI endpoints.", "Abuse and cost control.", "Rate-limit counters (Redis or DB).", "None.", "429 responses with Retry-After", "Friendly rate-limit message.", "Limiter unavailable -> fail closed for AI endpoints, open with logging for reads (decision recorded).", "AI and login endpoints have documented limits; 429 includes Retry-After.", "Adaptive limits."),
    ("SEC-015", "Input validation", "P0", "Schema validation of all inputs; file validation; length limits.", "Prevents injection and malformed data.", "Pydantic schemas.", "None.", "422 validation errors", "Inline form errors.", "Invalid input -> 422 with field details.", "No endpoint accepts unvalidated input.", "Content security scanning."),
    ("SEC-016", "Output validation", "P0", "Validates API responses and AI outputs against schemas; encodes rendered content.", "Prevents data leakage and XSS.", "Response schemas.", "Structured output validation for AI.", "Response models", "Sanitised rendering of AI text (no raw HTML).", "Schema mismatch -> error, not partial data.", "AI text rendered as plain text/markdown sanitised; responses filtered to declared fields.", "Output DLP (P2)."),
    ("SEC-017", "Secret management", "P0", "Secrets only in environment/secret store; never in code, logs, API responses or client bundles.", "Prevents credential leakage.", "Environment variables; secret store.", "None.", "N/A", "Settings never display secrets.", "Secret committed -> pre-commit/CI scan fails.", "Secret scanning in CI; .env git-ignored; .env.example has placeholders only.", "Managed secret store (hosting decision).", {"status": PART, "status_note": ".env git-ignored and .env.example placeholders only; no CI secret scanning."}),
    ("SEC-018", "Data retention", "P1", "Retention periods per data class with automated purge jobs.", "Data minimisation and compliance.", "Retention policy.", "None.", "Retention jobs (P1)", "Retention settings (ADM-018).", "Purge failure -> retried and alerted.", "Retention periods defined and approved before production (Decision required).", "Legal hold."),
    ("SEC-019", "Data deletion", "P1", "User and administrator-initiated deletion with propagation to derived data.", "Honours deletion requests.", "Deletion requests.", "None.", "POST /api/v1/me/deletion-requests (P1)", "Deletion request flow.", "Audit-required records -> pseudonymised instead of deleted (policy decision).", "Deletion propagates to chunks, embeddings and logs per policy.", "Automated DSAR handling."),
    ("SEC-020", "Backup and recovery", "P1", "Encrypted backups with tested restore procedure and defined RPO/RTO.", "Resilience.", "Backups.", "None.", "N/A", "None.", "Restore failure -> incident.", "Restore tested before production; RPO/RTO decided.", "Cross-region replicas."),
    ("SEC-021", "Threat modeling", "P0", "Documented threat model maintained per release.", "Systematic risk reduction.", "Threat model.", "None.", "N/A", "None.", "New feature without threat review -> blocked from release.", "Threat model in SECURITY_RESPONSIBLE_AI.md reviewed at each phase exit.", "External penetration test before production."),
])

# ------------------------------------------------------------ Q. RESPONSIBLE AI
category(
    "Q", "RAI", "Responsible AI", "Responsible AI",
    "Platform administrator", "System auditor; Trainer; Learner",
    "SEC-011 (AI interaction logs)",
    "Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).",
    "AI provider receives only authorised data; outputs validated; interactions logged.",
    "AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.",
)

batch([
    ("RAI-001", "Retrieval grounding", "P0", "Generative answers and questions are produced only from retrieved, accessible, licence-permitted sources.", "Reduces fabrication; keeps content official.", "Retrieved chunks.", "RAG constraints (AI_SYSTEM_SPEC.md §11).", "Enforced in document-qa and generation", "Source panel.", "No sources -> abstain.", "Prompts contain only retrieved chunks as knowledge; evaluation set checks unanswerable questions abstain.", "Claim-level verification."),
    ("RAI-002", "Citations", "P0", "Every grounded output carries verified citations (see MAT-019).", "See MAT-019.", "See MAT-019.", "See MAT-019.", "See MAT-019", "Citation chips.", "See MAT-019.", "See MAT-019.", "See MAT-019.", {"alias_of": "MAT-019"}),
    ("RAI-003", "Confidence indicators", "P0", "Rule-based confidence/evidence bands on AI outputs and estimates with defined meanings.", "Calibrated user trust.", "Retrieval scores; verification; evidence counts.", "Rule-based.", "confidence field on AI responses", "Band label and definition.", "Unknown -> 'low'.", "Band definitions published in UI copy; no numeric accuracy claims without evaluation.", "Calibrated probabilities."),
    ("RAI-004", "Hallucination mitigation", "P0", "Combination of grounding, span verification, independent validation and abstention.", "Protects learners from false statements.", "Chunks; outputs.", "Validators (AI_SYSTEM_SPEC.md §18).", "Internal", "Unsupported-content flags.", "Verification fails -> output withheld.", "Unverified generated statements are never displayed as fact.", "Entailment models."),
    ("RAI-005", "Question validation", "P0", "Automated schema, grounding, duplicate and answer-key validation before review (ASM-022 to ASM-024).", "Reviewer time focused on plausible questions.", "Questions; chunks.", "Validators.", "GET /api/v1/questions/{id}/validations", "Validation panel.", "Validator error -> 'validation_incomplete'.", "Every AI-generated question has a validation record before entering review.", "Quality scoring (ASM-025)."),
    ("RAI-006", "Human approval", "P0", "Approval gate for AI-generated learner-facing content (see ASM-028).", "See ASM-028.", "See ASM-028.", "See ASM-028.", "See ASM-028", "See ASM-028.", "See ASM-028.", "See ASM-028.", "See ASM-028.", {"alias_of": "ASM-028"}),
    ("RAI-007", "Prompt-injection protection", "P0", "Treat documents and user input as untrusted data; isolate instructions; no side-effecting tools; detect and flag injection patterns; test suite.", "Integrity of AI behaviour.", "Inputs; detection rules.", "Defences (AI_SYSTEM_SPEC.md §36).", "Internal", "Restricted-response notice.", "Detection -> restricted output and security event.", "Injection test corpus passes for Q&A and generation before MVP release.", "Classifier detection (P1)."),
    ("RAI-008", "Audit trails", "P0", "AI-related audit trail combining SEC-009 and SEC-011.", "See SEC-011.", "See SEC-011.", "See SEC-011.", "See SEC-011", "Audit logs screen.", "See SEC-011.", "See SEC-011.", "See SEC-011.", {"alias_of": "SEC-011"}),
    ("RAI-009", "Safety filters", "P0", "Blocks abusive, discriminatory or out-of-scope content in inputs and outputs; relies on provider safety plus application checks.", "Professional, safe environment.", "Filter rules.", "Provider safety behaviour plus rules.", "Internal; refusal handling", "Polite refusal message.", "Provider refusal -> handled as abstention with reason category.", "Refusals and filtered outputs logged and displayed with neutral messaging.", "Custom moderation model."),
    ("RAI-010", "Bias monitoring", "P1", "Monitors assessment and recommendation outcomes for disparities across permitted, consented groupings.", "Fairness.", "Aggregates; permitted attributes (none collected in MVP).", "Statistical checks.", "GET /api/v1/analytics/fairness (P1)", "Fairness report for auditors.", "No attributes -> item-level checks only.", "No sensitive attributes collected without legal basis; methodology reviewed.", "External fairness audit."),
    ("RAI-011", "Explainable recommendations", "P0", "Every recommendation and path item states the rule and data that produced it.", "Trust and contestability.", "Recommendation reasons.", "Template explanations.", "reason object on recommendation payloads", "'Why recommended' text.", "Missing reason -> recommendation suppressed.", "No recommendation is displayed without a reason.", "Natural-language explanations (P1)."),
    ("RAI-012", "Model evaluation", "P0", "Offline evaluation harness for Q&A grounding, abstention and question validation using golden datasets built from collected public documents.", "Evidence before claims.", "Golden datasets (to be created and approved).", "Evaluation runs.", "Internal tooling; results stored as reports", "Evaluation summary for administrators.", "No golden dataset -> release gate cannot pass.", "MVP release requires evaluation results recorded for each prompt version; no accuracy figures published without these results.", "Online evaluation (AI_SYSTEM_SPEC.md §34)."),
    ("RAI-013", "Dataset evaluation", "P1", "Evaluates coverage and quality of source corpora and question banks.", "Detects blind spots.", "Corpus metadata.", "Analysis.", "P1", "Corpus report.", "Stale sources -> flagged.", "Coverage by topic reported.", "Automated freshness checks."),
    ("RAI-014", "AI output versioning", "P0", "AI artefacts store model, prompt version, parameters and timestamps; edits create versions.", "Reproducibility and audit.", "Version fields.", "None.", "Version metadata on artefacts", "Version info panels.", "Missing metadata -> artefact rejected.", "Every AI artefact has model ID, prompt version, created_at and validation/review status.", "Replay tooling."),
    ("RAI-015", "Abstention behavior", "P0", "The system declines to answer when evidence is insufficient or verification fails.", "Prevents confident wrong answers.", "Retrieval scores; verification.", "Abstention rules.", "abstained flag with reason", "Abstention message with next steps.", "Over-abstention -> tuned via evaluation.", "Unanswerable golden questions yield abstentions; abstentions logged with reason.", "Escalation to trainers."),
    ("RAI-016", "Sensitive-data minimization", "P0", "Only necessary data sent to AI providers; personal identifiers excluded or redacted; uploads screened for personal data.", "Privacy protection.", "Redaction rules.", "Pre-call redaction.", "Internal", "Warning when redaction occurred.", "PII detected in upload -> quarantined for review.", "Provider payloads never include user names, emails or IDs; redaction tests pass.", "Self-hosted models for sensitive workloads (Decision required).", {"status": PART, "status_note": "collected datasets validated free of personal data (validator LP-09); no AI calls exist yet."}),
    ("RAI-017", "Human override", "P0", "Authorised humans can override AI validation results, estimates (CMP-019) and withdraw AI artefacts.", "Humans remain in control.", "Override records.", "None.", "Decision and adjustment endpoints", "Override actions with reason.", "Override without reason -> blocked.", "All overrides require reason and are audited.", "Override analytics."),
    ("RAI-018", "Appeal/correction workflow", "P0", "Learners request correction of estimates or question results; reviewers respond with outcome and reason.", "Contestability of automated outputs.", "CorrectionRequest.", "None.", "POST /api/v1/correction-requests; GET /api/v1/correction-requests; PATCH /api/v1/correction-requests/{id}", "Request action on profile/results; review queue.", "Unanswered request beyond SLA -> escalated to training manager (SLA: Decision required).", "Every request receives a recorded decision and reason; outcome visible to the learner.", "Formal grievance integration (P2).", {"primary": "Learner", "secondary": "Trainer; Training manager"}),
    ("RAI-019", "Model and prompt registry", "P0", "Versioned registry of prompt templates and model configurations used by AI services.", "Controlled change and traceability.", "PromptTemplate; model config.", "None.", "GET /api/v1/admin/prompt-templates; POST /api/v1/admin/prompt-templates/{key}/versions", "Registry view (platform administrator).", "Unregistered prompt in use -> startup check fails.", "AI services can only use registered prompt versions; changes audited and linked to evaluation results.", "Automated evaluation gating."),
])

# ------------------------------------------------------------ R. AUTOMATION
category(
    "R", "AUT", "Automation", "Automation",
    "Platform administrator", "Trainer; Learner",
    "AUT-012 (background jobs)",
    "Automations never publish AI-generated content or change employment-relevant data without human approval.",
    "Jobs run with least privilege, organisation scoping and audit of side effects.",
    "Job status and failures communicated accessibly in UI.",
)

batch([
    ("AUT-001", "Automated recommendations", "P0", "Recomputes recommendations after assessment submission or catalogue changes.", "Fresh guidance without manual steps.", "Gaps; catalogue.", "Rule-based.", "Background job triggered by attempt submission", "Updated recommendation cards.", "Job failure -> previous recommendations retained with 'may be outdated' notice.", "Recomputation is idempotent per input snapshot.", "Scheduled refresh (AUT-010).", {"deps": "AI-005; AUT-012"}),
    ("AUT-002", "Competency updates", "P0", "Recomputes estimates when evidence changes (new attempt, voided evidence, adjustment).", "Estimates stay consistent with evidence.", "Evidence.", "None.", "Background job", "Profile refresh.", "Failure -> estimate marked stale.", "Recomputation audited; stale estimates flagged.", "Event sourcing (P2).", {"deps": "AI-012; AI-016"}),
    ("AUT-003", "Quiz generation (job)", "P0", "Runs AI-007 generation as background jobs with progress.", "Long generation without blocking UI.", "Job parameters.", "LLM.", "POST /api/v1/question-generation-jobs", "Job progress.", "Timeout -> retry; exhausted -> failed with reason.", "Jobs idempotent by client key; partial results saved with status.", "Batch generation.", {"deps": "AI-007; AUT-012"}),
    ("AUT-004", "Answer evaluation (automation)", "P0", "Automatic scoring on submission (see AI-009).", "See AI-009.", "See AI-009.", "See AI-009.", "See AI-009", "See AI-009.", "See AI-009.", "See AI-009.", "See AI-009.", {"alias_of": "AI-009"}),
    ("AUT-005", "Weak-topic detection (automation)", "P1", "Scheduled computation of weak topics (see AI-014).", "See AI-014.", "See AI-014.", "See AI-014.", "See AI-014", "See AI-014.", "See AI-014.", "See AI-014.", "See AI-014.", {"alias_of": "AI-014"}),
    ("AUT-006", "Reassessment reminders", "P1", "Reminds learners when reassessment is suggested.", "Closes learning loop.", "Reassessment triggers.", "None.", "Notification job (P1)", "Reminder notifications.", "Delivery failure -> retry.", "Learners can opt out.", "Channels (email/SMS) via notification adapter."),
    ("AUT-007", "Notifications", "P1", "In-app and email notifications through a notification adapter.", "Timely awareness.", "Notification.", "None.", "GET /api/v1/notifications; PATCH /api/v1/notifications/{id} (P1)", "Notification centre.", "Provider down -> queued.", "Notification preferences respected; no personal data in email subject lines.", "SMS/WhatsApp adapters (P2)."),
    ("AUT-008", "Report generation (automation)", "P1", "Asynchronous generation for large reports.", "Scalability.", "Report jobs.", "None.", "POST /api/v1/reports (async)", "Report status.", "Failure -> retry.", "Idempotent by request key.", "Scheduled reports."),
    ("AUT-009", "Learning-path updates", "P1", "Automatic path refresh when gaps change.", "Paths stay current.", "Gaps.", "Rule-based.", "Background job (P1)", "'Path updated' notice with diff.", "Failure -> previous path kept.", "Learner sees what changed and why.", "Notifications."),
    ("AUT-010", "Scheduled data refresh", "P1", "Scheduled URL checks and re-collection of source documents via existing manifest-based scripts.", "Detects moved or updated official documents.", "Collection manifests; sidecars.", "None.", "Scheduled job (P1)", "Source freshness report.", "Source changed -> new version flagged for review, never overwritten.", "Refresh never overwrites raw files; changed checksums create review tasks.", "Change notifications.", {"status": PART, "status_note": "manual, re-runnable collection and URL-check scripts exist (scripts/collectors/fetch_documents.py, scripts/validators/check_document_urls.py); no scheduler."}),
    ("AUT-011", "Integration synchronization", "P1", "Scheduled iGOT sync jobs (see IGOT-005).", "See IGOT-005.", "See IGOT-005.", "See IGOT-005.", "See IGOT-005", "See IGOT-005.", "See IGOT-005.", "See IGOT-005.", "See IGOT-005.", {"alias_of": "IGOT-005", "status": BLOCK, "status_note": "requires authorised iGOT access."}),
    ("AUT-012", "Background jobs", "P0", "Job system for document processing, generation, recommendations and reports.", "Responsive UI and reliable long tasks.", "BackgroundJob.", "None.", "GET /api/v1/jobs/{id}", "Job status components.", "Worker crash -> job re-queued by visibility timeout.", "Every job records type, status, attempts, timestamps, error and correlation ID.", "Autoscaling workers."),
    ("AUT-013", "Retry queues", "P0", "Bounded retries with backoff and dead-letter state.", "Recovers from transient failures without infinite loops.", "Job attempts.", "None.", "Internal", "Failed state with retry action.", "Max attempts reached -> dead-letter and alert.", "Retry limits configured per job type; dead-lettered jobs visible to platform administrators.", "Automatic remediation."),
    ("AUT-014", "Job monitoring", "P0", "Job metrics and dashboard (queue depth, failures, durations).", "Operational visibility.", "Job metrics.", "None.", "GET /api/v1/admin/jobs (platform administrator)", "Jobs panel in Integration health/Admin.", "Metrics unavailable -> logs only.", "Failed and stuck jobs visible within one refresh interval.", "Alerting (OBSERVABILITY_SPEC.md)."),
    ("AUT-015", "Idempotency", "P0", "Idempotency keys for job-creating and state-changing POSTs; idempotent job handlers.", "No duplicates on retries.", "Idempotency records.", "None.", "Idempotency-Key header", "Double-submit protection.", "Key reuse with different payload -> 409.", "Repeating a request with the same key returns the original result.", "Global idempotency store.", {"status": PART, "status_note": "collection scripts skip already-collected files by checksum; no API idempotency."}),
])

# ------------------------------------------------ S. UX AND PLATFORM EXPERIENCE
category(
    "S", "UX", "UX and platform experience", "UX and platform experience",
    "Learner", "All users",
    "ACC-009 (screen reader); ACC-010 (keyboard)",
    "Not applicable unless the UX element displays AI-generated content (then RAI rules apply).",
    "UI never trusted for authorisation; no sensitive data cached in browser storage.",
    "Follows UI_UX_SPEC.md accessibility rules.",
)

batch([
    ("UX-001", "Responsive design", "P0", "Layouts adapt to desktop, tablet and mobile widths.", "Usable on office desktops and phones.", "None.", "None.", "N/A", "All screens (UI_UX_SPEC.md breakpoints).", "Horizontal scrolling -> layout bug.", "Core journeys usable at 360px width without horizontal page scrolling.", "Native app (FUT-011)."),
    ("UX-002", "Mobile-friendly experience", "P0", "Touch targets, readable text and simplified navigation on small screens.", "Access away from desks.", "None.", "None.", "N/A", "Mobile navigation pattern.", "Small targets -> test failure.", "Touch targets meet minimum size; assessments completable on mobile.", "PWA (P2)."),
    ("UX-003", "Personalized home", "P0", "Role-specific home: learner dashboard, trainer dashboard or admin dashboard (see PER-001, TRN-001).", "Relevant starting point per user.", "Role.", "None.", "GET /api/v1/me", "Home routing.", "Multiple roles -> role switcher.", "Users with multiple access roles can switch views; default matches primary role.", "Custom widgets."),
    ("UX-004", "Global search", "P1", "Search across courses, materials and help.", "Faster navigation.", "Search indexes.", "Optional semantic.", "GET /api/v1/search/global (P1)", "Header search.", "Partial index failure -> partial results notice.", "Results respect permissions.", "Command palette."),
    ("UX-005", "Notifications", "P1", "UI for notifications (see AUT-007).", "See AUT-007.", "See AUT-007.", "See AUT-007.", "See AUT-007", "Bell menu.", "See AUT-007.", "See AUT-007.", "See AUT-007.", {"alias_of": "AUT-007"}),
    ("UX-006", "Calendar", "P2", "Calendar of learning plans and programmes.", "Planning.", "Plans; programme dates (dates currently unknown).", "None.", "Not defined until P2 design.", "Calendar view.", "Dates unknown -> not shown.", "No invented dates.", "Calendar sync."),
    ("UX-007", "Bookmarks", "P1", "Save courses, materials and passages.", "Quick return.", "Bookmark.", "None.", "POST/DELETE /api/v1/me/bookmarks (P1)", "Bookmark toggle.", "Deleted target -> bookmark marked unavailable.", "Bookmarks private.", "Collections."),
    ("UX-008", "Recently viewed", "P1", "Recently opened items.", "Continuity.", "Activity.", "None.", "GET /api/v1/me/recent (P1)", "Recent list.", "None specific.", "Only own history.", "Cross-device."),
    ("UX-009", "Continue learning", "P0", "Card resuming the next in-progress path item or attempt.", "Reduces friction.", "Path; attempts.", "None.", "Included in GET /api/v1/me/dashboard", "Continue card on dashboard.", "Nothing in progress -> next recommended item.", "Card always points to an accessible, existing item.", "Deep resume positions."),
    ("UX-010", "Dark mode", "P2", "Dark colour theme.", "Comfort.", "Theme tokens.", "None.", "User preference (P2)", "Theme toggle.", "Contrast failures -> token fix.", "Meets contrast requirements.", "System sync."),
    ("UX-011", "Accessibility", "P0", "Umbrella for L-category accessibility features (see ACC-009/010/014/015/016).", "See category L.", "See category L.", "None.", "N/A", "All screens.", "See category L.", "See ACC-009, ACC-010, ACC-014, ACC-015, ACC-016.", "See category L.", {"alias_of": "ACC-009"}),
    ("UX-012", "Empty states", "P0", "Designed empty states explaining why content is empty and what to do.", "Guidance instead of dead ends.", "None.", "None.", "N/A", "Per-screen empty states (UI_UX_SPEC.md).", "None specific.", "Every list and dashboard card has a defined empty state.", "Contextual help."),
    ("UX-013", "Loading states", "P0", "Skeletons and progress for loading and background jobs.", "Perceived performance and clarity.", "None.", "None.", "N/A", "Skeleton and progress components.", "Long load -> timeout message.", "Every async view has loading and timeout states.", "Optimistic updates."),
    ("UX-014", "Error states", "P0", "Consistent recoverable error states mapped from API problem codes.", "Users can recover without support.", "Error codes.", "None.", "Problem responses (ERROR_HANDLING_SPEC.md)", "Error components.", "Unknown error -> generic message with correlation ID.", "Every error shows a human message, next step and correlation ID; no stack traces.", "Inline help links."),
    ("UX-015", "Onboarding", "P0", "First-login flow: profile confirmation, department and job role selection, privacy notice, optional pre-assessment start.", "Fast, informed start.", "User; roles.", "None.", "GET/PATCH /api/v1/me; PUT /api/v1/me/job-role", "Onboarding screen.", "No roles configured -> blocked with admin contact.", "Users see the privacy/AI-use notice before any assessment; onboarding resumable.", "Guided tours (UX-018)."),
    ("UX-016", "Help center", "P1", "Help articles, FAQs and AI-use explanations.", "Self-service support.", "Help content.", "Optional grounded help Q&A (P2).", "GET /api/v1/help (P1)", "Help panel.", "None specific.", "Includes plain-language explanation of AI use and limitations.", "Contextual help."),
    ("UX-017", "Feedback collection", "P1", "Product feedback widget (see TRN-014 for content feedback).", "Continuous improvement.", "Feedback.", "None.", "POST /api/v1/feedback (P1)", "Feedback widget.", "None specific.", "Feedback optional and anonymous where configured.", "In-app surveys."),
    ("UX-018", "Guided workflows", "P1", "Step-by-step guidance for complex tasks (e.g. building a quiz).", "Reduces errors.", "None.", "None.", "N/A", "Stepper components.", "Abandoned flow -> draft saved.", "Steps resumable.", "Interactive tours."),
    ("UX-019", "Search filters", "P0", "Filters for document library, courses and review queues (organisation, topic, type, status).", "Efficient browsing.", "Indexed metadata.", "None.", "Filter parameters per API_INTEGRATION_SPEC.md conventions", "Filter bars with chips.", "Invalid filter -> ignored with notice.", "Filters reflected in URL; accessible filter controls.", "Saved views (UX-020)."),
    ("UX-020", "Saved views", "P2", "Save filter combinations.", "Repeat analysis.", "Saved view.", "None.", "Not defined until P2 design.", "Saved view menu.", "None specific.", "Private by default.", "Shared views."),
    ("UX-021", "User profile and account settings", "P0", "Self-service profile (name, designation, department, job role, language preference) and privacy information. Added to satisfy the P0 'User profile' requirement, which had no item in the inventory.", "Accurate profile data and user control.", "User.", "None.", "GET/PATCH /api/v1/me", "Settings screen (profile section).", "Invalid change -> validation errors; role change -> audited.", "Users can view and edit permitted profile fields; changes affecting assessments (job role) are audited.", "Data download (P1).", {"deps": "SEC-001; ROLE-001"}),
])

# ------------------------------------------------------- T. FUTURE INTELLIGENCE
category(
    "T", "FUT", "Future intelligence", "Future intelligence",
    "Organization administrator", "Training manager; Platform administrator",
    "Validated historical data; fairness and ethics review",
    "Required: all outputs advisory; never used for automated employment decisions.",
    "Requires a new data protection impact assessment and ethics review before design.",
    "To be specified at design time.",
)

FUT = [
    ("FUT-001", "Predictive analysis", "Predictive models over learning and capability data."),
    ("FUT-002", "Skill-demand forecasting", "Forecasts future competency demand from role and programme trends."),
    ("FUT-003", "Career pathways", "Voluntary, learner-initiated pathway exploration between roles."),
    ("FUT-004", "Knowledge tracing", "Models mastery of knowledge components over time."),
    ("FUT-005", "Bayesian Knowledge Tracing", "BKT models for mastery estimation."),
    ("FUT-006", "Item Response Theory", "IRT calibration of items and ability estimation."),
    ("FUT-007", "AI certification", "Assessment programmes leading to certification with human sign-off."),
    ("FUT-008", "Competency passport", "Portable, verifiable record of human-verified competencies."),
    ("FUT-009", "Offline mode", "Offline access to materials and practice."),
    ("FUT-010", "Low-bandwidth mode", "Dedicated lite experience beyond ACC-017."),
    ("FUT-011", "Mobile application", "Native or installable mobile application."),
    ("FUT-012", "Voice interface", "Voice interaction for tutor and navigation."),
    ("FUT-013", "Workforce intelligence", "Aggregated capability intelligence for planning."),
    ("FUT-014", "Cross-department intelligence", "Cross-department capability insights with strict aggregation."),
    ("FUT-015", "Resource optimization", "Optimises allocation of training resources."),
    ("FUT-016", "AI trainer designer", "AI-assisted design of training programmes with expert review."),
    ("FUT-017", "Simulation-based learning", "Simulated statistical work scenarios."),
    ("FUT-018", "Organization-wide capability planning", "Long-range capability planning across the organisation."),
]
for fid, name, desc in FUT:
    F(fid, name, "P2", desc,
      "Strategic capability beyond MVP and P1.",
      "To be determined; requires validated historical data and legal basis.",
      "To be determined at design time; evaluation before any use.",
      API + "Not defined until P2 design.",
      "Not defined until P2 design.",
      "Insufficient validated data -> feature not enabled.",
      "Not built until a design, data protection impact assessment and evaluation plan are approved.",
      "To be defined.")
