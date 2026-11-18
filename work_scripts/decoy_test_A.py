#!/usr/bin/env python3
"""Decoy test A (blind). Section 1 = predictions, written from the word meanings only, before any sign data was looked at.
Section 2 = runner. Rules fixed in advance:
  came true            : direction right AND P < 0.05 on strat_shuffle_p (5000 seeded shuffles)
  right direction only : direction right, P >= 0.05
  against              : direction opposite (observed share <= mean share under shuffle for 'greater';
                         >= mean for 'less')
  too few              : fewer than 3 'has' rows
Base rate = pooled share of the outcome among ALL comparable rows (objects or faces) in the test universe.
Test types:
  KIND  : objects; outcome = object kind in set; shuffle strata = site (kind is the outcome, so site only)
  PIC   : objects with a picture label; outcome = picture label in set; strata = site|kind
  CO    : Lipi faces; has = sign on face; outcome = face also holds a sign from a named set; strata = site|kind
  COMU  : same on the NEW TEXTS (Mu); one stratum
"""
import sys, csv, time
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from decoy_loader import *

# ---------------- sign sets taken from the word meanings on the list ----------------
GRAIN   = {'752', '500', '416', '806', '320', '845', '711', '501'}      # paddy, granary, threshed heap, produce, field, sheaves, grain measure, stock
MEASURE = {'176', '463', '711', '171', '861', '820', '480'}             # cup, ration, grain measure, weight, quarter, share, seed-weight
SHARE   = {'861', '820', '070', '055'}                                  # quarter, share, half, hill share
WARD    = {'717', '741', '519'}
STAR    = {'220', '407', '140'}
MONTH   = {'900', '904'}
TITLE   = {'100', '400', '095', '742', '151', '104', '679', '482', '615', '137', '435'}
HILL    = {'503', '097', '055'}
PAIR    = {'700', '091', '690'}
HORNED  = {'Bull', 'Bull1', 'Bull2', 'Bull3', 'Zebu', 'Buff', 'Gaur', 'Stag', 'Goat'}
FIERCE  = {'Tigr', 'Rhin', 'Elep', 'Htgr'}
PRESTIGE = {'Bull1', 'Elep', 'Tigr', 'Rhin'}

