import { Archive, ArrowRight, CheckCircle2, FilePlus2, Loader2, Pencil, Search, Send, Undo2 } from "lucide-react";
import { useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { QuestionDetail, QuestionList } from "@/api/adminTypes";
import { useApi } from "@/api/useApi";
import { can, useAuth } from "@/auth/AuthContext";
import { formatDateTime, OriginBadge, QuestionStatusBadge, QUESTION_STATUS, ReviewHistory } from "@/components/admin/common";
import { PageHeader } from "@/components/layout/PageHeader";
import { ConfirmationDialog } from "@/components/product/ConfirmationDialog";
import { DifficultyBadge } from "@/components/product/competency";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input, Textarea } from "@/components/ui/form";
import { Select } from "@/components/ui/select";
import { toast } from "@/components/ui/toaster";
import { QuestionEditor } from "./QuestionEditor";

const STATUS_TABS = ["draft", "in_review", "approved", "rejected", "retired"];

/** /admin/questions: the question bank with lifecycle filters. */
export function AdminQuestionsPage() {
  const [params, setParams] = useSearchParams();
  const status = params.get("status") ?? "";
  const q = params.get("q") ?? "";
  const origin = params.get("origin") ?? "";
  const [search, setSearch] = useState(q);
  const query = useMemo(() => {
    const p = new URLSearchParams({ page_size: "50" });
    if (status) p.set("status", status);
    if (q) p.set("q", q);
    if (origin) p.set("origin", origin);
    return p.toString();
  }, [status, q, origin]);
  const list = useApi<QuestionList>(`/api/v1/admin/questions?${query}`);

  function set(key: string, value: string) {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    setParams(next, { replace: true });
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Questions"
        description="Author assessment questions, attach source metadata and send them for review. Only approved questions can be used in assessments."
        actions={<Button asChild><Link to="/admin/questions/new"><FilePlus2 aria-hidden="true" />New question</Link></Button>} className="pb-0" />

      <div role="group" aria-label="Filter by status" className="flex flex-wrap gap-2">
        <FilterChip active={!status} onClick={() => set("status", "")}>All</FilterChip>
        {STATUS_TABS.map((s) => (
          <FilterChip key={s} active={status === s} onClick={() => set("status", s)}>
            {QUESTION_STATUS[s].label} <span className="tabular-nums text-muted-foreground">{list.data?.status_counts[s] ?? 0}</span>
          </FilterChip>
        ))}
      </div>

      <Card className="p-4">
        <form role="search" className="grid gap-3 sm:grid-cols-[minmax(0,1fr)_14rem]" onSubmit={(e) => { e.preventDefault(); set("q", search.trim()); }}>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="question-search" className="text-sm font-medium">Search</label>
            <div className="flex gap-2">
              <Input id="question-search" type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Question text or competency" />
              <Button type="submit" variant="secondary" size="icon" aria-label="Search questions"><Search aria-hidden="true" /></Button>
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="question-origin" className="text-sm font-medium">Origin</label>
            <Select id="question-origin" value={origin} onChange={(e) => set("origin", e.target.value)}>
              <option value="">Any origin</option>
              <option value="human_authored">Authored here</option>
              <option value="demo_seed">Synthetic seed</option>
            </Select>
          </div>
        </form>
      </Card>

      {list.loading && !list.data ? <LoadingState label="Loading questions" lines={6} /> : null}
      {list.error ? <ErrorState error={list.error} onRetry={list.reload} /> : null}
      {list.data && list.data.items.length === 0 ? (
        <EmptyState title="No questions match" action={<Button asChild variant="secondary"><Link to="/admin/questions/new">Write a question</Link></Button>}>
          Change the filters, or write the first question.
        </EmptyState>
      ) : null}
      {list.data && list.data.items.length > 0 ? (
        <section aria-label={`${list.data.total} questions`} className="space-y-2">
          <p className="text-sm text-muted-foreground">{list.data.total} question{list.data.total === 1 ? "" : "s"}{list.data.total > list.data.items.length ? `, showing ${list.data.items.length}` : ""}</p>
          <ul className="grid gap-2">
            {list.data.items.map((item) => (
              <Card as="li" key={item.id} className="relative flex flex-col gap-2 p-4 hover:border-primary/40 sm:flex-row sm:items-center">
                <div className="min-w-0 flex-1 space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <QuestionStatusBadge status={item.status} />
                    <OriginBadge origin={item.origin} />
                    <DifficultyBadge difficulty={item.difficulty} />
                    {item.source_count === 0 ? <Badge tone="warning">No source</Badge> : null}
                  </div>
                  <Link to={`/admin/questions/${item.id}`} className="line-clamp-2 font-medium after:absolute after:inset-0 after:rounded-xl hover:text-primary focus-visible:outline-none after:focus-visible:ring-2 after:focus-visible:ring-ring">
                    {item.stem}
                  </Link>
                  <p className="text-sm text-muted-foreground">{item.competency.name} · version {item.version_number} · updated {formatDateTime(item.updated_at)}</p>
                </div>
                <ArrowRight className="hidden size-4 text-muted-foreground sm:block" aria-hidden="true" />
              </Card>
            ))}
          </ul>
        </section>
      ) : null}
    </div>
  );
}

