"""runs@ threads 2025-12-03 .. 2026-05-31."""
from _dsl import *

GOOGLE = P('Google', 'no-reply@accounts.google.com')
STRAVA = P('Strava', 'no-reply@strava.com')
GARMIN = P('Garmin Connect', 'noreply@garmin.com')
GARMIN_SUP = P('Garmin Product Support', 'support@garmin.com')
CHESS = P('Chess.com', 'hello@chess.com')
EVERNOTE = P('Evernote', 'no-reply@evernote.com')
XCOM = P('X', 'info@x.com')
GROK = P('Grok', 'noreply@x.ai')
PPLX = P('Perplexity', 'team@mail.perplexity.ai')
SHOES = P('Ridgeline Running Co.', 'orders@ridgelinerunning.com')
SUPPS = P('Steady State Nutrition', 'orders@steadystatenutrition.com')
BIKE = P('Drillfield Cycles', 'service@drillfieldcycles.com')
MERIDIAN = P('The Long Game', 'issues@thelonggame.news')
STRIDE = P('Stride & Base', 'newsletter@strideandbase.com')
TAX = P('FileRight Tax', 'support@filerighttax.com')
INSURE = P('Blue Ridge Mutual Auto', 'policy@blueridgemutual.com')
SAMPLES = P('Crateline Sounds', 'receipts@cratelinesounds.com')
NRV10K = P('New River Valley Spring 10K', 'race@nrvspring10k.org')
BAYHALF = P('Bay Area Half Marathon', 'registration@bayareahalf.org')
MEALKIT = P('Plateful Kitchen', 'orders@platefulkitchen.com')

UPD = ['Inbox', 'Category Updates']
PROMO = ['Category Promotions']
SOCIAL = ['Inbox', 'Category Social']
RUN = ['Inbox', 'Running']


def strava(date, week, hours, km, elev, runs, rides, other, longest, z2, highlight, kudos):
    """Format one hand-chosen weekly row into Strava's weekly-summary mail."""
    return M(date, STRAVA, ME_R, f"""
Your week on Strava: {week}

Hi David, here's how your week stacked up.

Total time | {hours}
Distance | {km} km
Elevation gain | {elev} m
Activities | {runs} runs, {rides} rides, {other}
Longest activity | {longest}
Time in Zone 2 (heart rate) | {z2}%
Kudos received | {kudos}

{highlight}

Keep it up. See your full training log at strava.com/athletes/training.

You're receiving this because weekly summaries are on. Manage email preferences in Settings > Email Notifications.
""", html=True)


def strava_thread(date, week, *a):
    return T(f'Your weekly recap: {week}', ['project_endurance_training'], [strava(date, week, *a)], labels=UPD, quote=False,
             modeled_on='')


