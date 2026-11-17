#!/usr/bin/env python3
"""Job 3, round two: one redesign (new word or new test) for each of the 14 signs whose A and B both missed,
all written before running. Appends stage C to work_data/sound_v6/job3_tests.csv."""
from sound_v6_common import *
from sound_v6_job2 import frac_with, sites
WC = {
 '592': ('paṭṭi', 'fold, pen, hamlet (box with a post inside a fence)', '4388'),
 '703': ('nāḻi', 'cup measure (variant of the cup 700, filled)', ''),
 '554': ('paṟai', 'a grain measure (bowtie variant)', '4032'),
 '064': ('kavar', 'fork, branch (the bare Y fork)', '1325'),
 '136': ('aṭimai', 'bondsman, servant (a counted person)', ''),
 '603': ('katavu', 'door (tall frame with bars)', '1187'),
 '098': ('ammai', 'lady (person with raised arm, variant of 140)', ''),
 '408': ('kiḷai', 'herd, flock, lot (counted tree)', '2018'),
 '621': ('kōṭṭai', 'store, fort (barred box, variant of 575)', ''),
 '243': ('vāḷai', 'scabbard-fish (hatched fish, variant of 233)', ''),
 '130': ('aṭiyāṉ', 'servant (person with a tool, counted)', ''),
 '697': ('kaṭṭu', 'bundle, tie (sticks tied across a diamond)', '1147'),
 '776': ('pū', 'flower (three-stemmed plant)', '4345'),
 '804': ('kūṭu', 'crate (produce in the four-stroke cage, as 226 is fish in it)', '1883'),
}
TESTS = [
 ('592', 'a place word: 592 stands in the frames of town 335, fort 575 or hill 503', lambda: frame_swap('592', {'335', '575', '503'})),
 ('703', 'one word with the cup: 703 stands in the frames of 700', lambda: frame_swap('703', '700')),
 ('554', 'a measure lives on records: faces with 554 sit on copper/moulded tablets more than all faces', lambda: on_kind('554', {'ctab', 'mtab'}, 'LM')),
 ('064', 'one word with the fork 415: 064 stands in its frames', lambda: frame_swap('064', '415')),
 ('136', 'one word with the bondsman/servant: 136 stands in the frames of 097/717', lambda: frame_swap('136', {'097', '717'})),
 ('603', 'a door word: 603 stands in the frames of the gate 550/555 or guard 525-527', lambda: frame_swap('603', {'550', '555', '525', '526', '527'})),
 ('098', 'one word with the lady: 098 stands in the frames of 140', lambda: frame_swap('098', '140')),
 ('408', 'a lot is counted like things: the counts beside 408 are short strokes', lambda: count_series('408', 'short', 'LM')),
 ('621', 'one word with the store/fort: 621 stands in the frames of 575', lambda: frame_swap('621', '575')),
 ('243', 'one word with the scabbard-fish: 243 stands in the frames of 233', lambda: frame_swap('243', '233')),
 ('130', 'one word with the servant: 130 stands in the frames of 717/097', lambda: frame_swap('130', {'717', '097'})),
 ('697', 'bundles are tied on goods: faces with 697 sit on tags/sealings more than all faces', lambda: on_kind('697', 'tag', 'LM')),
 ('776', 'the flowering plants stand for pictures on Mohenjo-daro copper tablets: faces with 776 are at Mohenjo-daro more than faces overall', lambda: sites('776', {'Mohenjo-daro'})),
 ('804', 'one word with the crate of fish: 804 stands in the frames of 226', lambda: frame_swap('804', '226')),
]
if __name__ == '__main__':
    for s, p, f in TESTS: print(f'[C] {s} {WC[s][0]}: {p}', flush=True)
    print('---- computing ----', flush=True)
    out = [run('C', s, WC[s][0], p, f) for s, p, f in TESTS]
    old = pd.read_csv(f'{OUT6}/job3_tests.csv'); old = old[old.stage != 'C']
    pd.concat([old, pd.DataFrame(out)]).to_csv(f'{OUT6}/job3_tests.csv', index=False)
