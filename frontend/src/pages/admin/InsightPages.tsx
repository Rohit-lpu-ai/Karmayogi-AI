import { Info, ShieldAlert } from "lucide-react";
import { Link, useSearchParams } from "react-router-dom";
import { useApi } from "@/api/useApi";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName } from "@/components/product/competency";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Select } from "@/components/ui/select";
import { cn } from "@/lib/utils";

export interface Count {
  value: number | null;
  suppressed: boolean;
}

interface GapCell {
  required_for: number | null;
  assessed: number | null;
  with_gap: number | null;
  share: number | null;
  average_gap: number | null;
  suppressed: boolean;
}

interface SkillGaps {
  competencies: { id: string; code: string; name: string }[];
  rows: { department: { id: string | null; name: string }; learners: Count; cells: Record<string, GapCell> }[];
  totals: Record<string, GapCell>;
  job_roles: { id: string; name: string }[];
  job_role_id: string | null;
  min_group_size: number;
  note: string;
}

interface TrainingNeeds {
  items: {
    competency: { id: string; code: string; name: string };
    learners_with_gap: number;
    average_gap: number;
    departments_affected: number;
    published_courses: number;
    learners_started_linked_course: Count;
    learners_completed_linked_course: Count;
    content_gap: boolean;
  }[];
  withheld_competencies: number;
  min_group_size: number;
  note: string;
}

export interface InsightSummary {
  learners: Count;
  baseline_completed: Count;
  learners_with_confirmed_gaps: Count;
  learners_started_learning: Count;
  learners_completed_a_course: Count;
  min_group_size: number;
  scope: "organisation" | "department";
  note: string;
}

export function countText(count: Count, min = 5): string {
  return count.suppressed || count.value === null ? `Under ${min}` : String(count.value);
}

/** Five steps from light to strong; text always carries the value so colour is never the only signal. */
function shade(share: number): string {
  if (share >= 0.8) return "bg-primary text-primary-foreground";
  if (share >= 0.6) return "bg-primary/75 text-primary-foreground";
  if (share >= 0.4) return "bg-primary/45 text-foreground";
  if (share >= 0.2) return "bg-primary/20 text-foreground";
  return "bg-primary/5 text-foreground";
}

function InsightNotice({ note }: { note: string }) {
  return (
    <Alert tone="neutral" icon={false}>
      <p className="flex gap-2"><ShieldAlert className="mt-0.5 size-4 shrink-0" aria-hidden="true" />{note}</p>
    </Alert>
  );
}

function Cell({ cell, min }: { cell: GapCell | undefined; min: number }) {
  if (!cell || (cell.required_for === null && !cell.suppressed && cell.assessed === null)) {
    return <td className="px-2 py-2 text-center text-muted-foreground"><span aria-hidden="true">-</span><span className="sr-only">Not required</span></td>;
  }
  if (cell.suppressed || cell.share === null) {
    return (
      <td className="bg-[repeating-linear-gradient(135deg,var(--muted),var(--muted)_4px,transparent_4px,transparent_8px)] px-2 py-2 text-center text-xs text-muted-foreground">
        &lt;{min}<span className="sr-only"> learners assessed; withheld</span>
      </td>
    );
  }
  return (
    <td className={cn("px-2 py-2 text-center tabular-nums", shade(cell.share))}>
      <span className="block text-sm font-semibold">{Math.round(cell.share * 100)}%</span>
      <span className="block text-[11px] opacity-90">{cell.with_gap} of {cell.assessed}</span>
    </td>
  );
}

