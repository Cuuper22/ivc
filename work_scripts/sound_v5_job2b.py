#!/usr/bin/env python3
"""Job 2 rescue: every sign whose A and B both missed in sound_v5_job2.py gets ONE new word (C), its prediction
written here before running.  All tests here are on fact kinds not printed for the sign while choosing.
Writes work_data/sound_v5/job2b_tests.csv."""
from sound_v5_job2 import *
R = {
 '407': [('C', 'kiḷai', 'kindred, clan branch (the tree as a family tree, not cloth)', '2018', 'a kindred name: names with the tree family take the house ending (jar, jar+man) on new-text seals', 'fresh', lambda: ending_of_names('405', {'jar', 'jar+man'}, None, 'Mu'))],
 '165': [('C', 'kātu', 'ear; ear-ring (the picture as an ear)', '1448', 'an ornament word: Harappa objects with 165 lie in mound E (the craft mound)', 'fresh', lambda: harappa_area('165', 'E'))],
 '645': [('C', 'pāti', 'half, a divided share (the X divides)', 'Ta. pāti half', 'a fraction word: 645 stands in the frames of the share and quarter words 861/817/820', 'fresh', lambda: frame_swap('645', {'861', '817', '820'}))],
 '167': [('C', 'kā', 'pole-load (a yoke with a load hanging from each end, without the man)', 'base kā', 'one word with the load-carriers: 167 stands in the frames of the carriers and the pole 417', 'fresh', lambda: frame_swap('167', PORTER | {'417'}))],
 '236': [('C', 'vēymīn', 'Bamboo-star (a crest variant of 235, caged)', '5541 vēy + 4885 mīṉ', 'a crest: 236 stands in the frames of the Bamboo-star 235', 'fresh', lambda: frame_swap('236', {'235'}))],
 '048': [('C', 'kōvai', 'a string of seven (beads)', 'Ta. kōvai string, garland', 'a bead word: 048 stands in the frames of the bead/gem words 790/792', 'fresh', lambda: frame_swap('048', {'790', '792'}))],
 '832': [('C', 'maṇi', 'gem with an eye, a pierced bead (variant of 790)', '4672', 'one word with the gem 790: 832 stands in the frames of 790', 'fresh', lambda: frame_swap('832', {'790'}))],
 '868': [('C', 'araikkāṇi', 'half-share (a fraction ending)', '1444 + arai half', 'a fraction ends the text in place of the possessive: faces with 868 carry the jar less than faces overall', 'fresh', lambda: no_jar('868', 'L'))],
 '222': [('C', 'aṭaimīn', 'shut-in fish: a marked-fish crest', '4885 + 72 aṭai', 'a crest: 222 stands in the frames of the four fish crests 231/233/235/240', 'fresh', lambda: frame_swap('222', {'231', '233', '235', '240'}))],
 '460': [('C', 'mukkōṭṭai', 'three forts (a town name)', '575 kōṭṭai', 'a town word: 460 stands in the frames of fort 575 and town 335', 'fresh', lambda: frame_swap('460', {'575', '335'}))],
 '519': [('C', 'vēli', 'fence, hedged plot (a name element)', 'Ta. vēli', 'a name element: the jar stands one or two places after 519', 'fresh', lambda: two_away('519', {'740'}, (1, 2)))],
 '347': [('C', 'kalai', 'stag', '1312', 'a tablet word: Harappa objects with 347 lie in mound E (the tablet mound)', 'fresh', lambda: harappa_area('347', 'E'))],
 '821': [('C', 'veṟṟilai', 'betel leaf (leaf with a crossed vein), a counted good', 'Ta. veṟṟilai', 'a counted good: a number stands one or two places from 821', 'fresh', lambda: two_away('821', set(VAL), (-2, -1, 1, 2)))],
 '792': [('C', 'aracu', 'pipal leaf; royal (leaf family)', '202', 'one word with the pipal leaves: 792 stands in the frames of 382/384/388', 'fresh', lambda: frame_swap('792', {'382', '384', '388'}))],
}
if __name__ == '__main__':
    rows = []
    for s, L in R.items():
        for st, w, en, ref, pred, fr, fn in L:
            r = run(st, s, w, pred, fn); r.update(english=en, dedr=ref, fresh=fr); rows.append(r)
    df = pd.DataFrame(rows); df.to_csv(f'{OUT5}/job2b_tests.csv', index=False)
    print('summary:', df.outcome.value_counts().to_dict())
