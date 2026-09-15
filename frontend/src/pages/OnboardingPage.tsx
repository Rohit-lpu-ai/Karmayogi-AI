import {
  ArrowLeft,
  ArrowRight,
  BookOpenCheck,
  BriefcaseBusiness,
  ClipboardCheck,
  Clock,
  Compass,
  FlaskConical,
  Gauge,
  Lightbulb,
  ListChecks,
  Save,
  ShieldCheck,
  Target,
} from "lucide-react";
import { useEffect, useRef, useState, type ReactNode, type RefObject } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { AssessmentSummary, JobRole, JobRoleCompetencies, Me } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { LevelScale } from "@/components/product/LevelScale";
import { ProgressStepper, type Step } from "@/components/product/ProgressStepper";
import { DemoBadge, EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { RadioCard } from "@/components/ui/radio-cards";
import { toast } from "@/components/ui/toaster";
import { PRODUCT } from "@/config/product";
import { cn } from "@/lib/utils";
import { questionTimeGuide } from "./assessment/timeGuide";

const STEPS: Step[] = [
  { id: "welcome", label: "Welcome" },
  { id: "notice", label: "Your data" },
  { id: "role", label: "Job role" },
  { id: "assessment", label: "Assessment" },
];

/** Where a learner resumes: the first step whose server-side requirement is not yet met (S-02 "progress is resumable"). */
function initialStep(user: Me): number {
  if (user.notice.acknowledged_at === null) return 0;
  if (user.job_role === null) return 2;
  return 3;
}

/**
 * First-time learner onboarding (UI_UX_SPEC.md S-02, MVP-03, MVP-04) and, for onboarded learners arriving from
 * "Change job role", a focused job-role page. Server state (notice acknowledgement, job role) is the source of truth.
 */
export function OnboardingPage() {
  const { user } = useAuth();
  const [changeMode] = useState(() => (user ? user.notice.acknowledged_at !== null && user.job_role !== null : false));
  if (!user) return null;
  if (!user.can_take_assessments) {
    return (
      <div className="mx-auto max-w-2xl">
        <EmptyState title="Your access role does not include learning features.">
          <p>Onboarding is for learners. Administration screens are not part of this release.</p>
        </EmptyState>
      </div>
    );
  }
  return changeMode ? <ChangeJobRole user={user} /> : <OnboardingFlow user={user} />;
}

function useFocusHeading(dependency: unknown) {
  const ref = useRef<HTMLHeadingElement>(null);
  const first = useRef(true);
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    ref.current?.focus();
  }, [dependency]);
  return ref;
}

function OnboardingFlow({ user }: { user: Me }) {
  const [step, setStep] = useState(() => initialStep(user));
  const headingRef = useFocusHeading(step);

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-8">
      <ProgressStepper steps={STEPS} current={step} />
      {step === 0 ? <WelcomeStep user={user} headingRef={headingRef} onNext={() => setStep(1)} /> : null}
      {step === 1 ? <NoticeStep user={user} headingRef={headingRef} onBack={() => setStep(0)} onNext={() => setStep(2)} /> : null}
      {step === 2 ? <RoleStep user={user} headingRef={headingRef} onBack={() => setStep(1)} onNext={() => setStep(3)} /> : null}
      {step === 3 ? <AssessmentStep user={user} headingRef={headingRef} onBack={() => setStep(2)} /> : null}
    </div>
  );
}

type HeadingRef = RefObject<HTMLHeadingElement>;

function StepHeader({ headingRef, title, children }: { headingRef: HeadingRef; title: string; children?: ReactNode }) {
  return (
    <header className="space-y-2">
      <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold tracking-tight text-balance focus:outline-none sm:text-3xl">
        {title}
      </h1>
      {children ? <div className="max-w-2xl text-base text-muted-foreground text-pretty sm:text-lg">{children}</div> : null}
    </header>
  );
}

function StepActions({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cn("flex flex-col-reverse gap-3 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between", className)}>{children}</div>;
}

