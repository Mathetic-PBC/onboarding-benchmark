"""Synthetic local files on David's Mac (PERSON.md): home-relative layout with zips (FL Studio project, UIST talk assets),
CSV exports (Strava, Garmin sleep, course data), an .ics travel export, JSON configs, a Brewfile, PIL screenshots, receipt
PDFs, a vague-titled invoice, a lease summary .docx, a PGN and a WAV. Deterministic; rebuilds synthetic/local-files/."""
import csv, io, math, os, random, re, struct, sys, wave, zipfile
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('local-files')
MOD = 'authentic/local-files home-relative file on the Mac'


def acct(rel):
    return rel.split('/')[0] if '/' in rel else rel


def meta(rel, pids, notes='', modeled_on=MOD):
    return dict(account=acct(rel), project_ids=pids, modeled_on=modeled_on, notes=notes)


def fix_office(data, modified):
    mod = dt(modified).astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    zin = zipfile.ZipFile(io.BytesIO(data)); out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            b = zin.read(it.filename)
            if it.filename == 'docProps/core.xml':
                x = b.decode()
                x = re.sub(r'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', lambda m_: m_.group(1) + mod + m_.group(2), x)
                x = re.sub(r'<dc:description>generated[^<]*</dc:description>', '<dc:description/>', x)
                b = x.encode()
            zi = zipfile.ZipInfo(it.filename, date_time=dt(modified).timetuple()[:6])  # no save-time leak, deterministic
            zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = it.external_attr
            zout.writestr(zi, b)
    return out.getvalue()


def csv_text(rows):
    b = io.StringIO(); w = csv.writer(b, lineterminator='\n'); w.writerows(rows); return b.getvalue()


# ---------------- PIL drawings ----------------

def _fonts():
    from PIL import ImageFont
    try:
        return ImageFont.load_default(size=16), ImageFont.load_default(size=22)
    except TypeError:
        f = ImageFont.load_default(); return f, f


ASC = {'—': '-', '←': '<-', '→': '->', '■': '#', '▲': '^', '◆': '*', '░': '.', '□': '.'}


def asc(t):
    """the default PIL font has no glyphs for these, draw ASCII stand-ins"""
    for a, b in ASC.items(): t = t.replace(a, b)
    return t


def png_boxes(title, boxes, arrows=(), size=(1000, 560), chrome=True):
    from PIL import Image, ImageDraw
    title = asc(title); boxes = [(x, y, w, h, asc(l), c) for x, y, w, h, l, c in boxes]
    f, ft = _fonts()
    im = Image.new('RGB', size, (250, 250, 250)); d = ImageDraw.Draw(im)
    if chrome:  # fake window title bar, like a screenshot of an app window
        d.rectangle([0, 0, size[0], 34], fill=(228, 228, 228))
        for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
            d.ellipse([12 + i * 22, 10, 26 + i * 22, 24], fill=c)
        d.text((size[0] // 2 - 120, 8), title, fill=(60, 60, 60), font=f)
    for x, y, w, h, lab, fill in boxes:
        d.rounded_rectangle([x, y, x + w, y + h], radius=8, outline=(90, 90, 90), width=2, fill=fill)
        d.multiline_text((x + 10, y + 8), lab, fill='black', font=f, spacing=4)
    for i, j in arrows:
        a, b = boxes[i], boxes[j]
        x1, y1 = a[0] + a[2], a[1] + a[3] // 2; x2, y2 = b[0], b[1] + b[3] // 2
        d.line([x1, y1, x2, y2], fill=(40, 40, 40), width=3)
        d.polygon([(x2, y2), (x2 - 12, y2 - 7), (x2 - 12, y2 + 7)], fill=(40, 40, 40))
    out = io.BytesIO(); im.save(out, 'PNG'); return out.getvalue()


def png_bars(title, bars, size=(900, 420), color=(70, 110, 180)):
    from PIL import Image, ImageDraw
    f, ft = _fonts()
    im = Image.new('RGB', size, 'white'); d = ImageDraw.Draw(im)
    d.text((20, 12), title, fill='black', font=ft)
    mx = max(v for _, v in bars); bw = (size[0] - 100) // len(bars)
    for i, (lab, v) in enumerate(bars):
        x0 = 60 + i * bw; h = int((size[1] - 130) * v / mx)
        d.rectangle([x0 + 8, size[1] - 50 - h, x0 + bw - 8, size[1] - 50], fill=color)
        d.text((x0 + 10, size[1] - 44), lab, fill='black', font=f)
        d.text((x0 + 10, size[1] - 70 - h), str(v), fill='black', font=f)
    out = io.BytesIO(); im.save(out, 'PNG'); return out.getvalue()


def png_chess(fen_rows, title):
    from PIL import Image, ImageDraw
    f, ft = _fonts()
    S = 56; im = Image.new('RGB', (S * 8 + 40, S * 8 + 70), 'white'); d = ImageDraw.Draw(im)
    d.text((20, 10), title, fill='black', font=f)
    for r, row in enumerate(fen_rows):
        c = 0
        for ch in row:
            if ch.isdigit():
                for _ in range(int(ch)):
                    d.rectangle([20 + c * S, 40 + r * S, 20 + (c + 1) * S, 40 + (r + 1) * S], fill=(238, 238, 210) if (r + c) % 2 == 0 else (118, 150, 86)); c += 1
            else:
                d.rectangle([20 + c * S, 40 + r * S, 20 + (c + 1) * S, 40 + (r + 1) * S], fill=(238, 238, 210) if (r + c) % 2 == 0 else (118, 150, 86))
                d.text((20 + c * S + 20, 40 + r * S + 16), ch, fill='white' if ch.isupper() else 'black', font=ft,
                       stroke_width=2, stroke_fill='black' if ch.isupper() else 'white')
                c += 1
    out = io.BytesIO(); im.save(out, 'PNG'); return out.getvalue()


# ---------------- audio / midi / flp ----------------

def synth_wav(seconds=5.7, bpm=84, sr=22050, seed='dusk'):
    """Two bars: kick on 1 and 3, snare/rim on 2 and 4, eighth hats, an Am9 pad ducked by the kick (sidechain)."""
    r = random.Random(seed)
    n = int(seconds * sr); beat = 60 / bpm
    out = [0.0] * n
    pad = [220.0, 261.63, 329.63, 392.0, 493.88]
    for i in range(n):
        t = i / sr; pos = t % beat
        duck = 0.35 + 0.65 * min(1.0, pos / 0.25)  # sidechain: pad dips after each kick
        bnum = int(t / beat)
        if bnum % 2 == 1: duck = 0.6 + 0.4 * duck
        out[i] += 0.06 * duck * sum(math.sin(2 * math.pi * fq * t) for fq in pad)
    for b in range(int(seconds / beat) + 1):
        s0 = int(b * beat * sr)
        if b % 2 == 0:  # kick: falling sine
            for k in range(int(0.25 * sr)):
                if s0 + k >= n: break
                tt = k / sr; fq = 50 + 70 * math.exp(-tt * 25)
                out[s0 + k] += 0.8 * math.exp(-tt * 12) * math.sin(2 * math.pi * fq * tt)
        else:  # snare-ish noise burst
            for k in range(int(0.15 * sr)):
                if s0 + k >= n: break
                out[s0 + k] += 0.35 * math.exp(-k / sr * 30) * (r.random() * 2 - 1)
        for h in (0, 0.5):  # hats
            s1 = int((b + h) * beat * sr)
            for k in range(int(0.03 * sr)):
                if s1 + k >= n: break
                out[s1 + k] += 0.12 * math.exp(-k / sr * 120) * (r.random() * 2 - 1)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 30000)) for x in out))
    return buf.getvalue()


