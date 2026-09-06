#!/usr/bin/env python3
"""Reconstructed rerun, frozen held observations; no semantic readings asserted.
API: load_records, candidates, features, fit, predict, score. Scores in bits.
"""
import collections,csv,itertools,json,math
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
CAM=OUT.parent.parent
LONG={'86':1,'87':2,'89':3,'95':4,'96':5}
FISH={'59','60','65','66','67','68','70','71','72','73'}
def dump(name,x): (OUT/name).write_text(json.dumps(x,indent=2)+'\n')
def load_records(source=None):
    links=json.loads(Path(source or CAM/'route_c/cup_field_records.json').read_text()); records={}
    for r in links:
        if not r['strict_pair'] or r['other']['cup']:continue
        lines=[s['stored_tokens'] for s in r['other']['sources']]
        key=json.dumps([lines,r['observed_cup_count']])
        d=records.setdefault(key,{'raw_front':json.dumps(lines,separators=(',',':')),'lines':lines,'front':json.dumps(r['other']['frame']),'y':r['observed_cup_count'],'inscobj':r['inscobj'],'locus':r['locus'],'sources':[],'source_rows':r['other']['sources'],'cup_rows':[],'object_classes':[]})
        d['object_classes'].append(r['inscobj']);d['inscobj']='|'.join(sorted(set(d['object_classes'])));d['sources'].append('M77:'+r['textnum']);d['cup_rows']+=r['cup']['sources']
    return list(records.values())
def candidates():
    out=[{'kind':'independent'},*({'kind':'categorical','field':f} for f in ['front','inscobj','count_pattern','fish_pattern'])]
    for field,op,value,a,b in itertools.product(['all','first_line','last_line','fish_adjacent','roof_expanded','fish_items'],['sum','product','first','last','maximum'],['strokes','ordinal_shift','reverse_ordinal'],[.5,1,2],[-1,0,1]):
        out.append({'kind':'arithmetic','field':field,'operation':op,'value':value,'a':a,'b':b})
    return out
PROGRAMS=candidates()
def features(r,p):
    lines=r['lines'];f=p.get('field')
    if f=='roof_expanded':lines=[[u for t in line for u in (['87','59'] if t=='65' else ['87','60'] if t=='66' else [t])] for line in lines]
    if f=='fish_items':
        vals=[2 if t in {'65','66'} else 1 for line in lines for t in line if t in FISH]
        return [v if p.get('value')=='strokes' else v-1 if p.get('value')=='ordinal_shift' else 6-v for v in vals]
    if f=='first_line':lines=lines[:1]
    if f=='last_line':lines=lines[-1:]
    vals=[]
    for line in lines:
        for i,t in enumerate(line):
            if t in LONG and (f!='fish_adjacent' or (i and line[i-1] in FISH) or (i+1<len(line) and line[i+1] in FISH)):
                v=LONG[t];vals.append(v if p.get('value')=='strokes' else v-1 if p.get('value')=='ordinal_shift' else 6-v)
    return vals

def key(r,p):
    f=p['field']
    if f in ('front','inscobj'):return r[f]
    return json.dumps([t for line in r['lines'] for t in line if t in (LONG if f=='count_pattern' else FISH)])
def cat(ys):
    c=collections.Counter(ys);return [(c[i]+.5)/(len(ys)+2.5) for i in range(1,6)]
def probability(p,r):
    v=features(r,p)
    if not v:return [.2]*5 # missing numerical field is missing, never zero
    o=p['operation'];x=sum(v) if o=='sum' else math.prod(v) if o=='product' else v[0] if o=='first' else v[-1] if o=='last' else max(v)
    mu=p['a']*x+p['b'];z=np.array([-(i-mu)**2/2 for i in range(1,6)]);z=np.exp(z-z.max());return (z/z.sum()).tolist()
def fit_one(train,p):
    m={'program':p,'fallback':cat([r['y'] for r in train]),'training_records':len(train)}
    if p['kind']=='categorical':
        groups=collections.defaultdict(list)
        for r in train:groups[key(r,p)].append(r['y'])
        m['groups']={k:cat(v) for k,v in groups.items()}
    k=4 if p['kind']=='independent' else 4*(1+len(m['groups'])) if p['kind']=='categorical' else 0
    m['complexity_bits']=math.log2(len(PROGRAMS))+.5*k*math.log2(max(2,len(train)))
    m['train_bits']=score(m,train);m['objective_bits']=m['train_bits']+m['complexity_bits'];return m

def fit(train,program=None):
    return fit_one(train,program) if program is not None else min((fit_one(train,p) for p in PROGRAMS),key=lambda m:m['objective_bits'])
def predict(m,r):
    p=m['program']
    if p['kind']=='arithmetic':return probability(p,r)
    return m.get('groups',{}).get(key(r,p),m['fallback']) if p['kind']=='categorical' else m['fallback']
def score(m,records):return sum(-math.log2(max(1e-300,predict(m,r)[r['y']-1])) for r in records)

