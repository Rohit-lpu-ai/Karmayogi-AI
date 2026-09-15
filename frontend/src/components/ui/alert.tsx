import { cva, type VariantProps } from "class-variance-authority";
import { AlertTriangle, CheckCircle2, Info, OctagonAlert, FlaskConical } from "lucide-react";
import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

const alertVariants = cva("relative flex gap-3 rounded-lg border p-4 text-sm [&>svg]:mt-0.5 [&>svg]:size-5 [&>svg]:shrink-0", {
  variants: {
    tone: {
      info: "border-info/20 bg-info-soft text-info",
      success: "border-success/20 bg-success-soft text-success",
      warning: "border-warning/25 bg-warning-soft text-warning",
      danger: "border-danger/25 bg-danger-soft text-danger",
      demo: "border-demo/20 bg-demo-soft text-demo",
      neutral: "border-border bg-muted text-foreground",
    },
  },
  defaultVariants: { tone: "info" },
});

const ICONS = { info: Info, success: CheckCircle2, warning: AlertTriangle, danger: OctagonAlert, demo: FlaskConical, neutral: Info };

export interface AlertProps extends Omit<HTMLAttributes<HTMLDivElement>, "title">, VariantProps<typeof alertVariants> {
  title?: ReactNode;
  icon?: boolean;
}

/**
 * Inline message. Pass role="alert" only for blocking errors and role="status" for polite updates (UI_UX_SPEC.md §6);
 * static notices need no live role.
 */
export function Alert({ className, tone = "info", title, icon = true, children, ...props }: AlertProps) {
  const Icon = ICONS[tone ?? "info"];
  return (
    <div className={cn(alertVariants({ tone }), className)} {...props}>
      {icon ? <Icon aria-hidden="true" /> : null}
      <div className="min-w-0 flex-1 space-y-1">
        {title ? <p className="font-semibold leading-snug">{title}</p> : null}
        {children ? <div className="leading-relaxed [&_a]:underline">{children}</div> : null}
      </div>
    </div>
  );
}
