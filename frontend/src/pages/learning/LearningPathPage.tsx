import { ArrowRight, ClipboardCheck, Info, Loader2, Map as MapIcon, RefreshCw, Target } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { LearningPath, PathItem } from "@/api/types";
import { useApi } from "@/api/useApi";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName, DifficultyBadge } from "@/components/product/competency";
import { CourseProgressBar, minutesLabel, ProgressBadge } from "@/components/product/learning";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { toast } from "@/components/ui/toaster";

/** Personal learning path (path-v1): courses grouped by assessed gap, in the order the rule gives, with progress. */
export function LearningPathPage() {
  const path = useApi<LearningPath>("/api/v1/me/learning-path");
  const [refreshing, setRefreshing] = useState(false);
  const [fresh, setFresh] = useState<LearningPath | null>(null);
  const data = fresh ?? path.data;

  async function regenerate() {
    setRefreshing(true);
    try {
      setFresh(await api<LearningPath>("/api/v1/me/learning-path/regenerate", { method: "POST" }));
      toast("Learning path refreshed", { description: "Completed courses were kept." });
    } catch (err) {
      toast("The path was not refreshed", { description: err instanceof ApiError ? err.detail : undefined });
    } finally {
      setRefreshing(false);
    }
  }

  const header = (
    <PageHeader
      breadcrumbs={[{ label: "Home", to: "/" }, { label: "Learning path" }]}
      title="Your learning path"
      description="Courses for the gaps your baseline assessment found, in a suggested order. You can take them in any order."
      actions={
        data?.state === "ready" ? (
          <Button variant="secondary" onClick={() => void regenerate()} disabled={refreshing}>
            {refreshing ? <Loader2 className="animate-spin" aria-hidden="true" /> : <RefreshCw aria-hidden="true" />}
            Refresh path
          </Button>
        ) : null
      }
    />
  );

  if (path.loading && !data) return <>{header}<Card className="p-6"><LoadingState label="Building your learning path" lines={6} /></Card></>;
  if (path.error) {
    if (path.error.code === "JOB_ROLE_REQUIRED") {
      return (
        <>
          {header}
          <EmptyState title="Choose your job role first" action={<Button asChild><Link to="/get-started">Choose job role</Link></Button>}>
            Your path is built from the requirements of your job role and your assessment results.
          </EmptyState>
        </>
      );
    }
    return <>{header}<ErrorState error={path.error} onRetry={path.reload} /></>;
  }
  if (!data) return null;

  if (data.state === "assessment_needed") {
    return (
      <>
        {header}
        <EmptyState
          icon={<ClipboardCheck className="size-5" />}
          title="Take your baseline assessment to build your path"
          action={<Button asChild><Link to="/assessment">Go to the baseline assessment</Link></Button>}
        >
          The path lists courses only for gaps confirmed by assessment evidence, so it stays empty until then.
        </EmptyState>
      </>
    );
  }
  if (data.state === "no_gaps") {
    return (
      <>
        {header}
        <EmptyState icon={<Target className="size-5" />} title="No confirmed gaps for your role" action={<Button variant="secondary" asChild><Link to="/courses">Browse all courses</Link></Button>}>
          Your baseline shows you at or above the required level for every assessed competency. You can still explore the catalogue.
        </EmptyState>
        {data.completed_earlier.length ? <CompletedEarlier items={data.completed_earlier} /> : null}
      </>
    );
  }

  const next = data.groups.flatMap((g) => g.items).find((i) => i.course && i.status !== "completed");
  const totalCourses = data.summary.courses;

  return (
    <div className="flex flex-col gap-6">
      {header}

      <section aria-label="Path summary" className="grid gap-4 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)]">
        <Card className="flex flex-col gap-3 border-primary/35 bg-primary-soft/40 p-5">
          <p className="text-sm font-semibold uppercase tracking-wide text-primary">Up next</p>
          {next?.course ? (
            <>
              <h2 className="text-lg font-semibold">{cleanName(next.course.title)}</h2>
              <p className="text-sm text-muted-foreground">{reasonText(next)}</p>
              <div>
                <Button asChild>
                  <Link to={nextHref(next)}>
                    {next.status === "in_progress" && next.progress?.resume_lesson ? "Continue learning" : "Open course"}
                    <ArrowRight aria-hidden="true" />
                  </Link>
                </Button>
              </div>
            </>
          ) : (
            <p>You have completed every course on your path. Your competency estimates change only with new assessment evidence.</p>
          )}
        </Card>
        <Card className="grid grid-cols-3 gap-3 p-5 text-center">
          <Stat label="Courses" value={String(totalCourses)} />
          <Stat label="Completed" value={`${data.summary.completed}`} />
          <Stat label="Est. time" value={minutesLabel(data.summary.total_minutes)} />
        </Card>
      </section>

      <ol className="flex flex-col gap-5" aria-label="Path by competency gap">
        {data.groups.map((group, index) => (
          <li key={group.competency.id}>
            <Card as="section" aria-labelledby={`gap-${group.competency.id}`} className="overflow-hidden">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border bg-muted/40 px-5 py-3.5">
                <h2 id={`gap-${group.competency.id}`} className="text-base font-semibold">
                  <span className="text-muted-foreground">{index + 1}. </span>
                  {group.competency.name ? cleanName(group.competency.name) : "Competency"}
                </h2>
                {group.gap !== null ? (
                  <p className="text-sm text-muted-foreground">
                    Level {group.estimated_level} now · level {group.required_level} needed ({group.gap} to go)
                  </p>
                ) : null}
              </div>
              <ol className="divide-y divide-border">
                {group.items.map((item) => <PathRow key={item.id} item={item} />)}
              </ol>
            </Card>
          </li>
        ))}
      </ol>

      {data.completed_earlier.length ? <CompletedEarlier items={data.completed_earlier} /> : null}

      <Collapsible>
        <CollapsibleTrigger asChild>
          <Button variant="link" className="self-start"><Info aria-hidden="true" />How this path is ordered</Button>
        </CollapsibleTrigger>
        <CollapsibleContent>
          <Alert tone="neutral" className="mt-2">
            <p>{data.rule}</p>
            <p className="mt-2">{data.note} Rule {data.rule_version}, generated {new Date(data.generated_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}. No AI is used.</p>
          </Alert>
        </CollapsibleContent>
      </Collapsible>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col justify-center">
      <span className="text-xl font-semibold tabular-nums">{value}</span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </div>
  );
}

function nextHref(item: PathItem): string {
  if (!item.course) return "/courses";
  const resume = item.progress?.resume_lesson;
  return item.status === "in_progress" && resume ? `/courses/${item.course.id}/lessons/${resume.id}` : `/courses/${item.course.id}/learn`;
}

function reasonText(item: PathItem): string {
  const first = item.reasons[0] as { rule?: string; for_course_title?: string; competency_name?: string } | undefined;
  if (first?.rule === "prerequisite") return `Recommended before ${cleanName(first.for_course_title ?? "a later course")}.`;
  if (first?.rule === "gap_match") return `Linked to your gap in ${cleanName(String(first.competency_name ?? "this competency"))}.`;
  if (first?.rule === "completed_earlier") return "Completed on an earlier version of your path.";
  return "";
}

function PathRow({ item }: { item: PathItem }) {
  if (item.item_type === "no_content_placeholder" || !item.course) {
    return (
      <li className="flex items-start gap-3 px-5 py-4 text-sm text-muted-foreground">
        <MapIcon className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
        No approved course covers this gap yet. Your gap analysis still shows where to focus.
      </li>
    );
  }
  const course = item.course;
  return (
    <li className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center">
      <div className="min-w-0 flex-1 space-y-1.5">
        <div className="flex flex-wrap items-center gap-2">
          <ProgressBadge status={item.status} />
          <DifficultyBadge difficulty={course.difficulty} />
          {item.progress ? <span className="text-sm text-muted-foreground">{item.progress.lesson_count} lessons · {minutesLabel(item.progress.total_minutes)}</span> : null}
        </div>
        <h3 className="font-semibold leading-snug">
          <Link to={`/courses/${course.id}`} className="underline-offset-4 hover:underline">{cleanName(course.title)}</Link>
        </h3>
        <p className="text-sm text-muted-foreground">{reasonText(item)}</p>
        {item.progress && item.status !== "not_started" ? <CourseProgressBar progress={item.progress} label={`Progress in ${cleanName(course.title)}`} className="max-w-sm" /> : null}
      </div>
      <Button variant={item.status === "completed" ? "ghost" : "secondary"} className="self-start sm:self-center" asChild>
        <Link to={nextHref(item)} aria-label={`${item.status === "in_progress" ? "Continue" : item.status === "completed" ? "Review" : "Start"} ${cleanName(course.title)}`}>
          {item.status === "in_progress" ? "Continue" : item.status === "completed" ? "Review" : "Start"}
          <ArrowRight aria-hidden="true" />
        </Link>
      </Button>
    </li>
  );
}

function CompletedEarlier({ items }: { items: PathItem[] }) {
  return (
    <Card as="section" aria-labelledby="earlier-title" className="p-5">
      <h2 id="earlier-title" className="text-base font-semibold">Completed earlier</h2>
      <ul className="mt-2 divide-y divide-border">
        {items.filter((i) => i.course).map((item) => (
          <li key={item.id} className="flex flex-wrap items-center justify-between gap-2 py-2.5">
            <Link to={`/courses/${item.course!.id}`} className="font-medium underline-offset-4 hover:underline">{cleanName(item.course!.title)}</Link>
            <ProgressBadge status={item.status} />
          </li>
        ))}
      </ul>
    </Card>
  );
}
