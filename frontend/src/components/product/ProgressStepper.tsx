import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

export interface Step {
  id: string;
  label: string;
}

/**
 * Progress through a fixed sequence (UI_UX_SPEC.md S-02: "stepper announces current step").
 * Display only: moving between steps happens through the page's own buttons.
 */
export function ProgressStepper({ steps, current, className }: { steps: Step[]; current: number; className?: string }) {
  return (
    <nav aria-label="Progress" className={className}>
      <p className="mb-3 text-sm font-medium text-muted-foreground sm:hidden">
        Step {current + 1} of {steps.length}: <span className="text-foreground">{steps[current]?.label}</span>
      </p>
      <ol className="flex items-center gap-2 sm:gap-3">
        {steps.map((step, index) => {
          const state = index < current ? "complete" : index === current ? "current" : "upcoming";
          return (
            <li key={step.id} className="flex min-w-0 flex-1 items-center gap-2 sm:gap-3" aria-current={state === "current" ? "step" : undefined}>
              <span
                className={cn(
                  "flex size-8 shrink-0 items-center justify-center rounded-full border-2 text-sm font-semibold",
                  state === "complete" && "border-primary bg-primary text-primary-foreground",
                  state === "current" && "border-primary bg-card text-primary",
                  state === "upcoming" && "border-input bg-card text-muted-foreground",
                )}
                aria-hidden="true"
              >
                {state === "complete" ? <Check className="size-4" /> : index + 1}
              </span>
              <span className={cn("hidden truncate text-sm sm:block", state === "current" ? "font-semibold text-foreground" : "text-muted-foreground")}>
                <span className="sr-only">{state === "complete" ? "Completed: " : state === "current" ? "Current step: " : "Upcoming: "}</span>
                {step.label}
              </span>
              <span className="sr-only sm:hidden">
                {state === "complete" ? "Completed: " : state === "current" ? "Current step: " : "Upcoming: "}
                {step.label}
              </span>
              {index < steps.length - 1 ? (
                <span className={cn("h-0.5 min-w-3 flex-1 rounded-full", index < current ? "bg-primary" : "bg-border")} aria-hidden="true" />
              ) : null}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
