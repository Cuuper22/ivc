#!/usr/bin/env python3
"""Reconstructed conditional ABC systems fitted on original channels once.

Shared spelling program is selected against text, motif and cup observations.
Continuous channel parameters are fitted conditionally for each program; their
joint optimum over this finite candidate set need not be the A-only optimum.
D supplies a separately reported conditional lexical prior, never another text
likelihood. All task masks are frozen before fitting and artifacts are cached
only with matching code and input fingerprints.
"""
import argparse, copy, importlib.util, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'shared'))
from common import load_rows, build_masks, digest, write

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

A=module('grammar',HERE/'route_a/grammar.py')
B=module('referent',HERE/'route_b/model.py')
C=module('counts',HERE/'route_c/run.py')

def transformed_b(examples,program):
    out=copy.deepcopy(examples)
    for e in out:
        e['lines']=[A.transform(s,program) for s in e['lines']]
        e['family']=B.stable(e['lines'])
    return out

def transformed_c(records,program):
    out=copy.deepcopy(records)
    for r in out:
        r['lines']=[A.transform(s,program) for s in r['lines']]
        # This is a candidate field representation. Source identity and masks
        # remain keyed by the ORIGINAL raw spelling.
        r['front']=json.dumps(r['lines']);r['raw_front']=json.dumps(r['lines'],separators=(',',':'))
    return out

def datasets(mask, rows, examples, counts):
    train_ids=set(mask['train_row_ids']);target_ids=set(mask['target_row_ids'])
    excluded=set(mask['excluded_object_ids'])
    target_objects={r['object_id'] for r in rows if r['row_id'] in target_ids}
    cup_ids={s['row_id'] for r in counts for s in r['cup_rows']}
    # Count source tokens are scored exactly once in the C channel.
    atr=[r for r in rows if r['row_id'] in train_ids and r['row_id'] not in cup_ids]
    ate=[r for r in rows if r['row_id'] in target_ids and r['row_id'] not in cup_ids]
    btr=[e for e in examples if not excluded.intersection(e['object_ids']) and not cup_ids.intersection(e['row_ids'])]
    bte=[e for e in examples if target_objects.intersection(e['object_ids']) and not cup_ids.intersection(e['row_ids'])]
    ctr=[r for r in counts if not excluded.intersection(r['sources'])]
    cte=[r for r in counts if target_objects.intersection(r['sources'])]
    return atr,ate,btr,bte,ctr,cte

def channel_bits(am,bm,cm,ar,br,cr):
    return {'text':A.score(am,ar)['data_bits'],'motif':B.score(bm,br)['data_bits'],'cup':C.score(cm,cr)}

def run_abc(task_filter=None):
    rows=load_rows();examples=B.build_examples();counts=C.load_records()
    mp=HERE/'shared/masks.json';masks=json.loads(mp.read_text()) if mp.exists() else build_masks(rows)
    codes={str(p.relative_to(HERE)):digest(p.read_text()) for p in [HERE/'run_joint.py',HERE/'route_a/grammar.py',HERE/'route_b/model.py',HERE/'route_c/run.py',HERE/'shared/common.py']}
    summaries=[]
    for task,mask in masks['masks'].items():
        if task_filter and task!=task_filter:continue
        folder=HERE/'joint'/task;folder.mkdir(parents=True,exist_ok=True)
        atr,ate,btr,bte,ctr,cte=datasets(mask,rows,examples,counts)
        signature=digest([codes,mask,atr,btr,ctr]);all_candidates=[]
        for program in A.PROGRAMS:
            bt=transformed_b(btr,program);be=transformed_b(bte,program)
            ct=transformed_c(ctr,program);ce=transformed_c(cte,program)
            bmodels=[B.fit_model(bt,n) for n in B.MODELS]
            bm=min(bmodels,key=lambda m:B.score(m,bt)['data_bits']+m['parameter_bits']+m['rule_bits'])
            cm=C.fit(ct)
            for roles in (1,2,3):
                path=folder/(program+'__r'+str(roles)+'.json')
                if path.exists() and (saved:=json.loads(path.read_text())).get('input_digest')==signature:
                    all_candidates.append(saved);continue
                am=A.fit(atr,program,roles,max_iter=120)
                if not am['converged']:am=A.fit(atr,program,roles,max_iter=350)
                tr=channel_bits(am,bm,cm,atr,bt,ct);te=channel_bits(am,bm,cm,ate,be,ce)
                penalties={'grammar_parameters':am['parameter_bits'],'graphical_program_once':am['rule_bits'],'motif_parameters':bm['parameter_bits'],'motif_model':bm['rule_bits'],'count_program_and_parameters':cm['complexity_bits']}
                saved={'schema':'ivc.reconstructed.joint.v1','task':task,'program':program,'roles':roles,'input_digest':signature,'code_digests':codes,'mask_digest':digest(mask),'train_channel_bits':tr,'held_channel_bits':te,'penalties':penalties,'train_objective_bits':sum(tr.values())+sum(penalties.values()),'held_data_bits':sum(te.values()),'models':{'a':am,'b':bm,'c':cm},'mask_sizes':{'text_train':len(atr),'text_target':len(ate),'motif_train':len(bt),'motif_target':len(be),'cup_train':len(ct),'cup_target':len(ce)},'factorization':'P(raw text excluding cup lines|A) P(raw motif|text,context,A,B) P(cup count|front,A,C). Conditional channel fit; not independent confirmations.','provenance':'executed reconstruction; retrospective targets'}
                write(path,saved);all_candidates.append(saved)
            print(task,program,'saved',flush=True)
        winner=min(all_candidates,key=lambda m:m['train_objective_bits'])
        local=min(all_candidates,key=lambda m:m['models']['a']['total_bits'])
        baseline=min((m for m in all_candidates if m['program']=='identity'),key=lambda m:m['train_objective_bits'])
        result={'task':task,'fitted_candidates':len(all_candidates),'selected':winner['program']+'__r'+str(winner['roles']),'a_only_selected':local['program']+'__r'+str(local['roles']),'held_channel_bits':winner['held_channel_bits'],'held_data_bits':winner['held_data_bits'],'baseline_held_data_bits':baseline['held_data_bits'],'gain_bits':baseline['held_data_bits']-winner['held_data_bits'],'mask_sizes':winner['mask_sizes'],'all_grammar_fits_converged':all(m['models']['a']['converged'] for m in all_candidates)}
        write(folder/'selected.json',winner);write(folder/'summary.json',result);summaries.append(result)
    result={'status':'executed_reconstructed_rerun','tasks':summaries,'fitted_candidates':sum(s['fitted_candidates'] for s in summaries),'no_new_accepted_readings':True,'mask_digest':masks['mask_digest'],'scope':'Finite shared spelling, latent role count, referent and numerical program selection optimized on joint original observations. All channel parameters refitted per mask. D coupling is separate.','source_sha256':rows[0]['source_sha256']}
    if not task_filter:write(HERE/'joint/summary.json',result)
    print(json.dumps(result),flush=True)

