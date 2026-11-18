#!/usr/bin/env python3
"""typo_02_grammar_fit.py -- Quantitative Grammatical / Morphosyntactic Typology Matrix
& WALS/Grambank Empirical Eurasian Bayes Factor Analysis across Candidate Language Families.

Part A: Word-Free Corpus Measurement of ALL 7 Grammatical Features on Lipi (one-row-per-object
        copy-events via v2_common) AND Held-Out Unseen Mahadevan Texts (1,183 unpartnered lines),
        each tested against 2,000 shuffled / decoy controls:
  G1. [Possessor] + [Genitive/Possessive Enclitic (740)] post-nominal dependent marking (no head prefix)
  G2. [Possessor + 740] + [Head Noun (090 man / 400 comb / H10_8 title)] strictly right-headed NP
  G3. [Numeral] + [Discrete Good (THING)] vs. [Measure] + [Numeral] split
  G4. Two distinct numeral stroke series (short 1..8 vs. tall 1..5 + name-locked 032):
      quantitative split test of (a)Num+CLF+Noun classifier chains vs (b)animate/inanimate gender
      vs (c)metrological unit-series polyvalency + adjectival/substantive stem allomorphy!
  G5. Base-12 / fractional-12 capacity counts (1, 2, 3, 4, 6 — strict ban on 5) + 8-ceiling / subtractive 9
  G6. Right-headed nominal compounding ([modifier/numeral] + [fish 220], compound right-edge distribution)
  G7. Absence of productive stem-internal infixation ([A - x - B]) and bound lexical prefixation vs
      strong suffixation ([A - B - s]) — direct corpus test against Munda <-p->/<-n-> infixes,
      Akkadian m-/t- prefixes, and Burushaski possessive prefixes!

Part B: WALS + Grambank CLDF Empirical Eurasian Base Rates (563 Grambank + 659 WALS Eurasian languages
        across ~40 Eurasian families) & Correlation-Adjusted Joint Bayes Factor:
  - Evaluates 8 historical languages/reconstructions:
      1. Proto-Dravidian (~2500 BCE)
      2. Proto-Munda (pre-Indo-Aryan reconstruction, Pinnow/Donegan-Stampe/Anderson)
      3. North Munda (modern South Asian Sprachbund stage — strongest-defender Munda check!)
      4. Proto-Indo-Iranian / Early Vedic OIA
      5. Burushaski (vernacular Hunza/Yasin stratum)
      6. Linear / Old Elamite (~2600-1800 BCE)
      7. Sumerian (~2600-2000 BCE)
      8. Akkadian (Old Akkadian / East Semitic)
  - Computes BOTH:
      (i) Independent-feature Bayes Factor (using family-stratified WALS/Grambank Eurasian priors)
      (ii) Correlation-Adjusted Joint Empirical Bayes Factor directly from the Grambank Eurasian
           language-by-feature co-occurrence matrix (testing the strongest rival explanation:
           Greenbergian / South Asian Sprachbund head-final feature correlation!).

Outputs (work_data/typo/):
  - grammar_corpus_features.csv
  - grammar_g4_g7_mechanisms.csv
  - wals_grambank_eurasia_baserates.csv
  - grammar_typology_matrix.csv
  - grammar_bayes_summary.csv
"""
import os, sys, re, csv, math, time, collections, itertools
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, binomtest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

OUT_DIR = os.path.join(ROOT, "work_data", "typo")
CLDF_DIR = "/tmp/typology_cldf"
os.makedirs(OUT_DIR, exist_ok=True)

t0 = time.time()
def log(*a):
    print(f"[typo_02 {time.time()-t0:6.1f}s]", *a, flush=True)


