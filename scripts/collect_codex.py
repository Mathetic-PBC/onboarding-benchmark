import os, sys, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, copy, mtime

H = os.path.expanduser('~')
m = Manifest('authentic', 'codex')
d = m.dir
copy(f'{H}/.codex/sessions', f'{d}/sessions')
for p in sorted(glob.glob(f'{d}/sessions/**/*.jsonl', recursive=True)):
    start = ''
    with open(p, errors='replace') as f:
        try: start = json.loads(f.readline()).get('timestamp', '')
        except Exception: pass
    m.add(os.path.relpath(p, d), 'Codex', '~/.codex (Codex CLI/app/VS Code extension, local)', start or mtime(p),
          source='~/.codex/' + os.path.relpath(p, d), notes=f'rollout transcript; mtime={mtime(p)}')
for name in ['session_index.jsonl', 'history.jsonl', 'external_agent_session_imports.json',
             'thread_history_1.sqlite', 'thread_history_1.sqlite-wal', 'thread_history_1.sqlite-shm',
             'state_5.sqlite', 'memories_1.sqlite', 'goals_1.sqlite', 'rules', 'skills']:
    s = f'{H}/.codex/{name}'
    if os.path.exists(s):
        copy(s, f'{d}/codex-home/{name}')
for p in glob.glob(f'{d}/codex-home/**/*', recursive=True):
    if os.path.isfile(p):
        rel = os.path.relpath(p, f'{d}/codex-home')
        note = {'history.jsonl': 'prompt history', 'session_index.jsonl': 'thread titles index',
                'thread_history_1.sqlite': 'thread items DB (57 threads, same as rollouts)', 'state_5.sqlite': 'threads/projects DB (96 threads)',
                'memories_1.sqlite': 'Codex memories DB (stage1_outputs empty)'}.get(rel, 'Codex state file')
        m.add(os.path.relpath(p, d), 'Codex', '~/.codex', mtime(p), source='~/.codex/' + rel, notes=note)
print(m.save())
