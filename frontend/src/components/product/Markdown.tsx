import { Fragment, type ReactNode } from "react";
import { cn } from "@/lib/utils";

/**
 * Renders the Markdown subset used by lesson bodies (Phase 4B): headings (## and ###), paragraphs, bullet and numbered
 * lists, tables, block quotes, horizontal rules, inline code blocks written with single backticks, bold and italics.
 *
 * Output is built from React elements only - there is no HTML parsing and no dangerouslySetInnerHTML - so any markup
 * inside a lesson is shown as text. Links and images are not supported by design: lesson content carries no
 * external references until source approval (no fabricated citations).
 */
export function Markdown({ source, className, headingOffset = 1 }: { source: string; className?: string; headingOffset?: number }) {
  return <div className={cn("lesson-prose", className)}>{parseBlocks(source, headingOffset)}</div>;
}

function inline(text: string, keyPrefix: string): ReactNode[] {
  const out: ReactNode[] = [];
  const pattern = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0;
  let match: RegExpExecArray | null;
  let i = 0;
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > last) out.push(text.slice(last, match.index));
    const token = match[0];
    const key = `${keyPrefix}-${i++}`;
    if (token.startsWith("`")) out.push(<code key={key}>{token.slice(1, -1)}</code>);
    else if (token.startsWith("**")) out.push(<strong key={key}>{token.slice(2, -2)}</strong>);
    else out.push(<em key={key}>{token.slice(1, -1)}</em>);
    last = match.index + token.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

function splitRow(line: string): string[] {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim());
}

function parseBlocks(source: string, headingOffset: number): ReactNode[] {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const blocks: ReactNode[] = [];
  let i = 0;
  let key = 0;

  const isBlank = (line: string | undefined) => line === undefined || line.trim() === "";
  const startsBlock = (line: string) =>
    /^#{2,3}\s/.test(line) || /^\s*[-*]\s+/.test(line) || /^\s*\d+\.\s+/.test(line) || line.startsWith("|") || line.startsWith(">") || /^---+\s*$/.test(line);

  while (i < lines.length) {
    const line = lines[i];
    if (isBlank(line)) {
      i++;
      continue;
    }
    const k = `b${key++}`;
    const heading = /^(#{2,3})\s+(.*)$/.exec(line);
    if (heading) {
      const level = Math.min(6, heading[1].length + headingOffset - 1);
      const Tag = `h${level}` as "h2" | "h3" | "h4";
      blocks.push(<Tag key={k}>{inline(heading[2], k)}</Tag>);
      i++;
    } else if (/^---+\s*$/.test(line)) {
      blocks.push(<hr key={k} />);
      i++;
    } else if (line.startsWith("|")) {
      const rows: string[] = [];
      while (i < lines.length && lines[i].startsWith("|")) rows.push(lines[i++]);
      const header = splitRow(rows[0]);
      const body = rows.slice(rows.length > 1 && /^\|?\s*:?-{2,}/.test(rows[1]) ? 2 : 1).map(splitRow);
      blocks.push(
        <div key={k} className="lesson-table" tabIndex={0} role="region" aria-label="Table">
          <table>
            <thead>
              <tr>{header.map((cell, c) => <th key={c} scope="col">{inline(cell, `${k}h${c}`)}</th>)}</tr>
            </thead>
            <tbody>
              {body.map((row, r) => (
                <tr key={r}>{row.map((cell, c) => <td key={c}>{inline(cell, `${k}r${r}c${c}`)}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>,
      );
    } else if (line.startsWith(">")) {
      const quote: string[] = [];
      while (i < lines.length && lines[i].startsWith(">")) quote.push(lines[i++].replace(/^>\s?/, ""));
      blocks.push(<blockquote key={k}><p>{inline(quote.join(" "), k)}</p></blockquote>);
    } else if (/^\s*[-*]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
      const ordered = /^\s*\d+\.\s+/.test(line);
      const items: string[] = [];
      while (i < lines.length && !isBlank(lines[i])) {
        const current = lines[i];
        if ((ordered ? /^\s*\d+\.\s+/ : /^\s*[-*]\s+/).test(current)) items.push(current.replace(ordered ? /^\s*\d+\.\s+/ : /^\s*[-*]\s+/, ""));
        else if (/^\s+\S/.test(current) && items.length) items[items.length - 1] += ` ${current.trim()}`; // wrapped item
        else break;
        i++;
      }
      const ListTag = ordered ? "ol" : "ul";
      blocks.push(<ListTag key={k}>{items.map((item, n) => <li key={n}>{inline(item, `${k}-${n}`)}</li>)}</ListTag>);
    } else if (/^`[^`]+`\s*$/.test(line.trim())) {
      blocks.push(<pre key={k}><code>{line.trim().slice(1, -1)}</code></pre>);
      i++;
    } else {
      const paragraph: string[] = [];
      while (i < lines.length && !isBlank(lines[i]) && !(paragraph.length && startsBlock(lines[i]))) paragraph.push(lines[i++].trim());
      blocks.push(<p key={k}>{paragraph.map((text, n) => <Fragment key={n}>{n ? " " : null}{inline(text, `${k}-${n}`)}</Fragment>)}</p>);
    }
  }
  return blocks;
}
