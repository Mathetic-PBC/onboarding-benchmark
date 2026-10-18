# Onboarding Benchmark

Write-up: [Onboarding Benchmark and Dataset Documentation](https://claude.ai/artifact/BNBu3qZwb9h4ktsdgw6Vk2)

```
onboarding-benchmark/
├── docs/                          the write-up as an HTML file
├── skills/
│   ├── wave1-categories-v1/       builds the category list
│   ├── wave2-shallow-sort-v1/     files each item from a short sample
│   └── deep-pass-v1/              rereads items in full, decides what gets imported
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
