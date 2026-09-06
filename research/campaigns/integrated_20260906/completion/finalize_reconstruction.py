#!/usr/bin/env python3
"""Consolidate only executed reconstructed research and its retained evidence."""
import argparse,ast,collections,gzip,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAM=HERE.parent
sys.path.insert(0,str(HERE/'shared'))
from common import load_rows,write,digest,raw_key

def read(p):return json.loads((HERE/p).read_text())

def summarize():
    tasks=list(read('shared/masks.json')['masks'])
    summaries=[read('joint/'+t+'/summary.json') for t in tasks]
    write(HERE/'joint/summary.json',{'status':'executed_reconstructed_rerun','tasks':summaries,'fitted_candidates':sum(x['fitted_candidates'] for x in summaries),'new_accepted_readings':0,'factorization':'conditional raw text, motif, and cup likelihoods; observed count source lines removed from text channel; shared spelling selection on joint original observations'})
    systems=[read('joint/linguistic_coupling/'+t+'__'+l+'.json') for t in tasks for l in ['tamil','sanskrit']]
    keys=['task','language','selected','baseline_abc_selected','held_original_data_gain_vs_abc','held_lexical_prior_bits']
    write(HERE/'joint/linguistic_coupling/summary.json',{'status':'executed_reconstructed_rerun','completed_systems':len(systems),'systems':[{k:s[k] for k in keys} for s in systems],'new_accepted_readings':0,'interpretation':'Conditional linguistic prior energies reported separately from original observed-data predictive scores. No known Indus phonetic targets supplied.'})

def contracts():
    candidates=[]
    for route in ['a','b']:
        for c in read('route_'+route+'/candidates.json'):
            c=dict(c);c['id']='REC-'+c['id'];c['reconstruction_origin']='rerun or explicitly retained prior conditional hypothesis';candidates.append(c)
    def candidate(id,route,kind,rule,paths,prereq,limits,parameters):
        return {'id':id,'route':route,'status':'conditional','claim_type':kind,'rule':rule,'namespace':'Mahadevan1977','context':'Retrospective frozen catalogue; object/copy exclusions; separate source namespaces','prerequisites':prereq,'support':paths,'contradictions':limits,'alternatives':['independent categorical description','unanchored latent class relabeling'],'parameters':parameters,'complexity':'Explicit parameter and finite program penalties retained in source models','predictions':paths,'source_paths':paths,'prior_exposure':'entire corpus and earlier results already inspected; no pristine blind claim'}
    cs=read('route_c/summary.json')
    candidates.append(candidate('REC-C-PROGRAM-FAMILY','C','operational_meaning','Finite joint field/value/operator program family; each parameter setting and outcome retained in program_search.json',['completion/route_c/program_search.json','completion/route_c/frozen_predictions.json','completion/route_c/observational_equivalence_classes.json'],['candidate numerical field and value interpretation'],['Independent reverse-count distribution wins reconstructed comparison; no physical unit or number meaning identified'],{'programs':cs['programs']}))
    candidates.append(candidate('REC-C-SUFFIX-SCOPE','C','structural_constraint','Retained suffix remains compatible with local and larger-field scope',['completion/route_c/retained_suffix_experiment.json'],['conditional roof87 graphical operation'],['unknown prefix in2275 cannot be completed; no independently identified scope'],{}))
    for language in ['tamil','sanskrit','anonymous','nonphonetic']:
        for orientation in ['append','prepend']:
            path=f'completion/route_d/{language}_{orientation}.json'
            candidates.append(candidate('REC-D-'+language+'-'+orientation,'D','sound_assignment',{'language':language,'orientation':orientation,'executable':'completion/route_d/run_completion_d.py'},[path,'completion/route_d/frozen_predictions.json'],['conditional graphical pairs','available comparative vocabulary','no positive independent semantic anchor'],['symbol renaming does not identify sounds','silent classifier role can beat phonetic role','unread70 remains unresolved'],read('route_d/'+language+'_'+orientation+'.json').get('mapping',{})))
    candidates.append(candidate('REC-B-SPECIES-EXCLUSION','B','structural_constraint','Conditionally equal complete expanded spellings cannot universally name the literal pictured animal species',['completion/sources/1380_2452_adjudication.json'],['65→87,59','71→70,211','normal-form equality is linguistic identity'],['raw spellings differ; category, institution, person or production role remain possible'],{}))
    write(HERE/'candidate_ledger.json',{'status':'reconstructed; no promotion','candidates':candidates,'new_accepted_readings':0})
    nodes=[{'id':'OBS','kind':'original observations'},{'id':'LEX','kind':'held comparative lexicons'},{'id':'SRC','kind':'original source entries'}]+[{'id':c['id'],'kind':'conditional candidate'} for c in candidates]+[{'id':'ABC','kind':'joint original-observation model'},{'id':'ABCD','kind':'conditional linguistic prior coupling'}]
    edges=[{'from':'OBS','to':c['id'],'kind':'uses same original evidence'} for c in candidates]
    edges += [{'from':'LEX','to':c['id'],'kind':'conditional vocabulary'} for c in candidates if c['route']=='D']
    edges += [{'from':'SRC','to':'REC-B-SPECIES-EXCLUSION','kind':'source code distinction'},{'from':'OBS','to':'ABC','kind':'one raw likelihood per declared channel'},{'from':'ABC','to':'ABCD','kind':'shared model alternative'},{'from':'LEX','to':'ABCD','kind':'lexical prior, not additional text likelihood'}]
    write(HERE/'claim_dependencies.json',{'nodes':nodes,'edges':edges,'evidence_policy':'Shared-source descendants do not constitute independent confirmation. B exclusions supply no positive lexical anchor; conditional outputs never return as new observed facts.'})

