import { ArrowLeft, ArrowRight, BookOpenCheck, Building2, CheckCircle2, Clock, Layers, PlayCircle, RotateCcw, Sparkles, Target } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import type { CourseDetail, CourseOutline } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName, CompetencyStatusBadge, DifficultyBadge, durationLabel } from "@/components/product/competency";
import { CourseProgressBar, LESSON_TYPE, LessonStatusIcon, minutesLabel, ProgressBadge } from "@/components/product/learning";
import { ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

/** Course detail (API GET /courses/{id}, MVP-17): what it is, why it is recommended for this learner, and what it covers. */
export function CourseDetailPage() {
  const { courseId } = useParams();
  const course = useApi<CourseDetail>(courseId ? `/api/v1/courses/${courseId}` : null);
  const { user } = useAuth();
  const canLearn = Boolean(user?.can_take_assessments);
  const outline = useApi<CourseOutline>(courseId && canLearn && course.data?.learning_content.available ? `/api/v1/courses/${courseId}/outline` : null);

  if (course.loading) {
    return <Card className="p-6"><LoadingState label="Loading course" lines={6} /></Card>;
  }
  if (course.error) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <ErrorState error={course.error} onRetry={course.error.status === 404 ? undefined : course.reload} />
        <Button variant="secondary" asChild>
          <Link to="/courses"><ArrowLeft aria-hidden="true" /> Back to the catalogue</Link>
        </Button>
      </div>
    );
  }
  if (!course.data) return null;
  const c = course.data;
  const gapReasons = c.recommendation?.reasons.filter((r) => r.rule === "gap_match") ?? [];

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Courses", to: "/courses" }, { label: cleanName(c.title) }]}
        title={cleanName(c.title)}
        description={c.description ?? undefined}
        meta={
          <>
            {c.recommendation ? <Badge tone="primary"><Sparkles aria-hidden="true" />{c.recommendation.rank <= 3 ? "Top pick for you" : "Matches your gaps"}</Badge> : null}
            <DifficultyBadge difficulty={c.difficulty} />
            {durationLabel(c.duration_days) ? <Badge tone="neutral"><Clock aria-hidden="true" />{durationLabel(c.duration_days)}</Badge> : null}
            <Badge tone="neutral"><Building2 aria-hidden="true" />{cleanName(c.provider_organisation)}</Badge>
            {c.lessons?.lesson_count ? <Badge tone="neutral"><BookOpenCheck aria-hidden="true" />{c.lessons.lesson_count} lessons · {minutesLabel(c.lessons.total_minutes)}</Badge> : null}
            {c.your_progress && c.your_progress.status !== "not_started" ? <ProgressBadge status={c.your_progress.status} /> : null}
          </>
        }
        className="pb-0"
      />

      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <div className="flex flex-col gap-6">
          {c.addresses_your_gaps.length > 0 || gapReasons.length > 0 ? (
            <Card as="section" aria-labelledby="why-title" className="border-primary/35 bg-primary-soft/40 p-6">
              <h2 id="why-title" className="flex items-center gap-2 text-lg font-semibold">
                <Target className="size-5 text-primary" aria-hidden="true" />
                Why this course is recommended for you
              </h2>
              <ul className="mt-4 space-y-3">
                {c.addresses_your_gaps.map((gap) => (
                  <li key={gap.competency_id} className="rounded-lg border border-border bg-card p-4">
                    <p className="font-medium">{cleanName(gap.competency_name)}</p>
                    <p className="mt-1 text-sm text-muted-foreground">
                      Your estimated level is {gap.estimated_level ?? "not available"}; your role requires level {gap.required_level}
                      {gap.gap ? ` (${gap.gap} level${gap.gap === 1 ? "" : "s"} to go)` : ""}. This course is linked to that competency.
                    </p>
                  </li>
                ))}
              </ul>
              <p className="mt-3 text-xs text-muted-foreground">Recommendations follow fixed rules from your assessment gaps and approved course links. No AI is used.</p>
            </Card>
          ) : null}

          <Card as="section" aria-labelledby="objectives-title" className="p-6">
            <h2 id="objectives-title" className="text-lg font-semibold">What you will learn</h2>
            {c.learning_objectives.length ? (
              <ul className="mt-4 grid gap-3 sm:grid-cols-2">
                {c.learning_objectives.map((objective) => (
                  <li key={objective} className="flex gap-2.5">
                    <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-success" aria-hidden="true" />
                    <span>{objective}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-muted-foreground">Learning objectives have not been published for this course.</p>
            )}
          </Card>

          <Card as="section" aria-labelledby="structure-title" className="p-6">
            <h2 id="structure-title" className="flex items-center gap-2 text-lg font-semibold">
              <Layers className="size-5 text-primary" aria-hidden="true" />
              Course structure
            </h2>
            {!c.learning_content.available ? (
              <Alert tone="neutral" className="mt-4" title="No lessons yet">
                {c.learning_content.reason}
              </Alert>
            ) : outline.data ? (
              <ol className="mt-4 space-y-4">
                {outline.data.modules.map((module) => (
                  <li key={module.id}>
                    <p className="text-sm font-semibold">Module {module.position}: {module.title}</p>
                    {module.summary ? <p className="text-sm text-muted-foreground">{module.summary}</p> : null}
                    <ul className="mt-2 divide-y divide-border rounded-lg border border-border">
                      {module.lessons.map((lesson) => {
                        const type = LESSON_TYPE[lesson.lesson_type];
                        return (
                          <li key={lesson.id} className="flex items-center gap-3 px-3 py-2.5 text-sm">
                            <LessonStatusIcon status={lesson.status} />
                            <span className="min-w-0 flex-1">{lesson.title}</span>
                            <span className="hidden text-muted-foreground sm:inline">{type.label}</span>
                            <span className="tabular-nums text-muted-foreground">{minutesLabel(lesson.estimated_minutes)}</span>
                          </li>
                        );
                      })}
                    </ul>
                  </li>
                ))}
              </ol>
            ) : canLearn ? (
              <LoadingState label="Loading course structure" className="mt-4" />
            ) : (
              <p className="mt-2 text-muted-foreground">
                {c.lessons?.module_count} modules and {c.lessons?.lesson_count} lessons. Learning and progress tracking are available to learners.
              </p>
            )}
            {c.completion_criteria ? <p className="mt-4 text-sm text-muted-foreground"><span className="font-medium text-foreground">To complete: </span>{c.completion_criteria}</p> : null}
          </Card>
        </div>

        <aside className="flex flex-col gap-4" aria-label="Course facts">
          <Card className="p-5">
            <h2 className="text-base font-semibold">Competencies addressed</h2>
            <ul className="mt-3 space-y-3">
              {c.competencies.map((m) => (
                <li key={m.competency.id} className="rounded-lg border border-border p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="font-medium">{cleanName(m.competency.name)}</span>
                    <Badge tone={m.relevance === "primary" ? "primary" : "neutral"}>{m.relevance === "primary" ? "Main focus" : "Also covers"}</Badge>
                  </div>
                  {m.your_status ? (
                    <div className="mt-2 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
                      <CompetencyStatusBadge status={m.your_status.status} />
                      {m.your_status.estimated_level !== null ? <span>You: level {m.your_status.estimated_level} · role needs {m.your_status.required_level}</span> : <span>Role needs level {m.your_status.required_level}</span>}
                    </div>
                  ) : (
                    <p className="mt-1 text-sm text-muted-foreground">Not required for your current role.</p>
                  )}
                </li>
              ))}
            </ul>
          </Card>

          {canLearn && c.learning_content.available ? (
            <Card className="p-5">
              <h2 className="text-base font-semibold">{c.your_progress?.status === "completed" ? "Course completed" : c.your_progress?.status === "in_progress" ? "Continue learning" : "Start learning"}</h2>
              {outline.data ? <CourseProgressBar progress={outline.data.progress} label={`Progress in ${cleanName(c.title)}`} className="mt-3" /> : null}
              <Button className="mt-4 w-full" variant={c.your_progress?.status === "completed" ? "secondary" : "primary"} asChild>
                <Link to={c.your_progress?.status === "in_progress" && c.your_progress.resume_lesson ? `/courses/${c.id}/lessons/${c.your_progress.resume_lesson.id}` : `/courses/${c.id}/learn`}>
                  {c.your_progress?.status === "completed" ? <RotateCcw aria-hidden="true" /> : c.your_progress?.status === "in_progress" ? <ArrowRight aria-hidden="true" /> : <PlayCircle aria-hidden="true" />}
                  {c.your_progress?.status === "completed" ? "Review course" : c.your_progress?.status === "in_progress" ? "Continue" : "Start course"}
                </Link>
              </Button>
              {c.prerequisites?.length ? (
                <div className="mt-4 border-t border-border pt-3">
                  <p className="text-sm font-medium">Recommended first</p>
                  <ul className="mt-1 space-y-1">
                    {c.prerequisites.map((p) => (
                      <li key={p.id}><Link to={`/courses/${p.id}`} className="text-sm text-primary underline underline-offset-4">{cleanName(p.title)}</Link></li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </Card>
          ) : null}

          {c.related_courses.length ? (
            <Card className="p-5">
              <h2 className="text-base font-semibold">Related courses</h2>
              <ul className="mt-3 space-y-2">
                {c.related_courses.map((r) => (
                  <li key={r.id}>
                    <Link to={`/courses/${r.id}`} className="block rounded-md px-2 py-2 hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                      <span className="block text-sm font-medium text-primary">{cleanName(r.title)}</span>
                      <span className="mt-0.5 flex flex-wrap gap-2 text-xs text-muted-foreground">
                        {r.difficulty ? <span className="capitalize">{r.difficulty}</span> : null}
                        {durationLabel(r.duration_days) ? <span>{durationLabel(r.duration_days)}</span> : null}
                        {r.is_recommended ? <span className="font-medium text-primary">Recommended</span> : null}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </Card>
          ) : null}
        </aside>
      </div>
    </div>
  );
}
