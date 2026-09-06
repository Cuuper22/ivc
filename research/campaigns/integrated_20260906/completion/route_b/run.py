#!/usr/bin/env python3
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from model import *
import importlib.util

def write(n,x):(HERE/n).write_text(json.dumps(x,indent=2)+'\n')
def main():
 examples=build_examples();write('examples.json',examples);summary={};allpred=[]
 for name in MODELS:
  model=fit_model(examples,name);write(name+'.model.json',model);folds=[]
  for fold in range(5):
   test=[e for e in examples if int(e['family'][:12],16)%5==fold];blocked={o for e in test for o in e['object_ids']};train=[e for e in examples if int(e['family'][:12],16)%5!=fold and not blocked.intersection(e['object_ids'])];m=fit_model(train,name);write(f'{name}.fold{fold}.json',m);s=score(m,test)
   folds.append(dict(fold=fold,targets=len(test),data_bits=s['data_bits'],parameter_bits=m['parameter_bits'],rule_bits=m['rule_bits']));allpred += [dict(model=name,evaluation='family_holdout',fold=fold,**r) for r in s['records']]
  transfers=[]
  for medium in sorted({e['medium'] for e in examples}):
   test=[e for e in examples if e['medium']==medium];families={e['family'] for e in test};blocked={o for e in test for o in e['object_ids']};train=[e for e in examples if e['medium']!=medium and e['family'] not in families and not blocked.intersection(e['object_ids'])]
   if not train or not test:continue
   m=fit_model(train,name);write(f'{name}.medium{medium}.json',m);s=score(m,test);transfers.append(dict(medium=medium,targets=len(test),training=len(train),data_bits=s['data_bits']));allpred += [dict(model=name,evaluation='medium_transfer',medium=medium,**r) for r in s['records']]
  summary[name]=dict(folds=folds,family_holdout_bits=sum(f['data_bits'] for f in folds),medium_transfer=transfers,full_parameter_bits=model['parameter_bits'])
  print(name,summary[name]['family_holdout_bits'],flush=True)
 write('predictions.json',allpred);write('competition.json',summary)
 # Re-execute surviving source-grounded network and contrasts in this output directory.
 spec=importlib.util.spec_from_file_location('original_b',CAMPAIGN/'route_b/run_route_b.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.HERE=HERE
 rows,faces,objects=b.load();tg,sl,ce,stats=b.network(faces,objects);types,bt=b.copper_models(ce,sl);stats.update(b.decisive_tests(rows,faces,objects,types,bt))
 # Original typology is a held derived observation, preserved separately and labeled.
 typ=json.loads((CAMPAIGN/'route_b/published_copper_type_network.json').read_text());typ['recovery_status']='Recovered checkpoint source-linked transcription; not independently reannotated in this reconstruction';write('published_copper_type_network.json',typ)
 stats.update(examples=len(examples),models=len(MODELS),family_and_medium_fits=sum(len(v['folds'])+len(v['medium_transfer']) for v in summary.values()),reconstruction='Executed anew from recovered checkpoint; no exact numerical recovery claimed',lexical_anchors=0,sound_anchors=0)
 write('summary.json',stats)
 write('conditional_alignment_contrast.json',dict(objects=[{'object_id':o,'rows':[r for r in rows if r['object_id']==o]} for o in ['M77:1380','M77:2452']],prior_summary='Composite animal versus unicorn was reported in lost image adjudication; requires source image reinspection. Text equality depends on Route A graphical expansion, not raw identity.',status='conditional dependency only; no recovered annotation asserted'))
 lines=['# Route B reconstruction','',f"Executed {len(MODELS)} motif models on {len(examples)} independent expression/motif/context types. Five expression-family folds and held-medium transfer also remove complete target objects and exact expression aliases.",'','| Model | Held-family bits |','|---|---:|']
 lines += [f'| {k} | {v["family_holdout_bits"]:.3f} |' for k,v in summary.items()]
 lines += ['','Anonymous categories and latent production classes use identical fitted likelihoods with different names. Their equality demonstrates an identifiability limit; no independently documented workshop labels are present. Site, medium, locus and level are observed context predictors; locus and level codes are namespaced by site. Complementary-field model uses shape of the inscription plus observed context, without a literal text-to-species identity constraint. Literal-string lookup predicts raw catalogue motif codes; different raw codes alone are not different species.','', 'The complete available checkpoint correspondence network and component contrasts were re-executed. Published copper typology survives as a source-linked transcription. All source-object copies remain provenance references rather than independent extra examples.','', 'The frozen358 component transfer and copper elephant/horned-tiger contrast preserve their original conditional exclusions. No lexical or sound anchor is established. The1380/2452 raw texts differ; their comparison requires the Route A expansion hypothesis.','', 'Parameter cost is a nominal BIC-style upper accounting, reported separately from held-target loss. It is not an estimate of shrinkage effective dimension. Every model predicts the fixed998-class rawfs80 alphabet with normalized probability. A total0.5 prior count is distributed across that alphabet; unseen labels share an explicit pooled probability mass. All evaluations are retrospective because the corpus was already inspected.','', 'Recovery status: these are newly executed reconstructed models. They are not represented as byte-identical recovery of the lost implementation or its scores.']
 (HERE/'REPORT.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
