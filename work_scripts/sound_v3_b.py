#!/usr/bin/env python3
"""Stage B: one better test of the SAME word for every stage-A value that did not come true (no, direction only,
too few).  Written after reading stage A's outcomes and before running this file.  Writes stage_b.csv."""
from sound_v3_common import *
EYE = {'790', '832', '850'}


def batch_share(s):
    """objects carrying s whose exact text recurs on 2+ objects (issued in copies), against miniature tablets overall."""
    t = objs.faces.apply(lambda fs: '-'.join(fs[0]) if fs else '')
    rep = t.map(t.value_counts()) >= 2
    mt = objs.kind == 'mtab'
    return share(rep[mt], rep[mt & has_obj(s)], 'tablets whose exact text recurs on another object')


B = {
 '061': ('kāl', 'a quarter is counted: on new texts a count stands right before it ("two quarters")', 'fresh', lambda: prev_count('061')),
 '104': ('kuṉṟavaṉ', 'a clan name: Mohenjo-daro house-mates share it (any object, chance within area and 3-ft band)', 'fresh', lambda: house_share('104', where='any', seals=False)),
 '167': ('poli', 'a yield receipt is issued in copies: its tablets repeat their exact text on other objects more than tablets overall', 'fresh', lambda: batch_share('167')),
 '233': ('varimīn', 'a crest closes a name: on new texts the jar or the spear follows it', 'fresh', lambda: adjacent('233', {'740', '520'}, 'next', 'Mu')),
 '240': ('mīmīn', 'a great house: on new texts names with it end in the spear (chief) more than names overall', 'fresh', lambda: ending_of_names('240', 'spear', cat='Mu')),
 '335': ('puṭṭi', 'a measure: on new texts faces with it carry a number', 'fresh', lambda: with_count('335', 'Mu')),
 '440': ('koḷ', 'a receipt word of the Harappa stores: on new texts it sits at Harappa more than chance', 'fresh', lambda: site_share('440', 'Harappa', 'Mu')),
 '460': ('mukkōṭu', 'a name-final house word: on new texts the jar or the spear follows it', 'fresh', lambda: adjacent('460', {'740', '520'}, 'next', 'Mu')),
 '595': ('peṭṭi', 'a chest like 590: on new texts it sits on copper tablets and tools (595 is on 3 copper tools in Lipi)', 'seen', lambda: on_kind('595', ['ctab', 'tool'])),
 '630': ('pal', 'same word as 632 (building as pal): 630 stands in the frames of 632', 'fresh', lambda: frame_swap('630', '632')),
 '645': ('kaṭṭu', 'a counted bundle: on new texts faces with it carry a number', 'fresh', lambda: with_count('645', 'Mu')),
 '711': ('vaḷḷam', 'a grain measure rides with the cup: objects with it carry the cup 700', 'seen', lambda: cooccur('711', '700', 'L', 'object')),
 '717': ('tāḷ', 'a lineage word: Mohenjo-daro house-mates share it (seals, chance within area and 3-ft band)', 'fresh', lambda: house_share('717')),
 '790': ('kaṇ ~ kaṉ', 'a goods word for copper: on new texts it sits off seals', 'fresh', lambda: off_kind('790', 'seal')),
 '832': ('kaṇ ~ kaṉ', 'a goods word for copper: on new texts it sits off seals', 'fresh', lambda: off_kind('832', 'seal')),
 '838': ('eḷumpu', 'bone: rods in both catalogues together (Lipi rods seen)', 'seen', lambda: on_kind('838', 'rod', 'LM')),
 '850': ('kaṇ ~ kaṉ', 'copper: both catalogues together on copper tablets and tools', 'seen', lambda: on_kind('850', ['ctab', 'tool'], 'LM')),
 '877': ('nālkāṇi', 'a holding opener: it opens the text in both catalogues', 'seen', lambda: text_pos('877', 'first', 'LM')),
 '048': ('mūṭai', 'a goods lot like the dozen: 048 stands in the frames of 055', 'fresh', lambda: frame_swap('048', '055')),
 '413': ('nel', 'the commodity heads the record: on new texts it opens the text', 'fresh', lambda: text_pos('413', 'first', 'Mu')),
 '391': ('kollaṉ', 'a smith: both catalogues together on copper tablets and tools (Lipi tools seen)', 'seen', lambda: on_kind('391', ['ctab', 'tool'], 'LM')),
 '590g': ('mañcu', 'a granary record: on new texts 590 sits at Harappa (the granary city) more than chance', 'fresh', lambda: site_share('590', 'Harappa', 'Mu')),
 '417': ('kā', 'a pole-load is counted: a count stands before it (Lipi, seen)', 'seen', lambda: prev_count('417', 'L')),
 '840b': ('vaḷai', 'a bangle word: Lipi bangles (seen in the goods job)', 'seen', lambda: on_kind('840', 'bangle', 'L')),
}
if __name__ == '__main__':
    rows = []
    for i, (s, (w, pred, fr, fn)) in enumerate(B.items(), 1):
        print(f'({i}/{len(B)})', end=' '); r = run('B', s, w, pred, fn); r['fresh'] = fr; rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT3}/stage_b.csv', index=False); print('\nsummary:', df.outcome.value_counts().to_dict())
