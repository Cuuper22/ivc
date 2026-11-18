#!/usr/bin/env python3
"""Replay B: blind tester replay of the confirm-a-word procedure on 60 Indus signs.
Part 1 (this block): LOOK helper = Step 1, Lipi (first catalogue) only. No new texts, no picture side, no time bin.
Later blocks (appended): predictions, run helpers, outcomes."""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from decoy_loader import *
import pandas as pd, numpy as np

TL = pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/decoy/test_list.csv', dtype=str).fillna('')
SIGN = {int(r.item): r.sign for r in TL.itertuples()}
_FL = faces_all('L'); _KL = kfaces('L')
_KIND_ALL = collections.Counter(k for x, k, s in _KL); _SITE_ALL = collections.Counter(s for x, k, s in _KL)
_NF = len(_KL)
_SIGNFREQ = collections.Counter(a for x, k, s in _KL for a in set(x))

def look(s):
    rows = [(x, k, st) for x, k, st in _KL if s in x]
    n = len(rows)
    out = [f'sign {s}: {n} Lipi faces']
    kc = collections.Counter(k for x, k, st in rows)
    out.append('kinds: ' + ', '.join(f'{k} {c} ({c/n:.0%} vs {_KIND_ALL[k]/_NF:.0%})' for k, c in kc.most_common(6)))
    sc = collections.Counter(st for x, k, st in rows)
    out.append('sites: ' + ', '.join(f'{k} {c} ({c/n:.0%} vs {_SITE_ALL[k]/_NF:.0%})' for k, c in sc.most_common(5)))
    pv = collections.Counter(); nx = collections.Counter(); first = last = 0
    for x, k, st in rows:
        for i, a in enumerate(x):
            if a != s: continue
            pv[x[i-1] if i > 0 else '^'] += 1; nx[x[i+1] if i+1 < len(x) else '$'] += 1
            first += i == 0; last += i == len(x)-1
    out.append(f'left: {pv.most_common(5)}  right: {nx.most_common(5)}')
    out.append(f'opens {first}, closes {last} of {n} faces (all faces: {sum(1 for x,k,st in _KL if x and x[0]==x[0])} ; mean len here {np.mean([len(x) for x,k,st in rows]):.1f})')
    cb = counts_beside(s); sh = sum(a in SHORT for a in cb); ta = sum(a in TALL for a in cb)
    out.append(f'counts beside: short {sh}, tall {ta}')
    co = collections.Counter(a for x, k, st in rows for a in set(x) if a != s and a not in VAL)
    lift = [(a, c, round(c / n / (_SIGNFREQ[a] / _NF), 1)) for a, c in co.most_common(40) if c >= 3]
    lift.sort(key=lambda t: -t[2]); out.append('same face (sign,n,lift): ' + str(lift[:7]))
    return '\n'.join(out)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'look':
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for i in range(lo, hi + 1):
        print(f'=== item {i} ===', TL.iloc[i-1].sound, '|', TL.iloc[i-1].english); print(look(SIGN[i])); print()


