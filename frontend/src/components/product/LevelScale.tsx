import { cn } from "@/lib/utils";

/**
 * Competency level on a segmented scale with the required level marked. The same information is always written
 * out in text next to it; the graphic is supporting only (UI_UX_SPEC.md §5, §6 Charts).
 */
export function LevelScale({
  levels,
  estimated,
  required,
  label,
  className,
}: {
  levels: number;
  estimated: number | null;
  required?: number | null;
  label: string;
  className?: string;
}) {
  const summary = [
    estimated !== null ? `estimated level ${estimated} of ${levels}` : "no estimated level",
    required ? `required level ${required}` : null,
  ]
    .filter(Boolean)
    .join(", ");
  return (
    <div className={cn("w-full", className)} role="img" aria-label={`${label}: ${summary}`}>
      <div className="flex gap-1">
        {Array.from({ length: levels }, (_, index) => {
          const level = index + 1;
          const filled = estimated !== null && level <= estimated;
          const isRequired = required === level;
          return (
            <div key={level} className="relative flex-1">
              <div
                className={cn(
                  "h-2.5 rounded-sm",
                  filled ? (estimated !== null && required && estimated >= required ? "bg-success" : "bg-primary") : "bg-muted",
                  isRequired && !filled && "bg-muted outline outline-2 -outline-offset-2 outline-primary/50",
                )}
              />
            </div>
          );
        })}
      </div>
      <div className="mt-1 flex gap-1" aria-hidden="true">
        {Array.from({ length: levels }, (_, index) => {
          const level = index + 1;
          return (
            <span key={level} className={cn("flex-1 text-center text-xs tabular-nums", required === level ? "font-semibold text-foreground" : "text-muted-foreground")}>
              {required === level ? `${level} required` : level}
            </span>
          );
        })}
      </div>
    </div>
  );
}
