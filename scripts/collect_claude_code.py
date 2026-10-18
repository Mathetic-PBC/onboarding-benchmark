import os, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, copy, mtime, ROOT

H = os.path.expanduser('~')
m = Manifest('authentic', 'claude-code')
dest = m.dir
EXCLUDE = '-Users-divadbaroon-Desktop-benchmark'  # this collection run itself


def first_ts(p):
    try:
        with open(p, errors='replace') as f:
            for i, line in enumerate(f):
                if i > 200: break
                try:
                    t = json.loads(line).get('timestamp')
                    if t: return t
                except Exception: pass
    except Exception: pass
    return ''

# 1. ~/.claude/projects (native Claude Code transcripts)
src = f'{H}/.claude/projects'
for proj in sorted(os.listdir(src)):
    if proj == EXCLUDE: continue
    sp = os.path.join(src, proj)
    if not os.path.isdir(sp): continue
    copy(sp, os.path.join(dest, 'projects', proj))
for p in glob.glob(f'{dest}/projects/**/*', recursive=True):
    if os.path.isfile(p) and not p.endswith('.DS_Store'):
        rel = os.path.relpath(p, dest)
        kind = 'subagent transcript' if '/subagents/' in rel else ('session transcript' if p.endswith('.jsonl') else 'session attachment/tool-result')
        start = first_ts(p) if p.endswith('.jsonl') else ''
        m.add(rel, 'Claude Code', '~/.claude/projects (CLI, local)', start or mtime(p), source='~/' + os.path.relpath(p.replace(dest + '/projects', f'{H}/.claude/projects'), H),
              notes=f'{kind}; mtime={mtime(p)}')

# 2. prompt history + plans
for name in ['history.jsonl', 'plans']:
    s = f'{H}/.claude/{name}'
    copy(s, os.path.join(dest, 'claude-home', name))
for p in glob.glob(f'{dest}/claude-home/**/*', recursive=True):
    if os.path.isfile(p):
        m.add(os.path.relpath(p, dest), 'Claude Code', '~/.claude', mtime(p), source='~/.claude/' + os.path.relpath(p, f'{dest}/claude-home'),
              notes='prompt history across all sessions' if p.endswith('history.jsonl') else 'saved plan')

# 3. Claude desktop app: Code tab session metadata (transcripts themselves live in ~/.claude/projects)
s = f'{H}/Library/Application Support/Claude/claude-code-sessions'
copy(s, os.path.join(dest, 'claude-desktop-code-sessions'))
for p in glob.glob(f'{dest}/claude-desktop-code-sessions/**/*', recursive=True):
    if os.path.isfile(p):
        m.add(os.path.relpath(p, dest), 'Claude Code (Claude desktop app)', 'Claude desktop app', mtime(p), source='~/Library/Application Support/Claude/claude-code-sessions',
              notes='desktop Code-tab session metadata; transcript is the matching cliSessionId under projects/')

# 4. claude-vault: the person's own tool's derived indexes of Claude Code sessions (+ older backups/resets)
vaults = [(f'{H}/.claude-vault', 'claude-vault')] + [(d + '/.claude-vault', 'vault-backups/' + os.path.basename(d)) for d in sorted(glob.glob(f'{H}/vault-reset-*')) if os.path.isdir(d + '/.claude-vault')] \
    + [(f'{H}/.claude-vault.bak-20260813-032937', 'vault-backups/claude-vault.bak-20260813-032937')]
for s, name in vaults:
    for sub in ['chat-sessions', 'sessions', 'trajectory']:
        if os.path.isdir(f'{s}/{sub}'):
            copy(f'{s}/{sub}', f'{dest}/derived/{name}/{sub}')
for p in glob.glob(f'{dest}/derived/**/*', recursive=True):
    if os.path.isfile(p) and not p.endswith('.DS_Store'):
        rel = os.path.relpath(p, dest)
        m.add(rel, 'Claude Code (derived by claude-vault)', 'claude-vault (person-built tool)', first_ts(p) if p.endswith('.jsonl') else mtime(p),
              source='~/' + rel.replace('derived/claude-vault', '.claude-vault').replace('derived/vault-backups/', ''),
              notes='HARD CASE: derived/duplicate index of Claude Code transcripts built by the person\'s claude-vault tool; not an original chat; mtime=' + mtime(p))
print(m.save())