# =====================================================================================================
# PART 2: FIRST PREDICTIONS for all 60 items (written after Step 1 looks, before any Step 3 run).
# Spec = (test_kind, params, direction, one-line prediction).  Base rate is always the overall rate in the comparison
# population, computed at run time (new-text tests: all new-text faces / tokens / counts; object tests: shuffle within site|kind).
# test kinds:
#  M_KIND   (set of kinds)       share of new-text faces carrying the sign that sit on those object kinds   vs share among all new-text faces
#  M_SITE   (site)               same for site
#  M_POS    ('first'|'last')     share of the sign's tokens in new-text faces (len>=2, no 000) that are text-initial / text-final vs all tokens
#  M_COUNT  ('tall'|'short')     style of number signs next to the sign in new texts vs share of that style among all new-text counts
#  M_CO     (set of signs)       new-text faces with the sign that also hold one of the set vs share of all new-text faces holding one
#  P_PIC    (set of labels)      among objects with a picture, share showing those pictures; shuffle within site|kind
#  T_BIN    (set of bins)        among dated objects; shuffle within site|kind
#  A_AREA   (site, prefixes)     among that city's objects, share found in those areas; shuffle within kind
# =====================================================================================================
G, L_ = 'greater', 'less'
FIRST = {
 1: ('M_POS', 'first', G, 'Person/status title: on new texts the sign stands text-initial more than the average sign.'),
 2: ('M_CO', {'900', '904'}, G, 'Star (calendar body): on new texts its faces carry a month sign (900/904) more than faces in general.'),
 3: ('M_POS', 'last', G, 'Junior/subordinate: on new texts it is text-final more than the average sign.'),
 4: ('M_SITE', 'Mohenjo-daro', G, 'House: on new texts its faces come from Mohenjo-daro (largest residential city) more than faces in general.'),
 5: ('M_KIND', {'seal'}, G, 'Second ward (administrative unit): new-text faces sit on seals more than faces in general.'),
 6: ('M_KIND', {'tag', 'pot'}, G, 'Received/bought (transaction): new-text faces sit on tags or pots (goods carriers) more than faces in general.'),
 7: ('M_KIND', {'mtab', 'tag'}, G, 'Cup measure (goods/store): new-text faces sit on moulded tablets or tags more than faces in general.'),
 8: ('M_CO', {'900'}, L_, 'Two months: alternates with month sign 900, so shares a face with it LESS than faces in general.'),
 9: ('M_COUNT', 'short', G, 'Ration measure: counts next to it on new texts are short-stroke more than short share among all counts.'),
 10: ('M_KIND', {'seal'}, G, 'Assembly/council (official body): new-text faces sit on seals more than faces in general.'),
 11: ('P_PIC', {'Anth', 'Mult', 'Scene', 'Archer'}, G, 'Maiden (human): the picture on the object shows a human figure/scene more than other pictured objects.'),
 12: ('P_PIC', {'Phyt'}, G, 'Paddy (plant): the picture on its object is a plant more than on other pictured objects.'),
 13: ('M_KIND', {'rod'}, G, 'Rod/sceptre: new-text faces sit on rod-kind objects more than faces in general.'),
 14: ('M_KIND', {'tag', 'pot'}, G, 'Tax/levy (goods paid): new-text faces sit on tags or pots more than faces in general.'),
 15: ('M_SITE', 'Mohenjo-daro', G, 'First ward (urban unit): new-text faces come from Mohenjo-daro more than faces in general.'),
 16: ('M_POS', 'last', G, 'Kindred/family (lineage term): text-final on new texts more than the average sign.'),
 17: ('M_COUNT', 'tall', G, 'Pair: counts next to it on new texts are tall-stroke more than tall share among all counts.'),
 18: ('M_SITE', 'Harappa', G, 'Town: new-text faces come from Harappa more than faces in general.'),
 19: ('P_PIC', {'Fish', 'Gavi'}, G, 'Crate of fish: the picture on its object is a fish or the fish-eating gharial more than on other pictured objects.'),
 20: ('M_CO', {'700'}, G, 'Bound/allied: shares a face with pair-sign 700 on new texts more than faces in general.'),
 21: ('M_POS', 'first', G, 'Banner (emblem heading a name): text-initial on new texts more than the average sign.'),
 22: ('M_KIND', {'seal'}, G, 'Third ward: new-text faces sit on seals more than faces in general.'),
 23: ('M_KIND', {'seal'}, G, 'Guard: new-text faces sit on seals (guarantee marks) more than faces in general.'),
 24: ('P_PIC', {'Goat'}, G, 'Three-peaks (mountain name): the picture is the mountain goat/markhor more than on other pictured objects.'),
 25: ('M_POS', 'last', L_, 'Elder (senior): text-final on new texts LESS than the average sign.'),
 26: ('M_KIND', {'ctab'}, G, 'Staff-bearer (ritual/official): new-text faces sit on copper tablets more than faces in general.'),
 27: ('M_CO', {'820', '861'}, G, 'Half-share: shares a face with share signs 820/861 on new texts more than faces in general.'),
 28: ('M_COUNT', 'tall', G, 'Weight: counts next to it on new texts are tall-stroke more than tall share among all counts.'),
 29: ('P_PIC', {'Buff', 'Gaur', 'Zebu', 'Bull', 'Bull2', 'Bull3', 'Rhin'}, G, 'Horn: the picture is a horned beast other than the unicorn more than on other pictured objects.'),
 30: ('M_SITE', 'Harappa', G, 'Spindle (craft): new-text faces come from Harappa more than faces in general.'),
 31: ('M_KIND', {'tag'}, G, 'Granary: new-text faces sit on tags (store tokens) more than faces in general.'),
 32: ('M_COUNT', 'short', G, 'Month: counts next to it on new texts are short-stroke more than short share among all counts.'),
 33: ('M_KIND', {'pot'}, G, 'Proclamation: new-text faces sit on pots (public containers) more than faces in general.'),
 34: ('M_POS', 'first', G, 'Child of: text-initial on new texts more than the average sign.'),
 35: ('P_PIC', {'Phyt'}, G, 'Bamboo-star: the picture is a plant more than on other pictured objects.'),
 36: ('M_POS', 'last', L_, 'Given (takes a recipient after it): text-final on new texts LESS than the average sign.'),
 37: ('M_KIND', {'mtab'}, G, 'Grain measure: new-text faces sit on moulded tablets more than faces in general.'),
 38: ('M_POS', 'first', G, 'Quarter-share: text-initial on new texts more than the average sign.'),
 39: ('M_POS', 'last', G, 'Keeper: text-final on new texts more than the average sign.'),
 40: ('M_SITE', 'Lothal', G, 'Goldsmith (craft/bead port): new-text faces come from Lothal more than faces in general.'),
 41: ('P_PIC', {'Pipal', 'Phyt'}, G, 'Pipal: the picture is a pipal leaf or plant more than on other pictured objects.'),
 42: ('P_PIC', {'Archer', 'Tigr', 'Stag', 'Elep', 'Rhin', 'Hare'}, G, 'Arrow (hunt): the picture is an archer or hunted beast more than on other pictured objects.'),
 43: ('M_KIND', {'mtab'}, G, 'Heap/stock: new-text faces sit on moulded tablets more than faces in general.'),
 44: ('M_POS', 'last', G, 'First-star: text-final on new texts more than the average sign.'),
 45: ('M_KIND', {'seal'}, G, 'King: new-text faces sit on seals more than faces in general.'),
 46: ('M_POS', 'first', G, 'Share/holding: text-initial on new texts more than the average sign.'),
 47: ('M_POS', 'first', L_, 'Servant: text-initial on new texts LESS than the average sign.'),
 48: ('A_AREA', ('Harappa', ['FGranery']), G, 'Produce/ripened crop: Harappa objects with it come from the Granary area more than other Harappa objects.'),
 49: ('P_PIC', {'Phyt'}, G, 'Paddy field: the picture is a plant more than on other pictured objects.'),
 50: ('A_AREA', ('Harappa', ['FGranery']), G, 'Heap of threshed grain: Harappa objects with it come from the Granary area more than other Harappa objects.'),
 51: ('P_PIC', {'Goat', 'Stag'}, G, 'Hill: the picture is a mountain/forest beast (markhor, stag) more than on other pictured objects.'),
 52: ('M_CO', {'700', '690'}, G, 'The pair/partners: shares a face with pair/allied signs 700/690 on new texts more than faces in general.'),
 53: ('M_POS', 'first', L_, 'Servant: text-initial on new texts LESS than the average sign.'),
 54: ('P_PIC', {'Fish', 'Gavi'}, G, 'Scabbard-fish: the picture is a fish or gharial more than on other pictured objects.'),
 55: ('M_KIND', {'ctab'}, G, 'Bundle of sheaves: new-text faces sit on copper tablets more than faces in general.'),
 56: ('M_KIND', {'pot', 'tool', 'other'}, G, 'Seed-weight: new-text faces sit on pots/tools/other (non-seal, non-tablet) more than faces in general.'),
 57: ('P_PIC', {'Archer', 'Tigr', 'Elep', 'Rhin'}, G, 'Warrior: the picture is an archer or fierce beast more than on other pictured objects.'),
 58: ('M_KIND', {'pot'}, G, 'Chest (container): new-text faces sit on pots more than faces in general.'),
 59: ('M_KIND', {'tag'}, G, 'Hill share: new-text faces sit on tags more than faces in general.'),
 60: ('M_COUNT', 'tall', G, 'Dozen: counts next to it on new texts are tall-stroke more than tall share among all counts.'),
}
assert len(FIRST) == 60


