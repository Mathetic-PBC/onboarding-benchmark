"""dbarron410@vt.edu (VT Google Workspace Gmail) — advisor, lab, grad office, course and UIST threads, Oct 2025 .. Sep 2026.
Date strings are David's local time (ET until 2026-08-08 12:00, PT after)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _dsl import *

SHARED = os.path.join(os.path.dirname(__file__), '..', '..', 'shared')
OSTROWSKI_V1 = os.path.abspath(os.path.join(SHARED, 'Ostrowski2025_arXiv_v1.pdf'))

PCS = P('UIST 2026 Program Committee', 'noreply@uist2026.confsys.org')
REG = P('UIST 2026 Registration', 'registration@uist2026.confsys.org')
STUDENT_P4 = P('Jared P.', 'jaredp21@vt.edu', ET)
STUDENT_P3 = P('Aisha K.', 'aishak04@vt.edu', ET)
CS3604_STAFF = P('CS 3604 Course Staff', 'cs3604-staff-f25@vt.edu', ET)
PRIME = P('PRIME Lab', 'prime-lab-g@vt.edu', ET)

UIST_DRAFT = [
    ('title', 'TutorTrace: Replaying Help-Seeking in LLM-Assisted Programming Labs'),
    ('p', 'Anonymous UIST 2026 submission · DRAFT 2026-03-29 · do not distribute'),
    ('h2', 'Abstract'),
    ('p', 'Instructors of introductory programming courses cannot see how students use AI assistants during lab sessions. '
          'We present TutorTrace, a system that records editor and assistant telemetry and lets instructors replay a session '
          'as a timeline of edits, runs, errors and prompts, with automatically flagged moments of stalling. We deployed '
          'TutorTrace in a CS1 course (87 students, 3 TAs) and labeled 2,340 thirty-second windows with a guide that '
          'distinguishes productive struggle, help-seeking, stalled-after-error and off-task. Three raters reached kappa = 0.71. '
          'Instructors used the replay to find students who never asked for help, and changed when TAs circulated.'),
    ('h2', '1 Introduction'),
    ('p', 'TODO(Yan): tighten the first paragraph; the "raised hand" framing may be too cute.'),
    ('h2', '3 System'),
    ('bullet', 'Recorder: browser IDE plugin; websocket stream with client-side buffering after the Nov 12 reconnect bug.'),
    ('bullet', 'Replay timeline: edits, runs, test results and prompts on one axis; stall flags as amber bands.'),
    ('bullet', 'Instructor dashboard: per-section heatmap of flagged windows.'),
    ('h2', '5 Deployment'),
    ('table', [['State', 'Windows', 'Share'], ['Productive struggle', '781', '33%'], ['Help-seeking', '612', '26%'],
               ['Stalled-after-error', '529', '23%'], ['Off-task', '418', '18%']]),
    ('p', 'Note: section B lost ~12% of events before the 4:10 pm hotfix; we exclude those windows from the agreement analysis.'),
]

LOA_FORM = [
    ('title', 'Virginia Tech Graduate School — Request for Leave of Absence'),
    ('p', 'Student: David Barron    Program: Computer Science and Applications (PhD)    Department: Computer Science'),
    ('p', 'Requested leave: Fall 2026 (effective August 2026), up to two semesters, with intent to return'),
    ('p', 'Reason (summary): professional opportunity — co-founding a research-tools company related to the student\'s research area.'),
    ('h3', 'Conditions agreed with advisor'),
    ('bullet', 'UIST 2026 camera-ready (due 2026-08-14) and talk (2026-10-07) completed during the leave.'),
    ('bullet', 'NeurIPS 2026 Datasets & Benchmarks rebuttal posted before the leave begins.'),
    ('bullet', 'GRA appointment ends 2026-08-15; no assistantship during the leave.'),
    ('table', [['Signature', 'Name', 'Date'], ['Student', 'David Barron', '2026-07-29'], ['Advisor', 'Yan Chen', '2026-07-30'],
               ['Graduate Program Coordinator', 'Grace Kim', '2026-07-31'], ['Graduate School', '', '']]),
]

POS = [
    ('title', 'Plan of Study — PhD, Computer Science and Applications'),
    ('p', 'David Barron · submitted 2025-10-27 · advisor: Dr. Yan Chen'),
    ('table', [['Course', 'Title', 'Term', 'Credits'],
               ['CS 5724', 'Models and Theories of HCI', 'Fall 2024', '3'],
               ['CS 5764', 'Information Visualization', 'Spring 2025', '3'],
               ['CS 6604', 'Advanced Topics: Learning at Scale', 'Fall 2025', '3'],
               ['ISE 6664', 'Affective Design & Computing', 'Spring 2026', '3'],
               ['CS 7994', 'Research and Dissertation', 'ongoing', '—']]),
    ('p', 'Committee: Yan Chen (chair) + three members to be confirmed before the preliminary exam.'),
]

TRAVEL_BUDGET = {
    'Budget': [['Item', 'Detail', 'Amount (USD)'],
               ['Registration', 'UIST 2026 student, early rate (paid 2026-08-27)', 425],
               ['Airfare', 'SFO round trip, economy, quoted 2026-09-22', 486.40],
               ['Lodging', 'conference hotel, 3 nights (Oct 5-8) at $219/night', 657],
               ['Meals', 'per diem, 4 days (first/last day 75%), minus conference-provided meals', 157.92],
               ['Ground transport', 'airport transfers', 60],
               ['Total', '', '=SUM(C2:C6)']],
    'Justification': [['Field', 'Text'],
                      ['Paper', 'TutorTrace: Replaying Help-Seeking in LLM-Assisted Programming Labs (UIST 2026, accepted)'],
                      ['Role', 'First author, presenting the talk on 2026-10-07, session "Learning & Tutoring"'],
                      ['Other funding', 'Advisor contributes airfare from lab funds if department cap is reached'],
                      ['Status', 'On approved leave of absence (Fall 2026); presenting work completed while enrolled']],
}

LABEL_PLAN = {
    'Assignments': [['Rater', 'Section', 'Windows', 'Overlap (for kappa)', 'Due'],
                    ['David', 'A (Nov 12)', 780, 120, '2025-11-21'],
                    ['Minsun', 'A + B', 780, 120, '2025-11-21'],
                    ['Xiaohang', 'B (Nov 12)', 780, 120, '2025-11-21'],
                    ['Total', '', '=SUM(C2:C4)', '', '']],
    'States (guide v2)': [['Code', 'State', 'Example'],
                          ['PS', 'Productive struggle', 'small edits + test runs, no prompt'],
                          ['HS', 'Help-seeking', 'prompt to assistant or TA hand raise'],
                          ['OT', 'Off-task', 'tab away > 20 s, no edits'],
                          ['??', 'unclear', 'flag for discussion']],
}

ISE_REPORT = [
    ('title', 'Frustration Signals in AI-Tutoring Transcripts'),
    ('p', 'ISE 6664 Final Project Report · David Barron, Maya Torres, Jordan Lee · Spring 2026 · Instructor: Dr. Alan Brooks'),
    ('h1', 'Abstract'),
    ('p', 'We annotated 300 student–AI tutoring transcripts from an introductory programming course for expressed frustration and '
          'compared lexical, temporal and interaction features as predictors. Short repeated prompts and terse negations ("no", '
          '"still wrong") were the strongest signals; message latency added little. We discuss the ethics of affect detection in '
          'tutoring and argue for surfacing signals to TAs rather than adapting the tutor automatically.'),
    ('h1', '1 Introduction'), ('p', 'Affective computing has long sought to detect frustration from faces and physiology; text-only '
                                    'tutoring removes those channels and leaves only what students type.'),
    ('h1', '3 Method'), ('p', 'Two annotators (Maya, Jordan) labeled each turn on a 3-point frustration scale; David built the feature '
                              'pipeline. Agreement: weighted kappa 0.66 on 60 double-coded transcripts.'),
    ('h1', '4 Results'),
    ('table', [['Feature set', 'Macro-F1'], ['Lexical only', '0.61'], ['Temporal only', '0.48'], ['Lexical + interaction', '0.67']]),
    ('h1', '6 Ethics and limitations'), ('p', 'Students did not consent to affect inference specifically; transcripts were de-identified.'),
]

THREADS = [
# ---------------- Fall 2025 ----------------
T('Plan of study — submitted for review', ['project_vt_phd_admin'], [
M('2025-10-27 16:20', ME_VT, GRACE, """
Hi Grace,

