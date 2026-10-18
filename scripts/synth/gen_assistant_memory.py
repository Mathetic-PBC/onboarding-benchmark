"""Synthetic assistant memory / profile items (profile-level: one file = one item), consistent with PERSON.md and the
synthetic chats in chatgpt / claude / grok / perplexity / gemini.

Layout (synthetic/assistant-memory/):
  chatgpt/memories_synthetic.json            ChatGPT saved memories (backend-api/memories shape)
  chatgpt/user_system_messages_synthetic.json ChatGPT custom instructions (backend-api/user_system_messages shape)
  claude/memory_synthetic.json               claude.ai memory (organizations/<org>/memory shape)
  claude/account_profile_synthetic.json      claude.ai personal preferences (account_profile shape)
  grok/memories.json                         Grok "Personalize → Memory" list
  grok/personalization.json                  Grok custom instructions
  perplexity/profile.json                    Perplexity "Introduce yourself" profile + location + response language
  gemini/saved_info.json                     Gemini Saved info (u/1 personal account; u/0 Workspace has no page)
"""
import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import *
import gen_chatgpt as gc  # only to link ChatGPT memories to the synthetic ChatGPT conversation ids (no side effects)

g = Gen('assistant-memory')

# ---- ChatGPT conversation ids by slug (same derivation as gen_chatgpt.py)
CIDS = {}
for f in sorted(glob.glob(os.path.join(gc.CONTENT, 'chatgpt', '*.txt'))):
    for c in gc.parse_chats(f):
        first, _ = gc.timeline(c, gc.SEED)
        CIDS[c['slug']] = gc.conv_id(first, c['slug'])

