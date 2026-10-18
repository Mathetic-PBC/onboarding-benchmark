"""davidbarron410@gmail.com — personal Gmail; synthetic threads are mostly Mathetic / Engelbart / Berkeley (Aug–Oct 2026).
Date strings are David's local time (ET until 2026-08-08 12:00, PT after)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _dsl import *

SHARED = os.path.join(os.path.dirname(__file__), '..', '..', 'shared')
OSTROWSKI_CR = os.path.abspath(os.path.join(SHARED, 'Ostrowski2025_LAS_camera_ready.pdf'))

GCAL = P('Google Calendar', 'calendar-notification@google.com')
GFORMS = P('Google Forms', 'forms-receipts-noreply@google.com')
GDRIVE = P('Google One', 'googleone-noreply@google.com')
AGENT = P('Harbor Registered Agents', 'compliance@harborregisteredagents.com')
BANK = P('Mercury', 'hello@mercury.com')
MONITOR = P('Best Buy', 'BestBuyInfo@emailinfo.bestbuy.com')
ZOOM = P('Zoom', 'no-reply@zoom.us')

ONE_PAGER = [
    ('title', 'Engelbart — a research notebook that remembers where your thoughts came from'),
    ('p', 'Mathetic PBC · David Barron & Hudson Mitchell-Pullman · August 2026'),
    ('h2', 'Problem'),
    ('p', 'Researchers think across a dozen tools: chats with Claude and ChatGPT, PDFs in Zotero and Downloads, notes in Notion or '
          'Obsidian, email, Slack. When they write, the trail of where an idea came from is gone. Re-finding it costs hours a week.'),
    ('h2', 'Product'),
    ('p', 'Engelbart imports a researcher\'s existing context once (chats, papers, notes, mail, drive), dedupes it, and builds a '
          'canvas where every claim links back to the conversation, page or paper it came from.'),
    ('h2', 'Early signal'),
    ('bullet', '6 Berkeley research chats planned for September (education, HCI, statistics).'),
    ('bullet', 'Two pilot users lined up for October onboarding sessions.'),
    ('bullet', 'Both founders are researchers (VT HCI PhD, PRIME Lab); first user is ourselves.'),
    ('h2', 'Who pays'),
    ('p', 'Individual PhD students and postdocs first ($15/month), then lab and department licenses where advisors want shared '
          'provenance across students. We are testing willingness to pay in the October pilots.'),
    ('h2', 'Ask'),
    ('p', 'Raising a pre-seed on a post-money SAFE. Looking for angels who have backed research or developer tools.'),
]

LANDING_V3 = [
    ('title', 'Engelbart landing page — copy v3'),
    ('p', 'Hudson, 26 Aug 2026. Changes from v2 marked [new].'),
    ('h2', 'Hero'),
    ('p', 'Headline: Your research, with its receipts.'),
    ('p', 'Sub: Engelbart brings your chats, papers and notes into one notebook and shows where every idea came from. [new]'),
    ('p', 'CTA: Join the pilot  ·  secondary: See how import works'),
    ('h2', 'Three panels'),
    ('number', 'Import once. Claude, ChatGPT, Zotero, Notion, Obsidian, Gmail, Drive. We dedupe the same PDF across tools. [new]'),
    ('number', 'Trace any thought. Click a sentence, see the chat turn or page it came from.'),
    ('number', 'Write with context. Draft a related-work section with sources already attached.'),
    ('h2', 'Open questions for David'),
    ('bullet', 'Do we promise Granola / Notion import on the page if neither connector is done yet?'),
    ('bullet', 'Is "receipts" too cute? Alternative: "Your research, with its sources".'),
    ('bullet', 'Need one real screenshot of the trail view, not the Figma mock.'),
]

THREADS = [
# ---------------- early-2026 cross-overs ----------------
T('papert lab notebook - first pass', ['project_engelbart', 'project_mathetic_company'], [
M('2026-02-02 23:41', ME_G, HUDSON, """
ok so I put the "Papert Lab notebook" idea into a notion page (sharing it with you now, check the teamspace). rough version:

- one place that holds your chats + papers + notes
- every paragraph you write keeps a link to where it came from
- named after Papert for now bc the whole thing is about learning by building, but not attached to the name

i wrote the first page last wednesday night and it's messy. the part i care about is the provenance thing, the rest is just furniture. can you read it before thursday and tell me if it's a product or a feature
"""),
M('2026-02-03 09:15', HUDSON, ME_G, """
Read it. It's a product if the import is good. If the import is bad it's a feature of some other notes app.

Two things I'd push on:
1. "where it came from" needs to work on day one, which means we're importing a year of someone's mess, not a clean folder.
2. The name. Papert Lab sounds like a research group. Fine for now.

Thursday works. I'll bring the three tools I actually use and we can try to trace one idea by hand.

