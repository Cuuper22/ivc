#!/usr/bin/env python3
"""Decoy replay A: for each of 60 items, (1) look at the sign on the Lipi catalogue only,
(2) write one prediction from the word's meaning about an unseen fact, (3) run it, (4) one redesign if it failed.
Run:  python3 decoy_replay_A.py look      -> prints step-1 profiles (Lipi only)
      python3 decoy_replay_A.py run1      -> runs first predictions
      python3 decoy_replay_A.py run2      -> runs second predictions for the items that did not come true, writes CSV
"""
import sys, collections, json
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from decoy_loader import *
import numpy as np, pandas as pd
from scipy.stats import binomtest

ITEMS = pd.read_csv('/home/claude/ivc/work_data/decoy/test_list.csv', dtype=str).fillna('')
NUM = set(VAL)

# ---------------- step 1: Lipi-only look ----------------
LF = [(f.tok, f.kind, f.site) for f in d.itertuples()]

def look(s):
    """Lipi faces only: kinds, sites, neighbours, counts beside (stroke style), first/last, face-mates."""
    fs = [x for x in LF if s in x[0]]
    kinds = collections.Counter(k for _, k, _ in fs); sites = collections.Counter(si for _, _, si in fs)
    prev = collections.Counter(); nxt = collections.Counter(); mates = collections.Counter()
    first = last = 0; cnt_beside = collections.Counter()
    for t, _, _ in fs:
        if t[0] == s: first += 1
        if t[-1] == s: last += 1
        for i, x in enumerate(t):
            if x != s: continue
            p = t[i-1] if i > 0 else '^'; n = t[i+1] if i < len(t)-1 else '$'
            prev[p] += 1; nxt[n] += 1
            for y in (p, n):
                if y in NUM: cnt_beside['short' if y in SHORT else 'tall' if y in TALL else 'other'] += 1
        for y in set(t) - {s}: mates[y] += 1
    nuse = sum(t.count(s) for t, _, _ in fs)
    return dict(nfaces=len(fs), kinds=kinds.most_common(6), sites=sites.most_common(5), prev=prev.most_common(6),
                next=nxt.most_common(6), first=first, last=last, counts_beside=dict(cnt_beside),
                mates=mates.most_common(8), nuse=nuse)

if __name__ == '__main__' and sys.argv[1:] == ['look']:
    # base rates on Lipi for comparison
    allf = [t for t, _, _ in LF if len(t) > 1]
    print('Lipi base: first-position share per use ~ 1/len; faces', len(LF))
    for r in ITEMS.itertuples():
        L = look(r.sign)
        print(f"\n#{r.item} sign {r.sign} '{r.sound}' = {r.english}")
        for k, v in L.items(): print(f"   {k}: {v}")

# ---------------- tests (steps 2-4) ----------------
MU = [(t, k, si) for t, k, si in kfaces('Mu')]           # new texts: (tokens, kind, site)
VALS = set(VAL)
CITADEL = {'Mohenjo-daro': ('SD', 'L'), 'Harappa': ('AB',), 'Dholavira': ('Castle', 'Bailey')}

def _binom(k, n, base, direction='greater'):
    if n < 3: return dict(base=base, obs=(k / n if n else None), n=n, P=None)
    p = binomtest(k, n, base, alternative=direction).pvalue
    return dict(base=base, obs=k / n, n=n, P=p, k=k)

def mu_pos(s, where):
    """new texts: share of s's uses at text-initial / text-final position vs all sign uses (faces of 2+ signs)."""
    tot = hit = k = n = 0
    for t, _, _ in MU:
        if len(t) < 2: continue
        tot += len(t); hit += 1          # one first and one last per face
        for i, x in enumerate(t):
            if x == s:
                n += 1; k += (i == 0) if where == 'first' else (i == len(t) - 1)
    return _binom(k, n, hit / tot)