function Feature({ icon, title, children }: { icon: ReactNode; title: string; children: ReactNode }) {
  return (
    <li className="flex gap-4 sm:flex-col sm:gap-3">
      <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary [&_svg]:size-5" aria-hidden="true">
        {icon}
      </span>
      <div className="space-y-1">
        <h3 className="font-semibold text-foreground">{title}</h3>
        <p className="text-muted-foreground">{children}</p>
      </div>
    </li>
  );
}

// --- Step 1: welcome -----------------------------------------------------------------------------

function WelcomeStep({ user, headingRef, onNext }: { user: Me; headingRef: HeadingRef; onNext: () => void }) {
  return (
    <section className="flex flex-col gap-8" aria-label="Welcome">
      <StepHeader headingRef={headingRef} title={`Welcome, ${user.display_name}`}>
        {PRODUCT.tagline}
      </StepHeader>

      <Card className="p-6 sm:p-8">
        <h2 className="mb-6 text-lg font-semibold">How the platform helps you</h2>
        <ol className="grid gap-6 sm:grid-cols-3">
          <Feature icon={<BriefcaseBusiness />} title="1. Know your role">
            See the competencies your job role requires and the level expected for each.
          </Feature>
          <Feature icon={<Gauge />} title="2. Find where you stand">
            A short baseline assessment estimates your current level, with the evidence behind it.
          </Feature>
          <Feature icon={<Compass />} title="3. Learn what helps">
            Get learning suggestions for the competencies where you have the most room to grow.
          </Feature>
        </ol>
      </Card>

      <Alert tone="info" title="Development guidance, not an appraisal">
        Results support your learning. They are not used for appraisal, promotion or eligibility decisions.
      </Alert>

      <StepActions>
        <p className="text-sm text-muted-foreground">Setup has three short steps after this one.</p>
        <Button size="lg" onClick={onNext}>
          Get started
          <ArrowRight aria-hidden="true" />
        </Button>
      </StepActions>
    </section>
  );
}

// --- Step 2: demo data and privacy notice ------------------------------------------------------------

