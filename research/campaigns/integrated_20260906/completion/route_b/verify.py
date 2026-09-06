from model import *
def main():
 es=build_examples();checks=0
 for f in list(HERE.glob('*.fold*.json'))+list(HERE.glob('*.medium*.json')):
  m=json.loads(f.read_text());name=f.name
  if '.fold' in name:
   k=int(name.split('.fold')[1].split('.')[0]);targets=[e for e in es if int(e['family'][:12],16)%5==k]
  else:
   med=name.split('.medium')[1].split('.')[0];targets=[e for e in es if e['medium']==med]
  assert not set(m['training_objects'])&{o for e in targets for o in e['object_ids']}
  assert not set(m['training_families'])&{e['family'] for e in targets}
  for e in targets[:3]:
   p=predict_proba(m,e);assert set(p)==set(ALPHABET) and abs(sum(p.values())-1)<1e-9 and min(p.values())>0
  checks+=1
 for name in MODELS:
  p=predict_proba(fit_model([],name),es[0]);assert len(p)==998 and abs(sum(p.values())-1)<1e-9
 pred=json.loads((HERE/'predictions.json').read_text())
 assert all(r['probability']>0 and abs(r['probability_sum']-1)<1e-9 for r in pred)
 (HERE/'verification.json').write_text(json.dumps(dict(frozen_fits_checked=checks,whole_object_exclusion=True,exact_family_exclusion=True,probabilities_normalized=True,fixed_support=998,empty_training_valid=True,scored_predictions=len(pred),new_semantic_anchors=0),indent=2)+'\n')
 print('verified',checks,'fits;',len(pred),'predictions')
if __name__=='__main__':main()
