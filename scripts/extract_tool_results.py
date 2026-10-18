"""Pull verbatim MCP tool results out of Claude Code session transcripts (JSONL), so connector reads are saved
exactly as returned instead of being retyped. Usage: extract_tool_results.py <name-prefix> <out.jsonl> <transcript>..."""
import json, sys

prefix, out, files = sys.argv[1], sys.argv[2], sys.argv[3:]
uses, n = {}, 0
with open(out, 'w') as o:
    for fn in files:
        for line in open(fn):
            try: d = json.loads(line)
            except Exception: continue
            c = (d.get('message') or {}).get('content')
            if not isinstance(c, list): continue
            for b in c:
                if b.get('type') == 'tool_use' and b.get('name', '').startswith(prefix):
                    uses[b['id']] = (b['name'], b.get('input'))
                elif b.get('type') == 'tool_result' and b.get('tool_use_id') in uses:
                    name, inp = uses[b['tool_use_id']]
                    cont = b.get('content')
                    text = ''.join(x.get('text', '') for x in cont if isinstance(x, dict)) if isinstance(cont, list) else cont
                    o.write(json.dumps({'tool': name, 'input': inp, 'is_error': b.get('is_error', False), 'result': text, 'ts': d.get('timestamp')}) + '\n'); n += 1
print(n, 'results')