Hudson
"""),
M('2026-02-03 10:02', ME_G, HUDSON, """
"import a year of someone's mess" is the whole company lol. ok thursday
"""),
]),

T('talked to yan about the leave', ['project_mathetic_company', 'project_vt_phd_admin'], [
M('2026-06-22 21:30', ME_G, HUDSON, """
quick update since you asked: had the 1:1 with yan this afternoon.

- she's supportive of a leave starting fall, as long as the uist camera-ready and the neurips rebuttal are handled before i go
- leave form goes through grace kim in the grad office, needs to be signed by end of july
- gra funding ends aug 15, so i'm on my own after that
- she asked that i still give the uist talk in october (obviously yes)

so: realistic SF date is early august. i'm going to start looking at sublets this week
"""),
M('2026-06-23 08:47', HUDSON, ME_G, """
This is great news. Early August works. I'll ask Lena whether the Surplus house has a room opening up then, it would save you the sublet hunt.

Hudson
"""),
]),

T("Surplus Fall cohort — you're in", ['project_mathetic_company'], [
M('2026-07-08 14:05', LENA, [ME_G, HUDSON], """
Hi David and Hudson,

Congratulations: Mathetic is in the Surplus Fall 2026 cohort. Eleven teams this round.

What it includes:
- desk space at the house on weekdays, plus a room for David from August 8 (month to month; the room on the second floor that faces the yard)
- weekly office hours with me, Tuesday afternoons
- demo night in late September, and an investor day in November
- no equity taken; we ask for a short monthly update

Kickoff is Tuesday, August 11 at 10:00. Details to follow closer to the date.

Welcome,
Lena Hoffmann
Program Lead, Surplus
"""),
M('2026-07-08 15:20', ME_G, [LENA, HUDSON], """
Hi Lena,

Thank you, this is great news. Yes to the room from August 8. I'll fly in that morning and should be at the house by early afternoon.

One question: is there a monitor or desk setup in the room, or should I ship mine?

Best,
David
"""),
M('2026-07-09 10:12', LENA, [ME_G, HUDSON], """
Desk and chair are in the room. No monitor; there's a shared pile of 27-inch monitors in the garage that people borrow, first come first served. I'd skip shipping yours.

Lena
"""),
]),

T('mercury account - need your ID verification', ['project_mathetic_company'], [
M('2026-08-05 11:16', HUDSON, ME_G, """
Hi David,

I opened the Mercury account for Mathetic PBC. It's stuck on "pending additional owner" until you verify. You should have an email from them; it takes a photo of your license and a selfie.

Also: I put both of us as signers. Card limits are $2,000/month each for now.

Hudson
"""),
M('2026-08-05 13:40', ME_G, HUDSON, """
done, verified from my phone. it says 1-2 business days. will forward the confirmation when it lands
"""),
]),

T('Action needed: verify your identity for Mathetic PBC', ['project_mathetic_company'], [
M('2026-08-05 12:02', BANK, ME_G, """
Hi David,

Hudson Mitchell-Pullman added you as an owner of Mathetic PBC's Mercury account.

To finish opening the account, please verify your identity. It takes about 3 minutes:
1. Photo of a government-issued ID
2. A selfie to match the ID
3. Confirm your home address

Status: Pending additional owner verification
Application reference: MRC-APP-48217

The Mercury team
""", html=True),
M('2026-08-07 09:31', BANK, ME_G, """
Hi David,

You're verified. Mathetic PBC's checking account is now open and both owners can sign in.

Account: Mathetic PBC Checking ••6620
Debit card: on its way to the business address on file (5-7 business days)

The Mercury team
""", html=True),
], quote=False, labels=['Inbox', 'Category Updates']),

T('Kickoff agenda — Tue Aug 11', ['project_mathetic_company'], [
M('2026-08-09 17:44', LENA, [ME_G, HUDSON], """
Hi all,

Agenda for Tuesday's kickoff (calendar invite attached):

10:00  coffee + intros (60 seconds per team: what you're building, who it's for, what you need)
10:45  how Surplus works: office hours, monthly updates, demo night Sep 24, investor day Nov 12
11:30  founder panel: "what we'd do differently in our first 90 days"
12:30  lunch on the back deck

Please bring one sentence on your biggest risk for the next 90 days. We'll put them on the wall and revisit at demo night.

Lena
""", att=[A('ics', 'invite.ics', dict(summary='Surplus Fall 2026 kickoff', start='2026-08-11 10:00', end='2026-08-11 13:30',
                                      location='Surplus house, main room', organizer=LENA, attendees=[ME_G, HUDSON],
                                      description='Intros, how Surplus works, founder panel, lunch. Bring your biggest 90-day risk.'))]),
M('2026-08-09 21:03', ME_G, [LENA, HUDSON], """
Thanks Lena. Our 90-day risk: people try Engelbart, the import misses half of what they have, and they never come back. We're going to run two pilot onboardings in October to find out.