def mu_adj(s, T, side='next'):
    """new texts: share of s's neighbours (next / prev / both) that are in T vs T's share among all neighbours."""
    T = set(T); allk = alln = k = n = 0
    for t, _, _ in MU:
        for i in range(len(t) - 1):
            alln += 1; allk += t[i + 1] in T     # base: share of tokens in T among all bigram positions
        for i, x in enumerate(t):
            if x != s: continue
            nb = []
            if side in ('next', 'both') and i < len(t) - 1: nb.append(t[i + 1])
            if side in ('prev', 'both') and i > 0: nb.append(t[i - 1])
            if side == 'both':
                if nb: n += 1; k += any(y in T for y in nb)
            else:
                for y in nb: n += 1; k += y in T
    base = allk / alln
    if side == 'both': base = 1 - (1 - base) ** 2
    return _binom(k, n, base)

def mu_count(s):
    """new texts: faces with s carry a number sign more than all new-text faces."""
    allf = [any(x in VALS for x in t if x != s) for t, _, _ in MU]
    sf = [any(x in VALS for x in t if x != s) for t, _, _ in MU if s in t]
    return _binom(sum(sf), len(sf), np.mean(allf))

def mu_kind(s, kinds):
    kinds = set(kinds)
    return _binom(sum(k in kinds for t, k, _ in MU if s in t), sum(s in t for t, _, _ in MU), np.mean([k in kinds for _, k, _ in MU]))

def mu_site(s, site):
    return _binom(sum(si == site for t, _, si in MU if s in t), sum(s in t for t, _, _ in MU), np.mean([si == site for _, _, si in MU]))

def mu_cooc(s, T):
    T = set(T)
    sf = [bool(T & (set(t) - {s})) for t, _, _ in MU if s in t]
    return _binom(sum(sf), len(sf), np.mean([bool(T & set(t)) for t, _, _ in MU]))

def _shuffle(sub, outcome, s, direction='greater'):
    has = sub.signs.apply(lambda z: s in z).values
    strata = (sub.site.astype(str) + '|' + sub.kind.astype(str)).values
    base = float(np.mean(outcome))
    if has.sum() < 3: return dict(base=base, obs=(float(np.mean(outcome[has])) if has.any() else None), n=int(has.sum()), P=None)
    obs, mean_shuf, P = strat_shuffle_p(has, outcome, strata, direction=direction)
    return dict(base=base, obs=obs, n=int(has.sum()), P=P, shuf_mean=mean_shuf)

def pic(s, labels, direction='greater'):
    sub = objs[objs.pic.notna()]
    return _shuffle(sub, sub.pic.isin(set(labels)).values, s, direction)

def tbin(s, bins, direction='greater'):
    sub = objs[objs.bin != '']
    return _shuffle(sub, sub.bin.isin(set(bins)).values, s, direction)

def area(s, spec, direction='greater'):
    """spec: {site: (area prefixes)}; objects at those sites with a known area; outcome = area starts with a prefix."""
    sub = objs[objs.site.isin(spec) & ~objs.area.isin(['--', '', '-'])]
    out = np.array([str(a).startswith(spec[si]) for si, a in zip(sub.site, sub.area)])
    return _shuffle(sub, out, s, direction)

def verdict(r, direction='greater'):
    if r is None or r['P'] is None or r.get('n', 0) < 3: return 'too few'
    right = r['obs'] > r.get('shuf_mean', r['base']) if direction == 'greater' else r['obs'] < r.get('shuf_mean', r['base'])
    if not right: return 'against'
    return 'came true' if r['P'] < 0.05 else 'right direction only'

