# Import dedupe rules (draft, 2026-09-03)

Principle: dedupe copies, never dedupe sources.

## Files and papers
1. Same bytes (sha256) → one file; keep every location as provenance.
2. Same DOI, or same arXiv id ignoring version → one work; files become versions.
3. Normalized title similarity >= 0.92 + same first-author last name + year within ±1 → proposed version group, confidence: inferred.
4. Never merge versions into one file. Show "2 versions" on the paper.
5. Metadata for loose PDFs: XMP → PDF info dict → page-1 text (largest block = title; arXiv margin stamp regex).

Test case: Ostrowski et al. 2025, "Productive Struggle or Silent Stalling?" — arXiv v1 in ~/Downloads, L@S camera-ready in Zotero. Expected: one paper, 2 versions.

## Chats
- Same tool + same conversation id → one item; newer updated_at wins; record each arrival path (export zip, browser session).
- Different tools → never dedupe.
- ChatGPT branches → hidden parts of one item (current branch is the item).
- Project chats → separate items with parent_id = project; don't double count chats that also appear in the project's conversation list.

## Messages with files (Slack, Gmail)
- Message and attachment are separate items.
- Attachment goes through the file rules; a byte match adds a provenance edge, not a new item.

## Reporting
- After every import, per source: found / imported / merged / versioned / skipped.
