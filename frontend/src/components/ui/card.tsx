import { forwardRef, type HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export const Card = forwardRef<HTMLDivElement, HTMLAttributes<HTMLElement> & { as?: "div" | "section" | "article" | "li" }>(
  ({ className, as: Tag = "div", ...props }, ref) => (
    <Tag
      ref={ref as never}
      className={cn("rounded-xl border border-border bg-card text-card-foreground shadow-card", className)}
      {...props}
    />
  ),
);
Card.displayName = "Card";

export function CardHeader({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-col gap-1 p-5 pb-3", className)} {...props} />;
}

export function CardTitle({ className, as: Tag = "h2", ...props }: HTMLAttributes<HTMLHeadingElement> & { as?: "h2" | "h3" | "h4" }) {
  return <Tag className={cn("text-base font-semibold leading-snug", className)} {...props} />;
}

export function CardDescription({ className, ...props }: HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("text-sm text-muted-foreground", className)} {...props} />;
}

export function CardContent({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("px-5 pb-5", className)} {...props} />;
}

export function CardFooter({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-wrap items-center gap-3 border-t border-border px-5 py-4", className)} {...props} />;
}
