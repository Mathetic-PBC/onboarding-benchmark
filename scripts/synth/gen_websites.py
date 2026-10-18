"""Synthetic saved web pages (Chrome/Firefox "Save Page As… Webpage, HTML only") and a Firefox bookmarks export (Netscape
bookmark file). Every article is fictional and written for this benchmark. Deterministic; rebuilds synthetic/websites/."""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('websites')
ACCT = 'Firefox (personal Mac)'

PAGES = []  # (url, title, site, author, published, saved, pids, desc, body_html, notes)


def page(url, title, site, author, published, saved, pids, desc, paras, notes=''):
    PAGES.append((url, title, site, author, published, saved, pids, desc, paras, notes))


def render(url, title, site, author, published, desc, paras):
    body = []
    for p in paras:
        if p.startswith('## '): body.append(f'<h2>{html.escape(p[3:])}</h2>')
        elif p.startswith('- '): body.append('<ul>' + ''.join(f'<li>{html.escape(x[2:])}</li>' for x in p.split('\n')) + '</ul>')
        elif p.startswith('> '): body.append(f'<blockquote><p>{html.escape(p[2:])}</p></blockquote>')
        elif p.startswith('|'):
            rows = [r.strip('|').split('|') for r in p.split('\n')]
            body.append('<table><thead><tr>' + ''.join(f'<th>{html.escape(c.strip())}</th>' for c in rows[0]) + '</tr></thead><tbody>' +
                        ''.join('<tr>' + ''.join(f'<td>{html.escape(c.strip())}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table>')
        else: body.append(f'<p>{html.escape(p)}</p>')
    pub = dt(published)
    return f"""<!-- saved from url=({len(url):04d}){url} -->
<!DOCTYPE html>
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="{html.escape(author)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:site_name" content="{html.escape(site)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="article:published_time" content="{iso(pub)}">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="./{re.sub(r'[^A-Za-z0-9]+', '_', site)}_files/main.css">
<style>body{{font-family:Georgia,serif;max-width:720px;margin:0 auto;padding:24px;line-height:1.6;color:#222}}header nav a{{margin-right:14px}}
table{{border-collapse:collapse}}td,th{{border:1px solid #ccc;padding:4px 8px}}blockquote{{border-left:3px solid #999;margin-left:0;padding-left:14px;color:#555}}</style>
</head>
<body>
<header><a class="site-title" href="/">{html.escape(site)}</a>
<nav><a href="/">Home</a><a href="/archive">Archive</a><a href="/about">About</a><a href="/subscribe">Subscribe</a></nav></header>
<main><article>
<h1>{html.escape(title.split(' | ')[0].split(' – ')[0])}</h1>
<p class="byline">By {html.escape(author)} · <time datetime="{pub.date().isoformat()}">{pub.strftime('%B %-d, %Y')}</time></p>
{chr(10).join(body)}
</article></main>
<footer><p>© {pub.year} {html.escape(site)}. All rights reserved.</p></footer>
<script src="./{re.sub(r'[^A-Za-z0-9]+', '_', site)}_files/analytics.js" async></script>
</body></html>
"""

# =================================================================================================
page('https://www.longmemory.press/essays/memex-at-80', 'The Memex at 80: What Bush Actually Proposed – Long Memory', 'Long Memory',
     'Iris Calloway', '2025-07-18 09:00', '2026-02-11 21:12', ['project_augmenting_cognition_reading_group'],
     'Vannevar Bush\'s memex is remembered as a hypertext prophecy. Read closely, it is a proposal about trails.', [
    'Every few years someone credits Vannevar Bush with inventing the web, and every few years the credit lands on the wrong part of his essay. '
    'The microfilm desk, the dry photography, the head-mounted camera: these are the gadgets, and they are mostly wrong. The idea that survives '
    'is buried in a paragraph about a man researching the history of the Turkish bow.',
    '## Storage was never the point',
    'Bush assumed storage would become cheap. He was right, and it made almost no difference to his argument. His complaint was that the record '
    'of science had outgrown our ability to consult it, and that indexing by alphabet or class forced the mind into paths it does not naturally '
    'take. The fix he proposes is associative indexing: the ability to tie any item to any other and to keep that tie.',
    '## Trails as artifacts',
    'The important move is that a trail is itself a document. It can be named, copied, and handed to a colleague. Bush imagines a lawyer passing a '
    'trail of opinions to a client, and a historian building a trail through a century of sources. The trail outlives the session that produced it.',
    '> The inheritance from the master becomes, not only his additions to the world\'s record, but for his disciples the entire scaffolding by which they were erected.',
    '## What we built instead',
    'We built links, which are one-hop and owned by the author of the page, and search, which forgets everything between queries. Neither keeps '
    'the reader\'s path. Browser history comes closest, and nobody treats it as something worth sharing.',
    'If there is a modern memex, it will not be a better search box. It will be a tool that keeps the scaffolding: which source led to which thought, '
    'and in what order, for a reader who comes back months later.'])

page('https://www.longmemory.press/essays/what-the-demo-showed', 'What the 1968 Demo Actually Showed – Long Memory', 'Long Memory',
     'Iris Calloway', '2025-12-09 08:30', '2026-03-04 22:05', ['project_augmenting_cognition_reading_group'],
     'Engelbart\'s demo is remembered for the mouse. The point was a way of working.', [
    'The famous ninety minutes in San Francisco are usually summarized as a list of firsts: the mouse, windows, hypertext, shared screens, '
    'video conferencing. The list is accurate and misses what Engelbart was trying to show.',
    '## A system, not a gadget',
    'Engelbart\'s 1962 report describes the human as part of a system with language, artifacts, methodology and training. The demo was a '
    'demonstration of that whole system: a team that had trained itself to think with structured documents, live links, and views it could '
    'reshape on command. The mouse was a means.',
    '## The grocery list',
    'The most-quoted segment, in which he plans an errand run, is easy to laugh at. Watch it again: he collapses a list to its top level, '
    'reorders it by route, and expands only what matters. The lesson is that the same content seen through different views supports different thinking.',
    '## Bootstrapping',
    'His lab used its own tools to build its tools. The improvement compounded because the people improving the system were its heaviest users.',
    'What did not transfer to the personal computer era was the training. Products optimized for walk-up usability, and walk-up usability is '
    'exactly what a deep augmentation system gives up.'])

page('https://fieldnotes.researchware.dev/why-lab-notebooks-never-went-digital', 'Why the Lab Notebook Never Went Digital | Field Notes on Research Software',
     'Field Notes on Research Software', 'Tomasz Wierzbicki', '2026-06-30 07:00', '2026-08-26 23:40', ['project_engelbart'],
     'Electronic lab notebooks solved compliance, not thinking. A look at what researchers actually keep.', [
    'Electronic lab notebooks have existed for thirty years. Most researchers outside regulated labs still do not use one. They keep a mix of '
    'paper, a running document per project, chat threads, and a downloads folder that doubles as a library.',
    '## What ELNs optimized for',
    'ELNs were built for audit: timestamps, signatures, immutable entries. Those features matter for patents and clinical work. They do little '
    'for the person trying to remember why they changed the analysis plan in March.',
    '## Where thinking actually happens',
    'In interviews with 31 graduate students, we found that the decisive reasoning for a project was most often recorded in a conversation: '
    'a chat with a labmate, an email to an advisor, and increasingly a long exchange with an AI assistant. None of these were linked to the '
    'notebook, the paper draft, or the data.',
    '- 27 of 31 kept a running document per project',
    '- 22 of 31 said their most useful notes were in chat tools',
    '- 4 of 31 could find the origin of a key decision within five minutes',
    '## What a notebook would need',
    'A useful research notebook would import from the places where reasoning already happens, keep a link back to each source, and treat '
    'duplicates across tools as one item. It would not ask researchers to move their thinking into it.'])

page('https://fieldnotes.researchware.dev/provenance-for-personal-knowledge', 'Provenance for Personal Knowledge | Field Notes on Research Software',
     'Field Notes on Research Software', 'Tomasz Wierzbicki', '2026-09-29 07:00', '2026-10-14 22:48', ['project_engelbart'],
     'Data provenance has standards. Personal knowledge has none. A sketch of what it would take.', [
    'Data engineering has a mature vocabulary for provenance: entities, activities, agents, derivations. Personal knowledge tools have almost '
    'none of it. A note in most apps knows when it was edited and nothing about where its content came from.',
    '## Three questions a note should answer',
    '- Where did this come from? (a chat message, a page in a paper, a meeting)',
    '- What else came from the same place?',
    '- What did this lead to?',
    '## Import is where provenance is won or lost',
    'If a tool imports a paper from a reference manager and the same PDF from a downloads folder as two items, every later link is split in two. '
    'If an import silently drops a fraction of a user\'s conversations, the trail has holes the user cannot see. Getting import right is less '
    'glamorous than a graph view and matters more.',
    '## Duplicates versus versions',
    'A copy of a document with three lines changed is not a duplicate. It is a version, and the change is often the most informative thing about it. '
    'Tools should group versions and show the difference, never quietly keep one.',
    'The test of a provenance-aware notebook is simple: pick any sentence in your draft and ask where it came from. The tool should answer in one click.'])

page('https://cs1notebook.org/posts/nobody-raises-their-hand', 'Nobody Raises Their Hand Anymore – The CS1 Notebook', 'The CS1 Notebook',
     'Dana Whitfield', '2026-02-17 10:00', '2026-03-24 23:15', ['project_tutortrace', 'project_vizpi'],
     'AI assistants changed help-seeking in intro programming labs. What TAs see, and what they miss.', [
    'I have run intro programming labs for eleven years. This fall was the first time I walked a lab for an hour and nobody raised a hand.',
    '## The quiet lab',
    'Every student had an assistant in the editor. The room was calmer, questions to TAs dropped by more than half, and our end-of-lab '
    'completion rate barely moved. The students who used to raise their hands were getting answers elsewhere. The students who never raised '
    'their hands were still stuck, now with nobody noticing.',
    '## Stuck looks different now',
    'The old signal was a hand or a frustrated sigh. The new one is a student re-running the same failing code, or sending the assistant the same '
    'question five times with small changes. From across the room, that looks like work.',
    '## What I want from tooling',
    '- A view of who has been stuck on an error for more than a few minutes',
    '- Not the text of what students asked; that is theirs',
    '- A nudge for me to walk over, not an automated message to the student',
    'Several research groups are building exactly this kind of instructor view from editor telemetry. I hope they keep the human in the loop. '
    'The best intervention I have is still a TA kneeling next to a desk and asking what the student thinks the error means.'])

page('https://cs1notebook.org/posts/what-40-syllabi-say-about-ai', 'What 40 CS1 Syllabi Say About AI Assistants – The CS1 Notebook', 'The CS1 Notebook',
     'Dana Whitfield', '2025-10-08 10:00', '2025-11-05 21:30', ['project_vizpi'],
     'A quick survey of AI policies in introductory programming courses, Fall 2025.', [
    'I collected public syllabi from 40 introductory programming courses for Fall 2025 and coded their AI-assistant policies.',
    '|Policy|Courses|\n|Banned outright|6|\n|Allowed with disclosure|17|\n|Allowed, course-provided assistant only|11|\n|No policy stated|6|',
    '## Course-provided assistants are rising',
    'Eleven courses now ship their own assistant, usually a wrapped model with a system prompt that refuses to write full solutions. These '
    'courses also tend to collect usage logs, which raises questions about consent that only three syllabi addressed.',
    '## Disclosure is vague',
    'Most "allowed with disclosure" policies ask students to mention AI use in a comment, without saying what level of detail counts.',
    '## Labs versus homework',
    'Seven courses allow assistants in labs but not on homework. The logic is that labs have TAs present to notice over-reliance. Whether TAs '
    'can actually notice is an open question.'])

page('https://aerobicbase.run/articles/zone-2-without-the-hype', 'Zone 2 Without the Hype | Aerobic Base', 'Aerobic Base',
     'Marta Lindgren', '2025-09-02 06:00', '2025-12-28 16:20', ['project_endurance_training'],
     'What low-intensity training does, how to set the ceiling, and why it is boring on purpose.', [
    'Zone 2 has become a wellness buzzword, which is a shame, because the underlying idea is old, simple and useful: most of an endurance '
    'athlete\'s training should be easy enough that you could hold a conversation.',
    '## Setting the ceiling',
    'Lab tests define the zone by lactate. Most of us will never see a lab. Practical proxies work: a heart rate around 70-77% of a tested max, '
    'nasal breathing, or the talk test. Pick one and be consistent. The ceiling matters more than the floor.',
    '## Why it works',
    'Easy volume builds the plumbing: capillaries, mitochondria, and the ability to use fat at moderate speeds. Those adaptations take months '
    'and years, not weeks, which is why base phases feel unrewarding.',
    '## The two common mistakes',
    '- Turning easy days into medium days because easy feels too slow',
    '- Abandoning the plan after three weeks because nothing seems to change',
    '## Measuring progress',
    'Run the same flat 60-minute course at the same heart rate every month. If pace at a fixed heart rate improves, or heart-rate drift in the '
    'second half shrinks, the base is working. Expect both to move slowly.'])

page('https://aerobicbase.run/articles/half-marathon-pacing-for-base-builders', 'Half Marathon Pacing for Base Builders | Aerobic Base', 'Aerobic Base',
     'Marta Lindgren', '2026-08-19 06:00', '2026-10-10 21:35', ['project_endurance_training'],
     'If most of your training is easy, here is how to race 21.1 km without blowing up.', [
    'Runners who build mostly on easy volume often race the half too conservatively or, more often, go out at 10k effort because the first '
    'kilometers feel absurdly easy.',
    '## The plan',
    '- First 5 km: 3-5 seconds per kilometer slower than goal pace',
    '- 5-15 km: goal pace, fuel at roughly 35 and 70 minutes',
    '- 15 km to the finish: race whoever is near you',
    '## Choosing a goal pace',
    'Use a recent 10k: multiply the time by about 2.21 for a well-trained base runner. A 37:00 10k suggests roughly 1:21-1:22; a base-heavy '
    'runner without much threshold work should add a minute or two.',
    '## Hills',
    'Pace by effort on climbs. A short hill late in the race costs ten seconds whether you fight it or not; fighting it costs you the next kilometer too.',
    'A negative split is the best evidence that the plan was right.'])

page('https://www.citywalker.guide/san-francisco/neighborhoods-for-newcomers', 'San Francisco Neighborhoods for Newcomers (2026 Guide) – City Walker',
     'City Walker', 'Rosa Delacroix', '2026-05-12 12:00', '2026-07-08 22:30', ['project_none'],
     'A practical guide to choosing where to live in San Francisco when you are new and on a budget.', [
    'San Francisco is small enough to walk across in an afternoon and varied enough that the fog line can split a neighborhood in two.',
    '## Sunny and central',
    'The Mission and Noe Valley get the most sun. The Mission is lively, well-connected, and loud on weekends; rooms in shared flats run high.',
    '## Foggy and calm',
    'The Inner and Outer Sunset and the Richmond are quieter and cheaper, with Golden Gate Park and the ocean nearby. Commutes downtown are '
    '30-50 minutes by train or bus.',
    '## Downtown-adjacent',
    'SoMa and the Tenderloin edge are close to many offices and cheaper than they look on a map. Check the specific block.',
    '|Area|Typical room in shared flat|Notes|\n|Mission|$1,700-2,100|sun, noise|\n|Inner Sunset|$1,500-1,800|park, fog|\n|Outer Richmond|$1,300-1,600|long commute|\n|SoMa|$1,400-2,000|varies by block|',
    'Visit at night and on a weekday morning before signing anything.'])

page('https://www.citywalker.guide/san-francisco/sublet-red-flags', 'Seven Sublet Red Flags – City Walker', 'City Walker', 'Rosa Delacroix',
     '2026-04-02 12:00', '2026-07-10 20:55', ['project_none'], 'How to spot a fake or risky sublet listing before you send money.', [
    '- The rent is far below anything else in the neighborhood',
    '- The "owner" is abroad and will mail the keys after a deposit\n- No video tour, or a tour that is a pre-recorded clip',
    '- Payment requested by wire, gift card, or a payments app with no buyer protection',
    '- No written agreement, or one that does not name the leaseholder',
    '- Pressure: "three other people want it, decide today"',
    '- The listing photos appear on other sites under different addresses',
    'A legitimate subletter will show the place live, put the terms in writing, and wait a day while you think.'])

page('https://beatlab.academy/tutorials/sidechain-compression-fl-studio', 'Sidechain Compression in FL Studio, Step by Step – BeatLab Academy',
     'BeatLab Academy', 'Kenji Morales', '2026-03-03 15:00', '2026-07-20 00:45', ['project_music_production'],
     'Make pads and bass breathe with the kick using Fruity Limiter or Fruity Compressor routing.', [
    'Sidechaining ducks one sound when another plays. In beat-making it usually means the pad or bass dips each time the kick hits, which '
    'clears space in the low end and adds a pulse.',
    '## Routing',
    '- Put the kick and the pad on separate mixer tracks',
    '- On the kick\'s mixer track, right-click the arrow on the pad\'s track and choose "Sidechain to this track only"',
    '- Add Fruity Limiter to the pad track and switch it to COMP mode',
    '## Settings to start with',
    '- SIDECHAIN input: select the kick\'s track number',
    '- Threshold low enough that the gain reduction meter moves 4-8 dB on each kick',
    '- Attack near zero; release 80-150 ms, adjusted to the tempo',
    '## Hearing it',
    'Solo the pad with the kick muted: the ducking should still be audible, because the sidechain listens to the kick even when you cannot hear it. '
    'Too much release makes the pad sound like it is gasping. At slower tempos (80-90 bpm) a longer release sounds more natural.'])

page('https://beatlab.academy/tutorials/drum-swing-lofi', 'Getting Lo-fi Drum Swing Right – BeatLab Academy', 'BeatLab Academy', 'Kenji Morales',
     '2025-11-20 15:00', '2026-03-14 00:05', ['project_music_production'], 'Swing percentage, velocity, and why your hats sound robotic.', [
    'Lo-fi drums sound human because nothing lands exactly on the grid and nothing hits at the same velocity.',
    '## Swing',
    'Start at 50-58% swing on the hats only. Leave the kick on the grid. Swinging the snare more than a few ticks late gives the lazy feel.',
    '## Velocity',
    'Vary hat velocity in a pattern: strong on the beat, softer off-beat, with small random changes on top.',
    '## Texture',
    'Route drums through a bus with gentle saturation and a low-pass around 9-11 kHz. Add vinyl noise on its own track at a very low level.'])

page('https://uist.acm.org/2026/program/', 'Program – UIST 2026', 'UIST 2026', 'UIST 2026 Organizing Committee', '2026-09-01 12:00',
     '2026-09-28 22:40', ['project_tutortrace'], 'Program of the ACM Symposium on User Interface Software and Technology 2026, Detroit, MI.', [
    'UIST 2026 takes place October 5-8 in Detroit, Michigan. All times are Eastern. Paper sessions are 80 minutes with four or five talks of '
    '15 minutes plus 5 minutes of questions.',
    '## Monday, October 5',
    '|Time|Session|\n|09:00|Doctoral Symposium|\n|13:00|Workshops|\n|18:30|Welcome reception|',
    '## Tuesday, October 6',
    '|Time|Session|\n|09:00|Opening and keynote|\n|10:40|Papers: Haptics I|\n|10:40|Papers: Programming Tools|\n|14:00|Papers: Accessibility|\n|16:00|Demos and posters|',
    '## Wednesday, October 7',
    '|Time|Session|\n|09:00|Papers: Fabrication|\n|10:40|Papers: Learning & Tutoring (chair: Tomás Reyes)|\n|14:00|Papers: AI Agents|\n|19:00|Conference dinner|',
    '## Learning & Tutoring (Wed 10:40, Room B)',
    '- 10:40 TutorTrace: Reading the Quiet Lab from LLM-Assisted Programming Telemetry — David Barron, Minsun, Xiaohang, Yan Chen',
    '- 11:00 Worked-example scaffolds for visual programming in middle school',
    '- 11:20 Feedback timing in sketch-based physics tutors',
    '- 11:40 Peer explanation prompts in collaborative notebooks',
    '## Thursday, October 8',
    '|Time|Session|\n|09:00|Papers: Input Techniques|\n|10:40|Papers: Visualization|\n|13:00|Closing and awards|'],
     notes='fictional program page for the synthetic UIST 2026 (Detroit); the session and paper are synthetic')

page('https://uist.acm.org/2026/presenter-instructions/', 'Presenter Instructions – UIST 2026', 'UIST 2026', 'UIST 2026 Organizing Committee',
     '2026-08-25 12:00', '2026-09-22 21:50', ['project_tutortrace'], 'What paper presenters need to know: timing, AV, and session logistics.', [
    '- Paper talks are 15 minutes plus 5 minutes of Q&A. Session chairs will hold you to time.',
    '- Rooms have HDMI and USB-C inputs. Bring an adapter anyway. A clicker is provided.',
    '- Upload a PDF backup of your slides to the presenter portal by October 2.',
    '- Meet your session chair in the room 20 minutes before the session starts.',
    '- Optional remote AV checks are offered September 28 to October 2; your session chair will contact you.',
    'Presenters on approved remote status must pre-record. All in-person presenters must register by September 7.'])

page('https://mlpitfalls.dev/posts/grouped-splits-and-leakage', 'Your Split Is Leaking: Grouped Cross-Validation for Behavioral Data – ML Pitfalls',
     'ML Pitfalls', 'Arun Venkatesan', '2025-10-30 09:00', '2026-07-24 23:52', ['project_idetrace'],
     'When samples come from the same person, random splits overestimate performance.', [
    'If your dataset has many samples per person (windows of a session, frames of a video, days of a log), a random train/test split puts the '
    'same person on both sides. The model learns the person, not the behavior.',
    '## The symptom',
    'Suspiciously high scores that drop sharply on new users. Rare classes look easier than they should.',
    '## The fix',
    'Split by group. In scikit-learn: GroupKFold, StratifiedGroupKFold, or GroupShuffleSplit, with the person id as the group. Then assert that '
    'the intersection of train and test ids is empty.',
    '## Reporting',
    'If you already published or submitted with a leaky split, report both numbers and say which one readers should trust. Reviewers respond '
    'better to a visible correction than to a quiet one.',
    '|Split|Typical change in F1|\n|Random by sample|baseline|\n|Grouped by person|-0.03 to -0.15|'])

page('https://mlpitfalls.dev/posts/hdbscan-parameters-for-text', 'HDBSCAN Parameters for Text Embeddings – ML Pitfalls', 'ML Pitfalls',
     'Arun Venkatesan', '2025-08-14 09:00', '2026-01-19 22:20', ['project_dynamite'],
     'min_cluster_size, min_samples, and why you should reduce dimensions first.', [
    'HDBSCAN is a good default for clustering sentence embeddings because it does not need the number of clusters and it labels outliers as noise.',
    '## Reduce first',
    'Density estimates are unreliable in 384 or 768 dimensions. Reduce to 5-15 dimensions with UMAP (cosine metric) before clustering.',
    '## min_cluster_size',
    'The smallest group you would care about. For a few thousand forum posts, 10-25 is a reasonable range. Too small gives hundreds of micro-clusters.',
    '## min_samples',
    'Controls how conservative the clustering is. Higher values push more points into noise. Start at 5 and look at what lands in noise; short '
    'replies like "thanks" should.',
    '## Labeling clusters',
    'Language models write decent cluster labels from a sample of posts, but check every label by hand. Generic labels like "questions about the '
    'assignment" usually hide two or three real topics.'])

page('https://foundernotes.legal/pbc/annual-report-delaware', 'Delaware PBC Annual Reports, Explained – Founder Notes', 'Founder Notes',
     'Claire Ostend, Esq.', '2026-01-20 08:00', '2026-08-12 22:15', ['project_mathetic_company'],
     'What a Delaware public benefit corporation owes the state each year, and the extra benefit report.', [
    'A Delaware corporation files an annual report and pays franchise tax by March 1 each year. A public benefit corporation (PBC) has the '
    'same filing plus a benefit statement to stockholders at least every two years.',
    '## The annual report',
    'Filed online. Lists directors and the principal place of business. Late filing carries a penalty plus interest on unpaid franchise tax.',
    '## Franchise tax',
    'The default "authorized shares" method can produce an alarming number for startups with millions of authorized shares. The "assumed par '
    'value capital" method usually yields a much smaller amount; you must choose it when filing.',
    '## The benefit statement',
    'Describes the objectives the board set to promote the stated public benefit, the standards used to measure progress, and an assessment.',
    'Put March 1 in your calendar now. Founders miss it most often in their first year.'])

page('https://foundernotes.legal/financing/post-money-safe-primer', 'A Post-Money SAFE Primer for First-Time Founders – Founder Notes', 'Founder Notes',
     'Claire Ostend, Esq.', '2025-11-11 08:00', '2026-07-14 21:50', ['project_mathetic_company'],
     'How post-money SAFEs convert and how to model dilution in a simple cap table.', [
    'A SAFE is a right to future equity. With a post-money valuation cap, the investor\'s ownership at conversion is fixed: investment divided '
    'by the post-money cap.',
    '|Investment|Post-money cap|Ownership at conversion|\n|$100,000|$8,000,000|1.25%|\n|$50,000|$8,000,000|0.625%|\n|$750,000 total|$8,000,000|9.375%|',
    '## Modeling it',
    'Keep a cap table with separate tabs for founders, SAFEs, the option pool, and scenarios. Use formulas, not typed numbers, so a change to the '
    'cap flows through.',
    '## Things founders miss',
    '- SAFE dilution falls entirely on existing holders, including the option pool',
    '- A priced round may ask for the pool to be topped up before the new money, which dilutes founders again',
    '- Side letters (pro rata rights, information rights) matter more than they look'])

page('https://chessclub.blog/openings/london-b2-problem', 'The London System\'s b2 Problem – Chess Club Blog', 'Chess Club Blog', 'Viktor Hale',
     '2025-06-10 18:00', '2026-02-21 22:20', ['project_none'], 'Why ...c5 and ...Qb6 keep winning a pawn against club-level London players.', [
    'The London System is solid, which is why club players love it, and it has one recurring weakness: once the dark-squared bishop leaves '
    'c1 for f4, the b2 pawn has one fewer defender.',
    '## The pattern',
    'Black plays ...c5, ...Nc6 and ...Qb6. If White has spent a tempo on an early h4 or Ne5, b2 often simply falls.',
    '## The fixes',
    '- Play Qc1 or Qb3 in time',
    '- Play Nc3 only when Nb5 ideas are real',
    '- Skip the early h4 until you have castled',
    'Sometimes taking on b2 is a mistake: if White can trap the queen with Nb5 and a later Rb1, the pawn is poisoned.'])

page('https://www.statecraftquarterly.org/essays/export-controls-buy-time', 'Do Export Controls Buy Time? – Statecraft Quarterly', 'Statecraft Quarterly',
     'Elias Brandt', '2026-05-18 07:00', '2026-05-24 23:05', ['project_none'],
     'An essay on technology controls, chokepoints, and what they can and cannot achieve.', [
    'Technology export controls are sold as a way to buy time. The interesting question is what the time is for.',
    '## Chokepoints',
    'Controls work best where production is concentrated in a few firms and countries: advanced lithography, certain chemicals, specialized '
    'design software. They work worst where knowledge diffuses through people and open publication.',
    '## The substitution problem',
    'Every control creates an incentive to build a substitute. The question for policymakers is whether the time bought exceeds the time the '
    'substitute takes to mature. Historical cases suggest a range of five to fifteen years, with wide variance.',
    '## Allies',
    'Controls require coordination among the few countries that hold the chokepoints. Each of them pays a commercial cost, and the coalition is '
    'only as strong as its least committed member.',
    'Time is only useful if it is spent: on building capacity at home, on alliances, and on standards. Bought time that is not spent is a cost.'])

page('https://weeknightpan.com/recipes/sheet-pan-gochujang-chicken', 'Sheet-Pan Gochujang Chicken with Broccoli – Weeknight Pan', 'Weeknight Pan',
     'Hye-jin Park', '2025-03-04 10:00', '2026-01-14 18:40', ['project_none'], 'A 35-minute sheet-pan dinner that meal-preps well.', [
    '## Ingredients (4 servings)',
    '- 900 g boneless chicken thighs\n- 3 tbsp gochujang\n- 1 tbsp soy sauce\n- 1 tbsp honey\n- 1 tbsp sesame oil\n- 2 cloves garlic, grated\n- 2 heads broccoli\n- 1 tbsp neutral oil, salt',
    '## Method',
    'Heat the oven to 220°C (425°F). Mix gochujang, soy, honey, sesame oil and garlic. Toss the chicken in two-thirds of the sauce. Toss broccoli '
    'with oil and salt. Roast everything on one pan for 22-25 minutes, then brush the chicken with the remaining sauce and broil for 2 minutes.',
    'Keeps four days in the fridge. Serve with rice and something crunchy.'])

page('https://spokeandchain.co/howto/derailleur-hanger-alignment', 'Is Your Derailleur Hanger Bent? – Spoke & Chain', 'Spoke & Chain',
     'Lou Ferreira', '2024-09-15 09:00', '2026-05-10 19:10', ['project_none'], 'Symptoms, a quick check, and when to replace instead of straighten.', [
    'If your shifting went bad right after a crash or after the bike fell on its drive side, suspect the hanger before the derailleur.',
    '## Symptoms',
    '- Skipping in the middle cogs under load\n- Indexing that will not settle with the barrel adjuster\n- The derailleur cage looks tilted from behind',
    '## Quick check',
    'Stand behind the bike and sight down the cassette. The jockey wheels should sit in a vertical line under the cog.',
    '## Straighten or replace',
    'Aluminum hangers can be straightened once with an alignment tool. If it is badly bent or has been straightened before, replace it; '
    'they are cheap and designed to fail before your frame does.'])

page('https://quietpages.design/inspiration/minimal-researcher-homepages', 'Minimal Researcher Homepages We Like – Quiet Pages', 'Quiet Pages',
     'Noor Haddad', '2026-04-22 10:00', '2026-07-12 21:00', ['project_portfolio'],
     'A small gallery of academic homepages that do more with less.', [
    'The best researcher homepages answer three questions in the first screen: who are you, what do you work on, and where is your work.',
    '## Patterns that work',
    '- A single sentence under the name instead of a bio paragraph',
    '- Papers listed with venue and year, linked directly to PDFs',
    '- One short video or image per project, not a carousel',
    '- A serif display face for the name with a plain sans for body text',
    '## Patterns to avoid',
    '- News sections that stopped updating two years ago',
    '- Skill bars and tag clouds',
    '- Dark mode that is the only mode'])

page('https://agentcraft.notes/posts/writing-a-pre-compact-hook', 'Writing a Pre-Compact Hook That Keeps What Matters – Agentcraft Notes',
     'Agentcraft Notes', 'Sven Aldridge', '2026-07-30 11:00', '2026-08-16 22:30', ['project_claude_code_plugins'],
     'Coding agents summarize their context when it fills up. A hook can decide what survives.', [
    'Long coding sessions eventually fill the context window, and the agent compacts: it replaces the history with a summary. Summaries lose '
    'the details you need most, like the exact name of a failing test or an environment variable.',
    '## Hooks',
    'Most agent CLIs expose a hook that runs before compaction. A hook script receives the session state and can add instructions to the summary prompt.',
    '## What to keep verbatim',
    '- The current task in one line, written by the human\n- File paths touched in this session\n- Failing test names and the last error message\n- Environment variable names (never values)',
    '## Measuring it',
    'Run the same task several times with and without the hook and record context size before and after compaction and whether the task finished. '
    'Six runs will tell you if something is badly wrong; you need more to compare two good versions.'])

page('https://affectlab.review/overviews/frustration-detection-in-tutoring', 'Detecting Frustration in Tutoring Dialogues: A Short Overview – Affect Lab Review',
     'Affect Lab Review', 'Ingrid Solberg', '2025-12-01 09:00', '2026-02-03 22:10', ['project_ise6664_affective_computing'],
     'Text, timing and interaction signals of frustration in intelligent tutoring, and the ethical questions they raise.', [
    'Frustration is among the most studied affective states in intelligent tutoring because it predicts disengagement. Detecting it reliably '
    'from a chat transcript is harder than it looks.',
    '## Signals',
    '- Text: negative sentiment, explicit giving up, sarcasm, repeated short messages',
    '- Timing: long pauses after errors, rapid repeated submissions',
    '- Interaction: help requests that escalate in specificity',
    '## Annotation',
    'Agreement among annotators is moderate at best (kappa 0.5-0.7 in most studies). Distinguishing mild frustration from neutral terseness is the main source of disagreement.',
    '## Models',
    'Lexicon methods miss sarcasm. Fine-tuned classifiers do better but need labeled data from the same population. Zero-shot language models '
    'are competitive and over-predict mild frustration in terse messages.',
    '## Ethics',
    'Students rarely know their affect is being inferred. Using detection to change what a tutor does without disclosure is hard to justify; '
    'surfacing it to a human teacher is easier to defend.'])

page('https://fieldnotes.researchware.dev/interviewing-researchers-without-pitching', 'Interviewing Researchers Without Pitching | Field Notes on Research Software',
     'Field Notes on Research Software', 'Tomasz Wierzbicki', '2026-05-05 07:00', '2026-08-28 23:20', ['project_berkeley_research_chats'],
     'How to run discovery conversations with graduate students and postdocs when you are building a research tool.', [
    'If you build tools for researchers, you will be tempted to demo in every conversation. Don\'t, at least not until the last five minutes.',
    '## Ask about the last time',
    'General questions get general answers. Ask about the last time they lost an idea, the last time they returned to a project after a break, '
    'the last paper they could not find.',
    '## Watch the screen',
    'Ask them to show you where a project lives right now. The downloads folder will tell you more than any survey.',
    '## Pay people',
    'Graduate students are busy and underpaid. A small gift card is respectful and improves show-up rates.',
    '## Write it up the same day',
    'Patterns fade fast. A short synthesis after every three conversations keeps you honest.'])

# =================================================================================================
for url, title, site, author, published, saved, pids, desc, paras, notes in PAGES:
    fname = re.sub(r'[/:?"<>|*]', '_', title) + '.html'
    rel = f'saved-pages/{fname}'
    pub = dt(published)
    g.text(rel, render(url, title, site, author, published, desc, paras), saved, saved, account=ACCT, project_ids=pids,
           modeled_on='Chrome/Firefox "Save Page As… Webpage, HTML only" file (saved-from-url comment)', source=url,
           notes=notes or f'fictional article saved {saved[:10]}')

# =================================================================================================
# Firefox bookmarks export (Netscape bookmark file)


def ts(s):
    return int(epoch(s))


FOLDERS = [
    ('Bookmarks Toolbar', '2025-10-17 09:00', True, [
        ('Mathetic', '2026-08-11 10:00', [
            ('https://github.com/Mathetic-PBC', 'Mathetic-PBC · GitHub', '2026-08-24 10:12'),
            ('https://linear.app/mathetic/team/ENG/active', 'Active issues · Mathetic', '2026-08-24 10:15'),
            ('http://localhost:3000/canvas', 'engelbart — canvas (local)', '2026-09-08 22:40'),
            ('http://localhost:3000/connect', 'engelbart — connect (local)', '2026-10-14 16:05'),
            ('https://foundernotes.legal/financing/post-money-safe-primer', 'A Post-Money SAFE Primer for First-Time Founders', '2026-07-14 21:51'),
            ('https://foundernotes.legal/pbc/annual-report-delaware', 'Delaware PBC Annual Reports, Explained', '2026-08-12 22:16'),
            ('https://fieldnotes.researchware.dev/provenance-for-personal-knowledge', 'Provenance for Personal Knowledge', '2026-10-14 22:49'),
            ('https://fieldnotes.researchware.dev/why-lab-notebooks-never-went-digital', 'Why the Lab Notebook Never Went Digital', '2026-08-26 23:41'),
            ('https://fieldnotes.researchware.dev/interviewing-researchers-without-pitching', 'Interviewing Researchers Without Pitching', '2026-08-28 23:21'),
            ('https://docs.google.com/spreadsheets/d/1mAthEtIcCaPtAbLe/edit', 'Mathetic cap table - Google Sheets', '2026-07-14 22:12')]),
        ('Research', '2025-10-17 09:05', [
            ('https://scholar.google.com/', 'Google Scholar', '2025-10-17 09:06'),
            ('https://uist.acm.org/2026/', 'UIST 2026', '2026-01-20 14:02'),
            ('https://uist.acm.org/2026/program/', 'Program – UIST 2026', '2026-09-28 22:41'),
            ('https://uist.acm.org/2026/presenter-instructions/', 'Presenter Instructions – UIST 2026', '2026-09-22 21:51'),
            ('https://www.overleaf.com/project', 'Your Projects - Overleaf', '2025-10-17 09:07'),
            ('https://neurips.cc/Conferences/2026/CallForDatasetsBenchmarks', 'NeurIPS 2026 Datasets and Benchmarks Track', '2026-03-02 21:30'),
            ('https://openreview.net/group?id=NeurIPS.cc/2026/Datasets_and_Benchmarks', 'NeurIPS 2026 D&B | OpenReview', '2026-05-01 22:10'),
            ('https://cs1notebook.org/posts/nobody-raises-their-hand', 'Nobody Raises Their Hand Anymore', '2026-03-24 23:16'),
            ('https://mlpitfalls.dev/posts/grouped-splits-and-leakage', 'Your Split Is Leaking', '2026-07-24 23:53'),
            ('https://mlpitfalls.dev/posts/hdbscan-parameters-for-text', 'HDBSCAN Parameters for Text Embeddings', '2026-01-19 22:21'),
            ('https://hdbscan.readthedocs.io/en/latest/parameter_selection.html', 'Parameter Selection for HDBSCAN', '2026-01-20 21:05'),
            ('https://scikit-learn.org/stable/modules/cross_validation.html', 'Cross-validation — scikit-learn', '2026-07-24 23:20'),
            ('https://affectlab.review/overviews/frustration-detection-in-tutoring', 'Detecting Frustration in Tutoring Dialogues', '2026-02-03 22:11')]),
        ('Reading group', '2026-02-10 20:00', [
            ('https://www.longmemory.press/essays/memex-at-80', 'The Memex at 80', '2026-02-11 21:13'),
            ('https://www.longmemory.press/essays/what-the-demo-showed', 'What the 1968 Demo Actually Showed', '2026-03-04 22:06'),
            ('https://www.dougengelbart.org/content/view/138', 'Augmenting Human Intellect: A Conceptual Framework', '2026-03-03 21:40')]),
        ('Running', '2025-10-17 09:10', [
            ('https://www.strava.com/dashboard', 'Dashboard | Strava', '2025-10-17 09:11'),
            ('https://connect.garmin.com/modern/sleep', 'Sleep | Garmin Connect', '2026-04-01 07:30'),
            ('https://aerobicbase.run/articles/zone-2-without-the-hype', 'Zone 2 Without the Hype', '2025-12-28 16:21'),
            ('https://aerobicbase.run/articles/half-marathon-pacing-for-base-builders', 'Half Marathon Pacing for Base Builders', '2026-10-10 21:36'),
            ('https://docs.google.com/spreadsheets/d/1tRaInInGlOg2026/edit', 'Training log 2026 - Google Sheets', '2026-01-04 19:32')]),
        ('Music', '2025-11-20 23:00', [
            ('https://beatlab.academy/tutorials/sidechain-compression-fl-studio', 'Sidechain Compression in FL Studio, Step by Step', '2026-07-20 00:46'),
            ('https://beatlab.academy/tutorials/drum-swing-lofi', 'Getting Lo-fi Drum Swing Right', '2026-03-14 00:06'),
            ('https://loopbank.example.com/packs/tape-drums', 'Tape Drums — Loopbank', '2026-08-30 22:05')]),
    ]),
    ('Personal', '2025-10-17 09:15', False, [
        ('SF move', '2026-07-08 22:00', [
            ('https://www.citywalker.guide/san-francisco/neighborhoods-for-newcomers', 'San Francisco Neighborhoods for Newcomers (2026 Guide)', '2026-07-08 22:31'),
            ('https://www.citywalker.guide/san-francisco/sublet-red-flags', 'Seven Sublet Red Flags', '2026-07-10 20:56'),
            ('https://www.sfmta.com/getting-around/transit/fares-passes', 'Fares & Passes | SFMTA', '2026-08-09 13:10'),
            ('https://www.dmv.ca.gov/portal/vehicle-registration/new-registration/', 'Register a vehicle new to California', '2026-08-17 21:05')]),
        ('Cooking', '2025-11-09 21:00', [
            ('https://weeknightpan.com/recipes/sheet-pan-gochujang-chicken', 'Sheet-Pan Gochujang Chicken with Broccoli', '2026-01-14 18:41'),
            ('https://weeknightpan.com/recipes/turkey-chili-meal-prep', 'Turkey Chili for Meal Prep', '2026-01-18 16:50')]),
        ('Chess', '2025-10-27 22:00', [
            ('https://lichess.org/training', 'Puzzles • lichess.org', '2025-10-27 22:01'),
            ('https://chessclub.blog/openings/london-b2-problem', 'The London System\'s b2 Problem', '2026-02-21 22:21')]),
        ('Reading', '2025-11-30 23:00', [
            ('https://www.statecraftquarterly.org/essays/export-controls-buy-time', 'Do Export Controls Buy Time?', '2026-05-24 23:06'),
            ('https://www.statecraftquarterly.org/essays/middle-powers-hedging', 'Middle Powers and the Art of Hedging', '2026-03-29 23:40')]),
        ('', None, [
            ('https://spokeandchain.co/howto/derailleur-hanger-alignment', 'Is Your Derailleur Hanger Bent?', '2026-05-10 19:11'),
            ('https://quietpages.design/inspiration/minimal-researcher-homepages', 'Minimal Researcher Homepages We Like', '2026-07-12 21:01'),
            ('https://agentcraft.notes/posts/writing-a-pre-compact-hook', 'Writing a Pre-Compact Hook That Keeps What Matters', '2026-08-16 22:31'),
            ('https://www.vt.edu/', 'Virginia Tech', '2025-10-17 09:16'),
            ('https://canvas.vt.edu/courses', 'Courses | Canvas', '2025-10-17 09:17'),
            ('https://parking.vt.edu/citations/appeal', 'Citation Appeals | Parking Services', '2026-01-28 10:15'),
            ('https://www.irs.gov/filing', 'File your taxes | IRS', '2026-03-08 20:10'),
            ('https://tax.virginia.gov/individual-income-tax-filing', 'Individual Income Tax Filing | Virginia Tax', '2026-03-08 20:12'),
            ('https://claude.ai/new', 'Claude', '2025-10-17 09:18'),
            ('https://chatgpt.com/', 'ChatGPT', '2025-10-17 09:18'),
            ('https://arxiv.org/list/cs.HC/recent', 'Human-Computer Interaction (recent) - arXiv', '2025-11-03 22:30'),
            ('http://localhost:5173/ta-dashboard', 'VizPI — TA dashboard (local)', '2025-11-10 15:20'),
            ('https://graduateschool.vt.edu/academics/forms.html', 'Forms | Graduate School | Virginia Tech', '2026-07-27 21:25'),
            ('https://www.chess.com/play/online', 'Play Chess Online', '2025-12-27 15:30'),
            ('https://www.surplus-house.example/residents', 'Residents — Surplus', '2026-08-11 09:40'),
            ('https://www.flyway.example/trips/QK7P2D', 'Trip QK7P2D — SFO to DTW', '2026-09-18 21:02')]),
    ]),
]
out = ['<!DOCTYPE NETSCAPE-Bookmark-file-1>', '<!-- This is an automatically generated file.', '     It will be read and overwritten.',
       '     DO NOT EDIT! -->', '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
       '<meta http-equiv="Content-Security-Policy"', '      content="default-src \'self\'; script-src \'none\'; img-src data: *; object-src \'none\'"></meta>',
       '<TITLE>Bookmarks</TITLE>', '<H1>Bookmarks Menu</H1>', '', '<DL><p>']
n_links = 0
newest = '2025-10-17 09:00'
for top, created, toolbar, subs in FOLDERS:
    links_all = [l for _, _, ls in subs for l in ls]
    lm = max(l[2] for l in links_all)
    attr = ' PERSONAL_TOOLBAR_FOLDER="true"' if toolbar else ''
    out.append(f'    <DT><H3 ADD_DATE="{ts(created)}" LAST_MODIFIED="{ts(lm)}"{attr}>{html.escape(top)}</H3>')
    out.append('    <DL><p>')
    for name, fcreated, links in subs:
        ind = '        '
        if name:
            out.append(f'{ind}<DT><H3 ADD_DATE="{ts(fcreated)}" LAST_MODIFIED="{ts(max(l[2] for l in links))}">{html.escape(name)}</H3>')
            out.append(f'{ind}<DL><p>'); ind += '    '
        for url, title, added in links:
            out.append(f'{ind}<DT><A HREF="{html.escape(url)}" ADD_DATE="{ts(added)}" LAST_MODIFIED="{ts(added)}">{html.escape(title)}</A>')
            n_links += 1; newest = max(newest, added)
        if name: out.append(f'{ind[:-4]}</DL><p>')
    out.append('    </DL><p>')
out.append('</DL>')
g.text('bookmarks/firefox-bookmarks.html', '\n'.join(out) + '\n', '2026-10-17 10:20', '2026-10-17 10:20', account=ACCT,
       project_ids=['project_engelbart', 'project_mathetic_company', 'project_tutortrace', 'project_idetrace', 'project_dynamite',
                    'project_augmenting_cognition_reading_group', 'project_endurance_training', 'project_music_production',
                    'project_ise6664_affective_computing', 'project_berkeley_research_chats', 'project_claude_code_plugins',
                    'project_portfolio', 'project_vt_phd_admin', 'project_none'],
       modeled_on='authentic/websites/bookmarks/chrome-bookmarks.html (Netscape bookmark file shape; Firefox export header)',
       notes=f'HARD CASE: personal clutter mixed with work — Firefox bookmarks export, {n_links} links in project and personal folders')
print('bookmarks:', n_links, 'newest', newest)
g.finish()
