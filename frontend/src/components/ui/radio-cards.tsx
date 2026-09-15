import type { InputHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

/**
 * A selectable card built on a native radio input, so arrow keys, Space and screen readers behave natively
 * (UI_UX_SPEC.md S-06: "options as native radio inputs"). Wrap a set in a <fieldset> with a <legend>.
 */
export function RadioCard({
  children,
  description,
  marker,
  className,
  ...inputProps
}: Omit<InputHTMLAttributes<HTMLInputElement>, "type" | "children"> & {
  children: ReactNode;
  description?: ReactNode;
  /** Short leading marker such as an option letter. */
  marker?: ReactNode;
}) {
  return (
    <label
      className={cn(
        "group relative flex min-h-14 cursor-pointer items-start gap-3 rounded-lg border border-input bg-card px-4 py-3 transition-colors",
        "hover:border-primary/60 hover:bg-primary-soft/40",
        "has-[:checked]:border-primary has-[:checked]:bg-primary-soft has-[:checked]:ring-1 has-[:checked]:ring-primary",
        "has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-ring has-[:focus-visible]:ring-offset-2",
        "has-[:disabled]:cursor-not-allowed has-[:disabled]:opacity-60",
        className,
      )}
    >
      <input
        type="radio"
        data-focus-ring=""
        className={cn(
          "peer mt-0.5 size-5 shrink-0 cursor-pointer appearance-none rounded-full border-2 border-input bg-card",
          "checked:border-primary checked:bg-primary checked:shadow-[inset_0_0_0_3px_var(--card)]",
          "focus-visible:outline-none disabled:cursor-not-allowed",
        )}
        {...inputProps}
      />
      {marker ? (
        <span
          className="flex size-6 shrink-0 items-center justify-center rounded-md bg-muted text-xs font-semibold text-muted-foreground group-has-[:checked]:bg-primary group-has-[:checked]:text-primary-foreground"
          aria-hidden="true"
        >
          {marker}
        </span>
      ) : null}
      <span className="min-w-0 flex-1">
        <span className="block text-base text-foreground">{children}</span>
        {description ? <span className="mt-0.5 block text-sm text-muted-foreground">{description}</span> : null}
      </span>
    </label>
  );
}
