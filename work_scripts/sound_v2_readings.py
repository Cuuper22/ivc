#!/usr/bin/env python3
"""Forty surest whole readings under the second sound list; writes /home/antigravity/Cuuper22/ivc/READINGS.md.
A text qualifies when it is complete and every sign is a number, a base value, or a value in the 'building' tier
(work_data/sound_v2/values_v2.csv); the cap mark 060 is read only inside the `920-060-jar+n` office prefix.
Ranked by how many objects carry the exact text, then sites, then length; one entry per text."""
import collections
from v2_common import *
from sound_v2_tiers import V2, TIER, CLASS
NUMW = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
ORD = {'741': 'first', '742': 'second', '745': 'third'}
OK = lambda s: s in VAL or TIER.get(s) in ('base', 'building') or s == '060'
FISHSET = FISH


def eng(s):
    if s == '700': return 'cups'
    if s == '806': return 'crop'
    g = V2[s][1].split(',')[0].split(';')[0].split('(')[0].strip()
    return g


def name_str(nm):
    parts = []
    i = 0
    while i < len(nm):
        s = nm[i]
        if s in VAL and i + 1 < len(nm) and nm[i + 1] in FISHSET:
            parts.append(f'{NUMW[VAL[s]].capitalize()}-star'); i += 2; continue
        if s in VAL and i + 1 < len(nm):
            parts.append(f'{NUMW[VAL[s]].capitalize()}-{eng(nm[i + 1]).capitalize()}'); i += 2; continue
        parts.append(eng(s)[0].upper() + eng(s)[1:]); i += 1
    return '-'.join(p.replace(' ', '-') for p in parts)


def read(x, P):
    R = P['roles']; n = len(x); out = []; snd = []; i = 0
    while i < n:
        s = x[i]; r = R[i]
        if r == 'opener':
            j = i
            while j + 1 < n and R[j + 1] == 'opener': j += 1
            blk = x[i:j + 1]
            if blk[0] in ('861', '817'):
                k = VAL.get(blk[1], 1) if len(blk) > 1 else 1
                out.append(f'Holder of {NUMW[k]} share{"s" if k > 1 else ""}:'); snd.append(f'{V2.get(blk[1], ("oru",))[0] + " " if len(blk) > 1 else ""}kāṇi')
            elif blk[0] == '820':
                k = VAL.get(blk[1], 1) if len(blk) > 1 else 1
                out.append(f'Holder of {NUMW[k]} quarter-share{"s" if k > 1 else ""}:'); snd.append(f'{V2.get(blk[1], ("oru",))[0] + " " if len(blk) > 1 else ""}kāl')
            else:
                sel = [b for b in blk if b in ORD]
                out.append(f'Office stamp, {ORD[sel[0]]} ward:' if sel else 'Office stamp:'); snd.append(' '.join(V2[b][0] for b in blk if b in V2))
            i = j + 1; continue
        if r in ('crest', 'self', 'tag', 'count', 'counted') and s not in ('740',):
            # gather a name run (numbers on fish stay in the name)
            j = i
            while j + 1 < n and R[j + 1] in ('crest', 'self', 'tag', 'count', 'counted'): j += 1
            seg = x[i:j + 1]
            nxt = R[j + 1] if j + 1 < n else None
            if all(a in VAL or CLASS.get(a) == 'GOODS' for a in seg) and nxt != 'poss' and any(CLASS.get(a) == 'GOODS' for a in seg):
                # count + goods
                ph = []
                q = 0
                while q < len(seg):
                    if seg[q] in VAL and q + 1 < len(seg): ph.append(f'{NUMW[VAL[seg[q]]]} {eng(seg[q + 1])}'); q += 2
                    elif seg[q] in VAL: ph[-1:] = [ph[-1] + f', {NUMW[VAL[seg[q]]]}'] if ph else [NUMW[VAL[seg[q]]]]; q += 1
                    else: ph.append(eng(seg[q])); q += 1
                out.append('; '.join(ph)); snd.append(' '.join(V2[a][0] for a in seg)); i = j + 1; continue
            if len(seg) >= 3 and seg[0] in VAL and CLASS.get(seg[1]) == 'GOODS':
                out.append(f'{NUMW[VAL[seg[0]]]} {eng(seg[1])}, for'); snd.append(' '.join(V2[a][0] for a in seg[:2])); seg = seg[2:]
            nm = name_str(seg); snd.append(' '.join(V2[a][0] for a in seg))
            if nxt == 'poss':
                k = j + 2; rel = [x[q] for q in range(k, n) if R[q] == 'relation']
                snd.append('kuṭi' + (' ' + ' '.join(V2[a][0] for a in rel) if rel else ''))
                if rel and rel[0] == '001':
                    out.append(f'of the {nm} house: one lot,'); i = k + 1; continue
                if '090' in rel: out.append(f'agent of the {nm} house')
                elif '400' in rel: out.append(f'junior hand of the {nm} house')
                elif '679' in rel: out.append(f'seat of the {nm} house')
                else: out.append(f'of the {nm} house')
                i = k + len(rel); continue
            if nxt == 'ending':
                e = x[j + 1]; snd.append(V2[e][0])
                out.append(f'{nm} the spearman (chief)' if e == '520' else f'{nm} the carrier' if e in PORTER else f'{nm}, junior hand' if e == '400' else nm)
                i = j + 2; continue
            out.append(nm); i = j + 1; continue
        if r and r.startswith('load'):
            out.append(('; ' if out else '') + 'n loads of crop, carried'); snd.append(' '.join(V2.get(a, ('?',))[0] for a in x[i:i + 3])); i += 3; continue
        if r == 'poss': out.append('of the house'); snd.append('kuṭi'); i += 1; continue
        if r == 'ending':
            out.append({'520': 'the spearman (chief)', '400': 'junior hand'}.get(s, 'the carrier')); snd.append(V2[s][0]); i += 1; continue
        out.append(eng(s)); snd.append(V2.get(s, ('?',))[0]); i += 1
    e = ' '.join(out).replace(' ; ', '; ').replace(': ', ': ')
    return ' '.join(snd), e[0].upper() + e[1:]


