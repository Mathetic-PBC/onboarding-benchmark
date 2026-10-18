---
name: deep-pass-v1
description: Read an item more fully, confirm or revise its categories, and decide whether it should be imported.
---

# Deep pass

You get:
- categories: the confirmed category list.
- selected: the category ids the person chose to import.
- shallow: this item's shallow-sort result (assignments, confidence, summary).
- item: the item's metadata and a much fuller sample (or all of it), with numbered units. For folder items, each unit also names the file it came from.

Re-judge the item from the fuller text. Don't anchor on the shallow result.

Rules
- Look for the whole arc: where the item starts, where it ends up, and any long passage that changes its topic.
- Revise assignments if the fuller text says otherwise, and say why in one line.
- Evidence quotes must be exact, with unit index (and file for folder items).
- Decide:
  - "import": it belongs to at least one selected category with confidence 0.7+.
  - "skip": it belongs to no selected category.
  - "pending": still unclear, or a selected category is only weakly supported. The person reviews these.
- You only decide. Code creates or reuses the library entry.

Return JSON only:
{
  "item_id": "...",
  "project_assignments": [
    { "project_id": "cat_...", "confidence": 0.0,
      "evidence": [ { "unit": "message", "index": 0, "file": null, "quote": "exact text" } ] } ],
  "changed_from_shallow": true,
  "change_reason": "one line, or null",
  "proposed_projects": [],
  "summary": "one line",
  "decision": "import | skip | pending"
}
