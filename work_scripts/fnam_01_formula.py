#!/usr/bin/env python3
"""fnam_01_formula.py -- Decode the Foreign Round-Seal Formula ([001][090], 091 front, M9902 & X-X reduplication).

Tests concrete West Asian / Gulf seal-legend models on the pooled foreign & Gulf-type corpus
(Lipi foreign_set + round_list including Dholavira 4247.1 + Mahadevan WA M98xx/M99xx + gulf2 plate readings,
strictly cross-linked so physical stones read in two catalogues are never double-counted):

  (1A) Cuneiform / Dilmun / Akkadian / Amorite logographic-determinative & relational calque:
       - Bimodal positional law of person signs: unpreceded ^[091 / 090 / 090-090 / X11] at text start
         (head-initial LU / LU.MES "man/men of X") vs. stroke-preceded [001/055][090/091/093] in the
         back/predicate slot ("[PN] + DIS-LU / 1-man / guild-man"), replacing home [740][090].
       - Strict interiority of 001 (DIS determinative / clause divider) on foreign round seals.
       - Segmentation coverage vs. 1,000 within-text shuffles and 1,000 length-matched home seal draws,
         plus held-out check on unseen Mahadevan new texts.

  (1B) Syllabic / Phonetic Repetition, Mahadevan Twin-Glyph Law (M9902 = 235-091-617 = Gadd no. 18),
       Rival Split & Multi-Language Onomastic Rescue Test:
       - Discovers that Mahadevan 1977 decomposes Lipi twin-glyphs into adjacent pairs (1-1 = 091 twin-men,
         245-245 = 617 twin-grid, 121-121 = 056 twin-dozen, 391-391 = 821, 328-328 = 701, 293-293 = 922),
         identifying M9902 (65-1-1-245-245) with G2-09 (Gadd 1932 no. 18 two-bull round seal) = 235-091-617!
       - Even after normalizing ALL twin-glyph decompositions across both Lipi and all 3,573 Mahadevan lines,
         true non-stroke, non-twin-glyph X-X reduplication (740-740 on 3889.1/M9901, X21-X21 on M9904,
         220-220 on M9905) is 25x-42x enriched abroad over both Lipi home (0.31%) and unseen Mahadevan new
         texts (0.63%)! And twin-men (091 / 090-090) sits on 13/38 (34.2%) Gulf round seals vs 0.26% home!
       - Rival explanation split: Sumerian-style Logographic Plural/Collective (LU-LU, GAN2-GAN2, E-E, MUL-MUL)
         vs. Pure Syllabic CV-CV Reduplication (calibrated on 918 Bronze Age CDLI texts).
       - Rescue redesign for stem alignment (after cross-stem sign-sharing came up null at 14 vs 18.53 because
         Gulf merchants lack Harappan house crests): direct multi-language acrophonic readout across 7 dictionaries
         (/tmp/dict_emb/ + values_master4) against the 28 attested CDLI Dilmun/Magan/Meluhha/Marhashi names vs.
         1,000 sound-shuffled lexicons.
"""
import os, sys, re, json, collections
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, binomtest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'work_scripts'))
OUT = os.path.join(ROOT, 'work_data', 'fnam')
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(20261117)

PERSON_SIGNS = {
    '070','071','072','073','090','091','093','094','095','097','098','099',
    '100','101','103','104','105','106','107','110','111','112','113','117',
    '118','119','121','122','123','125','126','127','130','131','132','133',
    '134','137','139','140','142','143','144','145','146','150','151','153',
    '154','155','156','157','158','159','160','161','176',
    'X11','X21','X29'
}
CORE_MAN_SIGNS = {'090', '091', '093', 'X11', 'X21'}
STROKE_COUNTS = {
    '001','002','003','004','005','006','007','012','013','014','015','016','017','018','019','020',
    '025','026','027','028','029','031','032','033','034','035','036','055','056'
}
DET_STROKES = {'001', '055'}
HOME_CLOSERS = {'740', '520', '400', '151', '153', '154', '156', '617', '621', '527'}

# Mahadevan's concordance decomposes Lipi's ligatured twin-glyphs into adjacent identical signs:
# Verified on M1084 (1-1-379-194 = Lipi 091-831-585), M8108 (1-1-121-121-... = Lipi 091-056-...),
# M1437 (25-245-245 = Lipi 142-617).
MAH_TWIN_COLLAPSE = {
    ('090', '090'): '091',
    ('615', '615'): '617',
    ('055', '055'): '056',
    ('820', '820'): '821',
    ('700', '700'): '701',
    ('920', '920'): '922',
    ('400', '400'): '401',
    ('X153', 'X153'): '521',
    ('832', '832'): '833',
}


def normalize_mah_twins(toks):
    """Collapse Mahadevan's decomposed twin-glyph pairs into Lipi single twin-glyph codes."""
    out = []
    i = 0
    while i < len(toks):
        if i + 1 < len(toks) and (toks[i], toks[i + 1]) in MAH_TWIN_COLLAPSE:
            out.append(MAH_TWIN_COLLAPSE[(toks[i], toks[i + 1])])
            i += 2
        else:
            out.append(toks[i])
            i += 1
    return out


def valid_tok(s):
    return bool(s) and s not in ('000', 'ALT', '?', '') and not s.startswith('?')


