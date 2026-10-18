# papert-lab-proto

Throwaway prototype of the Papert Lab notebook idea (Jan–Feb 2026), built to test one interaction: **every thought in the notebook keeps a trail back to where it came from** (a chat, a paper, a web page, an earlier cell).

What it is:
- Next.js app, notebooks in `localStorage` (no backend, no accounts)
- cells (markdown) with source chips; paste a URL to cite a page; cells can cite other cells
- trail view under each cell; ChatGPT export import (`conversations.json`); search
- demo data in `public/seed.json`

What it isn't: synced, multi-user, or careful about large imports.

Pitch notes from the first call with Hudson are in `docs/pitch-notes.md`.

## Status (2026-02-20)

Frozen. The trail interaction tested well with the 4 grad students Hudson and I showed it to; the next version is being planned as a proper app (working name Engelbart). Keeping this repo for reference only.
