# benchmark-data

Benchmark for Engelbart's context import: one person's digital footprint (`authentic/`, real data) plus synthetic data about the same person (`synthetic/`). Collection status is in `PROGRESS.md`. Everything that could not be collected or filled in is in `FAILURES.md`. Each tool folder keeps its own `MANIFEST.csv` (one row per collected file) and a `source_items.json` (that folder's slice of the table below).

## Tables

Each table is a JSON array of rows at the top of this folder.

| file | what it is for |
|---|---|
| `datasets.json` | One row per benchmark dataset: id, reference date, and the path to the person description. |
| `source_items.json` | One row per importable item (a chat, an email, a document, a coding session, a repo, …). Holds path, source, provenance (authentic/synthetic), dates, content hash and metadata, plus the item's ground-truth label. Built from the per-folder manifests by `_scripts/build_source_items.py`. |
| `ground_truth_projects.json` | The answer key: the person's real projects, plus `project_none` for items that belong to no project. Rows start as `"status": "draft"` and become `"reviewed"` once David checks them. |
| `generated_categories.json` | One row per category set the import agent generates in wave 1 of a benchmark run (`catset_<n>`). Empty until runs happen. |
| `analyses.json` | One row per analysis the import agent produces for one item in one run (classification, deep analysis, …). Empty until runs happen. |

## How they link

```
source_items.dataset_id               → datasets.id
source_items.ground_truth.project_ids → ground_truth_projects.id
analyses.item_id                      → source_items.id
analyses.category_set_id              → generated_categories.id
```

(`ground_truth_projects.dataset_id` and `generated_categories.dataset_id` also point to `datasets.id`.)

## Hidden from the agent under test

**`ground_truth_projects.json`, the `ground_truth` object on every source item, and `synthetic/ground_truth_labels.json` (the generator's labels for synthetic items) must never be shown to the import agent being benchmarked.** Give the agent only the item files themselves (or source items with `ground_truth` removed). Scoring compares the agent's output against these fields afterwards.

## Row shapes

`datasets.json`
```json
{ "id": "benchmark_001", "reference_date": "2026-10-17", "person_path": "synthetic/PERSON.md", "description": "…" }
```

`source_items.json`
```json
{ "id": "item_000123", "dataset_id": "benchmark_001", "provenance": "authentic|synthetic", "source": "gmail",
  "source_id": "…", "title": "…", "content_type": "email_thread|conversation|document|…",
  "created_at": "ISO-8601 UTC", "modified_at": "ISO-8601 UTC", "ingested_at": "ISO-8601 UTC",
  "path": "authentic/gmail/…", "source_url": "… or null", "content_hash": "sha256:…",
  "library_item_id": null,
  "modeled_on": "… (synthetic rows only, copied from the manifest)",
  "metadata": { "format": "eml", "language": "en|null", "message_count": 3, "tags": [], "parts": ["…"], "collection_notes": "…" },
  "ground_truth": { "status": "unlabeled", "project_ids": [], "notes": null } }
```
- An item is one unit an importer should bring in. Multi-file items list their files in `metadata.parts` and hash them together: a Gmail thread holds one .eml per message, a Claude Code session holds its subagent and tool-result files, and a Claude project holds its documents.
- `library_item_id` is null until Engelbart imports the item; it then holds the id of the resulting library item.
- `ground_truth.status` is exactly one of:
  - `unlabeled`: the default for authentic items.
  - `generated`: a synthetic item whose `project_ids` were set by the generator. `build_source_items.py` takes them from `synthetic/ground_truth_labels.json`.
  - `reviewed`: checked by David. Set by hand; rebuilds never overwrite a reviewed label.

`ground_truth_projects.json`
```json
{ "id": "project_<slug>", "dataset_id": "benchmark_001", "name": "…", "description": "one line", "status": "draft|reviewed" }
```

`generated_categories.json`
```json
{ "id": "catset_<n>", "run_id": "…", "dataset_id": "benchmark_001",
  "categories": [ { "id": "…", "name": "…", "description": "…" } ], "created_at": "…" }
```

`analyses.json`. One row per stage of the import agent's work on one item in one run.
```json
{ "id": "…", "item_id": "item_000123", "run_id": "…", "dataset_id": "benchmark_001",
  "parent_analysis_id": "… or null", "category_set_id": "catset_<n>", "content_hash": "sha256:… (of the item as analysed)",
  "stage": "wave1_category_discovery|wave2_shallow|deep", "status": "…", "error": null,
  "started_at": "…", "completed_at": "…", "model": "…", "prompt_version": "…", "config": { },
  "sample": { "metadata_fields_read": [], "unit": "…", "index_base": 0, "range_end": 0, "ranges": [],
              "units_read": 0, "total_units": 0, "coverage_fraction": 0.0, "input_snapshot_path": "…" },
  "result": { "project_assignments": [ { "project_id": "…", "confidence": 0.0,
                                         "evidence": [ { "unit": "…", "index": 0, "quote": "…" } ] } ],
              "proposed_projects": [], "summary": "…", "needs_deeper_read": false, "decision": "…", "library_action": "…" },
  "usage": { "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0 } }
```
