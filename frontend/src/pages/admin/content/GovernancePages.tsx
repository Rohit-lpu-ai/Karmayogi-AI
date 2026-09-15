import { ChevronDown, Lock, Search } from "lucide-react";
import { useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import type { AssessmentOverview, AuditEntry, AuditPage, CompetencyStructure } from "@/api/adminTypes";
import { api, ApiError } from "@/api/client";
import { useApi } from "@/api/useApi";
import { formatDateTime, GuardChecklist } from "@/components/admin/common";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName } from "@/components/product/competency";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Select } from "@/components/ui/select";
import { roleLabel } from "@/config/roles";
import { cn } from "@/lib/utils";

/** /admin/competencies: frameworks, competencies with approved-question coverage, and job-role requirements (read-only). */
export function AdminCompetenciesPage() {
  const structure = useApi<CompetencyStructure>("/api/v1/admin/competencies");
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Competencies"
        description="Frameworks, competencies and the levels each job role requires. Changing requirements needs a recorded decision and is not available on this screen."
        className="pb-0" />
      {structure.loading ? <LoadingState label="Loading competency structure" lines={6} /> : null}
      {structure.error ? <ErrorState error={structure.error} onRetry={structure.reload} /> : null}
      {structure.data ? (
        <>
          <section aria-labelledby="frameworks-title" className="space-y-3">
            <h2 id="frameworks-title" className="text-lg font-semibold">Frameworks</h2>
            {structure.data.frameworks.map((f) => (
              <Collapsible key={f.id} defaultOpen={!f.definitions_restricted && f.competencies.length <= 10}>
                <Card className="overflow-hidden">
                  <CollapsibleTrigger asChild>
                    <button type="button" data-focus-ring="" className="group flex w-full flex-wrap items-center gap-2 px-5 py-4 text-left hover:bg-muted/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring">
                      <span className="min-w-0 flex-1">
                        <span className="block font-semibold">{cleanName(f.name)}</span>
                        <span className="block text-sm text-muted-foreground">{f.code} · {f.version_label} · {f.competencies.length} competencies · {f.level_count} levels</span>
                      </span>
                      <Badge tone={f.status === "approved" ? "success" : "warning"}>{f.status === "approved" ? "Approved" : "Draft"}</Badge>
                      {f.definitions_restricted ? <Badge tone="warning"><Lock aria-hidden="true" />Licence-restricted</Badge> : null}
                      {f.is_demo ? <Badge tone="neutral">Synthetic</Badge> : null}
                      <ChevronDown className="size-4 text-muted-foreground transition-transform group-data-[state=open]:rotate-180" aria-hidden="true" />
                    </button>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    {f.definitions_restricted ? <p className="border-t border-border px-5 py-3 text-sm text-muted-foreground">Definitions are not shown or reused until permission from the publisher is confirmed.</p> : null}
                    <div className="relative overflow-x-auto border-t border-border" tabIndex={0} role="region" aria-label={`Competencies in ${f.code}`}>
                      <table className="w-full text-sm">
                        <thead><tr className="bg-muted/60 text-left"><th scope="col" className="px-5 py-2 font-semibold">Competency</th><th scope="col" className="px-3 py-2 font-semibold">Code</th><th scope="col" className="px-3 py-2 text-right font-semibold">Approved questions</th></tr></thead>
                        <tbody>
                          {f.competencies.map((c) => (
                            <tr key={c.id} className="border-t border-border align-top">
                              <td className="px-5 py-2.5"><p className="font-medium">{cleanName(c.name)}</p>{c.description ? <p className="mt-0.5 max-w-2xl text-muted-foreground">{c.description}</p> : null}</td>
                              <td className="px-3 py-2.5 font-mono text-xs">{c.code}</td>
                              <td className={cn("px-3 py-2.5 text-right tabular-nums", c.approved_questions < 5 && "text-warning")}>{c.approved_questions}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CollapsibleContent>
                </Card>
              </Collapsible>
            ))}
          </section>
          <section aria-labelledby="roles-title" className="space-y-3">
            <h2 id="roles-title" className="text-lg font-semibold">Job-role requirements</h2>
            <div className="grid gap-4 md:grid-cols-2">
              {structure.data.job_roles.map((r) => (
                <Card as="section" key={r.id} aria-labelledby={`role-${r.id}`} className="p-5">
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 id={`role-${r.id}`} className="min-w-0 flex-1 font-semibold">{cleanName(r.name)}</h3>
                    {r.status !== "active" ? <Badge>Inactive</Badge> : null}
                  </div>
                  {r.requirements.length ? (
                    <ul className="mt-3 space-y-1.5 text-sm">
                      {r.requirements.map((req) => (
                        <li key={req.competency.id} className="flex items-center justify-between gap-2">
                          <span>{cleanName(req.competency.name)}</span>
                          <span className="shrink-0 tabular-nums text-muted-foreground">Level {req.required_level}{req.status !== "approved" ? ` (${req.status})` : ""}</span>
                        </li>
                      ))}
                    </ul>
                  ) : <p className="mt-2 text-sm text-muted-foreground">No requirements defined.</p>}
                </Card>
              ))}
            </div>
          </section>
        </>
      ) : null}
    </div>
  );
}

/** /admin/assessments: item coverage per competency and the checks a publishable assessment must pass (read-only). */
export function AdminAssessmentsPage() {
  const assessments = useApi<AssessmentOverview[]>("/api/v1/admin/assessments");
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Assessments"
        description="Coverage and quality checks for each assessment. Published assessments are fixed: learners' results always refer to the exact items they answered."
        className="pb-0" />
      <Alert tone="neutral">New assessments are assembled from approved questions. Assembling and versioning assessments from this screen is planned for a later step; <Link to="/admin/questions">approved questions</Link> are already usable for that.</Alert>
      {assessments.loading ? <LoadingState label="Loading assessments" lines={6} /> : null}
      {assessments.error ? <ErrorState error={assessments.error} onRetry={assessments.reload} /> : null}
      {assessments.data?.length === 0 ? <EmptyState title="No assessments yet" /> : null}
      <ul className="grid gap-4">
        {(assessments.data ?? []).map((a) => (
          <Card as="li" key={a.id} className="grid gap-5 p-5 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)]">
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <Badge tone={a.status === "published" ? "success" : a.status === "draft" ? "neutral" : "warning"}>{a.status === "published" ? "Published" : a.status === "draft" ? "Draft" : "Retired"}</Badge>
                <Badge tone="neutral">{a.purpose === "pre" ? "Baseline" : a.purpose}</Badge>
                {a.is_demo ? <Badge tone="neutral">Synthetic</Badge> : null}
              </div>
              <h2 className="font-semibold">{cleanName(a.title)}</h2>
              <p className="text-sm text-muted-foreground">
                {a.job_role ? cleanName(a.job_role.name) : "No job role"} · {a.item_count} items{a.published_at ? ` · published ${formatDateTime(a.published_at)}` : ""}
                {a.demo_seed_items ? ` · ${a.demo_seed_items} synthetic seed items` : ""}
              </p>
              <div className="relative overflow-x-auto rounded-lg border border-border" tabIndex={0} role="region" aria-label={`Coverage for ${cleanName(a.title)}`}>
                <table className="w-full text-sm">
                  <caption className="sr-only">Items per competency</caption>
                  <thead><tr className="bg-muted/60 text-left"><th scope="col" className="px-3 py-2 font-semibold">Competency</th><th scope="col" className="px-3 py-2 text-right font-semibold">Items</th></tr></thead>
                  <tbody>{a.coverage.map((c) => (
                    <tr key={c.competency.id} className="border-t border-border">
                      <td className="px-3 py-2">{cleanName(c.competency.name)}</td>
                      <td className={cn("px-3 py-2 text-right tabular-nums", c.items < 5 && "font-medium text-danger")}>{c.items}</td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            </div>
            <div className="space-y-2">
              <GuardChecklist title="Quality checks" checks={a.checks} />
              <p className={cn("text-sm font-medium", a.publishable ? "text-success" : "text-danger")}>{a.publishable ? "Meets every check." : "Does not meet every check."}</p>
            </div>
          </Card>
        ))}
      </ul>
    </div>
  );
}

const OUTCOME_TONE = { success: "success", denied: "warning", failure: "danger" } as const;

/** /admin/audit: organisation audit trail, newest first, with filters and details (read-only). */
export function AdminAuditPage() {
  const [params, setParams] = useSearchParams();
  const action = params.get("action") ?? "";
  const outcome = params.get("outcome") ?? "";
  const query = useMemo(() => {
    const p = new URLSearchParams({ limit: "50" });
    if (action) p.set("action", `${action}.`);
    if (outcome) p.set("outcome", outcome);
    return p.toString();
  }, [action, outcome]);
  const page = useApi<AuditPage>(`/api/v1/admin/audit?${query}`);
  const [more, setMore] = useState<{ query: string; items: AuditEntry[]; next: number | null } | null>(null);
  const [loadingMore, setLoadingMore] = useState(false);
  const extra = more && more.query === query ? more : null;
  const items = [...(page.data?.items ?? []), ...(extra?.items ?? [])];
  const next = extra ? extra.next : page.data?.next_before_id ?? null;

  async function loadMore() {
    if (!next) return;
    setLoadingMore(true);
    try {
      const data = await api<AuditPage>(`/api/v1/admin/audit?${query}&before_id=${next}`);
      setMore({ query, items: [...(extra?.items ?? []), ...data.items], next: data.next_before_id });
    } catch (err) {
      console.error(err instanceof ApiError ? err.code : err);
    } finally {
      setLoadingMore(false);
    }
  }

  const set = (key: string, value: string) => {
    const nextParams = new URLSearchParams(params);
    if (value) nextParams.set(key, value);
    else nextParams.delete(key);
    setParams(nextParams, { replace: true });
  };

  return (
    <div className="flex flex-col gap-6">
      <PageHeader title="Audit trail"
        description="Every sign-in, account change, content decision and publication, newest first. Entries cannot be edited or deleted."
        className="pb-0" />
      <Card className="grid gap-3 p-4 sm:grid-cols-2 lg:max-w-2xl">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="audit-action" className="text-sm font-medium">Area</label>
          <Select id="audit-action" value={action} onChange={(e) => set("action", e.target.value)}>
            <option value="">All areas</option>
            {(page.data?.action_groups ?? []).map((g) => <option key={g} value={g}>{g}</option>)}
          </Select>
        </div>
        <div className="flex flex-col gap-1.5">
          <label htmlFor="audit-outcome" className="text-sm font-medium">Outcome</label>
          <Select id="audit-outcome" value={outcome} onChange={(e) => set("outcome", e.target.value)}>
            <option value="">Any outcome</option><option value="success">Success</option><option value="denied">Denied</option><option value="failure">Failure</option>
          </Select>
        </div>
      </Card>
      {page.loading && !page.data ? <LoadingState label="Loading audit trail" lines={8} /> : null}
      {page.error ? <ErrorState error={page.error} onRetry={page.reload} /> : null}
      {page.data && items.length === 0 ? <EmptyState icon={<Search className="size-5" />} title="No entries match these filters" /> : null}
      {items.length ? (
        <ol className="divide-y divide-border rounded-lg border border-border bg-card" aria-label="Audit entries">
          {items.map((entry) => (
            <li key={entry.id}>
              <Collapsible>
                <CollapsibleTrigger asChild>
                  <button type="button" data-focus-ring="" className="group flex w-full flex-wrap items-center gap-x-3 gap-y-1 px-4 py-3 text-left text-sm hover:bg-muted/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring">
                    <span className="w-40 shrink-0 tabular-nums text-muted-foreground">{formatDateTime(entry.occurred_at)}</span>
                    <span className="font-mono text-xs font-medium">{entry.action}</span>
                    <Badge tone={OUTCOME_TONE[entry.outcome]}>{entry.outcome}</Badge>
                    <span className="min-w-0 flex-1 truncate">{entry.actor}{entry.actor_roles.length ? ` (${entry.actor_roles.map(roleLabel).join(", ")})` : ""}</span>
                    <ChevronDown className="size-4 text-muted-foreground transition-transform group-data-[state=open]:rotate-180" aria-hidden="true" />
                  </button>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <dl className="grid gap-2 bg-muted/30 px-4 py-3 text-sm sm:grid-cols-[10rem_minmax(0,1fr)]">
                    <dt className="text-muted-foreground">Target</dt><dd className="break-all">{entry.target_type}{entry.target_id ? ` ${entry.target_id}` : ""}</dd>
                    {entry.reason ? (<><dt className="text-muted-foreground">Reason</dt><dd>{entry.reason}</dd></>) : null}
                    {entry.before ? (<><dt className="text-muted-foreground">Before</dt><dd><pre className="overflow-x-auto whitespace-pre-wrap break-all font-mono text-xs">{JSON.stringify(entry.before, null, 2)}</pre></dd></>) : null}
                    {entry.after ? (<><dt className="text-muted-foreground">After</dt><dd><pre className="overflow-x-auto whitespace-pre-wrap break-all font-mono text-xs">{JSON.stringify(entry.after, null, 2)}</pre></dd></>) : null}
                    <dt className="text-muted-foreground">Reference</dt><dd className="font-mono text-xs">{entry.correlation_id}</dd>
                  </dl>
                </CollapsibleContent>
              </Collapsible>
            </li>
          ))}
        </ol>
      ) : null}
      {next ? <Button variant="secondary" className="self-center" onClick={() => void loadMore()} disabled={loadingMore}>{loadingMore ? "Loading..." : "Load older entries"}</Button> : null}
    </div>
  );
}
