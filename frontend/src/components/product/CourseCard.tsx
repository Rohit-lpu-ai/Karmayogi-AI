import { ArrowRight, BookOpen, Building2, Clock, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import type { CourseSummary } from "@/api/types";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { cleanName, DifficultyBadge, durationLabel } from "./competency";
import { ProgressBadge } from "./learning";

/** Catalogue card: what the course is, what it helps with, and - if recommended - why, in one line. */
export function CourseCard({ course, compact = false, className }: { course: CourseSummary; compact?: boolean; className?: string }) {
  const gap = course.addresses_your_gaps[0];
  const primary = course.competencies.filter((c) => c.relevance === "primary");
  const shown = (primary.length ? primary : course.competencies).slice(0, compact ? 1 : 2);
  const more = course.competencies.length - shown.length;
  const duration = durationLabel(course.duration_days);

  return (
    <Card as="article" className={cn("group relative flex h-full flex-col gap-3 p-5 transition-shadow hover:shadow-raised", course.recommendation && course.recommendation.rank <= 3 && "border-primary/35", className)}>
      <div className="flex flex-wrap items-center gap-2">
        {course.recommendation ? (
          course.recommendation.rank <= 3 ? (
            <Badge tone="primary">
              <Sparkles aria-hidden="true" />
              Top pick for you
            </Badge>
          ) : (
            <Badge tone="info">Matches your gaps</Badge>
          )
        ) : null}
        <DifficultyBadge difficulty={course.difficulty} />
        {course.your_progress && course.your_progress.status !== "not_started" ? <ProgressBadge status={course.your_progress.status} /> : null}
      </div>

      <h3 className="text-base font-semibold leading-snug text-foreground text-balance">
        <Link to={`/courses/${course.id}`} className="after:absolute after:inset-0 after:rounded-xl focus-visible:outline-none after:focus-visible:ring-2 after:focus-visible:ring-ring">
          {cleanName(course.title)}
        </Link>
      </h3>

      {!compact && course.description ? <p className="line-clamp-2 text-sm text-muted-foreground">{course.description}</p> : null}

      {gap ? (
        <p className="rounded-md bg-primary-soft/60 px-3 py-2 text-sm text-primary-soft-foreground">
          Helps close your gap in <span className="font-medium">{cleanName(gap.competency_name)}</span>
          {gap.estimated_level !== null ? ` (level ${gap.estimated_level} of ${gap.required_level} needed)` : ""}
        </p>
      ) : shown.length > 0 ? (
        <p className="text-sm text-muted-foreground">
          Builds <span className="font-medium text-foreground">{shown.map((c) => cleanName(c.competency.name)).join(", ")}</span>
          {more > 0 ? ` and ${more} more` : ""}
        </p>
      ) : null}

      <div className="mt-auto flex flex-wrap items-center justify-between gap-2 pt-1 text-sm text-muted-foreground">
        <span className="flex flex-wrap items-center gap-x-3 gap-y-1">
          {duration ? (
            <span className="inline-flex items-center gap-1">
              <Clock className="size-3.5" aria-hidden="true" />
              {duration}
            </span>
          ) : null}
          {course.lessons?.lesson_count ? (
            <span className="inline-flex items-center gap-1">
              <BookOpen className="size-3.5" aria-hidden="true" />
              {course.your_progress && course.your_progress.status !== "not_started"
                ? `${course.your_progress.completed_lessons} of ${course.lessons.lesson_count} lessons`
                : `${course.lessons.lesson_count} lessons`}
            </span>
          ) : null}
          <span className="inline-flex items-center gap-1">
            <Building2 className="size-3.5" aria-hidden="true" />
            {cleanName(course.provider_organisation)}
          </span>
        </span>
        <ArrowRight className="size-4 text-primary transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
      </div>
    </Card>
  );
}
