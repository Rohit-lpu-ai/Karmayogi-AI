import { ArrowLeft, ArrowRight, CheckCircle2, ListTree, Loader2, PartyPopper } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { CourseOutline, LessonDetail, LessonProgressResult } from "@/api/types";
import { useApi } from "@/api/useApi";
import { Breadcrumbs } from "@/components/layout/PageHeader";
import { cleanName } from "@/components/product/competency";
import { CourseProgressBar, LESSON_TYPE, LessonStatusIcon, minutesLabel } from "@/components/product/learning";
import { Markdown } from "@/components/product/Markdown";
import { ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogDescription, DialogTitle, DialogTrigger, SheetContent } from "@/components/ui/dialog";
import { toast } from "@/components/ui/toaster";
import { cn } from "@/lib/utils";

/**
 * Lesson player (/courses/:courseId/lessons/:lessonId): readable body, course contents beside it (a drawer on small
 * screens), "Mark as complete", and previous / next. Opening a lesson records it as started; completion is the
 * learner's own statement and never changes a competency estimate.
 */
export function LessonPage() {
  const { courseId, lessonId } = useParams();
  const lesson = useApi<LessonDetail>(lessonId ? `/api/v1/lessons/${lessonId}` : null);
  const outline = useApi<CourseOutline>(courseId ? `/api/v1/courses/${courseId}/outline` : null);
  const [status, setStatus] = useState<LessonDetail["status"] | null>(null);
  const [result, setResult] = useState<LessonProgressResult | null>(null);
  const [saving, setSaving] = useState(false);
  const [contentsOpen, setContentsOpen] = useState(false);
  const opened = useRef<string | null>(null);
  const reloadOutline = outline.reload;

  useEffect(() => {
    setStatus(null);
    setResult(null);
    setContentsOpen(false);
  }, [lessonId]);

  // Record that the lesson was opened (once per lesson view); completed lessons stay completed on the server.
  useEffect(() => {
    const data = lesson.data;
    if (!data || data.id !== lessonId || opened.current === data.id) return;
    opened.current = data.id;
    setStatus(data.status);
    if (data.status === "not_started") {
      api<LessonProgressResult>(`/api/v1/me/lessons/${data.id}/progress`, { method: "PUT", body: { status: "in_progress" } })
        .then((r) => {
          setStatus(r.lesson_status);
          reloadOutline();
        })
        .catch(() => undefined); // reading still works; the next action retries
    }
  }, [lesson.data, lessonId, reloadOutline]);

  if (lesson.loading && !lesson.data) return <Card className="p-6"><LoadingState label="Loading lesson" lines={8} /></Card>;
  if (lesson.error) {
    return (
      <div className="mx-auto max-w-2xl space-y-4">
        <ErrorState error={lesson.error} onRetry={lesson.error.status === 404 ? undefined : lesson.reload} />
        <Button variant="secondary" asChild>
          <Link to={courseId ? `/courses/${courseId}/learn` : "/courses"}><ArrowLeft aria-hidden="true" /> Back to course contents</Link>
        </Button>
      </div>
    );
  }
  if (!lesson.data) return null;
  const l = lesson.data;
  const current = status ?? l.status;
  const type = LESSON_TYPE[l.lesson_type];
  const courseTitle = cleanName(l.course.title);
  const courseDone = result?.course_progress.status === "completed";

  async function complete() {
    setSaving(true);
    try {
      const r = await api<LessonProgressResult>(`/api/v1/me/lessons/${l.id}/progress`, { method: "PUT", body: { status: "completed" } });
      setStatus(r.lesson_status);
      setResult(r);
      reloadOutline();
    } catch (err) {
      toast("Progress was not saved", { description: err instanceof ApiError ? err.detail : "Try again in a moment." });
    } finally {
      setSaving(false);
    }
  }

  const contents = outline.data ? <CourseContents outline={outline.data} courseId={l.course.id} currentId={l.id} onNavigate={() => setContentsOpen(false)} /> : null;

  return (
    <div className="grid items-start gap-6 lg:grid-cols-[18rem_minmax(0,1fr)] xl:grid-cols-[20rem_minmax(0,1fr)]">
      <aside aria-label="Course contents" className="hidden lg:sticky lg:top-24 lg:block">
        <Card className="max-h-[calc(100vh-8rem)] overflow-y-auto p-4">{contents ?? <LoadingState label="Loading contents" />}</Card>
      </aside>

      <article aria-labelledby="lesson-title" className="min-w-0">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <Breadcrumbs items={[{ label: "Courses", to: "/courses" }, { label: courseTitle, to: `/courses/${l.course.id}/learn` }, { label: `Lesson ${l.position}` }]} />
          <Dialog open={contentsOpen} onOpenChange={setContentsOpen}>
            <DialogTrigger asChild>
              <Button variant="secondary" size="sm" className="lg:hidden">
                <ListTree aria-hidden="true" />
                Course contents
              </Button>
            </DialogTrigger>
            <SheetContent aria-describedby="contents-description">
              <div className="flex flex-col gap-4 overflow-y-auto px-4 pb-5 pt-5">
                <DialogTitle className="pr-10 text-base">{courseTitle}</DialogTitle>
                <DialogDescription id="contents-description" className="sr-only">Lessons in this course</DialogDescription>
                {contents}
              </div>
            </SheetContent>
          </Dialog>
        </div>

        <header className="mt-4 space-y-2">
          <p className="text-sm font-medium text-primary">
            Lesson {l.position} of {l.lesson_count} · Module {l.module.position}: {l.module.title}
          </p>
          <h1 id="lesson-title" className="text-2xl font-semibold tracking-tight text-balance sm:text-3xl">{l.title}</h1>
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone="primary"><type.icon aria-hidden="true" />{type.label}</Badge>
            <Badge tone="neutral">{minutesLabel(l.estimated_minutes)}</Badge>
            {current === "completed" ? <Badge tone="success"><CheckCircle2 aria-hidden="true" />Completed</Badge> : null}
          </div>
        </header>

        {l.content_notice ? <p className="mt-4 text-sm text-muted-foreground">{l.content_notice}</p> : null}

        <Card className="mt-5 px-5 py-6 sm:px-8 sm:py-8">
          {l.body_markdown ? <Markdown source={l.body_markdown} headingOffset={1} /> : <p className="text-muted-foreground">This lesson has no text content.</p>}
        </Card>

        <div role="status" aria-live="polite" className="mt-5 empty:hidden">
          {result && !courseDone ? (
            <p className="flex items-center gap-2 text-sm font-medium text-success">
              <CheckCircle2 className="size-4" aria-hidden="true" />
              Lesson marked as complete. {result.course_progress.completed_lessons} of {result.course_progress.lesson_count} lessons done.
            </p>
          ) : null}
          {courseDone && result ? (
            <Alert tone="success" title="Course complete">
              You completed all {result.course_progress.lesson_count} lessons in {courseTitle}. Your competency estimates only change with new
              assessment evidence. <Link to="/learning-path">See your learning path</Link>
            </Alert>
          ) : null}
        </div>

        <nav aria-label="Lesson navigation" className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="order-2 sm:order-1">
            {l.previous ? (
              <Button variant="ghost" asChild>
                <Link to={`/courses/${l.course.id}/lessons/${l.previous.id}`}>
                  <ArrowLeft aria-hidden="true" />
                  <span className="truncate">Previous<span className="sr-only">: {l.previous.title}</span></span>
                </Link>
              </Button>
            ) : (
              <Button variant="ghost" asChild>
                <Link to={`/courses/${l.course.id}/learn`}><ArrowLeft aria-hidden="true" />Course contents</Link>
              </Button>
            )}
          </div>
          <div className="order-1 flex flex-col gap-2 sm:order-2 sm:flex-row">
            {current !== "completed" ? (
              <Button size="lg" onClick={() => void complete()} disabled={saving}>
                {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <CheckCircle2 aria-hidden="true" />}
                Mark as complete
              </Button>
            ) : null}
            {l.next ? (
              <Button size="lg" variant={current === "completed" ? "primary" : "secondary"} asChild>
                <Link to={`/courses/${l.course.id}/lessons/${l.next.id}`}>
                  Next: <span className="max-w-56 truncate">{l.next.title}</span>
                  <ArrowRight aria-hidden="true" />
                </Link>
              </Button>
            ) : current === "completed" ? (
              <Button size="lg" variant="primary" asChild>
                <Link to={`/courses/${l.course.id}/learn`}>
                  {courseDone ? <PartyPopper aria-hidden="true" /> : null}
                  Back to course contents
                </Link>
              </Button>
            ) : null}
          </div>
        </nav>
      </article>
    </div>
  );
}

