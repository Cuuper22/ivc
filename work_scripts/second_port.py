#!/usr/bin/env python3
"""Steps 3 and 4: run the possessive-model parser (gloss2.py) on Mahadevan texts through the crosswalk, then pictures and loci.
Run: python3 second_port.py  -> prints tables; writes work_data/mahadevan_parsed.csv
"""
import sys, collections, random, math
import numpy as np
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from mah_common import *
import gloss2
from gloss2 import learn, parse_face, is_tight, is_strict, template, sentence
from gloss import load
from second_measure import MSHORT, MLONG, LSHORT, LLONG

W = f'{ROOT}/work_data'
STROKE = {97: '001', 98: '001', 99: '002', 100: '002', 101: '012', 102: '003', 103: '013', 104: '004', 105: '014', 106: '005', 107: '015',
          108: '006', 109: '016', 110: '007', 112: '017', 114: '018', 86: '031', 87: '032', 89: '033', 95: '034', 96: '035'}


def inverse_map():
    df = pd.read_csv(f'{W}/lipi_mahadevan_crosswalk.csv', dtype={'lipi': str})
    best = {}
    for r in df.itertuples():
        if r.text_positions < 2: continue
        if r.mahadevan not in best or r.text_positions > best[r.mahadevan][1]: best[r.mahadevan] = (r.lipi, r.text_positions)
    inv = {m: v[0] for m, v in best.items()}
    inv.update({15: '156', 12: '151', 178: '468', 267: '861', 99: '002'})
    inv.update(STROKE)
    return inv


def translate(toks, inv):
    out = []
    for i, x in enumerate(toks):
        if x == 0: out.append('000'); continue
        if x == 15 and i and toks[i - 1] == 389: out.append('158'); continue
        out.append(inv.get(x, f'X{x}'))
    return tuple(out)


def mah_frame(inv):
    m = load_mah()
    m['tok'] = [translate(t, inv) for t in m.toks]
    m['complete_txt'] = m.complete
    return m


def cramers(rows):
    """rows: list of (a, b) -> (chi2, dof-ish) via permutation of b."""
    a = [x for x, _ in rows]; b = [y for _, y in rows]
    def chi(a, b):
        ct = collections.Counter(zip(a, b)); ca = collections.Counter(a); cb = collections.Counter(b); n = len(a)
        return sum((ct[(x, y)] - ca[x] * cb[y] / n) ** 2 / (ca[x] * cb[y] / n) for x in ca for y in cb if ca[x] * cb[y] > 0 and ct[(x, y)] >= 0)
    obs = chi(a, b); rng = random.Random(1); ge = 0; null = []
    for _ in range(300):
        bb = b[:]; rng.shuffle(bb); c = chi(a, bb); null.append(c); ge += c >= obs
    return obs, float(np.mean(null)), (ge + 1) / 301


