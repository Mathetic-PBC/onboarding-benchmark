# Onboarding Benchmark

A benchmark of how accurately Claude Code and Codex sort a person's data into their projects during Engelbart's onboarding. It builds a dataset from the person's real accounts plus synthetic data, then scores each pass against the person's own classification.

Documentation: [Onboarding Benchmark Documentation](https://claude.ai/artifact/BNBu3qZwb9h4ktsdgw6Vk2)

```
onboarding-benchmark/
├── docs/                          the documentation as an HTML file
├── skills/
│   ├── wave1-categories-v1/       builds the category list
│   ├── wave2-shallow-sort-v1/     files each item from a short sample
│   ├── wave2-new-categories-v1/   adds the categories wave 2 found that the list was missing
│   └── deep-pass-v1/              rereads items in full, decides what gets imported
├── prompts/
│   ├── wave1.cjs                  first pass: builds the category list
│   ├── merge.cjs                  merges proposed categories into one list
│   ├── wave2.cjs                  shallow pass: files items from a short opening
│   ├── deep.cjs                   deep pass: rereads items, decides import, skip or pending
│   ├── shared.cjs                 rule blocks the prompts share
│   └── index.cjs                  all of them, with versions and hashes
├── run/                           one benchmark run, named by BENCH_RUN (e.g. run_002)
│   ├── pipeline.py                runs the import pipeline step by step on the sandbox
│   ├── from_engelbart.py          records an onboarding done in Engelbart (by hand in the UI, or by a scenario) as a run
│   └── scenarios/                 onboarding scenarios for Engelbart's scripts/onboarding-scenario.cjs (auto, manual)
├── scripts/                       import and build scripts
│   └── synth/                     one generator per source for the synthetic data
└── dataset/
    ├── tables/
    │   ├── datasets.json
    │   ├── analyses.json
    │   ├── generated_categories.json
    │   └── runs.json
    ├── authentic/<source>/        real data (placeholders only; real data stays out of the repo)
    ├── synthetic/
    │   ├── <source>/              synthetic data (1,210 items)
    │   ├── PERSON.md              the person the synthetic data is about
    │   └── ground_truth_labels.json   the project each synthetic item belongs to
    ├── PROGRESS.md                collection status
    └── FAILURES.md                what couldn't be collected
```
