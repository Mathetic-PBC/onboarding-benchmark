# Onboarding Benchmark

Tooling for building a personal onboarding dataset and benchmarking how well
Claude Code and Codex classify it.

The dataset is everything I have across ChatGPT, Claude, Claude Code, Codex,
Overleaf, Zotero, GitHub, Google Drive, Gmail, Notion, Linear, Granola,
Evernote, Apple Notes, PDFs and local files, plus synthetic data for the tools
I don't use. The ground truth is my own classification of my own data.

The full write-up (dataset layout, tables, sources, pipeline, library) is in
[docs/onboarding-benchmark-and-dataset-documentation.html](docs/onboarding-benchmark-and-dataset-documentation.html).
Clone the repo and open it in a browser.

Real data never goes in this repo: `authentic/`, `_incoming/` and the answer
key are gitignored. Only the scripts, the table schemas and the synthetic data
are committed.