def varlen(v):
    b = [v & 0x7F]; v >>= 7
    while v: b.append((v & 0x7F) | 0x80); v >>= 7
    return bytes(reversed(b))


def dusk_midi(bpm=84):
    """Format-0 MIDI written by hand: tempo, 4/4, track name, then Am9 | Fmaj7 | C | G/B as whole-bar chords on channel 1."""
    ppq = 96; bar = ppq * 4
    ev = b''
    ev += b'\x00\xff\x03' + varlen(len(b'dusk pad')) + b'dusk pad'
    us = round(60_000_000 / bpm); ev += b'\x00\xff\x51\x03' + us.to_bytes(3, 'big')
    ev += b'\x00\xff\x58\x04\x04\x02\x18\x08'
    ev += b'\x00\xc0\x04'  # program: electric piano
    chords = [[57, 60, 64, 67, 71], [53, 57, 60, 64], [48, 55, 60, 64], [47, 55, 59, 62]]
    for ch in chords:
        for i, nte in enumerate(ch): ev += b'\x00' + bytes([0x90, nte, 78 - i * 4])
        for i, nte in enumerate(ch): ev += (varlen(bar) if i == 0 else b'\x00') + bytes([0x80, nte, 0])
    ev += b'\x00\xff\x2f\x00'
    return b'MThd' + struct.pack('>IHHH', 6, 0, 1, ppq) + b'MTrk' + struct.pack('>I', len(ev)) + ev


def flp_stub():
    """PLACEHOLDER, not a loadable FL Studio project: the FLhd/FLdt chunk headers plus one version text event."""
    ver = b'21.2.3.4004\x00'
    data = bytes([199]) + varlen(len(ver)) + ver
    return b'FLhd' + struct.pack('<IhhH', 6, 0, 16, 96) + b'FLdt' + struct.pack('<I', len(data)) + data


# =================================================================================================
# zips (HARD CASE)
arr = """dusk loop v3 — arrangement notes (9/12/26)

84 bpm, A minor. 1:48 total.

0:00  intro: pad only (Am9 Fmaj7 C G/B), vinyl noise bus -28 dB
0:11  drums in: tape-drums kick, rim on 2 and 4, eighth hats swing 56%
0:34  bass enters (sub, follows roots, glide on the G/B -> Am9)
0:57  break: drums out, rhodes resampled through amp sim
1:08  drop: everything, pad sidechained to kick (-6 dB, release 120 ms)
1:31  outro: kick + pad, low-pass sweep closing to 800 Hz
(cut the 2nd drop from v2 — it dragged)

files:
- dusk_loop_v3.flp   project (NOTE: in this archive it is a placeholder stub, not the real project)
- dusk_loop_v3_preview.wav   5.7 s sketch of the groove (kick/rim/hats + ducked pad)
- dusk_loop_v3_chords.mid    the four-chord pad as MIDI
- stems/ not included (too big), they're on the external drive
"""
g.zip('Music/Projects/dusk_loop_v3.zip',
      [('dusk_loop_v3/arrangement_notes.txt', arr, '2026-09-12 01:30'),
       ('dusk_loop_v3/dusk_loop_v3_preview.wav', synth_wav(), '2026-09-12 01:12'),
       ('dusk_loop_v3/dusk_loop_v3_chords.mid', dusk_midi(), '2026-09-11 23:48'),
       ('dusk_loop_v3/dusk_loop_v3.flp', flp_stub(), '2026-09-12 01:28')],
      '2026-09-12 01:36', '2026-09-12 01:36',
      **meta('Music/Projects/dusk_loop_v3.zip', ['project_music_production'],
             'HARD CASE: zip archive of files — FL Studio beat project: notes txt, synthesized preview WAV, hand-written MIDI, '
             'and a PLACEHOLDER .flp (header stub only, not a real FL project)'))

fig_pipe = png_boxes('pipeline.png', [(40, 200, 190, 90, 'editor + assistant\ntelemetry', (235, 242, 252)),
                                      (290, 200, 170, 90, '30 s windows', (235, 242, 252)),
                                      (520, 200, 190, 90, 'state classifier\n(GBT, 0.78 F1)', (235, 242, 252)),
                                      (770, 200, 190, 90, 'instructor\ntimeline', (235, 242, 252))], [(0, 1), (1, 2), (2, 3)], chrome=False)