# ---------------------------------------------------------------------------
# 1. Build deduplicated Master Foreign & Gulf Corpus + Home Baselines
# ---------------------------------------------------------------------------
def build_corpora():
    fset = pd.read_csv(os.path.join(ROOT, 'work_data/abroad4/foreign_set.csv'), dtype=str).fillna('')
    rlist = pd.read_csv(os.path.join(ROOT, 'work_data/round/round_list.csv'), dtype=str).fillna('')
    g2 = pd.read_csv(os.path.join(ROOT, 'work_data/gulf2/sequences.csv'), dtype=str).fillna('')
    M = pd.read_csv(os.path.join(ROOT, 'work_data/mahadevan_parsed.csv'), dtype=str).fillna('')

    mah_restorations = {
        '3899.1': ('M9845a', '350-090-004-220-255'),
        '5222.1': ('M9852', '255-013-744-892-740'),
        '5224.1': ('M9903', '095-003-220-001-032-061-033'),
    }

    rows = []
    for _, r in fset[fset.tier.isin(['core', 'unk_round'])].iterrows():
        rest_id, rest_seq = mah_restorations.get(r.id, ('', ''))
        is_round = r['shape'] == 'round' or r['type'] in ('SEAL:C', 'SEAL:CY')
        rows.append(dict(
            uid=f'L:{r.id}', source='Lipi', orig_id=r.id, mah_partner=rest_id,
            site=r.site, region=r.region, kind=r.kind, shape='round' if is_round else r['shape'],
            animal=r.animal, complete=r.complete, seq_raw=r.text, seq_lipi_norm=r.text,
            seq_restored=rest_seq or r.text, gulf_pool=is_round, in_strict_cat=True
        ))

    dhol = rlist[rlist.id == '4247.1']
    if len(dhol):
        r = dhol.iloc[0]
        rows.append(dict(
            uid='L:4247.1', source='Lipi_home_Gulf_round', orig_id='4247.1', mah_partner='',
            site='Dholavira', region='Gujarat/Kutch (Gulf stamp)', kind='seal', shape='round',
            animal='SHORTHORN', complete='N', seq_raw=r.text, seq_lipi_norm=r.text,
            seq_restored=r.text, gulf_pool=True, in_strict_cat=True
        ))

    wa = M[M.site == 'WA'].copy()
    partnered_mah_keys = {
        ('9801', '173-10-97-121-185-97-297-57'),
        ('9811', '29-336-99-104-162'),
        ('9822', '173-403-123-102-59-249-162-342'),
        ('9832', '254-74-297-184-3'),
        ('9833', '0-1-0-157-97-0'),
        ('9845', '175-1-0-59-51'),
        ('9846', '171-387-97-341-107'),
        ('9852', '51-103-345-307-342'),
        ('9901', '178-53-97-342-342'),
        ('9903', '18-102-59-98-294-134-89'),
    }
    for _, r in wa.iterrows():
        if (r.textnum, r.reading_mah) in partnered_mah_keys:
            continue
        is_gulf_like = r.textnum.startswith('99')
        uid = f'M:{r.textnum}' + ('b' if r.textnum == '9845' else '')
        raw_toks = [t for t in r.reading_lipi.split('-') if t]
        norm_toks = normalize_mah_twins(raw_toks)
        rows.append(dict(
            uid=uid, source='Mahadevan_WA', orig_id=f'M{r.textnum}',
            mah_partner='G2-09 (Gadd 18)' if r.textnum == '9902' else '',
            site='West Asia (unprov. museum)' if r.textnum.startswith('99') else 'West Asia (excav.)',
            region='West Asia', kind='seal', shape='round_or_wa_museum' if is_gulf_like else 'wa_seal',
            animal='TWO_BULLS (Gadd 18)' if r.textnum == '9902' else '',
            complete='Y' if r.complete == 'True' else 'N',
            seq_raw=r.reading_lipi, seq_lipi_norm='-'.join(norm_toks),
            seq_restored='-'.join(norm_toks), gulf_pool=is_gulf_like, in_strict_cat=True
        ))

    for _, r in g2.iterrows():
        gid = r.gid
        if not gid.startswith('G2-') or gid.startswith('G2-D') or gid.startswith('G2-M'):
            continue
        if gid in ('G2-05', 'G2-09'):  # G2-05 pseudo-script; G2-09 = Gadd 1932 no. 18 = M9902
            continue
        seq = r.signs_best.strip()
        if not seq:
            continue
        is_round = ('round' in r.object) or ('cylinder' in r.object)
        is_comp = 'broken' not in r.object and 'broken' not in r.flag
        raw_toks = [t for t in seq.split('-') if t]
        # Note: on G2 plates, two men side-by-side were keyed 090-090 when slightly spaced, 091 when close;
        # seq_lipi_norm normalizes 090-090 -> 091 while seq_raw keeps exact plate tokens!
        norm_toks = normalize_mah_twins(raw_toks)
        rows.append(dict(
            uid=gid, source='gulf2_plate', orig_id=gid, mah_partner='',
            site=r.find_place, region=r.region, kind='seal', shape='round' if is_round else r.object,
            animal=r.animal, complete='Y' if is_comp else 'N',
            seq_raw=seq, seq_lipi_norm='-'.join(norm_toks), seq_restored='-'.join(norm_toks),
            gulf_pool=is_round, in_strict_cat=False
        ))

    df = pd.DataFrame(rows)
    df['tokens_raw'] = df.seq_raw.apply(lambda s: [t for t in s.split('-') if t])
    df['tokens'] = df.seq_lipi_norm.apply(lambda s: [t for t in s.split('-') if t])
    df['n_tok'] = df.tokens.apply(len)
    df['n_tok_raw'] = df.tokens_raw.apply(len)
    df.to_csv(os.path.join(OUT, 'foreign_corpus.csv'), index=False)

    with open(os.path.join(ROOT, 'work_data/sense/events_lipi.json')) as f:
        evL = json.load(f)
    with open(os.path.join(ROOT, 'work_data/sense/events_new.json')) as f:
        evN = json.load(f)

    abroad_sites = set(fset[fset.tier == 'core'].site.unique()) | {'abroad', 'Unknown'}
    home_distinct, home_seals_distinct = {}, {}
    for e in evL:
        if e['site'] in abroad_sites:
            continue
        for face in e['faces']:
            if e['site'] == 'Dholavira' and face == ['000', '255', '368', '001', '091', '806']:
                continue
            tup = tuple(face)
            if tup and tup not in home_distinct:
                home_distinct[tup] = e
            if e['kind'] == 'seal' and tup and tup not in home_seals_distinct:
                home_seals_distinct[tup] = e

    # Normalize Mahadevan twin-glyph splits on unseen new texts so Lipi and Mahadevan are on the EXACT same sign granularity!
    new_distinct_norm = {}
    for e in evN:
        if e['site'] in abroad_sites:
            continue
        for face in e['faces']:
            tup = tuple(normalize_mah_twins(face))
            if tup and tup not in new_distinct_norm:
                new_distinct_norm[tup] = e

    return df, list(home_distinct.keys()), list(home_seals_distinct.keys()), list(new_distinct_norm.keys())


