import { ArrowRight, BookOpen, BriefcaseBusiness, CalendarClock, ClipboardCheck, Gauge, Target } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import type { ApiError } from "@/api/client";
import type { AssessmentSummary, AttemptHistoryItem, Gaps, JobRoleCompetencies, Me, MyProgress, Recommendations } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { cleanName, CompetencyStatusBadge, DifficultyBadge, durationLabel } from "@/components/product/competency";
import { LearnerJourney, type JourneyStep } from "@/components/product/LearnerJourney";
import { LevelScale } from "@/components/product/LevelScale";
import { CourseProgressBar } from "@/components/product/learning";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PRODUCT } from "@/config/product";
import { cn } from "@/lib/utils";

interface State<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
  reload: () => void;
}

/**
 * Learner dashboard (UI_UX_SPEC.md S-03, MVP-19): orientation and the next action, built on the learner loop.
 * Every card loads and fails independently. No readiness score (ROLE-008 is P1) and no invented activity metrics.
 */
export function DashboardPage() {
  const { user } = useAuth();
  if (!user) return null;
  if (!user.can_take_assessments) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <h1 className="text-2xl font-semibold">Welcome, {user.display_name}</h1>
        <EmptyState title="Your access role does not include learning features.">
          <p>Your roles: {user.access_roles.join(", ")}. You can still browse the course catalogue.</p>
        </EmptyState>
        <Button variant="secondary" asChild>
          <Link to="/courses">Browse courses</Link>
        </Button>
      </div>
    );
  }
  return <LearnerDashboard user={user} />;
}

function LearnerDashboard({ user }: { user: Me }) {
  const assessments = useApi<AssessmentSummary[]>("/api/v1/assessments");
  const gaps = useApi<Gaps>("/api/v1/me/competency-gaps");
  const recommendations = useApi<Recommendations>("/api/v1/me/recommendations");
  const attempts = useApi<AttemptHistoryItem[]>("/api/v1/me/attempts");
  const progress = useApi<MyProgress>("/api/v1/me/progress");
  const requirements = useApi<JobRoleCompetencies>(user.job_role ? `/api/v1/job-roles/${user.job_role.id}/competencies` : null);

  const assessment = assessments.data?.[0];
  const status = assessment?.latest_attempt?.status;
  const baselineDone = status === "scored";
  const items = gaps.data?.items ?? [];
  const developing = items.filter((i) => i.status === "gap").sort((a, b) => (b.gap ?? 0) - (a.gap ?? 0));
  const atLevel = items.filter((i) => i.status === "meets_requirement").length;
  const levelsById = new Map((requirements.data?.requirements ?? []).map((r) => [r.competency.id, r.levels]));

  const journey: JourneyStep[] = [
    { id: "role", label: "Job role", detail: user.job_role ? cleanName(user.job_role.name) : "Choose a role", state: user.job_role ? "done" : "current", to: "/get-started" },
    { id: "requirements", label: "Requirements", detail: items.length ? `${items.length} competencies` : "What your role needs", state: items.length ? "done" : "next", to: "/competencies" },
    { id: "baseline", label: "Baseline", detail: baselineDone ? "Completed" : status === "in_progress" ? "In progress" : "Not started", state: baselineDone ? "done" : "current", to: "/assessment" },
    { id: "gaps", label: "Gap analysis", detail: baselineDone ? `${developing.length} to develop` : "After the baseline", state: baselineDone ? (developing.length ? "current" : "done") : "next", to: "/competencies/gaps" },
    { id: "learning", label: "Learning path", detail: recommendations.data?.items.length ? `${recommendations.data.items.length} courses suggested` : "Suggested courses", state: baselineDone && developing.length && !progress.data?.totals.courses_started ? "current" : baselineDone && progress.data?.totals.courses_started ? "done" : "next", to: "/learning-path" },
    { id: "progress", label: "Progress", detail: progress.data?.totals.lessons_completed ? `${progress.data.totals.lessons_completed} lessons completed` : "Lessons you complete", state: progress.data?.in_progress.length ? "current" : progress.data?.totals.courses_completed ? "done" : "next", to: "/learning-path" },
    { id: "reassess", label: "Reassessment", detail: "Updated profile", state: "later" },
  ];

  return (
    <div className="flex flex-col gap-6">
      <Hero user={user} assessment={assessment} assessmentsState={assessments} developing={developing} topCourse={courseForGap(recommendations.data, developing[0])} progress={progress.data} />

      <Card as="section" aria-labelledby="journey-title" className="p-5">
        <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="journey-title" className="text-base font-semibold">Your learning journey</h2>
          <p className="text-sm text-muted-foreground">From role requirements to evidence-based learning. Reassessment arrives in a later release.</p>
        </div>
        <LearnerJourney steps={journey} />
      </Card>

      <section aria-label="At a glance" className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Glance icon={<Gauge />} label="At required level" loading={gaps.loading}
          value={baselineDone ? `${atLevel} of ${items.length}` : "-"} hint={baselineDone ? "competencies for your role" : "after your baseline"} />
        <Glance icon={<Target />} label="Confirmed gaps" loading={gaps.loading}
          value={baselineDone ? String(developing.length) : "-"} hint={developing[0] ? `Largest: ${cleanName(developing[0].competency.name)}` : baselineDone ? "none confirmed" : "after your baseline"} />
        <Glance icon={<BookOpen />} label="Suggested courses" loading={recommendations.loading}
          value={recommendations.data ? String(recommendations.data.items.length) : "-"} hint="linked to your gaps" />
        <Glance icon={<CalendarClock />} label="Baseline assessment" loading={attempts.loading}
          value={latestScore(attempts.data)} hint={attempts.data?.[0]?.scored_at ? `completed ${shortDate(attempts.data[0].scored_at)}` : "not completed yet"} />
      </section>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] [&>*]:min-w-0">
        <PriorityGaps state={gaps} developing={developing} baselineDone={baselineDone} levelsById={levelsById} />
        <CompetencyOverview state={gaps} levelsById={levelsById} baselineDone={baselineDone} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] [&>*]:min-w-0">
        <div className="flex flex-col gap-6">
          <ContinueLearning state={progress} />
          <RecommendedLearning state={recommendations} baselineDone={baselineDone} />
        </div>
        <RecentActivity state={attempts} />
      </div>
    </div>
  );
}

