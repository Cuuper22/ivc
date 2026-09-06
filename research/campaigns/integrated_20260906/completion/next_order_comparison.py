#!/usr/bin/env python3
"""Next executable scope diagnostic; not executed as part of recovery.

Compare source-preserving boundary posterior at two alternative field divisions
under each retained multi-role grammar. This reports conditional consequences;
no unknown prefix is completed and no new source evidence is introduced.
"""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'route_a'));from grammar import analyze
rows=[json.loads(s) for s in (HERE.parent/'shared/observations.jsonl').read_text().splitlines()]
models=json.loads((HERE/'route_a/full_models.json').read_text())
selected=[r for r in rows if r['object_id'] in ['M77:1008','M77:1147','M77:2275']]
results=[]
for model in models:
    if model['roles']!=3:continue
    for r in selected:
        if not r['strict']:
            results.append({'row_id':r['row_id'],'program':model['program'],'raw':r['tokens_stored'],'status':'uncertain prefix retained; whole-expression boundary likelihood unavailable under strict grammar'})
            continue
        a=analyze(model,[r])[0];results.append({'row_id':r['row_id'],'program':model['program'],'raw':r['tokens_stored'],'posterior':a,'meaning':'role-boundary posterior under a conditional model, not independent grammatical evidence'})
out=HERE/'next_order_comparison_results.json';out.write_text(json.dumps({'status':'executed','results':results},indent=2)+'\n');print(out)