fig_find = png_bars('Time to find stuck students (median s)', [('prompt counts', 190), ('TutorTrace', 41)])
script_txt = """TutorTrace — talk script (export 10/6, the version I'm presenting)

[0:00] Quick show of hands: who has TA'd a lab where everyone had an AI assistant? Keep that room in mind.
[0:30] Quiet rooms are not productive rooms. Students who are stuck are now stuck quietly.
[3:00] TutorTrace: 30-second windows, five states, one row per student, last five minutes on the right.
[5:00] CS 3114: 87 students, 2,340 windows, kappa 0.71. Section B lost ~12% of events for 25 min; marked unlabelable.
[6:30] Gradient-boosted trees. Macro-F1 0.78 (0.74 on the second offering). Stalled-after-error recall 0.83.
[8:00] 9 instructors: 41 s vs 3 min 10 s to find stuck students.
[11:30] Privacy: states, not prompt text. Replays are logged.
[12:30] Takeaway: telemetry should prompt a human check-in, not an automatic intervention.
"""
deck = pdf_bytes([('title', 'TutorTrace: Reading the Quiet Lab'), ('p', 'David Barron, Minsun, Xiaohang, Yan Chen. UIST 2026, Detroit.'),
                  ('pagebreak', None), ('h1', 'Quiet rooms are not productive rooms'), ('p', '45 students, an assistant in every editor, no raised hands.'),
                  ('pagebreak', None), ('h1', 'Five states'), ('p', 'productive, help-seeking, stalled after error, stalled other, off-task'),
                  ('pagebreak', None), ('h1', 'Results'), ('p', 'Macro-F1 0.78; instructors found stuck students in 41 s vs 190 s.'),
                  ('pagebreak', None), ('h1', 'Thanks'), ('p', 'Questions?')],
                 'TutorTrace UIST 2026 talk', 'David Barron', '2026-10-06 22:30', '2026-10-06 22:30')
g.zip('Desktop/uist26_talk_assets.zip',
      [('uist26_talk_assets/TutorTrace_UIST26_final.pdf', deck, '2026-10-06 22:30'),
       ('uist26_talk_assets/figures/pipeline.png', fig_pipe, '2026-10-03 16:12'),
       ('uist26_talk_assets/figures/time_to_find.png', fig_find, '2026-10-03 16:20'),
       ('uist26_talk_assets/talk_script.txt', script_txt, '2026-10-06 22:20')],
      '2026-10-06 22:35', '2026-10-06 22:35',
      **meta('Desktop/uist26_talk_assets.zip', ['project_tutortrace'],
             'HARD CASE: zip archive of files — final talk PDF, figures and script; overlaps the Drive "UIST26 talk assets.zip" (later version)'))

# =================================================================================================
# Strava activities.csv (~200 rows)
SF_MOVE = datetime.date(2026, 8, 8)
NAMES_VA = ['Huckleberry easy', 'Duck pond loop', 'Pandapas trails', 'Prices Fork long run', 'Z2 + strides', 'Recovery jog',
            'Easy with Owen', 'Track 6x400 (relaxed)', 'Heritage Park loop', 'Snowy Z2', 'Brush Mountain ride', 'Commute + long way home']
NAMES_SF = ['Embarcadero easy', 'Golden Gate Park long run', 'Lands End hills', 'Crissy Field Z2', 'Panhandle loop', 'Presidio climbs ride',
            'Marin headlands ride', '3x3k @ HM', 'Twin Peaks (why)', 'Fog run', 'Shakeout', 'Bay Trail Z2']
DESCS = {'2025-11-27': 'turkey trot w/ Owen, 17:41, 4th', '2026-04-18': 'Spring 10k, 37:20. legs flat after UIST',
         '2026-09-26': 'tune-up 10k 36:58', '2026-10-15': 'Bay Area half. 1:24:51, negative split. Owen 1:22:10',
         '2026-08-10': 'first SF run. hills everywhere', '2026-01-24': 'treadmill, snow', '2026-07-29': 'rebuttal posted, celebratory slow run',
         '2026-05-09': 'crashed on a gravel corner, derailleur hanger bent, walked last 2 km', '2026-03-31': 'deadline day. 25 min to stay sane'}
RACES = {'2025-11-27': ('Turkey Trot 5k', 'Run', 5.0, 17 * 60 + 41, 9 * 60), '2026-04-18': ('Spring 10k', 'Run', 10.0, 37 * 60 + 20, 9 * 60),
         '2026-09-26': ('Tune-up 10k', 'Run', 10.0, 36 * 60 + 58, 8 * 60), '2026-10-15': ('Bay Area Half Marathon', 'Run', 21.1, 1 * 3600 + 24 * 60 + 51, 7 * 60 + 30)}
fixed_extra = ['2026-03-31', '2026-05-09', '2026-07-29', '2026-08-10', '2026-01-24']
rnd = random.Random('strava')
acts = []
day = datetime.date(2025, 10, 18)
wk_w = dict(week_weights())
while day <= datetime.date(2026, 10, 16):
    monday = day - datetime.timedelta(days=day.weekday())
    busy = wk_w.get(monday, 0.8)
    p = 0.62 if busy < 1.5 else (0.45 if busy < 2.6 else 0.32)
    if day.isoformat() in RACES or day.isoformat() in fixed_extra or rnd.random() < p:
        acts.append(day)
    day += datetime.timedelta(days=1)
rows = [['Activity ID', 'Activity Date', 'Activity Name', 'Activity Type', 'Activity Description', 'Elapsed Time', 'Distance', 'Max Heart Rate',
         'Relative Effort', 'Commute', 'Activity Gear', 'Filename', 'Moving Time', 'Average Heart Rate', 'Elevation Gain', 'Average Speed']]
