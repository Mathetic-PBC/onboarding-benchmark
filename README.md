<!-- Built from docs/onboarding-benchmark-and-dataset-documentation.html by docs/build_readme.py. Edit the page, then rerun the script. -->

# Onboarding Benchmark and Dataset Documentation

A dataset of all my authentic data across ChatGPT, Claude, Claude Code, Codex, Overleaf, Zotero, GitHub, Google Drive, Gmail, Notion, Linear, Granola, Evernote, Apple Notes, PDFs and local files, plus synthetic data to fill the gaps for the tools in that list I don't use. The benchmark measures how accurately Claude Code and Codex classify the data against the ground truth, which is my own classification of my own data.

The page itself, with its tabs: [onboarding-benchmark-and-dataset-documentation.html](docs/onboarding-benchmark-and-dataset-documentation.html) (open it in a browser after cloning). Each tab is a section below; click one to open it.

<details open>
<summary><b>Dataset</b></summary>

### Benchmark dataset

```
benchmark-data/
  datasets.json                one row per benchmark
  ground_truth_projects.json   the answer key: my real projects
  generated_categories.json    each category list the import agent generates
  source_items.json            one row per item
  analyses.json                one row per agent pass over an item
  README.md                    how the dataset was built
  FAILURES                     items that could not be copied or generated
  authentic/                   your own data from the past year, relevant and irrelevant,
                               so it holds all the papers and work you care about
    <source>/                  one folder per onboarding source (see Sources)
  synthetic/                   generated data about me (David) and my projects, mixed with
                               unrelated items, mostly on the platforms I don't use; each
                               written in the platform's own file type
    PERSON.md                  a summary of me drawn from the authentic data, used to
                               generate the synthetic data
    <source>/                  the same folders
```

</details>

<details>
<summary><b>Tables</b></summary>

### Tables

| name | what it holds | links to |
|---|---|---|
| `datasets` | one row per benchmark (reference date 2026-10-17, path to `PERSON.md`) | `source_items.dataset_id` → `datasets.id` |
| `ground_truth_projects` | the answer key: my real projects with a one-line description each, plus `project_none`. Never shown to the import agent | `source_items.ground_truth.project_ids` → `ground_truth_projects.id` |
| `generated_categories` | each category list the import agent generates in a run (wave 1 draft, confirmed list). Scored against `ground_truth_projects` | `analyses.category_set_id` → `generated_categories.id`; each row has a `run_id` |
| `source_items` | one row per item (existing) |  |
| `analyses` | one row per agent pass over an item (existing) | `analyses.item_id` → `source_items.id` |

<details>
<summary>Sample: datasets</summary>

**datasets**

```json
{
  "id": "benchmark_001",
  "reference_date": "2026-10-17",
  "person_path": "synthetic/PERSON.md",
  "description": "David's real digital footprint plus synthetic data about David."
}
```

</details>

<details>
<summary>Sample: ground_truth_projects</summary>

**ground_truth_projects**

```json
[
  {
    "id": "project_engelbart",
    "dataset_id": "benchmark_001",
    "name": "Engelbart",
    "description": "Research notebook that keeps track of where each thought came from: agents, workspaces, onboarding.",
    "status": "draft"
  },
  {
    "id": "project_engelbart_import",
    "dataset_id": "benchmark_001",
    "name": "Engelbart import quality",
    "description": "Onboarding context import, its category sort and this benchmark.",
    "status": "draft"
  },
  {
    "id": "project_tutortrace",
    "dataset_id": "benchmark_001",
    "name": "TutorTrace",
    "description": "Dataset and taxonomy of learner behavioral states in AI-assisted programming (UIST '26).",
    "status": "draft"
  },
  {
    "id": "project_idetrace",
    "dataset_id": "benchmark_001",
    "name": "IDETrace",
    "description": "Dataset for predicting novice programmer behavior in AI-assisted coding (NeurIPS '26).",
    "status": "draft"
  },
  {
    "id": "project_custody_verification",
    "dataset_id": "benchmark_001",
    "name": "Custody of verification",
    "description": "Research on who keeps responsibility for checking AI-assisted work.",
    "status": "draft"
  },
  {
    "id": "project_berkeley",
    "dataset_id": "benchmark_001",
    "name": "Berkeley research",
    "description": "Berkeley lab outreach and fellowship collaborations.",
    "status": "draft"
  },
  {
    "id": "project_spec_design",
    "dataset_id": "benchmark_001",
    "name": "Specification design",
    "description": "Teaching people to specify system behavior for AI coding agents.",
    "status": "draft"
  },
  {
    "id": "project_none",
    "dataset_id": "benchmark_001",
    "name": "None",
    "description": "Items that belong to no project.",
    "status": "draft"
  }
]
```

</details>

<details>
<summary>Sample: generated_categories</summary>

**generated_categories**

```json
{
  "id": "catset_v2",
  "run_id": "run_001",
  "dataset_id": "benchmark_001",
  "categories": [
    {
      "id": "project_engelbart",
      "label": "Engelbart",
      "description": "Research notebook, agents, onboarding.",
      "origin": "user"
    },
    {
      "id": "project_engelbart_import",
      "label": "Engelbart import quality",
      "parent_id": "project_engelbart",
      "description": "Context import, benchmark, category sort.",
      "origin": "wave1"
    },
    {
      "id": "project_tutortrace",
      "label": "TutorTrace",
      "description": "Learner-behavior dataset and taxonomy (UIST '26).",
      "origin": "profile"
    },
    {
      "id": "other",
      "label": "Other / new topic",
      "origin": "system"
    }
  ],
  "created_at": "2026-10-18T04:06:30Z"
}
```

</details>

<details>
<summary>Sample: source_items</summary>

**source_items**

```json
{
  "source_items": [
    {
      "id": "item_001",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "chatgpt",
      "source_id": "6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
      "title": "Thoughts",
      "content_type": "conversation",
      "created_at": "2026-09-01T10:00:00Z",
      "modified_at": "2026-09-02T12:00:00Z",
      "ingested_at": "2026-10-18T04:00:00Z",
      "path": "authentic/chatgpt/item_001.json",
      "source_url": "https://chatgpt.com/c/6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
      "content_hash": "sha256:a41f…01",
      "library_item_id": null,
      "metadata": {
        "format": "json",
        "language": "en",
        "message_count": 42,
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [
          "project_tutortrace"
        ],
        "notes": "Evaluation design for the guided/dependent help-seeking task."
      }
    },
    {
      "id": "item_002",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "google-docs",
      "source_id": "1Qx9fK3bT0aLm2…",
      "title": "Untitled document",
      "content_type": "document",
      "created_at": "2026-10-15T18:20:00Z",
      "modified_at": "2026-10-17T22:05:00Z",
      "ingested_at": "2026-10-18T04:00:02Z",
      "path": "authentic/google-docs/item_002.docx",
      "source_url": "https://docs.google.com/document/d/1Qx9fK3bT0aLm2…/edit",
      "content_hash": "sha256:b7c2…02",
      "library_item_id": null,
      "metadata": {
        "format": "docx",
        "language": "en",
        "word_count": 2310,
        "folder": "My Drive",
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [
          "project_engelbart_import"
        ],
        "notes": "Benchmark design draft."
      }
    },
    {
      "id": "item_003",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "google-docs",
      "source_id": "1Zr0pL8wQe…",
      "title": "Lease renewal 2026",
      "content_type": "document",
      "created_at": "2026-06-03T09:12:00Z",
      "modified_at": "2026-06-03T09:40:00Z",
      "ingested_at": "2026-10-18T04:00:03Z",
      "path": "authentic/google-docs/item_003.docx",
      "source_url": "https://docs.google.com/document/d/1Zr0pL8wQe…/edit",
      "content_hash": "sha256:c9d0…03",
      "library_item_id": null,
      "metadata": {
        "format": "docx",
        "language": "en",
        "word_count": 640,
        "folder": "Personal",
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [],
        "notes": "Personal. Belongs to no project."
      }
    }
  ]
}
```

</details>

<details>
<summary>Sample: analyses</summary>

**analyses**

