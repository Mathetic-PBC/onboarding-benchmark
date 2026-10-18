"""Hand-written PDFs for synthetic/pdfs (PDFs on David's Mac). All organisations except Virginia Tech, UIST/ACM and Surplus are
fictional; all people are from PERSON.md §2 or fictional walk-ons. Bodies use content/zotero/dsl.py markup.

Fields: path (home-relative), title (PDF title + first heading), author (PDF Author), body, file (created, modified) = file times,
pdf (created, modified) = PDF internal dates (default = file times), projects, notes."""

TUTORTRACE_CR_TITLE = 'TutorTrace: Classifying Learner States from Replayed AI-Assisted Programming Sessions'
TUTORTRACE_CR = '''
David Barron, et al. -- PRIME Lab, Department of Computer Science, Virginia Tech

UIST '26, October 2026. Camera-ready version.

## Abstract
Students in programming courses now work alongside AI assistants, and the moments when they need a person are hidden inside long
sessions of editing, running and prompting. We present TutorTrace, a dataset and taxonomy for classifying learner states from
replayed sessions that combine editor events, run results and assistant prompts. From a live deployment in a data structures course
(87 students, two lab sections), three trained raters labeled 2,340 thirty-second windows into six states, including a
stalled-after-error state that separates unproductive stalling from exploratory tinkering. Agreement was Fleiss' kappa 0.71. A
gradient-boosted classifier over telemetry features reached macro-F1 0.78 on held-out students and 0.69 on a second course after
per-course normalization. We describe the replay-based labeling interface, release the labeling guide and data under per-stream
consent, and discuss how such signals should prompt human check-ins rather than automatic interventions.

# 1 Introduction
An instructor walking around a lab sees a student staring at a screen. Is the student thinking, or stuck? With AI assistants in the
loop, the question has become harder: a student may be productively testing an assistant's suggestion, or cycling through the same
request with growing frustration. Neither the assistant nor the autograder sees the whole session.

TutorTrace makes the whole session visible. We contribute (1) a replayable dataset of AI-assisted programming sessions from a live
deployment, (2) a six-state taxonomy with a labeling guide and reliability evidence, and (3) a classifier and a cross-course analysis
that show what transfers and what does not.

# 2 Related Work
Process data from programming environments has been used to detect struggle and to support instructors through session replay.
Closest to our work, Ostrowski et al. labeled thirty-second windows of LLM-assisted CS1 sessions into four states and found repeated
near-identical prompts to be the strongest predictor of stalling. Our taxonomy separates stalled-after-error from general stalling and
from exploratory tinkering, and we evaluate transfer to a second course. Work on productive failure reminds us that some struggle is
valuable; our goal is to find the struggle that is not.

# 3 Data
## 3.1 Deployment
We deployed an instrumented browser editor with an assistant side panel in CS 3114 (Data Structures and Algorithms) in Fall 2025.
The labeled session took place in two lab sections led by three TAs. The editor logged insertions, deletions, pastes, runs with results,
and assistant exchanges with millisecond timestamps.

## 3.2 Telemetry gap
A websocket reconnect bug dropped roughly 12% of events in one section until a hotfix was deployed during the lab. We excluded every
window overlapping the gap before labeling and release the list of excluded windows.

## 3.3 Data and consent
Consent separated three streams: editor events, run results and assistant prompts. Nine of 87 students declined prompt logging. The
release contains derived features and labels for all consenting students and raw prompt text only for students who opted in to its
release. Identifiers are replaced with per-release random ids and string literals are stripped from code snapshots. A datasheet is in
the supplementary material.

# 4 Taxonomy and Labeling
| State | Definition (abridged) | Share of windows |
| Productive progress | edits that move toward a passing run | 31% |
| Exploratory tinkering | rapid small edits and runs, no reverts | 18% |
| Stalled after error | no successful run in 3 min, reverted edits or idle after an error | 14% |
| Assistant help-seeking | composing or reading an assistant exchange | 17% |
| Verifying | running tests and inspecting output | 13% |
| Disengaged | idle or off-task without a preceding error | 7% |

Raters labeled windows in a replay interface that shows the editor, a timeline with run and idle markers, and the assistant panel,
with 30 seconds of preceding context. After two calibration rounds with guide v3, three raters labeled all 2,340 windows independently.

| Agreement | Fleiss' kappa |
| Overall (3 raters) | 0.71 |
| Assistant help-seeking | 0.84 |
| Verifying | 0.77 |
| Productive progress | 0.73 |
| Disengaged | 0.66 |
| Tinkering vs stalled-after-error | 0.58 |

The tinkering/stalled boundary was hardest. Guide v3's rule for it raised agreement on that pair from 0.49 to 0.58.

# 5 Classifier
We trained gradient-boosted trees over 46 features per window: edit and run rates, time since last successful run, idle gaps,
revert counts, prompt counts and prompt similarity to the previous prompt. All evaluation uses folds grouped by student.

| Model | Macro-F1 (held-out students) |
| Majority class | 0.08 |
| Counts only (logistic regression) | 0.64 |
| Gradient boosting, all features | 0.78 |

The most important features were time since the last successful run, prompt similarity to the previous prompt, and idle time
following a failed run.

# 6 Cross-Course Analysis
To test generality we labeled 610 windows from an introductory Python course (Spring 2026, 41 students) with the same guide and
raters, trained on CS 3114 and tested on the second course.

| Test set | Macro-F1 raw | Macro-F1 normalized | F1 stalled-after-error |
| CS 3114, held-out students | 0.78 | 0.78 | 0.71 |
| Intro Python (Spring 2026) | 0.64 | 0.69 | 0.52 |

Normalizing rate features per course recovered part of the gap. Stalled-after-error transferred worst, because its signature depends
on the course's error messages and run habits.

# 7 Discussion
Telemetry can say that a student is probably stalled; it cannot say why. We recommend using predictions as prompts for a human
check-in, with replay as a second stage for flagged sessions. Assistant prompts were the most sensitive stream for students; derived
labels may be enough for most uses.

# 8 Limitations
Two courses at one institution; labels are judgments even at kappa 0.71; states depend on the assistant students used; the telemetry
gap shows that infrastructure failures shape datasets.

# References
[1] Ostrowski, H., Lindqvist, M., Bello, A., and Chandrasekar, R. Productive struggle or silent stalling? Telemetry signals of
help-seeking in LLM-assisted CS1. L@S 2025, 112-123.

[2] Kapur, M. Productive failure. Cognition and Instruction 26, 3 (2008), 379-424.

[3] Nakamura, R. and Feld, S. Labeling learner states in programming sessions. ICER 2025, 233-245.

[4] Duarte, P. and Sim, H. Beyond one course: do behavioral-state classifiers transfer across programming courses? EDM 2025.

[5] Brennan, C., Zhou, W., and Adler, R. What will students share? arXiv:2602.11873, 2026.
'''

