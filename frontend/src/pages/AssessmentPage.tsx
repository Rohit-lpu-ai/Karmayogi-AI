import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, ApiError } from "../api/client";
import type { AssessmentSummary, Attempt, SubmitResponse } from "../api/types";
import { useApi } from "../api/useApi";
import { DemoBadge, EmptyState, ErrorState, LoadingState } from "../components/States";

type SaveState = "idle" | "saving" | "saved" | "error";

export function AssessmentPage() {
  const assessments = useApi<AssessmentSummary[]>("/api/v1/assessments");
  const [attempt, setAttempt] = useState<Attempt | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [busy, setBusy] = useState(false);

  async function startOrResume(assessmentId: string) {
    setBusy(true);
    setError(null);
    try {
      setAttempt(await api<Attempt>(`/api/v1/assessments/${assessmentId}/attempts`, { method: "POST" }));
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Could not start the assessment"));
    } finally {
      setBusy(false);
    }
  }

  if (attempt) return <AttemptView attempt={attempt} onChange={setAttempt} />;

  return (
    <div className="stack">
      <h1>Baseline assessment</h1>
      <p className="muted">Your answers are scored by fixed rules (no AI) to estimate your level in each competency your job role requires.</p>
      {error ? <ErrorState error={error} /> : null}
      {assessments.loading ? <LoadingState label="Loading assessments" /> : null}
      {assessments.error ? <ErrorState error={assessments.error} onRetry={assessments.reload} /> : null}
      {assessments.data && assessments.data.length === 0 ? (
        <EmptyState title="No assessment is available for your job role yet.">
          <p>
            Check that you have <Link to="/get-started">selected a job role</Link>, or contact your trainer.
          </p>
        </EmptyState>
      ) : null}
      {assessments.data?.map((a) => (
        <section key={a.id} className="card" aria-labelledby={`assessment-${a.id}`}>
          <h2 id={`assessment-${a.id}`}>
            {a.title} {a.is_demo ? <DemoBadge /> : null}
          </h2>
          <p>
            {a.question_count} multiple-choice questions · no time limit · answers are saved as you go.
          </p>
          {a.latest_attempt?.status === "scored" ? (
            <p>
              You have completed this assessment. <Link to={`/attempts/${a.latest_attempt.id}/result`}>View your result</Link>
            </p>
          ) : (
            <button type="button" className="button" disabled={busy} onClick={() => startOrResume(a.id)}>
              {a.latest_attempt?.status === "in_progress" ? "Resume assessment" : "Start assessment"}
            </button>
          )}
        </section>
      ))}
    </div>
  );
}

function AttemptView({ attempt, onChange }: { attempt: Attempt; onChange: (a: Attempt) => void }) {
  const navigate = useNavigate();
  const [saveState, setSaveState] = useState<SaveState>("idle");
  const [error, setError] = useState<ApiError | null>(null);
  const [confirming, setConfirming] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const unanswered = attempt.questions.filter((q) => q.selected_option_id === null).length;

  async function choose(questionVersionId: string, optionId: string) {
    const previous = attempt;
    const questions = attempt.questions.map((q) => (q.question_version_id === questionVersionId ? { ...q, selected_option_id: optionId } : q));
    onChange({ ...attempt, questions, answered_count: questions.filter((q) => q.selected_option_id !== null).length });
    setSaveState("saving");
    setError(null);
    try {
      await api(`/api/v1/attempts/${attempt.id}/answers/${questionVersionId}`, { method: "PUT", body: { selected_option_id: optionId } });
      setSaveState("saved");
    } catch (err) {
      onChange(previous); // keep the screen consistent with what the server stored
      setSaveState("error");
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Answer not saved"));
    }
  }

  async function submit() {
    setSubmitting(true);
    setError(null);
    try {
      const result = await api<SubmitResponse>(`/api/v1/attempts/${attempt.id}/submit`, { method: "POST" });
      navigate(`/attempts/${result.attempt_id}/result`);
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Submission failed"));
      setSubmitting(false);
      setConfirming(false);
    }
  }

  return (
    <div className="stack">
      <h1>
        {attempt.assessment.title} {attempt.assessment.is_demo ? <DemoBadge /> : null}
      </h1>
      <p className="muted">
        Answered {attempt.answered_count} of {attempt.question_count}
      </p>
      <p className="save-status" role="status" aria-live="polite">
        {saveState === "saving" ? "Saving..." : saveState === "saved" ? "Saved" : ""}
      </p>
      {error ? <ErrorState error={error} /> : null}

      <ol className="questions">
        {attempt.questions.map((q) => (
          <li key={q.question_version_id} className="card">
            <fieldset>
              <legend>
                <span className="question-number">Question {q.position}</span> {q.stem}
              </legend>
              <p className="muted small">
                {q.competency.name} · {q.difficulty} {q.is_demo ? <DemoBadge label="DEMO item" /> : null}
              </p>
              {q.options.map((option) => (
                <label key={option.id} className="radio">
                  <input
                    type="radio"
                    name={`q-${q.question_version_id}`}
                    value={option.id}
                    checked={q.selected_option_id === option.id}
                    onChange={() => choose(q.question_version_id, option.id)}
                    disabled={submitting}
                  />
                  {option.text}
                </label>
              ))}
            </fieldset>
          </li>
        ))}
      </ol>

      {!confirming ? (
        <button type="button" className="button" onClick={() => setConfirming(true)}>
          Review and submit
        </button>
      ) : (
        <section className="card confirm" aria-labelledby="confirm-title">
          <h2 id="confirm-title">Submit your answers?</h2>
          <p>
            {unanswered > 0
              ? `${unanswered} question(s) are unanswered and will be scored as incorrect.`
              : "All questions are answered."}{" "}
            You cannot change answers after submitting.
          </p>
          <div className="row">
            <button type="button" className="button" onClick={submit} disabled={submitting}>
              {submitting ? "Submitting..." : "Submit answers"}
            </button>
            <button type="button" className="button button-secondary" onClick={() => setConfirming(false)} disabled={submitting}>
              Keep answering
            </button>
          </div>
        </section>
      )}
    </div>
  );
}
