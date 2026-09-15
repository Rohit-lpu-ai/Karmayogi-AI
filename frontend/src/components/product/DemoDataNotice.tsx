import { ChevronDown, FlaskConical } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

/**
 * Persistent, non-dismissible notice that the environment uses synthetic data (DEC-045, baseline risk R-01).
 * Compact by default; details expand inline. There is exactly one on a page (role="note").
 */
export function DemoDataNotice({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div role="note" aria-label="Demo environment" className={cn("border-b border-demo/15 bg-demo-soft text-demo", className)}>
      <div className="mx-auto flex max-w-[var(--content-max)] flex-wrap items-center gap-x-3 gap-y-1 px-4 py-2 text-sm sm:px-6">
        <FlaskConical className="size-4 shrink-0" aria-hidden="true" />
        <p className="min-w-0 flex-1 basis-[calc(100%-2rem)] sm:basis-0">
          <span className="font-semibold">DEMO environment</span>
          <span className="sm:hidden"> - synthetic data, not official.</span>
          <span className="hidden sm:inline">
            {" "}
            - synthetic users and synthetic content. Nothing shown here is official data, and results are development guidance
            only, not an appraisal.
          </span>
        </p>
        <button
          type="button"
          data-focus-ring=""
          aria-expanded={open}
          onClick={() => setOpen((value) => !value)}
          className="-ml-2 inline-flex min-h-8 items-center gap-1 rounded-md px-2 font-medium sm:ml-0 underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          What does this mean?
          <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} aria-hidden="true" />
        </button>
      </div>
      {open ? (
        <div className="mx-auto max-w-[var(--content-max)] px-4 pb-3 text-sm sm:px-6">
          <ul className="list-disc space-y-1 pl-5">
            <li>Job roles, competencies, questions and courses marked DEMO were written for local testing.</li>
            <li>They are not official competency frameworks, approved courses or government assessment content.</li>
            <li>This platform is not connected to iGOT Karmayogi or any government system.</li>
            <li>Level thresholds are provisional and have not been statistically validated.</li>
          </ul>
        </div>
      ) : null}
    </div>
  );
}
