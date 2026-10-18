"""Fictional papers (fictional authors, fictional results) for David's Zotero 'My Library'. Each becomes a PDF attachment and a
BibTeX/RIS entry. Bodies use content/zotero/dsl.py markup. Nothing here is a real paper.

Fields: key (citekey), type (bibtex type), title, authors [(last, first)], year, venue fields, pub (PDF internal date),
added (date added to Zotero, David's local time), collections, projects, keywords, abstract, body, refs.
"""

PAPERS = [
# ------------------------------------------------------------------ TutorTrace UIST26
dict(
key='haldane2024replaying', type='inproceedings',
title='Replaying the Keystroke: Session Reconstruction for Instructor Sense-Making in Large Programming Courses',
authors=[('Haldane', 'Iris'), ('Okafor', 'Tunde'), ('Brandt', 'Lucia')], year=2024,
booktitle="Proceedings of the ACM Technical Symposium on Computer Science Education", series="SIGCSE TS '24", pages='512--518',
publisher='ACM', address='Portland, OR, USA', pub='2024-03-08 10:00', added='2026-03-24 01:12',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['replay', 'instructor tools', 'CS1', 'keystroke data'],
abstract='Instructors of large programming courses see students\' final submissions but rarely the process that produced them. We built '
'SessionReel, a tool that reconstructs a student\'s editing session from keystroke logs and plays it back at adjustable speed with '
'run and error markers. In a within-subjects study, 9 instructors and 14 teaching assistants examined 40 sessions and were asked to '
'locate the moment a student became stuck. With final code alone, participants located the stuck point within 60 seconds in 41% of '
'sessions; with replay, 77%. Replay cost a median 3.8 minutes per session. We report which visual markers helped and argue that '
'replay is most useful as a targeted tool for sessions already flagged by simpler signals.',
body='''
# 1 Introduction
A CS1 course with 600 students produces tens of thousands of submissions per term. Autograders tell instructors whether code works;
they do not tell them how a student got there. Process data such as keystrokes, runs and error messages has been collected for over a
decade, but it is usually aggregated into dashboards of counts. Counts flatten the moments that matter to a teacher: the first failed
run, the long pause, the deletion of a working function.

We ask whether replaying a session, much like scrubbing through a screen recording, helps instructors make sense of struggle, and at
what cost in time.

# 2 SessionReel
SessionReel reconstructs file state at every keystroke from an append-only event log (insert, delete, paste, run, test result). The
player shows the editor on the left and a timeline on the right. The timeline carries three marker types: red ticks for runs that
raised an exception, green ticks for passing test runs, and grey bands for idle gaps longer than 45 seconds. Playback runs at 1x to
32x; idle gaps can be skipped automatically.

Reconstruction is exact for typed edits. Pastes are reconstructed as single events, which preserves their size but not their origin.

# 3 Study
Participants (9 instructors, 14 TAs) each reviewed 20 sessions in two blocks: final code plus error log (baseline), and SessionReel
(replay). Sessions came from a single assignment on list processing and were sampled to include 30 with an expert-annotated "stuck
point" and 10 without one. Block order was counterbalanced.

| Condition | Stuck point found (<= 60 s) | False alarms | Median time / session |
| Final code + error log | 41% | 0.22 | 1.1 min |
| Replay, no markers | 63% | 0.31 | 4.6 min |
| Replay with markers | 77% | 0.18 | 3.8 min |

Markers mattered more than playback itself. Without markers, participants scrubbed back and forth and reported "watching typing" as
tedious. Idle-gap bands were cited most often as useful (17 of 23 participants), followed by error ticks (14 of 23).

# 4 Findings
Instructors used replay to answer three questions: where did the student stop making progress, what did they try next, and did they
seem to understand the error message. The third was the hardest; participants disagreed on it in 38% of sessions. TAs, who had held
office hours that term, were faster than instructors (median 3.1 vs 4.4 minutes) but no more accurate.

Several participants said replay felt intrusive. One instructor noted that she would not want students to feel watched while they
were "allowed to be confused". We return to this in the discussion.

# 5 Discussion
Replay is expensive. At 3.8 minutes per session, reviewing every session in a 600-student course is out of reach. We therefore
recommend replay as a second stage: a cheap signal (repeated identical errors, idle gaps after a failed run) selects candidate
sessions, and an instructor or TA uses replay to decide whether to intervene.

Students should know that sessions can be replayed and by whom. In our deployment, consent forms described replay explicitly, and
4% of students opted out.

# 6 Limitations
One assignment, one institution, expert-annotated stuck points that are themselves a judgment. We did not measure whether replay
changed what instructors did next.
''',
refs=['Kapur, M. Productive failure. Cognition and Instruction 26, 3 (2008), 379-424.',
      'Wood, D., Bruner, J. S., and Ross, G. The role of tutoring in problem solving. Journal of Child Psychology and Psychiatry 17, 2 (1976), 89-100.',
      'Aleven, V., Stahl, E., Schworm, S., Fischer, F., and Wallace, R. Help seeking and help design in interactive learning environments. Review of Educational Research 73, 3 (2003), 277-320.']),

dict(
key='nakamura2025labeling', type='inproceedings',
title='Labeling Learner States in Programming Sessions: A Reliability Study of Thirty-Second Windows',
authors=[('Nakamura', 'Ren'), ('Feld', 'Sarah')], year=2025,
booktitle='Proceedings of the 2025 ACM Conference on International Computing Education Research - Volume 1', series="ICER '25",
pages='233--245', publisher='ACM', address='Charlottesville, VA, USA', pub='2025-08-01 09:00', added='2026-03-25 00:41',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['labeling', 'inter-rater reliability', 'learner states'],
abstract='Studies that label novice programmers\' behavioral states from logs choose a window length with little justification. We '
'asked three trained raters to label the same 400 minutes of replayed programming sessions at three window lengths (10, 30 and 60 '
'seconds) using a five-state scheme. Agreement was highest for 30-second windows (Fleiss\' kappa 0.66), lower for 60 seconds (0.61), '
'where windows often spanned two states, and lowest for 10 seconds (0.48), where raters lacked context. Most disagreements fell '
'between "tinkering" and "stuck". We release our rater training materials and recommend 30-second windows with a one-window context '
'margin.',
body='''
# 1 Motivation
Window length is a hidden parameter in behavioral labeling. Short windows give fine temporal resolution but little context; long
windows give context but blur transitions. Prior work has used anything from 5-second slices to whole-problem episodes. We isolate
the choice and measure what it does to agreement.

# 2 Method
We sampled 40 ten-minute segments from 31 students in a Python CS1 course. Three raters (two TAs and a graduate student) labeled
every segment three times, once per window length, with at least a week between passes and a randomized segment order. The scheme
had five states: productive work, tinkering (rapid small edits and runs without a clear plan), stuck, help-seeking, and off-task.

Raters saw the replayed editor, the run history and any assistant prompts, plus 30 seconds of preceding context in every condition.
Training took 90 minutes and used 12 practice segments with a reference key.

# 3 Results
| Window | Windows labeled | Fleiss' kappa | % windows with 2+ states (rater flag) |
| 10 s | 2,400 | 0.48 | 3% |
| 30 s | 800 | 0.66 | 11% |
| 60 s | 400 | 0.61 | 27% |

Disagreement concentrated on tinkering vs stuck (44% of all disagreements at 30 s). Raters who called a window "stuck" tended to
weight the time since the last successful run; those who called it "tinkering" weighted the number of edits. Adding an explicit rule
("if no run succeeded in the previous 3 minutes and edits are reverted, label stuck") raised kappa on a held-out set from 0.66 to
0.70.

Help-seeking was the easiest state (pairwise agreement 0.91) because prompts and forum visits are visible events. Off-task was
rarely labeled (2% of windows) and noisy.

# 4 Recommendations
- Use 30-second windows with at least 30 seconds of visible context before each window.
- Write decision rules for the tinkering/stuck boundary; most of the reliability gain comes from there.
- Report agreement per state, not only an overall kappa.
- Let raters flag mixed windows instead of forcing a single label; 11% is a real share of the data.

# 5 Limitations
Three raters from one institution; a five-state scheme. Agreement may differ with other schemes or with raters who did not teach the
course.
''',
refs=['Cohen, J. A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20, 1 (1960), 37-46.',
      'Landis, J. R. and Koch, G. G. The measurement of observer agreement for categorical data. Biometrics 33, 1 (1977), 159-174.',
      'Haldane, I., Okafor, T., and Brandt, L. Replaying the keystroke. SIGCSE TS 2024, 512-518.']),

dict(
key='vasquez2024where', type='inproceedings',
title='Where Did This Code Come From? Detecting Assistant-Pasted Code in Student Editor Logs',
authors=[('Vasquez', 'Dolores'), ('Ahmed', 'Kamal'), ('Petrov', 'Ilya')], year=2024,
booktitle='Proceedings of the 24th Koli Calling International Conference on Computing Education Research', series="Koli Calling '24",
pages='1--10', publisher='ACM', address='Koli, Finland', pub='2024-11-14 12:00', added='2026-03-26 23:58',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['paste detection', 'LLM assistants', 'academic integrity', 'telemetry'],
abstract='When a course permits an AI assistant, instructors still want to know how much of a submission a student wrote. We study paste '
'events in an instrumented editor used by 296 CS1 students alongside an integrated assistant. A classifier using paste size, time '
'since the last assistant response and token overlap with that response identified assistant-originated pastes with F1 = 0.88 '
'against assistant logs. Across the term, 23% of final submissions contained more than half pasted assistant code, concentrated in '
'the last 24 hours before deadlines. We discuss uses of provenance signals that support learning rather than policing.',
body='''
# 1 Introduction
Integrated assistants make provenance visible to the platform but not to the instructor. Paste events are a natural boundary: a
student who copies from an assistant panel or another window produces a single large insertion rather than a stream of keystrokes.
We ask how well paste events reveal assistant origin and what the pattern of pasting looks like over a term.

# 2 Data
The course used a browser IDE with an assistant side panel. With consent (296 of 341 students), the IDE logged insertions, deletions,
pastes, runs and assistant exchanges. Ground truth for assistant origin came from the assistant log: a paste was labeled
assistant-originated if at least 80% of its tokens appeared in an assistant response from the previous 10 minutes.

# 3 Detector
We trained a logistic regression on features that an instructor-facing tool could compute without the assistant log: paste length in
tokens, seconds since the last assistant response, whether the paste contained comments in the assistant's style ("# Step 1:"), and
indentation consistency with surrounding code.

| Feature set | Precision | Recall | F1 |
| Paste length only | 0.61 | 0.79 | 0.69 |
| + time since assistant response | 0.83 | 0.84 | 0.83 |
| + style and indentation | 0.87 | 0.89 | 0.88 |

Time since the assistant response carried most of the signal: 71% of assistant-originated pastes happened within 20 seconds of a
response.

# 4 Patterns over the term
Pasting rose across the term, from 9% of submissions with majority-pasted code in week 2 to 31% in week 12. Majority-pasted submissions
clustered near deadlines: 64% were finalized in the last 24 hours. Students who pasted heavily early in the term did not score lower
on the in-person midterm once prior programming experience was controlled, but students whose pasting increased sharply after week 6
did (by 7.4 points on average).

# 5 Discussion
Provenance can be used to punish or to teach. We argue for the second: showing a student the share of their submission that came from
the assistant, privately, before the deadline, and pairing it with an invitation to explain the pasted code. Our detector is too
imperfect for integrity cases and we do not recommend using it for them.

# 6 Limitations
One course, one assistant. Students can retype assistant code, which our detector misses by design.
''',
refs=['Aleven, V., Stahl, E., Schworm, S., Fischer, F., and Wallace, R. Help seeking and help design in interactive learning environments. Review of Educational Research 73, 3 (2003), 277-320.',
      'Haldane, I., Okafor, T., and Brandt, L. Replaying the keystroke: session reconstruction for instructor sense-making in large programming courses. SIGCSE TS 2024, 512-518.']),

dict(
key='lindgren2025like', type='inproceedings',
title="\"It's Like a TA That Never Sighs\": Novices' Mental Models of Code Assistants in CS1",
authors=[('Lindgren', 'Maja'), ('Mensah', 'Kofi')], year=2025,
booktitle='Proceedings of the 30th ACM Conference on Innovation and Technology in Computer Science Education V. 1', series="ITiCSE '25",
pages='88--94', publisher='ACM', address='Nijmegen, Netherlands', pub='2025-06-20 09:00', added='2026-03-29 22:16',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['mental models', 'interview study', 'help-seeking', 'CS1'],
abstract='We interviewed 22 CS1 students about how they understand and use an AI code assistant permitted in their course. Students held '
'three recurring models of the assistant: an oracle that knows the answer, a rubber duck that helps them think, and a shortcut that '
'saves time on parts they consider unimportant. Models shifted within a single session, often after a failed run. Students who '
'described the assistant as a rubber duck reported asking later and asking narrower questions. We discuss implications for when '
'and how assistants should respond to novices.',
body='''
# 1 Introduction
How students use an assistant depends on what they think it is. A student who treats it as an oracle asks for the answer; one who treats
it as a sounding board asks whether their plan makes sense. We report an interview study of these mental models.

# 2 Method
We recruited 22 students (11 women, 10 men, 1 non-binary; 15 with no prior programming) from a CS1 course in which an assistant was
permitted for homework. Semi-structured interviews (35-50 minutes) included a think-aloud on a short debugging task with the assistant
available. Two researchers coded transcripts with reflexive thematic analysis.

# 3 Three models
| Model | Students who described it (of 22) | Typical first prompt |
| Oracle | 17 | "write a function that ..." |
| Rubber duck | 9 | "is my approach right if ..." |
| Shortcut | 14 | "fix the syntax in this" |

Most students described more than one model. P7 explained: "When it's the hard part I want to figure it out, so I just ask if I'm
on track. When it's string formatting I just want it gone." The title quote came from P15, who said the assistant was like a TA that
"never sighs when you ask the same thing twice".

# 4 Shifts within a session
In the think-aloud, 13 students changed how they addressed the assistant after a failed run. The most common shift (9 students) was
from duck to oracle: after one or two failures, they pasted the error and asked for corrected code. Students described this moment as
running out of patience rather than running out of ideas.

Rubber-duck users waited longer before their first prompt (median 6.5 vs 2.0 minutes) and wrote narrower prompts that referenced
specific lines.

# 5 Implications
Assistants could support the duck model explicitly, for example by asking a student to state their plan before giving code, and by
noticing the duck-to-oracle shift after repeated failures, which may be the moment a human check-in helps most.

# 6 Limitations
Self-report and a single think-aloud task. Our sample over-represents students who volunteer for interviews.
''',
refs=['Wood, D., Bruner, J. S., and Ross, G. The role of tutoring in problem solving. Journal of Child Psychology and Psychiatry 17, 2 (1976), 89-100.',
      'Aleven, V. et al. Help seeking and help design in interactive learning environments. Review of Educational Research 73, 3 (2003), 277-320.']),

dict(
key='brennan2026what', type='article',
title='What Will Students Share? Consent and Comfort with Fine-Grained Telemetry in Educational IDEs',
authors=[('Brennan', 'Colm'), ('Zhou', 'Wei'), ('Adler', 'Ruth')], year=2026,
journal='arXiv preprint', eprint='2602.11873', archiveprefix='arXiv', primaryclass='cs.CY',
pub='2026-02-17 14:00', added='2026-06-13 23:27',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['privacy', 'telemetry', 'consent', 'survey'],
abstract='Research on novice programming increasingly depends on fine-grained telemetry, yet little is known about what students are '
'willing to share. We surveyed 418 students at three universities about eight data streams, from submission history to webcam video, '
'and four uses, from aggregate research to individual instructor review. Comfort was high for submissions (89%) and keystrokes (61%) '
'but low for assistant prompts (38%), which students saw as revealing confusion. Restricting use to aggregate dashboards raised '
'comfort by 22 percentage points on average. We propose a consent design that separates streams and uses.',
body='''
# 1 Introduction
Learning-analytics consent forms often ask for a single yes or no to "data collected by the IDE". Students may feel very differently
about a log of runs and a log of their questions to an assistant. We measure these differences.

# 2 Survey
Participants (N = 418; 3 universities; CS1 and CS2) rated comfort on a 5-point scale for each combination of eight streams and four
uses. We counted ratings of 4 or 5 as comfortable. The survey also included two open questions about what they would want to know
before agreeing.

# 3 Results
| Stream | Comfortable (any use) | Aggregate only | Instructor reviews my session |
| Submission history | 89% | 94% | 81% |
| Run and test results | 78% | 90% | 66% |
| Keystrokes | 61% | 82% | 40% |
| Assistant prompts | 38% | 63% | 19% |
| Screen recording | 21% | 37% | 9% |
| Webcam | 6% | 11% | 3% |

Assistant prompts were the least comfortable text stream. In open responses, 112 students said prompts showed "what I don't know" or
were "like a diary of being confused". Several students were more comfortable with an automated classifier reading prompts than with a
person reading them, provided only labels were stored.

# 4 Consent design
We recommend (1) separate consent per stream; (2) separate consent for aggregate research and individual review; (3) storing derived
labels instead of raw prompts where research questions allow; (4) a retention date stated in the form; and (5) a dashboard where
students can see what was recorded about them.

# 5 Limitations
Hypothetical comfort is not behavior; actual opt-out rates in deployments are lower than these numbers suggest.
''',
refs=['Haldane, I., Okafor, T., and Brandt, L. Replaying the keystroke. SIGCSE TS 2024.',
      'Vasquez, D., Ahmed, K., and Petrov, I. Where did this code come from? Koli Calling 2024.']),

dict(
key='duarte2025beyond', type='inproceedings',
title='Beyond One Course: Do Behavioral-State Classifiers Transfer Across Programming Courses?',
authors=[('Duarte', 'Paulo'), ('Sim', 'Hye-jin')], year=2025,
booktitle='Proceedings of the 18th International Conference on Educational Data Mining', series="EDM '25", pages='141--152',
publisher='International Educational Data Mining Society', address='Palermo, Italy', pub='2025-07-10 09:00', added='2026-06-14 01:03',
collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['generalization', 'transfer', 'behavior classification'],
abstract='Classifiers of learner behavioral states are almost always trained and evaluated within a single course. We trained a '
'gradient-boosted classifier on labeled windows from a Python CS1 course and evaluated it on two other courses: a Java data structures '
'course and a block-based CS0 course. Macro-F1 fell from 0.72 in-course to 0.61 and 0.55. Per-course normalization of rate features '
'recovered part of the gap (0.66 on data structures). Errors concentrated on the "stuck" state, whose behavioral signature depended on '
'the language\'s error messages. We recommend reporting cross-course results as a standard check.',
body='''
# 1 Introduction
A behavioral-state classifier that works in one course is a finding about that course. Whether it is a finding about learners depends
on transfer. We test transfer across three courses that differ in language, level and editor.

# 2 Data
| Course | Students | Labeled windows | Language |
| CS1 (train) | 140 | 3,050 | Python |
| Data structures | 62 | 1,120 | Java |
| CS0 | 88 | 980 | Blocks |

Windows were 30 seconds long and labeled with a four-state scheme (productive, stuck, help-seeking, off-task) by raters trained on
the same guide. Within-course agreement was kappa 0.68, 0.65 and 0.59.

# 3 Results
| Test course | Macro-F1 (raw) | Macro-F1 (normalized) | F1 stuck |
| CS1 (held-out students) | 0.72 | 0.73 | 0.69 |
| Data structures | 0.61 | 0.66 | 0.48 |
| CS0 | 0.55 | 0.57 | 0.41 |

Normalizing edit and run rates by each course's median helped most where students' baseline pace differed. The stuck state transferred
worst. In Java, compiler errors arrive before a run and stuck students compiled repeatedly; in CS0, blocks prevent most syntax errors
and stuck students instead dragged blocks in and out without running.

# 4 Recommendations
- Report at least one cross-course or cross-term evaluation.
- Normalize rate features per course before training.
- Expect "stuck" to need course-specific features tied to the error channel.

# 5 Limitations
Three courses at two institutions; label schemes were harmonized, which may hide real differences in what raters meant.
''',
refs=['Haldane, I., Okafor, T., and Brandt, L. Replaying the keystroke. SIGCSE TS 2024, 512-518.',
      'Ferreira, A. and Kowalczyk, P. Group-aware splits for educational sequence data. JEDM 15, 2 (2023).']),

# ------------------------------------------------------------------ IDETrace
dict(
key='ferreira2023groupaware', type='article',
title='Group-Aware Splits for Educational Sequence Data: How Student Overlap Inflates Reported Accuracy',
authors=[('Ferreira', 'Ana'), ('Kowalczyk', 'Piotr')], year=2023,
journal='Journal of Educational Data Mining', volume='15', number='2', pages='44--67', pub='2023-09-30 09:00', added='2026-07-24 23:46',
collections=['IDETrace'], projects=['project_idetrace'], keywords=['data leakage', 'cross-validation', 'evaluation', 'sequence data'],
abstract='Educational datasets are made of many short sequences from relatively few students. When windows or attempts are split into '
'train and test sets at random, the same student appears on both sides and models can learn the student rather than the behavior. We '
're-ran the evaluations of eleven prediction tasks on five public-style datasets with random splits and with splits grouped by '
'student. Grouped splits lowered reported performance by 4 to 17 points of AUC or F1, with the largest drops for tasks built from '
'short windows. We give a checklist for detecting and reporting this leakage.',
body='''
# 1 The problem
Suppose each student contributes 40 windows and a model sees 32 of them in training. Typing speed, preferred variable names and habitual
error types identify the student almost as well as a name would. If the label distribution differs by student, a model can score well by
recognizing who wrote a window.

This is a known form of leakage, but it is easy to introduce: most libraries split rows, not groups, by default.

# 2 Re-evaluation
We re-implemented eleven tasks (dropout, struggle, help-seeking, error type and others) on five datasets and evaluated each with random
5-fold splits and with 5-fold splits grouped by student.

| Task family | Unit | Random split | Grouped split | Drop |
| Struggle detection | 30 s window | 0.83 F1 | 0.69 F1 | 14 |
| Help-seeking | 60 s window | 0.79 F1 | 0.71 F1 | 8 |
| Next error type | attempt | 0.74 F1 | 0.65 F1 | 9 |
| Dropout | student-week | 0.81 AUC | 0.77 AUC | 4 |
| Off-task | 30 s window | 0.71 F1 | 0.54 F1 | 17 |

Drops were largest for short windows and for labels that were unevenly distributed across students. Dropout prediction, already defined
per student-week, changed least.

# 3 Detecting leakage
A quick diagnostic: train a model to predict the student id from the same features. If it is far above chance, random splits are
unsafe. On our struggle-detection data, student id was predicted with 64% top-1 accuracy among 120 students.

# 4 Checklist
1. State the unit of the split (row, attempt, student, section, term).
2. Group by student unless the claim is explicitly about known students.
3. Report the student-id probe accuracy.
4. If prior numbers used random splits, report both.

# 5 Limitations
Grouped splits answer a different question: performance on new students. Some applications, such as personalization for an enrolled
student, may legitimately use within-student data.
''',
refs=['Kaufman, S., Rosset, S., Perlich, C., and Stitelman, O. Leakage in data mining: formulation, detection, and avoidance. ACM TKDD 6, 4 (2012), Article 15.']),

dict(
key='hartmann2024novedit', type='inproceedings',
title='NovEdit: A Benchmark of Novice Program Edits for Next-Action Prediction',
authors=[('Hartmann', 'Jonas'), ('Ilunga', 'Benedicte'), ('Costa', 'Rafael')], year=2024,
booktitle='Advances in Neural Information Processing Systems 37, Datasets and Benchmarks Track', series='NeurIPS 2024',
pub='2024-10-30 09:00', added='2026-05-03 02:21',
collections=['IDETrace'], projects=['project_idetrace'], keywords=['benchmark', 'program edits', 'next-action prediction', 'dataset'],
abstract='We release NovEdit, 1.2 million edit events from 3,400 consenting novice programmers across four terms, with two benchmark '
'tasks: predicting the next action class (edit, run, delete block, seek help, idle) and predicting whether a student will recover from '
'an error within five minutes. Sequence models outperform count-based baselines on next action (macro-F1 0.58 vs 0.47) but not on '
'recovery (AUC 0.71 vs 0.70). We document collection, consent and splits grouped by student and term.',
body='''
# 1 Motivation
Models of novice programming are usually trained on private data from a single course, which makes them hard to compare. NovEdit is a
shared benchmark with fixed splits and a datasheet.

# 2 Collection
Data came from an instrumented editor in an introductory Python course over four terms. Students opted in (consent rate 71%). Events
were tokenized, identifiers were hashed per student, and string literals were removed.

| Split | Students | Terms | Events |
| Train | 2,380 | Terms 1-3 | 840k |
| Validation | 340 | Terms 1-3 | 118k |
| Test | 680 | Term 4 | 242k |

Splits are grouped by student; the test set is a later term to measure temporal shift.

# 3 Tasks and baselines
Next action: given the last 20 events, predict the next action class. Recovery: given the events up to an error, predict whether the
student reaches a passing run within five minutes.

| Model | Next action (macro-F1) | Recovery (AUC) |
| Majority | 0.14 | 0.50 |
| Counts + gradient boosting | 0.47 | 0.70 |
| GRU over events | 0.55 | 0.70 |
| Transformer (6 layers) | 0.58 | 0.71 |

# 4 Discussion
Recovery appears to depend on information not present in the edit stream, such as whether a student understood the error message. We
encourage submissions that combine edits with other channels, including assistant use.

# 5 Responsible use
NovEdit must not be used to identify individual students. We prohibit linking it with other data sources in the license.
''',
refs=['Gebru, T. et al. Datasheets for datasets. Communications of the ACM 64, 12 (2021), 86-92.',
      'Ferreira, A. and Kowalczyk, P. Group-aware splits for educational sequence data. JEDM 15, 2 (2023), 44-67.']),

dict(
key='quinlan2025datasheets', type='inproceedings',
title='Datasheets for Learning Traces: Documentation Practices for Educational Interaction Datasets',
authors=[('Quinlan', 'Moira'), ('Taufa', 'Sione'), ('Rao', 'Arjun')], year=2025,
booktitle='Proceedings of the 15th International Learning Analytics and Knowledge Conference', series="LAK '25", pages='402--412',
publisher='ACM', address='Dublin, Ireland', pub='2025-03-03 09:00', added='2026-05-04 23:12',
collections=['IDETrace'], projects=['project_idetrace'], keywords=['documentation', 'datasheets', 'dataset audit'],
abstract='We audited the documentation of 37 publicly released learning-interaction datasets against an adapted datasheet. Fewer than '
'a third reported how consent was obtained (30%) and fewer than a fifth stated how train and test splits were formed (19%). Only 4 '
'reported the share of students who opted out. We propose a 12-question supplement for learning traces covering consent, granularity, '
'de-identification, split units and known artifacts of the collection platform.',
body='''
# 1 Introduction
General-purpose datasheets do not ask the questions that matter most for learning traces: who could see a student's data while it was
collected, what granularity was logged, and whether a student can appear in both training and test data.

# 2 Audit
We identified 37 datasets released between 2015 and 2024 with event-level student interaction data. Two authors coded each dataset's
paper and documentation.

| Item | Reported |
| Institution and course context | 92% |
| Consent procedure | 30% |
| Opt-out rate | 11% |
| De-identification method | 57% |
| Split unit (row / student / term) | 19% |
| Known logging gaps or outages | 8% |

Known logging gaps were the rarest item, though three of the dataset maintainers we contacted confirmed outages during collection.

# 3 Supplement
Our 12 questions include: What events were logged and at what granularity? Were there periods when logging failed, and how are they
marked? What is the unit of the provided splits? Can a student appear in more than one split? What would a student need to do to have
their data removed?

# 4 Discussion
Logging gaps deserve special attention. A reconnect bug that drops events for one lab section produces a dataset in which that
section looks less active, which a model may learn as a property of the students.
''',
refs=['Gebru, T. et al. Datasheets for datasets. Communications of the ACM 64, 12 (2021), 86-92.']),

dict(
key='olsen2025macro', type='inproceedings',
title='Macro-F1 Is Not Enough: Calibration of Behavior Classifiers on Imbalanced Learning Logs',
authors=[('Olsen', 'Erik'), ('Mahmoud', 'Layla')], year=2025,
booktitle='Artificial Intelligence in Education: 26th International Conference, AIED 2025', series='AIED 2025', pages='318--331',
publisher='Springer', pub='2025-07-21 09:00', added='2026-07-27 22:40',
collections=['IDETrace'], projects=['project_idetrace'], keywords=['calibration', 'class imbalance', 'evaluation', 'macro-F1'],
abstract='Behavior classifiers in learning analytics are usually summarized by macro-F1. We show on three datasets that models with '
'similar macro-F1 can differ widely in calibration on minority states, which matters when predictions trigger interventions. We '
'recommend reporting per-class F1, expected calibration error per class, and a reliability diagram for the state that will drive an '
'intervention.',
body='''
# 1 Introduction
An intervention fires when a model's probability of "stuck" crosses a threshold. Macro-F1 says nothing about whether a probability of
0.8 means stuck 80% of the time. On imbalanced data, the minority state that triggers the intervention is the one most likely to be
miscalibrated.

# 2 Experiments
We trained four model families on three behavior datasets (minority-state prevalence 6% to 18%) and measured macro-F1 and expected
calibration error (ECE, 15 bins) for the minority state.

| Model | Macro-F1 | Minority F1 | Minority ECE |
| Logistic regression | 0.70 | 0.52 | 0.04 |
| Gradient boosting | 0.74 | 0.55 | 0.11 |
| Gradient boosting + class weights | 0.74 | 0.61 | 0.19 |
| GRU | 0.73 | 0.57 | 0.14 |

Class weighting raised minority F1 but nearly doubled its calibration error: the model learned to over-predict the minority state.
Temperature scaling on a grouped validation split reduced ECE to 0.05 without changing F1.

# 3 Reliability diagrams
Reliability diagrams make the problem visible. For the class-weighted gradient-boosting model, windows predicted "stuck" with
probability 0.7-0.8 were actually stuck 41% of the time. An instructor dashboard that flags students above 0.7 would send a TA to
the wrong student more often than the right one, even though the model's macro-F1 matches the best model in the table.

| Predicted probability bin | Windows | Observed rate (weighted GB) | Observed rate (after temperature scaling) |
| 0.5-0.6 | 412 | 0.29 | 0.53 |
| 0.6-0.7 | 288 | 0.34 | 0.62 |
| 0.7-0.8 | 197 | 0.41 | 0.73 |
| 0.8-0.9 | 121 | 0.55 | 0.84 |
| 0.9-1.0 | 64 | 0.70 | 0.91 |

# 4 Splits matter for calibration too
Calibration measured on a random split looked better than on a split grouped by student (ECE 0.07 vs 0.11 for the unweighted model).
A model that has seen a student's other windows is more confident about that student, and calibrated on that confidence. Temperature
should be fit on held-out students.

# 5 A worked example
Consider an intervention that pauses the assistant and suggests a TA check-in when P(stuck) > 0.8. With the weighted, uncalibrated
model, 45% of check-ins would target students who were not stuck. After calibration on a grouped validation split, the false share
drops to 16% while the number of stuck students reached falls only slightly (from 118 to 109 of 152 in our test set). The intervention
cost depends on calibration far more than on the second decimal of macro-F1.

# 6 Recommendations
- Report per-class F1 alongside macro-F1.
- Report ECE for any class used to trigger an intervention, measured on a split grouped by student.
- Calibrate after class weighting.
- Publish the reliability diagram for the intervention class.

# 7 Limitations
ECE is sensitive to binning; we report results for 10 and 20 bins in the supplement. Our datasets come from two platforms and may not
reflect the class balance of other courses.
''',
refs=['Ferreira, A. and Kowalczyk, P. Group-aware splits for educational sequence data. JEDM 15, 2 (2023), 44-67.']),

# ------------------------------------------------------------------ ISE 6664 readings
dict(
key='albrecht2022frustration', type='article',
title='Frustration Markers in Text-Based Tutoring Dialogues: A Lexicon and Validation Study',
authors=[('Albrecht', 'Selma'), ('Nwosu', 'Chidi')], year=2022,
journal='International Journal of Artificial Intelligence in Education', volume='32', number='4', pages='901--930',
pub='2022-11-15 09:00', added='2026-02-03 22:05',
collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['frustration', 'affect detection', 'tutoring dialogue', 'lexicon'],
abstract='We present a lexicon of 214 textual markers of frustration in learner turns of text-based tutoring dialogues, grouped into '
'six categories. Markers were derived from 1,800 annotated dialogues and validated against in-session self-reports from 240 '
'learners. A simple marker count correlated with self-reported frustration at r = 0.47, comparable to a fine-tuned classifier '
'(r = 0.52) and far more interpretable. Repetition of a prior question with added negation was the single strongest marker.',
body='''
# 1 Introduction
Frustration in face-to-face tutoring shows in posture and voice. In text, learners have fewer channels, but they still signal: they
shorten replies, repeat questions, and say they are giving up. We catalogue these signals.

# 2 Building the lexicon
Two annotators marked spans in 1,800 dialogues from an online algebra tutor where learners had rated their frustration every five
minutes. Candidate markers were kept if they appeared in at least 15 dialogues and were more frequent in high-frustration windows.

| Category | Markers | Example |
| Repetition with negation | 31 | "no I mean why doesn't it ..." |
| Terse replies | 18 | "ok", "k", "sure" after long explanations |
| Explicit giving up | 27 | "forget it", "I'll just guess" |
| Capitalization and punctuation | 22 | "WHY", "???" |
| Self-deprecation | 41 | "I'm so bad at this" |
| Meta-complaints about the tutor | 75 | "you already said that" |

# 3 Validation
On 240 new learners, the count of markers in a five-minute window correlated with self-reported frustration at r = 0.47. A fine-tuned
transformer reached r = 0.52. Combining both reached r = 0.55. The strongest single marker was repetition with negation (odds ratio
3.9 for high frustration).

# 4 Discussion
Terse replies were ambiguous: some learners were frustrated, others were simply efficient. Markers should be interpreted relative to a
learner's own baseline. Self-deprecation was frequent but weakly predictive; learners used it jokingly.

# 5 Limitations
One domain (algebra), English only, and self-reports that may themselves be affected by the act of reporting.
''',
refs=['D\'Mello, S. and Graesser, A. Dynamics of affective states during complex learning. Learning and Instruction 22, 2 (2012), 145-157.',
      'Russell, J. A. A circumplex model of affect. Journal of Personality and Social Psychology 39, 6 (1980), 1161-1178.']),

dict(
key='gallo2023confusion', type='inproceedings',
title='Confusion Is Not Frustration: Distinguishing Epistemic Affect in Chat-Based Tutoring Logs',
authors=[('Gallo', 'Marco'), ('Stein', 'Hedda')], year=2023,
booktitle='Proceedings of the 16th International Conference on Educational Data Mining', series="EDM '23", pages='77--88',
publisher='International Educational Data Mining Society', address='Bengaluru, India', pub='2023-07-11 09:00', added='2026-02-10 23:50',
collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['confusion', 'frustration', 'epistemic emotions', 'chat logs'],
abstract='Detectors of negative affect in tutoring logs often merge confusion and frustration. We annotated 6,200 learner turns from a '
'chat-based statistics tutor with separate labels and found that the two states have different textual signatures and different '
'consequences: confusion followed by a resolving explanation predicted higher post-test scores, while frustration did not. A detector '
'that separates the two improves the usefulness of affect-triggered interventions.',
body='''
# 1 Introduction
Confusion arises when new information conflicts with what a learner expects; it can be productive if resolved. Frustration arises when
goals are blocked; it tends to persist. Treating both as "negative affect" loses this difference.

# 2 Annotation
Three annotators labeled 6,200 learner turns as confused, frustrated, both, or neither, with access to the preceding three turns.
Agreement was kappa 0.61 for confusion and 0.57 for frustration.

| Label | Turns | Typical cues |
| Confused | 1,140 | questions with "but", hedges, restating the tutor's words |
| Frustrated | 610 | repetition, giving up, complaints about the tutor |
| Both | 230 | confused question followed by an exasperated aside |
| Neither | 4,220 | - |

# 3 Consequences
Confusion that was followed within two turns by an explanation the learner acknowledged predicted a 6-point higher post-test score
compared with no confusion. Unresolved confusion predicted no difference. Frustration predicted lower scores whether or not the tutor
responded.

# 4 Detector
A two-headed classifier reached F1 0.71 (confusion) and 0.63 (frustration). A merged negative-affect detector had higher overall F1
(0.74) but triggered interventions on confused learners who did not need them.

# 5 Implications
Respond to confusion with explanation and to frustration with a change of task or pace. Do not rush to remove confusion.
''',
refs=['D\'Mello, S. and Graesser, A. Dynamics of affective states during complex learning. Learning and Instruction 22, 2 (2012), 145-157.',
      'Baker, R. S. J. d. et al. Better to be frustrated than bored. International Journal of Human-Computer Studies 68, 4 (2010), 223-241.']),

dict(
key='yamada2024apologies', type='inproceedings',
title='Apologies, Empathy, and Persistence: How Conversational Tutors\' Affective Responses Shape Learner Effort',
authors=[('Yamada', 'Kei'), ('Ortiz', 'Lucía')], year=2024,
booktitle='Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems', series="CHI '24", pages='1--14',
publisher='ACM', address='Honolulu, HI, USA', pub='2024-05-11 09:00', added='2026-03-02 21:34',
collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['empathy', 'conversational agents', 'Wizard of Oz', 'persistence'],
abstract='When a learner expresses frustration, a conversational tutor can ignore it, apologize, or acknowledge the feeling and '
'reframe the difficulty. In a Wizard-of-Oz study with 96 participants solving logic puzzles, we compared these three response styles. '
'Acknowledge-and-reframe increased the number of puzzles attempted after a failure by 28% relative to ignoring, while apologizing had '
'no effect on persistence and lowered perceived tutor competence. Participants described scripted empathy as hollow when it repeated.',
body='''
# 1 Introduction
Affect-aware tutors often respond to detected frustration with sympathy. Whether sympathy helps learners keep going is less clear.

# 2 Study
96 participants solved a sequence of logic puzzles with a chat tutor operated by a trained wizard following scripts. Frustration was
induced with one unsolvable puzzle. Participants were randomly assigned to one of three response styles, triggered when they expressed
frustration in text.

| Style | Example response | Puzzles attempted after failure | Perceived competence (1-7) |
| Ignore | continues with next hint | 3.2 | 5.1 |
| Apologize | "Sorry, that one was hard." | 3.3 | 4.4 |
| Acknowledge + reframe | "That's frustrating. People usually get stuck here because ..." | 4.1 | 5.6 |

# 3 Qualitative findings
Participants found acknowledgement useful when it explained why the task was hard. The same sentence repeated a second time was
described as "robotic" by 19 participants. Apologies were read as the tutor admitting it had made a mistake.

# 4 Design implications
- Pair any acknowledgement of feeling with information about the task.
- Vary wording and avoid repeating the same empathic phrase.
- Avoid apologies unless the tutor actually erred.

# 5 Limitations
Puzzles, not course material; a single induced failure; a wizard rather than an automated detector.
''',
refs=['Picard, R. W. Affective Computing. MIT Press, 1997.',
      'Albrecht, S. and Nwosu, C. Frustration markers in text-based tutoring dialogues. IJAIED 32, 4 (2022), 901-930.']),

dict(
key='whitfield2021designing', type='inproceedings',
title='Designing for Recovery: Affective Design Patterns After Failure in Learning Software',
authors=[('Whitfield', 'Nora')], year=2021,
booktitle='Proceedings of the 2021 ACM Designing Interactive Systems Conference', series="DIS '21", pages='1250--1262',
publisher='ACM', address='Virtual Event, USA', pub='2021-06-28 09:00', added='2026-04-27 23:58',
collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['affective design', 'design patterns', 'failure', 'learning software'],
abstract='Learning software is full of failure: wrong answers, failed tests, broken builds. We reviewed 41 learning applications and '
'interviewed 12 designers to collect patterns for the moment after a learner fails. We describe nine patterns, from "name the next '
'smallest step" to "make the failure cheap to retry", and discuss their affective rationale with reference to broaden-and-build '
'theory and emotional design.',
body='''
# 1 Introduction
Most affective design guidance concerns delight. Learning software needs guidance for the opposite moment, when the learner has just
been told they are wrong.

# 2 Method
We reviewed 41 learning applications (programming, language, mathematics) by deliberately failing tasks and recording the response.
We then interviewed 12 designers who had worked on such applications about decisions behind failure screens.

# 3 Patterns
| Pattern | Seen in (of 41) | Rationale |
| Name the next smallest step | 14 | narrows attention to something achievable |
| Make retry cheap | 27 | lowers the cost of trying again |
| Separate the person from the attempt | 9 | avoids "you are wrong" framing |
| Show partial credit | 12 | makes progress visible |
| Delay the red | 5 | lets the learner read before seeing a failure color |
| Normalize the difficulty | 8 | "most people miss this" |
| Offer an exit | 6 | a different task, not just a hint |
| Preserve work | 22 | never lose what the learner typed |
| Invite reflection later | 3 | return to the failure once it is solved |

# 4 Discussion
Designers described tension between honesty and comfort. "Normalize the difficulty" works only when it is true. Several designers had
removed celebratory animations after failures were resolved because learners found them patronizing.

# 5 Limitations
A review by one designer-researcher, and an interview sample recruited through professional networks.
''',
refs=['Norman, D. A. Emotional Design: Why We Love (or Hate) Everyday Things. Basic Books, 2004.',
      'Fredrickson, B. L. The role of positive emotions in positive psychology. American Psychologist 56, 3 (2001), 218-226.']),

# ------------------------------------------------------------------ Augmenting cognition
dict(
key='marchetti2024trails', type='inproceedings',
title='Trails Revisited: Associative Indexing in Personal Knowledge Tools Eighty Years After the Memex',
authors=[('Marchetti', 'Elisa')], year=2024,
booktitle='Proceedings of the 35th ACM Conference on Hypertext and Social Media', series="HT '24", pages='201--210',
publisher='ACM', address='Poznan, Poland', pub='2024-09-10 09:00', added='2026-08-26 22:47',
collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group', 'project_engelbart'], keywords=['memex', 'trails', 'personal knowledge management', 'hypertext history'],
abstract='Bush\'s memex proposed that a reader could tie two items together and later replay the chain of associations as a trail. '
'Contemporary personal knowledge tools implement links and backlinks but rarely trails: ordered, named, shareable paths through '
'material. We analyze 18 tools and find that 16 support bidirectional links, 5 support ordered sequences, and none preserves the '
'reason a connection was made. We argue the reason, not the link, was the memex\'s central idea.',
body='''
# 1 Introduction
The memex is often cited as the ancestor of hypertext. What Bush actually emphasized was the trail: a named sequence of items, built
while thinking, that could be handed to someone else. Links are a mechanism; trails are a record of thought.

# 2 Tools analyzed
We examined 18 personal knowledge tools available in 2024: note apps with backlinks, outliners, canvas tools and reference managers.

| Capability | Tools (of 18) |
| Bidirectional links | 16 |
| Graph view | 12 |
| Ordered, named sequences | 5 |
| Sharing a sequence with others | 3 |
| Recording why a link was made | 0 |

# 3 What is missing
Every tool lets a user say that two notes are related. None records why, at the time the connection is made, in a form the tool can
use. Users who want this write it into the note body, where it is invisible to the link structure.

Five tools support sequences, but sequences are authored after the fact as tables of contents, not accumulated during reading.

# 4 Design proposals
- Capture the context of a link at creation: what was open, what was just read, what the user typed.
- Treat trails as first-class objects that can be replayed and forked.
- Let a trail survive export.

# 5 Conclusion
The question "where did this idea come from?" is answerable only if the tool keeps the path, not just the endpoints.
''',
refs=['Bush, V. As we may think. The Atlantic Monthly 176, 1 (1945), 101-108.',
      'Nelson, T. H. Complex information processing: a file structure for the complex, the changing and the indeterminate. In Proceedings of the 20th ACM National Conference (1965), 84-100.']),

dict(
key='halvorsen2025where', type='article',
title='Where Did That Idea Come From? Provenance Trails in Researchers\' Note-Taking',
authors=[('Halvorsen', 'Tor'), ('Quist', 'Amara')], year=2025,
journal='Proceedings of the ACM on Human-Computer Interaction', volume='9', number='CSCW2', pages='1--24',
pub='2025-10-18 09:00', added='2026-09-02 23:31',
collections=['Augmenting cognition', 'Engelbart competitors'], projects=['project_augmenting_cognition_reading_group', 'project_engelbart'],
keywords=['provenance', 'note-taking', 'diary study', 'researchers'],
abstract='Researchers write notes across many tools and later struggle to recall where an idea came from. In a three-week diary study '
'with 19 researchers, we asked participants to trace the origin of a sample of their own notes. After two weeks, 31% of notes had no '
'recoverable source; most of these originated in conversations, chat with AI assistants, or reading that was not saved. Participants '
'valued provenance most when writing related work and when revisiting abandoned projects.',
body='''
# 1 Introduction
A note records an idea; it rarely records the source. Researchers rebuild provenance when they need it, often at the worst time, such
as when citing.

# 2 Method
19 researchers (PhD students to faculty, HCI, education and biology) kept a diary for three weeks. Twice a week, we sampled five of
their notes from the previous days and asked them to find where each idea came from and how long it took.

# 3 Findings
| Origin of note | Share of notes | Recoverable after 2 weeks |
| Paper or article read | 34% | 81% |
| Conversation (meeting, hallway) | 22% | 39% |
| Chat with AI assistant | 17% | 46% |
| Own earlier note | 15% | 88% |
| Talk or video | 7% | 52% |
| Unknown at time of writing | 5% | - |

Overall, 31% of sampled notes had no recoverable source after two weeks. Median search time for recoverable sources was 3.5 minutes.

AI chats were a growing and fragile source: participants rarely saved them, and those who did could not search across providers.

# 4 Implications
Tools should attach source context automatically at capture time, link notes to conversations and chats, and make provenance visible
in the places researchers write (drafts, related-work sections). A single import of a researcher's existing tools is a precondition.

# 5 Limitations
Self-selected participants who already cared about note-taking; three weeks is short relative to a research project.
''',
refs=['Marchetti, E. Trails revisited. HT 2024, 201-210.',
      'Engelbart, D. C. Augmenting Human Intellect: A Conceptual Framework. SRI Summary Report AFOSR-3223, Stanford Research Institute, 1962.']),

dict(
key='sato2023bootstrapping', type='inproceedings',
title='Bootstrapping, Measured: Toward an Operational Definition of Collective IQ in Research Teams',
authors=[('Sato', 'Hiroshi'), ('Lemaire', 'Claire')], year=2023,
booktitle='Extended Abstracts of the 2023 CHI Conference on Human Factors in Computing Systems', series="CHI EA '23", pages='1--7',
publisher='ACM', address='Hamburg, Germany', pub='2023-04-19 09:00', added='2026-09-14 00:18',
collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['collective intelligence', 'research teams', 'bootstrapping'],
abstract='Engelbart argued that groups should improve the way they improve. We propose three operational measures of a research team\'s '
'collective capability, namely time-to-reuse of prior work, cross-member retrieval success and decision traceability, and pilot them '
'with four lab groups over eight weeks. Teams with shared, searchable records had faster reuse but not better traceability.',
body='''
# 1 Introduction
"Collective IQ" is a powerful phrase and an unmeasured one. Without measures, claims that a tool augments a group cannot be tested.

# 2 Measures
- Time-to-reuse: days between a piece of work being produced and its first reuse by another member.
- Cross-member retrieval: share of successful attempts by one member to find something another member produced, in a timed task.
- Decision traceability: share of a sample of past decisions for which the team can name the evidence and the meeting where it was
  decided.

# 3 Pilot
Four lab groups (5-9 members) participated for eight weeks. Two used a shared, searchable notes system; two used individual tools.

| Group | Shared records | Median time-to-reuse (days) | Retrieval success | Traceability |
| A | yes | 6 | 72% | 41% |
| B | yes | 9 | 68% | 35% |
| C | no | 17 | 44% | 38% |
| D | no | 21 | 39% | 30% |

# 4 Discussion
Shared records helped people find things but did not help them reconstruct why decisions were made. Decisions lived in meetings and
chats that no one recorded.

# 5 Limitations
Four groups, eight weeks, and measures that need validation.
''',
refs=['Engelbart, D. C. Augmenting Human Intellect: A Conceptual Framework. SRI, 1962.',
      'Hutchins, E. Cognition in the Wild. MIT Press, 1995.']),

# ------------------------------------------------------------------ Engelbart competitors
dict(
key='rinaldi2025importing', type='inproceedings',
title='Importing a Life: Duplicate and Near-Duplicate Detection Across Personal Information Sources',
authors=[('Rinaldi', 'Paola'), ('Uddin', 'Farhan')], year=2025,
booktitle='Proceedings of the 2025 ACM SIGIR Conference on Human Information Interaction and Retrieval', series="CHIIR '25", pages='96--107',
publisher='ACM', address='Melbourne, Australia', pub='2025-03-24 09:00', added='2026-10-12 23:04',
collections=['Engelbart competitors'], projects=['project_engelbart'], keywords=['deduplication', 'personal information management', 'import'],
abstract='Personal information tools increasingly offer to import everything a user has: email, files, notes, chats and references. '
'Imports produce duplicates. We collected consented exports from 14 participants across 9 source types and annotated duplicate and '
'near-duplicate pairs. 18% of imported items had at least one duplicate. Exact hashing found 41% of duplicate pairs, title-and-size '
'matching 73%, and content shingling 92%, but shingling also falsely merged successive versions of drafts that participants wanted '
'kept apart. We propose a two-stage policy: merge exact duplicates silently, group near-duplicates for the user to confirm.',
body='''
# 1 Introduction
The same PDF arrives through a reference manager, the downloads folder and an email attachment. The same draft exists as "report",
"report v2" and "Copy of report". A tool that imports all of these without care shows the user three of everything.

# 2 Data
14 participants (graduate students and knowledge workers) shared exports from up to 9 sources: email, cloud drive, local files,
reference manager, note app, chat assistant, calendar, code repositories and messaging. We annotated 6,410 candidate pairs.

| Duplicate kind | Pairs | Example |
| Exact byte copy | 512 | same PDF in Downloads and the reference manager |
| Same work, different file | 388 | preprint vs published version |
| Draft versions | 446 | report.docx vs report v2.docx |
| Same content, different format | 207 | note exported as Markdown and HTML |

# 3 Detection
| Method | Recall (all dup pairs) | False merges of draft versions |
| Exact hash | 41% | 0% |
| Title + size | 73% | 12% |
| Content shingling (Jaccard >= 0.8) | 92% | 61% |

Participants were clear that preprint and published versions of a paper are "the same paper" for reading, but drafts of their own
writing are not duplicates: each version marks a decision.

# 4 Policy
Merge exact duplicates silently and keep every location as provenance. Group same-work items (for example by DOI or normalized title)
under one entry. Show near-duplicate drafts as a version stack the user can expand, never merged.

# 5 Limitations
Fourteen participants; English-language content; exports taken at one point in time.
''',
refs=['Marchetti, E. Trails revisited: associative indexing in personal knowledge tools eighty years after the memex. HT 2024, 201-210.',
      'Sato, H. and Lemaire, C. Bootstrapping, measured. CHI EA 2023.']),

# ------------------------------------------------------------------ Unfiled (not project-related)
dict(
key='ellingsen2023polarized', type='article',
title='Polarized versus Threshold Intensity Distribution in Sub-Elite Middle-Distance Runners: A 16-Week Randomized Trial',
authors=[('Ellingsen', 'Kari'), ('Mwangi', 'Peter')], year=2023,
journal='Journal of Endurance Training Science', volume='11', number='3', pages='212--229', pub='2023-06-02 09:00', added='2026-01-18 22:12',
collections=[], projects=['project_endurance_training'], keywords=['polarized training', 'zone 2', 'middle distance', 'running'],
abstract='We randomized 34 sub-elite middle-distance runners to 16 weeks of polarized (about 80% low intensity, 20% high) or threshold-'
'focused training at matched total load. Both groups improved 1500 m time-trial performance; the polarized group improved more (2.1% '
'vs 1.4%). Velocity at lactate threshold improved similarly in both groups. Runners in the polarized group reported lower perceived '
'fatigue across the block.',
body='''
# 1 Introduction
Endurance coaches debate how to distribute intensity. Polarized programs keep most volume easy and add a small amount of very hard
work; threshold programs spend more time near lactate threshold. Evidence in middle-distance runners, whose events are short and
intense, is limited.

# 2 Methods
34 runners (1500 m personal bests 3:52-4:30 for men, 4:25-5:05 for women) were randomized to polarized (POL, n = 17) or threshold
(THR, n = 17) training for 16 weeks. Weekly training load was matched with session RPE. Intensity zones were set from a lactate test
before the block.

| Variable | POL pre | POL post | THR pre | THR post |
| 1500 m time trial (s) | 262.4 | 256.9 | 263.1 | 259.4 |
| vLT (km/h) | 16.1 | 16.8 | 16.0 | 16.7 |
| VO2max (ml/kg/min) | 62.3 | 64.0 | 61.9 | 62.8 |
| Weekly volume (h) | 7.8 | 8.4 | 7.9 | 8.1 |

# 3 Results
Both groups improved time-trial performance (POL 2.1%, THR 1.4%; group x time p = 0.04). Velocity at lactate threshold improved
similarly. Perceived fatigue (weekly questionnaire) was lower in POL from week 6 onward.

# 4 Discussion
For middle-distance runners, keeping easy days easy and concentrating hard work appears at least as effective as a threshold-heavy
program and better tolerated. Base phases built on long low-intensity volume remain a reasonable foundation.

# 5 Limitations
Small sample, one training group, and a block too short to observe long-term adaptations.
''',
refs=['Zone definitions, lactate protocols and individual training logs are available in the supplementary material.']),

dict(
key='draxler2025chokepoints', type='techreport',
title='Chokepoints and Patience: Export Controls as Grand Strategy in the Semiconductor Contest',
authors=[('Draxler', 'Viktor')], year=2025,
institution='Meridian Institute for Strategic Studies', number='Working Paper 25-07', pub='2025-09-15 09:00', added='2025-12-28 23:40',
collections=[], projects=['project_none'], keywords=['geopolitics', 'export controls', 'semiconductors', 'grand strategy'],
abstract='Export controls on advanced semiconductors and the tools to make them are often discussed as trade policy. This paper treats '
'them as grand strategy: a bet that a lead in a few chokepoint technologies can be converted into time. We set out the conditions '
'under which such a bet pays off (the chokepoint is real, allies hold the line, and the time bought is used) and argue that the third '
'condition receives the least attention.',
body='''
# 1 Argument
A chokepoint strategy has three parts: deny a rival a technology it cannot quickly make itself, keep partners aligned so the denial
holds, and use the time bought to extend one's own lead. Most debate focuses on the first two. This paper argues that the third is the
one that decides the outcome.

# 2 Conditions
| Condition | Question | Failure mode |
| Real chokepoint | Can the rival substitute within the planning horizon? | controls accelerate domestic substitution |
| Coalition | Do the few suppliers of the controlled items comply? | leakage through third countries |
| Use of time | Is the lead reinvested? | complacency behind the wall |

# 3 Time as the currency
Controls buy years, not permanence. Historical technology-denial regimes held for a decade or so before substitution or diffusion
eroded them. The strategic question is what is built in that decade: manufacturing capacity, talent pipelines, and the next generation
of tools.

# 4 Patience
Grand strategies fail when they demand quick results. Controls impose costs on the controlling side's firms immediately and deliver
benefits slowly. A strategy that cannot survive two electoral cycles is not a strategy.

# 5 Historical analogies and their limits
Cold War technology-denial regimes are the obvious comparison. They held longest where the controlled items were embedded in
complex supply chains that a single country could not rebuild, and they eroded fastest where the knowledge was in people rather than in
machines. Semiconductor manufacturing sits at both extremes at once: tools are concentrated in a handful of firms, but process know-how
moves with engineers.

| Era | Controlled domain | Approximate effective duration | What eroded it |
| Early Cold War | high-performance computing | 10-15 years | commercial diffusion of components |
| 1980s | machine tools and precision milling | about 8 years | third-country suppliers |
| 2020s | leading-edge chips and lithography tools | open question | substitution and stockpiling |

The table is illustrative; durations depend on how one defines "effective". The pattern is that denial buys time measured in years,
and that diffusion through commercial channels is the usual end.

# 6 Coalition maintenance
Controls held by one country invite substitution by its partners' firms. The coalition question is therefore about compensation: who
bears the lost revenue, and what do they receive in exchange? Arrangements that leave allied firms bearing costs with no share of the
strategic benefit are unstable. The paper proposes that coalition partners be offered priority access to the capacity built during the
window, which ties the third condition (use of time) to the second (coalition).

# 7 Indicators to watch
- Domestic tool substitution: share of a rival's new fabrication capacity using domestically produced tools.
- Talent flows: net movement of process engineers between the two ecosystems.
- Reinvestment: capital expenditure on next-generation capacity inside the coalition, relative to the pre-control baseline.
- Leakage: re-export volumes through third countries.

# 8 Conclusion
Measure the policy by what the time is used for, not by how long the wall stands.
''',
refs=['Working paper; views are the author\'s own.']),
]

