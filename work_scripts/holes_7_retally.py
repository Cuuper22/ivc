#!/usr/bin/env python3
"""Re-read the long-text phrases with the new values.  Reads work_data/long_texts/read.json (186 phrases, hand-split), changes the sound table in memory:
 060 uḷ 'in'; 335 kūṭu 'bin'; 711 pāṉai 'pot'; 525/526/527 katavu 'door'; 692 nāṭu 'district'; 842 tuṇai 'deputy'; 611 kuṭai 'umbrella (name)'; 645 kuṟi 'mark';
 705/706 paṭi 'ration measure'; 435 taṭi 'rod'.
Marks as in long_texts_read.py: reads = every sign valued and no avoided class pair; partial = an unvalued or lost sign; unread = one unvalued sign alone;
nonsense = an avoided class pair.  Output: work_data/holes/retally_phrases.csv and the counts."""
import sys, json, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import long_common as LC
HOLES = '/home/antigravity/Cuuper22/ivc/work_data/holes'
from long_common import *
from sound_v2_tiers import CLASS
NEW = {'060': ('uḷ', 'in'), '335': ('kūṭu', 'bin'), '711': ('pāṉai', 'pot'), '525': ('katavu', 'door'), '526': ('katavu', 'door'), '527': ('katavu', 'door'),
       '692': ('nāṭu', 'district'), '842': ('tuṇai', 'deputy'), '611': ('kuṭai', 'Umbrella'), '645': ('kuṟi', 'mark'),
       '705': ('paṭi', 'measure'), '706': ('paṭi', 'measure'), '435': ('taṭi', 'rod')}
NEWCLASS = {'060': 'LINK', '335': 'GOODS', '711': 'GOODS', '525': 'TITLE', '526': 'TITLE', '527': 'TRANS', '692': 'OPEN', '842': 'END', '611': 'SELF', '645': 'GOODS',
            '705': 'GOODS', '706': 'GOODS', '435': 'TITLE'}
OLDV = dict(LC.V2)
for s, v in NEW.items(): LC.V2[s] = v
for s, c in NEWCLASS.items(): CLASS[s] = c
bg = pd.read_csv(f'{OUTDIR}/class_bigrams.csv')
DEPLETED = {(r['first'], r['second']) for _, r in bg.iterrows() if r.ratio < 0.4 and r.expected >= 10}
def cls(s):
    if s in CNT: return 'NUM'
    return CLASS.get(s, '?') if LC.snd(s) else None
T = json.load(open(f'{OUTDIR}/read.json'))
rows = []
tall = {f'{k:03d}' for k in range(31, 37)}
for t in T:
    for P_ in t['read']:
        p = P_['signs']
        unv = [s for s in p if s != '000' and s not in CNT and s != '806' and not LC.snd(s)]
        lost = sum(1 for s in p if s == '000')
        cs = [cls(s) for s in p]
        breaks = []
        for i in range(len(p) - 1):
            a, b = cs[i], cs[i + 1]
            if a and b and (a, b) in DEPLETED:
                if b == 'POSS' and a == 'NUM' and p[i] in tall: continue
                breaks.append((p[i], p[i + 1], f'{a}>{b}'))
        potjar = any(p[i] in tall and p[i + 1] == '740' for i in range(len(p) - 1))
        mark = 'nonsense' if breaks else ('partial' if (unv or lost) else 'reads')
        if len(p) == 1 and unv: mark = 'unread'
        reason = ', '.join(b[2] for b in breaks)
        snd_s = ' '.join(('(n)' if (s in CNT and CNT[s][0] == 'comb') else '(crop)' if s == '806' else LC.snd(s) or '‹?›') for s in p)
        rows.append(dict(text=t['cisi'], face=P_['face'], line=P_['line'], signs='-'.join(p), kind=P_['kind'], old_mark=P_['mark'], old_reason=P_['reason'],
                         new_mark=mark, new_reason=reason, still_unvalued='-'.join(unv), lost=lost, potjar=potjar, old_english=P_['english'], new_sound=snd_s))
d = pd.DataFrame(rows); d.to_csv(f'{HOLES}/retally_phrases.csv', index=False)
print('old', d.old_mark.value_counts().to_dict(), ' new (mechanical)', d.new_mark.value_counts().to_dict())
print(pd.crosstab(d.old_mark, d.new_mark))
