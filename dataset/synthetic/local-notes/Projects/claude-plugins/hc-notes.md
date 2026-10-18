# hc plugin notes

hc = "human compact": a compaction hook that asks me (or a rule file) what must survive before Claude Code compacts.

- 0.5.0 (8/17): naive summary. lost the file list twice. bad
- 0.11.0 (8/21): keep a pinned TODO block + failing test names verbatim. task success 2/2
- 0.13.0 (8/25): "focus hint" — one line I write about what I'm doing. helps a lot
- 0.13.1 (8/27): dropped an env var detail (E2B key name). add "keep env var names" to rules
- next: measure tokens after compaction vs success over 10 runs, not 6
- compact-focus as a separate tiny plugin? Hudson thinks yes
