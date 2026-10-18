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

Real data never goes in this repo: `authentic/`, `_incoming/` and the answer
key are gitignored. Only the scripts, the table schemas and the synthetic data
are committed.
