"""runs@ threads 2026-06-01 .. 2026-10-17 (hand-written; walk-on senders defined below)."""
from _dsl import *

# ---------------- walk-on senders ----------------
STRAVA = P('Strava', 'no-reply@strava.com')
GARMIN = P('Garmin Connect', 'noreply@garmin.com')
CHESS = P('Chess.com', 'hello@chess.com')
GSEC = P('Google', 'no-reply@accounts.google.com')
RACE = P('Bay Area Half Marathon', 'info@bayareahalfmarathon.org', PT)
RACE_RESULTS = P('Bay Area Half Marathon Results', 'results@bayareahalfmarathon.org', PT)
NEST = P('Nestlist Alerts', 'alerts@nestlist.co', PT)
FOGLINE = P('Carla at Fogline Property Management', 'leasing@foglinepm.com', PT)
FOGLINE_PAY = P('Fogline Resident Payments', 'payments@foglinepm.com', PT)
JONAH = P('Jonah', 'jonah.sublets.sf@gmail.com', PT)
CRATE = P('Crate & Haul Shipping', 'bookings@crateandhaul.com', ET)
SHOES = P('Ridgeline Running Co.', 'orders@ridgelinerunning.com', PT)
FUEL = P('Fuel Lab Nutrition', 'orders@fuellabnutrition.com', ET)
LONGGAME = P('The Long Game', 'issues@thelonggame.news', ET)
STRIDE = P('Stride & Base', 'newsletter@strideandbase.com', ET)
LOOPFORGE = P('Loopforge Samples', 'receipts@loopforge.audio')
WAVEYARD = P('Waveyard Audio', 'store@waveyard.audio')
AIRLINE = P('Emerald Atlantic Airways', 'itinerary@emeraldatlantic.com', IE)
OWEN_SF = P('Owen Patel', 'owen.patel.runs@gmail.com', PT)  # Owen moved to Oakland on 2026-08-01


def strava(date, span, total, dist, elev, n, highlight, rows, note):
    body = f"""
Your week on Strava: {span}

Total time | {total}
Distance | {dist}
Elevation | {elev}
Activities | {n}

Highlight: {highlight}

{chr(10).join(rows)}

{note}

See your full training log: strava.com/athletes/training
You're receiving this weekly summary because you follow your own progress. Manage email settings in Strava.
"""
    return T(f'Your weekly summary: {span}', ['project_endurance_training'],
             [M(date, STRAVA, ME_R, body, html=True)], labels=['Inbox', 'Category Updates'], quote=False)