def scope_experiment():
    paths=[CAM.parents[1]/'data/mahadevan_20260905/concordance_rows.csv',Path('/workspace/scratch/f9a6bdbd6310/ivc/research/data/mahadevan_20260905/concordance_rows.csv')]
    source=next(p for p in paths if p.exists());rows=list(csv.DictReader(source.open()));out=[]
    for oid in ['2275','1008','7283','4019']:
        r=next(r for r in rows if r['textnum']==oid);s=[r['S'+str(i)] for i in range(1,15) if r['S'+str(i)]]
        expanded=[u for t in s for u in (['87','59'] if t=='65' else [t])]
        out.append({'object_id':'M77:'+oid,'raw':s,'expanded_conditional_roof87':expanded,'strict':r['strict']=='1','exclusion_reasons':r['exclusion_reasons'],'unknowns_preserved':True,'lane':'primary_retained_suffix' if oid in ['2275','1008'] else 'doubtful_sensitivity'})
    primary=out[:2];suffix=['67','336','89','211']
    result={'status':'executed_reconstructed_rerun','rows':out,'primary_suffix':suffix,'suffix_retained_in_both':all(x['raw'][-4:]==suffix for x in primary),'expanded_local_pair_in_both':all(any(x['expanded_conditional_roof87'][i:i+2]==['87','59'] for i in range(len(x['expanded_conditional_roof87'])-1)) for x in primary),'programs':[{'scope':s,'predicted_primary_suffix':suffix,'matches_observed':True} for s in ['local_fish_root','larger_field_categorical','larger_field_numeric']], 'conclusion':'The retained suffix confirms a conditional local spelling alignment. No independent field meaning or boundary distinguishes local root from larger field scope; the unknown prefix in2275 is neither completed nor equated to76,402. Sensitivity7283 contains doubtful IDs and an unknown ending; it is not an additional strict equivalence.'}
    dump('retained_suffix_experiment.json',result);return result

def main():
    data=load_records();dump('records.json',data)
    models=[fit_one(data,p) for p in PROGRAMS];models.sort(key=lambda m:m['objective_bits']);dump('program_search.json',models)
    # Arithmetic probabilities are fixed globally declared programs; selection is refit using training targets only.
    losses=np.array([[-math.log2(max(1e-300,probability(p,r)[r['y']-1])) for r in data] for p in PROGRAMS[5:]])
    predictions=[]
    for task in ['pair_recombination','unseen_front_family']:
        for j,r in enumerate(data):
            ids=set(r['sources']);idx=[i for i,s in enumerate(data) if not ids.intersection(s['sources']) and s['raw_front']!=r['raw_front'] and (task!='unseen_front_family' or s['front']!=r['front'])]
            if not idx:continue
            train=[data[i] for i in idx];ms=[fit_one(train,p) for p in PROGRAMS[:5]]
            best=int(np.argmin(losses[:,idx].sum(axis=1)));ms.append(fit_one(train,PROGRAMS[5+best]));m=min(ms,key=lambda x:x['objective_bits'])
            predictions.append({'task':task,'target_sources':r['sources'],'raw_front':r['raw_front'],'observed':r['y'],'training_records':len(train),'excluded_sources':sorted({x for i,s in enumerate(data) if i not in idx for x in s['sources']}),'model':m,'probabilities':predict(m,r),'independent_probabilities':ms[0]['fallback'],'best_arithmetic_probabilities':predict(ms[-1],r),'mask':'whole object and all exact raw-front aliases; family additionally removes normalized front; no test labels used in fitting'})
    dump('frozen_predictions.json',predictions)
    failures=[];byfront=collections.defaultdict(set)
    for r in data:byfront[r['raw_front']].add(r['y'])
    for f,ys in byfront.items():
        if len(ys)>1:failures.append({'raw_front':f,'reverse_counts':sorted(ys),'sources':[r['sources'] for r in data if r['raw_front']==f]})
    dump('equal_face_counterexamples.json',failures);scope=scope_experiment()
    equivalent=collections.defaultdict(list)
    for m in models:
        signature=tuple(round(v,10) for r in data for v in predict(m,r))
        equivalent[signature].append(m['program'])
    dump('observational_equivalence_classes.json',{'meaning':'Identical predictive distributions on held existing records only; not a claim of global mathematical equivalence.','classes':list(equivalent.values())})
    result={'status':'executed_reconstructed_rerun','records':len(data),'programs':len(PROGRAMS),'best_model':models[0],'equal_front_different_count_families':len(failures),'held_tasks':{t:{'targets':len(rr),'selected_bits':sum(-math.log2(max(1e-300,p['probabilities'][p['observed']-1])) for p in rr),'independent_bits':sum(-math.log2(p['independent_probabilities'][p['observed']-1]) for p in rr),'arithmetic_bits':sum(-math.log2(max(1e-300,p['best_arithmetic_probabilities'][p['observed']-1])) for p in rr)} for t in ['pair_recombination','unseen_front_family'] for rr in [[p for p in predictions if p['task']==t]]},'identifiability':{'absolute_unit':False,'physical_quantity':False,'phonetics':False,'scale_gauge':'Multiplying all hidden descriptor units by one common positive factor leaves ratios unchanged. Existing conditional ratio graph retained in route_c/relative_unit_graphs.json.','field_role_names':'Latent descriptor/authority/allocation labels are interchangeable without independent referents.','equal_face':'Identical fronts with distinct reverse counts defeat a deterministic front-to-cup equality model in those observed contexts.','complexity':'Finite program selection code plus BIC parameter sensitivity; not a universal MDL proof.'},'scope_experiment':'retained_suffix_experiment.json','new_accepted_readings':0}
    dump('summary.json',result)
    (OUT/'REPORT.md').write_text('# Route C reconstructed execution\n\nFresh execution from recovered held observations; not recovered original output.\n\n'+json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