# ---------------- SECTION 1: PREDICTIONS (one per item) ----------------
# (item, sign, test type, parameters, direction, one-line prediction)
P = [
 (1, '137', 'CO', GRAIN, 'greater', 'cultivator: shares a face with grain/field/granary signs more than faces in general'),
 (2, '220', 'CO', STAR | MONTH, 'greater', 'star: shares a face with other star names or month signs more than baseline (calendar vocabulary)'),
 (3, '400', 'CO', TITLE, 'greater', 'junior: shares a face with other person/title signs (elder, king, servant...) more than baseline'),
 (4, '235', 'KIND', {'seal', 'tag'}, 'greater', 'house: sits on seals/tags (household identity/property marks) more than on all objects'),
 (5, '717', 'CO', WARD, 'greater', 'second ward: shares a face with the first/third ward signs more than baseline'),
 (6, '440', 'KIND', {'tag'}, 'greater', 'received/bought: sits on tags (transaction tokens) more than all objects'),
 (7, '176', 'CO', GRAIN, 'greater', 'cup measure: shares a face with grain/commodity signs more than baseline'),
 (8, '904', 'KIND', {'ctab', 'mtab'}, 'greater', 'two months: sits on copper/moulded tablets (dated or terms-type texts) more than all objects'),
 (9, '463', 'CO', GRAIN, 'greater', 'ration measure: shares a face with grain signs more than baseline'),
 (10, '692', 'PIC', {'Mult', 'Scene'}, 'greater', 'assembly/council: objects carrying it show a several-figure or scene picture more than picture objects in general'),
 (11, '585', 'PIC', {'Anth', 'Scene', 'Mult'}, 'greater', 'maiden: objects carrying it show a human figure or scene picture more than picture objects in general'),
 (12, '752', 'CO', MEASURE, 'greater', 'paddy: shares a face with measure/share signs more than baseline (grain is measured)'),
 (13, '435', 'CO', {'742', '095', '100'}, 'greater', 'rod/sceptre: shares a face with king/staff-bearer/elder signs more than baseline'),
 (14, '840', 'KIND', {'tag', 'ctab'}, 'greater', 'tax/levy: sits on tags or copper tablets (administrative objects) more than all objects'),
 (15, '741', 'CO', WARD, 'greater', 'first ward: shares a face with the second/third ward signs more than baseline'),
 (16, '390', 'KIND', {'seal'}, 'greater', 'kindred/family: sits on seals (group/lineage identity) more than all objects'),
 (17, '700', 'COMU', set(VAL), 'less', 'pair: on the NEW TEXTS faces with it hold a count sign LESS often than baseline (it is already a number word)'),
 (18, '335', 'KIND', {'tag'}, 'greater', 'town: sits on tags (origin of goods) more than all objects'),
 (19, '632', 'PIC', {'Fish'}, 'greater', 'crate of fish: objects carrying it show a fish picture more than picture objects in general'),
 (20, '690', 'CO', PAIR, 'greater', 'bound/allied: shares a face with the pair/partner signs more than baseline'),
 (21, '255', 'PIC', {'Bull1'}, 'greater', 'banner: objects carrying it show the unicorn (the animal faced by a standard) more than picture objects in general'),
 (22, '519', 'CO', WARD, 'greater', 'third ward: shares a face with the first/second ward signs more than baseline'),
 (23, '527', 'PIC', FIERCE, 'greater', 'guard: objects carrying it show tiger/rhino/elephant more than picture objects in general'),
 (24, '097', 'CO', HILL, 'greater', 'Three-peaks: shares a face with other hill signs more than baseline'),
 (25, '100', 'CO', TITLE, 'greater', 'elder: shares a face with other person/title signs more than baseline'),
 (26, '095', 'CO', {'435', '742'}, 'greater', 'staff-bearer: shares a face with the rod/king signs more than baseline'),
 (27, '070', 'CO', SHARE, 'greater', 'half-share: shares a face with other share signs more than baseline'),
 (28, '171', 'CO', set(VAL), 'greater', 'weight/full measure: faces with it hold a count sign more often than baseline'),
 (29, '495', 'PIC', HORNED, 'greater', 'horn: objects carrying it show a horned animal more than picture objects in general'),
 (30, '605', 'KIND', {'tool'}, 'greater', 'spindle: sits on tools (spinning gear) more than all objects'),
 (31, '500', 'CO', GRAIN - {'500'}, 'greater', 'granary: shares a face with grain/stock signs more than baseline'),
 (32, '900', 'CO', set(VAL), 'greater', 'month: faces with it hold a count sign more often than baseline (months are counted)'),
 (33, '530', 'KIND', {'ctab', 'mtab'}, 'greater', 'proclamation: sits on copper/moulded tablets (public notices) more than all objects'),
 (34, '413', 'CO', TITLE, 'greater', 'child of: shares a face with person/title signs more than baseline'),
 (35, '140', 'CO', STAR, 'greater', 'Bamboo-star: shares a face with other star names more than baseline'),
 (36, '745', 'CO', set(VAL), 'greater', 'given: faces with it hold a count sign more often than baseline (things given are counted)'),
 (37, '711', 'CO', GRAIN - {'711'}, 'greater', 'grain measure: shares a face with grain signs more than baseline'),
 (38, '861', 'CO', SHARE, 'greater', 'quarter-share: shares a face with other share signs more than baseline'),
 (39, '151', 'CO', {'527', '500', '235'}, 'greater', 'keeper: shares a face with guard/granary/house signs more than baseline'),
 (40, '104', 'KIND', {'bangle', 'rod', 'tool'}, 'greater', 'goldsmith: sits on bangles/rods/tools (metal-working) more than all objects'),
 (41, '384', 'PIC', {'Pipal'}, 'greater', 'pipal/royal: objects carrying it show a pipal-leaf picture more than picture objects in general'),
 (42, '142', 'PIC', {'Archer'}, 'greater', 'arrow: objects carrying it show the bow-bearing figure more than picture objects in general'),
 (43, '501', 'CO', GRAIN - {'501'}, 'greater', 'heap/stock: shares a face with grain signs more than baseline'),
 (44, '407', 'CO', STAR, 'greater', 'First-star: shares a face with other star names more than baseline'),
 (45, '742', 'PIC', PRESTIGE, 'greater', 'king: objects carrying it show unicorn/elephant/tiger/rhino more than picture objects in general'),
 (46, '820', 'CO', SHARE, 'greater', 'share: shares a face with other share signs more than baseline'),
 (47, '615', 'CO', {'482'}, 'greater', 'foot/servant: shares a face with the servant sign 482 more than baseline'),
 (48, '806', 'CO', GRAIN, 'greater', 'produce: shares a face with grain signs more than baseline'),
 (49, '320', 'CO', {'752', '416', '845', '806'}, 'greater', 'paddy field: shares a face with paddy/heap/sheaves/produce signs more than baseline'),
 (50, '416', 'CO', {'752', '806', '845', '320'}, 'greater', 'heap of threshed grain: shares a face with paddy/produce/sheaves/field signs more than baseline'),
 (51, '503', 'CO', HILL, 'greater', 'hill: shares a face with other hill signs more than baseline'),
 (52, '091', 'CO', PAIR, 'greater', 'the pair/partners: shares a face with the pair/bound signs more than baseline'),
 (53, '482', 'CO', {'615'}, 'greater', 'servant: shares a face with sign 615 (foot/servant) more than baseline'),
 (54, '233', 'PIC', {'Fish', 'Gavi'}, 'greater', 'scabbard-fish: objects carrying it show a fish or gharial picture more than picture objects in general'),
 (55, '845', 'CO', GRAIN, 'greater', 'bundle of sheaves: shares a face with grain signs more than baseline'),
 (56, '480', 'CO', MEASURE - {'480'}, 'greater', 'seed-weight: shares a face with measure signs more than baseline'),
 (57, '679', 'PIC', {'Archer'}, 'greater', 'warrior: objects carrying it show the bow-bearing figure more than picture objects in general'),
 (58, '231', 'KIND', {'pot'}, 'greater', 'chest: sits on pots (containers) more than all objects'),
 (59, '055', 'CO', HILL | SHARE, 'greater', 'hill share: shares a face with hill or share signs more than baseline'),
 (60, '923', 'COMU', set(VAL), 'greater', 'dozen: on the NEW TEXTS faces with it hold a count sign more often than baseline'),
]

