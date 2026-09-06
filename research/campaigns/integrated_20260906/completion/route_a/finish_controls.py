"""Extend any iteration-capped matched-control fit; never refit held data."""
import json
from run import HERE,CAMPAIGN
from grammar import fit

def main():
    rows=[json.loads(s) for s in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()]
    path=HERE/'matched_controls.json';controls=json.loads(path.read_text())
    for c in controls:
        for i,m in enumerate(c['candidates']):
            if m['converged']:continue
            new=fit(rows,m['program'],m['roles'],max_iter=320,pairs=c['pairs'])
            c['candidates'][i]={k:new[k] for k in ['program','roles','data_bits','total_bits','iterations','converged']}
            c.setdefault('extended_models',[]).append(new)
        c['winner']={k:min(c['candidates'],key=lambda m:m['total_bits'])[k] for k in ['program','roles','total_bits']}
    path.write_text(json.dumps(controls,indent=2)+'\n')

if __name__=='__main__':main()
