import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  CircleDashed,
  CircleHelp,
  ClipboardList,
  Info,
  LayoutDashboard,
  MinusCircle,
  Target,
  TrendingUp,
  XCircle,
} from "lucide-react";
import type { ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import type { Attempt, AttemptResult, GapItem, Gaps, JobRoleCompetencies, Recommendations } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { LevelScale } from "@/components/product/LevelScale";
import { DemoBadge, EmptyState, ErrorState, EvidenceBadge, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Disclosure } from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";

type Competency = AttemptResult["competencies"][number];

const percent = (score: string | null) => (score === null ? null : Math.round(Number(score) * 100));

/**
 * Assessment result (UI_UX_SPEC.md S-07): outcome in plain language first, then per-competency detail,
 * next steps, question feedback, and the scoring method only inside a disclosure. Development guidance, not appraisal.
 */
export function ResultPage() {
  const { attemptId } = useParams();
  const { user } = useAuth();
  const result = useApi<AttemptResult>(attemptId ? `/api/v1/attempts/${attemptId}/result` : null);
  const attempt = useApi<Attempt>(attemptId ? `/api/v1/attempts/${attemptId}` : null);
  const gaps = useApi<Gaps>("/api/v1/me/competency-gaps");
  const recommendations = useApi<Recommendations>("/api/v1/me/recommendations");
  const requirements = useApi<JobRoleCompetencies>(user?.job_role ? `/api/v1/job-roles/${user.job_role.id}/competencies` : null);

  if (result.loading) {
    return (
      <Card className="p-6">
        <LoadingState label="Loading your result" lines={6} />
      </Card>
    );
  }
  if (result.error) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <ErrorState error={result.error} onRetry={result.reload} />
        <Button variant="secondary" asChild>
          <Link to="/assessment">Back to the assessment</Link>
        </Button>
      </div>
    );
  }
  if (!result.data) return null;
  const data = result.data;
  const gapByCompetency = new Map((gaps.data?.items ?? []).map((item) => [item.competency.id, item]));
  const levelsByCompetency = new Map((requirements.data?.requirements ?? []).map((r) => [r.competency.id, r.levels]));
  const scoredOn = new Date(data.scored_at).toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" });

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Baseline assessment", to: "/assessment" }, { label: "Your result" }]}
        title="Your baseline result"
        description={`${data.assessment.title} · completed ${scoredOn}`}
        meta={
          <>
            {data.is_baseline ? <Badge tone="info">Baseline</Badge> : null}
            {data.assessment.is_demo ? <DemoBadge /> : null}
          </>
        }
        actions={
          <Button variant="secondary" asChild>
            <Link to="/">
              <LayoutDashboard aria-hidden="true" />
              Go to my dashboard
            </Link>
          </Button>
        }
        className="pb-0"
      />

      <Alert tone="info" title="Development guidance, not an appraisal">
        Use this result to plan your learning. It is not used for appraisal, promotion or eligibility decisions.
      </Alert>

      <div className="grid gap-5 lg:grid-cols-[20rem_minmax(0,1fr)]">
        <OverallScore result={data} />
        <WhatThisMeans competencies={data.competencies} gaps={gaps} gapByCompetency={gapByCompetency} />
      </div>

      <section aria-labelledby="by-competency" className="space-y-4">
        <div>
          <h2 id="by-competency" className="text-xl font-semibold">
            Result by competency
          </h2>
          <p className="text-muted-foreground">Your estimated level compared with the level your job role requires.</p>
        </div>
        <ul className="grid gap-4 md:grid-cols-2">
          {data.competencies.map((c) => (
            <CompetencyResult key={c.competency.id} item={c} gap={gapByCompetency.get(c.competency.id)} levels={levelsByCompetency.get(c.competency.id)?.length} />
          ))}
        </ul>
        {gaps.error ? <ErrorState error={gaps.error} onRetry={gaps.reload} /> : null}
      </section>

      <NextSteps gaps={gaps.data} recommendations={recommendations} />

      <QuestionReview result={data} attempt={attempt.data} attemptError={attempt.error !== null} />

      <Methodology result={data} requirements={requirements.data} />
    </div>
  );
}

// --- Summary -----------------------------------------------------------------------------------------

