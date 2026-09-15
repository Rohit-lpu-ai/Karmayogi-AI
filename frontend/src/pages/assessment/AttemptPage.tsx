import { AlertTriangle, ArrowLeft, ArrowRight, Check, CheckCircle2, CloudOff, Grid3x3, Loader2, LogOut, RotateCcw, Send } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, Navigate, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { Attempt, DeliveredQuestion, SubmitResponse } from "@/api/types";
import { useApi } from "@/api/useApi";
import { ConfirmationDialog } from "@/components/product/ConfirmationDialog";
import { DemoBadge, EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Progress } from "@/components/ui/progress";
import { RadioCard } from "@/components/ui/radio-cards";
import { toast } from "@/components/ui/toaster";
import { cn } from "@/lib/utils";

type SaveStatus = "saved" | "saving" | "error";

/**
 * Taking an attempt (UI_UX_SPEC.md S-06): one question at a time, question grid, server-saved answers,
 * confirmation before submitting. The server stays authoritative: answers are PUT on selection, scoring happens on submit.
 */
export function AttemptPage() {
  const { attemptId } = useParams();
  const attempt = useApi<Attempt>(attemptId ? `/api/v1/attempts/${attemptId}` : null);

  if (attempt.loading) {
    return (
      <Card className="mx-auto max-w-3xl p-6">
        <LoadingState label="Loading your assessment" lines={6} />
      </Card>
    );
  }
  if (attempt.error) {
    if (attempt.error.code === "ATTEMPT_VOIDED") {
      return (
        <EmptyState
          title="This attempt is no longer available."
          className="mx-auto max-w-2xl"
          action={<Button asChild><Link to="/assessment">Go to the assessment</Link></Button>}
        >
          <p>{attempt.error.detail}</p>
        </EmptyState>
      );
    }
    return <ErrorState className="mx-auto max-w-2xl" error={attempt.error} onRetry={attempt.reload} />;
  }
  if (!attempt.data) return null;
  if (attempt.data.status !== "in_progress") return <Navigate to={`/attempts/${attempt.data.id}/result`} replace />;
  return <AttemptRunner initial={attempt.data} />;
}

