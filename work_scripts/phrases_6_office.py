#!/usr/bin/env python3
"""PHRASES step 6: the front formula 920-060-741 (38 objects, 7 cities). Fixed 2026-11-17 before the run.
Question: one office held by many, or many offices sharing a heading?
  Reading of the two sides (stated before the numbers):
   ONE OFFICE, MANY HOLDERS predicts: what follows the formula is a name (a person), nearly always; the formula is stamped by one
     kind of holder, so the stuff after it looks alike in shape (name + ending); the same holder-name can recur on several objects;
     the formula sits on seals and on the tags/tablets that carry its impressions.
   MANY OFFICES, ONE HEADING predicts: what follows is of several kinds (names, count lines, a role line); the part after the formula
     varies in shape; the same word-after-heading repeats rarely; the formula behaves like a front word in general.
  Tests (control for each = random draws of the same number of objects from the carriers of the commoner front formulas 861-002
  (172 objects) and 820-002 (100), 5,000 draws, same recipe):
   (1) next-sign job: the share of objects whose sign after 741 is a number (count line follows) vs draws.
   (2) rest-of-text variety: distinct rest strings / objects, and distinct first signs after the formula, vs draws.
   (3) repeated holders: pairs of carriers whose first sign after 741 is the same sign, vs draws.
   (4) the 350-504 line: number of carriers with the fixed tail 350-504, cities, bins.
   (5) fish crest (CREST class fish signs) first after the formula vs share among all seals with a name.
   (6) animal: unicorn (Bull1) share of seal carriers vs all seals, binomial; stand letters.
   (7) where in each city: area / building list; building-sharing repeats vs within-site draws (kinds.csv has it too).
   (8) object kinds and bins vs same-site draws (kinds.csv).
PREDICTIONS: 6a what follows is of several kinds (count line in 15-30% of objects, a name otherwise); 6b rest variety not lower than draws from
  861-002; 6c repeated first sign after the formula no more often than draws; 6d unicorn share equal to the all-seal share; 6e no building
  holds two carriers. If these hold the heading is shared by many offices/holders, with 350-504 as the one repeated sub-line.
Output: work_data/phrases/office_920_060_741.csv, log_6.txt
"""
from phrases_common import *
LOG = open(f'{OUTP}/log_6.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
from frame2_pictures import pic
from scipy.stats import binom
rng = np.random.default_rng(6)
O = build_objects()
HEAD = ('920', '060', '741')
def carriers(p):
    out = {}
    for o, tok in zip(d.obj, d.tok):
        if tok and find_in(tok, p): out.setdefault(str(o), []).append(tok)
    return out
def rest_after(tok, p):
    for (i, st, en) in positions(tok, p): return tuple(tok[i + len(p):])
    return None
def num_first(rest):
    return bool(rest) and rest[0] in V2 and v2c(rest[0]) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')
def stats(objs_, p):
    rests = []; firsts = []
    for o in objs_:
        r = rest_after(carr[p][o][0], p); rests.append(r); firsts.append(r[0] if r else '')
    nz = [r for r in rests if r]
    nfirst = [f for f in firsts if f and is_sign(f)]
    pairs = sum(c * (c - 1) // 2 for c in collections.Counter(nfirst).values())
    return dict(n=len(rests), num_first=sum(num_first(r) for r in nz) / max(1, len(nz)), n_rest=len(nz), distinct_rest=len(set(nz)) / max(1, len(nz)),
                distinct_first=len(set(nfirst)) / max(1, len(nfirst)), repeat_pairs=pairs)
carr = {HEAD: carriers(HEAD)}
for q in [('861', '002'), ('820', '002')]: carr[q] = carriers(q)
H = carr[HEAD]; say('carriers of 920-060-741:', len(H), ' cities:', O.loc[list(H), 'site'].nunique())
real = stats(list(H), HEAD); say('real:', {k: round(v, 3) for k, v in real.items()})
# controls
n = len(H); D = 5000
for q in [('861', '002'), ('820', '002')]:
    keys = list(carr[q]); res = []
    # pre-compute rests
    pre = {o: rest_after(carr[q][o][0], q) for o in keys}
    for t in range(D):
        sel = rng.choice(len(keys), n, replace=False); rs = [pre[keys[i]] for i in sel]; nz = [r for r in rs if r]
        nf = [r[0] for r in nz if is_sign(r[0])]
        pairs = sum(c * (c - 1) // 2 for c in collections.Counter(nf).values())
        res.append((sum(num_first(r) for r in nz) / max(1, len(nz)), len(set(nz)) / max(1, len(nz)), len(set(nf)) / max(1, len(nf)), pairs))
    R = np.array(res)
    say(f'control draws from {"-".join(q)} ({len(keys)} objects): num_first mean {R[:, 0].mean():.3f}; distinct rest mean {R[:, 1].mean():.3f}; distinct first mean {R[:, 2].mean():.3f}; repeat pairs mean {R[:, 3].mean():.2f}')
    say(f'   P(draw num_first >= real) {(np.sum(R[:, 0] >= real["num_first"]) + 1) / (D + 1):.3f};  P(draw distinct rest <= real) {(np.sum(R[:, 1] <= real["distinct_rest"] + 1e-9) + 1) / (D + 1):.3f}; '
        f'P(draw distinct first <= real) {(np.sum(R[:, 2] <= real["distinct_first"] + 1e-9) + 1) / (D + 1):.3f}; P(draw repeat pairs >= real) {(np.sum(R[:, 3] >= real["repeat_pairs"]) + 1) / (D + 1):.3f}')
# table
rows = []
for o, toks in H.items():
    r = O.loc[o]; rest = rest_after(toks[0], HEAD)
    rows.append(dict(obj=o, cisi=r.cisi, city=r.site, area=r.area, building=r.building, kind=r.kind, animal=r.animal, stand=r.stand, bin=r.bin, text='-'.join(toks[0]),
                     after='-'.join(rest) if rest else '', after_first_class=v2c(rest[0]) if rest and is_sign(rest[0]) else ('END' if not rest else 'cut'),
                     after_pictures=' '.join(pic(s) for s in rest if is_sign(s))))
Tt = pd.DataFrame(rows).sort_values(['city', 'text']); Tt.to_csv(f'{OUTP}/office_920_060_741.csv', index=False)
say('\n' + Tt[['obj', 'cisi', 'city', 'area', 'building', 'kind', 'animal', 'stand', 'bin', 'after', 'after_first_class']].to_string(index=False))
say('\nnext-sign classes:', Tt.after_first_class.value_counts().to_dict())
say('cities:', Tt.city.value_counts().to_dict()); say('kinds:', Tt.kind.value_counts().to_dict()); say('bins:', Tt.bin.replace('', 'undated').value_counts().to_dict())
say('animals (all objects):', Tt.animal.value_counts().to_dict(), ' stands:', Tt.stand.replace('', '-').value_counts().to_dict())
# 4 the 350-504 line
tail = Tt[Tt.after.str.contains('350-504')]; say('\n350-504 tail:', len(tail), 'objects', tail.city.value_counts().to_dict(), tail.bin.replace('', 'undated').value_counts().to_dict(), ' texts:', tail.text.tolist())
alltail = [o for o, tok in zip(d.obj, d.tok) if tok and find_in(tok, ('350', '504'))]
say('350-504 anywhere:', len(set(alltail)), 'objects; of them with the 920-060-741 front:', len(set(map(str, alltail)) & set(H)))
# 5 fish crest
FISH = {'220', '231', '233', '235', '240', '226', '222', '243', '236', '241'}
def first_name_sign(rest):
    for s in rest:
        if is_sign(s) and v2c(s) in ('CREST', 'PERSONAL', 'NUM_NAME', 'NUM_SHORT'):
            return s
    return None
def crest_after(rest):
    # name crest = first sign after the formula, skipping number strokes (the star number sits before the fish)
    for s in rest:
        if not is_sign(s): return None
        if v2c(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'): continue
        return s
    return None
names = Tt[(Tt.after_first_class != 'END')]
cr = [crest_after(tuple(a.split('-'))) for a in names.after if a]
fish_real = sum(1 for c in cr if c in FISH)
nameseals = []
for o, tok in zip(d.obj, d.tok):
    if not tok or O.loc[str(o), 'kind'] != 'seal': continue
    rr = [s for s in tok if is_sign(s)]
    if len(rr) >= 2: nameseals.append(rr[0] if v2c(rr[0]) not in ('NUM_SHORT', 'NUM_NAME', 'NUM_TALL', 'OPEN', 'SLOT') else None)
base = np.mean([1 if (c in FISH) else 0 for c in nameseals if c is not None])
say(f'\nfish sign first after the formula (numbers skipped): {fish_real} of {len([c for c in cr if c])}; share of seals whose first non-number sign is a fish: {base:.3f}; binomial P {1 - binom.cdf(fish_real - 1, len([c for c in cr if c]), base):.4f}')
# 6 animal
seals = Tt[Tt.kind == 'seal']; s_all = O[O.kind == 'seal']
bu = int((seals.animal == 'Bull1').sum()); pb = (s_all.animal == 'Bull1').mean()
say(f'unicorn: {bu} of {len(seals)} seal carriers; all seals {pb:.3f}; binomial P(>=) {1 - binom.cdf(bu - 1, len(seals), pb):.4f}; short-horned bull (Gaur) {int((seals.animal == "Gaur").sum())}')
# 7 where
say('\nbuilding repeats among carriers:', int(Tt[Tt.building != ''].building.duplicated().sum()), ' areas (Mohenjo-daro):', Tt[Tt.city == 'Mohenjo-daro'].area.value_counts().to_dict())
K = pd.read_csv(f'{OUTP}/kinds_all.csv', dtype={'phrase': str}); k = K[K.phrase == '920-060-741'].iloc[0]
say('kinds.csv row:', {c: (round(k[c], 4) if isinstance(k[c], float) else k[c]) for c in ['primary', 'P_house', 'P_city', 'P_area', 'P_goods', 'nonseal_share', 'null_nonseal_share', 'top_area', 'top_area_share', 'bins', 'n_bld_known', 'rep_bld', 'null_rep_bld']})
# other fillers in the slot
for s in ['741', '742', '745', '740', '746']:
    n_ = len({o for o, tok in zip(d.obj, d.tok) if tok and find_in(tok, ('920', '060', s))}); say(f'920-060-{s}: {n_} objects')
