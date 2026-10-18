"use client";
import { linkSource, addCell, type Notebook } from "@/lib/store";

// Import a ChatGPT export (conversations.json): each conversation becomes a "chat" source; the first user message
// becomes a cell that cites it, so a notebook can start from what you already asked.
export function importChatGPT(nb: Notebook, json: any[]) {
  let n = 0;
  for (const conv of json) {
    const msgs = Object.values(conv.mapping || {}).map((m: any) => m.message).filter((m: any) => m && m.author?.role === "user");
    const first = msgs.sort((a: any, b: any) => (a.create_time || 0) - (b.create_time || 0))[0];
    if (!first) continue;
    const text = (first.content?.parts || []).join(" ").slice(0, 500);
    addCell(nb.id, `> ${text}`);
    n++;
  }
  return n;
}
