---
name: wave2-new-categories-v1
description: Check the new categories the shallow sort proposed against the confirmed list, and decide which ones to add.
---

# New categories from the shallow sort

You get:
- categories: the confirmed category list (id, name, description), including "other".
- proposals: every new category the shallow sort proposed, grouped by name. Each has a key, name, descriptions (as proposed), items (how many items proposed it), sources (which tools those items came from) and titles (a few of those items' titles).

The confirmed list came from what the person's assistants and coding history remember, so it can miss work that lives mostly in email, documents, papers or notes. These proposals are how that work gets found. Decide what each one is.

For every proposal, choose one:
- add: a real project or area of work that is missing from the list. Several proposals that name the same work become one new category.
- existing: the same work as a category already on the list, under another name. Give that category's id.
- drop: not a project (a tool, a theme, a one-off question, personal life, admin with no project behind it). Say why in at most 12 words.

Rules
- Use the level the person thinks in. One project is one category. Don't add a strand of an existing project as its own category.
- Merge proposals that name the same work (different names, spellings or scopes) and keep the clearest name.
- Don't drop a proposal only because few items back it. Code checks support after you answer.
- Write each new category's description in one line that would let someone else file an item correctly.
- Every proposal key appears exactly once: in one new category's merged_from, in existing, or in dropped.

Return JSON only:
{
  "add": [ { "id": "cat_<slug>", "name": "...", "description": "one line", "merged_from": ["key", "..."] } ],
  "existing": [ { "key": "...", "category_id": "cat_..." } ],
  "dropped": [ { "key": "...", "why": "..." } ]
}
