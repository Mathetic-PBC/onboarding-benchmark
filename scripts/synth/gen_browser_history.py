"""Synthetic second/third browsers (PERSON.md): a Firefox profile places.sqlite (moz_places / moz_historyvisits / moz_origins /
moz_bookmarks, PRTime microseconds) used as the personal browser all year, and a Brave Default/History (Chrome schema, WebKit
microseconds since 1601) used from the new Mac (2026-08-04) for testing the landing page and the Engelbart app. Plus a derived
visits.csv per browser, like authentic/browser-history. Deterministic; rebuilds synthetic/browser-history/."""
import base64, csv, hashlib, io, os, random, sqlite3, sys
from urllib.parse import quote_plus, urlsplit
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *

g = Gen('browser-history')
R = random.Random('browser-history')

# ---------------------------------------------------------------------------------------------------------
# topic windows (PERSON.md §3-§5)
W = {
    'vizpi': ('2025-10-17', '2025-11-25'), 'cs3604': ('2025-10-17', '2025-12-16'), 'tacode': ('2025-11-15', '2025-11-21'),
    'ethic': ('2025-11-10', '2025-11-15'), 'sophia': ('2025-11-17', '2025-11-21'), 'dynamite': ('2026-01-12', '2026-02-14'),
    'ise': ('2026-01-12', '2026-05-08'), 'papert': ('2026-01-26', '2026-02-06'), 'augcog': ('2026-02-09', '2026-03-10'),
    'uist_crunch': ('2026-03-16', '2026-03-31 23:00'), 'uist_rebut': ('2026-06-11', '2026-06-18 20:00'), 'uist_cr': ('2026-08-01', '2026-08-14'),
    'uist_talk': ('2026-09-20', '2026-10-08'), 'ide_sub': ('2026-04-20', '2026-05-06 20:00'), 'ide_reb': ('2026-07-20', '2026-07-30'),
    'admin_leave': ('2026-06-20', '2026-08-06'), 'admin_travel': ('2026-09-01', '2026-09-25'), 'mathetic': ('2026-07-10', '2026-10-17'),
    'engelbart': ('2026-08-20', '2026-10-17'), 'berkeley': ('2026-08-24', '2026-09-20'), 'plugins': ('2026-08-10', '2026-08-31'),
    'portfolio': ('2026-07-10', '2026-07-22'), 'year': ('2025-10-17', '2026-10-17'), 'sfmove': ('2026-07-01', '2026-08-20'),
    'taxes': ('2026-02-01', '2026-04-05'), 'wedding': ('2026-05-05', '2026-06-05'), 'bike': ('2026-05-09', '2026-05-12'),
    'parking': ('2026-01-27', '2026-01-29'), 'newmac': ('2026-08-04', '2026-08-06'), 'race': ('2026-09-20', '2026-10-16'),
    'post_move': ('2026-08-08', '2026-10-17'), 'pre_move': ('2025-10-17', '2026-08-07'),
}
P = {'vizpi': ['project_vizpi'], 'cs3604': ['project_cs3604_gta'], 'tacode': ['project_tacode'], 'ethic': ['project_ethicconvo'],
     'sophia': ['project_sophia'], 'dynamite': ['project_dynamite'], 'ise': ['project_ise6664_affective_computing'],
     'papert': ['project_engelbart'], 'augcog': ['project_augmenting_cognition_reading_group'], 'uist_crunch': ['project_tutortrace'],
     'uist_rebut': ['project_tutortrace'], 'uist_cr': ['project_tutortrace'], 'uist_talk': ['project_tutortrace'], 'ide_sub': ['project_idetrace'],
     'ide_reb': ['project_idetrace'], 'admin_leave': ['project_vt_phd_admin'], 'admin_travel': ['project_vt_phd_admin'],
     'mathetic': ['project_mathetic_company'], 'engelbart': ['project_engelbart'], 'berkeley': ['project_berkeley_research_chats'],
     'plugins': ['project_claude_code_plugins'], 'portfolio': ['project_portfolio'], 'run': ['project_endurance_training'],
     'race': ['project_endurance_training'], 'music': ['project_music_production']}

# ---------------------------------------------------------------------------------------------------------
# Firefox place catalog: (url, title, window, n_visits, typed, topic)
PLACES = []


def add(url, title, win, n, topic, typed=0, via=None, hidden=0):
    PLACES.append(dict(url=url, title=title, win=W[win] if isinstance(win, str) else win, n=n, topic=topic, typed=typed, via=via, hidden=hidden))


def search(q, win, topic, n=1):
    url = f'https://www.google.com/search?client=firefox-b-1-d&q={quote_plus(q)}'
    add(url, f'{q} - Google Search', win, n, topic)
    return url


SEARCHES = {
    ('vizpi', 'vizpi'): ['websocket reconnect lose messages after token refresh', 'socket.io reconnect resubscribe room auth',
                         'buffer events client side until ack websocket', 'react virtualized timeline component', 'cohen kappa three raters',
                         'fleiss kappa python', 'irb amendment telemetry classroom consent opt out', 'mcbryde 116 wifi'],
    ('cs3604', 'cs3604'): ['express rest api status codes 422 vs 400', 'jest supertest example express', 'react testing library async fetch mock',
                           'axe accessibility checker chrome', 'canvas speedgrader rubric import csv', 'late day policy software engineering course',
                           'canvas status outage november'],
    ('tacode', 'tacode'): ['supabase row level security update only own rows', 'postgres select for update skip locked queue',
                           'canvas api cross listed sections roster'],
    ('ethic', 'ethic'): ['value sensitive design conversational agents', 'ethics case discussion llm classroom'],
    ('sophia', 'sophia'): ['socratic tutor for educators prompt design'],
    ('dynamite', 'dynamite'): ['hdbscan min_cluster_size text embeddings', 'umap cosine n_components clustering', 'sentence transformers all-MiniLM-L6-v2 dimension',
                               'hdbscan too much noise', 'llm generate cluster labels from samples', 'cursor agent rewriting whole file',
                               'bertopic vs hdbscan directly'],
    ('ise', 'ise'): ['frustration detection tutoring dialogue', 'affect annotation codebook kappa', 'survival analysis time to event python lifelines',
                     'lifelines coxph hazard ratio interpretation', 'nrc emotion lexicon', 'zero shot classification llm emotion',
                     'ise 6664 virginia tech affective'],
    ('papert', 'papert'): ['seymour papert constructionism', 'papert mindstorms quotes', 'export claude conversations json', 'chatgpt export format conversations.json'],
    ('augcog', 'augcog'): ['as we may think full text', 'augmenting human intellect conceptual framework 1962', 'licklider man computer symbiosis pdf',
                           'mother of all demos grocery list', 'bootstrapping engelbart'],
    ('uist_crunch', 'uist_crunch'): ['uist 2026 deadline aoe', 'acm primary article template latex anonymous', 'latex figure placement here definitely',
                                     'overleaf compile timeout large figures', 'colorblind safe palette matplotlib', 'aoe time now',
                                     'related work help seeking programming llm', 'ostrowski productive struggle silent stalling'],
    ('uist_rebut', 'uist_rebut'): ['uist rebuttal character limit', 'how to write a rebuttal hci', 'fleiss kappa interpretation 0.71'],
    ('uist_cr', 'uist_cr'): ['acm taps pdf font not embedded', 'acm rights form uist', 'burn captions into video ffmpeg'],
    ('uist_talk', 'uist_talk'): ['uist 2026 detroit venue', 'conference talk 15 minutes how many slides', 'keynote export pdf with presenter notes',
                                 'detroit riverwalk running route', 'dtw airport to downtown detroit'],
    ('ide_sub', 'ide_sub'): ['neurips datasets and benchmarks 2026 deadline', 'datasheets for datasets template', 'zenodo community dataset doi versioning',
                             'croissant metadata neurips'],
    ('ide_reb', 'ide_reb'): ['groupkfold vs stratifiedgroupkfold', 'data leakage same subject train test', 'openreview rebuttal markdown math'],
    ('admin_leave', 'admin_leave'): ['virginia tech graduate leave of absence', 'vt graduate school leave form', 'student health insurance after gra ends'],
    ('admin_travel', 'admin_travel'): ['vt graduate student travel fund', 'per diem detroit 2026'],
    ('mathetic', 'mathetic'): ['post money safe calculator', 'delaware pbc annual report franchise tax assumed par', 'option pool size pre seed',
                               'incubator san francisco founders house', 'pre seed deck 12 slides', 'who pays research software grad students'],
    ('engelbart', 'engelbart'): ['dedupe pdfs by doi', 'extract doi from pdf python', 'claude export pagination 1000', 'electron app canvas not re-rendering after state update',
                                 'react flow large graph performance', 'notion api export pages', 'granola export notes', 'w3c prov data model'],
    ('berkeley', 'berkeley'): ['berkeley graduate school of education phd', 'doe library cafe hours', 'user interview script researchers', 'amazon gift card email bulk'],
    ('plugins', 'plugins'): ['claude code hooks precompact', 'claude code plugin marketplace json', 'context compaction summary loses details'],
    ('portfolio', 'portfolio'): ['academic homepage minimal', 'serif display font free', 'static site github pages custom domain'],
    ('run', 'year'): ['zone 2 heart rate calculation', 'heart rate drift test', 'garmin hr strap battery', 'half marathon pacing negative split',
                      'blacksburg trail running routes', 'golden gate park running loop distance', 'treadmill incline equivalent', 'turkey trot blacksburg 2025',
                      'bay area half marathon 2026', 'how long recovery after half marathon'],
    ('music', 'year'): ['fl studio sidechain fruity limiter', 'lofi drum swing percentage', 'am9 chord voicing piano', 'fl studio export stems',
                        'vinyl crackle free sample'],
    ('none', 'year'): ['london system qb6 b2', 'caro kann advance bf5', 'rook endgame lucena', 'thucydides book 1 truest cause',
                       'export controls semiconductors 2026', 'middle powers hedging strategy', 'gochujang chicken sheet pan',
                       'turkey chili meal prep', 'overnight oats ratio', 'best cheap noise cancelling headphones', 'weather blacksburg',
                       'weather san francisco', 'usps change of address', 'macbook pro setup checklist developer'],
    ('none', 'sfmove'): ['inner sunset sublet', 'mission district room for rent', 'sf sublet scam', 'clipper card', 'car shipping cost virginia to california',
                         'renters insurance san francisco'],
    ('none', 'taxes'): ['1098-t scholarship box 5 greater than box 1', 'virginia state tax filing free', 'irs refund status'],
    ('none', 'wedding'): ['flights iad to dublin', 'dublin guesthouse', 'wedding gift etiquette registry'],
    ('none', 'bike'): ['derailleur hanger bent symptoms', 'bike shop blacksburg'],
    ('none', 'parking'): ['vt parking citation appeal'],
    ('none', 'newmac'): ['brew bundle brewfile', 'fl studio license transfer new computer'],
}
SEARCHES.update({
    ('vizpi', 'vizpi'): SEARCHES[('vizpi', 'vizpi')] + ['react window list replay scrubber', 'websocket heartbeat interval best practice', 'how to estimate lost telemetry events'],
    ('cs3604', 'cs3604'): SEARCHES[('cs3604', 'cs3604')] + ['regrade request response template ta', 'peer evaluation team project outlier', 'canvas grade posting policy manual'],
    ('dynamite', 'dynamite'): SEARCHES[('dynamite', 'dynamite')] + ['hdbscan seed stability', 'cluster map visualization plotly'],
    ('ise', 'ise'): SEARCHES[('ise', 'ise')] + ['sarcasm detection programming help messages', 'ethics of affect detection education'],
    ('uist_crunch', 'uist_crunch'): SEARCHES[('uist_crunch', 'uist_crunch')] + ['think aloud study instructors dashboard', 'median time to find wilcoxon', 'latex table too wide resizebox'],
    ('uist_talk', 'uist_talk'): SEARCHES[('uist_talk', 'uist_talk')] + ['presenter view keynote second display', 'how to answer hostile question conference'],
    ('ide_sub', 'ide_sub'): SEARCHES[('ide_sub', 'ide_sub')] + ['neurips checklist datasets', 'license for research dataset cc by nc'],
    ('mathetic', 'mathetic'): SEARCHES[('mathetic', 'mathetic')] + ['angel investor first call questions', 'pbc vs c corp startup', 'retention metric for note taking app'],
    ('engelbart', 'engelbart'): SEARCHES[('engelbart', 'engelbart')] + ['zotero storage folder structure', 'content hash docx text extraction', 'onboarding connect screen examples'],
    ('none', 'year'): SEARCHES[('none', 'year')] + ['grand strategy reading list', 'how to stop doomscrolling', 'cheap running shoes rotation', 'sparkling water maker worth it',
                                                     'how to clean a macbook keyboard', 'lichess vs chess.com rating', 'peloponnesian war translation which'],
    ('none', 'sfmove'): SEARCHES[('none', 'sfmove')] + ['soma safety at night', 'sf fog august', 'farmers market sf saturday'],
    ('run', 'year'): SEARCHES[('run', 'year')] + ['easy run too slow', 'strides how many', 'elliptical vs running aerobic'],
})
search_url = {}
for (topic, win), qs in SEARCHES.items():
    for q in qs:
        search_url[q] = search(q, win, topic, n=1 + (R.random() < 0.15))