function OverallScore({ result }: { result: AttemptResult }) {
  const score = percent(result.score_total) ?? 0;
  const marked = result.questions.filter((q) => q.is_correct !== null);
  const correct = marked.filter((q) => q.is_correct).length;
  const radius = 52;
  const circumference = 2 * Math.PI * radius;
  return (
    <Card as="section" aria-labelledby="overall-score" className="flex flex-col items-center gap-4 p-6 text-center">
      <h2 id="overall-score" className="self-start text-base font-semibold">
        Overall score
      </h2>
      <div className="relative size-40" role="img" aria-label={`Overall score ${score} out of 100`}>
        <svg viewBox="0 0 120 120" className="size-40 -rotate-90" aria-hidden="true">
          <circle cx="60" cy="60" r={radius} fill="none" stroke="var(--muted)" strokeWidth="10" />
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke="var(--primary)"
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference * (1 - score / 100)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center" aria-hidden="true">
          <span className="text-4xl font-semibold tabular-nums">{score}</span>
          <span className="text-sm text-muted-foreground">out of 100</span>
        </div>
      </div>
      {marked.length > 0 ? (
        <p className="font-medium">
          {correct} of {result.questions.length} questions correct
        </p>
      ) : null}
      <p className="text-sm text-muted-foreground">Harder questions count a little more towards the score.</p>
    </Card>
  );
}

const STATUS: Record<string, { label: string; tone: "warning" | "success" | "info" | "neutral"; icon: ReactNode }> = {
  gap: { label: "Developing", tone: "warning", icon: <TrendingUp aria-hidden="true" /> },
  meets_requirement: { label: "Meets requirement", tone: "success", icon: <CheckCircle2 aria-hidden="true" /> },
  insufficient_evidence: { label: "Reassess to confirm", tone: "info", icon: <CircleHelp aria-hidden="true" /> },
  level_unavailable: { label: "Level not available", tone: "neutral", icon: <CircleDashed aria-hidden="true" /> },
  not_assessed: { label: "Not assessed", tone: "neutral", icon: <CircleDashed aria-hidden="true" /> },
};

function WhatThisMeans({
  competencies,
  gaps,
  gapByCompetency,
}: {
  competencies: Competency[];
  gaps: { loading: boolean; error: unknown };
  gapByCompetency: Map<string, GapItem>;
}) {
  const items = competencies.map((c) => gapByCompetency.get(c.competency.id)).filter((g): g is GapItem => Boolean(g));
  const developing = items.filter((g) => g.status === "gap");
  const meets = items.filter((g) => g.status === "meets_requirement");
  const unsure = items.filter((g) => g.status === "insufficient_evidence" || g.status === "level_unavailable");
  const total = competencies.length;

  let headline: string;
  if (items.length === 0) headline = "Your estimated level for each competency is shown below.";
  else if (developing.length === 0 && unsure.length === 0)
    headline = total === 1 ? "You meet the level your role requires." : `You meet the level your role requires in ${total === 2 ? "both" : `all ${total}`} competencies.`;
  else if (developing.length === total)
    headline = `${total === 1 ? "Your competency is" : total === 2 ? "Both competencies are" : `All ${total} competencies are`} below the level your role requires. That is a clear starting point for learning.`;
  else if (developing.length > 0) headline = `${developing.length} of ${total} competencies ${developing.length === 1 ? "is" : "are"} below the level your role requires. Start your learning there.`;
  else headline = "There is not enough evidence yet to confirm where you stand in some competencies.";

  return (
    <Card as="section" aria-labelledby="what-this-means" className="flex flex-col gap-5 p-6">
      <div className="space-y-2">
        <h2 id="what-this-means" className="text-base font-semibold">
          What this means
        </h2>
        <p className="text-xl font-semibold leading-snug text-balance">{headline}</p>
        <p className="text-muted-foreground">
          This is a snapshot from {competencies.reduce((n, c) => n + c.evidence_count, 0)} questions, not a judgement of your ability. Everyone has
          competencies they are still developing; the aim is to show where learning will help most.
        </p>
      </div>
      {gaps.loading ? (
        <LoadingState label="Comparing with your role" lines={2} />
      ) : items.length > 0 ? (
        <dl className="grid gap-3 sm:grid-cols-3">
          <SummaryCount tone="warning" icon={<TrendingUp />} label="Developing" value={developing.length} hint="Below the required level" />
          <SummaryCount tone="success" icon={<CheckCircle2 />} label="Meets requirement" value={meets.length} hint="At or above the required level" />
          <SummaryCount tone="info" icon={<CircleHelp />} label="Reassess to confirm" value={unsure.length} hint="Not enough evidence yet" />
        </dl>
      ) : null}
    </Card>
  );
}