# ---------------------------------------------------------------------------
# 2. Test 1A: Cuneiform Determinative / Relational Calque & Bimodal Law
# ---------------------------------------------------------------------------
def segment_gulf_seal(toks):
    L = len(toks)
    if L == 0:
        return 'empty', [], False
    sp_idx = [i for i in range(L - 1) if toks[i] in DET_STROKES and toks[i + 1] in CORE_MAN_SIGNS]
    head_init = toks[0] in CORE_MAN_SIGNS
    head_len = 2 if (head_init and L >= 2 and toks[1] == toks[0]) else (1 if head_init else 0)

    if head_len > 0 and not sp_idx:
        div = [i for i in range(head_len + 1, L - 1) if toks[i] == '001']
        if div:
            d = div[0]
            segs = [('REL_HEAD', toks[:head_len]), ('STEM_1', toks[head_len:d]),
                    ('DET_DIV', [toks[d]]), ('STEM_2', toks[d + 1:])]
            return 'head_initial_bipartite', segs, True
        segs = [('REL_HEAD', toks[:head_len])]
        if head_len < L:
            segs.append(('GENITIVE_NAME', toks[head_len:]))
        return 'head_initial_LU', segs, True

    if sp_idx:
        i = sp_idx[0]
        segs = []
        if head_len > 0 and head_len <= i:
            segs.append(('REL_HEAD', toks[:head_len]))
            if head_len < i:
                segs.append(('STEM_1', toks[head_len:i]))
        elif i > 0:
            segs.append(('STEM_1', toks[:i]))
        segs.append(('DET_MAN', toks[i:i + 2]))
        if i + 2 < L:
            segs.append(('STEM_2_OR_TITLE', toks[i + 2:]))
        return 'stroke_man_calque', segs, (i > 0)

    div = [i for i in range(1, L - 1) if toks[i] == '001']
    if div:
        d = div[0]
        segs = [('STEM_1', toks[:d]), ('DET_DIV', ['001']), ('STEM_2', toks[d + 1:])]
        return 'disz_bipartite', segs, True

    # Medial twin-man [X][091 / X21-X21][Y] (e.g. M9902=235-091-617, G2-04, G2-11, M9904)
    mm2 = [i for i in range(1, L - 1) if toks[i] in CORE_MAN_SIGNS and i + 1 < L and toks[i + 1] == toks[i]]
    if mm2:
        m = mm2[0]
        segs = [('STEM_1', toks[:m]), ('PLURAL_LU_LU', toks[m:m + 2])]
        if m + 2 < L:
            segs.append(('STEM_2', toks[m + 2:]))
        return 'medial_plural_LU_LU', segs, True

    mm1 = [i for i in range(1, L - 1) if toks[i] == '091']
    if mm1:
        m = mm1[0]
        segs = [('STEM_1', toks[:m]), ('PLURAL_LU_LU', ['091']), ('STEM_2', toks[m + 1:])]
        return 'medial_plural_LU_LU', segs, True

    if toks[-1] in HOME_CLOSERS:
        return 'home_closer', [('STEM', toks[:-1]), ('CLOSER', [toks[-1]])], True

    return 'unsegmented_other', [('RAW', toks)], False


def run_test_1a(df, home_distinct, home_seals, new_distinct):
    gulf = df[(df.gulf_pool) & (df.n_tok >= 2)].copy()
    tok_lists = list(gulf.tokens)

    def count_sp_texts(seqs):
        return sum(1 for ts in seqs if any(ts[i] in DET_STROKES and ts[i + 1] in CORE_MAN_SIGNS for i in range(len(ts) - 1)))

    obs_sp = count_sp_texts(tok_lists)
    shuf_sp = np.array([count_sp_texts([list(rng.permutation(ts)) for ts in tok_lists]) for _ in range(1000)])
    p_sp_shuf = (1 + np.sum(shuf_sp >= obs_sp)) / 1001.0

    home_sp = count_sp_texts([ts for ts in home_distinct if len(ts) >= 2])
    home_n2 = sum(1 for ts in home_distinct if len(ts) >= 2)
    new_sp = count_sp_texts([ts for ts in new_distinct if len(ts) >= 2])
    new_n2 = sum(1 for ts in new_distinct if len(ts) >= 2)
    _, p_sp_home = fisher_exact([[obs_sp, len(tok_lists) - obs_sp], [home_sp, home_n2 - home_sp]], alternative='greater')
    _, p_sp_new = fisher_exact([[obs_sp, len(tok_lists) - obs_sp], [new_sp, new_n2 - new_sp]], alternative='greater')

    def bimodal_gap(seqs):
        unprec_pos, prec_pos, unprec_init = [], [], []
        for ts in seqs:
            L = len(ts)
            if L < 2:
                continue
            for i, t in enumerate(ts):
                if t in CORE_MAN_SIGNS:
                    if i > 0 and ts[i - 1] == t:
                        continue
                    npos = i / (L - 1)
                    if i > 0 and ts[i - 1] in DET_STROKES:
                        prec_pos.append(npos)
                    else:
                        unprec_pos.append(npos)
                        unprec_init.append(1 if i == 0 else 0)
        gap = (np.mean(prec_pos) - np.mean(unprec_pos)) if (prec_pos and unprec_pos) else 0.0
        init_rate = np.mean(unprec_init) if unprec_init else 0.0
        return gap, init_rate, unprec_pos, prec_pos, sum(unprec_init), len(unprec_init)

    obs_gap, obs_init_rate, unprec_pos, prec_pos, k_init, n_unprec = bimodal_gap(tok_lists)
    shuf_gaps, shuf_inits = [], []
    for _ in range(1000):
        s_seqs = [list(rng.permutation(ts)) for ts in tok_lists]
        g, ir, _, _, _, _ = bimodal_gap(s_seqs)
        shuf_gaps.append(g)
        shuf_inits.append(ir)
    shuf_gaps, shuf_inits = np.array(shuf_gaps), np.array(shuf_inits)
    p_gap = (1 + np.sum(shuf_gaps >= obs_gap)) / 1001.0
    p_init = (1 + np.sum(shuf_inits >= obs_init_rate)) / 1001.0

    def interior_001(seqs):
        tot, inter = 0, 0
        for ts in seqs:
            clean = [t for t in ts if t != '000']
            L = len(clean)
            if L < 3:
                continue
            for i, t in enumerate(clean):
                if t == '001':
                    tot += 1
                    if 0 < i < L - 1:
                        inter += 1
        return inter, tot

    obs_int001, tot_001 = interior_001(tok_lists)
    shuf_int001 = np.array([
        interior_001([list(rng.permutation([t for t in ts if t != '000'])) for ts in tok_lists])[0]
        for _ in range(1000)
    ])
    p_int001 = (1 + np.sum(shuf_int001 >= obs_int001)) / 1001.0

    seg_rows = []
    for _, r in gulf.iterrows():
        mtype, segs, ok = segment_gulf_seal(r.tokens)
        is_gulf_calque = mtype in ('head_initial_LU', 'head_initial_bipartite', 'stroke_man_calque', 'disz_bipartite', 'medial_plural_LU_LU')
        seg_str = ' | '.join(f"{k}:{'-'.join(v)}" for k, v in segs)
        seg_rows.append(dict(uid=r.uid, site=r.site, shape=r['shape'], seq_raw=r.seq_raw, seq_norm=r.seq_lipi_norm,
                             formula_type=mtype, gulf_calque=is_gulf_calque, segmented=seg_str))
    pd.DataFrame(seg_rows).to_csv(os.path.join(OUT, 'formula_segmentation.csv'), index=False)

    def calque_count(seqs):
        return sum(
            1 for ts in seqs
            if segment_gulf_seal(ts)[2] and segment_gulf_seal(ts)[0] in (
                'head_initial_LU', 'head_initial_bipartite', 'stroke_man_calque', 'disz_bipartite', 'medial_plural_LU_LU'
            )
        )

    obs_calque = calque_count(tok_lists)
    shuf_calque = np.array([calque_count([list(rng.permutation(ts)) for ts in tok_lists]) for _ in range(1000)])
    p_calque_shuf = (1 + np.sum(shuf_calque >= obs_calque)) / 1001.0

    by_len = collections.defaultdict(list)
    for ts in home_seals:
        if len(ts) >= 2:
            by_len[len(ts)].append(list(ts))
    home_draw_calque = []
    for _ in range(1000):
        sample = [(by_len.get(len(ts)) or by_len.get(len(ts) - 1) or by_len[4])[rng.integers(len(by_len.get(len(ts)) or by_len.get(len(ts) - 1) or by_len[4]))] for ts in tok_lists]
        home_draw_calque.append(calque_count(sample))
    home_draw_calque = np.array(home_draw_calque)
    p_calque_home = (1 + np.sum(home_draw_calque >= obs_calque)) / 1001.0

    # Held-out unseen Mahadevan new texts length-matched draws
    by_len_new = collections.defaultdict(list)
    for ts in new_distinct:
        if len(ts) >= 2:
            by_len_new[len(ts)].append(list(ts))
    new_draw_calque = []
    for _ in range(1000):
        sample = [(by_len_new.get(len(ts)) or by_len_new.get(len(ts) - 1) or by_len_new[4])[rng.integers(len(by_len_new.get(len(ts)) or by_len_new.get(len(ts) - 1) or by_len_new[4]))] for ts in tok_lists]
        new_draw_calque.append(calque_count(sample))
    new_draw_calque = np.array(new_draw_calque)

    stats = [
        dict(metric='stroke_man_unit_texts', real=obs_sp, n_texts=len(tok_lists),
             ctrl_shuf_mean=round(float(shuf_sp.mean()), 2), p_shuf=p_sp_shuf,
             home_obs=f'{home_sp}/{home_n2}', p_vs_home=p_sp_home,
             new_texts_obs=f'{new_sp}/{new_n2} (P={p_sp_new:.2e})'),
        dict(metric='unpreceded_man_initial_rate', real=round(obs_init_rate, 4), n_texts=f'{k_init}/{n_unprec}',
             ctrl_shuf_mean=round(float(shuf_inits.mean()), 4), p_shuf=p_init,
             home_obs='n/a', p_vs_home=np.nan, new_texts_obs='n/a'),
        dict(metric='bimodal_man_pos_gap_prec_minus_unprec', real=round(obs_gap, 4),
             n_texts=f'prec={len(prec_pos)},unprec={len(unprec_pos)}',
             ctrl_shuf_mean=round(float(shuf_gaps.mean()), 4), p_shuf=p_gap,
             home_obs=f'prec_mean={np.mean(prec_pos):.3f},unprec_mean={np.mean(unprec_pos):.3f}',
             p_vs_home=np.nan, new_texts_obs='n/a'),
        dict(metric='interior_001_divider_count', real=obs_int001, n_texts=tot_001,
             ctrl_shuf_mean=round(float(shuf_int001.mean()), 2), p_shuf=p_int001,
             home_obs='strictly interior 100%', p_vs_home=np.nan, new_texts_obs='n/a'),
        dict(metric='gulf_calque_segmented_texts', real=obs_calque, n_texts=len(tok_lists),
             ctrl_shuf_mean=round(float(shuf_calque.mean()), 2), p_shuf=p_calque_shuf,
             home_obs=f'len-matched mean {home_draw_calque.mean():.2f}/{len(tok_lists)}',
             p_vs_home=p_calque_home,
             new_texts_obs=f'len-matched new mean {new_draw_calque.mean():.2f}/{len(tok_lists)}'),
    ]
    pd.DataFrame(stats).to_csv(os.path.join(OUT, 'formula_stats.csv'), index=False)
    return stats, seg_rows