# Real works: bibliographic metadata only (no PDFs, no abstracts).
REAL = [
 dict(key='kapur2008productive', type='article', title='Productive Failure', authors=[('Kapur', 'Manu')], year=2008,
      journal='Cognition and Instruction', volume='26', number='3', pages='379--424', added='2026-03-24 00:31',
      collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['productive failure', 'learning sciences']),
 dict(key='cohen1960coefficient', type='article', title='A Coefficient of Agreement for Nominal Scales', authors=[('Cohen', 'Jacob')], year=1960,
      journal='Educational and Psychological Measurement', volume='20', number='1', pages='37--46', added='2026-03-27 01:45',
      collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['inter-rater reliability']),
 dict(key='landis1977measurement', type='article', title='The Measurement of Observer Agreement for Categorical Data',
      authors=[('Landis', 'J. Richard'), ('Koch', 'Gary G.')], year=1977, journal='Biometrics', volume='33', number='1', pages='159--174',
      added='2026-03-27 01:49', collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['inter-rater reliability']),
 dict(key='aleven2003help', type='article', title='Help Seeking and Help Design in Interactive Learning Environments',
      authors=[('Aleven', 'Vincent'), ('Stahl', 'Elmar'), ('Schworm', 'Silke'), ('Fischer', 'Frank'), ('Wallace', 'Raven')], year=2003,
      journal='Review of Educational Research', volume='73', number='3', pages='277--320', added='2026-03-30 23:10',
      collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['help-seeking']),
 dict(key='wood1976role', type='article', title='The Role of Tutoring in Problem Solving',
      authors=[('Wood', 'David'), ('Bruner', 'Jerome S.'), ('Ross', 'Gail')], year=1976,
      journal='Journal of Child Psychology and Psychiatry', volume='17', number='2', pages='89--100', added='2026-03-30 23:14',
      collections=['TutorTrace UIST26'], projects=['project_tutortrace'], keywords=['scaffolding']),
 dict(key='kaufman2012leakage', type='article', title='Leakage in Data Mining: Formulation, Detection, and Avoidance',
      authors=[('Kaufman', 'Shachar'), ('Rosset', 'Saharon'), ('Perlich', 'Claudia'), ('Stitelman', 'Ori')], year=2012,
      journal='ACM Transactions on Knowledge Discovery from Data', volume='6', number='4', pages='15:1--15:21', added='2026-07-25 00:20',
      collections=['IDETrace'], projects=['project_idetrace'], keywords=['data leakage']),
 dict(key='gebru2021datasheets', type='article', title='Datasheets for Datasets',
      authors=[('Gebru', 'Timnit'), ('Morgenstern', 'Jamie'), ('Vecchione', 'Briana'), ('Vaughan', 'Jennifer Wortman'), ('Wallach', 'Hanna'),
               ('Daumé III', 'Hal'), ('Crawford', 'Kate')], year=2021,
      journal='Communications of the ACM', volume='64', number='12', pages='86--92', added='2026-05-04 22:58',
      collections=['IDETrace'], projects=['project_idetrace'], keywords=['documentation', 'datasets']),
 dict(key='picard1997affective', type='book', title='Affective Computing', authors=[('Picard', 'Rosalind W.')], year=1997,
      publisher='MIT Press', address='Cambridge, MA', added='2026-01-14 21:20',
      collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['affective computing']),
 dict(key='norman2004emotional', type='book', title='Emotional Design: Why We Love (or Hate) Everyday Things', authors=[('Norman', 'Donald A.')],
      year=2004, publisher='Basic Books', address='New York', added='2026-01-21 22:02',
      collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['emotional design']),
 dict(key='russell1980circumplex', type='article', title='A Circumplex Model of Affect', authors=[('Russell', 'James A.')], year=1980,
      journal='Journal of Personality and Social Psychology', volume='39', number='6', pages='1161--1178', added='2026-01-27 23:41',
      collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['affect', 'valence', 'arousal']),
 dict(key='dmello2012dynamics', type='article', title='Dynamics of Affective States during Complex Learning',
      authors=[("D'Mello", 'Sidney'), ('Graesser', 'Art')], year=2012, journal='Learning and Instruction', volume='22', number='2',
      pages='145--157', added='2026-02-03 21:48',
      collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['confusion', 'affect dynamics']),
 dict(key='baker2010better', type='article',
      title="Better to Be Frustrated than Bored: The Incidence, Persistence, and Impact of Learners' Cognitive-Affective States during Interactions with Three Different Computer-Based Learning Environments",
      authors=[('Baker', 'Ryan S. J. d.'), ("D'Mello", 'Sidney K.'), ('Rodrigo', 'Ma. Mercedes T.'), ('Graesser', 'Arthur C.')], year=2010,
      journal='International Journal of Human-Computer Studies', volume='68', number='4', pages='223--241', added='2026-02-10 23:31',
      collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['boredom', 'frustration']),
 dict(key='fredrickson2001role', type='article',
      title='The Role of Positive Emotions in Positive Psychology: The Broaden-and-Build Theory of Positive Emotions',
      authors=[('Fredrickson', 'Barbara L.')], year=2001, journal='American Psychologist', volume='56', number='3', pages='218--226',
      added='2026-03-02 21:15', collections=['ISE 6664 readings'], projects=['project_ise6664_affective_computing'], keywords=['positive emotions']),
 dict(key='bush1945we', type='article', title='As We May Think', authors=[('Bush', 'Vannevar')], year=1945,
      journal='The Atlantic Monthly', volume='176', number='1', pages='101--108', added='2026-01-29 00:52',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['memex', 'trails']),
 dict(key='licklider1960mancomputer', type='article', title='Man-Computer Symbiosis', authors=[('Licklider', 'J. C. R.')], year=1960,
      journal='IRE Transactions on Human Factors in Electronics', volume='HFE-1', number='1', pages='4--11', added='2026-08-25 23:15',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['symbiosis']),
 dict(key='engelbart1962augmenting', type='techreport', title='Augmenting Human Intellect: A Conceptual Framework',
      authors=[('Engelbart', 'Douglas C.')], year=1962, institution='Stanford Research Institute', number='Summary Report AFOSR-3223',
      address='Menlo Park, CA', added='2026-01-29 01:05',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group', 'project_engelbart'], keywords=['augmentation', 'bootstrapping']),
 dict(key='nelson1965complex', type='inproceedings',
      title='Complex Information Processing: A File Structure for the Complex, the Changing and the Indeterminate', authors=[('Nelson', 'T. H.')],
      year=1965, booktitle='Proceedings of the 1965 20th National Conference', series="ACM '65", pages='84--100', publisher='ACM',
      added='2026-08-25 23:22', collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['hypertext']),
 dict(key='engelbart1968research', type='inproceedings', title='A Research Center for Augmenting Human Intellect',
      authors=[('Engelbart', 'Douglas C.'), ('English', 'William K.')], year=1968,
      booktitle='Proceedings of the December 9-11, 1968, Fall Joint Computer Conference, Part I', series="AFIPS '68 (Fall, part I)",
      pages='395--410', added='2026-08-31 22:30',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group', 'project_engelbart'], keywords=['NLS', 'augmentation']),
 dict(key='clark1998extended', type='article', title='The Extended Mind', authors=[('Clark', 'Andy'), ('Chalmers', 'David')], year=1998,
      journal='Analysis', volume='58', number='1', pages='7--19', added='2026-09-08 00:40',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['extended mind']),
 dict(key='hutchins1995cognition', type='book', title='Cognition in the Wild', authors=[('Hutchins', 'Edwin')], year=1995,
      publisher='MIT Press', address='Cambridge, MA', added='2026-09-14 00:05',
      collections=['Augmenting cognition'], projects=['project_augmenting_cognition_reading_group'], keywords=['distributed cognition']),
 dict(key='stokes2005creativity', type='book', title='Creativity from Constraints: The Psychology of Breakthrough',
      authors=[('Stokes', 'Patricia D.')], year=2005, publisher='Springer Publishing Company', address='New York', added='2024-11-06 22:14',
      collections=['PlotPact (old)'], projects=['project_plotpact'], keywords=['constraints', 'creativity']),
 dict(key='boden2004creative', type='book', title='The Creative Mind: Myths and Mechanisms', authors=[('Boden', 'Margaret A.')], year=2004,
      edition='2', publisher='Routledge', address='London', added='2024-11-06 22:20',
      collections=['PlotPact (old)'], projects=['project_plotpact'], keywords=['creativity']),
]

# Competitor web pages: metadata only (title, URL, access date). No claims about the products.
WEB = [
 dict(key='notebooklm', title='NotebookLM', url='https://notebooklm.google.com/', added='2026-08-25 22:51'),
 dict(key='elicit', title='Elicit', url='https://elicit.com/', added='2026-08-27 01:12'),
 dict(key='heptabase', title='Heptabase', url='https://heptabase.com/', added='2026-09-01 23:40'),
 dict(key='obsidian', title='Obsidian', url='https://obsidian.md/', added='2026-10-12 22:47'),
]
for w in WEB:
    w.update(type='online', authors=[], year=2026, collections=['Engelbart competitors'],
             projects=['project_engelbart', 'project_mathetic_company'], keywords=['competitor'])
