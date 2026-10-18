# PERSON — synthetic side of benchmark_001

Everything under `synthetic/` is generated from this page. Per David's schema-layer instruction (datasets.json: "synthetic data
about David on platforms he uses little or not at all"), the synthetic person **is David Barron**: his real projects, his real
collaborators and the real shape of his year, with *invented* items on top. Most of it goes on the platforms he doesn't use or
barely uses (Notion, OneNote, Evernote, Grok, Perplexity, Cursor, Google Meet, Granola, Zoom, Zotero, websites, a second Gmail
account). Some goes on the tools he does use (ChatGPT, Claude, Claude Code, Codex, Gmail, Drive, Slack, Linear, GitHub, Obsidian,
Apple Notes, PDFs, local files).

No synthetic item copies or paraphrases a real item. Real items were read only for style: formats, vocabulary, project types and
the mix of files. Events marked *(synthetic)* below never happened. They are plausible inventions that fit between the real ones.
Private matters from the authentic data (relationships, health, family conflict) are deliberately **not** used. Personal
clutter is generated from neutral themes only.

Reference date: **2026-10-17**. Synthetic items are dated 2025-10-17 → 2026-10-17. A few older items are allowed where the
format makes it natural (a 2024 Evernote recipe notebook, an old PDF).

---

## 1. Who

**David Barron**, 24. HCI PhD student in Computer Science at Virginia Tech, PRIME Lab, advised by **Dr. Yan Chen**. Since summer
2026 he has been on a leave of absence to co-found **Mathetic** (Mathetic PBC; earlier working names *Papert Lab*) with **Hudson
Mitchell-Pullman**. They are building **Engelbart**, a research notebook that remembers where a researcher's thoughts came from.
He did his undergrad at VT (graduated May 2024) and then stayed for grad school.

- Lived in **Blacksburg, VA** (America/New_York) until **2026-08-08**, then **San Francisco** (America/Los_Angeles) at the
  Surplus incubator house. Use the right time zone for each date.
- Writing voice: lowercase-heavy and fast in chats and Slack ("ok so", "wait", "lol", "can you just…"). He's careful and
  structured in paper drafts and emails to faculty. He leaves terse TODO-style personal notes. He pastes logs and stack traces
  into AI chats. He asks AI to "be concise" and to "not speculate".
- Habits: former competitive miler. Since 2025 he has been doing a multi-year aerobic base-building plan (Zone 2 running,
  cycling, elliptical; 8–11 h/week). He makes beats (FL Studio). He plays online chess. He reads geopolitics and grand strategy.

### Accounts
| account | what | real or synthetic usage |
|---|---|---|
| dbarron410@vt.edu | VT Google Workspace + Microsoft 365 (Outlook, OneNote), Claude, ChatGPT | real; OneNote use is **synthetic** |
| davidbarron410@gmail.com | personal Gmail, Drive, Gemini u/1 | real |
| **david.barron.runs@gmail.com** | *(synthetic)* second personal Gmail he opened in Dec 2025 for race sign-ups, Strava/Garmin, shopping and newsletters. Also used for his Evernote, Perplexity and Grok sign-ups | synthetic only |
| Mathetic Slack / Linear / GitHub org Mathetic-PBC | company tools | real; synthetic items added |
| Notion workspace "David's Notion" (personal, then shared "Mathetic HQ" teamspace with Hudson, Jan–Mar 2026) | *(synthetic)* tried for a company wiki and a reading list, then mostly abandoned in April 2026 | synthetic only |
| Evernote (david.barron.runs@gmail.com) | *(synthetic)* old habit from undergrad: recipes, gear lists, web clips, travel; trickles on | synthetic only |
| Perplexity (Pro trial Feb–Apr 2026) | *(synthetic)* literature search and quick facts | synthetic only |
| Grok (via X account @dbarron_runs) | *(synthetic)* news, geopolitics, training-science questions | synthetic only |
| Cursor | *(synthetic)* trial Nov 2025 – Jan 2026 on vizpi_frontend and Dynamite, then dropped in favour of Claude Code | synthetic only |
| Google Meet (vt.edu) | *(synthetic)* weekly advisor 1:1s and lab meetings recorded with transcripts + "Notes by Gemini" | synthetic only |
| Granola | *(synthetic)* his own Granola notes for investor, pilot-user and Berkeley research chats (Aug–Oct 2026). The real data only has the Mathetic shared links | synthetic additions |
| Zoom | *(synthetic)* occasional external calls (UIST AV check, a Berkeley chat, a recruiter) | synthetic additions |
| Zotero | *(synthetic)* his own "My Library" with collections per project (the real library is mostly a group mirror) | synthetic additions |