# ---------------------------------------------------------------------------
# 3. Test 1B: Reduplication, Twin-Men (091/1-1), Rival Split & Multi-Language Rescue
# ---------------------------------------------------------------------------
def has_nonstroke_xx(ts):
    return [ts[i] for i in range(len(ts) - 1) if valid_tok(ts[i]) and ts[i] == ts[i + 1] and ts[i] not in STROKE_COUNTS]


def extract_cdli_bronze_names():
    attested_east = [
        ('Rimum', 'ri-mu-um', 'rmm', 'PN', 'Dilmun/Bahrain', 'P507624 {disz}ri-mu-um ARAD2 {d}in-za-ak sza2 a-ka3-rum'),
        ('Yagli-El', 'ia-ag-li-il', 'ygll', 'PN', 'Dilmun/Bahrain', 'P507617 {disz}ia-ag-li-il3 dumu ri-mi-um ARAD2 {d}in-za-ak'),
        ('Sumu-lel', 'su-mu-la-il', 'smll', 'PN', 'Dilmun/Bahrain', 'Dilmun ruler, servant of Inzak of Agarum'),
        ('Inzak', 'in-za-ak', 'nzk', 'DN', 'Dilmun/Failaka', 'P507624 {d}in-za-ak, tutelary god of Dilmun/Agarum'),
        ('Meskilak', 'mes-ki-la-ak', 'msklk', 'DN', 'Dilmun/Failaka', 'Consort/co-deity of Inzak in Dilmun & Failaka'),
        ('Agarum', 'a-ka-rum', 'krm', 'GN', 'Dilmun/Bahrain', 'P507624 sza2 a-ka3-rum (Agarum)'),
        ('Tilmun', 'ti-il-mun', 'tlmn', 'GN', 'Persian Gulf', 'dilmun{ki} / til-mun{ki}'),
        ('Nituk', 'ni-tuk', 'ntk', 'GN', 'Persian Gulf', 'P511663 Failaka seal NI.TUK = Dilmun'),
        ('Makkan', 'ma-ak-kan', 'mkn', 'GN', 'Oman/Makran', 'ma2-gan{ki} (P108701 etc.)'),
        ('Meluhha', 'me-luh-ha', 'mlh', 'GN', 'Indus', 'me-luh-ha{ki} (P212982, P525331, etc.)'),
        ('Marhashi', 'mar-ha-szi', 'mrhs', 'GN', 'SE Iran', 'mar-ha-szi{ki} (P315657 etc.)'),
        ('Shu-ilishu', 'szu-i-li-su', 'sls', 'PN', 'Meluhha_interp', 'P525331 szu-i3-li2-su eme-bal me-luh-ha{ki}'),
        ('Ur-Lamma', 'ur-lam-ma', 'rlm', 'PN', 'Meluhha_son', 'P108448 ur-{d}lamma dumu me-luh-ha'),
        ('Ur-Igalim', 'ur-ig-a-lim', 'rglm', 'PN', 'Meluhha_son', 'P124739 ur-{d}ig-alim dumu me-luh-ha'),
        ('Lu-sunzida', 'lu-sun-zi-da', 'lsnzd', 'PN', 'Meluhha_man', 'P212982 lu2-sun2-zi-da lu2 me-luh-ha-ke4'),
        ('Lu-marza', 'lu-mar-za', 'lmrz', 'PN', 'Meluhha_son', 'P467759 lu2-mar-za dumu me-luh-ha'),
        ('Samar', 'sa-ma-ar', 'smr', 'PN', 'Meluhha_man', 'P516138 sa6-ma-ar ... i3-ba lu2 me-luh-ha{ki}-me'),
        ('Aliahhi', 'a-li-a-hi', 'lh', 'PN', 'Meluhha_wife', 'P516138 a-li-a-hi dam-a-ni ... lu2 me-luh-ha{ki}-me'),
        ('Dadi', 'da-di', 'dd', 'PN', 'Meluhha_boat', 'P212842 da-di3 lu2-tukul ma2 me-luh-ha-ka'),
        ('Inusadu', 'i-nu-sa-du', 'nsd', 'PN', 'Meluhha_boat', 'P212842 i-nu-sa-du2 (Meluhha boat tablet)'),
        ('Wedum', 'we-du-um', 'wdm', 'PN', 'Magan_envoy', 'P108701 we-du-um lu2 kin-gi4-a na-du-be-li2 ensi2 ma2-gan{ki}'),
        ('Nadubeli', 'na-du-be-li', 'ndbl', 'PN', 'Magan_ruler', 'P108701 na-du-be-li2 ensi2 ma2-gan{ki}'),
        ('Zuhar', 'zu-ha-ar', 'zhr', 'PN', 'Marhashi_ctx', 'P315657 lu2 mar-ha-szi{ki} / zu-ha-ar / i3-du-du'),
        ('Idudu', 'i-du-du', 'dd', 'PN', 'Marhashi_ctx', 'P315657 i3-du-du alongside lu2 mar-ha-szi{ki}'),
        ('Dudu', 'du-du', 'dd', 'PN', 'Girsu_Meluhha_ctx', 'P108448 ur-e2-ninnu dumu du-du'),
        ('Dada', 'da-da', 'dd', 'PN', 'Meluhha_ctx', 'P454137 lu2 me-luh-ha-me / da-da i3-du8'),
        ('Enki', 'en-ki', 'nk', 'DN', 'Mesopotamia/Dilmun', 'Lord of Abzu & Dilmun'),
        ('Suen', 'su-en', 'sn', 'DN', 'Ur/Failaka', 'P511661 {d}zu-en Failaka seal'),
    ]
    xx_sylls = collections.Counter()
    for fn in ('work_data/abroad3/cdli_east_atf.jsonl', 'work_data/abroad2/cdli_meluhha_atf.jsonl'):
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                obj = json.loads(line)
                per = obj.get('period') or ''
                if any(k in per for k in ('Neo-', 'Middle ', 'Hellenistic', 'Achaemenid')):
                    continue
                atf = obj.get('atf') or ''
                for ln in atf.splitlines():
                    if not ln or ln[0] in ('&', '#', '@', '$', '>'):
                        continue
                    for w in ln.split():
                        w_clean = re.sub(r'\{[^}]+\}|\[|\]|#|\?|\!|<|>', '', w)
                        parts = [re.sub(r'\d+$', '', s.lower()) for s in w_clean.split('-') if re.match(r'^[a-z]{1,4}\d*$', s, re.I)]
                        for i in range(len(parts) - 1):
                            if parts[i] == parts[i + 1] and len(parts[i]) >= 2:
                                xx_sylls[parts[i]] += 1
    cdf = pd.DataFrame(attested_east, columns=['name', 'syllables', 'skel', 'category', 'circuit', 'source'])
    cdf.to_csv(os.path.join(OUT, 'cdli_names.csv'), index=False)
    return cdf, xx_sylls