# =====================================================================================================
# PART 3: RUN HELPERS (Step 3 / Step 4).  Outcome rule: came true = right direction and P<0.05; right direction only;
# against = opposite direction; too few = fewer than 3 cases.
# =====================================================================================================
from scipy.stats import binomtest
_MU = None
def _mu():
    global _MU
    if _MU is None:
        _MU = kfaces('Mu')   # (tok, kind, site)
    return _MU

def _verdict(obs_gt_base, p, direction):
    right = obs_gt_base if direction == 'greater' else (not obs_gt_base)
    if right and p < 0.05: return 'came true'
    return 'right direction only' if right else 'against'

def _binom(k, n, base, direction):
    if n < 3: return None
    alt = 'greater' if direction == 'greater' else 'less'
    p = binomtest(k, n, base, alternative=alt).pvalue
    gt = (k / n) > base
    eq = abs(k / n - base) < 1e-12
    obs = f'{k}/{n} = {k/n:.1%}'; bs = f'{base:.1%}'
    return obs, bs, float(p), gt, eq

def run_M_KIND(s, kinds, direction, field=1):
    rows = _mu(); K = set(kinds)
    base = np.mean([r[field] in K for r in rows]); sub = [r[field] in K for r in rows if s in r[0]]
    r = _binom(int(sum(sub)), len(sub), base, direction)
    if r is None: return f'{len(sub)} new-text faces', f'{base:.1%}', None, 'too few'
    obs, bs, p, gt, eq = r
    return f'new-text faces on {"/".join(sorted(K))} {obs}', f'{bs} of all new-text faces', p, _verdict(gt, p, direction)

