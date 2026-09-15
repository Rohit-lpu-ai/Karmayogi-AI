import { Check } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

export type JourneyState = "done" | "current" | "next" | "later";

export interface JourneyStep {
  id: string;
  label: string;
  detail: string;
  state: JourneyState;
  to?: string;
}

/**
 * The learner loop (job role → requirements → baseline → gaps → learning → progress → reassessment) shown as a
 * sequence with the learner's position. Steps that are not in this release are marked "Later release" rather than
 * hidden, so the product's direction is visible without pretending the feature exists.
 */
export function LearnerJourney({ steps, className }: { steps: JourneyStep[]; className?: string }) {
  return (
    <nav aria-label="Your learning journey" className={className}>
      <ol className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7">
        {steps.map((step, index) => {
          const content = (
            <>
              <span className="flex items-center gap-2">
                <span
                  aria-hidden="true"
                  className={cn(
                    "flex size-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold tabular-nums",
                    step.state === "done" && "bg-success text-primary-foreground",
                    step.state === "current" && "bg-primary text-primary-foreground",
                    step.state === "next" && "border-2 border-primary text-primary",
                    step.state === "later" && "border border-dashed border-input text-muted-foreground",
                  )}
                >
                  {step.state === "done" ? <Check className="size-3.5" /> : index + 1}
                </span>
                <span className={cn("text-sm font-semibold", step.state === "later" ? "text-muted-foreground" : "text-foreground")}>{step.label}</span>
              </span>
              <span className="mt-1 block text-xs text-muted-foreground">
                <span className="sr-only">
                  {step.state === "done" ? "Done. " : step.state === "current" ? "Current step. " : step.state === "next" ? "Next. " : "Later release. "}
                </span>
                {step.detail}
              </span>
            </>
          );
          const base = cn(
            "block h-full rounded-lg border px-3 py-2.5",
            step.state === "current" ? "border-primary bg-primary-soft" : step.state === "later" ? "border-dashed border-border bg-transparent" : "border-border bg-card",
          );
          return (
            <li key={step.id} aria-current={step.state === "current" ? "step" : undefined}>
              {step.to && step.state !== "later" ? (
                <Link to={step.to} className={cn(base, "hover:border-primary/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring")}>
                  {content}
                </Link>
              ) : (
                <div className={base}>{content}</div>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
