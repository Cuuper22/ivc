#!/usr/bin/env python3
"""Decoy test, tester B. Predictions fixed BEFORE any sign data was computed or looked at.

Every prediction below comes only from the English meaning on test_list.csv plus general knowledge of what such a
word would do on seals, tablets, tags, pots and copper tablets. No sign's data was viewed when writing them.

Procedure (same for all 60 items, fixed in advance):
  unit        one object (Lipi catalogue, table objs) or one new text (second catalogue, partnered == False) when cat = 'Mu'
  has         the object / text carries the sign
  outcome     a True/False fact outside the sign's slot (picture, findspot area, kind of object, other signs on the object)
  base rate   the share of `outcome` the shuffle expects for the sign's objects (mean over 5,000 shuffles of the sign's labels
              inside site|kind strata, seed 12345). The raw share in the whole universe is printed too.
  observed    share of `outcome` among the sign's objects
  verdict     "came true"            = observed beats the base rate in the predicted direction AND P < 0.05 (strat_shuffle_p, 5,000 shuffles)
              "right direction only" = right direction, P >= 0.05
              "against"              = observed equal to or on the other side of the base rate
              "too few"              = fewer than 3 objects carry the sign in the universe
  strata      site|kind for every test, EXCEPT tests whose outcome is the object kind itself: there the outcome is constant inside a
              site|kind stratum (the test could never come true), so those shuffle inside site only.
  co-occurrence sets never include the sign itself; "number sign" = any sign in VAL other than the sign itself.
"""
import sys, csv, time
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from decoy_loader import *
import numpy as np

