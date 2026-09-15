import { BookOpen, CheckCircle2, CircleDashed, ClipboardList, Clock, Lightbulb, PlayCircle } from "lucide-react";
import type { ContentOrigin, CourseProgress, LessonType, ProgressStatus } from "@/api/types";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

export const LESSON_TYPE: Record<LessonType, { label: string; icon: typeof BookOpen }> = {
  reading: { label: "Reading", icon: BookOpen },
  worked_example: { label: "Worked example", icon: Lightbulb },
  practice_check: { label: "Practice check", icon: ClipboardList },
};

export const PROGRESS_META: Record<ProgressStatus, { label: string; tone: "neutral" | "info" | "success" }> = {
  not_started: { label: "Not started", tone: "neutral" },
  in_progress: { label: "In progress", tone: "info" },
  completed: { label: "Completed", tone: "success" },
};

export function ProgressBadge({ status, className }: { status: ProgressStatus; className?: string }) {
  const meta = PROGRESS_META[status];
  return (
    <Badge tone={meta.tone} className={className}>
      {status === "completed" ? <CheckCircle2 aria-hidden="true" /> : status === "in_progress" ? <PlayCircle aria-hidden="true" /> : null}
      {meta.label}
    </Badge>
  );
}

/** Lesson status as an icon plus visually hidden text (colour and shape are never the only signal). */
export function LessonStatusIcon({ status, className }: { status: ProgressStatus; className?: string }) {
  return (
    <span className={cn("inline-flex shrink-0", className)}>
      {status === "completed" ? (
        <CheckCircle2 className="size-5 text-success" aria-hidden="true" />
      ) : status === "in_progress" ? (
        <PlayCircle className="size-5 text-info" aria-hidden="true" />
      ) : (
        <CircleDashed className="size-5 text-muted-foreground" aria-hidden="true" />
      )}
      <span className="sr-only">{PROGRESS_META[status].label}</span>
    </span>
  );
}

export function minutesLabel(minutes: number): string {
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return rest ? `${hours} h ${rest} min` : `${hours} h`;
}

export function MinutesBadge({ minutes }: { minutes: number }) {
  return (
    <Badge tone="neutral">
      <Clock aria-hidden="true" />
      {minutesLabel(minutes)}
    </Badge>
  );
}

export function CourseProgressBar({ progress, label, className }: { progress: CourseProgress; label: string; className?: string }) {
  return (
    <div className={cn("space-y-1.5", className)}>
      <div className="flex items-baseline justify-between gap-2 text-sm">
        <span className="font-medium">{progress.completed_lessons} of {progress.lesson_count} lessons</span>
        <span className="tabular-nums text-muted-foreground">{progress.percent}%</span>
      </div>
      <Progress value={progress.percent} label={label} valueText={`${progress.completed_lessons} of ${progress.lesson_count} lessons completed`}
        indicatorClassName={progress.status === "completed" ? "bg-success" : undefined} />
    </div>
  );
}

export const ORIGIN_LABEL: Record<ContentOrigin, string> = {
  synthetic: "Synthetic example content",
  official_source: "From an official source (awaiting review)",
  provider: "Provider content",
};