def normalize_skel(s):
    s = s.lower()
    s = re.sub(r'[āăáà]', 'a', s)
    s = re.sub(r'[īĭíì]', 'i', s)
    s = re.sub(r'[ūŭúù]', 'u', s)
    s = re.sub(r'[ēĕéè]', 'e', s)
    s = re.sub(r'[ōŏóò]', 'o', s)
    s = re.sub(r'[ṭṯ]', 't', s)
    s = re.sub(r'[ḍḏ]', 'd', s)
    s = re.sub(r'[ṇṉṅñ]', 'n', s)
    s = re.sub(r'[ḷḻṛṟ]', 'l', s)
    s = re.sub(r'[śṣš]', 's', s)
    s = re.sub(r'[ḫḥ]', 'h', s)
    s = re.sub(r'[ġ]', 'g', s)
    s = re.sub(r'[^a-z]', '', s)
    cons = re.sub(r'[aeiouy]', '', s)
    # Collapse geminates for coarse skeleton
    out = []
    for ch in cons:
        if not out or out[-1] != ch:
            out.append(ch)
    return ''.join(out)


def run_rescue_acrophonic_onomastics(gulf_stems, cdf):
    """RESCUE REDESIGN FOR 1B: Since Gulf stems do not share Harappan house crests with each other
    (14 shared-sign edges vs 18.53 at home), test direct multi-language acrophonic/word readout!
    For each candidate dictionary in /tmp/dict_emb/ (+ values_master4), map each pictured sign in the
    22 Gulf name-stems to its primary onset consonant (acrophony) from the dictionary's words for that
    sign's blind picture noun, form 2-3 consonant skeletons for the Gulf stems, and count exact matches
    to the 28 attested CDLI East PNs/DNs/GNs vs. 1,000 dictionary-sound shuffles!
    """
    signs_df = pd.read_csv(os.path.join(ROOT, 'work_data/lang_m2/signs.csv'), dtype=str).fillna('')
    sign_nouns = {r.sign: [w.strip() for w in r.nouns.split(';') if w.strip()] for _, r in signs_df.iterrows() if r.nouns}
    # Supplement from sign_shapes.csv for Gulf-occurring signs missing in lang_m2
    extra_nouns = {
        '160': ['man', 'carry'], '190': ['spider', 'crab', 'insect'], '220': ['fish'],
        '255': ['fish', 'animal'], '340': ['deer', 'antelope', 'gazelle'], '350': ['comb', 'sprout', 'branch'],
        '384': ['heart', 'leaf'], '413': ['branch', 'stalk', 'tree'], '415': ['fork', 'branch', 'horn'],
        '455': ['triangle', 'mountain', 'hill'], '467': ['house', 'roof'], '528': ['box', 'square', 'cross'],
        '550': ['gate', 'door', 'tongs'], '617': ['field', 'grid', 'square'], '716': ['paw', 'hand', 'claw'],
        '740': ['jar', 'pot', 'vessel'], '803': ['leaf', 'tree'], '831': ['leaf', 'seed'], '840': ['leaf', 'two'],
    }
    for k, v in extra_nouns.items():
        if k not in sign_nouns or not sign_nouns[k]:
            sign_nouns[k] = v

    with open('/tmp/dict_emb/phrases.json') as f:
        phrases = json.load(f)['phrases']
    phrase_words = {i: set(re.findall(r'[a-z]+', p.lower())) for i, p in enumerate(phrases)}

    target_skels = {normalize_skel(s) for s in cdf.skel if len(normalize_skel(s)) >= 2}

    dicts_to_test = [
        ('Dravidian_DEDR_Tamil', '/tmp/dict_emb/dedr_tamil.csv'),
        ('IndoAryan_OIA_Turner', '/tmp/dict_emb/oia_turner.csv'),
        ('Munda_Santali_Campbell', '/tmp/dict_emb/santali_campbell.csv'),
        ('Elamite_HinzKoch', '/tmp/dict_emb/elamite_hinzkoch.csv'),
        ('Sumerian_Halloran', '/tmp/dict_emb/sumerian_halloran.csv'),
        ('Akkadian_Wiktionary', '/tmp/dict_emb/akkadian_wiktionary.csv'),
    ]

    needed_signs = sorted({s for _, _, _, st in gulf_stems for s in st if s in sign_nouns})
    rescue_rows = []

    for label, dpath in dicts_to_test:
        ddf = pd.read_csv(dpath, dtype=str).fillna('')
        # Precompute word -> list of entry indices
        kw_to_skels = collections.defaultdict(list)
        all_entry_onsets = []
        for sk, p1 in zip(ddf.skel, ddf.p1_id):
            csk = normalize_skel(sk)
            if not csk:
                continue
            onset = csk[0]
            all_entry_onsets.append(onset)
            pid = int(p1) if p1.isdigit() else -1
            if 0 <= pid < len(phrases):
                for w in phrase_words[pid]:
                    kw_to_skels[w].append(onset)

        # Sign -> set of top-3 commonest onset consonants among matching dictionary entries
        sign_onsets = {}
        sign_n_cand = {}
        for s in needed_signs:
            cands = []
            for kw in sign_nouns[s]:
                cands.extend(kw_to_skels.get(kw, []))
            if cands:
                top_c = [c for c, _ in collections.Counter(cands).most_common(3)]
                sign_onsets[s] = top_c
                sign_n_cand[s] = len(cands)

        def score_map(s_map):
            hits = 0
            matched_examples = []
            for uid, site, role, st in gulf_stems:
                if not all(x in s_map for x in st):
                    continue
                # Generate Cartesian product of top-3 acrophonic onsets
                pools = [s_map[x] for x in st]
                cur_combos = ['']
                for pl in pools:
                    cur_combos = [a + b for a in cur_combos for b in pl]
                norm_combos = {normalize_skel(c) for c in cur_combos if len(normalize_skel(c)) >= 2}
                ov = norm_combos & target_skels
                if ov:
                    hits += 1
                    matched_examples.append(f"{uid}:{'-'.join(st)}->{sorted(ov)[0]}")
            return hits, matched_examples

        real_hits, real_ex = score_map(sign_onsets)
        testable = sum(1 for _, _, _, st in gulf_stems if all(x in sign_onsets for x in st))

        # 1,000 sound-shuffled controls: draw same number of dictionary entries at random per sign, take top-3 onsets
        all_entry_onsets_arr = np.array(all_entry_onsets)
        ctrl_hits = []
        for _ in range(1000):
            shuf_map = {}
            for s, nc in sign_n_cand.items():
                drawn = all_entry_onsets_arr[rng.integers(0, len(all_entry_onsets_arr), size=nc)]
                shuf_map[s] = [str(c) for c, _ in collections.Counter(drawn).most_common(3)]
            h, _ = score_map(shuf_map)
            ctrl_hits.append(h)
        ctrl_hits = np.array(ctrl_hits)
        p_val = (1 + np.sum(ctrl_hits >= real_hits)) / 1001.0
        z = (real_hits - ctrl_hits.mean()) / (ctrl_hits.std() + 1e-9)

        rescue_rows.append(dict(
            language=label, testable_stems=testable, real_hits=real_hits,
            ctrl_mean=round(float(ctrl_hits.mean()), 2), ctrl_sd=round(float(ctrl_hits.std()), 2),
            z_score=round(float(z), 2), p_shuf=round(float(p_val), 4),
            sample_matches='; '.join(real_ex[:5])
        ))

    # Also test repository's values_master4.csv directly!
    vm4 = pd.read_csv(os.path.join(ROOT, 'work_data/values_master4.csv'), dtype=str).fillna('')
    vm_onsets = {}
    for _, r in vm4.iterrows():
        csk = normalize_skel(r.sound)
        if csk:
            vm_onsets[r.sign] = [csk[0], csk[:2]]
    vm_pool = list(vm_onsets.values())
    vm_testable = [st for _, _, _, st in gulf_stems if all(x in vm_onsets for x in st)]
    vm_hits = 0
    vm_ex = []
    for uid, site, role, st in gulf_stems:
        if not all(x in vm_onsets for x in st):
            continue
        cur = ['']
        for x in st:
            cur = [a + b for a in cur for b in vm_onsets[x]]
        ov = {normalize_skel(c) for c in cur if len(normalize_skel(c)) >= 2} & target_skels
        if ov:
            vm_hits += 1
            vm_ex.append(f"{uid}:{'-'.join(st)}->{sorted(ov)[0]}")
    vm_ctrl = []
    vm_keys = list(vm_onsets.keys())
    for _ in range(1000):
        perm_vals = [vm_pool[i] for i in rng.permutation(len(vm_pool))]
        smap = dict(zip(vm_keys, perm_vals))
        h = 0
        for _, _, _, st in gulf_stems:
            if not all(x in smap for x in st):
                continue
            cur = ['']
            for x in st:
                cur = [a + b for a in cur for b in smap[x]]
            if {normalize_skel(c) for c in cur if len(normalize_skel(c)) >= 2} & target_skels:
                h += 1
        vm_ctrl.append(h)
    vm_ctrl = np.array(vm_ctrl)
    rescue_rows.append(dict(
        language='Repo_Dravidian_values_master4', testable_stems=len(vm_testable), real_hits=vm_hits,
        ctrl_mean=round(float(vm_ctrl.mean()), 2), ctrl_sd=round(float(vm_ctrl.std()), 2),
        z_score=round(float((vm_hits - vm_ctrl.mean()) / (vm_ctrl.std() + 1e-9)), 2),
        p_shuf=round(float((1 + np.sum(vm_ctrl >= vm_hits)) / 1001.0), 4),
        sample_matches='; '.join(vm_ex[:5])
    ))

    pd.DataFrame(rescue_rows).to_csv(os.path.join(OUT, 'onomastic_acrophonic_rescue.csv'), index=False)
    return rescue_rows