aid = 16210000000
for d0 in acts:
    k = d0.isoformat(); sf = d0 >= SF_MOVE
    hour = rnd.choice([6, 6, 7, 7, 12, 17, 18]) if not sf else rnd.choice([6, 6, 7, 7, 12, 18])
    if k in RACES:
        nm, typ, dist, secs, hour = RACES[k][0], RACES[k][1], RACES[k][2], RACES[k][3], 8
        mhr, avg = 189, 176
    else:
        typ = rnd.choices(['Run', 'Ride', 'Elliptical', 'Workout'], [64, 21, 10, 5])[0]
        if d0.month in (12, 1, 2) and typ == 'Ride': typ = 'Elliptical'
        if typ == 'Run':
            dist = round(rnd.choice([8, 10, 10, 12, 12, 14, 16, 18, 21, 24]) * rnd.uniform(0.92, 1.05), 2)
            pace = rnd.uniform(5.0, 5.5) if not sf else rnd.uniform(4.9, 5.4)
            secs = int(dist * pace * 60); avg = rnd.randint(138, 147); mhr = avg + rnd.randint(8, 18)
        elif typ == 'Ride':
            secs = rnd.choice([45, 60, 75, 90, 120]) * 60; dist = round(secs / 3600 * rnd.uniform(24, 29), 2); avg = rnd.randint(128, 140); mhr = avg + 15
        else:
            secs = rnd.choice([30, 40, 45, 60]) * 60; dist = 0.0; avg = rnd.randint(125, 140); mhr = avg + 12
        default = {'Run': 'Run', 'Ride': 'Ride', 'Elliptical': 'Elliptical', 'Workout': 'Workout'}[typ]
        tod = 'Morning' if hour < 11 else ('Lunch' if hour < 14 else ('Afternoon' if hour < 17 else 'Evening'))
        nm = f'{tod} {default}'
        if typ in ('Run', 'Ride') and rnd.random() < 0.3:
            pool = [n for n in (NAMES_SF if sf else NAMES_VA) if ('ride' in n.lower()) == (typ == 'Ride')]
            nm = rnd.choice(pool) if pool else nm
        if typ == 'Workout': nm = rnd.choice(['Core + mobility', 'Strength (legs)', 'Hip stuff'])
    tz = PT if sf else ET
    local = datetime.datetime(d0.year, d0.month, d0.day, hour, rnd.randrange(60), rnd.randrange(60), tzinfo=tz)
    utcd = local.astimezone(UTC)
    moving = int(secs * (1.0 if k in RACES else rnd.uniform(0.95, 0.99)))
    elev = round(dist * (rnd.uniform(4, 9) if not sf else rnd.uniform(8, 16)), 1)
    gear = {'Run': 'racer' if k in ('2026-09-26', '2026-10-15') else rnd.choice(['trainer A (grey)', 'trainer B (blue)']) if d0 >= datetime.date(2026, 3, 10) else 'trainer A (grey)',
            'Ride': '11-speed road bike', 'Elliptical': '', 'Workout': ''}[typ]
    aid += rnd.randint(40_000_000, 160_000_000)
    re_ = int(secs / 60 * (1.9 if k in RACES else rnd.uniform(0.6, 1.1)))
    rows.append([aid, utcd.strftime('%b %-d, %Y, %-I:%M:%S %p'), nm, typ, DESCS.get(k, ''), secs, f'{dist:.2f}', mhr, re_,
                 'true' if typ == 'Ride' and hour in (7, 18) and not sf and rnd.random() < 0.4 else 'false', gear,
                 f'activities/{aid}.fit.gz', moving, avg, elev, f'{(dist * 1000 / moving) if moving and dist else 0:.3f}'])
g.text('Downloads/strava_export_2026-10-16/activities.csv', csv_text(rows), '2026-10-16 21:42', '2026-10-16 21:42',
       **meta('Downloads/strava_export_2026-10-16/activities.csv', ['project_endurance_training'],
              f'Strava bulk export activities.csv, {len(rows) - 1} activities 2025-10-18..2026-10-16'))

# Garmin sleep CSV
rnd = random.Random('sleep')
srows = [['Date', 'Sleep Score', 'Quality', 'Duration', 'Bedtime', 'Wake Time', 'Deep', 'Light', 'REM', 'Awake', 'Resting Heart Rate', 'Avg Overnight HRV']]
d0 = datetime.date(2026, 4, 1)
special = {'2026-05-06': (5.1, 'deadline'), '2026-08-07': (4.4, 'travel'), '2026-08-08': (6.0, 'travel'), '2026-10-04': (5.6, 'flight'),
           '2026-10-07': (6.1, 'talk'), '2026-10-14': (5.8, 'pre-race'), '2026-06-18': (5.3, 'rebuttal'), '2026-07-29': (5.5, 'rebuttal')}
while d0 <= datetime.date(2026, 10, 16):
    k = d0.isoformat()
    hrs = special.get(k, (None,))[0] or round(rnd.gauss(7.4, 0.55), 2)
    bed_h = 23 + rnd.choice([0, 0, 0, 1]) if hrs > 6.5 else 1
    bed = f'{bed_h % 24:02d}:{rnd.randrange(60):02d}'
    wake_min = (bed_h * 60 + int(hrs * 60) + rnd.randint(5, 25)) % (24 * 60)
    deep = round(hrs * rnd.uniform(0.15, 0.22), 2); rem = round(hrs * rnd.uniform(0.18, 0.25), 2); awake = round(rnd.uniform(0.1, 0.5), 2)
    light = round(hrs - deep - rem, 2)
    score = max(38, min(96, int(50 + (hrs - 5) * 14 + rnd.randint(-6, 6))))
    q = 'Excellent' if score >= 90 else 'Good' if score >= 80 else 'Fair' if score >= 60 else 'Poor'
    rhr = rnd.randint(41, 45) + (3 if k in special else 0)
    def hm(x): return f'{int(x)}h {int(round((x % 1) * 60)):02d}m'
    srows.append([k, score, q, hm(hrs), bed, f'{wake_min // 60:02d}:{wake_min % 60:02d}', hm(deep), hm(light), hm(rem), hm(awake), rhr,
                  rnd.randint(58, 74) - (8 if k in special else 0)])
    d0 += datetime.timedelta(days=1)
g.text('Downloads/garmin_sleep_2026-04-01_2026-10-16.csv', csv_text(srows), '2026-10-16 21:50', '2026-10-16 21:50',
       **meta('Downloads/garmin_sleep_2026-04-01_2026-10-16.csv', ['project_endurance_training'], 'Garmin Connect sleep export, daily rows'))

# =================================================================================================
# .ics travel export


def ics_dt(s):
    return dt(s).astimezone(UTC).strftime('%Y%m%dT%H%M%SZ')


EVENTS = [('2026-10-02 10:00', '2026-10-02 10:30', 'UIST AV check (Zoom) w/ Tomás Reyes', 'Zoom', 'Test slides + clicker over Zoom share.'),
          ('2026-10-04 07:55', '2026-10-04 15:40', 'Flight SFO → DTW (UA 1182)', 'SFO Terminal 3', 'Conf. code QK7P2D. Seat 23C.'),
          ('2026-10-04 17:00', '2026-10-08 11:00', 'Hotel — Detroit (UIST block)', 'Detroit, MI', 'Shared room, 3 nights + late checkout requested.'),
          ('2026-10-05 18:30', '2026-10-05 21:00', 'UIST 2026 welcome reception', 'Conference venue, Detroit', ''),
          ('2026-10-07 10:40', '2026-10-07 11:00', 'TALK: TutorTrace (Learning & Tutoring session)', 'Session room B, Detroit',
           'Chair: Tomás Reyes. 15 min + 5 Q&A. Be in the room by 10:20.'),
          ('2026-10-08 13:15', '2026-10-08 15:35', 'Flight DTW → SFO (UA 1543)', 'DTW McNamara Terminal', 'Conf. code QK7P2D.')]
