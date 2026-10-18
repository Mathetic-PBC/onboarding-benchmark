# Brief for synthetic generators (Phase 2 of benchmark-data)

You are generating **synthetic** data for a benchmark that tests Engelbart's context import (a research notebook that imports a
person's chats, files, papers, repos, notes, email and drive when they onboard; its import currently has omissions, wrong items
and duplicates). The benchmark root is `~/Desktop/benchmark/benchmark-data/` (call it ROOT).

## Read first
1. `ROOT/synthetic/PERSON.md`. **The source of truth.** The synthetic person is David Barron. Use its accounts, people, project
   ids, timeline, fixed event dates, burst calendar, unrelated themes and hard-case table. Don't invent new outsiders beyond its
   list unless a minor walk-on (a store, a newsletter, a support agent) needs one.
2. `ROOT/_scripts/synth/synthlib.py`: the helper library you must use (`Gen`, `bursty_dates`, `dt`, `iso`, `rfc2822`, `uid`,
   `hexid`, native writers for docx/xlsx/pptx/pdf/eml/zip/sqlite, `git_repo`, `SHARED`). **Do not edit it.** Put any extra helper
   in your own script.
3. The authentic folders for your tools, as a **style reference only** (`ROOT/authentic/<tool>/`, plus `ROOT/authentic/*` for
   related tools): look at file formats, JSON shapes, folder layout, naming, vocabulary and length. Sample a handful of files;
   don't read everything.

## Hard rules
- **Never copy or paraphrase a real item.** Write new content. Don't reuse real message text, real titles verbatim, real
  conversation ids, real secrets/keys/tokens/passwords, real phone numbers or real addresses. Don't use private matters from
  the authentic data (relationships, health, family conflict, finances). Personal clutter comes from PERSON.md §5 themes only.
- Write **only** inside `ROOT/synthetic/<your tools>/` (through `Gen`), your generator scripts `ROOT/_scripts/synth/gen_<tool>.py`,
  any content files your scripts read under `ROOT/_scripts/synth/content/<tool>/`, and (via `Gen.finish()`)
  `ROOT/_scripts/synth/labels/<tool>.json`. Don't touch `authentic/`, other tools' folders, `synthlib.py`, `shared/`, or any
  top-level file (PROGRESS, FAILURES, README, the json tables). Don't use the network or any browser/account.
- Use the scratch venv python for everything:
  `SYNTHPY=/private/tmp/claude-501/-Users-divadbaroon-Desktop-benchmark/ddaa4403-0276-46d5-8b1f-7fd3346e76de/scratchpad/synthvenv/bin/python`
- One generator script per tool, `ROOT/_scripts/synth/gen_<tool>.py`, deterministic and rerunnable (`Gen(tool)` wipes and
  rebuilds `synthetic/<tool>/`). Start it with `sys.path.insert(0, os.path.dirname(__file__)); from synthlib import *`.
  The *content* (the actual prose, messages, notes) must be written by you, item by item, with real substance. Templates and
  random word-salad aren't acceptable. Reusing a structure is fine, but every item needs its own specific content: names,
  numbers, decisions, errors, dates. Small helpers that wrap your hand-written content into the native format are expected.
- **Dates:** spread items over 2025-10-17 → 2026-10-17 using the PERSON.md burst calendar (`bursty_dates`, or the fixed event
  dates for items about those events). Include quiet weeks and a few heavy ones. Put dates **inside** the content too (note
  headers, email `Date:`, chat message timestamps, session timestamps). Set file times through the `Gen` writers
  (created + modified). Times must be consistent: no message after the item's modified time, nothing after 2026-10-17.
- **Labels:** every item gets `project_ids` (from PERSON.md §3, `project_none` for unrelated) via the writer's
  `project_ids=` / `label_key=` or `g.label()`. A label key is the **item key**: the file's path relative to
  `synthetic/<tool>/`, or the directory for multi-file items (see your tool spec). An item can belong to several projects. Put a
  short `notes=` on hard-case items starting with `HARD CASE: <kind> —` (PERSON.md §6 kinds), and on normal items when useful.
  Roughly 55–65% of items should relate to a project and 35–45% should be unrelated (`project_none` or personal), unless your
  spec says otherwise.
- `modeled_on`: when an item imitates the format or shape of a specific kind of real item, name that *kind/location*, e.g.
  `authentic/chatgpt conversation JSON (backend-api shape)` or `authentic/slack/Mathetic/<channel>/messages.json shape`. Never
  put real content there. Leave it empty when nothing real was imitated.
- `account=` is the account/library the item belongs to (PERSON.md §1 table).
- Store everything in the tool's **native shape** (given in your spec) and keep it whole.
- Run your script, then check its output: open a few files, check JSON parses, check dates, check `g.finish()` reports 0 files
  without a label, and run `python3 ROOT/_scripts/build_source_items.py --dry synthetic/<tool>` (always with `--dry`: it writes nothing; without it you would race other generators) to see the items it yields (item
  count and keys should match your labels; report any mismatch). It's fine to rerun.

## Report back (concise)
Per tool: number of items and files, the date range, the hard cases you placed (with paths), the project spread
(counts per project id), and anything you couldn't do and why (that goes into FAILURES.md; the coordinator writes it).