def run_test_1b(df, home_distinct, home_seals, new_distinct):
    cdf, cdli_xx_sylls = extract_cdli_bronze_names()

    strict_for = df[(df.in_strict_cat) & (df.n_tok >= 2)].copy()
    pooled_for = df[df.n_tok >= 2].copy()
    gulf_only = df[(df.gulf_pool) & (df.n_tok >= 2)].copy()

    home_n2 = [ts for ts in home_distinct if len(ts) >= 2]
    new_n2 = [ts for ts in new_distinct if len(ts) >= 2]

    # Measure BOTH:
    # (i) Twin-men presence (091 in Lipi-normalized tokens, which includes 1-1 / 090-090!)
    # (ii) True non-stroke, non-twin-ligature X-X reduplication (on Lipi-normalized tokens!)
    # (iii) Raw surface non-stroke X-X reduplication (including 090-090 and 615-615 before twin collapse)
    def count_091(seqs):
        return sum(1 for ts in seqs if '091' in ts)

    k091_gulf = count_091(list(gulf_only.tokens))
    k091_home = count_091(home_n2)
    k091_new = count_091(new_n2)
    _, p091_home = fisher_exact([[k091_gulf, len(gulf_only) - k091_gulf], [k091_home, len(home_n2) - k091_home]], alternative='greater')
    _, p091_new = fisher_exact([[k091_gulf, len(gulf_only) - k091_gulf], [k091_new, len(new_n2) - k091_new]], alternative='greater')

    def eval_xx(seqs):
        pos = [(ts, has_nonstroke_xx(ts)) for ts in seqs]
        pos = [(ts, ps) for ts, ps in pos if ps]
        return len(pos), len(seqs), pos

    # Normalized (twin-glyphs collapsed in both Lipi, Mahadevan WA, G2, and New Texts!)
    k_strict, n_strict, pos_strict = eval_xx(list(strict_for.tokens))
    k_gulf, n_gulf, pos_gulf = eval_xx(list(gulf_only.tokens))
    k_home, n_home, pos_home = eval_xx(home_n2)
    k_new, n_new, pos_new = eval_xx(new_n2)

    # Raw surface X-X (before collapsing 090-090/615-615 on G2 and M9902)
    k_raw_pool, n_raw_pool, pos_raw_pool = eval_xx(list(pooled_for.tokens_raw))

    _, p_strict_vs_home = fisher_exact([[k_strict, n_strict - k_strict], [k_home, n_home - k_home]], alternative='greater')
    _, p_strict_vs_new = fisher_exact([[k_strict, n_strict - k_strict], [k_new, n_new - k_new]], alternative='greater')
    _, p_gulf_vs_home = fisher_exact([[k_gulf, n_gulf - k_gulf], [k_home, n_home - k_home]], alternative='greater')
    _, p_gulf_vs_new = fisher_exact([[k_gulf, n_gulf - k_gulf], [k_new, n_new - k_new]], alternative='greater')
    _, p_raw_vs_home = fisher_exact([[k_raw_pool, n_raw_pool - k_raw_pool], [k_home, n_home - k_home]], alternative='greater')

    redup_rows = [
        dict(metric='Twin_men_091_or_090x2 (Gulf round pool)', k=k091_gulf, n=len(gulf_only),
             rate=round(k091_gulf / len(gulf_only), 4),
             home_obs=f'{k091_home}/{len(home_n2)} ({k091_home/len(home_n2)*100:.2f}%)',
             vs_home_ratio=round((k091_gulf / len(gulf_only)) / (k091_home / len(home_n2)), 1),
             p_vs_home=p091_home,
             new_obs=f'{k091_new}/{len(new_n2)} ({k091_new/len(new_n2)*100:.2f}%)',
             p_vs_new=p091_new,
             examples='2153.1,3887.1,4247.1,5227.1,5228.1,5229.1,M9902(=G2-09),G2-02,G2-04,G2-07,G2-11,G2-14 (plus 1-sign 5551.1,G2-01)'),
        dict(metric='True_nonstroke_XX_after_twin_collapse (Strict Foreign)', k=k_strict, n=n_strict,
             rate=round(k_strict / n_strict, 4),
             home_obs=f'{k_home}/{n_home} ({k_home/n_home*100:.2f}%)',
             vs_home_ratio=round((k_strict / n_strict) / (k_home / n_home), 1),
             p_vs_home=p_strict_vs_home,
             new_obs=f'{k_new}/{n_new} ({k_new/n_new*100:.2f}%)',
             p_vs_new=p_strict_vs_new,
             examples='; '.join(f"{'-'.join(ts)} ({','.join(ps)})" for ts, ps in pos_strict)),
        dict(metric='True_nonstroke_XX_after_twin_collapse (Gulf Pool)', k=k_gulf, n=n_gulf,
             rate=round(k_gulf / n_gulf, 4),
             home_obs=f'{k_home}/{n_home} ({k_home/n_home*100:.2f}%)',
             vs_home_ratio=round((k_gulf / n_gulf) / (k_home / n_home), 1),
             p_vs_home=p_gulf_vs_home,
             new_obs=f'{k_new}/{n_new} ({k_new/n_new*100:.2f}%)',
             p_vs_new=p_gulf_vs_new,
             examples='; '.join(f"{'-'.join(ts)} ({','.join(ps)})" for ts, ps in pos_gulf)),
        dict(metric='Surface_nonstroke_XX_raw (Pooled Foreign)', k=k_raw_pool, n=n_raw_pool,
             rate=round(k_raw_pool / n_raw_pool, 4),
             home_obs=f'{k_home}/{n_home} ({k_home/n_home*100:.2f}%)',
             vs_home_ratio=round((k_raw_pool / n_raw_pool) / (k_home / n_home), 1),
             p_vs_home=p_raw_vs_home,
             new_obs='n/a (raw M splits twins)', p_vs_new=np.nan,
             examples='; '.join(f"{'-'.join(ts)} ({','.join(ps)})" for ts, ps in pos_raw_pool)),
    ]
    pd.DataFrame(redup_rows).to_csv(os.path.join(OUT, 'reduplication_test.csv'), index=False)

    # Rival split stats
    foreign_xx_signs = collections.Counter(p for _, ps in pos_raw_pool for p in ps)
    total_xx_pairs = sum(foreign_xx_signs.values())
    person_xx_pairs = sum(v for k, v in foreign_xx_signs.items() if k in PERSON_SIGNS)
    nonstroke_pool = [t for ts in pooled_for.tokens_raw for t in ts if valid_tok(t) and t not in STROKE_COUNTS]
    man_rate_in_pool = sum(1 for t in nonstroke_pool if t in CORE_MAN_SIGNS) / len(nonstroke_pool)
    p_man_conc = binomtest(person_xx_pairs, total_xx_pairs, man_rate_in_pool, alternative='greater').pvalue
    cv_only = {k: v for k, v in cdli_xx_sylls.items() if len(k) == 2 and (k[0] in 'aeiou' or k[1] in 'aeiou')}
    top1_cdli_cv_share = max(cv_only.values()) / sum(cv_only.values()) if cv_only else 0.0

    # Foreign-enriched non-man, non-stroke signs
    home_sign_doc = collections.Counter(t for ts in home_n2 for t in set(ts) if valid_tok(t))
    gulf_sign_doc = collections.Counter(t for ts in gulf_only.tokens for t in set(ts) if valid_tok(t))
    enriched_foreign_signs = []
    for s, k in gulf_sign_doc.items():
        if k < 2 or s in CORE_MAN_SIGNS or s in STROKE_COUNTS:
            continue
        kh = home_sign_doc[s]
        _, pv = fisher_exact([[k, n_gulf - k], [kh, n_home - kh]], alternative='greater')
        ratio = (k / n_gulf) / max(1 / n_home, kh / n_home)
        if pv < 0.05:
            enriched_foreign_signs.append(dict(sign=s, gulf_texts=k, gulf_n=n_gulf, home_texts=kh, home_n=n_home,
                                               enrichment=round(ratio, 1), fisher_p=pv))
    enriched_foreign_signs.sort(key=lambda x: x['fisher_p'])
    pd.DataFrame(enriched_foreign_signs).to_csv(os.path.join(OUT, 'foreign_enriched_stem_signs.csv'), index=False)

    # Extract segmented Gulf name-stems & run both cross-stem edge test AND multi-language acrophonic rescue!
    stems = []
    for _, r in gulf_only.iterrows():
        mt, segs, ok = segment_gulf_seal(r.tokens)
        for role, s_toks in segs:
            if role in ('STEM_1', 'STEM_2', 'GENITIVE_NAME', 'STEM_2_OR_TITLE', 'STEM', 'RAW'):
                clean = [t for t in s_toks if valid_tok(t) and t not in STROKE_COUNTS]
                if 2 <= len(clean) <= 4:
                    stems.append((r.uid, r.site, role, tuple(clean)))

    unique_stems = sorted({st for _, _, _, st in stems})
    obs_edges = sum(1 for i in range(len(unique_stems)) for j in range(i + 1, len(unique_stems)) if set(unique_stems[i]) & set(unique_stems[j]))
    home_stems_by_len = collections.defaultdict(list)
    for ts in home_seals:
        cl = [t for t in ts if valid_tok(t) and t not in STROKE_COUNTS and t not in HOME_CLOSERS]
        if 2 <= len(cl) <= 4:
            home_stems_by_len[len(cl)].append(tuple(cl))
    ctrl_edges = np.array([
        sum(
            1 for i in range(len(unique_stems)) for j in range(i + 1, len(unique_stems))
            if set(s[i]) & set(s[j])
        )
        for s in [[home_stems_by_len[len(st)][rng.integers(len(home_stems_by_len[len(st)]))] for st in unique_stems] for _ in range(1000)]
    ])

    rescue_rows = run_rescue_acrophonic_onomastics(stems, cdf)

    rival_summary = dict(
        mahadevan_twin_law='M 1-1 = Lipi 091 (twin-men); M 245-245 = Lipi 617 (twin-grid); M 121-121 = Lipi 056; identifies M9902 = G2-09 (Gadd no. 18 two-bull round seal) as 235-091-617!',
        surface_xx_sign_counts=dict(foreign_xx_signs),
        person_share_of_surface_xx=round(person_xx_pairs / max(1, total_xx_pairs), 4),
        man_token_share_in_foreign_nonstroke=round(man_rate_in_pool, 4),
        binom_p_person_concentration=p_man_conc,
        top1_cdli_cv_xx_share=round(top1_cdli_cv_share, 4),
        unique_gulf_stems=len(unique_stems),
        obs_stem_shared_edges=obs_edges,
        home_stem_shared_edges_mean=round(float(ctrl_edges.mean()), 2),
        p_stem_edges_higher=round(float((1 + np.sum(ctrl_edges >= obs_edges)) / 1001.0), 4),
    )
    with open(os.path.join(OUT, 'rival_and_summary_1b.json'), 'w') as f:
        json.dump(rival_summary, f, indent=2)

    return redup_rows, enriched_foreign_signs, rival_summary, rescue_rows