function AttemptRunner({ initial }: { initial: Attempt }) {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [questions, setQuestions] = useState<DeliveredQuestion[]>(() => [...initial.questions].sort((a, b) => a.position - b.position));
  const [saveStatus, setSaveStatus] = useState<Record<string, SaveStatus>>({});
  const [saveError, setSaveError] = useState<ApiError | null>(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<ApiError | null>(null);
  const latestRequest = useRef<Record<string, number>>({});
  const headingRef = useRef<HTMLHeadingElement>(null);
  const firstRender = useRef(true);

  const total = questions.length;
  // The starting question (first unanswered on resume) is fixed once, so answering never moves the learner.
  const [startIndex] = useState(() => Math.max(0, initial.questions.findIndex((q) => q.selected_option_id === null)));
  const requested = Number(searchParams.get("q"));
  const validRequest = Number.isInteger(requested) && requested >= 1 && requested <= total;
  const index = validRequest ? requested - 1 : startIndex;
  const question = questions[index];
  const answered = questions.filter((q) => q.selected_option_id !== null).length;
  const unansweredPositions = questions.filter((q) => q.selected_option_id === null).map((q) => q.position);
  const statuses = Object.values(saveStatus);
  const anySaving = statuses.includes("saving");
  const failed = questions.filter((q) => saveStatus[q.question_version_id] === "error");

  const goTo = useCallback(
    (next: number) => setSearchParams({ q: String(Math.min(Math.max(next, 0), total - 1) + 1) }, { replace: false }),
    [setSearchParams, total],
  );

  // Put the position in the URL so reload and browser back/forward keep the learner's place.
  useEffect(() => {
    if (!validRequest) setSearchParams({ q: String(startIndex + 1) }, { replace: true });
  }, [validRequest, startIndex, setSearchParams]);

  // Move focus to the question heading when the question changes (not on first load).
  useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false;
      return;
    }
    headingRef.current?.focus();
  }, [index]);

  // Warn before closing or reloading the tab while an answer is not yet stored on the server.
  useEffect(() => {
    if (!anySaving && failed.length === 0) return;
    const handler = (event: BeforeUnloadEvent) => {
      event.preventDefault();
      event.returnValue = "";
    };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, [anySaving, failed.length]);

  async function saveAnswer(questionVersionId: string, optionId: string | null) {
    const token = (latestRequest.current[questionVersionId] ?? 0) + 1;
    latestRequest.current[questionVersionId] = token;
    setQuestions((current) => current.map((q) => (q.question_version_id === questionVersionId ? { ...q, selected_option_id: optionId } : q)));
    setSaveStatus((current) => ({ ...current, [questionVersionId]: "saving" }));
    setSaveError(null);
    try {
      await api(`/api/v1/attempts/${initial.id}/answers/${questionVersionId}`, { method: "PUT", body: { selected_option_id: optionId } });
      if (latestRequest.current[questionVersionId] === token) setSaveStatus((current) => ({ ...current, [questionVersionId]: "saved" }));
    } catch (err) {
      if (latestRequest.current[questionVersionId] !== token) return;
      // Keep the learner's choice on screen (held in memory only) and offer a retry (S-06 error state).
      setSaveStatus((current) => ({ ...current, [questionVersionId]: "error" }));
      setSaveError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Not saved", "Your answer was not saved."));
    }
  }

  function retryFailed() {
    for (const q of failed) void saveAnswer(q.question_version_id, q.selected_option_id);
  }

  async function submit() {
    setSubmitting(true);
    setSubmitError(null);
    try {
      const result = await api<SubmitResponse>(`/api/v1/attempts/${initial.id}/submit`, { method: "POST" });
      navigate(`/attempts/${result.attempt_id}/result`, { replace: true });
    } catch (err) {
      const error = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Submission failed", "Your answers were not submitted. Try again.");
      if (error.code === "ATTEMPT_NOT_IN_PROGRESS") {
        navigate(`/attempts/${initial.id}/result`, { replace: true });
        return;
      }
      setSubmitError(error);
      setSubmitting(false);
      setConfirmOpen(false);
    }
  }

  const saveLabel = anySaving ? "Saving..." : failed.length > 0 ? "Not saved" : Object.keys(saveStatus).length > 0 ? "All answers saved" : "Answers save automatically";

  const grid = useMemo(
    () => (
      <QuestionGrid
        questions={questions}
        currentIndex={index}
        saveStatus={saveStatus}
        onSelect={(i) => goTo(i)}
      />
    ),
    [questions, index, saveStatus, goTo],
  );

  if (!question) return null;
  const isLast = index === total - 1;
  const currentStatus = saveStatus[question.question_version_id];

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-5">
      {/* Assessment header: title, position, progress and save state */}
      <Card className="p-4 sm:p-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="min-w-0 space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge tone="primary">Baseline assessment</Badge>
              {initial.assessment.is_demo ? <DemoBadge /> : null}
            </div>
            <p className="truncate text-base font-semibold text-foreground" title={initial.assessment.title}>
              {initial.assessment.title}
            </p>
          </div>
          <Button
            variant="ghost"
            className="self-start"
            onClick={() => {
              toast.success("Your answers are saved", { description: "Resume the assessment any time from the Baseline assessment page." });
              navigate("/assessment");
            }}
            disabled={anySaving || failed.length > 0}
          >
            <LogOut aria-hidden="true" />
            Save and exit
          </Button>
        </div>
        <div className="mt-4 space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2 text-sm">
            <span className="font-medium text-foreground">
              {answered} of {total} answered
            </span>
            <span
              role="status"
              aria-live="polite"
              className={cn("inline-flex items-center gap-1.5", failed.length > 0 ? "font-medium text-danger" : "text-muted-foreground")}
            >
              {anySaving ? <Loader2 className="size-4 animate-spin" aria-hidden="true" /> : failed.length > 0 ? <CloudOff className="size-4" aria-hidden="true" /> : <Check className="size-4" aria-hidden="true" />}
              {saveLabel}
            </span>
          </div>
          <Progress value={(answered / Math.max(total, 1)) * 100} label="Assessment progress" valueText={`${answered} of ${total} questions answered`} />
        </div>
      </Card>

      {failed.length > 0 ? (
        <Alert tone="danger" role="alert" title={`${failed.length === 1 ? "An answer was" : `${failed.length} answers were`} not saved`}>
          <p>
            {saveError?.detail ?? "Check your connection."} Your choice is still selected on this page.{" "}
            {saveError?.correlationId ? <>Reference: <code>{saveError.correlationId}</code>.</> : null}
          </p>
          <Button variant="secondary" size="sm" className="mt-2" onClick={retryFailed}>
            <RotateCcw aria-hidden="true" /> Retry saving
          </Button>
        </Alert>
      ) : null}

      {/* Mobile and tablet: question grid in a collapsible panel */}
      <Collapsible className="lg:hidden">
        <Card className="overflow-hidden">
          <CollapsibleTrigger
            data-focus-ring=""
            className="group flex min-h-12 w-full items-center justify-between gap-3 px-4 text-left text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-ring"
          >
            <span className="flex items-center gap-2">
              <Grid3x3 className="size-4 text-primary" aria-hidden="true" />
              All questions
              <span className="text-muted-foreground">({unansweredPositions.length} unanswered)</span>
            </span>
            <span className="text-primary group-data-[state=open]:hidden">Show</span>
            <span className="hidden text-primary group-data-[state=open]:inline">Hide</span>
          </CollapsibleTrigger>
          <CollapsibleContent className="border-t border-border p-4">{grid}</CollapsibleContent>
        </Card>
      </Collapsible>

      <div className="grid items-start gap-5 lg:grid-cols-[minmax(0,1fr)_18rem]">
        <Card as="section" aria-labelledby="question-heading" className="overflow-hidden">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border px-5 py-4 sm:px-8">
            <h1 ref={headingRef} id="question-heading" tabIndex={-1} className="text-sm font-semibold uppercase tracking-wide text-primary focus:outline-none">
              Question {index + 1} of {total}
            </h1>
            <div className="flex flex-wrap items-center gap-2">
              <Badge tone="neutral">{question.competency.name}</Badge>
              {question.is_demo ? <DemoBadge label="DEMO item" /> : null}
            </div>
          </div>

          <fieldset className="px-5 py-6 sm:px-8 sm:py-8" disabled={submitting}>
            <legend className="float-left mb-6 w-full text-xl font-semibold leading-snug text-foreground text-pretty sm:text-2xl">
              {question.stem}
            </legend>
            <div className="clear-both space-y-3">
              {question.options.map((option, optionIndex) => (
                <RadioCard
                  key={option.id}
                  name={`q-${question.question_version_id}`}
                  value={option.id}
                  marker={String.fromCharCode(65 + optionIndex)} // letters follow the delivered (shuffled) order
                  checked={question.selected_option_id === option.id}
                  onChange={() => void saveAnswer(question.question_version_id, option.id)}
                >
                  {option.text}
                </RadioCard>
              ))}
            </div>
            <div className="mt-4 flex min-h-9 flex-wrap items-center justify-between gap-2 text-sm">
              <span className="text-muted-foreground" aria-hidden="true">
                {question.selected_option_id === null
                  ? "Not answered yet"
                  : currentStatus === "saving"
                    ? "Saving your answer..."
                    : currentStatus === "error"
                      ? "Answer not saved"
                      : "Answer saved"}
              </span>
              {question.selected_option_id !== null ? (
                <Button variant="link" size="sm" onClick={() => void saveAnswer(question.question_version_id, null)}>
                  Clear answer
                </Button>
              ) : null}
            </div>
          </fieldset>

          <div className="flex items-center justify-between gap-3 border-t border-border bg-muted/30 px-5 py-4 sm:px-8">
            <Button variant="secondary" onClick={() => goTo(index - 1)} disabled={index === 0}>
              <ArrowLeft aria-hidden="true" />
              Previous
            </Button>
            {isLast ? (
              <Button onClick={() => setConfirmOpen(true)} disabled={submitting}>
                Review and submit
                <Send aria-hidden="true" />
              </Button>
            ) : (
              <Button onClick={() => goTo(index + 1)}>
                Next
                <ArrowRight aria-hidden="true" />
              </Button>
            )}
          </div>
        </Card>

        <aside className="hidden lg:block" aria-label="Question overview">
          <Card className="sticky top-24 p-5">
            <h2 className="text-base font-semibold">Questions</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              {answered} answered · {unansweredPositions.length} unanswered
            </p>
            <div className="mt-4">{grid}</div>
            <Button variant="secondary" className="mt-5 w-full" onClick={() => setConfirmOpen(true)} disabled={submitting}>
              Review and submit
            </Button>
          </Card>
        </aside>
      </div>

      {submitError ? <ErrorState error={submitError} /> : null}

      <ConfirmationDialog
        open={confirmOpen}
        onOpenChange={setConfirmOpen}
        title="Submit your answers?"
        description="You cannot change your answers after submitting. Your result appears straight away."
        confirmLabel="Submit answers"
        busy={submitting}
        busyLabel="Submitting..."
        onConfirm={() => void submit()}
      >
        <div className="space-y-3">
          <p className="flex items-center gap-2 font-medium">
            <CheckCircle2 className="size-5 text-success" aria-hidden="true" />
            {answered} of {total} questions answered
          </p>
          {unansweredPositions.length > 0 ? (
            <div className="rounded-lg border border-warning/30 bg-warning-soft p-3 text-warning">
              <p className="flex items-start gap-2 font-medium">
                <AlertTriangle className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
                {unansweredPositions.length} unanswered question{unansweredPositions.length === 1 ? "" : "s"} will be counted as not correct.
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {unansweredPositions.slice(0, 6).map((position) => (
                  <Button
                    key={position}
                    size="sm"
                    variant="secondary"
                    onClick={() => {
                      setConfirmOpen(false);
                      goTo(position - 1);
                    }}
                  >
                    Go to question {position}
                  </Button>
                ))}
                {unansweredPositions.length > 6 ? (
                  <span className="self-center text-sm">and {unansweredPositions.length - 6} more (see the question grid)</span>
                ) : null}
              </div>
            </div>
          ) : null}
          {anySaving || failed.length > 0 ? (
            <p className="font-medium text-danger">Wait until every answer is saved before submitting.</p>
          ) : null}
        </div>
      </ConfirmationDialog>
    </div>
  );
}