THREADS = [
T('Welcome to your new Google Account', ['project_none'], [
M('2025-12-03 21:14', GOOGLE, ME_R, """
Hi David,

Welcome to Google. Your new account comes with access to Google products, apps and services.

Your account: david.barron.runs@gmail.com

Here are a few tips to get you started:
- Confirm your recovery phone and email so you can get back in if you forget your password.
- Review your privacy settings in Google Account > Data & privacy.
- Get 15 GB of free storage across Gmail, Drive and Photos.

The Google Accounts team
""", html=True),
], labels=['Inbox'], quote=False, notes='HARD CASE: second email account — first mail of the runs@ account (created 2025-12-03)'),

T('Saturday long run - Huckleberry out and back?', ['project_endurance_training'], [
M('2025-12-05 19:42', OWEN, ME_R, """
yo, saw you made a separate running email lol. smart, my main inbox is 90% race spam.

Saturday: thinking Huckleberry Trail out to Christiansburg and back, ~16 mi easy. Start 7:30 at the library lot? forecast says 31F at 7 so gloves.

Owen
"""),
M('2025-12-05 22:10', ME_R, OWEN, """
yeah down. but i'm keeping it zone 2 the whole way, HR cap 150, so if you want to push the back half go ahead without me

7:30 works. i'll bring the extra gels
"""),
], labels=['Inbox', 'Running']),

# ---------------- December 2025 ----------------
T('Your Evernote email address was changed', ['project_none'], [
M('2025-12-04 10:22', EVERNOTE, ME_R, """
Hi David,

The email address on your Evernote account was changed.

Old address: d***0@vt.edu
New address: david.barron.runs@gmail.com
Changed: December 4, 2025 at 10:21 AM EST
Device: Chrome on macOS

Your notes, notebooks (7) and tags were not affected. You'll use the new address the next time you sign in.

If you didn't make this change, secure your account at evernote.com/security right away.

The Evernote Team
""", html=True),
], labels=UPD, quote=False),

T('Welcome to Chess.com, dbarron_runs!', ['project_none'], [
M('2025-12-04 23:40', CHESS, ME_R, """
Welcome to Chess.com!

Your username: dbarron_runs
Starting rating (Rapid): 1200 (provisional)

We placed you based on the skill level you picked during sign-up ("I know the basics and some tactics"). Your rating will settle after about 20 rated games.

Three things to try this week:
- Play a 10|0 rapid game against someone near your rating.
- Do the Daily Puzzle. Today's is a back-rank mate in 2.
- Run a Game Review on your first loss to see where it turned.

Good luck and have fun,
The Chess.com Team
""", html=True),
], labels=SOCIAL, quote=False),

T('Confirm your X account, @dbarron_runs', ['project_none'], [
M('2025-12-06 13:05', XCOM, ME_R, """
Confirm your email address

There's one quick step you need to complete before creating your X account. Enter this verification code:

418 207

Your handle: @dbarron_runs
Code expires in 2 hours.

If you didn't request this, ignore this email.

X Corp.
"""),
M('2025-12-06 13:09', XCOM, ME_R, """
Welcome to X, David.

You're @dbarron_runs. Here's how to get the most out of your timeline:
- Follow a few topics. You picked: Running, Endurance sports, Geopolitics, Chess.
- Turn on notifications for accounts you care about.
- Try Grok, your AI assistant built into X, from the sidebar.

See what's happening at x.com.
"""),
], labels=SOCIAL, quote=False),

strava_thread('2025-12-08 08:02', 'Dec 1 - Dec 7', '9h 12m', 78.4, 412, 5, 2, '1 elliptical', 'Huckleberry long run, 25.8 km, 2:18:40', 84,
              'Highlight: your Saturday long run was your longest run since you joined Strava. Average HR 146 bpm on a 2:18 effort is a nice aerobic marker.', 23),

T('Welcome to Grok', ['project_none'], [
M('2025-12-09 00:15', GROK, ME_R, """
Hi David,

Thanks for trying Grok. You're signed in with your X account @dbarron_runs.

A few things Grok is good at:
- Real-time answers that draw on posts and news from X.
- Long questions. Paste a chart, an article or a training log and ask about it.
- Follow-ups. Keep the thread going instead of starting over.

Free accounts get a daily message limit. Upgrade any time from Settings.

The xAI team
""", html=True),
], labels=UPD, quote=False),

T('winter base block (sheet attached)', ['project_endurance_training'], [
M('2025-12-10 21:36', OWEN, ME_R, """
ok I made the sheet I was talking about. 8 weeks Dec 15 -> Feb 8, one tab. it's your numbers from saturday not mine, so yell if the hours are off.

basic idea: 3 weeks build, 1 down. long run caps at 2:30. zero intensity until feb except strides twice a week.

Owen
""", att=[A('xlsx', 'winter_base_block_dec-feb.xlsx', {
    'Plan': [['Week of', 'Run hrs', 'Bike/elliptical hrs', 'Total hrs', 'Long run', 'Strides', 'Notes'],
             ['2025-12-15', 6.0, 2.5, '=B2+C2', '2:00', '2x6', 'finals week, keep it simple'],
             ['2025-12-22', 5.0, 2.0, '=B3+C3', '1:45', '1x6', 'holiday, home trip'],
             ['2025-12-29', 5.5, 2.0, '=B4+C4', '1:50', '1x6', 'holiday'],
             ['2026-01-05', 4.0, 1.5, '=B5+C5', '1:30', '-', 'down week'],
             ['2026-01-12', 6.5, 3.0, '=B6+C6', '2:10', '2x6', 'semester starts'],
             ['2026-01-19', 7.0, 3.0, '=B7+C7', '2:20', '2x8', ''],
             ['2026-01-26', 7.5, 3.0, '=B8+C8', '2:30', '2x8', 'peak week'],
             ['2026-02-02', 5.0, 2.0, '=B9+C9', '1:40', '1x6', 'down week, test 5k-ish tempo? no, just easy'],
             ['', '', '', '', '', '', ''],
             ['Rules', 'HR cap 150 on all easy runs', '', '', '', '', ''],
             ['', 'if HR drifts >150 on hills, walk the hill', '', '', '', '', '']]}, 'Winter base block', 'Owen Patel')]),
M('2025-12-10 23:58', ME_R, OWEN, """
this is great. two things:
- the 12/22 and 12/29 weeks i'll be home, there's basically no trails, so swap some running for the trainer (call it 3 run / 4 bike)
- 7.5 + 3 in the peak week is 10.5h, that's at the top of my range, fine but i'm not adding anything on top

also i'm doing elliptical on monday mornings anyway so count that in the bike column
"""),
M('2025-12-11 08:47', OWEN, ME_R, """
done, updated my copy. also lol "zero intensity until feb" is going to be hard for me, I'll suffer quietly
"""),
], labels=RUN),

T('Your Ridgeline Running order #RR-48213 has shipped', ['project_endurance_training'], [
M('2025-12-12 14:18', SHOES, ME_R, """
Thanks for your order, David!

Order #RR-48213 | placed Dec 11, 2025

Item | Qty | Price
Trail daily trainer, men's 10.5, Slate/Orange | 1 | $139.95
Merino crew sock 3-pack, size L | 1 | $36.00
Reflective winter running vest | 1 | $54.00
Subtotal | | $229.95
Shipping (Standard, free over $99) | | $0.00
Tax (VA 5.3%) | | $12.19
Total charged to Visa ending 4417 | | $242.14

Tracking: UPS 1Z8V27E40391857226, estimated delivery Tuesday, Dec 16.

Not the right fit? Returns are free within 60 days, even if you've run in them.

Ridgeline Running Co.
""", html=True),
], labels=PROMO, quote=False),

strava_thread('2025-12-15 08:05', 'Dec 8 - Dec 14', '8h 03m', 64.9, 330, 5, 1, '2 elliptical', 'Sunday long run, 21.1 km, 1:58:22', 88,
              'Highlight: 88% of your heart-rate time was in Zone 2, your best this month. You ran 5 days in a row in a week you also logged 11 hours on your laptop, according to nobody.', 17),

T('Your Arena tournament starts in 30 minutes', ['project_none'], [
M('2025-12-17 20:30', CHESS, ME_R, """
Reminder: "Wednesday Night 10|0 Arena" starts at 9:00 PM EST.

Format: 10 minutes, no increment, 60-minute arena
Your rating: 1287 Rapid
Players registered: 214
Berserk: allowed

Your current stats: 23 rapid games, 13 wins, 8 losses, 2 draws.
Best win: vs. a 1402, Caro-Kann, Dec 13.

Join from the Play > Tournaments tab. Good luck!
"""),
], labels=SOCIAL, quote=False),

T('Stride & Base: why easy should feel embarrassingly easy', ['project_endurance_training'], [
M('2025-12-19 06:30', STRIDE, ME_R, """
STRIDE & BASE | Issue 212 | December 19, 2025

THIS WEEK: The case for embarrassing pace

If your easy runs are the subject of mild ridicule from the people you pass, you might be doing them right. Most recreational runners compress their training into a narrow band between "comfortable" and "comfortably hard", and the cost is cumulative: too tired to run the hard days hard, too fit to get much out of the easy ones.

The physiology isn't mysterious. Mitochondrial density, capillary networks and fat oxidation all respond to volume at low intensity, and they respond slowly, over months and years rather than a training block. The runners who sit at 70-75% of max heart rate for 80% of their week aren't sandbagging. They are paying into an account that compounds.

Three practical checks for the holiday weeks:
- The talk test. If you can't say a full sentence without a breath in the middle, slow down.
- Heart-rate drift. Run 60 minutes at a steady pace and compare the first and last 20 minutes. Drift above 5% means the pace wasn't really easy yet.
- Hills. Walk them if you have to. Nobody is grading you.

ALSO IN THIS ISSUE
- Reader question: "I was a miler in college and I can't run slowly without feeling like a fraud." Short answer: the fraud is the 6:40 pace you hold every day.
- Gear: we wore twelve winter gloves in 20F wind. The two winners are both under $40.
- Race calendar: spring halves that open registration in January.

Run easy, run often.
The Stride & Base editors
""", html=True),
], labels=PROMO, quote=False),

# ---------------- January 2026 ----------------
T('Software update available for your Forerunner', ['project_endurance_training'], [
M('2026-01-02 11:40', GARMIN, ME_R, """
A new software update is ready for your device.

Device: Forerunner 265
Current version: 20.26
New version: 21.18

What's new:
- Improved heart-rate accuracy at the start of cold-weather runs
- Training Readiness now accounts for sleep debt across the last 3 nights
- Fixed an issue where treadmill runs could save with a 0.0 km distance after calibration
- Battery: GPS-only mode up to 3 hours longer

To update, sync your watch with the Garmin Connect app and keep it near your phone until the update completes (about 15 minutes).

Garmin Connect
""", html=True),
], labels=UPD, quote=False),

T('The Long Game: The Long Game in the Taiwan Strait', ['project_none'], [
M('2026-01-06 07:00', MERIDIAN, ME_R, """
THE LONG GAME | No. 88 | January 6, 2026

The Long Game in the Taiwan Strait

Every new year brings a round of forecasts about the Strait, and most of them share a flaw: they treat a crisis as a single decision point rather than a slow change in costs. The more useful question for 2026 is not "will Beijing move" but "what is each side doing this year to make waiting cheaper for itself and dearer for the other."

On the Chinese side, the answer is mostly patience with pressure. Gray-zone activity, coast-guard patrols around outlying islands, and customs inspections that could become a quarantine are all ways to change facts without crossing a line that triggers a coalition response. Each one is reversible, which is the point.

On the American side, the answer has been a shift from deterrence by punishment to deterrence by denial: munitions stockpiles, dispersed basing in Japan and the Philippines, and a push to make Taiwan itself harder to swallow. The weak link is industrial. Shipbuilding capacity cannot be bought on a one-year horizon, and both governments know it.

The quiet variable is Japan. Tokyo's defense budget now sits on a path to 2% of GDP, and its public statements about the Strait have become noticeably less ambiguous. A Japan that treats a Taiwan contingency as its own changes Beijing's arithmetic more than any single U.S. carrier.

What to watch this year:
- Whether coast-guard boardings near Kinmen become routine rather than episodic.
- Munitions production numbers, not announcements.
- Semiconductor export controls, which both sides now treat as part of the same contest.

Forecasts are cheap. Watching which costs move is not.

Reply to this email to reach the editor. Forwarded this? Subscribe at thelonggame.news.
""", html=True),
], labels=PROMO, quote=False),

strava_thread('2026-01-12 08:03', 'Jan 5 - Jan 11', '5h 41m', 42.7, 188, 4, 3, '0 elliptical', 'Trainer ride, 1:30:00, 38.2 km', 91,
              'Highlight: a planned down week, and you stuck to it. 3 indoor rides this week, your most since you joined.', 9),

T('snow on the trail - treadmill or elliptical?', ['project_endurance_training'], [
M('2026-01-14 06:52', OWEN, ME_R, """
huckleberry is ice past the hospital, I slid twice yesterday. are you doing the long run indoors this weekend or bailing?
"""),
M('2026-01-14 12:31', ME_R, OWEN, """
indoors. i'm splitting it: 60 min treadmill at 1% then 60 min elliptical at the rec center. HR stays basically the same on the elliptical and my shins thank me

the plan says 2:10 this week anyway, so the last 10 min i'll just do on the bike
"""),
M('2026-01-14 13:05', OWEN, ME_R, """
2 hours on a treadmill is a war crime. I'll come for the first hour and then go home and feel superior about it
"""),
M('2026-01-14 13:20', ME_R, OWEN, """
lol deal. 9am sat, mcComas
"""),
], labels=RUN),

T('Order confirmed #SSN-20931', ['project_endurance_training'], [
M('2026-01-15 19:47', SUPPS, ME_R, """
Order confirmed. Thanks, David.

Order #SSN-20931 | January 15, 2026

Item | Qty | Price
Electrolyte drink mix, lemon-lime, 30 servings | 2 | $59.98
Endurance gel, salted caramel, 24-pack | 1 | $38.40
Magnesium glycinate 200 mg, 120 caps | 1 | $21.50
Subtotal | | $119.88
Subscribe & save (10%) | | -$11.99
Shipping | | $0.00
Total | | $107.89

Your next subscription delivery: February 15, 2026 (electrolyte mix only). Skip or edit any time in your account.

Steady State Nutrition
""", html=True),
], labels=PROMO, quote=False),

T('Your auto policy renews February 14', ['project_none'], [
M('2026-01-20 10:05', INSURE, ME_R, """
Hello David,

Your auto policy BRM-VA-7730214 renews on February 14, 2026.

Vehicle | 2014 sedan (VIN ending 4471)
Term | 6 months, Feb 14 - Aug 14, 2026
Current premium | $612.40
Renewal premium | $648.90
Change | +$36.50 (+6.0%)

Why your premium changed: statewide repair costs rose this year. Your driving record and coverage did not change.

Coverage summary: liability 50/100/50, uninsured motorist 50/100, collision with $1,000 deductible, comprehensive with $500 deductible.

Moving soon? If your car will be garaged in a different state, tell us before you move. Coverage and rates depend on where the car is kept.

Pay in full by February 13 to keep the paid-in-full discount ($24.00).

Blue Ridge Mutual Auto
""", html=True),
M('2026-01-20 22:41', ME_R, INSURE, """
Hi,

Quick question before I renew: I may move to California in the second half of the year (likely August). If that happens mid-term, do I cancel and get a prorated refund, or do you transfer the policy?

Thanks,
David Barron
Policy BRM-VA-7730214
"""),
M('2026-01-21 15:12', INSURE, ME_R, """
Hi David,

Thanks for asking ahead. We don't write policies in California, so you would buy a California policy first, then cancel this one effective the same day. Any unused premium is refunded prorated, minus a $25 cancellation fee, usually within 10 business days.

Renewing now is fine. Nothing about a later move changes today's renewal.

Best,
Renee
Policy Services, Blue Ridge Mutual Auto
"""),
], labels=UPD),

T('Your Plateful order is on its way', ['project_none'], [
M('2026-01-24 09:15', MEALKIT, ME_R, """
Your box arrives Monday, January 26.

This week's meals (2 servings each):
- Gochujang chicken rice bowls with quick-pickled cucumber (640 cal)
- Black bean and sweet potato chili (590 cal)
- Lemon-herb salmon with farro and roasted broccoli (710 cal)
- Peanut noodle stir-fry with tofu (680 cal)

Order #PK-7731-0126
4 meals x 2 servings | $71.92
Shipping | $10.99
Promo FIRSTBOX40 | -$32.97
Total | $49.94

Skip next week by Wednesday at 11:59 PM EST.
""", html=True),
], labels=PROMO, quote=False),

strava_thread('2026-01-26 08:01', 'Jan 19 - Jan 25', '10h 18m', 86.2, 455, 6, 2, '1 elliptical', 'Long run, 27.4 km, 2:24:51', 86,
              'Highlight: your biggest week on Strava so far, 10h 18m. You hit a 2:24 long run with an average HR of 145. You were also logging runs at 11:40 PM on Tuesday, which is a choice.', 31),

T('January on Chess.com: you climbed 96 points', ['project_none'], [
M('2026-02-01 12:00', CHESS, ME_R, """
Your January in chess

Rapid rating: 1287 -> 1383 (+96)
Games played: 41 (24 W, 14 L, 3 D)
Puzzles solved: 118 (rating 1612)
Most played opening (White): Queen's Gambit Declined, 14 games
Most played opening (Black): Caro-Kann Defense, 17 games
Best win: vs. 1511 on Jan 22, won a rook endgame in 58 moves
Accuracy (Game Review average): 79.4

Your weakest phase this month: middlegame time management. In 9 of your 14 losses you had under 1 minute left by move 30.

Goal for February? Try 15|10 for a week and see if the time trouble goes away.
""", html=True),
], labels=SOCIAL, quote=False),

# ---------------- February 2026 ----------------
T('Founding engineer role at Stackforge (dev tools, remote)', ['project_none'], [
M('2026-02-03 11:24', KEVIN, ME_R, """
Hi David,

I came across your public GitHub activity (the VS Code telemetry work in particular) and wanted to reach out. I recruit for Stackforge, a seed-stage dev-tools company building a debugger that records and replays production sessions for TypeScript services.

We're hiring a founding engineer with a research flavor: someone who's comfortable instrumenting editors and making sense of noisy interaction logs. The role is remote (US), $165-190k plus 0.4-0.8% equity, and the team is 6 people today.

Would you be open to a 20-minute call next week? Happy to send more details first if that's easier.

Best,
Kevin Liu
Talent Partner, Stackforge
"""),
M('2026-02-04 23:02', ME_R, KEVIN, """
Hi Kevin,

Thanks for reaching out, and it sounds like an interesting product. I'm in the middle of my PhD and not looking for a full-time role right now, so I'll pass.

Best of luck with the search,
David
"""),
M('2026-02-05 09:40', KEVIN, ME_R, """
Totally understood, David. I'll check back down the line. Good luck with the research!

Kevin
"""),
], labels=['Inbox']),

T('Save the date - Niamh & Cian, 11 July 2026, Dublin', ['project_none'], [
M('2026-02-07 18:10', NIAMH, ME_R, """
Hi David!

Formal invites go out in March but I wanted you to have the date now since you'll be flying in:

Saturday 11 July 2026
Ceremony at 1pm, reception after, both in south Dublin (venue details with the invite)

Mam says to tell you there's a bed at ours for the Thursday and Friday if you want it, and we've a room block at a hotel near the venue for the Saturday night.

Also, I only have this new email for you because your vt one bounced something last week? Use whichever you check more.

Love,
Niamh
"""),
M('2026-02-08 10:33', ME_R, NIAMH, """
congrats again!! it's in the calendar. i'll be there, flying in thursday the 9th most likely.

the vt one should work but this one is fine for anything non-school. i'll book the hotel saturday once the block is open
"""),
], labels=['Inbox', 'Family']),

strava_thread('2026-02-09 07:58', 'Feb 2 - Feb 8', '6h 05m', 51.3, 260, 5, 1, '1 elliptical', 'Long run, 18.0 km, 1:40:12', 90,
              'Highlight: end of an 8-week block. Your average easy-run pace at the same heart rate (145 bpm) is 11 s/km faster than in early December.', 14),

T('Welcome to Perplexity', ['project_none'], [
M('2026-02-10 09:12', PPLX, ME_R, """
Welcome to Perplexity, David.

Ask anything and get an answer with sources you can check. A few ways people use it:
- Literature search: "recent papers on help-seeking in intro programming courses"
- Quick facts with citations
- Spaces: keep threads, files and instructions for one topic together

Your account: david.barron.runs@gmail.com
Signed in with: Google

Happy asking,
The Perplexity Team
""", html=True),
], labels=UPD, quote=False),

T('Your Perplexity Pro trial has started', ['project_none'], [
M('2026-02-10 09:14', PPLX, ME_R, """
Your Pro trial is active.

Plan: Perplexity Pro (trial)
Trial started: February 10, 2026
Trial ends: April 10, 2026
After the trial: $20.00/month, billed to Visa ending 4417, unless you cancel before April 10.

What's included in Pro:
- Pro Search with deeper multi-step research
- Choice of advanced models
- File and image upload in threads
- Unlimited Spaces

Manage or cancel any time in Settings > Subscription.
""", html=True),
], labels=UPD, quote=False),

T('The Long Game: Chips, Ports and the New Containment', ['project_none'], [
M('2026-02-10 07:00', MERIDIAN, ME_R, """
THE LONG GAME | No. 93 | February 10, 2026

Chips, Ports and the New Containment

"Containment" is a word Washington still avoids, but the policies of the last three years add up to something close to it, with one difference from the Cold War version: it targets capabilities rather than territory.

Kennan's containment drew a line on a map and waited for the Soviet system to exhaust itself. Today's version draws lines around a few chokepoints: advanced lithography, high-end AI accelerators, certain chemicals, and increasingly the software that runs ports and logistics. The bet is the same, that time favors the side with the more productive system, but the chokepoints are narrower and the allies matter more. Export controls only bite if the Netherlands, Japan and South Korea enforce them too.

Beijing's response has been to treat self-sufficiency as a strategic goal in itself, accepting high costs and wasted capital in exchange for removing the chokepoint. That works slowly in chips and quickly in places where the gap was small, such as legacy nodes, batteries and solar, where China now sets prices for everyone else.

The risk for the containing side is the classic one of economic warfare: every control creates an incentive to substitute, and substitution is permanent. A control that slows a rival by three years and then disappears forever is a good trade only if the three years are used.

Three questions for the spring:
- Does the next round of controls cover equipment servicing, not just sales?
- Do allied governments keep matching U.S. rules when their own firms lose revenue?
- Where does the money go? Subsidy without workforce is a factory with no shifts.

Forwarded this? Subscribe at thelonggame.news.
""", html=True),
], labels=PROMO, quote=False),

T('Your Crateline Sounds receipt (order CS-118204)', ['project_music_production'], [
M('2026-02-12 01:37', SAMPLES, ME_R, """
Thanks for your purchase!

Order CS-118204 | February 12, 2026, 1:36 AM EST

Item | Format | Price
Dusty Tape Drums Vol. 2 (lo-fi drum kit, 212 one-shots, 40 loops, 82-94 BPM) | WAV 24-bit | $24.99
Warm Keys Chops (Rhodes and Wurli loops, key-labeled) | WAV 24-bit | $19.99
Bundle discount | | -$9.00
Total (Visa ending 4417) | | $35.98

Downloads (links expire in 30 days, re-download any time from your Library):
- Dusty_Tape_Drums_Vol2.zip (1.2 GB)
- Warm_Keys_Chops.zip (860 MB)

License: royalty-free for releases, including commercial streaming. No resale of the raw samples.

Tip: Drop the kits into FL Studio's Browser via Options > File settings > Add folder so they show up under Packs.
""", html=True),
], labels=PROMO, quote=False),

T('Chess.com Gold - payment receipt', ['project_none'], [
M('2026-02-22 16:44', CHESS, ME_R, """
Receipt for your Chess.com membership

Plan: Gold (annual)
Billing period: Feb 22, 2026 - Feb 21, 2027
Amount: $29.99
Paid with: Visa ending 4417
Invoice: CCM-2026-0222-55190

Gold includes unlimited Game Review, unlimited puzzles, and lessons. Manage your membership in Settings > Membership.
""", html=True),
], labels=SOCIAL, quote=False),

T('saturday club run + the hokie hill loop', ['project_endurance_training'], [
M('2026-02-25 20:15', OWEN, ME_R, """
club is doing the group run from the War Memorial gym saturday, 8am. two groups: 10 mi easy and 14 mi with the hokie hill loop at the end. invite attached so you stop saying "i didn't know when it was"

you coming to the 14?
""", att=[A('ics', 'VT_Running_Club_Saturday_Group_Run.ics', dict(
    summary='VT Running Club - Saturday group run (10 mi / 14 mi)', start='2026-02-28 08:00', end='2026-02-28 10:30',
    location='War Memorial Gym, front steps, Blacksburg VA',
    description='Two groups: 10 mi easy, 14 mi with the hill loop at the end. Coffee after at the usual place. Bring water, the fountains on the trail are off until April.',
    organizer=OWEN, attendees=[ME_R]))]),
M('2026-02-25 22:48', ME_R, OWEN, """
14 yes but i'm walking up the hill loop if HR goes over 150, don't wait for me at the top
"""),
], labels=RUN),

# ---------------- March 2026 ----------------
T('Your 2025 tax return: documents we still need', ['project_none'], [
M('2026-03-03 10:30', TAX, ME_R, """
Hi David,

You started your 2025 federal and Virginia return on February 26. Here's what's still missing before we can file:

Document | Status
W-2 (graduate assistantship) | Uploaded
1098-T (tuition statement) | Uploaded
1099-INT (savings interest, $41.18) | Missing
1099-NEC or 1099-MISC (any freelance or prize income) | Not sure? Answer the question in Income > Other
Health coverage (1095 forms) | Optional for federal

Heads up on the 1098-T: if your tuition was paid by a waiver or scholarship, box 5 may be larger than box 1. Scholarship amounts above qualified expenses can be taxable. Our interview walks you through it.

Your filing package: Deluxe federal + state, $54.99 (charged at filing).

FileRight Tax
"""),
], labels=UPD, quote=False),

T('Stride & Base: base phase, without the boredom', ['project_endurance_training'], [
M('2026-03-06 06:30', STRIDE, ME_R, """
STRIDE & BASE | Issue 223 | March 6, 2026

THIS WEEK: Base phase, without the boredom

Somewhere around week ten of an easy-only block, most runners hit the same wall: not fatigue but tedium. The data says keep going, the brain says do something interesting. A few ways to keep the aerobic work aerobic and still give the brain something to chew on:

1. Change the surface, not the effort. Trails, grass and gravel give your feet and ankles new work at the same heart rate.
2. Strides are free. Six 20-second strides at the end of two easy runs a week keep leg speed alive without a measurable cost to recovery. Former track runners in particular lose their turnover faster than their aerobic engine.
3. Cross-train with intent. A 90-minute ride at Zone 2 is not a punishment for an injury. It's the same aerobic stimulus with zero impact, and it's how some of the highest-volume runners we know get to 12 hours a week without breaking.
4. Track something besides pace. Aerobic decoupling, cadence drift, how many times you checked your watch. Pick one and watch it improve.

READER MAILBAG
"My heart rate goes from 140 to 158 on the same loop in March humidity versus February cold." That's normal. Use the cap, slow down, and remember the adaptation doesn't care what your pace looked like.

UPCOMING
Our spring half-marathon guide lands March 20, with 12-week plans for 1:45, 1:30 and sub-1:25.

The Stride & Base editors
""", html=True),
], labels=PROMO, quote=False),

T('Repair estimate - rear derailleur (ticket #4471)', ['project_none'], [
M('2026-03-09 16:22', BIKE, ME_R, """
Hi David,

We had a look at the road bike you dropped off this morning. Findings:

- Rear derailleur hanger is bent about 4 mm inboard, which is why the chain was jumping into the spokes in the 32t cog.
- Derailleur cage has a crack near the lower pivot, likely from the same fall. Not safe to reuse.
- Chain is at 0.75% wear on the checker, so it's due anyway.

Estimate:
Replacement hanger | $28.00
Rear derailleur, 11-speed, medium cage | $74.99
Chain, 11-speed | $36.00
Labor (install, index, true rear wheel) | $55.00
Total before tax | $193.99

We have the hanger and chain in stock. The derailleur would arrive Thursday. Reply "approved" and we'll order it today.

Thanks,
Josh
Drillfield Cycles service
"""),
M('2026-03-09 21:05', ME_R, BIKE, """
approved. one question, the rear wheel is only a little out of true, can you skip that and take it off the labor? i'm only riding it on the trainer until april
"""),
M('2026-03-10 09:41', BIKE, ME_R, """
Sure, we'll skip the truing and drop labor to $40. New total before tax is $178.99. Derailleur is ordered, we'll email when it's ready.

Josh
"""),
M('2026-03-12 17:55', BIKE, ME_R, """
Your bike is ready for pickup. Indexed and test-ridden through all 11 gears. We're open until 7 tonight and 10-6 tomorrow.

Josh
"""),
], labels=['Inbox']),

T('Receipt from Drillfield Cycles', ['project_none'], [
M('2026-03-13 12:14', BIKE, ME_R, """
Thanks for coming in, David. Your receipt is attached.

Ticket #4471 | Paid $188.48 | Visa ending 4417 | March 13, 2026

Reminder: your new chain will stretch fastest in the first 500 miles. Bring it in for a free re-index any time in the next 60 days.
""", att=[A('pdf', 'DrillfieldCycles_receipt_4471.pdf', [
    ('title', 'Drillfield Cycles - Service Receipt'),
    ('p', 'Ticket #4471 | Customer: David Barron | Opened 2026-03-09 | Closed 2026-03-13'),
    ('table', [['Item', 'Qty', 'Amount'],
               ['Derailleur hanger (replacement)', '1', '$28.00'],
               ['Rear derailleur, 11-speed, medium cage', '1', '$74.99'],
               ['Chain, 11-speed', '1', '$36.00'],
               ['Labor: install and index (wheel truing waived)', '1', '$40.00'],
               ['Subtotal', '', '$178.99'],
               ['Sales tax 5.3%', '', '$9.49'],
               ['Total paid', '', '$188.48']]),
    ('p', 'Payment: Visa ending 4417, approved 12:13 PM. 60-day free re-index included.'),
], 'Drillfield Cycles receipt 4471', 'Drillfield Cycles')]),
], labels=UPD, quote=False),

T('Niamh & Cian - RSVP by 15 April', ['project_none'], [
M('2026-03-11 13:20', NIAMH, ME_R, """
Hi David,

The proper invite is in the post to your Blacksburg address, but here's the RSVP form online since post to the US takes forever: just reply to this with the answers below.

1. Attending? (yes / no)
2. Plus one? (you have one if you want it)
3. Meal: beef, salmon or the mushroom risotto
4. Any allergies
5. Staying in the hotel block Saturday? (the rate is EUR 165 incl. breakfast, booking code BARRON-KELLY)

Also Cian's asking whether you'd do one of the readings. No pressure at all, it's 90 seconds.

Niamh
"""),
M('2026-03-11 23:47', ME_R, NIAMH, """
1. yes
2. no plus one, just me
3. salmon
4. none
5. yes, i'll book with the code this week

and yes i'll do the reading, tell cian i'm honored. send it whenever so i can practice not mumbling
"""),
M('2026-03-12 08:15', NIAMH, ME_R, """
Brilliant, thank you!! Reading is attached on the next email, it's the short one from Ruth. Mam is thrilled you're staying at ours Thursday and Friday.

N
"""),
M('2026-03-14 11:02', ME_R, NIAMH, """
hotel booked, confirmation DUB-88104, sat 11 -> sun 12. flight lands thursday 9 july at 7:05am
"""),
], labels=['Inbox', 'Family']),

strava_thread('2026-03-16 08:04', 'Mar 9 - Mar 15', '9h 47m', 81.0, 610, 5, 2, '1 elliptical', 'Long trail run, 24.6 km, 2:21:05, 540 m gain', 82,
              'Highlight: your first ride on the repaired bike, 1:15 on the trainer. 82% Zone 2 with 610 m of climbing is solid on hilly routes.', 22),

T('The Long Game: What Thucydides Doesn\'t Tell You', ['project_none'], [
M('2026-03-17 07:00', MERIDIAN, ME_R, """
THE LONG GAME | No. 98 | March 17, 2026

What Thucydides Doesn't Tell You

The "Thucydides trap", the claim that a rising power and an established one tend toward war, has become the default frame for U.S.-China relations. It is a useful warning and a poor model.

It's useful because it names a real mechanism: fear. The established power reads every gain by the riser as a threat, the riser reads every precaution as encirclement, and each side's defensive moves confirm the other's worst assumptions. Anyone who has watched the last decade of tariff and export-control escalation has seen that spiral.

It's a poor model for three reasons. First, the historical sample is small and contested; scholars can't agree on how many of the canonical cases fit. Second, nuclear weapons change the payoff of a direct war so much that the comparison with Athens and Sparta mostly breaks. Third, and most important, the trap is described as structural, which invites fatalism. Structure sets the pressures; it doesn't make the decisions.

A more useful frame is the security dilemma plus domestic politics. Leaders in both capitals face audiences that reward toughness and punish visible concessions. The dangerous moments are therefore less likely to be grand strategic choices than small incidents (a collision at sea, a detained crew) that leaders can't be seen to back down from.

What lowers the risk in practice:
- Crisis communication channels that work at the operational level, not just between presidents.
- Rules for unplanned encounters at sea and in the air, actually practiced.
- Economic interdependence in areas neither side wants to lose, which is shrinking.

History rhymes. It doesn't decide.

Forwarded this? Subscribe at thelonggame.news.
""", html=True),
], labels=PROMO, quote=False),

T('You\'re registered: New River Valley Spring 10K (April 18)', ['project_endurance_training'], [
M('2026-03-18 22:31', NRV10K, ME_R, """
You're in, David!

Event: New River Valley Spring 10K
Date: Saturday, April 18, 2026, 8:00 AM
Start/finish: Christiansburg Recreation Center
Registration #: NRV-10K-0583
Wave: A (seeded, sub-40 estimate)
Shirt: Men's M
Fee: $45.00 + $3.62 processing

Your signed waiver and registration receipt are attached. Bib pickup: Friday April 17, 4-7 PM, or race morning from 6:45 AM.

Proceeds support the regional trail conservancy. Thank you for running!
""", att=[A('pdf', 'NRV_Spring_10K_registration_NRV-10K-0583.pdf', [
    ('title', 'New River Valley Spring 10K - Registration and Waiver'),
    ('p', 'Registrant: David Barron | Registration #NRV-10K-0583 | Registered 2026-03-18 22:30 EDT'),
    ('table', [['Item', 'Amount'], ['10K entry (early)', '$45.00'], ['Processing fee', '$3.62'], ['Total', '$48.62']]),
    ('h2', 'Waiver and release'),
    ('p', 'I understand that running a 10K is a potentially hazardous activity. I attest that I am physically fit and have sufficiently trained for this event. I assume all risks associated with running in this event, including falls, contact with other participants, weather and traffic. I grant permission to the organizers to use photographs of me taken at the event.'),
    ('p', 'Electronically signed: David Barron, 2026-03-18 22:30 EDT, IP logged.'),
], 'NRV Spring 10K registration', 'NRV Spring 10K')]),
], labels=['Inbox', 'Running'], quote=False),

T('skipping sat long run (paper deadline)', ['project_endurance_training'], [
M('2026-03-27 00:48', ME_R, OWEN, """
heads up i'm out for saturday's long run, paper is due tuesday night and i'm basically living in the lab. i'll do 75 min easy sunday morning if my brain works

don't let the club do the hill loop without me
"""),
M('2026-03-27 07:30', OWEN, ME_R, """
lol go write. I'll take attendance. you're allowed one week off before the 10K, not two
"""),
], labels=RUN),

# ---------------- April 2026 ----------------
T('so... did the paper go in?', ['project_endurance_training', 'project_tutortrace'], [
M('2026-04-01 13:12', OWEN, ME_R, """
alive? did the paper go in? and are you running thursday or still sleeping it off
"""),
M('2026-04-01 22:40', ME_R, OWEN, """
it went in, about 40 min before the deadline (it was AoE so technically 8am today here). 10 pages + appendix. it's the tutortrace thing, using editor + tutor logs to figure out when students are stuck vs just thinking

reviews come back in june. i slept 11 hours

thursday yes, easy 8 mi. legs feel weird from sitting for a week
"""),
M('2026-04-02 07:05', OWEN, ME_R, """
congrats man. 8 mi thursday, 6:30am, my place. I'll go slow, you'll be rusty
"""),
], labels=RUN),

T('Your 2025 returns were accepted', ['project_none'], [
M('2026-04-02 14:06', TAX, ME_R, """
Good news, David. Both of your returns were accepted.

Return | Status | Accepted | Refund
Federal (2025) | Accepted | April 2, 2026 | $612.00
Virginia (2025) | Accepted | April 2, 2026 | $188.00

Expected deposit: federal within 21 days, Virginia within 4 weeks, to checking ending 0932.

Your filing summary is attached. Keep it with your records for at least three years.

FileRight Tax
""", att=[A('pdf', 'FileRight_2025_filing_summary.pdf', [
    ('title', '2025 Filing Summary'),
    ('p', 'Taxpayer: David Barron | Filing status: Single | Filed 2026-04-01 | Accepted 2026-04-02'),
    ('table', [['Line', 'Federal', 'Virginia'],
               ['Wages (W-2)', '$31,840', '$31,840'],
               ['Taxable interest', '$41', '$41'],
               ['Taxable scholarship (above qualified expenses)', '$0', '$0'],
               ['Standard deduction', '$15,000', '$8,000'],
               ['Tax withheld', '$2,710', '$1,402'],
               ['Refund', '$612', '$188']]),
    ('p', 'Prepared with FileRight Deluxe. Package fee $54.99 paid 2026-04-01.'),
], 'FileRight 2025 filing summary', 'FileRight Tax')]),
], labels=UPD, quote=False),

T('Your Perplexity Pro trial ends in 3 days', ['project_none'], [
M('2026-04-07 09:00', PPLX, ME_R, """
Hi David,

Your Perplexity Pro trial ends on April 10, 2026. After that, your plan converts to Pro at $20.00/month on Visa ending 4417.

During your trial you:
- Ran 96 Pro Searches
- Created 3 Spaces
- Uploaded 11 files

Want to keep Pro? You don't need to do anything.
Want to stay on Free? Cancel in Settings > Subscription before April 10. Your threads and Spaces stay either way.
""", html=True),
], labels=UPD, quote=False),

T('Your Pro trial has ended', ['project_none'], [
M('2026-04-10 10:02', PPLX, ME_R, """
Your Perplexity Pro trial ended today.

You cancelled before the trial ended, so you have not been charged. Your account is now on the Free plan.

Your threads, Spaces and uploaded files are still available. Free accounts get a limited number of Pro Searches each day.

Changed your mind? Upgrade any time from Settings > Subscription.
""", html=True),
], labels=UPD, quote=False),

T('Race week: New River Valley Spring 10K - bib #214', ['project_endurance_training'], [
M('2026-04-14 18:00', NRV10K, ME_R, """
Race week! Here's everything you need for Saturday.

Your bib number: 214 (Wave A, 8:00 AM)

Bib pickup: Friday April 17, 4-7 PM at Christiansburg Recreation Center, or race morning 6:45-7:40 AM.
Parking: Lot B and the overflow field on Independence Blvd. No parking at the start after 7:30.
Course: one loop, two short climbs at km 3.5 and km 7.8, net elevation 0. Water at km 3 and 6.
Timing: chip on the back of your bib. Don't fold it.
Weather: currently 48F at the start, light wind from the west.
Awards: 9:30 AM, top 3 overall and age groups (10-year bands).

See you on the line.
""", html=True),
], labels=['Inbox', 'Running'], quote=False),

T('Results: New River Valley Spring 10K', ['project_endurance_training'], [
M('2026-04-19 10:15', NRV10K, ME_R, """
Thanks for running, David! Your official results:

Bib | 214
Chip time | 36:48
Gun time | 36:51
Pace | 3:41/km (5:56/mi)
Overall | 9th of 612
Men 20-29 | 3rd of 74

Splits:
5 km | 18:31
10 km | 36:48 (second half 18:17)

Photos will be posted Tuesday. Full results at nrvspring10k.org/results.

See you next year!
""", html=True),
], labels=['Inbox', 'Running'], quote=False),

T('10k recap + what next', ['project_endurance_training'], [
M('2026-04-19 14:32', OWEN, ME_R, """
36:48 off zero speedwork. that's actually ridiculous. negative split too. I ran 36:02 and felt like death at 8k

ok serious question: bay area half in october? I start my job in oakland in august so I'll be out there. you said you might be in SF by then?
"""),
M('2026-04-19 21:10', ME_R, OWEN, """
lol the base stuff works, the second half felt controlled. i didn't look at pace once, just kept HR under 180 till 8k and then let it go

and yeah, very likely sf from august. i'm in for the half. goal would be low 1:25s if i keep 9-10h through the summer and add one tempo a week starting august

registration opens may 1 i think
"""),
M('2026-04-20 08:02', OWEN, ME_R, """
deal. I'm going for sub 1:23. we sign up the day it opens before the early price goes
"""),
], labels=RUN),

T('Your Ridgeline Running order #RR-51977', ['project_endurance_training'], [
M('2026-04-22 13:40', SHOES, ME_R, """
Thanks for your order, David!

Order #RR-51977 | placed April 22, 2026

Item | Qty | Price
Road daily trainer, men's 10.5, Black/Volt | 1 | $144.95
Lightweight racing flat, men's 10.5 | 1 | $159.95
Loyalty reward (500 points) | | -$10.00
Subtotal | | $294.90
Shipping | | $0.00
Tax (VA 5.3%) | | $15.63
Total charged to Visa ending 4417 | | $310.53

Your December trail shoes are at 612 km on Strava. Most daily trainers last 600-800 km, so the timing's about right.

Tracking: UPS 1Z8V27E40392014483, estimated delivery Friday, April 24.
""", html=True),
], labels=PROMO, quote=False),

strava_thread('2026-04-27 08:02', 'Apr 20 - Apr 26', '8h 34m', 72.6, 380, 5, 2, '0 elliptical', 'Long run, 22.5 km, 1:52:30', 83,
              'Highlight: recovery week after a 10K PR and you stayed patient. Your new road shoes logged their first 31 km.', 19),

T('Order shipped #SSN-24418', ['project_endurance_training'], [
M('2026-04-29 11:08', SUPPS, ME_R, """
Your order has shipped. Thanks, David.

Order #SSN-24418 | April 29, 2026

Item | Qty | Price
Electrolyte drink mix, unflavored, 30 servings | 1 | $29.99
Endurance gel, salted caramel, 24-pack | 1 | $38.40
Endurance gel, caffeinated espresso (50 mg), 12-pack | 1 | $21.60
Beta-alanine powder, 60 servings | 1 | $24.95
Subtotal | | $114.94
Shipping | | $0.00
Total | | $114.94

Tracking: USPS 9400 1118 9922 3374 5521 08

Note: you changed your subscription from monthly to every 6 weeks on April 28.
""", html=True),
], labels=PROMO, quote=False),

# ---------------- May 2026 ----------------
T('Registration confirmed: Bay Area Half Marathon, October 15, 2026', ['project_endurance_training'], [
M('2026-05-01 07:18', BAYHALF, ME_R, """
You're registered for the Bay Area Half Marathon!

Runner: David Barron
Event: Half Marathon (21.1 km)
Race date: Thursday, October 15, 2026
Confirmation #: BAHM26-11873
Projected finish entered: 1:25:00 (Corral A)
Fee: Early-bird $115.00 + $8.47 processing

Your receipt is attached. Corral assignments are confirmed in September based on a qualifying time; your 10K result (36:48, April 18) has been noted.

Transfers: allowed until September 15 for a $20 fee.
Packet pickup: race expo, October 13-14 (details in September).

See you at the start line!
""", att=[A('pdf', 'BAHM26_receipt_11873.pdf', [
    ('title', 'Bay Area Half Marathon 2026 - Registration Receipt'),
    ('p', 'Confirmation BAHM26-11873 | Registered 2026-05-01 10:17 PDT (07:17 EDT)'),
    ('table', [['Item', 'Amount'], ['Half Marathon entry (early bird)', '$115.00'], ['Processing fee', '$8.47'], ['Total charged (Visa ending 4417)', '$123.47']]),
    ('p', 'Runner: David Barron | Corral request: A (projected 1:25:00) | Qualifying time submitted: 10K 36:48 (2026-04-18)'),
    ('p', 'Refund policy: no refunds. Transfers to another runner until 2026-09-15 ($20).'),
], 'BAHM 2026 receipt', 'Bay Area Half Marathon')]),
], labels=['Inbox', 'Running'], quote=False),

T('Stride & Base: the 12-week half for people with real jobs', ['project_endurance_training'], [
M('2026-05-08 06:30', STRIDE, ME_R, """
STRIDE & BASE | Issue 232 | May 8, 2026

THIS WEEK: A half-marathon block for people with real jobs

Most half-marathon plans are written for someone who can run at 6 AM every day and nap at noon. This one is written for the rest of us: 6-7 sessions a week, one of them optional, and nothing that falls apart if you miss a day.

The structure:
- One long run, building from 90 minutes to 2 hours, with the last 20 minutes at goal pace in weeks 6, 8 and 10.
- One threshold session: 3x10 minutes at about one-hour race effort, building to 2x20.
- Everything else easy. Truly easy.
- A down week every fourth week, cutting volume by a third.

Why threshold and not intervals? For the half, the limiting factor is how fast you can run before lactate starts piling up, and that number moves most with 20-40 minutes of comfortably hard running per week. VO2max intervals are a nice garnish in the last month.

For readers with a big aerobic base (lots of you wrote in after our base-phase issue): you'll be surprised how quickly threshold pace comes around once you add it. Six weeks of one session a week is often worth 10-15 seconds per km.

GEAR
Race-day shoes with carbon plates: worth roughly 1-3% for most runners, more if your form holds up late. Train in them a few times first.

Download the full plan (PDF) at strideandbase.com/half12.

The Stride & Base editors
""", html=True),
], labels=PROMO, quote=False),

T('Puzzle Rush: new personal best (31)', ['project_none'], [
M('2026-05-10 22:58', CHESS, ME_R, """
New personal best!

Puzzle Rush (5 minutes): 31 solved
Previous best: 26 (March 3, 2026)
Rank among your friends: 2nd (owen_patel_runs: 34)

The puzzle that ended your run: #27, a knight fork on f7 that you saw one move too late.

Try Survival mode next. There's no clock, three strikes and you're out.
""", html=True),
], labels=SOCIAL, quote=False),

strava_thread('2026-05-11 08:00', 'May 4 - May 10', '7h 22m', 60.1, 290, 4, 3, '0 elliptical', 'Long run, 20.4 km, 1:44:10', 87,
              'Highlight: a lighter week by your standards. 3 of your 4 runs started after 10 PM. Your ride on Saturday (2:05, 61 km) was your longest since October.', 12),

T('The Long Game: India\'s Swing Strategy', ['project_none'], [
M('2026-05-12 07:00', MERIDIAN, ME_R, """
THE LONG GAME | No. 106 | May 12, 2026

India's Swing Strategy

Washington's Indo-Pacific strategy assumes that India will be on its side when it counts. New Delhi's strategy assumes nothing of the kind, and that is not a contradiction. It's the strategy.

India's tradition of non-alignment has been rebranded as "multi-alignment": deep defense ties with the United States, discounted oil and legacy weapons from Russia, a working if wary relationship with China, and leadership claims in the Global South. Critics call it fence-sitting. A better description is optionality. A country that expects to be the world's third-largest economy within a decade sees little reason to lock in today's alignment at today's price.

The China border is the hard constraint. The 2020 clashes in the Galwan Valley did more to push India toward Washington than any summit. But the push has limits: India wants U.S. technology, intelligence and investment, not a treaty that would draw it into a Taiwan conflict.

For the United States, the lesson is to stop measuring the partnership by votes at the United Nations or statements on Ukraine and to measure it by capabilities: jet engines co-produced in India, undersea cables, semiconductor packaging plants, and joint maritime patrols in the Indian Ocean. Those don't depend on India agreeing with Washington about everything. They depend on both countries seeing China the same way at sea.

What to watch:
- Whether co-production deals get past the memorandum stage.
- India's purchases of Russian oil as the price discount narrows.
- Border talks with Beijing, which tend to move quietly before big summits.

Forwarded this? Subscribe at thelonggame.news.
""", html=True),
], labels=PROMO, quote=False),

T('Re: Case 08837215 - Forerunner not syncing sleep data', ['project_endurance_training'], [
M('2026-05-13 23:12', ME_R, GARMIN_SUP, """
Hi,

My Forerunner 265 has stopped syncing sleep and HRV data to Garmin Connect since about May 6. Runs sync fine. I'm on software 21.18, the iPhone app is up to date, and I've already restarted both the watch and the phone. Morning reports on the watch show sleep, it just never shows up in the app.

Thanks,
David
""", subject='Case 08837215 - Forerunner not syncing sleep data'),
M('2026-05-14 14:26', GARMIN_SUP, ME_R, """
Hi David,

Thanks for the detail, it helps. This is a known issue with 21.18 when the watch's health data file grows past a certain size. Please try:

1. On the watch: Settings > System > Data Recording > Clear health data cache (this does not delete activities).
2. In Garmin Connect: More > Settings > Garmin Devices > Forerunner 265 > Sync now.
3. If sleep still doesn't appear after the next night, reply here and we'll send the 21.22 beta, which fixes it.

Kind regards,
Mariana
Garmin Product Support
"""),
M('2026-05-15 08:09', ME_R, GARMIN_SUP, """
that fixed it, last night's sleep and HRV showed up. thanks Mariana
"""),
], labels=['Inbox']),

T('Your April monthly report', ['project_endurance_training'], [
M('2026-05-03 09:00', GARMIN, ME_R, """
Your April in review

Activities | 23
Total time | 38h 51m
Running | 27h 10m, 305.6 km
Cycling | 10h 05m, 290.0 km
Other cardio | 1h 36m
Average resting heart rate | 46 bpm (March: 47)
Average HRV (overnight) | 78 ms, balanced
VO2 max (running) | 61 (up 1)
Personal record | 10K, 36:48 (April 18)
Training load focus | Low aerobic: 71%, High aerobic: 22%, Anaerobic: 7%

A chart of your weekly hours is attached.
""", html=True, att=[A('png', 'April_2026_weekly_hours.png', dict(
    title='Weekly training hours, April 2026', labels=['Mar 30', 'Apr 6', 'Apr 13', 'Apr 20', 'Apr 27'], values=[7.2, 9.6, 9.1, 8.6, 4.3],
    ylabel='hours', color='#1a73e8'))]),
], labels=UPD, quote=False),

strava_thread('2026-02-23 08:03', 'Feb 16 - Feb 22', '4h 49m', 38.8, 210, 3, 2, '1 elliptical', 'Trainer ride, 1:20:00, 36.5 km', 92,
              'Highlight: a quiet week, 4h 49m. Your rest-day streak on Wednesday and Thursday is the first back-to-back rest since you joined.', 6),

T('summer plan + you moving out west', ['project_endurance_training'], [
M('2026-05-26 19:21', OWEN, ME_R, """
made the summer sheet for the half. june/july is more base (you'll love that), tempo starts aug 3. you're gone 9-13 july for the wedding so I left that week at 5h.

also when do you actually move? I land in oakland aug 1. we should find a saturday long run route, apparently everyone does the bay trail or the marin headlands and the headlands will wreck your HR cap
"""),
M('2026-05-26 23:44', ME_R, OWEN, """
moving around aug 8, still looking at places in sf, nothing locked. july is going to be rough work-wise so the 5h week during the wedding is realistic, maybe even the week after

bay trail for the long runs, headlands once a month as a treat. i'll get the sheet into my training log this week
"""),
], labels=RUN),
]
