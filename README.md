# Onboarding Benchmark

Tooling for building a personal onboarding dataset and benchmarking how well
Claude Code and Codex classify it.

The dataset is everything I have across ChatGPT, Claude, Claude Code, Codex,
Overleaf, Zotero, GitHub, Google Drive, Gmail, Notion, Linear, Granola,
Evernote, Apple Notes, PDFs and local files, plus synthetic data for the tools
I don't use. The ground truth is my own classification of my own data.

The full write-up (dataset layout, tables, sources, pipeline, library) is
[here](https://claude.ai/artifact/BNBu3qZwb9h4ktsdgw6Vk2). The same page is in
`docs/` if you'd rather open it locally.

The prompts for each pass are in `skills/`: `wave1-categories-v1` builds the
category list, `wave2-shallow-sort-v1` files items from a short sample, and
`deep-pass-v1` rereads them in full and decides what gets imported.

`dataset/` has the tables (`dataset/tables/`) and one folder per source on
each side (`dataset/authentic/`, `dataset/synthetic/`). The real data never goes
in this repo: it stays in the folder the collection run builds, and
`dataset/authentic/` only holds empty placeholders. The import and build
scripts are in `scripts/`.