/** The highest-ranked recommendation that addresses this gap, so the hero's competency and course always match. */
function courseForGap(recs: Recommendations | null, gap: Gaps["items"][number] | undefined) {
  if (!recs || !gap) return undefined;
  return recs.items.find((r) => r.reasons.some((reason) => reason.rule === "gap_match" && reason.competency_code === gap.competency.code));
}

function latestScore(attempts: AttemptHistoryItem[] | null): string {
  const scored = attempts?.find((a) => a.score_total !== null);
  return scored ? `${Math.round(Number(scored.score_total) * 100)} / 100` : "-";
}

function shortDate(value: string): string {
  return new Date(value).toLocaleDateString(undefined, { day: "numeric", month: "short" });
}

// --- Hero with the single primary next action -------------------------------------------------------------

function Hero({
  user,
  assessment,
  assessmentsState,
  developing,
  topCourse,
  progress,
}: {
  user: Me;
  assessment: AssessmentSummary | undefined;
  assessmentsState: State<AssessmentSummary[]>;
  developing: Gaps["items"];
  topCourse: Recommendations["items"][number] | undefined;
  progress: MyProgress | null;
}) {
  const resume = progress?.in_progress[0];
  const status = assessment?.latest_attempt?.status;
  let next: { eyebrow: string; title: string; body: string; action: ReactNode };
  if (!assessment && !assessmentsState.loading) {
    next = { eyebrow: "Next step", title: "Explore the course catalogue", body: "No baseline assessment is published for your role yet.", action: <PrimaryLink to="/courses">Browse courses</PrimaryLink> };
  } else if (status === "in_progress") {
    next = { eyebrow: "Next step", title: "Finish your baseline assessment", body: "Your answers are saved. Pick up where you left off.", action: <PrimaryLink to={`/assessment/attempts/${assessment!.latest_attempt!.id}`}>Resume assessment</PrimaryLink> };
  } else if (status !== "scored") {
    next = { eyebrow: "Next step", title: "Take your baseline assessment", body: `${assessment?.question_count ?? "A few"} questions show where you stand in each competency your role requires.`, action: <PrimaryLink to="/assessment">Start baseline assessment</PrimaryLink> };
  } else if (resume && resume.progress.resume_lesson) {
    next = {
      eyebrow: "Continue learning",
      title: cleanName(resume.course.title),
      body: `${resume.progress.completed_lessons} of ${resume.progress.lesson_count} lessons done. Next: ${resume.progress.resume_lesson.title}.`,
      action: <PrimaryLink to={`/courses/${resume.course.id}/lessons/${resume.progress.resume_lesson.id}`}>Continue lesson</PrimaryLink>,
    };
  } else if (developing[0]) {
    next = {
      eyebrow: "Your priority",
      title: `Develop ${cleanName(developing[0].competency.name)}`,
      body: topCourse ? `Start with "${cleanName(topCourse.course.title)}".` : "Your estimated level is below what your role requires.",
      action: topCourse ? <PrimaryLink to="/learning-path">Open your learning path</PrimaryLink> : <PrimaryLink to="/competencies/gaps">View gap analysis</PrimaryLink>,
    };
  } else {
    next = { eyebrow: "Next step", title: "Keep your competencies current", body: "No confirmed gaps for your role. Explore courses to go further.", action: <PrimaryLink to="/courses">Browse courses</PrimaryLink> };
  }

  return (
    <Card as="section" aria-labelledby="dashboard-title" className="overflow-hidden">
      <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_minmax(0,24rem)]">
        <div className="space-y-3 p-6 sm:p-8">
          <p className="text-sm font-medium text-muted-foreground">{PRODUCT.name}</p>
          <h1 id="dashboard-title" className="text-2xl font-semibold tracking-tight text-balance sm:text-3xl">
            Welcome back, {user.display_name}
          </h1>
          <p className="max-w-xl text-muted-foreground">
            See what your role requires, where your assessment evidence places you, and which learning closes the gaps.
          </p>
          {user.job_role ? (
            <p className="flex flex-wrap items-center gap-2 pt-1 text-sm">
              <BriefcaseBusiness className="size-4 text-muted-foreground" aria-hidden="true" />
              <span className="font-medium">{cleanName(user.job_role.name)}</span>
              <Link to="/get-started" className="text-primary underline-offset-4 hover:underline">Change</Link>
            </p>
          ) : null}
        </div>
        <div className="flex flex-col justify-center gap-3 border-t border-border bg-primary-soft/50 p-6 sm:p-8 lg:border-l lg:border-t-0">
          {assessmentsState.loading ? (
            <LoadingState label="Working out your next step" lines={3} />
          ) : assessmentsState.error ? (
            <ErrorState error={assessmentsState.error} onRetry={assessmentsState.reload} />
          ) : (
            <>
              <p className="text-xs font-semibold uppercase tracking-wide text-primary">{next.eyebrow}</p>
              <h2 className="text-xl font-semibold text-balance">{next.title}</h2>
              <p className="text-sm text-muted-foreground">{next.body}</p>
              <div className="pt-1">{next.action}</div>
            </>
          )}
        </div>
      </div>
    </Card>
  );
}

