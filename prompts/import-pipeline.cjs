'use strict';

// The import pipeline's model calls: the first pass (builds the category list), the catalog merge, the shallow pass
// and the deep pass. Each answers once, as JSON. Code fills in ids, sample, usage, evidence units and library_action,
// and records the version below as prompt_version on every analysis row.

const VERSIONS = {
  wave1: 'wave1_discovery_v1',
  merge: 'catalog_merge_v1',
  wave2: 'wave2_shallow_v1',
  deep: 'deep_v1',
};

const CONTEXT = 'Engelbart is a research notebook. A person is bringing their work into it from the apps they use: chats, documents, mail, notes, code and papers. Items are sorted into categories, which are the projects the person works on. The person sees the categories and picks which to bring in, and only items in picked categories are imported.';

// What a category is. Used by every call that names or proposes one.
const CATEGORY_DEFINITION = `What a category is:
- A body of work with a goal: a study, a paper, a thesis chapter, a product, a course, a grant. Not a tool or app ("Zotero", "Claude Code"), a file type, a time period, a chore, or a theme so broad it fits everything ("AI", "research", "coding").
- Personal life (health, money, housing, travel, shopping, family) is never a category. Neither is Engelbart's own setup.
- Its label is 2 to 6 words, in the person's own terms: the name they use, or a repository's name made readable. No dates, no file extensions, no quotes.
- Its description is one plain sentence of at most 20 words: what it is and what it is for.`;

// When two categories are the same. Shared by the merge call, the check on new topics, and the librarian's edits.
const MERGE_RULES = `When two categories meet, decide one of three:
- Same project: merge them. They share one goal, and the person would call them the same work under different names (a repository's name and the paper's title; "Engelbart" and "Engelbart app").
- Part of a project: make the smaller one a sub-topic, with parent_id set to the larger. Use this when it is a distinct strand of the larger work and every item in it would also make sense under the parent ("Engelbart import quality" under "Engelbart"). One level only: a sub-topic has no sub-topics.
- Related but separate: keep both. They share a dataset, a method or people, but each has its own goal and output. Two papers from one dataset are two projects.
When unsure between merging and keeping separate, keep them separate and name the pair in unsure. A merge the person confirms costs them one click; a wrong merge hides a project.

Fixed categories (the person's own, and any already confirmed) keep their id, label, description and parent_id. Never merge a fixed category into another, rename it, or make it a sub-topic. Other categories can be merged into a fixed one or placed under it.`;

// How to put one item in categories. Shared by the first pass, the shallow pass and the deep pass.
const ASSIGNMENT_RULES = `Putting the item in categories:
- Assign it to every category in <catalog> it plainly belongs to: usually one, sometimes two. Assign none when it belongs to no project, or is personal.
- Judge from what the item says, not only its title. Titles like "Thoughts" or "Untitled document" tell you nothing.
- confidence is how sure you are the item belongs there: 0.9 or more when the item names the project or its unmistakable specifics; about 0.7 when several cues agree; about 0.5 on a single cue. Do not assign below 0.4.
- Give each assignment 1 to 3 pieces of evidence. index is the bracketed number of the unit you quote; quote is copied exactly from that unit, at most 25 words. Never quote text that is not in <sample>.
- Use only category ids that are in <catalog>.
- summary: one plain sentence of at most 15 words on what the item is about, not which category it is in.`;

const INPUTS = `You are given:
- <catalog>: the categories so far, as JSON: id, label, description, and parent_id for a sub-topic.
- <item>: the item's source, title, type, dates and other metadata.
- <sample>: the part of the item you may read, as units (messages, words or lines; its unit attribute says which). Each unit starts with its index in brackets: [0], [1], and so on. Gaps in the numbering are parts you were not given; its coverage attribute says how much of the item you have.`;

const ITEM_JSON = '{"project_assignments":[{"project_id":"...","confidence":0.0,"evidence":[{"index":0,"quote":"..."}]}],"proposed_projects":[{"id":"project_...","label":"...","description":"...","parent_id":"..."}],"summary":"...","needs_deeper_read":true}';

const WAVE1_SYSTEM_PROMPT = `${CONTEXT}

This is the first pass, which builds the category list. You read one item from the person's core sources (a chat, a coding session, a repository, a paper project) cheaply, and do two things: put it in the categories it fits, and propose a category when the item shows a project the catalog is missing. Your assignments are provisional. Your proposals matter more.

${INPUTS}

${ASSIGNMENT_RULES}

Proposing a category:
- Propose one only when the item shows work that is a project and no category in <catalog> covers it, not even as a sub-topic. Propose at most one per item, and none when you are unsure the work is a project.
- id is "project_" followed by a short lowercase slug of the label.
- When the item fits an existing category but is a distinct strand of it, propose the strand with parent_id set to that category, and also assign the item to the parent.
- Leave parent_id out of a proposal that has no parent.

${CATEGORY_DEFINITION}

needs_deeper_read is true when reading more of the item could change your answer: the sample is thin, the cues disagree, or your best confidence is under 0.8.

Reply with only this JSON object, nothing before or after it:
${ITEM_JSON}`;

