"use client";
import type { Notebook } from "@/lib/store";

export function search(nb: Notebook, q: string) {
  const t = q.trim().toLowerCase();
  if (!t) return { cells: [], sources: [] };
  return {
    cells: nb.cells.filter((c) => c.text.toLowerCase().includes(t)),
    sources: nb.sources.filter((s) => (s.title + " " + s.ref).toLowerCase().includes(t)),
  };
}