function PrimaryLink({ to, children }: { to: string; children: ReactNode }) {
  return (
    <Button size="lg" asChild>
      <Link to={to}>
        {children}
        <ArrowRight aria-hidden="true" />
      </Link>
    </Button>
  );
}

function Glance({ icon, label, value, hint, loading }: { icon: ReactNode; label: string; value: string; hint: string; loading: boolean }) {
  return (
    <Card className="flex min-w-0 flex-col gap-1 p-5">
      <p className="flex items-center gap-2 text-sm font-medium text-muted-foreground [&_svg]:size-4">
        <span aria-hidden="true">{icon}</span>
        {label}
      </p>
      {loading ? <LoadingState label={`Loading ${label}`} lines={1} className="py-2" /> : <p className="text-2xl font-semibold tabular-nums">{value}</p>}
      <p className="truncate text-sm text-muted-foreground" title={hint}>{hint}</p>
    </Card>
  );
}

function SectionCard({ id, title, action, children }: { id: string; title: string; action?: ReactNode; children: ReactNode }) {
  return (
    <Card as="section" aria-labelledby={id} className="flex flex-col gap-4 p-5 sm:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 id={id} className="text-base font-semibold">{title}</h2>
        {action}
      </div>
      {children}
    </Card>
  );
}

function ViewAll({ to, children }: { to: string; children: ReactNode }) {
  return (
    <Link to={to} className="inline-flex items-center gap-1 rounded-md text-sm font-medium text-primary underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
      {children}
      <ArrowRight className="size-4" aria-hidden="true" />
    </Link>
  );
}

// --- Cards ---------------------------------------------------------------------------------------------------

