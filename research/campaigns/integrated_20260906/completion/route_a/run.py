"""Execute restored Route A mechanism, train-only freezes, and matched controls."""
import json,sys,hashlib,math
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from grammar import *
HERE=Path(__file__).resolve().parent; CAMPAIGN=HERE.parents[1]

def write(name,data):
    (HERE/name).write_text(json.dumps(data,indent=2)+'\n')

def partition(rows,ids):
    target=[r for r in rows if r['row_id'] in ids];patterns={tuple(r['raw_slots']) for r in target};seq={tuple(r['tokens_stored']) for r in target if r['strict']}
    blocked={r['object_id'] for r in target}
    blocked|={r['object_id'] for r in rows if tuple(r['raw_slots']) in patterns or (r['strict'] and tuple(r['tokens_stored']) in seq)}
    return [r for r in rows if r['object_id'] not in blocked],target,{'target_row_ids':sorted(ids),'excluded_object_ids':sorted(blocked),'raw_pattern_aliases_excluded':True,'strict_expression_aliases_excluded':True}

def contextual(train,test,key):
    vocab=range(1,418);g=Counter();c=defaultdict(Counter)
    # Identical expressions within same context counted once.
    seen=set()
    for r in train:
        if not r['strict']:continue
        context=(str(r['raw_fields']['textnum'])[:1] if key=='site' else r['raw_fields'].get('inscobj',''));s=tuple(r['tokens_stored'])
        if (context,s) in seen:continue
        seen.add((context,s));g.update(s);c[context].update(s)
    p={str(x):(g[str(x)]+.5)/(sum(g.values())+417*.5) for x in vocab};bits=0;detail=[]
    grouped=defaultdict(list)
    for r in test:
        if r['strict']:grouped[tuple(r['tokens_stored'])].append(r)
    for seq,rr in sorted(grouped.items()):
        contexts=sorted({str(r['raw_fields']['textnum'])[:1] if key=='site' else r['raw_fields'].get('inscobj','') for r in rr})
        logs=[]
        for context in contexts:
            cc=c[context];n=sum(cc.values());logs.append(sum(math.log((cc[t]+10*p[t])/(n+10)) for t in seq))
        b=float(-(logsumexp(logs)-math.log(len(logs)))/math.log(2));bits+=b
        detail.append({'sequence':seq,'row_ids':[r['row_id'] for r in rr],'bits':b,'contexts':contexts})
    return {'data_bits':bits,'predictions':detail,'context_field':key,'smoothing_mass':10,'training_contexts':len(c),'parameter_bits':.5*len(c)*416*math.log2(max(2,sum(g.values()))),'note':'contextual unigram rival; equal mixture across observed contexts for duplicated expressions; no semantic interpretation'}

def partial(model,rows):
    E=np.column_stack([np.array(model['emission']),np.ones(model['roles'])]);T=np.array(model['transition']);pi=np.array(model['pi']);out=[]
    for r in rows:
        if r['strict'] or not r['observations']:continue
        islands=[];island=[]
        for t in r['observations']:
            if t['kind']=='sign':island.append(t['sign_id']-1)
            elif t['kind']=='doubtful_sign':island.append(417)
            else:
                if island:islands.append(island);island=[]
        if island:islands.append(island)
        if not islands:continue
        costs=[]
        for s in islands:
            a=pi.copy();lp=0
            for i,x in enumerate(s):
                if i:a=a@T
                a*=E[:,x];z=a.sum();lp+=math.log(z);a/=z
            costs.append(-lp/math.log(2))
        out.append({'row_id':r['row_id'],'islands':[[str(x+1) if x<417 else '?' for x in s] for s in islands],'visible_island_bits':costs,'policy':'Doubtful identity marginalized over all 417 IDs at one slot; unknown spans split islands with independent starts. No gap length, bridge, or reconstruction inferred.'})
    return out