def run_M_SITE(s, site, direction):
    return run_M_KIND(s, {site}, direction, field=2)

def run_M_POS(s, where, direction):
    k = n = K = N = 0
    for x, kd, st in _mu():
        if len(x) < 2 or '000' in x: continue
        L = len(x)
        for i, a in enumerate(x):
            hit = (i == L - 1) if where == 'last' else (i == 0)
            N += 1; K += hit
            if a == s: n += 1; k += hit
    r = _binom(k, n, K / N if N else 0.5, direction)
    if r is None: return f'{n} tokens', f'{K/max(N,1):.1%}', None, 'too few'
    obs, bs, p, gt, eq = r
    return f'text-{"final" if where=="last" else "initial"} tokens {obs}', f'{bs} of all new-text tokens', p, _verdict(gt, p, direction)

def run_M_COUNT(s, style, direction):
    c = counts_beside(s, 'Mu'); sh = sum(a in SHORT for a in c); ta = sum(a in TALL for a in c)
    allc = [a for x, kd, st in _mu() for a in x if a in VAL]
    bt = sum(a in TALL for a in allc) / max(1, sum((a in TALL) or (a in SHORT) for a in allc))
    base = bt if style == 'tall' else 1 - bt; k = ta if style == 'tall' else sh
    r = _binom(k, sh + ta, base, direction)
    if r is None: return f'{sh+ta} counts', f'{base:.1%}', None, 'too few'
    obs, bs, p, gt, eq = r
    return f'{style}-stroke counts beside it {obs}', f'{bs} of all new-text counts', p, _verdict(gt, p, direction)

