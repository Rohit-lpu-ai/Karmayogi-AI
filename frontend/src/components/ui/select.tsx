import { ChevronDown } from "lucide-react";
import { forwardRef, type InputHTMLAttributes, type SelectHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

/** Native select styled like Input: full keyboard, screen-reader and mobile picker support with no extra dependency. */
export const Select = forwardRef<HTMLSelectElement, SelectHTMLAttributes<HTMLSelectElement>>(({ className, children, ...props }, ref) => (
  <div className="relative">
    <select
      ref={ref}
      data-focus-ring=""
      className={cn(
        "flex h-11 w-full appearance-none rounded-md border border-input bg-card pl-3 pr-10 text-base text-foreground",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:border-ring",
        "disabled:cursor-not-allowed disabled:opacity-60 aria-[invalid=true]:border-danger",
        className,
      )}
      {...props}
    >
      {children}
    </select>
    <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
  </div>
));
Select.displayName = "Select";

export const Checkbox = forwardRef<HTMLInputElement, Omit<InputHTMLAttributes<HTMLInputElement>, "type">>(({ className, ...props }, ref) => (
  <input
    ref={ref}
    type="checkbox"
    data-focus-ring=""
    className={cn(
      "size-5 shrink-0 cursor-pointer rounded border-input accent-[var(--primary)]",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60",
      className,
    )}
    {...props}
  />
));
Checkbox.displayName = "Checkbox";
