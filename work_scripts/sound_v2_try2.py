#!/usr/bin/env python3
"""Rescue try 2 (a different word) for every value whose try 1 did not point the right way, and the
sharpened reruns for the 17 values that pointed the right way.  Words and predictions fixed here before the run;
DEDR entry numbers are from the local copy (work_data/lexicons/dedr/).  Writes work_data/sound_v2/try2.csv and
sharpen.csv.  Run: python3 sound_v2_try2.py"""
import os
from v2_common import *
OUT = f'{ROOT}/work_data/sound_v2'


def frame_swap(a, b, cat='LM'):
    """a and b stand in the same frames (same sign before and after) more than b and signs of b's frequency do."""
    ctx = collections.defaultdict(set); use = collections.Counter(); seen = set()
    for x, P, st, g in faces_all(cat):
        if x in seen: continue
        seen.add(x); y = ('^',) + tuple(x) + ('$',)
        for i in range(1, len(y) - 1):
            ctx[y[i]].add((y[i - 1], y[i + 1])); use[y[i]] += 1
    bs = set(b) if not isinstance(b, str) else {b}
    cb = set().union(*[ctx[s] for s in bs]); nb = sum(use[s] for s in bs)
    if use[a] < 3 or nb < 3: return None
    obs = len(ctx[a] & cb)
    peers = [len(ctx[a] & ctx[s]) for s in use if s not in bs and s != a and 0.5 * nb <= use[s] <= 2 * nb]
    k = sum(v >= obs for v in peers)
    return res(obs > np.median(peers), (k + 1) / (len(peers) + 1), f'{obs} shared frames with {sorted(bs)} against median {np.median(peers):.0f} for {len(peers)} signs of the same frequency ({cat}, distinct texts)')


def opener_names(s, cat='LM'):
    rows = []
    for x, P, st, g in faces_all(cat):
        if not P['name'] or g not in ('seal', 'SEAL'): pass
        if not P['names']: continue
        op = 'opener' in P['roles']; rows.append((op, any(s in n for n in P['names'])))
    base = np.mean([o for o, h in rows]); sub = [o for o, h in rows if h]
    return share(np.array([o for o, h in rows]), np.array(sub), 'texts with a name that carry an opener')


def end_porter_comb(s, cat='L'): return ending_of_names(s, ['porter', 'comb'], cat=cat)


def fish_last_spear(s, cat='Mu'):
    """among names ending in a fish sign, those ending in s take the spear more than the other fish-final names."""
    rows = []
    se = objs[objs.seal]
    if 'L' in cat: rows += [(nm, e) for nm, e in zip(se.name, se.ending)]
    if 'M' in cat or cat == 'Mu':
        m = M[(M.cls == 'seal') & ~M.partnered]
        for x, P in zip(m.tok, m.P):
            nm = tuple(P['name']); e = 'spear' if x and x[-1] == '520' else 'jar' if '740' in x else 'porter' if x and x[-1] in PORTER else 'none'
            rows.append((nm, e))
    rows = [(nm, e) for nm, e in rows if nm and nm[-1] in FISH and e != 'none']
    a = [e == 'spear' for nm, e in rows if nm[-1] == s]; b = [e == 'spear' for nm, e in rows if nm[-1] != s]
    if len(a) < 3: return None
    p = fisher_exact([[sum(a), len(a) - sum(a)], [sum(b), len(b) - sum(b)]], alternative='greater')[1]
    return res(np.mean(a) > np.mean(b), p, f'fish-final names: ending in {s} take the spear {sum(a)}/{len(a)} = {np.mean(a):.0%} against {sum(b)}/{len(b)} = {np.mean(b):.0%} for other fish ({cat})')


def next_count(s, cat='Mu'): return adjacent(s, set(VAL), 'next', cat)


