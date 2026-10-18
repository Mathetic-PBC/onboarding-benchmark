"""Outlook (VT Microsoft 365) mailbox dbarron410@vt.edu — hand-written conversations, 2025-10-17 .. 2026-10-17."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gmail'))
from _dsl import *

# walk-on senders (service / list addresses, invented)
GRADSCHOOL = P('VT Graduate School', 'gradschool-noreply@vt.edu')
GRADENROLL = P('Graduate Enrollment Services', 'grad-enrollment@vt.edu', ET)
REGISTRAR = P('University Registrar', 'registrar-notices@vt.edu')
PAYROLL = P('VT Human Resources - Payroll', 'hr-payroll-noreply@vt.edu')
CONCUR = P('SAP Concur', 'autonotification@concursolutions.com')
FOURHELP = P('4Help - Virginia Tech IT', '4help-noreply@vt.edu')
FOURHELP_TECH = P('4Help Service Desk', '4help@vt.edu', ET)
ITSO = P('VT IT Security Office', 'itso-notices@vt.edu')
CANVAS = P('Canvas Notifications', 'notifications@instructure.com')
STAFF3604 = P('CS 3604 Course Staff', 'cs3604-staff@vt.edu', ET)
SEMINAR = P('CS Seminar Series', 'cs-seminars@vt.edu')
PARKING = P('VT Parking Services', 'parking-noreply@vt.edu')
PARKING_APPEALS = P('Parking Appeals', 'parking-appeals@vt.edu', ET)
ILL = P('University Libraries ILLiad', 'illiad-noreply@vt.edu')
GSA = P('Graduate Student Assembly', 'gsa-travelfund@vt.edu')
CS_GRAD = P('CS Graduate Students', 'cs-grads@vt.edu')

SIG_GRACE = """Grace Kim | Graduate Program Coordinator | Department of Computer Science
Virginia Tech | 2202 Kraft Drive | Blacksburg, VA 24060"""
SIG_BROOKS = """Alan Brooks, Ph.D.
Grado Department of Industrial and Systems Engineering
Virginia Tech"""
SIG_ME = """David Barron
Ph.D. Student, Computer Science | PRIME Lab
Virginia Tech"""

P3_RUBRIC = {
    'P3 rubric v2': [
        ['Criterion', 'Points', 'Full credit', 'Partial', 'Notes for graders'],
        ['Stakeholder map', 20, 'All 4+ stakeholders, interests stated', '2-3 stakeholders', 'Do not require a diagram'],
        ['Ethical analysis (2 frameworks)', 30, 'Two frameworks applied to the same decision', 'One framework or name-dropping', 'ACM Code counts as a framework'],
        ['Recommendation', 20, 'Concrete, actionable, addresses tradeoff', 'Vague ("be more careful")', ''],
        ['Use of sources', 15, '3+ cited, at least 1 primary', '1-2 sources', 'Wikipedia alone = partial'],
        ['Writing / mechanics', 15, 'Clear, <= 1,500 words', 'Over length or hard to follow', '-2 per 250 words over'],
        ['Total', '=SUM(B2:B6)', '', '', ''],
    ],
    'Grading split': [
        ['Grader', 'Section', 'Students', 'Range (Canvas order)', 'Due'],
        ['David Barron', '001', 32, '1-32', '2025-11-03'],
        ['Second GTA', '002', 32, '33-64', '2025-11-03'],
        ['Total', '', '=SUM(C2:C3)', '', ''],
    ],
}

THREADS = [

# ------------------------------------------------------------------ CS 3604 (Fall 2025)
T('Submission comment: Project 3 - Case Study Analysis', ['project_cs3604_gta'], [
M('2025-10-22 23:41', CANVAS, ME_VT, """
Tyler M. just made a new comment on the submission for Tyler M. for Project 3: Case Study Analysis (Data Privacy)

"Hi, I uploaded the wrong PDF at 11:38 (it's my draft for another class). The correct file is attached now as a second attempt, still before the 11:59 deadline. Can you grade attempt 2? Sorry!"

You can review the submission details here: https://canvas.vt.edu/courses/218840/assignments/1984417/submissions/

You can change your notification settings at https://canvas.vt.edu/profile/communication
""", html=True),
], quote=False),

T('P3 rubric v2 + grading split', ['project_cs3604_gta'], [
M('2025-10-27 09:15', STAFF3604, ME_VT, """
Hi David,

Attached is the P3 rubric with the changes we talked about on Friday:

- "Ethical analysis" now explicitly requires two frameworks applied to the same decision (last term people listed frameworks without applying them).
- Writing/mechanics deduction is -2 per 250 words over the 1,500 limit, capped at -6.
- Second tab has the split: you take section 001 (32 students), the other GTA takes 002 (32). Grades back by Monday Nov 3.

Please grade three submissions first and send them to me so we can calibrate before you do the rest.

Thanks,
CS 3604 teaching team
""", att=[A('xlsx', 'CS3604_P3_rubric_v2.xlsx', P3_RUBRIC, 'CS 3604 P3 rubric v2', 'CS 3604 Course Staff')]),
M('2025-10-28 22:47', ME_VT, STAFF3604, """
Hi,