# ---------------------------------------------------------------- 1. ChatGPT memories
# (content, updated_at date, created local time, source chat slug or None, projects)
MEM = [
    ("Is an HCI PhD student in Computer Science at Virginia Tech (PRIME Lab), advised by Dr. Yan Chen.", '2025-10-27 18:44', None, []),
    ("Is a GTA for CS 3604 (Professionalism in Computing) in Fall 2025; grades P3, P4 and the final project for 64 students; final grades due 2025-12-15.",
     '2025-10-27 18:44', 'cs3604-rubric-p3', ['project_cs3604_gta']),
    ("Prefers concise answers, wants uncertainty flagged instead of speculation, and doesn't want numbers made up.", '2025-11-12 16:20', None, []),
    ("Ran VizPI deployment #2 in CS 3114 on 2025-11-12 (87 students, two lab sections). A socket.io reconnect bug dropped about 12% of section B telemetry before a 4:10 pm hotfix; affected 30-second windows are flagged possibly_incomplete.",
     '2025-11-12 16:40', 'vizpi-ws-reconnect', ['project_vizpi']),
    ("Labeling guide v3 (VizPI/TutorTrace) splits the old 'stuck' label into 'stuck' and 'stalled-after-error'; labels with Minsun and Xiaohang.",
     '2025-11-17 22:50', 'vizpi-label-agreement', ['project_vizpi', 'project_tutortrace']),
    ("Archived Sophia for Educators in Nov 2025; the instructor dashboard of student questions was the part instructors liked.",
     '2025-11-19 20:30', 'sophia-educators-revisit', ['project_sophia']),
    ("Is doing multi-year aerobic base building (Zone 2 running, cycling, elliptical), about 8–11 hours per week; Zone 2 HR cap is around 148; weighs about 66 kg.",
     '2025-12-02 21:50', 'zone2-cardiac-drift', ['project_endurance_training']),
    ("Dynamite: clusters ~3,100 forum discussion posts with mpnet embeddings, UMAP and HDBSCAN (min_cluster_size=15, min_samples=5): 41 clusters, LLM-labeled and hand-checked.",
     '2026-01-21 23:40', 'dynamite-hdbscan', ['project_dynamite']),
    ("Plays online chess (~1650 rapid); switched from the Najdorf to the Kan Sicilian as Black.", '2026-01-31 00:50', 'chess-untitled', []),
    ("Is taking ISE 6664 (Affective Design & Computing) with Dr. Alan Brooks in Spring 2026; team project 'Frustration signals in AI-tutoring transcripts' with Maya Torres and Jordan Lee.",
     '2026-02-03 21:35', 'ise6664-appraisal', ['project_ise6664_affective_computing']),
    ("Cancelled Cursor Pro, Notion Plus and Chess.com Diamond in Feb 2026; stopped using Cursor in January and uses Claude Code instead.",
     '2026-02-22 20:55', 'subscriptions-audit', []),
    ("TutorTrace (UIST 2026) reports Light's kappa = 0.71 across three raters, computed before adjudication; stalled-after-error F1 = 0.68.",
     '2026-03-29 01:30', 'tt-kappa-reporting', ['project_tutortrace']),
    ("Submitted IDETrace to the NeurIPS 2026 Datasets & Benchmarks track (deadline 2026-05-06).", '2026-05-04 00:20', 'idetrace-datasheet', ['project_idetrace']),
    ("Is taking a leave of absence from the PhD starting Fall 2026 to co-found Mathetic (Mathetic PBC) with Hudson Mitchell-Pullman; the paperwork goes through Grace Kim.",
     '2026-06-20 21:45', 'leave-email-yan', ['project_vt_phd_admin', 'project_mathetic_company']),
    ("Found a leakage bug in IDETrace on 2026-07-24: windows from the same student were in train and test. Re-split by student id (StratifiedGroupKFold); macro-F1 went from 0.81 to 0.74, and the GRU now beats the transformer (0.71 vs 0.70).",
     '2026-07-27 22:30', 'idetrace-rebuttal-numbers', ['project_idetrace']),
    ("Moved from Blacksburg, VA to San Francisco on 2026-08-08 and lives at the Surplus incubator house; sold his car before moving.",
     '2026-07-30 23:30', 'moving-checklist-sf', []),
    ("Got a new MacBook on 2026-08-04; uses zsh, VS Code, Claude Code, uv and fnm.", '2026-08-04 21:55', 'new-mac-setup', []),
    ("Mathetic is building Engelbart, a research notebook that remembers where a researcher's thoughts came from. It imports AI chats, papers and notes and keeps provenance. Preferred headline: 'Remember where your thinking came from.'",
     '2026-08-27 23:45', 'engelbart-landing-copy', ['project_engelbart', 'project_mathetic_company']),
    ("Had a first call with angel investor Marcus Oyelaran (Northfield Angels) on 2026-08-20; pricing hypothesis to float is $15/month individual, with lab bundles later.",
     '2026-08-19 22:40', 'marcus-call-prep', ['project_mathetic_company', 'project_engelbart']),
    ("Is doing research chats with Berkeley PhD students and postdocs (Sep 2026) about how researchers keep track of their thinking; doesn't mention Engelbart in outreach emails.",
     '2026-08-31 22:00', 'berkeley-outreach-email', ['project_berkeley_research_chats']),
    ("Mathetic PBC's first Delaware annual report and franchise tax are due 2027-03-01.", '2026-08-18 21:25', 'pbc-annual-report', ['project_mathetic_company']),
    ("Presents TutorTrace at UIST 2026 on 2026-10-07 in the 'Learning & Tutoring' session (15 min + 5 min Q&A; session chair Tomás Reyes).",
     '2026-09-22 21:30', 'tt-talk-outline', ['project_tutortrace']),
    ("Makes beats in FL Studio (boom bap, soul chops, 808s).", '2026-05-25 00:00', 'beats-soul-chop', ['project_music_production']),
    ("Ran the Bay Area half marathon on 2026-10-15 in 1:24:51 (goal was sub-1:25); training partner Owen Patel ran 1:22:10.",
     '2026-10-15 20:40', 'half-fueling', ['project_endurance_training']),
]
mems, projs = [], set()
for i, (content, when, slug, ps) in enumerate(MEM):
    d = dt(when)
    mems.append({'id': uid(('cgpt-mem', i)), 'content': content, 'updated_at': d.date().isoformat(), 'gizmo_id': None, 'status': 'warm',
                 'conversation_id': CIDS[slug] if slug else None, 'created_timestamp': d.timestamp(), 'last_updated': None, 'labels': []})
    projs |= set(ps)