function PriorityGaps({ state, developing, baselineDone, levelsById }: { state: State<Gaps>; developing: Gaps["items"]; baselineDone: boolean; levelsById: Map<string, { level_number: number }[]> }) {
  return (
    <SectionCard id="priority-gaps-title" title="Priority gaps" action={developing.length ? <ViewAll to="/competencies/gaps">Gap analysis</ViewAll> : null}>
      {state.loading ? (
        <LoadingState label="Loading gaps" lines={4} />
      ) : state.error ? (
        <ErrorState error={state.error} onRetry={state.reload} />
      ) : !baselineDone ? (
        <EmptyState title="Start with a baseline assessment to see your gaps." icon={<ClipboardCheck className="size-5" />} />
      ) : developing.length === 0 ? (
        <EmptyState title="No confirmed gaps for your role." icon={<Target className="size-5" />}>
          <p>Competencies needing more evidence are listed in your profile.</p>
        </EmptyState>
      ) : (
        <ol className="space-y-3">
          {developing.slice(0, 3).map((item, index) => (
            <li key={item.competency.id} className="rounded-lg border border-border p-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="flex items-center gap-2 font-medium">
                  <span className="flex size-6 items-center justify-center rounded-full bg-warning-soft text-xs font-semibold text-warning" aria-hidden="true">{index + 1}</span>
                  {cleanName(item.competency.name)}
                </p>
                <Badge tone="warning">{item.gap} level{item.gap === 1 ? "" : "s"} to go</Badge>
              </div>
              <LevelScale className="mt-3" levels={levelsById.get(item.competency.id)?.length ?? item.max_level_span + 1} estimated={item.estimated_level} required={item.required_level} label={item.competency.name} />
            </li>
          ))}
        </ol>
      )}
    </SectionCard>
  );
}

