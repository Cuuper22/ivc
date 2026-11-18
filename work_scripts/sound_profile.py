#!/usr/bin/env python3
"""Profile every sign: slots it fills, what it sits beside, where it lives in the world.
Reading order = stored order reversed. Roles from gloss2.parse_face (possessive parser).
Run: python3 sound_profile.py -> work_data/sound/profile.csv, work_data/sound/top80.txt
"""
import sys, os, collections, statistics
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss2 import load2, learn, parse_face, CNT
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/sound'

# signs that already have a working sound or a job of their own in this run
VALUED = {'740', '090', '220', '520', '400', '151', '153', '154', '155', '156', '157', '158', '142', '390', '100',
          '000', 'ALT'} | set(CNT)
OWN_TASK = {'235', '240', '233', '231', '226', '700', '806', '861', '817', '820', '060', '920'}

def main():
    print('stage 1/3: parsing every face ...', flush=True)
    d = load2(); lex = learn(d)
    sh = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str)
    shape = dict(zip(sh.lipi_wells_number, sh.shape_description))
    cw = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
    cw = cw[cw.rank_for_lipi_sign == '1']; mah = dict(zip(cw.lipi, cw.mahadevan))
    P = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    occ = collections.Counter(); objs = collections.defaultdict(set); face = collections.defaultdict(list)
    seen_txt = set()
    for k, row in d.iterrows():
        x = row.tok
        r = parse_face(x, lex)
        R = r['roles']
        grp = {}
        # position inside its name group
        gi = [i for i in range(len(x)) if R[i] in ('crest', 'self', 'tag')]
        groups = []; cur = []
        for i in range(len(x)):
            if R[i] in ('crest', 'self', 'tag', 'lost'): cur.append(i)
            else:
                if cur: groups.append(cur); cur = []
        if cur: groups.append(cur)
        for g in groups:
            for q, i in enumerate(g):
                grp[i] = 'alone' if len(g) == 1 else 'first' if q == 0 else 'last' if q == len(g) - 1 else 'mid'
        try: area = float(row['horizontal(mm)']) * float(row['vertical(mm)'])
        except: area = None
        animal = (row.symbol or '-').split(':')[0]
        for i, s in enumerate(x):
            occ[s] += 1; objs[s].add(row.cisi or row.id)
            p = P[s]
            p['role'][R[i] or 'none'] += 1
            if i in grp: p['namepos'][grp[i]] += 1
            p['prev'][x[i - 1] if i > 0 else '^'] += 1
            p['next'][x[i + 1] if i + 1 < len(x) else '$'] += 1
            if i > 0 and x[i - 1] in CNT and R[i] == 'counted': p['countbefore'][x[i - 1]] += 1
            if i + 1 < len(x) and x[i + 1] in CNT and R[i] == 'counted': p['countafter'][x[i + 1]] += 1
            p['group'][row.group] += 1
            p['site'][row.site] += 1
            p['animal'][animal] += 1
            p['area'][f'{row.site[:4]}:{row["area-section"]}'] += 1
            p['ending'][r['ending_kind']] += 1
            if row.group == 'seal' and area and area > 0: face[s].append(area)
    print('stage 2/3: baselines ...', flush=True)
    base = {k: collections.Counter() for k in ('group', 'site', 'animal', 'area')}
    for s in P:
        for k in base: base[k].update(P[s][k])
    tot = {k: sum(v.values()) for k, v in base.items()}
    def enr(s, k, top=3, minn=3):
        c = P[s][k]; n = sum(c.values()); out = []
        for v, m in c.most_common():
            e = (m / n) / (base[k][v] / tot[k])
            if m >= minn and e >= 1.8: out.append(f'{v} {m}/{n} x{e:.1f}')
            if len(out) >= top: break
        return '; '.join(out)
    allface = statistics.median([a for s in face for a in face[s]])
    rows = []
    for s, n in occ.most_common():
        p = P[s]
        rows.append(dict(sign=s, n=n, objects=len(objs[s]), mahadevan=mah.get(s, ''), shape=shape.get(s, ''),
            valued=s in VALUED, own_task=s in OWN_TASK,
            roles='; '.join(f'{a} {b}' for a, b in p['role'].most_common(5)),
            namepos='; '.join(f'{a} {b}' for a, b in p['namepos'].most_common()),
            prev='; '.join(f'{a} {b}' for a, b in p['prev'].most_common(5)),
            next='; '.join(f'{a} {b}' for a, b in p['next'].most_common(5)),
            countbefore='; '.join(f'{a} {b}' for a, b in p['countbefore'].most_common(4)),
            countafter='; '.join(f'{a} {b}' for a, b in p['countafter'].most_common(3)),
            groups='; '.join(f'{a} {b}' for a, b in p['group'].most_common(4)),
            sites='; '.join(f'{a} {b}' for a, b in p['site'].most_common(3)),
            enr_group=enr(s, 'group'), enr_site=enr(s, 'site'), enr_animal=enr(s, 'animal'), enr_area=enr(s, 'area'),
            seal_face_med=round(statistics.median(face[s])) if len(face[s]) >= 3 else '',
            endings='; '.join(f'{a} {b}' for a, b in p['ending'].most_common(3))))
    df = pd.DataFrame(rows); df.to_csv(f'{OUT}/profile.csv', index=False)
    top = df[~df.valued & ~df.own_task].head(80)
    top.to_csv(f'{OUT}/top80.csv', index=False)
    print('stage 3/3: done.', len(df), 'signs; all-seal median face', allface)
    print('top-80 cover', top.n.sum(), 'tokens of', df.n.sum())
main()
