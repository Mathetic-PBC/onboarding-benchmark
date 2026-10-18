# UIST talk — Q&A prep

likely questions + short answers (keep each < 30 s)

**Q: kappa 0.71 isn't that high?**
For five behavioral states from replays it's in line with prior affect/behavior labeling. Most disagreement is between the two
stalled states, and merging them gives 0.80. Confusion matrix is in the paper.

**Q: does it generalize?**
Second course offering in the camera-ready: macro-F1 0.78 -> 0.74. One university, so no strong claim.

**Q: isn't this surveillance?**
States not prompt text; replays are an explicit logged action; opt-out with no penalty; we discuss it in limitations. Default
output is "go check in", not a grade.

**Q: why not just use an LLM to label?**
We tried zero-shot as a baseline; worse on stalled-after-error because it depends on timing, not text.

**Q: what do instructors do with it?**
In the study they walked to stalled-after-error students first. They ignored off-task. That surprised us.

**Q: relation to Ostrowski et al. L@S 2025?**
Similar stalling signals (repeated prompts, idle after error). They label offline; we focus on a live instructor view.

if blank: "great question — can I find you after the session?"
