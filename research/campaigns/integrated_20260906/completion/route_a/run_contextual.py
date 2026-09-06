"""Fit cheap contextual rivals on the shared frozen raw-text masks."""
import json
from run import HERE,CAMPAIGN,contextual
from grammar import fit,score

def main():
    rows=[json.loads(s) for s in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()]
    masks=json.loads((CAMPAIGN/'completion/shared/masks.json').read_text())['masks'];out=[]
    for name,m in masks.items():
        ti=set(m['train_row_ids']);hi=set(m['target_row_ids'])
        train=[r for r in rows if r['row_id'] in ti];test=[r for r in rows if r['row_id'] in hi]
        model=fit(train,'identity',1);baseline=score(model,test)
        rivals=[contextual(train,test,k) for k in ['site','obj']]
        for r in rivals:r['heldout_gain_bits']=baseline['data_bits']-r['data_bits']
        out.append({'task':name,'rivals':rivals,'global_categorical_baseline':baseline,'baseline_model':model,'mask_source':'../shared/masks.json','scope':'all raw text targets, same unique expressions; separate from joint channel with count faces removed'})
    (HERE/'contextual_evaluations.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