const MERGE_SYSTEM_PROMPT = `${CONTEXT}

You combine the categories proposed from several sources into one list the person will confirm. Each source proposed its own, so the same project often appears several times under different names, and a strand of one project can appear as if it were its own.

You are given:
- <fixed>: categories you must keep as they are (the person's own, and any already confirmed), as JSON: id, label, description, origin, and parent_id for a sub-topic.
- <proposals>: every other proposal, as JSON: key (unique), id, label, description, parent_id when it was proposed as a sub-topic, source (profile, chats, coding sessions, repositories, and so on), items (how many items proposed it) and titles (a few of those items' titles).

${CATEGORY_DEFINITION}

${MERGE_RULES}

Build the list:
- Start from <fixed>. Then take each proposal and decide: merge it into a category on the list, place it under one as a sub-topic, add it as its own category, or drop it because it is plainly not a project (a tool, a theme, personal life, Engelbart's own setup).
- A merged category keeps the id of its fixed member, or else the id of the member proposed by the most items. Its label is the clearest of its members' labels, in the person's terms. Write a new description only when none of the members' descriptions fits the merged whole.
- origin: a fixed category keeps its own. Otherwise use "profile" when the profile proposed it, else the source of the member proposed by the most items.
- merged_from lists the keys of every proposal that went into a category. Every proposal key appears exactly once: either in one category's merged_from, or in dropped.
- Aim for the categories the person would name if asked what they work on. Do not split one project by phase (writing, analysis) or by app unless the person did.
- End the list with {"id":"other","label":"Other / new topic","origin":"system","merged_from":[]}.
- unsure lists the pairs you kept apart but could see as one project, and the sub-topics you placed but could see as separate. a and b are category ids or proposal keys; why is at most 12 words. Name each pair once.

Reply with only this JSON object, nothing before or after it:
{"projects":[{"id":"...","label":"...","description":"...","origin":"...","parent_id":"...","merged_from":["..."]}],"dropped":[{"key":"...","why":"..."}],"unsure":[{"a":"...","b":"...","why":"..."}]}`;

const WAVE2_SYSTEM_PROMPT = `${CONTEXT}

This is the shallow pass. The person has confirmed the categories in <catalog>. You read one item from their other sources (documents, mail, notes, PDFs and the rest) from its metadata and a short opening, and put it in the categories it fits, so the person can see what each category would bring in. Most items in these sources belong to no project, so assigning none is a normal answer.

${INPUTS}

${ASSIGNMENT_RULES}

A new category: when the item plainly shows a project that no category in <catalog> covers, assign "other" and propose it, at most one per item (id is "project_" followed by a slug of the label). It is checked against the confirmed list before the person sees it. Do not propose a near-copy of a category already in <catalog>; assign that category instead.

${CATEGORY_DEFINITION}

needs_deeper_read is true when reading the whole item could change your answer: you assigned a category below 0.8; the opening is cover matter (a title page, a greeting, boilerplate) and the substance comes later; or the metadata suggests a project the opening does not show. It is false when you are sure, including sure that the item belongs to none.

Reply with only this JSON object, nothing before or after it:
${ITEM_JSON}`;

const DEEP_SYSTEM_PROMPT = `${CONTEXT}

This is the deep pass, the last check before anything is imported. The person picked the categories they want, and an earlier, shallower read put this item in one or more of them. You read the whole item, or as much as <sample>'s coverage says, and decide whether it really belongs.

${INPUTS}
- <earlier>: the earlier read's assignments and summary, and which categories in <catalog> the person picked (picked="true").

${ASSIGNMENT_RULES}
- Judge afresh from what you read now. The earlier read saw only part of the item and may be wrong: raise, lower, add or remove assignments as the item shows.

decision:
- "import" when you assign at least one picked category at 0.8 or more.
- "skip" when the item belongs to no picked category, either because it belongs elsewhere or because it belongs to no project.
- "pending" when it may belong to a picked category but even the whole item does not get you to 0.8. The person decides those.
Do not propose categories here.

Reply with only this JSON object, nothing before or after it:
{"project_assignments":[{"project_id":"...","confidence":0.0,"evidence":[{"index":0,"quote":"..."}]}],"summary":"...","decision":"import"}`;

module.exports = {
  VERSIONS,
  CATEGORY_DEFINITION,
  MERGE_RULES,
  ASSIGNMENT_RULES,
  WAVE1_SYSTEM_PROMPT,
  MERGE_SYSTEM_PROMPT,
  WAVE2_SYSTEM_PROMPT,
  DEEP_SYSTEM_PROMPT,
};
