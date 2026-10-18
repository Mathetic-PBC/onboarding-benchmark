"""Build authentic/linear/Mathetic/ from verbatim Linear MCP results (read-only; linear.app web was not signed in)."""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from bm import Manifest, ROOT, set_mtime

OUT = os.path.join(ROOT, 'authentic/linear/Mathetic')
calls = [json.loads(l) for l in open(os.path.join(ROOT, '_incoming/linear_calls.jsonl')) if not json.loads(l)['is_error']]
issues = json.load(open(os.path.join(ROOT, '_incoming/linear_issues_raw.json')))['issues']
m = Manifest('authentic', 'linear')
ACCT = 'Mathetic workspace (linear.app/mathetic)'


def ts(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()


def write(rel, obj, date, notes):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w'), indent=2, ensure_ascii=False)
    if date: set_mtime(p, ts(date))
    m.add('Mathetic/' + rel, 'linear', ACCT, date or '', notes=notes)


def results(tool, **match):
    for c in calls:
        if c['tool'] == 'mcp__linear__' + tool and all((c['input'] or {}).get(k) == v for k, v in match.items()):
            try: yield c['input'], json.loads(c['result'])
            except Exception: yield c['input'], c['result']


comments = {i['issueId']: r for i, r in results('list_comments') if i.get('issueId')}
details = {i['id']: r for i, r in results('get_issue')}
for it in issues:
    k = it['id']
    cm = comments.get(k, {}).get('comments', []) if isinstance(comments.get(k), dict) else comments.get(k)
    write(f'issues/{k}.json', {'issue': it, 'detail': details.get(k), 'comments': cm}, it['updatedAt'],
          f'{it["title"]!r}; status={it["status"]}; project={it.get("project")}; {len(cm or [])} comments')
docs = {i['id']: r for i, r in results('get_document')}
for _, r in results('list_documents'):
    for d in r['documents']:
        full = docs.get(d['id'], d)
        write(f'documents/{d["id"]}.json', full, d['updatedAt'], f'{d["title"]!r}; archived {d["archivedAt"]}; project={d["project"]["name"] if d.get("project") else None}')
proj = {i['query']: r for i, r in results('get_project')}
ms = {i['project']: r for i, r in results('list_milestones')}
su = {}
for i, r in results('get_status_updates'):
    su[i.get('project') or i.get('projectId') or json.dumps(i)] = r
for pid, p in proj.items():
    write(f'projects/{pid}.json', {'project': p, 'milestones': ms.get(pid), 'status_updates': su.get(pid), 'comments': []},
          p.get('updatedAt'), f'{p.get("name")!r}; trashed={p.get("trashed")}')
for tool, name in [('list_teams', 'teams'), ('list_users', 'users'), ('list_issue_labels', 'labels'), ('list_issue_statuses', 'statuses'),
                   ('list_cycles', 'cycles'), ('list_custom_views', 'custom_views'), ('get_workspace', 'workspace')]:
    rs = [r for _, r in results(tool)]
    write(f'workspace/{name}.json', rs[-1] if rs else None, None, f'Linear MCP {tool}')
print(m.save(), 'manifest rows; status_updates keys:', list(su))
