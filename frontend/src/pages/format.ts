import type { GapItem } from "../api/types";

/** Scores are shown out of 100 with no false precision. They are estimates, not grades. */
export function formatScore(score: string | null): string {
  if (score === null) return "No score yet";
  return `${Math.round(Number(score) * 100)} / 100`;
}

export function bandLabel(band: string | null, count: number): string {
  if (!band) return "Not assessed";
  const labels: Record<string, string> = {
    insufficient: "Insufficient evidence",
    low: "Low evidence",
    medium: "Medium evidence",
    high: "High evidence",
  };
  return `${labels[band] ?? band} (${count} question${count === 1 ? "" : "s"})`;
}

/** Development-oriented wording (UI_UX_SPEC.md §10): never "weak", "failed" or "poor". */
export function gapStatusLabel(item: GapItem): string {
  switch (item.status) {
    case "gap":
      return `Developing - ${item.gap} level${item.gap === 1 ? "" : "s"} below the level required for your role`;
    case "meets_requirement":
      return "Strength - at or above the required level";
    case "insufficient_evidence":
      return "Reassess to confirm - not enough evidence yet";
    case "level_unavailable":
      return "Level not available - thresholds not configured";
    case "not_assessed":
      return "Not assessed yet";
  }
}