function CourseContents({ outline, courseId, currentId, onNavigate }: { outline: CourseOutline; courseId: string; currentId: string; onNavigate: () => void }) {
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Link to={`/courses/${courseId}/learn`} onClick={onNavigate} className="text-sm font-semibold text-foreground underline-offset-4 hover:underline">
          {cleanName(outline.course.title)}
        </Link>
        <CourseProgressBar progress={outline.progress} label="Course progress" />
      </div>
      {outline.modules.map((module) => (
        <div key={module.id}>
          <p className="px-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">Module {module.position}: {module.title}</p>
          <ol className="mt-1 space-y-0.5">
            {module.lessons.map((lesson) => {
              const active = lesson.id === currentId;
              return (
                <li key={lesson.id}>
                  <Link
                    to={`/courses/${courseId}/lessons/${lesson.id}`}
                    onClick={onNavigate}
                    aria-current={active ? "page" : undefined}
                    data-focus-ring=""
                    className={cn(
                      "flex min-h-11 items-center gap-2.5 rounded-md px-2 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                      active ? "bg-primary-soft font-medium text-primary-soft-foreground" : "text-foreground hover:bg-muted",
                    )}
                  >
                    <LessonStatusIcon status={lesson.status} />
                    <span className="min-w-0 flex-1">{lesson.title}</span>
                  </Link>
                </li>
              );
            })}
          </ol>
        </div>
      ))}
    </div>
  );
}