```json
{
  "id": "analysis_001",
  "item_id": "item_001",
  "run_id": "run_001",
  "parent_analysis_id": null,
  "category_set_id": "catset_v0",
  "content_hash": "sha256:a41f…01",
  "stage": "wave1_category_discovery",
  "status": "completed",
  "error": null,
  "started_at": "2026-10-18T04:01:00Z",
  "completed_at": "2026-10-18T04:01:04Z",
  "model": "REPLACE_WITH_MODEL_ID",
  "prompt_version": "wave1_discovery_v1",
  "config": {
    "sampling_strategy": "user_turns_digest",
    "max_input_tokens": 800
  },
  "sample": {
    "metadata_fields_read": [
      "title",
      "created_at",
      "modified_at"
    ],
    "unit": "message",
    "index_base": 0,
    "range_end": "exclusive",
    "ranges": [
      {
        "start": 0,
        "end": 1
      },
      {
        "start": 40,
        "end": 41
      }
    ],
    "digest": "first sentence of each user turn, 400 chars",
    "units_read": 2,
    "total_units": 42,
    "coverage_fraction": 0.047619,
    "input_snapshot_path": "runs/run_001/inputs/item_001.txt"
  },
  "result": {
    "project_assignments": [
      {
        "project_id": "project_tutortrace",
        "confidence": 0.55,
        "evidence": [
          {
            "unit": "message",
            "index": 0,
            "quote": "ok so for the help-seeking classifier, how do we validate the labels"
          }
        ]
      }
    ],
    "proposed_projects": [
      {
        "id": "project_engelbart_import",
        "label": "Engelbart import quality",
        "description": "Context import, benchmark, category sort.",
        "evidence_item_ids": [
          "item_017",
          "item_022"
        ]
      }
    ],
    "summary": "Validating labels for a help-seeking classifier.",
    "needs_deeper_read": true
  },
  "usage": {
    "input_tokens": 620,
    "output_tokens": 140,
    "cost_usd": null
  }
}
```

</details>

</details>

<details>
<summary><b>Sources</b></summary>

#### Notes

<details>
<summary>Obsidian</summary>

`obsidian/`

- **Stored as:** Vault folder copied whole: `.md` notes, attachments (png, pdf), and the `.obsidian/` config
- **One source item =** one `.md` note

**source_items row**