---

## 2. People

Real collaborators (names as they appear in the authentic data). Synthetic items only invent ordinary, non-sensitive work
exchanges with them.
- **Hudson Mitchell-Pullman**: co-founder (Mathetic, Engelbart). He is on Slack, Linear and Granola, and handles the landing page
  copy and fundraising with David.
- **Dr. Yan Chen**: PhD advisor (PRIME Lab, VT CS).
- **Minsun, Xiaohang, Rezky, Yue**: PRIME Lab collaborators on VizPI / TutorTrace / labeling infrastructure. Use first names
  only.
- **John Wenskovitch**: CS 3114 instructor; host of VizPI classroom deployments.

Invented people *(synthetic; use only these names for new outsiders)*:
- **Priya Raman**: PhD student at UC Berkeley (education + HCI). Pilot user of Engelbart and one of the Berkeley research chats.
- **Marcus Oyelaran**: angel investor (Northfield Angels). Two calls, Aug and Oct 2026.
- **Lena Hoffmann**: program lead at the Surplus incubator.
- **Tomás Reyes**: UIST 2026 session chair for David's talk.
- **Grace Kim**: VT CS graduate program coordinator (travel funding, leave paperwork).
- **Dr. Alan Brooks**: ISE 6664 (Affective Design & Computing) instructor, Spring 2026.
- **Owen Patel**: friend from the VT running club; running buddy and race partner.
- **Sam Whitaker**: housemate at the SF incubator house.
- **Niamh Barron**: cousin in Dublin. Family-logistics emails only.
- **Kevin Liu**: recruiter at a dev-tools company (unsolicited, unrelated).
- **Dr. Hannah Ostrowski**: author of the fictional paper used for the "same paper in several places" hard case (see §6).

---

## 3. Projects (ids = `ground_truth_projects.json`)

