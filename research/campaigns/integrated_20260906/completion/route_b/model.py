"""Reconstructed Route B: frozen motif likelihoods; no text likelihood charged."""
from pathlib import Path
import json, hashlib, collections, math
import numpy as np
HERE=Path(__file__).resolve().parent
CAMPAIGN=HERE.parents[1]
ALPHABET=[str(i) for i in range(1,999)]
MODELS=['independent','literal_string','anonymous_category','production_latent','complementary_fields','site','medium','context','components_context']
def stable(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def build_examples():
 rows=[json.loads(s) for s in (CAMPAIGN/'shared/observations.jsonl').read_text().splitlines()];objs=collections.defaultdict(list)
 for r in rows:objs[r['object_id']].append(r)
 result={}
 for oid,rr in objs.items():
  labels={str(r['raw_fields']['fs80']) for r in rr if int(r['raw_fields']['fs80']) not in (0,999) and int(r['raw_fields']['fs80'])//10 not in (35,17,37,39,46,90,91,92,93)}
  faces=collections.defaultdict(list)
  for r in rr:faces[r['face_code']].append(r)
  ff=[]
  for rs in faces.values():
   rs.sort(key=lambda x:x['line_code']);nonempty=[r for r in rs if r['tokens_stored']]
   if nonempty and all(r['strict'] for r in nonempty):ff.append(nonempty)
  if len(labels)!=1 or not ff:continue
  maxlen=max(sum(len(r['tokens_stored']) for r in rs) for rs in ff);ff=[rs for rs in ff if sum(len(r['tokens_stored']) for r in rs)==maxlen]
  if len(ff)!=1:continue
  rs=ff[0];f=rs[0]['raw_fields'];num=int(oid.split(':')[-1]);site='Mohenjodaro' if num<4000 else 'Harappa' if num<6000 else 'Chanhudaro' if num<7000 else 'Lothal' if num<8000 else 'Kalibangan' if num<9000 else 'other'
  e=dict(object_ids=[oid],row_ids=[r['row_id'] for r in rs],lines=[r['tokens_stored'] for r in rs],label=next(iter(labels)),site=site,medium=str(f['inscobj']),locus=str(f['locus']),level=str(f['level']))
  e['family']=stable(e['lines']);key=(e['family'],e['label'],site,e['medium'])
  if key in result:result[key]['object_ids'].append(oid);result[key]['row_ids']+=e['row_ids']
  else:result[key]=e
 return list(result.values())
def features(e,mode):
 fs=[]
 if mode in ('components_context','anonymous_category','production_latent'):
  for line in e['lines']:
   for n in (1,2):
    for i in range(len(line)-n+1):fs.append('sign:'+','.join(line[i:i+n]))
 if mode in ('components_context','context','complementary_fields'):fs+=['site:'+e['site'],'medium:'+e['medium'],'locus:'+e['site']+':'+e['locus'],'level:'+e['site']+':'+e['level']]
 if mode=='complementary_fields':fs+=['length:'+str(sum(map(len,e['lines']))),'lines:'+str(len(e['lines']))]
 return sorted(set(fs))
def key(e,mode):return e['family'] if mode=='literal_string' else e['site'] if mode=='site' else e['medium'] if mode=='medium' else 'all'
def fit_model(examples,model_name='components_context'):
 labels=sorted({str(e['label']) for e in examples})+['__other__'];li={s:i for i,s in enumerate(labels)};alpha=np.array([.5/998]*(len(labels)-1)+[.5*(999-len(labels))/998]);counts=alpha.copy()
 for e in examples:counts[li[str(e['label'])]]+=1
 m=dict(name=model_name,alphabet='raw_fs80_integers_1_through_998',labels=labels,prior=(counts/counts.sum()).tolist(),training_objects=sorted({o for e in examples for o in e['object_ids']}),training_families=sorted({e['family'] for e in examples}))
 if not examples or model_name=='independent':
  parameters=max(0,len(labels)-1);m.update(tables={},parameters=parameters,parameter_bits=parameters*math.log2(max(2,len(examples)))/2,rule_bits=math.log2(len(MODELS)));return m
 if model_name in ('independent','literal_string','site','medium'):
  tables={}
  for e in examples:
   k=key(e,model_name);tables.setdefault(k,np.array(m['prior'])*4);tables[k][li[str(e['label'])]]+=1
  m['tables']={k:(v/v.sum()).tolist() for k,v in tables.items()};m['parameters']=len(tables)*(len(labels)-1)
 else:
  vocab=sorted({f for e in examples for f in features(e,model_name)});vi={s:i for i,s in enumerate(vocab)};X=np.zeros((len(examples),len(vocab)))
  for i,e in enumerate(examples):
   for f in features(e,model_name):X[i,vi[f]]=1
  if model_name in ('anonymous_category','production_latent'):
   K=min(4,len(examples));rng=np.random.default_rng(20260906);resp=rng.dirichlet(np.ones(K),len(examples));Y=np.eye(len(labels))[[li[str(e['label'])] for e in examples]];trace=[]
   for iteration in range(80):
    theta=(resp.T@X+.5);theta/=theta.sum(axis=1,keepdims=True);phi=(resp.T@Y+alpha);phi/=phi.sum(axis=1,keepdims=True);mix=(resp.sum(axis=0)+1)/(len(examples)+K)
    logp=X@np.log(theta).T+Y@np.log(phi).T+np.log(mix);mx=logp.max(axis=1,keepdims=True);z=np.exp(logp-mx);resp=z/z.sum(axis=1,keepdims=True);ll=float((mx[:,0]+np.log(z.sum(axis=1))).sum());trace.append(ll)
    if len(trace)>1 and abs(trace[-1]-trace[-2])<1e-7:break
   m.update(vocab=vocab,theta=theta.tolist(),phi=phi.tolist(),mix=mix.tolist(),trace=trace,parameters=K*(len(vocab)+len(labels)-2)+K-1,latent_meaning='anonymous; production name is an observationally equivalent relabeling')
  else:
   T=np.ones((len(labels),len(vocab)))
   for i,e in enumerate(examples):T[li[str(e['label'])]]+=X[i]
   T/=T.sum(axis=1,keepdims=True);m.update(vocab=vocab,theta=T.tolist(),parameters=len(labels)*(len(vocab)-1)+len(labels)-1)
 m['parameter_bits']=m['parameters']*math.log2(max(2,len(examples)))/2;m['rule_bits']=math.log2(len(MODELS));return m

def predict_proba(model,example):
 m=model;name=m['name'];prior=np.array(m['prior'])
 if 'tables' in m:p=np.array(m['tables'].get(key(example,name),m['prior']))
 else:
  vi={f:i for i,f in enumerate(m['vocab'])};ix=[vi[f] for f in features(example,name) if f in vi];theta=np.array(m['theta'])
  if name in ('anonymous_category','production_latent'):
   logp=np.log(m['mix'])+np.log(theta[:,ix]).sum(axis=1);p=np.exp(logp-logp.max());p/=p.sum();p=p@np.array(m['phi'])
  else:
   logp=np.log(prior)+np.log(theta[:,ix]).sum(axis=1);p=np.exp(logp-logp.max());p/=p.sum()
 out=dict(zip(m['labels'],map(float,p)));other=out.pop('__other__');missing=998-len(out)
 if missing:out.update({label:other/missing for label in ALPHABET if label not in out})
 return out
def score(model,examples):
 records=[]
 for e in examples:
  p=predict_proba(model,e);q=p[str(e['label'])];records.append(dict(object_ids=e['object_ids'],row_ids=e['row_ids'],family=e['family'],actual=e['label'],probability=q,predicted=max(p,key=p.get),probability_sum=sum(p.values())))
 return dict(data_bits=-sum(math.log2(r['probability']) for r in records),records=records)
