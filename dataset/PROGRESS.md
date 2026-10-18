# PROGRESS

Reference date: 2026-10-17. Person (authentic): David Barron (dbarron410@vt.edu), macOS user `divadbaroon`.
Check this file before starting any tool. Status values: TODO, IN PROGRESS, DONE, DONE (rechecked), BLOCKED (see FAILURES.md).

## Phase 1 — authentic

| tool | status | notes |
|---|---|---|
| obsidian | DONE (rechecked) | 2 vaults from obsidian.json (Obsidian Vault 8 files, mathetic 23 files); no other .obsidian dirs found |
| notion | BLOCKED | not signed in; logged |
| apple-notes | DONE (rechecked) | 27/27 notes (AppleScript count = 27), iCloud account, folders Notes + Engelbart |
| onenote | BLOCKED | not signed in (SSO needed); logged |
| google-docs | IN PROGRESS | dbarron410@vt.edu Drive via connector listing + docs.google.com exports (1,130 native docs/sheets/slides/drawings) + connector downloads (90 binaries); gmail-account Drive blocked (see FAILURES) |
| evernote | BLOCKED | not signed in; logged |
| granola | PARTIAL (rechecked) | local store encrypted, no web app; 9 notes from public share links found in Slack/Linear; logged |
| google-meet | DONE (rechecked, none exist) | no Meet recordings/transcripts/Gemini notes in either Drive; MANIFEST cross-references 15 meeting-notes Docs in google-docs; logged |
| zoom | DONE | local recordings (1 meeting); zoom.us web not signed in (logged) |
| gmail | DONE (rechecked) | davidbarron410@gmail.com: 11,316 messages / 10,860 threads as raw .eml (4.9 GB; all mail 2025-10-17→, plus Sent/Starred/Important of any age); spot-check 2 longest threads match Gmail API counts. dbarron410@vt.edu Gmail: 1 message (attachment body unavailable) |
| chatgpt | DONE (scope: last year) | STOPGAP from chatgpt.com; 2,360 listed; 148 collected (all 139 from the last year + 9 older); 2,212 older not collected (David's choice); logged |
| claude | DONE (rechecked) | STOPGAP from claude.ai: 2,182 conversations (paged count = 2,182), 10 projects (docs, files, conversation lists); memory + profile in assistant-memory |
| claude-code | DONE (rechecked) | 1708 sessions / 4164 files in projects match source; + history.jsonl, plans, desktop session metadata, claude-vault derived indexes (12437 manifest rows) |
| codex | DONE (rechecked) | 95/95 rollouts present (state DB lists 96; 1 rollout missing at source), history, indexes, DBs |
| cursor | DONE (none exist) | not installed; logged in FAILURES |
| grok | BLOCKED | not signed in; logged |
| gemini | DONE | u/1 38 chats, u/0 3 chats (raw batchexecute JSON); no Gems |
| perplexity | BLOCKED | not signed in; logged |
| assistant-memory | DONE | claude (memory, profile), chatgpt (59 memories, custom instructions, settings, profile), gemini (empty state) |
| zotero | DONE (mirror) | ~/.engelbart/.zotero mirror (zotero.org not signed in): user lib 3 items + group 6141877 99 items, 6 PDFs |
| overleaf | BLOCKED (rechecked) | Chrome not signed in; session is in Engelbart's embedded browser; mirror not used (needs David's OK); logged |
| pdfs | DONE (rechecked) | 157 PDFs from user folders; exclusions logged |
| github | DONE (rechecked) | 72 local repos + 29 github.com mirror clones (account + Mathetic-PBC org + collaborator repos) with issues/PRs/comments/releases JSON; starred list |
| websites | DONE | 3 bookmarks only; no saved pages exist |
| linear | DONE (rechecked) | via Linear MCP (web not signed in): 146 issues (+detail, 97 comments), 3 documents, 2 projects (+milestones, status updates), workspace metadata |
| browser-history | DONE | Chrome x3 profiles + Codex app browser; Safari blocked |
| local-notes | DONE | 152 note-type files (md/txt/docx/html/pages) outside Obsidian & repos |
| local-files (added) | DONE | 871 other loose files |
| outlook (added) | BLOCKED (mail) | 1,392 cached attachments collected; outlook.office.com has no raw-source/Save-as option, so mail is not collected; options for David in FAILURES |
| slack (added) | DONE | Mathetic workspace via Slack MCP: 27 conversations (15 channels, 12 DMs), ~742 messages, 27 threads, 102 files, 12 user profiles |

## Schema layer

DONE 2026-10-17: datasets.json, ground_truth_projects.json (22 draft rows), generated_categories.json ([]), analyses.json ([]), source_items.json (rebuilt, all unlabeled), README.md. Re-run `_scripts/build_source_items.py` after every tool finishes.

Checkpoint when the schema layer was added (background browser loops still running): chatgpt 129/2,360 conversations in _incoming/chatgpt (window.__g3, ~1/min); vt Drive native exports 395 done, 734 queued (window.__D, docs tab); gmail-account Drive natives 47 (window.__E, docs tab); Drive binaries 125 gmail-account + 9 vt retries (window.__B, drive tab).

## Phase 2 — synthetic

Not started (begins only after Phase 1 is DONE and logged).