I submitted my plan of study through the Graduate School system today and attached a PDF copy here for the department file. Dr. Chen has reviewed it. The committee section lists her as chair; I'll add the remaining members before my preliminary exam.

Please let me know if anything is missing.

Best,
David Barron
PhD student, Computer Science (PRIME Lab)
""", att=[A('pdf', 'Barron_Plan_of_Study_Oct2025.pdf', POS, 'Plan of Study — David Barron')]),
M('2025-10-28 09:42', GRACE, ME_VT, """
Hi David,

Thanks, received. The plan looks complete for now. You'll need all committee members listed and approved at least one semester before the preliminary exam; I'd aim for spring.

Best,
Grace

Grace Kim | Graduate Program Coordinator | Department of Computer Science | Virginia Tech
"""),
]),

T('P3 case study — counterargument points', ['project_cs3604_gta'], [
M('2025-10-30 22:14', STUDENT_P3, ME_VT, """
Hi David,

I lost 4 of the 10 points for "engages the strongest counterargument" on P3 (Case Study Analysis). My paper has a whole paragraph on the company's side (that the data was already public). Was that not the counterargument you were looking for?

Thanks,
Aisha
"""),
M('2025-10-31 10:05', ME_VT, STUDENT_P3, """
Hi Aisha,

Good question. You do present the company's position, and that's why you got 6 of 10 rather than fewer. What the rubric asks for at the 9-10 level is to respond to the strongest version of it: here, that users had agreed to the terms of service. Your paragraph raises "the data was public" but doesn't address consent, which is the argument a reader on the company's side would actually make, and then moves on to your own position.

For P4 (policy memo), the same item exists. One paragraph that states the best objection to your recommendation and answers it directly is usually enough.

David
CS 3604 GTA
"""),
M('2025-10-31 11:30', STUDENT_P3, ME_VT, """
That makes sense, thanks for explaining. I'll do that for the memo.
"""),
]),

T('CS 3114 lab Nov 12 — VizPI setup', ['project_vizpi'], [
M('2025-11-05 14:40', WENSKOVITCH, ME_VT, """
Hi David,

Confirming the second VizPI deployment for CS 3114 on Wednesday Nov 12, lab session starting 3:30 pm, both sections (McBryde 106 and 118). Roughly 87 students total and 3 TAs.

