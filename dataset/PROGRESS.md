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
| google-docs | DONE | vt.edu: 1,271 placed / 22 not collected (folders, sites, scripts, 2 forms 403, 6 binaries 503); gmail.com: 303 placed / 41 not collected (13 probable folders, 28 binaries 503); logged |
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
| overleaf | DONE | signed in by David 2026-10-18; 22/22 project source zips; logged |
| pdfs | DONE (rechecked) | 157 PDFs from user folders; exclusions logged |
| github | DONE (rechecked) | 72 local repos + 29 github.com mirror clones (account + Mathetic-PBC org + collaborator repos) with issues/PRs/comments/releases JSON; starred list |
| websites | DONE | 3 bookmarks only; no saved pages exist |
| linear | DONE (rechecked) | via Linear MCP (web not signed in): 146 issues (+detail, 97 comments), 3 documents, 2 projects (+milestones, status updates), workspace metadata |
| browser-history | DONE | Chrome x3 profiles + Codex app browser; Safari blocked |
| local-notes | DONE | 152 note-type files (md/txt/docx/html/pages) outside Obsidian & repos |
| local-files (added) | DONE | 871 other loose files |
| outlook (added) | SKIPPED (David's choice) | 1,392 cached attachments + 86 web-downloaded .eml (partial sample, 57 threads); rest of mail not collected; logged |
| slack (added) | DONE | Mathetic workspace via Slack MCP: 27 conversations (15 channels, 12 DMs), ~742 messages, 27 threads, 102 files, 12 user profiles |

## Schema layer

DONE 2026-10-17: datasets.json, ground_truth_projects.json (22 draft rows), generated_categories.json ([]), analyses.json ([]), source_items.json (rebuilt, all unlabeled), README.md. Re-run `_scripts/build_source_items.py` after every tool finishes.

Phase 1 collection finished 2026-10-18. Overleaf collected after David signed in; Outlook mail skipped at David's request (86-message partial sample kept); see FAILURES. Background browser loops stopped.

Checkpoint when the schema layer was added (background browser loops still running): chatgpt 129/2,360 conversations in _incoming/chatgpt (window.__g3, ~1/min); vt Drive native exports 395 done, 734 queued (window.__D, docs tab); gmail-account Drive natives 47 (window.__E, docs tab); Drive binaries 125 gmail-account + 9 vt retries (window.__B, drive tab).

## Phase 2 — synthetic

Started 2026-10-18 on David's go-ahead ("just do phase 2 now"; he waived reviewing ground_truth_projects.json first).
Inputs: synthetic/PERSON.md (the synthetic person is David, per datasets.json), _scripts/synth/AGENT_BRIEF.md,
_scripts/synth/synthlib.py, shared assets from _scripts/synth/gen_shared.py. One deterministic generator per tool:
_scripts/synth/gen_<tool>.py (rerun = rebuild that folder). Labels: _scripts/synth/labels/<tool>.json, merged into
synthetic/ground_truth_labels.json by _scripts/synth/merge_labels.py. Then run build_source_items.py.
Added project_hint_timing_study (synthetic only) to ground_truth_projects.json.

| group | tools | status |
|---|---|---|
| A notes | notion 73, onenote 40, evernote 56, obsidian 35, apple-notes 27 | DONE |
| B meetings | granola 22, google-meet 26, zoom 7 | DONE |
| C email | gmail 178 threads (3 accounts incl. second account runs@), outlook 35 | DONE |
| D AI chats | chatgpt 50, claude 43, grok 35, gemini 22, perplexity 48, assistant-memory 8 | DONE |
| E code | claude-code 32, codex 22, cursor 38, github 9 | DONE |
| F papers | zotero 41, overleaf 6, pdfs 37 | DONE |
| G drive/local | google-docs 70, local-notes 37, local-files 30, websites 27, browser-history 4 | DONE |
| H work tools | slack 101, linear 51 | DONE |


Phase 2 DONE 2026-10-18: 1,210 synthetic items, all labelled "generated"; merge_labels.py → build_source_items.py →
review.py (no problems). Aggregate source_items.json 23,558 items. Gaps and deviations: FAILURES.md "Phase 2". Open item:
David's review of ground_truth_projects.json (all rows still draft).