function SummaryCount({ tone, icon, label, value, hint }: { tone: "warning" | "success" | "info"; icon: ReactNode; label: string; value: number; hint: string }) {
  const tones = { warning: "bg-warning-soft text-warning", success: "bg-success-soft text-success", info: "bg-info-soft text-info" };
  return (
    <div className={cn("flex flex-col gap-1 rounded-lg p-4", tones[tone])}>
      <dt className="flex items-center gap-2 text-sm font-medium [&_svg]:size-4">
        <span aria-hidden="true">{icon}</span>
        {label}
      </dt>
      <dd>
        <span className="text-2xl font-semibold tabular-nums">{value}</span>
        <span className="block text-sm opacity-90">{hint}</span>
      </dd>
    </div>
  );
}

// --- Per competency -----------------------------------------------------------------------------------------

function explanationFor(item: Competency, gap: GapItem | undefined): string {
  if (!gap) return "Compared with your role when your role requirements are available.";
  switch (gap.status) {
    case "gap":
      return `${gap.gap} level${gap.gap === 1 ? "" : "s"} below what your role requires. Learning suggestions focus here.`;
    case "meets_requirement":
      return "At or above what your role requires. Keep it current by applying it in your work.";
    case "insufficient_evidence":
      return `Only ${item.evidence_count} question${item.evidence_count === 1 ? "" : "s"} measured this, so the estimate needs more evidence before a gap is confirmed.`;
    case "level_unavailable":
      return "A level could not be estimated because level thresholds are not set up for this competency.";
    default:
      return "Not assessed yet.";
  }
}

function CompetencyResult({ item, gap, levels }: { item: Competency; gap: GapItem | undefined; levels: number | undefined }) {
  const status = STATUS[gap?.status ?? "not_assessed"];
  const levelCount = levels ?? (gap ? gap.max_level_span + 1 : 4);
  return (
    <Card as="li" className="flex flex-col gap-4 p-5">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <h3 className="min-w-0 font-semibold text-foreground">
          {item.competency.name} {item.competency.is_demo ? <DemoBadge /> : null}
        </h3>
        {gap ? (
          <Badge tone={status.tone}>
            {status.icon}
            {status.label}
          </Badge>
        ) : null}
      </div>

      <dl className="grid grid-cols-3 gap-2 text-center">
        <LevelFact label="Estimated level" value={item.level_number !== null ? `${item.level_number}` : "-"} strong />
        <LevelFact label="Required level" value={gap ? `${gap.required_level}` : "-"} />
        <LevelFact label="Score" value={percent(item.score) !== null ? `${percent(item.score)}` : "-"} suffix="/ 100" />
      </dl>

      <LevelScale levels={levelCount} estimated={item.level_number} required={gap?.required_level ?? null} label={item.competency.name} />

      <p className="text-sm text-foreground">{explanationFor(item, gap)}</p>
      <div className="flex flex-wrap items-center gap-2">
        <EvidenceBadge band={item.evidence_band} count={item.evidence_count} />
        {item.thresholds_status !== "approved" ? <Badge tone="neutral">Provisional levels</Badge> : null}
      </div>
    </Card>
  );
}

function LevelFact({ label, value, suffix, strong = false }: { label: string; value: string; suffix?: string; strong?: boolean }) {
  return (
    <div className="rounded-lg bg-muted/60 px-2 py-3">
      <dt className="text-xs text-muted-foreground">{label}</dt>
      <dd className={cn("mt-0.5 tabular-nums", strong ? "text-2xl font-semibold text-foreground" : "text-2xl text-foreground")}>
        {value}
        {suffix && value !== "-" ? <span className="ml-1 text-sm text-muted-foreground">{suffix}</span> : null}
      </dd>
    </div>
  );
}

// --- Next steps ------------------------------------------------------------------------------------------------