What do you need from me? Last time the TAs weren't sure how to tell students to install the plugin.

John
"""),
M('2025-11-05 17:12', ME_VT, WENSKOVITCH, """
Hi John,

Thanks for hosting again. Three things:

1. A 2-minute slot at the start to explain the study and the opt-out (consent text unchanged from deployment #1).
2. The TAs should have the install link open before 3:30: it's now a single browser link, no plugin install, so that problem should be gone.
3. I'll be in 106 and Minsun will be in 118 for the whole session in case anything breaks.

We'll share an anonymized summary of help-seeking patterns per section by Thanksgiving.

David
"""),
], quote=True),

T('section B telemetry drop + hotfix (deployment #2)', ['project_vizpi'], [
M('2025-11-12 19:48', ME_VT, [YAN, MINSUN, XIAOHANG], """
Hi all,

Quick report on today's deployment in CS 3114.

- 87 students across two sections, 3 TAs. Consent opt-outs: 4.
- Section B: the websocket reconnect logic didn't resend buffered events after a dropped connection. Comparing client counters to the server log, we lost about 12% of section B's telemetry events between 3:30 and the hotfix at 4:10 pm. Section A was unaffected.
- Hotfix: the client now buffers events locally and replays them with sequence numbers on reconnect; the server dedupes by (session, seq).

For labeling, I propose we exclude section B windows from 3:30-4:10 from the agreement analysis but keep them in the dataset with a flag.

David
"""),
M('2025-11-12 21:15', YAN, [ME_VT, MINSUN, XIAOHANG], """
Thanks David, good catch and good fix. Agree with excluding the affected windows from agreement but flagging them. Please document the incident in the deployment log so we can describe it honestly in the paper.

Yan
"""),
M('2025-11-12 22:02', MINSUN, [ME_VT, YAN, XIAOHANG], """
I'll add a `degraded=true` column for those windows in the export. The rest of section B looked normal after 4:10.
"""),
]),

T('labeling sprint 11/14 → 11/21: assignments', ['project_vizpi'], [
M('2025-11-13 23:30', ME_VT, [MINSUN, XIAOHANG], """
hi both, sprint plan attached. 2,340 thirty-second windows total, 780 each, with 120 overlapping windows per pair so we can compute kappa. due friday 11/21.

guide is still v2 (PS / HS / OT). i keep hitting windows where someone gets an error, stops typing and just stares for 40 seconds, and none of our codes fit. proposal: add a "stalled-after-error" state before we start, otherwise we'll relabel later
""", att=[A('xlsx', 'labeling_sprint_nov14.xlsx', LABEL_PLAN, 'VizPI labeling sprint — Nov 14-21')]),
M('2025-11-14 09:20', XIAOHANG, [ME_VT, MINSUN], """
Agree on stalled-after-error. Definition suggestion: a run or test fails, then no edit and no prompt for 30+ seconds. If they prompt within the window it's help-seeking instead.
"""),
M('2025-11-14 10:05', MINSUN, [ME_VT, XIAOHANG], """
+1. I'll write it into the guide as v3 today and add three example windows from section A so we calibrate on the same cases.
"""),
]),

T('labeling guide v3 — stalled-after-error', ['project_vizpi'], [
M('2025-11-19 16:12', MINSUN, [ME_VT, XIAOHANG], """
Guide v3 is in the lab drive. Changes:

- New state SAE (stalled-after-error): failed run/test followed by >=30 s with no edit and no prompt.
- HS now explicitly wins over SAE if a prompt happens in the same window.
- Added 6 calibration windows (3 SAE, 3 borderline PS/SAE).

Midpoint check: after the first 400 each, our pairwise kappa on the overlap is 0.68. The disagreements are almost all PS vs SAE.
"""),
M('2025-11-19 23:48', ME_VT, [MINSUN, XIAOHANG], """
0.68 at the midpoint is better than i expected. for PS vs SAE i've been using "did they change anything in the 30s after the error" as the tiebreaker, maybe we write that into the guide too?
"""),
]),

T('related work: Ostrowski et al. (arXiv) — very close to us', ['project_vizpi', 'project_tutortrace'], [
M('2025-11-20 13:35', MINSUN, [ME_VT], """
David, have you seen this? Ostrowski et al. on arXiv (July). They label 30-second windows as productive struggle / stalling / help-seeking / off-task in an LLM-assisted CS1 course. Very close to our states. Their kappa is 0.62 and they get 0.69 macro-F1 with a classifier.

PDF attached. We should cite it and say what's different (we do replay for instructors, they do classification).
""", att=[A('file', 'Ostrowski2025_arXiv_v1.pdf', OSTROWSKI_V1, 'application/pdf')]),
M('2025-11-20 15:02', ME_VT, [MINSUN], """
oh wow, hadn't seen it. yes we cite it. their "stalling" is basically our stalled-after-error without the error trigger. good for us actually, independent evidence the state is real

adding to the zotero group
"""),
], notes='HARD CASE: same paper in several places — Minsun sends the arXiv v1 of the Ostrowski 2025 paper (near-duplicate of the camera-ready); also an email with attachments'),

T('TACode handoff: repo, deploy, open issues', ['project_tacode'], [
M('2025-11-11 22:40', ME_VT, REZKY, """
Hi Rezky,

As discussed in lab meeting, here's the TACode handoff. I'm stepping back so I can focus on VizPI/TutorTrace.

- Repo: PRIME-Lab/tacode (you're now an admin). main is deployable; the `queue-v2` branch is half-finished, don't merge it as is.
- Deploy: the course VM, `make deploy` from the repo root. The .env template is in the lab password manager under "TACode prod".
- Open issues that matter: #41 (office-hours queue doesn't clear at midnight), #44 (Canvas roster sync fails for cross-listed sections), #47 (TA notes export as CSV).
- The spring instructor wants the queue running by the first week of classes.

Happy to do a 30-minute walkthrough Thursday.

David
"""),
M('2025-11-12 09:30', REZKY, ME_VT, """
Thanks David, this is super clear. Thursday 2pm for the walkthrough? I'll start with #44 since roster sync blocks everything else.

Rezky
"""),
M('2025-11-12 10:10', ME_VT, REZKY, """
thursday 2pm works. and yes #44 first, the fix is probably just matching on the crn instead of the section name
"""),
]),

T('EthicConvo — handing off the study materials', ['project_ethicconvo'], [
M('2025-11-13 15:25', ME_VT, YUE, """
Hi Yue,

Handing off EthicConvo to you as planned. Everything is in the lab drive under EthicConvo/2025:

- Study protocol (IRB-approved amendment from September) and the consent form
- The 14 conversation scenarios, with the two you suggested revising flagged in yellow
- Pilot transcripts (6 participants) and my coding notes; I only got through the first 3 with the codebook
- The prompt templates for the conversational agent, versioned by date

The thing I'd change first: scenario 9 (the plagiarism one) led every participant to the same answer, so it isn't discriminating.

David
"""),
M('2025-11-14 11:02', YUE, ME_VT, """
Thanks David! I'll read everything this weekend. Agree about scenario 9, I'll draft a version where the ethical choice costs the student something.

Yue
"""),
]),

T('P4 late penalty — I had 2 late days left', ['project_cs3604_gta'], [
M('2025-12-08 23:40', STUDENT_P4, ME_VT, """
Hi David,

The course staff said to email you since you graded P4. I got -10% on the policy memo for lateness, but I submitted at 12:14 AM on 11/23, which is 2 late days, and I had 2 left: I only used 1 on P2. The P2 resubmission was inside the resubmission window, so it shouldn't have used a late day.

I'll also post my late-days page screenshot as a comment on the submission in Canvas.

Thanks,
Jared
"""),
M('2025-12-09 23:55', ME_VT, STUDENT_P4, """
Hi Jared,

You're right. Your P4 submission (11/23, 12:14 AM) used 2 late days and you had 2 remaining, so there should be no penalty. The "Late Days" column in Canvas double-counted your P2 resubmission as a late day, which is why I applied the 10%.

I've corrected your P4 grade from 78 to 87 and left a comment on the submission. I've also flagged the column issue to the course staff in case it affected anyone else.

David
CS 3604 GTA
""", cc=[CS3604_STAFF]),
M('2025-12-10 08:15', STUDENT_P4, ME_VT, """
Thank you, I appreciate you checking!
"""),
], notes='CS 3604 regrade dispute about P4 late days (Dec 2025); same dispute as the Canvas comment in outlook'),

T('P4 + final project grades: status before Dec 15', ['project_cs3604_gta'], [
M('2025-12-13 11:40', ME_VT, CS3604_STAFF, """
Status before the final grade deadline (Mon Dec 15, 5 PM):

- Final project, teams 1-8: all graded in the final-project tab of the rubric sheet (written report + the presentation score you entered). Average 87.9; lowest 74 (team 7, the appendix with the stakeholder map was missing).
- P4: all graded and posted. Jared P.'s late-day penalty corrected (78 -> 87) after the Late Days column double-counted his P2 resubmission; you said you'd fix the other three resubmitters.
- No open regrade requests on my side.

Everything is in Canvas, so you have Sunday for disputes and the Banner export.

David
"""),
]),

T('Dynamite clustering — 41 clusters, labels checked', ['project_dynamite'], [
M('2026-02-03 22:10', ME_VT, YAN, """
Hi Yan,

Update on Dynamite before Thursday:

- Embedded all 3,100 discussion posts and clustered with HDBSCAN (min_cluster_size=15). 41 clusters; 9% of posts are noise, mostly one-line "thanks" replies.
- Cluster labels were generated by an LLM from the 10 most central posts in each cluster. I checked all 41 by hand and rewrote 7 (the model kept calling things "general discussion").
- The interesting ones: three separate clusters about the same week-6 assignment, split by whether students were confused about the spec, the autograder, or the math.

Question for Thursday: do we want the instructor view to show clusters by week, or by topic across weeks?

David
"""),
M('2026-02-04 08:30', YAN, ME_VT, """
Nice progress. By week first — instructors think in weeks. Then let them merge across weeks. Please bring two examples of the rewritten labels; I want to see what the model got wrong.

Yan
"""),
]),

T('ISE 6664 — project team and topic', ['project_ise6664_affective_computing'], [
M('2026-01-21 17:30', ME_VT, BROOKS, """
Dear Dr. Brooks,

Maya Torres, Jordan Lee and I would like to form a team for the final project. Our proposed topic: "Frustration signals in AI-tutoring transcripts" — whether expressed frustration can be detected from the text of student conversations with an AI tutor, and what it would mean ethically to act on it.

We have access to de-identified tutoring transcripts from an introductory programming course through my lab, under an existing IRB protocol. Would this topic fit the course's scope given that it is text-only, without physiological signals?

Best regards,
David Barron
""", cc=[MAYA, JORDAN]),
M('2026-01-22 10:15', BROOKS, ME_VT, """
Dear David,

Yes, this fits. Text-only affect detection is a legitimate and interesting constraint; make the ethics section substantive, not an afterthought. Please confirm in your proposal that your IRB protocol covers secondary analysis for a course project.

Proposals are due February 13.

Alan Brooks
""", cc=[MAYA, JORDAN]),
]),

T('ISE 6664 final presentation — April 30 logistics', ['project_ise6664_affective_computing'], [
M('2026-04-27 09:10', BROOKS, [ME_VT, MAYA, JORDAN], """
Dear team,

Your final presentation is on Thursday, April 30, slot 3 (approximately 2:40 pm). 15 minutes plus 5 minutes of questions. Please send your slides by Wednesday at 6 pm so I can load them on the room computer.

The written report (12-15 pages) is due May 6.

Alan Brooks
"""),
M('2026-04-27 22:45', ME_VT, [BROOKS, MAYA, JORDAN], """
Dear Dr. Brooks,

Thank you, we'll send the slides by Wednesday 6 pm. Maya will present the annotation study, Jordan the results, and I'll cover the pipeline and the ethics discussion.

Best,
David
"""),
]),

T('ISE 6664 final report — Torres, Lee, Barron', ['project_ise6664_affective_computing'], [
M('2026-05-05 23:20', ME_VT, BROOKS, """
Dear Dr. Brooks,

Attached is our final report, "Frustration Signals in AI-Tutoring Transcripts" (14 pages). Following your comments at the presentation, we expanded the ethics section and added the per-feature ablation table.

Best regards,
David Barron (with Maya Torres and Jordan Lee)
""", cc=[MAYA, JORDAN], att=[A('docx', 'ISE6664_Final_Report_Torres_Lee_Barron.docx', ISE_REPORT, 'Frustration Signals in AI-Tutoring Transcripts')]),
M('2026-05-12 14:00', BROOKS, ME_VT, """
Dear David, Maya and Jordan,

A strong report. The ethics section is the best in the class this year; the argument for surfacing signals to TAs rather than adapting the tutor is well made. My main criticism: the 300 transcripts come from one course and one tutor, so the claims in Section 5 should be more modest.

Grade: A. Have a good summer.

Alan Brooks
""", cc=[MAYA, JORDAN]),
]),

# ---------------- UIST crunch ----------------
T('UIST draft for your read — TutorTrace', ['project_tutortrace'], [
M('2026-03-29 23:12', ME_VT, YAN, """
Hi Yan,

The full draft is attached (10 pages + references). Status:

- Sections 1-5 complete; 6 (discussion) is a skeleton.
- Kappa across the 3 raters is 0.71 on the overlap set after guide v3.
- I excluded the section B windows affected by the Nov 12 reconnect bug from the agreement analysis and say so in Section 5.

Could you focus on the introduction and the framing of the contribution? I'm not sure whether to lead with the system or with the deployment findings.

Thanks,
David
""", att=[A('pdf', 'TutorTrace_UIST2026_draft_0329.pdf', UIST_DRAFT, 'TutorTrace UIST 2026 draft')]),
M('2026-03-30 14:05', YAN, ME_VT, """
David,

Read it. Lead with the system, but make the first paragraph about the instructor's problem, not about AI. Specific comments:

1. Intro: cut the "raised hand" metaphor; it's cute but costs three sentences.
2. Contribution list: three items max. Right now there are five.
3. Section 5: say clearly that labels are TA judgments, not ground truth about students' experience.
4. The heatmap figure is the strongest thing in the paper; move it to page 2.

Send me the revised intro tonight if you can.

Yan
"""),
M('2026-03-30 23:58', ME_VT, YAN, """
Revised intro and contribution list (now 3 items) are in the Overleaf; heatmap is on page 2. Section 6 is written. I'm going to do a full read for page limit tomorrow morning.
"""),
M('2026-03-31 11:20', YAN, ME_VT, """
The intro is much better. Two small things in Section 6: don't claim generalization beyond CS1, and add one sentence on telemetry privacy (reviewers will ask). Then submit. Good work.
"""),
M('2026-03-31 23:10', ME_VT, YAN, """
Submitted (#1187), 10 pages exactly. Added the privacy sentence and softened the generalization claim. Thank you for the fast turnaround these last three days.
"""),
]),

T('UIST 2026: submission #1187 received', ['project_tutortrace'], [
M('2026-04-01 00:14', PCS, ME_VT, """
Dear David Barron,

Your submission to the UIST 2026 Papers track has been received.

Submission #1187
Title: TutorTrace: Replaying Help-Seeking in LLM-Assisted Programming Labs
Authors: David Barron, Minsun, Xiaohang, Yan Chen
Last updated: 2026-04-01 03:58 UTC

You can update your submission until the deadline (March 31, 23:59 AoE). Reviews will be released on June 11, 2026, followed by a one-week rebuttal period ending June 18.

UIST 2026 Program Committee
"""),
], quote=False, labels=['Inbox', 'Category Updates']),

T('UIST 2026 reviews for submission #1187 are available', ['project_tutortrace'], [
M('2026-06-11 15:02', PCS, ME_VT, """
Dear David Barron,

Reviews for your UIST 2026 submission #1187 "TutorTrace: Replaying Help-Seeking in LLM-Assisted Programming Labs" are now available in the submission system.

You received 4 reviews (scores: 4, 3.5, 3, 2.5 on a 5-point scale). The rebuttal is optional, limited to 5,000 characters, and due June 18, 2026, 23:59 AoE.

Please address the main concerns raised by reviewers; do not introduce new contributions.

UIST 2026 Program Committee
"""),
], quote=False, labels=['Inbox', 'Category Updates']),

T('rebuttal plan — UIST #1187', ['project_tutortrace'], [
M('2026-06-12 00:40', ME_VT, YAN, """
Hi Yan,

Reviews are in (4 / 3.5 / 3 / 2.5). The three concerns that come up in more than one review:

1. Label reliability (R2, R4): is kappa 0.71 across 3 raters good enough, and were raters independent of the system design?
2. Generalization (R1, R3, R4): one course, one semester.
3. Telemetry privacy (R3): what do students consent to, and can instructors identify students in replays?

Plan: (1) report per-pair kappa and note that one rater (Xiaohang) wasn't involved in the guide's design; (2) promise a cross-course analysis using the spring CS 2114 data we already have consent for, plus a limitations section; (3) describe the consent text and the pseudonymized replay view.

Draft by Monday?

David
"""),
M('2026-06-12 09:15', YAN, ME_VT, """
Good plan. On (2), promise only what we can deliver by camera-ready: a cross-course comparison of state distributions, not a full re-labeling. On (3), R3 is the 2.5; be concrete and short. Monday is fine.
"""),
M('2026-06-15 22:30', ME_VT, YAN, """
Draft is in the Overleaf rebuttal project, 4,620 characters. Per-pair kappas are 0.69 / 0.71 / 0.74. I scoped the cross-course promise to state distributions as you suggested.
"""),
M('2026-06-17 10:05', YAN, ME_VT, """
Edits made directly in Overleaf. Mostly cuts in the privacy paragraph. It reads well now. Submit when ready.
"""),
M('2026-06-18 21:40', ME_VT, YAN, """
Rebuttal submitted (4,880 characters). Thanks Yan.
"""),
]),

T('kappa numbers for the rebuttal', ['project_tutortrace'], [
M('2026-06-13 14:20', ME_VT, [MINSUN, XIAOHANG], """
hey, for the uist rebuttal i need per-pair kappa on the 120-window overlap sets, guide v3 labels only. overall is 0.71. can one of you rerun the script on the final export so i'm not using numbers from march?
"""),
M('2026-06-14 11:05', XIAOHANG, [ME_VT, MINSUN], """
Reran on the final export: David–Minsun 0.69, David–Xiaohang 0.71, Minsun–Xiaohang 0.74. Fleiss' kappa across all three 0.71, same as before. Most disagreement is still PS vs SAE.
"""),
M('2026-06-14 11:40', ME_VT, [MINSUN, XIAOHANG], """
perfect, thank you. putting these in tonight
"""),
]),

T('Could we talk about a leave of absence?', ['project_vt_phd_admin', 'project_mathetic_company'], [
M('2026-06-19 16:30', ME_VT, YAN, """
Hi Yan,

Now that the rebuttal is in, I'd like to use part of our 1:1 on Monday (June 22) to talk about taking a leave of absence starting in the fall. Hudson and I have been building a research-notebook tool, and we have a chance to work on it full time through an incubator in San Francisco.

I want to make sure the UIST paper, the NeurIPS rebuttal and the lab's deployment data are in good shape before I go, and to hear what you think honestly.

Best,
David
"""),
M('2026-06-20 09:12', YAN, ME_VT, """
David,

Thank you for telling me ahead of time. Yes, let's talk Monday; I'll keep the full hour open. Please come with a timeline for the camera-ready and the NeurIPS rebuttal.

Yan
"""),
M('2026-06-22 18:05', ME_VT, YAN, """
Hi Yan,

Thank you for today. To confirm what we agreed:

- Leave of absence effective Fall 2026, up to two semesters, with intent to return.
- Before the leave: NeurIPS rebuttal (late July) and the leave form signed by Grace by July 31.
- During the leave: UIST camera-ready (Aug 14) and the talk in October.
- GRA funding ends August 15.
- I'll hand off the labeling infrastructure to Minsun with a written guide.

I'll start the paperwork with Grace this week.

David
"""),
]),

T('UIST 2026: conditional acceptance of submission #1187', ['project_tutortrace'], [
M('2026-07-02 13:00', PCS, ME_VT, """
Dear David Barron,

We are pleased to inform you that your submission #1187 "TutorTrace: Replaying Help-Seeking in LLM-Assisted Programming Labs" has been conditionally accepted to UIST 2026.

Conditions (from the meta-review):
1. Add the cross-course comparison promised in the rebuttal.
2. Add a limitations section covering generalization and telemetry privacy.
3. Report per-pair agreement.

Camera-ready versions are due August 14, 2026. Instructions will follow.

UIST 2026 Program Committee
"""),
M('2026-07-02 13:40', ME_VT, [YAN, MINSUN, XIAOHANG], """
we're in (conditionally)!! conditions are exactly what we promised in the rebuttal. thank you all
""", subject='Fwd: UIST 2026: conditional acceptance of submission #1187', quote=True),
M('2026-07-02 14:22', YAN, [ME_VT, MINSUN, XIAOHANG], """
Congratulations, everyone. Well deserved. Let's get the cross-course comparison done before David's leave starts.
""", subject='Re: Fwd: UIST 2026: conditional acceptance of submission #1187'),
], quote=False),

T('IDETrace: leakage bug in the train/test split', ['project_idetrace'], [
M('2026-07-24 23:50', ME_VT, YAN, """
Hi Yan,

I found a problem in IDETrace while preparing the NeurIPS rebuttal. The split script assigned windows to train/test at random, so windows from the same student ended up in both sets. The model was partly recognizing students, not states.

I fixed it with a split grouped by student id. Macro-F1 drops from 0.81 to 0.74.

My proposal: report both numbers in the rebuttal, explain the bug plainly, and release the corrected split script. I think hiding it would be worse than the drop.

David
"""),
M('2026-07-25 08:40', YAN, ME_VT, """
David, I agree completely. Report both, explain the fix, release the script. 0.74 with a correct split is still a solid baseline for a datasets paper. Thank you for catching it before a reviewer did.

Yan
"""),
]),

T('Leave of absence form — signatures', ['project_vt_phd_admin'], [
M('2026-07-28 10:20', ME_VT, GRACE, """
Hi Grace,

Following up on my leave of absence for Fall 2026, which Dr. Chen and I discussed on June 22. I've filled in and signed the Graduate School leave request (attached). Dr. Chen has agreed to sign as advisor.

Could you tell me what else the department needs, and whether my GRA appointment end date (August 15) has to be entered separately?

Thank you,
David
""", att=[A('pdf', 'Barron_Leave_of_Absence_Request_unsigned.pdf', LOA_FORM[:-1] + [('table', [['Signature', 'Name', 'Date'], ['Student', 'David Barron', '2026-07-28'], ['Advisor', '', ''], ['Graduate Program Coordinator', '', ''], ['Graduate School', '', '']])], 'Leave of Absence Request — David Barron')]),
M('2026-07-28 15:45', GRACE, ME_VT, """
Hi David,

Thanks. I'll route it to Dr. Chen for her signature, then sign as coordinator and submit it to the Graduate School. The GRA end date is handled separately through HR; I'll start that today with an end date of August 15.

One thing: you'll stay enrolled through the end of summer session, so you should still have VT email and library access during the leave.

Best,
Grace

Grace Kim | Graduate Program Coordinator | Department of Computer Science | Virginia Tech
"""),
M('2026-07-31 11:30', GRACE, ME_VT, """
Hi David,

All signatures are in (you July 29 on the revised version, Dr. Chen July 30, me today). The signed form is attached for your records and has been submitted to the Graduate School. You should receive an official confirmation from them within two weeks.

Good luck in San Francisco!

Grace
""", att=[A('pdf', 'Barron_Leave_of_Absence_Request_signed.pdf', LOA_FORM, 'Leave of Absence Request — David Barron (signed)')]),
M('2026-07-31 12:05', ME_VT, GRACE, """
Thank you so much, Grace, for moving this so quickly.

David
"""),
], notes='HARD CASE: email with attachments — leave-of-absence form PDF (unsigned and signed versions), signed 2026-07-31'),

T('UIST 2026 camera-ready instructions', ['project_tutortrace'], [
M('2026-07-20 12:00', PCS, ME_VT, """
Dear authors,

Camera-ready instructions for accepted UIST 2026 papers:

- Deadline: August 14, 2026, 23:59 AoE. No extensions.
- Use the ACM TAPS workflow; upload LaTeX source, not PDF only.
- Include CCS concepts, keywords, and the rights statement you will receive after completing the ACM rights form.
- Upload a 30-second preview video and a 3-minute video figure by August 21.
- At least one author must register at the presenter rate by September 4.

UIST 2026 Program Committee
"""),
M('2026-08-14 22:40', PCS, ME_VT, """
Dear David Barron,

Your camera-ready for submission #1187 has been received and passed TAPS validation.

Final page count: 11 + references
ACM rights form: completed (2026-08-10)
DOI (reserved): 10.1145/3746059.3747711

Thank you,
UIST 2026 Program Committee
""", subject='UIST 2026: camera-ready received for #1187'),
], quote=False, labels=['Inbox', 'Category Updates']),

T('Presenter registration reminder — UIST 2026', ['project_tutortrace'], [
M('2026-08-25 09:00', REG, ME_VT, """
Dear David Barron,

Our records show that paper #1187 does not yet have a registered presenting author. At least one author must register at the presenter rate by September 4, 2026, or the paper may be removed from the program and proceedings.

Student rate (early): $425
Regular presenter rate: $795

Register in the conference portal with your submission ID.

UIST 2026 Registration
"""),
M('2026-08-27 15:22', REG, ME_VT, """
Dear David Barron,

Thank you for registering for UIST 2026.

Registration: Student (early)
Confirmation: UIST26-S-2214
Amount paid: $425.00
Presenting: #1187, session "Learning & Tutoring", Wednesday October 7

A receipt is available in the conference portal.

UIST 2026 Registration
""", subject='UIST 2026 registration confirmation — UIST26-S-2214'),
], quote=False, labels=['Inbox', 'Category Updates']),

T("it's been a while — UIST talk prep", ['project_tutortrace'], [
M('2026-09-08 20:15', ME_VT, YAN, """
Hi Yan,

I realize I've gone quiet since the camera-ready; the move and the first month at Surplus swallowed August, and I'm sorry for not keeping you updated.

The UIST talk is October 7 (15 minutes + 5 Q&A, session "Learning & Tutoring"). I have a first outline:
1. The instructor's problem (2 min)
2. TutorTrace replay demo (5 min)
3. Deployment: 87 students, labeling, kappa 0.71 (4 min)
4. Cross-course comparison + limitations (3 min)
5. What instructors changed (1 min)

Would you be willing to watch a practice run in late September? Zoom is easiest from here.

David
"""),
M('2026-09-10 08:50', YAN, ME_VT, """
David,

Good to hear from you, and no need to apologize; I assumed you were busy. Yes to a practice run. How about Tuesday September 29 at 4 pm Eastern? Invite the lab; Minsun and Xiaohang will want to see it.

One suggestion now: move the demo earlier. Show the replay in the first two minutes, then explain the problem.

Yan
"""),
M('2026-09-10 10:30', ME_VT, YAN, """
Sept 29 at 4 pm ET (1 pm for me) works. I'll invite the lab and restructure so the demo comes first.
"""),
]),

T('session chair — Learning & Tutoring, Oct 7', ['project_tutortrace'], [
M('2026-09-15 07:45', TOMAS, ME_VT, """
Dear David,

I'm chairing the "Learning & Tutoring" session at UIST on Wednesday October 7, where you'll present TutorTrace (#1187). A few details:

- Session runs 10:30-12:00; you're the third of four talks (approx. 11:10).
- 15 minutes for the talk and 5 for questions. I'll give you a 3-minute and a 1-minute warning.
- Please send me a two-sentence bio I can read before your talk.
- We're doing a remote AV check over Zoom on Friday October 2; would 9:00 am Pacific work for you?

Looking forward to it,
Tomás Reyes
"""),
M('2026-09-15 10:20', ME_VT, TOMAS, """
Dear Tomás,

Thank you for chairing. Friday October 2 at 9:00 am PT works for the AV check. My bio:

"David Barron is a PhD student in Computer Science at Virginia Tech, advised by Yan Chen in the PRIME Lab, currently on leave to co-found Mathetic. He builds tools that help instructors see how students learn with AI assistants."

I'll show a short live demo during the talk; I'll test it during the AV check and bring a recorded backup.

Best,
David
"""),
M('2026-09-30 16:10', TOMAS, ME_VT, """
Great, thanks David. Zoom details for the AV check on Friday: Meeting ID 934 5512 0087, passcode uist26. Please join from the laptop you'll present with.

Tomás
"""),
]),

T('practice talk feedback', ['project_tutortrace'], [
M('2026-09-29 15:30', YAN, ME_VT, """
David,

Thank you for the practice talk. Overall: clear, the demo-first structure works, and you finished at 14:20. Comments:

1. Slide 6: the kappa table is too dense to read in 10 seconds. Show only the overall 0.71 and put per-pair numbers in backup.
2. The section B incident: one sentence is enough; you spent a minute on it.
3. Limitations slide: lead with generalization; that's the question you'll get.
4. Expect a privacy question. Have the pseudonymized replay screenshot ready.

Minsun noted the ordering of states on the legend differs between the demo and the slides.

Yan
""", cc=[MINSUN, XIAOHANG]),
M('2026-09-29 21:45', ME_VT, YAN, """
Thank you, Yan (and Minsun for the legend catch). I'll simplify slide 6, cut the incident to one sentence, and reorder the limitations. I'll send the final deck before the AV check on Friday.
""", cc=[MINSUN, XIAOHANG]),
]),

T('travel funding request — UIST 2026 (Oct 7 talk)', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-09-24 14:30', ME_VT, GRACE, """
Hi Grace,

I'd like to request departmental travel funding to present our UIST 2026 paper (TutorTrace, #1187) on October 7. I'm the first author and presenter. A budget and justification are attached; the estimated total is $1,786.32. Dr. Chen has agreed that PRIME Lab funds will cover whatever the department award does not.

I'm on approved leave this semester; the paper was written and accepted while I was enrolled. Please let me know if that affects eligibility.

Thank you,
David
""", att=[A('xlsx', 'Barron_UIST2026_travel_budget.xlsx', TRAVEL_BUDGET, 'UIST 2026 travel budget — David Barron')]),
M('2026-09-25 10:05', GRACE, ME_VT, """
Hi David,

Thanks, received. Being on leave doesn't make you ineligible for presenting work done while enrolled, but the request needs Dr. Chen's approval email and a copy of your registration receipt. The department travel award for a presenting student is capped at $1,000; the remaining $786.32 would be charged to PRIME Lab.

Once approved, you'll need a Concur travel request before the trip and an expense report afterwards.

Best,
Grace
"""),
M('2026-09-25 13:40', ME_VT, GRACE, """
Thank you, Grace. Registration confirmation attached (UIST26-S-2214), and I've asked Dr. Chen to send her approval directly to you. I'll create the Concur request today.
""", att=[A('pdf', 'UIST26_registration_confirmation_S-2214.pdf', [
    ('title', 'UIST 2026 — Registration Confirmation'),
    ('p', 'Confirmation: UIST26-S-2214 · 2026-08-27'),
    ('table', [['Registrant', 'Category', 'Status'], ['David Barron (Virginia Tech)', 'Student (early)', 'Confirmed']]),
    ('p', 'Presenting paper #1187, session "Learning & Tutoring", Wednesday October 7. An itemized receipt can be downloaded from the registration portal.'),
], 'UIST 2026 registration confirmation', '')]),
], notes='HARD CASE: email with attachments — travel-funding request with xlsx budget (2026-09-24) and registration confirmation PDF'),
]