def local_city(s, cat='LM'):
    sites = collections.defaultdict(collections.Counter); use = collections.Counter()
    for x, P, st, g in faces_all(cat):
        for a in set(x): sites[a][st] += 1; use[a] += 1
    if use[s] < 5: return None
    top = lambda a: max(sites[a].values()) / use[a]
    peers = [top(a) for a in use if a != s and 0.6 * use[s] <= use[a] <= 1.6 * use[s]]
    k = sum(v < top(s) for v in peers)
    return res(top(s) > np.median(peers), 1 - k / max(1, len(peers)), f'top city holds {top(s):.0%} ({sites[s].most_common(1)[0][0]}) against median {np.median(peers):.0%} for {len(peers)} signs ({cat})')


def batch_check(s):
    t = {x for x, c in zip(d.tok, d.complete_txt) if s in x}
    return None if len(t) < 3 else res(True, 1.0, f'{len(t)} distinct texts')


# sign: (old word, lesson from the failed checks, new word with DEDR, prediction, callable)
T2 = {
 '231': ('puḷḷimīn', 'not shared in houses at any level; the mark is one short stroke', 'oru-mīn "first star" (oru one, DEDR 990 in the 1025 block; mīṉ 4885); guess', 'a "first" house: names with it carry an opener (a holding) more than names overall', lambda: opener_names('231')),
 '226': ('kūṭumīn', 'seal-heavy, counted with tall strokes (containers), texts end with no owner ending', 'kūṭu "receptacle for grain, coop, hive, pen" (DEDR 1883): a fish basket, a goods unit', 'objects carrying it have no animal more often than objects overall', lambda: share(objs.noanimal, objs[has_obj('226')].noanimal, 'objects with no animal')),
 '236': ('vēykūṭumīn', 'too few in houses; ends texts, comb follows 7 times', 'vēy-kūṭu "thatched receptacle for grain" (vēy 5541 + kūṭu 1883): a grain bin', 'at Harappa it sits in mound F (granary area)', lambda: harappa_area('236', 'F')),
 '706': ('kaḷam', 'not a granary-mound sign; counted with three tall strokes', 'kalam "vessel, earthenware" (DEDR 1305): a vessel-ful', 'objects carrying it also carry the cup 700', lambda: cooccur('706', {'700'}, 'L', unit='object')),
 '705': ('kaḷam', '(try 1 direction only)', 'kalam "vessel" (DEDR 1305)', 'objects carrying it also carry the cup 700', lambda: cooccur('705', {'700'}, 'L', unit='object')),
 '550': ('vāy', 'average spread over sites; heads the 550-060 cap and the pair 550-527', 'koṭiṟu "pincers" (DEDR 2052) ~ koṭu "to give" (2053): "given"', 'its faces carry a number more than faces overall', lambda: cooccur('550', set(VAL), 'LM')),
 '900': ('tiṅkaḷ', 'no second number; counts beside it stop at 5 (a month would run to 12)', 'maruppu "horns of the crescent moon" (4720) ~ marukaṉ "descendant, member of a clan" (4715)', 'a kin word: house-mates share it right before the jar', lambda: house_share('900', pos='prejar')),
 '692': ('office (opening)', 'fewer sites than its peers: a local institution', 'kaṭṭu "tie, fastening" (1147; the X is crossed bars) ~ kaṭṭu "to pay up, dues" (1149): the dues office', 'its faces are on sealings (goods stamped) in the second catalogue, unpartnered texts', lambda: group_share('692', ['sealing'], 'Mu')),
 '617': ('title word (after kō)', 'not bigger at equal length', 'ūr̤iyaṉ "slave, servant", Ma. ūr̤an "servant of kings" (DEDR 758): kō ūr̤iyaṉ "king\'s servant"; picture unread', 'names with it close with the porter or comb', lambda: end_porter_comb('617', 'LM')),
 '435': ('miṉ', 'fewer sites than peers; always 255-435-(690|156)', 'iṭi "stroke, blow" (DEDR 443; the zig-zag as a strike)', 'names with it close with an office ending (spear or porter) more than names overall', lambda: ending_of_names('435', ['spear', 'porter'], cat='LM')),
 '527': ('(none)', 'not house-shared; always after 550/555; ends the text with no jar', 'paṭi "rung of a ladder, grade" (3850; the hatched box) ~ paṭi "ordinary measure of capacity, fixed daily allowance" (3849): "allowance"', 'its faces carry a number more than faces overall', lambda: cooccur('527', set(VAL), 'LM')),
 '416': ('irukavar', 'no house sharing', 'kavai "fork; place where several ways meet, crossroads" (1325): a place', 'a place word is local: one city holds more of it than for its peers', lambda: local_city('416')),
 '413': ('katir "ear of grain"', 'not a mound-F sign even among tablets', 'katir "ray of light, sun"; katiravaṉ sun (DEDR 1193, a different word from 1194)', 'it sits on one object with the crescent 900', lambda: cooccur('413', {'900', '904'}, 'L', unit='object')),
 '717': ('aṭi', 'seals bigger, not shared in houses, not deeper', 'tāḷ "foot, foot of a tree or mountain, stem" (DEDR 3185): the stem of a line (guess)', 'names with it take the plain jar (owner) more than names overall (second catalogue, new texts)', lambda: ending_of_names('717', ['jar'], cat='Mu')),
 '350': ('(none)', 'not shared in houses', 'nāṟu "seedling; to sprout, come into being, be born; origin" (DEDR 2919): seedling (goods)', 'objects carrying it have no animal more often than objects overall', lambda: share(objs.noanimal, objs[has_obj('350')].noanimal, 'objects with no animal')),
 '923': ('maru', 'not shared before the jar in houses', 'the outlined crescent is the crescent 900 written another way (same word as 900)', '923 and 900 stand in the same frames', lambda: frame_swap('923', '900')),
 '832': ('kaṇ "eye"', 'fewer sites; the shape list calls it a leaf with a stroke', 'kaṇṇi "sprout, shoot, tender leaf" (DEDR 1185): a leaf word', 'it stands in the same frames as the leaf signs 803/798/840', lambda: frame_swap('832', ['803', '798', '840'])),
 '480': ('kuṉṟu', 'not local; pottery-heavy with a stroke after it', 'kuṉṟi Abrus seed (1865), used as a goldsmith\'s weight (4636: a seed "weighing two kuṉṟi")', 'a weight unit: the next sign is a count (second catalogue, new texts)', lambda: next_count('480', 'LM')),
 '482': ('kōṭu', 'no house sharing (0.07 expected)', 'kōṭu + kāṇi: "hill share" (2049, 1444), peak with the diamond inside (guess)', 'names with it take the plain jar (holder) more than names overall', lambda: ending_of_names('482', ['jar'], cat='LM')),
 '495': ('kompu', 'no house sharing (0.15 expected)', 'maruppu "horn, branch" (4720) ~ marukaṉ "descendant" (4715)', 'names with it take the plain jar (owner) more than names overall', lambda: ending_of_names('495', ['jar'], cat='LM')),
 '463': ('mukkōṭu', 'no house sharing', 'same word as 460, three triangles = three peaks drawn another way', '463 and 460 stand in the same frames', lambda: frame_swap('463', '460')),
 '501': ('kumi', 'one moulded batch', 'pōr "heap of unthreshed grain, straw stack" (DEDR 4591)', 'needs 3 distinct texts', lambda: batch_check('501')),
 '165': ('nāḷ', 'too few fresh texts', 'poḻutu "time, sun, day" (DEDR 4559)', 'its faces carry a number (count of days)', lambda: cooccur('165', set(VAL), 'LM')),
 '097': ('kāppu', 'too few fresh texts', 'kaṭṭu "tie, bind" (1147): a bound labourer, the man between two bars', 'seals smaller than seals of the same sign count', lambda: seal_size('097', False)),
 '530': ('paṟai', 'too few counts', 'the half bow-tie is the drum 540 paṟai written another way', '530 and 540 stand in the same frames', lambda: frame_swap('530', '540')),
}

