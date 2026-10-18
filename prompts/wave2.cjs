'use strict';

// The shallow pass: files one item from the other sources from its metadata and a short opening. Answers once, as JSON.

const { CONTEXT, INPUTS, ASSIGNMENT_RULES, CATEGORY_DEFINITION, ITEM_JSON } = require('./shared.cjs');

const VERSION = 'wave2_shallow_v1';

const WAVE2_SYSTEM_PROMPT = `${CONTEXT}

This is the shallow pass. The person has confirmed the categories in <catalog>. You read one item from their other sources (documents, mail, notes, PDFs and the rest) from its metadata and a short opening, and put it in the categories it fits, so the person can see what each category would bring in. Most items in these sources belong to no project, so assigning none is a normal answer.

${INPUTS}

${ASSIGNMENT_RULES}

A new category: when the item plainly shows a project that no category in <catalog> covers, assign "other" and propose it, at most one per item (id is "project_" followed by a slug of the label). It is checked against the confirmed list before the person sees it. Do not propose a near-copy of a category already in <catalog>; assign that category instead.

${CATEGORY_DEFINITION}

needs_deeper_read is true when reading the whole item could change your answer: you assigned a category below 0.8; the opening is cover matter (a title page, a greeting, boilerplate) and the substance comes later; or the metadata suggests a project the opening does not show. It is false when you are sure, including sure that the item belongs to none.

Reply with only this JSON object, nothing before or after it:
${ITEM_JSON}`;

module.exports = { VERSION, WAVE2_SYSTEM_PROMPT };