function QuestionGrid({
  questions,
  currentIndex,
  saveStatus,
  onSelect,
}: {
  questions: DeliveredQuestion[];
  currentIndex: number;
  saveStatus: Record<string, SaveStatus>;
  onSelect: (index: number) => void;
}) {
  return (
    <div>
      <ol className="grid grid-cols-5 gap-2">
        {questions.map((q, i) => {
          const isAnswered = q.selected_option_id !== null;
          const isCurrent = i === currentIndex;
          const failed = saveStatus[q.question_version_id] === "error";
          const state = failed ? "answer not saved" : isAnswered ? "answered" : "not answered";
          return (
            <li key={q.question_version_id}>
              <button
                type="button"
                data-focus-ring=""
                onClick={() => onSelect(i)}
                aria-current={isCurrent ? "step" : undefined}
                aria-label={`Question ${i + 1}, ${state}${isCurrent ? ", current" : ""}`}
                className={cn(
                  "relative flex h-11 w-full items-center justify-center rounded-md border-2 text-sm font-semibold tabular-nums transition-colors",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
                  isAnswered ? "border-primary bg-primary text-primary-foreground hover:bg-primary-hover" : "border-input bg-card text-foreground hover:bg-muted",
                  failed && "border-danger bg-danger-soft text-danger",
                  isCurrent && "ring-2 ring-primary ring-offset-2",
                )}
              >
                {i + 1}
                {isAnswered && !failed ? <Check className="absolute right-0.5 top-0.5 size-3" aria-hidden="true" /> : null}
              </button>
            </li>
          );
        })}
      </ol>
      <ul className="mt-4 flex flex-wrap gap-x-4 gap-y-1.5 text-xs text-muted-foreground" aria-label="Legend">
        <li className="flex items-center gap-1.5">
          <span className="size-3 rounded-sm bg-primary" aria-hidden="true" /> Answered
        </li>
        <li className="flex items-center gap-1.5">
          <span className="size-3 rounded-sm border-2 border-input" aria-hidden="true" /> Not answered
        </li>
        <li className="flex items-center gap-1.5">
          <span className="size-3 rounded-sm ring-2 ring-primary ring-offset-1" aria-hidden="true" /> Current
        </li>
      </ul>
    </div>
  );
}