def docs():
    a=read('route_a/summary.json');b=read('route_b/summary.json');c=read('route_c/summary.json');d=read('route_d/summary.json');j=read('joint/summary.json');ling=read('joint/linguistic_coupling/summary.json')
    write(HERE/'novelty.json',{'prior_scholarship':'Original source codebook and pictures, paired-face descriptions, and published lexical forms are prior material.','retained_formalizations':'Original checkpoint spelling-alignment and cross-face counterexamples retained with prior exposure.','new_reconstruction':'Ordered raw normalized latent-role grammar, fitted referent/numerical/mixed-script candidates, joint frozen comparisons, source-linked exclusions.','novelty_priority':'Not established by held literature coverage.','new_translation':False,'new_sound_correspondence':False,'accepted_ledger_changed':False})
    queue=[{'id':'NEXT-ORDER-SCOPE','question':'Does a scope boundary supported by a multi-role grammar improve predicting the retained suffix around roof-expanded fish beyond whole-expression categorical models?','source_rows':['M77:2275','M77:1008','M77:1147'],'alternatives':['local graphical spelling change','larger anonymous field','numerical field with independently unanchored scope'],'completed_precursor':'route_c/retained_suffix_experiment.json','next_executable':'python completion/next_order_comparison.py','reason':'The retained suffix alone does not identify scope; reconstructed latent grammar can disagree with the earlier proposed boundary.','status':'next experiment preserved; not executed in this reconstruction'},{'id':'REOPEN-PHONETICS','question':'Can independently grounded held semantic constraints distinguish named sounds from classifier/anonymous relabelings?','current_result':'No positive lexical anchor; current sound models are conditional and language vocabularies differ.','reopening_condition':'A source-bound anchor not generated by the same phonetic hypothesis.'}]
    write(HERE/'experiment_queue.json',queue)
    write(HERE/'continuation.json',{'status':'reconstructed research actions executed; decipherment unresolved','active_models':'joint/*/selected.json and joint/linguistic_coupling/*.json','next_experiment':queue[0],'work_continues_unattended':False,'new_accepted_readings':0})
    (HERE/'WORKED_EXAMPLES.md').write_text('''# Worked reconstruction examples

## Conditional shared spelling, distinct pictured animals

Mahadevan1380 has raw `65 70 211`;2452 has raw `87 59 71`. Under the proposed rules `65→87 59` and `71→70 211`, both expand to `87 59 70 211`. Original printed entries label the pictures25 (composite animal) and01 (unicorn). If the expanded spelling represents the same entire linguistic expression, that expression cannot universally name the literal pictured species. Category or production-context explanations remain possible. No word or pronunciation follows. See sources/1380_2452_adjudication.json and its four original page images.

## Retained suffix and unresolved scope

The2275/1008 contrast retains `67 336 89 211` under the proposed local spelling transformation.2275’s unknown prefix is retained as unknown, never copied from1008. Local fish-root, larger categorical-field and larger numerical-field scope remain compatible. The three-role reconstructed grammar’s boundary probabilities are separately retained in route_a/latent_segmentation_alternatives.json; a recurring suffix alone cannot fix the boundary.

## Numerical prediction versus numerical meaning

The reconstructed search compares explicit field parses, shared value assignments, operators, multipliers and offsets with categorical and independent reverse-count alternatives. Identical fronts occur with several reverse counts, contradicting deterministic equal-face interpretations in those contexts. An independent count distribution wins the declared frozen comparisons; this does not establish a unit or rule of arithmetic. Exact records and predicted distributions are in route_c/frozen_predictions.json.

## Conditional sound assignment and unread text

The Tamil and Sanskrit searches alternate shared roots, affixes, segmentation and a global marker role. Named-language phonetic competitors remain available even when a silent classifier is preferred. Their forms are conditional hypotheses derived from the held lexicons. Sign70 stays unread. cross_route_predictions.json compares ordinary decoding with a losing numerical-role hypothesis and records the effect without treating it as new evidence. The alphabet-renaming control exposes the absence of an independent sound anchor.

All examples reuse the original observation strings. Detailed lexical parses and their contradictory alternatives remain in route_d and joint/linguistic_coupling.
''')
    table='\n'.join(f"| {x['task']} | {x['selected']} | {x['gain_bits']:.4f} |" for x in j['tasks'])
    (HERE/'README.md').write_text(f'''# Reconstructed completion pass

The earlier completion files were lost after an unsuccessful push. This package rebuilds executable research from Git checkpoint0ad84ef and held sources. These are newly run results, not a byte-for-byte restoration. RECOVERY.md preserves what the conversation recorded about the lost pass separately.

The reconstructed execution includes27 writing-operation/latent-role candidates, six matched graphical controls, nine referent/context models, {c['programs']} numerical programs, eight mixed/rival linguistic systems and three optimized phonetic alternatives. Joint fitting completed {j['fitted_candidates']} ABC candidates across seven frozen tasks, then {ling['completed_systems']} language-conditioned joint systems. No new reading or language identification is accepted.

| Frozen task | Training-selected joint model | Gain over identity, bits |
|---|---|---:|
{table}

Negative gain means the selected graphical system predicts the held original observations worse. Lexical-prior energies are reported separately and cannot identify a language from dictionaries of different coverage.

Run `python completion/run_completion.py --stage verify` from the campaign directory to check the retained execution package. Use `--stage all` to execute the whole reconstructed campaign, or individual stages. All source observations remain fixed. The continuation state names the next unexecuted discriminating experiment without implying unattended work.

Key files: candidate_ledger.json, claim_dependencies.json, WORKED_EXAMPLES.md, audit/task_status.json, verification.json, experiment_queue.json and continuation.json. The original campaign artifacts outside completion remain available as the recovered checkpoint, including the earlier exact structured alignments.
''')

