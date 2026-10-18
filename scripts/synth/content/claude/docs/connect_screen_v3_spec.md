# Connect screen v3 (spec, 2026-09-16)

## Purpose
First screen after signup. The user picks the tools their research lives in. Imports start immediately and keep running in the background.

## Header
**Connect your sources**
Every item keeps a link back to where it came from.

## Groups (v3)
- AI chats: Claude, ChatGPT
- Papers: Zotero, local PDF folder
- Notes: Obsidian, Google Docs
- More sources: Gmail (labels you choose), Slack (channels you pick), Google Drive (folders you pick), local folder

Open question: "More sources" replaced "Other" on 2026-09-15. Revisit after pilots (log whether users open it and what they look for).

## Per-source row
- Logo, name, one helper line (what we import / what we don't), time estimate range.
- Button states: `Connect` → `Importing… N items` → `Connected · N items` (+ `View`), or `Connected · N items · K skipped` with K clickable.

## Page footer
`Continue to notebook` is always enabled. Line under it: "Imports keep running in the background."

## Not in v3
- Notion, Granola, Overleaf connectors.
- Browser-session import for Claude (export zip only in the UI).
- Privacy line (to decide).
