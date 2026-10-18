"""Synthetic Evernote (david.barron.runs@gmail.com): one ENEX file per note under <account>/<Notebook>/<title>.enex, plus a
whole-notebook export of Recipes (HARD CASE: near-duplicate). Content hand-written below; helpers only wrap it into ENEX/ENML.
Run: $SYNTHPY _scripts/synth/gen_evernote.py"""
import os, sys, re, base64, hashlib, struct, zlib, html
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('evernote')
ACCT_DIR = 'david.barron.runs@gmail.com'
ACCOUNT = 'Evernote (david.barron.runs@gmail.com)'
VERSION = '10.105.4'

# ---------------- tiny PNG writer (no PIL) ----------------

def png_bytes(w, h, pix):
    raw = b''.join(b'\x00' + bytes(c for x in range(w) for c in pix(x, y)) for y in range(h))
    def chunk(t, d): return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def elevation_png():
    """Bay Area Half course profile sketch: 13.1 mi across 330 px, flat start, ~120 ft climb at miles 7-8, gentle run-in."""
    W, H = 330, 120
    def elev(mi):
        if mi < 6.8: return 15 + 4 * ((mi * 3) % 1)
        if mi < 8.0: return 15 + 120 * (mi - 6.8) / 1.2
        if mi < 9.2: return 135 - 95 * (mi - 8.0) / 1.2
        return 40 - 22 * (mi - 9.2) / 3.9
    top = []
    for x in range(W):
        mi = x / (W - 1) * 13.1
        top.append(int(H - 10 - elev(mi) * 0.75))
    def pix(x, y):
        mi_px = (W - 1) / 13.1
        if abs(y - top[x]) <= 1: return (34, 102, 51)
        if y > top[x] and y < H - 10: return (186, 226, 190)
        if y >= H - 10: return (90, 90, 90) if (x % round(mi_px) == 0) else (240, 240, 240)
        if x % round(mi_px) == 0: return (225, 225, 225)
        return (255, 255, 255)
    return png_bytes(W, H, pix)


def drum_grid_png(pattern):
    """16-step grid, one row per instrument, 20 px cells."""
    rows = list(pattern.values()); W, H = 16 * 20, len(rows) * 20
    def pix(x, y):
        r, c = y // 20, x // 20
        if x % 20 == 0 or y % 20 == 0: return (60, 60, 60)
        if rows[r][c] == 'x': return (230, 120, 40) if r != 2 else (240, 200, 60)
        return (35, 35, 40) if (c // 4) % 2 == 0 else (48, 48, 55)
    return png_bytes(W, H, pix)


IMAGES = {
    'elev': ('bay-half-elevation.png', elevation_png()),
    'drums': ('pattern-sf-bounce.png', drum_grid_png({'kick': 'x-----x---x-----', 'snare': '----x-------x---',
                                                      'hat': 'x-x-x-xxx-x-x-x-', 'perc': '-----x-------x-x'})),
}

# ---------------- ENML / ENEX helpers ----------------

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'\[\[(https?://[^ \]]+) ([^\]]+)\]\]', lambda m: f'<a href="{m.group(1)}">{m.group(2)}</a>', s)
    return s


def enml(body):
    out, lst, table = [], None, []
    def flush():
        nonlocal lst, table
        if lst: out.append(f'<{lst[0]}>' + ''.join(f'<li>{inline(i)}</li>' for i in lst[1]) + f'</{lst[0]}>'); lst = None
        if table:
            rows = []
            for i, r in enumerate(table):
                cells = [c.strip() for c in r.strip().strip('|').split('|')]
                tag = 'b' if i == 0 else None
                rows.append('<tr>' + ''.join(f'<td style="border:1px solid #ccc;padding:4px">' + (f'<b>{inline(c)}</b>' if tag else inline(c)) + '</td>' for c in cells) + '</tr>')
            out.append('<table style="border-collapse:collapse">' + ''.join(rows) + '</table>'); table = []
    for line in body.strip('\n').split('\n'):
        line = line.rstrip()
        m_ol = re.match(r'^\d+\. (.*)', line)
        if line.startswith('|'):
            if lst: flush()
            table.append(line); continue
        if table: flush()
        if line.startswith('- '):
            if lst and lst[0] != 'ul': flush()
            lst = lst or ('ul', []); lst[1].append(line[2:]); continue
        if m_ol:
            if lst and lst[0] != 'ol': flush()
            lst = lst or ('ol', []); lst[1].append(m_ol.group(1)); continue
        flush()
        if not line: out.append('<div><br/></div>')
        elif line.startswith('# '): out.append(f'<h3>{inline(line[2:])}</h3>')
        elif line.startswith('[ ] ') or line.startswith('[x] '):
            out.append(f'<div><en-todo checked="{"true" if line[1] == "x" else "false"}"/>{inline(line[4:])}</div>')
        elif line.startswith('> '): out.append(f'<blockquote>{inline(line[2:])}</blockquote>')
        elif line == '---': out.append('<hr/>')
        elif line.startswith('{IMG:'):
            name, data = IMAGES[line[5:-1]]
            out.append(f'<div><en-media hash="{hashlib.md5(data).hexdigest()}" type="image/png"/></div>')
        else: out.append(f'<div>{inline(line)}</div>')
    flush()
    return ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n'
            '<en-note>' + ''.join(out) + '</en-note>')


def enex_stamp(d):
    return dt(d).astimezone(UTC).strftime('%Y%m%dT%H%M%SZ')


def note_xml(n, body=None, updated=None):
    body = body or n['body']
    x = ['  <note>', f'    <title>{html.escape(n["title"], quote=False)}</title>',
         f'    <created>{enex_stamp(n["created"])}</created>', f'    <updated>{enex_stamp(updated or n["updated"])}</updated>']
    x += [f'    <tag>{html.escape(t, quote=False)}</tag>' for t in n.get('tags', [])]
    x.append('    <note-attributes>')
    x.append('      <author>David Barron</author>')
    if n.get('url'):
        x.append('      <source>web.clip7</source>')
        x.append(f'      <source-url>{html.escape(n["url"])}</source-url>')
    x.append('    </note-attributes>')
    x.append('    <content>\n      <![CDATA[' + enml(body) + ']]>\n    </content>')
    for key in re.findall(r'\{IMG:(\w+)\}', body):
        name, data = IMAGES[key]
        w, h = struct.unpack('>II', data[16:24])
        b64 = base64.encodebytes(data).decode()
        x.append(f'    <resource>\n      <data encoding="base64">\n{b64}      </data>\n      <mime>image/png</mime>\n'
                 f'      <width>{w}</width>\n      <height>{h}</height>\n'
                 f'      <resource-attributes>\n        <file-name>{name}</file-name>\n      </resource-attributes>\n    </resource>')
    x.append('  </note>')
    return '\n'.join(x)


def enex(notes_xml, export_date):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">\n'
            f'<en-export export-date="{enex_stamp(export_date)}" application="Evernote" version="{VERSION}">\n'
            + '\n'.join(notes_xml) + '\n</en-export>\n')


def safe(title):
    return re.sub(r'[/:]', '-', title).strip()


NOTES = []
def note(notebook, title, created, updated, project_ids, body, tags=(), url=None, notes='', export_body=None, export_updated=None):
    NOTES.append(dict(notebook=notebook, title=title, created=created, updated=updated or created, project_ids=project_ids,
                      body=body, tags=list(tags), url=url, notes=notes, export_body=export_body, export_updated=export_updated))

NONE = ['project_none']
RUN = ['project_endurance_training']
CLUTTER = 'HARD CASE: personal clutter — recipe/meal-prep note (also repeated in the Recipes whole-notebook export)'

