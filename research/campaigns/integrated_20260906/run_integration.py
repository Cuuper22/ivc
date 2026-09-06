#!/usr/bin/env python3
"""Execute cross-route predictions from frozen candidate writing operations.

Joint targets are original field-symbol codes and companion cup-stroke counts.
No route score is multiplied into another; all models see the same observations.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import json, math, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'research/tools'))
from semantic_transducer_search import load, TICK_PAIRS

MODELS={
    'categorical_identity': {'pairs':[], 'marker':None,'rule_bits':0},
    'fish211': {'pairs':TICK_PAIRS[:5],'marker':'211','rule_bits':11},
    'all_four_stroke211': {'pairs':TICK_PAIRS,'marker':'211','rule_bits':12},
    'fish342': {'pairs':TICK_PAIRS[:5],'marker':'342','rule_bits':11},
    'fish_unmarked_category': {'pairs':TICK_PAIRS[:5],'marker':None,'rule_bits':2},
    'fish_roof87': {'pairs':[], 'marker':None,'rule_bits':11,
        'overrides':{'65':['87','59'],'66':['87','60']}},
    'fish_roof87_tick211': {'pairs':TICK_PAIRS[:5], 'marker':'211','rule_bits':22,
        'overrides':{'65':['87','59'],'66':['87','59','211']}},
    'fish_roof102_tick211': {'pairs':TICK_PAIRS[:5], 'marker':'211','rule_bits':22,
        'overrides':{'65':['102','59'],'66':['102','59','211']}},
}


def normalize(seq, model):
    cfg=MODELS[model]
    mapping={str(m):[str(b)]+([cfg['marker']] if cfg['marker'] else []) for b,m in cfg['pairs']}
    mapping.update(cfg.get('overrides',{}))
    return tuple(t for x in seq for t in mapping.get(str(x),[str(x)]))


def site(row):
    code=str(row['textnum'])[0]
    return {'1':'M','2':'M','3':'M','4':'H','5':'H','6':'C','7':'L','8':'K','9':'other'}.get(code,'unresolved')


def records(rows):
    faces=defaultdict(list)
    for r in rows:
        faces[(r['textnum'],int(r['sideline'])//10)].append(r)
    out=[]
    for rr in faces.values():
        # The B route handles multiline structures separately. Do not fabricate
        # inter-line adjacency to extend a single-line writing rule here.
        if len(rr)!=1 or not rr[0]['clean']: continue
        r=rr[0]
        if r['fs80'] not in (0,999):
            out.append({'channel':'field_symbol_code','object':r['textnum'],
                'row_id':f"M77:{r['textnum']}:{r['sideline']}",
                'sequence':r['seq'],'context':(site(r),r['inscobj']),
                'target':str(r['fs80']), 'source':'raw fs80; includes symbolic object shape'})
    paired=json.loads((ROOT/'research/data/mahadevan_20260905/paired_objects.json').read_text())
    for p in paired:
        f=p['front']
        out.append({'channel':'companion_cup_strokes','object':p['textnum'],
            'row_id':f"M77:{p['textnum']}:{f['sideline']}",
            'sequence':tuple(f['tokens_raw']), 'context':(site(f),f['inscobj']),
            'target':str(p['long_stroke_count']), 'source':'reused frozen strict paired objects'})
    return out


def distribution(train, target, model, alphabet):
    # Count each exact expression/target/context type once, even when repeated
    # on several objects. Physical-object weighted losses are reported separately.
    types={(r['sequence'],r['target'],r['context']) for r in train}
    global_c=Counter(t for s,t,c in types)
    local=Counter(t for s,t,c in types if c==target['context'])
    prior={t:(global_c[t]+0.5)/(sum(global_c.values())+0.5*len(alphabet)) for t in alphabet}
    background={t:(local[t]+2*prior[t])/(sum(local.values())+2) for t in alphabet}
    key=normalize(target['sequence'],model)
    matched=[(s,t,c) for s,t,c in types if normalize(s,model)==key]
    counts=Counter(t for s,t,c in matched)
    # Sharing across observed metadata contexts is explicitly part of the model;
    # the background already conditions on site and object type.
    probs={t:(counts[t]+2*background[t])/(sum(counts.values())+2) for t in alphabet}
    return probs,matched


def evaluate(rows, rr, model):
    predictions=[]
    channels=defaultdict(list)
    for r in rr: channels[r['channel']].append(r)
    for channel, records in channels.items():
        # Remove every object containing the target complete expression, on ANY
        # strict line, even if a companion face would otherwise enter training.
        aliases=defaultdict(set)
        for row in rows:
            if row['clean']: aliases[row['seq']].add(row['textnum'])
        # Catalogue field-code alphabet is fixed across candidates and folds;
        # target frequencies never enter training. 1..5 graphical stroke outcomes
        # likewise come from the pre-existing codebook, not held target labels.
        alphabet=([str(i) for i in range(1,1000)] if channel=='field_symbol_code'
                  else [str(i) for i in range(1,6)])
        for target in records:
            blocked=aliases[target['sequence']]|{target['object']}
            train=[r for r in records if r['object'] not in blocked]
            probs,matched=distribution(train,target,model,alphabet)
            predictions.append({'channel':channel,'row_id':target['row_id'],'object':target['object'],
                'source_sequence':target['sequence'],'normalized':normalize(target['sequence'],model),
                'context':target['context'],'observed_target':target['target'],
                'predicted_target':max(probs,key=probs.get),
                'nll_bits':-math.log2(probs[target['target']]),
                'alternative_spellings_in_train':sorted({s for s,t,c in matched}),
                'alternative_target_codes_in_train':sorted({t for s,t,c in matched}),
                'excluded_objects':sorted(blocked),
                'exposure':'retrospective; candidate operations already inspected corpus'})
    summary=[]
    for channel in channels:
        pp=[p for p in predictions if p['channel']==channel]
        types=defaultdict(list)
        for p in pp:
            types[(tuple(p['source_sequence']),p['observed_target'],tuple(p['context']))].append(p)
        type_loss=sum(sum(p['nll_bits'] for p in g)/len(g) for g in types.values())
        summary.append({'model':model,'channel':channel,'objects_or_faces':len(pp),
            'distinct_expression_target_context_types':len(types),
            'object_weighted_nll_bits':sum(p['nll_bits'] for p in pp),
            'type_weighted_nll_bits':type_loss,'rule_bits':MODELS[model]['rule_bits'],
            'type_weighted_total_bits':type_loss+MODELS[model]['rule_bits'],
            'cross_spelling_predictions':sum(bool(p['alternative_spellings_in_train']) for p in pp),
            'correct':sum(p['predicted_target']==p['observed_target'] for p in pp)})
    return summary,predictions


def run():
    out=HERE/'integration';out.mkdir(exist_ok=True)
    rows,digest=load(ROOT/'research/data/mahadevan_20260905/concordance_documents.json.gz')
    rr=records(rows)
    summaries=[];predictions={}
    for model in MODELS:
        s,p=evaluate(rows,rr,model)
        summaries.extend(s);predictions[model]=p
    # Keep only informative changes to avoid redundant 5x full-corpus dumps.
    base={p['row_id']+'|'+p['channel']:p for p in predictions['categorical_identity']}
    contrasts=[]
    for model,pp in predictions.items():
        if model=='categorical_identity':continue
        for p in pp:
            b=base[p['row_id']+'|'+p['channel']]
            if p['alternative_spellings_in_train']:
                contrasts.append(p|{'model':model,'identity_nll_bits':b['nll_bits'],
                    'gain_bits':b['nll_bits']-p['nll_bits']})
    # One joint code cost per candidate, with channels visible separately. We
    # do not sum A/B/C/D reports, which often reuse these same inscriptions.
    joint=[]
    for model in MODELS:
        ss=[s for s in summaries if s['model']==model]
        joint.append({'model':model,'channel_data_bits':{s['channel']:s['type_weighted_nll_bits'] for s in ss},
            'rule_bits_once':MODELS[model]['rule_bits'],
            'total_bits':sum(s['type_weighted_nll_bits'] for s in ss)+MODELS[model]['rule_bits'],
            'interpretation':'conditional composite descriptive score; channels may share production causes, not independent confirmation'})
    packet={'source_sha256':digest,'models':MODELS,'summaries':summaries,'joint':joint,
        'evaluation':'leave-complete-expression and all aliases/objects out; metadata background',
        'prior_exposure':'retrospective; no new blind discovery test',
        'decoding_scope':'no target word, pronunciation, or absolute unit is supplied by this test',
        'code_costs':'relative descriptive costs for fixed prior graphical families, not calibrated Bayes factors',
        'field_symbols':'raw catalogue field codes include motifs, uncertain animals and symbolic object shapes; no literal lexical labels inferred'}
    for name,value in [('summary.json',packet),('cross_route_predictions.json',contrasts)]:
        (out/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'joint':joint,'cross_route_predictions':len(contrasts)},indent=2))


if __name__=='__main__':run()