| id | synthetic coverage (what the generated items are about) |
|---|---|
| project_engelbart | onboarding/connect-screen ideas, import-dedupe design notes, pilot-session notes (Priya, two invented pilots), demo scripts, Cursor/Claude Code sessions on a canvas-render bug, Linear issues, Notion product page (Feb 2026, pre-Engelbart "Papert Lab notebook" idea) |
| project_mathetic_company | Marcus Oyelaran calls (Granola), Surplus logistics (Lena), Delaware PBC paperwork reminders, cap-table sheet (multi-tab), pitch-deck drafts, Notion "Mathetic HQ" wiki |
| project_berkeley_research_chats | Granola + Zoom notes of research chats, outreach email drafts, a sign-up sheet, Perplexity searches on interviewees' papers |
| project_claude_code_plugins | hc plugin notes, Codex/Claude Code sessions, a compaction-experiment log |
| project_tutortrace | UIST submission crunch (late Mar 2026), rebuttal (Jun), camera-ready (Aug), talk prep (Sep–Oct): Overleaf rebuttal project, Zotero collection, talk-script docs, Meet 1:1 transcripts with Yan, Perplexity/Grok lookups, AV-check Zoom |
| project_idetrace | NeurIPS D&B submission (May 2026), rebuttal (late Jul–Aug), leakage-bug notebook in OneNote, Codex sessions on the split script |
| project_vizpi | Fall 2025 CS 3114 deployment notes, Cursor sessions on vizpi_frontend, labeling-guide docs, lab-meeting transcripts |
| project_tacode | a couple of late-2025 handoff emails and one archived Notion page |
| project_sophia | one Evernote web clip + one ChatGPT chat revisiting Sophia for Educators (Nov 2025) |
| project_plotpact | one old Zotero item + a Grok chat about constraint-based creativity |
| project_dynamite | Cursor sessions + a Google Doc on discussion-clustering (Jan–Feb 2026) |
| project_ethicconvo | one email thread (Nov 2025) |
| project_juno | an Evernote note of old Juno ideas (2024) + a Notion "graveyard" page |
| project_clarityx | one Apple Note |
| project_ise6664_affective_computing | Spring 2026 course: OneNote class notebook, Zotero readings, project report docx, presentation pptx, emails with Dr. Brooks |
| project_cs3604_gta | Fall 2025 grading rubric sheet, attendance CSV, Canvas announcement drafts, Outlook threads |
| project_vt_phd_admin | leave-of-absence paperwork (Jun–Jul 2026), travel-funding forms (Sep 2026), Grace Kim emails, plan-of-study PDF |
| project_augmenting_cognition_reading_group | Notion reading list + Obsidian notes on Engelbart/Bush/Licklider, a few Perplexity threads |
| project_portfolio | a ChatGPT chat + browser history on portfolio redesign |
| project_endurance_training | training logs (Evernote, Apple Notes, Grok chats, Google Sheet with tabs), race emails in the runs@ account, Strava exports |
| project_music_production | beat ideas notes, sample-pack receipts, FL Studio project zip |
| **project_hint_timing_study** *(synthetic only)* | "When should the hint appear?": a small pilot David scoped in Feb 2026 on when AI hints should be offered in CS1 labs. **Exists only in Notion** (a database of 6 pages). Hard case "project in only one tool" |
| project_none | personal clutter, newsletters, receipts, apartment search, taxes, chess, geopolitics, one-off questions |

---

## 4. Timeline and bursts

Synthetic dates follow this calendar. Weights are relative activity per week (1 = normal). Generators sample dates with
`synthlib.bursty_dates()`, which uses exactly these weights. Inside each week, activity skews toward late nights and Sun–Wed.

| week of | weight | what is going on |
|---|---|---|
| 2025-10-20 | 1.0 | Fall semester; CS 3604 GTA; VizPI deployment in CS 3114 |
| 2025-11-03 | 1.8 | VizPI deployment week 2 and labeling; starts Cursor trial |
| 2025-11-10 | 2.5 | **heavy**: deployment data dump, labeling sprint, EthicConvo/TACode handoffs |
| 2025-12-08 | 2.2 | **heavy**: finals grading for CS 3604 |
| 2025-12-22 → 2026-01-04 | 0.2 | **quiet**: holidays |
| 2026-01-12 | 1.4 | Spring starts; ISE 6664; Dynamite clustering |
| 2026-01-26 | 2.0 | **heavy**: Notion experiment begins, Papert Lab idea, Dynamite |
| 2026-02-09 | 1.6 | hint-timing pilot scoping (Notion only), Perplexity trial |
| 2026-02-16 | 0.3 | **quiet** |
| 2026-03-23 | 2.6 | **heavy**: UIST paper crunch |
| 2026-03-30 | 3.0 | **heavy**: UIST deadline week |
| 2026-04-06 | 0.4 | quiet after deadline |
| 2026-04-27 | 1.8 | ISE 6664 final project |
| 2026-05-04 | 2.8 | **heavy**: NeurIPS D&B submission |
| 2026-05-18 → 2026-05-31 | 0.3 | **quiet** |
| 2026-06-15 | 2.4 | **heavy**: UIST rebuttal; leave-of-absence talk with Yan |
| 2026-06-29 → 2026-07-05 | 0.2 | **quiet** |
| 2026-07-27 | 2.4 | **heavy**: NeurIPS rebuttal; leave paperwork |
| 2026-08-03 | 2.0 | move to SF (2026-08-08); new Mac (2026-08-04) |
| 2026-08-10 | 2.6 | **heavy**: UIST camera-ready; Surplus onboarding; claude-plugins |
| 2026-08-24 | 2.2 | Engelbart repos start; Berkeley research site |
| 2026-09-07 | 2.6 | **heavy**: Berkeley research chats; Engelbart canvas |
| 2026-09-21 | 1.8 | UIST talk prep; travel funding |
| 2026-10-05 | 3.0 | **heavy**: UIST talk; pilot onboarding sessions; investor call 2 |
| 2026-10-12 | 2.4 | onboarding/import redesign (the reason this benchmark exists) |
| any other week | 0.8 | background |

