import { ArrowRight, BookPlus, Eye, EyeOff, Loader2, Pencil, Plus, Rocket, Save, Search, Send, Trash2, Undo2 } from "lucide-react";
import { useMemo, useState, type FormEvent } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { AdminCourseDetail, AdminCourseList, AdminLesson, CompetencyOption, CourseState } from "@/api/adminTypes";
import { useApi } from "@/api/useApi";
import { can, useAuth } from "@/auth/AuthContext";
import { COURSE_STATE, CourseStateBadge, formatDateTime, GuardChecklist, OriginBadge, ReviewHistory } from "@/components/admin/common";
import { PageHeader } from "@/components/layout/PageHeader";
import { ConfirmationDialog } from "@/components/product/ConfirmationDialog";
import { cleanName } from "@/components/product/competency";
import { LESSON_TYPE, minutesLabel } from "@/components/product/learning";
import { Markdown } from "@/components/product/Markdown";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Field, Input, Textarea } from "@/components/ui/form";
import { Select } from "@/components/ui/select";
import { toast } from "@/components/ui/toaster";
import { FilterChip } from "./QuestionPages";

const STATES: CourseState[] = ["draft", "in_review", "approved", "published"];

/** /admin/courses */
export function AdminCoursesPage() {
  const [params, setParams] = useSearchParams();
  const state = params.get("state") ?? "";
  const origin = params.get("origin") ?? "";
  const q = params.get("q") ?? "";
  const [search, setSearch] = useState(q);
  const query = useMemo(() => {
    const p = new URLSearchParams();
    if (state) p.set("state", state);
    if (origin) p.set("origin", origin);
    if (q) p.set("q", q);
    return p.toString();
  }, [state, origin, q]);
  const list = useApi<AdminCourseList>(`/api/v1/admin/courses${query ? `?${query}` : ""}`);
  const set = (key: string, value: string) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    setParams(next, { replace: true });
  };

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Courses"
        description="Prepare courses, send them for review, and publish approved courses to the learner catalogue."
        actions={<Button asChild><Link to="/admin/courses/new"><BookPlus aria-hidden="true" />New course</Link></Button>} className="pb-0" />
      <div role="group" aria-label="Filter by state" className="flex flex-wrap gap-2">
        <FilterChip active={!state} onClick={() => set("state", "")}>All</FilterChip>
        {STATES.map((s) => (
          <FilterChip key={s} active={state === s} onClick={() => set("state", s)}>
            {COURSE_STATE[s].label} <span className="tabular-nums text-muted-foreground">{list.data?.state_counts[s] ?? 0}</span>
          </FilterChip>
        ))}
      </div>
      <Card className="p-4">
        <form role="search" className="grid gap-3 sm:grid-cols-[minmax(0,1fr)_16rem]" onSubmit={(e) => { e.preventDefault(); set("q", search.trim()); }}>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="course-search" className="text-sm font-medium">Search</label>
            <div className="flex gap-2">
              <Input id="course-search" type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Title or provider" />
              <Button type="submit" variant="secondary" size="icon" aria-label="Search courses"><Search aria-hidden="true" /></Button>
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="course-origin" className="text-sm font-medium">Content origin</label>
            <Select id="course-origin" value={origin} onChange={(e) => set("origin", e.target.value)}>
              <option value="">Any origin</option>
              <option value="synthetic">Synthetic example</option>
              <option value="provider">Provider content</option>
              <option value="official_source">Official source, awaiting review</option>
            </Select>
          </div>
        </form>
      </Card>
      {list.loading && !list.data ? <LoadingState label="Loading courses" lines={6} /> : null}
      {list.error ? <ErrorState error={list.error} onRetry={list.reload} /> : null}
      {list.data && list.data.items.length === 0 ? <EmptyState title="No courses match">Change the filters or create a course.</EmptyState> : null}
      {list.data && list.data.items.length > 0 ? (
        <ul className="grid gap-2" aria-label={`${list.data.total} courses`}>
          {list.data.items.map((c) => (
            <Card as="li" key={c.id} className="relative flex flex-col gap-2 p-4 hover:border-primary/40 sm:flex-row sm:items-center">
              <div className="min-w-0 flex-1 space-y-1.5">
                <div className="flex flex-wrap items-center gap-2"><CourseStateBadge state={c.state} /><OriginBadge origin={c.content_origin} /></div>
                <Link to={`/admin/courses/${c.id}`} className="font-medium after:absolute after:inset-0 after:rounded-xl hover:text-primary focus-visible:outline-none after:focus-visible:ring-2 after:focus-visible:ring-ring">
                  {cleanName(c.title)}
                </Link>
                <p className="text-sm text-muted-foreground">{cleanName(c.provider_organisation)} · {c.lesson_count} lessons{c.published_at ? ` · published ${formatDateTime(c.published_at)}` : ""}</p>
              </div>
              <ArrowRight className="hidden size-4 text-muted-foreground sm:block" aria-hidden="true" />
            </Card>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

interface CourseForm {
  title: string;
  description: string;
  provider_organisation: string;
  duration_days: string;
  difficulty: string;
  learning_objectives: string;
  completion_criteria: string;
  content_origin: "synthetic" | "provider";
}

function toForm(c?: AdminCourseDetail): CourseForm {
  return {
    title: c?.title ?? "", description: c?.description ?? "", provider_organisation: c?.provider_organisation ?? "",
    duration_days: c?.duration_days ? String(c.duration_days) : "", difficulty: c?.difficulty ?? "",
    learning_objectives: (c?.learning_objectives ?? []).join("\n"), completion_criteria: c?.completion_criteria ?? "",
    content_origin: c?.content_origin === "provider" ? "provider" : "synthetic",
  };
}

function formBody(f: CourseForm) {
  return {
    title: f.title.trim(), description: f.description.trim() || null, provider_organisation: f.provider_organisation.trim(),
    duration_days: f.duration_days ? Number(f.duration_days) : null, difficulty: f.difficulty || null,
    learning_objectives: f.learning_objectives.split("\n").map((o) => o.trim()).filter(Boolean),
    completion_criteria: f.completion_criteria.trim() || null, content_origin: f.content_origin,
  };
}

function CourseDetailsForm({ value, onChange, disabled }: { value: CourseForm; onChange: (f: CourseForm) => void; disabled?: boolean }) {
  const set = (key: keyof CourseForm) => (e: { target: { value: string } }) => onChange({ ...value, [key]: e.target.value });
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="md:col-span-2"><Field id="course-title" label="Title"><Input id="course-title" value={value.title} onChange={set("title")} disabled={disabled} required /></Field></div>
      <div className="md:col-span-2"><Field id="course-description" label="Description"><Textarea id="course-description" rows={3} value={value.description} onChange={set("description")} disabled={disabled} /></Field></div>
      <Field id="course-provider" label="Provider"><Input id="course-provider" value={value.provider_organisation} onChange={set("provider_organisation")} disabled={disabled} /></Field>
      <Field id="course-origin-field" label="Content origin" hint="Official-source courses come only from reviewed imports.">
        <Select id="course-origin-field" value={value.content_origin} onChange={set("content_origin")} disabled={disabled} aria-describedby="course-origin-field-hint">
          <option value="synthetic">Synthetic example</option>
          <option value="provider">Provider content</option>
        </Select>
      </Field>
      <Field id="course-difficulty" label="Difficulty">
        <Select id="course-difficulty" value={value.difficulty} onChange={set("difficulty")} disabled={disabled}>
          <option value="">Not set</option><option value="foundational">Foundational</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option>
        </Select>
      </Field>
      <Field id="course-days" label="Duration in days (optional)"><Input id="course-days" type="number" min={1} max={365} value={value.duration_days} onChange={set("duration_days")} disabled={disabled} /></Field>
      <div className="md:col-span-2"><Field id="course-objectives" label="Learning objectives" hint="One per line."><Textarea id="course-objectives" rows={4} value={value.learning_objectives} onChange={set("learning_objectives")} disabled={disabled} aria-describedby="course-objectives-hint" /></Field></div>
      <div className="md:col-span-2"><Field id="course-completion" label="Completion criteria (optional)"><Input id="course-completion" value={value.completion_criteria} onChange={set("completion_criteria")} disabled={disabled} /></Field></div>
    </div>
  );
}

/** /admin/courses/new */
export function AdminCourseNewPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<CourseForm>(toForm());
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (form.title.trim().length < 3 || form.provider_organisation.trim().length < 2) {
      setError("Give a title (3+ characters) and a provider.");
      return;
    }
    setSaving(true);
    try {
      const created = await api<AdminCourseDetail>("/api/v1/admin/courses", { method: "POST", body: formBody(form) });
      toast("Course created as a draft");
      navigate(`/admin/courses/${created.id}`, { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.detail ?? err.message : "The course was not created.");
      setSaving(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader breadcrumbs={[{ label: "Courses", to: "/admin/courses" }, { label: "New course" }]} title="New course"
        description="Starts as a draft that learners cannot see. Add modules, lessons and competency links next." className="pb-0" />
      <form onSubmit={submit} noValidate className="flex flex-col gap-4">
        {error ? <Alert tone="danger" role="alert">{error}</Alert> : null}
        <Card className="p-6"><CourseDetailsForm value={form} onChange={setForm} /></Card>
        <div className="flex justify-end gap-2">
          <Button type="button" variant="ghost" onClick={() => navigate("/admin/courses")}>Cancel</Button>
          <Button type="submit" disabled={saving}>{saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Save aria-hidden="true" />}Create draft</Button>
        </div>
      </form>
    </div>
  );
}

/** /admin/courses/:courseId */
export function AdminCourseDetailPage() {
  const { courseId } = useParams();
  const { user } = useAuth();
  const loaded = useApi<AdminCourseDetail>(courseId ? `/api/v1/admin/courses/${courseId}` : null);
  const options = useApi<{ competencies: CompetencyOption[] }>(user && can(user, "courses.manage") ? "/api/v1/admin/courses/options" : null);
  const [fresh, setFresh] = useState<AdminCourseDetail | null>(null);
  const [editingDetails, setEditingDetails] = useState(false);
  const [form, setForm] = useState<CourseForm>(toForm());
  const [busy, setBusy] = useState<string | null>(null);
  const [moduleTitle, setModuleTitle] = useState("");
  const [lessonDialog, setLessonDialog] = useState<{ moduleId: string; lesson?: AdminLesson } | null>(null);
  const [linkCompetency, setLinkCompetency] = useState("");
  const [linkRelevance, setLinkRelevance] = useState<"primary" | "secondary">("primary");
  const [note, setNote] = useState("");
  const [confirmPublish, setConfirmPublish] = useState(false);
  const [unpublishReason, setUnpublishReason] = useState("");
  const [confirmUnpublish, setConfirmUnpublish] = useState(false);
  const course = fresh && fresh.id === courseId ? fresh : loaded.data;

  if (loaded.loading && !course) return <LoadingState label="Loading course" lines={8} />;
  if (loaded.error) return <ErrorState error={loaded.error} onRetry={loaded.error.status === 404 ? undefined : loaded.reload} />;
  if (!course || !user) return null;
  const manager = can(user, "courses.manage");
  const editable = manager && course.actions.can_edit;

  async function call(label: string, path: string, method: "POST" | "PATCH" | "PUT", body?: unknown) {
    setBusy(label);
    try {
      const updated = await api<AdminCourseDetail>(`/api/v1/admin/courses/${course!.id}${path}`, { method, body: body ?? {} });
      setFresh(updated);
      toast(label);
      return updated;
    } catch (err) {
      toast("That did not work", { description: err instanceof ApiError ? err.detail : undefined });
      return null;
    } finally {
      setBusy(null);
    }
  }

  const linkedIds = new Set(course.competencies.map((c) => c.competency.id));

  return (
    <div className="flex flex-col gap-6">
      <PageHeader breadcrumbs={[{ label: "Courses", to: "/admin/courses" }, { label: cleanName(course.title) }]}
        title={cleanName(course.title)}
        meta={<><CourseStateBadge state={course.state} /><OriginBadge origin={course.content_origin} />{course.published_at ? <Badge tone="neutral">Published {formatDateTime(course.published_at)}</Badge> : null}</>}
        actions={course.state === "published" ? <Button variant="secondary" asChild><Link to={`/courses/${course.id}`}><Eye aria-hidden="true" />View as learner</Link></Button> : null}
        className="pb-0" />
      <p className="text-sm text-muted-foreground">{COURSE_STATE[course.state].description}</p>

      {course.source ? (
        <Alert tone="warning" title="Imported programme listing">
          {course.source.attribution}. Source review {course.source.verified ? "verified" : "not yet verified"}. Listings are read-only here and stay hidden from learners until reviewed.
        </Alert>
      ) : null}
      {course.state === "published" && manager ? <Alert tone="info">Unpublish the course to edit it. Learners' progress is kept.</Alert> : null}

      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <div className="flex flex-col gap-6">
          <Card as="section" aria-labelledby="details-title" className="p-6">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h2 id="details-title" className="text-base font-semibold">Details</h2>
              {editable && !editingDetails ? <Button variant="secondary" size="sm" onClick={() => { setForm(toForm(course)); setEditingDetails(true); }}><Pencil aria-hidden="true" />Edit details</Button> : null}
            </div>
            {editingDetails ? (
              <form className="mt-4 space-y-4" onSubmit={async (e) => { e.preventDefault(); const r = await call("Details saved", "", "PATCH", { ...formBody(form), row_version: course.row_version }); if (r) setEditingDetails(false); }}>
                {course.state === "approved" ? <Alert tone="warning">Saving changes sends this approved course back to draft for a new review.</Alert> : null}
                <CourseDetailsForm value={form} onChange={setForm} />
                <div className="flex justify-end gap-2">
                  <Button type="button" variant="ghost" onClick={() => setEditingDetails(false)}>Cancel</Button>
                  <Button type="submit" disabled={busy !== null}><Save aria-hidden="true" />Save details</Button>
                </div>
              </form>
            ) : (
              <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                <div className="sm:col-span-2"><dt className="text-muted-foreground">Description</dt><dd>{course.description ?? "Not written yet"}</dd></div>
                <div><dt className="text-muted-foreground">Provider</dt><dd>{cleanName(course.provider_organisation)}</dd></div>
                <div><dt className="text-muted-foreground">Difficulty</dt><dd className="capitalize">{course.difficulty ?? "Not set"}</dd></div>
                <div className="sm:col-span-2"><dt className="text-muted-foreground">Learning objectives</dt>
                  <dd>{course.learning_objectives.length ? <ul className="list-disc pl-5">{course.learning_objectives.map((o) => <li key={o}>{o}</li>)}</ul> : "None yet"}</dd></div>
              </dl>
            )}
          </Card>

          <Card as="section" aria-labelledby="structure-title" className="p-6">
            <h2 id="structure-title" className="text-base font-semibold">Modules and lessons</h2>
            {course.modules.length === 0 ? <p className="mt-2 text-sm text-muted-foreground">No modules yet.</p> : null}
            <ol className="mt-4 space-y-4">
              {course.modules.map((module) => (
                <li key={module.id} className="rounded-lg border border-border">
                  <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border bg-muted/40 px-4 py-3">
                    <p className="font-medium">Module {module.position}: {module.title}</p>
                    {editable ? <Button size="sm" variant="secondary" onClick={() => setLessonDialog({ moduleId: module.id })}><Plus aria-hidden="true" />Add lesson</Button> : null}
                  </div>
                  {module.lessons.length ? (
                    <ul className="divide-y divide-border">
                      {module.lessons.map((lesson) => (
                        <li key={lesson.id} className="flex flex-wrap items-center gap-2 px-4 py-2.5 text-sm">
                          <span className="min-w-0 flex-1">{lesson.position}. {lesson.title}</span>
                          <span className="text-muted-foreground">{LESSON_TYPE[lesson.lesson_type].label} · {minutesLabel(lesson.estimated_minutes)}</span>
                          {lesson.status === "inactive" ? <Badge>Hidden</Badge> : null}
                          <Button size="sm" variant="ghost" onClick={() => setLessonDialog({ moduleId: module.id, lesson })} aria-label={`${editable ? "Edit" : "View"} lesson ${lesson.title}`}>
                            {editable ? <Pencil aria-hidden="true" /> : <Eye aria-hidden="true" />}{editable ? "Edit" : "View"}
                          </Button>
                        </li>
                      ))}
                    </ul>
                  ) : <p className="px-4 py-3 text-sm text-muted-foreground">No lessons in this module.</p>}
                </li>
              ))}
            </ol>
            {editable ? (
              <form className="mt-4 flex flex-col gap-2 sm:flex-row sm:items-end" onSubmit={async (e) => { e.preventDefault(); if (moduleTitle.trim().length < 2) return; const r = await call("Module added", "/modules", "POST", { title: moduleTitle.trim() }); if (r) setModuleTitle(""); }}>
                <div className="flex-1"><Field id="new-module" label="New module title"><Input id="new-module" value={moduleTitle} onChange={(e) => setModuleTitle(e.target.value)} /></Field></div>
                <Button type="submit" variant="secondary" disabled={busy !== null || moduleTitle.trim().length < 2}><Plus aria-hidden="true" />Add module</Button>
              </form>
            ) : null}
          </Card>

          <Card as="section" aria-labelledby="links-title" className="p-6">
            <h2 id="links-title" className="text-base font-semibold">Competency links</h2>
            <p className="mt-1 text-sm text-muted-foreground">Links decide which learner gaps this course is recommended for. A reviewer approves them with the course.</p>
            {course.competencies.length ? (
              <ul className="mt-3 divide-y divide-border rounded-lg border border-border">
                {course.competencies.map((link) => (
                  <li key={link.id} className="flex flex-wrap items-center gap-2 px-4 py-2.5 text-sm">
                    <span className="min-w-0 flex-1">{cleanName(link.competency.name)}</span>
                    <Badge tone={link.relevance === "primary" ? "primary" : "neutral"}>{link.relevance === "primary" ? "Main focus" : "Also covers"}</Badge>
                    <Badge tone={link.status === "approved" ? "success" : "warning"}>{link.status === "approved" ? "Approved" : "Awaiting review"}</Badge>
                    {editable ? <Button size="sm" variant="ghost" onClick={() => void call("Link removed", "/competencies", "PUT", { competency_id: link.competency.id, relevance: null })} aria-label={`Remove link to ${link.competency.name}`}><Trash2 aria-hidden="true" /></Button> : null}
                  </li>
                ))}
              </ul>
            ) : <p className="mt-3 text-sm text-muted-foreground">No competency links yet.</p>}
            {editable && options.data ? (
              <form className="mt-4 grid gap-2 sm:grid-cols-[minmax(0,1fr)_10rem_auto] sm:items-end" onSubmit={async (e) => { e.preventDefault(); if (!linkCompetency) return; const r = await call("Competency linked", "/competencies", "PUT", { competency_id: linkCompetency, relevance: linkRelevance }); if (r) setLinkCompetency(""); }}>
                <Field id="link-competency" label="Competency">
                  <Select id="link-competency" value={linkCompetency} onChange={(e) => setLinkCompetency(e.target.value)}>
                    <option value="">Choose a competency</option>
                    {options.data.competencies.filter((c) => !linkedIds.has(c.id)).map((c) => <option key={c.id} value={c.id}>{cleanName(c.name)} ({c.code})</option>)}
                  </Select>
                </Field>
                <Field id="link-relevance" label="Relevance">
                  <Select id="link-relevance" value={linkRelevance} onChange={(e) => setLinkRelevance(e.target.value as "primary" | "secondary")}>
                    <option value="primary">Main focus</option><option value="secondary">Also covers</option>
                  </Select>
                </Field>
                <Button type="submit" variant="secondary" disabled={!linkCompetency || busy !== null}><Plus aria-hidden="true" />Link</Button>
              </form>
            ) : null}
          </Card>

          <Card as="section" aria-labelledby="course-history-title" className="p-6">
            <h2 id="course-history-title" className="text-base font-semibold">Review history</h2>
            <div className="mt-3"><ReviewHistory items={course.reviews} /></div>
          </Card>
        </div>

        <aside className="flex flex-col gap-4" aria-label="Publishing">
          <Card className="space-y-4 p-5">
            <h2 className="text-base font-semibold">Publishing checks</h2>
            <GuardChecklist checks={course.guards.checks} />
            {manager && course.actions.can_submit ? (
              <div className="space-y-2 border-t border-border pt-4">
                <label htmlFor="course-note" className="text-sm font-medium">Note for the reviewer (optional)</label>
                <Textarea id="course-note" rows={2} value={note} onChange={(e) => setNote(e.target.value)} />
                <Button className="w-full" disabled={busy !== null} onClick={async () => { const r = await call("Sent for review", "/submit", "POST", { note: note || null }); if (r) setNote(""); }}>
                  <Send aria-hidden="true" />Send for review
                </Button>
                <p className="text-xs text-muted-foreground">Another person with review rights decides. You cannot approve a course you submitted.</p>
              </div>
            ) : null}
            {manager && course.state === "draft" && !course.actions.can_submit && course.course_type === "internal" ? (
              <p className="border-t border-border pt-4 text-sm text-muted-foreground">Complete the first four checks to send this course for review.</p>
            ) : null}
            {manager && course.actions.can_withdraw ? <Button variant="secondary" className="w-full" disabled={busy !== null} onClick={() => void call("Withdrawn from review", "/withdraw", "POST")}><Undo2 aria-hidden="true" />Withdraw from review</Button> : null}
            {course.state === "in_review" ? <p className="text-sm text-muted-foreground">Waiting in the <Link to="/admin/review" className="text-primary underline underline-offset-4">review queue</Link>.</p> : null}
            {manager && course.actions.can_publish ? <Button className="w-full" disabled={busy !== null} onClick={() => setConfirmPublish(true)}><Rocket aria-hidden="true" />Publish to learners</Button> : null}
            {manager && course.actions.can_unpublish ? <Button variant="danger" className="w-full" disabled={busy !== null} onClick={() => setConfirmUnpublish(true)}><EyeOff aria-hidden="true" />Unpublish</Button> : null}
          </Card>
        </aside>
      </div>

      {lessonDialog ? (
        <LessonDialog courseId={course.id} moduleId={lessonDialog.moduleId} lesson={lessonDialog.lesson} readOnly={!editable}
          onClose={() => setLessonDialog(null)} onSaved={(updated) => { setFresh(updated); setLessonDialog(null); }} />
      ) : null}
      <ConfirmationDialog open={confirmPublish} onOpenChange={setConfirmPublish} title="Publish this course?"
        description="Learners will see it in the catalogue and it can be recommended for their gaps." confirmLabel="Publish"
        onConfirm={() => { setConfirmPublish(false); void call("Course published", "/publish", "POST"); }} />
      <ConfirmationDialog open={confirmUnpublish} onOpenChange={setConfirmUnpublish} title="Unpublish this course?" tone="danger"
        description="Learners will no longer see it. Their recorded progress is kept." confirmLabel="Unpublish"
        onConfirm={() => { if (unpublishReason.trim().length < 5) { toast("Give a reason of at least 5 characters"); return; } setConfirmUnpublish(false); void call("Course unpublished", "/unpublish", "POST", { reason: unpublishReason.trim() }).then(() => setUnpublishReason("")); }}>
        <Field id="unpublish-reason" label="Reason (recorded in the audit trail)" hint="At least 5 characters.">
          <Input id="unpublish-reason" value={unpublishReason} onChange={(e) => setUnpublishReason(e.target.value)} aria-describedby="unpublish-reason-hint" />
        </Field>
      </ConfirmationDialog>
    </div>
  );
}

function LessonDialog({ courseId, moduleId, lesson, readOnly, onClose, onSaved }: {
  courseId: string; moduleId: string; lesson?: AdminLesson; readOnly: boolean; onClose: () => void; onSaved: (c: AdminCourseDetail) => void;
}) {
  const [title, setTitle] = useState(lesson?.title ?? "");
  const [type, setType] = useState<AdminLesson["lesson_type"]>(lesson?.lesson_type ?? "reading");
  const [minutes, setMinutes] = useState(String(lesson?.estimated_minutes ?? 8));
  const [body, setBody] = useState(lesson?.body_markdown ?? "");
  const [status, setStatus] = useState<AdminLesson["status"]>(lesson?.status ?? "active");
  const [preview, setPreview] = useState(readOnly);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function save(event: FormEvent) {
    event.preventDefault();
    const m = Number(minutes);
    if (title.trim().length < 2 || !(m >= 1 && m <= 240) || body.trim().length < 20) {
      setError("Give a title, 1-240 minutes, and at least 20 characters of lesson text.");
      return;
    }
    setSaving(true);
    try {
      const payload = { title: title.trim(), lesson_type: type, estimated_minutes: m, body_markdown: body };
      const updated = lesson
        ? await api<AdminCourseDetail>(`/api/v1/admin/courses/${courseId}/lessons/${lesson.id}`, { method: "PATCH", body: { ...payload, status } })
        : await api<AdminCourseDetail>(`/api/v1/admin/courses/${courseId}/modules/${moduleId}/lessons`, { method: "POST", body: payload });
      toast(lesson ? "Lesson saved" : "Lesson added");
      onSaved(updated);
    } catch (err) {
      setError(err instanceof ApiError ? err.detail ?? err.message : "The lesson was not saved.");
      setSaving(false);
    }
  }

  return (
    <Dialog open onOpenChange={(open) => (open ? null : onClose())}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle>{readOnly ? lesson?.title : lesson ? "Edit lesson" : "Add lesson"}</DialogTitle>
          <DialogDescription>Lesson text uses simple Markdown: ## headings, lists, tables, **bold**. Links and images are not shown to learners.</DialogDescription>
        </DialogHeader>
        {error ? <Alert tone="danger" role="alert">{error}</Alert> : null}
        {readOnly ? (
          <div className="rounded-lg border border-border p-4"><Markdown source={body} /></div>
        ) : (
          <form id="lesson-form" onSubmit={save} noValidate className="grid gap-4 sm:grid-cols-3">
            <div className="sm:col-span-3"><Field id="lesson-title" label="Title"><Input id="lesson-title" value={title} onChange={(e) => setTitle(e.target.value)} /></Field></div>
            <Field id="lesson-type" label="Type">
              <Select id="lesson-type" value={type} onChange={(e) => setType(e.target.value as AdminLesson["lesson_type"])}>
                <option value="reading">Reading</option><option value="worked_example">Worked example</option><option value="practice_check">Practice check</option>
              </Select>
            </Field>
            <Field id="lesson-minutes" label="Minutes"><Input id="lesson-minutes" type="number" min={1} max={240} value={minutes} onChange={(e) => setMinutes(e.target.value)} /></Field>
            {lesson ? (
              <Field id="lesson-status" label="Visibility">
                <Select id="lesson-status" value={status} onChange={(e) => setStatus(e.target.value as AdminLesson["status"])}>
                  <option value="active">Shown</option><option value="inactive">Hidden</option>
                </Select>
              </Field>
            ) : <span />}
            <div className="sm:col-span-3 space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="lesson-body" className="text-sm font-medium">{preview ? "Preview" : "Lesson text"}</label>
                <Button type="button" size="sm" variant="ghost" onClick={() => setPreview((p) => !p)} aria-pressed={preview}>{preview ? "Edit text" : "Preview"}</Button>
              </div>
              {preview ? <div className="min-h-40 rounded-lg border border-border p-4"><Markdown source={body || "Nothing to preview yet."} /></div>
                : <Textarea id="lesson-body" rows={14} value={body} onChange={(e) => setBody(e.target.value)} className="font-mono text-sm" />}
            </div>
          </form>
        )}
        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>{readOnly ? "Close" : "Cancel"}</Button>
          {readOnly ? null : <Button type="submit" form="lesson-form" disabled={saving}>{saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Save aria-hidden="true" />}Save lesson</Button>}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