```json
{
  "id": "item_obsidian_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "obsidian",
  "source_id": "Engelbart/Agent handoff protocol.md",
  "title": "Agent handoff protocol",
  "content_type": "note",
  "created_at": "2026-08-12T16:03:00Z",
  "modified_at": "2026-09-30T21:44:00Z",
  "ingested_at": "2026-10-18T04:00:00Z",
  "path": "authentic/obsidian/mathetic/Engelbart/Agent handoff protocol.md",
  "source_url": "obsidian://open?vault=mathetic&file=Engelbart%2FAgent%20handoff%20protocol",
  "content_hash": "sha256:fc27…b9",
  "library_item_id": null,
  "metadata": {
    "format": "md",
    "language": "en",
    "vault": "mathetic",
    "folder": "Engelbart",
    "word_count": 1840,
    "frontmatter_tags": [
      "spec",
      "agents"
    ],
    "wikilinks_out": 12,
    "attachments": []
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": "Spec for agent handoffs."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `line / word` (what `sample.unit` counts)
- **Engelbart today:** `list_note_files` over the vault folder, then `import_note_files`. Only `.md`, `.markdown`, `.txt` are listed. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Notes in the default vault that are just welcome or daily notes (noise)
  - Wikilinks to notes outside the date window

</details>

</details>

<details>
<summary>Notion</summary>

`notion/`

- **Stored as:** Notion's "Markdown & CSV" export: one `.md` per page (id suffix in the filename), databases as `.csv`, folders mirroring the page tree
- **One source item =** one page (a database row is also a page)

**source_items row**

```json
{
  "id": "item_notion_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": "authentic/granola/item_granola_001",
  "source": "notion",
  "source_id": "1a7f3c2e-9b0d-4e51-a8c6-77e2d0f4b913",
  "title": "Weekly sync — Oct 6",
  "content_type": "page",
  "created_at": "2026-10-06T17:00:00Z",
  "modified_at": "2026-10-06T18:12:00Z",
  "ingested_at": "2026-10-18T04:00:01Z",
  "path": "synthetic/notion/Team wiki/Meetings/Weekly sync — Oct 6 1a7f3c2e9b0d4e51a8c677e2d0f4b913.md",
  "source_url": "https://www.notion.so/Weekly-sync-Oct-6-1a7f3c2e9b0d4e51a8c677e2d0f4b913",
  "content_hash": "sha256:af70…46",
  "library_item_id": null,
  "metadata": {
    "format": "md",
    "language": "en",
    "workspace": "synthetic person's workspace",
    "parent_path": [
      "Team wiki",
      "Meetings"
    ],
    "is_database_row": true,
    "database": "Meetings",
    "properties": {
      "Date": "2026-10-06",
      "Attendees": [
        "Collaborator A",
        "Collaborator B"
      ]
    },
    "word_count": 620
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `block / word` (what `sample.unit` counts)
- **Engelbart today:** Official MCP server, read tools only: `notion-search` plus `notion-list-recent / shared / private / favorite-pages` and `notion-fetch`. No full workspace walk. The pre-run health check skips Notion (no `reads` entry in `connect-sources.cjs`). (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - An old page deep in the tree that is not recent, shared or favorited
  - Database rows that only make sense with the database's columns

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Apple Notes</summary>

`apple-notes/`

- **Stored as:** No native export. One `.html` body per note (what macOS Automation returns), plus an `_attachments/` folder for pictures
- **One source item =** one note

**source_items row**

```json
{
  "id": "item_apple-notes_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "apple-notes",
  "source_id": "x-coredata://5E1D…/ICNote/p1423",
  "title": "reading list",
  "content_type": "note",
  "created_at": "2025-03-11T02:20:00Z",
  "modified_at": "2025-09-02T19:05:00Z",
  "ingested_at": "2026-10-18T04:00:02Z",
  "path": "authentic/apple-notes/iCloud/Notes/reading list.html",
  "source_url": null,
  "content_hash": "sha256:ba66…e4",
  "library_item_id": null,
  "metadata": {
    "format": "html",
    "language": "en",
    "account": "iCloud",
    "folder": "Notes",
    "pinned": true,
    "locked": false,
    "word_count": 210,
    "attachments": [
      {
        "type": "image/png",
        "path": "authentic/apple-notes/iCloud/Notes/reading list_attachments/IMG_0412.png"
      }
    ]
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": "Tools-for-thought reading list. Outside the one-year window but pinned: tests the cutoff bypass."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `line / word` (what `sample.unit` counts)
- **Engelbart today:** `apple_notes_folders` → `apple_notes_list` (500 default) → `import_apple_notes` (200 per call). HTML converted to Markdown, pictures saved, Recently Deleted excluded. Locked and pinned notes aren't handled. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - A pinned reading list last edited more than a year ago
  - A locked note
  - Folders like Recipes or Shopping

</details>

</details>

<details>
<summary>OneNote</summary>

`onenote/`

- **Stored as:** One `.html` per page, the shape OneNote's API returns page content in, under notebook/section folders
- **One source item =** one page

**source_items row**

```json
{
  "id": "item_onenote_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": "authentic/obsidian/item_obsidian_014",
  "source": "onenote",
  "source_id": "0-8c1e5f0d2b7a4a19b3e0d6f1c2a9e744!1-3F2A…",
  "title": "Pilot session notes",
  "content_type": "page",
  "created_at": "2026-04-22T14:10:00Z",
  "modified_at": "2026-04-23T09:31:00Z",
  "ingested_at": "2026-10-18T04:00:03Z",
  "path": "synthetic/onenote/Lab notebook/Pilot study/Pilot session notes.html",
  "source_url": null,
  "content_hash": "sha256:7439…82",
  "library_item_id": null,
  "metadata": {
    "format": "html",
    "language": "en",
    "notebook": "Lab notebook",
    "section": "Pilot study",
    "page_level": 0,
    "word_count": 480
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)
- **Hard cases to plant:**
  - Subpages (page_level 1) that only make sense under their parent page

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Google Drive / Docs</summary>

`google-docs/`

- **Stored as:** Docs as `.docx`, Sheets as `.xlsx` (every tab), Slides as `.pptx`, other files as they are, in folders mirroring Drive (My Drive, Shared with me)
- **One source item =** one file

**source_items row**

```json
{
  "id": "item_google-docs_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "google-docs",
  "source_id": "1kV0x7bQnR3…",
  "title": "Berkeley labs + contacts",
  "content_type": "spreadsheet",
  "created_at": "2026-08-26T20:14:00Z",
  "modified_at": "2026-10-09T03:02:00Z",
  "ingested_at": "2026-10-18T04:00:04Z",
  "path": "authentic/google-docs/u0/My Drive/Berkeley labs + contacts.xlsx",
  "source_url": "https://docs.google.com/spreadsheets/d/1kV0x7bQnR3…/edit",
  "content_hash": "sha256:ab07…75",
  "library_item_id": null,
  "metadata": {
    "format": "xlsx",
    "kind": "sheet",
    "mime_type": "application/vnd.google-apps.spreadsheet",
    "account": "u/0",
    "folder": "My Drive",
    "owner": "me",
    "shared_with_me": false,
    "tabs": [
      "Labs",
      "Contacts",
      "Status"
    ],
    "rows_total": 212
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_berkeley"
    ],
    "notes": "Multi-tab sheet. Today's import keeps only the first tab."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word (Docs), row (Sheets), slide (Slides)` (what `sample.unit` counts)
- **Engelbart today:** No list tool today. The agent reads Drive search and folder pages with `browser_*` tools, then `import_google_files` by `{id, kind}`: Docs → Markdown, Sheets → first tab only as CSV, Slides → text. Planned: a paged `drive_files` list with a count. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Multi-tab sheet
  - "Untitled document" / "Doc1"
  - Files in Shared with me
  - A second Google account (`/u/1`)

</details>

</details>

<details>
<summary>Evernote</summary>

`evernote/`

- **Stored as:** One `.enex` (XML) file per notebook, notes inside it with their resources
- **One source item =** one note inside a notebook's `.enex`

**source_items row**

```json
{
  "id": "item_evernote_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": null,
  "source": "evernote",
  "source_id": "c3f1a2b4-7d0e-4f9a-b2c1-08e5d6a7f390",
  "title": "Sheet-pan gnocchi",
  "content_type": "note",
  "created_at": "2026-02-14T01:40:00Z",
  "modified_at": "2026-02-14T01:52:00Z",
  "ingested_at": "2026-10-18T04:00:05Z",
  "path": "synthetic/evernote/Personal.enex",
  "source_url": null,
  "content_hash": "sha256:7eba…c1",
  "library_item_id": null,
  "metadata": {
    "format": "enex",
    "language": "en",
    "notebook": "Personal",
    "note_index": 7,
    "tags": [
      "recipes"
    ],
    "resources": 1,
    "word_count": 180
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [],
    "notes": "Personal clutter."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word` (what `sample.unit` counts)
- **Engelbart today:** Official MCP server (beta), search tools only: `search_notebooks`, `search_notes`, `semantic_search`, `search_tags`, `search_spaces`. No list. Web fallback kept. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Notes only reachable by search
  - Personal notebooks mixed with work

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

#### Meetings

<details>
<summary>Granola</summary>

`granola/`

- **Stored as:** One `.md` per meeting (Granola's notes) plus a `.transcript.txt` beside it
- **One source item =** one meeting (notes + transcript)

**source_items row**

```json
{
  "id": "item_granola_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "granola",
  "source_id": "not_8Gq2…",
  "title": "Context import strategy session",
  "content_type": "meeting",
  "created_at": "2026-10-17T19:00:00Z",
  "modified_at": "2026-10-17T19:41:00Z",
  "ingested_at": "2026-10-18T04:00:06Z",
  "path": "authentic/granola/2026-10-17 Context import strategy session.md",
  "source_url": null,
  "content_hash": "sha256:2a5b…a3",
  "library_item_id": null,
  "metadata": {
    "format": "md",
    "language": "en",
    "transcript_path": "authentic/granola/2026-10-17 Context import strategy session.transcript.txt",
    "folder": null,
    "attendees_count": 2,
    "duration_min": 38,
    "has_ai_notes": true
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart_import"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `transcript line` (what `sample.unit` counts)
- **Engelbart today:** Official MCP server: `list_meetings`, `list_meeting_folders`, `get_meetings`, transcripts. The skill lists meetings in the plan's time range; the agent writes each as a note with `add_note`. No import-by-id tool, no counts. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Short meetings with generic titles ("Sync")
  - Onboarding calls that mention several projects

</details>

</details>

<details>
<summary>Google Meet</summary>

`google-meet/`

- **Stored as:** Transcript Google Docs as `.docx` from the Meet Recordings folder; recordings (`.mp4`) optional
- **One source item =** one meeting transcript

**source_items row**

```json
{
  "id": "item_google-meet_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "google-meet",
  "source_id": "1Tm4Rr9…",
  "title": "Engelbart sync - 2026/09/03 14:02 PDT - Transcript",
  "content_type": "transcript",
  "created_at": "2026-09-03T21:47:00Z",
  "modified_at": "2026-09-03T21:48:00Z",
  "ingested_at": "2026-10-18T04:00:07Z",
  "path": "authentic/google-meet/u0/Meet Recordings/Engelbart sync - 2026-09-03 14-02 PDT - Transcript.docx",
  "source_url": "https://docs.google.com/document/d/1Tm4Rr9…/edit",
  "content_hash": "sha256:5f8c…b5",
  "library_item_id": null,
  "metadata": {
    "format": "docx",
    "kind": "doc",
    "account": "u/0",
    "folder": "Meet Recordings",
    "recording_path": null,
    "speakers": 3,
    "word_count": 7400
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word / speaker turn` (what `sample.unit` counts)
- **Engelbart today:** Not a separate reader: transcripts are Google Docs. The Drive skill points the agent at Drive searches like `q=Transcript` or the Meet Recordings folder, then `import_google_files`. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Transcript and Gemini "notes by Gemini" doc for the same meeting (near-duplicates)

</details>

</details>

<details>
<summary>Zoom</summary>

`zoom/`

- **Stored as:** Zoom's local recording folder per meeting (`~/Documents/Zoom/<date time topic>/`): `.m4a`/`.mp4` and a `.vtt` or `closed_caption.txt` transcript
- **One source item =** one meeting folder

**source_items row**

```json
{
  "id": "item_zoom_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": "authentic/google-meet/item_google-meet_003",
  "source": "zoom",
  "source_id": "2026-05-12 10.00.03 Advisor 1-1",
  "title": "Advisor 1-1",
  "content_type": "transcript",
  "created_at": "2026-05-12T17:00:03Z",
  "modified_at": "2026-05-12T17:43:10Z",
  "ingested_at": "2026-10-18T04:00:08Z",
  "path": "synthetic/zoom/2026-05-12 10.00.03 Advisor 1-1/closed_caption.vtt",
  "source_url": null,
  "content_hash": "sha256:d7f3…09",
  "library_item_id": null,
  "metadata": {
    "format": "vtt",
    "language": "en",
    "folder": "2026-05-12 10.00.03 Advisor 1-1",
    "media": [
      "audio1849302217.m4a"
    ],
    "duration_min": 42,
    "cues": 611
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `caption cue` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)
- **Hard cases to plant:**
  - Audio-only folder with no transcript

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

#### Email

<details>
<summary>Gmail</summary>

`gmail/`

- **Stored as:** One folder per thread with one `.eml` per message and an `attachments/` folder (or an `.mbox` from Takeout), per account
- **One source item =** one thread

**source_items row**

```json
{
  "id": "item_gmail_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "gmail",
  "source_id": "18f2a9c4d0e7b3a1",
  "title": "Re: IRB amendment for the delayed-transfer study",
  "content_type": "email_thread",
  "created_at": "2026-08-05T15:12:00Z",
  "modified_at": "2026-08-11T13:30:00Z",
  "ingested_at": "2026-10-18T04:00:09Z",
  "path": "authentic/gmail/u1/18f2a9c4d0e7b3a1/",
  "source_url": "https://mail.google.com/mail/u/1/#all/18f2a9c4d0e7b3a1",
  "content_hash": "sha256:853f…0c",
  "library_item_id": null,
  "metadata": {
    "format": "eml",
    "language": "en",
    "account": "u/1",
    "messages": [
      "01.eml",
      "02.eml",
      "03.eml",
      "04.eml"
    ],
    "labels": [
      "INBOX",
      "IMPORTANT"
    ],
    "participants_count": 3,
    "attachments": [
      {
        "name": "Protocol_v3.0.pdf",
        "path": "authentic/gmail/u1/18f2a9c4d0e7b3a1/attachments/Protocol_v3.0.pdf"
      }
    ]
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_custody_verification"
    ],
    "notes": "Today's importer keeps the attachment name only."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `message` (what `sample.unit` counts)
- **Engelbart today:** `gmail_accounts` (each `/mail/u/N`) → `gmail_search` with agent-written queries → `import_gmail_threads` from the print view. One note per thread, attachment names only, capped per call and per session. Planned: bulk listing by label or date with counts. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Thread with attachments
  - Second account
  - Newsletters and receipts

</details>

</details>

#### AI chats

<details>
<summary>ChatGPT</summary>

`chatgpt/`

- **Stored as:** Official export (`conversations.json`, all chats in one file) split into one `.json` per conversation; scraped stopgap until the export arrives
- **One source item =** one conversation

**source_items row**

```json
{
  "id": "item_chatgpt_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "chatgpt",
  "source_id": "6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
  "title": "Thoughts",
  "content_type": "conversation",
  "created_at": "2026-09-01T10:00:00Z",
  "modified_at": "2026-09-02T12:00:00Z",
  "ingested_at": "2026-10-18T04:00:10Z",
  "path": "authentic/chatgpt/conversations/6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1.json",
  "source_url": "https://chatgpt.com/c/6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
  "content_hash": "sha256:f550…8c",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "export_file": "exports/chatgpt/conversations.json",
    "stopgap": true,
    "chatgpt_project": "TutorTrace",
    "message_count": 42
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_tutortrace"
    ],
    "notes": "Vague title, and it sits inside a Project, so the main list leaves it out."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `message` (what `sample.unit` counts)
- **Engelbart today:** `web_chats` calls the site's own endpoints from the hidden signed-in page: 100 per page, cap 2,000, plus a separate walk of each Project. `web_chat_read` for 6,000 characters; `import_web_chats` saves Markdown. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Vague title ("Thoughts", "New chat")
  - Chat inside a ChatGPT Project
  - Relevant passage buried in a long unrelated chat

</details>

</details>

<details>
<summary>Claude</summary>

`claude/`

- **Stored as:** Official Anthropic export (`conversations.json`, `projects.json`) split into one `.json` per conversation
- **One source item =** one conversation

**source_items row**

```json
{
  "id": "item_claude_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "claude",
  "source_id": "9d1c4e7a-2b3f-4a60-8e15-5c0b7d9f2a61",
  "title": "Discover reading guide format",
  "content_type": "conversation",
  "created_at": "2026-10-02T06:11:00Z",
  "modified_at": "2026-10-02T07:40:00Z",
  "ingested_at": "2026-10-18T04:00:11Z",
  "path": "authentic/claude/conversations/9d1c4e7a-2b3f-4a60-8e15-5c0b7d9f2a61.json",
  "source_url": "https://claude.ai/chat/9d1c4e7a-2b3f-4a60-8e15-5c0b7d9f2a61",
  "content_hash": "sha256:365d…b6",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "export_file": "exports/claude/conversations.json",
    "stopgap": false,
    "project": "Engelbart",
    "message_count": 18,
    "attachments": 2,
    "artifacts": 1
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `message (your turns; tool output left out)` (what `sample.unit` counts)
- **Engelbart today:** `web_chats`: finds the organization, lists `chat_conversations` 100 at a time tagged with project names, cap 2,000. Full message tree includes tool output, so snippets are noisier. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Chat with attached documents and artifacts
  - Project chats

</details>

</details>

<details>
<summary>Claude Code</summary>

`claude-code/`

- **Stored as:** Session files copied as they are: `~/.claude/projects/<folder>/<session>.jsonl`
- **One source item =** one session

**source_items row**

```json
{
  "id": "item_claude-code_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "claude-code",
  "source_id": "4b0e9c2d-7f1a-4e83-9a6c-1d2e3f405a7b",
  "title": "Windows-port catch-up to 0.1.19",
  "content_type": "conversation",
  "created_at": "2026-10-16T02:15:00Z",
  "modified_at": "2026-10-16T05:58:00Z",
  "ingested_at": "2026-10-18T04:00:12Z",
  "path": "authentic/claude-code/-Users-divadbaroon-Desktop-engelbart-canvas/4b0e9c2d-7f1a-4e83-9a6c-1d2e3f405a7b.jsonl",
  "source_url": null,
  "content_hash": "sha256:edd6…3e",
  "library_item_id": null,
  "metadata": {
    "format": "jsonl",
    "language": "en",
    "cwd": "/Users/divadbaroon/Desktop/engelbart-canvas",
    "git_branch": "windows-port",
    "entrypoint": "cli",
    "is_sidechain": false,
    "automated": false,
    "user_turns": 23,
    "lines": 1412
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": "Folder alone decides the project."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `user turn` (what `sample.unit` counts)
- **Engelbart today:** `list_chats` / `read_chat` / `import_chats` read the files directly. Title from Claude Code's own title, then summary, then first prompt. Sidechains and `entrypoint sdk-cli` runs are flagged `automated` and skipped by default (the 836 skipped). (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Automated-looking session that holds real work
  - Long pasted logs swamping the snippet

</details>

</details>

<details>
<summary>Codex</summary>

`codex/`

- **Stored as:** Session files copied as they are: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- **One source item =** one session

**source_items row**

```json
{
  "id": "item_codex_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "codex",
  "source_id": "rollout-2026-09-14T22-10-05-0199a3c1-5e2f-7b40-9d18-6a0c2e4f8b13",
  "title": "add the brainstormPrompt flow to the setup pages",
  "content_type": "conversation",
  "created_at": "2026-09-15T05:10:05Z",
  "modified_at": "2026-09-15T05:41:22Z",
  "ingested_at": "2026-10-18T04:00:13Z",
  "path": "authentic/codex/2026/09/14/rollout-2026-09-14T22-10-05-0199a3c1-5e2f-7b40-9d18-6a0c2e4f8b13.jsonl",
  "source_url": null,
  "content_hash": "sha256:bf57…6a",
  "library_item_id": null,
  "metadata": {
    "format": "jsonl",
    "language": "en",
    "cwd": "/Users/divadbaroon/Projects/berkeley-research",
    "originator": "codex_exec",
    "automated": true,
    "user_turns": 1,
    "lines": 388
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_berkeley"
    ],
    "notes": "Flagged automated, but holds real work."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `user turn` (what `sample.unit` counts)
- **Engelbart today:** Same readers as Claude Code. Injected pseudo-messages (environment context, permissions, subagent notices) are stripped. `codex exec` runs count as automated. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - `codex exec` run that did real work
  - Trivial one-line sessions

</details>

</details>

<details>
<summary>Cursor</summary>

`cursor/`

- **Stored as:** Cursor keeps chats in SQLite (`workspaceStorage/<hash>/state.vscdb`, as far as I know). For the benchmark: one `.json` per chat extracted from it, with the source DB noted
- **One source item =** one chat

**source_items row**

```json
{
  "id": "item_cursor_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": "authentic/claude-code/item_claude-code_041",
  "source": "cursor",
  "source_id": "composer:7e2c91b0-4d3a-4f58-a0e6-2b9c1d7f5e04",
  "title": "Fix telemetry segmenter off-by-one",
  "content_type": "conversation",
  "created_at": "2026-03-03T23:02:00Z",
  "modified_at": "2026-03-03T23:27:00Z",
  "ingested_at": "2026-10-18T04:00:14Z",
  "path": "synthetic/cursor/workspaceStorage/a91f…/composer-7e2c91b0.json",
  "source_url": null,
  "content_hash": "sha256:0909…f5",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "origin_db": "state.vscdb (SQLite)",
    "workspace": "~/Projects/telemetry-pipeline",
    "message_count": 14
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `message` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)
- **Hard cases to plant:**
  - Chat whose workspace folder no longer exists

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Grok</summary>

`grok/`

- **Stored as:** One `.json` per conversation, in the shape of Grok's account data export (unverified)
- **One source item =** one conversation

**source_items row**

```json
{
  "id": "item_grok_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": "authentic/chatgpt/item_chatgpt_212",
  "source": "grok",
  "source_id": "b04d7e21-93fa-4c6b-8e52-f1a0c3d9e7b8",
  "title": "is a 0.72 AUROC good",
  "content_type": "conversation",
  "created_at": "2026-07-28T04:55:00Z",
  "modified_at": "2026-07-28T05:01:00Z",
  "ingested_at": "2026-10-18T04:00:15Z",
  "path": "synthetic/grok/conversations/b04d7e21-93fa-4c6b-8e52-f1a0c3d9e7b8.json",
  "source_url": null,
  "content_hash": "sha256:2ca6…c0",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "message_count": 6
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `message` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Gemini</summary>

`gemini/`

- **Stored as:** Google Takeout's "My Activity → Gemini Apps" file (JSON), one entry per prompt and reply (unverified)
- **One source item =** one activity entry (Takeout doesn't group by conversation)

**source_items row**

```json
{
  "id": "item_gemini_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": null,
  "source": "gemini",
  "source_id": "takeout:gemini:2026-04-02T18:21:44Z",
  "title": "Summarize this paper on affective computing",
  "content_type": "conversation",
  "created_at": "2026-04-02T18:21:44Z",
  "modified_at": "2026-04-02T18:21:44Z",
  "ingested_at": "2026-10-18T04:00:16Z",
  "path": "synthetic/gemini/MyActivity.json",
  "source_url": null,
  "content_hash": "sha256:f069…00",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "origin": "Google Takeout, My Activity, Gemini Apps",
    "account": "u/0",
    "entry_index": 311
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `entry` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)
- **Hard cases to plant:**
  - No conversation grouping in the export, so one chat becomes many entries

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Perplexity</summary>

`perplexity/`

- **Stored as:** One `.md` per thread with its cited sources (I don't know of a bulk export)
- **One source item =** one thread

**source_items row**

```json
{
  "id": "item_perplexity_001",
  "dataset_id": "benchmark_001",
  "provenance": "synthetic",
  "modeled_on": null,
  "source": "perplexity",
  "source_id": "cheapest-flights-sfo-to-iad-thanksgiving-QvL8…",
  "title": "cheapest flights SFO to IAD thanksgiving",
  "content_type": "conversation",
  "created_at": "2026-10-09T16:40:00Z",
  "modified_at": "2026-10-09T16:44:00Z",
  "ingested_at": "2026-10-18T04:00:17Z",
  "path": "synthetic/perplexity/threads/cheapest-flights-sfo-to-iad-thanksgiving.md",
  "source_url": null,
  "content_hash": "sha256:c458…5e",
  "library_item_id": null,
  "metadata": {
    "format": "md",
    "language": "en",
    "turns": 3,
    "sources_cited": 8
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [],
    "notes": "Personal clutter."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `turn` (what `sample.unit` counts)
- **Engelbart today:** On the onboarding app list. I haven't seen which reader handles it. (not checked; the file type above is a best guess at the platform's export, so check it against what the /goal run produced)

`modeled_on` is an addition from the `/goal` manifest rule, not part of the original schema.

</details>

</details>

<details>
<summary>Assistant memory</summary>

`assistant-memory/`

- **Stored as:** One `.md` per assistant: saved memory entries plus custom instructions, read from the settings page
- **One source item =** one assistant's memory set

**source_items row**

```json
{
  "id": "item_assistant-memory_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "assistant-memory",
  "source_id": "chatgpt:memory",
  "title": "ChatGPT saved memories and custom instructions",
  "content_type": "memory",
  "created_at": null,
  "modified_at": "2026-10-17T00:00:00Z",
  "ingested_at": "2026-10-18T04:00:18Z",
  "path": "authentic/assistant-memory/chatgpt.md",
  "source_url": "https://chatgpt.com/#settings/Personalization",
  "content_hash": "sha256:2b67…8d",
  "library_item_id": null,
  "metadata": {
    "format": "md",
    "language": "en",
    "assistant": "chatgpt",
    "memory_entries": 37,
    "custom_instructions": true,
    "read_from": "settings page, no prompt sent"
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart",
      "project_tutortrace",
      "project_idetrace"
    ],
    "notes": "One row, several projects."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `memory entry` (what `sample.unit` counts)
- **Engelbart today:** Connect builds `MEMORY.md` from what the assistants remember. The beta flow sends the profile prompt and deletes the chat; the benchmark reads settings pages instead and sends nothing. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - One item spanning several projects

</details>

</details>

#### Papers

<details>
<summary>Zotero</summary>

`zotero/`

- **Stored as:** Per item: `item.bib` (BibTeX), the attached PDF, and notes/annotations; `library.bib` per library; group libraries in their own folders
- **One source item =** one Zotero item with its attachments

**source_items row**

```json
{
  "id": "item_zotero_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "zotero",
  "source_id": "groups/6141877/items/ABCD1234",
  "title": "Developing an artificial intelligence literacy framework: Evaluation of a literacy course for senior secondary students using a project-based learning approach",
  "content_type": "paper",
  "created_at": "2026-07-02T18:30:00Z",
  "modified_at": "2026-07-02T18:31:00Z",
  "ingested_at": "2026-10-18T04:00:19Z",
  "path": "authentic/zotero/groups/6141877/ABCD1234/",
  "source_url": "https://www.zotero.org/groups/6141877/items/ABCD1234",
  "content_hash": "sha256:6095…77",
  "library_item_id": null,
  "metadata": {
    "format": "bibtex",
    "language": "en",
    "library": "group 6141877 (Sophia1)",
    "item_type": "journalArticle",
    "year": 2024,
    "collections": [
      "AI literacy"
    ],
    "files": [
      "item.bib",
      "attachment.pdf",
      "notes.md"
    ],
    "doi": null,
    "annotations": 4
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `page (PDF) / field (metadata)` (what `sample.unit` counts)
- **Engelbart today:** Synced local mirror at `~/.engelbart/.zotero`, group libraries included. `zotero_collections`, `zotero_items` (500 default, 2,000 max), `import_zotero_items` (300 per call). PDFs fetched on demand. Closest to complete. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Same paper in Zotero, Downloads and Drive
  - Item with no PDF attached

</details>

</details>

<details>
<summary>Overleaf</summary>

`overleaf/`

- **Stored as:** LaTeX project folder from the project zip: `.tex` files, `.bib`, figures, styles, plus the compiled PDF
- **One source item =** one project

**source_items row**

```json
{
  "id": "item_overleaf_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "overleaf",
  "source_id": "66a1f0c2e4b9d83a7c5e1f20",
  "title": "[UIST '26] Camera Ready TutorTrace",
  "content_type": "latex_project",
  "created_at": "2026-07-22T03:10:00Z",
  "modified_at": "2026-08-02T06:48:00Z",
  "ingested_at": "2026-10-18T04:00:20Z",
  "path": "authentic/overleaf/66a1f0c2e4b9d83a7c5e1f20/",
  "source_url": "https://www.overleaf.com/project/66a1f0c2e4b9d83a7c5e1f20",
  "content_hash": "sha256:b8bc…4f",
  "library_item_id": null,
  "metadata": {
    "format": "latex",
    "main_file": "main.tex",
    "file_count": 46,
    "tex_files": [
      "main.tex",
      "sections/intro.tex",
      "sections/taxonomy.tex",
      "sections/eval.tex"
    ],
    "bib_files": [
      "refs.bib"
    ],
    "compiled_pdf": "output.pdf",
    "owner": "me",
    "archived": false
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_tutortrace"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `line of <code>.tex</code>` (what `sample.unit` counts)
- **Engelbart today:** `overleaf_projects` scrapes the project list (`ol-prefetchedProjectsBlob`, cap 500). `import_overleaf_projects` downloads `/project/<id>/download/zip` (20 per call), saves the `.tex` with `\documentclass` (main.tex first) as a note and up to three PDFs. Needs approval. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Archived project
  - Several near-identical copies of the same paper (camera-ready, copy)

</details>

</details>

<details>
<summary>PDFs on the Mac</summary>

`pdfs/`

- **Stored as:** The `.pdf` copied as it is, under folders mirroring where it was found (Downloads, Desktop, iCloud…)
- **One source item =** one PDF file

**source_items row**

```json
{
  "id": "item_pdfs_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "pdfs",
  "source_id": "~/Downloads/_UIST_26___Camera_Ready__TutorTrace__…__Copy_-3.pdf",
  "title": "TutorTrace: A Dataset and Taxonomy for Classifying Learner Behavioral States during AI-Assisted Programming Education",
  "content_type": "pdf",
  "created_at": "2026-10-05T06:28:00Z",
  "modified_at": "2026-10-05T06:28:00Z",
  "ingested_at": "2026-10-18T04:00:21Z",
  "path": "authentic/pdfs/Downloads/_UIST_26___Camera_Ready__TutorTrace__…__Copy_-3.pdf",
  "source_url": null,
  "content_hash": "sha256:10ee…6d",
  "library_item_id": null,
  "metadata": {
    "format": "pdf",
    "folder": "~/Downloads",
    "size_bytes": 2841733,
    "pages": 14,
    "kind_guess": "paper",
    "pdf_title": "TutorTrace: A Dataset and Taxonomy for Classifying Learner Behavioral States during AI-Assisted Programming Education"
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_tutortrace"
    ],
    "notes": "Duplicate: same content as the -2 and -4 copies and the Overleaf compile."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `page` (what `sample.unit` counts)
- **Engelbart today:** `list_pdfs` (300 default, 1,000 max) with a paper / book / personal guess and an optional first-pages check (80 max), then `import_pdfs` (200 per call), tagged `paper`. No truncation signal. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Four copies of the same paper (`-2`, `-3`, `-4`)
  - Receipts and statements
  - Old but central paper

</details>

</details>

#### Code

<details>
<summary>GitHub</summary>

`github/`

- **Stored as:** A git clone per repo, plus `<repo>.repo.json` with the API metadata (owner, fork, parent, pushed_at)
- **One source item =** one repository

**source_items row**

```json
{
  "id": "item_github_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "github",
  "source_id": "Mathetic-PBC/engelbart-canvas",
  "title": "Mathetic-PBC/engelbart-canvas",
  "content_type": "repository",
  "created_at": "2026-08-30T19:02:00Z",
  "modified_at": "2026-10-17T23:58:00Z",
  "ingested_at": "2026-10-18T04:00:22Z",
  "path": "authentic/github/Mathetic-PBC/engelbart-canvas/",
  "source_url": "https://github.com/Mathetic-PBC/engelbart-canvas",
  "content_hash": "sha256:ee0c…9d",
  "library_item_id": null,
  "metadata": {
    "format": "git",
    "repo_json": "authentic/github/Mathetic-PBC/engelbart-canvas.repo.json",
    "owner": "Mathetic-PBC",
    "owner_type": "Organization",
    "private": true,
    "fork": false,
    "parent": null,
    "default_branch": "main",
    "pushed_at": "2026-10-17T23:58:00Z",
    "my_commits_in_window": null,
    "description": null,
    "readme_path": "README.md"
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `file (README first)` (what `sample.unit` counts)
- **Engelbart today:** `github_repos` pages through GitHub App installations, newest push first, but trims each repo to full name, URL, description and private flag. `shapeRepo` has `pushedAt` and owner; fork status isn't collected. Orgs without the App are silently missing. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Fork you built on
  - Org repo you never committed to
  - Old fork never pushed

</details>

</details>

#### Other

<details>
<summary>Websites</summary>

`websites/`

- **Stored as:** Saved page as a single `.html`, with the URL in the row
- **One source item =** one page

**source_items row**

```json
{
  "id": "item_websites_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "websites",
  "source_id": "https://maggieappleton.com/garden-history",
  "title": "A Brief History & Ethos of the Digital Garden",
  "content_type": "web_page",
  "created_at": null,
  "modified_at": "2026-10-17T06:24:00Z",
  "ingested_at": "2026-10-18T04:00:23Z",
  "path": "authentic/websites/maggieappleton.com/garden-history.html",
  "source_url": "https://maggieappleton.com/garden-history",
  "content_hash": "sha256:0d56…f1",
  "library_item_id": null,
  "metadata": {
    "format": "html",
    "language": "en",
    "saved_at": "2026-10-17T06:24:00Z",
    "found_via": [
      "links_in_notes",
      "browser-history"
    ],
    "word_count": 4100
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word` (what `sample.unit` counts)
- **Engelbart today:** `links_in_notes` returns the most-used links (200 default, 1,000 max) and the agent adds them with `add_to_library`. Stage pages are saved as html. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Same URL with tracking parameters (near-duplicate)
  - Shopping or news pages

</details>

</details>

<details>
<summary>Linear</summary>

`linear/`

- **Stored as:** One `.json` per issue in the API's shape (comments included); project documents as `.md`
- **One source item =** one issue, project or document

**source_items row**

```json
{
  "id": "item_linear_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "linear",
  "source_id": "MATH-92",
  "title": "Orchestrator agent that routes between Brainstorm and Discover",
  "content_type": "issue",
  "created_at": "2026-10-06T22:14:00Z",
  "modified_at": "2026-10-12T18:03:00Z",
  "ingested_at": "2026-10-18T04:00:24Z",
  "path": "authentic/linear/issues/MATH-92.json",
  "source_url": "https://linear.app/mathetic/issue/MATH-92",
  "content_hash": "sha256:865b…c6",
  "library_item_id": null,
  "metadata": {
    "format": "json",
    "language": "en",
    "team": "Mathetic",
    "project": "Engelbart",
    "state": "Backlog",
    "priority": 2,
    "labels": [],
    "comments": 3,
    "assignee": "me"
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_engelbart"
    ],
    "notes": ""
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `field / comment` (what `sample.unit` counts)
- **Engelbart today:** Official MCP server, read-only: `list_issues`, `list_projects`, `list_documents`, `list_teams`, `list_cycles`. The skill filters `list_issues` by words from the plan and drops old closed issues, so it searches rather than lists. Agent writes notes with `add_note`. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Closed issue older than the window that still matters

</details>

</details>

<details>
<summary>Browser history</summary>

`browser-history/`

- **Stored as:** Copies of each browser profile's database: Chrome/Brave `History` (SQLite) and `Bookmarks` (JSON), Safari `History.db` and `Bookmarks.plist`, Firefox `places.sqlite`
- **One source item =** one profile's history database (bookmarks alongside)

**source_items row**

```json
{
  "id": "item_browser-history_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "browser-history",
  "source_id": "chrome:Default:History",
  "title": "Chrome · Default profile history",
  "content_type": "history_db",
  "created_at": null,
  "modified_at": "2026-10-17T23:59:00Z",
  "ingested_at": "2026-10-18T04:00:25Z",
  "path": "authentic/browser-history/chrome/Default/History",
  "source_url": null,
  "content_hash": "sha256:af3b…e1",
  "library_item_id": null,
  "metadata": {
    "format": "sqlite",
    "browser": "chrome",
    "profile": "Default",
    "bookmarks_path": "authentic/browser-history/chrome/Default/Bookmarks",
    "url_rows": 48211,
    "visits_in_window": 131902
  },
  "ground_truth": {
    "status": "unlabeled",
    "project_ids": [],
    "notes": "Discovery source. Score it by whether the ids it points to get found, not as an import."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `visit / URL` (what `sample.unit` counts)
- **Engelbart today:** History and bookmarks tool, default 50 most-visited sites, Chromium only; Safari needs Full Disk Access. A discovery hint that feeds Drive, Overleaf and paper ids to the other importers. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - Drive file visited often but linked from nowhere else

</details>

</details>

<details>
<summary>Local notes and docs</summary>

`local-notes/`

- **Stored as:** Files copied as found: `.md`, `.txt`, `.docx`, `.html` outside Obsidian
- **One source item =** one file

**source_items row**

```json
{
  "id": "item_local-notes_001",
  "dataset_id": "benchmark_001",
  "provenance": "authentic",
  "source": "local-notes",
  "source_id": "~/Documents/spec design outline.docx",
  "title": "spec design outline",
  "content_type": "document",
  "created_at": "2026-06-18T05:40:00Z",
  "modified_at": "2026-06-21T22:12:00Z",
  "ingested_at": "2026-10-18T04:00:26Z",
  "path": "authentic/local-notes/Documents/spec design outline.docx",
  "source_url": null,
  "content_hash": "sha256:0e5a…6f",
  "library_item_id": null,
  "metadata": {
    "format": "docx",
    "language": "en",
    "folder": "~/Documents",
    "size_bytes": 48213,
    "word_count": 2900
  },
  "ground_truth": {
    "status": "reviewed",
    "project_ids": [
      "project_spec_design"
    ],
    "notes": "Invisible to list_note_files today (.docx isn't in NOTE_EXT)."
  }
}
```

<details>
<summary>Notes</summary>

- **Analysis unit:** `word` (what `sample.unit` counts)
- **Engelbart today:** `list_note_files` / `import_note_files`, which only accept `.md`, `.markdown`, `.txt` (`NOTE_EXT` in `readers.cjs`). `.docx` and `.html` are on the TODO, and the lister and importer have to change together. (from the Onboarding 3 code reading)
- **Hard cases to plant:**
  - `.docx` draft that today's lister can't see

</details>

</details>

</details>

<details>
<summary><b>Pipeline</b></summary>

### Stage 0: source rows

An import script per platform copies each original into `benchmark-data/`, hashes it and writes one `source_items` row per item, in code with no model, and leaves `library_item_id` null.

**source_items**

```json
{
  "source_items": [
    {
      "id": "item_001",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "chatgpt",
      "source_id": "6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
      "title": "Thoughts",
      "content_type": "conversation",
      "created_at": "2026-09-01T10:00:00Z",
      "modified_at": "2026-09-02T12:00:00Z",
      "ingested_at": "2026-10-18T04:00:00Z",
      "path": "authentic/chatgpt/item_001.json",
      "source_url": "https://chatgpt.com/c/6713f0a2-41c8-8003-9f1e-2b7d0c55a9e1",
      "content_hash": "sha256:a41f…01",
      "library_item_id": null,
      "metadata": {
        "format": "json",
        "language": "en",
        "message_count": 42,
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [
          "project_tutortrace"
        ],
        "notes": "Evaluation design for the guided/dependent help-seeking task."
      }
    },
    {
      "id": "item_002",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "google-docs",
      "source_id": "1Qx9fK3bT0aLm2…",
      "title": "Untitled document",
      "content_type": "document",
      "created_at": "2026-10-15T18:20:00Z",
      "modified_at": "2026-10-17T22:05:00Z",
      "ingested_at": "2026-10-18T04:00:02Z",
      "path": "authentic/google-docs/item_002.docx",
      "source_url": "https://docs.google.com/document/d/1Qx9fK3bT0aLm2…/edit",
      "content_hash": "sha256:b7c2…02",
      "library_item_id": null,
      "metadata": {
        "format": "docx",
        "language": "en",
        "word_count": 2310,
        "folder": "My Drive",
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [
          "project_engelbart_import"
        ],
        "notes": "Benchmark design draft."
      }
    },
    {
      "id": "item_003",
      "dataset_id": "benchmark_001",
      "provenance": "authentic",
      "source": "google-docs",
      "source_id": "1Zr0pL8wQe…",
      "title": "Lease renewal 2026",
      "content_type": "document",
      "created_at": "2026-06-03T09:12:00Z",
      "modified_at": "2026-06-03T09:40:00Z",
      "ingested_at": "2026-10-18T04:00:03Z",
      "path": "authentic/google-docs/item_003.docx",
      "source_url": "https://docs.google.com/document/d/1Zr0pL8wQe…/edit",
      "content_hash": "sha256:c9d0…03",
      "library_item_id": null,
      "metadata": {
        "format": "docx",
        "language": "en",
        "word_count": 640,
        "folder": "Personal",
        "tags": []
      },
      "ground_truth": {
        "status": "reviewed",
        "project_ids": [],
        "notes": "Personal. Belongs to no project."
      }
    }
  ]
}
```

<details>
<summary>Notes</summary>

Titles, dates and platform ids come straight from the export; missing values stay `null`. Listing an item never adds it to the library.

#### The three items followed through the pipeline

| id | source | title | what it really is (ground truth, hidden from the agent) |
|---|---|---|---|
| `item_001` | ChatGPT | "Thoughts" | TutorTrace evaluation design. The vague title is a deliberate hard case. |
| `item_002` | Google Drive | "Untitled document" | A draft of the Engelbart import benchmark. |
| `item_003` | Google Drive | "Lease renewal 2026" | Personal clutter that belongs to no project. |

Engelbart project being onboarded: `project_id = 7c1e…` ("Engelbart").

#### Fields in a source item

These come from the `source_items` JSON in the Gronola note, with `library_item_id` added afterward. Two more are additions on this page: `modeled_on` on synthetic items (the `/goal` manifest rule) and per-source keys inside `metadata`.

| field | meaning |
|---|---|
| `id` | internal id, stable across content changes |
| `provenance` | `authentic` or `synthetic` |
| `modeled_on` (addition) | synthetic only: the authentic item it imitates, or null |
| `source` / `source_id` | the subfolder name, and the platform's own id (conversation id, Drive file id, Overleaf project id, vault path…) |
| `content_type` | conversation, note, page, document, spreadsheet, email_thread, latex_project, paper, pdf, repository, issue, meeting, transcript, web_page, memory, history_db |
| `created_at` / `modified_at` | authentic: the original timestamps, never changed. Synthetic: generated, bursty across the year before 2026-10-17 |
| `path` | the stored file or folder, relative to `benchmark-data/`. The row holds metadata; the file holds the content |
| `content_hash` | hash of the stored content; updated when the content changes, with the old version kept |
| `library_item_id` | null until the deep pass imports the item |
| `metadata` | source-specific: format, folder, account, counts… Varies per tool (see the Sources tab) |
| `ground_truth` | hidden from the agent. `unlabeled` until reviewed; `reviewed` with empty `project_ids` means "belongs to no project" |

#### Project ids used as ground truth in the samples

`project_engelbart`, `project_engelbart_import`, `project_tutortrace`, `project_idetrace`, `project_custody_verification`, `project_berkeley`, `project_spec_design`. They are rows in `ground_truth_projects` (see the Dataset tab).

</details>

### Wave 1: category list

Wave 1 reads the chats cheaply, together with the profile and the person's own categories, and proposes the category list the person then confirms; it only reads.

**catset_v0: the user's typed categories plus the profile's projects**

```json
{
  "id": "catset_v0",
  "run_id": "run_001",
  "projects": [
    {
      "id": "project_engelbart",
      "label": "Engelbart",
      "description": "Research notebook, agents, onboarding.",
      "origin": "user"
    },
    {
      "id": "project_tutortrace",
      "label": "TutorTrace",
      "description": "Learner-behavior dataset and taxonomy (UIST '26).",
      "origin": "profile"
    }
  ]
}
```

**analysis_001 for item_001 (provisional)**

```json
{
  "id": "analysis_001",
  "item_id": "item_001",
  "run_id": "run_001",
  "parent_analysis_id": null,
  "category_set_id": "catset_v0",
  "content_hash": "sha256:a41f…01",
  "stage": "wave1_category_discovery",
  "status": "completed",
  "error": null,
  "started_at": "2026-10-18T04:01:00Z",
  "completed_at": "2026-10-18T04:01:04Z",
  "model": "REPLACE_WITH_MODEL_ID",
  "prompt_version": "wave1_discovery_v1",
  "config": {
    "sampling_strategy": "user_turns_digest",
    "max_input_tokens": 800
  },
  "sample": {
    "metadata_fields_read": [
      "title",
      "created_at",
      "modified_at"
    ],
    "unit": "message",
    "index_base": 0,
    "range_end": "exclusive",
    "ranges": [
      {
        "start": 0,
        "end": 1
      },
      {
        "start": 40,
        "end": 41
      }
    ],
    "digest": "first sentence of each user turn, 400 chars",
    "units_read": 2,
    "total_units": 42,
    "coverage_fraction": 0.047619,
    "input_snapshot_path": "runs/run_001/inputs/item_001.txt"
  },
  "result": {
    "project_assignments": [
      {
        "project_id": "project_tutortrace",
        "confidence": 0.55,
        "evidence": [
          {
            "unit": "message",
            "index": 0,
            "quote": "ok so for the help-seeking classifier, how do we validate the labels"
          }
        ]
      }
    ],
    "proposed_projects": [
      {
        "id": "project_engelbart_import",
        "label": "Engelbart import quality",
        "description": "Context import, benchmark, category sort.",
        "evidence_item_ids": [
          "item_017",
          "item_022"
        ]
      }
    ],
    "summary": "Validating labels for a help-seeking classifier.",
    "needs_deeper_read": true
  },
  "usage": {
    "input_tokens": 620,
    "output_tokens": 140,
    "cost_usd": null
  }
}
```

**catset_v2: confirmed**

```json
{
  "id": "catset_v2",
  "run_id": "run_001",
  "confirmed_at": "2026-10-18T04:06:30Z",
  "projects": [
    {
      "id": "project_engelbart",
      "label": "Engelbart",
      "description": "Research notebook, agents, onboarding.",
      "origin": "user"
    },
    {
      "id": "project_engelbart_import",
      "label": "Engelbart import quality",
      "parent_id": "project_engelbart",
      "description": "Context import, benchmark, category sort.",
      "origin": "wave1"
    },
    {
      "id": "project_tutortrace",
      "label": "TutorTrace",
      "description": "Learner-behavior dataset and taxonomy (UIST '26).",
      "origin": "profile"
    },
    {
      "id": "other",
      "label": "Other / new topic",
      "origin": "system"
    }
  ]
}
```

<details>
<summary>Notes</summary>

"Cheaply" means the title, the first user message, the last user message, and a digest of the person's turns. Any assignments wave 1 makes along the way are provisional.

The title "Thoughts" gives the agent nothing. The opening message alone puts `item_001` under TutorTrace, at medium confidence, and flags it for a deeper read.

Merging the proposals from all wave 1 analyses gives `catset_v1`, a draft. The person confirms it with one edit, making "Engelbart import quality" a sub-topic of Engelbart. Everything after this point runs against the result, `catset_v2`.

</details>

### Wave 2: shallow pass

Wave 2 runs concurrently over Drive, Gmail, notes, PDFs and the rest, reading metadata and a short snippet against `catset_v2`, and the person then picks which categories go to the deep pass.

**analyses**

```json
[
  {
    "id": "analysis_002",
    "item_id": "item_002",
    "run_id": "run_001",
    "parent_analysis_id": null,
    "category_set_id": "catset_v2",
    "content_hash": "sha256:b7c2…02",
    "stage": "wave2_shallow",
    "status": "completed",
    "error": null,
    "started_at": "2026-10-18T04:07:10Z",
    "completed_at": "2026-10-18T04:07:13Z",
    "model": "REPLACE_WITH_MODEL_ID",
    "prompt_version": "wave2_shallow_v1",
    "config": {
      "sampling_strategy": "head_words",
      "max_input_tokens": 600
    },
    "sample": {
      "metadata_fields_read": [
        "title",
        "folder",
        "modified_at"
      ],
      "unit": "word",
      "index_base": 0,
      "range_end": "exclusive",
      "ranges": [
        {
          "start": 0,
          "end": 300
        }
      ],
      "units_read": 300,
      "total_units": 2310,
      "coverage_fraction": 0.12987,
      "input_snapshot_path": "runs/run_001/inputs/item_002.txt"
    },
    "result": {
      "project_assignments": [
        {
          "project_id": "project_engelbart_import",
          "confidence": 0.7,
          "evidence": [
            {
              "unit": "word",
              "index": 41,
              "quote": "personas: founder with many projects, single-project user"
            }
          ]
        }
      ],
      "proposed_projects": [],
      "summary": "Draft plan for a benchmark of context import.",
      "needs_deeper_read": true
    },
    "usage": {
      "input_tokens": 480,
      "output_tokens": 110,
      "cost_usd": null
    }
  },
  {
    "id": "analysis_003",
    "item_id": "item_003",
    "run_id": "run_001",
    "parent_analysis_id": null,
    "category_set_id": "catset_v2",
    "content_hash": "sha256:c9d0…03",
    "stage": "wave2_shallow",
    "status": "completed",
    "error": null,
    "started_at": "2026-10-18T04:07:10Z",
    "completed_at": "2026-10-18T04:07:11Z",
    "model": null,
    "prompt_version": "wave2_free_signals_v1",
    "config": {
      "sampling_strategy": "metadata_only"
    },
    "sample": {
      "metadata_fields_read": [
        "title",
        "folder"
      ],
      "unit": "word",
      "units_read": 0,
      "total_units": 640,
      "coverage_fraction": 0.0,
      "input_snapshot_path": null
    },
    "result": {
      "project_assignments": [],
      "proposed_projects": [],
      "summary": "Personal folder, lease document.",
      "decided_by": "free_signal: folder=Personal",
      "needs_deeper_read": false
    },
    "usage": {
      "input_tokens": 0,
      "output_tokens": 0,
      "cost_usd": null
    }
  }
]
```

<details>
<summary>Notes</summary>

For these two Drive items the snippet is the title, the folder and the first ~300 words.

`item_003` was settled by a free signal (its folder), with no model call. It still gets an analysis row, so the report can count it as "looked at, none". Wave 2 examines irrelevant material too, and examining an item doesn't import it.

#### What the person sees and picks

| category | items | picked |
|---|---|---|
| TutorTrace | 1 (item_001) | yes |
| Engelbart › import quality | 1 (item_002) | yes |
| none | 1 (item_003) | — |

</details>

### Deep pass

The deep pass reads the whole of each item in a picked category, revises the assignment, and on import inserts or reuses a library row and writes `library_item_id` back to the source row.

**analyses (parent_analysis_id points at the shallow row)**

```json
[
  {
    "id": "analysis_004",
    "item_id": "item_001",
    "run_id": "run_001",
    "parent_analysis_id": "analysis_001",
    "category_set_id": "catset_v2",
    "content_hash": "sha256:a41f…01",
    "stage": "deep",
    "status": "completed",
    "error": null,
    "started_at": "2026-10-18T04:09:00Z",
    "completed_at": "2026-10-18T04:09:21Z",
    "model": "REPLACE_WITH_MODEL_ID",
    "prompt_version": "deep_v1",
    "config": {
      "sampling_strategy": "full",
      "max_input_tokens": 24000
    },
    "sample": {
      "metadata_fields_read": [
        "title",
        "created_at",
        "modified_at"
      ],
      "unit": "message",
      "index_base": 0,
      "range_end": "exclusive",
      "ranges": [
        {
          "start": 0,
          "end": 42
        }
      ],
      "units_read": 42,
      "total_units": 42,
      "coverage_fraction": 1.0,
      "input_snapshot_path": "runs/run_001/inputs/item_001.deep.txt"
    },
    "result": {
      "project_assignments": [
        {
          "project_id": "project_tutortrace",
          "confidence": 0.93,
          "evidence": [
            {
              "unit": "message",
              "index": 0,
              "quote": "ok so for the help-seeking classifier, how do we validate the labels"
            },
            {
              "unit": "message",
              "index": 21,
              "quote": "guided vs dependent, held out by student not by session"
            }
          ]
        }
      ],
      "proposed_projects": [],
      "summary": "Label validation and held-out split for TutorTrace's guided/dependent task.",
      "needs_deeper_read": false,
      "decision": "import",
      "library_action": {
        "op": "insert",
        "library_item_id": "e2a8…11"
      }
    },
    "usage": {
      "input_tokens": 9800,
      "output_tokens": 260,
      "cost_usd": null
    }
  },
  {
    "id": "analysis_005",
    "item_id": "item_002",
    "run_id": "run_001",
    "parent_analysis_id": "analysis_002",
    "category_set_id": "catset_v2",
    "content_hash": "sha256:b7c2…02",
    "stage": "deep",
    "status": "completed",
    "error": null,
    "started_at": "2026-10-18T04:09:00Z",
    "completed_at": "2026-10-18T04:09:14Z",
    "model": "REPLACE_WITH_MODEL_ID",
    "prompt_version": "deep_v1",
    "config": {
      "sampling_strategy": "full",
      "max_input_tokens": 24000
    },
    "sample": {
      "metadata_fields_read": [
        "title",
        "folder",
        "modified_at"
      ],
      "unit": "word",
      "index_base": 0,
      "range_end": "exclusive",
      "ranges": [
        {
          "start": 0,
          "end": 2310
        }
      ],
      "units_read": 2310,
      "total_units": 2310,
      "coverage_fraction": 1.0,
      "input_snapshot_path": "runs/run_001/inputs/item_002.deep.txt"
    },
    "result": {
      "project_assignments": [
        {
          "project_id": "project_engelbart_import",
          "confidence": 0.95,
          "evidence": [
            {
              "unit": "word",
              "index": 1204,
              "quote": "score omissions, commissions and duplicates per persona"
            }
          ]
        }
      ],
      "proposed_projects": [],
      "summary": "Benchmark design: personas, scoring and synthetic data.",
      "needs_deeper_read": false,
      "decision": "import",
      "library_action": {
        "op": "insert",
        "library_item_id": "f3b9…22"
      }
    },
    "usage": {
      "input_tokens": 3900,
      "output_tokens": 210,
      "cost_usd": null
    }
  }
]
```

**source_items after the deep pass: only library_item_id changes**

```json
[
  {
    "id": "item_001",
    "library_item_id": "e2a8…11"
  },
  {
    "id": "item_002",
    "library_item_id": "f3b9…22"
  },
  {
    "id": "item_003",
    "library_item_id": null
  }
]
```

<details>
<summary>Notes</summary>

Compare `analysis_001` with `analysis_004`. Both the category set (`catset_v0` → `catset_v2`) and the reading depth changed, and `category_set_id` is what separates the two causes. Here the category itself didn't change, so the rise from 0.55 to 0.93 came from the deeper read.

Writing `library_item_id` back is what keeps a retry from creating a second library row.

</details>

</details>

<details>
<summary><b>Library</b></summary>

### Before the deep pass

No `library` rows for these items. Stage 0, wave 1 and wave 2 add only `analyses` rows.

### After the deep pass

One column per new `library` row; `item_003` was looked at and never imported.

| column | `e2a8…11` | `f3b9…22` |
|---|---|---|
| id | `e2a8…11` | `f3b9…22` |
| name | Thoughts | Untitled document |
| type | md | md |
| path | `~/.engelbart/assets/md/e2a8…11/Thoughts.md` | `~/.engelbart/assets/md/f3b9…22/Untitled document.md` |
| project_id | `7c1e…` | `7c1e…` |
| source | ChatGPT | Google Docs |
| category | chat | document |
| item_date | 2026-09-02 | 2026-10-17 |
| origin_url | `https://chatgpt.com/c/6713f0a2…` | `https://docs.google.com/document/d/1Qx9fK3bT0aLm2…/edit` |
| place | null | My Drive |
| messages | 42 | null |
| tags | `{}` | `{}` |

### library_categories

A proposed join table, not in the code: `library.project_id` is the Engelbart project, so linking a row to one or more categories needs a separate table.

| library_item_id | category_id | category_set_id | analysis_id |
|---|---|---|---|
| `e2a8…11` | project_tutortrace | catset_v2 | analysis_004 |
| `f3b9…22` | project_engelbart_import | catset_v2 | analysis_005 |

<details>
<summary>Notes</summary>

Library columns are copied from `LIBRARY_SCHEMA` in `src/main/store/db.cjs`; unlisted columns are null or their default. The link back to the app goes in `origin_url`, not `url`, following the comment in `db.cjs`.

#### What each source becomes in the library

When the deep pass imports an item, today's import tools decide its library shape:

| source | library entry today |
|---|---|
| ChatGPT, Claude | one Markdown file of the chat's turns, named by title (`import_web_chats`) |
| Claude Code, Codex | one Markdown file of what you asked and what the assistant answered (`import_chats`) |
| Overleaf | the unzipped project folder, the main `.tex` saved as a note, and up to three compiled PDFs |
| Google Drive | Docs as Markdown with pictures, Sheets as a CSV table (first tab only), Slides as text, other files as they are |
| Gmail | one note per thread, messages in order, attachment names only |
| Apple Notes | one Markdown note per note, pictures saved |
| PDFs | the PDF as a file, tagged `paper` when it looks like one |
| GitHub | a `folder` row tagged `git` |
| Granola, Linear, Notion, Evernote | notes the agent writes itself with `add_note`; no import-by-id tool yet |

#### Rules the example relies on

- **Only the deep pass writes to the library.** Stage 0, wave 1 and wave 2 only add `analyses` rows.
- **Reuse before insert.** If `library_item_id` is already set, or a library row already matches the item's `origin_url` or file, the deep pass links that row (`"op": "reuse"`) instead of inserting.
- **One library row per item, whatever its categories.** An item in two categories gets one row and two `library_categories` links.
- **Unsure stays pending.** A deep pass that ends below the confidence threshold sets `"decision": "pending"`, writes nothing to the library, and the item appears in the "unsure" group.
- **`ground_truth` never reaches the agent.** The benchmark compares it with the final decision and assignments afterward.

#### End-of-run report for this example

| found | looked at | brought in | skipped | unsure |
|---|---|---|---|---|
| 3 | 3 | 2 | 1 (item_003, none) | 0 |

</details>

</details>