# ---------------------------------------------------------------------------------------------------------------
# PREDICTIONS (written first; not changed after running)
# type: ('co', {signs})      object also carries one of these signs (the other list words named), direction greater/less
#       ('num',)             object / text also carries a number sign
#       ('kind', {kinds})    object is of one of these kinds (shuffle within site only)
#       ('pic', {labels})    object's picture is one of these (universe: objects with a picture)
#       ('area', name)       findspot area inside the city (universe: objects with a known area at the listed cities)
# ---------------------------------------------------------------------------------------------------------------
GRAIN = {'752', '500', '806', '320', '845', '416', '711'}
WARDS = {'717', '741', '519'}
P = {
 1: ('137', 'cultivator', ('co', GRAIN), 'L', 'greater', 'objects with it also carry a grain/field word (paddy, granary, produce, paddy field, sheaves, threshed grain, grain measure) more than chance'),
 2: ('220', 'star', ('co', {'900', '904', '407', '140'}), 'L', 'greater', 'objects with it also carry a calendar/star-name word (month, two months, First-star, Bamboo-star) more than chance'),
 3: ('400', 'junior', ('kind', {'seal'}), 'L', 'greater', 'a personal kin-title word: sits on seals more than chance'),
 4: ('235', 'house', ('co', WARDS | {'335'}), 'L', 'greater', 'an address word: objects with it also carry a ward or town word more than chance'),
 5: ('717', 'second ward', ('co', {'235', '335'}), 'L', 'greater', 'an address word: objects with it also carry house or town more than chance'),
 6: ('440', 'received, bought', ('kind', {'tag'}), 'L', 'greater', 'a transaction word: sits on tags (sealings on goods) more than chance'),
 7: ('176', 'cup measure', ('num',), 'L', 'greater', 'a measure: objects with it carry a number sign more than chance'),
 8: ('904', 'two months', ('co', {'463', '752', '711', '501', '500'}), 'L', 'greater', 'a ration-period word: objects with it also carry a ration/grain word more than chance'),
 9: ('463', 'ration measure', ('num',), 'L', 'greater', 'a measure: objects with it carry a number sign more than chance'),
 10: ('692', 'assembly, council', ('area', 'citadel'), 'L', 'greater', 'an institution: found in citadel areas (Mohenjo SD, Harappa AB, Kalibangan KLB-1, Dholavira Castle/Bailey) more than chance'),
 11: ('585', 'maiden', ('pic', {'Anth', 'Scene', 'Mult', 'Archer', 'Phyt'}), 'L', 'greater', 'a female/goddess word: its objects show human-figure, scene or plant pictures more than chance'),
 12: ('752', 'paddy, grain', ('num',), 'L', 'greater', 'a commodity: objects with it carry a number sign more than chance'),
 13: ('435', 'rod, sceptre', ('co', {'742', '095'}), 'L', 'greater', 'regalia: objects with it also carry king or staff-bearer more than chance'),
 14: ('840', 'tax, levy', ('num',), 'L', 'greater', 'a levy: objects with it carry a number sign more than chance'),
 15: ('741', 'first ward', ('co', {'235', '335'}), 'L', 'greater', 'an address word: objects with it also carry house or town more than chance'),
 16: ('390', 'kindred, family', ('co', {'413', '100', '400'}), 'L', 'greater', 'a kin word: objects with it also carry child-of, elder or junior more than chance'),
 17: ('700', 'pair', ('num',), 'L', 'less', 'a word that itself counts: objects with it carry a separate number sign LESS than chance'),
 18: ('335', 'town', ('co', WARDS), 'L', 'greater', 'a place word: objects with it also carry a ward word more than chance'),
 19: ('632', 'crate of fish', ('pic', {'Fish', 'Gavi'}), 'L', 'greater', 'a fish commodity: its objects show fish or gharial pictures more than chance'),
 20: ('690', 'bound, allied', ('co', {'091', '390'}), 'L', 'greater', 'a relation word: objects with it also carry partners or kindred more than chance'),
 21: ('255', 'banner', ('pic', {'Bull1'}), 'L', 'greater', 'a standard/banner: its objects show the unicorn (the animal drawn with a standard) more than chance'),
 22: ('519', 'third ward', ('co', {'235', '335'}), 'L', 'greater', 'an address word: objects with it also carry house or town more than chance'),
 23: ('527', 'guard', ('area', 'citadel'), 'L', 'greater', 'a guard: found in citadel areas more than chance'),
 24: ('097', 'Three-peaks', ('co', {'335', '503'}), 'L', 'greater', 'a mountain place name: objects with it also carry town or hill more than chance'),
 25: ('100', 'elder', ('kind', {'seal'}), 'L', 'greater', 'a personal kin-title word: sits on seals more than chance'),
 26: ('095', 'staff-bearer', ('co', {'435', '742'}), 'L', 'greater', 'an official: objects with it also carry rod/sceptre or king more than chance'),
 27: ('070', 'half-share', ('num',), 'Mu', 'greater', 'a fraction: on the NEW TEXTS, texts with it carry a number sign more than chance'),
 28: ('171', 'weight, full measure', ('co', {'752', '416', '501', '845', '806', '632'}), 'L', 'greater', 'a measure of goods: objects with it also carry a goods word more than chance'),
 29: ('495', 'horn', ('pic', {'Gaur', 'Buff', 'Zebu', 'Bull', 'Goat', 'Rhin', 'Stag'}), 'L', 'greater', 'horn: its objects show big-horned animals other than the unicorn more than chance'),
 30: ('605', 'spindle', ('kind', {'tool', 'bangle', 'rod', 'other'}), 'L', 'greater', 'a craft object: sits on small inscribed objects (tools, bangles, rods, other) more than chance'),
 31: ('500', 'grain bin, granary', ('area', 'granary'), 'L', 'greater', 'a granary: found in the granary areas (Harappa FGranery, Mohenjo SD citadel granary mound) more than chance'),
 32: ('900', 'month', ('num',), 'L', 'greater', 'months are counted: objects with it carry a number sign more than chance'),
 33: ('530', 'proclamation', ('kind', {'mtab'}), 'L', 'greater', 'a mass message: sits on moulded tablets more than chance'),
 34: ('413', 'child of', ('kind', {'seal'}), 'L', 'greater', 'a personal-name kin marker: sits on seals more than chance'),
 35: ('140', 'Bamboo-star', ('co', {'220'}), 'L', 'greater', 'a star name: objects with it also carry star more than chance'),
 36: ('745', 'given', ('kind', {'tag'}), 'L', 'greater', 'a transaction word: sits on tags more than chance'),
 37: ('711', 'grain measure', ('num',), 'Mu', 'greater', 'a measure: on the NEW TEXTS, texts with it carry a number sign more than chance'),
 38: ('861', 'quarter-share', ('num',), 'Mu', 'greater', 'a fraction: on the NEW TEXTS, texts with it carry a number sign more than chance'),
 39: ('151', 'keeper', ('co', {'500', '231', '501', '752'}), 'L', 'greater', 'a store keeper: objects with it also carry granary, chest, stock or grain more than chance'),
 40: ('104', 'goldsmith', ('kind', {'seal'}), 'Mu', 'greater', 'a craftsman title: on the NEW TEXTS, sits on seals more than chance'),
 41: ('384', 'pipal; royal', ('pic', {'Phyt', 'Pipal', 'Scene'}), 'L', 'greater', 'pipal: its objects show plant, pipal-leaf or (tree-deity) scene pictures more than chance'),
 42: ('142', 'arrow', ('pic', {'Archer'}), 'L', 'greater', 'arrow: its objects show the figure with a bow more than chance'),
 43: ('501', 'heap, stock', ('num',), 'L', 'greater', 'a stock: objects with it carry a number sign more than chance'),
 44: ('407', 'First-star', ('co', {'220'}), 'L', 'greater', 'a star name: objects with it also carry star more than chance'),
 45: ('742', 'king', ('co', {'435', '255', '095'}), 'L', 'greater', 'a ruler: objects with it also carry sceptre, banner or staff-bearer more than chance'),
 46: ('820', 'share, holding', ('num',), 'Mu', 'greater', 'a share: on the NEW TEXTS, texts with it carry a number sign more than chance'),
 47: ('615', 'foot; servant', ('co', {'742', '151', '104'}), 'L', 'greater', 'a servant of someone: objects with it also carry king, keeper or goldsmith more than chance'),
 48: ('806', 'produce, ripened crop', ('kind', {'tag', 'pot'}), 'L', 'greater', 'a commodity: sits on tags or pots (goods labels) more than chance'),
 49: ('320', 'paddy field', ('co', {'752', '806', '845', '416'}), 'L', 'greater', 'a field: objects with it also carry paddy, produce, sheaves or threshed grain more than chance'),
 50: ('416', 'heap of threshed grain', ('num',), 'L', 'greater', 'a grain quantity: objects with it carry a number sign more than chance'),
 51: ('503', 'hill', ('co', {'097', '055'}), 'L', 'greater', 'a hill word: objects with it also carry Three-peaks or hill-share more than chance'),
 52: ('091', 'the pair, partners', ('co', {'137', '104', '482', '679', '527', '151'}), 'L', 'greater', 'partners: objects with it also carry an occupation word more than chance'),
 53: ('482', 'servant', ('co', {'742', '151', '104'}), 'L', 'greater', 'a servant of someone: objects with it also carry king, keeper or goldsmith more than chance'),
 54: ('233', 'scabbard-fish', ('pic', {'Fish', 'Gavi'}), 'L', 'greater', 'a fish: its objects show fish or gharial pictures more than chance'),
 55: ('845', 'bundle of sheaves', ('num',), 'L', 'greater', 'a counted commodity: objects with it carry a number sign more than chance'),
 56: ('480', 'seed-weight', ('num',), 'Mu', 'greater', 'a small weight unit: on the NEW TEXTS, texts with it carry a number sign more than chance'),
 57: ('679', 'warrior', ('pic', {'Archer', 'Scene', 'Anth', 'Mult'}), 'L', 'greater', 'a warrior: its objects show human figures, bowman or scenes more than chance'),
 58: ('231', 'chest', ('kind', {'tag'}), 'L', 'greater', 'a container: sits on tags (sealings on containers) more than chance'),
 59: ('055', 'hill share', ('co', {'503', '097'}), 'L', 'greater', 'a hill share: objects with it also carry hill or Three-peaks more than chance'),
 60: ('923', 'dozen', ('co', {'752', '632', '845', '416', '501'}), 'L', 'greater', 'a count of goods: objects with it also carry a goods word more than chance'),
}
assert len(P) == 60
# ===================== END OF PREDICTIONS =====================


