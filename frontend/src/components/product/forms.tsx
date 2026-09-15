import { Eye, EyeOff } from "lucide-react";
import { forwardRef, useState, type InputHTMLAttributes } from "react";
import type { ApiError } from "@/api/client";
import { Input } from "@/components/ui/form";

export const PASSWORD_MIN_LENGTH = 12;
export const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
export const REGISTRATION_ID_RE = /^[A-Za-z0-9][A-Za-z0-9/-]{2,39}$/;

export type FieldErrors = Record<string, string | undefined>;

/** Password input with a show/hide toggle. The value is never logged or placed in the URL. */
export const PasswordInput = forwardRef<HTMLInputElement, Omit<InputHTMLAttributes<HTMLInputElement>, "type">>(
  ({ className, ...props }, ref) => {
    const [visible, setVisible] = useState(false);
    return (
      <div className="relative">
        <Input ref={ref} type={visible ? "text" : "password"} className={`pr-12 ${className ?? ""}`} {...props} />
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          aria-pressed={visible}
          data-focus-ring=""
          className="absolute right-1 top-1/2 flex size-9 -translate-y-1/2 items-center justify-center rounded-md text-muted-foreground hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          {visible ? <EyeOff className="size-4" aria-hidden="true" /> : <Eye className="size-4" aria-hidden="true" />}
          <span className="sr-only">Show password</span>
        </button>
      </div>
    );
  },
);
PasswordInput.displayName = "PasswordInput";

/** Maps server field errors (problem+json `errors`) onto form fields. */
export function serverFieldErrors(error: ApiError): FieldErrors {
  const out: FieldErrors = {};
  for (const item of error.fieldErrors) {
    const field = item.field.replace(/^body\./, "");
    out[field] = item.message;
  }
  return out;
}

/**
 * Error summary at the top of a form (GOV.UK pattern, UI_UX_SPEC.md §6): focusable, lists each problem as a link to
 * its field, or shows one request-level message.
 */
export const ErrorSummary = forwardRef<
  HTMLDivElement,
  { errors: FieldErrors; labels: Record<string, string>; problem?: { title: string; body?: string; reference?: string } | null }
>(({ errors, labels, problem }, ref) => {
  const entries = Object.entries(errors).filter((entry): entry is [string, string] => Boolean(entry[1]));
  if (!problem && entries.length === 0) return null;
  return (
    <div
      ref={ref}
      tabIndex={-1}
      role="alert"
      className="rounded-lg border border-danger/25 bg-danger-soft p-4 text-danger focus:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      {problem ? (
        <>
          <p className="font-semibold">{problem.title}</p>
          {problem.body ? <p className="mt-1 text-sm">{problem.body}</p> : null}
          {problem.reference ? (
            <p className="mt-1 text-xs">
              Reference: <code>{problem.reference}</code>
            </p>
          ) : null}
        </>
      ) : null}
      {entries.length ? (
        <>
          {problem ? null : <p className="font-semibold">There {entries.length === 1 ? "is a problem" : "are problems"} with the form</p>}
          <ul className="mt-1 list-disc pl-5 text-sm">
            {entries.map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`} className="underline">
                  {labels[field] ? `${labels[field]}: ` : ""}
                  {message}
                </a>
              </li>
            ))}
          </ul>
        </>
      ) : null}
    </div>
  );
});
ErrorSummary.displayName = "ErrorSummary";

export function describedBy(id: string, error?: string, hint = false): string | undefined {
  const ids = [hint ? `${id}-hint` : null, error ? `${id}-error` : null].filter(Boolean);
  return ids.length ? ids.join(" ") : undefined;
}
