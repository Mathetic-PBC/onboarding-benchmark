'use strict';

// The first pass: reads one item from the core sources cheaply, assigns it, and proposes categories the catalog is missing. Answers once, as JSON.

const { CONTEXT, INPUTS, ASSIGNMENT_RULES, CATEGORY_DEFINITION, ITEM_JSON } = require('./shared.cjs');

const VERSION = 'wave1_discovery_v1';

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

module.exports = { VERSION, WAVE1_SYSTEM_PROMPT };