# =====================================================================================================================
# Recipes (personal clutter)
# =====================================================================================================================
note('Recipes', 'Chicken burrito bowls (meal prep x5)', '2024-02-11 18:20', '2025-11-16 19:05', NONE, '''
Makes 5 bowls. ~45 min total, most of it rice + oven time.

# Ingredients
- 2.5 lb boneless skinless chicken thighs
- 1.5 cups dry jasmine rice (cooked with 1 tbsp lime juice + cilantro after)
- 2 cans black beans, rinsed
- 1 bag frozen corn (roast it on the sheet pan with the chicken for the last 10 min)
- 1 jar salsa verde
- 2 tbsp taco seasoning (or: 2 tsp cumin, 2 tsp chili powder, 1 tsp smoked paprika, 1 tsp garlic powder, salt)
- 2 limes
- plain nonfat greek yogurt instead of sour cream

# Steps
1. Oven 425F. Toss chicken with seasoning + 1 tbsp oil. 22-25 min, internal 175F for thighs.
2. Rice cooker: 1.5 cups rice, 2.25 cups water.
3. Rest chicken 5 min, chop. Squeeze one lime over it.
4. Divide: rice, beans, corn, chicken. Salsa + yogurt go in a separate little container or it gets soggy by day 3.

# Macros (per bowl, my numbers from MyFitnessPal)
| kcal | protein | carbs | fat |
| 612 | 52 g | 64 g | 15 g |

11/16/25: swapped to thighs from breast permanently. way less dry on day 4-5. bumped chicken from 2 lb to 2.5 lb.
''', tags=['meal-prep', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Greek yogurt overnight oats', '2024-03-03 22:41', '2026-01-18 21:12', NONE, '''
Per jar (make 4 on Sunday night, they last to Thursday):
- 1/2 cup rolled oats
- 3/4 cup nonfat greek yogurt
- 1/2 cup unsweetened almond milk
- 1 scoop vanilla whey (~25 g protein)
- 1 tbsp chia seeds
- 1/2 cup frozen blueberries on top (they thaw overnight)
- pinch of salt + cinnamon

Shake the whey with the milk first in the jar or it clumps.

Macros per jar: ~455 kcal, 44 g protein, 52 g carbs, 8 g fat.

Variations
- PB: swap blueberries for 1 tbsp PB2 + half banana (+60 kcal)
- coffee: 2 oz cold brew instead of half the milk. good before the morning long run
- pumpkin (fall): 1/4 cup canned pumpkin + pumpkin spice

1/18/26: wide-mouth pint jars > the plastic tubs, nothing leaks in the backpack.
''', tags=['breakfast', 'meal-prep', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Turkey chili (big pot)', '2024-10-27 17:03', '2025-12-07 16:40', NONE, '''
Big dutch oven, 7-8 servings. Freezes great in the 32 oz deli containers.

- 2 lb 93/7 ground turkey
- 1 yellow onion, 1 red bell pepper, 4 cloves garlic
- 2 cans kidney beans + 1 can pinto, rinsed
- 1 can (28 oz) crushed tomatoes + 1 can diced fire-roasted
- 1 cup low sodium chicken broth
- 3 tbsp chili powder, 1 tbsp cumin, 2 tsp oregano, 1 tsp cocoa powder (trust it), 1 chipotle in adobo minced
- salt to taste at the end, not the start

Brown turkey in 2 batches (crowding = gray steamed meat). Onion/pepper 6 min. Spices in for 1 min. Everything else, simmer 45 min lid off the last 15.

Per serving (1/8 pot): 362 kcal, 33 g protein, 34 g carbs, 9 g fat.

Top with greek yogurt + scallions. With 1 cup rice it's ~565 kcal.

12/7/25: finals grading week batch. doubled the chipotle, good. froze 4.
''', tags=['meal-prep', 'freezer', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Sheet-pan salmon + potatoes', '2025-01-19 18:55', '2025-10-26 19:30', NONE, '''
2 servings, 30 min, one pan.

- 2 salmon fillets (~6 oz each), skin on
- 1 lb baby potatoes halved
- 1 bunch asparagus or a bag of green beans
- 1 tbsp olive oil, lemon, dill, garlic powder, salt, pepper

1. 425F. Potatoes first, oil + salt, 15 min.
2. Push potatoes to the edges, salmon in the middle skin down, veg around it. 12 more min.
3. Lemon + dill when it comes out.

Per serving: 520 kcal, 40 g protein, 38 g carbs, 22 g fat.

Not great as meal prep (reheated salmon smells up the office microwave). Cook it fresh on Mon/Thu.
''', tags=['dinner', 'fish'], notes=CLUTTER)

note('Recipes', 'Egg white muffin cups', '2025-11-09 20:14', '2025-11-09 20:58', NONE, '''
12 cups. Two cups + toast = breakfast during the week.

- 1 carton (32 oz) liquid egg whites
- 4 whole eggs
- 1 cup chopped spinach, 1/2 red pepper, 1/2 onion (sauteed first, otherwise watery)
- 1/2 cup reduced fat feta
- salt, pepper, everything bagel seasoning on top

Silicone muffin tray, 350F for 22 min. Let cool in the tray 5 min.

Per 2 cups: 168 kcal, 24 g protein, 4 g carbs, 6 g fat.

Note: the metal tray needs a lot of spray, first batch welded itself in. use silicone.
''', tags=['breakfast', 'meal-prep', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Beef and broccoli (lean)', '2025-12-14 19:22', '2025-12-14 20:10', NONE, '''
4 servings.

- 1.5 lb flank steak, sliced thin against the grain (freeze 20 min first, easier to slice)
- 1 big head broccoli (or 2 bags florets)
- Sauce: 1/3 cup low-sodium soy, 2 tbsp oyster sauce, 1 tbsp honey, 1 tbsp cornstarch, 1 tsp sesame oil, 1/2 cup water, garlic + ginger
- 1 cup dry rice for 4 portions (cook 2 cups if not cutting)

Sear beef in 2 batches, very hot pan, 90 s per side. Out. Steam broccoli 3 min in the same pan with a splash of water. Beef back, sauce in, 2 min till glossy.

Per serving (with 1/4 cup dry rice): 478 kcal, 41 g protein, 45 g carbs, 14 g fat.
''', tags=['dinner', 'meal-prep', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Protein pancakes', '2026-01-11 10:02', '2026-01-11 10:40', NONE, '''
Sunday after long run. Makes ~8 small pancakes, 2 servings.

- 1 cup oat flour (blend rolled oats)
- 1 scoop vanilla whey
- 1 tsp baking powder, pinch salt, cinnamon
- 2 eggs
- 3/4 cup nonfat greek yogurt
- 1/3 cup milk (more if thick)

Medium-low heat, they burn fast because of the whey. Flip when edges look dry.

Per serving: 405 kcal, 37 g protein, 42 g carbs, 9 g fat (before syrup; 2 tbsp real maple = +104 kcal).
''', tags=['breakfast', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Lentil dal + rice', '2026-02-22 18:44', '2026-02-22 19:51', NONE, '''
Cheap week recipe. 6 servings.

- 2 cups red lentils, rinsed until water runs mostly clear
- 1 onion, 4 garlic, thumb of ginger
- 1 can diced tomatoes, 1 can light coconut milk, 4 cups water
- 2 tsp turmeric, 2 tsp cumin, 1 tsp garam masala, 1/2 tsp chili flakes
- spinach at the end, lemon

Onion 8 min, garlic/ginger/spices 1 min, lentils + tomatoes + water 25 min stirring. Coconut milk last 5 min.

Per serving dal only: 318 kcal, 18 g protein, 46 g carbs, 7 g fat. Low protein by my standards -> serve with 2 eggs or a chicken thigh on the side.
''', tags=['dinner', 'vegetarian', 'cheap'], notes=CLUTTER)

note('Recipes', 'Meal prep Sunday — shopping list template', '2026-01-25 11:30', '2026-03-08 12:05', NONE, '''
Copy this every Sunday. Kroger on Prices Fork, go before 10.

# Protein
[ ] chicken thighs 2.5 lb
[ ] 93/7 ground turkey 2 lb (every other week)
[ ] eggs 18
[ ] egg whites carton
[ ] nonfat greek yogurt 32 oz x2
[ ] cottage cheese 24 oz
[ ] whey (check tub, ~6 scoops left = buy)
# Carbs
[ ] jasmine rice (bulk)
[ ] rolled oats
[ ] potatoes 3 lb
[ ] bananas x7
[ ] frozen blueberries
[ ] tortillas (high fiber)
# Veg
[ ] spinach, broccoli, bell peppers x3, onions, garlic
[ ] frozen corn + green beans
# Other
[ ] salsa verde, soy sauce, chipotle in adobo
[ ] coffee

Budget target: under $95/week. Last 4 weeks: $88, $102 (whey), $79, $91.
''', tags=['meal-prep', 'shopping'], notes=CLUTTER)

note('Recipes', 'Cottage cheese pasta sauce', '2026-03-15 20:40', '2026-03-15 21:02', NONE, '''
Saw this everywhere, actually good.

- 1 cup low-fat cottage cheese
- 1/2 cup jarred marinara
- 1/4 cup parmesan
- garlic, chili flakes, basil
Blend until smooth, warm gently in a pan (don't boil, it splits).

Over 3 oz dry protein pasta (Barilla Protein+) + 4 oz chicken breast:
~720 kcal, 74 g protein, 76 g carbs, 13 g fat. Big bowl.

Next time: add roasted red peppers to the blender.
''', tags=['dinner', 'high-protein'], notes=CLUTTER)

note('Recipes', 'Post-long-run smoothie', '2026-05-10 11:18', '2026-05-10 11:25', NONE, '''
Within 30 min of anything over 90'.

- 1 banana (frozen)
- 1 cup frozen mango
- 1 scoop whey
- 1 cup skim milk
- 1 tbsp honey
- pinch of salt (actually helps on hot days)
- ice

~520 kcal, 36 g protein, 88 g carbs, 3 g fat. Roughly 3:1 carb:protein which is what the coach article said.
''', tags=['smoothie', 'recovery'], notes=CLUTTER)

note('Recipes', 'Chicken shawarma wraps', '2026-06-14 18:10', '2026-06-14 19:35', NONE, '''
Marinade the night before. 6 wraps.

Marinade (for 2 lb thighs): 1/2 cup nonfat greek yogurt, juice of 1 lemon, 3 garlic, 2 tsp cumin, 2 tsp paprika, 1 tsp coriander, 1/2 tsp turmeric, 1/2 tsp cinnamon, salt.

Bake 425F 25 min on a rack, then broil 3 min for the char. Slice.

Wrap: high-fiber tortilla, chicken, cucumber/tomato/red onion, garlic yogurt sauce (yogurt + garlic + lemon + dill).

Per wrap: 445 kcal, 41 g protein, 30 g carbs, 16 g fat.

Rebuttal week dinner. made these 2x.
''', tags=['dinner', 'meal-prep', 'high-protein'], notes=CLUTTER)

CHIA_V1 = '''
For the SF fridge (shared kitchen, label the jar!). 4 servings.

- 1/2 cup chia seeds
- 2 cups unsweetened soy milk
- 1 cup nonfat greek yogurt
- 2 scoops vanilla protein
- 2 tbsp maple
- vanilla, pinch salt

Whisk, rest 10 min, whisk again (prevents clumps), fridge overnight. Top with berries.

Per serving: 330 kcal, 27 g protein, 26 g carbs, 13 g fat.
'''
note('Recipes', 'Overnight chia pudding', '2026-08-23 21:40', '2026-10-04 20:15', NONE, CHIA_V1 + '''
10/4: dropped the maple to 1 tbsp and added 1/2 cup canned pumpkin + pumpkin spice for the fall version. per serving now ~315 kcal. taper week = less sugar anyway.
''', tags=['breakfast', 'meal-prep', 'high-protein'], notes=CLUTTER, export_body=CHIA_V1, export_updated='2026-08-23 21:58')

# =====================================================================================================================
# Training (project_endurance_training)
# =====================================================================================================================
note('Training', 'Zone 2 HR numbers', '2025-10-26 21:15', '2025-11-02 20:44', RUN, '''
From the 30-min solo TT on the track 10/19 (avg HR last 20 min = 178). Using LTHR ~178.

| zone | % LTHR | bpm | use |
| Z1 | < 81% | < 144 | recovery jogs, cooldowns |
| Z2 | 81-89% | 144-158 | almost everything. aim 148-154 |
| Z3 | 90-93% | 159-165 | avoid ("grey zone") |
| Z4 | 94-99% | 166-176 | threshold work |
| Z5 | 100%+ | 177+ | strides, hills only |

Max HR seen this year: 197 (the 1 mile TT in august).
Bike Z2 is ~8 bpm lower for the same feel: use 136-148 on the trainer.

Rules for myself
- If HR drifts above 158 on an easy run -> walk 30 s, don't just "push through".
- Easy pace right now = 8:05-8:30/mi at 150. that's fine. it will come down.
- Check drift: first half vs second half avg HR on the 70' runs. < 5% decoupling = aerobically ok at that pace.
''', tags=['zones', 'heart-rate'])

note('Training', 'Week of 2025-11-10', '2025-11-10 06:40', '2025-11-16 21:30', RUN, '''
Target 9 h. Got 6 h 48. Labeling sprint + deployment data dump ate Wed.

| day | session | time | notes |
| Mon | run Z2 | 1:00 | 7.2 mi @ 8:20, HR 151 |
| Tue | trainer bike Z2 | 1:15 | HR 141, podcast |
| Wed | — | 0 | in the lab till 11pm |
| Thu | run Z2 | 0:50 | 6.0 mi, legs flat |
| Fri | — | 0 | |
| Sat | long run | 1:38 | 12.0 mi @ 8:10, HR 153, decoupling 4.1% |
| Sun | elliptical | 0:45 | gym before grading |

- Sleep avg 6:20 (bad). That's the main thing.
- Long run was good despite everything, 4.1% drift is my best this fall.
- Next week: protect Wed. even 30' easy counts.
''', tags=['log', 'weekly'])

note('Training', '2026 base-building plan — overview', '2025-12-28 15:20', '2026-01-04 18:02', RUN, '''
Year 2 of the multi-year aerobic plan. Not chasing races until fall.

# Principles
- 80-90% of time in Z1/Z2. One quality session/week max during base, none during heavy work weeks.
- Volume measured in **hours**, not miles: 8 h -> 11 h/week by end of summer.
- Running 4-5x/week, cycling 2x, elliptical when legs need a break.
- Long run grows 90' -> 120' by August, never more than +10'/2 weeks.
- Down week every 4th week (~70% volume).

# Blocks
| block | dates | hours/wk | focus |
| 1 | Jan 5 - Feb 28 | 8-9 | consistency, strides 2x/wk |
| 2 | Mar 2 - Apr 26 | 8-9 | hold volume through UIST deadline; 1 threshold/wk when possible |
| 3 | May 4 - Jul 26 | 9-10 | long run to 110', hills |
| 4 | Aug 10 - Oct 15 | 9-11 | half marathon specific (fall race w/ Owen?) |

# Checks
- Resting HR (Garmin, 7-day avg): 49 now. want < 46 by summer.
- Easy pace at 150 bpm: 8:15 now. want < 7:45.
- Monthly: 30' TT or a 5k effort, just to see.
''', tags=['plan', '2026'])

note('Training', 'Treadmill workouts for bad weather', '2026-01-20 22:10', '2026-02-01 20:30', RUN, '''
Blacksburg ice days. Set incline 1% always.

1. **Easy progression** 50': 10' @ 6.8 mph, then +0.1 mph every 5' up to 7.5. HR cap 155.
2. **Strides on the belt** 45' easy @ 7.0 + 6 x 20 s @ 10.0 mph, step off to the rails for recovery (carefully).
3. **Hill grind** 40' @ 6.0 mph, incline 4-6%, keeps HR in Z2 without pounding.
4. **Cruise intervals** (only in quality weeks) 15' WU, 4 x 6' @ 9.2 mph (6:31/mi) w/ 2' @ 6.5, 10' CD.
5. **Boredom killer** 60' alternating 5' @ 7.0 / 5' @ 7.3 with a different podcast each segment.

Gym treadmill reads ~3% fast vs Garmin footpod. Trust HR, not the screen.
''', tags=['treadmill', 'workouts'])

note('Training', 'Bike + elliptical sessions', '2026-02-08 19:45', '2026-02-08 20:05', RUN, '''
Cross-training menu for when running volume is capped (shins were cranky last week).

# Trainer (dumb trainer + HR strap)
- 75' Z2 @ HR 136-148, cadence 85-90. Gear 50x17 on the trainer ~ 155 W estimate.
- 60' with 6 x 3' high cadence (100+) / 2' normal.
- 90' long Z2 on Saturdays when the long run moves to Sunday.

# Elliptical (gym)
- 45-60' Z2 = level 9, ~150 strides/min, HR 140-150.
- Counts as roughly 0.8x a run for "hours" in the plan, so 60' elliptical logged as 48'.

Feb so far: 3 trainer sessions, 2 elliptical. Shins fine now.
''', tags=['cross-training', 'bike', 'elliptical'])

note('Training', 'Spring race calendar ideas', '2026-02-15 21:50', '2026-03-01 19:12', RUN, '''
Not racing seriously, but one tune-up per block keeps it honest.

- Apr 18 — Huckleberry Trail 10K (local, flat out-and-back). probably. right after UIST deadline though.
- May 16 — downtown Roanoke 5K (night race?) — skip, NeurIPS aftermath.
- Jun 6 — track mile at the summer series. for fun. goal sub-4:50.
- Fall — half marathon w/ Owen. he wants something fast + flat in October. look at Bay Area options if the SF thing actually happens.

3/1: Owen says he's in for an October half wherever I end up. registration usually opens in June.
''', tags=['races', 'planning'])

note('Training', 'Mile time trial — 2026-03-07', '2026-03-07 11:05', '2026-03-07 13:20', RUN, '''
Solo on the VT track, 10:30am, 41F, light wind on the back straight.

**4:52.8** (73.1 / 73.6 / 74.2 / 71.9)

- Warmup 20' easy + drills + 4 strides.
- Lap 3 slump as usual. Didn't have the gear change I used to.
- HR max 194, avg last 2 laps 189.
- College PR 4:14. Not the point anymore, but faster than December (4:58).

Takeaway: aerobic base is clearly better (lap 4 was the fastest), top-end speed is gone. That's expected and fine. Strides 2x/week stay in.
''', tags=['time-trial', 'mile'])

note('Training', 'Running shoe rotation', '2026-04-12 18:30', '2026-08-30 16:10', RUN, '''
| shoe | role | miles (as of 8/30) | retire at |
| daily trainer #1 (grey) | easy days | 448 | 450 -> retiring now |
| daily trainer #2 (blue) | easy days | 112 | 450 |
| max cushion | long runs | 296 | 500 |
| tempo shoe (no plate) | threshold + strides | 188 | 350 |
| race shoe (plate) | race + 1 rehearsal | 21 | 200 |

- Rotate the two dailies, never same shoe two days in a row.
- Race shoe: only the 10-mile rehearsal at goal pace + the half itself.
- Old daily trainers go in the donation bag (SF Goodwill on Mission takes them).
''', tags=['gear', 'shoes'])

note('Training', 'Block 3 review (May–Jul)', '2026-07-26 20:20', '2026-07-26 21:15', RUN, '''
12 weeks, May 4 - Jul 26.

- Average 8.6 h/week (plan said 9-10). Two holes: NeurIPS deadline week (5.1 h) and the week of Jul 27 coming up (rebuttal + leave paperwork; expect ~6).
- Long run peaked at 1:52 (14.3 mi) on 7/11.
- Resting HR 7-day avg: 46 (from 49 in Jan).
- Easy pace at 150 bpm: 7:48 (from 8:15).
- Decoupling on 100'+ runs: 3-5%.
- Track mile 6/6: 4:49.6. small win.
- Missed: hills. only did hill reps 3 times.

For Block 4: the move to SF is 8/8, so week of 8/3 is a write-off. Start Block 4 properly on 8/10. SF has hills whether I like it or not.
''', tags=['review', 'block-3'])

note('Training', 'Block 4 plan (Aug 10 – Oct 15)', '2026-08-02 17:40', '2026-08-30 19:05', RUN, '''
Goal race: **Bay Area Half, Thu Oct 15**, with Owen. Goal ~1:25 (6:29/mi). Owen wants 1:22.
Volume 9-11 h/week. Running ~55-62 mi at peak.

| week of | hours | key sessions |
| Aug 10 | 9 | settle in SF. all easy + strides. find a flat loop (Embarcadero?) |
| Aug 17 | 9.5 | threshold 3 x 10' @ 6:15-6:20, long 100' |
| Aug 24 | 10 | hills 8 x 60 s, long 105' w/ last 20' @ 6:45 |
| Aug 31 | 7 (down) | strides only, long 85' |
| Sep 7 | 10.5 | threshold 2 x 15', long 110' |
| Sep 14 | 11 | 10 mi @ goal pace rehearsal in race shoes (Sat), long 115' Sun? no — one or the other |
| Sep 21 | 10.5 | 5 x 1 mi @ 6:05 w/ 90 s, long 110' with 6 mi @ 6:35 |
| Sep 28 | 10 | threshold 3 x 12', long 100' |
| Oct 5 | 8 | UIST talk week (Oct 7). keep it simple: 1 x 4 mi @ 6:25, long 80' |
| Oct 12 | 5 + race | taper. Tue 4 x 1k @ 6:10 pace. race Thu |

Cycling 2 x 60-75' Z2 when the running is under 8 h. Elliptical unlikely (no gym yet, check the incubator's).

8/30 update: Aug 17 + 24 done as written. HR at 6:15 pace on threshold = 172-174. good sign.
''', tags=['plan', 'block-4', 'half-marathon'])

note('Training', 'Daily macro targets (Block 4)', '2026-08-19 20:05', '2026-08-19 20:30', RUN, '''
Weight 147 lb. Not cutting during Block 4, just fueling.

| day type | kcal | protein | carbs | fat |
| hard / long day | 3,000 | 160 g | 410 g | 80 g |
| easy day | 2,700 | 160 g | 340 g | 80 g |
| rest / travel | 2,400 | 150 g | 270 g | 80 g |

- Protein ~1.1 g/lb, spread 4 x 40 g.
- Long runs > 90': 1 gel every 35-40'. practice the race gels (the caffeinated one at 60').
- Before threshold sessions: oats + banana 2 h before.
- Incubator kitchen is shared — prep Sunday, label everything.
''', tags=['nutrition', 'block-4'])

note('Training', 'Long run log — Block 4', '2026-08-16 10:50', '2026-10-11 11:40', RUN, '''
| date | route | time | dist | avg HR | notes |
| Aug 16 | Embarcadero -> Crissy Field out/back | 1:35 | 11.9 mi | 149 | foggy, perfect |
| Aug 23 | Golden Gate Park loop + Ocean Beach | 1:42 | 12.8 mi | 152 | last 20' @ 6:44 avg |
| Aug 30 | down week: GGP | 1:25 | 10.6 mi | 147 | |
| Sep 6 | Embarcadero -> Fort Mason -> Crissy | 1:50 | 14.0 mi | 151 | |
| Sep 13 | (rehearsal instead) 10 mi @ goal | 1:04:38 | 10.0 mi | 171 | 6:28 avg, race shoes. hard but controlled |
| Sep 20 | GGP + Great Highway | 1:52 | 14.3 mi | 153 | 6 mi @ 6:36 in the middle |
| Sep 27 | Crissy + bridge out and back | 1:41 | 12.9 mi | 154 | windy on the bridge, HR up |
| Oct 4 | GGP easy | 1:20 | 10.3 mi | 148 | with Sam for the first 5 |
| Oct 11 | Embarcadero easy | 0:55 | 7.4 mi | 146 | taper. legs bouncy |

Rehearsal 9/13 is the confidence one: 6:28 for 10 miles at 171 means 1:25 is realistic if the course is as flat as advertised.
''', tags=['long-run', 'block-4', 'log'])

note('Training', 'Bay Area Half — race plan (Oct 15)', '2026-09-27 21:30', '2026-10-13 20:45', RUN, '''
Thu Oct 15, 7:00 am start. With Owen (he flies in Tue night, crashes on the incubator couch).

{IMG:elev}
Course profile from the race site (sketched): flat first 6.8 mi, ~120 ft climb miles 7-8, descent mile 9, flat-ish run-in.

# Goal
- A: 1:24:59 or better (6:29/mi)
- B: sub-1:26
- C: finish strong, no blow-up on the hill

# Splits plan
| miles | pace | notes |
| 1-3 | 6:32-6:35 | let Owen go. he's running 6:16s |
| 4-6 | 6:27-6:29 | settle, HR should be ~172 |
| 7-8 | effort, not pace (6:40s ok) | the climb. don't chase pace |
| 9 | 6:25 | use the downhill, relax shoulders |
| 10-13.1 | 6:20 -> whatever's left | |

# Fuel
- 2.5 h before: bagel + PB + banana, coffee.
- Gel at mile 4.5 and mile 8.5 (caffeinated one at 8.5). water at every station, sip.

# Logistics
- Bib pickup Wed 4-7 pm.
- Leave the house 5:55.
- Bag check closes 6:45.
''', tags=['race', 'half-marathon', 'plan'])

note('Training', 'Race recap — Bay Area Half 1:24:51', '2026-10-15 21:30', '2026-10-16 08:10', RUN, '''
**1:24:51** (6:29/mi avg by chip). A goal by 8 seconds. Owen ran 1:22:10, hit his goal on the nose.

| mile | split | | mile | split |
| 1 | 6:33 | | 8 | 6:37 |
| 2 | 6:30 | | 9 | 6:26 |
| 3 | 6:29 | | 10 | 6:24 |
| 4 | 6:27 | | 11 | 6:22 |
| 5 | 6:26 | | 12 | 6:20 |
| 6 | 6:28 | | 13 | 6:18 |
| 7 | 6:41 | | last 0.14 (watch long) | 0:50 |

- Avg HR 173, max 188 in the last 400 m.
- Hill (7-8) cost ~20 s total vs flat pace, exactly what the plan allowed.
- Gels at 4.5 / 8.5 worked, no stomach issues.
- Negative split second half. First race since college where the last 3 miles were the fastest.

Next: 2 weeks easy, then think about Block 5 / a spring full? Owen keeps saying CIM.
''', tags=['race', 'half-marathon', 'results'])

# =====================================================================================================================
# Gear & Travel
# =====================================================================================================================
note('Gear & Travel', 'Carry-on essentials (master list)', '2024-05-12 14:20', '2025-11-23 18:45', NONE, '''
The list I copy for any trip. One carry-on + backpack, no checked bag.

# Backpack
- laptop + charger (USB-C 65 W), phone charger, watch charger
- USB-C -> HDMI adapter (presentations!)
- headphones
- passport / ID, wallet
- water bottle (empty through security)
- book or kindle

# Carry-on
- running shoes + 2 running kits
- 3 shirts, 2 pants, 1 nicer outfit
- socks/underwear for days + 1
- toiletry bag (3-1-1 bag lives in it permanently)
- light rain jacket

11/23/25: added watch charger after forgetting it at Thanksgiving. Garmin died day 2.
''', tags=['packing', 'travel'], notes='HARD CASE: personal clutter — generic packing list')

note('Gear & Travel', 'Bike — rear derailleur fix', '2026-05-24 16:30', '2026-06-06 12:10', NONE, '''
Problem: chain skips in the 4th/5th cog under load, ghost shifting on the trainer too. Started after the bike fell over in the bike rack 5/20.

What I checked
- Barrel adjuster: 1/4 turn counter-clockwise x2 -> better on 4th, still skips on 5th.
- Derailleur hanger looks bent inward when sighting from behind. probably the real problem.
- Cable not frayed.

Shop (Downtown Blacksburg bike shop) quote
- hanger alignment $15, if bent too far new hanger ~$22 + install
- full tune $75 (skip)

6/6: hanger was bent ~4 mm. they aligned it, $15 + $6 for a new cable end. shifting perfect. Ordered a spare hanger ($22) to keep in the drawer because the rack at the apartment is cursed.
''', tags=['bike', 'repair'], notes='HARD CASE: personal clutter — bike repair note (PERSON.md §5 derailleur theme)')

note('Gear & Travel', 'Dublin wedding — logistics', '2026-06-07 21:05', '2026-07-02 22:20', NONE, '''
Niamh's wedding, Sat July 11. RSVP by June 15.

Flights (looked 6/7)
- ROA -> IAD -> DUB Wed 7/8 overnight, land Thu 7/9 morning
- back Tue 7/14 (Mon was $180 more)
- ~$870 economy with a bag. via BOS: cheaper but 2 stops on return

Hotel: family block near the venue, rate in Niamh's email. Need to book by 6/25. Thu–Sat at the block, Sun–Mon with the cousins in Drumcondra.
Dress code: smart / summer suit.

[x] RSVP sent 6/9 (yes, 1 guest = just me)
[x] book flight (6/14)
[ ] book hotel
[ ] gift from the registry

7/2 update: hotel booked (3 nights). Gift: the Irish linen set off the registry, $120, shipped to Niamh's. Bring laptop, NeurIPS rebuttal lands right after I'm back (7/24-ish), so Mon 7/13 = work day at the cousins'. Leave paperwork can wait until 7/15.
''', tags=['travel', 'family'], notes='HARD CASE: personal clutter — family-logistics only')

note('Gear & Travel', 'SF move checklist', '2026-07-12 20:40', '2026-08-09 22:15', NONE, '''
Moving Sat Aug 8. Flying BWI? no — ROA -> SFO via CLT. Room at the incubator house is furnished.

# Before (Blacksburg)
[x] sell desk + chair (FB marketplace, $60)
[x] donate kitchen stuff I won't ship
[x] ship 6 boxes UPS ground (books, kitchen basics, winter clothes) -> arrive ~8/12
[x] bike: box it at the shop ($50) and ship? -> shipped w/ BikeFlights, $89
[x] cancel internet (last day 8/7), electric transfer off 8/8
[x] USPS mail forwarding to SF starting 8/8
[x] lease end walkthrough 8/7 10am, keys back
[x] car: sold to the dealership on 7/30. cancel car insurance after title transfer -> done 8/3
[x] VT parking permit refund (prorated)
# Arrival (SF)
[x] keys from Lena / house manager
[x] Clipper card on phone
[ ] update address: bank, VT records (Grace), Garmin, Evernote billing
[x] grocery run, label fridge shelf
[ ] find a gym or pool
[ ] CA driver license? only needed if staying > 10 days for residency... look it up

8/9: arrived 8/8 at 7:40 pm. boxes not here yet. house is great. Sam showed me the run route to the Embarcadero.
''', tags=['move', 'sf', 'checklist'], notes='HARD CASE: personal clutter — moving checklist')

note('Gear & Travel', 'New Mac setup checklist', '2026-08-04 19:15', '2026-08-06 23:40', NONE, '''
New MacBook arrived 8/4. Clean setup, no migration assistant this time.

[x] macOS updates, FileVault on
[x] Homebrew
[x] brew install git gh node pnpm uv jq ripgrep fd tmux
[x] git config user.name / user.email, new ssh key -> GitHub (personal + Mathetic-PBC org)
[x] iTerm2 + zsh config from dotfiles repo
[x] VS Code + settings sync
[x] Claude Code (npm i -g), log in
[x] Obsidian, open the vaults from iCloud
[x] 1Password, Arc, Slack, Zoom, Linear
[x] FL Studio 2025 reinstall + license, copy packs from external SSD
[ ] Time Machine to the external SSD (it's full, need a new one)
[ ] Garmin Express? (or just the phone app)
[x] trackpad: tap to click, three-finger drag (accessibility settings)
[x] Dock: autohide, remove everything

Old Mac: wipe after the move, sell or give to Sam.
''', tags=['laptop', 'setup'], notes='HARD CASE: personal clutter — laptop setup notes (PERSON.md §5)')

note('Gear & Travel', 'UIST 2026 packing list', '2026-09-29 22:10', '2026-10-05 21:30', ['project_tutortrace'], '''
Talk: **Wed Oct 7**, session "Learning & Tutoring" (chair: Tomás Reyes). 15 min + 5 Q&A. TutorTrace.
AV check with Tomás on Zoom was 10/2 — 16:9, HDMI at the podium, they provide a clicker but bring mine.

# Talk stuff
[x] laptop + charger
[x] USB-C -> HDMI adapter AND USB-C -> USB-C (some podiums have USB-C now)
[x] my clicker + spare AAA
[x] slides as PDF on a USB stick (backup if the laptop dies)
[x] slides + demo video in Drive, offline-available
[x] demo video as standalone mp4 (don't rely on embedded video in Keynote)
[x] printed speaker notes (1 page, big font)
[x] conference badge QR (email from registration)
# Clothes
[x] 1 nicer shirt for the talk day, 2 casual
[x] running kit x2 (keep the streak through taper-ish week; half is Oct 15)
[x] light jacket
# Misc
[x] business cards? -> Mathetic ones arrived 9/30, take 30
[ ] poster tube - no poster this time
[x] reimbursement: keep ALL receipts (VT travel funding approved, Grace says itemized receipts within 10 days)

10/5: packed. rehearsed the opening twice more. remember: 80 seconds max before the first figure.
''', tags=['uist', 'travel', 'packing', 'conference'],
     notes='UIST 2026 trip for the TutorTrace talk (2026-10-07); Gear & Travel notebook, packing-list format')

note('Gear & Travel', 'Race-day gear checklist', '2026-10-12 21:00', '2026-10-14 21:35', RUN, '''
Bay Area Half, Thu 10/15. Lay it all out Wed night.

[x] race shoes (plate) — 21 mi on them, fine
[x] socks (the thin ones), shorts with gel pockets, singlet
[x] bib + 4 pins (pick up Wed 4-7)
[x] Garmin charged, set to auto-lap 1 mi, data page: lap pace / lap time / HR
[x] 2 gels + 1 caffeinated gel
[x] throwaway long sleeve (old VT running club one) for the start corral
[x] anti-chafe
[x] post-race bag: dry shirt, sweats, recovery shake, phone charger
[x] ride to the start booked for 5:55 (Owen + me)
[x] breakfast staged: bagel, PB, banana, coffee pods
''', tags=['race', 'gear', 'checklist'])

# =====================================================================================================================
# Web Clips
# =====================================================================================================================
note('Web Clips', 'Voice tutors that talk while you code — what the first classroom pilots show', '2025-11-18 23:05', '2025-11-19 00:20',
     ['project_sophia'], '''
> my note: relevant to Sophia for Educators. their "interruptibility" point is basically what we argued for the IDE voice agent — the tutor should wait for a pause in editing, not fire on every error. also the teacher-side simulation idea in the last section = our simulated-student testing.
---
# Voice tutors that talk while you code: what the first classroom pilots show
By Rosa Delgado, The Learning Stack, November 2025

A new class of programming tutors does not wait for a typed question. They sit inside the editor, listen when invited, and answer out loud. Over the past year several university courses have piloted these voice-first assistants in introductory programming labs. The early reports are mixed in an interesting way: students like talking to them, instructors worry about what they say, and almost everyone underestimates how much timing matters.

**Talking changes the question.** In the pilots, students who spoke to the tutor asked longer and more exploratory questions than students who typed. A typed prompt tends to be "fix this error"; a spoken one is closer to "I think the loop is wrong but I'm not sure why the index goes past the end". Instructors read that difference as a sign that voice invites students to explain their own reasoning, which is the part of help-seeking they actually want to encourage.

**Interruptions are the main complaint.** Tutors that offered help automatically after an error were described as "a backseat driver". Several teams moved to a rule where the tutor only speaks after the student pauses editing for a while, or after the same error repeats. One lab assistant described the best version as "the TA who walks by, sees you're thinking, and keeps walking".

**Teachers want to rehearse the tutor.** The strongest request from instructors was not a better model. It was a way to test the tutor before students see it: feed it typical student mistakes, listen to what it says, and adjust its instructions. Some teams built simple simulators that replay anonymized student sessions against a configured tutor so a teacher can hear how it behaves on a bad day.

**What is still unknown.** None of the pilots measured learning outcomes carefully, and most ran for a few weeks. Accessibility questions (noisy labs, students who are not comfortable speaking English aloud) came up in every report and were not solved. The open question for the next round is less "can it explain code" and more "when should it say anything at all".
''', tags=['clip', 'ai-tutors', 'voice', 'sophia'], url='https://thelearningstack.net/2025/11/voice-tutors-in-the-ide',
     notes='web clip on voice-first coding tutors with David\'s note linking it to Sophia for Educators')

note('Web Clips', 'Why your easy runs feel hard: cardiac drift explained', '2025-12-03 22:40', '2025-12-03 22:52', RUN, '''
> my note: this is why I check decoupling on the long runs. keep the < 5% rule.
---
# Why your easy runs feel hard: cardiac drift explained
Trail & Track Weekly, Dec 2025

If you run at the same pace for an hour, your heart rate usually creeps up even though nothing about the effort changed. Exercise physiologists call this cardiovascular drift. As you warm up and sweat, plasma volume drops a little, the heart pumps slightly less blood per beat, and it compensates by beating faster. Heat, dehydration and poor sleep make it worse.

Coaches use drift as a cheap fitness test. Run a steady hour at an easy pace, compare the average heart rate of the first and second halves, and divide pace by heart rate for each half. If the ratio drops by less than about five percent, the pace is comfortably inside your aerobic range. If it drops by more, the pace is too ambitious for your current base, or the conditions were bad.

The practical advice is boring and effective: slow down on hot days, drink before you are thirsty on runs over an hour, and judge an easy run by heart rate and breathing rather than the watch pace. Fitness shows up as the same pace at a lower heart rate over months, not weeks.
''', tags=['clip', 'running-science', 'heart-rate'], url='https://trailandtrackweekly.com/training/cardiac-drift-easy-runs',
     notes='running-science web clip; tied to his base-building plan')

note('Web Clips', 'Chips, export controls and the long game', '2026-01-14 23:30', '2026-01-14 23:41', NONE, '''
# Chips, export controls and the long game
The Strategic Brief (newsletter), January 2026

The argument in this issue: export controls on advanced chips buy time, not victory. Restricting the newest accelerators slows a rival's frontier training runs, but it also creates a guaranteed domestic market for that rival's own chip designers, who no longer have to compete with the best foreign product at home.

Three things to watch over the next few years:
- **Yield, not node.** A rival can announce an advanced process; the question is what fraction of wafers come out usable and at what cost. Low yields make a chip a strategic demonstration rather than an industrial one.
- **The tooling chokepoint.** Lithography and some deposition tools are made by a handful of firms in allied countries. Controls on servicing and spare parts matter as much as controls on new machines.
- **Talent flows.** Engineers moving between firms and countries carry more know-how than any shipment.

The newsletter's conclusion is that the policy is best judged in five-year windows. Measured quarter to quarter it always looks either like a decisive win or a total failure, and it is neither.
''', tags=['clip', 'geopolitics', 'us-china'], url='https://thestrategicbrief.com/p/chips-export-controls-long-game',
     notes='geopolitics newsletter clip (PERSON.md §5 theme)')

note('Web Clips', 'The Catalan for club players', '2026-02-02 22:15', '2026-02-02 22:20', NONE, '''
# The Catalan for club players
ChessBytes, Opening Guides

1. d4 Nf6 2. c4 e6 3. g3 d5 4. Bg2 — the Catalan in one line.

Why club players like it: White fianchettoes the light-squared bishop so it stares down the long diagonal at Black's queenside. Even if Black grabs the c4 pawn, White usually gets it back with Qa4+ or Qc2 and a rook to c1, and the pressure on b7 lasts deep into the middlegame.

Plans to remember
- **Open Catalan (…dxc4):** don't rush to win the pawn back. Castle, Qc2 or Qa4+, Ne5 ideas. Black's problem is developing the c8 bishop.
- **Closed Catalan (…Be7, …O-O, …c6):** slow buildup. Qc2, Nbd2, e4 when ready. Patience wins.
- **Common trap:** in the open line, Black playing …b5 to hold the pawn often loses to a4 hitting the chain.

Typical mistake at 1500-1800: trading the g2 bishop for a knight. That bishop is the whole point.
''', tags=['clip', 'chess', 'openings'], url='https://chessbytes.net/openings/catalan-club-players',
     notes='online chess study clip (PERSON.md §5)')

note('Web Clips', 'How to appeal a parking citation', '2026-03-02 13:05', '2026-03-04 09:40', NONE, '''
> my note: ticket from 2/27 in the Perry St lot — the permit was on the dash, fell off the mirror. appeal within 10 business days. submitted 3/4 with the photo.
---
# How to appeal a parking citation
Campus Parking Services — Citations

Citations may be appealed online within 10 business days of the date of issue. Appeals received after that window are not reviewed.

What to include
- the citation number and your permit number
- a short explanation of why the citation should be voided or reduced
- supporting documents or photos (for example, a photo of a valid permit)

What does not count as grounds for appeal
- not seeing a sign
- parking for a short time
- other vehicles also parked in violation

You will receive a decision by email. If the appeal is denied, a second-level review can be requested within 10 business days of that decision.
''', tags=['clip', 'parking', 'admin'], url='https://parking.example.edu/citations/appeals',
     notes='HARD CASE: personal clutter — parking-ticket appeal clip (PERSON.md §5)')

note('Web Clips', 'A grand-strategy reading list for the rest of us', '2026-04-19 21:50', '2026-04-19 22:05', NONE, '''
> my note: have read 2 of these. next: the one on sea power. library has it.
---
# A grand-strategy reading list for the rest of us
The Strategic Brief (newsletter), April 2026

People keep asking for "one book on grand strategy". There isn't one. Here is a short path instead, ordered so each book makes the next easier.

1. **A classic on war and politics** — read the first book and the chapter on the trinity of passion, chance and reason. Skip the rest on a first pass.
2. **A history of the Peloponnesian War** — the Melian dialogue and the Sicilian expedition are the parts everyone cites; read them in context.
3. **A modern account of sea power and trade routes** — why geography still decides which countries can project force.
4. **A study of the Cold War's long containment strategy** — strategy as decades of patient, boring consistency.
5. **A recent book on US–China competition** — read it last, so you can tell which parts are new and which are old ideas in new clothes.

The common thread: strategy is the art of matching limited means to large ends over time. Most failures in these books come from ends growing while means stay the same.
''', tags=['clip', 'geopolitics', 'reading-list'], url='https://thestrategicbrief.com/p/grand-strategy-reading-list',
     notes='geopolitics reading list clip (PERSON.md §5)')

note('Web Clips', 'Lactate threshold testing without a lab', '2026-05-27 22:30', '2026-05-27 22:44', RUN, '''
> my note: my Oct 30' TT gave LTHR 178. redo it in August before Block 4 threshold work.
---
# Lactate threshold testing without a lab
Trail & Track Weekly, May 2026

You don't need finger pricks to estimate your threshold. Two field tests get most runners close enough to set training zones.

**The 30-minute time trial.** Warm up well, then run 30 minutes as hard as you can sustain evenly, alone, on a flat route. Your average heart rate over the last 20 minutes is a decent estimate of lactate-threshold heart rate. Your average pace is close to threshold pace, a little fast for most people because of the short duration.

**The recent-race method.** Pace from a recent 10K race, slowed by roughly 10 to 15 seconds per mile, approximates threshold pace for well-trained runners.

Use the result to set threshold sessions such as three to four repeats of eight to twelve minutes with short jog recoveries. Retest every eight to twelve weeks; the number moves as fitness changes. If the test day is hot or you slept badly, the result will be off, so pick a cool morning.
''', tags=['clip', 'running-science', 'threshold'], url='https://trailandtrackweekly.com/training/lactate-threshold-field-tests',
     notes='running-science clip; he applies it to his own zones')

note('Web Clips', 'Taiwan Strait shipping and the insurance question', '2026-06-21 23:10', '2026-06-21 23:18', NONE, '''
# Taiwan Strait shipping and the insurance question
The Strategic Brief (newsletter), June 2026

Most discussion of a crisis in the Taiwan Strait focuses on missiles and fleets. This issue looks at something duller and possibly more decisive: marine insurance.

A large share of global container traffic and much of the world's advanced chip output pass near the strait. Commercial shipping does not need a blockade to stop; it needs underwriters to raise war-risk premiums high enough, or to withdraw cover, and shipowners will reroute or wait. That decision is made in a handful of insurance markets, quickly, and without any government declaring anything.

The implication is that "gray-zone" pressure (inspections, exercises that close sea lanes for days, coast-guard incidents) can impose real economic costs while staying below the threshold of war. Planners who model only military thresholds miss the commercial ones, which come first.
''', tags=['clip', 'geopolitics', 'us-china'], url='https://thestrategicbrief.com/p/strait-shipping-insurance',
     notes='geopolitics newsletter clip (PERSON.md §5 theme)')

note('Web Clips', 'SF neighborhoods for first-time renters', '2026-07-19 22:00', '2026-07-21 23:15', NONE, '''
> my note: incubator house covers Aug-Nov. this is for after, if we stay. Inner Sunset / Cole Valley look right (park for running, N-Judah).
---
# SF neighborhoods for first-time renters
Bay Rent Guide, July 2026

**Inner Sunset.** Fog, Golden Gate Park on the doorstep, the N-Judah to downtown. Studios and one-bedrooms are a bit cheaper than the eastern neighborhoods. Good for people who run or have a dog.

**Cole Valley.** Small, quiet, walkable, close to the park and the N line. Fewer listings, they go fast.

**Mission / Mission Dolores.** Sunniest weather in the city, lots of food, more noise. Close to BART for the East Bay and the airport.

**SoMa / Mission Bay.** Newer buildings with amenities and higher rents. Close to Caltrain and many offices; quieter at night than you'd expect.

**Richmond.** Longer commute downtown, more space for the money, near the park and the ocean.

Tips: listings that ask for deposits before a viewing are scams. Expect to show income or a guarantor. Ask whether the unit is rent-controlled (generally buildings first occupied before mid-1979).
''', tags=['clip', 'sf', 'apartment'], url='https://bayrentguide.com/sf-neighborhoods-first-time-renters',
     notes='HARD CASE: personal clutter — apartment-search clip (PERSON.md §5)')

note('Web Clips', 'Heat and humidity: adjusting pace for fall races', '2026-08-27 22:20', '2026-08-27 22:31', RUN, '''
> my note: SF is not hot but Oct can surprise. if race morning > 65F, start at 6:35 not 6:32.
---
# Heat and humidity: adjusting pace for fall races
Trail & Track Weekly, August 2026

Fall race season starts in weather that can still be warm. A common rule of thumb: above roughly 60°F, add about 1 to 2 percent to goal pace for every 5°F, more if the humidity is high or the dew point is above 60.

Heat acclimation takes about 10 to 14 days of easy running in warm conditions. Most of the benefit (a larger plasma volume, earlier sweating, lower heart rate at a given pace) arrives in the first week. If your race may be warm but your training is cool, a few easy sessions in extra layers can help, but don't do workouts that way.

On race day: pour water on your head and neck early, not when you already feel hot; take fluids at every station on warm days; and start conservatively. In the heat, the runners who go out slow pass a lot of people in the last 5K.
''', tags=['clip', 'running-science', 'heat'], url='https://trailandtrackweekly.com/racing/heat-humidity-fall-races',
     notes='running-science clip tied to his October half-marathon plan')

# =====================================================================================================================
# Ideas
# =====================================================================================================================
note('Ideas', 'Juno — feature ideas', '2024-03-14 23:50', '2024-06-02 01:10', ['project_juno'], '''
Juno = a voice agent you can actually customize (personality, voice, memory), not a fixed assistant.

# Must have
- **Latency budget < 800 ms** end of speech -> first audio. streaming STT -> LLM (stream tokens) -> TTS on first sentence.
- barge-in: if I start talking, Juno stops mid-sentence.
- persona file (yaml): name, voice id, speaking style, things it knows about me, things it should never do.
- CLI first: `juno create`, `juno talk <name>`, `juno edit <name>`.

# Nice to have
- long-term memory: summarize each conversation into 5 bullets, retrieve top 3 by embedding next time.
- "walkie-talkie" mode for the lab web app (push to talk) vs always-listening mode on desktop.
- multiple Junos in one call (a debate between two personas?) — fun demo, probably useless.
- share a persona with a link.

# Not doing
- phone number / telephony. too much infra.
- custom wake word training. use push-to-talk.

6/2/24: STT is fine, TTS first-chunk latency is the bottleneck (~450 ms alone). try sentence-split + smaller voice model for the first sentence only.
''', tags=['juno', 'ideas', 'voice-agents'], notes='old (2024) Juno ideas note; predates the scope year')

note('Ideas', 'Juno voices — personality presets', '2024-07-21 22:35', '2024-07-28 00:20', ['project_juno'], '''
Starter personas for the lab web app demo. Each = system prompt + voice + speaking rate.

| preset | voice | rate | style |
| Coach | warm, low | 1.05 | short sentences, asks one question back, encouraging |
| Professor | neutral | 0.95 | explains with an example first, then the rule |
| Rubber duck | soft | 1.0 | says almost nothing, repeats back what you said as a question |
| Debater | sharp | 1.1 | takes the opposite side on purpose, polite |
| Narrator | deep | 0.9 | reads pages aloud, pauses at headings (for the browser extension) |

Observations from testing with 4 friends (7/27)
- everyone liked Rubber duck the most for coding. nobody expected that.
- Debater got annoying after 3 minutes. needs a "stop arguing" command.
- speaking rate matters more than voice choice for "does it feel natural".
''', tags=['juno', 'personas'], notes='old (2024) Juno note; predates the scope year')

note('Ideas', 'Juno browser extension — scope', '2024-11-03 21:10', '2025-01-12 19:45', ['project_juno'], '''
Goal: talk to the page you're reading. Juno reads the article, you ask questions out loud.

v0 scope (2 weekends)
1. content script grabs the readable text (readability-style extraction).
2. side panel with push-to-talk button.
3. send page text (chunked, top-k by embedding vs the question) + question to the backend.
4. answer spoken back with the selected persona.

Open questions
- PDFs in the browser viewer: can't get text easily. skip for v0.
- privacy: do NOT send the page unless the user presses the button. say so in the panel.
- Chrome Web Store review: microphone permission needs a justification paragraph.

1/12/25: v0 works on articles. long pages (> 15k tokens) are slow; summarize-then-answer helped. Shelving for now — research is eating everything. Maybe the extension is the right shape for something later.
''', tags=['juno', 'browser-extension'], notes='Juno extension scope note (2024 → Jan 2025); predates the scope year')

note('Ideas', 'Beat ideas — Oct', '2025-10-22 01:15', '2025-10-30 00:40', ['project_music_production'], '''
- 142 bpm, F# minor. flip a choir sample, pitch down 3 semitones, 808 glides between F# and C#.
- lo-fi thing at 84 bpm: dusty rhodes chords (Fmaj7 - Em7 - Dm7 - Cmaj7), swing the hats 58%.
- try Gross Beat "half speed" on the last bar before the drop instead of a riser.
- drums: layer a clap with a rim on the 2 and 4, short reverb only on the clap.
- the melody I hummed walking back from the lab: 4 notes, D - F - A - G, repeat with the last note up an octave. record it into a voice memo before I forget (did, 10/22).

Mixing note to self: stop mastering while producing. Fruity Limiter off until the arrangement is done.
''', tags=['beats', 'fl-studio', 'ideas'])

note('Ideas', 'Startup names — brainstorm', '2026-01-27 23:40', '2026-02-01 00:15', ['project_mathetic_company'], '''
With Hudson, for the notebook/learning-tools thing. Working name right now: **Papert Lab**.

Candidates
- Papert Lab — honest about the inspiration, sounds like a research group not a product.
- **Mathetic** — Papert's word for the art of learning (as opposed to didactics, the art of teaching). short, ownable? check.
- Mindstorm — taken by everyone.
- Turtle Labs — cute, LOGO reference, sounds like a kids' coding camp.
- Memex — Bush. a hundred projects already use it.
- Marginalia — nice but sounds like a reading app.
- Augment Co — too generic.

Checks for the top 2
[x] mathetic .com — taken (parked). .ai/.co? Hudson checking
[ ] Delaware entity name search (Mathetic, Inc. / Mathetic PBC)
[ ] trademark quick search (USPTO)
[x] say it out loud 10 times: Mathetic is fine. people may say "ma-THET-ic".

2/1: we both lean Mathetic for the company, keep "Papert Lab notebook" as the codename for the product idea for now.
''', tags=['startup', 'naming'], notes='naming brainstorm for the company (Papert Lab → Mathetic), late Jan 2026')

note('Ideas', 'What I want from a research notebook', '2026-01-29 00:30', '2026-01-30 23:55', ['project_engelbart'], '''
Brain dump after the Papert Lab call. The thing I actually want, as a researcher:

1. **Remember where a thought came from.** If I write "leakage is probably per-student", I want one click to the chat / paper / Slack message / run log where that came from.
2. Pull in what I already have: chats with Claude + ChatGPT, my Zotero PDFs, notes apps, repos. I'm not going to re-type anything.
3. Don't make me organize. Projects should emerge from the material (cluster by project, let me fix it).
4. Duplicates are the enemy: same paper from Zotero and Downloads should be ONE thing with two locations.
5. A canvas, not just a doc. Ideas next to their sources.
6. Works offline-ish, fast search.

Anti-goals
- not another second-brain template system.
- not a chatbot over my files that makes things up. citations or nothing.

Engelbart's "augmenting human intellect" is the frame. the notebook should make the trail visible.
''', tags=['product', 'notebook', 'ideas'], notes='pre-Engelbart product wishlist (late Jan 2026, Papert Lab period)')

note('Ideas', 'Sample chops to try', '2026-01-31 22:50', '2026-02-07 23:30', ['project_music_production'], '''
From the sample pack I bought in December + old records.

| sample | idea | bpm | status |
| strings loop #14 | chop into 8 slices, re-sequence, reverse slice 6 | 90 | done, sounds great |
| soul vocal "oh-oh" | formant shift down, use as a hook between 808 hits | 140 | tried, too obvious |
| piano one-shot C3 | play it chromatically in Fruity Slicer, detune 7 cents | 75 | todo |
| vinyl crackle | sidechain to the kick so it ducks | any | done |
| brass stab | gate it 1/16, filter sweep into the drop | 150 | todo |

Rule: no more than 20 min on a chop. If it's not working, next sample.
''', tags=['beats', 'samples', 'fl-studio'])

note('Ideas', 'Untitled Note', '2026-02-19 07:05', '2026-02-19 07:12', RUN, '''
8 x 400 @ 74-75
90s jog
wu 2mi cd 1.5

shins ok? -> yes

- bring bike to shop?? (still clicking)
- owen sat 7:30 huckleberry
''', tags=[], notes='HARD CASE: vague title — default "Untitled Note" holding an interval workout scribble + two errands')

note('Ideas', 'Beat ideas — late night', '2026-04-11 01:40', '2026-04-11 02:25', ['project_music_production'], '''
Post-deadline decompress beats. UIST is in, brain is mush, this is the only thing that sounds fun.

- 160 bpm half-time feel, sparse. kick only on 1 and the "and" of 3. big room reverb on the snare, gated.
- E minor, pluck lead with Sytrus preset, distortion 20%.
- arrangement: 8 bar intro (filtered), 16 hook, 16 verse, 8 break (drums out, only pad + vocal chop), 16 hook.
- the bounce is too long (3:40). cut verse 2.
- 808: tune to E, decay 600 ms, a little saturation so it shows up on laptop speakers.

Exported "aprilwip_03.wav". send to Owen? he has good ears for drums.
''', tags=['beats', 'fl-studio'])

note('Ideas', 'Drum bus chain (FL)', '2026-06-28 22:10', '2026-06-28 22:40', ['project_music_production'], '''
Finally writing down the chain so I stop rebuilding it.

Drum bus (mixer track 10, kick/snare/hats/perc routed in)
1. Fruity parametric EQ 2: HP at 30 Hz, small cut at 300 Hz (-2 dB, Q 1.2)
2. Compressor: ratio 4:1, attack 10 ms, release 80 ms, ~3 dB GR on the snare hits
3. Soft clipper: threshold -3 dB, post gain 0
4. Parallel send to track 11 (smash bus): ratio 10:1, attack 1 ms, blend at 20%
5. Fruity Limiter only on master, ceiling -1 dB

808 separate (track 12): sidechain from kick, Fruity Limiter in comp mode 3:1, saturation.

Template saved as "drum-bus-2026.fst".
''', tags=['mixing', 'fl-studio'])

note('Ideas', 'Beat ideas — SF', '2026-09-05 23:20', '2026-09-13 00:45', ['project_music_production'], '''
First beats on the new Mac. Headphones only (thin walls at the house).

{IMG:drums}
Pattern for "sf-bounce" (kick / snare / hat / perc, 16 steps). 96 bpm, the hats with 2 ghost 16ths.

- Key: D minor. chords Dm9 - Bbmaj7 - Gm7 - A7(b9).
- Fog-horn sample from Crissy Field (recorded on the phone 8/30). pitch it to D, low pass, use as the intro.
- Bass: Sytrus sub + a little FM grit on the top octave.
- Sam suggests a live guitar line. maybe.

9/13: arrangement done to 2:50. needs a better hook. leaving it for after the UIST talk.
''', tags=['beats', 'fl-studio', 'sf'], notes='beat ideas note with an attached drum-pattern PNG resource')

# =====================================================================================================================
# write
# =====================================================================================================================
REF_LOCAL = dt('2026-10-17 23:59')
for n in NOTES:
    assert dt(n['created']) <= dt(n['updated']) <= REF_LOCAL, n['title']
    rel = f"{ACCT_DIR}/{safe(n['notebook'])}/{safe(n['title'])}.enex"
    g.text(rel, enex([note_xml(n)], n['updated']), n['created'], n['updated'], account=ACCOUNT, project_ids=n['project_ids'],
           notes=n['notes'], source=f"Evernote note in notebook \"{n['notebook']}\" exported as single-note ENEX")

# whole-notebook export of Recipes (exported 2026-09-20; the chia note was edited after the export, so its copy here is older)
EXPORT_AT = '2026-09-20 10:15'
recipes = [n for n in NOTES if n['notebook'] == 'Recipes']
assert all(dt(n['created']) <= dt(EXPORT_AT) for n in recipes)
xs = []
for n in recipes:
    if n['export_body']: xs.append(note_xml(n, body=n['export_body'], updated=n['export_updated']))
    else:
        assert dt(n['updated']) <= dt(EXPORT_AT), n['title']
        xs.append(note_xml(n))
g.text(f'{ACCT_DIR}/Recipes (notebook export).enex', enex(xs, EXPORT_AT), EXPORT_AT, EXPORT_AT, account=ACCOUNT, project_ids=NONE,
       notes=f'HARD CASE: near-duplicate — whole-notebook export repeats every Recipes note ({len(xs)} notes; '
             '"Overnight chia pudding" is the older pre-2026-10-04 version)',
       source='Evernote notebook "Recipes" exported as one ENEX (File > Export notebook)')

g.finish()