function CompetencyOverview({ state, levelsById, baselineDone }: { state: State<Gaps>; levelsById: Map<string, { level_number: number }[]>; baselineDone: boolean }) {
  const items = state.data?.items ?? [];
  return (
    <SectionCard id="overview-title" title="Competencies for your role" action={items.length ? <ViewAll to="/competencies">My competencies</ViewAll> : null}>
      {state.loading ? (
        <LoadingState label="Loading competencies" lines={4} />
      ) : state.error ? (
        <ErrorState error={state.error} onRetry={state.reload} />
      ) : items.length === 0 ? (
        <EmptyState title="Your job role's requirements haven't been approved yet." />
      ) : (
        <ul className="divide-y divide-border">
          {items.map((item) => {
            const levels = levelsById.get(item.competency.id)?.length ?? item.max_level_span + 1;
            return (
              <li key={item.competency.id} className="flex flex-col gap-1.5 py-3 first:pt-0 last:pb-0">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-sm font-medium">{cleanName(item.competency.name)}</span>
                  <CompetencyStatusBadge status={item.status} />
                </div>
                <div className="flex items-center gap-3" aria-hidden="true">
                  <div className="flex flex-1 gap-0.5">
                    {Array.from({ length: levels }, (_, i) => (
                      <span key={i} className={cn("h-1.5 flex-1 rounded-sm", item.estimated_level !== null && i < item.estimated_level ? (item.status === "meets_requirement" ? "bg-success" : "bg-primary") : "bg-muted", i + 1 === item.required_level && "outline outline-1 outline-primary/50")} />
                    ))}
                  </div>
                  <span className="w-28 text-right text-xs tabular-nums text-muted-foreground">
                    {baselineDone && item.estimated_level !== null ? `level ${item.estimated_level} · needs ${item.required_level}` : `needs ${item.required_level}`}
                  </span>
                </div>
                <span className="sr-only">
                  {item.estimated_level !== null ? `Estimated level ${item.estimated_level}, ` : "Not assessed, "}required level {item.required_level}.
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </SectionCard>
  );
}

function RecommendedLearning({ state, baselineDone }: { state: State<Recommendations>; baselineDone: boolean }) {
  const items = state.data?.items.slice(0, 3) ?? [];
  return (
    <SectionCard id="recommended-title" title="Recommended learning" action={<ViewAll to="/courses">All courses</ViewAll>}>
      {state.loading ? (
        <LoadingState label="Loading recommendations" lines={4} />
      ) : state.error ? (
        <ErrorState error={state.error} onRetry={state.reload} />
      ) : items.length === 0 ? (
        <EmptyState title={baselineDone ? "No approved learning content matches your gaps yet." : "Recommendations appear after your baseline assessment."} icon={<BookOpen className="size-5" />} />
      ) : (
        <ul className="space-y-3">
          {items.map((rec) => (
            <RecommendationRow key={rec.course.id} rec={rec} />
          ))}
        </ul>
      )}
    </SectionCard>
  );
}

function RecommendationRow({ rec }: { rec: Recommendations["items"][number] }) {
  const reason = rec.reasons.find((r) => r.rule === "gap_match");
  const course = rec.course;
  return (
    <li className="relative flex flex-col gap-2 rounded-lg border border-border p-4 hover:border-primary/50">
      <div className="flex flex-wrap items-center gap-2">
        <DifficultyBadge difficulty={course.difficulty} />
        {durationLabel(course.duration_days) ? <Badge tone="neutral">{durationLabel(course.duration_days)}</Badge> : null}
      </div>
      <Link to={`/courses/${rec.course.id}`} className="font-medium text-foreground after:absolute after:inset-0 after:rounded-lg hover:text-primary focus-visible:outline-none after:focus-visible:ring-2 after:focus-visible:ring-ring">
        {cleanName(rec.course.title)}
      </Link>
      {reason?.competency_name ? (
        <p className="text-sm text-muted-foreground">
          Recommended because your level in <span className="font-medium text-foreground">{cleanName(reason.competency_name)}</span> is {reason.estimated}, and your role needs {reason.required}.
        </p>
      ) : null}
    </li>
  );
}

function ContinueLearning({ state }: { state: State<MyProgress> }) {
  if (state.loading || state.error || !state.data) return null; // the hero and path already cover the empty case
  const items = state.data.in_progress.slice(0, 2);
  if (items.length === 0) return null;
  return (
    <SectionCard id="continue-title" title="Continue learning" action={<ViewAll to="/learning-path">Learning path</ViewAll>}>
      <ul className="space-y-3">
        {items.map((item) => (
          <li key={item.course.id} className="relative flex flex-col gap-2 rounded-lg border border-border p-4 hover:border-primary/50">
            <Link
              to={item.progress.resume_lesson ? `/courses/${item.course.id}/lessons/${item.progress.resume_lesson.id}` : `/courses/${item.course.id}/learn`}
              className="font-medium text-foreground after:absolute after:inset-0 after:rounded-lg hover:text-primary focus-visible:outline-none after:focus-visible:ring-2 after:focus-visible:ring-ring"
            >
              {cleanName(item.course.title)}
            </Link>
            {item.progress.resume_lesson ? <p className="text-sm text-muted-foreground">Next: {item.progress.resume_lesson.title}</p> : null}
            <CourseProgressBar progress={item.progress} label={`Progress in ${cleanName(item.course.title)}`} />
          </li>
        ))}
      </ul>
    </SectionCard>
  );
}

function RecentActivity({ state }: { state: State<AttemptHistoryItem[]> }) {
  const items = state.data?.slice(0, 4) ?? [];
  return (
    <SectionCard id="activity-title" title="Recent assessment activity">
      {state.loading ? (
        <LoadingState label="Loading activity" lines={3} />
      ) : state.error ? (
        <ErrorState error={state.error} onRetry={state.reload} />
      ) : items.length === 0 ? (
        <EmptyState title="No assessment activity yet." icon={<CalendarClock className="size-5" />} />
      ) : (
        <ol className="space-y-3">
          {items.map((a) => (
            <li key={a.id} className="flex items-start gap-3">
              <span className={cn("mt-1.5 size-2.5 shrink-0 rounded-full", a.status === "scored" ? "bg-success" : "bg-primary")} aria-hidden="true" />
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium">{a.status === "scored" ? "Completed" : "Started"} {a.is_baseline ? "baseline assessment" : "assessment"}</p>
                <p className="truncate text-sm text-muted-foreground" title={a.assessment.title}>{cleanName(a.assessment.title)}</p>
                <p className="text-xs text-muted-foreground">
                  {shortDate(a.scored_at ?? a.started_at)}
                  {a.score_total !== null ? ` · score ${Math.round(Number(a.score_total) * 100)} / 100` : ""}
                </p>
              </div>
              {a.status === "scored" ? (
                <Link to={`/attempts/${a.id}/result`} className="shrink-0 rounded-md text-sm font-medium text-primary underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                  Result<span className="sr-only"> for {a.assessment.title}</span>
                </Link>
              ) : null}
            </li>
          ))}
        </ol>
      )}
    </SectionCard>
  );
}
