import { forwardRef, type InputHTMLAttributes, type LabelHTMLAttributes, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    data-focus-ring=""
    className={cn(
      "flex h-11 w-full rounded-md border border-input bg-card px-3 text-base text-foreground placeholder:text-muted-foreground",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-ring",
      "disabled:cursor-not-allowed disabled:opacity-60 aria-[invalid=true]:border-danger",
      className,
    )}
    {...props}
  />
));
Input.displayName = "Input";

export function Label({ className, ...props }: LabelHTMLAttributes<HTMLLabelElement>) {
  return <label className={cn("text-sm font-medium text-foreground", className)} {...props} />;
}

/** Label, control, hint and inline error wired together with ids (UI_UX_SPEC.md §6 Forms). */
export function Field({
  id,
  label,
  hint,
  error,
  children,
}: {
  id: string;
  label: ReactNode;
  hint?: ReactNode;
  error?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <Label htmlFor={id}>{label}</Label>
      {hint ? (
        <p id={`${id}-hint`} className="text-sm text-muted-foreground">
          {hint}
        </p>
      ) : null}
      {children}
      {error ? (
        <p id={`${id}-error`} className="text-sm font-medium text-danger">
          {error}
        </p>
      ) : null}
    </div>
  );
}