/** /admin/skill-gaps: share of assessed learners with a confirmed gap, by department and competency (aggregates only). */
export function SkillGapsPage() {
  const [params, setParams] = useSearchParams();
  const jobRole = params.get("job_role_id") ?? "";
  const data = useApi<SkillGaps>(`/api/v1/admin/insight/skill-gaps${jobRole ? `?job_role_id=${jobRole}` : ""}`);
  const d = data.data;

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Skill gaps by department"
        description="Where assessed learners most often fall below the level their job role needs. Use it to plan learning support, not to judge people."
        className="pb-0" />
      {d ? <InsightNotice note={d.note} /> : null}
      <Card className="flex flex-col gap-3 p-4 sm:flex-row sm:items-end">
        <div className="flex flex-col gap-1.5 sm:w-80">
          <label htmlFor="insight-role" className="text-sm font-medium">Job role</label>
          <Select id="insight-role" value={jobRole} onChange={(e) => setParams(e.target.value ? { job_role_id: e.target.value } : {}, { replace: true })}>
            <option value="">All job roles</option>
            {(d?.job_roles ?? []).map((r) => <option key={r.id} value={r.id}>{cleanName(r.name)}</option>)}
          </Select>
        </div>
        <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground" aria-label="Legend">
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-primary/5 ring-1 ring-border" aria-hidden="true" />0-19%</span>
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-primary/20" aria-hidden="true" />20-39%</span>
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-primary/45" aria-hidden="true" />40-59%</span>
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-primary/75" aria-hidden="true" />60-79%</span>
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-primary" aria-hidden="true" />80% or more</span>
          <span className="flex items-center gap-1.5"><span className="inline-block size-4 rounded bg-[repeating-linear-gradient(135deg,var(--muted),var(--muted)_3px,transparent_3px,transparent_6px)] ring-1 ring-border" aria-hidden="true" />Fewer than {d?.min_group_size ?? 5} assessed: withheld</span>
          <span>- not required for that group</span>
        </div>
      </Card>
      {data.loading && !d ? <LoadingState label="Loading skill gaps" lines={6} /> : null}
      {data.error ? <ErrorState error={data.error} onRetry={data.reload} /> : null}
      {d && d.rows.length === 0 ? <EmptyState title="No learners in scope yet" /> : null}
      {d && d.rows.length > 0 ? (
        <div className="relative overflow-x-auto rounded-lg border border-border bg-card" tabIndex={0} role="region" aria-label="Skill gap heatmap, scrolls sideways">
          <table className="w-full min-w-[48rem] border-collapse text-sm">
            <caption className="sr-only">Share of assessed learners with a confirmed gap, by department (rows) and competency (columns)</caption>
            <thead>
              <tr className="border-b border-border bg-muted/60">
                <th scope="col" className="sticky left-0 z-10 min-w-48 bg-muted px-3 py-2 text-left font-semibold">Department</th>
                {d.competencies.map((c) => (
                  <th key={c.id} scope="col" className="min-w-24 px-2 py-2 text-center text-xs font-semibold leading-tight">{cleanName(c.name)}<span className="mt-0.5 block font-mono text-[10px] font-normal text-muted-foreground">{c.code}</span></th>
                ))}
              </tr>
            </thead>
            <tbody>
              {d.rows.map((row) => (
                <tr key={row.department.id ?? "none"} className="border-b border-border">
                  <th scope="row" className="sticky left-0 z-10 bg-card px-3 py-2 text-left font-medium">
                    {cleanName(row.department.name)}
                    <span className="block text-xs font-normal text-muted-foreground">{countText(row.learners, d.min_group_size)} learners</span>
                  </th>
                  {d.competencies.map((c) => <Cell key={c.id} cell={row.cells[c.id]} min={d.min_group_size} />)}
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr className="bg-muted/40">
                <th scope="row" className="sticky left-0 z-10 bg-muted px-3 py-2 text-left font-semibold">All in scope</th>
                {d.competencies.map((c) => <Cell key={c.id} cell={d.totals[c.id]} min={d.min_group_size} />)}
              </tr>
            </tfoot>
          </table>
        </div>
      ) : null}
      <p className="flex gap-2 text-sm text-muted-foreground">
        <Info className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
        Each figure counts learners whose baseline evidence is at least medium. A learner appears once per competency their role requires.
        See <Link to="/admin/training-needs" className="text-primary underline underline-offset-4">training needs</Link> for what to act on first.
      </p>
    </div>
  );
}

/** /admin/training-needs: competencies ranked by how many learners have a confirmed gap, with learning coverage. */
export function TrainingNeedsPage() {
  const data = useApi<TrainingNeeds>("/api/v1/admin/insight/training-needs");
  const d = data.data;
  const max = Math.max(1, ...(d?.items ?? []).map((i) => i.learners_with_gap));
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Training needs"
        description="Competencies ranked by the number of learners with a confirmed gap, with the learning currently available for each."
        className="pb-0" />
      {d ? <InsightNotice note={d.note} /> : null}
      {data.loading && !d ? <LoadingState label="Loading training needs" lines={6} /> : null}
      {data.error ? <ErrorState error={data.error} onRetry={data.reload} /> : null}
      {d && d.items.length === 0 ? <EmptyState title="No training needs to show">Needs appear when at least {d.min_group_size} assessed learners share a gap.</EmptyState> : null}
      {d && d.items.length > 0 ? (
        <ol className="grid gap-3">
          {d.items.map((item, index) => (
            <Card as="li" key={item.competency.id} className="grid gap-4 p-5 md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] md:items-center">
              <div className="min-w-0 space-y-2">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-semibold tabular-nums text-muted-foreground">{index + 1}.</span>
                  <h2 className="font-semibold">{cleanName(item.competency.name)}</h2>
                  {item.content_gap ? <Badge tone="danger">No published course</Badge> : null}
                </div>
                <div className="flex items-center gap-3">
                  <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-muted" aria-hidden="true">
                    <div className="h-full rounded-full bg-primary" style={{ width: `${(item.learners_with_gap / max) * 100}%` }} />
                  </div>
                  <span className="w-40 shrink-0 text-sm tabular-nums">{item.learners_with_gap} learners with a gap</span>
                </div>
                <p className="text-sm text-muted-foreground">Average gap {item.average_gap} level{item.average_gap === 1 ? "" : "s"} · {item.departments_affected} department{item.departments_affected === 1 ? "" : "s"}</p>
              </div>
              <dl className="grid grid-cols-3 gap-2 text-center text-sm">
                <div className="rounded-lg bg-muted/60 px-2 py-2"><dt className="text-xs text-muted-foreground">Published courses</dt><dd className="text-lg font-semibold tabular-nums">{item.published_courses}</dd></div>
                <div className="rounded-lg bg-muted/60 px-2 py-2"><dt className="text-xs text-muted-foreground">Started one</dt><dd className={cn("font-semibold tabular-nums", item.learners_started_linked_course.suppressed ? "text-sm leading-7" : "text-lg")}>{countText(item.learners_started_linked_course, d.min_group_size)}</dd></div>
                <div className="rounded-lg bg-muted/60 px-2 py-2"><dt className="text-xs text-muted-foreground">Completed one</dt><dd className={cn("font-semibold tabular-nums", item.learners_completed_linked_course.suppressed ? "text-sm leading-7" : "text-lg")}>{countText(item.learners_completed_linked_course, d.min_group_size)}</dd></div>
              </dl>
            </Card>
          ))}
        </ol>
      ) : null}
      {d && d.withheld_competencies > 0 ? (
        <p className="text-sm text-muted-foreground">{d.withheld_competencies} competenc{d.withheld_competencies === 1 ? "y is" : "ies are"} not listed because fewer than {d.min_group_size} learners have that gap.</p>
      ) : null}
    </div>
  );
}
