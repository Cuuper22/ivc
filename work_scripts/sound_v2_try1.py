#!/usr/bin/env python3
"""Rescue try 1 for the 38 values whose first check went against them.
Same word, better test: the first check was asked whether it was the wrong slot, the wrong comparison group,
or too small a count; each line below states the redesigned test (direction fixed here, before the run).
Writes work_data/sound_v2/try1.csv.  Run: python3 sound_v2_try1.py"""
import os
from v2_common import *

OUT = f'{ROOT}/work_data/sound_v2'; os.makedirs(OUT, exist_ok=True)


def name_has_seq(seq):
    def f(o):
        for g in o.names:
            for i in range(len(g) - len(seq) + 1):
                if tuple(g[i:i + len(seq)]) == tuple(seq): return True
        return False
    return f


def any_of(*fs): return lambda o: any(f(o) for f in fs)


def counts_le(s, lim, cat):
    v = [VAL[a] for a in counts_beside(s, cat)]
    if len(v) < 3: return None
    k = sum(x <= lim for x in v)
    return res(k == len(v), 0.0 if k == len(v) else 1.0, f'counts beside it <= {lim}: {k} of {len(v)} ({collections.Counter(v).most_common(5)}; {cat})')


# sign: (word, why the first test was wrong, redesigned test, callable)
T1 = {
 '233': ('varimīn', 'by-sign test counted every use; a crest is the house part of a name, and a cadet line writes it out as 415-220',
         'house-mates share the crest at name level, 233 or its spelled-out form 415-220 counted together, chance within area and 3-ft band',
         lambda: house_share('233', pred=any_of(name_has_seq(['233']), name_has_seq(['415', '220'])))),
 '231': ('puḷḷimīn', 'all objects and all of Mohenjo-daro as the comparison; tablets and copper dilute a seal-owner crest',
         'house-mates share it in a seal name, chance within area and 3-ft band', lambda: house_share('231')),
 '226': ('kūṭumīn', 'seal-or-record was the wrong question for a star name; a star name should behave like the plain fish 220 in names',
         'it is the last sign of a name that takes an ending (as 220 is 63% of the time on seals) more than signs overall', lambda: ending_of_names('226', ['jar', 'jar+man', 'spear', 'porter', 'comb'], cat='L')),
 '236': ('vēykūṭumīn', 'too few house objects (0.17 expected)', 'house-mates share it, all objects, chance within band', lambda: house_share('236', where='any', seals=False)),
 '705': ('kaḷam', 'records against seals is not what a threshing-floor word predicts', 'at Harappa it sits in mound F (the granary and threshing-platform area)', lambda: harappa_area('705', 'F')),
 '706': ('kaḷam', 'same as 705', 'at Harappa it sits in mound F', lambda: harappa_area('706', 'F')),
 '803': ('il', 'any use counted; the house word is the first sign of a name', 'house-mates share it as the first name sign, chance within area and 3-ft band', lambda: house_share('803', pos='first')),
 '550': ('vāy', 'an office word ("the Gate") is not a record word; an office is citywide', 'it occurs at more sites than signs of the same frequency (both catalogues)', lambda: multi_site('550', 'LM')),
 '900': ('tiṅkaḷ', 'a month need not carry a second number; the month itself is the counted thing', 'a month runs to 12: counts beside it should include 6 or more about 3 times in 8 (Lipi + new second-catalogue texts)', lambda: (lambda v: res(sum(x > 5 for x in v) / len(v) >= 0.2, binomtest(sum(x > 5 for x in v), len(v), 3 / 8, alternative='less').pvalue if sum(x > 5 for x in v) / len(v) < 0.2 else 0.0, f'counts beside it above 5: {sum(x > 5 for x in v)} of {len(v)} ({collections.Counter(v).most_common(6)}; LM)'))([VAL[a] for a in counts_beside('900', 'LM')])),
 '140': ('ammai', 'any use counted', 'house-mates share it as the first name sign, chance within band', lambda: house_share('140', pos='first')),
 '575': ('kōṭṭai', 'pots and copper diluted the record share', 'a capacity measure lives on clay tablets: faces on tablets (second catalogue, miniature tablets)', lambda: group_share('575', ['miniature tablet'], 'Mu')),
 '692': ('office (opening)', 'an office head is citywide, not record-bound', 'more sites than signs of the same frequency (both catalogues)', lambda: multi_site('692', 'LM')),
 '617': ('title word', 'raw size mixes text length', 'seals bigger at equal sign count', lambda: seal_size('617', True)),
 '435': ('miṉ', 'by-sign house test, 2 expected', 'the compound mutal-miṉ (255-435) is one name carried across cities: more sites than signs of the same frequency', lambda: multi_site('435', 'LM')),
 '904': ('irutiṅkaḷ', 'records against seals is not what a date predicts', 'a date word sits on a face that carries a number', lambda: cooccur('904', set(VAL), 'LM')),
 '527': ('second member (no sound)', 'by-sign house test', 'house-mates share it, chance within band (seals)', lambda: house_share('527')),
 '585': ('kaṉṉi?', 'records against seals; the "Seven Maidens" reading predicts the seven, not the object', 'the count before it is seven in the second catalogue', lambda: res(*(lambda c: (c.count('017') + c.count('007') > len(c) / 2, binomtest(c.count('017') + c.count('007'), max(1, len(c)), 0.05, alternative='greater').pvalue, f'counts before it {collections.Counter(c).most_common(4)} (Mu)'))(counts_beside('585', 'M', 'before')))),
 '125': ('vēṭṭuvaṉ', 'house test, 1.7 expected', 'a clan crest goes with one animal: seals with it carry one animal type more than seals overall (top animal share)',
         lambda: (lambda se: share(se.animal.eq(se[se.signs.apply(lambda z: '125' in z)].animal.mode()[0]), se[se.signs.apply(lambda z: '125' in z)].animal.eq(se[se.signs.apply(lambda z: '125' in z)].animal.mode()[0]), 'seals with its commonest animal'))(objs[objs.seal & ~objs.noanimal])),
 '440': ('koḷ', 'pots in the record group', 'a receipt word lives on sealings and tablets: second catalogue, faces on sealings', lambda: group_share('440', ['sealing'], 'Mu')),
 '416': ('irukavar', 'house test with 1 expected', 'house-mates share it, all objects, chance within band', lambda: house_share('416', where='any', seals=False)),
 '413': ('katir', 'mound F against all Harappa objects; 413 is a tablet sign and tablets are spread over mounds E and F',
         'Harappa tablets with it from mound F against Harappa tablets overall', lambda: (lambda H: share(H.area.str.startswith('F'), H[H.signs.apply(lambda z: '413' in z)].area.str.startswith('F'), 'Harappa tablets from mound F'))(objs[(objs.site == 'Harappa') & objs.type.str.startswith('TAB')])),
 '717': ('aṭi', 'already two rescue lines: servant (size) and founder (house share); founder predicts older',
         'Mohenjo-daro objects with it sit deeper than their area (older)', lambda: depth_rel('717', True)),
 '350': ('name front (no sound)', 'house test', 'house-mates share it in a seal name, chance within band', lambda: house_share('350')),
 '923': ('maru', 'any use; the kin word sits before the jar', 'house-mates share it right before the jar, chance within band', lambda: house_share('923', pos='prejar')),
 '832': ('kaṇ', 'records against seals; an eye/overseer word is an office', 'more sites than signs of the same frequency (both catalogues)', lambda: multi_site('832', 'LM')),
 '480': ('kuṉṟu', 'mound F for a hill word was the wrong place test', 'a place (hill) word is local: one city holds more of it than for signs of the same frequency',
         lambda: (lambda: None)()),
 '482': ('kōṭu', 'house test, 0.27 expected', 'house-mates share it, all objects, chance within band', lambda: house_share('482', where='any', seals=False)),
 '460': ('mukkōṭu', 'any use; the diary saw it right before the jar in one room', 'house-mates share it right before the jar, chance within band', lambda: house_share('460', pos='prejar')),
 '070': ('ampu', 'house test, 1.1 expected', 'arrow sits next to the spear: next sign is the spear 520 (second catalogue)', lambda: adjacent('070', {'520'}, 'next', 'Mu')),
 '501': ('kumi', 'all 30 copies are one moulded batch; the area test counts one event 30 times', 'a heap/stock word sits beside counts; counted on distinct texts, not on 30 copies of one mould', lambda: (lambda t: None if len(t) < 3 else cooccur('501', set(VAL), 'L'))({x for x, c in zip(d.tok, d.complete_txt) if '501' in x})),
 '495': ('kompu', 'house test, 0.09 expected', 'house-mates share it, all objects, chance within band', lambda: house_share('495', where='any', seals=False)),
 '165': ('nāḷ?', 'records against seals is not the day test', 'the day follows the month: preceded by 900 (second catalogue)', lambda: adjacent('165', {'900'}, 'prev', 'Mu')),
 '171': ('niṟai', 'already two lines (cup face, house); a weight/measure word should take the container count', 'counts beside it are tall strokes (second catalogue)', lambda: count_series('171', 'tall', 'Mu')),
 '463': ('mukkōṭu', 'house test 0.28 expected', 'house-mates share it, all objects, chance within band', lambda: house_share('463', where='any', seals=False)),
 '091': ('iruvar', 'house test 0.08 expected', 'a pair-heading word opens the text (second catalogue)', lambda: text_pos('091', 'first', 'Mu')),
 '877': ('nālkāṇi', 'before-jar was the wrong slot for a holding word; holdings sit in the opener slot', 'it opens the text (second catalogue)', lambda: text_pos('877', 'first', 'Mu')),
 '097': ('kāppu?', 'records against seals; a guard is a person with an office ending', 'names with it take the porter ending (second catalogue)', lambda: ending_of_names('097', ['porter'], cat='Mu')),
 '530': ('paṟai', 'records against seals; DEDR 4032 paṟai is also "a measure of capacity"', 'counts beside it are tall strokes (both catalogues)', lambda: count_series('530', 'tall', 'LM')),
}


