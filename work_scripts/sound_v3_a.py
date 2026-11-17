#!/usr/bin/env python3
"""Stage A of the third sound pass: one bold prediction for each of the 37 values under test, and for 16 brand-new
values (8 signs that had no word, 8 signs the object-kind tables made ripe).  Every word and prediction below was
written into this file before the script was first run.  'fresh' = the tested fact was not looked at while choosing
(new second-catalogue texts, or a Lipi findspot / size / animal fact); 'seen' = a Lipi fact visible in the sign
profiles printed while choosing.  Writes work_data/sound_v3/stage_a.csv.  Run: python3 sound_v3_a.py"""
from sound_v3_common import *

EYE = {'790', '832', '850'}
COPPER = ['ctab', 'tool']
# sign: (word, English, DEDR / source, prediction, freshness, callable)
A = {
 # ---- the 37 under test ----
 '055': ('paṉṉiru', 'dozen', 'twelve strokes; Ta. paṉṉiraṇṭu', 'a goods lot size: on new texts it sits on sealings/tags more than chance', 'fresh', lambda: on_kind('055', 'tag')),
 '061': ('kāl', 'quarter (of land)', '1479 block (kāl leg, quarter)', 'a land fraction: on new texts it sits on copper tablets (the land-deed objects) more than chance', 'fresh', lambda: on_kind('061', 'ctab')),
 '104': ('kuṉṟavaṉ', 'hillman (clan)', 'kuṉṟu hill, kuṉṟuvar mountaineers (1864); person + the caret 480', 'person + caret is the caret word made a person: 104 stands in the frames of the caret 480', 'fresh', lambda: frame_swap('104', '480')),
 '140': ('ammai', 'lady', 'mem; Ta. ammai mother', 'a title heading a name: on new texts it opens the text more than chance', 'fresh', lambda: text_pos('140', 'first', 'Mu')),
 '165': ('poḻutu', 'sun, day', '4559', 'sun pairs with moon: on one face with the crescent 900 more than chance (both catalogues)', 'seen', lambda: cooccur('165', '900', 'LM')),
 '167': ('poli', 'heap of threshed grain, yield in kind', '4550 (poli increase; interest paid in kind)', 'kaḷam poli "threshing-floor yield": at Harappa its tablets lie in mound F (threshing floors, granary) more than tablets overall', 'fresh', lambda: harappa_area('167', 'F')),
 '171': ('niṟai', 'weight, full measure', '3682', 'a measure word takes its number after it: on new texts the next sign is a count', 'fresh', lambda: next_count('171')),
 '175': ('iṟai', 'tax', '521', 'a levy word lives on tablets: on new texts it sits on miniature tablets more than chance', 'fresh', lambda: on_kind('175', 'mtab')),
 '233': ('varimīn', 'Striped-star', 'vari stripe + mīṉ (4885)', 'a great-house crest: on new texts the spear (chief) follows it more than chance', 'fresh', lambda: adjacent('233', '520', 'next', 'Mu')),
 '240': ('mīmīn', 'High-star', 'mī above + mīṉ', 'the High-star house is a Harappa house: on new texts it sits at Harappa more than chance', 'fresh', lambda: site_share('240', 'Harappa', 'Mu')),
 '320': ('paṭi', 'ration measure, daily allowance (pun: rung of a ladder)', '3850 rung of a ladder; 3849 measure of capacity, fixed daily allowance', 'paṭi tiṅkaḷ "monthly allowance": on new texts the month sign 920 follows it more than chance', 'fresh', lambda: adjacent('320', '920', 'next', 'Mu')),
 '335': ('puṭṭi', 'large grain measure', '4262 measure of capacity; the box picture (peṭṭi) is the pun', 'a grain measure lives on tablets: on new texts it sits on miniature tablets more than chance', 'fresh', lambda: on_kind('335', 'mtab')),
 '407': ('kiḷai', 'herd, lot', '2018', 'a herd word goes with an animal: copper tablets with it carry an animal on the reverse more than copper tablets overall', 'seen', lambda: share(objs[objs.kind == 'ctab'].symbol.isin(['Anth', 'Buff', 'Bull', 'Bull1:W', 'Elep', 'Gaur', 'Goat:8', 'Hare', 'Rhin', 'Tigr']), objs[(objs.kind == 'ctab') & has_obj('407')].symbol.isin(['Anth', 'Buff', 'Bull', 'Bull1:W', 'Elep', 'Gaur', 'Goat:8', 'Hare', 'Rhin', 'Tigr']), 'copper tablets with an animal on the reverse')),
 '440': ('koḷ', 'received, bought', '2151', 'a receipt word on vessels: on new texts it sits on pots more than chance', 'fresh', lambda: on_kind('440', 'pot')),
 '460': ('mukkōṭu', 'Three-peaks (house)', '2049', 'a house name: on new texts the jar follows it more than chance', 'fresh', lambda: adjacent('460', '740', 'next', 'Mu')),
 '503': ('malai', 'hill', 'mem; Ta. malai', 'a land word: on new texts it sits on copper tablets (deeds) more than chance', 'fresh', lambda: on_kind('503', 'ctab')),
 '540': ('paṟai', 'drum; a rice measure', '4032 (drum, a measure of capacity)', 'the drum is a grain measure: on new texts it sits on pots more than chance', 'fresh', lambda: on_kind('540', 'pot')),
 '575': ('kōṭṭai', 'great grain measure (21 marakkāl)', '2208', 'a measure counted: on new texts a count stands right before it more than chance', 'fresh', lambda: prev_count('575')),
 '595': ('peṭṭi', 'chest', '4388', 'a container: on new texts the counts beside it are tall strokes (the container series)', 'fresh', lambda: count_series('595', 'tall', 'Mu')),
 '615': ('vayal', 'field', 'mem; Ta. vayal', 'a land word: on new texts it sits on copper tablets more than chance', 'fresh', lambda: on_kind('615', 'ctab')),
 '617': ('ūḻiyaṉ', "(king's) servant", '758', 'a title that closes in place of the possessive: faces with it carry the jar less than faces overall', 'fresh', lambda: no_jar('617', 'L')),
 '630': ('pal', 'many', 'mem; Ta. pal', 'a quantity word: objects with it carry a number sign more than objects overall', 'fresh', lambda: cooccur('630', set(VAL), 'L', 'object')),
 '636': ('pal', 'many', 'as 630', '636 is 630 written another way: it stands in the frames of 630', 'fresh', lambda: frame_swap('636', '630')),
 '645': ('kaṭṭu', 'bundle, packet', '1147', 'a counted bundle: on new texts a count stands right before it', 'fresh', lambda: prev_count('645')),
 '690': ('piṇai', 'bound, allied', 'mem; Ta. piṇai', 'a kin word closing a name: on new texts the jar follows it', 'fresh', lambda: adjacent('690', '740', 'next', 'Mu')),
 '711': ('vaḷḷam', 'grain measure (4 marakkāl), dish', '5315', 'a ration measure: its Harappa tablets lie in E trench 11 (the ration-chit trench) more than Harappa objects overall', 'fresh', lambda: harappa_area('711', 'ETrench 11')),
 '717': ('tāḷ', 'stem (of a line)', '3185', 'a lineage word closing a name: on new texts the jar follows it', 'fresh', lambda: adjacent('717', '740', 'next', 'Mu')),
 '760': ('maka', 'child of', 'mem; Ta. makaṉ', 'the kin word before the possessive: on new texts the jar follows it more than chance', 'fresh', lambda: adjacent('760', '740', 'next', 'Mu')),
 '790': ('kaṇ ~ kaṉ', 'eye ~ copper', '1402', 'copper pun: on new texts it sits on copper tablets and bronze tools more than chance', 'fresh', lambda: on_kind('790', COPPER)),
 '803': ('il', 'house', 'mem; Ta. il', '"house of" + crest: on new texts a fish crest follows it more than chance', 'fresh', lambda: adjacent('803', FISH, 'next', 'Mu')),
 '824': ('vilai', 'price', '5421 (noun of vil "sell")', 'the price of grain sold: its Harappa objects lie in mound E (the ration and tablet mound) more than Harappa objects overall', 'fresh', lambda: harappa_area('824', 'E')),
 '832': ('kaṇ ~ kaṉ', 'eye ~ copper', '1402', 'copper pun: on new texts it sits on copper tablets and bronze tools more than chance', 'fresh', lambda: on_kind('832', COPPER)),
 '838': ('eḷumpu ~ eḷ', 'bone ~ sesame', '839, 854', 'bone: on new texts it sits on ivory/bone rods more than chance', 'fresh', lambda: on_kind('838', 'rod')),
 '840': ('iṇai', 'pair', '457', 'a pair is counted: on new texts two tall strokes (032) follow it more than chance', 'fresh', lambda: adjacent('840', '032', 'next', 'Mu')),
 '845': ('cūṭu', 'bundle of sheaves', '2723', 'a field-produce lot: on new texts it sits on copper tablets more than chance', 'fresh', lambda: on_kind('845', 'ctab')),
 '850': ('kaṇ ~ kaṉ', 'eye ~ copper', '1402', 'copper pun: faces with it (new texts; the second catalogue merges 850 with 790) on copper tablets and tools', 'fresh', lambda: on_kind('850', COPPER)),
 '877': ('nālkāṇi', 'four shares', '1444', 'a big holding: seals with it are bigger than seals with the same number of signs', 'fresh', lambda: seal_size('877', True, True)),
 # ---- brand-new values from the object-kind tables ----
 '500': ('pāy', 'sail (ship)', '4088 (spreading, mat, sail); the tall triangle on a divider is a sail on a mast', 'a ship word: on new texts it sits at Lothal, the port, more than chance', 'fresh', lambda: site_share('500', 'Lothal', 'Mu')),
 '890': ('koṭu', 'given (pun: koṭu bent, the bow without arrow)', '2053 give; 2054 bent', 'a transfer word on goods: on new texts it sits on sealings/tags more than chance', 'fresh', lambda: on_kind('890', 'tag')),
 '048': ('mūṭai', 'sack-load, packed bundle', '5037', 'a packed lot is not an owner word: objects with it carry no animal more than objects overall', 'fresh', lambda: share(objs.noanimal, objs[has_obj('048')].noanimal, 'objects with no animal')),
 '413': ('nel', 'paddy, grain', '3753 (the picture is an ear of grain)', 'grain is measured in cups: on new texts it shares a face with the cup 700', 'fresh', lambda: cooccur('413', '700', 'Mu')),
 '806': ('viḷai', 'produce, ripened crop', '5437', 'crop carried in: on new texts a load-carrier follows it more than chance', 'fresh', lambda: adjacent('806', PORTER, 'next', 'Mu')),
 '391': ('kollaṉ', 'smith', '2133', 'a smith works copper: on new texts it sits on copper tablets and bronze tools', 'fresh', lambda: on_kind('391', COPPER)),
 '590g': ('mañcu', 'granary, storehouse (second reading beside peṭṭi)', '4640 (mañcikai chest, grain bin; mañcu granary)', 'a store record: on new texts 590 sits on miniature tablets more than chance', 'fresh', lambda: on_kind('590', 'mtab')),
 '417': ('kā', 'carrying pole with loads at both ends', '1417 (kā, kāvaṭi)', 'the same word as the load-carriers: 417 stands in the frames of 151-158', 'fresh', lambda: frame_swap('417', PORTER)),
 '840b': ('vaḷai', 'bangle, ring (second reading beside iṇai)', '5313', 'a bangle word: on new texts it sits off seals (bangles are absent from the second catalogue, so: not on seals)', 'fresh', lambda: off_kind('840', 'seal')),
 '055b': ('paṉṉiru', 'dozen (of fish)', 'as 055', 'a dozen of fish: on new texts the fish 220 follows it more than chance', 'fresh', lambda: adjacent('055', '220', 'next', 'Mu')),
 '480b': ('kuṉṟi', 'seed-weight', '1865', 'a small weight for goods: on new texts it sits on pots more than chance', 'fresh', lambda: on_kind('480', 'pot')),
 '892b': ('vil', 'sale', '5421', 'a sale word on goods: on new texts it sits on sealings/tags more than chance', 'fresh', lambda: on_kind('892', 'tag')),
}

if __name__ == '__main__':
    rows = []
    print(f'stage A: {len(A)} predictions, written before this run', flush=True)
    for i, (s, (w, en, ref, pred, fr, fn)) in enumerate(A.items(), 1):
        print(f'({i}/{len(A)})', end=' ')
        r = run('A', s, w, pred, fn); r.update(english=en, dedr=ref, fresh=fr); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT3}/stage_a.csv', index=False)
    print('\nsummary:', df.outcome.value_counts().to_dict())
