#!/usr/bin/env python3
"""New seeded draw of 60 'whole' faces from work_data/corpus_english2.csv for a read by eye (sense / odd / nonsense).
Seed 20261119 (earlier draws: 20261117, and 20261118 on the rules before the 390 fix and the fifth-pass values). Rules were frozen (corpus_build2.py, values_master2.csv) before this was run.
Faces are drawn as they occur (copies count as often as they occur). Writes work_data/odd/corpus_draw60b.csv."""
import random, pandas as pd
ROOT = '/home/claude/ivc'
SEED = 20261119
c = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
w = c[c.grade == 'whole'].reset_index(drop=True)
idx = random.Random(SEED).sample(range(len(w)), 60)
s = w.loc[idx].copy(); s['old_english'] = s.face_id.map(dict(zip(*[pd.read_csv(f'{ROOT}/work_data/corpus_english.csv', dtype=str).fillna('')[k] for k in ('face_id', 'english')])))
s.to_csv(f'{ROOT}/work_data/odd/corpus_draw60b.csv', index=False)
for n, r in enumerate(s.itertuples(), 1): print(n, r.face_id, r.site, '/', r.object_kind, '|', r.signs, '|', r.sounds, '|', r.english)
