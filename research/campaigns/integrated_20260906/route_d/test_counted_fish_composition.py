#!/usr/bin/env python3
"""Compose A roof87 with C's one-frame87→two59, then look outside that frame."""
import collections,json,sys
from run_route_d import HERE
sys.path.insert(0,str(HERE.parent/'shared'))
from foundation import compatible,task_partition

def edit_one(a,b):
    """One paid context edit, returning count of fixed matching anchors."""
    if abs(len(a)-len(b))>1:return None
    prev=[(j,0) for j in range(len(b)+1)]
    for i,x in enumerate(a,1):
        row=[(i,0)]
        for j,y in enumerate(b,1):
            options=[(prev[j][0]+1,prev[j][1]),(row[j-1][0]+1,row[j-1][1]),
                     (prev[j-1][0]+(x!=y),prev[j-1][1]+(x==y))]
            row.append(min(options,key=lambda z:(z[0],-z[1])))
        prev=row
    return prev[-1] if prev[-1][0]<=1 else None

def strict_rule_scan(rule,byseq,blocked):
    core=tuple(rule['expanded']);targets=[];hits=[]
    for seq in byseq:
        for pos in range(len(seq)-len(core)+1):
            if seq[pos:pos+len(core)]==core:targets.append((seq,pos))
    for seq in sorted(byseq):
        for pos,sign in enumerate(seq):
            if sign!=rule['compact'][0]:continue
            for target,tpos in targets:
                left=edit_one(seq[:pos],target[:tpos]);right=edit_one(seq[pos+1:],target[tpos+len(core):])
                if left is None or right is None:continue
                cost=left[0]+right[0];anchors=left[1]+right[1]
                if cost!=1 or anchors<2:continue
                source_rows=[r for r in byseq[seq] if r['object_id'] not in blocked]
                target_rows=[r for r in byseq[target] if r['object_id'] not in blocked]
                if not source_rows or not target_rows:continue
                hits.append({'compact_sequence':seq,'expanded_sequence':target,
                    'context_edit_cost':cost,'fixed_context_anchors':anchors,
                    'compact_witnesses':[r['row_id'] for r in source_rows],
                    'expanded_witnesses':[r['row_id'] for r in target_rows]})
    return hits

def partial_rule_scan(rule,rows,byseq,blocked):
    core=tuple(rule['expanded']);hits=[];eligible=0
    for row in rows:
        if row['strict'] or row['object_id'] in blocked or row['direction_code_raw'] not in ('1','2','3'):continue
        obs=row['observations']
        for pos,o in enumerate(obs):
            if o['kind']!='sign' or str(o['sign_id'])!=rule['compact'][0]:continue
            anchors=sum(x['kind']=='sign' for i,x in enumerate(obs) if i!=pos)
            if anchors<2:continue
            eligible+=1
            for target,rr in byseq.items():
                clean=[r for r in rr if r['object_id'] not in blocked]
                if not clean:continue
                for tpos in range(len(target)-len(core)+1):
                    if target[tpos:tpos+len(core)]!=core:continue
                    if compatible(obs[:pos],target[:tpos]) and compatible(obs[pos+1:],target[tpos+len(core):]):
                        hits.append({'partial_compact_row':row['row_id'],'raw_tokens':row['tokens_stored'],
                            'strict_expanded_sequence':target,'strict_expanded_rows':[r['row_id'] for r in clean],
                            'visible_context_anchors':anchors,'reconstructed_source':False,
                            'compatible_with_doubtful_ids_respected':compatible(obs[:pos],target[:tpos],False) and compatible(obs[pos+1:],target[tpos+len(core):],False),
                            'compatibility_only':'unknown spans consume0..remaining; doubtful signs treated as unknown single slots'})
    return {'eligible_partial_occurrences':eligible,'compatibility_pairs':len(hits),'hits':hits,
        'scope':'partial compact observation against strict observed expansion; no partial completion trained or counted as lexical evidence'}