Fixed synthetic events (use these dates when an item is about them):
- 2025-11-12: VizPI CS 3114 deployment #2 (lab session 3:30 pm ET).
- 2025-12-15: CS 3604 final grades due.
- 2026-01-28: first "Papert Lab notebook" Notion page (shared with Hudson 2026-02-02).
- 2026-02-11: hint-timing pilot kickoff (Notion only).
- 2026-03-31 23:59 AoE: UIST 2026 paper deadline (TutorTrace).
- 2026-04-30: ISE 6664 final presentation.
- 2026-05-06: NeurIPS 2026 Datasets & Benchmarks deadline (IDETrace).
- 2026-06-18: UIST rebuttal due. 2026-06-22: leave-of-absence 1:1 with Yan (Meet transcript).
- 2026-07-29: NeurIPS rebuttal posted. 2026-07-31: leave-of-absence form signed (Grace Kim).
- 2026-08-08: arrives in SF. 2026-08-11: Surplus kickoff with Lena.
- 2026-08-14: UIST camera-ready due.
- 2026-08-20: first call with Marcus Oyelaran (Granola).
- 2026-09-09, 09-10, 09-16: Berkeley research chats (one with Priya Raman, 09-10).
- 2026-09-24: VT travel-funding request submitted.
- 2026-10-02: Zoom AV check with Tomás Reyes. 2026-10-07: UIST talk (TutorTrace).
- 2026-10-09 and 2026-10-13: Engelbart pilot onboarding sessions (Priya; "pilot B" Daniel Osei *(synthetic)*).
- 2026-10-14: second call with Marcus Oyelaran.
- 2026-10-15: Bay Area half marathon *(synthetic)* with Owen Patel (results email in the runs@ account).

---

## 5. Unrelated / personal themes (project_none or endurance/music)
SF apartment and sublet search (Jul–Aug 2026), moving checklist, car insurance and registration, 2025 taxes (Mar–Apr 2026),
subscriptions and receipts, recipes and meal prep, online chess, a cousin's wedding RSVP in Dublin (Niamh, summer 2026,
logistics only), geopolitics reading (US–China, grand strategy), newsletters (Stratechery-like, running magazines), dev-tools
recruiter spam, a broken bike derailleur, VT parking ticket appeal, laptop setup notes (new Mac 2026-08-04).

---

## 6. Hard cases (each one is noted in its folder's MANIFEST.csv with `HARD CASE: <kind>`)
| kind | where |
|---|---|
| vague titles ("Notes", "Untitled", "Doc1", "New Recording", "asdf") | notion, onenote, evernote, google-docs, apple-notes, local-notes, chatgpt, perplexity |
| near-duplicates (v2 / "copy of" / exported twice, a few lines changed) | google-docs, local-notes, evernote (single-note and whole-notebook ENEX), overleaf, pdfs |
| same paper in several places: Ostrowski et al. 2025, *"Productive Struggle or Silent Stalling? Telemetry Signals of Help-Seeking in LLM-Assisted CS1"* (fictional) | zotero (PDF + BibTeX), pdfs (~/Downloads and ~/Desktop/papers), gmail attachment, google-docs, overleaf .bib entry, slack file share |
| relevant passage buried in a long unrelated chat | chatgpt (long meal-prep chat with an IDETrace leakage insight), grok (long geopolitics thread with an Engelbart import idea), claude |
| personal clutter | evernote, apple-notes, gmail runs@ account, local-files, browser-history |
| project that exists in only one tool | notion (project_hint_timing_study) |
| chats inside projects | chatgpt (project "TutorTrace UIST"), claude (project "Engelbart onboarding") |
| second email account | gmail/david.barron.runs@gmail.com |
| multi-tab sheet | google-docs (cap table; training log; CS 3604 grades) |
| email with attachments | gmail, outlook |
| zip archive of files | local-files (FL Studio project zip; UIST talk assets zip), google-docs (zip in Drive) |
| automated-looking coding sessions that hold real work | claude-code, codex (`-p` / headless style, but the edits are real fixes) |

