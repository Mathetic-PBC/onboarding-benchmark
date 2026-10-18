---
tags: [lit, tutortrace, reading-group, telemetry]
author: Hannah Ostrowski, Mateo Lindqvist, Aisha Bello, Ravi Chandrasekar
year: 2025
venue: L@S '25 (arXiv 2507.01842 first)
citekey: ostrowski2025productive
read: 2026-02-09
status: read twice (arXiv v1 in Feb, camera-ready in Mar)
---
# Ostrowski et al. 2025, Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1

**one-line claim:** editor + assistant telemetry can separate productive struggle from stalling in CS1 reasonably well, with
repeated near-identical prompts and idle gaps after errors as the strongest stalling signals.

## setup
- intro Python course, N=212, two sections, browser IDE logging edits/runs/tests/assistant prompts
- 30-second windows (same as ours!), 4 TAs, labels: productive struggle / stalling / help-seeking / off-task
- 1,904 labeled windows. kappa on 10% overlap: 0.62 in arXiv v1, **0.64 in camera-ready**
- gradient-boosted classifier: macro-F1 0.69 (v1) → **0.71** (camera-ready)

## findings I care about
- stalling ← prompts that are nearly the same as the previous one (edit distance under ~15%), and long idle after a failed run
- productive struggle ← many small edits, frequent test runs
- they report a lower number when same-student windows can't leak across folds. good practice
- (07-25 addendum) we did NOT do this in IDETrace and it bit us, see [[IDETrace - leakage]]
- discussion: hints offered *during* productive struggle were rated less helpful in their follow-up survey

## where we differ (for the UIST related-work paragraph)
- our label set adds "stalled-after-error" as its own state (labeling guide v3), they fold it into stalling
- we have 2,340 windows from the VizPI CS 3114 deployment, 3 raters, kappa 0.71
- they have one course and one assistant; so do we, honestly. reviewers will hit both of us on generalization

## careful
- I have this paper in like four places (Zotero, Downloads, the papers folder, the Overleaf .bib). the v1 and the camera-ready
  have different numbers. **cite the camera-ready (0.71 / 0.64)**, not the arXiv numbers
- for the reading group: good example of a "trail" problem. two versions of the same paper, and which one I read determines
  which number ends up in my draft

## connections
- [[Kapur2008 - Productive Failure]]
- [[Papert1980 - Mindstorms]]
- [[TutorTrace - talk Q&A prep]]
- [[Engelbart - import dedupe]] (the same-paper-in-several-places case)