function NoticeStep({ user, headingRef, onBack, onNext }: { user: Me; headingRef: HeadingRef; onBack: () => void; onNext: () => void }) {
  const { setUser } = useAuth();
  const [checked, setChecked] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const acknowledged = user.notice.acknowledged_at !== null;

  async function acknowledge() {
    setBusy(true);
    setError(null);
    try {
      setUser(await api<Me>("/api/v1/me/notice-acknowledgements", { method: "POST", body: { notice_version: user.notice.version } }));
      onNext();
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Could not save", "Your acknowledgement was not saved. Try again."));
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="flex flex-col gap-6" aria-label="Your data and this demo">
      <StepHeader headingRef={headingRef} title="Your data and this demo">
        Before you start, here is what this environment contains and how your answers are used.
      </StepHeader>

      {user.is_synthetic ? (
        <Card className="border-demo/25 bg-demo-soft/60 p-6">
          <div className="flex gap-4">
            <span className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-demo-soft text-demo" aria-hidden="true">
              <FlaskConical className="size-5" />
            </span>
            <div className="space-y-3">
              <h2 className="text-lg font-semibold text-demo">You are using a demo environment</h2>
              <ul className="list-disc space-y-1.5 pl-5 text-foreground">
                <li>Your account, job roles, competencies, questions and courses are synthetic, written for testing.</li>
                <li>Nothing here is an official competency framework, an approved course or government assessment content.</li>
                <li>The platform is not connected to iGOT Karmayogi or any other government system.</li>
              </ul>
            </div>
          </div>
        </Card>
      ) : null}

      <Card className="p-6">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="text-lg font-semibold">Privacy and AI-use notice</h2>
          <Badge tone="warning">Draft - not legally reviewed</Badge>
        </div>
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          <NoticePoint icon={<Target />} title="Why answers are recorded">To estimate your competency levels for learning and development.</NoticePoint>
          <NoticePoint icon={<ShieldCheck />} title="No AI in scoring">Estimates come from fixed rules. They are not an appraisal or eligibility decision.</NoticePoint>
          <NoticePoint icon={<Lightbulb />} title="Your right to ask">Your trainer and authorised administrators may see results. You can ask for a review.</NoticePoint>
        </div>
        <details className="mt-5 rounded-lg border border-border bg-muted/40 px-4 py-3 text-sm">
          <summary className="cursor-pointer font-medium text-foreground">Read the full notice text</summary>
          <p className="mt-2 text-muted-foreground">{user.notice.text}</p>
          <p className="mt-2 text-xs text-muted-foreground">Version {user.notice.version}</p>
        </details>

        {acknowledged ? (
          <Alert tone="success" className="mt-5" title="You have acknowledged this notice" />
        ) : (
          <label className="mt-5 flex cursor-pointer items-start gap-3 rounded-lg border border-input p-4 has-[:checked]:border-primary has-[:checked]:bg-primary-soft">
            <input
              type="checkbox"
              checked={checked}
              onChange={(event) => setChecked(event.target.checked)}
              className="mt-0.5 size-5 shrink-0 cursor-pointer accent-[var(--primary)]"
            />
            <span className="text-foreground">
              I have read this notice and understand that my assessment results are used for learning and development only.
            </span>
          </label>
        )}
      </Card>

      {error ? <ErrorState error={error} /> : null}

      <StepActions>
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft aria-hidden="true" />
          Back
        </Button>
        {acknowledged ? (
          <Button size="lg" onClick={onNext}>
            Continue
            <ArrowRight aria-hidden="true" />
          </Button>
        ) : (
          <Button size="lg" onClick={acknowledge} disabled={!checked || busy} aria-describedby={checked ? undefined : "notice-hint"}>
            {busy ? "Saving..." : "Acknowledge and continue"}
            {busy ? null : <ArrowRight aria-hidden="true" />}
          </Button>
        )}
      </StepActions>
      {!acknowledged && !checked ? (
        <p id="notice-hint" className="-mt-3 text-right text-sm text-muted-foreground">
          Tick the box above to continue.
        </p>
      ) : null}
    </section>
  );
}

function NoticePoint({ icon, title, children }: { icon: ReactNode; title: string; children: ReactNode }) {
  return (
    <div className="space-y-1.5">
      <p className="flex items-center gap-2 font-medium text-foreground [&_svg]:size-4 [&_svg]:text-primary">
        <span aria-hidden="true">{icon}</span>
        {title}
      </p>
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  );
}

// --- Step 3: job role ------------------------------------------------------------------------------------

function RolePicker({
  selected,
  onSelect,
  disabled,
}: {
  selected: string | null;
  onSelect: (id: string) => void;
  disabled?: boolean;
}) {
  const roles = useApi<JobRole[]>("/api/v1/job-roles");
  const requirements = useApi<JobRoleCompetencies>(selected ? `/api/v1/job-roles/${selected}/competencies` : null);

  if (roles.loading) return <LoadingState label="Loading job roles" lines={4} />;
  if (roles.error) return <ErrorState error={roles.error} onRetry={roles.reload} />;
  if (!roles.data || roles.data.length === 0) {
    return (
      <EmptyState title="Your organisation hasn't set up job roles yet." icon={<BriefcaseBusiness className="size-5" />}>
        <p>Contact your administrator. You can continue once a job role is available.</p>
      </EmptyState>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
      <fieldset className="space-y-3">
        <legend className="mb-3 text-sm font-semibold text-foreground">Job role</legend>
        {roles.data.map((role) => (
          <RadioCard
            key={role.id}
            name="job-role"
            value={role.id}
            checked={selected === role.id}
            onChange={() => onSelect(role.id)}
            disabled={disabled}
            description={role.description ?? undefined}
          >
            <span className="font-medium">{role.name}</span> {role.is_demo ? <DemoBadge /> : null}
          </RadioCard>
        ))}
      </fieldset>

      <div aria-live="polite">
        {!selected ? (
          <div className="flex h-full min-h-40 items-center justify-center rounded-lg border border-dashed border-border p-6 text-center text-sm text-muted-foreground">
            Select a job role to see the competencies it requires.
          </div>
        ) : requirements.loading ? (
          <Card className="p-5">
            <LoadingState label="Loading requirements" />
          </Card>
        ) : requirements.error ? (
          <ErrorState error={requirements.error} onRetry={requirements.reload} />
        ) : requirements.data && requirements.data.requirements.length === 0 ? (
          <EmptyState title="This job role's requirements haven't been approved yet.">
            <p>You can still select it, but there is nothing to assess until requirements are approved.</p>
          </EmptyState>
        ) : requirements.data ? (
          <Card className="p-5">
            <h2 className="text-base font-semibold">What this role requires</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              {requirements.data.requirements.length} competenc{requirements.data.requirements.length === 1 ? "y" : "ies"}, each
              with a required level.
            </p>
            <ul className="mt-4 space-y-4">
              {requirements.data.requirements.map((req) => (
                <li key={req.competency.id} className="space-y-2">
                  <div className="flex flex-wrap items-baseline justify-between gap-2">
                    <span className="font-medium text-foreground">{req.competency.name}</span>
                    <span className="text-sm text-muted-foreground">
                      Level {req.required_level} of {req.levels.length} required
                    </span>
                  </div>
                  <LevelScale levels={req.levels.length} estimated={null} required={req.required_level} label={req.competency.name} />
                </li>
              ))}
            </ul>
            {requirements.data.requirements.some((r) => r.levels.some((l) => l.threshold_status !== "approved")) ? (
              <p className="mt-4 text-xs text-muted-foreground">Level definitions are provisional and have not been statistically validated.</p>
            ) : null}
          </Card>
        ) : null}
      </div>
    </div>
  );
}

function useSaveRole() {
  const { user, setUser } = useAuth();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  async function save(roleId: string): Promise<boolean> {
    if (user?.job_role?.id === roleId) return true;
    setBusy(true);
    setError(null);
    try {
      setUser(await api<Me>("/api/v1/me/job-role", { method: "PUT", body: { job_role_id: roleId } }));
      return true;
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Could not save", "Your job role was not saved. Try again."));
      return false;
    } finally {
      setBusy(false);
    }
  }
  return { save, busy, error };
}

function RoleStep({ user, headingRef, onBack, onNext }: { user: Me; headingRef: HeadingRef; onBack: () => void; onNext: () => void }) {
  const [selected, setSelected] = useState<string | null>(user.job_role?.id ?? null);
  const { save, busy, error } = useSaveRole();
  return (
    <section className="flex flex-col gap-6" aria-label="Select your job role">
      <StepHeader headingRef={headingRef} title="Select your job role">
        Your job role decides which competencies are assessed and which learning is suggested. You can change it later.
      </StepHeader>
      <RolePicker selected={selected} onSelect={setSelected} disabled={busy} />
      {error ? <ErrorState error={error} /> : null}
      <StepActions>
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft aria-hidden="true" />
          Back
        </Button>
        <Button size="lg" disabled={!selected || busy} onClick={async () => selected && (await save(selected)) && onNext()}>
          {busy ? "Saving..." : "Confirm job role"}
          {busy ? null : <ArrowRight aria-hidden="true" />}
        </Button>
      </StepActions>
    </section>
  );
}

// --- Step 4: explain the assessment ------------------------------------------------------------------------

function AssessmentStep({ user, headingRef, onBack }: { user: Me; headingRef: HeadingRef; onBack: () => void }) {
  const navigate = useNavigate();
  const assessments = useApi<AssessmentSummary[]>("/api/v1/assessments");
  const assessment = assessments.data?.[0];
  const completed = assessment?.latest_attempt?.status === "scored";

  return (
    <section className="flex flex-col gap-6" aria-label="Your baseline assessment">
      <StepHeader headingRef={headingRef} title="Your baseline assessment">
        A short multiple-choice assessment gives a first estimate of where you stand in each competency for{" "}
        <span className="font-medium text-foreground">{user.job_role?.name}</span>.
      </StepHeader>

      {assessments.loading ? (
        <Card className="p-6">
          <LoadingState label="Loading assessment details" />
        </Card>
      ) : assessments.error ? (
        <ErrorState error={assessments.error} onRetry={assessments.reload} />
      ) : !assessment ? (
        <EmptyState title="No assessment is available for this job role yet." icon={<ClipboardCheck className="size-5" />}>
          <p>You can still explore your dashboard. Your trainer will let you know when an assessment is published.</p>
        </EmptyState>
      ) : (
        <Card className="p-6 sm:p-8">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="text-lg font-semibold">{assessment.title}</h2>
            {assessment.is_demo ? <DemoBadge /> : null}
          </div>
          <dl className="mt-5 grid gap-4 sm:grid-cols-3">
            <Fact icon={<ListChecks />} label="Questions" value={`${assessment.question_count} multiple choice`} />
            <Fact icon={<Clock />} label="Time" value="No time limit" hint={questionTimeGuide(assessment.question_count)} />
            <Fact icon={<Save />} label="Progress" value="Saved as you answer" />
          </dl>
          <h3 className="mt-8 font-semibold">What to expect</h3>
          <ol className="mt-3 space-y-3">
            <Expect n={1}>Answer one question at a time. You can go back and change answers before you submit.</Expect>
            <Expect n={2}>Leave and come back whenever you like; your answers stay saved.</Expect>
            <Expect n={3}>After you submit, you see your estimated level for each competency and suggested next steps.</Expect>
          </ol>
          <p className="mt-6 text-sm text-muted-foreground">
            In this release the baseline can be taken once. Answer on your own so the estimate reflects where you are today.
          </p>
        </Card>
      )}

      <StepActions>
        <Button variant="ghost" onClick={onBack}>
          <ArrowLeft aria-hidden="true" />
          Back
        </Button>
        <div className="flex flex-col-reverse gap-3 sm:flex-row">
          <Button variant="secondary" size="lg" asChild>
            <Link to="/">Go to my dashboard</Link>
          </Button>
          {assessment ? (
            <Button size="lg" onClick={() => navigate(completed ? `/attempts/${assessment.latest_attempt!.id}/result` : "/assessment")}>
              {completed ? "View my result" : "Continue to the assessment"}
              <ArrowRight aria-hidden="true" />
            </Button>
          ) : null}
        </div>
      </StepActions>
    </section>
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
      <dd className="font-medium text-foreground">
        {value}
        {hint ? <span className="block text-sm font-normal text-muted-foreground">{hint}</span> : null}
      </dd>
    </div>
  );
}

function Expect({ n, children }: { n: number; children: ReactNode }) {
  return (
    <li className="flex gap-3">
      <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-primary-soft text-xs font-semibold text-primary" aria-hidden="true">
        {n}
      </span>
      <span className="text-foreground">{children}</span>
    </li>
  );
}

// --- Change job role (already onboarded) -----------------------------------------------------------------------

function ChangeJobRole({ user }: { user: Me }) {
  const navigate = useNavigate();
  const [selected, setSelected] = useState<string | null>(user.job_role?.id ?? null);
  const { save, busy, error } = useSaveRole();
  const unchanged = selected === user.job_role?.id;

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-6">
      <header className="space-y-2">
        <p className="flex items-center gap-2 text-sm font-semibold text-primary">
          <BookOpenCheck className="size-4" aria-hidden="true" /> Settings
        </p>
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Your job role</h1>
        <p className="max-w-2xl text-base text-muted-foreground">
          Your job role decides which competencies are assessed and which learning is suggested.
        </p>
      </header>
      <Alert tone="warning" title="Changing your role changes what you see">
        Your competency gaps and learning suggestions are recalculated for the competencies the new role requires.
      </Alert>
      <RolePicker selected={selected} onSelect={setSelected} disabled={busy} />
      {error ? <ErrorState error={error} /> : null}
      <StepActions>
        <Button variant="ghost" asChild>
          <Link to="/">
            <ArrowLeft aria-hidden="true" />
            Back to dashboard
          </Link>
        </Button>
        <Button
          size="lg"
          disabled={!selected || busy || unchanged}
          onClick={async () => {
            if (selected && (await save(selected))) {
              toast.success("Job role updated");
              navigate("/");
            }
          }}
        >
          {busy ? "Saving..." : "Save job role"}
        </Button>
      </StepActions>
    </div>
  );
}
