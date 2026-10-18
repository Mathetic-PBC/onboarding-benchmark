"""Merge the generators' labels (_scripts/synth/labels/<tool>.json) into synthetic/ground_truth_labels.json
({source: {item key: {project_ids, notes}}}), which build_source_items.py reads. Hidden from the agent under test."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from synthlib import ROOT, SYN, LABEL_DIR, PROJECTS

out, bad = {}, []
for f in sorted(glob.glob(os.path.join(LABEL_DIR, '*.json'))):
    tool = os.path.basename(f)[:-5]
    labs = json.load(open(f))
    for k, v in labs.items():
        unknown = set(v.get('project_ids', [])) - PROJECTS
        if unknown or not v.get('project_ids'): bad.append((tool, k, sorted(unknown) or 'no project'))
    out[tool] = labs
json.dump(out, open(os.path.join(SYN, 'ground_truth_labels.json'), 'w'), indent=1, ensure_ascii=False)
print({t: len(v) for t, v in out.items()}, 'total', sum(len(v) for v in out.values()))
for b in bad: print('BAD', b)
