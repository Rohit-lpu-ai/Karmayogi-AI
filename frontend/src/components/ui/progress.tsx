import * as ProgressPrimitive from "@radix-ui/react-progress";
import { cn } from "@/lib/utils";

export interface ProgressProps {
  /** 0-100 */
  value: number;
  /** Accessible name, e.g. "Assessment progress". */
  label: string;
  /** Text alternative for assistive technology, e.g. "4 of 10 questions answered". */
  valueText?: string;
  className?: string;
  indicatorClassName?: string;
}

export function Progress({ value, label, valueText, className, indicatorClassName }: ProgressProps) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <ProgressPrimitive.Root
      value={clamped}
      aria-label={label}
      aria-valuetext={valueText}
      className={cn("relative h-2 w-full overflow-hidden rounded-full bg-muted", className)}
    >
      <ProgressPrimitive.Indicator
        className={cn("h-full rounded-full bg-primary transition-[width] duration-300", indicatorClassName)}
        style={{ width: `${clamped}%` }}
      />
    </ProgressPrimitive.Root>
  );
}
