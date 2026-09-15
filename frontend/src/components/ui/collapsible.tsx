import * as CollapsiblePrimitive from "@radix-ui/react-collapsible";
import { ChevronDown } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export const Collapsible = CollapsiblePrimitive.Root;
export const CollapsibleTrigger = CollapsiblePrimitive.Trigger;
export const CollapsibleContent = CollapsiblePrimitive.Content;

/**
 * Progressive disclosure for secondary detail such as scoring methodology ("How was this calculated?").
 * The trigger is a native button with aria-expanded; content stays in the DOM order after it.
 */
export function Disclosure({
  title,
  children,
  defaultOpen = false,
  className,
}: {
  title: ReactNode;
  children: ReactNode;
  defaultOpen?: boolean;
  className?: string;
}) {
  return (
    <Collapsible defaultOpen={defaultOpen} className={cn("rounded-lg border border-border", className)}>
      <CollapsibleTrigger
        data-focus-ring=""
        className="group flex min-h-11 w-full items-center justify-between gap-3 rounded-lg px-4 py-2 text-left text-sm font-medium text-foreground hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        <span>{title}</span>
        <ChevronDown className="size-4 shrink-0 text-muted-foreground transition-transform group-data-[state=open]:rotate-180" aria-hidden="true" />
      </CollapsibleTrigger>
      <CollapsibleContent className="border-t border-border px-4 py-3 text-sm text-muted-foreground">{children}</CollapsibleContent>
    </Collapsible>
  );
}
