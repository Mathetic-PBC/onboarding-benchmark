"use client";
import ReactMarkdown from "react-markdown";
import type { Cell, Notebook } from "@/lib/store";
import { TrailView } from "@/components/Trail";

export function CellView({ nb, cell }: { nb: Notebook; cell: Cell }) {
  const srcs = cell.sources.map((id) => nb.sources.find((s) => s.id === id)).filter(Boolean);
  return (
    <div className="cell">
      <ReactMarkdown>{cell.text}</ReactMarkdown>
      <div>{srcs.map((s) => <span key={s!.id} className="chip" title={s!.ref}>{s!.kind}: {s!.title}</span>)}</div>
      <TrailView nb={nb} cellId={cell.id} />
    </div>
  );
}
