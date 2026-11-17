#!/usr/bin/env python3
"""Seeded draw of 40 'whole' faces from work_data/corpus_english.csv for a hand read (sense / odd / nonsense).
Seed 20261117, drawn from faces (copies count as often as they occur). Writes work_data/corpus_draw40.csv."""
import random, pandas as pd
ROOT = '/home/claude/ivc'
c = pd.read_csv(f'{ROOT}/work_data/corpus_english.csv', dtype=str).fillna('')
w = c[c.grade == 'whole'].reset_index(drop=True)
idx = random.Random(20261117).sample(range(len(w)), 40)
s = w.loc[idx].copy(); s.to_csv(f'{ROOT}/work_data/corpus_draw40.csv', index=False)
for n, r in enumerate(s.itertuples(), 1): print(n, r.face_id, r.site, '/', r.object_kind, '|', r.signs, '|', r.sounds, '|', r.english)
