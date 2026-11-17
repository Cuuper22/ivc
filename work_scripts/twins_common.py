#!/usr/bin/env python3
"""Shared kit for the TWINS job (what is a text, what is a stone).  Written 2026-11-17.

Plain words:
- SEAL: a carved stamp (catalogue type SEAL...). Tablets, tags, sealings and pots are left out of this job.
- FACE: one inscribed side. Most seals have one face; prisms have 3-5.
- COMPLETE TEXT: a face with no lost sign and no break flag in the first catalogue (Lipi).
  'wide' = no lost sign, a break flag allowed (the break is on the stone, not through the text).
- TWIN SET: two or more different seals (different object ids) carrying the identical complete text, sign for sign.
- KIND of a text: from the frame-v2 job classes (work_data/frame/corpus_jobs.csv, column v2_classes), see text_kind().
- STAND letter: the catalogue code after 'Bull1:' (unicorn seals): W, J, S, I, L = the stand drawn before the unicorn
  (column stand5 keeps only these five; rarer codes U, II, V, X ... stay in column stand).
- ANIMAL: species from the catalogue symbol; 'none' = an inscription-only seal (no animal carved); '' = not recorded.
- BOSS code: the catalogue 'boss' column. First letter P = pierced (perforated), N = not pierced, ? = unknown;
  second letter B = a boss (knob) on the back, N = no boss. Further letters describe the boss (kept raw).
Loaders: seals() -> one row per seal face with every attribute used in the job.
"""
import sys, os, re, io, contextlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
ROOT = '/home/claude/ivc'
OUT = f'{ROOT}/work_data/twins'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
T0 = time.time()
def log(tag, *a): print(f'[{tag} {time.time()-T0:6.1f}s]', *a, flush=True)

OPEN = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556'}


def text_kind(signs, v2):
    """Frame-v2 shape of a complete text. Priority order as listed."""
    x = signs.split('-'); c = v2.split('-') if v2 else []
    if len(c) != len(x): return 'unparsed'
    num = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
    core = c[:]
    front = False
    if core and core[0] == 'OPEN':
        front = True; core = core[1:]
        if core and core[0] == 'SLOT': core = core[1:]
    if front and not core: return 'front alone'
    # count line: numbers then a counted thing, nothing else after the front
    if core and core[-1] == 'THING' and all(k in num for k in core[:-1]) and len(core) >= 2:
        return 'count line'
    if front: return 'front formula'
    if len(x) == 3 and x[1] == '740' and x[2] == '090': return '[crest][jar][man]'
    if len(c) >= 2 and c[-1] == 'TITLE' and c[-2] == 'CLOSER': return 'name + closer + title'
    if c[-1] == 'CLOSER' and len(c) >= 2: return 'name + closer'
    if len(c) == 1 and c[0] in ('CLOSER', 'TITLE'): return 'closer alone'
    if c[-1] == 'TITLE': return 'name + title'
    if 'CLOSER' not in c and 'TITLE' not in c: return 'bare name'
    return 'other'


def seals():
    O = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str).fillna('')
    S = O[O.tier == 'seal'].copy()
    with contextlib.redirect_stdout(io.StringIO()):
        from sound_v4_common import d
    extra = d.set_index('id')[['symbol', 'boss', 'condition', 'preservation', 'complete', 'cult', 'excavation-idno', 'thickness(mm)', 'cross-section', 'period', 'phase']]
    extra.columns = ['symbol', 'boss', 'condition', 'preservation', 'cat_complete', 'cult', 'excav_id', 'thmm', 'xsec', 'period', 'phase']
    S = S.join(extra, on='face')
    S['n'] = S.n.astype(int)
    S['complete'] = (S.lost == '0') & (S.broken == 'False') & (S.signs != '')
    S['complete_wide'] = (S.lost == '0') & (S.signs != '') & (S.cat_complete != 'N')
    S['area_mm2'] = pd.to_numeric(S.hmm, errors='coerce') * pd.to_numeric(S.vmm, errors='coerce')
    S.loc[S.area_mm2 <= 0, 'area_mm2'] = np.nan
    S['depth'] = pd.to_numeric(S.depth_ft, errors='coerce')
    S['fmt'] = S.type.map(lambda t: {'SEAL:S': 'square', 'SEAL:R': 'rectangular', 'SEAL:C': 'round', 'SEAL:CY': 'cylinder'}.get(t, 'other'))
    S['pierced'] = S.boss.str[:1].map({'P': 'pierced', 'N': 'not pierced'}).fillna('')
    S['knob'] = S.boss.map(lambda b: 'boss' if len(b) >= 2 and b[1] == 'B' else ('no boss' if len(b) >= 2 and b[1] == 'N' else ''))
    # animal: catalogue symbol '' = no animal carved (inscription-only seal) -> 'none'; '-' = not recorded -> ''
    SP = {'Bull1': 'unicorn', 'Gaur': 'short-horned bull', 'Zebu': 'zebu', 'Elep': 'elephant', 'Rhin': 'rhinoceros',
          'Tigr': 'tiger', 'Buff': 'buffalo', 'Goat': 'goat', 'Bull': 'bull'}
    def anim(sym):
        sym = str(sym).strip()
        if sym in ('', 'None', 'nan'): return 'none'
        if sym in ('-', '?', 'Unknown'): return ''
        k = sym.split(':', 1)[0]
        return SP.get(k, k)
    S['animal'] = S.symbol.map(anim)
    S['stand5'] = [st if a == 'unicorn' and st in ('W', 'J', 'S', 'I', 'L') else '' for a, st in zip(S.animal, S.stand)]
    S['kind'] = [text_kind(s, v) if s else '' for s, v in zip(S.signs, S.v2)]
    S['holder'] = [f'{a}:{s}' if a else '' for a, s in zip(S.animal, S.stand)]
    S['first'] = S.signs.str.split('-').str[0]
    return S.reset_index(drop=True)


def crest_of(signs):
    """first sign of the name: first sign after an opener (+slot) that is not a number."""
    x = signs.split('-'); i = 0
    if x and x[0] in OPEN:
        i = 1
        if i < len(x) and x[i] in ('002', '060', '741', '742', '368', '365'): i += 1
    num = {'001', '002', '003', '004', '005', '016', '013', '017', '031', '032', '033', '034', '035', '036'}
    while i < len(x) and x[i] in num: i += 1
    return x[i] if i < len(x) else ''