# dates above are wall-clock where each event happens: DTW/Detroit is Eastern, SFO is Pacific
TZ_OF = {0: PT, 1: PT, 2: ET, 3: ET, 4: ET, 5: ET}
ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Apple Inc.//macOS 15.6//EN', 'CALSCALE:GREGORIAN', 'X-WR-CALNAME:UIST 2026 trip']
for i, (a, b, summ, loc, desc) in enumerate(EVENTS):
    tz = TZ_OF[i]
    s = datetime.datetime.fromisoformat(a).replace(tzinfo=tz); e = datetime.datetime.fromisoformat(b).replace(tzinfo=tz)
    if i == 1: e = datetime.datetime.fromisoformat(b).replace(tzinfo=ET)  # lands in Detroit
    if i == 5: e = datetime.datetime.fromisoformat(b).replace(tzinfo=PT)  # lands at SFO
    ics += ['BEGIN:VEVENT', f'UID:{uid(("uist-ics", i)).upper()}', f'DTSTAMP:{ics_dt("2026-09-30 22:05")}', f'DTSTART:{ics_dt(s)}',
            f'DTEND:{ics_dt(e)}', f'SUMMARY:{summ}', f'LOCATION:{loc}', f'DESCRIPTION:{desc}', 'END:VEVENT']
ics.append('END:VCALENDAR')
g.text('Downloads/UIST 2026 trip.ics', '\r\n'.join(ics) + '\r\n', '2026-09-30 22:06', '2026-09-30 22:06',
       **meta('Downloads/UIST 2026 trip.ics', ['project_tutortrace', 'project_vt_phd_admin'], 'calendar export of the UIST travel'))

# =================================================================================================
# JSON configs / outputs
g.json('Projects/engelbart/import.config.json', {
    'version': 2, 'updated': '2026-10-15',
    'connectors': {
        'claude': {'enabled': True, 'source': 'export_zip', 'paginate_until_empty': True, 'page_size': 100, 'note': 'v1 stopped at 1000 convos'},
        'chatgpt': {'enabled': True, 'source': 'export_zip'},
        'zotero': {'enabled': True, 'source': 'local_sqlite', 'include_attachments': True},
        'downloads_pdfs': {'enabled': True, 'paths': ['~/Downloads', '~/Desktop/papers']},
        'github': {'enabled': True, 'orgs': ['Mathetic-PBC'], 'include_forks': False},
        'notion': {'enabled': False, 'note': 'pilot B asked for it (10/13)'},
        'granola': {'enabled': False, 'note': 'pilot B asked for it (10/13)'}},
    'dedupe': {'paper': ['doi', 'title_author_year'], 'chat': ['vendor_conversation_id', 'first_message_hash+created'],
               'doc': ['content_hash', 'title+modified'], 'zip': ['member_content_hash'], 'group_versions': ['Copy of *', '* v[0-9]*', '* copy']},
    'report_expected_counts': True, 'unassigned_bucket': 'none'}, '2026-09-02 16:20', '2026-10-15 23:10', indent=2,
    **meta('Projects/engelbart/import.config.json', ['project_engelbart']))

g.json('Projects/claude-plugins/hc/settings.json', {
    'name': 'hc', 'version': '0.13.1', 'compaction': {'trigger_tokens': 170000, 'ask_focus_hint': True,
    'keep_verbatim': ['TODO block', 'failing test names', 'file paths touched', 'env var names'], 'max_summary_tokens': 6000},
    'rules_file': 'hc-rules.md', 'log': {'path': 'logs/hc.jsonl', 'level': 'info'}}, '2026-08-17 21:40', '2026-08-27 23:30', indent=2,
    **meta('Projects/claude-plugins/hc/settings.json', ['project_claude_code_plugins']))

g.json('Desktop/hc_compaction_results.json', {'runs': [
    {'run': 1, 'date': '2026-08-17', 'version': '0.5.0', 'before': 182000, 'after': 61000, 'success': False, 'lost': 'file list'},
    {'run': 2, 'date': '2026-08-19', 'version': '0.5.0', 'before': 176000, 'after': 58000, 'success': False, 'lost': 'failing test name'},
    {'run': 3, 'date': '2026-08-21', 'version': '0.11.0', 'before': 181000, 'after': 72000, 'success': True},
    {'run': 4, 'date': '2026-08-23', 'version': '0.11.0', 'before': 190000, 'after': 70500, 'success': True},
    {'run': 5, 'date': '2026-08-25', 'version': '0.13.0', 'before': 185000, 'after': 66000, 'success': True},
    {'run': 6, 'date': '2026-08-27', 'version': '0.13.1', 'before': 188000, 'after': 64800, 'success': 'partial', 'lost': 'E2B env var name'}],
    'summary': 'focus hint + verbatim TODO block fixes most losses; next: 10 runs per version'}, '2026-08-27 23:40', '2026-08-28 00:05', indent=2,
    **meta('Desktop/hc_compaction_results.json', ['project_claude_code_plugins']))

g.json('Projects/vizpi_frontend/telemetry.config.json', {
    'endpoint': 'wss://vizpi-lab.example.edu/ws', 'window_seconds': 30,
    'reconnect': {'await_token_refresh': True, 'buffer_limit': 500, 'backoff_ms': [250, 500, 1000, 2000, 4000],
                  'note': 'await refresh before re-subscribe — hotfix 2025-11-12 16:10 (section B gap)'},
    'heartbeat': {'interval_s': 15, 'report_buffered_count': True}, 'consent': {'opt_out_url': '/plain-ide'}},
    '2025-10-30 14:00', '2025-11-14 10:40', indent=2, **meta('Projects/vizpi_frontend/telemetry.config.json', ['project_vizpi']))

g.json('Documents/idetrace/split_check_2026-07-24.json', {
    'script': 'make_splits.py', 'run_at': '2026-07-24T23:32:10-04:00',
    'window_random': {'folds': 5, 'students_overlap_fold1': 38, 'macro_f1_mean': 0.81},
    'grouped_by_student': {'folds': 5, 'students_overlap_fold1': 0, 'macro_f1_mean': 0.74},
    'decision': 'report both in rebuttal; grouped split is the default from v1.1'}, '2026-07-24 23:32', '2026-07-24 23:35', indent=2,
    **meta('Documents/idetrace/split_check_2026-07-24.json', ['project_idetrace']))