def run_M_CO(s, signs, direction):
    T = set(signs) - {s}
    rows = [set(x) for x, kd, st in _mu()]
    base = np.mean([bool(z & T) for z in rows]); sub = [bool(z & T) for z in rows if s in z]
    r = _binom(int(sum(sub)), len(sub), base, direction)
    if r is None: return f'{len(sub)} new-text faces', f'{base:.1%}', None, 'too few'
    obs, bs, p, gt, eq = r
    return f'new-text faces also holding {sorted(T)} {obs}', f'{bs} of all new-text faces', p, _verdict(gt, p, direction)

def _obj_shuffle(s, mask, outcome, direction, label, site_only=False, n=10000):
    O = objs[mask]
    has = O.signs.apply(lambda z: s in z).values
    if has.sum() < 3: return f'{int(has.sum())} objects', '', None, 'too few'
    strata = (O.site.astype(str) if site_only else O.site.astype(str) + '|' + O.kind.astype(str)).values
    res_ = strat_shuffle_p(has, np.asarray(outcome(O), bool), strata, direction=direction, n=n)
    obs, mean, p = res_
    return f'{label}: {obs:.1%} of {int(has.sum())} objects', f'{mean:.1%} expected under shuffle within site and kind', p, _verdict(obs > mean, p, direction)

def run_P_PIC(s, labels, direction):
    L = set(labels)
    return _obj_shuffle(s, objs.pic.notna().values, lambda O: O.pic.isin(L).values, direction, f'pictured objects showing {"/".join(sorted(L))}')

def run_T_BIN(s, bins, direction):
    B = set(bins)
    return _obj_shuffle(s, (objs.bin != '').values, lambda O: O.bin.isin(B).values, direction, f'dated objects in {"/".join(sorted(B))}')

def run_A_AREA(s, args, direction):
    site, pre = args
    return _obj_shuffle(s, (objs.site == site).values, lambda O: O.area.apply(lambda a: any(str(a).startswith(p) for p in pre)).values, direction,
                        f'{site} objects from {"/".join(pre)}')

RUNNERS = {'M_KIND': run_M_KIND, 'M_SITE': run_M_SITE, 'M_POS': run_M_POS, 'M_COUNT': run_M_COUNT, 'M_CO': run_M_CO,
           'P_PIC': run_P_PIC, 'T_BIN': run_T_BIN, 'A_AREA': run_A_AREA}

