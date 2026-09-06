#!/usr/bin/env python3
"""Compare all already observed exact modifier candidates under one metric.

This is a selected-rule rival comparison, not a random-sign null. Zero observed
counterparts never count as disproof. Every program uses the same graphical
fish decomposition and the same recursive rewrite semantics. Cyclic programs
are reported explicitly rather than assigned a convenient normal form.
"""
from collections import defaultdict
import itertools,json
from pathlib import Path
from run_route_a import ROOT,load,witness,TICK_PAIRS,load_observations,task_partition,write

HERE=Path(__file__).parent

def program(roof,tick):
    mapping={}
    if tick:
        m,side=tick
        for b,t in TICK_PAIRS[:5]:
            mapping[str(t)]=(str(m),str(b)) if side=='before' else (str(b),str(m))
    if roof:
        m,side=roof
        mapping['65']=(str(m),'59') if side=='before' else ('59',str(m))
        if not tick: mapping['66']=(str(m),'60') if side=='before' else ('60',str(m))
    memo={};active=set()
    def expand(t):
        if t in memo:return memo[t]
        if t not in mapping:return (t,)
        if t in active:raise ValueError('cyclic rewrite: '+t)
        active.add(t);out=tuple(x for y in mapping[t] for x in expand(y));active.remove(t)
        memo[t]=out;return out
    for t in mapping:expand(t)
    return lambda seq:tuple(y for x in seq for y in memo.get(x,(x,)))

def classes(seq,normalizer):
    groups=defaultdict(list)
    for s in seq:groups[normalizer(s)].append(s)
    return [(n,ss) for n,ss in groups.items() if len(ss)>1]

def stats(seq,joint,roof,tick,detail=False):
    groups=classes(seq,joint);cross=[];cross_only=[]
    for n,ss in groups:
        single=[];both=[]
        for a,b in itertools.combinations(ss,2):
            if roof(a)==roof(b) or tick(a)==tick(b):single.append((a,b))
            else:both.append((a,b))
        if both:cross.append((n,ss,both))
        if both and not single:cross_only.append((n,ss,both))
    target_bases={str(b):str(b) for b,m in TICK_PAIRS[:5]}|{str(m):str(b) for b,m in TICK_PAIRS[:5]}
    result=dict(expression_classes=len(groups),distinct_member_expressions=len({s for _,ss in groups for s in ss}),
        expression_pairs=sum(len(ss)*(len(ss)-1)//2 for _,ss in groups),
        cross_operation_pairs=sum(len(bb) for _,ss,bb in cross),
        classes_with_cross_operation_pair=len(cross),
        exclusively_cross_operation_classes=len(cross_only),
        exclusively_cross_operation_bases=sorted({target_bases[t] for _,ss,_ in cross_only for s in ss for t in s if t in target_bases},key=int))
    if detail:
        result['cross_operation_classes']=[dict(normal_form=n,members=ss,cross_operation_pairs=bb,
            exclusively_cross_operation=any(n==nn for nn,_,_ in cross_only)) for n,ss,bb in cross]
    return result

def main():
    raw,digest=load(ROOT/'research/data/mahadevan_20260905/concordance_documents.json.gz')
    byseq=defaultdict(list)
    for r in raw:
        if r['clean']:byseq[r['seq']].append(r)
    seq=sorted(byseq)
    old=json.loads((ROOT/'research/data/semantic_search_20260906/modifier_context_pairs.json').read_text())
    # Use every prior exact candidate, including zero-context candidates, in
    # the declared graphical family. This deliberately gives rivals breadth.
    roofs=sorted({(h['extra'],h['side']) for h in old if h['family']=='roof'})
    ticks=sorted({(h['extra'],h['side']) for h in old if h['family']=='four_surrounding_strokes'})
    observations=load_observations()
    related=[s for s in seq if '70' in s or '71' in s]
    mask=task_partition(observations,[witness(r)['row_id'] for s in related for r in byseq[s]],related)
    allowed=set(mask['train_row_ids'])
    train=[s for s in seq if any(witness(r)['row_id'] in allowed for r in byseq[s])]
    without_frame=[s for s in seq if s[:2]!=('267','99')]
    results=[];invalid=[]
    for roof,tick in itertools.product(roofs,ticks):
        try:rfun,tfun,jfun=program(roof,None),program(None,tick),program(roof,tick)
        except ValueError as e:
            invalid.append(dict(roof=roof,tick=tick,reason=str(e)));continue
        full=stats(seq,jfun,rfun,tfun,detail=(roof==(87,'before') and tick==(211,'after')))
        results.append(dict(roof=roof,tick=tick,full=full,
            leave_70_training=stats(train,jfun,rfun,tfun),
            without_267_99=stats(without_frame,jfun,rfun,tfun)))
    # Ranking chosen before examining this comparison: total independent
    # expression classes; ties favor genuinely cross-operation classes.
    def score(r,field):
        s=r[field]
        return (s['expression_classes'],s['exclusively_cross_operation_classes'],s['cross_operation_pairs'])
    full_rank=sorted(results,key=lambda r:(tuple(-x for x in score(r,'full')),r['roof'],r['tick']))
    training_rank=sorted(results,key=lambda r:(tuple(-x for x in score(r,'leave_70_training')),r['roof'],r['tick']))
    chosen=next(r for r in results if r['roof']==(87,'before') and r['tick']==(211,'after'))
    for c in chosen['full'].get('cross_operation_classes',[]):
        c['member_witnesses']=[dict(sequence=s,witnesses=[witness(r) for r in byseq[tuple(s)]]) for s in c['members']]
    target_a=('65','70','211');target_b=('87','59','71')
    matching=[]
    for r in results:
        p=program(r['roof'],r['tick'])
        if p(target_a)==p(target_b):matching.append(dict(roof=r['roof'],tick=r['tick'],normal_form=p(target_a)))
    summary=dict(input_sha256=digest,roof_candidate_orders=len(roofs),tick_candidate_orders=len(ticks),
        candidate_products=len(roofs)*len(ticks),executable_acyclic_programs=len(results),cyclic_programs=len(invalid),
        chosen_full_rank=next(i+1 for i,r in enumerate(full_rank) if r is chosen),
        chosen_leave70_training_rank=next(i+1 for i,r in enumerate(training_rank) if r is chosen),
        chosen=chosen,top10_full=full_rank[:10],top10_leave70_training=training_rank[:10],
        target_pair=dict(left=target_a,right=target_b,left_witnesses=[witness(r) for r in byseq[target_a]],right_witnesses=[witness(r) for r in byseq[target_b]],
            matching_programs=matching),
        scope='Retrospective comparison of only modifiers with a prior observed exact application; no global417x417 completeness claim',
        interpretation='A collision is a predicted equivalence class, not independent evidence that the two records mean the same thing.',
        rule_complexity='Two fixed marker IDs, two placement bits, fixed tick-then-roof recursive grammar. Rival exceptions not permitted.',
        exposure='Both corpus and prior exact modifier rankings exposed. Cross-op70pair first noticed only after frozen joint transform produced it; not a pristine blind test.',
        leave70_mask=mask)
    write(HERE/'composition_adjudication.json',summary)
    write(HERE/'composition_all_candidates.json',results)
    write(HERE/'composition_cyclic_candidates.json',invalid)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['chosen','top10_full','top10_leave70_training','leave70_mask','target_pair']},indent=2))
    print(json.dumps({'chosen':chosen,'target_matching_programs':matching},indent=2))

if __name__=='__main__':main()