# ---------------- step 2: first predictions (written after step-1 look, before any run) ----------------
CIT = CITADEL
HAR_E = {'Harappa': ('E',)}
MOH_DK = {'Mohenjo-daro': ('DK',)}
TWO = {'002', '012', '032'}
FIRST = {
 1: ("cultivator is an occupational title heading the text: on new texts 137 is text-initial more than base", lambda: mu_pos('137', 'first')),
 2: ("star belongs to the calendar: on new texts 220 shares a face with month signs 900/904 more than base", lambda: mu_cooc('220', {'900', '904'})),
 3: ("junior qualifies the person and closes the name: on new texts 400 is text-final more than base", lambda: mu_pos('400', 'last')),
 4: ("house: Mohenjo-daro objects with 235 come from the DK residential area more than base (shuffle site|kind)", lambda: area('235', MOH_DK)),
 5: ("second ward is a district of Mohenjo-daro (its main city): new texts with 717 are at Mohenjo-daro more than base", lambda: mu_site('717', 'Mohenjo-daro')),
 6: ("received/bought is a transaction: new-text faces with 440 carry a number more than base", lambda: mu_count('440')),
 7: ("cup measure is a unit: new-text faces with 176 carry a number more than base", lambda: mu_count('176')),
 8: ("two months is a duration counted in records: new-text faces with 904 carry a number more than base", lambda: mu_count('904')),
 9: ("ration measure is issued on tickets/vessels: new texts with 463 are on tags or pots more than base", lambda: mu_kind('463', {'tag', 'pot'})),
 10: ("assembly/council sits in the citadel: objects with 692 come from citadel areas (MD SD/L, Harappa AB, Dholavira Castle/Bailey) more than base", lambda: area('692', CIT)),
 11: ("maiden is a person: objects with 585 show human figure / scene pictures more than base", lambda: pic('585', {'Anth', 'Scene', 'Mult', 'Archer'})),
 12: ("paddy is a commodity labelled on goods: new texts with 752 are on tags or pots more than base", lambda: mu_kind('752', {'tag', 'pot'})),
 13: ("rod/sceptre is an emblem of authority: objects with 435 come from citadel areas more than base", lambda: area('435', CIT)),
 14: ("tax/levy is an amount: new-text faces with 840 carry a number more than base", lambda: mu_count('840')),
 15: ("first ward is a district of Mohenjo-daro (its main city): new texts with 741 are at Mohenjo-daro more than base", lambda: mu_site('741', 'Mohenjo-daro')),
 16: ("kindred/family closes a lineage name: on new texts 390 is text-final more than base", lambda: mu_pos('390', 'last')),
 17: ("pair = two: on new texts a count of two (002/012/032) stands next to 700 more than base", lambda: mu_adj('700', TWO, 'both')),
 18: ("town is a local place name of Harappa (its main city): new texts with 335 are at Harappa more than base", lambda: mu_site('335', 'Harappa')),
 19: ("crate of fish: objects with 632 show fish or gharial pictures more than base", lambda: pic('632', {'Fish', 'Gavi'})),
 20: ("bound/allied is bound to the rod-sceptre pair: on new texts 690 is preceded by 435/436 more than base", lambda: mu_adj('690', {'435', '436'}, 'prev')),
 21: ("banner = the standard set before the unicorn: objects with 255 show the unicorn more than base", lambda: pic('255', {'Bull1'})),
 22: ("third ward is a district of Harappa (its main city): new texts with 519 are at Harappa more than base", lambda: mu_site('519', 'Harappa')),
 23: ("guard posts are at the citadel gates: objects with 527 come from citadel areas more than base", lambda: area('527', CIT)),
 24: ("Three-peaks is a mountain place: objects with 097 show the mountain goat/markhor more than base", lambda: pic('097', {'Goat'})),
 25: ("elder is a title followed by the ending: on new texts 100 is followed by 740 more than base", lambda: mu_adj('100', {'740'}, 'next')),
 26: ("staff-bearer is an official of the citadel: objects with 095 come from citadel areas more than base", lambda: area('095', CIT)),
 27: ("half-share is a fraction of an amount: new-text faces with 070 carry a number more than base", lambda: mu_count('070')),
 28: ("weight/full measure is followed by its amount in tall strokes: on new texts 171 is followed by a tall count more than base", lambda: mu_adj('171', TALL, 'next')),
 29: ("horn: objects with 495 show strongly horned beasts (buffalo, goat, gaur, zebu, rhino) more than base", lambda: pic('495', {'Buff', 'Goat', 'Gaur', 'Zebu', 'Rhin'})),
 30: ("spindle is a craft: Harappa objects with 605 come from the craft mounds E/ET more than base", lambda: area('605', HAR_E)),
 31: ("granary goods are sealed with tags: new texts with 500 are on tags more than base", lambda: mu_kind('500', {'tag'})),
 32: ("month is counted: on new texts 900 is preceded by a number more than base", lambda: mu_adj('900', VALS, 'prev')),
 33: ("proclamation comes from the citadel: objects with 530 come from citadel areas more than base", lambda: area('530', CIT)),
 34: ("child-of opens a filiation formula: on new texts 413 is text-initial more than base", lambda: mu_pos('413', 'first')),
 35: ("Bamboo-star is a star (calendar) name: on new texts 140 shares a face with month signs 900/904 more than base", lambda: mu_cooc('140', {'900', '904'})),
 36: ("given is a transaction: new-text faces with 745 carry a number more than base", lambda: mu_count('745')),
 37: ("grain measure is followed by its amount in tall strokes: on new texts 711 is followed by a tall count more than base", lambda: mu_adj('711', TALL, 'next')),
 38: ("quarter-share is followed by an amount: on new texts 861 is followed by a number more than base", lambda: mu_adj('861', VALS, 'next')),
 39: ("keeper is a title closing the text: on new texts 151 is text-final more than base", lambda: mu_pos('151', 'last')),
 40: ("goldsmith is an occupational title heading the text: on new texts 104 is text-initial more than base", lambda: mu_pos('104', 'first')),
 41: ("pipal: objects with 384 show the pipal leaf or plant pictures more than base", lambda: pic('384', {'Pipal', 'Phyt'})),
 42: ("arrow: objects with 142 show the archer / hunting scene pictures more than base", lambda: pic('142', {'Archer', 'Scene', 'Mult'})),
 43: ("heap/stock is counted: new-text faces with 501 carry a number more than base", lambda: mu_count('501')),
 44: ("First-star is a star (calendar) name: on new texts 407 shares a face with month signs 900/904 more than base", lambda: mu_cooc('407', {'900', '904'})),
 45: ("king sits in the citadel: objects with 742 come from citadel areas more than base", lambda: area('742', CIT)),
 46: ("share/holding is followed by its amount: on new texts 820 is followed by a number more than base", lambda: mu_adj('820', VALS, 'next')),
 47: ("foot is a length measure: new-text faces with 615 carry a number more than base", lambda: mu_count('615')),
 48: ("produce is labelled on goods: new texts with 806 are on tags or pots more than base", lambda: mu_kind('806', {'tag', 'pot'})),
 49: ("paddy field is measured in amounts: new-text faces with 320 carry a number more than base", lambda: mu_count('320')),
 50: ("threshed-grain heap is labelled on goods: new texts with 416 are on tags or pots more than base", lambda: mu_kind('416', {'tag', 'pot'})),
 51: ("hill: objects with 503 show mountain beasts (goat/markhor, branch-horned stag) more than base", lambda: pic('503', {'Goat', 'Stag'})),
 52: ("the pair = two partners: on new texts a count of two stands next to 091 more than base", lambda: mu_adj('091', TWO, 'both')),
 53: ("servant is a title followed by the ending: on new texts 482 is followed by 740 more than base", lambda: mu_adj('482', {'740'}, 'next')),
 54: ("scabbard-fish: objects with 233 show fish or gharial pictures more than base", lambda: pic('233', {'Fish', 'Gavi'})),
 55: ("bundle of sheaves: objects with 845 show plant pictures more than base", lambda: pic('845', {'Phyt', 'Pipal'})),
 56: ("seed-weight is followed by its amount: on new texts 480 is followed by a number more than base", lambda: mu_adj('480', VALS, 'next')),
 57: ("warrior: objects with 679 show human / archer / scene pictures more than base", lambda: pic('679', {'Anth', 'Archer', 'Scene', 'Mult'})),
 58: ("chest is a container that was sealed: new texts with 231 are on tags more than base", lambda: mu_kind('231', {'tag'})),
 59: ("hill share is a land share counted: new-text faces with 055 carry a number more than base", lambda: mu_count('055')),
 60: ("dozen is a counted quantity: new-text faces with 923 carry a number more than base", lambda: mu_count('923')),
}
FIRST_DIR = {}   # all 'greater'

