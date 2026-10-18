---
tags: [engelbart, import, dedupe]
created: 2026-09-08
updated: 2026-10-15
---
# Engelbart: import dedupe

## the problem (from pilots)
- Priya's onboarding (10-09): same paper showed up twice, once from Zotero and once from ~/Downloads. she thought we were
  broken. also her Claude import missed ~140 chats
- Daniel's onboarding (10-13): no Notion/Granola importer at all, so nothing to dedupe there, but he asked why "Other" had
  both a PDF and the same PDF inside a zip
- my own test account: the Ostrowski paper appears as arXiv v1 PDF, camera-ready PDF, a .bib entry, a Slack file share, a Gmail
  attachment ([[Ostrowski2025 - Productive Struggle]])

## kinds of "duplicate"
| kind | example | what to do |
|---|---|---|
| byte-identical | same PDF in Downloads and ~/Desktop/papers | merge into one node, list both locations |
| same work, different version | arXiv v1 vs camera-ready | one *work* node, two *version* children, newest preferred for citing |
| same content, different container | PDF vs PDF inside a zip, email attachment | merge, keep the container as an origin |
| exported twice | Notion `.csv` and `_all.csv`, Evernote single note + notebook export | merge silently, but count both for "did we import everything" |
| near-duplicate drafts | doc v2, "copy of" | **don't merge**. Nelson was right, drafts are history ([[Nelson1965 - A File Structure for the Complex]]). group under one title |

## matching ladder (cheap → expensive)
1. sha256 of bytes
2. DOI / arXiv id from PDF metadata or first page text
3. normalized title + first author + year (lowercase, strip punctuation and LaTeX braces)
4. MinHash over text shingles, threshold ~0.9, for things without identifiers
5. only then ask the LLM, and only for borderline pairs, with both snippets shown

## things that bit us
- titles with `{LLM}` braces from BibTeX didn't match PDF titles until we stripped braces
- the zip case: we were hashing the zip, not its members
- Apple Notes exports truncate long titles with an ellipsis, so title matching against the same note elsewhere fails. use body
- recall is the thing pilots notice first. a missed item is worse than a duplicate. don't let dedupe eat real items

## todo
- [ ] write the version-children UI on the canvas (Hudson has a sketch)
- [x] log every merge decision with the reason so we can audit it
- [ ] benchmark: build a fake person with stuff spread across ~30 tools and measure omissions / wrong items / duplicates
