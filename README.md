# Onboarding Benchmark

A benchmark of how accurately Claude Code and Codex sort a person's data into their projects during Engelbart's onboarding. It builds a dataset from the person's real accounts plus synthetic data, then scores each pass against the person's own classification.

Documentation: [Onboarding Benchmark and Dataset Documentation](https://claude.ai/artifact/BNBu3qZwb9h4ktsdgw6Vk2)

```
onboarding-benchmark/
├── docs/                          the documentation as an HTML file
├── skills/
│   ├── wave1-categories-v1/       builds the category list
│   ├── wave2-shallow-sort-v1/     files each item from a short sample
│   └── deep-pass-v1/              rereads items in full, decides what gets imported
├── prompts/
│   └── import-pipeline.cjs        the first pass, merge, shallow pass and deep pass prompts
├── scripts/                       import and build scripts
└── dataset/
    ├── tables/
    │   ├── datasets.json
    │   ├── analyses.json
    │   └── generated_categories.json
    ├── authentic/<source>/        real data (placeholders only; real data stays out of the repo)
    ├── synthetic/<source>/        synthetic data
    ├── PROGRESS.md                collection status
    └── FAILURES.md                what couldn't be collected
```
