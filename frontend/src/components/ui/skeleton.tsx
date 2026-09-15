import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

/** Decorative placeholder shaped like the content. Pair with a visually hidden status label. */
export function Skeleton({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div aria-hidden="true" className={cn("animate-pulse rounded-md bg-muted", className)} {...props} />;
}