def citadel(site, area):
    a = str(area)
    return ((site == 'Mohenjo-daro' and a.startswith('SD')) or (site == 'Harappa' and a.startswith('AB')) or
            (site == 'Kalibangan' and a.startswith('KLB-1')) or (site == 'Dholavira' and (a.startswith('Castle') or a.startswith('Bailey'))))


def granary(site, area):
    a = str(area)
    return (site == 'Harappa' and a.startswith('FGran')) or (site == 'Mohenjo-daro' and a.startswith('SD'))


def run(item):
    s, en, (typ, *arg), cat, direc, text = P[item]
    if cat == 'Mu':
        U = M[M.partnered == False]
        signs = [set(t) for t in U.tok]; site = list(U.site); kind = list(U.kind)
    else:
        U = objs
        signs = list(U.signs); site = list(U.site); kind = list(U.kind)
    n = len(signs); keep = np.ones(n, bool)
    if typ == 'co':
        T = set(arg[0]) - {s}; out = np.array([bool(z & T) for z in signs])
    elif typ == 'num':
        T = set(VAL) - {s}; out = np.array([bool(z & T) for z in signs])
    elif typ == 'kind':
        out = np.array([k in arg[0] for k in kind])
    elif typ == 'pic':
        pic = list(U.pic); keep = np.array([p is not None and p == p for p in pic]); out = np.array([p in arg[0] for p in pic])
    elif typ == 'area':
        area = list(U.area)
        cities = {'citadel': {'Mohenjo-daro', 'Harappa', 'Kalibangan', 'Dholavira'}, 'granary': {'Harappa', 'Mohenjo-daro'}}[arg[0]]
        f = citadel if arg[0] == 'citadel' else granary
        keep = np.array([si in cities and str(a) not in ('--', '', 'nan') for si, a in zip(site, area)])
        out = np.array([f(si, a) for si, a in zip(site, area)])
    has = np.array([s in z for z in signs])
    strata = np.array([f'{si}' if typ == 'kind' else f'{si}|{k}' for si, k in zip(site, kind)])
    has, out, strata = has[keep], out[keep], strata[keep]
    raw = float(out.mean())
    r = strat_shuffle_p(has, out, strata, direction=direc, n=5000, seed=12345)
    if r is None:
        return dict(n=int(has.sum()), raw=raw, obs=None, base=None, P=None, outcome='too few')
    obs, base, p = r
    right = obs > base if direc == 'greater' else obs < base
    oc = ('came true' if p < 0.05 else 'right direction only') if right else 'against'
    return dict(n=int(has.sum()), raw=raw, obs=obs, base=base, P=p, outcome=oc)