g.json('Desktop/Engelbart/dedupe_candidates_priya.json', {'pilot': 'Priya', 'generated': '2026-10-10T09:14:00-07:00', 'groups': [
    {'key': 'doi:10.1145/3698205.3729841', 'title': 'Productive Struggle or Silent Stalling? (Ostrowski et al. 2025)',
     'copies': ['zotero/storage/8KQ2M1/Ostrowski2025.pdf', '~/Downloads/Ostrowski2025_LAS_camera_ready.pdf'], 'action': 'merge'},
    {'key': 'title:copy-of', 'title': 'TA dashboard study plan / Copy of TA dashboard study plan', 'action': 'group as versions'},
    {'key': 'chat:dup-export', 'title': '31 Claude chats present in both Aug and Oct export zips', 'action': 'merge by conversation id'}],
    'missing': {'claude': {'expected': 1400, 'imported': 1262}}}, '2026-10-10 09:14', '2026-10-10 09:20', indent=2,
    **meta('Desktop/Engelbart/dedupe_candidates_priya.json', ['project_engelbart']))

# =================================================================================================
# Brewfile (new Mac 2026-08-04)
brew = """# new mac 2026-08-04 — brew bundle --file ~/Brewfile
tap "homebrew/bundle"

# cli
brew "git"
brew "gh"
brew "node"
brew "uv"
brew "python@3.12"
brew "jq"
brew "ripgrep"
brew "fd"
brew "sqlite"
brew "ffmpeg"        # bouncing beats to mp3, screen recordings
brew "pandoc"        # paper drafts -> docx for Yan
brew "tree"

# apps
cask "firefox"       # personal
cask "brave-browser" # testing landing page
cask "google-chrome" # work accounts
cask "visual-studio-code"
cask "iterm2"
cask "rectangle"
cask "zotero"
cask "obsidian"
cask "zoom"
cask "slack"
cask "spotify"
# FL Studio: installed from the vendor site, license re-activated manually
"""
g.text('Brewfile', brew, '2026-08-04 11:05', '2026-08-04 12:20', **meta('Brewfile', ['project_none'], 'setup list for the new Mac'))

# =================================================================================================
# screenshots (PIL)
g.bytes('Desktop/Screenshot 2026-10-13 at 4.12.08 PM.png',
        png_boxes('Engelbart — Connect your tools', [
            (40, 70, 280, 150, 'Conversations\n  Claude  1,400\n  ChatGPT  212\n  Slack', (235, 242, 252)),
            (360, 70, 280, 150, 'Papers\n  Zotero  312\n  Downloads PDFs  188', (235, 242, 252)),
            (680, 70, 280, 150, 'Code\n  GitHub  9 repos\n  Claude Code sessions', (235, 242, 252)),
            (40, 260, 280, 150, 'Writing\n  Google Docs\n  Obsidian', (235, 242, 252)),
            (360, 260, 280, 150, 'Other  (?)\n  Notion ← put here by pilot B', (255, 236, 220)),
            (680, 260, 280, 60, 'Import 2,121 items →', (210, 235, 210))]),
        '2026-10-13 16:12', '2026-10-13 16:12',
        **meta('Desktop/Screenshot 2026-10-13 at 4.12.08 PM.png', ['project_engelbart'], 'screenshot of the connect screen during pilot B'))
g.bytes('Desktop/Screenshot 2026-03-30 at 11.48.22 PM.png',
        png_boxes('TutorTrace — instructor timeline (fig 1 draft)', [
            (40, 70, 920, 50, 'student 01  ■■■■■■□□□□■■■■  productive', (210, 235, 210)),
            (40, 130, 920, 50, 'student 02  ■■▲▲▲▲▲▲▲▲▲▲▲▲  stalled after error (6 min)', (255, 220, 210)),
            (40, 190, 920, 50, 'student 03  ■■■■◆◆■■■■■■■■  help-seeking then productive', (235, 242, 252)),
            (40, 250, 920, 50, 'student 04  ░░░░░░░░■■■■■■  unlabelable (telemetry gap)', (235, 235, 235)),
            (40, 330, 420, 80, 'click a row → replay', (250, 250, 220))]),
        '2026-03-30 23:48', '2026-03-30 23:48',
        **meta('Desktop/Screenshot 2026-03-30 at 11.48.22 PM.png', ['project_tutortrace'], 'screenshot of a figure draft during the UIST crunch'))
g.bytes('Desktop/Screenshot 2026-09-15 at 7.02.40 AM.png',
        png_bars('Time in HR zone — 3x3 km @ HM pace (min)', [('Z1', 9), ('Z2', 22), ('Z3', 14), ('Z4', 19), ('Z5', 1)], color=(200, 90, 70)),
        '2026-09-15 07:02', '2026-09-15 07:02',
        **meta('Desktop/Screenshot 2026-09-15 at 7.02.40 AM.png', ['project_endurance_training']))
g.bytes('Desktop/Screenshot 2026-02-21 at 10.14.55 PM.png',
        png_chess(['r1b1kbnr', 'pp3ppp', '2n1p3', '2ppP3', '1q1P1B1P', '2P1PN2', 'PP3PP1', 'RN1QKB1R'], 'how do I keep losing b2 (London, move 7)'),
        '2026-02-21 22:14', '2026-02-21 22:14',
        **meta('Desktop/Screenshot 2026-02-21 at 10.14.55 PM.png', ['project_none'], 'HARD CASE: personal clutter — chess screenshot on the Desktop'))

# =================================================================================================
# PDFs: receipts, vague invoice, checklist


def receipt(rel, vendor, when, lines, pids, extra=None, notes='', title=None):
    tot = sum(a for _, a in lines)
    blocks = [('title', vendor), ('p', f'Receipt — {dt(when).strftime("%B %-d, %Y")}'), ('p', 'Billed to: David Barron')]
    blocks.append(('table', [['Item', 'Amount']] + [[n, f'${a:,.2f}'] for n, a in lines] + [['Total', f'${tot:,.2f}']]))
    blocks += [('p', x) for x in (extra or [])]
    g.pdf(rel, blocks, when, when, title=title or f'{vendor} receipt', author=vendor, **meta(rel, pids, notes))


receipt('Downloads/Receipt-Loopbank-2026-08-30.pdf', 'Loopbank', '2026-08-30 22:12',
        [('Tape Drums (WAV, 24-bit) — sample pack', 14.99), ('Sales tax', 1.29)], ['project_music_production'],
        ['Order LB-77310. License: royalty-free for commercial releases.'])
