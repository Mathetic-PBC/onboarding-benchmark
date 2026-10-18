"use client";
import { useState } from "react";
import { useNotebooks, addCell } from "@/lib/store";
import { CellView } from "@/components/CellView";

export default function NotebookPage({ params }: { params: { id: string } }) {
  const nb = useNotebooks().find((n) => n.id === params.id);
  const [draft, setDraft] = useState("");
  if (!nb) return <main>Notebook not found</main>;
  return (
    <main>
      <h1>{nb.title}</h1>
      {nb.cells.map((c) => <CellView key={c.id} nb={nb} cell={c} />)}
      <textarea value={draft} onChange={(e) => setDraft(e.target.value)} placeholder="Write a thought (markdown)…" rows={3} style={{ width: "100%" }} />
      <button onClick={() => { addCell(nb.id, draft); setDraft(""); }} disabled={!draft.trim()}>Add</button>
    </main>
  );
}
