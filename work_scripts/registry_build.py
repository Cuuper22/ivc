#!/usr/bin/env python3
"""WHO'S WHO, step 1: the registry of people and houses.

Plain words:
- A NAME is the run of signs between the opener (share / quarter / office words at the front) and the ending
  (the jar 740 "house of", the spear 520 "chief", keepers 151-161, comb 400 "junior", text-final guard 525-527,
  standard-bearer 368, deputy 842). Reading order = stored order reversed (the loader already reverses).
- CREST = the first word-sign of the name (number strokes skipped): the family element (name_slot.md: house-mates
  share the FIRST name sign). For the plain fish 220 / caged fish 226 the number in front is part of the star word
  (star_names.md: the form is locked to the fish), so the house key keeps it: 032+220 = Dark-star.
  Fixed two-sign house: 590-390 Boxed-cotton (cotton_house.md).
- PERSONAL part = word-signs between crest and tag; TAG = the last word-sign of a name of 2+ signs.
- AGENT = name + jar + man 090 ("X's man"): the name is the MASTER's; the seal's house key is the master's crest.
- FINDSPOT: site; area (area-section); building = area + block-house; block = area + the block number in front of
  the house number (Mohenjo-daro '7III' = block 7, house III); room = building + room-grid. At sites with no
  block-house, building = area + room-grid (Harappa grid squares, Kalibangan grid).
Writes work_data/registry/people.csv (seals read whole or nearly whole: no lost sign in the name or ending, at most
one sign without a value), names_all.csv (every face of every object kind with a name closed by an ending: used for
houses' goods words and the seal-tablet test), houses.csv.
Run: python3 registry_build.py   (about 30 s; prints progress)
"""
import sys, os, re, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
print('[registry_build] loading the catalogue and parser ...', flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v4_common import d, CNT
import pandas as pd, numpy as np

ROOT = '/home/claude/ivc'
OUT = f'{ROOT}/work_data/registry'; os.makedirs(OUT, exist_ok=True)
V3 = pd.read_csv(f'{ROOT}/work_data/values_master3.csv', dtype=str).fillna('')
V2 = pd.read_csv(f'{ROOT}/work_data/values_master2.csv', dtype=str).fillna('')
STATUS = dict(zip(V3.sign, V3.status)); SOUND = dict(zip(V3.sign, V3.sound))
READ = {s for s, st in STATUS.items() if st in ('strict', 'wide')}
SHORT = {s: w for s, w in zip(V2.sign, V2.short) if w}
SHORTN = {s: w for s, w in zip(V2.sign, V2.short_name) if w}
for s, e in zip(V3.sign, V3.english):
    if s not in SHORT: SHORT[s] = re.split(r'[;,(]', e)[0].strip()
def word(s):
    w = SHORTN.get(s) or SHORT.get(s) or f'[{s}]'
    return w[:1].upper() + w[1:]

ENG = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
ENG = ENG.set_index('face_id')
TA = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
TBIN = dict(zip(TA.obj, TA.bin))

NAMEROLES = {'crest', 'self', 'tag', 'count', 'counted'}
KEEP = {'151', '152', '153', '154', '155', '156', '157', '158', '161'}
GUARD = {'525', '526', '527'}
FINAL_TITLES = GUARD | {'368', '842'}
STARNUM = {'001': 'Lone', '031': 'Lone', '002': 'Dark', '032': 'Dark', '003': 'Three', '013': 'Three', '033': 'Three',
           '004': 'Asterism', '014': 'Asterism', '034': 'Asterism', '005': 'Five', '015': 'Five', '035': 'Five',
           '006': 'Pleiades', '016': 'Pleiades', '036': 'Pleiades', '007': 'Great-Bear', '017': 'Great-Bear', '018': 'Eight'}
STARSND = {'Lone': 'or-mīn', 'Dark': 'iru-mīn', 'Three': 'mum-mīn', 'Asterism': 'nāṇ-mīn', 'Five': 'ai-mīn',
           'Pleiades': 'aṟu-mīn', 'Great-Bear': 'eḻu-mīn', 'Eight': 'eṇ-mīn'}
SPECIES = {'Bull1': 'unicorn', 'Gaur': 'short-horned bull', 'Zebu': 'zebu', 'Elep': 'elephant', 'Rhin': 'rhinoceros',
           'Tigr': 'tiger', 'Buff': 'buffalo', 'Bull3': 'goat', 'Goat': 'goat', 'Comp': 'composite beast',
           'CompBull': 'composite beast', 'Mult': 'multi-headed beast', 'Scene': 'scene', 'Bull': 'bull (unspecified)',
           'Bull2': 'bull (type 2)', 'Bult': 'bull with table', 'Othr': 'other', 'T-A-T': 'tree-animal-tree'}

def blank(v): return v.strip() in ('', '-', '--', '- -')
def clean(v): return '' if blank(v) else v.strip().strip('-').strip()

def parse(x, R):
    """-> dict(opener, office, name_idx, ending, ending_signs, end_idx, damaged) from reading-order tokens and roles"""
    n = len(x); i = 0; op = []
    office = n >= 3 and tuple(x[:3]) == ('920', '060', '741')
    if office: op = [0, 1, 2]; i = 3
    while i < n and R[i] == 'opener': op.append(i); i += 1
    # ending
    j = next((k for k in range(i, n) if R[k] in ('poss', 'ending')), None)
    end_sig = []; end_idx = []
    if j is not None:
        name_idx = list(range(i, j)); end_idx = [j]; k = j + 1
        if R[j] == 'poss':
            while k < n and R[k] in ('relation', 'ending'): end_idx.append(k); k += 1
        rest = list(range(k, n))
    else:
        k = i; name_idx = []
        while k < n and R[k] in NAMEROLES | {'lost'}: name_idx.append(k); k += 1
        rest = list(range(k, n))
        core = [q for q in name_idx if x[q] not in CNT]
        if len(core) >= 2 and x[core[-1]] in FINAL_TITLES and core[-1] == name_idx[-1]:      # text-final title after a name
            end_idx = [core[-1]]; name_idx = name_idx[:-1]
    damaged = any(x[q] in ('000', 'ALT') or R[q] == 'lost' for q in op + name_idx + end_idx) or any(R[q] not in NAMEROLES for q in name_idx)
    return dict(op=op, office=office, name_idx=name_idx, end_idx=end_idx, rest=rest, damaged=damaged)

def ending_label(x, end_idx, name_idx):
    s = [x[q] for q in end_idx]
    if not s: return 'none', ''
    if s[0] == '740':
        rel = s[1:]
        if not rel: return 'house of', '740'
        if rel[0] == '090': return ("X's man, junior" if '400' in rel[1:] else "X's man"), '-'.join(s)
        if rel[0] == '400': return 'house of, junior', '-'.join(s)
        if rel[0] == '679': return 'house of, seat', '-'.join(s)
        if rel[0] == '621': return 'house of, store', '-'.join(s)
        if rel[0] in KEEP: return 'house of, keeper', '-'.join(s)
        if rel[0] == '520': return 'house of, chief', '-'.join(s)
        return f'house of, {word(rel[0]).lower()}', '-'.join(s)
    if s[0] == '520': return 'chief', '520'
    if s[0] in KEEP: return 'keeper', s[0]
    if s[0] == '400': return 'junior', '400'
    if s[0] in GUARD:
        core = [x[q] for q in name_idx if x[q] not in CNT]
        return ('gate-guard' if core and core[-1] in ('550', '555') else 'guard'), s[0]
    if s[0] == '368': return 'standard-bearer', '368'
    if s[0] == '842': return 'deputy', '842'
    return word(s[0]).lower(), s[0]

def name_parts(x, name_idx):
    """crest / personal / tag / house key / house English / house sounds"""
    core = [q for q in name_idx if x[q] not in CNT]
    if not core: return None
    c0 = core[0]; crest = x[c0]
    pre = [x[q] for q in name_idx if q < c0 and x[q] in CNT]
    key = crest; heng = word(crest); hsnd = SOUND.get(crest, f'[{crest}]')
    if crest in ('220', '226') and pre:
        key = pre[-1] + '+' + crest; sw = STARNUM.get(pre[-1], 'Num')
        heng = f'{sw}-star'; hsnd = STARSND.get(sw, hsnd)
    if crest == '590' and len(core) >= 2 and x[core[1]] == '390':
        key = '590-390'; heng = 'Boxed-cotton'; hsnd = 'peṭṭi-parutti'; core = [c0] + core[2:]
        core_rest = core[1:]
    else: core_rest = core[1:]
    tag = x[core_rest[-1]] if core_rest else ''
    personal = '-'.join(x[q] for q in core_rest[:-1]) if len(core_rest) >= 2 else ''
    return dict(crest=crest, house_key=key, house_en=heng, house_snd=hsnd, personal=personal, tag=tag,
                name_full='-'.join(x[q] for q in name_idx), name_core='-'.join(x[q] for q in core))

rows = []
print(f'[registry_build] parsing {len(d)} faces ...', flush=True)
for n_, (fid, x, P, kind, site) in enumerate(zip(d.id, d.tok, d.P, d.kind, d.site)):
    if n_ % 1000 == 0: print(f'   {n_} / {len(d)} faces', flush=True)
    R = P['roles']; x = list(x)
    if len(R) != len(x): continue
    p = parse(x, R)
    if not p['name_idx']: continue
    if not p['end_idx'] and kind != 'seal': continue        # goods objects: only names closed by an ending
    np_ = name_parts(x, p['name_idx'])
    if np_ is None: continue
    endl, ends = ending_label(x, p['end_idx'], p['name_idx'])
    r = d[d.id == fid].iloc[0] if False else None
    rows.append(dict(face_id=fid, n=n_, kind=kind, site=site, damaged=p['damaged'], office=p['office'],
                     opener='-'.join(x[q] for q in p['op']), ending=endl, ending_signs=ends,
                     rest='-'.join(x[q] for q in p['rest']), signs='-'.join(x), **np_))
A = pd.DataFrame(rows)
meta = d.set_index('id')
def gm(col): return A.face_id.map(meta[col])
A['object_id'] = gm('obj'); A['cisi'] = gm('cisi'); A['region'] = gm('region')
A['area'] = gm('area-section').map(clean); A['bh'] = gm('block-house').map(clean); A['room_raw'] = gm('room-grid').map(clean)
A['symbol'] = gm('symbol').fillna(''); A['type'] = gm('type')
A['hmm'] = pd.to_numeric(gm('horizontal(mm)'), errors='coerce'); A['vmm'] = pd.to_numeric(gm('vertical(mm)'), errors='coerce')
A['depth'] = gm('depth')
def building(r):
    if not r.area: return ''
    if r.bh: return f'{r.site}|{r.area}|{r.bh}'
    if r.room_raw: return f'{r.site}|{r.area}|{r.room_raw}'
    return ''
def block(r):
    if not r.area: return ''
    if r.bh:
        m = re.match(r'^(\d+)', r.bh)
        return f'{r.site}|{r.area}|blk{m.group(1)}' if m else f'{r.site}|{r.area}|{r.bh}'
    if r.room_raw:
        m = re.match(r'^-?([A-Z]+)', r.room_raw)
        return f'{r.site}|{r.area}|{m.group(1)}' if m else f'{r.site}|{r.area}|{r.room_raw}'
    return ''
A['area_key'] = [f'{s}|{a}' if a else '' for s, a in zip(A.site, A.area)]
A['building'] = A.apply(building, axis=1); A['block'] = A.apply(block, axis=1)
A['room'] = [f'{b}|{r}' if b and r and r != b.split('|')[-1] else '' for b, r in zip(A.building, A.room_raw)]
A['bin'] = A.object_id.map(TBIN).fillna('')
sp = A.symbol.str.split(':', n=1)
A['animal'] = [SPECIES.get(s[0], s[0]) if s[0] not in ('', '-') else ('none' if s[0] == '' else '') for s in sp]
A['stand'] = [s[1] if len(s) > 1 else '' for s in sp]
A['master'] = np.where(A.ending.str.startswith("X's man"), A.name_core, '')
A['sounds'] = A.face_id.map(ENG.sounds).fillna(''); A['english'] = A.face_id.map(ENG.english).fillna('')
A['grade'] = A.face_id.map(ENG.grade).fillna('')
A['n_unread'] = [sum(1 for s in sg.split('-') if s not in READ and s not in ('000', 'ALT')) for sg in A.signs]
A.to_csv(f'{OUT}/names_all.csv', index=False)
print(f'[registry_build] names_all: {len(A)} faces with a name ({(A.kind == "seal").sum()} seals)', flush=True)

# ---------- people.csv: seals, read whole or nearly whole ----------
GOODSW = {'390', '405', '413', '416', '806', '838', '845', '844', '831', '501', '700', '705', '706', '711', '575', '590', '923', '226'}
A['goods_line'] = [(e == 'none') and (c in GOODSW) and (f.split('-')[0] != c) for e, c, f in zip(A.ending, A.crest, A.name_full)]   # 'three cotton' with no ending: an amount, not a person
Pp = A[(A.kind == 'seal') & (~A.damaged) & (A.n_unread <= 1) & A.grade.isin(['whole', 'part']) & (~A.goods_line)].copy()
cols = ['cisi', 'object_id', 'face_id', 'site', 'area', 'bh', 'block', 'room_raw', 'bin', 'animal', 'stand', 'opener', 'office',
        'crest', 'house_key', 'house_en', 'personal', 'tag', 'ending', 'ending_signs', 'master', 'name_full', 'signs', 'sounds', 'english',
        'grade', 'n_unread', 'hmm', 'vmm', 'building', 'area_key', 'room']
Pp = Pp[cols].rename(columns={'site': 'city', 'bh': 'house_block', 'room_raw': 'room_grid', 'bin': 'date_bin'})
Pp.to_csv(f'{OUT}/people.csv', index=False)
print(f'[registry_build] people.csv: {len(Pp)} seals (whole {(Pp.grade == "whole").sum()}, nearly whole {(Pp.grade != "whole").sum()}); '
      f'{Pp.house_key.nunique()} house keys; agents {(Pp.master != "").sum()}', flush=True)

# ---------- houses.csv ----------
GOODS = {  # goods words, by kind (from MAP.md readings)
    'cotton': {'390', '405', '370', '371'},
    'grain': {'413', '416', '421', '422', '423', '424', '605', '806', '838', '831', '844', '845', '501'},
    'store/measure': {'575', '621', '590', '592', '335', '336', '700', '703', '705', '706', '711', '540', '554', '320', '321', '323', '171', '480'},
    'ivory/metal/bead': {'923', '595', '790', '645', '850'},
    'fish': {'226'},
    'ship': {'500'},
    'loads': {str(s) for s in range(465, 476)},
}
G2K = {s: k for k, v in GOODS.items() for s in v}
Aok = A[(~A.damaged) & (~A.goods_line)]
# goods words beside a house name on goods objects: signs on any face of the object outside the name itself
objfaces = d.groupby('obj')
goods_by_obj = {}
for o, g in objfaces:
    goods_by_obj[o] = [s for x in g.tok for s in x]
H = []
seals = Pp
for key, g in Aok.groupby('house_key'):
    sg = seals[seals.house_key == key]
    agents_seal = sg[sg.master != '']
    members = sg[sg.master == '']
    goods_objs = g[g.kind != 'seal']
    gw = collections.Counter()
    for _, r in goods_objs.drop_duplicates('object_id').iterrows():
        nm = r.name_full.split('-')
        toks = list(goods_by_obj.get(r.object_id, []))
        for s in nm:
            if s in toks: toks.remove(s)
        for s in set(toks):
            if s in G2K: gw[f'{s} {word(s).lower()}'] += 1
    H.append(dict(house_key=key, sounds=g.house_snd.iloc[0], english=g.house_en.iloc[0],
                  members=len(members), agents_kept=len(agents_seal), seals=len(sg),
                  objects_all=g.object_id.nunique(), goods_objects=goods_objs.object_id.nunique(),
                  cities=';'.join(f'{k} {v}' for k, v in g.drop_duplicates('object_id').site.value_counts().items()),
                  n_cities=g.site.nunique(),
                  areas=';'.join(f'{k} {v}' for k, v in g[g.area_key != ''].drop_duplicates('object_id').area_key.value_counts().head(8).items()),
                  date_bins=';'.join(f'{b} {(g.drop_duplicates("object_id").bin == b).sum()}' for b in ('early', 'middle', 'late')),
                  endings=';'.join(f'{k} {v}' for k, v in sg.ending.value_counts().items()),
                  animals=';'.join(f'{k} {v}' for k, v in sg.animal.value_counts().items() if k),
                  overseas_bull=int((sg.animal == 'short-horned bull').sum()),
                  goods_words=';'.join(f'{k} {v}' for k, v in gw.most_common(8))))
H = pd.DataFrame(H).sort_values(['objects_all', 'seals'], ascending=False)
H.to_csv(f'{OUT}/houses.csv', index=False)
print(f'[registry_build] houses.csv: {len(H)} house keys; top 10 by objects:', flush=True)
print(H.head(10)[['house_key', 'english', 'seals', 'members', 'agents_kept', 'objects_all', 'n_cities']].to_string(index=False))
