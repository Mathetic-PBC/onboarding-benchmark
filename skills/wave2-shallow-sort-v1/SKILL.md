---
name: wave2-shallow-sort-v1
description: File each item in a batch under the person's categories, from a short sample of it.
---

# Shallow sort

You get:
- categories: the confirmed category list (id, name, description), including "other".
- items: a batch of about 50 records. Each has id, title, date, source, an optional hint (folder, project, label) and a snippet: a short sample of the item, with numbered units (messages, lines or pages).

For every item, decide which categories it belongs to. Every item gets an answer. Do not skip any.

Rules
- Judge from what the person wrote (their own messages, their own notes) more than from assistant replies, tool output or pasted logs.
- An item can belong to more than one category, or to none.
- Don't trust titles alone. "Notes", "Untitled" or "New chat" says nothing; read the snippet.
- A folder or project hint is strong evidence, but the snippet overrides it if they disagree.
- If it looks like real work but fits no category, assign "other" and propose a new category.
- If the snippet is too thin to decide, say so with needs_deeper_read and don't guess.
- Evidence quotes must be copied exactly from the snippet, with the unit index they came from.
- Confidence: 0.9+ clearly about it, 0.6–0.9 probably, below 0.6 unsure (set needs_deeper_read).

Return JSON only, one entry per item, in the order given:
{
  "results": [
    { "item_id": "...",
      "project_assignments": [
        { "project_id": "cat_...", "confidence": 0.0,
          "evidence": [ { "unit": "message", "index": 0, "quote": "exact text" } ] } ],
      "proposed_projects": [ { "name": "...", "description": "one line" } ],
      "summary": "one line on what the item is",
      "needs_deeper_read": false }
  ]
}
