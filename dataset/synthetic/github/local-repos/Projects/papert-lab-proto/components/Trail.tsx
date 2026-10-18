"use client";
import type { Notebook } from "@/lib/store";

// Walk back from a cell through the cells and sources it cites ("where did this thought come from").
export function trail(nb: Notebook, cellId: string, depth = 0, seen = new Set<string>()): string[] {
  // two cells citing each other used to recurse forever (2026-02-10)
  if (seen.has(cellId)) return [`${"  ".repeat(depth)}(cycle)`];
  seen.add(cellId);
  const c = nb.cells.find((x) => x.id === cellId);
  if (!c) return [];
  const out: string[] = [];
  for (const sid of c.sources) {
    const s = nb.sources.find((x) => x.id === sid);
    if (!s) continue;
    out.push(`${"  ".repeat(depth)}${s.kind}: ${s.title}`);
    if (s.kind === "cell") out.push(...trail(nb, s.ref, depth + 1, seen));
  }
  return out;
}

export function TrailView({ nb, cellId }: { nb: Notebook; cellId: string }) {
  const lines = trail(nb, cellId);
  if (!lines.length) return null;
  return <pre className="trail">{lines.join("\n")}</pre>;
}
