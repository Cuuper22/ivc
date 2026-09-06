"""Reconstructed Route A: normalized raw-sign latent role and boundary grammar.

Graphical programs tie emission parameters through expanded component counts.
The softmax normalizes over ORIGINAL sign IDs; no expanded-string likelihood is
mistaken for raw data probability. Latent state changes are neutral boundaries.
"""
import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.sparse import csr_matrix

PAIRS=[(59,60),(65,66),(67,68),(70,71),(72,73)]
PROGRAMS=['identity','tick211-after','tick388-after','tick342-after','tick211-before','roof87','roof102','roof87_tick211','roof102_tick211']
V=417

def transform(tokens, program='identity', pairs=None):
    mapping={}; pairs=PAIRS if pairs is None else pairs
    if 'tick' in program:
        marker=211 if 'roof' in program else int(program.split('-')[0][4:])
        before=program.endswith('before')
        mapping.update({str(b):[str(marker),str(a)] if before else [str(a),str(marker)] for a,b in pairs})
    if 'roof' in program:
        marker='102' if '102' in program else '87'
        mapping['65']=[marker,'59']
        if 'tick' not in program: mapping['66']=[marker,'60']
    def expand(t,active=()):
        if t not in mapping:return [t]
        if t in active: raise ValueError('cyclic graphical program')
        return [z for x in mapping[t] for z in expand(x,active+(t,))]
    return [z for t in tokens for z in expand(str(t))]

def features(program,pairs=None):
    f=np.zeros((V,V))
    for t in range(1,V+1):
        for x in transform([str(t)],program,pairs):f[t-1,int(x)-1]+=1
    # Order is represented separately by transition-side contextual emission below.
    return csr_matrix(f)

def sequences(rows):
    out={}
    for r in rows:
        if isinstance(r,dict):
            if not r.get('strict',True):continue
            s=tuple(r.get('tokens_stored',r.get('sequence',[])))
        else:s=tuple(r)
        if s and all(str(x).isdigit() and 1<=int(x)<=V for x in s):out[tuple(map(int,s))]=1
    return sorted(out)

def batch(seq):
    n=len(seq); l=max(map(len,seq),default=1)
    x=np.zeros((n,l),int); mask=np.zeros((n,l),bool)
    for i,s in enumerate(seq):x[i,:len(s)]=np.array(s)-1;mask[i,:len(s)]=True
    return x,mask

def fb(x,mask,pi,T,E,stats=True):
    n,l=x.shape;k=len(pi);a=np.zeros((n,l,k));c=np.ones((n,l))
    for t in range(l):
        p=np.broadcast_to(pi,(n,k)) if t==0 else a[:,t-1]@T
        z=p*E[:,x[:,t]].T; c[:,t]=z.sum(1)
        a[:,t]=z/c[:,t,None]
        if t:a[~mask[:,t],t]=a[~mask[:,t],t-1]
        c[~mask[:,t],t]=1
    ll=np.log(c).sum(1)
    if not stats:return ll,None
    b=np.ones((n,l,k));tc=np.zeros((k,k))
    for t in range(l-2,-1,-1):
        v=E[:,x[:,t+1]].T*b[:,t+1]/c[:,t+1,None]
        v[~mask[:,t+1]]=1
        b[:,t]=v@T.T
        idx=mask[:,t+1]
        tc+=np.einsum('ni,nj->ij',a[idx,t],v[idx])*T
    g=a*b;g/=g.sum(2,keepdims=True);g*=mask[:,:,None]
    ec=np.zeros((k,V))
    for j in range(k):ec[j]=np.bincount(x.ravel(),weights=g[:,:,j].ravel(),minlength=V)
    return ll,(g[:,0].sum(0),tc,ec,g)

def emission(theta,F,program='identity',T=None,pairs=None,gradient=None):
    # Modified signs share the bare component role; ordered additions integrate
    # over a preceding/following latent role through the shared transition.
    logits=theta.copy(); cache=[]
    T=np.eye(len(theta)) if T is None else T
    for raw in sorted(({b for a,b in (PAIRS if pairs is None else pairs)} if 'tick' in program else set()) | ({65,66} if 'roof' in program else set())):
        expanded=transform([str(raw)],program,pairs)
        if expanded==[str(raw)]:continue
        markers=[]; core=expanded[:]
        if 'roof' in program and core[0] in ['87','102']:
            markers.append((int(core.pop(0))-1,'before'))
        if 'tick' in program and len(core)>1:
            side='before' if program.endswith('before') else 'after'
            markers.append((int(core.pop(0 if side=='before' else -1))-1,side))
        base=int(core[0])-1; logits[:,raw-1]=theta[:,base]
        local=[]
        for marker,side in markers:
            z=(np.log(T.T+1e-300) if side=='before' else np.log(T+1e-300))+theta[:,marker][None,:]
            l=logsumexp(z,axis=1);w=np.exp(z-l[:,None]);logits[:,raw-1]+=l;local.append((marker,w))
        cache.append((raw-1,base,local))
    p=np.exp(logits-logsumexp(logits,axis=1,keepdims=True))
    if gradient is None:return p
    # gradient is derivative w.r.t. logits; chain through ordered additions.
    grad=gradient.copy()
    for raw,base,local in cache:
        v=gradient[:,raw];grad[:,raw]-=v;grad[:,base]+=v
        for marker,w in local:grad[:,marker]+=v@w
    return grad