# sharpen: the 17 that pointed the right way. Tighter group (seals only, shuffle within area and 3-ft band)
# or a bigger sample (second-catalogue texts with no Lipi partner added).
SH = {
 '235': ('vēymīn', 'house-mates share it, seals, within band', lambda: house_share('235')),
 '240': ('mīmīn', 'house-mates share it, seals, within band', lambda: house_share('240')),
 '590': ('paṭṭi', 'house-mates share it, seals, within band', lambda: house_share('590')),
 '741': ('orukuṭi', 'house-mates share it, seals, within band', lambda: house_share('741')),
 '760': ('maka', 'house-mates share it right before the jar, within band', lambda: house_share('760', pos='prejar')),
 '840': ('iṇai', 'texts with two names or two jars (Lipi + new second-catalogue texts)', None),
 '690': ('piṇai', 'house-mates share it, all objects, within band', lambda: house_share('690', where='any', seals=False)),
 '503': ('malai', 'place word: one city holds more of it than for its peers', lambda: local_city('503')),
 '388': ('aracu', 'seals bigger at equal sign count', lambda: seal_size('388', True)),
 '752': ('maka', 'frames shared with 760 (same word)', lambda: frame_swap('752', '760')),
 '595': ('paṭṭi', 'frames shared with 590 (same word)', lambda: frame_swap('595', '590')),
 '632': ('pal', 'frames shared with 630 (same word)', lambda: frame_swap('632', '630')),
 '384': ('aracu', 'seals bigger at equal sign count', lambda: seal_size('384', True)),
 '175': ('iṟai', 'frames shared with 176 (same word)', lambda: frame_swap('175', '176')),
 '104': ('name front', 'house-mates share it, all objects, within band', lambda: house_share('104', where='any', seals=False)),
 '382': ('aracu', 'frames shared with 388/384 (same word)', lambda: frame_swap('382', ['388', '384'])),
 '320': ('name word', 'house-mates share it, all objects, within band', lambda: house_share('320', where='any', seals=False)),
}


