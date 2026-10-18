import os, sys, json, shutil, datetime
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, set_mtime
INC = os.path.expanduser('~/Desktop/benchmark/benchmark-data/_incoming/claude')
m = Manifest('authentic', 'claude')
os.makedirs(f'{m.dir}/conversations', exist_ok=True); os.makedirs(f'{m.dir}/_collection', exist_ok=True)
def ts(s): return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
idx = json.load(open(f'{INC}/index/chat_conversations.json'))
projs = {p['uuid']: p['name'] for p in json.load(open(f'{INC}/index/projects.json'))}
for f in os.listdir(f'{INC}/index'):
    shutil.copy(f'{INC}/index/{f}', f'{m.dir}/_collection/{f}')
n = 0
for c in idx:
    src = f'{INC}/conversations/{c["uuid"]}.json'
    if not os.path.exists(src): print('MISSING', c['uuid']); continue
    d = f'{m.dir}/conversations/{c["uuid"]}.json'
    shutil.move(src, d); set_mtime(d, ts(c['updated_at']))
    pj = (c.get('project') or {}).get('uuid') if isinstance(c.get('project'), dict) else c.get('project_uuid')
    note = 'STOPGAP: collected from signed-in claude.ai web API (no official export in benchmark-data/exports/)'
    if pj: note += f'; in project "{projs.get(pj, pj)}"'
    if c.get('is_archived'): note += '; archived'
    if c.get('is_starred'): note += '; starred'
    m.add(f'conversations/{c["uuid"]}.json', 'Claude', "claude.ai — dbarron410@vt.edu's Organization", c['updated_at'],
          source=f'https://claude.ai/chat/{c["uuid"]}', notes=note); n += 1
print(n, m.save())
