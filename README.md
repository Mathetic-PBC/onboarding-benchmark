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
│   ├── wave1.cjs                  first pass: builds the category list
│   ├── merge.cjs                  merges proposed categories into one list
│   ├── wave2.cjs                  shallow pass: files items from a short opening
│   ├── deep.cjs                   deep pass: rereads items, decides import, skip or pending
│   ├── shared.cjs                 rule blocks the prompts share
│   └── index.cjs                  all of them, with versions and hashes
├── scripts/                       import and build scripts
│   └── synth/                     one generator per source for the synthetic data
└── dataset/
    ├── tables/
    │   ├── datasets.json
    │   ├── analyses.json
    │   └── generated_categories.json
    ├── authentic/<source>/        real data (placeholders only; real data stays out of the repo)
    ├── synthetic/
    │   ├── <source>/              synthetic data (1,210 items)
    │   ├── PERSON.md              the person the synthetic data is about
    │   └── ground_truth_labels.json   the project each synthetic item belongs to
    ├── PROGRESS.md                collection status
    └── FAILURES.md                what couldn't be collected
```
