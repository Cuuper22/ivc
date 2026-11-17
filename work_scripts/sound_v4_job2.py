#!/usr/bin/env python3
"""Job 2 of the fourth sound pass: the coverage push.  The 25 signs without a built-on value that block the most
faces from reading start to finish (ranked by sound_v4_common.gains, 705/706 handled in sound_v4_job1.py).
For each: the word (picture fits, sound-alike does the slot's job), prediction A, a better test B of the same word,
and for some a new word C to try if A and B miss.  Every word and prediction below was written into this file
before it was first run.  'fresh' = the tested fact was not printed while choosing; 'seen' = it was visible in the
sign profiles (top neighbours, kinds, top sites) printed while choosing.
Writes work_data/sound_v4/job2_tests.csv."""
from sound_v4_common import *
OPEN = {'920', '692', '550', '820'}
MEAS = {'705', '706', '320', '711', '575', '540', '171', '700'}
PERSON = {'090', '095', '617', '520', '151', '153', '154', '155', '156', '157', '158', '100', '140'}
HERD = {'Bull', 'Bull1:W', 'Buff', 'Gaur', 'Goat:8'}
BEAD = {'Chanhu-daro', 'Lothal', 'Dholavira'}
COAST = {'Lothal', 'Dholavira', 'Bala-kot', 'Gola Dhoro (Bagasra)', 'Kanmer', 'Surkotada', 'Desalpur', 'Juna Khatiya', 'abroad', 'Ur', 'Failaka',
         "Ra's al-Junayz", 'Kish', 'Susa', 'Nippur', "Qala'at al-Bahrain", 'Tell Umma', 'Tello', 'Girsu', 'Saar', 'Janabiyah', 'Kalba'}
TIMEPLACE = {'904', '900', '920', '335', '615', '503'}
WARD = {'741', '742', '745'}


def sites_share(s, sites, cat='LM'):
    S_ = {s} if isinstance(s, str) else set(s)
    rows = kfaces(cat)
    return share([st in sites for x, k, st in rows], [st in sites for x, k, st in rows if S_ & set(x)], f'faces at {"/".join(sorted(sites))[:40]} ({cat})')


def same_face(s, t, cat='Mu'):
    rows = kfaces(cat)
    t = set(t)
    return share([bool(t & (set(x) - {s})) for x, k, st in rows], [bool(t & (set(x) - {s})) for x, k, st in rows if s in x], f'faces with {sorted(t)[:5]} beside it ({cat})')


def herd_reverse(s):
    c = objs[(objs.kind == 'ctab') & ~objs.noanimal]
    return share(c.animal.isin(HERD), c[c.signs.apply(lambda z: s in z)].animal.isin(HERD), 'copper tablets whose reverse animal is a herd beast')


def prev_in(s, t, cat='Mu'): return adjacent(s, set(t), 'prev', cat)


def jar_end(s): return ending_of_names(s, {'jar', 'jar+man'}, None, 'Mu')


def series(s, want, cat='LM', side='both'): return count_series(s, want, cat, side)