See you Tuesday (I'm already upstairs).
David
"""),
]),

T('house wifi + groceries', ['project_none'], [
M('2026-08-12 19:20', SAM, ME_G, """
hey welcome to the house! couple of logistics:

- wifi is "surplus-house-5G", password is on the fridge
- we split groceries for shared stuff (coffee, oat milk, eggs, bread) on a shared Splitwise, I'll add you. usually ~$25/week each
- trash goes out Sunday night, recycling is the blue bin

also there's a Saturday morning run group that goes to the Presidio, very slow pace, you'd probably find it boring lol

Sam
"""),
M('2026-08-12 21:05', ME_G, SAM, """
thanks sam! added myself on splitwise. slow pace is actually perfect, i'm doing zone 2 base stuff so i'll come saturday
"""),
]),

T('Order confirmation #BBY01-806614523', ['project_none'], [
M('2026-08-10 13:12', MONITOR, ME_G, """
Thanks for your order, David.

Order number: BBY01-806614523
Order date: Aug 10, 2026

Item | Qty | Price
USB-C to HDMI adapter, 4K60 | 1 | $24.99
Laptop stand, aluminum | 1 | $39.99
Subtotal | | $64.98
Tax | | $5.69
Total | | $70.67

Pickup: Store pickup, ready in about 1 hour. Bring a photo ID.
""", html=True),
], quote=False, labels=['Category Promotions']),

T('Intro: Marcus Oyelaran (Northfield Angels) <> Mathetic', ['project_mathetic_company'], [
M('2026-08-13 10:31', LENA, [MARCUS, ME_G], """
Marcus, David,

Connecting you two. Marcus is with Northfield Angels and has backed a few research and developer tools (he asked me for founders working on "tools for thinking", and Mathetic came to mind immediately). David and his co-founder Hudson are building Engelbart, a research notebook that keeps track of where ideas come from. David is on leave from a PhD at Virginia Tech.

I'll let you take it from here.

Lena
""", cc=[HUDSON]),
M('2026-08-13 12:47', MARCUS, [ME_G], """
Thanks Lena (to bcc).

David, glad to meet. I'd love 30 minutes. I'm free Thursday 8/20 between 2 and 5 Pacific, or the following Monday morning. Zoom or I can come by the Surplus house.

Marcus
""", cc=[HUDSON]),
M('2026-08-13 14:10', ME_G, [MARCUS], """
Hi Marcus,

Thanks for making time. Thursday 8/20 at 3:00 PT works for us. Happy to host at the Surplus house; I'll send an invite with the address. Hudson will join.

Best,
David
""", cc=[HUDSON]),
]),

T('Following up from today — Engelbart one-pager', ['project_mathetic_company', 'project_engelbart'], [
M('2026-08-20 18:22', ME_G, MARCUS, """
Hi Marcus,

Thanks again for coming by today. The one-pager is attached.

On the two questions you asked:

Retention. We don't have retention numbers yet, and I don't want to make one up. What we'll have by mid-October: two pilot users onboarded with their real data (one Berkeley PhD student, one CMU postdoc), and whether they open Engelbart in week 2 without us nudging them. That's the number we're watching.

Who pays. Individual researchers first, at about $15/month. The bigger bet is lab licenses, because the person who most wants provenance across a lab is the advisor, not the student. We'll ask both pilot users what they'd pay and who would approve it.

I'll send a short update after the pilots.

Best,
David
""", cc=[HUDSON], att=[A('pdf', 'Engelbart_one_pager_Aug2026.pdf', ONE_PAGER, 'Engelbart one-pager')]),
M('2026-08-22 08:05', MARCUS, ME_G, """
David, thanks. This is clear and I appreciate you not making up a retention number. The advisor-pays angle is interesting; I'd want to hear from two advisors who say yes.

Let's talk again after your pilots. Mid-October is good.

Marcus
""", cc=[HUDSON]),
]),

T('notes from marcus + deck changes', ['project_mathetic_company'], [
M('2026-08-20 20:41', HUDSON, ME_G, """
My notes from Marcus, before I forget:

- He liked the provenance demo (the click-a-sentence part), less interested in the canvas
- Pushed twice on retention. We had nothing. Fair.
- "Who pays" — he doesn't believe students pay. Advisors maybe.
- Typical check $25-50k, wants to see usage before committing
- Said he'd talk again in October

Deck changes I'd make:
1. Move the trail demo to slide 2
2. Kill the "market size" slide, it's made up anyway
3. Add a "what we'll know by Oct 15" slide: pilots, week-2 opens, willingness to pay
"""),
M('2026-08-20 22:58', ME_G, HUDSON, """
agree on all 3. also want a slide on why import is hard (the same paper shows up in zotero + downloads + an email attachment, chats split across 3 accounts). that's our moat if we get it right

i'll do the deck tomorrow, you do the landing page?
"""),
M('2026-08-21 07:30', HUDSON, ME_G, """
Deal. Landing copy v3 by Wednesday.
"""),
]),

T('landing page copy v3', ['project_engelbart', 'project_mathetic_company'], [
M('2026-08-26 16:48', HUDSON, ME_G, """
v3 attached. Main change is the import panel now explicitly says we dedupe the same PDF across tools — that's straight from your moat slide.

Three open questions at the bottom of the doc. The Granola/Notion one matters most: I don't want to promise connectors we haven't built.
""", att=[A('docx', 'Engelbart_landing_copy_v3.docx', LANDING_V3, 'Engelbart landing page copy v3', 'Hudson Mitchell-Pullman')]),
M('2026-08-26 22:15', ME_G, HUDSON, """
read it. answers:
1. don't promise granola/notion yet. say "more connectors coming" and list only what works today
2. "receipts" is good, keep it
3. i'll grab a real screenshot of the trail view tomorrow once the canvas stops flickering

ship it after that
"""),
]),

T('berkeley research chats - sign-up page', ['project_berkeley_research_chats'], [
M('2026-08-28 15:02', ME_G, HUDSON, """
the berkeley research site is up. the sign-up form asks:
- field + year
- which tools you use to think (checkboxes)
- one sentence: "the last time you couldn't find where an idea came from"
- availability sep 8-18

i'm going to email 3 people directly (a learning sciences phd student, priya raman from the ed+hci group, and a stats postdoc) and let the form catch the rest. goal is 6 chats, 30 min each, no pitch, just how they work
"""),
M('2026-08-28 17:30', HUDSON, ME_G, """
Love the "last time you couldn't find where an idea came from" question. Please record (with consent) so I can listen later.
"""),
]),

T('Quick research chat? (how you keep track of ideas)', ['project_berkeley_research_chats'], [
M('2026-09-01 10:14', ME_G, ELENA, """
Hi Elena,

I'm David Barron, an HCI PhD student at Virginia Tech (currently on leave and working in San Francisco). I'm doing a handful of 30-minute research chats with Berkeley grad students about how they keep track of ideas across papers, notes and AI chats. Your work on how students revise explanations came up when I asked around the learning-sciences group.

No pitch and nothing to prepare. Would any 30 minutes on Sep 9 or 10 work? Zoom or in person on campus, whichever you prefer.

Thanks,
David
"""),
M('2026-09-02 13:40', ELENA, ME_G, """
Hi David,

Happy to. Wednesday Sep 9 at 11 works, in person is nicer. I'm usually at the Berkeley School of Education building; there's a quiet table on the second floor.

Fair warning, my system is mostly a paper notebook and a very long Google Doc.

Elena
"""),
M('2026-09-02 15:05', ME_G, ELENA, """
Perfect, Sep 9 at 11 at the second-floor table. A paper notebook and a very long Google Doc is exactly the kind of thing I want to hear about.

David
"""),
]),

T('research chat - Sep 10?', ['project_berkeley_research_chats'], [
M('2026-09-02 10:48', ME_G, PRIYA, """
Hi Priya,

I'm David Barron (HCI PhD at Virginia Tech, on leave and building a research tool in SF). I'm talking to a few Berkeley researchers about how they keep track of where ideas come from across papers, notes and AI chats. Your work at the intersection of education and HCI is close to my own (help-seeking telemetry in CS1), so I'd love to hear how you work.

30 minutes, no pitch. Would Thursday Sep 10 work?

Best,
David
"""),
M('2026-09-03 09:22', PRIYA, ME_G, """
Hi David,

Sure! Sep 10 at 2pm on Zoom works best for me. And I've seen your VizPI work, so I'm curious what you're building.

Warning: I have something like four Zotero libraries and I use Claude for basically everything now.

Priya
"""),
M('2026-09-03 10:01', ME_G, PRIYA, """
Four Zotero libraries and heavy Claude use is my ideal interviewee, honestly. Sending a Zoom link for Sep 10, 2:00 PT.

David
"""),
]),

T('New response: Berkeley research chats sign-up', ['project_berkeley_research_chats'], [
M('2026-09-04 08:36', GFORMS, ME_G, """
Berkeley research chats — sign-up has a new response.

Field and year: Statistics, postdoc (2nd year)
Tools: Overleaf, Zotero, ChatGPT, Obsidian, R notebooks
The last time you couldn't find where an idea came from: "I had a variance-reduction trick in a ChatGPT chat from March and I re-derived it from scratch in July because I couldn't find it."
Availability: Sep 15, 16 (afternoons)
Name: Ben Adeyemi

View all responses in Google Forms.
""", html=True),
], quote=False, labels=['Inbox', 'Category Updates']),

T('Berkeley research chat — Sep 16 on Zoom', ['project_berkeley_research_chats'], [
M('2026-09-08 11:20', ME_G, BEN, """
Hi Ben,

Thanks for signing up for a research chat. Your example (re-deriving the variance-reduction trick because the March chat was lost) is exactly what I want to understand.

Would Wednesday Sep 16 at 2:30 PT work? Zoom, 30 minutes. With your OK I'd like to record so my co-founder can listen later; I'll delete the recording after we take notes.

David
"""),
M('2026-09-08 16:54', BEN, ME_G, """
Sep 16 at 2:30 is fine. Recording is fine too. I'll try to find the chat before then so I can show you how bad it is.

Ben
"""),
M('2026-09-08 17:10', ME_G, BEN, """
Great. Zoom link: Meeting ID 812 4471 9036, passcode berk16. See you Wednesday.

David
"""),
]),

T('the paper I mentioned (Ostrowski et al., L@S 25)', ['project_berkeley_research_chats', 'project_tutortrace'], [
M('2026-09-10 17:52', PRIYA, ME_G, """
Hi David,

Thanks for the chat today, that was fun. Here is the paper I mentioned, the camera-ready from L@S. The bit you'll like is Section 4: repeated near-identical prompts are the strongest predictor of stalling, and they report the leakage drop (0.71 -> 0.58 macro-F1) instead of hiding it.

Also, I'm in for trying Engelbart when it's ready. My Zotero situation needs help.

Priya
""", att=[A('file', 'Ostrowski2025_LAS_camera_ready.pdf', OSTROWSKI_CR, 'application/pdf')]),
M('2026-09-10 21:15', ME_G, PRIYA, """
Thanks Priya! This is very close to TutorTrace. We cited the arXiv version in the UIST paper, but I hadn't seen that the camera-ready reports the leakage number; I'll update the reference before the talk.

And yes, I'd love to have you as a pilot user. I'll reach out in a couple of weeks with a time for an onboarding session (about an hour, with your real data).

David
"""),
], notes='HARD CASE: same paper in several places — Priya sends Ostrowski2025_LAS_camera_ready.pdf as an attachment (same bytes as the zotero/pdfs copies); also an email with attachments'),

T('research chats: notes so far', ['project_berkeley_research_chats', 'project_engelbart'], [
M('2026-09-17 22:40', ME_G, HUDSON, """
three chats done (elena 9/9, priya 9/10, ben 9/16). quick synthesis, longer notes in granola:

- all three lose ideas in AI chats. ben re-derived a whole trick. priya has claude chats across 2 accounts
- nobody trusts automatic tagging. they want to see the source, not a summary of it
- elena's system is a paper notebook + one 80-page google doc. she would not import the notebook, but the doc yes
- priya: same paper lives in 3 places (zotero, downloads, an email from her advisor). she said "i don't even know which one has my highlights"

implication for import: dedupe papers across tools before anything else, and show the source chat turn, not a summary
"""),
M('2026-09-18 08:12', HUDSON, ME_G, """
"show the source, not a summary" should go on the landing page. Agree on dedupe-first.
"""),
]),

T('Engelbart waitlist — 212', ['project_engelbart'], [
M('2026-09-21 09:05', HUDSON, ME_G, """
Waitlist is at 212 as of this morning. Breakdown from the "what do you do" field:

PhD students 131
Postdocs 29
Faculty 18
Industry researchers 22
Other 12

Most came from the Berkeley research page and one HN comment. I'd invite 10 after the pilots, not before.
"""),
M('2026-09-21 10:30', ME_G, HUDSON, """
agreed, after the pilots. faculty 18 is more than i expected, that's the "advisor pays" crowd marcus wanted to hear from
"""),
]),

T('Mathetic PBC — Delaware annual report and franchise tax due March 1, 2027', ['project_mathetic_company'], [
M('2026-09-01 07:00', AGENT, ME_G, """
Mathetic PBC (Delaware File No. 7731904)

This is a courtesy reminder from your registered agent.

Delaware corporations must file an Annual Franchise Tax Report and pay franchise tax by March 1, 2027.

- Public benefit corporations must include the biennial statement on the public benefit in their report.
- The minimum tax under the Assumed Par Value Capital Method is $400; the filing fee is $50.
- Late filings incur a $200 penalty plus interest of 1.5% per month.

You can file through the Delaware Division of Corporations website or ask us to file on your behalf.

Harbor Registered Agents, Compliance Team
""", html=True),
M('2026-09-01 09:48', ME_G, HUDSON, """
fyi. put "Delaware annual report + PBC statement, due Mar 1" on the shared calendar for mid-Feb. and remind me to use the assumed par value method, the default calc gives an absurd number
""", subject='Fwd: Mathetic PBC — Delaware annual report and franchise tax due March 1, 2027', quote=True),
M('2026-09-01 10:20', HUDSON, ME_G, """
On the calendar for Feb 15. Noted on the par value method.
""", subject='Re: Fwd: Mathetic PBC — Delaware annual report and franchise tax due March 1, 2027'),
], labels=['Inbox']),

T('Demo night Sep 24 — sign-ups', ['project_mathetic_company', 'project_engelbart'], [
M('2026-09-14 12:10', LENA, [ME_G, HUDSON], """
Hi teams,

Demo night is Thursday Sep 24, 6:30pm at the house. Five minutes per team, live demo strongly preferred over slides. Reply by Friday if you want a slot. About 40 guests, mostly founders and a handful of angels.

Lena
"""),
M('2026-09-14 13:55', ME_G, [LENA, HUDSON], """
Hi Lena, Mathetic would like a slot. Live demo: import a real researcher's folder (mine), then click from a sentence in a draft back to the Claude chat it came from. Hudson will present, I'll drive.

David
"""),
M('2026-09-14 14:20', LENA, [ME_G, HUDSON], """
You're slot 4 of 9. Test on the projector Wednesday; the HDMI on the left wall is the one that works.
"""),
]),

T('Your Google storage is almost full', ['project_none'], [
M('2026-09-18 06:12', GDRIVE, ME_G, """
You've used 14.2 GB of your 15 GB of storage.

When you run out of space, you won't be able to upload new files to Drive, back up photos, or send and receive email in Gmail.

Biggest items:
- Gmail: 9.8 GB
- Drive: 3.9 GB
- Photos: 0.5 GB

Get 100 GB for $1.99/month, or free up space.
""", html=True),
], quote=False, labels=['Inbox', 'Category Updates']),

T('Engelbart pilot onboarding — times?', ['project_engelbart'], [
M('2026-09-29 11:04', ME_G, PRIYA, """
Hi Priya,

The pilot is ready for real data. The onboarding session is about an hour: you connect your accounts (Claude, Zotero, Drive, whatever you use), we watch the import together, and then you try to trace one idea from a draft back to its source. I'll take notes on everything that's confusing.

Would Friday Oct 9 work, any time after 1? I'll be giving a talk on the 7th so earlier that week is hard.

David
""", cc=[HUDSON]),
M('2026-09-30 08:30', PRIYA, ME_G, """
Oct 9 at 2pm works. Should I clean up my Zotero first? (Please say no.)

Priya
""", cc=[HUDSON]),
M('2026-09-30 09:12', ME_G, PRIYA, """
Please don't clean anything up! The mess is what we need to see. Invite coming from my calendar.

David
""", cc=[HUDSON]),
]),

T('Invitation: Engelbart pilot onboarding — Priya Raman @ Fri Oct 9, 2026 2pm - 3:15pm (PDT)', ['project_engelbart'], [
M('2026-09-30 09:15', ME_G, [PRIYA, HUDSON], """
David Barron has invited you to this event.

Engelbart pilot onboarding — Priya Raman
When: Friday Oct 9, 2026 2pm – 3:15pm (Pacific Time - Los Angeles)
Where: Zoom (link in description)
Who: David Barron (organizer), Priya Raman, Hudson Mitchell-Pullman

Agenda: connect accounts, watch the import, trace one idea back to its source, 10 min of questions about pricing.

Going? Yes - Maybe - No
""", att=[A('ics', 'invite.ics', dict(summary='Engelbart pilot onboarding — Priya Raman', start='2026-10-09 14:00', end='2026-10-09 15:15',
                                      location='Zoom', organizer=ME_G, attendees=[PRIYA, HUDSON],
                                      description='Connect accounts, watch the import, trace one idea back to its source, pricing questions.'))]),
], quote=False, labels=['Sent'], notes='HARD CASE: email with attachments — calendar invite (.ics) sent from David\'s calendar for the 10-09 pilot'),

T('intro: Daniel Osei (CMU) <> David', ['project_engelbart'], [
M('2026-10-03 10:40', PRIYA, [ME_G, DANIEL], """
Hi both,

Daniel is a postdoc at CMU working on learning analytics; he complained to me last week that he can't find anything he's discussed with ChatGPT. David is building Engelbart, the tool I'm piloting next week. I think Daniel would be a great second pilot.

Priya
"""),
M('2026-10-03 14:22', DANIEL, ME_G, """
Thanks Priya. David, happy to try it. I'm in Pittsburgh so it'd be remote. Tuesday Oct 13 would be best, morning Eastern if possible.

Daniel
""", cc=[PRIYA]),
M('2026-10-03 15:01', ME_G, DANIEL, """
Hi Daniel, thanks for being up for it. Tuesday Oct 13 at 10:00 Eastern (7:00 PT for me, coffee will be involved) works. It's about an hour on Zoom: connect your accounts, watch the import, and try to trace one idea back to where it came from. Invite on its way.

David
""", cc=[PRIYA]),
]),

T('UIST talk — can I watch?', ['project_tutortrace'], [
M('2026-10-05 18:20', HUDSON, ME_G, """
Is your UIST talk on Wednesday streamed anywhere? I'd like to watch, and honestly it's good material for the "founders are researchers" slide.
"""),
M('2026-10-05 19:02', ME_G, HUDSON, """
should be streamed for registered attendees, recorded videos go up a few weeks later. i'm in the "Learning & Tutoring" session, 15 min + 5 Q&A. practice run tomorrow night in the main room if you want the live version
"""),
]),

T('Marcus — time for a second conversation?', ['project_mathetic_company'], [
M('2026-10-06 09:30', ME_G, MARCUS, """
Hi Marcus,

As promised in August, a short update and a request.

- We're running two pilot onboardings this week and next (a Berkeley PhD student on Oct 9, a CMU postdoc on Oct 13), with their real data.
- Waitlist is at 212, including 18 faculty.
- I'm giving the UIST talk on our earlier research (TutorTrace) on Oct 7.

Could we talk on Wednesday Oct 14? By then we'll have both pilots done and I can show you what broke.

Best,
David
""", cc=[HUDSON]),
M('2026-10-06 13:15', MARCUS, ME_G, """
Yes. Oct 14 at 4pm PT, I'll come to the house again.

Marcus
""", cc=[HUDSON]),
]),

T('Pilot recap — Oct 9 session', ['project_engelbart'], [
M('2026-10-09 18:45', ME_G, [PRIYA, HUDSON], """
Hi Priya,

Thank you for today, and for being patient with the import. Recap of what we saw, so you can correct me:

What broke
1. Claude import missed about 140 of your chats. We think it only pulled chats inside Projects and skipped the ones in your main list; we're checking that first.
2. Duplicate PDFs: the same paper showed up twice, once from Zotero and once from Downloads (the Ostrowski L@S paper was one of them). Engelbart treated them as two sources, so the trail view split.
3. The connect screen didn't say what "Drive" would import (Docs only? PDFs too?).

What worked
- You liked the "where did this thought come from" trail: clicking a sentence in your draft and landing on the Claude turn from March.
- Search across Zotero notes and chats in one box.

Pricing: you said $10-15/month is plausible personally, and that your lab would pay if your advisor saw the trail across students.

Next: we fix the Claude import and the PDF dedupe this week, and I'll ask you to re-import on the 16th.

Thanks again,
David
"""),
M('2026-10-10 10:02', PRIYA, [ME_G, HUDSON], """
This is accurate. Two additions:

- The ~140 missing chats are probably the ones from my old account; I switched accounts in March. So it might be two problems.
- On the duplicates: the copy in Downloads is the one with my highlights. If you merge them, please keep the highlights.

Happy to re-import on the 16th.

Priya
"""),
], notes='Pilot recap: import missed ~140 Claude chats, duplicate PDFs (same paper from Zotero and Downloads)'),

T('priya import misses - root cause', ['project_engelbart'], [
M('2026-10-12 00:35', ME_G, HUDSON, """
ok found it. two bugs, priya was right that it's two problems:

1. claude connector only paginates project conversations; the main list stopped at the first page (50). that's ~90 of the 140
2. the rest are from her old account, which we never asked for. the connect screen needs "add another account" per source

pdf dedupe: hashing exact bytes doesn't work, the zotero copy and the downloads copy differ (annotations). switching to doi + title match, keep the annotated copy as primary

pushing fixes tomorrow before daniel's session
"""),
M('2026-10-12 08:20', HUDSON, ME_G, """
Nice. "Add another account" is a connect-screen change, I can sketch it today.
"""),
]),

T('Follow-up from this morning — Engelbart pilot', ['project_engelbart'], [
M('2026-10-13 11:40', ME_G, DANIEL, """
Hi Daniel,

Thanks for this morning. Notes from the session:

- You wanted Notion and Granola import; neither exists yet. Notion is next on our list; Granola I hadn't considered until you mentioned your meeting notes live there.
- The connect screen's "Other" category confused you (fair: it mixed Overleaf, local folders and Slack). We'll split it.
- Your ChatGPT import worked: 412 conversations, and you found the April thread on mixed-effects models in under a minute.

Would you be up for a 15-minute check-in on Oct 27 to see if you're still opening it?

David
""", cc=[PRIYA]),
M('2026-10-13 15:08', DANIEL, ME_G, """
Yes to Oct 27. And yes, please do Notion first, half my lab lives there.

Daniel
"""),
]),

T('Following up — pilots and next steps', ['project_mathetic_company'], [
M('2026-10-14 19:10', ME_G, MARCUS, """
Hi Marcus,

Thanks for today. Summary of what we showed and what you asked for:

- Pilot 1 (Oct 9): import missed ~140 chats and duplicated PDFs; both root-caused and fixed by Oct 12. She re-imports Oct 16.
- Pilot 2 (Oct 13): ChatGPT import worked (412 conversations); wants Notion and Granola import.
- You said you'd be interested in a $50k check into the pre-seed SAFE if the pilots convert. We'll define "convert" as both pilot users opening Engelbart in week 2 without a nudge, and one of them getting a second person in their lab onto it.

I'll send the week-2 numbers by Oct 30.

Best,
David
""", cc=[HUDSON]),
M('2026-10-15 07:55', MARCUS, ME_G, """
That definition of "convert" works for me. Send the numbers when you have them and I'll move quickly.

Marcus
""", cc=[HUDSON]),
]),

T('data room checklist', ['project_mathetic_company'], [
M('2026-10-15 21:20', HUDSON, ME_G, """
If Marcus moves quickly we need a data room ready. Checklist attached; I filled in what I know. Your column is mostly the product/pilot stuff.
""", att=[A('xlsx', 'Mathetic_data_room_checklist.xlsx', {
    'Checklist': [['Item', 'Owner', 'Status', 'Notes'],
                  ['Certificate of incorporation (DE PBC)', 'Hudson', 'done', 'PDF in Drive / Legal'],
                  ['Bylaws + board consent', 'Hudson', 'done', ''],
                  ['Founder stock purchase agreements', 'Hudson', 'done', ''],
                  ['Cap table (current)', 'Hudson', 'in progress', 'update after SAFE terms'],
                  ['Post-money SAFE (template)', 'Hudson', 'in progress', 'cap TBD with Marcus'],
                  ['Pilot notes (Priya, Daniel)', 'David', 'todo', 'anonymize before sharing'],
                  ['Week-2 usage numbers', 'David', 'todo', 'due Oct 30'],
                  ['Product demo video (2 min)', 'David', 'todo', 'record after import fix'],
                  ['Delaware annual report reminder', 'Hudson', 'calendar', 'due 2027-03-01']],
    'Contacts': [['Name', 'Role', 'Last contact'],
                 ['Marcus Oyelaran', 'Northfield Angels', '2026-10-14'],
                 ['Lena Hoffmann', 'Surplus', '2026-10-13']],
}, 'Mathetic data room checklist', 'Hudson Mitchell-Pullman')]),
M('2026-10-15 23:05', ME_G, HUDSON, """
ran a half marathon this morning so my brain is soup, but i'll fill my column tomorrow. pilot notes will need priya and daniel's ok before they go in
"""),
]),

T('connect screen: "add another account" sketch', ['project_engelbart'], [
M('2026-10-16 14:30', HUDSON, ME_G, """
Sketch attached: each source gets its own row, with accounts listed under it and an "add another account" link. "Other" is gone; Overleaf, local folders and Slack each get a row. I also added a count per source after import so people notice when something is missing (the 140-chats problem).
""", att=[A('png', 'connect_screen_counts.png', dict(title='Mock: items found per source after import (Priya re-import, est.)',
                                                       labels=['Claude', 'ChatGPT', 'Zotero', 'Drive', 'Gmail', 'Notion'],
                                                       values=[318, 96, 1240, 210, 85, 0], color='#3b5bdb'))]),
M('2026-10-16 18:02', ME_G, HUDSON, """
yes. the per-source count is the most important thing on this screen, it's how priya would have caught the missing chats herself. one change: show "0" sources in grey with "not connected" instead of hiding them
"""),
]),

T('your new address?', ['project_none'], [
M('2026-08-17 13:05', NIAMH, ME_G, """
Hi David,

Hope the move went well! Mam says you're in San Francisco now. Can you send me your new address? We're posting out the wedding photo books and I don't want yours going to Blacksburg.

Also thanks again for coming over in July, it meant a lot.

Niamh x
"""),
M('2026-08-17 16:40', ME_G, NIAMH, """
Hi Niamh! Move went fine, I'm living in a shared house that's also a startup office, which is exactly as chaotic as it sounds. I'll text you the address so it isn't sitting in email.

So glad I made it over. Still recovering from the ceili.

David
"""),
]),

T('November visit', ['project_none'], [
M('2026-10-04 12:18', NIAMH, ME_G, """
Hi David,

We're doing a few days in California in November (13th-17th), flying into SFO. Would you be around for dinner on the 14th or 15th? No pressure if you're swamped with the company.

Also do you know a hotel that isn't mad expensive near somewhere walkable?

Niamh
"""),
M('2026-10-04 19:30', ME_G, NIAMH, """
Yes! The 14th works. I'll book somewhere in the Mission.

For hotels, look around Hayes Valley or near Union Square if you want to walk everywhere; I'd avoid anything right on Market Street. I'll send a couple of names.

David
"""),
]),
]