def run_spec(item, spec):
    kind, par, direction, text = spec
    return RUNNERS[kind](SIGN[item], par, direction)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'stage1':
    import json
    results = {}
    for i in range(1, 61):
        obs, base, p, out = run_spec(i, FIRST[i])
        results[i] = dict(obs=obs, base=base, p=p, out=out)
        print(f'[stage1] item {i} sign {SIGN[i]} -> {out} | {obs} vs {base} | P={p}', flush=True)
        json.dump(results, open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B_stage1.json', 'w'))
    print('[stage1] done', flush=True)


# =====================================================================================================
# PART 4: SECOND PREDICTIONS (Step 4 redesign), written after seeing the first outcomes, only for items that did not come true.
# (Stage-1 outcomes: 19 came true, 15 right direction only, 17 against, 9 too few.)  Each is a different test of the same word.
# =====================================================================================================
STAR_PICS = {'Bult', 'Cros', 'Xcrs', 'Swas', 'Tri4', 'Xhch', 'Crs'}
GRAIN = {'752', '416', '845', '806', '501'}
SECOND = {
 1: ('A_AREA', ('Harappa', ['FGranery']), G, 'Cultivator delivers grain: Harappa objects with it come from the Granary area more than other Harappa objects.'),
 2: ('P_PIC', STAR_PICS, G, 'Star: the picture on its object is a star-like motif (dotted circles, crosses, swastika) more than on other pictured objects.'),
 4: ('A_AREA', ('Mohenjo-daro', ['DKG']), G, 'House: Mohenjo-daro objects with it come from the big residential block DK-G more than other Mohenjo-daro objects.'),
 5: ('T_BIN', {'middle'}, G, 'Ward (urban quarter): dated objects with it sit in the middle (mature urban) bin more than other dated objects.'),
 6: ('M_SITE', 'Lothal', G, 'Bought/received (trade): new-text faces come from the port Lothal more than faces in general.'),
 8: ('M_COUNT', 'short', G, 'Two months: counts next to it on new texts are short-stroke more than short share among all counts (as with the month sign).'),
 9: ('A_AREA', ('Harappa', ['FGranery']), G, 'Ration measure (issued from stores): Harappa objects with it come from the Granary area more than other Harappa objects.'),
 10: ('A_AREA', ('Mohenjo-daro', ['VS']), G, 'Assembly: Mohenjo-daro objects with it come from the citadel VS area more than other Mohenjo-daro objects.'),
 11: ('M_KIND', {'ctab'}, G, 'Maiden: new-text faces sit on copper tablets more than faces in general.'),
 13: ('M_CO', {'255'}, G, 'Rod/sceptre with banner: shares a face with koṭi (255) on new texts more than faces in general.'),
 14: ('M_COUNT', 'tall', G, 'Tax (large recurring sums): counts next to it on new texts are tall-stroke more than tall share among all counts.'),
 15: ('A_AREA', ('Mohenjo-daro', ['DKG']), G, 'First ward: Mohenjo-daro objects with it come from DK-G more than other Mohenjo-daro objects.'),
 18: ('M_KIND', {'mtab'}, G, 'Town: new-text faces sit on moulded tablets more than faces in general.'),
 19: ('M_KIND', {'tag', 'pot'}, G, 'Crate of fish (trade goods): new-text faces sit on tags or pots more than faces in general.'),
 21: ('M_CO', {'435'}, G, 'Banner with rod: shares a face with kōl (435) on new texts more than faces in general.'),
 22: ('T_BIN', {'middle'}, G, 'Third ward: dated objects with it sit in the middle bin more than other dated objects.'),
 24: ('P_PIC', {'Gaur', 'Stag', 'Goat', 'Tigr', 'Elep', 'Rhin', 'Hare'}, G, 'Three-peaks (hill country): picture is a wild hill/forest beast more than on other pictured objects.'),
 27: ('M_KIND', {'seal'}, G, 'Half-share: new-text faces sit on seals more than faces in general.'),
 28: ('M_POS', 'first', G, 'Weight/full measure: text-initial on new texts more than the average sign.'),
 29: ('P_PIC', {'Bull1'}, G, 'Horn: the picture is the one-horned bull (unicorn) more than on other pictured objects.'),
 30: ('P_PIC', {'Phyt'}, G, 'Spindle (cotton): the picture is a plant more than on other pictured objects.'),
 33: ('P_PIC', {'Scene', 'Mult', 'Anth', 'Archer'}, G, 'Proclamation (to a crowd): the picture shows people/a scene more than on other pictured objects.'),
 34: ('M_CO', {'335'}, G, 'Child of the town: shares a face with ūr (335) on new texts more than faces in general.'),
 35: ('M_POS', 'first', G, 'Bamboo-star (asterism name): text-initial on new texts more than the average sign.'),
 36: ('M_POS', 'first', G, 'Given (donor first): text-initial on new texts more than the average sign.'),
 37: ('A_AREA', ('Harappa', ['FGranery']), G, 'Grain measure: Harappa objects with it come from the Granary area more than other Harappa objects.'),
 40: ('T_BIN', {'late'}, G, 'Goldsmith (specialised craft): dated objects with it sit in the late bin more than other dated objects.'),
 41: ('M_KIND', {'ctab'}, G, 'Royal: new-text faces sit on copper tablets more than faces in general.'),
 42: ('M_KIND', {'ctab'}, G, 'Arrow (weapon, official): new-text faces sit on copper tablets more than faces in general.'),
 43: ('A_AREA', ('Harappa', ['FGranery']), G, 'Heap/stock: Harappa objects with it come from the Granary area more than other Harappa objects.'),
 44: ('P_PIC', STAR_PICS, G, 'First-star: the picture is a star-like motif more than on other pictured objects.'),
 45: ('P_PIC', {'Elep', 'Tigr', 'Rhin', 'Scene', 'Anth'}, G, 'King: the picture is a royal beast or a figure/scene more than on other pictured objects.'),
 48: ('M_CO', GRAIN, G, 'Produce: shares a face with other grain signs (752/416/845/501) on new texts more than faces in general.'),
 49: ('M_CO', GRAIN, G, 'Paddy field: shares a face with grain signs on new texts more than faces in general.'),
 50: ('M_CO', GRAIN, G, 'Heap of threshed grain: shares a face with other grain signs on new texts more than faces in general.'),
 52: ('M_KIND', {'tag'}, G, 'Partners: new-text faces sit on tags more than faces in general.'),
 53: ('M_CO', {'235'}, G, 'Servant of the house: shares a face with il (235) on new texts more than faces in general.'),
 54: ('M_CO', {'632', '140', '220', '407'}, G, 'Fish: shares a face with the other fish/star-name signs (632/140/220/407) on new texts more than faces in general.'),
 57: ('M_POS', 'last', G, 'Warrior (person title): text-final on new texts more than the average sign.'),
 58: ('M_KIND', {'ctab'}, G, 'Chest: new-text faces sit on copper tablets more than faces in general.'),
 60: ('T_BIN', {'middle'}, G, 'Dozen: dated objects with it sit in the middle bin more than other dated objects.'),
}
NEED2 = None  # set at run time: every item whose first outcome was not 'came true'

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'stage2':
    import json
    st = json.load(open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B_stage1.json'))
    need = sorted(int(i) for i, v in st.items() if v['out'] != 'came true')
    assert need == sorted(SECOND), (set(need) ^ set(SECOND))
    r2 = {}
    for i in need:
        obs, base, p, out = run_spec(i, SECOND[i])
        r2[i] = dict(obs=obs, base=base, p=p, out=out)
        print(f'[stage2] item {i} sign {SIGN[i]} -> {out} | {obs} vs {base} | P={p}', flush=True)
        json.dump(r2, open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B_stage2.json', 'w'))
    print('[stage2] done', flush=True)


# =====================================================================================================
# PART 5: WRITE replay_B.csv.  final = 'came true' if either stage came true, else the better of the two outcomes
# with the order  right direction only > too few > against  (too few is no evidence, against is evidence the other way).
# =====================================================================================================
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'write':
    import json, csv
    s1 = json.load(open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B_stage1.json'))
    s2 = json.load(open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B_stage2.json'))
    RANK = {'came true': 3, 'right direction only': 2, 'too few': 1, 'against': 0}
    fmt = lambda p: '' if p is None else f'{p:.4g}'
    with open('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['item', 'sign', 'word', 'first_prediction', 'first_base', 'first_observed', 'first_P', 'first_outcome',
                    'second_prediction', 'second_base', 'second_observed', 'second_P', 'second_outcome', 'final'])
        for i in range(1, 61):
            a = s1[str(i)]; b = s2.get(str(i))
            word = f'{TL.iloc[i-1].sound} ({TL.iloc[i-1].english})'
            if b is None: fin = a['out']
            else: fin = max([a['out'], b['out']], key=lambda o: RANK[o])
            w.writerow([i, SIGN[i], word, FIRST[i][3], a['base'], a['obs'], fmt(a['p']), a['out'],
                        SECOND[i][3] if b else '', b['base'] if b else '', b['obs'] if b else '', fmt(b['p']) if b else '', b['out'] if b else '', fin])
    df = pd.read_csv('/home/antigravity/Cuuper22/ivc/work_data/decoy/replay_B.csv')
    print('first_outcome', df.first_outcome.value_counts().to_dict()); print('final', df.final.value_counts().to_dict())
