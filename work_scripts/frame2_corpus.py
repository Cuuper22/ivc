#!/usr/bin/env python3
"""JOB 3: the corpus in jobs. Writes work_data/frame/corpus_jobs.csv and FRAMEBOOK.md (repo root).
Rules fixed before running (2026-11-17):
  every first-catalogue face (5,679): sign numbers in reading order, each sign's v2 base class and v2 pushed class,
  the text kind (frame2_common patterns; seals use the same split as frame2_seals.py), and for every lost or unclear sign
  the top 3 restored candidates with probabilities.
  Restoration model = the best mixed model on the fill-the-gap test (77 items) by top 5 in frame2_score.py:
  0.5 sign bigram + 0.5 v2-pushed class grammar (pooled), trained on all distinct first-catalogue texts; forward-backward
  over the whole face; text start and end counted only when the face has no broken edge.
  Faces with lost signs also get a 'restored kind': the text kind after putting the top candidate in every lost place.
"""
from frame2_common import *
from frame2_pictures import pic

c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2B = dict(zip(c2.sign, c2.v2_base)); V2P = dict(zip(c2.sign, c2.v2_pushed))
T = train_texts(); vocab, idx = vocab_of(T); C = counts(T, idx)
big = bigram_model(C)
cm = class_model(C, {s: V2P.get(s, 'PERSONAL') for s in vocab}, 'v2 pushed', vocab)[0]
mix = mix_model(big, cm, 0.5, 'mix: bigram + v2 pushed')


def text_kind(x, kind, flg=frozenset()):
    if not x: return 'empty'
    if set(x) & UNK or flg & {'broken', 'lost', 'alt'}: return 'damaged'
    cl = [V2B.get(s, 'PERSONAL') for s in x]
    t = v2_type(cl, kind)
    if t == 'count line': return 'opener + count line' if cl[0] == 'OPEN' else 'bare count line'
    if t: return t
    if 'CLOSER' in cl or 'TITLE' in cl: return 'loose name text'
    return 'other'


rows = []
t0 = time.time()
for n_, (fid, x, f, k) in enumerate(zip(d.id, d.tok, d.flg, d.kind)):
    if n_ % 1000 == 0: log(f'  face {n_} of {len(d)}')
    r = dict(face=fid, cisi=d.cisi.iloc[n_], site=d.site.iloc[n_], area=d['area-section'].iloc[n_], object_kind=KIND_PLAIN.get(kind_of(k), k),
             signs='-'.join(x), v2_classes='-'.join(V2B.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x),
             v2_pushed='-'.join(V2P.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x),
             pictures=' '.join(f'[{pic(s)}]' for s in x), broken_edge='broken' in f, text_kind=text_kind(x, k, f))
    ids = [idx.get(s) if s not in UNK else None for s in x]
    lost = [i for i, v in enumerate(ids) if v is None]
    rest = []; xx = list(x)
    if lost and x:
        post = gap_posteriors(mix, ids, 'broken' not in f)
        for t in lost:
            p = post[t]; top = np.argsort(-p)[:3]
            rest.append(f'{t + 1}:' + '/'.join(f'{vocab[i]}={p[i]:.2f}' for i in top))
            xx[t] = vocab[top[0]]
            r.setdefault('lost_positions', []); r['lost_positions'].append(dict(pos=t + 1, stored=x[t], cand=[vocab[i] for i in top], p=[float(p[i]) for i in top]))
        r['restored_kind'] = text_kind(tuple(xx), k, frozenset(f) - {'lost', 'alt'})
    r['restorations'] = ' '.join(rest)
    r['restored_signs'] = '-'.join(xx) if lost else ''
    rows.append(r)
R = pd.DataFrame(rows)
lostrows = []
for r in rows:
    for lp in r.get('lost_positions', []):
        lostrows.append(dict(face=r['face'], cisi=r['cisi'], site=r['site'], object_kind=r['object_kind'], signs=r['signs'], position=lp['pos'], stored=lp['stored'],
                             cand1=lp['cand'][0], p1=round(lp['p'][0], 3), cand2=lp['cand'][1], p2=round(lp['p'][1], 3), cand3=lp['cand'][2], p3=round(lp['p'][2], 3),
                             v2_class_of_cand1=V2B.get(lp['cand'][0], 'PERSONAL')))
L = pd.DataFrame(lostrows); L.to_csv(f'{OUT2}/restorations_v2.csv', index=False)
R.drop(columns=['lost_positions']).to_csv(f'{OUT2}/corpus_jobs.csv', index=False)
log(f'corpus_jobs.csv: {len(R)} faces; lost or unclear signs restored: {len(L)} on {L.face.nunique()} faces; top candidate p >= 0.5: {(L.p1 >= 0.5).sum()} ({(L.p1 >= 0.5).mean():.1%})')
log('text kinds: ' + ', '.join(f'{k} {v}' for k, v in R.text_kind.value_counts().items()))
log('restored kinds of damaged faces: ' + ', '.join(f'{k} {v}' for k, v in R.restored_kind.value_counts().items()))
R.drop(columns=['lost_positions']).to_pickle('/tmp/corpus_jobs.pkl')