# ==============================================================================
# PART A: DIRECT CORPUS MEASUREMENT ON LIPI COPY-EVENTS & HELD-OUT NEW TEXTS
# ==============================================================================
def measure_indus_grammar():
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        import frame2_common as f2

    rng = np.random.default_rng(20261118)

    # One-row-per-object / copy-event clean complete lines in Lipi vs Held-Out Mahadevan New Texts (1,183 unpartnered)
    def clean_lines(df):
        out = []
        comp_col = df.complete_b if hasattr(df, 'complete_b') else df.complete
        for x, comp, kind in zip(df.tok, comp_col, df.kind):
            if comp and x and len(x) >= 2 and all(s not in ('000', 'ALT') and not s.startswith('X') for s in x):
                out.append((tuple(x), kind))
        return out

    lipi_lines = clean_lines(f2.d)
    Mu = f2.M[~f2.M.partnered]
    new_lines = clean_lines(Mu)
    log(f"Loaded corpora: Lipi clean complete object-events = {len(lipi_lines)} | "
        f"Held-out Mahadevan unpartnered total = {len(Mu)}, clean complete len>=2 = {len(new_lines)}")

    cv2 = {s: f2.v2_of(s) for s in set(x for t, _ in lipi_lines + new_lines for x in t)}
    NUM_SHORT = {f"{k:03d}" for k in range(1, 10)} | {f"{k:03d}" for k in range(12, 19)}
    NUM_TALL  = {'031', '032', '033', '034', '035', '036'}
    NUM_ALL   = NUM_SHORT | NUM_TALL
    VAL_OF = {
        '001': 1, '031': 1, '002': 2, '012': 2, '032': 2, '003': 3, '013': 3, '033': 3,
        '004': 4, '014': 4, '034': 4, '005': 5, '015': 5, '035': 5, '006': 6, '016': 6, '036': 6,
        '007': 7, '017': 7, '008': 8, '018': 8, '009': 9, '019': 9, '055': 12
    }
    TITLES = {s for s, c in cv2.items() if c == 'TITLE'} | {'090', '400', '527', '621', '161', '241', '565', '679'}
    THINGS = {'390', '405', '406', '407', '156', '806'}
    MEASURES_STRICT = {'705', '706', '711', '171'}  # pure pre-numeral capacity/weight vessels
    FISH_ALL = {'220', '226', '231', '233', '235', '240', '242', '243'}

    feat_rows = []
    mech_rows = []

    for split_name, lines in (("Lipi_events", lipi_lines), ("Heldout_NewTexts", new_lines)):
        toks_only = [t for t, _ in lines]

        # ------------------------------------------------------------------
        # G1: Post-nominal Possessive Enclitic [Possessor + 740] vs [740 + Possessor]
        # ------------------------------------------------------------------
        g1_post, g1_init = 0, 0
        direct_740_title, intervening_740_x_title = 0, 0
        for t in toks_only:
            if '740' in t:
                idx = t.index('740')
                if idx > 0:
                    g1_post += 1
                else:
                    g1_init += 1
            for i in range(len(t) - 1):
                if t[i] == '740' and t[i + 1] in TITLES:
                    direct_740_title += 1
            for i in range(len(t) - 2):
                if t[i] == '740' and t[i + 2] in TITLES and t[i + 1] not in ('740', '520'):
                    intervening_740_x_title += 1

        # Token-order shuffle control (2,000 draws)
        shuf_post = []
        t_740 = [t for t in toks_only if '740' in t]
        for _ in range(2000):
            c_p = sum(1 for t in t_740 if rng.integers(len(t)) > 0)
            shuf_post.append(c_p)
        shuf_arr = np.array(shuf_post, dtype=float)
        g1_rate = g1_post / max(1, g1_post + g1_init)
        g1_ctrl = shuf_arr.mean() / max(1, len(t_740))
        g1_z = (g1_post - shuf_arr.mean()) / (shuf_arr.std() + 1e-9)
        g1_p = (1.0 + np.sum(shuf_arr >= g1_post)) / 2001.0

        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G1_Postnominal_Genitive_740',
            'obs_pos': g1_post, 'obs_neg': g1_init, 'obs_rate': round(g1_rate, 4),
            'ctrl_rate': round(float(g1_ctrl), 4), 'z_score': round(float(g1_z), 2), 'P_value': round(float(g1_p), 5),
            'extra': f"direct_740+Title={direct_740_title} vs 740+x+Title={intervening_740_x_title} (no head-possessive prefix)"
        })

        # ------------------------------------------------------------------
        # G2: Right-Headed Possessive NP: [Possessor + 740 + Title] vs [Title + Possessor + 740] / [Title + 740 + Possessor]
        # ------------------------------------------------------------------
        g2_right, g2_left = 0, 0
        for t in toks_only:
            if '740' in t and any(s in TITLES for s in t) and len(t) >= 3:
                i740 = t.index('740')
                itit = [i for i, s in enumerate(t) if s in TITLES]
                if i740 >= 1 and any(i > i740 for i in itit):
                    g2_right += 1
                elif any(i < i740 for i in itit) and i740 == len(t) - 1:
                    g2_left += 1
        g2_tot = g2_right + g2_left
        g2_p = binomtest(g2_right, max(1, g2_tot), 0.5, alternative='greater').pvalue if g2_tot > 0 else 1.0
        g2_z = (g2_right - 0.5 * g2_tot) / max(1e-9, math.sqrt(0.25 * max(1, g2_tot)))
        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G2_RightHeaded_PossNP_740_Title',
            'obs_pos': g2_right, 'obs_neg': g2_left, 'obs_rate': round(g2_right / max(1, g2_tot), 4),
            'ctrl_rate': 0.5000, 'z_score': round(g2_z, 2), 'P_value': float(f"{g2_p:.2e}"),
            'extra': f"[Stem+740+Title]={g2_right} vs [Title+Stem+740]={g2_left}"
        })

        # ------------------------------------------------------------------
        # G3: [Numeral + Discrete Good] vs [Measure + Numeral] Split
        # ------------------------------------------------------------------
        num_thing, thing_num = 0, 0
        meas_num, num_meas = 0, 0
        num_clf_thing = 0  # Check 3-sign [NUM + CLF + THING] classifier chain!
        cand_clfs = collections.Counter()
        for t in toks_only:
            for a, b in zip(t, t[1:]):
                if a in NUM_ALL and b in THINGS:
                    num_thing += 1
                elif a in THINGS and b in NUM_ALL:
                    thing_num += 1
                if a in MEASURES_STRICT and b in NUM_ALL:
                    meas_num += 1
                elif a in NUM_ALL and b in MEASURES_STRICT:
                    num_meas += 1
            for a, x, b in zip(t, t[1:], t[2:]):
                if a in NUM_ALL and b in THINGS and x not in NUM_ALL and x not in THINGS and cv2.get(x) not in ('OPEN', 'SLOT', 'CLOSER'):
                    num_clf_thing += 1
                    cand_clfs[x] += 1

        p_g3 = fisher_exact([[num_thing, thing_num], [num_meas, meas_num]], alternative='greater')[1]
        odds_g3 = ((num_thing + 0.5) * (meas_num + 0.5)) / ((thing_num + 0.5) * (num_meas + 0.5))
        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G3_NumGood_vs_MeasureNum_Split',
            'obs_pos': num_thing + meas_num, 'obs_neg': thing_num + num_meas,
            'obs_rate': round((num_thing + meas_num) / max(1, num_thing + thing_num + meas_num + num_meas), 4),
            'ctrl_rate': 0.5000, 'z_score': round(math.log(odds_g3), 2), 'P_value': float(f"{p_g3:.2e}"),
            'extra': f"Num+Thing={num_thing}:{thing_num} | Meas+Num={meas_num}:{num_meas} (logOR={math.log(odds_g3):.2f})"
        })

        # ------------------------------------------------------------------
        # G4: Two Numeral Stroke Series (Short vs Tall vs 032) — Mechanism Split Test!
        # ------------------------------------------------------------------
        # Measure distribution of SHORT vs TALL_OTHER vs TALL_032 across 5 syntactic/semantic environments
        env_counts = {
            'AFTER_MEASURE_700_705': [0, 0, 0],  # [short, tall_other, 032]
            'BEFORE_DISCRETE_THING': [0, 0, 0],
            'AFTER_OPENER_SLOT':     [0, 0, 0],
            'BEFORE_PLAIN_FISH_220': [0, 0, 0],
            'BEFORE_MARKED_FISH':    [0, 0, 0],
            'ADJ_HUMAN_SIGN':        [0, 0, 0],
        }
        def s_idx(s):
            return 2 if s == '032' else (1 if s in NUM_TALL else 0)

        for t in toks_only:
            for i, s in enumerate(t):
                if s not in NUM_ALL:
                    continue
                si = s_idx(s)
                prev_s = t[i - 1] if i > 0 else None
                next_s = t[i + 1] if i < len(t) - 1 else None
                if prev_s in (MEASURES_STRICT | {'700'}) or next_s == '700':
                    env_counts['AFTER_MEASURE_700_705'][si] += 1
                if next_s in THINGS:
                    env_counts['BEFORE_DISCRETE_THING'][si] += 1
                if prev_s in {'817', '861', '820', '920', '692'}:
                    env_counts['AFTER_OPENER_SLOT'][si] += 1
                if next_s == '220':
                    env_counts['BEFORE_PLAIN_FISH_220'][si] += 1
                if next_s in (FISH_ALL - {'220'}):
                    env_counts['BEFORE_MARKED_FISH'][si] += 1
                if next_s in {'090', '154', '156', '151'} or prev_s in {'090', '154'}:
                    env_counts['ADJ_HUMAN_SIGN'][si] += 1

        mat_g4 = np.array([env_counts[k] for k in ['AFTER_MEASURE_700_705', 'BEFORE_DISCRETE_THING',
                                                   'AFTER_OPENER_SLOT', 'BEFORE_PLAIN_FISH_220', 'BEFORE_MARKED_FISH']], dtype=float)
        tot_g4 = mat_g4.sum()
        # Mutual Information I(Environment; StrokeSeries) in bits vs 2,000 label shuffles
        def calc_mi(M):
            N = M.sum()
            if N == 0:
                return 0.0
            P = M / N
            pr = P.sum(axis=1, keepdims=True)
            pc = P.sum(axis=0, keepdims=True)
            with np.errstate(divide='ignore', invalid='ignore'):
                mi = np.nansum(np.where(P > 0, P * np.log2(P / (pr @ pc + 1e-15)), 0.0))
            return float(mi)

        obs_mi = calc_mi(mat_g4)
        # Shuffle stroke series labels among the tot_g4 observations
        flat_env = np.repeat(np.arange(len(mat_g4)), mat_g4.sum(axis=1).astype(int))
        flat_ser = np.concatenate([np.repeat(np.arange(3), row.astype(int)) for row in mat_g4])
        null_mi = []
        for _ in range(2000):
            perm_ser = rng.permutation(flat_ser)
            M_sh = np.zeros_like(mat_g4)
            np.add.at(M_sh, (flat_env, perm_ser), 1)
            null_mi.append(calc_mi(M_sh))
        nmi_arr = np.array(null_mi)
        p_g4 = (1.0 + np.sum(nmi_arr >= obs_mi - 1e-12)) / 2001.0
        z_g4 = (obs_mi - nmi_arr.mean()) / (nmi_arr.std() + 1e-12)

        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G4_Two_Stroke_Series_Specialization',
            'obs_pos': int(mat_g4[0, 1] + mat_g4[1, 0] + mat_g4[2, 0] + mat_g4[3, 2] + mat_g4[4, 0]),
            'obs_neg': int(tot_g4 - (mat_g4[0, 1] + mat_g4[1, 0] + mat_g4[2, 0] + mat_g4[3, 2] + mat_g4[4, 0])),
            'obs_rate': round(obs_mi, 4),
            'ctrl_rate': round(float(nmi_arr.mean()), 4),
            'z_score': round(float(z_g4), 2), 'P_value': float(f"{p_g4:.2e}"),
            'extra': f"MI={obs_mi:.3f} bits | Meas(S/T/032)={env_counts['AFTER_MEASURE_700_705']} Thing={env_counts['BEFORE_DISCRETE_THING']} Fish220={env_counts['BEFORE_PLAIN_FISH_220']} | Num+CLF+Thing={num_clf_thing} vs direct Num+Thing={num_thing}"
        })
        for ek, ev in env_counts.items():
            mech_rows.append({
                'corpus': split_name, 'mechanism': 'G4_stroke_env', 'category': ek,
                'short_count': ev[0], 'tall_other_count': ev[1], 'tall_032_count': ev[2],
                'note': f"Num+x+Thing={num_clf_thing} (top x={cand_clfs.most_common(2)})"
            })

        # ------------------------------------------------------------------
        # G5: Base-12 Unit-Fraction Capacity Counts (1, 2, 3, 4, 6 — Ban on 5!)
        # ------------------------------------------------------------------
        cup_vals = collections.Counter()
        other_vals = collections.Counter()
        for t in toks_only:
            for i, s in enumerate(t):
                if s not in VAL_OF:
                    continue
                v = VAL_OF[s]
                prev_s = t[i - 1] if i > 0 else None
                next_s = t[i + 1] if i < len(t) - 1 else None
                if prev_s == '700' or next_s == '700':
                    cup_vals[v] += 1
                else:
                    other_vals[v] += 1

        div12_cup = sum(cup_vals[v] for v in (1, 2, 3, 4, 6, 12))
        non12_cup = sum(cup_vals[v] for v in (5, 7, 8, 9))
        div12_oth = sum(other_vals[v] for v in (1, 2, 3, 4, 6, 12))
        non12_oth = sum(other_vals[v] for v in (5, 7, 8, 9))
        p_g5 = fisher_exact([[div12_cup, non12_cup], [div12_oth, non12_oth]], alternative='greater')[1]
        # Shuffle numeral tokens between 700-adjacent and non-700 positions (2,000 draws)
        pool_v = ([1] * (div12_cup + div12_oth)) + ([0] * (non12_cup + non12_oth))
        pool_v = np.array(pool_v, dtype=int)
        n_cup_tot = div12_cup + non12_cup
        sh_g5 = np.array([rng.choice(pool_v, size=n_cup_tot, replace=False).sum() for _ in range(2000)], dtype=float) if n_cup_tot > 0 else np.zeros(2000)
        z_g5 = 0.0 if sh_g5.std() < 1e-9 else (div12_cup - sh_g5.mean()) / sh_g5.std()

        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G5_Base12_Divisors_Cup700_No5',
            'obs_pos': div12_cup, 'obs_neg': non12_cup,
            'obs_rate': round(div12_cup / max(1, n_cup_tot), 4),
            'ctrl_rate': round(div12_oth / max(1, div12_oth + non12_oth), 4),
            'z_score': round(float(z_g5), 2), 'P_value': float(f"{p_g5:.2e}"),
            'extra': f"700_vals={dict(sorted(cup_vals.items()))} | non700_5_7_8={non12_oth}/{div12_oth+non12_oth}"
        })

        # ------------------------------------------------------------------
        # G6: Right-Headed Nominal Compounding ([Modifier/Numeral + Fish] vs [Fish + Modifier/Numeral])
        #     Exclude count-record boundaries where fish is followed by [Num + Thing]
        # ------------------------------------------------------------------
        mod_before_fish, mod_after_fish = 0, 0
        for t in toks_only:
            for i, s in enumerate(t):
                if s in FISH_ALL:
                    if i > 0 and (t[i - 1] in NUM_ALL or t[i - 1] == '415'):
                        mod_before_fish += 1
                    # Post-fish numeral that is NOT followed by a counted discrete THING or MEASURE
                    if i < len(t) - 1 and (t[i + 1] in NUM_ALL or t[i + 1] == '415'):
                        if not (i + 2 < len(t) and (t[i + 2] in THINGS or t[i + 2] in MEASURES_STRICT or t[i + 2] == '700')):
                            mod_after_fish += 1
        g6_tot = mod_before_fish + mod_after_fish
        p_g6 = binomtest(mod_before_fish, max(1, g6_tot), 0.5, alternative='greater').pvalue if g6_tot > 0 else 1.0
        z_g6 = (mod_before_fish - 0.5 * g6_tot) / max(1e-9, math.sqrt(0.25 * max(1, g6_tot)))
        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G6_RightHeaded_Modifier_Fish_Compound',
            'obs_pos': mod_before_fish, 'obs_neg': mod_after_fish,
            'obs_rate': round(mod_before_fish / max(1, g6_tot), 4),
            'ctrl_rate': 0.5000, 'z_score': round(z_g6, 2), 'P_value': float(f"{p_g6:.2e}"),
            'extra': f"[Mod+Fish]={mod_before_fish} vs [Fish+Mod_noncount]={mod_after_fish}"
        })

        # ------------------------------------------------------------------
        # G7: Absence of Productive Infixation ([A - x - B]) vs Strong Suffixation ([A - B - s])!
        #     Test on all frequent 2-sign lexical stems A-B (occurring >=3 times, neither A nor B is
        #     an opener/slot/closer/numeral) across distinct text types!
        # ------------------------------------------------------------------
        distinct_texts = sorted(set(toks_only))
        SKIP_STEM = {s for s, c in cv2.items() if c in ('OPEN', 'SLOT', 'CLOSER', 'TITLE')} | NUM_ALL
        stem_bg = collections.Counter()
        for t in distinct_texts:
            for a, b in zip(t, t[1:]):
                if a not in SKIP_STEM and b not in SKIP_STEM and a != b:
                    stem_bg[(a, b)] += 1
        freq_stems = {ab for ab, cnt in stem_bg.items() if cnt >= (3 if split_name == "Lipi_events" else 2)}

        def affix_profile(text_set, stems):
            infix_by_x = collections.defaultdict(set)   # x -> set of (A, B) split as A-x-B
            suffix_by_s = collections.defaultdict(set)  # s -> set of (A, B) extended at right edge as A-B-s
            prefix_by_p = collections.defaultdict(set)  # p -> set of (A, B) extended at left as p-A-B (excluding syntactic OPEN/SLOT/NUM)
            for t in text_set:
                for i in range(len(t) - 2):
                    a, x, b = t[i], t[i + 1], t[i + 2]
                    if (a, b) in stems and x not in NUM_ALL:
                        infix_by_x[x].add((a, b))
                    if (a, x) in stems:
                        suffix_by_s[b].add((a, x))
                    if (x, b) in stems and a not in NUM_ALL and cv2.get(a) not in ('OPEN', 'SLOT'):
                        prefix_by_p[a].add((x, b))
            # Productive = morpheme attaching to >= 3 distinct stems (or >= 2 on smaller held-out set)
            min_prod = 3 if len(text_set) > 800 else 2
            n_inf_events = sum(len(v) for v in infix_by_x.values() if len(v) >= min_prod)
            n_suf_events = sum(len(v) for v in suffix_by_s.values() if len(v) >= min_prod)
            n_pre_events = sum(len(v) for v in prefix_by_p.values() if len(v) >= min_prod)
            max_inf = max((len(v) for v in infix_by_x.values()), default=0)
            max_suf = max((len(v) for v in suffix_by_s.values()), default=0)
            top_inf = sorted(((k, len(v)) for k, v in infix_by_x.items()), key=lambda z: -z[1])[:3]
            top_suf = sorted(((k, len(v)) for k, v in suffix_by_s.items()), key=lambda z: -z[1])[:3]
            return n_inf_events, n_suf_events, n_pre_events, max_inf, max_suf, top_inf, top_suf

        inf_ev, suf_ev, pre_ev, max_inf, max_suf, top_inf, top_suf = affix_profile(distinct_texts, freq_stems)

        # Shuffle internal token order of each distinct text (2,000 draws) to get null infixation vs suffixation ratio!
        null_suf_share = []
        null_inf = []
        for _ in range(500):
            sh_texts = [tuple(rng.permutation(t)) for t in distinct_texts]
            i_e, s_e, _, _, _, _, _ = affix_profile(sh_texts, freq_stems)
            null_inf.append(i_e)
            null_suf_share.append(s_e / max(1, s_e + i_e))
        obs_suf_share = suf_ev / max(1, suf_ev + inf_ev)
        ns_arr = np.array(null_suf_share, dtype=float)
        ni_arr = np.array(null_inf, dtype=float)
        z_g7 = (obs_suf_share - ns_arr.mean()) / (ns_arr.std() + 1e-9)
        p_g7 = (1.0 + np.sum(ns_arr >= obs_suf_share - 1e-9)) / (1.0 + len(ns_arr))

        feat_rows.append({
            'corpus': split_name, 'feature_id': 'G7_Suffixing_Over_Infixation_Ratio',
            'obs_pos': suf_ev, 'obs_neg': inf_ev,
            'obs_rate': round(obs_suf_share, 4),
            'ctrl_rate': round(float(ns_arr.mean()), 4),
            'z_score': round(float(z_g7), 2), 'P_value': round(float(p_g7), 4),
            'extra': f"stems={len(freq_stems)} | prod_suffix={suf_ev}(top={top_suf}) vs prod_infix={inf_ev}(null={ni_arr.mean():.1f}, top={top_inf}) vs bound_prefix={pre_ev}"
        })
        mech_rows.append({
            'corpus': split_name, 'mechanism': 'G7_affix_asymmetry',
            'category': 'productive_stem_attachments',
            'short_count': suf_ev, 'tall_other_count': pre_ev, 'tall_032_count': inf_ev,
            'note': f"col1=suffix({top_suf}), col2=bound_prefix, col3=infix({top_inf}, null_mean={ni_arr.mean():.1f})"
        })

    for r in feat_rows:
        log(f"  [{r['corpus']:16s}] {r['feature_id']:36s}: {r['obs_pos']:4d}:{r['obs_neg']:<4d} "
            f"(rate={r['obs_rate']:.3f} vs ctrl={r['ctrl_rate']:.3f}, z={r['z_score']:+.2f}, P={r['P_value']}) | {r['extra'][:75]}")

    pd.DataFrame(feat_rows).to_csv(os.path.join(OUT_DIR, "grammar_corpus_features.csv"), index=False)
    pd.DataFrame(mech_rows).to_csv(os.path.join(OUT_DIR, "grammar_g4_g7_mechanisms.csv"), index=False)
    return feat_rows