def verify():
    checks=[];rows=load_rows();masks=read('shared/masks.json')['masks']
    raw=gzip.decompress((CAM.parents[1]/'data/mahadevan_20260905/concordance_documents.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==rows[0]['source_sha256']
    checks.append('immutable raw corpus digest')
    for name,m in masks.items():
        blocked=set(m['excluded_object_ids']);ids=set(m['train_row_ids']);patterns={tuple(x) for x in m['exact_raw_patterns']}
        assert not any(r['row_id'] in ids and (r['object_id'] in blocked or raw_key(r) in patterns) for r in rows)
    checks.append('seven whole-object and raw-pattern alias masks')
    import numpy as np
    count=0
    for name,m in masks.items():
        models=[json.loads(p.read_text()) for p in (HERE/'joint'/name).glob('*__r*.json')];assert len(models)==27
        for x in models:
            a=x['models']['a'];assert a['converged'];assert np.max(np.abs(np.array(a['emission']).sum(1)-1))<1e-8
            assert np.max(np.abs(np.array(a['transition']).sum(1)-1))<1e-8
            assert x['mask_digest']==digest(m)
            assert abs(sum(x['held_channel_bits'].values())-x['held_data_bits'])<1e-7
        count+=len(models)
    checks.append('189 fitted normalized frozen ABC systems and channel accounting')
    ds=[json.loads(p.read_text()) for p in (HERE/'joint/linguistic_coupling').glob('*__*.json')];assert len(ds)==14
    for s in ds:
        assert s['no_held_refit'] and s['frozen_model_digest']==s['post_evaluation_model_digest']
    assert read('route_d/summary.json')['unread_70']
    checks.append('14 frozen linguistic couplings; unread70 retained')
    assert len(read('route_a/full_models.json'))==27 and len(read('route_a/matched_controls.json'))==6
    assert read('route_c/summary.json')['programs']==len(read('route_c/program_search.json'))
    assert read('sources/summary.json')['witnesses']==5858
    assert read('cross_route_predictions.json')['changed_decodings']>0
    checks.append('executed route searches, controls, source adjudication and C-to-D exchange')
    ledger=read('candidate_ledger.json');required=json.loads((CAM/'shared/candidate_contract.json').read_text())['required_fields']
    assert all(set(required)<=set(c) for c in ledger['candidates'])
    graph=read('claim_dependencies.json');degree={x['id']:0 for x in graph['nodes']};adj=collections.defaultdict(list)
    for e in graph['edges']:degree[e['to']]+=1;adj[e['from']].append(e['to'])
    todo=[n for n,d in degree.items() if d==0];seen=[]
    while todo:
        n=todo.pop();seen.append(n)
        for t in adj[n]:
            degree[t]-=1
            if not degree[t]:todo.append(t)
    assert len(seen)==len(degree);assert ledger['new_accepted_readings']==0
    checks.append('candidate contracts, acyclic dependencies and no unsupported promotions')
    for p in HERE.rglob('*.py'):ast.parse(p.read_text(),str(p))
    audit=read('audit/task_status.json')
    assert audit['task_count']==53 and audit['clause_count']==217 and not audit['pending_tasks']
    checks.append('Python syntax and original task audit present')
    result={'status':'passed','checks':checks,'check_count':len(checks),'joint_candidates':count,'linguistic_systems':len(ds),'source_sha256':rows[0]['source_sha256'],'provenance':'reconstructed execution; old exact outputs not recoverable'}
    write(HERE/'verification.json',result);print(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage',choices=['consolidate','verify'],default='consolidate');args=p.parse_args()
    if args.stage=='verify':verify()
    else:summarize();contracts();docs()