def fit(rows, program='identity', roles=3, max_iter=50, pairs=None, seed=20260906):
    seq=sequences(rows)
    if not seq:raise ValueError('no strict observations')
    x,mask=batch(seq);F=features(program,pairs)
    rng=np.random.default_rng(seed);theta=rng.normal(0,.1,(roles,V))
    pi=np.ones(roles)/roles;T=.8*np.eye(roles)+.2/roles;trace=[]
    prior=.05
    for iteration in range(max_iter):
        E=emission(theta,F,program,T,pairs);ll,st=fb(x,mask,pi,T,E);ic,tc,ec,g=st
        objective=float(ll.sum()-prior/2*(theta**2).sum())
        trace.append(objective)
        if len(trace)>1 and abs(trace[-1]-trace[-2])<1e-5*max(1,abs(trace[-1])):break
        pi=(ic+.01)/(ic.sum()+roles*.01)
        target_T=(tc+.01)/(tc.sum(1,keepdims=True)+roles*.01)
        # Ordered emissions also depend on T: accept only likelihood-improving
        # transition steps, rather than claiming an invalid ordinary EM update.
        for fraction in (1.,.5,.25,.125,.0625,.03125,0.):
            trial=(1-fraction)*T+fraction*target_T
            trial_ll,_=fb(x,mask,pi,trial,emission(theta,F,program,trial,pairs),False)
            if trial_ll.sum() >= ll.sum()-1e-8:
                T=trial;break
        def loss(flat):
            th=flat.reshape(roles,V);p=emission(th,F,program,T,pairs)
            val=-(ec*np.log(p+1e-300)).sum()+prior/2*(th**2).sum()
            grad=emission(th,F,program,T,pairs,gradient=p*ec.sum(1,keepdims=True)-ec)+prior*th
            return val,grad.ravel()
        opt=minimize(loss,theta.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':60,'ftol':1e-10})
        theta=opt.x.reshape(roles,V)
    E=emission(theta,F,program,T,pairs);ll,_=fb(x,mask,pi,T,E,False)
    # rank cost charges independent tied features, not unconstrained 417 emissions.
    rank=V-len({b for a,b in (PAIRS if pairs is None else pairs)}) if 'tick' in program else V
    if 'roof' in program:rank-=1 if 'tick' in program else 2
    npar=roles*(rank-1)+roles*(roles-1)+roles-1
    rule_bits=0 if program=='identity' else math.log2(V)+2
    if 'roof' in program and 'tick' in program:rule_bits*=2
    data_bits=float(-ll.sum()/math.log(2));parameter_bits=.5*npar*math.log2(int(mask.sum()))
    return {'program':program,'roles':roles,'pairs':pairs,'pi':pi.tolist(),'transition':T.tolist(),'emission':E.tolist(),'theta':theta.tolist(),'trace_penalized_loglik':trace,'iterations':len(trace),'converged':len(trace)<max_iter,'train_distinct_expressions':len(seq),'train_signs':int(mask.sum()),'data_bits':data_bits,'parameter_bits':parameter_bits,'rule_bits':rule_bits,'total_bits':data_bits+parameter_bits+rule_bits,'seed':seed,'provenance':'reconstruction; newly executed, not recovered lost numerical results','boundary_definition':'latent role changes; same-role internal boundaries unidentifiable','ordered_component_roles':True}

def score(model,rows):
    seq=sequences(rows)
    if not seq:return {'data_bits':0.,'expressions':0,'per_expression':[]}
    x,mask=batch(seq);ll,_=fb(x,mask,np.array(model['pi']),np.array(model['transition']),np.array(model['emission']),False)
    return {'data_bits':float(-ll.sum()/math.log(2)),'expressions':len(seq),'per_expression':[{'sequence':list(map(str,s)),'bits':float(-v/math.log(2))} for s,v in zip(seq,ll)]}

def analyze(model,rows):
    seq=sequences(rows);x,m=batch(seq);pi=np.array(model['pi']);T=np.array(model['transition']);E=np.array(model['emission'])
    ll,st=fb(x,m,pi,T,E);g=st[-1]
    # Exact adjacent pair posterior by conditioning one edge with forward/backward.
    out=[]
    for i,s in enumerate(seq):
        xx,mm=batch([s]);a=np.zeros((len(s),len(pi)));b=np.ones_like(a)
        a[0]=pi*E[:,xx[0,0]];a[0]/=a[0].sum()
        for t in range(1,len(s)):
            a[t]=(a[t-1]@T)*E[:,xx[0,t]];a[t]/=a[t].sum()
        for t in range(len(s)-2,-1,-1):
            b[t]=T@(E[:,xx[0,t+1]]*b[t+1]);b[t]/=b[t].sum()
        boundaries=[]
        for t in range(len(s)-1):
            joint=a[t,:,None]*T*(E[:,xx[0,t+1]]*b[t+1])[None,:];joint/=joint.sum();boundaries.append(float(1-np.trace(joint)))
        out.append({'sequence':list(map(str,s)),'expanded':transform(s,model['program'],model.get('pairs')),'roles':g[i,:len(s)].tolist(),'boundary_probabilities':boundaries,'bits':float(-ll[i]/math.log(2))})
    return out

def select(rows,programs=PROGRAMS,role_counts=(1,2,3),max_iter=50,pairs=None):
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(fit,rows,p,k,max_iter,pairs) for p in programs for k in role_counts]
        models=[f.result() for f in futures]
    return min(models,key=lambda m:m['total_bits']),models