def fmt(x): return '' if x is None else (f'{x:.4g}' if isinstance(x, float) else str(x))

if __name__ == '__main__' and sys.argv[1:] == ['run1']:
    res = {}
    for r in ITEMS.itertuples():
        i = int(r.item); pred, fn = FIRST[i]; out = fn(); v = verdict(out)
        base = out.get('shuf_mean', out['base'])
        res[i] = dict(item=i, sign=r.sign, word=f"{r.sound} ({r.english})", first_prediction=pred, first_base=fmt(base),
                      first_observed=f"{fmt(out['obs'])} (n={out['n']})", first_P=fmt(out['P']), first_outcome=v)
        print(f"#{i} {r.sign} {r.english}: base {fmt(base)} obs {fmt(out['obs'])} n={out['n']} P={fmt(out['P'])} -> {v}", flush=True)
    json.dump(res, open('/home/claude/ivc/work_data/decoy/replay_A_stage1.json', 'w'), ensure_ascii=False, indent=1)

# ---------------- step 4: one redesign for items whose first prediction did not come true ----------------
HAR_F = {'Harappa': ('F',)}
SECOND = {
 1: ("cultivator works with plough oxen: objects with 137 show short-horned / humped bulls more than base", lambda: pic('137', {'Zebu', 'Bull', 'Bull2', 'Bull3'})),
 2: ("star goes with the other star names: on new texts 220 shares a face with 140/407 more than base", lambda: mu_cooc('220', {'140', '407'})),
 4: ("house name heads the address: on new texts 235 is text-initial more than base", lambda: mu_pos('235', 'first')),
 5: ("second ward heads the address: on new texts 717 is text-initial more than base", lambda: mu_pos('717', 'first')),
 6: ("received/bought marks goods: new texts with 440 are on tags or pots more than base", lambda: mu_kind('440', {'tag', 'pot'})),
 7: ("cup measure belongs on vessels: new texts with 176 are on pots more than base", lambda: mu_kind('176', {'pot'})),
 8: ("two months dates a delivery: new texts with 904 are on tags more than base", lambda: mu_kind('904', {'tag'})),
 9: ("ration measure is issued at the granary: Harappa objects with 463 come from Mound F (granary area) more than base", lambda: area('463', HAR_F)),
 10: ("council heads the text: on new texts 692 is text-initial more than base", lambda: mu_pos('692', 'first')),
 11: ("maiden is a person term taking the ending: on new texts 585 is followed by 740 more than base", lambda: mu_adj('585', {'740'}, 'next')),
 12: ("paddy: objects with 752 show plant pictures more than base", lambda: pic('752', {'Phyt', 'Pipal'})),
 13: ("sceptre marks authority: new texts with 435 are on seals more than base", lambda: mu_kind('435', {'seal'})),
 15: ("first ward is an address on labels: new texts with 741 are on tags more than base", lambda: mu_kind('741', {'tag'})),
 16: ("kindred is counted (number of kin): on new texts 390 is preceded by a number more than base", lambda: mu_adj('390', VALS, 'prev')),
 17: ("pair is counted in tall-stroke amounts: on new texts a tall count stands next to 700 more than base", lambda: mu_adj('700', TALL, 'both')),
 18: ("town name is preceded by its qualifier 575: on new texts 335 is preceded by 575 more than base", lambda: mu_adj('335', {'575'}, 'prev')),
 19: ("crate of fish goes with the fish signs: on new texts 632 shares a face with a fish sign more than base", lambda: mu_cooc('632', FISH)),
 21: ("banner is followed by its pole 435/436: on new texts 255 is followed by 435/436 more than base", lambda: mu_adj('255', {'435', '436'}, 'next')),
 22: ("third ward lies in the lower town: Harappa objects with 519 come from Mound E/ET more than base", lambda: area('519', HAR_E)),
 23: ("guard is a title closing the text: on new texts 527 is text-final more than base", lambda: mu_pos('527', 'last')),
 24: ("Three-peaks is a place with a keeper: on new texts 097 is followed by 151 more than base", lambda: mu_adj('097', {'151'}, 'next')),
 26: ("staff-bearer title is followed by 520: on new texts 095 is followed by 520 more than base", lambda: mu_adj('095', {'520'}, 'next')),
 29: ("horn is a traded good: new texts with 495 are on tags or pots more than base", lambda: mu_kind('495', {'tag', 'pot'})),
 30: ("spindle goes with 760: on new texts 605 is followed by 760 more than base", lambda: mu_adj('605', {'760'}, 'next')),
 33: ("proclamation heads the text: on new texts 530 is text-initial more than base", lambda: mu_pos('530', 'first')),
 34: ("child-of is followed by the parent's name 575/892: on new texts 413 is followed by 575/892 more than base", lambda: mu_adj('413', {'575', '892'}, 'next')),
 35: ("Bamboo-star is a personal name heading the text: on new texts 140 is text-initial more than base", lambda: mu_pos('140', 'first')),
 36: ("given marks goods: new texts with 745 are on tags or pots more than base", lambda: mu_kind('745', {'tag', 'pot'})),
 37: ("grain measure is used at the granary: Harappa objects with 711 come from Mound F more than base", lambda: area('711', HAR_F)),
 40: ("goldsmith works in the craft quarter: Harappa objects with 104 come from Mound E/ET more than base", lambda: area('104', HAR_E)),
 41: ("royal sits in the citadel: objects with 384 come from citadel areas more than base", lambda: area('384', CIT)),
 42: ("arrow is for hunting: objects with 142 show hunted wild beasts (rhino, tiger, gaur, buffalo, stag) more than base", lambda: pic('142', {'Rhin', 'Tigr', 'Gaur', 'Buff', 'Stag'})),
 43: ("heap/stock is kept at the granary: Harappa objects with 501 come from Mound F more than base", lambda: area('501', HAR_F)),
 44: ("First-star is a deity: objects with 407 show human-figure / archer / scene pictures more than base", lambda: pic('407', {'Anth', 'Archer', 'Scene', 'Mult'})),
 45: ("king's seal: new texts with 742 are on seals more than base", lambda: mu_kind('742', {'seal'})),
 48: ("ripened crop: objects with 806 show plant pictures more than base", lambda: pic('806', {'Phyt', 'Pipal'})),
 49: ("paddy field is followed by 920: on new texts 320 is followed by 920 more than base", lambda: mu_adj('320', {'920'}, 'next')),
 50: ("threshed-grain heap is counted: new-text faces with 416 carry a number more than base", lambda: mu_count('416')),
 54: ("scabbard-fish goes with the fish signs: on new texts 233 shares a face with a fish sign more than base", lambda: mu_cooc('233', FISH)),
 55: ("sheaves are counted in tall strokes: on new texts a tall count stands next to 845 more than base", lambda: mu_adj('845', TALL, 'both')),
 57: ("warrior is a title closing the text: on new texts 679 is text-final more than base", lambda: mu_pos('679', 'last')),
 58: ("chest contents are counted: new-text faces with 231 carry a number more than base", lambda: mu_count('231')),
}

