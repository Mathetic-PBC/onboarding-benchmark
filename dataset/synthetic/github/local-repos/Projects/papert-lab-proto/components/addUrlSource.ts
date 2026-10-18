"use client";
import { linkSource } from "@/lib/store";

// Paste a URL into a cell's source box -> a source card titled from the page <title> (via /api/title).
export async function addUrlSource(nbId: string, cellId: string, url: string) {
  let title = url;
  try {
    const r = await fetch(`/api/title?url=${encodeURIComponent(url)}`);
    if (r.ok) title = (await r.json()).title || url;
  } catch {}
  linkSource(nbId, cellId, { kind: "url", title, ref: url });
}
