'use strict';

// The deep pass: rereads an item in full and decides import, skip or pending. Answers once, as JSON.

const { CONTEXT, INPUTS, ASSIGNMENT_RULES } = require('./shared.cjs');

const VERSION = 'deep_v1';

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

module.exports = { VERSION, DEEP_SYSTEM_PROMPT };
