import { ArrowLeft, ArrowRight, Info, Loader2, PlayCircle, RotateCcw } from "lucide-react";
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { CourseOutline } from "@/api/types";
import { useApi } from "@/api/useApi";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName, DifficultyBadge } from "@/components/product/competency";
import { CourseProgressBar, LESSON_TYPE, LessonStatusIcon, MinutesBadge, minutesLabel, ProgressBadge } from "@/components/product/learning";
import { ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { toast } from "@/components/ui/toaster";

/** Course learning hub (/courses/:courseId/learn): modules, lessons with status, progress and the one next action. */
export function CourseLearnPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const outline = useApi<CourseOutline>(courseId ? `/api/v1/courses/${courseId}/outline` : null);
  const [starting, setStarting] = useState(false);

  if (outline.loading) return <Card className="p-6"><LoadingState label="Loading course contents" lines={6} /></Card>;
  if (outline.error) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <ErrorState error={outline.error} onRetry={outline.error.status === 404 ? undefined : outline.reload} />
        <Button variant="secondary" asChild>
          <Link to="/courses"><ArrowLeft aria-hidden="true" /> Back to courses</Link>
        </Button>
      </div>
    );
  }
  if (!outline.data) return null;
  const { course, modules, progress, prerequisites } = outline.data;
  const lessons = modules.flatMap((m) => m.lessons);
  const title = cleanName(course.title);

  async function start() {
    setStarting(true);
    try {
      const started = await api<CourseOutline>(`/api/v1/courses/${course.id}/start`, { method: "POST" });
      const target = started.progress.resume_lesson ?? lessons[0];
      if (target) navigate(`/courses/${course.id}/lessons/${target.id}`);
    } catch (err) {
      toast("The course could not be started", { description: err instanceof ApiError ? err.detail : undefined });
      setStarting(false);
    }
  }

  const resume = progress.resume_lesson ?? lessons[0];
  const action =
    lessons.length === 0 ? null : progress.status === "not_started" ? (
      <Button size="lg" onClick={() => void start()} disabled={starting}>
        {starting ? <Loader2 className="animate-spin" aria-hidden="true" /> : <PlayCircle aria-hidden="true" />}
        Start course
      </Button>
    ) : progress.status === "in_progress" && resume ? (
      <Button size="lg" asChild>
        <Link to={`/courses/${course.id}/lessons/${resume.id}`}>
          Continue: {resume.title}
          <ArrowRight aria-hidden="true" />
        </Link>
      </Button>
    ) : (
      <Button size="lg" variant="secondary" asChild>
        <Link to={`/courses/${course.id}/lessons/${lessons[0].id}`}>
          <RotateCcw aria-hidden="true" />
          Review from the start
        </Link>
      </Button>
    );

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        breadcrumbs={[{ label: "Courses", to: "/courses" }, { label: title, to: `/courses/${course.id}` }, { label: "Learn" }]}
        eyebrow="Course contents"
        title={title}
        meta={
          <>
            <ProgressBadge status={progress.status} />
            <DifficultyBadge difficulty={course.difficulty} />
            <MinutesBadge minutes={progress.total_minutes} />
          </>
        }
        actions={action}
        className="pb-0"
      />

      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <section aria-labelledby="modules-title" className="flex flex-col gap-4">
          <h2 id="modules-title" className="sr-only">Modules and lessons</h2>
          {modules.length === 0 ? (
            <Alert tone="neutral" title="No lessons yet">This course has no lessons in the platform yet.</Alert>
          ) : (
            modules.map((module) => {
              const done = module.lessons.filter((l) => l.status === "completed").length;
              return (
                <Card as="section" key={module.id} aria-labelledby={`module-${module.id}`} className="overflow-hidden">
                  <div className="flex flex-wrap items-start justify-between gap-2 border-b border-border bg-muted/40 px-5 py-4">
                    <div className="min-w-0">
                      <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Module {module.position}</p>
                      <h3 id={`module-${module.id}`} className="text-base font-semibold">{module.title}</h3>
                      {module.summary ? <p className="text-sm text-muted-foreground">{module.summary}</p> : null}
                    </div>
                    <p className="text-sm tabular-nums text-muted-foreground">{done} of {module.lessons.length} done</p>
                  </div>
                  <ol className="divide-y divide-border">
                    {module.lessons.map((lesson) => {
                      const type = LESSON_TYPE[lesson.lesson_type];
                      return (
                        <li key={lesson.id}>
                          <Link
                            to={`/courses/${course.id}/lessons/${lesson.id}`}
                            data-focus-ring=""
                            className="flex items-center gap-3 px-5 py-3.5 hover:bg-muted/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring"
                          >
                            <LessonStatusIcon status={lesson.status} />
                            <span className="min-w-0 flex-1">
                              <span className="block font-medium text-foreground">{lesson.title}</span>
                              <span className="mt-0.5 flex flex-wrap items-center gap-x-3 text-sm text-muted-foreground">
                                <span className="inline-flex items-center gap-1"><type.icon className="size-3.5" aria-hidden="true" />{type.label}</span>
                                <span>{minutesLabel(lesson.estimated_minutes)}</span>
                              </span>
                            </span>
                            <ArrowRight className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
                          </Link>
                        </li>
                      );
                    })}
                  </ol>
                </Card>
              );
            })
          )}
        </section>

        <aside className="flex flex-col gap-4" aria-label="Your progress">
          <Card className="p-5">
            <h2 className="text-base font-semibold">Your progress</h2>
            <CourseProgressBar progress={progress} label={`Progress in ${title}`} className="mt-3" />
            {course.completion_criteria ? <p className="mt-3 text-sm text-muted-foreground">{course.completion_criteria}</p> : null}
          </Card>
          {prerequisites.length ? (
            <Card className="p-5">
              <h2 className="text-base font-semibold">Recommended first</h2>
              <p className="mt-1 text-sm text-muted-foreground">These courses prepare you for this one. You can still start now.</p>
              <ul className="mt-3 space-y-2">
                {prerequisites.map((p) => (
                  <li key={p.id} className="flex flex-wrap items-center justify-between gap-2">
                    <Link to={`/courses/${p.id}`} className="text-sm font-medium text-primary underline underline-offset-4">{cleanName(p.title)}</Link>
                    <ProgressBadge status={p.status} />
                  </li>
                ))}
              </ul>
            </Card>
          ) : null}
          {course.content_origin === "synthetic" ? (
            <p className="flex gap-2 text-sm text-muted-foreground">
              <Info className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
              Lessons in this course are synthetic examples written for product evaluation.
            </p>
          ) : null}
        </aside>
      </div>
    </div>
  );
}