# sign: list of (stage, word, English, DEDR, prediction, fresh, callable)
J = {
 '240': [('A', 'mīmīn', 'High-star (house crest)', '4885 mīṉ + mī above', 'a house crest: names with it take the house ending (jar or jar+man) on new-text seals', 'fresh', lambda: jar_end('240')),
         ('B', 'mīmīn', 'High-star', '', 'star names compound: on new texts another fish crest follows it', 'seen', lambda: adjacent('240', FISH - {'240'}, 'next', 'Mu'))],
 '233': [('A', 'vāḷmīn', 'Bright-star (house crest; fish crossed by a blade, vāḷ)', '5377 vāḷ lustre; 5376 vāḷ blade', 'a house crest: names with it take the house ending on new-text seals', 'fresh', lambda: jar_end('233')),
         ('B', 'vāḷmīn', 'Bright-star', '', 'a great house: seals with it are bigger than seals with the same number of signs', 'fresh', lambda: seal_size('233', True, True)),
         ('C', 'vāḷai', 'scabbard-fish, a counted commodity', '5379', 'a goods word: on new texts a measure word follows it', 'seen', lambda: adjacent('233', MEAS, 'next', 'Mu'))],
 '060': [('A', '-iṉ', 'of (oblique/genitive ending)', 'Old Tamil case ending', 'a grammatical ending: it turns up at more sites than signs of its frequency', 'fresh', lambda: multi_site('060', 'LM')),
         ('B', '-iṉ', 'of', '', 'on new texts the sign before it is an opener (month, office, gate, wheel)', 'seen', lambda: prev_in('060', OPEN))],
 '435': [('A', 'taṭi', 'staff, rod (mutal taṭi "chief staff", an office)', '3030', 'an office: seals with it are bigger than seals with the same number of signs', 'fresh', lambda: seal_size('435', True, True)),
         ('B', 'taṭi', 'staff', '', 'an office of the whole civilisation: more sites than signs of its frequency', 'fresh', lambda: multi_site('435', 'LM'))],
 '407': [('A', 'kiḷai', 'herd, lot', '2018', 'a herd word: on copper tablets the reverse animal is a herd beast (bull, buffalo, gaur, goat) more than on copper tablets overall', 'fresh', lambda: herd_reverse('407')),
         ('B', 'kiḷai', 'herd, lot', '', 'a lot word stands last: house-mates at Mohenjo-daro share it (a house tally)', 'fresh', lambda: house_share('407', where='any', seals=False))],
 '900': [('A', 'tiṅkaḷ', 'month', '3213', 'months are counted: on new texts a count stands before it', 'seen', lambda: prev_count('900')),
         ('B', 'tiṅkaḷ', 'month', '', 'months are counted like things, with short strokes (both catalogues)', 'fresh', lambda: series('900', 'short'))],
 '416': [('A', 'turumpu', 'heap of threshed grain (the double fork heaps it)', '3345', 'a threshing-floor word: Harappa objects with it lie in mound F (granary, threshing floors)', 'fresh', lambda: harappa_area('416', 'F')),
         ('B', 'turumpu', 'heap of threshed grain', '', 'a heading word: on new texts it opens the text', 'seen', lambda: text_pos('416', 'first', 'Mu')),
         ('C', 'turumpu', 'heap of threshed grain', '', 'grain goes in containers: counts beside it are tall strokes (both catalogues)', 'fresh', lambda: series('416', 'tall'))],
 '413': [('A', 'nel', 'paddy, grain', '3753', 'grain chits: Harappa objects with it lie in mound E (the tablet mound) more than Harappa objects overall', 'fresh', lambda: harappa_area('413', 'E')),
         ('B', 'nel', 'paddy, grain', '', 'grain is measured: on new texts a measure word follows', 'seen', lambda: adjacent('413', MEAS | {'575'}, 'next', 'Mu'))],
 '388': [('A', 'aracu', 'pipal; royal (house name)', '202 pipal', 'a house name before the jar: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('388', where='any', seals=False)),
         ('B', 'aracu', 'pipal; royal', '', 'a house name: on new texts the jar follows it', 'seen', lambda: adjacent('388', '740', 'next', 'Mu'))],
 '384': [('A', 'aracu', 'pipal; royal (house name)', '202', 'a house name: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('384', where='any', seals=False)),
         ('B', 'aracu', 'pipal; royal', '', 'a house name: on new-text seals names with it take the house ending', 'fresh', lambda: jar_end('384')),
         ('C', 'aracu', 'pipal; royal', '', 'the same word as 388: it stands in the frames of 388 and 382', 'fresh', lambda: frame_swap('384', {'388', '382'}))],
 '382': [('A', 'aracu', 'pipal; royal (house name)', '202', 'the same word as 384/388: it stands in their frames', 'fresh', lambda: frame_swap('382', {'384', '388'})),
         ('B', 'aracu', 'pipal; royal', '', 'a house name: the jar follows it (both catalogues)', 'seen', lambda: adjacent('382', '740', 'next', 'LM'))],
 '226': [('A', 'kūṭumīn', 'crate of fish (fish caged in a kūṭu "receptacle")', '1883 kūṭu', 'fish goods travel by water: faces with it sit at the coast and abroad (both catalogues)', 'fresh', lambda: sites_share('226', COAST)),
         ('B', 'kūṭumīn', 'crate of fish', '', 'crates are counted with tall strokes (the container series)', 'seen', lambda: series('226', 'tall'))],
 '048': [('A', 'er̤uvar', 'the Seven (a body of seven; seven strokes bracketed)', '910', 'the same word as the Seven maidens 585: it stands in the frames of 585', 'fresh', lambda: frame_swap('048', '585')),
         ('B', 'er̤uvar', 'the Seven', '', 'a group name before the jar: the jar follows it more than chance (both catalogues)', 'seen', lambda: adjacent('048', '740', 'next', 'LM'))],
 '097': [('A', 'aṭimai', 'bondsman, servant (a person shut in between posts; aṭai "shut in")', '72; 83', 'a ration receiver: Harappa objects with it lie in mound E (ration chits)', 'fresh', lambda: harappa_area('097', 'E')),
         ('B', 'aṭimai', 'servant', '', 'a ration receiver: on new texts a cup or count stands before it', 'seen', lambda: prev_in('097', set(VAL) | {'700'}))],
 '717': [('A', 'aṭi', 'foot; servant (aṭiyāṉ), the paw', '72', 'a servant word: on new texts a person or title sign stands on the same face', 'fresh', lambda: same_face('717', PERSON)),
         ('B', 'aṭi', 'foot; servant', '', 'a servant\'s seal is small: seals with it are smaller than seals with the same number of signs', 'fresh', lambda: seal_size('717', False, True))],
 '832': [('A', 'kaṇ', 'eye; at, in (place, locative)', '1161 kaṇ place; 1402 eye', 'a grammatical place word: more sites than signs of its frequency', 'fresh', lambda: multi_site('832', 'LM')),
         ('B', 'kaṇ', 'at, in', '', 'on new texts a time or place word stands before it', 'fresh', lambda: prev_in('832', TIMEPLACE | {'832'}))],
 '790': [('A', 'maṇi', 'bead, gem (the plain lens)', 'maṇi (Ta. gem, bead; DEDR 4672 maṇi bell)', 'beads: faces with it sit at the bead towns (Chanhu-daro, Lothal, Dholavira)', 'fresh', lambda: sites_share('790', BEAD)),
         ('B', 'maṇi', 'bead', '', 'beads are goods: on new texts it sits on sealings/tags', 'seen', lambda: on_kind('790', 'tag'))],
 '605': [('A', 'kutir', 'grain bin, granary (tall hatched box)', '1710', 'a granary word: Harappa objects with it lie in mound F (granary)', 'fresh', lambda: harappa_area('605', 'F')),
         ('B', 'kutir', 'grain bin', '', 'a lineage head: on new texts maka "child of" follows it', 'seen', lambda: adjacent('605', '760', 'next', 'Mu'))],
 '137': [('A', 'vēḷāḷaṉ', 'cultivator (person with a leaf)', '5507', 'a ration receiver: Harappa objects with it lie in mound E', 'fresh', lambda: harappa_area('137', 'E')),
         ('B', 'vēḷāḷaṉ', 'cultivator', '', 'a cultivator gets grain: the cup 700 or a grain word on the same face (both catalogues)', 'fresh', lambda: same_face('137', {'700', '413', '806', '575'}, 'LM'))],
 '550': [('A', 'vāy', 'gate, mouth', '5352', 'the gate of a ward: on new texts a ward jar (741/742/745) stands on the same face', 'fresh', lambda: same_face('550', WARD)),
         ('B', 'vāy', 'gate', '', 'a gate word heads an address: on new texts the joiner 060 or the gate-guard 527/555 follows', 'seen', lambda: adjacent('550', {'060', '527', '555', '525'}, 'next', 'Mu'))],
 '923': [('A', 'maruppu', 'horn of the crescent: a phase of the month', '4720', 'a date word after a count: a count stands before it (both catalogues)', 'seen', lambda: prev_in('923', set(VAL), 'LM')),
         ('B', 'maruppu', 'crescent phase', '', 'a date word: it shares a face with the month signs 900/904/920 more than chance (both catalogues)', 'fresh', lambda: same_face('923', {'900', '904', '920'}, 'LM'))],
 '877': [('A', 'nālkāṇi', 'four shares', '1444', 'a holding: Mohenjo-daro house-mates share it', 'fresh', lambda: house_share('877', where='any', seals=False)),
         ('B', 'nālkāṇi', 'four shares', '', 'a counted holding: on new texts a count follows it', 'seen', lambda: next_count('877'))],
 '104': [('A', 'kuṉṟavaṉ', 'hillman', '1864', 'a person word: it stands in the frames of the plain man 090 and the staff-bearer 095', 'fresh', lambda: frame_swap('104', {'090', '095'})),
         ('B', 'kuṉṟavaṉ', 'hillman', '', 'a person word: seals with it carry no jar more than chance (a title in the possessive place)', 'fresh', lambda: no_jar('104', 'L'))],
 '527': [('A', 'kāval', 'guard, watch (vāy kāval "gate-guard")', '1416', 'a title in the possessive place: faces with it carry the jar less than faces overall', 'fresh', lambda: no_jar('527', 'L')),
         ('B', 'kāval', 'guard', '', 'a closing title: on new texts it ends the text', 'seen', lambda: text_pos('527', 'last', 'Mu'))],
 '831': [('A', 'tiṉai', 'Italian millet (leaf with ribbed decoration)', '3265', 'a crop: Harappa objects with it lie in mound E (grain chits)', 'fresh', lambda: harappa_area('831', 'E')),
         ('B', 'tiṉai', 'millet', '', 'a crop sold and grown: sale, price, field or grain words on the same face (both catalogues)', 'seen', lambda: same_face('831', {'892', '824', '615', '413', '806', '845'}, 'LM'))],
}

if __name__ == '__main__':
    rows = []; n = sum(len(v) for v in J.values()); i = 0
    print(f'job 2: {len(J)} signs, {n} predictions, written before this run', flush=True)
    for s, L in J.items():
        for st, w, en, ref, pred, fr, fn in L:
            i += 1; print(f'({i}/{n})', end=' ')
            r = run(st, s, w, pred, fn); r.update(english=en, dedr=ref, fresh=fr); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT4}/job2_tests.csv', index=False)
    print('\nsummary:', df.outcome.value_counts().to_dict())