if __name__ == '__main__':
    print('stage 1/2: choosing texts ...', flush=True)
    seals = d.copy()
    seals['cplt'] = seals.complete_txt
    groups = collections.defaultdict(list)
    for row in seals.itertuples():
        x = row.tok
        if not row.cplt or len(x) < 3 or not all(OK(a) for a in x): continue
        if x.count('740') > 1: continue
        if '060' in x and not any(x[i] == '920' and x[i + 1] == '060' for i in range(len(x) - 1)): continue
        groups[x].append(row)
    cand = []
    for x, rows in groups.items():
        P = parse_face(x, lex)
        if 'unknown' in P['roles']: continue
        if P['name'] and all(a in VAL for a in P['name']): continue
        if any(R in ('count',) for R in P['roles']) and not any(R == 'counted' for R in P['roles']) and not any(a in A for a in x for A in [('465','466','467','468','469','470','471','472','473','474','475')]): continue
        sites = {r.site for r in rows}
        cand.append((len(rows), len(sites), len(x), x, rows, P))
    cand.sort(key=lambda c: (-c[0], -c[1], -c[2]))
    # keep variety: at most 8 one-copy load or ration lines of the same shape
    pick = []; shapes = collections.Counter()
    for c in cand:
        key = tuple(CLASS.get(a, 'N') for a in c[3])
        if shapes[key] >= 4: continue
        shapes[key] += 1; pick.append(c)
        if len(pick) == 40: break
    print(f'   {len(cand)} texts qualify; writing 40', flush=True)
    L = ['# Readings', '',
         'Forty inscriptions read whole under the second sound list (`jobs/out/sound_list_v2.md`; script `work_scripts/sound_v2_readings.py`). '
         'Every sign in these texts is a number, one of the first values (jar, man, fish, spear, comb, carrier, staff-bearer, tree, three-headed person) or a value whose own prediction came true. '
         'Reading order = stored order reversed. Ranked by how many objects carry the exact text, then how many cities.', '',
         'How a seal reads: [holding or office stamp] [name: house + self + tag] [ending]. The jar *kuṭi* is "of the house of"; jar + man *kuṭi āḷ* is "agent of the house of"; spear *vēḷ*, carrier *kā* and comb *ciṟ* say what the named person is. Word meanings are guesses built on measured slots; DEDR entry numbers are in the sound list.', '']
    good = []
    for c in cand:
        sn, en = read(c[3], c[5])
        import re as _re
        if _re.search(r'-(One|Two|Three|Four|Five|Six|Seven)(-|$| )', en) or en.startswith('Cups;'): continue
        if 'House-of' in en or en.split(':')[-1].strip().split('-')[0] in ('Two', 'Three', 'Four', 'One') and 'star' not in en.split(':')[-1] and 'Warrior' not in en: continue
        good.append(c)
    pick = []; shapes = collections.Counter()
    for c in good:
        key = tuple(CLASS.get(a, 'N') for a in c[3])
        if shapes[key] >= 4: continue
        shapes[key] += 1; pick.append(c)
        if len(pick) == 40: break
    for k, (nobj, nsite, ln, x, rows, P) in enumerate(pick, 1):
        snd, en = read(x, P)
        r0 = rows[0]
        types = collections.Counter(r.type.split(':')[0] for r in rows)
        sites = collections.Counter(r.site for r in rows)
        L.append(f'## {k}. {en}')
        L.append('')
        L.append(f'- Signs: `{"-".join(x)}`')
        L.append(f'- Sound: *{snd}*')
        L.append(f'- Objects: {nobj} ({", ".join(f"{t} {v}" for t, v in types.most_common())}); cities: {", ".join(f"{s} {v}" for s, v in sites.most_common())}; example {r0.cisi}')
        nm = tuple(P['name'])
        if len(nm) >= 2:
            hits = [o for o in objs.itertuples() if any(tuple(g) == nm for g in o.names)]
            L.append(f'- The name `{"-".join(nm)}` stands on {len(hits)} objects in {len({o.site for o in hits})} cities.')
        L.append(f'- Word by word: ' + ' · '.join(f'`{a}` {V2[a][0] if a in V2 else "mark"} "{eng(a) if a in V2 else "mark"}"' for a in x))
        L.append('')
    open(f'{ROOT}/READINGS.md', 'w').write('\n'.join(L) + '\n')
    print('stage 2/2: READINGS.md written', flush=True)
