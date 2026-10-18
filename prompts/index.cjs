'use strict';

// The import pipeline's model calls: the first pass (builds the category list), the catalog merge, the shallow pass
// and the deep pass, one file each, with the pieces they share in shared.cjs. Code fills in ids, sample, usage,
// evidence units and library_action, and records each prompt's version (and its hash) on every analysis row.

const crypto = require('crypto');
const { CATEGORY_DEFINITION, MERGE_RULES, ASSIGNMENT_RULES } = require('./shared.cjs');
const wave1 = require('./wave1.cjs');
const merge = require('./merge.cjs');
const wave2 = require('./wave2.cjs');
const deep = require('./deep.cjs');

const VERSIONS = { wave1: wave1.VERSION, merge: merge.VERSION, wave2: wave2.VERSION, deep: deep.VERSION };

// A short hash of each prompt's full text: a change to a shared block changes the text without changing the version,
// and this is what shows it in a run's results.
const hash = (text) => crypto.createHash('sha256').update(text).digest('hex').slice(0, 12);
const HASHES = {
  wave1: hash(wave1.WAVE1_SYSTEM_PROMPT),
  merge: hash(merge.MERGE_SYSTEM_PROMPT),
  wave2: hash(wave2.WAVE2_SYSTEM_PROMPT),
  deep: hash(deep.DEEP_SYSTEM_PROMPT),
};

module.exports = {
  VERSIONS,
  HASHES,
  CATEGORY_DEFINITION,
  MERGE_RULES,
  ASSIGNMENT_RULES,
  WAVE1_SYSTEM_PROMPT: wave1.WAVE1_SYSTEM_PROMPT,
  MERGE_SYSTEM_PROMPT: merge.MERGE_SYSTEM_PROMPT,
  WAVE2_SYSTEM_PROMPT: wave2.WAVE2_SYSTEM_PROMPT,
  DEEP_SYSTEM_PROMPT: deep.DEEP_SYSTEM_PROMPT,
};