THREADS = [
# ======================= Strava weekly summaries =======================
strava('2026-06-08 07:05', 'Jun 1 – Jun 7', '7h 42m', '41.6 mi run · 38.0 mi ride', '2,310 ft', 8,
       'Longest run of the week: 14.2 mi on Huckleberry Trail at 8:41/mi, avg HR 146.',
       ['Mon | Run | 6.1 mi | 53:20 | avg HR 141',
        'Tue | Elliptical | — | 1:00:00 | avg HR 138',
        'Wed | Run | 7.0 mi | 1:00:45 | avg HR 144',
        'Thu | Ride | 24.5 mi | 1:22:10 | avg HR 132',
        'Fri | Run | 5.0 mi | 44:02 | avg HR 139',
        'Sat | Run | 14.2 mi | 2:03:21 | avg HR 146',
        'Sun | Ride | 13.5 mi | 48:30 | avg HR 128',
        'Sun | Run | 9.3 mi | 1:21:15 | avg HR 145'],
       'You logged 18% more time than your 4-week average.'),
strava('2026-06-22 06:58', 'Jun 15 – Jun 21', '6h 51m', '35.2 mi run · 22.4 mi ride', '1,640 ft', 6,
       'Most consistent: 4 runs within 3 bpm of your Zone 2 ceiling (150).',
       ['Mon | Run | 6.4 mi | 55:48 | avg HR 143',
        'Tue | Elliptical | — | 45:00 | avg HR 136',
        'Thu | Run | 8.1 mi | 1:10:02 | avg HR 147',
        'Fri | Ride | 22.4 mi | 1:15:40 | avg HR 130',
        'Sat | Run | 12.0 mi | 1:44:10 | avg HR 148',
        'Sun | Run | 8.7 mi | 1:15:33 | avg HR 145'],
       'You logged 11% less time than your 4-week average. Rest weeks count too.'),
strava('2026-07-20 07:12', 'Jul 13 – Jul 19', '8h 14m', '47.9 mi run · 30.2 mi ride', '2,980 ft', 9,
       'New best effort: 10K in 39:58 during Thursday\'s progression run.',
       ['Mon | Run | 5.2 mi | 46:10 | avg HR 137 | jet lag shakeout',
        'Tue | Run | 7.5 mi | 1:04:30 | avg HR 144',
        'Wed | Ride | 30.2 mi | 1:41:05 | avg HR 133',
        'Thu | Run | 9.0 mi | 1:08:40 | avg HR 158 | progression',
        'Fri | Elliptical | — | 50:00 | avg HR 135',
        'Sat | Run | 15.1 mi | 2:09:44 | avg HR 147',
        'Sun | Run | 6.0 mi | 52:02 | avg HR 139',
        'Sun | Strength | — | 25:00 | —',
        'Sun | Run | 5.1 mi | 44:30 | avg HR 140'],
       'You logged 22% more time than your 4-week average.'),
strava('2026-08-10 07:01', 'Aug 3 – Aug 9', '5h 18m', '30.4 mi run', '1,150 ft', 5,
       'First activity in a new city: 8.2 mi Crissy Field – Fort Point out and back on Aug 9.',
       ['Mon | Run | 6.3 mi | 54:55 | avg HR 142',
        'Tue | Run | 5.8 mi | 50:31 | avg HR 140',
        'Thu | Elliptical | — | 40:00 | avg HR 134',
        'Fri | Run | 10.1 mi | 1:28:12 | avg HR 146 | last Huckleberry Trail run',
        'Sun | Run | 8.2 mi | 1:11:40 | avg HR 149 | Crissy Field'],
       'You logged 31% less time than your 4-week average.'),
strava('2026-08-24 06:55', 'Aug 17 – Aug 23', '9h 36m', '52.8 mi run · 41.0 mi ride', '4,870 ft', 9,
       'Biggest climb: 1,120 ft up Twin Peaks on Wednesday\'s run, still under HR 150.',
       ['Mon | Run | 7.0 mi | 1:00:40 | avg HR 143',
        'Tue | Ride | 21.3 mi | 1:18:20 | avg HR 131 | Great Highway',
        'Wed | Run | 8.4 mi | 1:16:05 | avg HR 149 | Twin Peaks',
        'Thu | Run | 6.2 mi | 53:44 | avg HR 140',
        'Fri | Elliptical | — | 45:00 | avg HR 135',
        'Sat | Run | 16.0 mi | 2:15:30 | avg HR 147 | Presidio loops w/ Owen',
        'Sun | Ride | 19.7 mi | 1:10:45 | avg HR 129',
        'Sun | Run | 8.0 mi | 1:09:12 | avg HR 144',
        'Sun | Run | 7.2 mi | 1:01:50 | avg HR 141'],
       'Block 4, week 2. You logged 9% more time than your 4-week average.'),
strava('2026-09-07 07:04', 'Aug 31 – Sep 6', '10h 52m', '61.3 mi run · 35.6 mi ride', '6,240 ft', 10,
       'Longest run this year: 18.4 mi Golden Gate Bridge – Sausalito – Tennessee Valley, 2:38:15.',
       ['Mon | Run | 6.5 mi | 56:10 | avg HR 140',
        'Tue | Run | 9.0 mi | 1:07:20 | avg HR 156 | 3x2 mi @ 6:40',
        'Wed | Ride | 35.6 mi | 2:05:00 | avg HR 132 | Paradise Loop',
        'Thu | Run | 7.2 mi | 1:02:40 | avg HR 142',
        'Fri | Run | 5.1 mi | 45:30 | avg HR 136',
        'Sat | Run | 18.4 mi | 2:38:15 | avg HR 148 | Marin',
        'Sun | Run | 8.0 mi | 1:10:05 | avg HR 141',
        'Sun | Strength | — | 30:00 | —',
        'Thu | Elliptical | — | 40:00 | avg HR 133',
        'Sun | Run | 7.1 mi | 1:01:22 | avg HR 139'],
       'Block 4, week 4. Highest weekly time since you joined in December.'),
strava('2026-09-21 06:59', 'Sep 14 – Sep 20', '10h 18m', '58.0 mi run · 28.9 mi ride', '3,910 ft', 9,
       'Fastest tempo: 7.0 mi at 6:34/mi average along the Embarcadero, avg HR 168.',
       ['Mon | Run | 6.0 mi | 52:05 | avg HR 139',
        'Tue | Run | 10.0 mi | 1:12:30 | avg HR 163 | 7 mi tempo',
        'Wed | Ride | 28.9 mi | 1:39:40 | avg HR 130',
        'Thu | Run | 7.5 mi | 1:05:00 | avg HR 141',
        'Fri | Elliptical | — | 45:00 | avg HR 134',
        'Sat | Run | 16.2 mi | 2:14:50 | avg HR 147 | 3 mi @ HM pace at the end',
        'Sun | Run | 8.3 mi | 1:12:10 | avg HR 142',
        'Sun | Run | 5.0 mi | 44:05 | avg HR 136',
        'Sun | Strength | — | 25:00 | —'],
       'Block 4, week 6. You logged 4% more time than your 4-week average.'),
strava('2026-10-12 07:08', 'Oct 5 – Oct 11', '7h 09m', '42.5 mi run · 14.0 mi ride', '1,820 ft', 7,
       'Sharpest session: 6x800m averaging 2:51 on the Kezar track on Oct 9.',
       ['Mon | Run | 6.2 mi | 53:20 | avg HR 140',
        'Tue | Run | 4.0 mi | 35:10 | avg HR 137 | hotel treadmill',
        'Thu | Run | 5.5 mi | 47:44 | avg HR 139',
        'Fri | Run | 8.0 mi | 58:30 | avg HR 160 | 6x800m',
        'Sat | Ride | 14.0 mi | 52:15 | avg HR 126',
        'Sat | Run | 12.1 mi | 1:42:40 | avg HR 145',
        'Sun | Run | 6.7 mi | 57:55 | avg HR 138'],
       'Taper week. You logged 29% less time than your 4-week average.'),

# ======================= Garmin =======================
T('Your Training Status is now Productive', ['project_endurance_training'], [
M('2026-06-14 09:20', GARMIN, ME_R, """
Hi David,

Your Training Status on your Forerunner 255 changed from Maintaining to Productive.

Acute load (7-day) | 612
Chronic load (28-day) | 548
Load focus | Low aerobic 64% · High aerobic 29% · Anaerobic 7%
VO2 max (running) | 57 (+1)
HRV status | Balanced (7-day avg 68 ms)

What this means: your current training load is moving your fitness in the right direction. Your low-aerobic base is well covered; one more high-aerobic session per week would balance your load focus.

Open Garmin Connect to see your full training report.
""", html=True),
], labels=['Inbox', 'Category Updates'], quote=False),

T('Your August Report from Garmin Connect', ['project_endurance_training'], [
M('2026-09-01 08:40', GARMIN, ME_R, """
Hi David,

Here's how August went.

Activities | 37
Total time | 39h 22m
Running distance | 218.6 mi
Cycling distance | 96.6 mi
Avg resting HR | 44 bpm
Avg sleep | 7h 06m
VO2 max (running) | 58

Your weekly time is charted in the attached image. The week of Aug 3 dips while you were traveling (and your time zone changed from Eastern to Pacific on Aug 8; your daily stats were adjusted).

Personal records this month:
- Longest run: 16.0 mi (Aug 22)
- Most elevation gain in a run: 1,120 ft (Aug 19)

Keep moving,
Garmin Connect
""", html=True, att=[A('png', 'august_weekly_training_time.png',
    dict(title='August 2026 - weekly training time (hours)', labels=['Jul 27', 'Aug 3', 'Aug 10', 'Aug 17', 'Aug 24', 'Aug 31*'],
         values=[8.6, 5.3, 8.9, 9.6, 10.1, 1.4], ylabel='hours', color='#007cc3'))]),
], labels=['Inbox', 'Category Updates'], quote=False),

T('New personal record: Half Marathon 1:24:51', ['project_endurance_training'], [
M('2026-10-16 08:15', GARMIN, ME_R, """
Hi David,

Nice work. Your Forerunner 255 recorded a new personal record.

Half Marathon | 1:24:51 (previous: 1:28:37, Apr 2025)
Avg pace | 6:29 /mi
Avg HR | 171 bpm
Max HR | 188 bpm
Cadence | 182 spm
Training Effect | Aerobic 4.6 Tempo · Anaerobic 1.8

Race predictor (updated): 5K 18:51 · 10K 39:20 · Half 1:24:30 · Marathon 2:59:40

Your Training Status is Recovery. We suggest 2 to 3 easy days before your next hard session; your recovery time is 72 hours.
""", html=True),
], labels=['Inbox', 'Category Updates'], quote=False),

# ======================= Bay Area Half Marathon (2026-10-15) =======================
T('12 weeks out: pace groups and your training plan', ['project_endurance_training'], [
M('2026-07-22 10:00', RACE, ME_R, """
Hi David,

Race day is 12 weeks away: Thursday, October 15, 2026. Start gun 7:00 AM at the Embarcadero.

PACE GROUPS
This year we have pacers for 1:25, 1:30, 1:35, 1:40, 1:45, 1:50, 2:00, 2:15 and 2:30. Pacers run even splits and wear a flag with their finish time. The 1:25 group runs 6:29/mi (4:02/km).

FREE 12-WEEK PLANS
Our coaching partner put together three plans (Finish, Improve, Compete). The Compete plan assumes 40+ mi/week now and peaks at about 55 mi/week in week 9 with a 3-week taper. Download the plans from your participant dashboard.

KEY DATES
- Aug 31: last day to change distance (Half to 10K) free of charge
- Sep 25: corral assignments and bib numbers emailed
- Oct 13–14: packet pickup at the Ferry Building plaza tent

COURSE
Embarcadero > Fisherman's Wharf > Marina Green > Crissy Field > Golden Gate Bridge turnaround at the Vista Point side > back along Crissy Field > finish at Marina Green. Two short climbs: the Fort Mason hill (mile 3 and mile 11) and the bridge approach (mile 6).

See you on the start line,
Bay Area Half Marathon Team
""", html=True),
], labels=['Inbox', 'Races'], quote=False),

T('Your corral assignment and bib number: #2187, Corral A', ['project_endurance_training'], [
M('2026-09-25 12:30', RACE, ME_R, """
Hi David,

Your race assignment for the 2026 Bay Area Half Marathon:

Bib number | 2187
Corral | A (seeded, sub-1:30 projected)
Wave start | 7:00 AM
Projected finish (from your submitted time) | 1:25:00
Bag check | Truck 4, Marina Green

Your bib has a timing chip on the back. Do not fold or bend it. Pin it to the front of your shirt.

Corral A closes at 6:50 AM. Runners who arrive after closing will be moved to Corral B.

If anything above is wrong, reply to this email before October 9.
""", html=True),
M('2026-09-25 21:47', ME_R, RACE, """
Hi, quick question: my friend Owen Patel (bib 2044) is also in Corral A. Is there anything we need to do to start together or is Corral A just open seeding inside the corral?

Thanks,
David Barron
"""),
M('2026-09-26 10:12', RACE, ME_R, """
Hi David,

Corral A is open seeding, so you and Owen can line up anywhere inside it. Just make sure both of you are in before 6:50.

Best,
Bay Area Half Marathon Team
"""),
], labels=['Inbox', 'Races'], quote=True),

T('Race week: everything you need (course map attached)', ['project_endurance_training'], [
M('2026-10-10 09:00', RACE, ME_R, """
Hi David,

It's race week. Here's everything in one place. The course map and the start/finish layout are in the attached PDF.

PACKET PICKUP
Tuesday Oct 13, 11 AM – 7 PM and Wednesday Oct 14, 10 AM – 6 PM, Ferry Building plaza tent. Bring a photo ID. No race-morning pickup.

RACE MORNING
- 5:45 AM: bag check opens (Marina Green, trucks by bib number)
- 6:00 AM: shuttles from Marina Green to the start every 10 minutes until 6:35
- 6:50 AM: corrals close
- 7:00 AM: start

AID STATIONS
Water and electrolyte drink at miles 2, 4, 6 (bridge turnaround), 8, 10 and 12. Gels at miles 6 and 10.

WEATHER
Typical mid-October morning: 54–60°F, fog near the bridge, light westerly wind. The return along Crissy Field is often into a headwind.

Results will be posted live and emailed to you after you finish.
""", html=True, att=[A('pdf', 'BAHM_2026_course_map_and_race_week_guide.pdf', [
    ('title', 'Bay Area Half Marathon 2026 — Race Week Guide'),
    ('p', 'Thursday, October 15, 2026 · Start 7:00 AM · Embarcadero at Mission St · Finish: Marina Green'),
    ('h2', 'Course (13.1 mi)'),
    ('table', [['Mile', 'Landmark', 'Notes'],
               ['0', 'Embarcadero at Mission St', 'Start, Corrals A–F'],
               ['2', "Fisherman's Wharf", 'Aid: water + electrolyte'],
               ['3', 'Fort Mason hill', 'Climb ~70 ft'],
               ['4', 'Marina Green', 'Aid'],
               ['5', 'Crissy Field', 'Flat, gravel shoulder on left'],
               ['6', 'Golden Gate Bridge, Vista Point turnaround', 'Aid + gels, bridge approach climb'],
               ['8', 'Crissy Field (return)', 'Aid, usually headwind'],
               ['10', 'Marina Blvd', 'Aid + gels'],
               ['11', 'Fort Mason hill (return)', 'Short climb'],
               ['12', 'Aquatic Park', 'Aid'],
               ['13.1', 'Marina Green', 'Finish, medals, recovery area']]),
    ('h2', 'Start area'),
    ('bullet', 'Corral A: sub-1:30 projected, enter from Mission St, closes 6:50 AM.'),
    ('bullet', 'Corral B: 1:30–1:45. Corrals C–F behind.'),
    ('bullet', 'Port-a-johns at Steuart St and Howard St.'),
    ('h2', 'Finish area'),
    ('bullet', 'Bag check trucks numbered by bib range. Truck 4: bibs 2001–2600.'),
    ('bullet', 'Medical tent at the west end of Marina Green.'),
    ('p', 'Course cutoff: 3 hours 30 minutes. Runners behind the 16:00/mi sweep will be asked to move to the sidewalk.'),
], 'BAHM 2026 Race Week Guide', 'Bay Area Half Marathon')]),
], labels=['Inbox', 'Races'], quote=False),

T('Packet pickup reminder + add race day to your calendar', ['project_endurance_training'], [
M('2026-10-13 08:30', RACE, ME_R, """
Hi David,

Packet pickup opens today at 11 AM at the Ferry Building plaza tent and runs through tomorrow (10 AM – 6 PM). Bib 2187 is at the Corral A table.

Your packet: bib with chip, four safety pins, gear-check bag tag (Truck 4), and your shirt (size M as selected).

A calendar invite for race morning is attached.
""", html=True, att=[A('ics', 'bay_area_half_2026_race_morning.ics', dict(
    summary='Bay Area Half Marathon — Corral A closes 6:50, start 7:00',
    start='2026-10-15 06:00', end='2026-10-15 09:30',
    location='Embarcadero at Mission St, San Francisco',
    description='Bib 2187, Corral A. Bag check Truck 4 at Marina Green (opens 5:45). Shuttles to start 6:00-6:35.',
    organizer=RACE, attendees=[ME_R]))]),
], labels=['Inbox', 'Races'], quote=False),

T('Your official result: 1:24:51 — Bay Area Half Marathon 2026', ['project_endurance_training'], [
M('2026-10-15 14:22', RACE_RESULTS, ME_R, """
Congratulations, David!

Your official result for the 2026 Bay Area Half Marathon:

Name | David Barron
Bib | 2187
Chip time | 1:24:51
Gun time | 1:24:58
Pace | 6:29 /mi
Overall place | 87 of 2,914
Gender place | 74 of 1,402
Division (M 20–24) | 9 of 143

SPLITS
5K | 20:12
10K | 40:16
15K | 1:00:22
20K | 1:20:28
Finish | 1:24:51

Your second half (42:21) was faster than your first half (42:30). Nicely paced.

Results may be updated during the next 48 hours while timing is reviewed. Download your finisher certificate from the results page.
""", html=True),
], labels=['Inbox', 'Races'], quote=False),

T('Your race photos are ready', ['project_endurance_training'], [
M('2026-10-17 10:05', RACE, ME_R, """
Hi David,

We found 6 photos of bib 2187 from the 2026 Bay Area Half Marathon: two at the Golden Gate Bridge turnaround (mile 6), one on Crissy Field (mile 8), and three in the finishing chute.

Photo package (all 6, digital) | $39.99
Single digital photo | $14.99
Free photo | finish-line medal shot, already unlocked

Photos stay available until November 15, 2026.
""", html=True),
], labels=['Inbox', 'Category Promotions'], quote=False),

# ======================= Owen Patel =======================
T('oakland lease signed + summer plan for the half', ['project_endurance_training'], [
M('2026-06-09 21:33', OWEN, ME_R, """
ok lease signed, temescal, 10 min from the new office. I land in oakland aug 1, start aug 3.

so we're both registered (BAHM26 confirmations from may), both projected corral A. question is what we do june-july before your block 4 starts. I'm thinking I keep 45-50 mi/week easy + strides, no workouts till august. you?

still going for 1:22.
"""),
M('2026-06-09 23:58', ME_R, OWEN, """
nice, temescal is a good spot. the hills behind it are going to wreck your easy days lol

same plan basically. 9-10h/week, all zone 2, strides twice a week, one longer run on saturdays (16-18). no speed till block 4 in august, then ~10 weeks of real work before oct 15. i put 1:25 as projected and i'm sticking with it

1:22 is a real goal for you. i'm not chasing you
"""),
M('2026-06-10 07:41', OWEN, ME_R, """
lol fair. once we're both out there we do the long runs together and I go off on my own for the workouts
"""),
], labels=['Inbox', 'Running']),

T('saturday: presidio loops?', ['project_endurance_training'], [
M('2026-08-19 20:15', OWEN_SF, ME_R, """
you're finally here! saturday long run: i've been doing a loop from crissy field up through the presidio (lover's lane, inspiration point, back down by baker beach). ~5.3 mi per loop with ~500 ft. 3 loops = 16.

meet 7:30 at the crissy field warming hut? there's parking but you're probably biking over
"""),
M('2026-08-19 22:40', ME_R, OWEN_SF, """
perfect, 16 is exactly what the plan says for saturday. i'll bike over, there's a rack by the warming hut right?

hr cap 150 still, but if the hills push me over on the inspiration point climb i'm not going to walk it
"""),
M('2026-08-20 07:02', OWEN_SF, ME_R, """
yeah racks right there. bring a jacket, it's 55 and foggy until 10 every day here. august in sf is a lie
"""),
], labels=['Inbox', 'Running']),

T('Marin long run sat 9/5 - ferry back?', ['project_endurance_training'], [
M('2026-09-01 19:50', ME_R, OWEN_SF, """
plan says 18 this saturday. idea: start at crissy field, over the bridge, down into sausalito, out to tennessee valley trailhead and back to sausalito, ferry home. ~18.4 by my map

ferry from sausalito leaves 11:05 and 12:20. if we start 7:15 we make the 11:05 easily

you in?
"""),
M('2026-09-01 21:12', OWEN_SF, ME_R, """
in. bring a card for the ferry, they don't take cash. also there's a water fountain at the tennessee valley lot but nothing between the bridge and sausalito so carry a bottle

i'll do the last 3 at marathon pace if i feel good, you do your thing
"""),
M('2026-09-06 13:40', ME_R, OWEN_SF, """
that was the best run of the year. 18.4 in 2:38, avg hr 148. legs fine today, did an easy 8

we're doing that again in october for the last long one before taper
"""),
], labels=['Inbox', 'Running']),

T('race plan - pacing sheet', ['project_endurance_training'], [
M('2026-09-18 22:05', ME_R, OWEN_SF, """
ok i made a pacing sheet for the half. attached. my plan: 6:32-6:35 for the first 3 (fort mason hill + crowded start), settle to 6:28 on crissy field, take the bridge climb by effort not pace, then whatever's left from mile 10.

goal 1:25:00, stretch 1:24:30. the 1:25 pacer starts in corral A too so i'll probably sit on him until the turnaround

yours has 6:16 avg for 1:22 — check the hill splits, i guessed
""", att=[A('xlsx', 'bahm_2026_pacing.xlsx', {
    'David 1h25 goal': [['Mile', 'Target pace', 'Cumulative', 'Note'],
                   [1, '6:34', '6:34', 'crowded start, Embarcadero'], [2, '6:32', '13:06', 'aid station'],
                   [3, '6:35', '19:41', 'Fort Mason hill'], [4, '6:28', '26:09', 'Marina Green'],
                   [5, '6:27', '32:36', 'Crissy Field, sit on 1:25 pacer'], [6, '6:38', '39:14', 'bridge climb by effort, gel'],
                   [7, '6:22', '45:36', 'downhill off bridge'], [8, '6:30', '52:06', 'Crissy headwind, draft'],
                   [9, '6:28', '58:34', ''], [10, '6:27', '1:05:01', 'gel, go from here'],
                   [11, '6:30', '1:11:31', 'Fort Mason hill'], [12, '6:24', '1:17:55', ''],
                   [13, '6:20', '1:24:15', 'everything left'], ['13.1', '0:40', '1:24:55', 'finish Marina Green']],
    'Owen 1h22 goal': [['Mile', 'Target pace', 'Cumulative', 'Note'],
                  [1, '6:20', '6:20', ''], [2, '6:16', '12:36', ''], [3, '6:18', '18:54', 'hill (guess)'],
                  [4, '6:14', '25:08', ''], [5, '6:13', '31:21', ''], [6, '6:22', '37:43', 'bridge (guess)'],
                  [7, '6:10', '43:53', ''], [8, '6:16', '50:09', 'headwind'], [9, '6:15', '56:24', ''],
                  [10, '6:14', '1:02:38', ''], [11, '6:18', '1:08:56', 'hill'], [12, '6:12', '1:15:08', ''],
                  [13, '6:08', '1:21:16', ''], ['13.1', '0:38', '1:21:54', '']],
    'Fueling': [['When', 'What'], ['4:50 AM', 'bagel + banana + coffee'], ['6:45 AM', 'gel #1 + water'],
                ['Mile 6', 'gel #2 (course gel)'], ['Mile 10', 'gel #3'], ['Every aid station', '2-3 sips electrolyte']],
}, 'BAHM 2026 pacing')]),
M('2026-09-19 08:30', OWEN_SF, ME_R, """
this is great. my hill splits are too optimistic, put 6:28 for mile 3 and 6:35 for mile 6. i'll make it back on the downhill off the bridge.

also the headwind on crissy field coming back is real every morning. draft off whoever you can between 7 and 9
"""),
], labels=['Inbox', 'Running'], quote=True),

T('wait when is your talk', ['project_endurance_training', 'project_tutortrace'], [
M('2026-10-04 18:22', OWEN_SF, ME_R, """
are you around for the tuesday workout this week or is that the conference week? also when is the talk and can i watch it

and explain what the paper is again like i'm a mech-e. last time you said "telemetry" and i zoned out
"""),
M('2026-10-04 20:47', ME_R, OWEN_SF, """
yeah conference week. talk is wed oct 7, 15 min + 5 min q&a, in the "learning & tutoring" session. i'm out tue–thu so let's move the workout to monday, 6x800 at kezar?

the paper (tutortrace): we logged what intro CS students do in their code editor (edits, runs, errors) plus when they ask the AI tutor for help. then 3 of us labeled 30-second windows as productive struggle / stalled / asking for help etc. agreement between raters was decent (kappa 0.71). the point is to tell an instructor which students are stuck in a bad way vs struggling in a useful way, without watching over their shoulder

reviewers pushed on whether it works beyond one course, so the camera ready has a cross-course analysis now. the talk is mostly that + a demo of the replay timeline

it's not streamed publicly, only for registered attendees. i'll send you the recording if they post it
"""),
M('2026-10-04 21:15', OWEN_SF, ME_R, """
ok that actually makes sense. monday kezar 6:30am works. good luck wednesday, don't do anything dumb with your legs the week before the race
"""),
], labels=['Inbox', 'Running'], notes='HARD CASE: second email account — runs@ thread with Owen that turns into an explanation of the TutorTrace UIST talk (cross-over into project_tutortrace)'),

T('race morning logistics', ['project_endurance_training'], [
M('2026-10-12 19:30', OWEN_SF, ME_R, """
race morning: i'll pick you up at 5:25 at the house, we park at the marina garage ($15 early bird), drop bags at truck 4, shuttle to the start by 6:15. corral closes 6:50.

pickup tuesday after work? ferry building tent is open till 7
"""),
M('2026-10-12 20:02', ME_R, OWEN_SF, """
5:25 works, i'll be outside. tuesday pickup at 6 works too, i'll meet you at the tent

breakfast plan: bagel + banana at 4:50, gel at 6:45 and at miles 6 and 10. no new shoes, no new food
"""),
], labels=['Inbox', 'Running']),

T('1:22:10!!!', ['project_endurance_training'], [
M('2026-10-15 16:40', ME_R, OWEN_SF, """
1:22:10!!! you absolutely nailed it. 52nd overall. the official results just came in

mine's 1:24:51. second half faster than the first which never happens to me. sat on the 1:25 pacer to the bridge then went at mile 10 like we said

recovery tacos tonight?
"""),
M('2026-10-15 17:05', OWEN_SF, ME_R, """
DUDE. sub 1:25 off a base block with almost no speed work. that's a 3:46 PR right?

tacos yes. 7:30, the place on irving. i can barely walk down stairs
"""),
M('2026-10-15 17:20', ME_R, OWEN_SF, """
3:46 yeah (1:28:37 last april). see you at 7:30. next one is the full in the spring, don't fight me on it
"""),
], labels=['Inbox', 'Running']),

# ======================= SF apartment / sublet search (Jul–Aug 2026) =======================
T('4 new listings match "Sunset / Richmond / Mission, under $2,200, Aug 1"', ['project_none'], [
M('2026-07-07 08:10', NEST, ME_R, """
New listings for your saved search

1. Room in 3BR, Inner Sunset (Irving & 9th) | $1,650/mo | Sublet Aug 1 – Oct 31 | furnished
2. Studio, Outer Richmond (Balboa & 34th) | $2,150/mo | 12-month lease, available Sep 1
3. Room in 4BR, Mission (Valencia & 20th) | $1,800/mo | month-to-month
4. Junior 1BR, Lower Haight | $2,195/mo | 12-month lease, available Aug 15

Tap a listing to message the poster. Listings under $2,000 in your search area are getting an average of 23 inquiries in the first 48 hours.
""", html=True),
], labels=['Inbox', 'Apartment'], quote=False),

T('Re: Inner Sunset room sublet (Aug 1 – Oct 31)', ['project_none'], [
M('2026-07-07 12:44', ME_R, JONAH, """
Hi Jonah,

I saw your listing on Nestlist for the furnished room at Irving & 9th, Aug 1 – Oct 31. I'm moving to SF from Virginia in early August for work (a startup incubator in the city) and I'd be interested.

A few questions:
- Is the start date flexible? I arrive Aug 8.
- Is the $1,650 including utilities and internet?
- Is there a place to keep a bike?

I'm a quiet housemate, no pets, don't smoke. Happy to do a video call.

Thanks,
David
"""),
M('2026-07-07 19:20', JONAH, ME_R, """
Hey David,

Aug 8 is fine, rent would be prorated for August ($1,280 for Aug 8–31). Utilities are split three ways, usually $70–90/mo, internet included. Bikes go in the garage.

Could you do a video tour Thursday at 6pm Pacific?

Jonah
"""),
M('2026-07-07 21:02', ME_R, JONAH, """
Thursday 6pm Pacific (9pm for me) works. I'll send a Google Meet link. Thanks!
"""),
M('2026-07-27 10:15', JONAH, ME_R, """
Hi David,

Bad news, sorry. I had to run the sublet past the leaseholder and the building manager won't approve sublets shorter than 6 months this year. So I can't do Aug–Oct. I should have checked before listing it.

I can refund the $200 you sent through Venmo today. Really sorry about the timing.

Jonah
"""),
M('2026-07-27 12:30', ME_R, JONAH, """
Hi Jonah, thanks for letting me know, I understand. Yes please refund the $200 to the same Venmo. Good luck with the room.

David
"""),
], labels=['Inbox', 'Apartment']),

T('3 new listings match "Sunset / Richmond / Mission, under $2,200, Aug 1"', ['project_none'], [
M('2026-07-14 08:12', NEST, ME_R, """
New listings for your saved search

1. Studio, Inner Richmond (Clement & 6th) | $2,095/mo | 12-month lease, available Sep 1 | Fogline Property Management
2. Room in 2BR, Outer Sunset (Judah & 42nd) | $1,550/mo | month-to-month, available now
3. Room in 5BR co-op house, Duboce Triangle | $1,400/mo | min 6 months, interview required

Price change: Junior 1BR, Lower Haight dropped from $2,195 to $2,095.
""", html=True),
], labels=['Inbox', 'Apartment'], quote=False),

T('Application received: 412 Clement St, Unit 3', ['project_none'], [
M('2026-07-16 15:05', FOGLINE, ME_R, """
Hi David,

Thank you for applying to 412 Clement St, Unit 3 (studio, $2,095/mo, available September 1). Your application ID is FPM-26-0716-118.

To finish screening we need:
1. Proof of income: an offer letter or two recent pay stubs showing at least 2.5x monthly rent ($5,237.50/mo)
2. A copy of a government photo ID
3. The $45 screening fee (paid through the resident portal)

Since you're relocating from out of state, a letter from your employer or a bank statement showing 6 months of rent in savings also works.

Best,
Carla
Leasing Coordinator, Fogline Property Management
"""),
M('2026-07-16 22:40', ME_R, FOGLINE, """
Hi Carla,

Thanks. I've paid the screening fee and uploaded my ID through the portal. For income: I'm co-founding a company and my university stipend ends Aug 15, so I'll send a bank statement showing savings instead of pay stubs. Uploading that tomorrow.

One question: the listing says September 1. Is there any chance of an earlier move-in? I arrive in SF on August 8.

Best,
David Barron
"""),
M('2026-07-17 11:18', FOGLINE, ME_R, """
Hi David,

Got the statement, thank you. Unfortunately Sept 1 is firm because the unit is being repainted and the floors refinished during August.

I'll let you know as soon as screening is complete (usually 2–3 business days).

Carla
"""),
M('2026-07-21 14:02', FOGLINE, ME_R, """
Hi David,

Good news: you're approved for 412 Clement St, Unit 3. To hold the unit we need a $500 holding deposit by Friday 7/24 (applied to your security deposit at signing). The draft lease is attached for your review. Lease start September 1, 2026, 12 months.

Carla
""", att=[A('pdf', 'DRAFT_Lease_412_Clement_Unit3.pdf', [
    ('title', 'Residential Lease Agreement — DRAFT'),
    ('p', 'Fogline Property Management · 412 Clement St, Unit 3, San Francisco, CA 94118'),
    ('table', [['Term', 'Value'],
               ['Tenant', 'David Barron'],
               ['Lease term', 'September 1, 2026 – August 31, 2027 (12 months)'],
               ['Monthly rent', '$2,095.00, due on the 1st'],
               ['Security deposit', '$2,095.00 (holding deposit of $500 applied)'],
               ['Late fee', '$50 after the 5th of the month'],
               ['Utilities', 'Tenant pays electricity and internet; water/garbage included'],
               ['Pets', 'Not permitted without written addendum'],
               ['Bike storage', 'Shared basement room, one bike per unit']]),
    ('h2', '1. Use and occupancy'),
    ('p', 'The premises shall be used only as a private residence for the Tenant named above. Guests staying more than 14 days in any 6-month period require written consent.'),
    ('h2', '2. Early termination'),
    ('p', 'Tenant may terminate early with 60 days written notice and payment of one month of rent as a lease-break fee.'),
    ('h2', '3. Holding deposit'),
    ('p', 'The $500 holding deposit is refundable in full if Tenant withdraws in writing before signing this lease and before August 7, 2026. After that date it is non-refundable.'),
    ('h2', '4. Move-in inspection'),
    ('p', 'Landlord and Tenant will complete a move-in inspection checklist within 3 days of move-in.'),
], 'Draft lease 412 Clement Unit 3', 'Fogline Property Management')]),
M('2026-07-30 16:55', ME_R, FOGLINE, """
Hi Carla,

Thank you for approving me and for being so responsive. I've decided to withdraw my application for 412 Clement St, Unit 3. A furnished room in a shared house tied to my work came through for August onward, and I'd rather not commit to a 12-month lease right now.

Per section 3 of the draft lease, I'm withdrawing before signing and before August 7, so could you please refund the $500 holding deposit to the card on file?

Sorry for the back-and-forth, and thanks again.

Best,
David Barron
"""),
M('2026-07-31 10:20', FOGLINE, ME_R, """
Hi David,

Understood, and thanks for letting us know quickly. I've withdrawn the application and requested the $500 refund. You'll get a confirmation from our payments team; it usually posts in 5–7 business days.

Best of luck with the move,
Carla
"""),
], labels=['Inbox', 'Apartment']),

T('Payment receipt: Holding deposit — 412 Clement St, Unit 3', ['project_none'], [
M('2026-07-22 09:41', FOGLINE_PAY, ME_R, """
Payment received. Thank you.

Receipt number | FPM-PAY-2026-073319
Property | 412 Clement St, Unit 3
Description | Holding deposit (applied to security deposit at lease signing)
Amount | $500.00
Payment method | Visa ending 4471
Date | July 22, 2026 9:41 AM ET

A PDF copy of this receipt is attached for your records.
""", html=True, att=[A('pdf', 'Receipt_FPM-PAY-2026-073319.pdf', [
    ('title', 'Payment Receipt'),
    ('p', 'Fogline Property Management · Resident Payments'),
    ('table', [['Field', 'Value'],
               ['Receipt number', 'FPM-PAY-2026-073319'],
               ['Payer', 'David Barron'],
               ['Property', '412 Clement St, Unit 3, San Francisco, CA 94118'],
               ['Description', 'Holding deposit'],
               ['Amount', '$500.00'],
               ['Method', 'Visa ending 4471'],
               ['Date', '2026-07-22']]),
    ('p', 'Holding deposits are refundable per the terms of the lease agreement.'),
], 'Receipt FPM-PAY-2026-073319', 'Fogline Property Management')]),
M('2026-08-05 13:15', FOGLINE_PAY, ME_R, """
Refund issued.

Refund number | FPM-REF-2026-080517
Original receipt | FPM-PAY-2026-073319
Amount | $500.00
Refunded to | Visa ending 4471
Reason | Application withdrawn before lease signing

Refunds typically appear on your statement within 5–7 business days.
""", html=True),
], labels=['Inbox', 'Apartment'], quote=False),

T('Booking confirmed: Blacksburg, VA → San Francisco, CA (CH-58213)', ['project_none'], [
M('2026-07-29 11:30', CRATE, ME_R, """
Hi David,

Your shipment is booked.

Booking | CH-58213
Pickup | Mon Aug 3, 2026, 8 AM – 12 PM, Blacksburg, VA
Delivery window | Aug 10 – Aug 14, 2026, San Francisco, CA 94122
Items | 14 medium boxes, 1 bike box (road bike, wheels off), 1 desk chair
Declared value | $3,800
Total | $684.00 (paid)

Your bill of lading and packing checklist are attached. Please have every box labeled with your booking number on two sides.
""", html=True, att=[A('pdf', 'CH-58213_bill_of_lading.pdf', [
    ('title', 'Crate & Haul — Bill of Lading'),
    ('p', 'Booking CH-58213 · Shipper/Consignee: David Barron'),
    ('table', [['#', 'Item', 'Qty', 'Est. weight (lb)'],
               ['1', 'Medium box (18x18x16)', '14', '420'],
               ['2', 'Bike box (road bike, wheels removed, pedals off)', '1', '38'],
               ['3', 'Desk chair (wrapped)', '1', '32'],
               ['', 'Total', '16', '490']]),
    ('h2', 'Packing checklist'),
    ('bullet', 'Label each box with CH-58213 on two sides.'),
    ('bullet', 'No batteries over 100 Wh, no aerosols, no liquids over 1 gallon.'),
    ('bullet', 'Bike: deflate tires to 30 psi, remove pedals, protect derailleur hanger.'),
    ('bullet', 'Photograph valuable items before pickup for any damage claim.'),
    ('p', 'Liability: $3,800 declared value. Claims must be filed within 9 days of delivery.'),
], 'Bill of lading CH-58213', 'Crate & Haul Shipping')]),
M('2026-08-03 12:48', CRATE, ME_R, """
Picked up: booking CH-58213

Your 16 items were picked up at 11:52 AM in Blacksburg, VA. Tracking will update when your shipment reaches our Sacramento hub.

Delivery window: Aug 10 – Aug 14.
""", html=True),
M('2026-08-12 15:20', CRATE, ME_R, """
Delivered: booking CH-58213

16 of 16 items were delivered at 3:02 PM. Signed by: D. BARRON.

If any item arrived damaged, file a claim within 9 days (by Aug 21) from your booking page.
""", html=True),
], labels=['Inbox', 'Apartment'], quote=False),

T('welcome to the house + move-in stuff', ['project_none'], [
M('2026-08-05 20:10', SAM, ME_R, """
hey david, sam here, i'm one of the housemates at the incubator house. lena said you're getting in saturday the 8th. some move-in stuff so you're not surprised:

- you're in room 3 (second floor, back). bed, desk, dresser, no chair (desk chairs are a fight, bring one if you can)
- bring towels, the house ones vanished in june
- door code gets texted to you the morning you arrive
- garage has bike hooks, 2 are free
- quiet hours 11pm–7am on weeknights, people take calls late though
- groceries: shared staples (oil, rice, eggs, coffee) on a splitwise, everything else is yours. label your stuff in the fridge
- recycling/compost go out tuesday night

also heard you run. a few of us do a slow 5 mi to ocean beach on wednesday mornings at 7 if you want in
"""),
M('2026-08-05 22:35', ME_R, SAM, """
this is super helpful, thank you. my desk chair is literally on a truck right now (arrives ~aug 10-14) so i'm covered

landing at SFO ~10am saturday, should be at the house by noon. and yes to the wednesday run, i'm doing mostly easy volume right now so 5 mi slow is perfect
"""),
], labels=['Inbox', 'Apartment']),

T('Your saved search "Sunset / Richmond / Mission, under $2,200" has been paused', ['project_none'], [
M('2026-08-09 09:00', NEST, ME_R, """
Hi David,

We paused your saved search "Sunset / Richmond / Mission, under $2,200, Aug 1" because you haven't opened an alert in 10 days.

You received 41 matching listings since July 2 and contacted 6 posters.

Found a place? Congrats. If not, resume alerts any time from your dashboard.
""", html=True),
], labels=['Category Updates'], quote=False),

T('Moving out of Blacksburg — utility and mail checklist', ['project_none'], [
M('2026-08-01 23:40', ME_R, ME_R, """
note to self (moving checklist, update as i go)

done
- crate & haul booked (CH-58213), pickup mon aug 3 8-12
- fogline application withdrawn, $500 refund requested
- flight IAD -> SFO sat aug 8, 7:05am, bag + bike? no, bike goes on the truck

todo
- USPS change of address effective aug 8 -> house address (get from lena)
- cancel blacksburg electric, final read aug 7
- internet return: modem to the store by aug 6 or $150 fee
- renter's insurance: cancel aug 8, new policy for SF room?
- car: sell or ship? decided: sell. buyer picks up aug 6, $6,400, title signed at DMV
- DMV: CA license within 10 days of becoming resident
- return library books (2)
- last huckleberry run fri aug 7
"""),
], labels=['Inbox']),

# ======================= Niamh's wedding (Dublin, 2026-07-11) =======================
T('wedding hotel block + the weekend plan', ['project_none'], [
M('2026-06-03 13:15', NIAMH, ME_R, """
Hi David!

So glad you're coming. Practical bits for the weekend of the 11th:

Hotel block: The Harcourt Rooms, near St Stephen's Green. Rate is EUR 165/night incl. breakfast if you book by 12 June. Use the code BARRON-JULY when you ring them or in the "special requests" box online.

Schedule
- Fri 10 July, 7pm: welcome drinks at the hotel bar, very casual
- Sat 11 July, 2pm: ceremony, then dinner and dancing at the venue (coaches from the hotel at 1:15)
- Sun 12 July, 11am: brunch for whoever survives

Dress code is "summer formal", so a suit but no tie needed.

Can you let me know your flights when you have them so I can sort the coach list?

Love,
Niamh
"""),
M('2026-06-03 21:50', ME_R, NIAMH, """
Hi Niamh,

Booked the Harcourt with the code, Fri 10 and Sat 11 (2 nights). Flights: landing Dublin Fri 10 July 7:35am, leaving Mon 13 July 12:50pm. I'll send the itinerary once it's issued.

Count me on the Saturday coach. Can't wait.

David
"""),
M('2026-06-04 08:12', NIAMH, ME_R, """
Perfect, you're on coach 1. If you're up early Saturday there's a parkrun in the Phoenix Park at 9:30, Mam said you'd want to know :)
"""),
], labels=['Inbox']),

T('Your itinerary: Washington Dulles (IAD) – Dublin (DUB), booking reference QK7M2R', ['project_none'], [
M('2026-06-05 10:22', AIRLINE, ME_R, """
Dear Mr Barron,

Thank you for booking with Emerald Atlantic. Your e-ticket is issued.

Booking reference | QK7M2R
Passenger | David Barron
Outbound | EA 118 · Thu 9 Jul 2026 · IAD 18:40 → DUB 07:35 (+1) · Economy
Return | EA 119 · Mon 13 Jul 2026 · DUB 12:50 → IAD 15:25 · Economy
Baggage | 1 x 23 kg checked, 1 x 7 kg cabin
Total paid | USD 812.40

Your itinerary receipt is attached. Online check-in opens 24 hours before departure.
""", html=True, att=[A('pdf', 'EA_itinerary_QK7M2R.pdf', [
    ('title', 'Emerald Atlantic Airways — Itinerary Receipt'),
    ('p', 'Booking reference QK7M2R · Issued 5 June 2026'),
    ('table', [['Flight', 'Date', 'From', 'To', 'Departs', 'Arrives', 'Seat'],
               ['EA 118', 'Thu 09 Jul 2026', 'Washington Dulles (IAD)', 'Dublin (DUB)', '18:40', '07:35 +1', '31C'],
               ['EA 119', 'Mon 13 Jul 2026', 'Dublin (DUB)', 'Washington Dulles (IAD)', '12:50', '15:25', '28D']]),
    ('table', [['Fare item', 'USD'], ['Base fare', '548.00'], ['Taxes, fees and charges', '264.40'], ['Total', '812.40']]),
    ('p', 'US preclearance is available in Dublin for EA 119. Allow 2 hours 30 minutes before departure.'),
], 'Itinerary QK7M2R', 'Emerald Atlantic Airways')]),
], labels=['Inbox', 'Category Updates'], quote=False),

T('thank you + photos!', ['project_none'], [
M('2026-07-16 14:30', NIAMH, ME_R, """
David,

Thank you so much for coming all that way, and for the very generous gift. It meant a lot to have you there (and you were the only one who did the parkrun Saturday morning, legend).

The photographer's gallery is up. Password is the wedding date, 110726. There are some great ones of you and Granda at the dinner, numbers 212 to 230.

We're in Lisbon until the 25th and then back to real life.

Love,
Niamh
"""),
M('2026-07-16 22:05', ME_R, NIAMH, """
Niamh, it was such a great weekend, thank you for having me. The photos of Granda are gold, I downloaded 214 and 221.

Enjoy Lisbon. Heads up that I'm moving to San Francisco on Aug 8, so I'll send my new address for anything that would come by post.

David
"""),
], labels=['Inbox']),

# ======================= Google security =======================
T('Security alert: new sign-in on Mac', ['project_none'], [
M('2026-08-04 16:42', GSEC, ME_R, """
A new sign-in on Mac

david.barron.runs@gmail.com

We noticed a new sign-in to your Google Account on a Mac device (Chrome, Blacksburg, VA, USA) on August 4, 2026 at 4:41 PM EDT. If this was you, you don't need to do anything. If not, we'll help you secure your account.

Check activity: myaccount.google.com/notifications

You received this email to let you know about important changes to your Google Account and services.
""", html=True),
], labels=['Inbox', 'Category Updates'], quote=False),

# ======================= chess.com =======================
T('It\'s your move against kfischer_nrv (Daily, 3 days/move)', ['project_none'], [
M('2026-06-17 07:30', CHESS, ME_R, """
kfischer_nrv played 14...Nxe4 in your Daily game.

Opening: Sicilian Defense, Najdorf, English Attack
Time left to move: 2 days 23 hours
Your Daily rating: 1712

You have 3 games waiting for your move. Vacation time remaining this year: 14 days.
""", html=True),
], labels=['Category Social'], quote=False),

T('Your August on Chess.com', ['project_none'], [
M('2026-09-02 09:00', CHESS, ME_R, """
Your August on Chess.com

Games played | 61 (Rapid 38 · Blitz 19 · Daily 4)
Rapid rating | 1648 (+37)
Blitz rating | 1491 (−12)
Puzzles solved | 214 · Puzzle rating 2105
Best win | vs. 1802-rated opponent, Rapid 10|0, Aug 23 (Queen's Gambit Declined, Exchange)
Most played opening | Queen's Gambit (as White), Caro-Kann (as Black)

You played most often between 10 PM and midnight. Your accuracy is 6 points higher in games before 10 PM.
""", html=True),
], labels=['Category Social'], quote=False),

T('Congrats! New Rapid rating high: 1,701', ['project_none'], [
M('2026-09-29 23:48', CHESS, ME_R, """
You just reached a new personal best in Rapid: 1,701.

The game that did it: Rapid 10|0 vs. bayside_bishop (1688), won in 41 moves. Caro-Kann, Advance Variation. Accuracy 88.4.

Next milestone: 1,750. You're in the top 6.2% of Rapid players.
""", html=True),
], labels=['Category Social'], quote=False),

# ======================= The Long Game (strategy newsletter) =======================
T('The Long Game #74 — The silicon shield is a wasting asset', ['project_none'], [
M('2026-06-14 06:00', LONGGAME, ME_R, """
The Long Game · Strategy weekly · Issue 74

THE SILICON SHIELD IS A WASTING ASSET

For a decade the comfortable argument about the Taiwan Strait went like this: the world's most advanced chips are made on one island, so no one, Beijing included, can afford a war that stops the fabs. Deterrence by indispensability.

Three things are eroding that argument, slowly and all at once.

First, the fabs are moving, a little. The new plants in Arizona, Kumamoto and Dresden will not match Hsinchu's leading node for years, but they change the question from "no advanced chips at all" to "fewer and more expensive chips for a while". That is a cost governments can imagine absorbing.

Second, Beijing has spent five years building a domestic supply at the older nodes that cars, appliances and most weapons actually use. Its leverage on mature chips is growing as its dependence on the leading edge stays.

Third, the shield was always partly a story Washington told itself. Indispensability deters only if the other side values the same thing you do, at the same moment you need it to.

None of this makes conflict likely next year. It means the margin of safety comes from something other than economics: forces, alliances, and the patience of everyone involved. The question for the next decade is whether those are being built as fast as the shield is wearing thin.

Reading this week
- Two long reads on Japan's southwestern island defence buildup
- A data piece on mature-node capacity, 2020 vs 2026

Forward to a friend who still thinks TSMC is a peace plan.
""", html=True, unread=True),
], labels=['Category Promotions'], quote=False),

T('The Long Game #80 — Middle powers and the art of not choosing', ['project_none'], [
M('2026-07-26 06:00', LONGGAME, ME_R, """
The Long Game · Strategy weekly · Issue 80

MIDDLE POWERS AND THE ART OF NOT CHOOSING

A useful habit when reading the news: count the governments that refuse to pick a side and are rewarded for it.

India buys discounted oil from one camp and joins naval exercises with the other. The Gulf states host American bases, sell energy to China, and broker talks no one else can. Turkey sits inside NATO and outside its consensus. Indonesia, Brazil and South Africa each have their own versions.

This used to be called non-alignment and was treated as a stance of weakness. Today it looks more like arbitrage. When two large powers compete for partners, the partners can charge for their attention: technology transfer, investment, arms on better terms, a quieter voice on human rights.

Three implications follow.

1. Coalitions will be thinner and more transactional. Expect "minilaterals" built around a single task (undersea cables, critical minerals, a shipping lane) instead of grand alliances.
2. The price of loyalty rises. Any great power that asks for exclusivity will have to pay for it, and both are reluctant.
3. Arbitrage has limits. If competition turns into crisis, fence-sitters lose leverage fast because the large powers stop bidding and start demanding.

The comfortable middle exists because the competition is still managed. Watch the hedgers. When they start choosing, the era has changed.

Reading this week
- A long profile of Gulf sovereign wealth funds' Asia strategy
- An old essay on Nehru's non-alignment, which reads differently now
""", html=True),
], labels=['Category Promotions'], quote=False),

T('The Long Game #85 — The Arctic is a shipping story, not a military one (yet)', ['project_none'], [
M('2026-08-30 06:00', LONGGAME, ME_R, """
The Long Game · Strategy weekly · Issue 85

THE ARCTIC IS A SHIPPING STORY, NOT A MILITARY ONE (YET)

Every summer brings a new round of Arctic alarm: bases reopened, icebreakers launched, flags planted. Most of it misreads the region.

The Northern Sea Route carried a record tonnage last season, but that still amounts to a rounding error next to the Suez Canal. Insurance is expensive, the season is short, and the route depends on Russian escorts and Russian permission. For shippers it is an option, not a highway.

What is new is who is buying the option. Chinese carriers now make up most of the non-Russian transits, and Beijing's "Polar Silk Road" language has quietly turned into ice-class hulls and port investment. Russia needs the cargo and the capital; China wants a route that bypasses the Malacca Strait. Their interests overlap, but they are not identical. Moscow is wary of anyone else gaining standing in waters it considers its own.

For the West the useful questions are practical. Who builds icebreakers (the US has two working heavy ones)? Who maps the seabed? Who insures the ships? Strategic competition in the Arctic will be decided by these boring capacities long before it is decided by deployments.

The military story will come. The shipping story is already here.

Reading this week
- A shipbuilding analyst on why icebreakers take a decade
- Satellite imagery of new Arctic port works, annotated
""", html=True, unread=True),
], labels=['Category Promotions'], quote=False),

T('The Long Game #89 — Shipyards are the new aircraft carriers', ['project_none'], [
M('2026-09-27 06:00', LONGGAME, ME_R, """
The Long Game · Strategy weekly · Issue 89

SHIPYARDS ARE THE NEW AIRCRAFT CARRIERS

Military balance is usually counted in ships, planes and missiles. A better leading indicator is the capacity to build and repair them.

The numbers are lopsided. China's commercial shipyards launch more tonnage in a year than the United States has in decades, and the same yards, workers and supply chains can build warships. American naval construction is slower, more expensive and concentrated in a few yards with long backlogs. Repair is worse: ships wait months for drydock slots.

This matters for a simple reason. Wars between peers become wars of attrition, and attrition rewards the side that can replace losses. A fleet that cannot be repaired or replaced is a fleet that has to be hoarded, and a hoarded fleet deters less.

What would fixing it look like? Allies help: South Korea and Japan have world-class yards and an interest in using them. Workforce matters more than money; welders and pipefitters are the binding constraint. And procurement must allow simpler ships built in larger numbers, rather than a few exquisite ones.

Industrial policy debates often sound like economics. In shipbuilding, they are strategy.

Reading this week
- A visit to a Korean shipyard by a defense reporter
- A history of the Liberty ships and what they can and cannot teach us

Next issue: the October edition takes a week off. Back on Oct 11.
""", html=True),
], labels=['Category Promotions'], quote=False),

# ======================= Stride & Base (running magazine) =======================
T('Stride & Base: Zone 2 is a tool, not a religion', ['project_endurance_training'], [
M('2026-06-25 07:00', STRIDE, ME_R, """
Stride & Base · Weekly for patient runners

ZONE 2 IS A TOOL, NOT A RELIGION

Easy running has had a great few years. Talk-test pace, nasal breathing, heart-rate caps: the message that most of your miles should be easy has finally stuck. Good. Now for the caveats.

1. Zone 2 is a range, not a number. Lab tests put the first lactate threshold anywhere from 65 to 80 percent of max HR depending on the runner. A 150 bpm cap that works for one person is junk miles or overreach for another. If you can, get tested once; if not, use a 30-minute time trial and the talk test together.

2. Drift is real. On hot days or late in long runs your heart rate climbs at the same pace. Slowing down to hold the cap is fine. Walking every hill to hold it is usually not; a few minutes above the line won't erase the session.

3. Base building is a phase, not an identity. After 12 to 20 weeks of mostly easy volume, most runners benefit more from adding one quality session a week than from adding another hour of easy running.

THIS WEEK'S SESSION
The "base-builder's tempo": 3 x 10 minutes at a comfortably hard effort (you can speak in short phrases), 2 minutes easy between. Once a week, for four weeks, before any real speed work.

FROM THE MAILBAG
"Does cycling count toward my running base?" Yes, for the aerobic system. No, for the tendons and bones that running loads. Keep at least 70% of your aerobic time on your feet if running is the goal.
""", html=True),
], labels=['Category Promotions'], quote=False),

T('Stride & Base: Fog, heat and the summer you actually have', ['project_endurance_training'], [
M('2026-08-13 07:00', STRIDE, ME_R, """
Stride & Base · Weekly for patient runners

FOG, HEAT AND THE SUMMER YOU ACTUALLY HAVE

Half our readers are sweating through 90-degree mornings. The other half live somewhere coastal and are wearing gloves in August. Both groups ask the same question: does this weather ruin my training?

If it's hot: heat costs you roughly 1 to 3 percent of pace per 10°F above 60°F, more if it's humid. Run by effort, accept the slower splits, and drink to thirst plus some sodium on runs over 75 minutes. Ten to fourteen days of regular heat exposure brings real adaptations (more plasma volume, earlier sweating), which pay off on cooler race days.

If it's cool and foggy: lucky you, but don't skip hydration just because you don't feel hot. And if you're racing somewhere warmer this fall, two or three sessions a week in extra layers or a warm gym will get you part of the heat adaptation.

If you just moved between the two: give yourself a week. New hills, new routes, new sleep. A drop in pace in week one is not lost fitness.

THIS WEEK'S SESSION
Hill strides: 8 x 20 seconds up a moderate grade at strong but relaxed effort, walk down. After an easy run, twice a week.

GEAR NOTE
Our long-term test of three daily trainers is out next week. Spoiler: the cushioned one wore out at 310 miles.
""", html=True, unread=True),
], labels=['Category Promotions'], quote=False),

T('Stride & Base: How to taper without losing your mind', ['project_endurance_training'], [
M('2026-09-24 07:00', STRIDE, ME_R, """
Stride & Base · Weekly for patient runners

HOW TO TAPER WITHOUT LOSING YOUR MIND

The taper is when all the hard work turns into speed, and it's when runners feel worst. Legs feel heavy, every twinge seems serious, and the urge to "test fitness" is strong. Some guidelines:

- Length: 10 to 14 days for a half marathon, 2 to 3 weeks for a marathon.
- Volume: cut it by 30 to 50 percent, gradually. Keep the frequency, so run as many days, just shorter.
- Intensity: keep it. A short session at race pace or faster 4 to 5 days before the race keeps the legs sharp. Example: 6 x 800m at 10K pace with full recovery.
- Sleep and food: more of the first, normal amounts of the second. Many runners undereat in taper week and feel flat.
- Nothing new: shoes, gels, breakfast, socks. Everything on race day should be something you've done before.

The flat, heavy feeling in the first week of taper is common and usually gone by the final days. Trust the block.

RACE-DAY PACING
For a half, aim to run the first 5K 5 to 10 seconds per mile slower than goal pace, settle in through 15K, and then race the last 10 minutes. Negative splits are rarely an accident.

READER RESULTS
Send us your fall race result and one thing you'd change about your build. We publish the best ones in November.
""", html=True),
], labels=['Category Promotions'], quote=False),

# ======================= receipts =======================
T('Your Fuel Lab order #FL-208841 has shipped', ['project_endurance_training'], [
M('2026-06-11 14:05', FUEL, ME_R, """
Thanks for your order, David. It's on its way.

Order | #FL-208841
Ship to | Blacksburg, VA 24060
Carrier | UPS Ground, est. delivery Mon Jun 15

Item | Qty | Price
Electrolyte Drink Mix, Lemon, 30 servings | 2 | $49.98
Endurance Gel, Salted Caramel, 24-pack | 1 | $38.00
Whey Isolate, Unflavored, 2 lb | 1 | $54.99
Subtotal | | $142.97
Subscribe & save (10%) | | -$14.30
Shipping | | $0.00
Tax | | $7.72
Total | | $136.39

Your next subscription delivery: August 11, 2026. Change your address before then if you're moving.
""", html=True),
], labels=['Inbox', 'Category Updates'], quote=False),

T('Order confirmation: Ridgeline Running Co. #RRC-77302', ['project_endurance_training'], [
M('2026-08-19 18:22', SHOES, ME_R, """
Thanks for shopping with Ridgeline Running Co. (Irving St store)

Order | #RRC-77302
Date | Aug 19, 2026, 6:20 PM
Fitter | Ana at the Irving St store (gait analysis done)

Item | Size | Price
Daily trainer, neutral, 8 mm drop (black/volt) | M 10 | $140.00
Daily trainer, neutral, 8 mm drop (grey/blue) | M 10 | $140.00
Merino crew socks, 3-pack | L | $36.00
Run club discount (15%) | | -$47.40
Tax (8.625%) | | $23.07
Total | | $291.67

Rotate the two pairs to extend their life. Most trainers last 300 to 500 miles. Returns accepted within 60 days, even if worn.
""", html=True),
], labels=['Inbox', 'Category Updates'], quote=False),

T('Your race-day shoes are ready for pickup (#RRC-81955)', ['project_endurance_training'], [
M('2026-09-30 11:10', SHOES, ME_R, """
Hi David,

Your special order is in.

Order | #RRC-81955
Item | Carbon-plate racer, half/full marathon (white/orange), M 10
Price | $250.00 (paid)
Pickup | Irving St store, held until Oct 14

Our advice for a race on Oct 15: pick them up this week and do at least two runs in them before race day, one easy and one with some race-pace miles.
""", html=True),
M('2026-10-01 19:48', ME_R, SHOES, """
Hi, I'll pick them up tomorrow (Fri Oct 2) after 5. Thanks!

David
"""),
], labels=['Inbox', 'Category Updates'], quote=False),

# ======================= music =======================
T('Your Loopforge receipt — Lo-Fi Drum Rooms Vol. 3', ['project_music_production'], [
M('2026-07-07 23:51', LOOPFORGE, ME_R, """
Thanks for your purchase!

Receipt | LF-1931-0707
Item | Lo-Fi Drum Rooms Vol. 3 (WAV, 24-bit) | $24.99
Item | Dusty Keys One-Shots | $14.99
Discount code SUMMER20 | -$8.00
Total | $31.98

What's inside Lo-Fi Drum Rooms Vol. 3: 212 drum loops (70–94 BPM), 160 one-shots recorded in three rooms (tape, spring reverb, dry), plus FL Studio and Ableton kit presets.

Download links stay active for 5 downloads or 1 year.
""", html=True),
], labels=['Category Promotions'], quote=False),

T('Waveyard Audio: your license for Tapehead Saturator', ['project_music_production'], [
M('2026-09-13 00:22', WAVEYARD, ME_R, """
Hi David,

Thank you for buying Tapehead Saturator v2.1.

Order | WY-55028
Price | $29.00 (intro price, regular $49)
Formats | VST3 / AU / AAX, macOS 12+ (Apple silicon native)
Activations | 2 machines

License key: delivered in your Waveyard account under Products > Licenses.

Getting started in FL Studio: rescan plugins (Options > Manage plugins > Find more plugins), then add Tapehead to a mixer insert. Start with the "Cassette 90" preset on drum buses.
""", html=True),
], labels=['Category Promotions'], quote=False),

# ======================= Kevin Liu (recruiter) =======================
T('Founding engineer role — dev tools, Series A, SF', ['project_none'], [
M('2026-09-15 10:05', KEVIN, ME_R, """
Hi David,

Following up from my note earlier this year. I saw you've moved to SF, congrats!

Stackforge just closed a $14M Series A and we're hiring our second founding engineer: build our code-review agent end to end (TypeScript, Rust for the indexer, lots of LLM eval work). Team of 9, office in SoMa, 4 days in person.

Comp: $185–215k base + 0.5–0.9% equity.

Would you be open to a 20-minute call this week?

Best,
Kevin Liu
Head of Talent, Stackforge
"""),
M('2026-09-15 21:40', ME_R, KEVIN, """
Hi Kevin,

Thanks for thinking of me, and congrats on the round. I'm not looking right now: I'm co-founding a company myself (on leave from my PhD), so I'm fully committed there.

Best of luck with the hire.

David
"""),
M('2026-09-16 08:12', KEVIN, ME_R, """
Totally understand, and congrats! If you ever want to compare notes on hiring engineers in SF, I'm happy to share what we've learned. Good luck!

Kevin
"""),
], labels=['Inbox']),

# ======================= Sam (house) =======================
T('sat ride - hawk hill + paradise loop?', ['project_endurance_training'], [
M('2026-09-10 21:15', SAM, ME_R, """
you said you wanted a long easy ride this weekend. i'm doing hawk hill then the paradise loop on saturday, ~38 mi, mostly chill except hawk hill. leaving the house 8am

your bike survived the shipping right?
"""),
M('2026-09-10 22:02', ME_R, SAM, """
bike survived, just had to re-true the rear wheel a bit. saturday's my long run day though, can we do sunday? if not i'll join for just the loop part and keep it easy, plan has 2h ride on sunday
"""),
M('2026-09-11 07:30', SAM, ME_R, """
sunday 8am works, same route. bring 2 bottles, nothing open in tiburon before 9
"""),
], labels=['Inbox']),
]