def two_parties(s, cat='LM'):
    a = b = c = e = 0
    for x, P, st, g in faces_all(cat):
        if not P['names']: continue
        two = len(P['jars']) >= 2 or len(P['names']) >= 2
        a += 1; b += two
        if s in x: c += 1; e += two
    p = binomtest(e, c, b / a, alternative='greater').pvalue
    return res(e / c > b / a, p, f'texts with two names or two jars {e}/{c} = {e / c:.0%} against {b / a:.0%} ({cat})')


SH['840'] = SH['840'][:2] + (lambda: two_parties('840'),)

if __name__ == '__main__':
    for name, T, cols in (('try2', T2, 5), ('sharpen', SH, 3)):
        rows = []
        for k, (s, v) in enumerate(T.items()):
            r = v[-1]()
            base = dict(sign=s, old_word=v[0])
            if cols == 5: base.update(lesson=v[1], new_word=v[2], prediction=v[3])
            else: base.update(test=v[1])
            if r is None: base.update(result='too few cases', outcome='n/a', p='')
            else:
                ok, p, txt = r; base.update(result=txt, outcome='yes' if ok and p <= 0.10 else 'direction only' if ok else 'no', p=f'{p:.3g}')
            rows.append(base); print(f'[{name} {k + 1}/{len(T)}] {s}: {base["outcome"]} | {base["result"]} | P {base["p"]}', flush=True)
        pd.DataFrame(rows).to_csv(f'{OUT}/{name}.csv', index=False)
        print(name, pd.DataFrame(rows).outcome.value_counts().to_dict())