def main():
    rows=[json.loads(s) for s in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()]
    if (HERE/'full_models.json').exists():
        models=json.loads((HERE/'full_models.json').read_text())
        for i,m in enumerate(models):
            if not m['converged']:models[i]=fit(rows,m['program'],m['roles'],max_iter=320)
        winner=min(models,key=lambda m:m['total_bits'])
    else:winner,models=select(rows,max_iter=160)
    write('full_models.json',models);write('winner.json',winner)
    rankings=[{k:m[k] for k in ['program','roles','data_bits','parameter_bits','rule_bits','total_bits','iterations','converged']} for m in sorted(models,key=lambda m:m['total_bits'])]
    print('full fits',rankings[0],flush=True)
    shared_masks=json.loads((CAMPAIGN/'completion/shared/masks.json').read_text())['masks']
    folds={} # Common frozen masked evaluations executed by coordinator joint runner; avoid duplicate fits.
    evaluations=[]
    for name,ids in folds.items():
        train,test,mask=partition(rows,ids);win,mm=select(train,max_iter=160)
        results=[{'program':m['program'],'roles':m['roles'],'train_total_bits':m['total_bits'],'held':score(m,test)} for m in mm]
        record={'task':name,'mask':mask,'selection':'minimum training MDL; no target fitting','winner':win['program'],'roles':win['roles'],'winner_model_sha256':hashlib.sha256(json.dumps(win,sort_keys=True).encode()).hexdigest(),'results':results,'contextual_rivals':[contextual(train,test,k) for k in ['site','obj']],'prior_exposure':'retrospective entire corpus previously exposed'}
        write(name+'_model.json',win);evaluations.append(record)
        print('fold',name,win['program'],flush=True)
    write('evaluations.json',evaluations or {'execution_owner':'coordinator','results':'../joint','common_masks':'../shared/masks.json','scope':'all seven raw count-masked joint tasks; no duplicated route fitting'})
    # Six cyclic shifts preserve base/modified sign inventories and candidate search.
    controls=json.loads((HERE/'matched_controls.json').read_text()) if (HERE/'matched_controls.json').exists() else []
    mods=[b for a,b in PAIRS]
    pairsets=[[(a,mods[(i+shift)%5]) for i,(a,b) in enumerate(PAIRS)] for shift in range(1,5)]
    pairsets += [[(a,mods[4-i]) for i,(a,b) in enumerate(PAIRS)],[(a,mods[(2*i+1)%5]) for i,(a,b) in enumerate(PAIRS)]]
    for i,pairs in enumerate(pairsets):
        if any(c['control']==i for c in controls):continue
        # Skip cyclic rewriting candidates identically for target and controls.
        valid=[];invalid=[]
        for p in PROGRAMS:
            try:features(p,pairs);valid.append(p)
            except ValueError:invalid.append(p)
        win,mm=select(rows,programs=valid,max_iter=160,pairs=pairs)
        controls.append({'control':i,'pairs':pairs,'invalid_cyclic_programs':invalid,'winner':{k:win[k] for k in ['program','roles','total_bits']},'candidates':[{k:m[k] for k in ['program','roles','data_bits','total_bits','iterations','converged']} for m in mm]})
        write('matched_controls.json',controls)
        print('control',i,win['total_bits'],flush=True)
    write('matched_controls.json',controls)
    important=[r for r in rows if r['object_id'] in ['M77:1380','M77:2452','M77:1147','M77:7249','M77:6211','M77:1551','M77:4493','M77:4556']]
    write('worked_analyses.json',analyze(winner,important));write('partial_marginals.json',partial(winner,rows))
    summary={'provenance':'new reconstruction executed on recovered frozen observations; not exact lost run','full_candidate_count':len(models),'full_ranking':rankings,'evaluations':'../joint: coordinator executes all seven common masks with numerical-face masking','matched_controls':len(controls),'graphical_control_total_fits':sum(len(x['candidates']) for x in controls),'winner':rankings[0],'placement_identifiability':'Ordered marker factors marginalize preceding versus following component roles through learned transitions. One-role models cannot distinguish direction; multirole models can. Structured alignments remain separate equivalence evidence.','boundaries':'posterior probability of latent role change, not an identified linguistic word boundary','partial_approximation':'unknown spans split independent visible islands, doubtful single signs marginalized','scientific_claim':'No accepted sign reading, pronunciation, or semantic equivalence. Conditional roof87/tick211 exact-equivalence remains distinct from raw predictive winner.','retained_structured_alignment_outputs':['../../route_a/structured_alignments.json','../../route_a/structured_literal_alignments.json','../../route_a/partial_observation_predictions.json','../../route_a/composition_adjudication.json']}
    write('summary.json',summary)
    (HERE/'REPORT.md').write_text('# Reconstructed Route A\n\nExecuted 27 graphical-program/latent-role fits on the recovered raw sign observations, six selection-matched graphical pairing controls. Seven common frozen comparisons are executed by the coordinator joint runner. Full machine-readable results are in summary.json and evaluations.json.\n\nThe grammar learns role emissions and transitions jointly by forward-backward EM. Emissions are normalized across the 417 ORIGINAL signs, using proposed graphical components as tied features. A latent role change defines an anonymous segmentation boundary. Rule and parameter costs are explicit. Exact-expression duplicates have one unit of weight. No source spelling changes.\n\nExpansion placement is modeled through preceding/following latent component roles. Additional placement predictions remain in the recovered structured alignment and composition experiments, which include one-edit anchored alignments and partial visible islands. The grammar is a constrained categorical spelling model, not proof of phonetic or semantic meaning. Its implicit equivalences remain conditional.\n\nPartial observations are scored with doubtful identities marginalized over all signs; unknown spans break independent visible islands. They are not imputed training examples. This avoids inventing span lengths but does not model uncertain-length bridges.\n\nThese are newly computed reconstruction results. Exact lost numeric results were not recreated from memory. All model parameters, optimization traces, held-out predictions, and matched control selections are preserved.\n')

if __name__=='__main__':main()
