import { Link } from "react-router-dom";
import type { Gaps, Profile, Recommendations } from "../api/types";
import { useApi } from "../api/useApi";
import { useAuth } from "../auth/AuthContext";
import { DemoBadge, EmptyState, ErrorState, LoadingState } from "../components/States";
import { bandLabel, formatScore, gapStatusLabel } from "./format";

export function DashboardPage() {
  const { user } = useAuth();
  if (!user) return null;

  if (!user.can_take_assessments) {
    return (
      <div className="stack">
        <h1>Welcome, {user.display_name}</h1>
        <EmptyState title="Your access role does not include taking assessments.">
          <p>Your roles: {user.access_roles.join(", ")}. Administration screens are not part of this release.</p>
        </EmptyState>
      </div>
    );
  }

  return (
    <div className="stack">
      <h1>Welcome, {user.display_name}</h1>
      <p className="muted">
        Job role: {user.job_role?.name} {user.job_role?.is_demo ? <DemoBadge /> : null} · <Link to="/get-started">Change</Link>
      </p>
      <div className="grid">
        <GapsCard />
        <RecommendationsCard />
      </div>
      <ProfileCard />
    </div>
  );
}

function GapsCard() {
  const gaps = useApi<Gaps>("/api/v1/me/competency-gaps");
  return (
    <section className="card" aria-labelledby="gaps-title">
      <h2 id="gaps-title">Competencies for your role</h2>
      {gaps.loading ? <LoadingState label="Loading competencies" /> : null}
      {gaps.error ? <ErrorState error={gaps.error} onRetry={gaps.reload} /> : null}
      {gaps.data && gaps.data.items.length === 0 ? <EmptyState title="Your job role's requirements haven't been approved yet." /> : null}
      {gaps.data && gaps.data.items.length > 0 ? (
        <>
          {gaps.data.items.every((i) => i.status === "not_assessed") ? (
            <EmptyState title="Start with a baseline assessment to see your competency profile.">
              <Link className="button" to="/assessment">
                Start assessment
              </Link>
            </EmptyState>
          ) : (
            <p>
              {gaps.data.summary.gap} of {gaps.data.items.length} competencies are below the level required for your role.
            </p>
          )}
          <table>
            <caption>Required and estimated levels</caption>
            <thead>
              <tr>
                <th scope="col">Competency</th>
                <th scope="col">Required</th>
                <th scope="col">Estimated</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {gaps.data.items.map((item) => (
                <tr key={item.competency.id}>
                  <td>
                    {item.competency.name} {item.competency.is_demo ? <DemoBadge /> : null}
                  </td>
                  <td>Level {item.required_level}</td>
                  <td>
                    {item.estimated_level !== null ? `Level ${item.estimated_level}` : "-"}
                    <span className="muted small"> {bandLabel(item.evidence_band, item.evidence_count)}</span>
                  </td>
                  <td>{gapStatusLabel(item)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : null}
    </section>
  );
}

function RecommendationsCard() {
  const recs = useApi<Recommendations>("/api/v1/me/recommendations");
  return (
    <section className="card" aria-labelledby="recs-title">
      <h2 id="recs-title">Recommended learning</h2>
      {recs.loading ? <LoadingState label="Loading recommendations" /> : null}
      {recs.error ? <ErrorState error={recs.error} onRetry={recs.reload} /> : null}
      {recs.data && recs.data.items.length === 0 ? (
        <EmptyState title="No recommendations yet.">
          <p className="muted">Recommendations appear for confirmed gaps that have reviewed, approved learning content.</p>
        </EmptyState>
      ) : null}
      {recs.data && recs.data.items.length > 0 ? (
        <ol className="recommendations">
          {recs.data.items.map((item) => (
            <li key={item.course.id}>
              <h3>
                {item.course.title} {item.course.is_demo ? <DemoBadge /> : null}
              </h3>
              <p className="muted small">
                {item.course.provider_organisation}
                {item.course.duration_days ? ` · ${item.course.duration_days} day(s)` : ""}
              </p>
              <p className="why">Recommended because:</p>
              <ul>
                {item.reasons.map((reason, index) =>
                  reason.rule === "gap_match" ? (
                    <li key={index}>
                      {reason.competency_name}: estimated level {reason.estimated}, required level {reason.required}
                    </li>
                  ) : (
                    <li key={index}>{reason.relevance === "primary" ? "Focuses on" : "Also covers"} that competency</li>
                  ),
                )}
              </ul>
            </li>
          ))}
        </ol>
      ) : null}
      {recs.data && recs.data.gaps_without_approved_content.length > 0 ? (
        <p className="muted small">No approved content yet for: {recs.data.gaps_without_approved_content.join(", ")}.</p>
      ) : null}
      {recs.data ? (
        <details>
          <summary>How are recommendations chosen?</summary>
          <p>
            Courses are suggested for competencies where your estimated level is below the level your role requires. Only
            courses linked to that competency are considered, and larger gaps come first. No AI is used.
          </p>
          <p className="muted small">External course catalogues (such as iGOT Karmayogi) are not connected to this platform.</p>
        </details>
      ) : null}
    </section>
  );
}

function ProfileCard() {
  const profile = useApi<Profile>("/api/v1/me/competency-profile");
  return (
    <section className="card" aria-labelledby="profile-title">
      <h2 id="profile-title">How was this calculated?</h2>
      <p className="muted small">
        Estimates come from your baseline assessment using fixed scoring rules (no AI). They are provisional development
        guidance, not an appraisal.
      </p>
      {profile.loading ? <LoadingState label="Loading estimates" /> : null}
      {profile.error ? <ErrorState error={profile.error} onRetry={profile.reload} /> : null}
      {profile.data && profile.data.items.length === 0 ? <EmptyState title="No estimates yet." /> : null}
      {profile.data?.items.map((item) => (
        <details key={item.competency.id}>
          <summary>
            {item.competency.name}: {formatScore(item.score)}, level {item.level_number ?? "not available"}
          </summary>
          <ul>
            {item.explanation.limitations.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
          <details className="methodology">
            <summary>Scoring method details</summary>
            <p className="muted small">{item.explanation.formula}.</p>
            <p className="muted small">
              Method {item.method_version} · thresholds {item.explanation.thresholds_status} · evidence rule:{" "}
              {item.explanation.band_rule}
            </p>
          </details>
        </details>
      ))}
    </section>
  );
}
