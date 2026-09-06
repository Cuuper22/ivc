#!/usr/bin/env python3
"""A13--18: competing, anchor-preserving graphical-operation models.

Only existing Mahadevan rows and previously proposed graphical decompositions
are used.  No proposed decomposition changes a source transcription.  Alignment
is candidate generation, never evidence that expressions mean the same thing.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'research/tools'))
from semantic_transducer_search import load, TICK_PAIRS, ROOF_PAIRS, PARTS, witness as old_witness
sys.path.insert(0, str(Path(__file__).parent.parent/'shared'))
from foundation import load_observations, task_partition


def witness(r):
    return old_witness(r) | {'row_id':f"M77:{r['textnum']}:{r['sideline']}",
                             'object_id':f"M77:{r['textnum']}"}


def normalize_sequence(sequence, model='fish211'):
    """Executable CONDITIONAL candidate, not a source normalization.

    model fish211: marked fish becomes corresponding base then 211.
    model global211: same claim for all declared four-stroke pairs.
    model categorical: original tokens unchanged; no equivalence asserted.
    """
    pairs=TICK_PAIRS[:5] if model in ('fish211','fish211_roof87','fish211_roof102') else TICK_PAIRS if model=='global211' else []
    mapping={str(m):(str(b),'211') for b,m in pairs}
    if model in ('roof87','roof102','fish211_roof87','fish211_roof102'):
        roof='87' if model.endswith('87') else '102'
        mapping['65']=(roof,'59')
        mapping['66']=(roof,'59','211') if model.startswith('fish211') else (roof,'60')
    return tuple(z for t in sequence for z in mapping.get(str(t),(str(t),)))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def align(a, b):
    """Unit edit cost; among equal-cost paths maximize observed exact anchors."""
    prev = [(j, 0) for j in range(len(b) + 1)]
    for i, x in enumerate(a, 1):
        row = [(i, 0)]
        for j, y in enumerate(b, 1):
            candidates = [(prev[j][0]+1, prev[j][1]),
                          (row[j-1][0]+1, row[j-1][1]),
                          (prev[j-1][0]+int(x != y), prev[j-1][1]+int(x == y))]
            row.append(min(candidates, key=lambda z:(z[0], -z[1])))
        prev = row
    return prev[-1]


def context_alignment(s, i, t, j, marker_index=None):
    p, q = t[:j], t[j+1:]
    if marker_index is not None:
        if marker_index < j: p = t[:marker_index] + t[marker_index+1:j]
        else: q = t[j+1:marker_index] + t[marker_index+1:]
    a, b = align(s[:i], p), align(s[i+1:], q)
    return a[0]+b[0], a[1]+b[1]


def enumerate_alignments(sequences, occurrence, byseq, max_edits=1, min_anchors=2):
    out=[]
    for family, pairs in [('four_surrounding_strokes', TICK_PAIRS), ('roof', ROOF_PAIRS),
                          ('roof_on_marked_fish',[(60,66)])]:
        for base, modified in pairs:
            for s, i in occurrence[str(modified)]:
                for t, j in occurrence[str(base)]:
                    if s == t: continue
                    # A shared anchor must remain on its side of the graphical base.
                    if abs(len(s)-len(t)) > max_edits+1: continue
                    ed, n = context_alignment(s, i, t, j)
                    if ed <= max_edits and n >= min_anchors:
                        out.append(dict(family=family,base=base,modified=modified,
                            compact=s,expanded=t,compact_position=i,base_position=j,
                            marker=None,marker_position=None,placement='no_extra_unit',
                            residual_edits=ed,exact_anchors=n))
                    if abs(len(s)+1-len(t)) > max_edits: continue
                    for k, token in enumerate(t):
                        if k == j: continue
                        ed, n = context_alignment(s, i, t, j, k)
                        if ed <= max_edits and n >= min_anchors:
                            if k == j+1: placement='adjacent_after'
                            elif k == j-1: placement='adjacent_before'
                            elif k > j: placement='nonadjacent_after'
                            else: placement='nonadjacent_before'
                            out.append(dict(family=family,base=base,modified=modified,
                                compact=s,expanded=t,compact_position=i,base_position=j,
                                marker=int(token),marker_position=k,placement=placement,
                                residual_edits=ed,exact_anchors=n))
    for h in out:
        h['compact_witnesses']=[witness(r) for r in byseq[tuple(h['compact'])]]
        h['expanded_witnesses']=[witness(r) for r in byseq[tuple(h['expanded'])]]
    return out


def literal_alignments(sequences, byseq):
    """One context edit beyond the earlier zero-hit exact literal search."""
    out=[]
    for composite,base,part in PARTS:
        for expansion in sorted({(str(base),str(part)),(str(part),str(base))}):
            compact=[(s,i) for s in sequences for i,t in enumerate(s) if t==str(composite)]
            expanded=[(s,i) for s in sequences for i in range(len(s)-1) if s[i:i+2]==expansion]
            for s,i in compact:
                for t,j in expanded:
                    if abs(len(s)+1-len(t))>1:continue
                    left=align(s[:i],t[:j]);right=align(s[i+1:],t[j+2:])
                    ed,n=left[0]+right[0],left[1]+right[1]
                    if ed<=1 and n>=2:
                        out.append(dict(composite=composite,base=base,part=part,expansion=expansion,
                            compact=s,expanded=t,residual_edits=ed,exact_anchors=n,
                            compact_witnesses=[witness(r) for r in byseq[s]],
                            expanded_witnesses=[witness(r) for r in byseq[t]]))
    return out


def summarize_hits(hits):
    return dict(alignments=len(hits),
        distinct_text_pairs=len({(tuple(h['compact']),tuple(h['expanded'])) for h in hits}),
        compact_texts=len({tuple(h['compact']) for h in hits}),
        expanded_texts=len({tuple(h['expanded']) for h in hits}),
        bases=sorted({h['base'] for h in hits}),
        residual_edits=dict(Counter(h['residual_edits'] for h in hits)),
        placements=dict(Counter(h['placement'] for h in hits)),
        source_objects=sorted({str(w['textnum']) for h in hits for key in ['compact_witnesses','expanded_witnesses'] for w in h[key]}))


def rank_markers(hits, exclude_base=None):
    groups=defaultdict(list)
    for h in hits:
        if h['base'] != exclude_base: groups[h['marker']].append(h)
    records=[]
    for marker, hh in groups.items():
        nbase=len({h['base'] for h in hh})
        pairs=len({(tuple(h['compact']),tuple(h['expanded'])) for h in hh})
        exact=len({(tuple(h['compact']),tuple(h['expanded'])) for h in hh if not h['residual_edits']})
        records.append(dict(marker=marker,base_count=nbase,distinct_pairs=pairs,
                            exact_pairs=exact,score=10000*nbase+100*exact+pairs))
    return sorted(records,key=lambda x:(-x['score'],x['marker'] or -1))


def occurrence_profiles(sequences, byseq):
    profiles=[]; contradictions=[]
    for base, marked in TICK_PAIRS:
        for token in (str(base),str(marked)):
            occ=[(s,i) for s in sequences for i,t in enumerate(s) if t==token]
            with211=[(s,i) for s,i in occ if '211' in s]
            profiles.append(dict(base=base,sign=int(token),marked=int(token)==marked,
                unique_text_occurrences=len(occ),terminal=sum(i==len(s)-1 for s,i in occ),
                separate211_texts=len({s for s,i in with211}),
                after211=sum('211' in s[i+1:] for s,i in occ),
                before211=sum('211' in s[:i] for s,i in occ),
                next=dict(Counter(s[i+1] if i+1<len(s) else '$' for s,i in occ))))
            if int(token)==marked:
                for s,i in with211:
                    contradictions.append(dict(base=base,modified=marked,sequence=s,
                        fish_family=base in [59,65,67,70,72],
                        witnesses=[witness(r) for r in byseq[s]],
                        contradicts='unconditional mutually-exclusive graphical-mark/separate211 rule; not optional expansion'))
    return profiles,contradictions


def boundary_model(sequences, byseq):
    """Score marked-fish next contexts against base+211 and categorical rivals.

    Train on OTHER fish bases: marked target rows are never included in their
    own predictive table. Each unique expression contributes total unit mass,
    distributed over its relevant occurrences. Outcomes are *observed* next
    sign or boundary, not presence of an unattested alternative inscription.
    """
    bases=[str(a) for a,b in TICK_PAIRS[:5]]
    marked={str(b):str(a) for a,b in TICK_PAIRS[:5]}
    rec=[]
    for s in sequences:
        active=[i for i,x in enumerate(s) if x in bases or x in marked]
        for i in active:
            x=s[i]; b=marked.get(x,x); m=x in marked
            out=s[i+1] if i+1<len(s) else '$'
            records=[dict(sequence=s,index=i,base=b,marked=m,
                outcome=out,weight=1/len(active),
                sitecodes=sorted({str(r['textnum'])[:1] for r in byseq[s]}),
                objectcodes=sorted({r['inscobj'] for r in byseq[s]}))]
            rec.extend(records)
    targets=[r for r in rec if r['marked']]
    alphabet=[str(i) for i in range(1,418)]+['$']
    # A shared TRAIN-ONLY backoff avoids rewarding a model merely because its
    # much larger sample escapes a large per-symbol smoothing penalty.
    alpha=1.0
    models=['bare_base','base_then211','all211','marked_other_base','terminal_category',
            'marked_objectclass','marked_catalogue_prefix']
    observations=load_observations()
    masks={}
    train_sequences={}
    allowed_rows={}
    for b in bases:
        related=[s for s in sequences if any(x==b or marked.get(x)==b for x in s)]
        target_ids=[witness(r)['row_id'] for s in related for r in byseq[s]]
        mask=task_partition(observations,target_ids,related)
        allowed=set(mask['train_row_ids'])
        allowed_rows[b]=allowed
        train_sequences[b]=[s for s in sequences if any(witness(r)['row_id'] in allowed for r in byseq[s])]
        masks[b]={k:v for k,v in mask.items() if k!='train_row_ids'}|{'training_rows':len(allowed),'training_unique_sequences':len(train_sequences[b])}
    predictions=[]
    for q in targets:
        counts={m:Counter() for m in models}
        contextual={'marked_objectclass':defaultdict(Counter),'marked_catalogue_prefix':defaultdict(Counter)}
        background=Counter()
        for s in train_sequences[q['base']]:
            for i,x in enumerate(s):
                nxt=s[i+1] if i+1<len(s) else '$'
                background[nxt]+=1
                if x in bases: counts['bare_base'][nxt]+=1
                if x in bases and nxt=='211':
                    counts['base_then211'][s[i+2] if i+2<len(s) else '$']+=1
                if x=='211': counts['all211'][nxt]+=1
                if x in marked:
                    counts['marked_other_base'][nxt]+=1
                    permitted=[r for r in byseq[s] if witness(r)['row_id'] in allowed_rows[q['base']]]
                    classes=sorted({r['inscobj'] for r in permitted})
                    prefixes=sorted({str(r['textnum'])[:1] for r in permitted})
                    for model,keys in [('marked_objectclass',classes),('marked_catalogue_prefix',prefixes)]:
                        for key in keys:contextual[model][key][nxt]+=1/len(keys)
        counts['terminal_category']['$']=1
        p0={x:(background[x]+1)/(sum(background.values())+len(alphabet)) for x in alphabet}
        scores={}
        for m,c in counts.items():
            if m in contextual:
                keys=q['objectcodes'] if m=='marked_objectclass' else q['sitecodes']
                shared=counts['marked_other_base']
                backoff=(shared[q['outcome']]+p0[q['outcome']])/(sum(shared.values())+1)
                p=sum((contextual[m][key][q['outcome']]+2*backoff)/(sum(contextual[m][key].values())+2) for key in keys)/len(keys)
            elif m=='terminal_category':
                # One fitted parameter, trained only on OTHER marked families.
                cc=counts['marked_other_base']; n=sum(cc.values())
                p_end=(cc['$']+0.5)/(n+1)
                p=p_end if q['outcome']=='$' else (1-p_end)*p0[q['outcome']]/(1-p0['$'])
            else:
                p=(c[q['outcome']]+alpha*p0[q['outcome']])/(sum(c.values())+alpha)
            scores[m]=dict(probability=p,bits=-math.log2(p),training_examples=sum(c.values()))
        predictions.append(q|{'scores':scores,'object_ids':sorted({r['textnum'] for r in byseq[tuple(q['sequence'])]})})
    totals={m:sum(p['weight']*p['scores'][m]['bits'] for p in predictions) for m in models}
    bybase={b:{m:sum(p['weight']*p['scores'][m]['bits'] for p in predictions if p['base']==b) for m in models} for b in bases}
    return dict(task='predict observed next sign/boundary after marked fish; leave target graphical base and all its texts out',
        exposure='retrospective; graphical family and 211 candidate previously proposed',
        targets=len(predictions),weighted_targets=sum(p['weight'] for p in predictions),
        alpha=alpha,alphabet=alphabet,total_bits=totals,by_base_bits=bybase,
        parameter_note='Categorical boundary has one fitted parameter; token distributions have common alphabet degrees of freedom. Graphical mappings/211 choice are additional hypotheses, not free semantic evidence.',
        masks=masks,predictions=predictions)


def partial_observations(rows, byseq, sequences):
    """Use only visible islands, never fill a missing sign or unknown span."""
    marked={str(b):str(a) for a,b in TICK_PAIRS[:5]}
    out=[]
    for r in rows:
        if r['clean']: continue
        slots=[str(r[f'S{i}']) for i in range(1,15)]
        last=max((i for i,t in enumerate(slots) if t),default=-1)
        seq=tuple(slots[:last+1])
        for i,t in enumerate(seq):
            if t not in marked: continue
            left=[]; right=[]
            for x in reversed(seq[:i]):
                if not (x.isdigit() and 1<=int(x)<=417):break
                left.insert(0,x)
            for x in seq[i+1:]:
                if not (x.isdigit() and 1<=int(x)<=417):break
                right.append(x)
            island=tuple(left+[t]+right); p=len(left)
            expanded=island[:p]+(marked[t],'211')+island[p+1:]
            matches=[]
            if len(left)+len(right)>=2:
                for s in sequences:
                    for j in range(len(s)-len(expanded)+1):
                        if s[j:j+len(expanded)]==expanded:
                            matches.append(dict(sequence=s,position=j,witnesses=[witness(z) for z in byseq[s]]))
            out.append(dict(source=witness(r),visible_island=island,
                raw_slots=slots,
                modified=t,predicted_expanded_island=expanded,
                exact_matches_in_strict_observations=matches,
                unknown_handling='Uncertain signs bound the visible island. No completion or assumed span length.',
                direction_status='source direction retained; no alternative reversal'))
    return out


def spelling_search(sequences,byseq):
    """Select extra unit using training families, predict full withheld forms.

    The observable scored target is the continuation after the modified sign.
    Predicted full spellings are exported; absent spellings remain unknown.
    """
    observations=load_observations();bases={str(a) for a,b in TICK_PAIRS[:5]}
    marked={str(b):str(a) for a,b in TICK_PAIRS[:5]}
    vocabulary=[str(i) for i in range(1,418)];alphabet=vocabulary+['$']
    folds=[];predictions=[]
    for base in sorted(bases,key=int):
        related=[s for s in sequences if any(t==base or marked.get(t)==base for t in s)]
        mask=task_partition(observations,[witness(r)['row_id'] for s in related for r in byseq[s]],related)
        allowed=set(mask['train_row_ids'])
        train=[s for s in sequences if any(witness(r)['row_id'] in allowed for r in byseq[s])]
        background=Counter();after_marker=defaultdict(Counter);training_marked=Counter()
        for s in train:
            for i,t in enumerate(s):
                nxt=s[i+1] if i+1<len(s) else '$';background[nxt]+=1
                if t in marked:training_marked[nxt]+=1
                if t in bases and i+1<len(s):
                    after_marker[s[i+1]][s[i+2] if i+2<len(s) else '$']+=1
        p0={x:(background[x]+1)/(sum(background.values())+len(alphabet)) for x in alphabet}
        def probability(marker,outcome):
            c=after_marker[marker]
            return (c[outcome]+p0[outcome])/(sum(c.values())+1)
        ranks=sorted([{'marker':m,'training_bits':sum(-n*math.log2(probability(m,x)) for x,n in training_marked.items()),
                      'base_marker_examples':sum(after_marker[m].values())} for m in vocabulary],
                    key=lambda r:(r['training_bits'],int(r['marker'])))
        winner=ranks[0]['marker']
        targets=[(s,i) for s in related for i,t in enumerate(s) if marked.get(t)==base]
        bits=0;observed=0
        for s,i in targets:
            nxt=s[i+1] if i+1<len(s) else '$'
            proposed=s[:i]+(base,winner)+s[i+1:]
            seen=proposed in byseq
            observed+=seen;bits-=math.log2(probability(winner,nxt))
            predictions.append(dict(source=s,source_witnesses=[witness(r) for r in byseq[s]],
                withheld_base=base,predicted_marker=winner,predicted_sequence=proposed,
                observed_continuation=nxt,continuation_probability=probability(winner,nxt),
                exact_prediction_observed=seen,prediction_witnesses=[witness(r) for r in byseq.get(proposed,[])],
                absent_prediction_policy='Unobserved combinations are unknown, never counted false',
                exposure='retrospective; any six old exact pairs are not new discoveries'))
        folds.append(dict(withheld_base=base,winner=winner,training_top5=ranks[:5],
            target_occurrences=len(targets),heldout_continuation_bits=bits,
            exact_predicted_forms_observed=observed,excluded_object_ids=mask['excluded_object_ids']))
    return dict(task='Select a separate written unit from other graphical bases; predict expanded form and observed continuation of target base',
        folds=folds,predictions=predictions,
        complexity={'marker_selection_bits':math.log2(417),'symbolic_expansion_rule_bits':2,
                    'fish_subset_selection_bits_if_not_prespecified':math.log2(math.comb(len(TICK_PAIRS),5)),
                    'pair_mapping_cost':'shared declared graphical pairs are conditioning evidence; raw identity not merged'},
        status='full-form reach and continuation prediction; equivalence remains a hypothesis')


def boundary_repair(sequences,byseq):
    block=('336','89','211');stem=('336','89')
    matches=[];marked={str(b) for a,b in TICK_PAIRS[:5]}
    for s in sequences:
        for i in range(len(s)-len(block)+1):
            if s[i:i+len(block)]==block:
                matches.append(dict(sequence=s,block_position=i,prefix=s[:i],suffix=s[i+3:],
                                    witnesses=[witness(r) for r in byseq[s]]))
    marked_before_stem=[dict(sequence=s,position=i,witnesses=[witness(r) for r in byseq[s]])
        for s in sequences for i in range(len(s)-2) if s[i] in marked and s[i+1:i+3]==stem]
    separate_before_stem=[dict(sequence=s,position=i,witnesses=[witness(r) for r in byseq[s]])
        for s in sequences for i in range(len(s)-2) if s[i]=='211' and s[i+1:i+3]==stem]
    return dict(counterexample='M77:1147:0',candidate_segmentation=[['387','66'],list(block)],
        independently_attested_suffix_witnesses=[witness(r) for r in byseq.get(block,[])],
        block_unique_texts=len({tuple(x['sequence']) for x in matches}),
        block_object_count=len({w['object_id'] for x in matches for w in x['witnesses']}),
        block_matches=matches,marked_before_stem=marked_before_stem,separate211_before_stem=separate_before_stem,
        left_fragment_standalone_witnesses=[witness(r) for r in byseq.get(('387','66'),[])],
        inference='An independent recurring suffix makes local field scope plausible. It does not establish a boundary or make marked66 equivalent to65+211.',
        operation_cost='Requires one shared segmentation/boundary rule; no object-specific hidden meaning allowed',
        next_test='Compare complete336–89 field continuations across independently held object classes and linked faces; do not treat absent211–336 as a counterexample.')


def roof_transfer(sequences,byseq,alignments):
    """Selection-aware alternative accounting for the newly tested lattice."""
    ticks=dict(TICK_PAIRS);lattices=[];incomplete=[]
    for b,r in ROOF_PAIRS:
        if b in ticks and r in ticks:
            lattices.append(dict(base=b,roof=r,tick=ticks[b],roof_tick=ticks[r],
                implied_roof_pair=[ticks[b],ticks[r]]))
        else:
            incomplete.append(dict(base=b,roof=r,missing_declared_edges=[f'ticks({x})' for x in (b,r) if x not in ticks]))
    old=json.loads((ROOT/'research/data/semantic_search_20260906/modifier_context_pairs.json').read_text())
    observations=load_observations();folds=[]
    for lattice in lattices:
        a,b=lattice['implied_roof_pair']
        related=[s for s in sequences if str(a) in s or str(b) in s]
        partition=task_partition(observations,[witness(r)['row_id'] for s in related for r in byseq[s]],related)
        allowed=set(partition['train_row_ids'])
        training=[h for h in old if h['family']=='roof' and h['base']==lattice['base'] and h['unchanged_context_length']>=2
            and all(any(f"M77:{w['textnum']}:{w['sideline']}" in allowed for w in h[key]) for key in ['compact_witnesses','expanded_witnesses'])]
        groups=defaultdict(list)
        for h in training:groups[(h['extra'],h['side'])].append(h)
        trials=[]
        for marker in range(1,418):
            for side in ('before','after'):
                target=[]
                expansion=(str(marker),str(a)) if side=='before' else (str(a),str(marker))
                for s in related:
                    for i,t in enumerate(s):
                        if t!=str(b):continue
                        proposed=s[:i]+expansion+s[i+1:]
                        if len(s)-1>=2 and proposed in byseq:
                            target.append(dict(compact=s,expanded=proposed,
                                compact_witnesses=[witness(r) for r in byseq[s]],
                                expanded_witnesses=[witness(r) for r in byseq[proposed]],
                                unchanged_context=len(s)-1))
                if groups[(marker,side)] or target:
                    trials.append(dict(marker=marker,side=side,training_exact_contexts=len(groups[(marker,side)]),
                        training_context_signs=sum(h['unchanged_context_length'] for h in groups[(marker,side)]),
                        training_witness_pairs=groups[(marker,side)],
                        target_observed_exact_pairs=target,
                        target_not_observed_status='unknown; not negative'))
        folds.append(dict(lattice=lattice,marker_order_trials=834,training_min_context_signs=2,
            prior_exposure='Both target strings had already appeared separately in this campaign. Lattice hypothesis was proposed before dedicated pair search; test is retrospective.',
            alternatives=trials,excluded_object_ids=partition['excluded_object_ids'],
            conclusion='87 and102 each have two old exact training contexts. Only87 has an observed exact counterpart in the withheld marked lattice; unobserved102 alternative is not falsified.'))
    classes={}
    for model in ['fish211','roof87','roof102','fish211_roof87','fish211_roof102']:
        bynorm=defaultdict(list)
        for s in sequences:bynorm[normalize_sequence(s,model)].append(s)
        classes[model]=[dict(normal_form=n,members=[dict(sequence=s,witnesses=[witness(r) for r in byseq[s]]) for s in ss])
                       for n,ss in sorted(bynorm.items()) if len(ss)>1]
    return dict(declared_graphical_lattices=lattices,incomplete_lattices=incomplete,folds=folds,
        candidate_normal_form_classes=classes,
        interpretation='Normal-form classes are conditional outputs of the proposed operations, not observed synonymy or arithmetic equality.')


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=ROOT/'research/data/mahadevan_20260905/concordance_documents.json.gz')
    p.add_argument('--output',type=Path,default=Path(__file__).parent)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    rows,digest=load(args.input);clean=[r for r in rows if r['clean']]
    byseq=defaultdict(list)
    for r in clean:byseq[r['seq']].append(r)
    sequences=sorted(byseq);occurrence=defaultdict(list)
    for s in sequences:
        for i,t in enumerate(s):occurrence[t].append((s,i))
    alignments=enumerate_alignments(sequences,occurrence,byseq)
    write(args.output/'structured_alignments.json',alignments)
    rankings={f:rank_markers([h for h in alignments if h['family']==f]) for f in ['four_surrounding_strokes','roof','roof_on_marked_fish']}
    write(args.output/'structured_marker_rankings.json',rankings)
    literal=literal_alignments(sequences,byseq)
    write(args.output/'structured_literal_alignments.json',literal)
    transfer=[]
    observations=load_observations()
    for family,pairs in [('four_surrounding_strokes',TICK_PAIRS),('roof',ROOF_PAIRS)]:
        hh=[h for h in alignments if h['family']==family and h['marker'] is not None]
        for base,modified in pairs:
            related=[s for s in sequences if str(base) in s or str(modified) in s]
            target_ids=[witness(r)['row_id'] for s in related for r in byseq[s]]
            mask=task_partition(observations,target_ids,related)
            allowed=set(mask['train_row_ids'])
            training=[h for h in hh if h['base']!=base and all(any(w['row_id'] in allowed for w in h[k]) for k in ['compact_witnesses','expanded_witnesses'])]
            ranks=rank_markers(training)
            local=[h for h in hh if h['base']==base]
            winner=ranks[0]['marker'] if ranks else None
            transfer.append(dict(family=family,withheld_base=base,withheld_modified=modified,
                training_winner=winner,training_top5=ranks[:5],
                heldout_markers=rank_markers(local),
                heldout_winner_observed=any(h['marker']==winner for h in local),
                heldout_support=summarize_hits([h for h in local if h['marker']==winner]),
                training_alignments=len(training),excluded_object_ids=mask['excluded_object_ids'],
                scope='retrospective leave-base generalization of candidate marker search, not blind evidence'))
    write(args.output/'graphical_family_transfer.json',transfer)
    profiles,contradictions=occurrence_profiles(sequences,byseq)
    write(args.output/'operation_context_profiles.json',profiles)
    write(args.output/'exclusivity_counterexamples.json',contradictions)
    boundary=boundary_model(sequences,byseq)
    write(args.output/'boundary_predictions.json',boundary)
    spelling=spelling_search(sequences,byseq)
    write(args.output/'spelling_predictions.json',spelling)
    repair=boundary_repair(sequences,byseq)
    write(args.output/'local_boundary_repair.json',repair)
    roof=roof_transfer(sequences,byseq,alignments)
    write(args.output/'roof_lattice_predictions.json',roof)
    partial=partial_observations(rows,byseq,sequences)
    write(args.output/'partial_observation_predictions.json',partial)
    fish=[h for h in alignments if h['family']=='four_surrounding_strokes' and h['base'] in [59,65,67,70,72]]
    selected=[h for h in fish if h['marker']==211]
    summary=dict(input_sha256=digest,namespace='Mahadevan1977',
        strict_lines=len(clean),unique_texts=len(sequences),structured_search=dict(max_residual_edits=1,min_exact_context_anchors=2,
        anchor_rule='prefix and suffix aligned independently around the graphical base; no cross-base reordering'),
        fish211=summarize_hits(selected),fish_categorical_no_extra=summarize_hits([h for h in fish if h['marker'] is None]),
        all_family211=summarize_hits([h for h in alignments if h['marker']==211]),
        partial_marked_occurrences=len(partial),partial_occurrences_with_exact_observed_expansion=sum(bool(q['exact_matches_in_strict_observations']) for q in partial),
        fish_exclusivity_counterexamples=sum(q['fish_family'] for q in contradictions),
        literal_structured_matches=len(literal),literal_matching_composites=sorted({q['composite'] for q in literal}),
        roof_on_marked_fish_matches=len([h for h in alignments if h['family']=='roof_on_marked_fish']),
        boundary_prediction_total_bits=boundary['total_bits'],
        spelling_search_fold_winners={f['withheld_base']:f['winner'] for f in spelling['folds']},
        spelling_search_exact_form_reach=sum(f['exact_predicted_forms_observed'] for f in spelling['folds']),
        complete_roof_tick_lattices=len(roof['declared_graphical_lattices']),
        composed_normal_form_classes={m:len(c) for m,c in roof['candidate_normal_form_classes'].items()},
        status='competing writing-operation hypotheses; no sign meanings or sounds established')
    write(args.output/'summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