mems.reverse()  # newest first, as the API returns them
g.json('chatgpt/memories_synthetic.json', {'memories': mems, 'memory_max_tokens': 10000, 'memory_num_tokens': sum(len(m['content']) for m in mems) // 4},
       created='2025-10-27 18:44', modified='2026-10-15 20:40', account='dbarron410@vt.edu (ChatGPT personal workspace)',
       project_ids=sorted(projs), modeled_on='authentic/assistant-memory/chatgpt/memories.json shape (backend-api/memories)',
       notes=f'saved memories ({len(mems)} entries) spanning the synthetic ChatGPT chats; profile-level item')

# ---------------------------------------------------------------- 2. ChatGPT custom instructions
g.json('chatgpt/user_system_messages_synthetic.json', {
    'object': 'user_system_message_detail',
    'about_user_message': "HCI PhD student at Virginia Tech (PRIME Lab), on leave since Fall 2026 to co-found Mathetic (we build Engelbart, a research "
                          "notebook). I paste logs, code and paper drafts. I train for running (Zone 2 base, half marathons).",
    'about_model_message': "Be concise. Don't speculate; if you're not sure, say so. Never invent numbers or citations. For paper prose: academic, not hedgy, "
                           "no buzzwords. For code: give the fix first, then the explanation.",
    'name_user_message': 'David', 'role_user_message': 'PhD student / founder', 'traits_model_message': 'Direct. Short paragraphs. No emojis.',
    'other_user_message': '', 'personality_type_selection': 'default', 'disabled_tools': [], 'enabled': True, 'traits_enabled': True, 'personality_traits': {}},
    created='2025-11-12 16:25', modified='2026-08-06 22:10', account='dbarron410@vt.edu (ChatGPT personal workspace)',
    project_ids=['project_mathetic_company', 'project_engelbart', 'project_endurance_training'],
    modeled_on='authentic/assistant-memory/chatgpt/user_system_messages.json shape', notes='custom instructions (Customize ChatGPT); updated after the leave began')

# ---------------------------------------------------------------- 3. Claude memory
CLAUDE_MEM = """**Work context**

David is an HCI PhD student in Computer Science at Virginia Tech (PRIME Lab, advised by Dr. Yan Chen), on a leave of absence since Fall 2026 to co-found Mathetic PBC with Hudson Mitchell-Pullman. Mathetic is building Engelbart, a research notebook that remembers where a researcher's thoughts came from: it imports AI chats (Claude, ChatGPT), papers (Zotero, PDFs), notes and email, and keeps a provenance trail from each idea back to its sources. The company is in the Surplus incubator in San Francisco (program lead Lena Hoffmann). David designs the onboarding and import flow; Hudson handles landing-page copy and fundraising with him.

His research centers on instructor-facing telemetry in CS education: TutorTrace (UIST 2026, presented 2026-10-07), IDETrace (NeurIPS 2026 Datasets & Benchmarks, decision pending), and VizPI (classroom deployments in CS 3114). He also builds Claude Code plugins (the "hc" plugin) and uses Claude Code as his main coding tool after dropping Cursor in January 2026.

**Personal context**

He moved from Blacksburg, VA to San Francisco on 2026-08-08 and lives at the incubator house. He runs (former miler, now multi-year Zone 2 base building, 9–11 h/week in the current "Block 4") and ran a half marathon on 2026-10-15 in 1:24:51 with his friend Owen Patel. He makes beats in FL Studio, plays online chess, and reads geopolitics and grand strategy. He prefers concise answers without speculation and often pastes logs and drafts directly.

**Top of mind**

- Engelbart onboarding/import redesign after the two pilot onboarding sessions: Priya Raman (2026-10-09; import missed about 140 of her Claude chats, duplicate PDFs from Zotero and Downloads, liked the "where did this thought come from" trail) and Daniel Osei (2026-10-13; wants Notion and Granola import, was confused by the connect screen's "Other" category).
- Import dedupe rules: same work from several sources should become one item with several provenance pointers, with v1/camera-ready treated as versions.
- Follow-up with angel investor Marcus Oyelaran after the 2026-10-14 call (interested in a $50k check into the pre-seed SAFE if pilots convert).

**Brief history**

*Recent months*

- UIST 2026 camera-ready for TutorTrace (2026-08-14) and the talk on 2026-10-07; NeurIPS rebuttal for IDETrace posted 2026-07-29 after fixing a student-level leakage bug (macro-F1 0.81 → 0.74 under a student-grouped split).
- Berkeley research chats in September 2026 (Elena Park 09-09, Priya Raman 09-10, Ben Adeyemi 09-16) about how researchers keep track of their thinking.
- Started the Engelbart repos and canvas in late August 2026.

*Earlier context*

- Spring 2026: ISE 6664 (Affective Design & Computing, Dr. Alan Brooks) team project on frustration signals in AI-tutoring transcripts (presentation 2026-04-30); UIST submission 2026-03-31.
- Fall 2025: GTA for CS 3604; VizPI deployment #2 on 2025-11-12 and the labeling sprint that produced guide v3 with a "stalled-after-error" state.
"""
g.json('claude/memory_synthetic.json', {'memory': CLAUDE_MEM, 'controls': [], 'updated_at': iso('2026-10-16 23:12', z=True).replace('Z', '+00:00'),
                                        'project_import': None, 'project_memory_mode': None},
       created='2025-11-20 09:00', modified='2026-10-16 23:12', account='claude.ai — dbarron410@vt.edu',
       project_ids=['project_engelbart', 'project_mathetic_company', 'project_tutortrace', 'project_idetrace', 'project_vizpi',
                    'project_claude_code_plugins', 'project_berkeley_research_chats', 'project_ise6664_affective_computing',
                    'project_cs3604_gta', 'project_vt_phd_admin', 'project_endurance_training', 'project_music_production'],
       modeled_on='authentic/assistant-memory/claude/memory.json shape (organizations/<org>/memory)',
       notes='memory synthesized by Claude from the synthetic Claude chats; profile-level item')

g.json('claude/account_profile_synthetic.json', {
    'work_function': 'Research', 'conversation_preferences':
        "Be concise. Don't speculate. If something depends on a fact you don't have (a number, a date, a file), ask instead of guessing. "
        "When I paste a stack trace, give the fix first. For writing, keep my voice: plain, specific, no hype words.",
    'cowork_global_instructions': None, 'cowork_instructions_union': True, 'conversation_preferences_cloud_max_chars': 32768,
    'conversation_preferences_over_cloud_max_chars': False, 'locale': 'en-US', 'onboarding_topics': None, 'science_fields': ['Computer science'],
    'avatar': None, 'pixel_avatar': None, 'avatar_image_url': None, 'display_avatar': None},
    created='2025-11-20 09:00', modified='2026-08-12 10:30', account='claude.ai — dbarron410@vt.edu', project_ids=['project_none'],
    modeled_on='authentic/assistant-memory/claude/account_profile.json shape', notes='personal preferences (custom instructions); generic, mentions no project')

# ---------------------------------------------------------------- 4. Grok memory + personalization
GROK = [
    ('2026-02-05 22:14', "Follows US–China relations, chip export controls and grand strategy (Mackinder, Spykman, Mearsheimer)."),
    ('2026-02-12 07:40', "Is a former competitive miler doing multi-year aerobic base building: Zone 2 running plus cycling and elliptical."),
    ('2026-03-02 21:05', "Wants sources for news claims and prefers X posts from primary accounts over aggregators."),
    ('2026-05-24 23:58', "Makes boom bap beats in FL Studio and asked about sample clearance before uploading to SoundCloud."),
    ('2026-06-08 22:30', "Is interested in constraint-based creativity (PlotPact: writing prompts with rules)."),
    ('2026-08-02 20:10', "Training block 'Block 4' (Aug–Oct 2026): 9–11 hours/week, building to a half marathon on Oct 15."),
    ('2026-08-09 19:00', "Lives in San Francisco since August 2026."),
    ('2026-09-27 21:40', "Is giving a 15-minute UIST talk on TutorTrace on Oct 7, 2026."),
    ('2026-10-12 00:30', "Is working on Engelbart's import: deduplicating the same paper found in Zotero and Downloads while keeping both provenance pointers."),
    ('2026-10-16 18:20', "Ran the half marathon in 1:24:51 on Oct 15, 2026."),
]
g.json('grok/memories.json', {'memories': [{'memoryId': uid(('grok-mem', i)), 'text': t, 'createTime': iso(d, z=True), 'source': 'conversation'}
                                          for i, (d, t) in enumerate(GROK)][::-1],
                              'memoryEnabled': True, 'referencePastConversations': True},
       created='2026-02-05 22:14', modified='2026-10-16 18:20', account='david.barron.runs@gmail.com (Grok via X @dbarron_runs)',
       project_ids=['project_none', 'project_endurance_training', 'project_music_production', 'project_plotpact', 'project_tutortrace', 'project_engelbart'],
       modeled_on='', notes='Grok "Personalize → Memory" list (no real Grok data; documented settings shape); profile-level item')
g.json('grok/personalization.json', {
    'customInstructions': "Keep answers short unless I ask for depth. For news and geopolitics, cite sources and say when something is unconfirmed. "
                          "For training questions assume I'm an experienced runner, ~66 kg, 9–11 h/week.",
    'responseStyle': 'concise', 'language': 'en', 'updateTime': iso('2026-08-02 20:12', z=True)},
    created='2026-02-05 22:20', modified='2026-08-02 20:12', account='david.barron.runs@gmail.com (Grok via X @dbarron_runs)',
    project_ids=['project_endurance_training', 'project_none'], modeled_on='', notes='Grok custom instructions')

# ---------------------------------------------------------------- 5. Perplexity profile
g.json('perplexity/profile.json', {
    'user': {'email': 'david.barron.runs@gmail.com', 'username': 'dbarron_runs', 'subscription_status': 'none',
             'subscription_history': [{'plan': 'pro_trial', 'start': '2026-02-09', 'end': '2026-04-30'}]},
    'personalization': {
        'introduce_yourself': "I'm an HCI PhD student (Virginia Tech, on leave) working on tools for computing education: TutorTrace (UIST 2026) and the "
                              "IDETrace dataset (NeurIPS D&B). Now co-founding a startup building a research notebook. I mostly use Perplexity for related "
                              "work and quick facts. Prefer peer-reviewed sources (ACM DL, arXiv) over blogs. I also train for half marathons.",
        'location': 'San Francisco, CA', 'location_updated_at': '2026-08-09', 'previous_location': 'Blacksburg, VA',
        'response_language': 'English', 'ai_data_retention': True},
    'spaces': ['UIST related work', 'Berkeley chats prep', 'Training']},
    created='2025-12-16 21:00', modified='2026-08-09 11:15', account='david.barron.runs@gmail.com (Perplexity)',
    project_ids=['project_tutortrace', 'project_idetrace', 'project_mathetic_company', 'project_endurance_training', 'project_berkeley_research_chats'],
    modeled_on='', notes='Perplexity profile ("Introduce yourself" + location + response language); no real Perplexity data')

# ---------------------------------------------------------------- 6. Gemini saved info
SAVED = [
    ('2025-11-25', "My training log is a Google Sheet with tabs per week; columns are Date, Activity (Run/Bike/Elliptical), Minutes, Avg HR, Distance."),
    ('2026-01-07', "Zone 2 for me is roughly 138–148 bpm."),
    ('2026-05-25', "I'm travelling to Dublin in summer 2026 for my cousin Niamh's wedding; I'm vegetarian-flexible and prefer public transport."),
    ('2026-09-21', "For VT travel funding, my advisor is Dr. Yan Chen and the coordinator is Grace Kim."),
]
g.json('gemini/saved_info.json', {
    'tool': 'gemini', 'read_at': '2026-10-17',
    'accounts': {
        'davidbarron410@gmail.com': {'saved_info_page': 'https://gemini.google.com/u/1/saved-info',
                                     'saved_info': [{'id': 'si_' + hexid(('gem-si', i), 16), 'text': t, 'created': d} for i, (d, t) in enumerate(SAVED)],
                                     'custom_instructions': None, 'custom_gems': []},
        'dbarron410@vt.edu': {'saved_info_page': 'https://gemini.google.com/u/0/saved-info', 'saved_info': None,
                              'page_text': 'Saved info is not available for this Workspace account', 'custom_instructions': None, 'custom_gems': []}}},
    created='2025-11-25 20:00', modified='2026-09-21 22:05', account='davidbarron410@gmail.com; dbarron410@vt.edu',
    project_ids=['project_endurance_training', 'project_vt_phd_admin', 'project_none'],
    modeled_on='authentic/assistant-memory/gemini/saved_info.json shape (with entries instead of the real empty state)',
    notes='Gemini Saved info: 4 entries on the personal account; Workspace account has no Saved info page')

g.finish()