def main():
    rows=[json.loads(x) for x in (HERE.parent/'shared/observations.jsonl').read_text().splitlines()]
    byseq=collections.defaultdict(list)
    for r in rows:
        if r['strict']:byseq[tuple(r['tokens_stored'])].append(r)
    rules=[{'compact':['65'],'expanded':['59','59'],'meaning':'roof65 denotes two plain59'},
        {'compact':['66'],'expanded':['59','59','211'],'meaning':'two plain59 with one group-scope211'},
        {'compact':['66'],'expanded':['60','60'],'meaning':'roof66 denotes two marked60; ticks distributed to each fish'}]
    defining_rows=[r['row_id'] for r in rows if r['strict'] and tuple(r['tokens_stored'][:2])==('267','99')]
    partition=task_partition(rows,defining_rows)
    blocked=set(partition['excluded_object_ids'])
    rivals=[{'compact':[base],'expanded':[marker,'59']+(['211'] if base=='66' else []),
        'meaning':'generic slot-rival expansion','slot_marker':marker}
        for base in ['65','66'] for marker in ['65','87','104']]
    for rule in rules+rivals:
        hits=[];opportunities=0
        for seq in sorted(byseq):
            for pos,sign in enumerate(seq):
                if sign!=rule['compact'][0]:continue
                opportunities+=1
                target=seq[:pos]+tuple(rule['expanded'])+seq[pos+1:]
                if target not in byseq:continue
                context=seq[:pos]+seq[pos+1:]
                hits.append({'compact_sequence':seq,'expanded_sequence':target,'unchanged_context':context,
                    'defining_267_99_frame':seq[:2]==('267','99'),
                    'eligible_compact_rows':[r['row_id'] for r in byseq[seq] if r['object_id'] not in blocked],
                    'eligible_expanded_rows':[r['row_id'] for r in byseq[target] if r['object_id'] not in blocked],
                    'compact_witnesses':[{'row_id':r['row_id'],'object_id':r['object_id'],'source_record':r['source_record']} for r in byseq[seq]],
                    'expanded_witnesses':[{'row_id':r['row_id'],'object_id':r['object_id'],'source_record':r['source_record']} for r in byseq[target]]})
        rule.update({'source_expression_occurrences':opportunities,'exact_counterparts':len(hits),
            'outside_defining_frame_counterparts':sum(bool(h['eligible_compact_rows'] and h['eligible_expanded_rows']) for h in hits),'hits':hits})
    for rule in rules+rivals:
        rule['one_paid_context_edit']=strict_rule_scan(rule,byseq,blocked)
        rule['one_edit_distinct_source_types']=len({tuple(h['compact_sequence']) for h in rule['one_paid_context_edit']})
        rule['partial_compatibility']=partial_rule_scan(rule,rows,byseq,blocked)
    result={'question':'Does A+C composition transfer the count-two interpretation outside its267–99defining frame?',
        'hypothesis_dependencies':['A65=87+59 and66=87+60','C87+59=59+59 in267–99frame only'],
        'rules':rules,'slot_rivals':rivals,'partition':partition,
        'missing_counterpart_policy':'absence is unknown, not a negative attestation',
        'scope':'exact plus one paid context edit with2fixed anchors; separate visible partial lane; no source lines joined or sounds invented',
        'alternatives':['87phoneticmodifier','87categoricalquantitylabel','65/66independentgraphicalcategories'],
        'exposure':'retrospective; original267–99data excluded from transfer count'}
    (HERE/'outputs/counted_fish_composition.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{'compact':r['compact'],'expanded':r['expanded'],
        'exact_counterparts':r.get('exact_counterparts'),'exact_outside_frame':r.get('outside_defining_frame_counterparts'),
        'one_edit_pairs':len(r['one_paid_context_edit']),'one_edit_source_types':r['one_edit_distinct_source_types'],
        'partial_pairs':r['partial_compatibility']['compatibility_pairs']} for r in rules+rivals],indent=2))

if __name__=='__main__':main()
