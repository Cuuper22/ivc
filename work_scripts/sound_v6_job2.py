#!/usr/bin/env python3
"""Job 2: split the live rivals. For each pair both words get a prediction, all written here before any was computed.
842 and 611 have 5 and 6 uses; their texts were printed while this script was being written (sound_v6 notes), so their
tests are marked 'seen'. Writes work_data/sound_v6/job2_tests.csv."""
from sound_v6_common import *
PERSON = {'090', '520', '095', '617', '679', '142', '140', '125', '097', '400'} | PORTER
PLACE = {'335', '503', '615', '575', '519', '061', '820', '845'}
NUMS = set(VAL)
def frac_with(s, T, cat='LM'):
    rows = faces_all(cat)
    allm = np.array([bool(set(x) & T) for x, P, st, g in rows]); sub = np.array([bool(set(x) & T) for x, P, st, g in rows if s in x])
    return share(allm, sub, f'faces with {s} that carry one of {sorted(T)[:6]}{"..." if len(T) > 6 else ""} ({cat})')
def sites(s, S, cat='LM'):
    rows = faces_all(cat)
    allm = np.array([st in S for x, P, st, g in rows]); sub = np.array([st in S for x, P, st, g in rows if s in x])
    return share(allm, sub, f'faces with {s} at {"/".join(sorted(S))} ({cat})')
def ends_in_jar_after(s, cat='Mu'):
    rows = faces_all(cat); allm = []; sub = []
    for x, P, st, g in rows:
        if '000' in x or len(x) < 3: continue
        e = '740' in x[-2:]
        allm.append(e)
        if s in x[:-1]: sub.append(e)
    return share(allm, sub, f'texts with {s} that end in the house ending (jar in the last two places) ({cat})')
def after_count(s, offs=(1, 2), cat='Mu'):
    return two_away(s, NUMS | {'700', '705', '706', '711', '575'}, offs=offs, cat=cat)
SEC = {'Lothal', 'Chanhu-daro', 'abroad', 'Dholavira', 'Gola Dhoro (Bagasra)', 'Kanmer', 'Desalpur', 'Surkotada', 'Kish', 'Ur', 'Tello', 'Nippur', 'Salut', "Ra's al-Junayz", 'Failaka', 'Susa', 'Bala-kot'}
T = [
 ('692', 'kūṭṭam "assembly" (DEDR 1882)', 'an assembly is people: faces with 692 carry a person or title word (man, chief, staff-bearer, servant, seat, lady, hunter, bondsman, comb, carriers) more than faces overall', lambda: frac_with('692', PERSON)),
 ('692', 'nāṭu "district" (DEDR 3638)', 'a district is land: faces with 692 carry a place or land word (town, hill, field, fort, hedge, quarter, sheaves) more than faces overall', lambda: frac_with('692', PLACE)),
 ('711', 'vaḷḷam "grain measure, 4 marakkāl" (DEDR 5315)', 'a ration measure on a two-faced tablet: the other face holds a who-word (jar, man, a person sign)', lambda: reverse_has('711', {'740', '090'} | PERSON)),
 ('711', 'pāṉai "large pot" (DEDR 4124)', 'pots are counted things: the other face holds a number or the cup', lambda: reverse_has('711', NUMCUP)),
 ('060', '-iṉ "of" (genitive)', 'a chain of possessives: new texts with 060 end in the house ending more than new texts overall', lambda: ends_in_jar_after('060')),
 ('060', 'uḷ "in" (DEDR 698)', 'place or time, then an amount: on new texts a number or measure stands one or two places after 060 more than after signs in general', lambda: after_count('060')),
 ('838', 'viḷai "produce" (DEDR 5437)', 'produce is carried and counted: the sign right after 838 is a carrier or a number more than after signs in general (both catalogues)', lambda: adjacent('838', PORTER | {'161'} | NUMS, 'next', 'LM')),
 ('838', 'eḷ "sesame" (DEDR 839; Akkadian ellu)', 'sesame is a coast and export good: faces with 838 lie at Lothal, Chanhu-daro, the Gujarat sites or abroad more than faces overall', lambda: sites('838', SEC)),
 ('407', 'kiḷai "kindred, family; branch" (DEDR 2018)', 'kindred is a household word: Mohenjo-daro house-mates (same room, 3-ft band shuffle) both carry 407', lambda: house_share('407', where='any', seals=False)),
 ('407', 'tuṇi "cloth" (DEDR 3307)', 'cloth is a trade good: faces with 407 lie at Lothal, Chanhu-daro, the Gujarat sites or abroad more than faces overall', lambda: sites('407', SEC)),
 ('842', 'tuṇai "companion, deputy" (DEDR 3308) [seen]', 'a deputy closes the text after an office opening: 842 is the last sign more than signs in general', lambda: text_pos('842', 'last', 'LM')),
 ('842', 'tuṇai [seen]', 'a deputy belongs to an office: faces with 842 carry the month or assembly opener (920, 692) more than faces overall', lambda: frac_with('842', {'920', '692'})),
 ('611', 'kuṭai "umbrella", a ruling house (DEDR 1663) [seen]', 'the quarter of the Umbrella: the wheel kāl 820 stands right before 611 more than before signs in general', lambda: adjacent('611', {'820'}, 'prev', 'LM')),
 ('611', 'kuṭai [seen]', 'a ruling house name takes the house ending or a royal word: jar 740, aracu 382/384/388 or the gate 550 within two places after it', lambda: two_away('611', {'740', '382', '384', '388', '550'}, offs=(1, 2), cat='LM')),
]
if __name__ == "__main__":
  for s, w, p, f in T: print(f'[{s}] {w}: {p}', flush=True)
  print("---- computing ----", flush=True)
  out = [run("J2", s, w, p, f) for s, w, p, f in T]
  pd.DataFrame(out).to_csv(f"{OUT6}/job2_tests.csv", index=False)
