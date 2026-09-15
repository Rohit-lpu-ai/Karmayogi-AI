import { CheckCircle2, CircleDashed, CircleHelp, TrendingUp } from "lucide-react";
import type { ReactNode } from "react";
import type { CourseDifficulty, GapItem, GapStatus, Level } from "@/api/types";
import { Badge } from "@/components/ui/badge";

/**
 * Shared words and badges for competency status, so every screen describes the same state the same way
 * (UI_UX_SPEC.md §10: development-oriented language, never "weak" or "failed").
 */
export const STATUS_META: Record<GapStatus, { label: string; tone: "warning" | "success" | "info" | "neutral"; icon: ReactNode; short: string }> = {
  gap: { label: "Developing", tone: "warning", icon: <TrendingUp aria-hidden="true" />, short: "Below the required level" },
  meets_requirement: { label: "Meets requirement", tone: "success", icon: <CheckCircle2 aria-hidden="true" />, short: "At or above the required level" },
  insufficient_evidence: { label: "Reassess to confirm", tone: "info", icon: <CircleHelp aria-hidden="true" />, short: "Not enough evidence yet" },
  level_unavailable: { label: "Level not available", tone: "neutral", icon: <CircleDashed aria-hidden="true" />, short: "Thresholds not set up" },
  not_assessed: { label: "Not assessed yet", tone: "neutral", icon: <CircleDashed aria-hidden="true" />, short: "Take the baseline assessment" },
};

export function CompetencyStatusBadge({ status }: { status: GapStatus }) {
  const meta = STATUS_META[status];
  return (
    <Badge tone={meta.tone}>
      {meta.icon}
      {meta.label}
    </Badge>
  );
}

/** "Level 3 - Proficient" -> "Proficient"; falls back to "Level 3". */
export function levelName(levels: Level[] | undefined, number: number | null): string | null {
  if (number === null) return null;
  const level = levels?.find((l) => l.level_number === number);
  if (!level) return `Level ${number}`;
  const [, name] = level.label.split(/\s+-\s+/);
  return name ?? level.label;
}

export function gapSentence(item: GapItem): string {
  switch (item.status) {
    case "gap":
      return `${item.gap} level${item.gap === 1 ? "" : "s"} below what your role requires.`;
    case "meets_requirement":
      return "At or above what your role requires.";
    case "insufficient_evidence":
      return `Only ${item.evidence_count} question${item.evidence_count === 1 ? "" : "s"} measured this, so a gap cannot be confirmed yet.`;
    case "level_unavailable":
      return "A level could not be estimated because thresholds are not set up.";
    default:
      return "Not assessed yet. The baseline assessment will estimate your level.";
  }
}

const DIFFICULTY_LABEL: Record<CourseDifficulty, string> = {
  foundational: "Foundational",
  intermediate: "Intermediate",
  advanced: "Advanced",
};

export function DifficultyBadge({ difficulty }: { difficulty: CourseDifficulty | null | undefined }) {
  if (!difficulty) return null;
  const bars = difficulty === "foundational" ? 1 : difficulty === "intermediate" ? 2 : 3;
  return (
    <Badge tone="neutral" title="Difficulty">
      <span className="flex items-end gap-0.5" aria-hidden="true">
        {[1, 2, 3].map((n) => (
          <span key={n} className={`w-1 rounded-sm ${n <= bars ? "bg-foreground/70" : "bg-foreground/20"}`} style={{ height: `${4 + n * 3}px` }} />
        ))}
      </span>
      {DIFFICULTY_LABEL[difficulty]}
    </Badge>
  );
}

/**
 * Display name without the "DEMO - " prefix and "(synthetic ...)" suffix that the seed puts on every synthetic record.
 * Only use it where a DEMO badge or the demo notice labels the same content (DEC-045 labelling still holds).
 */
export function cleanName(name: string): string {
  return name.replace(/^DEMO - /, "").replace(/\s*\(synthetic[^)]*\)$/, "").trim();
}

export function durationLabel(days: number | null | undefined): string | null {
  if (!days) return null;
  return `${days} day${days === 1 ? "" : "s"}`;
}