def run_d(task_filter=None):
    D=module('linguistic',HERE/'route_d/run_completion_d.py')
    rows=load_rows();examples=B.build_examples();counts=C.load_records();masks=json.loads((HERE/'shared/masks.json').read_text())['masks'];summary=[]
    def drows(ar,p):
        out=[]
        for r in ar:
            if not r['strict']:continue
            v=dict(r);v['tokens_stored']=A.transform(r['tokens_stored'],p);out.append(v)
        return out
    def energy(dm,rr,p):
        return sum(D.lexical_residual_bits(dm,s) for s in A.sequences(drows(rr,p)))
    for task,mask in masks.items():
        if task_filter and task!=task_filter:continue
        folder=HERE/'joint'/task;atr,ate,*_=datasets(mask,rows,examples,counts)
        cand=[json.loads(p.read_text()) for p in folder.glob('*__r*.json')]
        base=min(cand,key=lambda c:c['train_objective_bits'])
        for language in ('tamil','sanskrit'):
            current=base;models=[D.fit_system(drows(atr,current['program']),language,o) for o in ('append','prepend')]
            dm=min(models,key=lambda m:energy(m,atr,current['program'])+D.parameter_bits(m))
            objective=current['train_objective_bits']+energy(dm,atr,current['program'])+D.parameter_bits(dm);trace=[]
            for iteration in range(6):
                trial=min(cand,key=lambda c:c['train_objective_bits']+energy(dm,atr,c['program']))
                trial_dm=D.fit_system(drows(atr,trial['program']),language,dm['orientation'])
                new=trial['train_objective_bits']+energy(trial_dm,atr,trial['program'])+D.parameter_bits(trial_dm)
                accepted=new<objective-1e-8
                trace.append({'iteration':iteration,'from':current['program'],'to':trial['program'],'previous_objective':objective,'trial_objective':new,'accepted':accepted})
                if not accepted:break
                current,dm,objective=trial,trial_dm,new
            frozen=digest([current,dm]);held_prior=energy(dm,ate,current['program'])
            # Raw observation predictions and lexical prior are distinct results.
            output={'status':'executed_reconstructed_rerun','task':task,'language':language,'selected':current['program']+'__r'+str(current['roles']),'baseline_abc_selected':base['program']+'__r'+str(base['roles']),'trace':trace,'train_objective_with_lexical_prior':objective,'held_original_channel_bits':current['held_channel_bits'],'held_original_data_gain_vs_abc':base['held_data_bits']-current['held_data_bits'],'held_lexical_prior_bits':held_prior,'linguistic_model':dm,'frozen_model_digest':frozen,'post_evaluation_model_digest':digest([current,dm]),'mask_digest':digest(mask),'no_held_refit':True,'evidence_statement':'D is a conditional lexical prior. Its code cost is neither another text observation nor independent sound correctness. Tamil/Sanskrit dictionary coverage differs.','worked_decodings':[{'raw':list(map(str,s)),'conditional':D.decode(dm,A.transform(s,current['program']))} for s in A.sequences(ate) if any(str(x) in ('59','60','65','66','70','71','211') for x in s)][:40]}
            write(HERE/'joint/linguistic_coupling'/(task+'__'+language+'.json'),output);summary.append({k:output[k] for k in ['task','language','selected','baseline_abc_selected','held_original_data_gain_vs_abc','held_lexical_prior_bits']});print('ABCD',task,language,'saved',flush=True)
    if not task_filter:write(HERE/'joint/linguistic_coupling/summary.json',{'status':'executed_reconstructed_rerun','systems':summary,'completed_systems':len(summary),'new_accepted_readings':0})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['abc','d'],default='abc');parser.add_argument('--task');args=parser.parse_args()
    run_abc(args.task) if args.stage=='abc' else run_d(args.task)