if __name__ == '__main__':
    rows = []; t0 = time.time()
    for i in range(1, 61):
        r = run(i); s, en, pr, cat, direc, text = P[i]
        rows.append((i, s, r, text, direc, cat))
        print(f'[{i:2d}/60 {100*i/60:5.1f}% {time.time()-t0:5.0f}s] sign {s} ({en}): n={r["n"]} obs={r["obs"]} base={r["base"]} P={r["P"]} -> {r["outcome"]}', flush=True)
    with open('/home/claude/ivc/work_data/decoy/results_B.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['item', 'sign', 'prediction', 'base_rate', 'observed', 'P', 'outcome'])
        for i, s, r, text, direc, cat in rows:
            pred = f'[{"new texts" if cat == "Mu" else "Lipi"}; {"higher" if direc == "greater" else "lower"}] {text}'
            fmt = lambda x: '' if x is None else f'{x:.4f}'
            base = '' if r['base'] is None else f'{r["base"]:.4f} (shuffle-expected; raw universe share {r["raw"]:.4f})'
            obs = '' if r['obs'] is None else f'{r["obs"]:.4f} (n={r["n"]})'
            if r['obs'] is None: obs = f'n={r["n"]}'
            w.writerow([i, s, pred, base, obs, fmt(r['P']), r['outcome']])
    from collections import Counter
    print('COUNTS', Counter(r['outcome'] for _, _, r, _, _, _ in rows))