receipt('Downloads/receipt_valley_cycles_2026-05-12.pdf', 'Valley Cycles (Blacksburg)', '2026-05-12 17:55',
        [('Rear derailleur hanger', 28.00), ('Labor: hanger install + indexing', 35.00), ('Sales tax', 1.48)], ['project_none'],
        ['Work order 4471. Hanger was bent ~4 degrees; indexing adjusted.'], 'HARD CASE: personal clutter — bike shop receipt')
receipt('Downloads/CarHaul_receipt_order_58213.pdf', 'CarHaul Auto Transport', '2026-08-05 09:30',
        [('Open carrier, Blacksburg VA → San Francisco CA', 1150.00), ('Insurance (included)', 0.00)], ['project_none'],
        ['Pickup 2026-08-05, estimated delivery 7-10 days. Delivered 2026-08-15.'], 'HARD CASE: personal clutter — car shipping receipt for the move')
receipt('Downloads/UIST2026_registration_receipt.pdf', 'UIST 2026 Registration', '2026-09-02 14:20',
        [('Student registration (early), ACM member', 475.00)], ['project_tutortrace', 'project_vt_phd_admin'],
        ['Registrant: David Barron, Virginia Tech. Conference: UIST 2026, Detroit, MI. Keep this for travel reimbursement.'])
g.pdf('Downloads/invoice_final_FINAL.pdf', [
    ('title', 'INVOICE #0007'), ('p', 'R. Alvarado — illustration & design'), ('p', 'Date: 2026-09-19   Due: 2026-10-03'),
    ('p', 'Bill to: Mathetic PBC (attn: David Barron, Hudson Mitchell-Pullman)'),
    ('table', [['Description', 'Qty', 'Rate', 'Amount'], ['Landing page hero illustration ("trails")', '1', '$600', '$600.00'],
               ['Three column icons (import / trail / private)', '3', '$80', '$240.00'], ['Revision round 2', '1', '$120', '$120.00'],
               ['Total', '', '', '$960.00']]),
    ('p', 'Payment by bank transfer. Thank you!'), ('p', '(final version — replaces invoice_final.pdf sent 9/17 which had the wrong total)'),
], '2026-09-19 18:40', '2026-09-19 18:40', title='Invoice 0007', author='R. Alvarado',
    **meta('Downloads/invoice_final_FINAL.pdf', ['project_mathetic_company'],
           'HARD CASE: vague title — "invoice_final_FINAL.pdf" is a Mathetic landing-page illustration invoice'))
g.pdf('Downloads/CA vehicle registration checklist.pdf', [
    ('title', 'Registering an out-of-state vehicle in California — checklist'),
    ('bullet', 'Application for Title or Registration form'), ('bullet', 'Out-of-state title or registration card'),
    ('bullet', 'Smog certificate (most vehicles)'), ('bullet', 'Vehicle verification at a DMV office'), ('bullet', 'Proof of CA insurance'),
    ('bullet', 'Fees: registration, use tax if purchased recently'), ('p', 'Saved 2026-08-17. Appointment booked for 2026-09-03.'),
], '2026-08-17 21:10', '2026-08-17 21:10', title='CA registration checklist', author='',
    **meta('Downloads/CA vehicle registration checklist.pdf', ['project_none']))

# lease summary docx (fictional)
lease = docx_bytes([
    ('title', 'Lease summary — Surplus house room'),
    ('p', 'My summary of the room agreement, signed 2026-08-11. Not the agreement itself.'),
    ('table', [['Term', 'Value'], ['Premises', 'Room 3, Surplus incubator house, SoMa, San Francisco'], ['Start', '2026-08-08'],
               ['End', '2026-12-31 (month-to-month after, 30 days notice)'], ['Rent', '$1,200 / month, due on the 1st'],
               ['Deposit', '$1,200, refundable'], ['Utilities', 'included (internet, water, power)'], ['Guests', 'max 3 nights in a row'],
               ['Quiet hours', '11 pm – 7 am'], ['Shared spaces', 'kitchen, living room (demo Fridays 4 pm), roof']]),
    ('p', 'Questions for Lena: renters insurance covered by the house policy? (answer 8/12: no, get my own)'),
], 'Lease summary', 'David Barron', '2026-08-11 21:30', '2026-08-12 18:05')
g.bytes('Documents/Lease summary - Surplus house.docx', fix_office(lease, '2026-08-12 18:05'), '2026-08-11 21:30', '2026-08-12 18:05',
        **meta('Documents/Lease summary - Surplus house.docx', ['project_none'], 'fictional lease summary'))

# =================================================================================================
# CSVs: course + research + personal
FIRST = ['Ava', 'Ethan', 'Maya', 'Liam', 'Sofia', 'Noah', 'Chloe', 'Lucas', 'Grace', 'Mason', 'Aaliyah', 'Logan', 'Priyanka', 'Caleb',
         'Hana', 'Jacob', 'Isabel', 'Owen', 'Nadia', 'Tyler', 'Zoe', 'Ryan', 'Leah', 'Arjun', 'Emily', 'Daniel', 'Fatima', 'Ben',
         'Sara', 'Kofi', 'Julia', 'Marco', 'Ellie', 'Sean', 'Mei', 'Nathan', 'Rosa', 'Kyle', 'Anika', 'Victor']
LAST = ['Alvarez', 'Bennett', 'Chowdhury', 'Dawson', 'Ellis', 'Fitzgerald', 'Gupta', 'Hale', 'Ibarra', 'Jensen', 'Kowalski', 'Lam',
        'Mendoza', 'Nakamura', 'Okafor', 'Price', 'Quinn', 'Rahman', 'Sullivan', 'Tran', 'Underwood', 'Vasquez', 'Walsh', 'Xu',
        'Yilmaz', 'Zimmerman', 'Barnes', 'Castillo', 'Delgado', 'Foster', 'Greene', 'Holt', 'Iqbal', 'Jordan', 'Kaur', 'Lowe']
rnd = random.Random('cs3604-roster')  # same roster as the Drive grading sheet
names = set()
while len(names) < 64: names.add((rnd.choice(FIRST), rnd.choice(LAST)))
roster = sorted(names, key=lambda x: (x[1], x[0]))
pids = [(f[0] + l[:5]).lower() + str(rnd.randint(1, 99)) for f, l in roster]
SESS = ['2025-10-21', '2025-10-28', '2025-11-04', '2025-11-11', '2025-11-18', '2025-12-02', '2025-12-09']
ar = random.Random('attendance')
att = [['PID', 'Last', 'First'] + [f'Demo check-in {s}' for s in SESS] + ['Attended']]
for i, ((f, l), pid) in enumerate(zip(roster, pids)):
    marks = ['P' if ar.random() < 0.88 else ar.choice(['A', 'E']) for _ in SESS]
    att.append([pid, l, f] + marks + [marks.count('P')])
