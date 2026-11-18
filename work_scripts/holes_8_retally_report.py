#!/usr/bin/env python3
"""Tally and per-sign effect of the new values on the 186 long-text phrases.  Reads retally_phrases.csv (holes_7_retally.py) and read.json."""
import json, collections, pandas as pd
HOLES = '/home/antigravity/Cuuper22/ivc/work_data/holes'
d = pd.read_csv(f'{HOLES}/retally_phrases.csv', keep_default_na=False)
T = json.load(open('/home/antigravity/Cuuper22/ivc/work_data/long_texts/read.json'))
old_unv = []
for t in T:
    for p in t['read']: old_unv.append(p['unvalued'])
d['old_unvalued'] = ['-'.join(u) for u in old_unv]
# judgment overrides (see report): the three signboard phrases read as head-noun "quarter" phrases, not seal openers
board = d.text == '-'
d['final_strict'] = d.new_mark
d.loc[board, 'final_strict'] = 'reads'
special = d.old_reason.str.contains('counted pot|tax tax') | d.old_reason.str.contains('jar read as') | d.old_reason.str.contains('two drawings')
d['final_strict'] = d.apply(lambda r: 'nonsense' if (special[r.name] and r.final_strict == 'reads') else r.final_strict, axis=1)
d['final_with_section5'] = d.final_strict
d.loc[special & (d.new_mark == 'reads'), 'final_with_section5'] = 'reads'
d.to_csv(f'{HOLES}/retally_phrases_final.csv', index=False)
print('OLD   ', d.old_mark.value_counts().to_dict())
print('STRICT', d.final_strict.value_counts().to_dict(), '(eight + paṭi + taṭi only)')
print('SEC5  ', d.final_with_section5.value_counts().to_dict(), '(also counted-pot jar and iṟai-iṟai rereads)')
print(pd.crosstab(d.old_mark, d.final_strict)); print(pd.crosstab(d.old_mark, d.final_with_section5))
eight = ['060', '335', '711', '525', '526', '527', '692', '842', '611', '645', '821', '705', '706', '435']
rows = []
for s in eight:
    has = d[d.signs.str.split('-').apply(lambda x: s in x)]
    fixed = has[(has.old_mark.isin(['partial', 'nonsense'])) & (has.final_strict == 'reads')]
    rows.append(dict(sign=s, phrases_with_it=len(has), old_partial_or_nonsense=int(has.old_mark.isin(['partial', 'nonsense']).sum()), now_reads=len(fixed)))
print(pd.DataFrame(rows).to_string())
pd.DataFrame(rows).to_csv(f'{HOLES}/retally_by_sign.csv', index=False)
# what is still unvalued in the 58 partial
rest = d[d.final_strict == 'partial']
c = collections.Counter(s for u in rest.still_unvalued for s in str(u).split('-') if s)
print('still partial', len(rest), 'phrases; unvalued signs', c.most_common(12), 'lost-only', int(((rest.still_unvalued == '') ).sum()))
print(d[d.final_strict == 'nonsense'][['text', 'signs', 'new_reason', 'old_reason']].to_string())