# ---------------- SECTION 2: RUNNER ----------------
def run_item(sign, typ, S, direction):
    if typ == 'KIND':
        has = objs.signs.apply(lambda z: sign in z).values
        outcome = objs.kind.isin(S).values
        strata = objs.site.astype(str).values
    elif typ == 'PIC':
        U = objs[objs.pic.notna()]
        has = U.signs.apply(lambda z: sign in z).values
        outcome = U.pic.isin(S).values
        strata = (U.site.astype(str) + '|' + U.kind.astype(str)).values
    elif typ == 'CO':
        toks = list(d.tok)
        has = np.array([sign in t for t in toks])
        outcome = np.array([any((x in S) and x != sign for x in t) for t in toks])
        strata = (d.site.astype(str) + '|' + d.kind.astype(str)).values
    elif typ == 'COMU':
        FM = faces_all('Mu')   # runner fix: each row is (tokens, parse, site, kind)
        toks = [tuple(r[0]) for r in FM]
        has = np.array([sign in t for t in toks])
        outcome = np.array([any((x in S) and x != sign for x in t) for t in toks])
        strata = np.array([str(r[2]) + '|' + str(r[3]) for r in FM])
    base = float(outcome.mean())
    n = int(has.sum())
    if n < 3:
        return base, None, None, 'too few', n
    r = strat_shuffle_p(has, outcome, strata, direction=direction)
    obs, mean_sim, p = r
    right = obs > mean_sim if direction == 'greater' else obs < mean_sim
    if not right: oc = 'against'
    elif p < 0.05: oc = 'came true'
    else: oc = 'right direction only'
    return base, obs, p, oc, n, mean_sim

if __name__ == '__main__':
    rows = []
    for (item, sign, typ, S, direction, pred) in P:
        t0 = time.time()
        try:
            res = run_item(sign, typ, S, direction)
            base, obs, p, oc, n = res[:5]
            ms = res[5] if len(res) > 5 else None
            obs_txt = ('n=%d, share %.4f, shuffle mean %.4f' % (n, obs, ms)) if obs is not None else 'n=%d' % n
            rows.append((item, sign, pred + ' [dir=%s]' % direction, '%.4f' % base, obs_txt, '' if p is None else '%.4f' % p, oc))
        except Exception as e:
            rows.append((item, sign, pred + ' [dir=%s]' % direction, '', 'could not run: %r' % (e,), '', 'could not run'))
        print(item, sign, rows[-1][-1], rows[-1][4], 'P=%s' % rows[-1][5], '%.1fs' % (time.time() - t0), flush=True)
    with open('/home/antigravity/Cuuper22/ivc/work_data/decoy/results_A.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['item', 'sign', 'prediction', 'base_rate', 'observed', 'P', 'outcome'])
        w.writerows(rows)
    import collections
    print(collections.Counter(r[-1] for r in rows))