g.text('Documents/VT/cs3604_attendance_F25.csv', csv_text(att), '2025-10-21 17:40', '2025-12-09 18:30',
       **meta('Documents/VT/cs3604_attendance_F25.csv', ['project_cs3604_gta'], 'attendance for project demo check-ins, 64 fictional students'))

er = random.Random('eventrate')
ev = [['minute_et', 'section', 'events', 'clients_connected', 'note']]
for mnt in range(0, 81):
    t = datetime.datetime(2025, 11, 12, 15, 30) + datetime.timedelta(minutes=mnt); hhmm = t.strftime('%H:%M')
    for sec, n in (('A', 44), ('B', 43)):
        gap = sec == 'B' and datetime.time(15, 45) <= t.time() < datetime.time(16, 10)
        rate = er.randint(3, 9) if gap else er.randint(48, 62)
        note = {('B', '15:45'): 'wifi blip, reconnect storm', ('B', '16:10'): 'hotfix deployed, reload requested'}.get((sec, hhmm), '')
        ev.append([hhmm, sec, rate, n - (er.randint(0, 2) if gap else 0), note])
g.text('Desktop/vizpi_deploy2_event_rates.csv', csv_text(ev), '2025-11-12 17:25', '2025-11-12 21:05',
       **meta('Desktop/vizpi_deploy2_event_rates.csv', ['project_vizpi'], 'per-minute telemetry event rate per section, deployment #2'))

bs = [['Timestamp', 'Name', 'Email', 'Department / role', 'What are you working on?', 'Preferred slot', 'OK to record?'],
      ['2026-09-01 09:12:44', 'Elena Park', 'elena.park@berkeley.example', 'Graduate School of Education (PhD)', 'how students revise explanations after feedback', 'Wed 9/9 2pm', 'Yes'],
      ['2026-09-01 21:40:03', 'Priya Raman', 'priya.raman@berkeley.example', 'Education + HCI (PhD)', 'TA dashboards in large CS courses', 'Thu 9/10 10:30am', 'Yes'],
      ['2026-09-08 13:05:51', 'Ben Adeyemi', 'ben.adeyemi@berkeley.example', 'Statistics (postdoc)', 'reproducibility of applied stats workflows', 'Wed 9/16 4pm (Zoom)', 'Yes']]
g.text('Downloads/Berkeley research chats - sign-up (Responses).csv', csv_text(bs), '2026-09-08 22:30', '2026-09-08 22:30',
       **meta('Downloads/Berkeley research chats - sign-up (Responses).csv', ['project_berkeley_research_chats'], 'form responses export'))

bud = [['date', 'category', 'item', 'amount'],
       ['2026-08-01', 'rent', 'Blacksburg apt (last month, prorated)', 210.00], ['2026-08-05', 'move', 'car transport', 1150.00],
       ['2026-08-07', 'move', 'flight ROA-SFO', 289.40], ['2026-08-08', 'rent', 'Surplus house deposit', 1200.00],
       ['2026-08-09', 'groceries', 'first SF grocery run', 96.12], ['2026-08-12', 'transit', 'Clipper card load', 40.00],
       ['2026-08-16', 'insurance', 'car insurance CA (6 mo)', 640.00], ['2026-08-20', 'food', 'burritos x too many', 58.75],
       ['2026-08-30', 'music', 'Tape Drums sample pack', 16.28], ['2026-08-31', 'subscriptions', 'monthly subs', 46.96]]
g.text('Documents/budget_aug2026.csv', csv_text(bud), '2026-08-01 20:00', '2026-08-31 22:10',
       **meta('Documents/budget_aug2026.csv', ['project_none'], 'HARD CASE: personal clutter — move-month budget'))

ic = [['source', 'expected', 'imported', 'duplicates_found', 'note'], ['claude', 1400, 1262, 31, 'pagination stopped at 1000 then partial page'],
      ['chatgpt', 212, 212, 0, ''], ['zotero', 312, 312, 23, '23 also in Downloads'], ['downloads_pdfs', 188, 188, 23, ''],
      ['github', 9, 9, 0, ''], ['google_docs', 140, 137, 4, '3 shortcuts skipped']]
g.text('Desktop/Engelbart/import_counts_pilot1_2026-10-09.csv', csv_text(ic), '2026-10-09 16:55', '2026-10-09 17:02',
       **meta('Desktop/Engelbart/import_counts_pilot1_2026-10-09.csv', ['project_engelbart']))

# PGN (personal clutter)
pgn = """[Event "Rated Rapid game"]
[Site "online"]
[Date "2026.02.21"]
[White "dbarron_runs"]
[Black "opponent_1622"]
[Result "1-0"]
[TimeControl "600"]
[Termination "dbarron_runs won by resignation"]

1. d4 d5 2. Bf4 c5 3. e3 Nc6 4. h4 Qb6 5. Nc3 Qxb2 6. Nb5 Qb4+ 7. c3 Qxb5 8. Bxb5 1-0

[Event "Rated Rapid game"]
[Site "online"]
[Date "2026.02.21"]
[White "opponent_1701"]
[Black "dbarron_runs"]
[Result "1-0"]
[TimeControl "600"]
[Termination "opponent_1701 won on time"]

1. e4 c6 2. d4 d5 3. e5 Bf5 4. Nf3 e6 5. Be2 c5 6. O-O Nc6 7. c3 Qb6 8. Na3 cxd4 9. cxd4 Bxa3 10. bxa3 Nge7 1-0
"""
g.text('Downloads/chess_games_2026-02-21.pgn', pgn, '2026-02-21 22:30', '2026-02-21 22:30',
       **meta('Downloads/chess_games_2026-02-21.pgn', ['project_none'], 'HARD CASE: personal clutter — exported chess games'))

# lone sample (music)
g.bytes('Music/Samples/dusk_kick_tape.wav', synth_wav(seconds=0.75, seed='kick-only'), '2026-08-30 22:40', '2026-08-30 22:40',
        **meta('Music/Samples/dusk_kick_tape.wav', ['project_music_production'], 'short synthesized one-bar sketch used as a kick reference'))

g.finish()
