#!/usr/bin/env python3
"""Writes the tables of jobs/out/sound_list_v3.md (the prose sections are kept in sound_v3_report_head.md and
sound_v3_report_tail.md beside this script).  Run after sound_v3_a/b/c.py and sound_v3_values.py."""
import csv, os
import pandas as pd
from sound_values import VALUES
from sound_v3_values import V3, TIER3, OLDTIER, NOTE
ROOT = '/home/claude/ivc'; O = f'{ROOT}/work_data/sound_v3'
PIC = {v[0]: v[1] for v in VALUES}
PIC.update({'890': 'bow without arrow (right-facing bow)', '048': 'seven short strokes in brackets', '391': 'three-pronged tree with a caret hat',
            '417': 'two pitchforks facing each other', '806': 'leaf on a tree', '500': 'tall triangle with a divider (horn or sail shape)'})
ev2 = {}
for r in csv.DictReader(open(f'{ROOT}/work_data/sound_v2/values_v2.csv')): ev2[r['sign']] = r
v2txt = open(f'{ROOT}/jobs/out/sound_list_v2.md').read()


def v2_evidence(s):
    for line in v2txt.splitlines():
        if line.startswith(f'| {s} |'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            return cells[-1][:260] + ('...' if len(cells[-1]) > 260 else '')
    return ''


def table(tier):
    out = ['| sign | picture | sound | English | before | evidence |', '|---|---|---|---|---|---|']
    for s in sorted(V3):
        if TIER3[s] != tier: continue
        ev = NOTE.get(s) or ('second list: ' + v2_evidence(s))
        out.append(f'| {s} | {PIC.get(s, "")} | *{V3[s][0]}* | {V3[s][1]} | {OLDTIER.get(s, "new")} | {ev} |')
    return out


def stage_rows():
    out = ['| stage | sign | word | prediction | outcome | number | P | fact unseen while choosing? |', '|---|---|---|---|---|---|---|---|']
    for st in 'abcd':
        df = pd.read_csv(f'{O}/stage_{st}.csv', dtype={'sign': str})
        for r in df.itertuples():
            p = '' if pd.isna(r.p) else f'{r.p:.2g}'
            out.append(f'| {st.upper()} | {r.sign} | *{r.word}* | {r.prediction} | {r.outcome} | {r.result} | {p} | {r.fresh} |')
    return out


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    head = open(f'{here}/sound_v3_report_head.md').read(); tail = open(f'{here}/sound_v3_report_tail.md').read()
    nb = {s: t for s, t in TIER3.items() if t != 'base'}
    from collections import Counter
    c = Counter(nb.values())
    L = [head.rstrip(), '',
         f'## 2. The whole list, sorted ({len(nb)} values: {c["building"]} building on, {c["testing"]} testing, {c["paused"]} paused)', '',
         '"before" = the value\'s status in the second list ("new" = the sign had no value). Evidence: the third-pass checks for values touched in this pass (A = bold prediction, B = better test of the same word, C = new word, D = the ship lead); the second-list evidence, shortened, for the rest. Base values (numbers, jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) are not listed.', '',
         f'### Building on ({c["building"]})', ''] + table('building') + ['', f'### Testing ({c["testing"]})', ''] + table('testing') + \
        ['', f'### Paused ({c["paused"]})', ''] + table('paused') + ['', tail.rstrip(), '', '## 5. Every check of this pass', '',
         'Each prediction was written into its script before the script ran. "yes" = right direction with P at or under 0.1; "direction only" = right direction, P above 0.1; "no" = wrong direction; "n/a" = too few cases.', ''] + stage_rows()
    open(f'{ROOT}/jobs/out/sound_list_v3.md', 'w').write('\n'.join(L) + '\n')
    print('written jobs/out/sound_list_v3.md')