Calibration set graded (Canvas order #4, #11, #19): 84, 71, 92. Comments are in SpeedGrader.

Two questions:
1. #11 cites the ACM Code and then Kantian ethics but only applies Kant to the decision. I gave 18/30 under "one framework". OK?
2. For the stakeholder map, one student included "future users of the dataset" as a stakeholder. I counted it, seems like a good catch rather than padding.

Will finish the remaining 29 by Sunday night.

""" + SIG_ME),
M('2025-10-29 08:52', STAFF3604, ME_VT, """
Both calls are right. 18/30 is what I would have given #11, and yes, count "future users of the dataset" (that's exactly the kind of thinking we want).

Thanks for turning these around fast.
"""),
]),

T('Announcement: P4 due date and late-day policy reminder', ['project_cs3604_gta'], [
M('2025-11-04 14:05', CANVAS, ME_VT, """
CS 3604: Professionalism in Computing (Fall 2025) - Announcement

P4 due date and late-day policy reminder

Project 4 (Policy Memo: Automated Screening in Hiring) is due Friday, November 21 at 11:59 PM.

Reminder about late days:
- Everyone has 3 late days for the semester, used in whole-day increments.
- Late days are tracked automatically from the Canvas submission timestamp. A submission at 12:05 AM uses one late day.
- You cannot use more than 2 late days on any single project.
- Once you are out of late days, late work loses 10% per day.

Check your remaining late days in the "Late Days" column in Grades before you plan around them.

Posted by: CS 3604 Course Staff

View announcement: https://canvas.vt.edu/courses/218840/discussion_topics/
""", html=True),
], quote=False),

T('Reminder: Final grades due Monday, December 15 at 5:00 PM', ['project_cs3604_gta'], [
M('2025-12-08 08:00', REGISTRAR, ME_VT, """
To: Instructors and Graduate Teaching Assistants with grading access

Final grades for Fall 2025 are due in Hokie SPA / Banner by Monday, December 15, 2025 at 5:00 PM ET.

- Grades of I (Incomplete) require a completed Incomplete Grade Agreement on file with the department.
- Grades entered in Canvas are not automatically submitted; use the Canvas Grade Export or enter them directly in Banner.
- After the deadline, grade changes require a Grade Change Form signed by the department head.

Questions: registrar@vt.edu

Office of the University Registrar
Virginia Tech
"""),
], quote=False),

T('Final project grading split + calibration', ['project_cs3604_gta'], [
M('2025-12-08 10:32', STAFF3604, ME_VT, """
Hi David,

Final projects are in: 63 of 64 submitted (one student has an approved incomplete). Plan:

- You grade teams 1-8 (presentation + written report), I take 9-16.
- Use the final-project tab in the shared rubric sheet. The presentation score is already entered from the in-class peer + staff scores.
- Please have everything in by Saturday Dec 13 at noon so I have Sunday to resolve disputes and export to Banner before the Monday 5 PM deadline.

Also: Jared P. emailed about P4 late days. I asked him to send you the timestamp screenshot since you graded P4. Please look at it before Friday.
"""),
M('2025-12-09 23:58', ME_VT, STAFF3604, """
Sounds good. Teams 1-4 done (avg 88.5). 5-8 tomorrow night.

On Jared's P4: the Canvas timestamp is 11/23 00:14, so that's 2 late days (due 11/21 11:59 PM). He had 2 left after P2, so it should be 0 penalty. I had applied -10% because the Late Days column showed 1 remaining. That column was wrong: it double-counted his P2 resubmission. I've fixed the grade (78 -> 87) and left a comment. Flagging it in case the column double-counted for anyone else who resubmitted.

""" + SIG_ME),
M('2025-12-10 09:20', STAFF3604, ME_VT, """
Good catch. I checked: three other students resubmitted P2 and were affected the same way. I'll fix those myself. Thanks.
"""),
]),

T('Submission comment: Project 4 - Policy Memo', ['project_cs3604_gta'], [
M('2025-12-09 16:12', CANVAS, ME_VT, """
Jared P. just made a new comment on the submission for Jared P. for Project 4: Policy Memo (Automated Screening in Hiring)

"I don't think the late penalty is right. I submitted at 12:14am on 11/23 which is 2 late days and I still had 2 left (I only used 1 on P2, the resubmission was within the window). Screenshot of my late days page attached. Could you re-check?"

Attachments: latedays_screenshot.png

You can review the submission details here: https://canvas.vt.edu/courses/218840/assignments/1984421/submissions/
""", html=True),
], quote=False),

T('Recent Canvas Notifications', ['project_cs3604_gta'], [
M('2025-12-12 07:00', CANVAS, ME_VT, """
Daily summary for CS 3604: Professionalism in Computing (Fall 2025)

Submission comment - Final Project Report: Team 6 ("Ethics review for a campus facial-recognition pilot")
  Lauren S.: "We noticed our appendix B didn't render in the PDF, it's in the shared doc linked on page 2 if that's OK."

Submission comment - Project 4: Policy Memo
  Jared P.: "Thank you for fixing it!"

Grade changed - Project 4: Policy Memo
  1 grade was changed by David Barron.

Discussion reply - Week 15: Professional licensing for software engineers?
  4 new replies.

Change notification preferences: https://canvas.vt.edu/profile/communication
""", html=True),
], quote=False),

# ------------------------------------------------------------------ IT / security
T('Phishing alert: fake "Payroll Adjustment" messages', ['project_none'], [
M('2025-11-18 11:30', ITSO, ME_VT, """
The IT Security Office is aware of a phishing campaign targeting Virginia Tech employees and graduate assistants.

The messages:
- have the subject "Payroll Adjustment - Action Required" or "Updated Direct Deposit Form"
- claim to come from "VT HR Payroll" but are sent from external addresses
- link to a fake VT login page that asks for your PID, password and a Duo code

What to do:
- Do not click the link or enter your credentials.
- Use the "Report Phishing" button in Outlook, or forward the message as an attachment to abuse@vt.edu.
- If you already entered your password, change it at https://onecampus.vt.edu and contact 4Help at 540-231-4357.

VT HR will never ask you to update direct deposit information through an emailed link.

IT Security Office
Division of Information Technology
"""),
], quote=False),

T('Your VT password expires in 14 days', ['project_none'], [
M('2026-02-02 06:00', FOURHELP, ME_VT, """
Hello David Barron (PID: dbarron410),

The password for your Virginia Tech account will expire on Monday, February 16, 2026.

To change it before then, go to https://accounts.it.vt.edu and choose "Change Password". Your new password must:
- be at least 12 characters long
- not match any of your previous 5 passwords

After you change it, update the saved password on your phone's mail app and on eduroam, or you may be locked out after repeated failed attempts.

4Help - Virginia Tech IT
540-231-HELP (4357) | 4help.vt.edu
"""),
], quote=False),

T('New Duo device activated for dbarron410', ['project_none'], [
M('2026-08-04 19:22', FOURHELP, ME_VT, """
A new device was added to your Duo two-factor account.

Account: dbarron410
Device: macOS (Duo Device Health / Touch ID platform authenticator)
Added: Tuesday, August 4, 2026 at 7:21 PM ET
Method: Added from an existing device (iPhone, Duo Mobile push approved)

If you added this device, no action is needed.

If you did not add this device, contact 4Help immediately at 540-231-4357 so we can remove it and secure your account.

4Help - Virginia Tech IT
"""),
], quote=False),

T('Outlook on new Mac keeps asking for password (Ticket INC0412877)', ['project_none'], [
M('2026-08-05 10:48', ME_VT, FOURHELP_TECH, """
Hi,

I set up a new MacBook yesterday (Duo device already added). Outlook for Mac (16.88) keeps popping up a password prompt every few minutes for dbarron410@vt.edu. Entering the password works for a bit and then it comes back. Web Outlook is fine, and Teams on the same Mac signs in without problems.

Things I tried: removed and re-added the account, deleted the "Microsoft Office Identities Cache 3" keychain entries, rebooted.

Thanks,
David Barron
"""),
M('2026-08-05 15:16', FOURHELP_TECH, ME_VT, """
Hi David,

Thanks for the details, that helps. This is almost always a stale legacy-auth profile on new Macs. Please try:

1. Quit Outlook. In Keychain Access, delete every item named "Exchange" or "MicrosoftOffice15_2_Data:ADAL:..." (not just the Identities Cache).
2. Open Outlook, Settings > Accounts, remove the account.
3. Re-add it, and when you are asked which kind of account, pick "Microsoft 365" (not "Exchange"). You should get the VT Duo prompt in a browser window, not the small grey password box.

If the grey box comes back, reply here with the Outlook version and we'll do a remote session.

Chris
4Help Service Desk | Virginia Tech IT
"""),
M('2026-08-05 21:40', ME_VT, FOURHELP_TECH, """
That fixed it. Choosing "Microsoft 365" instead of "Exchange" was the missing step. I got the Duo browser prompt and no password boxes since. You can close the ticket.

Thanks!
David
"""),
]),

# ------------------------------------------------------------------ seminars
T('CS Seminar Thu Oct 23: "Augmenting the Intellect, Sixty Years Later"', ['project_augmenting_cognition_reading_group'], [
M('2025-10-20 12:10', SEMINAR, ME_VT, """
Computer Science Seminar Series

Augmenting the Intellect, Sixty Years Later: What the Mother of All Demos Still Asks of HCI
Thursday, October 23, 2025 | 4:00-5:15 PM | McBryde 100 (light refreshments at 3:45)
Speaker: Prof. L. Hartwell, School of Information

Abstract: In 1962 Douglas Engelbart framed computing as a way to augment human intellect, not to automate it. Most of what we build today, including AI assistants, optimizes for the automation half. This talk revisits the original "augmentation" framework (artifacts, language, methodology, training), shows three recent systems that take it seriously, and argues that provenance, knowing where a thought came from, is the missing piece in current tools for thought.

Graduate students enrolled in CS 5944 should sign the attendance sheet at the door.

Zoom (for remote attendees): link on the CS events calendar.
"""),
], quote=False),

T('HCI Seminar Wed Jan 21: "Do students ask for help at the right time?"', ['project_tutortrace'], [
M('2026-01-19 09:00', SEMINAR, ME_VT, """
Computer Science Seminar Series (HCI)

Do Students Ask for Help at the Right Time? Telemetry from Two Years of Introductory Programming Labs
Wednesday, January 21, 2026 | 12:30-1:30 PM | Torgersen 1100 (lunch provided, RSVP below)
Speaker: Dr. K. Mendes, Department of Computer Science

Abstract: We logged editor activity, test runs and help requests in 14 CS1 lab sections over four semesters. Students who waited more than six minutes after a failing test before asking for help were much less likely to finish the lab, but students who asked within the first minute did not do better than those who waited two to four minutes. I will show what predicts a "productive wait" and what TAs can see in real time.

RSVP for lunch: https://forms.office.com/r/cs-seminar-rsvp
"""),
M('2026-01-19 22:37', ME_VT, YAN, """
Hi Yan,

This seems very close to the TutorTrace framing, especially the "productive wait" window. Their signal is wait time after a failing test, and ours is the stalled-after-error state from labeling guide v3. I'm planning to go and will take notes. It might be worth citing in the related work if they have a paper out, and maybe asking whether their lab sections had an AI assistant at all.

Best,
David
""", subject='FW: HCI Seminar Wed Jan 21: "Do students ask for help at the right time?"'),
M('2026-01-20 08:14', YAN, ME_VT, """
Yes, please go. Ask about the assistant question. If they had none, that's a clean contrast for us. Send me your notes after.

Yan
"""),
]),

T('CS Distinguished Lecture Mon Mar 2: Robust learning under distribution shift', ['project_none'], [
M('2026-02-24 10:00', SEMINAR, ME_VT, """
Computer Science Distinguished Lecture

When the Test Set Lies: Robust Learning Under Distribution Shift
Monday, March 2, 2026 | 3:30-4:45 PM | Goodwin Hall 155
Speaker: Prof. S. Varga, Department of Statistics and Data Science

Abstract: Benchmarks report accuracy on held-out data drawn from the training distribution, but deployed models meet hospitals, cities and users that differ from the training set. This talk covers three practical tools: grouped and temporal splits that expose leakage, importance-weighted validation, and a simple stress-testing protocol that has caught overstated results in published work.

Reception to follow in the Goodwin atrium.
"""),
], quote=False),

T('CANCELED: Grad Seminar Thu Sept 10', ['project_none'], [
M('2026-09-08 09:30', SEMINAR, ME_VT, """
The Graduate Seminar scheduled for Thursday, September 10 (12:30 PM, Torgersen 1100) is canceled because the speaker is ill. We will try to reschedule later in the semester.

The September 17 seminar ("Verified compilers for smart contracts") will go ahead as planned.

CS Seminar Series
"""),
], quote=False),

# ------------------------------------------------------------------ ISE 6664 (Spring 2026)
T('ISE 6664 - Week 1 readings and Teams channel', ['project_ise6664_affective_computing'], [
M('2026-01-13 16:20', BROOKS, ME_VT, """
Welcome to ISE 6664: Affective Design & Computing.

Before Thursday:
1. Read the course syllabus on Canvas (note: the final project is a team project, 2-3 people, with a presentation on April 30 and a written report due May 8).
2. Read the two Week 1 readings in the "Readings" folder: the 1997 overview chapter on affective computing and the short critique of emotion recognition from facial expressions. Come with one question for each.
3. Join the course Teams channel (link on Canvas). Project team formation and office-hour sign-ups will happen there.

Office hours: Tuesdays 2-3:30 PM, Whittemore 529, or on Teams by appointment.

""" + SIG_BROOKS),
], quote=False),

T('ISE 6664 project check-in: Frustration signals team', ['project_ise6664_affective_computing'], [
M('2026-03-05 13:02', BROOKS, [ME_VT, MAYA, JORDAN], """
Hi David, Maya and Jordan,

I've scheduled our mid-semester project check-in for Tuesday, March 10 at 2:00 PM on Teams (invite attached).

Please bring:
- the final list of transcript sources (how many tutoring sessions, from which system)
- your draft coding scheme for frustration markers, with 2-3 examples per code
- a one-paragraph plan for checking inter-rater agreement

20 minutes is enough.

""" + SIG_BROOKS, att=[A('ics', 'invite.ics', dict(summary='ISE 6664 project check-in: Frustration signals in AI-tutoring transcripts',
    start='2026-03-10 14:00', end='2026-03-10 14:20', location='Microsoft Teams Meeting',
    description='Mid-semester check-in. Bring: transcript sources, draft coding scheme, IRR plan.',
    organizer=BROOKS, attendees=[ME_VT, MAYA, JORDAN], outlook=True))]),
M('2026-03-05 21:15', ME_VT, BROOKS, """
Accepted. We'll have the coding scheme draft and the source list ready (currently 212 anonymized sessions from two course-tutor deployments, 9,800 student turns).

Thanks,
David
""", subject='Accepted: ISE 6664 project check-in: Frustration signals team'),
]),

T('Coding scheme for frustration markers - draft v1', ['project_ise6664_affective_computing'], [
M('2026-04-14 22:51', MAYA, [ME_VT, JORDAN], """
Hi both,

Draft v1 of the coding scheme is attached. Main changes since the check-in with Dr. Brooks:

- Merged "repeated question" and "rephrased question" into one code, REPEAT, since we couldn't tell them apart reliably.
- Added NEG-SELF ("I'm so dumb", "I'll never get this") separate from NEG-TUTOR ("this isn't helping").
- Dropped the punctuation-intensity code ("???", "!!!"). It fired on 30% of turns and most were neutral.

Jordan, can you run the IRR on the 120-turn sample before Thursday? We need kappa per code for the slides.

Maya
""", att=[A('docx', 'FrustrationCodingScheme_v1.docx', [
    ('title', 'Coding Scheme: Frustration Markers in AI-Tutoring Transcripts (v1)'),
    ('p', 'ISE 6664 team project — D. Barron, M. Torres, J. Lee. Unit of analysis: one student turn.'),
    ('table', [['Code', 'Definition', 'Example'],
               ['REPEAT', 'Student repeats or rephrases a question already answered in the last 3 turns', '"ok but why is it still index out of range"'],
               ['NEG-SELF', 'Negative self-evaluation', '"i am so bad at recursion"'],
               ['NEG-TUTOR', 'Negative evaluation of the tutor or its help', '"that hint is useless"'],
               ['GIVE-UP', 'Explicit intent to stop or ask for the answer', '"just tell me the code"'],
               ['TERSE', 'Reply of 1-2 words after a long tutor explanation', '"ok"'],
               ['NONE', 'No frustration marker', '']]),
    ('h2', 'Decision rules'),
    ('bullet', 'A turn can have more than one code except NONE.'),
    ('bullet', 'TERSE only counts when the previous tutor turn is longer than 80 words.'),
    ('bullet', 'Sarcasm is coded by its literal target (self vs tutor).'),
], 'Frustration coding scheme v1', 'Maya Torres')]),
M('2026-04-15 09:40', JORDAN, [ME_VT, MAYA], """
Ran it on the 120-turn sample (David and me as coders). Cohen's kappa per code:
REPEAT 0.78, NEG-SELF 0.81, NEG-TUTOR 0.66, GIVE-UP 0.84, TERSE 0.52.

TERSE is the problem. I kept coding "ok" as TERSE even after short tutor turns. The 80-word rule needs to be checked mechanically, not by eye.

Jordan
"""),
M('2026-04-15 11:05', ME_VT, [MAYA, JORDAN], """
Agree on TERSE. I'll compute it in the script (tutor turn length > 80 words + student turn <= 2 words) and drop it from human coding. Then the human codes are all >= 0.66, and we report TERSE as an automatic feature.

I'll update the slides tonight. I can also write the methods section for the report since I'm doing the script anyway.

David
"""),
]),

T('ISE 6664 final presentations - Thursday April 30 schedule', ['project_ise6664_affective_computing'], [
M('2026-04-27 08:45', BROOKS, ME_VT, """
Final presentations are Thursday, April 30 in Whittemore 300 (regular class time, 2:00-4:45 PM).

- 12 minutes per team + 3 minutes questions. I will cut you off at 13.
- Upload slides (PDF or PPTX) to the Canvas assignment by 12:00 PM that day. We'll present from the room PC.
- Order: (1) Haptic stress cues, (2) Frustration signals in AI-tutoring transcripts, (3) Music and mood in study playlists, (4) Wearables and exam anxiety, (5) Voice prosody in customer support calls.
- Written reports (max 15 pages) are due Friday, May 8 at 11:59 PM.

""" + SIG_BROOKS),
M('2026-04-27 12:20', ME_VT, BROOKS, """
Dr. Brooks,

Quick question for our team (2nd slot): can we show a 40-second screen recording of the annotation tool inside the 12 minutes, or should we keep to static slides? We have a static backup either way.

Thank you,
David Barron
"""),
M('2026-04-27 14:02', BROOKS, ME_VT, """
The recording is fine. Test the audio on the room PC at 1:45 if it has sound. Embedding it in the PPTX is safer than linking out.

AB
"""),
]),

T('Team sync - final presentation dry run', ['project_ise6664_affective_computing'], [
M('2026-04-28 10:30', MAYA, [ME_VT, JORDAN], """
Dry run tomorrow, 7 PM on Teams (invite attached). Let's time it. Last run was 14:30, we need to be under 12.

Proposed cuts: drop the related-work slide (say it in one sentence), and merge the two kappa slides into one table.
""", att=[A('ics', 'invite.ics', dict(summary='Dry run: Frustration signals final presentation',
    start='2026-04-29 19:00', end='2026-04-29 20:00', location='Microsoft Teams Meeting',
    description='Timed run-through. Target: 12 min. Slides: Teams > Files > Final.',
    organizer=MAYA, attendees=[ME_VT, JORDAN], outlook=True))]),
], quote=False),

T('Project report feedback - Frustration signals in AI-tutoring transcripts', ['project_ise6664_affective_computing'], [
M('2026-05-12 15:30', BROOKS, [ME_VT, MAYA, JORDAN], """
Hi team,

Your report grade is 93/100 (the feedback sheet is attached). Overall: a well-scoped project with an honest reliability analysis. The decision to move TERSE to an automatic feature, and to explain why, was the right call.

Main points:
- The 14 pages are well used. Section 5 is the strongest part of the report.
- -4: the claim that NEG-TUTOR "predicts session abandonment" rests on 31 abandoned sessions. Call it an association and report the confidence interval.
- -3: the limitations section doesn't discuss that both tutoring deployments were in the same university and course level.

If you're planning to turn this into a workshop paper, I'm happy to read a draft over the summer.

""" + SIG_BROOKS, att=[A('pdf', 'ISE6664_FinalReport_Feedback_FrustrationSignals.pdf', [
    ('title', 'ISE 6664 Final Project: Report Feedback'),
    ('p', 'Team: D. Barron, M. Torres, J. Lee — "Frustration signals in AI-tutoring transcripts" (14 pp.)'),
    ('table', [['Component', 'Points', 'Score'], ['Problem framing & motivation', 15, 15], ['Related work', 10, 9],
               ['Method & coding scheme', 25, 25], ['Results & reliability', 25, 21], ['Discussion & limitations', 15, 12],
               ['Writing & figures', 10, 10], ['Total', 100, 93]]),
    ('h2', 'Comments'),
    ('p', 'NEG-TUTOR vs. abandonment: n=31 abandoned sessions; report as an association with a 95% CI rather than "predicts".'),
    ('p', 'Limitations: both deployments come from one institution and course level; say how this limits the claims.'),
    ('p', 'Strength: kappa per code reported, and TERSE moved to an automatic feature with a clear rationale.'),
], 'ISE 6664 report feedback', 'Alan Brooks')]),
M('2026-05-12 21:08', ME_VT, BROOKS, """
Thank you, Dr. Brooks. This was a fun project. We'll fix the abandonment wording (a bootstrap CI over sessions) and add the single-institution limitation before we post a version anywhere. We may take you up on the summer read.

Best,
David
"""),
]),

# ------------------------------------------------------------------ parking
T('Parking Citation Notice - Citation VT0418827', ['project_none'], [
M('2026-03-03 07:45', PARKING, ME_VT, """
A parking citation has been issued to a vehicle associated with your Virginia Tech account.

Citation number: VT0418827
Issued: 03/02/2026 9:52 PM
Location: Perry Street Lot (Lot 2B), row F
Violation: Parking in a reserved space without a valid permit (24-hour reserved)
Fine: $45.00
Due date: 03/23/2026

You may pay or appeal online through the Parking Portal within 14 calendar days of the issue date. Appeals filed after 03/16/2026 will not be considered.

Virginia Tech Parking and Transportation
"""),
], quote=False),

T('Citation appeal received - VT0418827', ['project_none'], [
M('2026-03-05 23:20', PARKING_APPEALS, ME_VT, """
Your appeal for citation VT0418827 has been received.

Appeal text submitted:
"I parked in row F after 9:30 PM to drop off lab equipment at McBryde. The signs at the row F entrance say reserved 7AM-5PM, and only the sign at the far end says 24-hour. My commuter permit (C-2025-31187) was valid and on the dashboard. Photos of both signs attached."

Appeals are reviewed in the order received, usually within 10 business days. Payment is put on hold while your appeal is under review.

Parking Appeals | Virginia Tech Parking and Transportation
"""),
M('2026-03-19 14:10', PARKING_APPEALS, ME_VT, """
Appeal decision: citation VT0418827

Your appeal has been GRANTED IN PART. The citation is reduced to a written warning ($0.00 due).

Reviewer's note: The signage in row F of Lot 2B is inconsistent and has been referred to Facilities for correction. Please note that row F is reserved 24 hours a day, and future citations in this row will not be reduced.

Parking Appeals | Virginia Tech Parking and Transportation
"""),
], quote=False),

# ------------------------------------------------------------------ library ILL (TutorTrace crunch)
T('Interlibrary Loan article available: TN 1184520', ['project_tutortrace'], [
M('2026-03-26 10:12', ILL, ME_VT, """
Dear David Barron,

The article you requested through Interlibrary Loan is now available electronically.

Transaction number: 1184520
Title: Hint abuse and help avoidance in step-based tutoring: a log-data perspective
Source: Journal article scan, 18 pages
Note from requester: "needed for UIST submission related work, by 3/30 if possible"

Log in to ILLiad to view it: https://vt.illiad.oclc.org/illiad/
The PDF will be available for 30 days and can be viewed up to 5 times.

University Libraries at Virginia Tech | Interlibrary Loan
"""),
], quote=False),

# ------------------------------------------------------------------ leave of absence (Fall 2026)
T('Leave of Absence Request Received - David Barron (Computer Science)', ['project_vt_phd_admin'], [
M('2026-08-03 09:12', GRADSCHOOL, ME_VT, """
Dear David Barron,

The Graduate School has received your Leave of Absence request.

Student: David Barron (ID 9064xxxxx)
Program: Computer Science and Applications, Ph.D.
Leave term(s) requested: Fall 2026
Reason category: Personal / professional (non-medical)
Department approval: Grace Kim, Graduate Program Coordinator, on behalf of the Graduate Program Director (07/31/2026)
Advisor acknowledgement: Yan Chen (07/30/2026)

Your request is now in review by Graduate Enrollment Services. You will receive an email when a decision is made, usually within 5 business days.

While your request is under review, please do not register for Fall 2026 classes.

The Graduate School | Virginia Tech
"""),
], quote=False),

T('Leave of Absence Approved - Fall 2026', ['project_vt_phd_admin'], [
M('2026-08-06 14:40', GRADENROLL, ME_VT, """
Dear David,

Your Leave of Absence for Fall 2026 has been approved. Your approval letter is attached; please keep it for your records.

Key points:
- Your enrollment status for Fall 2026 will show as "Leave of Absence". You will not be registered and will not be charged tuition or fees.
- Time on approved leave does not count toward your time-to-degree limit.
- Your graduate assistantship cannot continue while you are on leave; your department has set your GRA end date to August 15, 2026.
- To return for Spring 2027, submit a Return from Leave request at least 30 days before the first day of classes.

Best regards,
Graduate Enrollment Services
The Graduate School | Virginia Tech
""", att=[A('pdf', 'LOA_Approval_Barron_Fall2026.pdf', [
    ('title', 'Leave of Absence Approval'),
    ('p', 'The Graduate School, Virginia Tech — August 6, 2026'),
    ('p', 'Student: David Barron. Program: Computer Science and Applications, Ph.D. Department: Computer Science.'),
    ('table', [['Item', 'Value'], ['Leave term', 'Fall 2026'], ['Leave type', 'Personal / professional (non-medical)'],
               ['Department approval', '07/31/2026 (G. Kim for the Graduate Program Director)'], ['Advisor', 'Yan Chen'],
               ['Assistantship end date', '08/15/2026'], ['Earliest return term', 'Spring 2027'],
               ['Return request deadline', '30 days before the first day of classes of the return term']]),
    ('p', 'While on leave the student keeps their VT PID and email account, but may not use university facilities as an enrolled student. '
          'Approved leave time is excluded from the time-to-degree calculation.'),
], 'Leave of Absence Approval — David Barron', 'The Graduate School')]),
M('2026-08-06 16:05', ME_VT, GRADENROLL, """
Hello,

Thank you for the quick approval. Two questions:

1. Will I keep access to my vt.edu email and Microsoft 365 during the leave? I have a paper (UIST 2026) in camera-ready and the conference system uses this address.
2. Does the leave affect my ability to be reimbursed for presenting that paper in October, if the department approves travel funding?

Best,
David Barron
"""),
M('2026-08-07 10:20', GRADENROLL, ME_VT, """
Hi David,

1. Yes. Your PID, email and Microsoft 365 account stay active during an approved leave. Accounts are only deactivated if you do not return or request an extension after your leave ends.
2. The Graduate School does not restrict this. Travel reimbursement is handled by your department through Concur, so please confirm eligibility with Grace Kim. Departments usually approve travel to present work done while you were enrolled.

Best regards,
Graduate Enrollment Services
"""),
]),

T('GRA appointment end date: August 15, 2026', ['project_vt_phd_admin'], [
M('2026-08-10 06:30', PAYROLL, ME_VT, """
Dear David Barron,

This is an automated notice that your graduate research assistant (GRA) appointment in the Department of Computer Science will end on 08/15/2026.

Position: Graduate Research Assistant (Org 090xxx, PI: Yan Chen)
Final pay period: 08/01/2026 - 08/15/2026
Final pay date: 09/01/2026 (direct deposit)
Health insurance (Graduate Student Health Plan): coverage through the assistantship ends 08/31/2026. Information about continuing coverage on your own was mailed to your address on file.

Please make sure your mailing address in Hokie Team is current so your 2026 W-2 reaches you.

VT Human Resources - Payroll
"""),
], quote=False),

T('Enrollment status change: Fall 2026', ['project_vt_phd_admin'], [
M('2026-08-12 09:05', REGISTRAR, ME_VT, """
Dear David Barron,

Your enrollment status for Fall 2026 has been updated.

Previous status: Registered (0 credits, pending)
New status: Leave of Absence (Graduate School approved 08/06/2026)
Effective: 08/24/2026 (first day of classes, Fall 2026)

Your Fall 2026 course requests (CS 7994, 9 credits) were removed. Your enrollment verification will show "Leave of Absence" for Fall 2026. If you have student loans, your lender will be notified through the National Student Clearinghouse.

Office of the University Registrar | Virginia Tech
"""),
], quote=False),

T('GSA Travel Fund Program - Fall 2026 cycle now open', ['project_vt_phd_admin'], [
M('2026-09-02 08:00', GSA, ME_VT, """
Hello graduate students,

The Graduate Student Assembly Travel Fund Program is accepting applications for travel between September 1 and December 31, 2026.

- Awards up to $500 for presenting at a conference; up to $300 for attending only.
- Applications must be submitted at least 30 days before travel.
- Applicants must be enrolled full-time in the semester of travel. Students on an approved leave of absence are not eligible.
- Department matching funds are encouraged but not required.

Apply here: https://gsa.vt.edu/travel-fund

Graduate Student Assembly | Virginia Tech
"""),
], quote=False),

T('Planning your return from leave', ['project_vt_phd_admin'], [
M('2026-09-28 07:30', GRADSCHOOL, ME_VT, """
Dear David Barron,

Our records show you are on an approved Leave of Absence for Fall 2026. If you plan to return in Spring 2027:

1. Submit the Return from Leave request in the Graduate School portal by December 13, 2026 (30 days before classes begin on January 12, 2027).
2. Meet with your advisor to update your Plan of Study, if your timeline has changed.
3. Clear any holds on your account before registration opens on November 2, 2026.

If you need to extend your leave into Spring 2027, submit a new Leave of Absence request by the same date. Leaves usually cannot exceed two consecutive semesters without the Dean's approval.

The Graduate School | Virginia Tech
"""),
], quote=False),

# ------------------------------------------------------------------ Concur / UIST travel
T('Travel Request Submitted: UIST 2026 - TutorTrace talk (Request 4KQ7)', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-09-24 17:32', CONCUR, ME_VT, """
Travel Request 4KQ7 has been submitted for approval.

Request name: UIST 2026 - TutorTrace talk
Traveler: David Barron
Purpose: Present accepted paper (session "Learning & Tutoring", talk on 10/07/2026)
Trip dates: 10/05/2026 - 10/08/2026
Departing from: San Francisco, CA (SFO)
Funding source: CS department student travel award + PRIME Lab (PI: Yan Chen)

Estimated expenses
Conference registration (student, early) | $425.00
Airfare (SFO round trip, economy) | $412.60
Lodging (3 nights x $189.00 + tax) | $648.72
Ground transportation | $64.00
Meals & incidentals (per diem) | $236.00
Total estimated | $1,786.32

Next approver: Grace Kim

SAP Concur | Virginia Tech
""", html=True),
], quote=False),

T('Travel Request Approved: UIST 2026 - TutorTrace talk (Request 4KQ7)', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-09-29 11:48', CONCUR, ME_VT, """
Your travel request has been approved.

Request: 4KQ7 - UIST 2026 - TutorTrace talk
Approved by: Grace Kim (09/29/2026 2:46 PM ET)
Approved amount: $1,786.32

Approver comment: "Approved. Dept travel award covers $1,000; remainder charged to PRIME Lab per Dr. Chen's email 9/25. Keep itemized receipts, including registration. You are eligible while on leave since this is presenting work from your enrolled terms."

You can now book travel. After the trip, create an expense report from this request in Concur within 30 days.

SAP Concur | Virginia Tech
""", html=True),
], quote=False),

T('Expense Report Submitted: UIST 2026 - TutorTrace talk', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-10-12 21:14', CONCUR, ME_VT, """
Expense report "UIST 2026 - TutorTrace talk" has been submitted.

Report ID: 8F2C1D9A
Linked travel request: 4KQ7
Report total: $1,486.32
Amount due employee: $1,486.32
Receipts: 6 images, combined into the attached PDF

Expense lines
Registration (student) | $425.00
Airfare SFO round trip | $412.60
Lodging 10/05-10/08 | $508.72
Rideshare (airport-hotel, hotel-airport) | $58.00
Meals & incidentals (3 days, partial per diem for travel days) | $82.00

Next approver: Grace Kim

SAP Concur | Virginia Tech
""", html=True, att=[A('pdf', 'ExpenseReport_8F2C1D9A_receipts.pdf', [
    ('title', 'Expense Report 8F2C1D9A — UIST 2026 - TutorTrace talk'),
    ('p', 'Employee: David Barron (dbarron410). Trip: 10/05/2026 - 10/08/2026. Linked request: 4KQ7.'),
    ('table', [['Date', 'Expense type', 'Vendor', 'Amount', 'Receipt'],
               ['08/27/2026', 'Registration', 'UIST 2026 registration', '$425.00', 'attached (p.2)'],
               ['09/30/2026', 'Airfare', 'Airline, SFO round trip, economy', '$412.60', 'attached (p.2)'],
               ['10/08/2026', 'Lodging', 'Conference hotel, 3 nights @ $148 group rate + tax', '$508.72', 'attached (p.3)'],
               ['10/05/2026', 'Ground transport', 'Rideshare, airport to hotel', '$31.50', 'attached (p.3)'],
               ['10/08/2026', 'Ground transport', 'Rideshare, hotel to airport', '$26.50', 'attached (p.3)'],
               ['10/05-10/08', 'Meals & incidentals', 'Per diem (breakfast/lunch provided by conference deducted)', '$82.00', 'not required'],
               ['', '', 'Total', '$1,486.32', '']]),
    ('p', 'Business purpose: present the accepted UIST 2026 paper (TutorTrace) in the "Learning & Tutoring" session on 10/07/2026.'),
    ('p', 'Note: the lodging total is below the estimate because the conference group rate ($148/night) applied.'),
], 'Expense report 8F2C1D9A', 'SAP Concur')]),
], quote=False),

T('UIST expense report - registration receipt needs the itemized version', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-10-13 08:40', GRACE, ME_VT, """
Hi David,

Congratulations on the talk! I'm reviewing your expense report (8F2C1D9A). Everything looks good except the registration receipt. The one uploaded is the order confirmation page and doesn't show the payment method or the student rate line item. Accounts Payable will send it back without an itemized receipt.

Could you send me the itemized registration receipt (it is usually emailed by the registration system as a PDF)? I'll attach it to the report on my end so you don't have to recall and resubmit.

Thanks,
""" + SIG_GRACE),
M('2026-10-13 10:22', ME_VT, GRACE, """
Hi Grace,

Thanks, and sorry about that. The itemized receipt is attached (paid 08/27 by card ending 4417, student early rate $425.00).

Best,
David
""", att=[A('pdf', 'UIST2026_registration_receipt_itemized.pdf', [
    ('title', 'UIST 2026 — Registration Receipt'),
    ('p', 'Receipt no. R-26-03518 · Issued 08/27/2026'),
    ('p', 'Registrant: David Barron, Virginia Tech (dbarron410@vt.edu) · Presenting author'),
    ('table', [['Item', 'Qty', 'Amount'], ['Student registration, early (ACM/SIGCHI member)', 1, '$425.00'],
               ['Conference reception', 1, '$0.00'], ['Total paid', '', '$425.00']]),
    ('p', 'Payment: Visa ending 4417, authorized 08/27/2026 14:06 PDT.'),
], 'UIST 2026 registration receipt', 'Conference registration system')]),
M('2026-10-13 15:55', GRACE, ME_VT, """
Perfect, attached and approved. It's with Accounts Payable now. Reimbursements usually go out in 3-5 business days by direct deposit.

""" + SIG_GRACE),
]),

T('Payment Notification: Expense Report 8F2C1D9A', ['project_vt_phd_admin', 'project_tutortrace'], [
M('2026-10-16 09:02', CONCUR, ME_VT, """
A payment has been issued for your expense report.

Report: UIST 2026 - TutorTrace talk (8F2C1D9A)
Amount paid: $1,486.32
Payment method: Direct deposit to the account on file (ending 0932)
Payment date: 10/16/2026
Funding split: CS department student travel award $1,000.00; PRIME Lab $486.32

SAP Concur | Virginia Tech
""", html=True),
], quote=False),

]
