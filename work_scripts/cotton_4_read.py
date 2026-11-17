"""PART 3b. Read whole: every face from the Mohenjo-daro dyers' quarter (area VS*) and from Karanpura.
Sounds: the v2 working table with three overrides from this job (390 parutti 'cotton', 405 nul 'thread', 407 tuni 'cloth'; 590 stays petti 'chest').
Output: cotton_out/readings_dyers.csv, cotton_out/readings_karanpura.csv  (columns: id, cisi, site, findspot, text in reading order, sounds, English)."""
from cotton_common import *
import long_common as lc
from long_common import *
lc.V2['390'] = ('parutti', 'cotton'); lc.V2['405'] = ('nūl', 'thread'); lc.V2['407'] = ('tuṇi', 'cloth')
d = faces()
sel = d[(d['area-section'].str.startswith('VS') & d.site.eq('Mohenjo-daro')) | d.site.eq('Karanpura')]
rows = []
for _, r in sel.iterrows():
    x = r.toks
    try:
        P = lc.parse_phrase(x)
        snd_s, en = lc.read_phrase(x, P)
    except Exception as e:
        snd_s, en = ' '.join(lc.snd(s) or '?' for s in x), f'(parser error {e})'
    rows.append(dict(id=r.id, cisi=r.cisi, site=r.site, findspot=f"{r['area-section']} {r['block-house']} {r['room-grid']} {r['depth']}".strip(), type=r.type, material=r.material, text='-'.join(x), sounds=snd_s, english=en))
R = pd.DataFrame(rows)
R[R.site == 'Mohenjo-daro'].to_csv(f'{OUTC}/readings_dyers.csv', index=False)
R[R.site == 'Karanpura'].to_csv(f'{OUTC}/readings_karanpura.csv', index=False)
print(len(R))
