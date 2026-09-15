import { Loader2, Plus, Save, Trash2 } from "lucide-react";
import { useRef, useState, type FormEvent } from "react";
import { api, ApiError } from "@/api/client";
import type { QuestionAuthoringOptions, QuestionDetail, SourceInput, SourceKind } from "@/api/adminTypes";
import { useApi } from "@/api/useApi";
import { ErrorSummary, describedBy, serverFieldErrors, type FieldErrors } from "@/components/product/forms";
import { ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field, Input, Textarea } from "@/components/ui/form";
import { Select } from "@/components/ui/select";

interface OptionDraft {
  text: string;
  is_correct: boolean;
}

const KIND_LABEL: Record<SourceKind, string> = {
  synthetic: "Synthetic scenario (invented for practice)",
  source_record: "Imported source document",
  external_reference: "Other published reference (author-provided)",
};

/**
 * Question form for new questions and new versions of a draft. Saving never sends a question to review; that is a
 * separate step with its own checks. Every save creates a new version, so reviewers always see exact content.
 */
export function QuestionEditor({ existing, onSaved, onCancel }: { existing?: QuestionDetail; onSaved: (q: QuestionDetail) => void; onCancel?: () => void }) {
  const options = useApi<QuestionAuthoringOptions>("/api/v1/admin/questions/options");
  const v = existing?.current_version;
  const [competencyId, setCompetencyId] = useState(v?.competency.id ?? "");
  const [difficulty, setDifficulty] = useState<string>(v?.difficulty ?? "foundational");
  const [stem, setStem] = useState(v?.stem ?? "");
  const [explanation, setExplanation] = useState(v?.explanation ?? "");
  const [answers, setAnswers] = useState<OptionDraft[]>(v?.options.map((o) => ({ text: o.text, is_correct: o.is_correct })) ?? [
    { text: "", is_correct: true }, { text: "", is_correct: false }, { text: "", is_correct: false }, { text: "", is_correct: false },
  ]);
  const [sources, setSources] = useState<SourceInput[]>(v?.sources.map((s) => ({
    source_kind: s.source_kind, source_record_id: s.source_record_id, title: s.title, publisher: s.publisher, url: s.url, locator: s.locator, note: s.note,
  })) ?? []);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  if (options.loading) return <LoadingState label="Loading form" lines={6} />;
  if (options.error) return <ErrorState error={options.error} onRetry={options.reload} />;
  const data = options.data!;
  const selectable = data.competencies.filter((c) => !c.restricted);

  function validate(): FieldErrors {
    const found: FieldErrors = {};
    if (!competencyId) found.competency_id = "Choose the competency this question gives evidence for.";
    if (stem.trim().length < 10) found.stem = "Write the question (at least 10 characters).";
    if (answers.some((a) => !a.text.trim())) found.options = "Fill in every answer option, or remove empty ones.";
    else if (answers.filter((a) => a.is_correct).length !== 1) found.options = "Mark exactly one option as correct.";
    if (explanation.trim().length < 10) found.explanation = "Explain why the correct answer is right.";
    sources.forEach((s, i) => {
      if (s.source_kind === "synthetic" && !(s.note ?? "").trim()) found[`source_${i}`] = "Say that the scenario and figures are invented.";
      if (s.source_kind === "source_record" && !s.source_record_id) found[`source_${i}`] = "Choose a source document.";
      if (s.source_kind === "external_reference" && !((s.title ?? "").trim() && (s.publisher ?? "").trim())) found[`source_${i}`] = "Give a title and publisher.";
      if (s.url && !/^https?:\/\/\S+$/.test(s.url)) found[`source_${i}`] = "Links must start with http:// or https://.";
    });
    return found;
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found = validate();
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSaving(true);
    const body = {
      competency_id: competencyId, difficulty, stem: stem.trim(), explanation: explanation.trim(),
      options: answers.map((a) => ({ text: a.text.trim(), is_correct: a.is_correct })),
      sources: sources.map((s) => ({ ...s, url: s.url || null, title: s.title || null, publisher: s.publisher || null, locator: s.locator || null, note: s.note || null })),
    };
    try {
      const saved = existing
        ? await api<QuestionDetail>(`/api/v1/admin/questions/${existing.id}`, { method: "PUT", body: { ...body, row_version: existing.row_version } })
        : await api<QuestionDetail>("/api/v1/admin/questions", { method: "POST", body });
      onSaved(saved);
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
      const fields = serverFieldErrors(apiError);
      setErrors(fields);
      setProblem({ title: "The question was not saved.", body: apiError.detail, reference: apiError.correlationId });
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    } finally {
      setSaving(false);
    }
  }

  const setAnswer = (index: number, patch: Partial<OptionDraft>) =>
    setAnswers((list) => list.map((a, i) => (i === index ? { ...a, ...patch } : patch.is_correct ? { ...a, is_correct: false } : a)));
  const setSource = (index: number, patch: Partial<SourceInput>) => setSources((list) => list.map((s, i) => (i === index ? { ...s, ...patch } : s)));

  return (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-6">
      <div className="empty:hidden">
        <ErrorSummary ref={summaryRef} errors={errors} problem={problem}
          labels={{ competency_id: "Competency", stem: "Question", options: "Answer options", explanation: "Explanation", sources: "Sources", ...Object.fromEntries(sources.map((_, i) => [`source_${i}`, `Source ${i + 1}`])) }} />
      </div>

      <Card className="grid gap-5 p-6 md:grid-cols-2">
        <Field id="competency_id" label="Competency" error={errors.competency_id}>
          <Select id="competency_id" value={competencyId} onChange={(e) => setCompetencyId(e.target.value)} aria-invalid={errors.competency_id ? true : undefined} aria-describedby={describedBy("competency_id", errors.competency_id)}>
            <option value="">Choose a competency</option>
            {selectable.map((c) => <option key={c.id} value={c.id}>{c.name} ({c.code})</option>)}
          </Select>
        </Field>
        <Field id="difficulty" label="Difficulty">
          <Select id="difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            {data.difficulties.map((d) => <option key={d} value={d} className="capitalize">{d[0].toUpperCase() + d.slice(1)}</option>)}
          </Select>
        </Field>
        {data.competencies.some((c) => c.restricted) ? (
          <p className="text-sm text-muted-foreground md:col-span-2">Competencies from licence-restricted frameworks are not listed: their definitions cannot be quoted until permission is confirmed.</p>
        ) : null}
        <div className="md:col-span-2">
          <Field id="stem" label="Question" hint="A short scenario with invented figures works well. One question on screen at a time for learners." error={errors.stem}>
            <Textarea id="stem" rows={4} value={stem} onChange={(e) => setStem(e.target.value)} aria-invalid={errors.stem ? true : undefined} aria-describedby={describedBy("stem", errors.stem, true)} />
          </Field>
        </div>
      </Card>

      <Card as="section" aria-labelledby="options-heading" className="p-6">
        <h2 id="options-heading" className="text-base font-semibold">Answer options</h2>
        <p className="mt-1 text-sm text-muted-foreground">3 to 5 options. Choose the one correct answer. Learners see options in a shuffled order.</p>
        {errors.options ? <p id="options-error" className="mt-2 text-sm font-medium text-danger">{errors.options}</p> : null}
        <fieldset id="options" className="mt-4 space-y-3" aria-describedby={errors.options ? "options-error" : undefined}>
          <legend className="sr-only">Answer options and the correct answer</legend>
          {answers.map((answer, index) => (
            <div key={index} className="flex items-center gap-3">
              <input type="radio" name="correct" id={`correct-${index}`} checked={answer.is_correct} onChange={() => setAnswer(index, { is_correct: true })}
                className="size-5 shrink-0 accent-[var(--primary)]" data-focus-ring="" />
              <label htmlFor={`correct-${index}`} className="sr-only">Option {index + 1} is correct</label>
              <label htmlFor={`option-${index}`} className="sr-only">Option {index + 1} text</label>
              <Input id={`option-${index}`} value={answer.text} onChange={(e) => setAnswer(index, { text: e.target.value })} placeholder={`Option ${index + 1}`} />
              <Button type="button" variant="ghost" size="icon" disabled={answers.length <= 3} onClick={() => setAnswers((list) => list.filter((_, i) => i !== index))} aria-label={`Remove option ${index + 1}`}>
                <Trash2 aria-hidden="true" />
              </Button>
            </div>
          ))}
        </fieldset>
        <Button type="button" variant="secondary" size="sm" className="mt-3" disabled={answers.length >= 5} onClick={() => setAnswers((list) => [...list, { text: "", is_correct: false }])}>
          <Plus aria-hidden="true" />
          Add option
        </Button>
        <div className="mt-5">
          <Field id="explanation" label="Explanation" hint="Shown to learners after they submit, where the assessment's feedback policy allows it." error={errors.explanation}>
            <Textarea id="explanation" rows={3} value={explanation} onChange={(e) => setExplanation(e.target.value)} aria-invalid={errors.explanation ? true : undefined} aria-describedby={describedBy("explanation", errors.explanation, true)} />
          </Field>
        </div>
      </Card>

      <Card as="section" aria-labelledby="sources-heading" className="p-6">
        <h2 id="sources-heading" className="text-base font-semibold">Source metadata</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Required before review. Say where the content comes from. References you add are shown as author-provided and unverified; they are never presented as official citations.
        </p>
        {sources.length === 0 ? <Alert tone="warning" className="mt-4">No source yet. You can save a draft, but it cannot be sent for review.</Alert> : null}
        <div className="mt-4 space-y-4">
          {sources.map((source, index) => (
            <fieldset key={index} id={`source_${index}`} className="grid gap-3 rounded-lg border border-border p-4 md:grid-cols-2" aria-describedby={errors[`source_${index}`] ? `source_${index}-error` : undefined}>
              <legend className="px-1 text-sm font-medium">Source {index + 1}</legend>
              <div className="md:col-span-2 flex items-end gap-2">
                <div className="flex-1">
                  <Field id={`source-kind-${index}`} label="Type">
                    <Select id={`source-kind-${index}`} value={source.source_kind} onChange={(e) => setSource(index, { source_kind: e.target.value as SourceKind })}>
                      {(Object.keys(KIND_LABEL) as SourceKind[]).map((k) => <option key={k} value={k}>{KIND_LABEL[k]}</option>)}
                    </Select>
                  </Field>
                </div>
                <Button type="button" variant="ghost" onClick={() => setSources((list) => list.filter((_, i) => i !== index))}>
                  <Trash2 aria-hidden="true" />
                  Remove
                </Button>
              </div>
              {source.source_kind === "synthetic" ? (
                <div className="md:col-span-2">
                  <Field id={`source-note-${index}`} label="Note">
                    <Input id={`source-note-${index}`} value={source.note ?? ""} onChange={(e) => setSource(index, { note: e.target.value })} placeholder="Invented scenario and figures written for practice." />
                  </Field>
                </div>
              ) : null}
              {source.source_kind === "source_record" ? (
                <>
                  <div className="md:col-span-2">
                    <Field id={`source-record-${index}`} label="Source document">
                      <Select id={`source-record-${index}`} value={source.source_record_id ?? ""} onChange={(e) => setSource(index, { source_record_id: e.target.value })}>
                        <option value="">Choose a document</option>
                        {data.source_records.map((r) => <option key={r.id} value={r.id}>{r.record_id}: {r.label}{r.verified ? "" : " (not yet verified)"}</option>)}
                      </Select>
                    </Field>
                  </div>
                  <Field id={`source-locator-${index}`} label="Page or section (optional)">
                    <Input id={`source-locator-${index}`} value={source.locator ?? ""} onChange={(e) => setSource(index, { locator: e.target.value })} />
                  </Field>
                  <p className="self-end text-xs text-muted-foreground">Do not copy text from licence-restricted documents into the question.</p>
                </>
              ) : null}
              {source.source_kind === "external_reference" ? (
                <>
                  <Field id={`source-title-${index}`} label="Title"><Input id={`source-title-${index}`} value={source.title ?? ""} onChange={(e) => setSource(index, { title: e.target.value })} /></Field>
                  <Field id={`source-publisher-${index}`} label="Publisher"><Input id={`source-publisher-${index}`} value={source.publisher ?? ""} onChange={(e) => setSource(index, { publisher: e.target.value })} /></Field>
                  <Field id={`source-url-${index}`} label="Link (optional)"><Input id={`source-url-${index}`} type="url" value={source.url ?? ""} onChange={(e) => setSource(index, { url: e.target.value })} /></Field>
                  <Field id={`source-loc-${index}`} label="Page or section (optional)"><Input id={`source-loc-${index}`} value={source.locator ?? ""} onChange={(e) => setSource(index, { locator: e.target.value })} /></Field>
                </>
              ) : null}
              {errors[`source_${index}`] ? <p id={`source_${index}-error`} className="md:col-span-2 text-sm font-medium text-danger">{errors[`source_${index}`]}</p> : null}
            </fieldset>
          ))}
        </div>
        <Button type="button" variant="secondary" size="sm" className="mt-3" disabled={sources.length >= 5}
          onClick={() => setSources((list) => [...list, { source_kind: "synthetic", note: "" }])}>
          <Plus aria-hidden="true" />
          Add source
        </Button>
      </Card>

      <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
        {onCancel ? <Button type="button" variant="ghost" onClick={onCancel}>Cancel</Button> : null}
        <Button type="submit" disabled={saving}>
          {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Save aria-hidden="true" />}
          {existing ? "Save as new version" : "Save draft"}
        </Button>
      </div>
    </form>
  );
}