export function FilterChip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button type="button" aria-pressed={active} onClick={onClick} data-focus-ring=""
      className={`inline-flex min-h-9 items-center gap-1.5 rounded-full border px-3 text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring ${active ? "border-primary bg-primary-soft text-primary-soft-foreground" : "border-border bg-card text-foreground hover:bg-muted"}`}>
      {children}
    </button>
  );
}

/** /admin/questions/new */
export function AdminQuestionNewPage() {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col gap-6">
      <PageHeader breadcrumbs={[{ label: "Questions", to: "/admin/questions" }, { label: "New question" }]}
        title="New question" description="Saved as a draft. Send it for review when it has source metadata." className="pb-0" />
      <QuestionEditor onSaved={(q) => { toast("Draft saved"); navigate(`/admin/questions/${q.id}`, { replace: true }); }} onCancel={() => navigate("/admin/questions")} />
    </div>
  );
}

/** /admin/questions/:questionId: current version, sources, lifecycle actions, versions and review history. */
export function AdminQuestionDetailPage() {
  const { questionId } = useParams();
  const { user } = useAuth();
  const loaded = useApi<QuestionDetail>(questionId ? `/api/v1/admin/questions/${questionId}` : null);
  const [fresh, setFresh] = useState<QuestionDetail | null>(null);
  const [editing, setEditing] = useState(false);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [confirmRetire, setConfirmRetire] = useState(false);
  const question = fresh && fresh.id === questionId ? fresh : loaded.data;

  if (loaded.loading && !question) return <LoadingState label="Loading question" lines={8} />;
  if (loaded.error) return <ErrorState error={loaded.error} onRetry={loaded.error.status === 404 ? undefined : loaded.reload} />;
  if (!question || !user) return null;
  const v = question.current_version;
  const isAuthor = can(user, "questions.author");

  async function act(path: string, label: string, body?: unknown) {
    setBusy(label);
    try {
      setFresh(await api<QuestionDetail>(`/api/v1/admin/questions/${question!.id}/${path}`, { method: "POST", body: body ?? {} }));
      toast(label);
      setNote("");
    } catch (err) {
      toast("That did not work", { description: err instanceof ApiError ? err.detail : undefined });
    } finally {
      setBusy(null);
    }
  }

  if (editing) {
    return (
      <div className="flex flex-col gap-6">
        <PageHeader breadcrumbs={[{ label: "Questions", to: "/admin/questions" }, { label: `Question v${v.version_number}`, to: `/admin/questions/${question.id}` }, { label: "Edit" }]}
          title="Edit question" description={`Saving creates version ${v.version_number + 1}. Earlier versions stay unchanged.`} className="pb-0" />
        <QuestionEditor existing={question} onSaved={(q) => { setFresh(q); setEditing(false); toast("New version saved"); }} onCancel={() => setEditing(false)} />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader breadcrumbs={[{ label: "Questions", to: "/admin/questions" }, { label: `Version ${v.version_number}` }]}
        title="Question"
        meta={<><QuestionStatusBadge status={question.status} /><OriginBadge origin={question.origin} /><DifficultyBadge difficulty={v.difficulty} /><Badge tone="neutral">Version {v.version_number}</Badge></>}
        actions={isAuthor && question.actions.can_edit ? <Button variant="secondary" onClick={() => setEditing(true)}><Pencil aria-hidden="true" />Edit</Button> : null}
        className="pb-0" />

      {question.is_demo ? <Alert tone="neutral">Synthetic seed question created for local evaluation. It was not written or reviewed by a person; it cannot be edited here.</Alert> : null}

      <div className="grid items-start gap-6 lg:grid-cols-[minmax(0,1fr)_22rem]">
        <div className="flex flex-col gap-6">
          <Card as="section" aria-labelledby="content-title" className="p-6">
            <h2 id="content-title" className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">{v.competency.name}</h2>
            <p className="mt-3 whitespace-pre-line text-lg leading-relaxed">{v.stem}</p>
            <ol className="mt-4 space-y-2">
              {v.options.map((o) => (
                <li key={o.label} className={`flex items-start gap-3 rounded-lg border px-3 py-2.5 ${o.is_correct ? "border-success/40 bg-success-soft" : "border-border"}`}>
                  <span className="font-semibold tabular-nums">{o.label}.</span>
                  <span className="flex-1">{o.text}</span>
                  {o.is_correct ? <span className="inline-flex items-center gap-1 text-sm font-medium text-success"><CheckCircle2 className="size-4" aria-hidden="true" />Correct</span> : null}
                </li>
              ))}
            </ol>
            <div className="mt-4 rounded-lg bg-muted px-4 py-3">
              <p className="text-sm font-semibold">Explanation</p>
              <p className="mt-1 whitespace-pre-line text-sm">{v.explanation}</p>
            </div>
          </Card>

          <Card as="section" aria-labelledby="checks-title" className="p-6">
            <h2 id="checks-title" className="text-base font-semibold">Wording and structure checks</h2>
            <p className="mt-1 text-sm text-muted-foreground">Fixed rules ({question.quality_checks.method}), not AI. They help the author and reviewer; they do not approve anything.</p>
            {question.quality_checks.findings.length === 0 ? (
              <p className="mt-3 flex items-center gap-2 text-sm text-success"><CheckCircle2 className="size-4" aria-hidden="true" />No issues found by the rules.</p>
            ) : (
              <ul className="mt-3 space-y-2">
                {question.quality_checks.findings.map((f) => (
                  <li key={f.code} className="flex items-start gap-2 text-sm">
                    <Badge tone={f.severity === "error" ? "danger" : "warning"}>{f.severity === "error" ? "Must fix" : "Consider"}</Badge>
                    <span>{f.message}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card as="section" aria-labelledby="sources-title" className="p-6">
            <h2 id="sources-title" className="text-base font-semibold">Source metadata</h2>
            {v.sources.length === 0 ? (
              <p className="mt-2 text-sm text-muted-foreground">{question.origin === "demo_seed" ? "Seeded before source metadata existed; labelled as synthetic content." : "No source yet. Add one before sending for review."}</p>
            ) : (
              <ul className="mt-3 space-y-3">
                {v.sources.map((s) => (
                  <li key={s.id} className="rounded-lg border border-border p-3 text-sm">
                    <p className="font-medium">{s.label}</p>
                    <p className="text-muted-foreground">{s.status}{s.locator ? ` · ${s.locator}` : ""}</p>
                    {s.note ? <p className="mt-1">{s.note}</p> : null}
                    {s.url ? <p className="mt-1 break-all text-muted-foreground">{s.url}</p> : null}
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card as="section" aria-labelledby="history-title" className="p-6">
            <h2 id="history-title" className="text-base font-semibold">Review history</h2>
            <div className="mt-3"><ReviewHistory items={question.reviews} /></div>
          </Card>
        </div>

        <aside className="flex flex-col gap-4" aria-label="Question actions and versions">
          {isAuthor && (question.actions.can_submit || question.actions.can_withdraw || question.actions.can_retire) ? (
            <Card className="space-y-3 p-5">
              <h2 className="text-base font-semibold">Next step</h2>
              {question.actions.can_submit ? (
                <>
                  <p className="text-sm text-muted-foreground">A different reviewer decides. You cannot approve your own question.</p>
                  <label htmlFor="submit-note" className="text-sm font-medium">Note for the reviewer (optional)</label>
                  <Textarea id="submit-note" rows={2} value={note} onChange={(e) => setNote(e.target.value)} />
                  <Button className="w-full" onClick={() => void act("submit", "Sent for review", { note: note || null })} disabled={busy !== null || v.sources.length === 0}>
                    {busy === "Sent for review" ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Send aria-hidden="true" />}
                    Send for review
                  </Button>
                  {v.sources.length === 0 ? <p className="text-sm text-danger">Add source metadata first.</p> : null}
                </>
              ) : null}
              {question.actions.can_withdraw ? (
                <Button variant="secondary" className="w-full" onClick={() => void act("withdraw", "Withdrawn from review")} disabled={busy !== null}>
                  <Undo2 aria-hidden="true" />Withdraw from review
                </Button>
              ) : null}
              {question.actions.can_retire ? (
                <Button variant="danger" className="w-full" onClick={() => setConfirmRetire(true)} disabled={busy !== null}>
                  <Archive aria-hidden="true" />Retire question
                </Button>
              ) : null}
            </Card>
          ) : null}
          {question.status === "in_review" && question.open_task_id ? (
            <Alert tone="info" title="Waiting for review">A reviewer decides from the <Link to="/admin/review">review queue</Link>.</Alert>
          ) : null}

          <Card className="p-5">
            <h2 className="text-base font-semibold">Versions</h2>
            <ol className="mt-3 space-y-2 text-sm">
              {question.versions.map((ver) => (
                <li key={ver.id} className="flex flex-wrap items-center justify-between gap-2">
                  <span>Version {ver.version_number}{ver.created_by ? ` by ${ver.created_by}` : ""}</span>
                  <span className="flex items-center gap-2 text-muted-foreground">{ver.is_approved ? <Badge tone="success">Approved</Badge> : null}{formatDateTime(ver.created_at)}</span>
                </li>
              ))}
            </ol>
          </Card>
          <Card className="p-5">
            <h2 className="text-base font-semibold">Used in assessments</h2>
            {question.used_in_assessments.length ? (
              <ul className="mt-2 space-y-1 text-sm">{question.used_in_assessments.map((a) => <li key={a.id}>{a.title} <span className="text-muted-foreground">({a.status})</span></li>)}</ul>
            ) : <p className="mt-2 text-sm text-muted-foreground">Not used in any assessment.</p>}
          </Card>
        </aside>
      </div>

      <ConfirmationDialog open={confirmRetire} onOpenChange={setConfirmRetire} title="Retire this question?"
        description="Retired questions cannot be added to new assessments. The question and its history are kept."
        confirmLabel="Retire question" tone="danger" onConfirm={() => { setConfirmRetire(false); void act("retire", "Question retired"); }} />
    </div>
  );
}