# fictional articles (also saved as pages in synthetic/websites) and other articles
ART = [
    ('https://www.longmemory.press/essays/memex-at-80', 'The Memex at 80: What Bush Actually Proposed – Long Memory', 'augcog', 'augcog', 'as we may think full text'),
    ('https://www.longmemory.press/essays/what-the-demo-showed', 'What the 1968 Demo Actually Showed – Long Memory', 'augcog', 'augcog', 'mother of all demos grocery list'),
    ('https://fieldnotes.researchware.dev/why-lab-notebooks-never-went-digital', 'Why the Lab Notebook Never Went Digital | Field Notes on Research Software', 'engelbart', 'engelbart', None),
    ('https://fieldnotes.researchware.dev/provenance-for-personal-knowledge', 'Provenance for Personal Knowledge | Field Notes on Research Software', 'engelbart', 'engelbart', 'w3c prov data model'),
    ('https://fieldnotes.researchware.dev/interviewing-researchers-without-pitching', 'Interviewing Researchers Without Pitching | Field Notes on Research Software', 'berkeley', 'berkeley', 'user interview script researchers'),
    ('https://cs1notebook.org/posts/nobody-raises-their-hand', 'Nobody Raises Their Hand Anymore – The CS1 Notebook', 'uist_crunch', 'uist_crunch', 'related work help seeking programming llm'),
    ('https://cs1notebook.org/posts/what-40-syllabi-say-about-ai', 'What 40 CS1 Syllabi Say About AI Assistants – The CS1 Notebook', 'vizpi', 'vizpi', None),
    ('https://aerobicbase.run/articles/zone-2-without-the-hype', 'Zone 2 Without the Hype | Aerobic Base', 'year', 'run', 'zone 2 heart rate calculation'),
    ('https://aerobicbase.run/articles/half-marathon-pacing-for-base-builders', 'Half Marathon Pacing for Base Builders | Aerobic Base', 'race', 'run', 'half marathon pacing negative split'),
    ('https://www.citywalker.guide/san-francisco/neighborhoods-for-newcomers', 'San Francisco Neighborhoods for Newcomers (2026 Guide) – City Walker', 'sfmove', 'none', 'inner sunset sublet'),
    ('https://www.citywalker.guide/san-francisco/sublet-red-flags', 'Seven Sublet Red Flags – City Walker', 'sfmove', 'none', 'sf sublet scam'),
    ('https://beatlab.academy/tutorials/sidechain-compression-fl-studio', 'Sidechain Compression in FL Studio, Step by Step – BeatLab Academy', 'year', 'music', 'fl studio sidechain fruity limiter'),
    ('https://beatlab.academy/tutorials/drum-swing-lofi', 'Getting Lo-fi Drum Swing Right – BeatLab Academy', 'year', 'music', 'lofi drum swing percentage'),
    ('https://uist.acm.org/2026/program/', 'Program – UIST 2026', 'uist_talk', 'uist_talk', None),
    ('https://uist.acm.org/2026/presenter-instructions/', 'Presenter Instructions – UIST 2026', 'uist_talk', 'uist_talk', None),
    ('https://mlpitfalls.dev/posts/grouped-splits-and-leakage', 'Your Split Is Leaking: Grouped Cross-Validation for Behavioral Data – ML Pitfalls', 'ide_reb', 'ide_reb', 'data leakage same subject train test'),
    ('https://mlpitfalls.dev/posts/hdbscan-parameters-for-text', 'HDBSCAN Parameters for Text Embeddings – ML Pitfalls', 'dynamite', 'dynamite', 'hdbscan min_cluster_size text embeddings'),
    ('https://foundernotes.legal/pbc/annual-report-delaware', 'Delaware PBC Annual Reports, Explained – Founder Notes', 'mathetic', 'mathetic', 'delaware pbc annual report franchise tax assumed par'),
    ('https://foundernotes.legal/financing/post-money-safe-primer', 'A Post-Money SAFE Primer for First-Time Founders – Founder Notes', 'mathetic', 'mathetic', 'post money safe calculator'),
    ('https://chessclub.blog/openings/london-b2-problem', 'The London System\'s b2 Problem – Chess Club Blog', 'year', 'none', 'london system qb6 b2'),
    ('https://www.statecraftquarterly.org/essays/export-controls-buy-time', 'Do Export Controls Buy Time? – Statecraft Quarterly', 'year', 'none', 'export controls semiconductors 2026'),
    ('https://www.statecraftquarterly.org/essays/middle-powers-hedging', 'Middle Powers and the Art of Hedging – Statecraft Quarterly', 'year', 'none', 'middle powers hedging strategy'),
    ('https://weeknightpan.com/recipes/sheet-pan-gochujang-chicken', 'Sheet-Pan Gochujang Chicken with Broccoli – Weeknight Pan', 'year', 'none', 'gochujang chicken sheet pan'),
    ('https://weeknightpan.com/recipes/turkey-chili-meal-prep', 'Turkey Chili for Meal Prep – Weeknight Pan', 'year', 'none', 'turkey chili meal prep'),
    ('https://spokeandchain.co/howto/derailleur-hanger-alignment', 'Is Your Derailleur Hanger Bent? – Spoke & Chain', 'bike', 'none', 'derailleur hanger bent symptoms'),
    ('https://quietpages.design/inspiration/minimal-researcher-homepages', 'Minimal Researcher Homepages We Like – Quiet Pages', 'portfolio', 'portfolio', 'academic homepage minimal'),
    ('https://agentcraft.notes/posts/writing-a-pre-compact-hook', 'Writing a Pre-Compact Hook That Keeps What Matters – Agentcraft Notes', 'plugins', 'plugins', 'claude code hooks precompact'),
    ('https://affectlab.review/overviews/frustration-detection-in-tutoring', 'Detecting Frustration in Tutoring Dialogues: A Short Overview – Affect Lab Review', 'ise', 'ise', 'frustration detection tutoring dialogue'),
    ('https://www.statecraftquarterly.org/essays/the-strait-problem', 'The Strait Problem – Statecraft Quarterly', 'year', 'none', None),
    ('https://www.statecraftquarterly.org/essays/alliances-after-tariffs', 'Alliances After the Tariff Year – Statecraft Quarterly', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/03/chip-controls-round-three', 'Chip Controls, Round Three: What Changed – The Global Brief', 'year', 'none', None),
    ('https://www.globalbrief.example/2025/11/the-chip-truce', 'The Chip Truce, Explained – The Global Brief', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/01/a-year-of-tariffs', 'A Year of Tariffs in Five Charts – The Global Brief', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/04/rare-earth-processing', 'Rare Earths Are a Processing Story – The Global Brief', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/08/arctic-routes', 'Arctic Routes and the Summer Melt – The Global Brief', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/09/middle-power-summit', 'What the Middle-Power Summit Did Not Say – The Global Brief', 'year', 'none', None),
    ('https://aerobicbase.run/articles/strides-and-easy-days', 'Strides on Easy Days | Aerobic Base', 'year', 'run', 'strides how many'),
    ('https://aerobicbase.run/articles/cross-training-counts', 'Does Cross-Training Count? | Aerobic Base', 'year', 'run', 'elliptical vs running aerobic'),
    ('https://weeknightpan.com/recipes/peanut-noodles', 'Ten-Minute Peanut Noodles – Weeknight Pan', 'year', 'none', None),
    ('https://www.globalbrief.example/2026/06/shipping-lanes-insurance', 'Why Shipping Insurance Is the Real Signal – The Global Brief', 'year', 'none', None),
    ('https://aerobicbase.run/articles/heart-rate-drift-test', 'The 60-Minute Drift Test | Aerobic Base', 'year', 'run', 'heart rate drift test'),
    ('https://aerobicbase.run/articles/treadmill-vs-road', 'Treadmill vs Road: Is 1% Incline Real? | Aerobic Base', 'year', 'run', 'treadmill incline equivalent'),
    ('https://beatlab.academy/tutorials/exporting-stems', 'Exporting Stems Cleanly – BeatLab Academy', 'year', 'music', 'fl studio export stems'),
    ('https://www.citywalker.guide/san-francisco/running-routes', 'Ten Running Routes in San Francisco – City Walker', 'post_move', 'run', 'golden gate park running loop distance'),
    ('https://www.citywalker.guide/blacksburg/trails', 'Trails Around Blacksburg – City Walker', 'pre_move', 'run', 'blacksburg trail running routes'),
    ('https://cs1notebook.org/posts/office-hours-queues', 'Office Hours Queues That Do Not Collapse – The CS1 Notebook', 'tacode', 'tacode', None),
    ('https://mlpitfalls.dev/posts/llm-cluster-labels', 'Can an LLM Name Your Clusters? – ML Pitfalls', 'dynamite', 'dynamite', 'llm generate cluster labels from samples'),
    ('https://affectlab.review/overviews/survival-analysis-for-engagement', 'Survival Analysis for Engagement Data – Affect Lab Review', 'ise', 'ise', 'survival analysis time to event python lifelines'),
    ('https://foundernotes.legal/financing/option-pool-shuffle', 'The Option Pool Shuffle – Founder Notes', 'mathetic', 'mathetic', 'option pool size pre seed'),
    ('https://fieldnotes.researchware.dev/dedupe-is-a-product-decision', 'Dedupe Is a Product Decision | Field Notes on Research Software', 'engelbart', 'engelbart', 'dedupe pdfs by doi'),
]
for url, title, win, topic, via in ART:
    add(url, title, win, R.choice([1, 1, 2, 2, 3]), topic, via=search_url.get(via))

# docs pages
DOCS = [
    ('https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html', 'GroupKFold — scikit-learn 1.5 documentation', 'ide_reb', 'ide_reb', 4),
    ('https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html', 'GroupShuffleSplit — scikit-learn 1.5 documentation', 'ide_reb', 'ide_reb', 3),
    ('https://scikit-learn.org/stable/modules/cross_validation.html', '3.1. Cross-validation: evaluating estimator performance — scikit-learn', 'ide_reb', 'ide_reb', 2),
    ('https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html', 'cohen_kappa_score — scikit-learn', 'vizpi', 'vizpi', 3),
    ('https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting', '1.11. Ensembles — scikit-learn', 'uist_crunch', 'uist_crunch', 2),
    ('https://hdbscan.readthedocs.io/en/latest/parameter_selection.html', 'Parameter Selection for HDBSCAN* — hdbscan 0.8.1 documentation', 'dynamite', 'dynamite', 5),
    ('https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html', 'How HDBSCAN Works — hdbscan documentation', 'dynamite', 'dynamite', 2),
    ('https://umap-learn.readthedocs.io/en/latest/clustering.html', 'Using UMAP for Clustering — umap 0.5 documentation', 'dynamite', 'dynamite', 3),
    ('https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html', 'Survival regression — lifelines documentation', 'ise', 'ise', 3),
    ('https://developer.mozilla.org/en-US/docs/Web/API/WebSocket', 'WebSocket - Web APIs | MDN', 'vizpi', 'vizpi', 3),
    ('https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API', 'Page Visibility API - Web APIs | MDN', 'vizpi', 'vizpi', 2),
    ('https://socket.io/docs/v4/client-socket-instance/', 'The Socket instance (client-side) | Socket.IO', 'vizpi', 'vizpi', 4),
    ('https://expressjs.com/en/guide/error-handling.html', 'Express error handling', 'cs3604', 'cs3604', 2),
    ('https://testing-library.com/docs/react-testing-library/intro/', 'React Testing Library | Testing Library', 'cs3604', 'cs3604', 3),
    ('https://supabase.com/docs/guides/database/postgres/row-level-security', 'Row Level Security | Supabase Docs', 'tacode', 'tacode', 2),
    ('https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE', 'PostgreSQL: SELECT ... FOR UPDATE', 'tacode', 'tacode', 1),
    ('https://www.overleaf.com/learn/latex/Positioning_of_Figures', 'Positioning of Figures - Overleaf, Online LaTeX Editor', 'uist_crunch', 'uist_crunch', 2),
    ('https://www.acm.org/publications/proceedings-template', 'ACM Primary Article Template', 'uist_crunch', 'uist_crunch', 3),
    ('https://www.acm.org/publications/taps/accepted-latex-packages', 'TAPS Accepted LaTeX Packages', 'uist_cr', 'uist_cr', 2),
    ('https://ffmpeg.org/ffmpeg-filters.html#subtitles-1', 'FFmpeg Filters Documentation', 'uist_cr', 'uist_cr', 1),
    ('https://docs.anthropic.com/en/docs/claude-code/hooks', 'Hooks reference - Claude Code', 'plugins', 'plugins', 5),
    ('https://docs.anthropic.com/en/docs/claude-code/plugins', 'Plugins - Claude Code', 'plugins', 'plugins', 3),
    ('https://www.w3.org/TR/prov-dm/', 'PROV-DM: The PROV Data Model', 'engelbart', 'engelbart', 2),
    ('https://reactflow.dev/learn/advanced-use/performance', 'Performance - React Flow', 'engelbart', 'engelbart', 3),
    ('https://www.electronjs.org/docs/latest/tutorial/performance', 'Performance | Electron', 'engelbart', 'engelbart', 2),
    ('https://developers.notion.com/reference/intro', 'Introduction - Notion API', 'engelbart', 'engelbart', 2),
    ('https://www.crossref.org/documentation/retrieve-metadata/rest-api/', 'REST API - Crossref', 'engelbart', 'engelbart', 2),
    ('https://docs.python.org/3/library/sqlite3.html', 'sqlite3 — DB-API 2.0 interface for SQLite databases — Python 3.12', 'year', 'none', 2),
    ('https://docs.brew.sh/Brew-Bundle-and-Brewfile', 'brew bundle and Brewfile — Homebrew Documentation', 'newmac', 'none', 2),
    ('https://neurips.cc/Conferences/2026/CallForDatasetsBenchmarks', 'NeurIPS 2026 Call for Datasets & Benchmarks', 'ide_sub', 'ide_sub', 4),
]
for url, title, win, topic, n in DOCS:
    add(url, title, win, n, topic)

# GitHub
REPOS = [('Mathetic-PBC/engelbart', 'engelbart', 'engelbart', 30), ('Mathetic-PBC/engelbart-canvas', 'engelbart', 'engelbart', 18),
         ('Mathetic-PBC/landing', 'mathetic', 'mathetic', 9), ('Mathetic-PBC/claude-plugins', 'plugins', 'plugins', 14),
         ('PRIME-Lab-VT/vizpi_frontend', 'vizpi', 'vizpi', 16), ('PRIME-Lab-VT/tutortrace', 'uist_crunch', 'uist_crunch', 12),
         ('PRIME-Lab-VT/idetrace', 'ide_sub', 'ide_sub', 10), ('PRIME-Lab-VT/dynamite', 'dynamite', 'dynamite', 8),
         ('PRIME-Lab-VT/tacode', 'tacode', 'tacode', 4), ('dbarron410/portfolio', 'portfolio', 'portfolio', 6)]
for repo, win, topic, n in REPOS:
    add(f'https://github.com/{repo}', f'{repo}', win, n, topic, typed=1)
    add(f'https://github.com/{repo}/pulls', f'Pull requests · {repo}', win, max(1, n // 4), topic)
ISSUES = [
    ('Mathetic-PBC/engelbart', 'issues', 41, 'Claude import stops at 1000 conversations', 'engelbart'),
    ('Mathetic-PBC/engelbart', 'issues', 43, 'Same paper imported twice (Zotero + Downloads)', 'engelbart'),
    ('Mathetic-PBC/engelbart', 'pull', 46, 'import: paginate until cursor is empty', 'engelbart'),
    ('Mathetic-PBC/engelbart', 'pull', 48, 'dedupe: DOI first, title/author/year fallback', 'engelbart'),
    ('Mathetic-PBC/engelbart', 'issues', 50, 'Connect screen: rename "Other" to "More tools"', 'engelbart'),
    ('Mathetic-PBC/engelbart-canvas', 'issues', 12, 'Canvas does not re-render after import finishes', 'engelbart'),
    ('Mathetic-PBC/engelbart-canvas', 'pull', 15, 'canvas: subscribe to import-complete event', 'engelbart'),
    ('Mathetic-PBC/claude-plugins', 'pull', 7, 'hc: keep env var names verbatim through compaction', 'plugins'),
    ('Mathetic-PBC/claude-plugins', 'issues', 5, 'hc 0.5.0 loses file list after compaction', 'plugins'),
    ('Mathetic-PBC/landing', 'pull', 3, 'copy v3 from Hudson', 'mathetic'),
    ('PRIME-Lab-VT/vizpi_frontend', 'pull', 88, 'Await token refresh before re-subscribing (deploy-2 hotfix)', 'vizpi'),
    ('PRIME-Lab-VT/vizpi_frontend', 'issues', 90, 'Heartbeat should report buffered event count', 'vizpi'),
    ('PRIME-Lab-VT/vizpi_frontend', 'pull', 84, 'Replay timeline: virtualize rows', 'vizpi'),
    ('PRIME-Lab-VT/idetrace', 'pull', 31, 'make_splits: group by student_id', 'ide_reb'),
    ('PRIME-Lab-VT/idetrace', 'issues', 30, 'Leakage: students appear in train and test', 'ide_reb'),
    ('PRIME-Lab-VT/tutortrace', 'pull', 22, 'Fig 4: colorblind-safe palette', 'uist_cr'),
    ('PRIME-Lab-VT/tutortrace', 'pull', 25, 'Cross-course analysis (Spring 2026 offering)', 'uist_cr'),
    ('PRIME-Lab-VT/dynamite', 'pull', 4, 'UMAP to 10d before HDBSCAN', 'dynamite'),
    ('PRIME-Lab-VT/tacode', 'issues', 19, 'Two TAs can claim the same ticket', 'tacode'),
]
for repo, kind, num, title, topic in ISSUES:
    win = topic if topic in W else 'engelbart'
    add(f'https://github.com/{repo}/{kind}/{num}', f'{title} · {"Issue" if kind == "issues" else "Pull Request"} #{num} · {repo}', win, R.randint(2, 6), topic)

# Linear
LIN = [(101, 'Import: expected vs imported counts per connector'), (102, 'Claude export pagination'), (103, 'DOI dedupe'),
       (104, 'Group "Copy of" / v2 as versions'), (105, 'Connect screen v3 groups'), (106, 'Notion connector spike'),
       (107, 'Granola connector spike'), (108, 'Canvas re-render after import'), (109, 'Pilot metrics: trails opened per week'),
       (110, 'Landing copy v3'), (111, 'Berkeley site: sign-up form'), (112, 'Unassigned bucket for non-research items'),
       (113, 'Per-project import exclusions'), (114, 'Onboarding script for pilots'), (115, 'Demo workspace for Surplus Friday')]
for num, title in LIN:
    add(f'https://linear.app/mathetic/issue/ENG-{num}', f'ENG-{num} {title}', 'engelbart' if num != 111 else 'berkeley',
        R.randint(2, 6), 'engelbart' if num not in (110, 111, 115) else ('mathetic' if num != 111 else 'berkeley'))
add('https://linear.app/mathetic/team/ENG/active', 'Active issues · ENG · Mathetic', 'engelbart', 24, 'engelbart', typed=1)

# claude.ai / chatgpt chats (titles only; the chats themselves are other tools' data)
CHATS = [('Websocket reconnect drops events', 'vizpi'), ('Kappa for three raters', 'vizpi'), ('P4 late-day regrade wording', 'cs3604'),
         ('TACode claim race fix', 'tacode'), ('HDBSCAN noise too high', 'dynamite'), ('Cluster label sanity check', 'dynamite'),
         ('Frustration codebook draft', 'ise'), ('Lifelines Cox model output', 'ise'), ('Papert Lab notebook idea', 'papert'),
         ('Engelbart 1962 summary', 'augcog'), ('Tighten related work paragraph', 'uist_crunch'), ('LaTeX figure overflow', 'uist_crunch'),
         ('Rebuttal: label reliability', 'uist_rebut'), ('Rebuttal character count', 'uist_rebut'), ('TAPS font embedding error', 'uist_cr'),
         ('Talk script timing cuts', 'uist_talk'), ('Q&A prep for UIST talk', 'uist_talk'), ('Datasheet for IDETrace', 'ide_sub'),
         ('Leakage check in split script', 'ide_reb'), ('Rebuttal numbers table', 'ide_reb'), ('Leave of absence email to Yan', 'admin_leave'),
         ('Post-money SAFE math', 'mathetic'), ('Pitch deck narrative', 'mathetic'), ('Call prep: angel investor', 'mathetic'),
         ('Import dedupe design', 'engelbart'), ('Connect screen copy', 'engelbart'), ('Canvas render bug', 'engelbart'),
         ('Pilot onboarding script', 'engelbart'), ('Berkeley interview questions', 'berkeley'), ('Synthesis of three interviews', 'berkeley'),
         ('Compaction hook rules', 'plugins'), ('Portfolio page structure', 'portfolio'), ('Meal prep for base training', 'none'),
         ('Half marathon race plan', 'race'), ('Chess: why do I lose b2', 'none'), ('Export controls reading list', 'none'),
         ('SF neighborhoods for a runner', 'sfmove'), ('Brewfile for new Mac', 'newmac'), ('Car shipping vs driving', 'sfmove'),
         ('Sidechain settings at 84 bpm', 'music')]
for i, (title, topic) in enumerate(CHATS):
    win = topic if topic in W else ('sfmove' if topic == 'sfmove' else 'year')
    if topic == 'music': win = ('2026-07-15', '2026-09-14')
    t = topic if topic in P or topic == 'none' else 'none'
    host = 'https://claude.ai/chat/' if i % 4 else 'https://chatgpt.com/c/'
    add(host + uid(('bh-chat', i)), f'{title} - Claude' if i % 4 else title, win, R.randint(1, 5), t if topic not in ('sfmove', 'newmac') else 'none')
add('https://claude.ai/new', 'Claude', 'year', 110, 'none', typed=1)
add('https://chatgpt.com/', 'ChatGPT', 'year', 18, 'none', typed=1)

# Google workspace / VT / course sites
GW = [('https://mail.google.com/mail/u/0/#inbox', 'Inbox - dbarron410@vt.edu - Virginia Tech Mail', 'year', 115, 'none', 1),
      ('https://mail.google.com/mail/u/1/#inbox', 'Inbox - davidbarron410@gmail.com - Gmail', 'year', 85, 'none', 1),
      ('https://mail.google.com/mail/u/2/#inbox', 'Inbox - david.barron.runs@gmail.com - Gmail', ('2025-12-06', '2026-10-17'), 30, 'run', 0),
      ('https://drive.google.com/drive/u/0/my-drive', 'My Drive - Google Drive', 'year', 25, 'none', 1),
      ('https://calendar.google.com/calendar/u/0/r/week', 'Google Calendar - Week', 'year', 50, 'none', 1),
      ('https://canvas.vt.edu/courses/214503', 'CS 3604: Professionalism in Computing (Fall 2025)', 'cs3604', 28, 'cs3604', 1),
      ('https://canvas.vt.edu/courses/214503/gradebook', 'Gradebook: CS 3604', 'cs3604', 22, 'cs3604', 0),
      ('https://canvas.vt.edu/courses/214503/assignments/2290431', 'P3: REST API', 'cs3604', 6, 'cs3604', 0),
      ('https://canvas.vt.edu/courses/214503/assignments/2290432', 'P4: React Front End', 'cs3604', 7, 'cs3604', 0),
      ('https://canvas.vt.edu/courses/214503/assignments/2290440', 'Final Project', 'cs3604', 8, 'cs3604', 0),
      ('https://canvas.vt.edu/courses/219877', 'ISE 6664: Affective Design & Computing (Spring 2026)', 'ise', 20, 'ise', 1),
      ('https://canvas.vt.edu/courses/219877/modules', 'Modules: ISE 6664', 'ise', 9, 'ise', 0),
      ('https://canvas.vt.edu/courses/219877/assignments/2311050', 'Final Project Report', 'ise', 4, 'ise', 0),
      ('https://graduateschool.vt.edu/academics/forms.html', 'Forms | Graduate School | Virginia Tech', 'admin_leave', 4, 'admin_leave', 0),
      ('https://graduateschool.vt.edu/academics/leave-of-absence.html', 'Leave of Absence | Graduate School | Virginia Tech', 'admin_leave', 3, 'admin_leave', 0),
      ('https://www.overleaf.com/project/6612a4c0f1e2b3a4c5d6e7f8', 'TutorTrace UIST 2026 - Online LaTeX Editor Overleaf', ('2026-03-01', '2026-08-14'), 45, 'uist_crunch', 0),
      ('https://www.overleaf.com/project/66d0b1c2e3f4a5b6c7d8e9f0', 'TutorTrace rebuttal - Online LaTeX Editor Overleaf', 'uist_rebut', 12, 'uist_rebut', 0),
      ('https://www.overleaf.com/project/6630c9d8e7f6a5b4c3d2e1f0', 'IDETrace NeurIPS D&B - Online LaTeX Editor Overleaf', 'ide_sub', 25, 'ide_sub', 0),
      ('https://openreview.net/group?id=NeurIPS.cc/2026/Datasets_and_Benchmarks', 'NeurIPS 2026 Datasets and Benchmarks Track | OpenReview', ('2026-04-28', '2026-07-30'), 9, 'ide_sub', 0),
      ('https://openreview.net/forum?id=Xk3pQ9vR2t', 'IDETrace: A Dataset for Novice Programmer Behavior in AI-Assisted Coding | OpenReview', 'ide_reb', 14, 'ide_reb', 0),
      ('https://new.precisionconference.com/uist26/author', 'PCS - UIST 2026 submissions', ('2026-03-20', '2026-07-03'), 16, 'uist_crunch', 0),
      ('https://uist.acm.org/2026/', 'UIST 2026 - ACM Symposium on User Interface Software and Technology', ('2026-01-20', '2026-10-08'), 10, 'uist_talk', 0),
      ('https://uist.acm.org/2026/registration/', 'Registration – UIST 2026', ('2026-08-25', '2026-09-03'), 3, 'uist_talk', 0),
      ('https://scholar.google.com/', 'Google Scholar', 'year', 30, 'none', 1),
      ('https://scholar.google.com/scholar?q=productive+struggle+silent+stalling+telemetry', 'productive struggle silent stalling telemetry - Google Scholar', 'uist_crunch', 2, 'uist_crunch', 0),
      ('https://arxiv.org/abs/2507.01842', '[2507.01842] Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1', 'uist_crunch', 3, 'uist_crunch', 0),
      ('https://arxiv.org/list/cs.HC/recent', 'Human-Computer Interaction authors/titles recent submissions - arXiv', 'year', 14, 'none', 1),
      ('https://zoom.us/j/93117722045', 'Launch Meeting - Zoom', ('2026-09-16', '2026-10-13'), 3, 'berkeley', 0),
      ('https://www.dougengelbart.org/content/view/138', 'Augmenting Human Intellect: A Conceptual Framework', 'augcog', 3, 'augcog', 0)]
for url, title, win, n, topic, typed in GW:
    add(url, title, win, n, topic, typed=typed)
for i, (name, win, topic) in enumerate([('VizPI labeling guide v3', 'vizpi', 'vizpi'), ('CS 3604 F25 grading', 'cs3604', 'cs3604'),
                                        ('Dynamite clustering notes', 'dynamite', 'dynamite'), ('ISE 6664 project proposal', 'ise', 'ise'),
                                        ('UIST26 rebuttal draft', 'uist_rebut', 'uist_rebut'), ('UIST26 talk script', 'uist_talk', 'uist_talk'),
                                        ('Copy of UIST26 talk script', 'uist_talk', 'uist_talk'), ('Leave of absence plan', 'admin_leave', 'admin_leave'),
                                        ('Mathetic cap table', 'mathetic', 'mathetic'), ('Mathetic pre-seed v2', 'mathetic', 'mathetic'),
                                        ('Berkeley research chats sign-up', 'berkeley', 'berkeley'), ('Engelbart import dedupe spec', 'engelbart', 'engelbart'),
                                        ('Training log 2026', 'year', 'run'), ('SF apartment comparison', 'sfmove', 'none'), ('Meal plan', 'year', 'none')]):
    kind = 'spreadsheets' if any(k in name for k in ('grading', 'cap table', 'sign-up', 'Training', 'apartment')) else (
        'presentation' if 'pre-seed' in name else 'document')
    suffix = {'spreadsheets': 'Google Sheets', 'presentation': 'Google Slides', 'document': 'Google Docs'}[kind]
    add(f'https://docs.google.com/{kind}/d/{base64.urlsafe_b64encode(hashlib.sha256(name.encode()).digest()).decode()[:44]}/edit',
        f'{name} - {suffix}', win, R.randint(4, 14), topic)

# localhost (VizPI dev, Engelbart dev)
for route, title, win, topic, n in [('5173/', 'VizPI', 'vizpi', 'vizpi', 14), ('5173/replay', 'VizPI — Replay', 'vizpi', 'vizpi', 12),
                                    ('5173/ta-dashboard', 'VizPI — TA dashboard', 'vizpi', 'vizpi', 10), ('3000/', 'Engelbart', 'engelbart', 'engelbart', 20),
                                    ('3000/canvas', 'Engelbart — Canvas', 'engelbart', 'engelbart', 26), ('3000/connect', 'Engelbart — Connect your tools', 'engelbart', 'engelbart', 18),
                                    ('3000/import/summary', 'Engelbart — Import summary', 'engelbart', 'engelbart', 12), ('8888/lab', 'JupyterLab', 'dynamite', 'dynamite', 10),
                                    ('8888/lab/tree/make_splits.ipynb', 'make_splits.ipynb - JupyterLab', 'ide_reb', 'ide_reb', 6)]:
    add(f'http://localhost:{route}', title, win, n, topic, typed=1)

# Strava activities, Garmin, lichess, YouTube, Reddit, shopping, misc
rr = random.Random('strava-ids')
for i in range(75):
    d = bursty_dates(1, f'strava-{i}')[0]
    aid = 16210000000 + int((d.timestamp() - 1760000000) * 700) + rr.randint(0, 999)
    nm = rr.choice(['Morning Run', 'Morning Run', 'Evening Run', 'Lunch Ride', 'Morning Ride', 'Elliptical'])
    kind = 'Ride' if 'Ride' in nm else ('Elliptical' if nm == 'Elliptical' else 'Run')
    add(f'https://www.strava.com/activities/{aid}', f'{nm} | {kind} | Strava', (d, min(d + datetime.timedelta(hours=6), dt(REF))), rr.choice([1, 1, 2]), 'run')
add('https://www.strava.com/dashboard', 'Dashboard | Strava', 'year', 70, 'run', typed=1)
add('https://www.strava.com/athletes/58213377/training/log', 'Training Log | Strava', 'year', 12, 'run')
add('https://connect.garmin.com/modern/sleep', 'Sleep | Garmin Connect', ('2026-04-01', '2026-10-17'), 14, 'run')
add('https://www.bayareahalf.example/results/2026', '2026 Results – Bay Area Half Marathon', ('2026-10-15 13:00', '2026-10-17'), 4, 'run')
add('https://www.bayareahalf.example/participant-info', 'Participant Info – Bay Area Half Marathon', 'race', 3, 'run')
lr = random.Random('lichess')
for i in range(46):
    d = bursty_dates(1, f'lichess-{i}', end='2026-08-01')[0]
    gid = ''.join(lr.choice('abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(8))
    opp = lr.choice(['knightowl88', 'pawnstorm_', 'castle_long', 'zugzwang_zed', 'bishoppair', 'rook_n_roll', 'e4e5fan', 'tempo_thief'])
    col = lr.choice(['White', 'Black'])
    add(f'https://lichess.org/{gid}', f'Rapid Chess • dbarron_runs vs {opp} • lichess.org' if col == 'White' else f'Rapid Chess • {opp} vs dbarron_runs • lichess.org',
        (d, d + datetime.timedelta(minutes=30)), 1, 'none')
add('https://lichess.org/', 'lichess.org • Free Online Chess', 'year', 55, 'none', typed=1)
add('https://lichess.org/training', 'Puzzles • lichess.org', 'year', 25, 'none')
YT = [('dQ1rK8vLmX0', 'FL Studio sidechain in 5 minutes (no plugins)', 'music'), ('pX4n7sB2wQe', 'Making a lofi beat from scratch at 84 bpm', 'music'),
      ('h7Gm2xLq9Rt', 'How pros voice minor 9 chords', 'music'), ('Zr8kW3eNvY1', 'Zone 2 explained by an exercise physiologist', 'run'),
      ('c2Lp9dTsQ4a', 'Half marathon race day mistakes', 'run'), ('mN5vB8xK2Ls', 'Golden Gate Park long run loop tour', 'run'),
      ('qW3eR6tY9uI', 'The London System: every trap in 20 minutes', 'none'), ('aS1dF4gH7jK', 'Caro-Kann Advance: the modern main line', 'none'),
      ('zX2cV5bN8mQ', 'The Mother of All Demos (1968), full', 'augcog'), ('lK9jH6gF3dS', 'Why the strait matters: a shipping explainer', 'none'),
      ('pO8iU5yT2rE', 'How to give a 15 minute conference talk', 'uist_talk'), ('wE4rT7yU1iO', 'Fixing a bent derailleur hanger at home', 'none'),
      ('tY6uI9oP3aS', 'Moving to San Francisco: what nobody tells you', 'none'), ('gH2jK5lZ8xC', 'HDBSCAN clustering visually explained', 'dynamite'),
      ('vB3nM6qW9eR', 'Survival analysis in 15 minutes', 'ise'), ('yU7iO1pA4sD', 'Startup cap tables for first-time founders', 'mathetic'),
      ('fG8hJ2kL5zX', 'Gochujang chicken meal prep', 'none'), ('cV4bN7mQ1wE', 'Treadmill vs outdoor running: the science', 'run')]
for vid, title, topic in YT:
    win = {'music': 'year', 'run': 'year', 'none': 'year', 'augcog': 'augcog', 'uist_talk': 'uist_talk', 'dynamite': 'dynamite', 'ise': 'ise', 'mathetic': 'mathetic'}[topic]
    if 'San Francisco' in title: win = 'sfmove'
    if 'derailleur' in title: win = 'bike'
    add(f'https://www.youtube.com/watch?v={vid}', f'{title} - YouTube', win, R.randint(1, 3), topic)
add('https://www.youtube.com/', 'YouTube', 'year', 45, 'none', typed=1)
RED = [('running', 'how strict are you about the zone 2 ceiling?', 'run', 'year'), ('running', 'first half marathon after a year of base building', 'run', 'race'),
       ('AskSF', 'which neighborhood for someone who runs every morning?', 'none', 'sfmove'), ('AskSF', 'is this sublet listing a scam', 'none', 'sfmove'),
       ('FL_Studio', 'sidechain sounds like pumping too much', 'music', 'year'), ('chess', 'I keep losing b2 in the London', 'none', 'year'),
       ('GradSchool', 'taking a leave of absence to start a company', 'none', 'admin_leave'), ('cscareerquestions', 'recruiter keeps emailing about a dev tools role', 'none', 'year'),
       ('bikewrench', 'skipping in middle cogs after a crash', 'none', 'bike'), ('MachineLearning', 'found leakage after submission, what now', 'ide_reb', 'ide_reb'),
       ('Blacksburg', 'best long run routes', 'run', 'pre_move'), ('geopolitics', 'do export controls actually work', 'none', 'year'),
       ('mealprep', 'cheap high carb meal prep for runners', 'none', 'year'), ('startups', 'post-money safe dilution confusion', 'mathetic', 'mathetic')]
for i, (sub, title, topic, win) in enumerate(RED):
    add(f'https://www.reddit.com/r/{sub}/comments/{hexid(("rd", i), 7)}/{title.replace(" ", "_").replace("?", "").replace(",", "")[:50]}/',
        f'{title} : r/{sub}', win, R.randint(1, 2), topic)
MISC = [('https://www.valleycycles.example/service', 'Service – Valley Cycles Blacksburg', 'bike', 'none', 2),
        ('https://loopbank.example.com/packs/tape-drums', 'Tape Drums — Loopbank', ('2026-08-28', '2026-08-31'), 'music', 3),
        ('https://loopbank.example.com/packs/brass-stabs-vol-2', 'Brass Stabs Vol. 2 — Loopbank', ('2026-02-12', '2026-02-15'), 'music', 2),
        ('https://loopbank.example.com/packs/dusty-keys', 'Dusty Keys — Loopbank', ('2026-05-28', '2026-05-31'), 'music', 2),
        ('https://www.carhaul.example/quote', 'Get a Quote – CarHaul Auto Transport', ('2026-07-14', '2026-07-20'), 'none', 4),
        ('https://www.carhaul.example/track/58213', 'Track Order 58213 – CarHaul', ('2026-08-05', '2026-08-15'), 'none', 6),
        ('https://www.flyway.example/trips/QK7P2D', 'Trip QK7P2D — SFO to DTW', ('2026-09-18', '2026-10-08'), 'uist_talk', 5),
        ('https://www.flyway.example/flights/iad-dub', 'Flights from Washington to Dublin', 'wedding', 'none', 3),
        ('https://www.roomboard.example/sf/inner-sunset/room-1650', 'Sunny room in Inner Sunset 3BR – $1,650 – RoomBoard', 'sfmove', 'none', 3),
        ('https://www.roomboard.example/sf/mission/room-1900', 'Room in Mission 2BR, in-unit laundry – $1,900 – RoomBoard', 'sfmove', 'none', 4),
        ('https://www.roomboard.example/sf/outer-richmond/room-1450', 'Room in Outer Richmond 4BR – $1,450 – RoomBoard', 'sfmove', 'none', 2),
        ('https://www.roomboard.example/sf/nob-hill/studio-2350', 'Nob Hill studio – $2,350 – RoomBoard', 'sfmove', 'none', 1),
        ('https://www.sfmta.com/getting-around/transit/fares-passes', 'Fares & Passes | SFMTA', 'sfmove', 'none', 2),
        ('https://www.dmv.ca.gov/portal/vehicle-registration/new-registration/', 'Register a Vehicle New to California', ('2026-08-17', '2026-09-03'), 'none', 3),
        ('https://www.irs.gov/refunds', 'Refunds | Internal Revenue Service', 'taxes', 'none', 3),
        ('https://tax.virginia.gov/individual-income-tax-filing', 'Individual Income Tax Filing | Virginia Tax', 'taxes', 'none', 3),
        ('https://parking.vt.edu/citations/appeal', 'Citation Appeals | Parking Services | Virginia Tech', 'parking', 'none', 2),
        ('https://moversguide.usps.com/', 'Official USPS Change of Address', ('2026-07-28', '2026-08-06'), 'none', 2),
        ('https://www.surplus-house.example/residents', 'Residents — Surplus', 'mathetic', 'mathetic', 8),
        ('https://www.surplus-house.example/fridays', 'Demo Fridays — Surplus', 'mathetic', 'mathetic', 5),
        ('https://weather.example.com/forecast/blacksburg-va', 'Blacksburg, VA 10-Day Weather Forecast', 'pre_move', 'none', 20),
        ('https://weather.example.com/forecast/san-francisco-ca', 'San Francisco, CA 10-Day Weather Forecast', 'post_move', 'none', 10),
        ('https://www.chess.com/play/online', 'Play Chess Online', 'year', 'none', 6),
        ('https://www.statecraftquarterly.org/', 'Statecraft Quarterly', 'year', 'none', 8),
        ('https://www.globalbrief.example/', 'The Global Brief — daily newsletter', 'year', 'none', 10),
        ('https://www.registry.example/niamh-and-conor', 'Niamh & Conor — Wedding Registry', 'wedding', 'none', 3),
        ('https://www.amazon.com/gp/your-account/order-history', 'Your Orders', 'year', 'none', 9),
        ('https://www.apple.com/shop/buy-mac/macbook-pro', 'Buy MacBook Pro - Apple', ('2026-07-20', '2026-07-24'), 'none', 4),
        ('https://www.apple.com/shop/order/list', 'Order Status - Apple', ('2026-07-24', '2026-08-04'), 'none', 5),
        ('https://accounts.google.com/o/oauth2/v2/auth?client_id=strava', 'Sign in - Google Accounts', 'year', 'none', 3, )]
for url, title, win, topic, n in MISC:
    add(url, title, win, n, topic)
for i in range(12):  # sign-in / redirect places, hidden like Firefox does for redirect sources
    add(f'https://www.google.com/url?q=https://www.longmemory.press/essays/{i}&sa=D&ust={1760000000000 + i * 977}', None, 'year', 1, 'none', hidden=1)

# ---------------------------------------------------------------------------------------------------------
# build Firefox visits


def prtime(d):
    return int(round(epoch(d) * 1_000_000))


def moz_hash(s):
    h = 0
    for ch in s.encode('utf-8'):
        h = (((h << 5) | (h >> 27)) & 0xFFFFFFFF) ^ ch
        h = (0x9E3779B9 * h) & 0xFFFFFFFF
    return h


def url_hash(url):
    prefix = url.split(':', 1)[0][:50]
    return ((moz_hash(prefix) & 0x0000FFFF) << 32) + moz_hash(url)


def guid(seed):
    return base64.urlsafe_b64encode(hashlib.sha256(str(seed).encode()).digest()).decode()[:12]


def rev_host(url):
    h = urlsplit(url).hostname or ''
    return h[::-1] + '.'


def topic_pids(t):
    return P.get(t, ['project_none'])


# dedupe urls (first wins)
seen = set(); PL = []
for p in PLACES:
    if p['url'] in seen: continue
    seen.add(p['url']); PL.append(p)
for i, p in enumerate(PL, 1): p['id'] = i
by_url = {p['url']: p for p in PL}

raw = []  # (time, place, from_place_url, visit_type)
for p in PL:
    lo, hi = p['win']
    lo, hi = dt(lo), min(dt(hi), REF)
    if hi <= lo: hi = lo + datetime.timedelta(hours=2)
    times = bursty_dates(p['n'], 'ff|' + p['url'], start=lo, end=hi) if hi - lo > datetime.timedelta(days=2) else \
        sorted(lo + (hi - lo) * random.Random(f"ffs|{p['url']}|{k}").random() for k in range(p['n']))
    for k, t in enumerate(times):
        vt = 2 if (p['typed'] and k % 2 == 0) else 1
        if p['hidden']: vt = 6
        raw.append([t, p, None, vt])
        if p['via'] and k == 0:  # first visit came from a search
            raw.append([t - datetime.timedelta(seconds=random.Random(p['url']).randint(20, 95)), by_url[p['via']], None, 1, 'search_for', p])
raw.sort(key=lambda r: r[0])
visits = []; vid_of_search = {}
for i, r in enumerate(raw, 1):
    t, p, _, vt = r[:4]
    visits.append([i, 0, p['id'], prtime(t), vt, 0, 3 if 'google.com/search' in p['url'] else 0, None])  # source 3 = search results page
    if len(r) > 4: vid_of_search[r[5]['url']] = (i, p['id'])
    elif p['via'] and p['url'] in vid_of_search and visits[-1][1] == 0 and i - vid_of_search[p['url']][0] < 50:
        visits[-1][1] = vid_of_search.pop(p['url'])[0]
# session-like from_visit chains for github issue pages from the repo page
last_visit_of = {}
for v in visits:
    pl = PL[v[2] - 1]
    if 'github.com' in pl['url'] and pl['url'].count('/') > 4 and v[1] == 0:
        repo = '/'.join(pl['url'].split('/')[:5])
        if repo in last_visit_of and v[3] - last_visit_of[repo][1] < 15 * 60 * 1_000_000: v[1] = last_visit_of[repo][0]
    last_visit_of[pl['url']] = (v[0], v[3])

stats = {}
for v in visits:
    s = stats.setdefault(v[2], [0, 0, 0]); s[0] += 1; s[1] = max(s[1], v[3]); s[2] += 1 if v[4] == 2 else 0
origins = {}
for p in PL:
    sp = urlsplit(p['url']); key = (sp.scheme + '://', sp.netloc)
    if key not in origins: origins[key] = len(origins) + 1
place_rows = []
for p in PL:
    cnt, last, typed = stats.get(p['id'], (0, None, 0))
    fre = int(cnt * 100 * (2 if typed else 1) * (0.5 if p['hidden'] else 1))
    sp = urlsplit(p['url'])
    site = {'www.longmemory.press': 'Long Memory', 'cs1notebook.org': 'The CS1 Notebook', 'aerobicbase.run': 'Aerobic Base'}.get(sp.netloc)
    desc = None
    if site: desc = 'Saved for later.' if False else None
    place_rows.append((p['id'], p['url'], p['title'], rev_host(p['url']), cnt, p['hidden'], 1 if typed else 0, fre, last, guid(('place', p['url'])),
                       0, url_hash(p['url']), desc, None, site, origins[(sp.scheme + '://', sp.netloc)], 0, None, 0))
origin_rows = [(i, k[0], k[1], sum(r[7] for r in place_rows if r[15] == i), 0, None, 0) for k, i in origins.items()]

# minimal moz_bookmarks: roots + a few toolbar bookmarks
ROOT_T = prtime('2025-10-17 09:00')
bm = [(1, 2, None, 0, 0, '', None, None, ROOT_T, ROOT_T, 'root________', 1, 1), (2, 2, None, 1, 0, 'menu', None, None, ROOT_T, ROOT_T, 'menu________', 1, 1),
      (3, 2, None, 1, 1, 'toolbar', None, None, ROOT_T, ROOT_T, 'toolbar_____', 1, 1), (4, 2, None, 1, 2, 'tags', None, None, ROOT_T, ROOT_T, 'tags________', 1, 1),
      (5, 2, None, 1, 3, 'unfiled', None, None, ROOT_T, ROOT_T, 'unfiled_____', 1, 1), (6, 2, None, 1, 4, 'mobile', None, None, ROOT_T, ROOT_T, 'mobile______', 1, 1)]
BMK = [('https://claude.ai/new', 3), ('https://www.strava.com/dashboard', 3), ('https://lichess.org/', 3), ('https://linear.app/mathetic/team/ENG/active', 3),
       ('http://localhost:3000/canvas', 3), ('https://www.longmemory.press/essays/memex-at-80', 5),
       ('https://foundernotes.legal/financing/post-money-safe-primer', 5), ('https://aerobicbase.run/articles/zone-2-without-the-hype', 5)]
fc = {}
for i, (u, parent) in enumerate(BMK):
    p = by_url[u]; added = stats[p['id']][1] - 60_000_000 if p['id'] in stats else ROOT_T
    first = min(v[3] for v in visits if v[2] == p['id'])
    bm.append((7 + i, 1, p['id'], parent, i, p['title'], None, None, first + 30_000_000, first + 30_000_000, guid(('bm', u)), 1, 1))
    fc[p['id']] = fc.get(p['id'], 0) + 1
place_rows = [r[:10] + (fc.get(r[0], 0),) + r[11:] for r in place_rows]

FF_SCHEMA = """
CREATE TABLE moz_origins ( id INTEGER PRIMARY KEY, prefix TEXT NOT NULL, host TEXT NOT NULL, frecency INTEGER NOT NULL, recalc_frecency INTEGER NOT NULL DEFAULT 0, alt_frecency INTEGER, recalc_alt_frecency INTEGER NOT NULL DEFAULT 0, UNIQUE (prefix, host) );
CREATE TABLE moz_places (   id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL, typed INTEGER DEFAULT 0 NOT NULL, frecency INTEGER DEFAULT -1 NOT NULL, last_visit_date INTEGER , guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL, url_hash INTEGER DEFAULT 0 NOT NULL , description TEXT, preview_image_url TEXT, site_name TEXT, origin_id INTEGER REFERENCES moz_origins(id), recalc_frecency INTEGER NOT NULL DEFAULT 0, alt_frecency INTEGER, recalc_alt_frecency INTEGER NOT NULL DEFAULT 0);
CREATE TABLE moz_historyvisits (  id INTEGER PRIMARY KEY, from_visit INTEGER, place_id INTEGER, visit_date INTEGER, visit_type INTEGER, session INTEGER, source INTEGER DEFAULT 0 NOT NULL, triggeringPlaceId INTEGER);
CREATE TABLE moz_bookmarks (  id INTEGER PRIMARY KEY, type INTEGER, fk INTEGER DEFAULT NULL, parent INTEGER, position INTEGER, title LONGVARCHAR, keyword_id INTEGER, folder_type TEXT, dateAdded INTEGER, lastModified INTEGER, guid TEXT, syncStatus INTEGER NOT NULL DEFAULT 0, syncChangeCounter INTEGER NOT NULL DEFAULT 1);
CREATE INDEX moz_places_url_hashindex ON moz_places (url_hash);
CREATE INDEX moz_places_hostindex ON moz_places (rev_host);
CREATE INDEX moz_places_visitcount ON moz_places (visit_count);
CREATE INDEX moz_places_frecencyindex ON moz_places (frecency);
CREATE INDEX moz_places_lastvisitdateindex ON moz_places (last_visit_date);
CREATE UNIQUE INDEX moz_places_guid_uniqueindex ON moz_places (guid);
CREATE INDEX moz_places_originidindex ON moz_places (origin_id);
CREATE INDEX moz_historyvisits_placedateindex ON moz_historyvisits (place_id, visit_date);
CREATE INDEX moz_historyvisits_fromindex ON moz_historyvisits (from_visit);
CREATE INDEX moz_historyvisits_dateindex ON moz_historyvisits (visit_date);
CREATE INDEX moz_bookmarks_itemindex ON moz_bookmarks (fk, type);
CREATE INDEX moz_bookmarks_parentindex ON moz_bookmarks (parent, position);
CREATE UNIQUE INDEX moz_bookmarks_guid_uniqueindex ON moz_bookmarks (guid);
PRAGMA user_version = 78;
"""

FF_DIR = 'firefox/Profiles/x7k2p9qd.default-release'
ff_topics = sorted({t for p in PL for t in [p['topic']]})
FF_PIDS = sorted({x for t in ff_topics for x in topic_pids(t)})
first_t = min(v[3] for v in visits) / 1e6; last_t = max(v[3] for v in visits) / 1e6
g.sqlite(f'{FF_DIR}/places.sqlite', FF_SCHEMA, {'moz_origins': origin_rows, 'moz_places': place_rows, 'moz_historyvisits': visits, 'moz_bookmarks': bm},
         datetime.datetime.fromtimestamp(first_t, UTC), datetime.datetime.fromtimestamp(last_t + 40, UTC), account='Firefox (x7k2p9qd.default-release)',
         project_ids=FF_PIDS, modeled_on='Firefox places.sqlite (moz_places / moz_historyvisits schema); authentic/browser-history/<browser>/<profile>/History role',
         notes=f'HARD CASE: personal clutter mixed with work — {len(place_rows)} places, {len(visits)} visits over the year, personal browser with research, company and personal browsing interleaved')


def local_str(us):
    d = datetime.datetime.fromtimestamp(us / 1e6, UTC)
    return d.astimezone(PT if d >= MOVE else ET).strftime('%Y-%m-%d %H:%M:%S')


buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
w.writerow(['visit_time_local', 'url', 'title', 'visit_type'])
for v in visits:
    pl = PL[v[2] - 1]
    if pl['hidden']: continue
    w.writerow([local_str(v[3]), pl['url'], pl['title'] or '', v[4]])
g.text(f'{FF_DIR}/visits.csv', buf.getvalue(), datetime.datetime.fromtimestamp(last_t + 300, UTC), datetime.datetime.fromtimestamp(last_t + 300, UTC),
       account='Firefox (x7k2p9qd.default-release)', project_ids=FF_PIDS,
       modeled_on='authentic/browser-history/<browser>/<profile>/visits.csv (derived flat export)',
       notes='HARD CASE: personal clutter mixed with work — flat CSV derived from places.sqlite (hidden redirect places dropped)')

# ---------------------------------------------------------------------------------------------------------
# Brave (Chrome schema), new Mac 2026-08-04 → 2026-10-17: app + landing-page testing, some personal clutter
BR = []


def badd(url, title, win, n, topic, typed=0):
    BR.append(dict(url=url, title=title, win=win, n=n, topic=topic, typed=typed))


ROUTES = ['/', '/canvas', '/connect', '/import', '/import/summary', '/projects', '/projects/tutortrace', '/projects/engelbart',
          '/projects/idetrace', '/trail', '/settings', '/settings/connectors', '/onboarding', '/onboarding/welcome', '/onboarding/connect',
          '/notebook', '/search', '/debug/dedupe', '/debug/import-log']
for r_ in ROUTES:
    badd(f'http://localhost:3000{r_}', f'Engelbart{" — " + r_.strip("/").replace("/", " / ") if r_ != "/" else ""}', ('2026-08-24', '2026-10-17'), R.randint(3, 14), 'engelbart', typed=1)
for q in ['source=claude', 'source=zotero', 'source=downloads', 'dedupe=preview', 'pilot=priya', 'pilot=daniel', 'debug=1']:
    for r_ in ['/import/summary', '/connect']:
        badd(f'http://localhost:3000{r_}?{q}', f'Engelbart — {r_.strip("/")} ({q})', ('2026-10-01', '2026-10-17'), R.randint(1, 4), 'engelbart')
for nid in range(1, 61):
    badd(f'http://localhost:3000/trail/{hexid(("trail", nid), 10)}', f'Trail — note {nid}', ('2026-09-07', '2026-10-17'), R.randint(1, 3), 'engelbart')
BRANCHES = ['copy-v1', 'copy-v2', 'copy-v3', 'hero-illustration', 'pricing-section', 'pilot-form', 'mobile-nav', 'og-image', 'footer-links',
            'berkeley-page', 'berkeley-signup', 'dark-mode', 'perf-images', 'faq', 'privacy-page', 'cta-wording']
for b in BRANCHES:
    badd(f'https://landing-git-{b}-mathetic.vercel.app/', f'Mathetic — preview ({b})', ('2026-08-20', '2026-10-15'), R.randint(1, 5),
         'berkeley' if 'berkeley' in b else 'mathetic')
for pth, title in [('/', 'Mathetic — Engelbart remembers where your thoughts came from'), ('/pilot', 'Request pilot access — Mathetic'),
                   ('/privacy', 'Privacy — Mathetic'), ('/about', 'About — Mathetic'), ('/berkeley', 'Research chats at Berkeley — Mathetic'),
                   ('/berkeley/signup', 'Sign up for a research chat — Mathetic'), ('/berkeley/thanks', 'Thanks! — Mathetic')]:
    badd(f'https://mathetic.example.com{pth}', title, ('2026-08-26', '2026-10-17'), R.randint(3, 12), 'berkeley' if 'berkeley' in pth else 'mathetic', typed=1)
for slug in ['vizpi', 'dynamite', 'ise6664', 'berkeley-chats', 'mathetic', 'half-marathon', 'beats', 'reading-group', 'cs3604', 'tacode', 'portfolio', 'uist-talk']:
    badd(f'http://localhost:3000/projects/{slug}', f'Engelbart — project {slug}', ('2026-09-07', '2026-10-17'), R.randint(1, 4), 'engelbart')
for i in range(20):
    badd(f'https://landing-{hexid(("dep", i), 9)}-mathetic.vercel.app/', 'Mathetic — Engelbart remembers where your thoughts came from',
         ('2026-08-20', '2026-10-15'), R.randint(1, 2), 'mathetic')
for num, title in LIN:
    badd(f'https://linear.app/mathetic/issue/ENG-{num}', f'ENG-{num} {title}', ('2026-08-24', '2026-10-17'), R.randint(1, 3), 'engelbart')
for b in ['main', 'import-v2', 'dedupe-doi', 'connect-v3', 'canvas-rerender']:
    badd(f'https://github.com/Mathetic-PBC/engelbart/tree/{b}', f'Mathetic-PBC/engelbart at {b}', ('2026-09-01', '2026-10-17'), R.randint(2, 6), 'engelbart')
for n in range(30, 72):
    badd(f'https://github.com/Mathetic-PBC/engelbart/pull/{n}', f'PR #{n} · Mathetic-PBC/engelbart', ('2026-09-01', '2026-10-17'), R.randint(1, 4), 'engelbart')
for n in range(1, 9):
    badd(f'https://github.com/Mathetic-PBC/landing/pull/{n}', f'PR #{n} · Mathetic-PBC/landing', ('2026-08-20', '2026-10-10'), R.randint(1, 3), 'mathetic')
for i, (name, topic) in enumerate([('Lighthouse report: mathetic.example.com', 'mathetic'), ('PageSpeed Insights', 'mathetic'),
                                   ('Open Graph debugger', 'mathetic'), ('Responsive design checker', 'mathetic'),
                                   ('Form submissions — pilot', 'mathetic'), ('Form submissions — berkeley', 'berkeley')]):
    badd(f'https://tools.example.dev/{hexid(("tool", i), 8)}', name, ('2026-08-25', '2026-10-15'), R.randint(2, 6), topic)
QS = ['electron devtools not opening', 'react rerender after ipc event', 'pdf doi regex', 'crossref api doi lookup rate limit', 'vercel preview password',
      'og image size twitter', 'css clamp font size hero', 'html form honeypot spam', 'next.js static export images', 'safari flexbox gap bug',
      'zotero sqlite schema items attachments', 'claude conversations export format', 'chatgpt export conversations.json schema', 'notion export markdown zip',
      'granola api', 'sqlite json_extract array', 'electron app notarize mac', 'detect duplicate files content hash python', 'fuzzy title match papers',
      'berkeley doe library rooms', 'amazon gift card bulk', 'sf mission burrito best', 'embarcadero running route', 'twin peaks run from soma',
      'clipper card apple wallet', 'electron ipc renderer invoke handle', 'react memo not rerendering', 'zustand subscribe outside react',
      'pdfjs extract text first page', 'doi in pdf metadata xmp', 'levenshtein ratio python fast', 'sqlite fts5 tutorial', 'electron auto update github releases',
      'landing page social proof without customers', 'pricing page research tool', 'privacy policy template small startup', 'cookie banner needed if no tracking',
      'interview synthesis affinity mapping', 'consent to record interview template', 'zoom transcript download', 'sf laundromat soma',
      'best burrito mission', 'golden gate bridge run from soma distance', 'presidio running trails', 'detroit people mover', 'uist 2026 badge pickup',
      'pitch deck traction slide pre revenue', 'safe side letter pro rata', 'notion api rate limits', 'granola export markdown', 'renters insurance sf cheap', 'ca dmv appointment', 'smog check sf', 'half marathon taper week', 'detroit hotel near cobo']
for q in QS:
    topic = ('engelbart' if any(k in q for k in ('electron', 'react', 'doi', 'crossref', 'zotero', 'claude', 'chatgpt', 'notion', 'granola', 'sqlite', 'duplicate', 'fuzzy'))
             else 'mathetic' if any(k in q for k in ('vercel', 'og image', 'css', 'honeypot', 'next.js', 'safari')) else
             'berkeley' if any(k in q for k in ('berkeley', 'gift card')) else 'race' if 'half' in q else 'uist_talk' if 'detroit' in q else 'none')
    win = ('2026-08-08', '2026-10-17') if any(k in q for k in ('sf ', 'soma', 'mission', 'golden gate', 'presidio', 'embarcadero', 'twin peaks', 'clipper',
                                                                 'renters', 'dmv', 'smog', 'burrito')) else \
        ('2026-09-20', '2026-10-08') if any(k in q for k in ('detroit', 'uist')) else ('2026-08-26', '2026-09-20') if topic == 'berkeley' else \
        ('2026-09-25', '2026-10-15') if topic == 'race' else ('2026-08-04', '2026-10-17')
    badd(f'https://search.brave.com/search?q={quote_plus(q)}&source=web', f'{q} - Brave Search', win, 1, topic)
for i, (t, topic) in enumerate([('Moving to SF in 2026 — honest review', 'none'), ('Lo-fi beat with tape drums', 'music'), ('Detroit in 48 hours', 'none'),
                                ('Building a canvas app with React Flow', 'engelbart'), ('Startup pitch deck teardown', 'mathetic'),
                                ('Half marathon pacing strategy', 'race'), ('How to interview users', 'berkeley'), ('Electron performance tips', 'engelbart')]):
    badd(f'https://www.youtube.com/watch?v={hexid(("bv", i), 11)}', f'{t} - YouTube', ('2026-08-04', '2026-10-17'), R.randint(1, 2), topic)
for i, t in enumerate(['SoMa coffee with wifi', 'Golden Gate Park loop', 'Ferry Building', 'Mission Dolores Park', 'DMV San Francisco', 'SFO Terminal 3']):
    badd(f'https://www.google.com/maps/place/{quote_plus(t)}/@37.77{i},-122.4{i},15z', f'{t} - Google Maps', ('2026-08-08', '2026-10-17'), R.randint(1, 3), 'none')
badd('https://www.strava.com/dashboard', 'Dashboard | Strava', ('2026-08-04', '2026-10-17'), 6, 'run')
badd('https://claude.ai/new', 'Claude', ('2026-08-04', '2026-10-17'), 14, 'engelbart', typed=1)
badd('https://linear.app/mathetic/team/ENG/active', 'Active issues · ENG · Mathetic', ('2026-08-24', '2026-10-17'), 10, 'engelbart')
badd('https://www.bayareahalf.example/results/2026', '2026 Results – Bay Area Half Marathon', ('2026-10-15 14:00', '2026-10-17'), 2, 'run')
badd('https://uist.acm.org/2026/program/', 'Program – UIST 2026', ('2026-09-25', '2026-10-07'), 3, 'uist_talk')

seen = set(); BL = []
for b in BR:
    if b['url'] in seen: continue
    seen.add(b['url']); BL.append(b)
for i, b in enumerate(BL, 1): b['id'] = i


def webkit(d):
    return int(round((epoch(d) + 11644473600) * 1_000_000))


braw = []
for b in BL:
    lo, hi = dt(b['win'][0]), min(dt(b['win'][1]), REF)
    for k, t in enumerate(bursty_dates(b['n'], 'br|' + b['url'], start=lo, end=hi)):
        braw.append((t, b, k))
braw.sort(key=lambda r: r[0])
bvisits = []; last_by_host = {}
for i, (t, b, k) in enumerate(braw, 1):
    core = 1 if (b['typed'] and k % 2 == 0) else (5 if 'search.brave.com' in b['url'] else 0)
    trans = core | 0x30000000
    host = urlsplit(b['url']).netloc
    frm = 0
    if core == 0 and host in last_by_host and webkit(t) - last_by_host[host][1] < 10 * 60 * 1_000_000: frm = last_by_host[host][0]
    last_by_host[host] = (i, webkit(t))
    dur = random.Random(f'dur-{i}').randint(3, 600) * 1_000_000
    bvisits.append((i, b['id'], webkit(t), frm, None, trans, 0, dur, 0, 0, '', 0, 0, 0, 0, 1, 0, None))
bstats = {}
for v in bvisits:
    s = bstats.setdefault(v[1], [0, 0, 0]); s[0] += 1; s[1] = max(s[1], v[2]); s[2] += 1 if (v[5] & 0xFF) == 1 else 0
urls = [(b['id'], b['url'], b['title'], bstats[b['id']][0], bstats[b['id']][2], bstats[b['id']][1], 0) for b in BL if b['id'] in bstats]
kst = []
for b in BL:
    if 'search.brave.com' in b['url'] and b['id'] in bstats:
        term = b['title'].rsplit(' - Brave Search', 1)[0]
        kst.append((2, b['id'], term, term.lower()))
CH_SCHEMA = """
CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR);
CREATE TABLE urls(id INTEGER PRIMARY KEY AUTOINCREMENT,url LONGVARCHAR,title LONGVARCHAR,visit_count INTEGER DEFAULT 0 NOT NULL,typed_count INTEGER DEFAULT 0 NOT NULL,last_visit_time INTEGER NOT NULL,hidden INTEGER DEFAULT 0 NOT NULL);
CREATE TABLE visits(id INTEGER PRIMARY KEY AUTOINCREMENT,url INTEGER NOT NULL,visit_time INTEGER NOT NULL,from_visit INTEGER,external_referrer_url TEXT,transition INTEGER DEFAULT 0 NOT NULL,segment_id INTEGER,visit_duration INTEGER DEFAULT 0 NOT NULL,incremented_omnibox_typed_score BOOLEAN DEFAULT FALSE NOT NULL,opener_visit INTEGER,originator_cache_guid TEXT,originator_visit_id INTEGER,originator_from_visit INTEGER,originator_opener_visit INTEGER,is_known_to_sync BOOLEAN DEFAULT FALSE NOT NULL,consider_for_ntp_most_visited BOOLEAN DEFAULT FALSE NOT NULL,visited_link_id INTEGER DEFAULT 0 NOT NULL,app_id TEXT);
CREATE TABLE keyword_search_terms (keyword_id INTEGER NOT NULL,url_id INTEGER NOT NULL,term LONGVARCHAR NOT NULL,normalized_term LONGVARCHAR NOT NULL);
CREATE TABLE visit_source(id INTEGER PRIMARY KEY,source INTEGER NOT NULL);
CREATE INDEX urls_url_index ON urls (url);
CREATE INDEX visits_url_index ON visits (url);
CREATE INDEX visits_from_index ON visits (from_visit);
CREATE INDEX visits_time_index ON visits (visit_time);
CREATE INDEX keyword_search_terms_index1 ON keyword_search_terms (keyword_id, normalized_term);
CREATE INDEX keyword_search_terms_index2 ON keyword_search_terms (url_id);
"""
meta_rows = [('mmap_status', '-1'), ('version', '70'), ('last_compatible_version', '16'), ('early_expiration_threshold', str(webkit('2026-08-04 12:40')))]
BR_PIDS = sorted({x for b in BL for x in topic_pids(b['topic'])})
blast = max(v[2] for v in bvisits)
bl_dt = datetime.datetime.fromtimestamp(blast / 1e6 - 11644473600, UTC)
g.sqlite('brave/Default/History', CH_SCHEMA, {'meta': meta_rows, 'urls': urls, 'visits': bvisits, 'keyword_search_terms': kst},
         '2026-08-04 12:40', bl_dt + datetime.timedelta(seconds=30), account='Brave (Default profile)', project_ids=BR_PIDS,
         modeled_on='Chromium History sqlite (urls/visits schema as in authentic/browser-history/chrome/<profile>/History)',
         notes=f'HARD CASE: personal clutter mixed with work — Brave on the new Mac, {len(urls)} urls / {len(bvisits)} visits: app + landing-page testing with SF errands mixed in')
buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
w.writerow(['visit_time_local', 'url', 'title', 'transition_core'])
for v in bvisits:
    b = BL[v[1] - 1]
    d = datetime.datetime.fromtimestamp(v[2] / 1e6 - 11644473600, UTC)
    w.writerow([d.astimezone(PT if d >= MOVE else ET).strftime('%Y-%m-%d %H:%M:%S'), b['url'], b['title'], v[5] & 0xFF])
g.text('brave/Default/visits.csv', buf.getvalue(), bl_dt + datetime.timedelta(seconds=120), bl_dt + datetime.timedelta(seconds=120),
       account='Brave (Default profile)', project_ids=BR_PIDS, modeled_on='authentic/browser-history/<browser>/<profile>/visits.csv (derived flat export)',
       notes='HARD CASE: personal clutter mixed with work — flat CSV derived from Brave History')

print(f'firefox: {len(place_rows)} places, {len(visits)} visits, {len(origin_rows)} origins; brave: {len(urls)} urls, {len(bvisits)} visits')
print('firefox projects:', FF_PIDS); print('brave projects:', BR_PIDS)
g.finish()
