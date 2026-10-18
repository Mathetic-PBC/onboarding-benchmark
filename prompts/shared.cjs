'use strict';

// Pieces the import pipeline's prompts share: the opening context, what a category is, when two categories are the
// same, how to assign an item, the inputs an item call gets, and the item reply's shape. A change here changes every
// prompt that uses it, so bump those prompts' versions too.

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

module.exports = { CONTEXT, CATEGORY_DEFINITION, MERGE_RULES, ASSIGNMENT_RULES, INPUTS, ITEM_JSON };