def main():
    df, home_distinct, home_seals, new_distinct = build_corpora()
    print(f"[fnam_01] Master foreign corpus: {len(df)} objects "
          f"(strict cat={df.in_strict_cat.sum()}, Gulf round pool={df.gulf_pool.sum()}, >=2 signs={(df.n_tok>=2).sum()})")
    print(f"[fnam_01] Home baselines: {len(home_distinct)} Lipi distinct texts ({len(home_seals)} seal texts), "
          f"Unseen Mahadevan new texts (twin-normalized): {len(new_distinct)} distinct texts")

    stats_1a, seg_rows = run_test_1a(df, home_distinct, home_seals, new_distinct)
    print("\n=== TEST 1A: Cuneiform Determinative / Relational Calque ===")
    for s in stats_1a:
        print(" ", s)

    redup_rows, enr_signs, rival, rescue_rows = run_test_1b(df, home_distinct, home_seals, new_distinct)
    print("\n=== TEST 1B: Twin-Men (091) & True Non-Stroke X-X Reduplication Abroad vs Home & New Texts ===")
    for r in redup_rows:
        print(f"  {r['metric']}: {r['k']}/{r['n']} ({r['rate']*100:.2f}%), "
              f"home {r['home_obs']} (x{r['vs_home_ratio']}, P={r['p_vs_home']:.2e}), "
              f"new {r['new_obs']} (P={r['p_vs_new']})")
    print("\n=== RIVAL SPLIT & TWIN-GLYPH DISCOVERY ===")
    for k, v in rival.items():
        print(f"  {k}: {v}")
    print("\n=== RESCUE 1B: Multi-Language Acrophonic Onomastic Readout vs 28 Attested CDLI East Names ===")
    for rr in rescue_rows:
        print(" ", rr)
    print("\n=== Foreign-Enriched Non-Man, Non-Stroke Signs in Gulf Pool (P < 0.05) ===")
    for e in enr_signs[:10]:
        print(" ", e)


if __name__ == '__main__':
    main()
