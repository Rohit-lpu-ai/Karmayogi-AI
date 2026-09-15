import { ArrowRight, CheckCircle2, ClipboardCheck, Clock, ListChecks, PlayCircle, Save, UserCheck } from "lucide-react";
import { useState, type ReactNode } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { AssessmentSummary, Attempt, JobRoleCompetencies } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { DemoBadge, EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { questionTimeGuide } from "./timeGuide";

/** Assessment introduction (UI_UX_SPEC.md S-06 entry): purpose, expectations and the start/resume action. */
export function AssessmentIntroPage() {
  const { user } = useAuth();
  const assessments = useApi<AssessmentSummary[]>("/api/v1/assessments");
  const requirements = useApi<JobRoleCompetencies>(user?.job_role ? `/api/v1/job-roles/${user.job_role.id}/competencies` : null);

  return (
    <div className="flex flex-col gap-2">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Baseline assessment" }]}
        title="Baseline assessment"
        description="A first, evidence-based estimate of where you stand in each competency your job role requires."
      />
      {assessments.loading ? (
        <Card className="p-6">
          <LoadingState label="Loading assessment" lines={5} />
        </Card>
      ) : assessments.error ? (
        <ErrorState error={assessments.error} onRetry={assessments.reload} />
      ) : !assessments.data || assessments.data.length === 0 ? (
        <EmptyState title="No assessment is available for your job role yet." icon={<ClipboardCheck className="size-5" />}
          action={<Button variant="secondary" asChild><Link to="/get-started">Check your job role</Link></Button>}>
          <p>Your trainer will let you know when a baseline assessment is published for your role.</p>
        </EmptyState>
      ) : (
        <IntroContent assessment={assessments.data[0]} requirements={requirements.data} requirementsLoading={requirements.loading} />
      )}
    </div>
  );
}

function IntroContent({
  assessment,
  requirements,
  requirementsLoading,
}: {
  assessment: AssessmentSummary;
  requirements: JobRoleCompetencies | null;
  requirementsLoading: boolean;
}) {
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const status = assessment.latest_attempt?.status;
  const completed = status === "scored" || status === "submitted";
  const inProgress = status === "in_progress";

  async function start() {
    setBusy(true);
    setError(null);
    try {
      const attempt = await api<Attempt>(`/api/v1/assessments/${assessment.id}/attempts`, { method: "POST" });
      navigate(`/assessment/attempts/${attempt.id}`);
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Could not start", "The assessment could not be started. Try again."));
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
      <Card as="section" aria-labelledby="assessment-title" className="overflow-hidden">
        <div className="border-b border-border bg-muted/40 px-6 py-5 sm:px-8">
          <div className="flex flex-wrap items-center gap-2">
            {completed ? (
              <Badge tone="success">
                <CheckCircle2 aria-hidden="true" /> Completed
              </Badge>
            ) : inProgress ? (
              <Badge tone="primary">In progress</Badge>
            ) : (
              <Badge tone="neutral">Not started</Badge>
            )}
            {assessment.is_demo ? <DemoBadge /> : null}
          </div>
          <h2 id="assessment-title" className="mt-3 text-xl font-semibold text-balance">
            {assessment.title}
          </h2>
        </div>

        <div className="space-y-8 px-6 py-6 sm:px-8">
          <dl className="grid gap-3 sm:grid-cols-3">
            <Fact icon={<ListChecks />} label="Questions" value={`${assessment.question_count}`} hint="Multiple choice, one answer each" />
            <Fact icon={<Clock />} label="Time" value="No time limit" hint={questionTimeGuide(assessment.question_count)} />
            <Fact icon={<Save />} label="Progress" value="Saved automatically" hint="Leave and resume any time" />
          </dl>

          <div>
            <h3 className="font-semibold">How it works</h3>
            <ol className="mt-3 grid gap-3 sm:grid-cols-3">
              <HowStep n={1} title="Answer">One question at a time. Move back and forth freely.</HowStep>
              <HowStep n={2} title="Review">Check the question grid for anything unanswered, then submit.</HowStep>
              <HowStep n={3} title="See your result">Estimated level per competency, with next steps.</HowStep>
            </ol>
          </div>

          <div>
            <h3 className="font-semibold">Before you start</h3>
            <ul className="mt-3 space-y-2 text-foreground">
              <Guideline>Answer on your own, so the estimate reflects where you are today.</Guideline>
              <Guideline>Questions you leave unanswered are counted as not correct.</Guideline>
              <Guideline>You cannot change answers after submitting. In this release the baseline is taken once.</Guideline>
            </ul>
          </div>

          {error ? <ErrorState error={error} /> : null}
        </div>

        <div className="flex flex-col gap-3 border-t border-border px-6 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-8">
          <p className="text-sm text-muted-foreground">
            {completed ? "You have completed this assessment." : inProgress ? "Your saved answers are waiting for you." : "Ready when you are."}
          </p>
          {completed ? (
            <Button size="lg" asChild>
              <Link to={`/attempts/${assessment.latest_attempt!.id}/result`}>
                View your result
                <ArrowRight aria-hidden="true" />
              </Link>
            </Button>
          ) : (
            <Button size="lg" onClick={start} disabled={busy}>
              {inProgress ? <PlayCircle aria-hidden="true" /> : null}
              {busy ? "Opening..." : inProgress ? "Resume assessment" : "Start assessment"}
              {busy || inProgress ? null : <ArrowRight aria-hidden="true" />}
            </Button>
          )}
        </div>
      </Card>

      <aside className="flex flex-col gap-4" aria-label="About this assessment">
        <Card className="p-5">
          <h2 className="flex items-center gap-2 text-base font-semibold">
            <UserCheck className="size-4 text-primary" aria-hidden="true" />
            Competencies for your role
          </h2>
          {requirementsLoading ? (
            <LoadingState label="Loading competencies" className="mt-3" />
          ) : requirements && requirements.requirements.length > 0 ? (
            <>
              <p className="mt-1 text-sm text-muted-foreground">Your answers estimate your level in each of these.</p>
              <ul className="mt-4 space-y-3">
                {requirements.requirements.map((req) => (
                  <li key={req.competency.id} className="rounded-lg border border-border p-3">
                    <p className="font-medium text-foreground">{req.competency.name}</p>
                    <p className="mt-0.5 text-sm text-muted-foreground">
                      Your role requires level {req.required_level} of {req.levels.length}
                    </p>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">The competencies for your role are not available right now.</p>
          )}
        </Card>
        <Alert tone="info" title="Development guidance">
          Your result helps you plan learning. It is not an appraisal, promotion or eligibility decision.
        </Alert>
      </aside>
    </div>
  );
}

function Fact({ icon, label, value, hint }: { icon: ReactNode; label: string; value: string; hint?: string }) {
  return (
    <div className="flex flex-col gap-1 rounded-lg bg-muted/60 p-4">
      <dt className="flex items-center gap-2 text-sm text-muted-foreground">
        <span className="text-primary [&_svg]:size-4" aria-hidden="true">
          {icon}
        </span>
        {label}
      </dt>
      <dd className="text-lg font-semibold text-foreground">
        {value}
        {hint ? <span className="block text-sm font-normal text-muted-foreground">{hint}</span> : null}
      </dd>
    </div>
  );
}

function HowStep({ n, title, children }: { n: number; title: string; children: ReactNode }) {
  return (
    <li className="flex gap-3 rounded-lg border border-border p-4">
      <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground" aria-hidden="true">
        {n}
      </span>
      <span>
        <span className="block font-medium text-foreground">{title}</span>
        <span className="block text-sm text-muted-foreground">{children}</span>
      </span>
    </li>
  );
}

function Guideline({ children }: { children: ReactNode }) {
  return (
    <li className="flex gap-2.5">
      <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-primary" aria-hidden="true" />
      <span>{children}</span>
    </li>
  );
}
