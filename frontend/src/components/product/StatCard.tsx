import type { ReactNode } from "react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

/**
 * One headline figure with its meaning in words. Only show values the API returned;
 * never derive performance metrics in the browser (baseline audit R-02).
 */
export function StatCard({
  label,
  value,
  description,
  icon,
  className,
}: {
  label: string;
  value: ReactNode;
  description?: ReactNode;
  icon?: ReactNode;
  className?: string;
}) {
  return (
    <Card className={cn("flex flex-col gap-2 p-5", className)}>
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-medium text-muted-foreground">{label}</p>
        {icon ? (
          <span className="text-muted-foreground [&_svg]:size-4" aria-hidden="true">
            {icon}
          </span>
        ) : null}
      </div>
      <p className="text-2xl font-semibold tabular-nums text-foreground">{value}</p>
      {description ? <p className="text-sm text-muted-foreground">{description}</p> : null}
    </Card>
  );
}
