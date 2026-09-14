import { Link, useParams } from "react-router-dom";
import type { AttemptResult } from "../api/types";
import { useApi } from "../api/useApi";
import { DemoBadge, ErrorState, LoadingState, StatusBadge } from "../components/States";
import { bandLabel, formatScore } from "./format";

export function ResultPage() {
  const { attemptId } = useParams();
  const result = useApi<AttemptResult>(attemptId ? `/api/v1/attempts/${attemptId}/result` : null);

  if (result.loading) return <LoadingState label="Loading your result" />;
  if (result.error) return <ErrorState error={result.error} onRetry={result.reload} />;
  if (!result.data) return null;
  const data = result.data;

  return (
    <div className="stack">
      <h1>
        Your result {data.assessment.is_demo ? <DemoBadge /> : null}
      </h1>
      <p className="notice">{data.notice}</p>
      <section className="card" aria-labelledby="overall-title">
        <h2 id="overall-title">{data.assessment.title}</h2>
        <p>
          Weighted score: <strong>{formatScore(data.score_total)}</strong>
          {data.is_baseline ? <> · <StatusBadge tone="info">Baseline</StatusBadge></> : null}
        </p>
        <table>
          <caption>Result by competency (method {data.competencies[0]?.method_version ?? "score-v1"})</caption>
          <thead>
            <tr>
              <th scope="col">Competency</th>
              <th scope="col">Score</th>
              <th scope="col">Estimated level</th>
              <th scope="col">Evidence</th>
            </tr>
          </thead>
          <tbody>
            {data.competencies.map((c) => (
              <tr key={c.competency.id}>
                <td>
                  {c.competency.name} {c.competency.is_demo ? <DemoBadge /> : null}
                </td>
                <td>{formatScore(c.score)}</td>
                <td>
                  {c.level_number ?? "Not available"}
                  {c.thresholds_status !== "approved" ? <span className="muted small"> (provisional thresholds)</span> : null}
                </td>
                <td>{bandLabel(c.evidence_band, c.evidence_count)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <Link className="button" to="/">
          See gaps and recommended learning
        </Link>
      </section>

      <section className="card" aria-labelledby="feedback-title">
        <h2 id="feedback-title">Question feedback</h2>
        <ol className="feedback">
          {data.questions.map((q) => (
            <li key={q.question_version_id}>
              <p>{q.stem}</p>
              {q.is_correct === null ? null : q.is_correct ? (
                <StatusBadge tone="success">Correct</StatusBadge>
              ) : (
                <StatusBadge tone="warning">{q.selected_option_id ? "Not correct" : "Not answered"}</StatusBadge>
              )}
              {q.explanation ? <p className="muted">{q.explanation}</p> : null}
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
