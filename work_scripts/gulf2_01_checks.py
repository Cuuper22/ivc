#!/usr/bin/env python3
"""gulf2 step 1: the same word-free checks as jobs/out/abroad_frame.md, on the round-seal sequences read off the printed
plates (work_data/gulf2/sequences.csv). No word is attached to any sign.
PREDICTIONS (written before running): 
 G1  new Gulf/Near-East round-seal texts cost MORE bits per step than matched home seal texts (sign-pair and frame v2), as the 15 scored round seals did (+3.8 / +2.4 bits).
 G2  a person sign (090 or 091) sits in at least half of the new texts of 2+ signs (abroad round seals: 12 of 16 in the old set; home: about 2 in 15 round faces, rare in home seals).
 G3  the jar (740) ends none of them and closer/after-jar-title class endings are rarer than at home.
Unit: bits per step between neighbouring identified signs; ALT (a sign not matched) cuts the text, as lost signs do in abroad4.
Texts here = status 'new', not pseudo-script, 2+ drawn signs. Sensitivity: add the four 'maybe' rows as extra texts.
"""
import sys, csv
sys.path.insert(0,'/home/claude/ivc/work_scripts')
from abroad4_common import *
GD='/home/claude/ivc/work_data/gulf2'
rows=list(csv.DictReader(open(f'{GD}/sequences.csv')))
def toks(r): return tuple(t for t in r['signs_best'].split('-') if t)
def want(r, maybe=False):
    ok = r['dup_status']=='new' or (maybe and r['dup_status'].startswith('maybe'))
    return ok and 'pseudo' not in r['flag'] and r['signs_best'] not in ('-','') and len(toks(r))>=2
def mk(r):
    class R: pass
    q=R(); q.tok=toks(r); q.kind='seal'; q.clean=False; q.id=r['gid']; q.site=r['find_place']
    q.ag='short-horned bull' if 'bull' in r['animal'] else ('none' if r['animal'] in ('none','n/a (horizontal text centred)') else 'other beast')
    q.round=True
    return q
def scored(rs): return [score_foreign(mk(r)) for r in rs]
log('home pool'); pool=score_home_pool(); by=pool_index(pool)
setA=[r for r in rows if want(r)]
setB=[r for r in rows if want(r,True)]
print('texts A',len(setA),'B',len(setB))
for r in setA: print(r['gid'],'-'.join(toks(r)))
def person_stats(rs,label):
    n=len(rs); hit=sum(any(t in('090','091') for t in toks(r)) for r in rs)
    ident=sum(1 for r in rs for t in toks(r) if t!='ALT'); allsg=sum(len(toks(r)) for r in rs)
    pers=sum(1 for r in rs for t in toks(r) if t in('090','091'))
    # home seal texts, matched on number of signs
    hd=[(x,v) for x,v in home_distinct.items() if v[1]=='seal' and len([s for s in x if real(s)])>=2]
    rng=np.random.default_rng(77); bylen=collections.defaultdict(list)
    for x,v in hd: bylen[min(len([s for s in x if real(s)]),9)].append(x)
    sims=[];simsh=[]
    for _ in range(4000):
        h=0;pt=0;ts=0
        for r in rs:
            L=min(len(toks(r)),9); x=bylen[L][rng.integers(len(bylen[L]))]
            h+=any(s in('090','091') for s in x); pt+=sum(s in('090','091') for s in x); ts+=len(x)
        sims.append(h); simsh.append(pt/ts)
    sims=np.array(sims)
    ph=(np.sum(sims>=hit)+1)/(len(sims)+1)
    allhome=np.mean([any(s in('090','091') for s in x) for x,v in hd])
    print(f'{label}: texts {n}; with a person sign {hit} ({hit/n:.0%}); matched-home expectation {sims.mean():.2f} ({sims.mean()/n:.0%}), 95% range [{np.percentile(sims,2.5):.0f},{np.percentile(sims,97.5):.0f}], P(home draw >= real) {ph:.4f}; person tokens {pers} of {allsg} drawn signs ({pers/allsg:.0%}); home matched person share {np.mean(simsh):.1%}; identified tokens {ident} of {allsg}; all home seal texts of 2+ signs with a person sign {allhome:.1%}')
    return hit,n,sims.mean(),ph
person_stats(setA,'A new')
person_stats(setB,'B new+maybe')
for lab,rs in (('A',setA),('B',setB)):
    sc=[s for s in scored(rs) if s.n_step>=1]
    print(lab,'texts with >=1 step',len(sc),'steps',sum(s.n_step for s in sc))
    if not sc: continue
    idx,lv=matched_draws(pool,by,sc,2000,5)
    for c,nm in enumerate(NMODEL):
        s=summarize(pooled_bits(sc,c),draws_bits(pool,idx,c))
        print(f'  {nm:10s} real {s["real"]:.2f} control {s["ctrl_mean"]:.2f} [{s["ctrl_lo"]:.2f},{s["ctrl_hi"]:.2f}] diff {s["diff"]:+.2f} P(real higher) {s["P_real_higher"]:.4f}')
    # pooled with the round seals already in abroad4 (core round + unknown-site round)
    old=[]
    for r in F[(F.tier.isin(['core','unk_round'])) & F['round'] & (F.kind=='seal')].itertuples(): old.append(score_foreign(r))
    old=[s for s in old if s.n_step>=1]; both=old+sc
    idx2,lv2=matched_draws(pool,by,both,2000,6)
    print(f'  pooled with old round seals: texts {len(both)} steps {sum(s.n_step for s in both)}')
    for c,nm in enumerate(NMODEL[:3]):
        s=summarize(pooled_bits(both,c),draws_bits(pool,idx2,c))
        print(f'  {nm:10s} real {s["real"]:.2f} control {s["ctrl_mean"]:.2f} [{s["ctrl_lo"]:.2f},{s["ctrl_hi"]:.2f}] diff {s["diff"]:+.2f} P {s["P_real_higher"]:.4f}')
# job classes of each identified sign and class strings
print('job classes (frame v2):')
for r in setB:
    print(r['gid'],' '.join(f"{t}:{V2CLASS.get(t,'?') if t!='ALT' else '-'}" for t in toks(r)))
# ends and the jar
ends=[toks(r)[-1] for r in setA if toks(r)[-1]!='ALT']; starts=[toks(r)[0] for r in setA if toks(r)[0]!='ALT']
print('known last signs',ends,'classes',[V2CLASS.get(e) for e in ends]); print('known first signs',starts)
print('jar 740/741/700 anywhere in set A:', [(r['gid'],t) for r in setA for t in toks(r) if t in ('740','741','700')])
# stroke directly before person
unit=[(r['gid']) for r in rows if want(r,True) for a,b in zip(toks(r),toks(r)[1:]) if a in('001','002','003','004','005','055') and b in('090','091','093','095')]
print('short stroke directly before a person sign:',unit)
