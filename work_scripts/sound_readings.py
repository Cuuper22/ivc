#!/usr/bin/env python3
"""Task 6: read 40 inscriptions whole (sounds + English) with the sound table, surest first; writes READINGS.md.
Sureness = every sign has a working sound, and the share of its signs whose value is one of the first seven,
a number, or a value whose own check came true (work_data/sound/checks.csv)."""
import sys, os, collections
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss2 import load2, learn, parse_face
from sound_values import ALL_SOUNDS, OLD
ROOT = '/home/antigravity/Cuuper22/ivc'
chk = pd.read_csv(f'{ROOT}/work_data/sound/checks.csv', dtype=str)
PASSED = set(chk[chk.came_true == 'yes'].sign) | set(OLD) | {'233', '235', '240', '231'}   # fish: 'mark + mīn' split test came true
NUM = {f'{i:03d}': i for i in range(1, 8)}; NUM.update({'012': 2}); NUM.update({f'{i:03d}': i - 10 for i in range(13, 19)}); NUM.update({f'{i:03d}': i - 30 for i in range(31, 37)})
WORD = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
REL = {'090': 'manager', '400': 'junior', '679': 'seat', '001': 'one'}
END = {'520': 'chief', '090': 'manager', '400': 'junior', '151': 'keeper', '154': 'keeper', '156': 'keeper', '158': 'keeper', '155': 'keeper'}
def snd(s): return ALL_SOUNDS.get(s, ('?', '?'))
def title(g): return g.split(',')[0].split('(')[0].strip()

def english(x, P):
    R = list(P['roles']); out = []; i = 0; n = len(x)
    FISH = {'220', '235', '240', '233', '231', '226', '236'}
    for q in range(n - 1):   # a number written on a fish inside a name is part of the name (iru mīn = Two-star)
        if R[q] == 'count' and R[q + 1] == 'counted' and x[q + 1] in FISH: R[q] = R[q + 1] = 'self'
    while i < n:
        s, r = x[i], R[i]
        if r == 'opener':
            j = i
            while j + 1 < n and R[j + 1] == 'opener': j += 1
            blk = x[i:j + 1]
            if blk[0] in ('861', '817'): out.append(f'{WORD[NUM.get(blk[1], 1)] if len(blk) > 1 else "a"} share{"s" if len(blk) > 1 and NUM.get(blk[1], 1) > 1 else ""} (kāṇi):')
            elif blk[0] == '820': out.append(f'{WORD[NUM.get(blk[1], 1)] if len(blk) > 1 else "a"} quarter{"s" if len(blk) > 1 and NUM.get(blk[1], 1) > 1 else ""} (kāl):')
            else:
                sel = [b for b in blk if b in ('741', '742', '745')]
                head = {'920': 'month', '692': 'X-office', '550': 'Gate', '820': 'quarter'}.get(blk[0], 'opening')
                out.append(f'[{head}, {({"741": "first", "742": "second", "745": "third"}[sel[0]]) + " ward" if sel else "mark"}]:')
            i = j + 1; continue
        if r == 'count' and i + 1 < n and R[i + 1] == 'counted':
            v = NUM.get(s, 'n'); out.append(f'{WORD[v] if isinstance(v, int) and v < 9 else v} {title(snd(x[i + 1])[1])}'); i += 2; continue
        if r == 'counted' and i + 1 < n and R[i + 1] == 'count':
            v = NUM.get(x[i + 1], 0); out.append(f'{title(snd(s)[1])}, {WORD[v] if v < 9 else v}'); i += 2; continue
        if r in ('load-count',):
            out.append(f'n loads of {title(snd(x[i + 1])[1])}, carried'); i += 3; continue
        if r in ('crest', 'self', 'tag', 'lost'):
            j = i
            while j + 1 < n and R[j + 1] in ('crest', 'self', 'tag', 'lost'): j += 1
            nm = '-'.join(title(snd(t)[1]).replace(' ', '-').capitalize() if t not in ('000', 'ALT') else '(lost)' for t in x[i:j + 1])
            if j + 1 < n and R[j + 1] == 'poss':
                k = j + 2; rels = []
                while k < n and R[k] == 'relation': rels.append(REL.get(x[k], title(snd(x[k])[1]))); k += 1
                out.append((' '.join(rels) + ' of ' if rels else 'of ') + f'the {nm} house'); i = k; continue
            out.append(nm); i = j + 1; continue
        if r == 'poss': out.append('of the house'); i += 1; continue
        if r == 'ending': out.append(END.get(s, title(snd(s)[1]))); i += 1; continue
        if r == 'count': out.append(WORD[NUM[s]] if NUM.get(s, 0) < 9 else str(NUM[s])); i += 1; continue
        out.append(title(snd(s)[1])); i += 1
    return ' '.join(out).replace(': ', ': ').strip()

