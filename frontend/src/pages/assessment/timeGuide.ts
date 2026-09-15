/**
 * A rough reading-and-thinking guide derived only from the number of questions (1-2 minutes each).
 * The API has no duration field, so this is presented as guidance, never as a measured or official figure.
 */
export function questionTimeGuide(questionCount: number): string {
  if (questionCount <= 0) return "Rough guide: a few minutes";
  const low = Math.max(1, questionCount);
  const high = Math.max(2, questionCount * 2);
  return `Rough guide: ${low}-${high} minutes`;
}
