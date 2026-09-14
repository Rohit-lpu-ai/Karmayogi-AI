import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, ApiError } from "../api/client";
import type { JobRole, JobRoleCompetencies, Me } from "../api/types";
import { useApi } from "../api/useApi";
import { useAuth } from "../auth/AuthContext";
import { DemoBadge, EmptyState, ErrorState, LoadingState, StatusBadge } from "../components/States";

export function OnboardingPage() {
  const { user, setUser } = useAuth();
  const navigate = useNavigate();
  const [acknowledged, setAcknowledged] = useState(false);
  const [selectedRole, setSelectedRole] = useState<string | null>(user?.job_role?.id ?? null);
  const [error, setError] = useState<ApiError | null>(null);
  const [busy, setBusy] = useState(false);
  const roles = useApi<JobRole[]>("/api/v1/job-roles");
  const requirements = useApi<JobRoleCompetencies>(selectedRole ? `/api/v1/job-roles/${selectedRole}/competencies` : null);

  if (!user) return null;
  const noticeDone = user.notice.acknowledged_at !== null;

  async function run(action: () => Promise<Me>, then?: () => void) {
    setBusy(true);
    setError(null);
    try {
      setUser(await action());
      then?.();
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Request failed"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="stack">
      <h1>Get started</h1>
      {error ? <ErrorState error={error} /> : null}

      <section className="card" aria-labelledby="notice-title">
        <h2 id="notice-title">
          Step 1 of 2: Privacy and AI-use notice{" "}
          {noticeDone ? <StatusBadge tone="success">Acknowledged</StatusBadge> : null}
        </h2>
        <StatusBadge tone="warning">Draft notice - not legally reviewed</StatusBadge>
        <p>{user.notice.text}</p>
        {!noticeDone ? (
          <>
            <label className="checkbox">
              <input type="checkbox" checked={acknowledged} onChange={(e) => setAcknowledged(e.target.checked)} />
              I have read this notice and understand that my assessment results are used for learning and development only.
            </label>
            <button
              type="button"
              className="button"
              disabled={!acknowledged || busy}
              onClick={() =>
                run(() => api<Me>("/api/v1/me/notice-acknowledgements", { method: "POST", body: { notice_version: user.notice.version } }))
              }
            >
              Acknowledge notice
            </button>
          </>
        ) : null}
      </section>

      <section className="card" aria-labelledby="role-title" aria-disabled={!noticeDone}>
        <h2 id="role-title">Step 2 of 2: Select your job role</h2>
        {!noticeDone ? <p className="muted">Acknowledge the notice first.</p> : null}
        {noticeDone && roles.loading ? <LoadingState label="Loading job roles" /> : null}
        {noticeDone && roles.error ? <ErrorState error={roles.error} onRetry={roles.reload} /> : null}
        {noticeDone && roles.data && roles.data.length === 0 ? (
          <EmptyState title="Your organisation hasn't set up job roles yet.">
            <p>Contact your administrator.</p>
          </EmptyState>
        ) : null}
        {noticeDone && roles.data && roles.data.length > 0 ? (
          <fieldset>
            <legend>Job role</legend>
            {roles.data.map((role) => (
              <label key={role.id} className="radio">
                <input type="radio" name="job-role" value={role.id} checked={selectedRole === role.id} onChange={() => setSelectedRole(role.id)} />
                {role.name} {role.is_demo ? <DemoBadge /> : null}
              </label>
            ))}
          </fieldset>
        ) : null}

        {selectedRole && noticeDone ? (
          <div className="requirements">
            <h3>What this role requires</h3>
            {requirements.loading ? <LoadingState label="Loading requirements" /> : null}
            {requirements.error ? <ErrorState error={requirements.error} onRetry={requirements.reload} /> : null}
            {requirements.data && requirements.data.requirements.length === 0 ? (
              <EmptyState title="This job role's requirements haven't been approved yet." />
            ) : null}
            {requirements.data && requirements.data.requirements.length > 0 ? (
              <ul>
                {requirements.data.requirements.map((r) => (
                  <li key={r.competency.id}>
                    {r.competency.name} - Level {r.required_level} of {r.levels.length} {r.competency.is_demo ? <DemoBadge /> : null}
                  </li>
                ))}
              </ul>
            ) : null}
            <button
              type="button"
              className="button"
              disabled={busy}
              onClick={() => run(() => api<Me>("/api/v1/me/job-role", { method: "PUT", body: { job_role_id: selectedRole } }), () => navigate("/"))}
            >
              Confirm job role
            </button>
          </div>
        ) : null}
      </section>
    </div>
  );
}