def main():
    print('stage 1/2: parsing and scoring ...', flush=True)
    d = load2(); lex = learn(d)
    meta = d
    rows = []
    seen = collections.Counter()
    for k, r in d.iterrows():
        x = r.tok
        if not r.complete_txt or len(x) < 2: continue
        if not all(s in ALL_SOUNDS and snd(s)[0] not in ('?',) for s in x): continue
        P = parse_face(x, lex); R = P['roles']
        if any(q is None or q in ('lost', 'tail') for q in R): continue
        sure = sum(s in PASSED for s in x) / len(x)
        rows.append((sure, len(x), r, x, P))
        seen['-'.join(x)] += 1
    print(f'   {len(rows)} faces read whole with the table', flush=True)
    rows.sort(key=lambda t: (-t[0], -min(t[1], 6), -seen['-'.join(t[3])]))
    pick, used, tmpl = [], set(), collections.Counter()
    for sure, L, r, x, P in rows:
        key = '-'.join(x)
        t = ' '.join(q[:4] for q in P['roles'])
        if key in used or tmpl[t] >= 3 or L < 3: continue
        used.add(key); tmpl[t] += 1; pick.append((sure, r, x, P))
        if len(pick) == 40: break
    print('stage 2/2: writing READINGS.md ...', flush=True)
    L = ['# Readings', '',
         'Forty inscriptions read whole with the working sound table (`jobs/out/sound_list.md`, script `work_scripts/sound_readings.py`), the surest first. Reading order = stored order reversed. Sureness = share of the signs whose value is one of the first seven, a number, or a value whose own prediction came true on the data (`work_data/sound/checks.csv`); every sign in these texts has a working sound.',
         '', 'Each sign is written `number picture [measured slot / working sound]`. The measured slot is the role the possessive parser (`work_scripts/gloss2.py`) gives the sign from position alone; the working sound is the early Dravidian value we build on. Copies: number of faces in the corpus with exactly this text.', '']
    for n, (sure, r, x, P) in enumerate(pick, 1):
        signs = ' · '.join(f'`{s}` {title(snd(s)[1]) if s not in NUM else WORD[NUM[s]]} [{P["roles"][i]} / {snd(s)[0]}]' for i, s in enumerate(x))
        where = ', '.join(v for v in [r.site, r['area-section'], r['block-house'], r['room-grid'], ('depth ' + r.depth) if r.depth not in ('- -', '') else ''] if v and v not in ('--', '-'))
        L += [f'## {n}. {r.cisi or r.id}: {r.type}, {where}', '',
              f'- Text: `{"-".join(x)}` ({seen["-".join(x)]} cop{"y" if seen["-".join(x)] == 1 else "ies"}; animal: {r.symbol or "-"}; sureness {sure:.0%})',
              f'- Sound: *{" ".join(snd(s)[0] for s in x)}*',
              f'- English: {english(x, P)}', f'- Signs: {signs}', '']
    open(f'{ROOT}/READINGS.md', 'w').write('\n'.join(L))
    print('done:', len(pick), 'readings')
main()