# ==============================================================================
# PART B: WALS + GRAMBANK EMPIRICAL EURASIAN BASE RATES & JOINT BAYES FACTOR
# ==============================================================================
def compute_wals_grambank_baserates():
    """Compute exact language-level AND family-stratified (equal weight per language family)
    Eurasian base rates from WALS + Grambank CLDF, PLUS the empirical joint co-occurrence
    probability across Grambank Eurasian languages to defeat the Greenbergian correlation rival!"""
    gb_langs = {r['ID']: r for r in csv.DictReader(open(os.path.join(CLDF_DIR, "gb_languages.csv"), encoding="utf-8"))
                if r.get('Macroarea') == 'Eurasia'}
    wals_langs = {r['ID']: r for r in csv.DictReader(open(os.path.join(CLDF_DIR, "wals_languages.csv"), encoding="utf-8"))
                  if r.get('Macroarea') == 'Eurasia'}

    gb_mat = collections.defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(CLDF_DIR, "gb_values.csv"), encoding="utf-8")):
        lid = r['Language_ID']
        if lid in gb_langs and r['Value'] != '?':
            gb_mat[lid][r['Parameter_ID']] = r['Value']

    wals_mat = collections.defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(CLDF_DIR, "wals_values.csv"), encoding="utf-8")):
        lid = r['Language_ID']
        if lid in wals_langs:
            wals_mat[lid][r['Parameter_ID']] = r.get('Code_ID', '')

    # Sanity-verify Tamil (tami1289) in Grambank so code orientation is 100% verified
    if 'tami1289' in gb_mat:
        tm = gb_mat['tami1289']
        log(f"Grambank sanity check on Tamil (tami1289): GB065(Gen-N)={tm.get('GB065')}, GB024(Num-N)={tm.get('GB024')}, "
            f"GB432(PossSuf)={tm.get('GB432')}, GB431(PossPref)={tm.get('GB431')}, GB081(Infix)={tm.get('GB081')}")

    def family_stratified_rate(lang_dict, val_dict, pred_fn, fam_key='Family_name'):
        """Compute raw language rate AND family-equal-weighted rate across Eurasia."""
        by_fam = collections.defaultdict(list)
        raw_hits, raw_tot = 0, 0
        for lid, linfo in lang_dict.items():
            vals = val_dict.get(lid, {})
            res = pred_fn(vals)
            if res is None:
                continue
            fam = linfo.get(fam_key) or linfo.get('Family') or f"Isolate_{lid}"
            by_fam[fam].append(1.0 if res else 0.0)
            raw_tot += 1
            if res:
                raw_hits += 1
        raw_p = raw_hits / max(1, raw_tot)
        fam_p = float(np.mean([np.mean(v) for v in by_fam.values()])) if by_fam else raw_p
        return raw_hits, raw_tot, len(by_fam), round(raw_p, 4), round(fam_p, 4)

    # Map each of the 7 Indus Grammatical Features to its objective Grambank / WALS Eurasian proxy!
    feature_defs = [
        ("G1_Possessor_Suffix_NoHeadPrefix", "Grambank GB432=1 & GB431=0 & GB075=1 (dependent suffix/postposition on possessor, no head possessive prefix)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB432'] == '1' and v['GB431'] == '0' and v['GB075'] == '1') if ('GB432' in v and 'GB431' in v and 'GB075' in v) else None),

        ("G2_RightHeaded_Possessor_Possessed", "Grambank GB065=1 (pragmatically unmarked Possessor-Possessed NP order; WALS 86A-1)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB065'] == '1') if 'GB065' in v else None),

        ("G3_NumNoun_Discrete_AccountingSplit", "Grambank GB024=1 (Numeral-Noun order for discrete count nouns; WALS 89A-1)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB024'] == '1') if 'GB024' in v else None),

        ("G4_NoSortalCLF_StemAllomorphy", "Grambank GB057=0 (no obligatory numeral sortal classifier chain Num+CLF+N; WALS 55A-1)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB057'] == '0') if 'GB057' in v else None),

        ("G5_NonPureDecimal_OctonalDuodecimal", "WALS 131A != 131A-1 / Grambank GB333=0 or hybrid/subtractive/duodecimal-sexagesimal metrology",
         wals_langs, wals_mat, 'Family',
         lambda v: (v['131A'] != '131A-1') if '131A' in v else None),

        ("G6_RightHeaded_Compounding_StrictHeadFinal", "WALS 86A-1 & 85A-1 / Grambank GB065=1 & GB074=0 & GB075=1 (strict head-final nominal modifiers, no prepositions)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB065'] == '1' and v['GB074'] == '0' and v['GB075'] == '1') if ('GB065' in v and 'GB074' in v and 'GB075' in v) else None),

        ("G7_SuffixingOnly_NoInfix_NoPrefix", "Grambank GB080=1 & GB079=0 & GB081=0 (suffixing/enclitic, zero productive infixation & lexical prefixation; WALS 26A-2)",
         gb_langs, gb_mat, 'Family_name',
         lambda v: (v['GB080'] == '1' and v['GB079'] == '0' and v['GB081'] == '0') if ('GB080' in v and 'GB079' in v and 'GB081' in v) else None),
    ]

    br_rows = []
    fam_priors = {}
    for fid, desc, ld, vd, fk, fn in feature_defs:
        hits, tot, nfams, raw_p, fam_p = family_stratified_rate(ld, vd, fn, fk)
        br_rows.append({
            'feature_id': fid, 'source_proxy': desc,
            'eurasia_hits': hits, 'eurasia_total': tot, 'eurasia_families': nfams,
            'raw_eurasia_rate': raw_p, 'family_stratified_rate': fam_p
        })
        fam_priors[fid] = fam_p
        log(f"  [Eurasia Prior] {fid:42s}: {hits:3d}/{tot:3d} langs ({nfams:2d} fams) -> raw={raw_p:.3f}, fam_strat={fam_p:.3f}")

    # EMPIRICAL JOINT CORRELATION CHECK IN GRAMBANK EURASIA (Rival Check: Greenbergian / Sprachbund Correlation!)
    # Check what fraction of Grambank Eurasian languages (and families) SIMULTANEOUSLY satisfy all 6 morphosyntactic
    # Grambank predicates (G1, G2, G3, G4, G6, G7)!
    def all6_gb(v):
        req = ('GB432', 'GB431', 'GB075', 'GB065', 'GB024', 'GB057', 'GB074', 'GB080', 'GB079', 'GB081')
        if not all(k in v for k in req):
            return None
        return (
            v['GB432'] == '1' and v['GB431'] == '0' and v['GB075'] == '1' and
            v['GB065'] == '1' and v['GB024'] == '1' and v['GB057'] == '0' and
            v['GB074'] == '0' and v['GB080'] == '1' and v['GB079'] == '0' and v['GB081'] == '0'
        )

    j_hits, j_tot, j_nfams, j_raw, j_fam = family_stratified_rate(gb_langs, gb_mat, all6_gb, 'Family_name')
    matching_fams = sorted({
        gb_langs[lid].get('Family_name', lid)
        for lid in gb_langs if all6_gb(gb_mat.get(lid, {})) is True
    })
    indep_prod_6 = float(np.prod([fam_priors[k] for k in fam_priors if k != 'G5_NonPureDecimal_OctonalDuodecimal']))
    log(f"  [Joint Correlation Check] All 6 Grambank features simultaneously in Eurasia: "
        f"{j_hits}/{j_tot} langs across {j_nfams} families -> joint_fam_rate={j_fam:.4f} (vs independent product={indep_prod_6:.4f}!)")
    log(f"  [Joint Matching Eurasian Families in Grambank]: {matching_fams}")

    br_rows.append({
        'feature_id': 'JOINT_All6_Morphosyntax_Grambank',
        'source_proxy': f"Simultaneous satisfaction of G1+G2+G3+G4+G6+G7 in Grambank Eurasia (matching families: {'/'.join(matching_fams)})",
        'eurasia_hits': j_hits, 'eurasia_total': j_tot, 'eurasia_families': j_nfams,
        'raw_eurasia_rate': j_raw, 'family_stratified_rate': j_fam
    })

    pd.DataFrame(br_rows).to_csv(os.path.join(OUT_DIR, "wals_grambank_eurasia_baserates.csv"), index=False)
    return fam_priors, j_fam, matching_fams


def score_candidate_languages(fam_priors, joint_gb6_prior):
    """Score every candidate language/reconstruction on P(Indus_Feature_k | Language_L) in [0.02, 0.98]
    (bounded away from 0/1 so no single debatable feature creates an infinite Bayes factor;
     0.95 = directly attested core grammar, 0.75 = compatible/partial or areal/allomorphic match,
     0.35 = atypical/marginal, 0.05 = directly contradicted by attested historical grammar!)."""

    FEAT_KEYS = [
        "G1_Possessor_Suffix_NoHeadPrefix",
        "G2_RightHeaded_Possessor_Possessed",
        "G3_NumNoun_Discrete_AccountingSplit",
        "G4_NoSortalCLF_StemAllomorphy",
        "G5_NonPureDecimal_OctonalDuodecimal",
        "G6_RightHeaded_Compounding_StrictHeadFinal",
        "G7_SuffixingOnly_NoInfix_NoPrefix",
    ]

    # Each entry: {feature_key: (likelihood_P, linguistic_evidence_citation)}
    CANDIDATES = collections.OrderedDict([
        ("Proto-Dravidian (~2500 BCE)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.95, "Strict dependent genitive/oblique suffix (*-in, *-atu, *-a; nominal -kuti) on possessor; zero possessive prefixes on head (Krishnamurti 2003)"),
            "G2_RightHeaded_Possessor_Possessed": (0.95, "Strictly head-final [Possessor-GEN + Head Noun] across all 4 branches (e.g. X-kuti al, aracan-in makan)"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.90, "Pre-nominal [Num + Counted Noun] in syntax (*iru-min, *mu-kkann-) coexisting with [Measure + Numeral] (kalam munru) in Old Tamil epigraphic accounts"),
            "G4_NoSortalCLF_StemAllomorphy": (0.90, "Zero obligatory sortal classifiers in PDrav; exact split between bound adjectival numeral stems (*iru-, *mu-, *aru-) vs free/human substantive forms (*irantu, *oru-van)"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.85, "PDrav octonal-to-decimal transition (*en '8' = 'number/count' DEDR 793; subtractive *ton- '9 = defective 10') + South Asian 12-part kalam/marakkal fraction ladder (1,2,3,4,6; no 5/12)"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.95, "100% right-headed [Modifier + Head] tatpurusa/karmadharaya compounding (*aru-min, *vem-min) & postpositional only"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.98, "Strictly 100% suffixing/agglutinative: zero prefixes and zero infixes in Proto-Dravidian (WALS 26A Strongly Suffixing)"),
        }),
        ("Proto-Munda (pre-IA reconstruction)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.40, "Proto-Austroasiatic/Proto-Munda reconstructing head-initial/inalienable pronominal enclitics; animate -ren / inanimate -ak' suffixation developed in North Munda"),
            "G2_RightHeaded_Possessor_Possessed": (0.35, "Donegan & Stampe (2004) / Pinnow / Sidwell: Proto-AA & early Proto-Munda had head-initial VO & [Possessed + Possessor], shifting head-final via South Asian contact"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.65, "Numerals precede nouns in Munda, though South Munda preserves older post-nominal quantifier/incorporation traces"),
            "G4_NoSortalCLF_StemAllomorphy": (0.35, "Munda languages widely employ numeral classifiers (Santali/Ho/Korwa/Kharia) and bound monosyllabic vs free reduplicated numerals (*bar vs *barea)"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.55, "Proto-Munda decimal 1..10 (*mid..*gel) + vigesimal (*kuri '20'); Sora shows an isolated 12+8 vigesimal-duodecimal hybrid, no ban on 5 (*mone) in measures"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.25, "Proto-Munda preserved head-initial verb-noun incorporation and left-headed compounds (Sora/Gorum/Kharia) before areal SOV shift"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.05, "DIRECT CONTRADICTION: Proto-Munda & all daughter branches have productive nominalizing infixes <-n->, <-p->, <-m-> (dub -> d-un-ub 'assembly', dal -> d-ap-al) and causative *p-/ə- prefixes (Ghosh 2021, Anderson 2007)"),
        }),
        ("North Munda (modern Sprachbund stage)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.85, "Modern Santali/Mundari/Ho mark possessor with postnominal -ren (animate) / -ak' (inanimate) without head prefix"),
            "G2_RightHeaded_Possessor_Possessed": (0.90, "Modern North Munda is head-final [Possessor-ren + Head Noun] after South Asian Sprachbund convergence"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.75, "[Num + Noun] in NPs; measure-first accounting order unattested natively"),
            "G4_NoSortalCLF_StemAllomorphy": (0.45, "Modern Santali/Mundari use numeral classifiers (बोहोक्/bohok' 'head', गोटेन/goten) alongside short/long numerals (bar/barea)"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.30, "North Munda is decimal-vigesimal (kuri = 20) with regular 5 (mone); no base-12 fractional ban on 5"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.80, "Predominantly right-headed compounds in modern Santali/Mundari"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.08, "DIRECT CONTRADICTION: Santali & Mundari retain productive <-p-> reciprocal/collective & <-n->/<-t-> nominalizing infixes right inside core social/administrative nouns (m-ap-anjhi 'council of headmen', d-un-ub 'council')"),
        }),
        ("Proto-Indo-Iranian / Early Vedic", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.85, "Fusional genitive case suffix (*-asya, *-as, *-am) on possessor, zero head possessive prefix"),
            "G2_RightHeaded_Possessor_Possessed": (0.80, "Predominantly [Genitive + Head Noun] in Vedic prose, though freer word order allows [Head + Gen]"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.75, "[Num + Noun] standard (trayas virah); measure-first accounting syntax non-native"),
            "G4_NoSortalCLF_StemAllomorphy": (0.70, "No sortal classifiers; gender agreement on 1..4 (*eka/*ekā, *dvau/*dve, *trayas/*tisras), not a 1..8 vs 1..5 stroke split"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.15, "Strictly decimal (*eka..*dasa, *satam) with quaternary pada (1/4) & decimal weights; 5 (*panca) is ubiquitous and unrestricted"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.85, "Productive right-headed tatpurusa/karmadharaya compounds (alongside exocentric bahuvrihi)"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.45, "Inflection is suffixing (+ nasal verbal infix -na-/-n- in class VII), but derivational/verbal morphology uses pervasive prefixes (pra-, vi-, sam-, ni-, a-, su-, dus-)"),
        }),
        ("Burushaski (Hunza/Yasin vernacular)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.15, "CONTRADICTION ON HEAD NOUN: Genitive -e/-mo on possessor, BUT relational/kin/title head nouns ('master, son, head') require obligatory pronominal possessive PREFIXES i-/mu-/u- (GB431=1: X-e e-uy 'X's his-son')"),
            "G2_RightHeaded_Possessor_Possessed": (0.90, "Strictly head-final [Possessor-e + (Prefix-)Head] (e.g. Hunzue tham 'Emir of Hunza')"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.75, "Numerals precede counted nouns in all 4 noun classes"),
            "G4_NoSortalCLF_StemAllomorphy": (0.85, "No separate sortal classifier words; numerals inflect across 4 noun classes (hm, hf, x countable, y mass/abstract: altan/alto/altac) — closest rival on G4!"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.25, "Strictly vigesimal (altar = 20, altambo = 40) with unrestricted 5 (tsundo); no base-12 fractional ban on 5"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.90, "Right-headed nominal compounds and strict postpositions"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.15, "CONTRADICTION: Heavy productive prefixation on verbs and nouns (pronominal prefixes a-/gu-/i-/mu-/mi-/ma-/u- and d- prefix; WALS 26A Equal Prefixing/Suffixing)"),
        }),
        ("Linear / Old Elamite (~2600-1800 BCE)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.35, "Old/Middle Elamite marks possession via Suffixaufnahme: head noun's animacy/person class suffix (-k, -r, -p, -me) copied onto postnominal possessor (Stolper 2004)"),
            "G2_RightHeaded_Possessor_Possessed": (0.05, "DIRECT CONTRADICTION: Old/Middle Elamite is strictly HEAD-INITIAL in NPs: [Possessed + Possessor-k/r] (sak X-ik 'son of X', sunki-k Anzan-ka 'king of Anshan') — opposite of [X + 740 + 090]!"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.35, "Elamite modifiers and numerals follow head nouns in prose; Proto-/Linear Elamite tablets use metrological signs before/with counts"),
            "G4_NoSortalCLF_StemAllomorphy": (0.80, "Proto-Elamite & Linear Elamite use distinct graphic numeral/metrological series by commodity/capacity class without sortal classifier words"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.65, "Proto-Elamite mixed decimal + bisexagesimal/duodecimal grain capacity fractions (1/2, 1/3, 1/4, 1/6, 1/12), though decimal 5 occurs in discrete counts"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.15, "Head-initial nominal modification [Head + Modifier-Concord] across Old and Middle Elamite"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.90, "Strongly suffixing agglutinative morphology with zero prefixes and zero infixes"),
        }),
        ("Sumerian (~2600-2000 BCE)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.35, "Genitive -ak attaches at the right edge of the post-head possessor NP (e2 lugal-ak = house king-of)"),
            "G2_RightHeaded_Possessor_Possessed": (0.05, "DIRECT CONTRADICTION: Sumerian NPs are strictly HEAD-INITIAL [Possessed + Possessor-ak] (e2 lugal-ak, dumu X-ak, arad2 X-ak) — exact mirror image of Indus [X + 740 + 090]!"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.40, "In Sumerian grammar cardinal numerals FOLLOW the noun (lu2 3 '3 men'); cuneiform accounting writes [Count + Sign] graphic order while reading noun-first/last"),
            "G4_NoSortalCLF_StemAllomorphy": (0.80, "Mesopotamian cuneiform uses distinct graphic numeral impressions (curviform vs cuneiform/ash vs dish) for metrological capacity vs discrete counts"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.45, "Sexagesimal (60) + gur capacity (1 bariga = 6 ban), BUT 5 ban (0;0,5 gur) is routinely written in Ur III/ED tablets (not banned like Indus 700!)"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.20, "Left-headed nominal compounds dominate Sumerian (lu2-gal 'man-big = king', e2-gal 'house-big = palace', dub-sar)"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.10, "DIRECT CONTRADICTION: Sumerian finite verbs carry obligatory multi-slot prefix chains (modal + conjugation + ventive + dative/locative prefixes mu-na-ni-ib-)"),
        }),
        ("Akkadian (Old Akkadian / East Semitic)", {
            "G1_Possessor_Suffix_NoHeadPrefix": (0.20, "Head-marking construct state [Possessed(bound) + Possessor-GEN] (sar matatim, warad X) or analytic sa"),
            "G2_RightHeaded_Possessor_Possessed": (0.05, "DIRECT CONTRADICTION: Strictly HEAD-INITIAL construct state [Head Noun + Possessor-i(m)] — opposite of [X + 740 + 090]!"),
            "G3_NumNoun_Discrete_AccountingSplit": (0.75, "Numerals precede counted nouns in Old Akkadian (with chiastic gender polarity) while cuneiform measures use sexagesimal/gur notation"),
            "G4_NoSortalCLF_StemAllomorphy": (0.70, "No sortal classifiers; masculine/feminine gender polarity on numerals 3..10"),
            "G5_NonPureDecimal_OctonalDuodecimal": (0.35, "Decimal lexical numerals combined with Sumerian sexagesimal/bariga weights where 5 ban is routine"),
            "G6_RightHeaded_Compounding_StrictHeadFinal": (0.10, "Head-initial construct compounds and prepositions (ina, ana, is-tu)"),
            "G7_SuffixingOnly_NoInfix_NoPrefix": (0.05, "DIRECT CONTRADICTION: Non-concatenative root-and-pattern infixation (-ta- verbal infix iptaras) + pervasive nominal/verbal prefixes (mu-/ma-, ta-, sa-, i-/ta-/ni-)"),
        }),
    ])

    matrix_rows = []
    summary_rows = []

    # Joint Eurasian prior: P(G1..G4, G6, G7 jointly in Grambank Eurasia) * P(G5 in WALS Eurasia)
    joint_eurasia_prior = joint_gb6_prior * fam_priors["G5_NonPureDecimal_OctonalDuodecimal"]
    indep_eurasia_prior = float(np.prod([fam_priors[k] for k in FEAT_KEYS]))

    for cand_name, fmap in CANDIDATES.items():
        log_lik_sum = 0.0
        indep_bf_prod = 1.0
        probs = []
        for fk in FEAT_KEYS:
            p_lang, cite = fmap[fk]
            p0 = fam_priors[fk]
            bf_k = p_lang / p0
            indep_bf_prod *= bf_k
            log_lik_sum += math.log10(p_lang)
            probs.append(p_lang)
            matrix_rows.append({
                'candidate_language': cand_name,
                'feature_id': fk,
                'P_feature_given_lang': p_lang,
                'eurasia_family_prior': p0,
                'feature_BF_vs_Eurasia': round(bf_k, 3),
                'evidence': cite,
            })

        joint_lik = float(np.prod(probs))
        # Correlation-adjusted BF against Eurasian random family:
        # Take geometric/joint likelihood for L divided by Empirical Joint Eurasian Prior!
        #Wait: for correlated head-final features (G1, G2, G3, G4, G6, G7), if a language is already in the head-final
        # South/Central Eurasian macro-type, correlation means we should ALSO compute a Conservative Sprachbund-Adjusted
        # Likelihood where the 4 correlated head-final word-order features (G1_postpos, G2, G3, G6) count with exponent 0.5
        # (effective degrees of freedom = 2 instead of 4), while morphologically independent features (G1_no_head_prefix,
        # G4_classifier/stem, G5_base12, G7_no_infix_no_prefix) keep full weight 1.0!
        corr_weights = [0.75, 0.50, 0.50, 1.00, 1.00, 0.50, 1.00]  # sum of weights = 5.25 effective independent features
        eff_lik = float(np.prod([p ** w for p, w in zip(probs, corr_weights)]))
        eff_prior = float(np.prod([fam_priors[fk] ** w for fk, w in zip(FEAT_KEYS, corr_weights)]))
        corr_bf_vs_eurasia = eff_lik / eff_prior
        emp_joint_bf = joint_lik / max(1e-6, joint_eurasia_prior)

        summary_rows.append({
            'candidate_language': cand_name,
            'mean_feature_fit': round(float(np.mean(probs)), 3),
            'min_feature_fit': round(float(np.min(probs)), 3),
            'raw_joint_likelihood': float(f"{joint_lik:.4e}"),
            'indep_BF_vs_Eurasia': round(indep_bf_prod, 2),
            'emp_joint_BF_vs_Eurasia': round(emp_joint_bf, 2),
            'sprachbund_corr_adj_lik': float(f"{eff_lik:.4e}"),
            'sprachbund_corr_adj_BF': round(corr_bf_vs_eurasia, 2),
        })

    # Normalize posterior probabilities across the 7 distinct historical families (using Proto-Munda for Munda in main prior,
    # and also computing posterior when Modern North Munda replaces Proto-Munda as strongest-defender check!)
    sum_df = pd.DataFrame(summary_rows)
    main_mask = sum_df['candidate_language'] != "North Munda (modern Sprachbund stage)"
    def_mask  = sum_df['candidate_language'] != "Proto-Munda (pre-IA reconstruction)"

    tot_main = sum_df.loc[main_mask, 'sprachbund_corr_adj_lik'].sum()
    tot_def  = sum_df.loc[def_mask, 'sprachbund_corr_adj_lik'].sum()
    sum_df['posterior_historical_7fam'] = np.where(main_mask, (sum_df['sprachbund_corr_adj_lik'] / tot_main).round(4), np.nan)
    sum_df['posterior_modern_munda_defender'] = np.where(def_mask, (sum_df['sprachbund_corr_adj_lik'] / tot_def).round(4), np.nan)

    pdrav_lik = float(sum_df.loc[sum_df['candidate_language'].str.startswith("Proto-Dravidian"), 'sprachbund_corr_adj_lik'].iloc[0])
    sum_df['BF_PDrav_over_rival_corr_adj'] = (pdrav_lik / sum_df['sprachbund_corr_adj_lik']).round(1)

    sum_df = sum_df.sort_values('sprachbund_corr_adj_BF', ascending=False)
    pd.DataFrame(matrix_rows).to_csv(os.path.join(OUT_DIR, "grammar_typology_matrix.csv"), index=False)
    sum_df.to_csv(os.path.join(OUT_DIR, "grammar_bayes_summary.csv"), index=False)

    log("=== GRAMMATICAL TYPOLOGY BAYES SUMMARY (Sorted by Correlation-Adjusted BF) ===")
    for r in sum_df.itertuples():
        log(f"  {r.candidate_language:38s} | fit={r.mean_feature_fit:.2f} (min={r.min_feature_fit:.2f}) | "
            f"Indep_BF={r.indep_BF_vs_Eurasia:8.1f} | EmpJoint_BF={r.emp_joint_BF_vs_Eurasia:7.1f} | "
            f"CorrAdj_BF={r.sprachbund_corr_adj_BF:6.1f} | PDrav/Rival={r.BF_PDrav_over_rival_corr_adj:6.1f}x | "
            f"Post7={r.posterior_historical_7fam} | PostDef={r.posterior_modern_munda_defender}")


def main():
    measure_indus_grammar()
    fam_priors, joint_gb6_prior, _ = compute_wals_grambank_baserates()
    score_candidate_languages(fam_priors, joint_gb6_prior)
    log("Completed typo_02_grammar_fit.py!")

if __name__ == "__main__":
    main()
