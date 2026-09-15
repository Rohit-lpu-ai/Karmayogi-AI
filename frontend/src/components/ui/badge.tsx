import { cva, type VariantProps } from "class-variance-authority";
import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export const badgeVariants = cva(
  "inline-flex items-center gap-1 whitespace-nowrap rounded-full border px-2 py-0.5 text-xs font-medium leading-5 align-middle [&_svg]:size-3.5",
  {
    variants: {
      tone: {
        neutral: "border-border bg-muted text-muted-foreground",
        primary: "border-transparent bg-primary-soft text-primary-soft-foreground",
        success: "border-transparent bg-success-soft text-success",
        warning: "border-transparent bg-warning-soft text-warning",
        danger: "border-transparent bg-danger-soft text-danger",
        info: "border-transparent bg-info-soft text-info",
        demo: "border-demo/20 bg-demo-soft text-demo",
        ai: "border-transparent bg-ai-soft text-ai",
      },
    },
    defaultVariants: { tone: "neutral" },
  },
);

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

/** Badges always carry text; colour is never the only signal (UI_UX_SPEC.md §5). */
export function Badge({ className, tone, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ tone }), className)} {...props} />;
}
