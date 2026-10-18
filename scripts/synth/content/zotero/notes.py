"""David's Zotero child notes (reading notes). parent = citekey in papers.PAPERS / REAL. Body markup: lines starting with
'- ' are bullets, '# ' a heading, everything else a paragraph. Written by David, terse."""

NOTES = [
dict(parent='ostrowski2025productive', title='reading notes - ostrowski LaS25', date='2026-03-24 02:05',
     projects=['project_tutortrace'], body='''
# Ostrowski et al. 2025 (L@S) - notes
closest prior work to TutorTrace. MUST cite in related work + discussion.
- N=212 CS1, 1,904 windows, 4 states (productive struggle / stalling / help-seeking / off-task). ours has stalled-after-error as its own state, they fold it into stalling
- their kappa 0.64 (4 TAs, 10% overlap). ours 0.71 across 3 raters -> say this carefully, different schemes
- strongest stalling signal = near-identical repeated prompts (edit distance < 15%). we see the same thing in VizPI replays, worth one sentence
- they report a leakage check (0.58 when same-student windows removed). note to self: double check our own split before submission
- discussion: flags as prompts for a human check-in, not auto interventions. aligns w our framing
heads up: arXiv v1 (2507.01842v1) has 0.69 F1 / kappa 0.62, camera-ready has 0.71 / 0.64. cite the camera-ready numbers. I have both pdfs floating around (Downloads + Desktop/papers), the zotero one is camera-ready
'''),
dict(parent='nakamura2025labeling', title='window length justification', date='2026-03-25 01:10',
     projects=['project_tutortrace'], body='''
cite this for why 30s windows. kappa 0.66 at 30s vs 0.48 at 10s vs 0.61 at 60s.
- tinkering vs stuck = 44% of their disagreements. our guide v3 "stalled-after-error" rule does basically what their decision rule does (no successful run + reverts) -> mention
- they let raters flag mixed windows (11%). we forced one label. reviewer might ask. prep a line for limitations
'''),
dict(parent='haldane2024replaying', title='replay - compare to our tool', date='2026-03-26 00:22',
     projects=['project_tutortrace'], body='''
SessionReel ~ our replay viewer but instructor-facing, we're rater-facing.
- markers mattered more than playback: idle bands 17/23, error ticks 14/23. we have idle bands, no error ticks in the labeling UI. add error ticks? (not before deadline lol)
- 3.8 min/session -> argument for classifier-as-first-stage. same framing as Ostrowski discussion
- 4% opt-out under explicit replay consent. useful number for the privacy question if it comes up
'''),
dict(parent='brennan2026what', title='R2 privacy response', date='2026-06-14 00:31',
     projects=['project_tutortrace'], body='''
# for the rebuttal (R2 asked about telemetry privacy)
- assistant prompts least comfortable text stream: 38% comfortable, 19% if an instructor reviews individual sessions
- aggregate-only raises comfort ~22 pts
- their rec: store derived labels not raw prompts where possible -> we can say the released dataset keeps prompt text only for consented students and ships labels + features for the rest (confirm with Yan before promising)
- separate consent per stream: our IRB form already separates keystrokes vs prompts, say that
keep it to 3 sentences in the rebuttal, char limit is brutal
'''),
dict(parent='duarte2025beyond', title='cross-course - what to promise', date='2026-06-15 01:47',
     projects=['project_tutortrace'], body='''
R1 + R3 both said "one course". this paper is the template for the analysis we promise.
- they drop 0.72 -> 0.61 (DS, Java) and 0.55 (CS0). per-course normalization recovers some (0.66)
- stuck transfers worst, depends on error channel. our stalled-after-error is literally defined on the error channel so expect the same
- promise: train on CS 3114 deployment, test on the second course data Minsun has from spring, report normalized + raw. do NOT promise a number
'''),
dict(parent='ferreira2023groupaware', title='this is our bug', date='2026-07-25 00:12',
     projects=['project_idetrace'], body='''
# IDETrace leakage - found 07-24
this paper describes exactly what happened: windows from the same student in train and test. random split over windows, sklearn default. ugh
- their off-task drop was 17 pts, struggle 14. ours: macro-F1 0.81 -> 0.74 with GroupKFold on student_id. in line with them
- do the student-id probe they suggest and report it (my quick run: way above chance, ~0.5 top-1 over 160 students)
- rebuttal: report BOTH numbers, say we found it ourselves, cite this + Kaufman 2012
- fix split script: group by student id, then also hold out a lab section as a sanity check
'''),
dict(parent='olsen2025macro', title='per-class + calibration for rebuttal', date='2026-07-27 23:30',
     projects=['project_idetrace'], body='''
reviewer 2 asked whether macro-F1 hides the minority states. this paper says yes.
- add per-class F1 table to the rebuttal (help-seeking is our minority, ~7%)
- we use class weights -> check ECE on the grouped split, calibrate w temperature scaling if bad
- not enough time to redo everything before 07-29. per-class table yes, calibration as "will add"
'''),
dict(parent='albrecht2022frustration', title='lexicon for our project', date='2026-02-04 23:15',
     projects=['project_ise6664_affective_computing'], body='''
# ISE 6664 project - frustration in AI tutoring transcripts
use their 6 categories as our first-pass codebook, adapted to code tutoring.
- repetition w negation strongest marker (OR 3.9). in our transcripts this looks like re-asking the assistant the same thing w "no" / "still"
- terse replies ambiguous -> baseline per learner (Jordan's idea of z-scoring reply length per student)
- r = 0.47 for marker counts, transformer 0.52. we don't have self-reports so we validate against our own hand labels instead
split: Maya takes lexicon adaptation, Jordan the per-student baselines, me the transcript sampling + coding tool
'''),
dict(parent='gallo2023confusion', title='confusion vs frustration', date='2026-02-11 00:40',
     projects=['project_ise6664_affective_computing'], body='''
key distinction for our codebook: confusion != frustration. resolved confusion is GOOD (6 pt post-test gain), frustration is not.
- confused cues: "but", hedges, restating. frustrated: repetition, giving up, complaining about the tutor
- they label "both" (230 turns). we should allow both too
- Dr. Brooks will like this for the theory section (link to appraisal stuff from lecture 5)
'''),
dict(parent='bush1945we', title='trails, reading group', date='2026-09-03 00:15',
     projects=['project_augmenting_cognition_reading_group', 'project_engelbart'], body='''
re-read for reading group. the part people skip: the trail is the point, not the machine. a named path through stuff, built while thinking, that you can hand to someone else.
- engelbart (the product) "where did this thought come from" = a trail recorded automatically instead of by hand
- question for the group: is an AI chat log a trail? it's ordered and has the reasoning, but nobody names it or shares it
- pair with Marchetti 2024 (no tool records why a link was made)
'''),
dict(parent='halvorsen2025where', title='provenance numbers for pitch', date='2026-09-03 00:48',
     projects=['project_augmenting_cognition_reading_group', 'project_engelbart'], body='''
good numbers for the deck / one-pager:
- 31% of notes had no recoverable source after 2 weeks
- AI chats = 17% of note origins, only 46% recoverable
- median 3.5 min to find a recoverable source
their implication = "a single import of a researcher's existing tools is a precondition". that is literally our onboarding. send to Hudson
'''),
dict(parent='rinaldi2025importing', title='dedupe policy for import', date='2026-10-13 00:20',
     projects=['project_engelbart'], body='''
# import dedupe - after Priya's pilot (10-09)
Priya saw the same paper twice (zotero + Downloads). this paper's numbers:
- exact hash only catches 41% of dups. title+size 73%. shingling 92% but merges draft versions 61% of the time (bad)
- policy: exact dup -> merge silently, keep every location as provenance. same work (preprint vs published) -> group under one entry. own drafts (v2, "Copy of") -> version stack, never merge
- preprint vs camera-ready is the interesting case: e.g. the Ostrowski paper is in my own library as both arXiv v1 and the L@S version. those should group, not merge
for the 10-14 redesign doc
'''),
]
