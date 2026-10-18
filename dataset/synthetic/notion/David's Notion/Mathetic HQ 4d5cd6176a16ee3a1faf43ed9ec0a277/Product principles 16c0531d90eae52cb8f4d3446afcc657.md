# Product principles

Created: February 25, 2026 11:20 PM
Tags: product

Rules for deciding what the notebook does and doesn't do.

## 1. Import is the onboarding

The first 10 minutes are: connect your stuff, watch it come in. If import misses things or shows duplicates, the user decides the product is broken. **Import quality > every other feature.**

- show counts per source as it imports ("312 Claude chats, 41 PDFs")
- dedupe the same paper across sources, but show that it was in 3 places
- never silently drop items; list what failed

## 2. Every paragraph has a trail

Provenance is visible on hover and clickable. A paragraph with no trail is marked as "yours" (that's fine, it's a feature).

## 3. Local-first

Data on disk, readable formats. Cloud is for sync and only when asked.

## 4. Notebook, not inbox

We don't show a feed of imported stuff. You start from a blank page and pull things in.

## 5. Slow AI, not chatty AI

Model calls happen when the user asks or in the background for indexing. No assistant popping up mid-sentence.

## 6. Respect existing tools

Don't make people leave Zotero or Obsidian. Read from them, link back to them.

## Anti-goals

- not a reference manager
- not a chat UI with a sidebar
- not team wiki software (we know, we're writing this in one)
