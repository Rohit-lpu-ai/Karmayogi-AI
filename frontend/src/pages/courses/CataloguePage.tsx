import { Search, SlidersHorizontal, X } from "lucide-react";
import { useEffect, useId, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import type { Catalogue } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName } from "@/components/product/competency";
import { CourseCard } from "@/components/product/CourseCard";
import { EmptyState, ErrorState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/form";
import { Skeleton } from "@/components/ui/skeleton";

const DURATIONS = [
  { value: "", label: "Any length" },
  { value: "1", label: "1 day" },
  { value: "2", label: "Up to 2 days" },
  { value: "3", label: "Up to 3 days" },
];
const SORTS = [
  { value: "recommended", label: "Recommended first" },
  { value: "title", label: "Title A-Z" },
  { value: "duration_asc", label: "Shortest first" },
  { value: "duration_desc", label: "Longest first" },
];

/** Course discovery (UI_UX_SPEC.md S-09, MVP-17). Filters live in the URL so a view can be shared and reloaded. */
export function CataloguePage() {
  const [params, setParams] = useSearchParams();
  const q = params.get("q") ?? "";
  const [draft, setDraft] = useState(q);
  const searchId = useId();
  const { user } = useAuth();
  const canLearn = Boolean(user?.can_take_assessments);

  // Debounce typing into the q parameter.
  useEffect(() => {
    const timer = window.setTimeout(() => {
      if (draft.trim() === q) return;
      const next = new URLSearchParams(params);
      if (draft.trim()) next.set("q", draft.trim());
      else next.delete("q");
      setParams(next, { replace: true });
    }, 300);
    return () => window.clearTimeout(timer);
  }, [draft, q, params, setParams]);

  const query = new URLSearchParams();
  for (const key of ["q", "competency_id", "difficulty", "max_days", "sort", "progress"]) {
    const value = params.get(key);
    if (value) query.set(key, value);
  }
  const catalogue = useApi<Catalogue>(`/api/v1/courses${query.toString() ? `?${query}` : ""}`);
  const filtersActive = ["q", "competency_id", "difficulty", "max_days", "progress"].some((k) => params.get(k));

  function setParam(key: string, value: string) {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    setParams(next, { replace: true });
  }

  function clearFilters() {
    setDraft("");
    const next = new URLSearchParams();
    if (params.get("sort")) next.set("sort", params.get("sort")!);
    setParams(next, { replace: true });
  }

  const data = catalogue.data;
  const recommendedCount = data?.items.filter((i) => i.recommendation).length ?? 0;

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Courses" }]}
        title="Course catalogue"
        description="Learning linked to the competencies in your role. Courses recommended for your gaps are marked and listed first."
        className="pb-0"
      />

      <Alert tone="demo">
        This catalogue currently contains synthetic learning examples for product evaluation. Official course integrations will be added after source approval.
      </Alert>

      <Card as="section" aria-label="Search and filter courses" className="p-4 sm:p-5">
        <div className={`grid gap-3 sm:grid-cols-2 lg:items-end ${canLearn ? "lg:grid-cols-[minmax(0,1.6fr)_repeat(5,minmax(0,1fr))]" : "lg:grid-cols-[minmax(0,1.6fr)_repeat(4,minmax(0,1fr))]"}`}>
          <div className="flex flex-col gap-1.5">
            <label htmlFor={`${searchId}-q`} className="text-sm font-medium">Search</label>
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
              <Input id={`${searchId}-q`} type="search" value={draft} onChange={(e) => setDraft(e.target.value)} placeholder="Title, topic or objective" className="pl-9" />
            </div>
          </div>
          <Select id={`${searchId}-competency`} label="Competency" value={params.get("competency_id") ?? ""} onChange={(v) => setParam("competency_id", v)}
            options={[{ value: "", label: "All competencies" }, ...(data?.filters.competencies ?? []).map((c) => ({ value: c.id, label: `${cleanName(c.name)} (${c.course_count})` }))]} />
          <Select id={`${searchId}-difficulty`} label="Difficulty" value={params.get("difficulty") ?? ""} onChange={(v) => setParam("difficulty", v)}
            options={[{ value: "", label: "Any difficulty" }, { value: "foundational", label: "Foundational" }, { value: "intermediate", label: "Intermediate" }, { value: "advanced", label: "Advanced" }]} />
          <Select id={`${searchId}-duration`} label="Duration" value={params.get("max_days") ?? ""} onChange={(v) => setParam("max_days", v)} options={DURATIONS} />
          {canLearn ? (
            <Select id={`${searchId}-progress`} label="Your progress" value={params.get("progress") ?? ""} onChange={(v) => setParam("progress", v)}
              options={[{ value: "", label: "Any progress" }, { value: "not_started", label: "Not started" }, { value: "in_progress", label: "In progress" }, { value: "completed", label: "Completed" }]} />
          ) : null}
          <Select id={`${searchId}-sort`} label="Sort by" value={params.get("sort") ?? "recommended"} onChange={(v) => setParam("sort", v === "recommended" ? "" : v)} options={SORTS} />
        </div>
      </Card>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <p role="status" aria-live="polite" className="text-sm text-muted-foreground">
          {catalogue.loading ? "Loading courses..." : data ? `${data.total} course${data.total === 1 ? "" : "s"}${data.has_learning_context && recommendedCount ? `, ${recommendedCount} linked to your gaps` : ""}` : ""}
        </p>
        {filtersActive ? (
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            <X aria-hidden="true" />
            Clear filters
          </Button>
        ) : null}
      </div>

      {catalogue.loading && !data ? (
        <ul className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-hidden="true">
          {Array.from({ length: 6 }, (_, i) => (
            <li key={i}><Card className="space-y-3 p-5"><Skeleton className="h-5 w-24" /><Skeleton className="h-5 w-4/5" /><Skeleton className="h-4 w-full" /><Skeleton className="h-4 w-2/3" /></Card></li>
          ))}
        </ul>
      ) : catalogue.error ? (
        <ErrorState error={catalogue.error} onRetry={catalogue.reload} />
      ) : data && data.items.length === 0 ? (
        <EmptyState
          title={filtersActive ? "No courses match these filters." : "No approved courses are available yet."}
          icon={<SlidersHorizontal className="size-5" />}
          action={filtersActive ? <Button variant="secondary" onClick={clearFilters}>Clear filters</Button> : null}
        >
          <p>{filtersActive ? "Try a broader search or remove a filter." : "Your training team has not published courses yet."}</p>
        </EmptyState>
      ) : data ? (
        <>
          {!data.has_learning_context ? (
            <p className="text-sm text-muted-foreground">
              Complete your <Link to="/assessment" className="font-medium text-primary underline-offset-4 hover:underline">baseline assessment</Link> to see which courses fit your gaps.
            </p>
          ) : null}
          <ul className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {data.items.map((course) => (
              <li key={course.id}><CourseCard course={course} /></li>
            ))}
          </ul>
        </>
      ) : null}
    </div>
  );
}

function Select({ id, label, value, onChange, options }: { id: string; label: string; value: string; onChange: (value: string) => void; options: { value: string; label: string }[] }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium">{label}</label>
      <select
        id={id}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        data-focus-ring=""
        className="h-11 w-full rounded-md border border-input bg-card px-3 text-base text-foreground focus-visible:border-ring focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );
}