def local_city(s, cat='LM'):
    """place-word test: largest single-city share of its faces against signs of the same frequency."""
    sites = collections.defaultdict(collections.Counter); use = collections.Counter()
    for x, P, st, g in faces_all(cat):
        for a in set(x): sites[a][st] += 1; use[a] += 1
    if use[s] < 5: return None
    top = lambda a: max(sites[a].values()) / use[a]
    peers = [top(a) for a in use if a != s and 0.6 * use[s] <= use[a] <= 1.6 * use[s]]
    k = sum(v < top(s) for v in peers)
    return res(top(s) > np.median(peers), 1 - k / max(1, len(peers)), f'top city holds {top(s):.0%} ({sites[s].most_common(1)[0][0]}) against median {np.median(peers):.0%} for {len(peers)} signs of similar frequency ({cat})')


T1['480'] = T1['480'][:3] + (lambda: local_city('480'),)

if __name__ == '__main__':
    rows = []
    for k, (s, (word, why, test, fn)) in enumerate(T1.items()):
        r = fn()
        if r is None: rows.append(dict(sign=s, word=word, why_first_test_wrong=why, test=test, result='too few cases', outcome='n/a', p='')); continue
        ok, p, txt = r
        rows.append(dict(sign=s, word=word, why_first_test_wrong=why, test=test, result=txt, outcome='yes' if ok and p <= 0.10 else 'direction only' if ok else 'no', p=f'{p:.3g}'))
        print(f'[{k + 1}/{len(T1)}] {s} {word}: {rows[-1]["outcome"]} | {txt} | P {p:.3g}', flush=True)
    pd.DataFrame(rows).to_csv(f'{OUT}/try1.csv', index=False)
    print(pd.DataFrame(rows).outcome.value_counts().to_dict())