function NextSteps({ gaps, recommendations }: { gaps: Gaps | null; recommendations: { data: Recommendations | null; loading: boolean; error: import("@/api/client").ApiError | null; reload: () => void } }) {
  const developing = (gaps?.items ?? []).filter((g) => g.status === "gap").sort((a, b) => (b.gap ?? 0) - (a.gap ?? 0));
  const top = recommendations.data?.items.slice(0, 3) ?? [];

  return (
    <section aria-labelledby="next-steps" className="space-y-4">
      <div>
        <h2 id="next-steps" className="text-xl font-semibold">
          What to do next
        </h2>
        <p className="text-muted-foreground">Three steps to turn this result into progress.</p>
      </div>
      <ol className="grid items-start gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.3fr)_minmax(0,1fr)]">
        <StepCard n={1} icon={<Target />} title="Look at your competency gaps">
          {developing.length > 0 ? (
            <p>
              Focus first on <span className="font-medium text-foreground">{developing[0].competency.name}</span>
              {developing[0].gap ? ` (${developing[0].gap} level${developing[0].gap === 1 ? "" : "s"} to go)` : ""}.
            </p>
          ) : (
            <p>No confirmed gaps. Your dashboard shows each competency and the evidence behind it.</p>
          )}
          <Button variant="secondary" className="mt-1 self-start" asChild>
            <Link to="/competencies/gaps">
              View competency gaps
              <ArrowRight aria-hidden="true" />
            </Link>
          </Button>
        </StepCard>

        <StepCard n={2} icon={<BookOpen />} title="Start recommended learning" primary>
          {recommendations.loading ? (
            <LoadingState label="Loading recommendations" lines={2} />
          ) : recommendations.error ? (
            <ErrorState error={recommendations.error} onRetry={recommendations.reload} />
          ) : top.length === 0 ? (
            <p>No approved learning content matches your gaps yet. Your trainer can suggest resources in the meantime.</p>
          ) : (
            <ul className="space-y-2.5">
              {top.map((rec) => {
                const reason = rec.reasons.find((r) => r.rule === "gap_match");
                return (
                  <li key={rec.course.id} className="rounded-lg border border-border bg-card p-3">
                    <p className="font-medium text-foreground">
                      <Link to={`/courses/${rec.course.id}`} className="underline-offset-4 hover:text-primary hover:underline">
                        {rec.course.title}
                      </Link>{" "}
                      {rec.course.is_demo ? <DemoBadge label="DEMO" /> : null}
                    </p>
                    <p className="mt-0.5 text-sm text-muted-foreground">
                      {reason?.competency_name ? `Helps with ${reason.competency_name}` : rec.course.provider_organisation}
                      {rec.course.duration_days ? ` · ${rec.course.duration_days} day${rec.course.duration_days === 1 ? "" : "s"}` : ""}
                    </p>
                  </li>
                );
              })}
            </ul>
          )}
          <Button className="mt-1 self-start" asChild>
            <Link to="/courses">
              See recommended learning
              <ArrowRight aria-hidden="true" />
            </Link>
          </Button>
        </StepCard>

        <StepCard n={3} icon={<ClipboardList />} title="Learn from your answers">
          <p>Each question below shows your answer and a short explanation. Reviewing the ones you missed is a quick win.</p>
          <Button variant="secondary" className="mt-1 self-start" asChild>
            <a href="#question-review">
              Review your answers
              <ArrowRight aria-hidden="true" />
            </a>
          </Button>
        </StepCard>
      </ol>
      <p className="flex items-start gap-2 text-sm text-muted-foreground">
        <Info className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
        Reassessment is not available in this release, so this baseline stays as your starting point.
      </p>
    </section>
  );
}

function StepCard({ n, icon, title, primary = false, children }: { n: number; icon: ReactNode; title: string; primary?: boolean; children: ReactNode }) {
  return (
    <Card as="li" className={cn("flex flex-col gap-3 p-5", primary && "border-primary/40 bg-primary-soft/40")}>
      <div className="flex items-center gap-3">
        <span className="flex size-9 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground" aria-hidden="true">
          {n}
        </span>
        <h3 className="flex items-center gap-2 font-semibold [&_svg]:size-4 [&_svg]:text-primary">
          <span aria-hidden="true">{icon}</span>
          <span>
            <span className="sr-only">Step {n}: </span>
            {title}
          </span>
        </h3>
      </div>
      <div className="flex flex-1 flex-col gap-3 text-sm text-muted-foreground">{children}</div>
    </Card>
  );
}

// --- Question review -------------------------------------------------------------------------------------------------