---

## 7. Shared story facts (all synthetic; use these so tools agree with each other)
- **VizPI deployment #2 (2025-11-12, CS 3114):** 87 students, 3 TAs, two lab sections. A websocket reconnect bug dropped ~12% of
  telemetry events in section B until a hotfix at 4:10 pm. Labeling sprint 11-14 → 11-21 with Minsun and Xiaohang: 2,340
  thirty-second windows. Labeling guide v3 added a "stalled-after-error" state.
- **CS 3604 (Fall 2025):** David grades P3 and P4 and the final project. Rubric in a sheet with one tab per assignment. 64 students.
  Final grades due 2025-12-15. One regrade dispute about P4 (late-day policy).
- **Cursor trial (2025-11-05 → 2026-01-20):** used on vizpi_frontend (replay timeline component, reconnect handling) and Dynamite
  (embedding + HDBSCAN clustering of discussion posts). Dropped because "agent kept rewriting files I didn't ask about".
- **Dynamite (Jan–Feb 2026):** clustering 3,100 discussion posts from a virtual class forum. HDBSCAN min_cluster_size=15.
  The labels for 41 clusters were generated by an LLM and checked by hand.
- **ISE 6664 project (Spring 2026, Dr. Alan Brooks):** "Frustration signals in AI-tutoring transcripts". Team: David + two
  classmates *(synthetic)* **Maya Torres** and **Jordan Lee**. Final presentation 2026-04-30. Report 14 pages.
- **TutorTrace UIST 2026:** submitted 2026-03-31. Reviews (2026-06-11) asked about label reliability (kappa 0.71 across 3
  raters), generalization beyond one course, and the privacy of telemetry. The rebuttal (2026-06-18) promised a cross-course
  analysis and a limitations section. Conditionally accepted 2026-07-02. Camera-ready 2026-08-14. Talk 2026-10-07 (15 min + 5 Q&A),
  in session "Learning & Tutoring", chair Tomás Reyes.
- **IDETrace NeurIPS 2026 D&B:** submitted 2026-05-06. Leakage bug found 2026-07-24: windows from the same student were in both
  train and test. Fixed with a split grouped by student id. Macro-F1 went 0.81 → 0.74 and the rebuttal (posted 2026-07-29) reports
  both numbers. Decision pending as of the reference date.
- **Leave of absence:** discussed with Yan 2026-06-22. Form signed 2026-07-31 (Grace Kim). Effective Fall 2026. GRA funding ends
  2026-08-15.
- **Mathetic / Engelbart:** Surplus kickoff 2026-08-11 (Lena Hoffmann). First Marcus Oyelaran call 2026-08-20: he asked about
  retention and "who pays". Second call 2026-10-14: interested in a $50k check into the pre-seed SAFE if pilots convert. Delaware
  PBC annual report reminder due 2027-03-01.
- **Engelbart pilots:** Priya Raman (2026-10-09): import missed ~140 of her Claude chats, showed duplicate PDFs (same paper from
  Zotero and Downloads), and she liked the "where did this thought come from" trail. Daniel Osei *(synthetic; postdoc, CMU)*
  (2026-10-13): wanted Notion and Granola import and was confused by the connect screen's "Other" category.
- **Berkeley research chats:** 2026-09-09 (a learning-sciences PhD student, *synthetic* **Elena Park**), 2026-09-10 (Priya
  Raman), 2026-09-16 (a statistics postdoc, *synthetic* **Ben Adeyemi**, on Zoom).
- **Half marathon 2026-10-15:** David 1:24:51, Owen Patel 1:22:10. Training plan "Block 4" (Aug–Oct 2026), 9–11 h/week.
- **Hint-timing pilot (Notion only, Feb 2026):** never mentioned anywhere else.
