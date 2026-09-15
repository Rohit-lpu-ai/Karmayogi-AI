import { ArrowRight, BookOpenCheck, FileQuestion, Gavel, Loader2 } from "lucide-react";
import { useRef, useState, type FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { ReviewTaskItem } from "@/api/adminTypes";
import { useApi } from "@/api/useApi";
import { formatDateTime } from "@/components/admin/common";
import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Field, Textarea } from "@/components/ui/form";
import { toast } from "@/components/ui/toaster";
import { FilterChip } from "./QuestionPages";

const DECISIONS = [
  { value: "approve", label: "Approve", hint: "The exact submitted version becomes usable (courses still need publishing)." },
  { value: "request_changes", label: "Request changes", hint: "Returns it to the author as a draft. A reason is required." },
  { value: "reject", label: "Reject", hint: "Marks it rejected. A reason is required." },
] as const;

/** /admin/review: human review of questions and courses (single reviewer; authors cannot decide their own work). */
export function ReviewQueuePage() {
  const [params, setParams] = useSearchParams();
  const status = (params.get("status") ?? "open") as "open" | "decided" | "all";
  const tasks = useApi<ReviewTaskItem[]>(`/api/v1/admin/reviews?status=${status}`);
  const [deciding, setDeciding] = useState<ReviewTaskItem | null>(null);

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Review queue"
        description="Every approval is a recorded human decision. You cannot decide an item you submitted; another reviewer must." className="pb-0" />
      <div role="group" aria-label="Filter reviews" className="flex flex-wrap gap-2">
        {(["open", "decided", "all"] as const).map((s) => (
          <FilterChip key={s} active={status === s} onClick={() => setParams(s === "open" ? {} : { status: s }, { replace: true })}>
            {s === "open" ? "Waiting" : s === "decided" ? "Decided" : "All"}
          </FilterChip>
        ))}
      </div>
      {tasks.loading && !tasks.data ? <LoadingState label="Loading review tasks" lines={5} /> : null}
      {tasks.error ? <ErrorState error={tasks.error} onRetry={tasks.reload} /> : null}
      {tasks.data && tasks.data.length === 0 ? (
        <EmptyState icon={<Gavel className="size-5" />} title={status === "open" ? "Nothing is waiting for review" : "No review decisions yet"}>
          Items appear here when an author sends a question or a course manager sends a course for review.
        </EmptyState>
      ) : null}
      {tasks.data && tasks.data.length > 0 ? (
        <ul className="grid gap-3">
          {tasks.data.map((task) => {
            const isQuestion = task.target_type === "question";
            const href = isQuestion ? `/admin/questions/${task.target_id}` : `/admin/courses/${task.target_id}`;
            return (
              <Card as="li" key={task.id} className="flex flex-col gap-3 p-5 md:flex-row md:items-center">
                <div className="min-w-0 flex-1 space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge tone="primary">{isQuestion ? <FileQuestion aria-hidden="true" /> : <BookOpenCheck aria-hidden="true" />}{isQuestion ? "Question" : "Course"}</Badge>
                    {task.decision ? <Badge tone={task.decision.decision === "approve" ? "success" : task.decision.decision === "reject" ? "danger" : "warning"}>
                      {task.decision.decision === "approve" ? "Approved" : task.decision.decision === "reject" ? "Rejected" : "Changes requested"}</Badge>
                      : task.status === "cancelled" ? <Badge>Withdrawn</Badge> : <Badge tone="info">Waiting</Badge>}
                  </div>
                  <h2 className="line-clamp-2 font-semibold">{task.title}</h2>
                  <p className="text-sm text-muted-foreground">
                    Submitted by {task.submitted_by?.display_name ?? "unknown"}, {formatDateTime(task.submitted_at)}
                    {task.decision ? ` · decided by ${task.decision.decided_by ?? "a reviewer"}` : ""}
                  </p>
                  {task.submission_note ? <p className="text-sm">"{task.submission_note}"</p> : null}
                  {task.decision?.reason ? <p className="rounded-md bg-muted px-3 py-2 text-sm">{task.decision.reason}</p> : null}
                  {task.blocked_reason ? <p className="text-sm text-warning">{task.blocked_reason}</p> : null}
                </div>
                <div className="flex flex-col gap-2 sm:flex-row md:flex-col lg:flex-row">
                  <Button variant="secondary" asChild>
                    <Link to={href}>Open {isQuestion ? "question" : "course"}<ArrowRight aria-hidden="true" /></Link>
                  </Button>
                  {task.can_decide ? <Button onClick={() => setDeciding(task)}><Gavel aria-hidden="true" />Decide</Button> : null}
                </div>
              </Card>
            );
          })}
        </ul>
      ) : null}
      {deciding ? <DecisionDialog task={deciding} onClose={() => setDeciding(null)} onDone={() => { setDeciding(null); tasks.reload(); }} /> : null}
    </div>
  );
}

function DecisionDialog({ task, onClose, onDone }: { task: ReviewTaskItem; onClose: () => void; onDone: () => void }) {
  const [decision, setDecision] = useState<(typeof DECISIONS)[number]["value"]>("approve");
  const [reason, setReason] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const reasonRef = useRef<HTMLTextAreaElement>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (decision !== "approve" && !reason.trim()) {
      setError("Give a reason so the author knows what to change.");
      reasonRef.current?.focus();
      return;
    }
    setSaving(true);
    try {
      await api(`/api/v1/admin/reviews/${task.id}/decision`, { method: "POST", body: { decision, reason: reason.trim() || null, row_version: task.row_version } });
      toast(decision === "approve" ? "Approved" : decision === "reject" ? "Rejected" : "Changes requested");
      onDone();
    } catch (err) {
      setError(err instanceof ApiError ? err.detail ?? err.message : "The decision was not saved.");
      setSaving(false);
    }
  }

  return (
    <Dialog open onOpenChange={(open) => (open ? null : onClose())}>
      <DialogContent className="sm:max-w-xl">
        <DialogHeader>
          <DialogTitle>Decide review</DialogTitle>
          <DialogDescription className="line-clamp-3">{task.title}</DialogDescription>
        </DialogHeader>
        <form id="decision-form" onSubmit={submit} noValidate className="space-y-4">
          <fieldset className="space-y-2">
            <legend className="text-sm font-medium">Decision</legend>
            {DECISIONS.map((d) => (
              <label key={d.value} className="flex cursor-pointer gap-3 rounded-lg border border-border p-3 has-[:checked]:border-primary has-[:checked]:bg-primary-soft/50">
                <input type="radio" name="decision" value={d.value} checked={decision === d.value} onChange={() => setDecision(d.value)} className="mt-1 size-4 accent-[var(--primary)]" />
                <span>
                  <span className="block font-medium">{d.label}</span>
                  <span className="block text-sm text-muted-foreground">{d.hint}</span>
                </span>
              </label>
            ))}
          </fieldset>
          <Field id="decision-reason" label={decision === "approve" ? "Comment (optional)" : "Reason"} error={error ?? undefined}>
            <Textarea ref={reasonRef} id="decision-reason" rows={3} value={reason} onChange={(e) => { setReason(e.target.value); setError(null); }}
              aria-invalid={error ? true : undefined} aria-describedby={error ? "decision-reason-error" : undefined} />
          </Field>
          <Alert tone="neutral">Open the item and read it in full before deciding. Your name and decision are recorded in the audit trail.</Alert>
        </form>
        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" form="decision-form" disabled={saving}>
            {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
            Record decision
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