function QuestionReview({ result, attempt, attemptError }: { result: AttemptResult; attempt: Attempt | null; attemptError: boolean }) {
  const optionsByQuestion = new Map((attempt?.questions ?? []).map((q) => [q.question_version_id, q.options]));
  const textOf = (questionVersionId: string, optionId: string | null) =>
    optionId ? optionsByQuestion.get(questionVersionId)?.find((o) => o.id === optionId)?.text ?? null : null;
  const policyShowsCorrectness = result.feedback_policy !== "score_only";

  return (
    <section id="question-review" aria-labelledby="question-review-title" className="scroll-mt-24 space-y-4">
      <div>
        <h2 id="question-review-title" className="text-xl font-semibold">
          Your answers
        </h2>
        <p className="text-muted-foreground">
          {policyShowsCorrectness ? "Open a question to see the correct answer and why." : "Feedback for individual questions is not shown for this assessment."}
        </p>
      </div>
      {attemptError ? <p className="text-sm text-muted-foreground">Answer text could not be loaded; correctness is still shown.</p> : null}
      {result.questions.length === 0 ? (
        <EmptyState title="No questions to review." />
      ) : (
        <ol className="space-y-2">
          {[...result.questions].sort((a, b) => a.position - b.position).map((q) => {
            const state = q.selected_option_id === null ? "unanswered" : q.is_correct === null ? "unknown" : q.is_correct ? "correct" : "incorrect";
            const badge = {
              correct: <Badge tone="success"><CheckCircle2 aria-hidden="true" />Correct</Badge>,
              incorrect: <Badge tone="warning"><XCircle aria-hidden="true" />Not correct</Badge>,
              unanswered: <Badge tone="neutral"><MinusCircle aria-hidden="true" />Not answered</Badge>,
              unknown: null,
            }[state];
            const yours = textOf(q.question_version_id, q.selected_option_id);
            const right = textOf(q.question_version_id, q.correct_option_id);
            return (
              <li key={q.question_version_id}>
                <details className="group rounded-lg border border-border bg-card open:shadow-card">
                  <summary className="flex min-h-14 cursor-pointer list-none items-center gap-3 rounded-lg px-4 py-3 hover:bg-muted/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring [&::-webkit-details-marker]:hidden">
                    <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-muted text-sm font-semibold tabular-nums text-muted-foreground" aria-hidden="true">
                      {q.position}
                    </span>
                    <span className="min-w-0 flex-1 text-foreground">
                      <span className="sr-only">Question {q.position}: </span>
                      {q.stem}
                    </span>
                    {badge}
                  </summary>
                  <div className="space-y-2 border-t border-border px-4 py-3 pl-14 text-sm">
                    <p>
                      <span className="text-muted-foreground">Your answer: </span>
                      <span className="font-medium">{q.selected_option_id === null ? "Not answered" : yours ?? "Selected"}</span>
                    </p>
                    {q.correct_option_id && state !== "correct" ? (
                      <p>
                        <span className="text-muted-foreground">Correct answer: </span>
                        <span className="font-medium">{right ?? "See explanation"}</span>
                      </p>
                    ) : null}
                    {q.explanation ? <p className="text-muted-foreground">{q.explanation}</p> : null}
                  </div>
                </details>
              </li>
            );
          })}
        </ol>
      )}
    </section>
  );
}

// --- Methodology (collapsed by default) -------------------------------------------------------------------------------

function Methodology({ result, requirements }: { result: AttemptResult; requirements: JobRoleCompetencies | null }) {
  const method = result.competencies[0]?.method_version;
  const levels = requirements?.requirements[0]?.levels ?? [];
  return (
    <Disclosure title="How was this calculated?" className="bg-card">
      <div className="space-y-3 text-foreground">
        <p>
          Each answer is marked correct or not correct by fixed rules; no AI is involved. Harder questions carry more weight
          (foundational 1, intermediate 1.5, advanced 2). A competency's score is the weighted share of marks earned on the
          questions that measured it, and the overall score does the same across all questions.
        </p>
        {levels.some((l) => l.min_score !== null) ? (
          <p>
            Levels come from score thresholds:{" "}
            {levels
              .filter((l) => l.min_score !== null)
              .map((l) => `${l.label} from ${Math.round(Number(l.min_score) * 100)}`)
              .join(", ")}
            . {levels.some((l) => l.threshold_status !== "approved") ? "These thresholds are provisional and have not been statistically validated." : ""}
          </p>
        ) : null}
        <p>
          Evidence strength depends on how many questions measured a competency: fewer than 3 is insufficient, 3-4 low, 5-9
          medium, 10 or more high. A gap is only confirmed with medium or high evidence.
        </p>
        <p className="text-muted-foreground">
          Limitations: multiple-choice questions measure knowledge, not everything a role involves, and this is one attempt.
          {method ? ` Method version: ${method}.` : ""}
        </p>
      </div>
    </Disclosure>
  );
}