ORDER = {'came true': 3, 'right direction only': 2, 'against': 1, 'too few': 0}
if __name__ == '__main__' and sys.argv[1:] == ['run2']:
    res = {int(k): v for k, v in json.load(open('/home/claude/ivc/work_data/decoy/replay_A_stage1.json')).items()}
    for i in sorted(res):
        R = res[i]
        if R['first_outcome'] == 'came true':
            R.update(second_prediction='', second_base='', second_observed='', second_P='', second_outcome='', final='came true')
        else:
            pred, fn = SECOND[i]; out = fn(); v = verdict(out); base = out.get('shuf_mean', out['base'])
            R.update(second_prediction=pred, second_base=fmt(base), second_observed=f"{fmt(out['obs'])} (n={out['n']})",
                     second_P=fmt(out['P']), second_outcome=v,
                     final='came true' if v == 'came true' else max([R['first_outcome'], v], key=ORDER.get))
            print(f"#{i} {R['sign']} {R['word']}: base {fmt(base)} obs {fmt(out['obs'])} n={out['n']} P={fmt(out['P'])} -> {v}", flush=True)
    cols = 'item,sign,word,first_prediction,first_base,first_observed,first_P,first_outcome,second_prediction,second_base,second_observed,second_P,second_outcome,final'.split(',')
    pd.DataFrame([res[i] for i in sorted(res)])[cols].to_csv('/home/claude/ivc/work_data/decoy/replay_A.csv', index=False)
    df = pd.DataFrame([res[i] for i in sorted(res)])
    print('first_outcome:', df.first_outcome.value_counts().to_dict()); print('final:', df.final.value_counts().to_dict())