DOCS = [
# ------------------------------------------------------------------ TutorTrace / UIST
dict(path='Desktop/UIST talk/TutorTrace_UIST26_talk.pdf', title='TutorTrace: Classifying Learner States in AI-Assisted Programming',
     author='David Barron', file=('2026-10-06 23:20', '2026-10-06 23:20'), projects=['project_tutortrace'],
     notes='slides exported from the Overleaf beamer project "UIST26 talk script (beamer)" (no speaker notes)', kind='slides'),
dict(path='Downloads/UIST2026_program_Learning_and_Tutoring.pdf', title='UIST 2026 Program - Session: Learning & Tutoring',
     author='', file=('2026-09-28 21:14', '2026-09-28 21:14'), pdf=('2026-09-25 18:00', '2026-09-25 18:00'), projects=['project_tutortrace'],
     notes='program excerpt for David\'s session; other talks in the session are fictional', body='''
UIST 2026 -- The ACM Symposium on User Interface Software and Technology

Program excerpt -- Wednesday, October 7, 2026

## Session: Learning & Tutoring
Session chair: Tomás Reyes

Time: 10:40 - 12:00. Each paper: 15 minute talk + 5 minutes Q&A.

| Time | Paper | Presenter |
| 10:40 | TutorTrace: Classifying Learner States from Replayed AI-Assisted Programming Sessions | David Barron |
| 11:00 | ScaffoldLens: Visualizing How Hints Change Novice Code Over Time | Mira Castellanos |
| 11:20 | Pair-Prompting: Co-Writing Assistant Requests in Collaborative Programming Labs | Anders Holm |
| 11:40 | Chalkline: A Pen-Based Tutor for Stepwise Algebra with Live Misconception Feedback | Yusuf Demir |

## Presenter information
Please arrive in the session room 10 minutes before the session starts and introduce yourself to the session chair. Rooms are
equipped with HDMI and USB-C; bring adapters for other connectors. Slides must be 16:9. A presenter view is available if your laptop
supports a second display. Session chairs will give a 5-minute and a 1-minute warning.

## Accessibility
Live captioning is provided in all paper sessions. Presenters are asked to describe key figures verbally and to avoid relying on
color alone.
'''),
dict(path='Downloads/IDETrace_NeurIPS26_author_response.pdf', title='IDETrace -- Author Response (NeurIPS 2026 Datasets & Benchmarks)',
     author='David Barron', file=('2026-07-29 18:31', '2026-07-29 18:31'), pdf=('2026-07-29 18:29', '2026-07-29 18:29'),
     projects=['project_idetrace'], notes='compiled from the Overleaf project "IDETrace NeurIPS rebuttal"', kind='idetrace_rebuttal'),
dict(path='Desktop/IDETrace/leakage_writeup_0725.pdf', title='IDETrace split leakage -- what happened and what changes',
     author='David Barron', file=('2026-07-25 14:12', '2026-07-25 14:12'), projects=['project_idetrace'],
     notes='internal two-page memo for Yan before the rebuttal', body='''
Internal memo -- David Barron to Dr. Yan Chen -- July 25, 2026

## Summary
Our IDETrace evaluation leaked. make_splits.py assigned thirty-second windows to folds with KFold over rows, so windows from the same
student were in both training and test folds. With folds grouped by student id, the transformer baseline drops from 0.81 to 0.74
macro-F1. The ranking of models does not change. I propose we report both numbers in the rebuttal (due July 29) and release v1.1
splits grouped by student.

## How I found it
While computing per-class F1 for reviewer xT4q, I trained a quick probe to predict student id from the window features as a sanity
check. It reached 49% top-1 accuracy over 160 students. That is far above chance (0.6%) and means a model can recognize who wrote a
window. I then checked make_splits.py: it shuffles windows, not students.

## Corrected results
| Model | Random split | Grouped by student | Held-out lab section |
| Counts + logistic regression | 0.69 | 0.66 | 0.65 |
| Counts + gradient boosting | 0.77 | 0.71 | 0.70 |
| GRU | 0.79 | 0.72 | 0.71 |
| Transformer baseline | 0.81 | 0.74 | 0.73 |

## What changes
- make_splits.py: GroupKFold(n_splits=5) on student_id, fixed seed; unit test that fails if any student id appears in two folds.
- Datasheet: state the split unit; add the probe accuracy.
- Paper: Section 5 rewritten around grouped results; footnote with original numbers.
- Release: v1.1 splits; v1.0 kept but marked deprecated.

## What I need from you
A yes/no on reporting both numbers in the general response (my recommendation: yes, we found it ourselves and it reads better to say
so plainly). And whether you want Rezky to re-run the GRU baselines independently before Wednesday.

## Related reading
Ferreira and Kowalczyk (JEDM 2023) document the same failure across eleven tasks, with drops of 4 to 17 points; ours (7 points) is in
the middle of their range.
'''),
# ------------------------------------------------------------------ ISE 6664
dict(path='Desktop/ISE6664/ISE6664_Final_Report_draft.pdf', title='Frustration Signals in AI-Tutoring Transcripts (DRAFT)',
     author='David Barron', file=('2026-04-29 01:22', '2026-04-29 01:22'), projects=['project_ise6664_affective_computing'],
     notes='HARD CASE: near-duplicate — draft export of the ISE 6664 report two days before the final: no design-implications section, '
           'older detector numbers, "DRAFT" in title', kind='ise_draft'),
dict(path='Desktop/ISE6664/ISE6664_Final_Report_Barron_Torres_Lee.pdf',
     title='Frustration Signals in AI-Tutoring Transcripts: A Codebook and Detector for Programming Help Conversations',
     author='David Barron', file=('2026-05-02 01:21', '2026-05-02 01:21'), projects=['project_ise6664_affective_computing'],
     notes='HARD CASE: near-duplicate — final report PDF (compiled from the Overleaf project "ISE 6664 Final Report"); the draft sits next to it',
     kind='ise_final'),
dict(path='Downloads/ISE6664_Final_Project_Guidelines_Spring2026.pdf', title='ISE 6664 Final Project: Report and Presentation Guidelines',
     author='Alan Brooks', file=('2026-04-20 10:12', '2026-04-20 10:12'), pdf=('2026-04-17 15:30', '2026-04-17 15:30'),
     projects=['project_ise6664_affective_computing'], notes='course handout from Dr. Brooks', body='''
ISE 6664 Affective Design and Computing -- Spring 2026 -- Dr. Alan Brooks

## Deliverables
- Final presentation: Thursday, April 30, in class. 12 minutes plus 5 minutes of questions per team.
- Final report: due Saturday, May 2, 11:59 pm, via Canvas, one PDF per team.

## Report requirements
The report should be 12-16 pages, double-spaced, 12-point font, 1-inch margins, excluding references. It must include: a problem
statement grounded in affect theory from the course; related work; data and method; results; design implications; limitations; and a
statement of each team member's contributions.

## Grading
| Component | Weight |
| Theoretical grounding (course concepts used correctly) | 20% |
| Method and rigor | 25% |
| Results and analysis | 20% |
| Design implications | 15% |
| Writing and organization | 10% |
| Presentation | 10% |

## Notes
Projects that use human-subjects data must cite the IRB protocol or approval. If you reuse data from another project, say so and
describe what you added. Late reports lose 10% per day.
'''),
# ------------------------------------------------------------------ VT admin
dict(path='Downloads/LOA_form_Barron_signed_2026-07-31.pdf', title='Graduate School Request for Leave of Absence',
     author='Virginia Tech Graduate School', file=('2026-07-31 16:24', '2026-07-31 16:24'), pdf=('2026-07-27 11:02', '2026-07-31 16:18'),
     projects=['project_vt_phd_admin'], notes='leave-of-absence form, signed 2026-07-31 (Grace Kim processed)', body='''
Virginia Tech -- The Graduate School -- Request for Leave of Absence

## Student information
| Field | Entry |
| Name | David Barron |
| Student ID | 9061-XXXXX (redacted in this copy) |
| Degree / program | PhD, Computer Science |
| Department | Computer Science |
| Advisor | Dr. Yan Chen |
| VT email | dbarron410@vt.edu |

## Leave requested
| Field | Entry |
| First term of leave | Fall 2026 |
| Expected return term | Fall 2027 |
| Reason | Professional / entrepreneurial (co-founding a company related to research area) |
| Assistantship ends | August 15, 2026 |

## Student statement
I am requesting a leave of absence beginning Fall 2026 to co-found Mathetic, a public benefit corporation building research tools
closely related to my dissertation area. I will complete my outstanding UIST 2026 camera-ready and conference presentation
obligations, which concern work done while enrolled. I understand that I will not be enrolled during the leave, that my graduate
assistantship ends on August 15, 2026, and that I must notify the Graduate School before my expected return term.

## Signatures
| Role | Name | Date |
| Student | David Barron (signed) | 07/27/2026 |
| Advisor | Yan Chen (signed) | 07/29/2026 |
| Graduate program director | (signed) | 07/30/2026 |
| Graduate program coordinator | Grace Kim (processed) | 07/31/2026 |

Processing note: approved effective Fall 2026. Time-to-degree clock extended by the length of the approved leave. University email
and storage access remain active during an approved leave.
'''),
dict(path='Downloads/Travel_Funding_Request_UIST2026_Barron.pdf', title='CS Graduate Travel Funding Request',
     author='David Barron', file=('2026-09-24 11:06', '2026-09-24 11:06'), projects=['project_vt_phd_admin', 'project_tutortrace'],
     notes='VT CS travel-funding request submitted 2026-09-24 for the UIST talk', body='''
Department of Computer Science, Virginia Tech -- Graduate Student Travel Funding Request

Submitted: September 24, 2026 -- to Grace Kim, Graduate Program Coordinator

## Traveler
| Field | Entry |
| Name | David Barron |
| Program | PhD, Computer Science (on approved leave, Fall 2026) |
| Advisor | Dr. Yan Chen |
| Email | dbarron410@vt.edu |

## Event
| Field | Entry |
| Conference | UIST 2026, ACM Symposium on User Interface Software and Technology |
| Role | First author, full paper presentation |
| Paper | TutorTrace: Classifying Learner States from Replayed AI-Assisted Programming Sessions |
| Presentation date | October 7, 2026 |
| Travel dates | October 5 - October 8, 2026 |
| Departing from | San Francisco, CA |

## Budget
| Item | Estimated cost (USD) |
| Registration (student, early) | 450.00 |
| Airfare (economy, round trip) | 612.00 |
| Lodging (3 nights, shared room) | 495.00 |
| Ground transportation | 80.00 |
| Total requested | 1,637.00 |

## Justification
The paper reports work done while I was enrolled (data collected Fall 2025, submitted March 2026) and is co-authored with PRIME Lab
members. The leave policy allows travel support for work completed while enrolled if requested before the end of September.
Dr. Chen has approved the request; PRIME Lab will cover any amount not funded by the department.

## Attachments
Acceptance notification (July 2, 2026); registration quote; advisor approval email.
'''),
dict(path='iCloud Drive/Plan_of_Study_DBarron_PhD_CS.pdf', title='Plan of Study - Doctor of Philosophy, Computer Science',
     author='David Barron', file=('2025-10-29 15:41', '2025-10-29 15:41'), pdf=('2025-10-29 15:30', '2025-10-29 15:38'),
     projects=['project_vt_phd_admin'], notes='PhD plan of study filed Fall 2025', body='''
Virginia Tech -- Graduate School -- Plan of Study (Doctoral)

Student: David Barron -- Department: Computer Science -- Degree: PhD -- Advisor and committee chair: Dr. Yan Chen

Area: Human-Computer Interaction -- Filed: October 29, 2025

## Coursework
| Course | Title | Credits | Term | Status |
| CS 5714 | Usability Engineering | 3 | Fall 2024 | completed |
| CS 5724 | Models and Theories of Human-Computer Interaction | 3 | Fall 2024 | completed |
| CS 5805 | Machine Learning | 3 | Spring 2025 | completed |
| CS 6724 | Advanced Topics in HCI | 3 | Spring 2025 | completed |
| CS 5764 | Information Visualization | 3 | Fall 2025 | in progress |
| ISE 6664 | Affective Design and Computing | 3 | Spring 2026 | planned |
| STAT 5615 | Statistics in Research I | 3 | Spring 2026 | planned |
| CS 7994 | Research and Dissertation | 60+ | ongoing | ongoing |

## Milestones
| Milestone | Target |
| Qualifying exam | Spring 2026 |
| Preliminary exam (proposal) | Spring 2027 |
| Final defense | Spring 2028 |

## Notes
ISE 6664 counts as the out-of-department course. Committee membership to be finalized before the preliminary exam.
'''),
# ------------------------------------------------------------------ CS 3604 / VizPI
dict(path='Downloads/CS3604_P4_grading_rubric.pdf', title='CS 3604 Fall 2025 - Project 4 Grading Rubric (GTA copy)',
     author='David Barron', file=('2025-11-18 22:06', '2025-11-18 22:06'), projects=['project_cs3604_gta'],
     notes='GTA rubric for P4 incl. the late-day policy that came up in the regrade dispute', body='''
CS 3604 Professionalism in Computing -- Fall 2025 -- Project 4 rubric (GTA: David Barron)

## Scoring (100 points)
| Criterion | Points | Full credit means |
| Case analysis | 30 | identifies all stakeholders and at least two competing obligations |
| Use of ethical frameworks | 25 | applies two frameworks correctly and compares their conclusions |
| Recommendation | 20 | specific, actionable, and consistent with the analysis |
| Sources | 10 | at least four credible sources, cited consistently |
| Writing | 15 | clear structure, within 1,800-2,200 words |

## Late policy (from syllabus)
Each student has three late days for the semester, usable on P1-P4 but not the final project. Late days are counted in whole days
from the deadline (11:59 pm). Submissions after late days are exhausted lose 10% per day. Canvas timestamps are authoritative.

## Grader notes
- 64 students; P4 split with the other GTA by last name (A-L me).
- Deduct for word count only beyond 10% outside the range.
- Flag any submission that reads as generated without disclosure; do not deduct, send to instructor.
- Regrade requests go through the form within 7 days; I respond within 5 days.
'''),
dict(path='Desktop/vizpi/VizPI_deploy2_TA_runsheet.pdf', title='VizPI deployment #2 - CS 3114 lab - TA run sheet',
     author='David Barron', file=('2025-11-11 23:34', '2025-11-12 13:05'), projects=['project_vizpi'],
     notes='run sheet for the 2025-11-12 deployment', body='''
VizPI deployment #2 -- CS 3114, Wednesday November 12, 2025 -- lab session 3:30 pm ET

Host: John Wenskovitch. Research team: David, Minsun, Xiaohang. TAs: 3 (two sections).

## Before the lab (by 3:00 pm)
- Deploy vizpi_frontend build from main; confirm websocket server health check returns ok.
- Open the dashboard on the instructor laptop; check both section rooms appear.
- Print 90 consent sheets (87 enrolled) with the per-stream opt-in boxes.

## During the lab
| Time | Who | What |
| 3:30 | John | introduce the activity; consent reminder |
| 3:35 | David | students log in; check event counts per section on dashboard |
| 3:40-4:50 | TAs | circulate; note any student who asks for help (seat number + time) |
| every 10 min | Minsun | screenshot event-rate panel for both sections |
| 4:50 | John | wrap up, exit survey link |

## If events drop
If a section's event rate falls below 50% of the other section for more than 2 minutes, check the reconnect log. Do not restart the
server during the lab without telling John. Hotfix procedure: deploy the patched client, ask students to refresh once.

## After the lab
Export raw events to the lab bucket; record any gaps with start and end times in the deployment log. Labeling sprint starts Friday
(Nov 14) with Minsun and Xiaohang.

## Log (filled in after)
Section B lost events from about 3:52 pm (reconnect bug). Hotfix deployed 4:10 pm; students refreshed. About 12% of section B events
lost; gap recorded for exclusion.
'''),
dict(path='Downloads/Labeling_Guide_v3.pdf', title='Labeling Guide v3 - Learner States in Replayed Sessions',
     author='David Barron', file=('2025-11-15 01:12', '2025-11-15 01:12'), projects=['project_vizpi', 'project_tutortrace'],
     notes='labeling guide v3 (adds the stalled-after-error state) for the 11-14 -> 11-21 labeling sprint', body='''
PRIME Lab -- Labeling guide v3 -- November 14, 2025 -- for raters: David, Minsun, Xiaohang

## What changed from v2
- New state: stalled-after-error. Previously these windows were split between tinkering and disengaged.
- Decision rule for the tinkering / stalled boundary (below).
- Context: always watch the 30 seconds before the window.

## States
| State | Use when |
| Productive progress | edits that move toward a passing run; new code is kept |
| Exploratory tinkering | rapid small edits and runs, trying variations, no reverts |
| Stalled after error | after a failed run: no successful run in the last 3 minutes AND edits are reverted, or idle > 45 s |
| Assistant help-seeking | writing a prompt or reading an assistant response |
| Verifying | running tests and inspecting output after a change |
| Disengaged | idle or off-task without a preceding error |

## Decision rules
1. If the window contains an assistant exchange for more than half of its duration, label help-seeking.
2. If there was a failed run in the last 3 minutes, no successful run since, and the student reverts edits or is idle for more than 45
seconds, label stalled-after-error, even if the student is also typing.
3. If edits are kept and runs vary, prefer tinkering.
4. If a window clearly contains two states, label the one that occupies more time and tick the "mixed" box.

## Process
Label in batches of 50 windows. Do not discuss specific windows until the batch is submitted. Calibration rounds: 2 rounds of 40
windows with discussion. Target: all 2,340 windows by Friday, November 21.

## Excluded windows
Windows overlapping the section B telemetry gap on November 12 (3:52-4:10 pm) are pre-excluded and will not appear in the queue.
'''),
# ------------------------------------------------------------------ Engelbart / Mathetic
dict(path='Desktop/engelbart/import_dedupe_v2.pdf', title='Engelbart import: dedupe and grouping (v2)',
     author='David Barron', file=('2026-10-14 01:33', '2026-10-14 01:33'), projects=['project_engelbart'],
     notes='design doc exported to PDF for the 10-14 onboarding/import redesign', body='''
Engelbart -- Import redesign: dedupe and grouping -- v2, October 13, 2026 -- David (with Hudson)

## Why
Both pilots hit duplicate problems. Priya (Oct 9): the same paper appeared twice, once from Zotero and once from Downloads, and the
import missed about 140 of her Claude chats. Daniel (Oct 13): wanted Notion and Granola import and could not tell what the "Other"
tile on the connect screen meant.

## Three kinds of "same"
| Kind | Example | Policy |
| Exact copy | same PDF bytes in Zotero storage and ~/Downloads | merge silently; keep every location as provenance |
| Same work, different version | arXiv v1 and the camera-ready of one paper | group under one paper; show versions |
| Own drafts | report.pdf vs report_draft.pdf, Overleaf "Copy of" projects | version stack; never merge |

## Signals
- Exact: content hash (sha256).
- Same work: DOI or arXiv id when present; otherwise normalized title + first author + year.
- Drafts: same title stem with v2 / draft / "Copy of" / "(1)" markers, or same Overleaf project lineage; compare section headings.

## False merges to avoid
Content similarity alone merged draft versions about 61% of the time in a published study of personal imports. Our own test on my
accounts: shingling at Jaccard 0.8 merged the TutorTrace rebuttal with its copy, which I do not want merged.

## Connect screen
Rename "Other" to "Files & folders" and list what it covers. Add Notion and Granola tiles behind a "coming soon" state.

## Missed chats
Claude export pagination: the import stopped at the first page of conversations in a project. Fix in importer, add a count check
("we found 312 chats; your export lists 452").

## Next
Ship exact-merge + same-work grouping for pilot C; version stacks after.
'''),
dict(path='Downloads/Mathetic_onepager.pdf', title='Engelbart - Mathetic PBC', author='David Barron',
     file=('2026-08-18 22:52', '2026-08-18 22:52'), projects=['project_mathetic_company', 'project_engelbart'],
     notes='compiled one-pager downloaded from the Overleaf project "Mathetic one-pager"', body='''
A research notebook that remembers where your thoughts came from.

## The problem
Researchers think across a dozen tools: papers in a reference manager, drafts in Overleaf and Docs, ideas in chats with AI
assistants, decisions in Slack and meetings. Notes record ideas but not their sources. Two weeks later, about a third of a
researcher's notes can no longer be traced to where they came from, and AI chats are the hardest to recover.

## What Engelbart does
- Imports a researcher's existing tools in one step -- chats, files, papers, repos, notes, email and drive -- and groups them by project.
- Keeps provenance: every thought on the canvas links back to the chat, paper or conversation it came from.
- Deduplicates without losing history: the same paper from Zotero and Downloads becomes one entry; drafts stay as versions.
- Answers "where did this come from?" for any claim in a draft.

## Why now
AI assistants have multiplied the volume of research thinking that happens in chat. None of it is connected to the rest of a
researcher's work. Export formats are finally rich enough to import it.

## Who it is for, and who pays
PhD students and postdocs first, then research labs, then R&D teams in industry. Individuals pay a monthly subscription; labs pay per
seat with shared projects. Retention target for pilots: weekly use in 6 of the first 8 weeks.

## Traction
Working canvas prototype; import from 10+ sources; pilot onboarding sessions with researchers at UC Berkeley and CMU scheduled for
October 2026.

## Team
David Barron (CEO) -- HCI PhD student at Virginia Tech (on leave). Hudson Mitchell-Pullman (co-founder) -- product, design and
go-to-market. Based at the Surplus incubator, San Francisco.

## Public benefit
Mathetic is a Delaware public benefit corporation. Our purpose: to help people learn and think more clearly by keeping the record of
how their ideas formed in their own hands.

## The ask
Raising a pre-seed round on a SAFE to fund 12 months of product work and pilots.
'''),
dict(path='Downloads/Surplus_Fall2026_Residents_Handbook.pdf', title='Surplus - Fall 2026 Residents Handbook', author='Surplus',
     file=('2026-08-11 09:41', '2026-08-11 09:41'), pdf=('2026-08-06 16:00', '2026-08-06 16:00'), projects=['project_mathetic_company'],
     notes='incubator handbook sent by Lena Hoffmann at the 2026-08-11 kickoff', body='''
Surplus -- Fall 2026 cohort -- Residents handbook -- Program lead: Lena Hoffmann

## Welcome
You are one of nine teams in the Fall 2026 cohort. The program runs from the August 11 kickoff to Demo Night in mid-November. The house
is both a workplace and a home; this handbook covers how we share it.

## Weekly rhythm
| Day | What |
| Monday 10:00 | stand-up: each team, 2 minutes, one number that moved |
| Wednesday 18:00 | founder dinner (house kitchen, rotating cooks) |
| Thursday | office hours with mentors (sign-up sheet in the shared drive) |
| Friday 16:00 | demo hour: show something working, however small |

## House rules
- Quiet hours 23:00-07:00 in bedrooms and the upstairs hall. The garage studio is open 24 hours.
- Label food in the shared fridge with your name and date; unlabeled items are cleared on Sundays.
- Guests sign in at the front desk tablet; overnight guests need a day's notice to Lena.
- Bikes in the side yard rack, not the hallway.

## Getting help
Program questions: Lena. House maintenance: maintenance form in the shared drive. Urgent issues: the house phone list on the fridge.

## Milestones
Week 2: one-page company summary to Lena. Week 6: mid-program review. Week 13: Demo Night rehearsal.
'''),
dict(path='Downloads/Mathetic_PBC_annual_report_notice.pdf', title='Annual Report and Franchise Tax Notice - Mathetic PBC',
     author='Keystone Registered Agents LLC', file=('2026-09-30 19:15', '2026-09-30 19:15'), pdf=('2026-09-29 08:00', '2026-09-29 08:00'),
     projects=['project_mathetic_company'], notes='registered-agent reminder (fictional agent); Delaware annual report due 2027-03-01', body='''
Keystone Registered Agents LLC -- Compliance notice

Entity: Mathetic PBC -- Jurisdiction: Delaware -- Entity type: public benefit corporation

Notice date: September 29, 2026

## Upcoming filing
| Item | Due date | Status |
| Annual franchise tax report | March 1, 2027 | not filed |
| Franchise tax payment | March 1, 2027 | not paid |
| Public benefit statement (biennial) | with annual report as required | check with counsel |

## What you need
- Issued shares and total gross assets as of December 31, 2026 (for the assumed par value capital method).
- Names and addresses of all directors.
- Principal place of business.

## Reminder
Late filings incur a penalty and interest on unpaid tax. We will send reminders in January and February. Reply to this notice to
have us prepare the filing for you.
'''),
# ------------------------------------------------------------------ personal (endurance, music, none)
dict(path='Downloads/BAHM26_receipt_11873.pdf', title='Bay Area Half Marathon 2026 - Registration Receipt', author='Bay Area Half Marathon',
     file=('2026-05-01 07:21', '2026-05-01 07:21'), pdf=('2026-05-01 07:18', '2026-05-01 07:18'), projects=['project_endurance_training'],
     notes='HARD CASE: personal clutter — race registration receipt (the same receipt is attached to the runs@ Gmail confirmation)', body='''
Bay Area Half Marathon -- Registration receipt

Confirmation #: BAHM26-11873 -- Issued May 1, 2026

## Registrant
| Field | Entry |
| Runner | David Barron |
| Email | david.barron.runs@gmail.com |
| Event | Half Marathon (21.1 km) |
| Race date | Thursday, October 15, 2026 |
| Projected finish | 1:25:00 (Corral A, pending qualifying time) |

## Charges
| Item | Amount (USD) |
| Half marathon entry, early bird | 115.00 |
| Processing fee | 8.47 |
| Total charged | 123.47 |

Payment: card ending in 4419, approved.

Transfers allowed until September 15 for a $20 fee. Refunds are not available. Packet pickup at the race expo, October 13-14.
'''),
dict(path='Downloads/Block4_training_plan_Aug-Oct.pdf', title='Block 4 - Aug 10 to Oct 15 - half marathon build', author='David Barron',
     file=('2026-08-02 21:04', '2026-08-02 21:04'), projects=['project_endurance_training'],
     notes='personal training plan printed to PDF', body='''
Block 4 -- 10 weeks -- goal: Bay Area Half Marathon Oct 15, sub-1:25 -- 9-11 h/week

## Principles
- Most volume in Zone 2 (HR 138-152). Easy days easy.
- Two quality sessions a week max. Never back to back.
- Cycling and elliptical count toward hours, not mileage.
- Long run grows to 2:00 by week 7, then holds.

## Weeks
| Week | Dates | Hours | Quality 1 | Quality 2 | Long run |
| 1 | Aug 10-16 | 9.0 | 6 x 3 min @ threshold | strides | 1:30 |
| 2 | Aug 17-23 | 9.5 | 5 x 5 min @ threshold | hills 8 x 45 s | 1:35 |
| 3 | Aug 24-30 | 10.0 | 3 x 10 min @ threshold | strides | 1:40 |
| 4 | Aug 31-Sep 6 | 8.0 (down) | 20 min tempo | - | 1:20 |
| 5 | Sep 7-13 | 10.5 | 4 x 2 km @ HM pace | hills | 1:50 |
| 6 | Sep 14-20 | 11.0 | 2 x 5 km @ HM pace | strides | 1:55 |
| 7 | Sep 21-27 | 11.0 | 10 x 1 km @ 10K pace | - | 2:00 |
| 8 | Sep 28-Oct 4 | 9.0 (down, travel) | 3 x 3 km @ HM pace | - | 1:45 |
| 9 | Oct 5-11 | 8.0 | 6 x 1 km @ HM pace | strides | 1:15 |
| 10 | Oct 12-15 | 4.5 | 3 x 1 km @ HM pace (Tue) | race Thu | - |

## Notes
Move to SF on Aug 8: first week of block on new routes, keep everything easy for 3 days. UIST travel Oct 5-8: run easy only, hotel
gym fine. Pace for 1:25: 4:02/km.
'''),
dict(path='Downloads/Invoice_4471_rear_derailleur.pdf', title='Invoice 4471 - Spoke & Chain Cycles', author='Spoke & Chain Cycles',
     file=('2026-05-12 17:46', '2026-05-12 17:46'), pdf=('2026-05-12 17:40', '2026-05-12 17:40'), projects=['project_none'],
     notes='HARD CASE: personal clutter — bike repair invoice (fictional shop), broken derailleur theme', body='''
Spoke & Chain Cycles -- Blacksburg, VA -- Service invoice #4471

Date: May 12, 2026 -- Customer: David Barron -- Bike: road bike, 2x11 drivetrain

## Work performed
| Item | Qty | Price (USD) |
| Rear derailleur (11-speed, mid-cage) | 1 | 74.99 |
| Derailleur hanger (replacement) | 1 | 28.00 |
| Shift cable and housing | 1 | 14.50 |
| Labor: derailleur install and indexing | 1 | 35.00 |
| Labor: hanger alignment check | 1 | 10.00 |
| Subtotal | | 162.49 |
| Sales tax (5.3% on parts) | | 6.20 |
| Total | | 168.69 |

Paid in full -- card.

## Mechanic notes
Hanger was bent inward, likely from a fall on the drive side; derailleur cage cracked. Replaced both. Indexed and test-ridden. Chain
at 0.5% wear, fine for now; recheck in about 1,000 miles. Free re-index within 30 days.
'''),
dict(path='Downloads/Renters_Insurance_Policy_Summary_2026.pdf', title='Renters Insurance - Policy Summary', author='Harborline Mutual',
     file=('2026-08-13 13:32', '2026-08-13 13:32'), pdf=('2026-08-13 13:20', '2026-08-13 13:20'), projects=['project_none'],
     notes='HARD CASE: personal clutter — renter\'s insurance summary after the move (fictional insurer)', body='''
Harborline Mutual -- Renters insurance -- Policy summary

Policy holder: David Barron -- Policy period: August 13, 2026 to August 13, 2027

Insured location: shared residence, San Francisco, CA (room rental)

## Coverages
| Coverage | Limit (USD) | Deductible (USD) |
| Personal property | 20,000 | 500 |
| Personal liability | 100,000 | - |
| Medical payments to others | 1,000 | - |
| Loss of use | 6,000 | - |

## Scheduled items
| Item | Value (USD) |
| Laptop (purchased August 2026) | 2,499 |
| Road bike | 1,400 |

## Premium
Annual premium: 168.00, paid monthly (14.00 per month).

## Notes
Personal property is covered anywhere in the world, subject to the deductible. Bicycles are covered for theft when locked. Shared
common areas of the residence are not covered under this policy. Contact your agent to update the insured location if you move.
'''),
dict(path='Downloads/scan_0001.pdf', title='scan_0001', author='', file=('2026-08-11 18:42', '2026-08-11 18:42'),
     pdf=('2026-08-11 18:40', '2026-08-11 18:40'), projects=['project_none'],
     notes='HARD CASE: vague titles — scanner default name; content is the signed room-agreement addendum for the Surplus house room (fictional)', body='''
ADDENDUM TO ROOM AGREEMENT -- SUMMARY OF TERMS (scanned, signed copy)

Premises: Room 3, Surplus incubator house, SoMa, San Francisco, CA

Resident: David Barron -- Move-in: August 8, 2026

## Terms
1. Term: August 8, 2026 to December 31, 2026; month-to-month afterwards with 30 days' written notice.
2. Rent: $1,200 per month, due on the 1st; August prorated from the 8th.
3. Deposit: $1,200, refundable, returned with an itemized statement after move-out.
4. Utilities: internet, water and power included.
5. Guests: no more than 3 consecutive nights; overnight guests registered with the program lead.
6. Quiet hours: 11 pm to 7 am.
7. Shared spaces: kitchen, living room (demo Fridays at 4 pm) and roof; personal items cleared from shared spaces overnight.
8. Insurance: the house policy does not cover residents' belongings; residents are responsible for their own renters insurance.
9. Subletting: not permitted.

## Signatures
Resident: David Barron (signed) -- Date: 08/11/2026

For the house: (signed) -- Date: 08/11/2026

Page 1 of 1
'''),
dict(path='Downloads/VT_Parking_Citation_Appeal_Barron.pdf', title='Parking Citation Appeal', author='David Barron',
     file=('2026-02-12 16:21', '2026-02-12 16:21'), projects=['project_none'],
     notes='HARD CASE: personal clutter — VT parking ticket appeal', body='''
Virginia Tech Parking and Transportation -- Citation appeal

Submitted: February 12, 2026 -- Appellant: David Barron (graduate student) -- Email: dbarron410@vt.edu

## Citation
| Field | Entry |
| Citation number | P26-018834 |
| Date issued | February 9, 2026, 8:47 am |
| Location | Perry Street lot |
| Violation | No valid permit displayed |
| Fine | $40.00 |

## Statement
I hold a valid graduate commuter permit for this lot. On February 9 I was driving a borrowed car while mine was in the shop and had
moved my hang tag to it, but the tag had fallen from the mirror onto the dashboard, where it was face-down and not visible. I have
attached a photo of the permit and the repair-shop receipt showing my car was being serviced that day. I ask that the citation be
reduced to a warning.

## Attachments
Permit photo; shop receipt dated February 9, 2026.
'''),
dict(path='Downloads/2025_taxes_checklist.pdf', title='2025 taxes - checklist', author='David Barron',
     file=('2026-03-08 22:03', '2026-04-11 20:15'), projects=['project_none'],
     notes='HARD CASE: personal clutter — own tax checklist (no real figures)', body='''
2025 taxes -- what I need -- started March 8, 2026

## Documents
- [x] W-2 from Virginia Tech (GRA) -- arrived Jan 28
- [x] 1098-T tuition statement -- downloaded from Hokie SPA
- [x] 1099-INT from savings account
- [ ] Virginia state return: check whether any part-year issues (no, full year in VA for 2025)
- [x] Health coverage form -- not needed for federal

## Questions
- Is the tuition waiver taxable? -> qualified tuition reduction, not taxable for a GRA; confirm 1098-T box 5 vs box 1.
- Can I deduct the conference registration I paid myself? -> no (employee expenses not deductible federally).
- Moving in August 2026 -> matters for 2026 return, not 2025.

## Plan
File federal + Virginia with free file software by April 12. Keep PDFs of both returns in iCloud "Taxes/2025".

## Done
Filed April 11, 2026. Federal and state accepted April 12.
'''),
dict(path='Downloads/caro-kann_advance_notes.pdf', title='Caro-Kann Advance - my lines', author='David Barron',
     file=('2026-01-06 23:12', '2026-01-06 23:12'), projects=['project_none'],
     notes='HARD CASE: personal clutter — online chess opening notes', body='''
Caro-Kann, Advance Variation -- notes for blitz (as Black)

1. e4 c6 2. d4 d5 3. e5

## Main choice: 3...Bf5
- 4. Nf3 e6 5. Be2 c5 -- the short system. Aim for ...Nc6, ...Qb6, pressure on d4.
- 4. h4 h5 -- don't panic. 5. c4 is the critical try; 5...e6 6. Nc3 Ne7.
- 4. Nc3 e6 5. g4 Bg6 6. Nge2 c5 -- sharp. I keep losing here in 3+0. Option: 4...h5!? to avoid g4 lines.

## Plans to remember
| Structure | My plan |
| White plays c3, Bd3 | trade light-squared bishops, then ...c5 |
| White castles queenside | ...c5 and ...Qa5 fast; push b-pawn |
| e5 pawn overextended | ...f6 break only after development |

## Mistakes from recent games
- Grabbing b2 with the queen when White has Nc3 and Rb1 tempo. Twice in December.
- Playing ...c5 before ...Nc6 when d4xc5 hits with tempo.
- Flagging in won endgames: premove less, think on opponent's time.
'''),
dict(path='Downloads/Loopwell_receipt_88213.pdf', title='Loopwell Samples - Order 88213', author='Loopwell Samples',
     file=('2026-02-24 00:31', '2026-02-24 00:31'), pdf=('2026-02-24 00:29', '2026-02-24 00:29'), projects=['project_music_production'],
     notes='HARD CASE: personal clutter — sample-pack receipt (fictional store)', body='''
Loopwell Samples -- Order confirmation and receipt

Order #88213 -- February 24, 2026 -- Customer: David Barron (david.barron.runs@gmail.com)

## Items
| Item | Format | Price (USD) |
| Late Night Keys Vol. 2 (one-shots + MIDI) | WAV 24-bit | 24.00 |
| Dusty Breaks Toolkit (120 drum loops, 85-95 BPM) | WAV | 19.00 |
| Sub Bass Essentials (FL Studio presets) | .fst | 12.00 |
| Discount (bundle 3) | | -9.00 |
| Total | | 46.00 |

Licence: royalty-free for use in your own productions. Not for redistribution as samples.

Downloads available for 30 days from your account page. Redownloads after that: contact support with your order number.
'''),
dict(path='Downloads/Vehicle_Registration_Renewal_Notice.pdf', title='Vehicle Registration Renewal Notice', author='',
     file=('2026-06-02 19:10', '2026-06-02 19:10'), pdf=('2026-06-01 06:00', '2026-06-01 06:00'), projects=['project_none'],
     notes='HARD CASE: personal clutter — car registration renewal (car insurance/registration theme)', body='''
Vehicle registration renewal notice

Registered owner: David Barron -- Vehicle: 2014 sedan -- Plate: (on file)

Current registration expires: July 31, 2026

## Renewal options
| Option | Fee (USD) |
| 1 year | 40.75 |
| 2 years | 81.50 |

## Before you renew
- Confirm your insurance is active; your insurer must be on file.
- If you are moving out of state, you must register the vehicle in your new state of residence within the time required there and may
  cancel this registration afterward.

Renew online, by mail, or in person. Keep this notice for your records.
'''),
dict(path='Downloads/SF_move_checklist.pdf', title='SF move checklist', author='David Barron',
     file=('2026-07-30 22:15', '2026-08-07 23:50'), projects=['project_none'],
     notes='HARD CASE: personal clutter — moving checklist (Blacksburg -> SF, arrive 2026-08-08)', body='''
Move to SF -- arrive Saturday Aug 8 -- started Jul 30

## Before leaving Blacksburg
- [x] give notice on apartment (done Jun 30), move-out inspection Aug 6
- [x] forward mail (USPS) starting Aug 7
- [x] cancel internet, transfer electric to landlord
- [x] sell desk + chair (sold Aug 2)
- [x] ship 3 boxes of books ahead (arrive ~Aug 12)
- [x] bike: box at the shop, ship with the books
- [ ] car: decide sell vs drive -> keeping it with a friend in Blacksburg until October, decide then

## First week in SF
- [ ] renters insurance -- ask Lena whether the house policy covers residents
- [ ] update address: bank, VT records, Strava/Garmin, race registration
- [ ] find a running route that isn't all hills (lol)
- [x] Surplus kickoff Tue Aug 11 10:00

## New Mac (arrives Aug 4)
Set up before the flight so I'm not doing it at the house: see setup checklist.
'''),
dict(path='iCloud Drive/New_Mac_setup_checklist.pdf', title='new mac setup', author='David Barron',
     file=('2026-08-04 20:31', '2026-08-05 00:12'), projects=['project_none'],
     notes='HARD CASE: personal clutter — laptop setup notes for the new Mac (2026-08-04)', body='''
new mac setup -- Aug 4 2026

## Basics
- [x] migrate nothing; fresh install, pull from iCloud + GitHub
- [x] Homebrew, git, gh, node (via fnm), python (uv), postgres
- [x] VS Code + settings sync; Claude Code; iTerm2 profile
- [x] FileVault on; Time Machine to the external drive
- [x] FL Studio reinstall + plugin licences (keep the licence emails!)

## Dotfiles
- [x] zsh config from the dotfiles repo
- [x] ssh keys: new key for this machine, add to GitHub, revoke the old laptop's key after a week
- [ ] gpg signing -- later

## Research stuff
- [x] Zotero + Better BibTeX; library syncs, storage folder relinked
- [x] Overleaf: nothing to install
- [ ] old laptop: copy ~/Desktop/papers and ~/Downloads PDFs I still need before wiping

## Don't forget
Wipe and return the old VT laptop to the department after the leave paperwork is done.
'''),
dict(path='Downloads/meridian_wp_25-07_chokepoints.pdf', kind='zotero_paper', paper_key='draxler2025chokepoints',
     file=('2025-12-28 23:35', '2025-12-28 23:35'), projects=['project_none'],
     notes='HARD CASE: same paper in several places — fictional geopolitics working paper; byte-identical to the Zotero attachment (unrelated to projects)'),
# ------------------------------------------------------------------ papers also in Zotero
dict(path='Desktop/papers/Ferreira_Kowalczyk_2023_group_splits.pdf', kind='zotero_paper', paper_key='ferreira2023groupaware',
     file=('2026-07-24 23:44', '2026-07-24 23:44'), projects=['project_idetrace'],
     notes='HARD CASE: same paper in several places — fictional paper, byte-identical to its Zotero attachment'),
dict(path='Downloads/2602.11873v1.pdf', kind='zotero_paper', paper_key='brennan2026what',
     file=('2026-06-13 23:25', '2026-06-13 23:25'), projects=['project_tutortrace'],
     notes='HARD CASE: same paper in several places — fictional arXiv preprint downloaded before adding to Zotero (byte-identical attachment)'),
dict(path='Desktop/papers/Halvorsen_Quist_2025_provenance_trails.pdf', kind='zotero_paper', paper_key='halvorsen2025where',
     file=('2026-09-02 23:29', '2026-09-02 23:29'), projects=['project_augmenting_cognition_reading_group', 'project_engelbart'],
     notes='HARD CASE: same paper in several places — fictional paper, byte-identical to its Zotero attachment'),
]
