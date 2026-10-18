# Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1

Authors: Hannah Ostrowski, Mateo Lindqvist, Aisha Bello, Ravi Chandrasekar
Year: 2025
Type: Paper
Status: Read
Tags: related work, TutorTrace
Rating: ⭐⭐⭐⭐
Created: March 26, 2026 1:20 AM
Last edited time: March 27, 2026 12:05 AM

## Why it's here

Closest prior work to TutorTrace. Need it in related work before the UIST deadline (Mar 31).

## Summary

L@S '25 paper. Instrumented a CS1 course (N=212) with editor + assistant telemetry; four TAs labeled 1,904 thirty-second windows as productive struggle / stalling / help-seeking / off-task. A gradient-boosted classifier hits 0.71 macro-F1 (0.69 in the arXiv v1). Repeated near-identical prompts and long idle gaps after a failed run predict stalling.

## How we differ

- They label 4 states; we have the finer state set incl. "stalled-after-error" from labeling guide v3.
- Their kappa is 0.64 on a 10% overlap; ours is 0.71 across 3 raters. Say this carefully, different label sets.
- They report a leakage-style number (windows from the same student in train and test) — cite it in our evaluation section as precedent for grouped splits.

## To do

- [x] add bib entry to the Overleaf (`ostrowski2025productive`)
- [ ] make sure we cite the camera-ready, not the arXiv v1 — numbers differ
