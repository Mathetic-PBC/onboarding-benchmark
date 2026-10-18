---
name: wave1-categories-v1
description: Build the category list of a person's work from their own words, before anything is sorted.
---

# Build the category list

You get some or all of these inputs:
- user_categories: categories the person typed themselves. Keep them exactly as written. Never rename, merge away or drop them.
- project: the project name and description entered at setup.
- profile_projects: project entries from an AI assistant's profile of the person. Treat them as a draft: useful for names and descriptions, but unchecked.
- chats: a list of chats (title, date, project, first user message).
- sessions: coding sessions (folder they ran in, title, first prompt).
- titles: repo names and paper titles.

Produce the list of distinct things this person works on.

Rules
- Use the level the person thinks in. One project is one category, even if it has many parts. Don't split it into sub-topics (its onboarding, its agents, its benchmark).
- A category needs evidence: several items, or one input the person wrote themselves. A single stray chat is not a category.
- Personal clutter (receipts, recipes, travel, one-off questions) is not a category. Leave it out; the sort files it as "none".
- If a profile project has no chats, sessions or titles behind it, keep it but flag it as "profile_only".
- If a group of chats or sessions matches no profile project, add it and flag it as "evidence_only".
- Merge near-duplicates (same work under two names) and keep the clearer name.
- Always include one "other" category for work that fits none of the above.
- Write each description in one line that would let someone else file an item correctly.

Return JSON only:
{
  "categories": [
    { "id": "cat_<slug>", "name": "...", "description": "one line",
      "source": "user | profile | evidence | merged",
      "flag": null | "profile_only" | "evidence_only",
      "evidence": ["chat or session titles that support it, up to 5"] }
  ]
}