def main():
    inv = inverse_map()
    d = load2 = gloss2.load2()
    lex = learn(d)
    m = mah_frame(inv)
    # parse everything
    res = [parse_face(x, lex, lex['owner']) for x in m.tok]
    m['tight'] = [is_tight(x, r, lex) for x, r in zip(m.tok, res)]
    m['strict'] = [is_strict(x, r) for x, r in zip(m.tok, res)]
    m['template'] = [template(x, r) for x, r in zip(m.tok, res)]
    m['gloss'] = [sentence(x, r) for x, r in zip(m.tok, res)]
    m['ending'] = [r['ending_kind'] for r in res]
    m['relation'] = [r['relation'] or '' for r in res]
    m['name'] = ['-'.join(r['name']) for r in res]
    m['roles'] = [' '.join(r['roles']) for r in res]
    m['unmapped'] = [sum(1 for s in x if s.startswith('X')) for x in m.tok]
    m['reading_mah'] = ['-'.join(map(str, t)) for t in m.toks]
    m['reading_lipi'] = ['-'.join(x) for x in m.tok]
    m[['textnum', 'site', 'cls', 'fs', 'locus', 'level', 'sideline', 'complete', 'n', 'reading_mah', 'reading_lipi', 'template', 'name', 'ending',
       'relation', 'gloss', 'tight', 'strict', 'unmapped']].to_csv(f'{W}/mahadevan_parsed.csv', index=False)
    c = m[m.complete & (m.n >= 2)].drop_duplicates(['site', 'cls', 'reading_mah'])
    print('MAHADEVAN distinct complete texts (2+ signs):', len(c), 'tight', int(c.tight.sum()), round(100 * c.tight.mean(), 1), 'strict', int(c.strict.sum()), round(100 * c.strict.mean(), 1))
    print('  with every sign mapped to a Lipi sign:', int((c.unmapped == 0).sum()), '; tight among those', int(c[c.unmapped == 0].tight.sum()), round(100 * c[c.unmapped == 0].tight.mean(), 1))
    print('  by site:'); print(c.groupby('site').tight.agg(['size', 'sum', 'mean']).round(3).to_string())
    print('  by object class:'); print(c.groupby('cls').tight.agg(['size', 'sum', 'mean']).round(3).to_string())
    # Lipi same rule, same filter
    l = d.copy(); l['gsite'] = [lipi_site(s, r) for s, r in zip(l.site, l.region)]
    lc = l[l.complete_txt & (l.tok.apply(len) >= 2)].drop_duplicates(['gsite', 'tok'])
    lr = [parse_face(x, lex, lex['owner']) for x in lc.tok]
    lc = lc.assign(tight=[is_tight(x, r, lex) for x, r in zip(lc.tok, lr)])
    print('LIPI same rule:', len(lc), int(lc.tight.sum()), round(100 * lc.tight.mean(), 1)); print(lc.groupby('gsite').tight.agg(['size', 'mean']).round(3).to_string())
    # texts of Mahadevan with no Lipi partner = objects the Lipi catalogue did not supply
    tp = pd.read_csv(f'{W}/crosswalk_text_pairs.csv', dtype=str)
    matched = set(tp.mahadevan_text)
    c = c.assign(matched=[r in matched for r in c.reading_mah])
    for k, g in c.groupby('matched'):
        print('  M texts', 'with a Lipi partner' if k else 'with NO Lipi partner (unseen)', len(g), 'tight', int(g.tight.sum()), round(100 * g.tight.mean(), 1))
    print('  unseen texts by site:', c[~c.matched].groupby('site').tight.agg(['size', 'mean']).round(3).to_dict())
    # what breaks M parses
    bad = c[~c.tight]
    print('untight M texts: with lost/tail roles', sum(('lost' in r or 'tail' in r) for r in bad.roles), 'of', len(bad)); 
    print('  untight M texts carrying at least one unmapped sign:', int((bad.unmapped > 0).sum()))
    # ---- name roles in M vs Lipi
    def name_stats(frame_tok, label):
        first = collections.Counter(); n = 0; last = collections.Counter(); fishfirst = 0
        for x in frame_tok:
            r = parse_face(x, lex, lex['owner'])
            nm = r['name']
            if len(nm) >= 2 and r['ending_kind'] != 'none':
                n += 1; first[nm[0]] += 1; last[nm[-1]] += 1
        fish = sum(first[s] for s in ('235', '240', '233', '231')); tags = sum(last[s] for s in ('760', '100'))
        print(label, 'multi-sign names', n, '| open with a fish crest', fish, f'({100 * fish / n:.0f}%) | end in 760/100', tags, f'({100 * tags / n:.0f}%)')
        return n
    name_stats(list(c.tok), 'M names (through crosswalk):'); name_stats(list(lc.tok), 'Lipi names:')
    for tg in ('760', '100'):
        for lab, frame in (('M', c.tok), ('Lipi', lc.tok)):
            ends = cnt = 0
            for x in frame:
                r = parse_face(x, lex, lex['owner']); nm = r['name']
                if tg in nm: cnt += 1; ends += (nm[-1] == tg and len(nm) >= 2)
            print(f'  sign {tg} inside names: last in {ends} of {cnt} ({lab})')
    # ---- two counting systems: share of full-height vs short counts before each thing
    def count_systems(toks_list, short, long, things, label):
        out = {}
        for nm, ss in things.items():
            sh = lg = 0
            for t in toks_list:
                for i in range(1, len(t)):
                    if t[i] in ss:
                        if t[i - 1] in short: sh += 1
                        elif t[i - 1] in long: lg += 1
            out[nm] = (sh, lg)
        print(label, {k: f'short {a} / tall {b}' for k, (a, b) in out.items()})
    mt = list(c.toks); lt = list(lc.tok)
    count_systems(mt, set(MSHORT), set(MLONG), {'cup 328': {328}, 'jar 342': {342}, 'box 249': {249}, 'tree 162': {162}, 'plain fish 59': {59}, 'whisker fish 67': {67}, 'crop 389': {389}, 'woman 17': {17}}, 'M  ')
    count_systems(lt, set(LSHORT), set(LLONG), {'cup 700': {'700'}, 'jar 740': {'740'}, 'box 590': {'590'}, 'tree 390': {'390'}, 'plain fish 220': {'220'}, 'whisker fish 240': {'240'}, 'crop 806': {'806'}, 'woman 140': {'140'}}, 'Lipi')
    # ---- step 4: picture
    s = m[(m.cls.isin(['seal', 'sealing'])) & m.complete & (m.fs != '0') & (m.n >= 2)].drop_duplicates(['site', 'reading_mah', 'fs'])
    s = s.assign(animal=[field_symbol(f)[0] for f in s.fs])
    top = s.animal.value_counts()
    print('seal texts with a picture code', len(s), '; most common picture codes:', top.head(8).to_dict())
    keep = set(top[top >= 12].index)
    ss = s[s.animal.isin(keep)]
    # ending (class) sign vs animal
    e = ss[ss.relation != ''].copy(); e['cl'] = [rel.split('+')[0] for rel in e.relation]
    e = e[e.cl.isin(e.cl.value_counts()[lambda v: v >= 8].index)]
    rows = list(zip(e.animal, e.cl))
    print('closing/relation sign vs picture code: n', len(rows), 'chi2 %.1f, shuffle mean %.1f, p %.3f' % cramers(rows))
    # first name sign vs animal
    nm = ss[ss.name.str.contains('-') | (ss.name != '')].copy(); nm['first'] = [x.split('-')[0] for x in nm.name]
    nm = nm[nm['first'].isin(nm['first'].value_counts()[lambda v: v >= 8].index)]
    rows = list(zip(nm.animal, nm['first']))
    print('first name sign vs picture code: n', len(rows), 'chi2 %.1f, shuffle mean %.1f, p %.3f' % cramers(rows))
    # picture x class sign table (top)
    ct = pd.crosstab(e.animal, e.cl); print(ct.loc[ct.sum(1).sort_values(ascending=False).index[:6], ct.sum(0).sort_values(ascending=False).index[:7]].to_string())
    # ---- loci
    print('locus: pairs at one site/locus (and level within 3) sharing first name sign vs shuffled')
    z = m[(m.cls.isin(['seal', 'sealing'])) & m.complete & (m.name != '') & (m.ending != 'none')].drop_duplicates(['site', 'reading_mah', 'locus', 'level'])
    z = z.assign(first=[x.split('-')[0] for x in z.name], last=[x.split('-')[-1] for x in z.name], lv=[int(v) for v in z.level])
    def pairs(z, key):
        c = 0; tot = 0
        for (site, loc), g in z.groupby(['site', 'locus']):
            if loc in ('0', '') : continue
            rows = list(g.itertuples())
            for i in range(len(rows)):
                for j in range(i + 1, len(rows)):
                    if abs(rows[i].lv - rows[j].lv) <= 3 and rows[i].reading_mah != rows[j].reading_mah:
                        tot += 1; c += getattr(rows[i], key) == getattr(rows[j], key)
        return c, tot
    for key in ('first', 'last'):
        obs, tot = pairs(z, key)
        rng = random.Random(2); nulls = []
        for _ in range(100):
            zz = z.copy(); zz[key] = rng.sample(list(z[key]), len(z)) if False else np.random.RandomState(rng.randrange(10**6)).permutation(z[key].values)
            nulls.append(pairs(zz, key)[0])
        print(f'  {key} name sign shared: {obs} of {tot} pairs against {np.mean(nulls):.1f} by shuffling (max in 100 shuffles {max(nulls)})')
    # house-like: loci by level sign sharing among rare signs: first sign among crest fish
    return m


if __name__ == '__main__': main()
