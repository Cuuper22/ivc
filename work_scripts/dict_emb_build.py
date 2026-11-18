#!/usr/bin/env python3
"""dict_emb_build.py -- Build shared multi-language dictionary primary-sense & full-sense tables
and precompute local CPU embeddings (multilingual Model2Vec + dense ONNX BGE-small) once up front
so parallel swarm subagents can run global solvers without CPU contention.

Outputs:
  /tmp/dict_emb/entries_<lang>.parquet (or .csv) & primary_phrases.json & emb_m2v.npy & emb_bge.npy
  work_data/dict_emb/summary.json (tracked metadata + verification stats)
  work_data/dict_emb/tamil_senses_37k.npz (compact float16 vectors + index for ~37.6k Tamil senses)
"""
import os, sys, re, json, time, collections, unicodedata
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

import nltk
nltk.data.path.insert(0, os.path.expanduser("~/nltk_data"))
import sense_common as sc

OUT_TMP = "/tmp/dict_emb"
OUT_REPO = os.path.join(ROOT, "work_data", "dict_emb")
os.makedirs(OUT_TMP, exist_ok=True)
os.makedirs(OUT_REPO, exist_ok=True)

t0 = time.time()
def log(*a):
    print(f"[{time.time()-t0:6.1f}s]", *a, flush=True)

# German keyword supplement for Elamite Hinz-Koch
DE_KW = {
    'number': ['eins', 'zwei', 'drei', 'vier', 'fuenf', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'zwölf', 'hundert', 'zahl', 'beide', 'paar'],
    'measure': ['mass', 'maß', 'gewicht', 'anteil', 'teil', 'ration', 'menge', 'elle', 'voll'],
    'commodity': ['getreide', 'korn', 'gerste', 'weizen', 'mehl', 'öl', 'oel', 'wolle', 'stoff', 'gewand', 'kleid', 'silber', 'gold', 'kupfer', 'bronze', 'metall', 'steuer', 'abgabe', 'tribut', 'lohn', 'preis', 'holz', 'sesam', 'vieh', 'honig'],
    'tool': ['gefäss', 'gefaess', 'topf', 'krug', 'korb', 'kiste', 'pflug', 'messer', 'axt', 'bogen', 'pfeil', 'speer', 'waffe', 'wagen', 'rad', 'schiff', 'boot', 'thron', 'siegel', 'stab', 'becher', 'schale'],
    'person': ['könig', 'koenig', 'herr', 'herrscher', 'fürst', 'fuerst', 'diener', 'knecht', 'sklave', 'mann', 'frau', 'herrin', 'mensch', 'leute', 'jäger', 'bauer', 'schmied', 'weber', 'krieger', 'priester', 'ältester', 'leiter', 'aufseher', 'wächter', 'waechter', 'bote', 'beamter', 'händler', 'hirt', 'träger', 'traeger'],
    'kin': ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'gattin', 'gatte', 'kind', 'sippe', 'stamm', 'familie', 'geschlecht', 'enkel', 'nachkomme'],
    'place': ['stadt', 'dorf', 'haus', 'heim', 'ort', 'platz', 'feld', 'land', 'gebiet', 'bezirk', 'berg', 'fluss', 'festung', 'burg', 'garten', 'weg', 'tor', 'palast', 'hof'],
    'time': ['tag', 'monat', 'jahr', 'nacht', 'morgen', 'abend', 'mond', 'sonne', 'stern', 'zeit', 'regen', 'fest'],
    'deity': ['gott', 'göttin', 'goettin', 'tempel', 'opfer', 'heilig', 'altar', 'kult'],
    'animal': ['fisch', 'vogel', 'rind', 'stier', 'kuh', 'ochse', 'hirsch', 'ziege', 'schaf', 'hund', 'löwe', 'loewe', 'pferd', 'schlange', 'tier'],
    'plant': ['baum', 'blatt', 'gras', 'blume', 'frucht', 'pflanze', 'zweig', 'wurzel', 'rohr', 'palme'],
    'quality': ['gross', 'groß', 'klein', 'hoch', 'gut', 'alt', 'neu', 'jung', 'viel', 'wenig', 'stark', 'weiss', 'schwarz', 'rot', 'lang', 'kurz', 'ganz'],
}

CAT_IDX = {c: i for i, c in enumerate(sc.CATS)}

def clean_any_gloss(g, is_german=False, maxw=8):
    g = re.sub(r'\([^)]*\)', ' ', str(g))
    g = re.sub(r'\[[^\]]*\]', ' ', g)
    out = []
    for p in re.split(r'[;,]', g):
        p = re.sub(r'\s+', ' ', p).strip(' .:/"\'')
        p = re.sub(r'^(n|adj|adv|v|vt|vi|id|cf|esp|also|usu|pl|mfn)\.?\s+', '', p, flags=re.I)
        if not p or len(p) < 2:
            continue
        if not is_german and re.search(r'[^\x00-\x7f]', p):
            continue
        if re.search(r'-pp-|-tt-|-v-|-nt-|\bKoll|\bsyn\b|combination of|english dictionary', p, flags=re.I):
            continue
        p = ' '.join(p.split()[:maxw]).lower()
        if len(p) >= 2 and p not in out:
            out.append(p)
    return out

def get_cat_mask(ph, is_german=False):
    mask = 0
    cats = sc.phrase_cats(ph, use_wn=not is_german)
    for c in cats:
        mask |= (1 << CAT_IDX[c])
    if is_german:
        toks = re.findall(r"[a-zäöüß]+", ph.lower())[:6]
        for c, ws in DE_KW.items():
            for t in toks:
                if any(t == w or (len(w) >= 4 and t.startswith(w)) for w in ws):
                    mask |= (1 << CAT_IDX[c])
    return mask

LEX_DIR = os.path.join(ROOT, "work_data", "lang_m", "lex")
LEX_FILES = sorted([f for f in os.listdir(LEX_DIR) if f.endswith(".tsv")])

phrase_to_id = {}
all_phrases = []
phrase_masks = []

def reg_phrase(ph, is_german=False):
    if ph not in phrase_to_id:
        phrase_to_id[ph] = len(all_phrases)
        all_phrases.append(ph)
        phrase_masks.append(get_cat_mask(ph, is_german=is_german))
    return phrase_to_id[ph]

summary_dicts = {}
tamil_all_senses = []  # (dict_name, entry_id, headword, norm_form, skel, sense_idx, phrase_id)

for fn in LEX_FILES:
    dname = fn[:-4]
    is_de = (dname == "elamite_hinzkoch")
    path = os.path.join(LEX_DIR, fn)
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5:
                continue
            eid, hw, nform, skel, gloss = parts[0], parts[1], parts[2], parts[3], parts[4]
            if not nform or len(nform) < 1:
                continue
            ps = clean_any_gloss(gloss, is_german=is_de)
            if not ps:
                continue
            # Keep sanskrit_mw compact to primary + second sense so total unique phrases stays ~45k-55k
            cap = 25 if dname in ("dedr_tamil", "tamil_wiktionary") else (2 if dname == "sanskrit_mw" else 6)
            ps = ps[:cap]
            pids = [reg_phrase(p, is_german=is_de) for p in ps]
            rows.append((eid, hw, nform, skel, pids[0], "|".join(map(str, pids[:6]))))
            if dname in ("dedr_tamil", "tamil_wiktionary"):
                for sidx, pid in enumerate(pids):
                    tamil_all_senses.append((dname, eid, hw, nform, skel, sidx, pid))
    df = pd.DataFrame(rows, columns=["eid", "hw", "norm", "skel", "p1_id", "p6_ids"])
    df.to_csv(os.path.join(OUT_TMP, f"{dname}.csv"), index=False)
    summary_dicts[dname] = {"rows": len(df), "unique_norm": int(df["norm"].nunique()), "unique_p1": int(df["p1_id"].nunique())}
    log(f"Parsed {dname:28s}: {len(df):6d} rows | total unique phrases so far: {len(all_phrases)}")

# Also register sign picture descriptions so sign shapes share the exact same embedding space
shapes_df = pd.read_csv(os.path.join(ROOT, "work_data", "sign_shapes.csv"), dtype=str).fillna("")
blind_path = os.path.join(ROOT, "work_data", "pictures", "pictures_blind.csv")
blind_df = pd.read_csv(blind_path, dtype=str).fillna("") if os.path.exists(blind_path) else pd.DataFrame()

sign_desc = {}
for r in shapes_df.itertuples():
    s = str(getattr(r, "sign", getattr(r, shapes_df.columns[0]))).zfill(3)
    desc = " ".join(str(getattr(r, c, "")) for c in shapes_df.columns[1:4]).strip()
    if desc:
        sign_desc[s] = clean_any_gloss(desc) or [desc.lower()[:60]]

sign_pids = {}
for s, ps in sign_desc.items():
    sign_pids[s] = reg_phrase(ps[0], is_german=False)

log(f"Total unique sense/shape phrases to embed: {len(all_phrases)} (Tamil sense rows: {len(tamil_all_senses)})")

# 1. Embed ALL phrases with multilingual Model2Vec (covers English + German Elamite in one space)
from model2vec import StaticModel
log("Loading minishlab/potion-multilingual-128M...")
m2v = StaticModel.from_pretrained("minishlab/potion-multilingual-128M")
emb_m2v = m2v.encode(all_phrases).astype(np.float32)
# Mean-center and L2-normalize (fixes anisotropy, matching sense_test.md)
emb_m2v -= emb_m2v.mean(axis=0, keepdims=True)
norms = np.linalg.norm(emb_m2v, axis=1, keepdims=True) + 1e-8
emb_m2v = (emb_m2v / norms).astype(np.float16)
np.save(os.path.join(OUT_TMP, "emb_m2v.npy"), emb_m2v)
log(f"Saved emb_m2v.npy: shape={emb_m2v.shape}, dtype={emb_m2v.dtype}")

# 2. Also embed ALL phrases (and save compact Tamil ~37.6k table) with English BGE-base-distilled (potion-base-32M)
log("Loading minishlab/potion-base-32M (BGE-base distilled)...")
m2v_en = StaticModel.from_pretrained("minishlab/potion-base-32M")
emb_bge = m2v_en.encode(all_phrases).astype(np.float32)
emb_bge -= emb_bge.mean(axis=0, keepdims=True)
emb_bge = (emb_bge / (np.linalg.norm(emb_bge, axis=1, keepdims=True) + 1e-8)).astype(np.float16)
np.save(os.path.join(OUT_TMP, "emb_bge.npy"), emb_bge)
log(f"Saved emb_bge.npy: shape={emb_bge.shape}")

tamil_pid_set = sorted(set([x[6] for x in tamil_all_senses] + list(sign_pids.values())))
bge_vecs = emb_bge[tamil_pid_set]
np.savez_compressed(
    os.path.join(OUT_TMP, "tamil_bge.npz"),
    pids=np.array(tamil_pid_set, dtype=np.int32),
    vecs=bge_vecs,
)
log(f"Saved tamil_bge.npz: Tamil + sign-shape unique phrases = {len(tamil_pid_set)}, shape={bge_vecs.shape}")

# Save phrase lookup & category masks
with open(os.path.join(OUT_TMP, "phrases.json"), "w", encoding="utf-8") as f:
    json.dump({"phrases": all_phrases, "sign_pids": sign_pids, "cats": sc.CATS}, f)
np.save(os.path.join(OUT_TMP, "phrase_masks.npy"), np.array(phrase_masks, dtype=np.int32))
pd.DataFrame(tamil_all_senses, columns=["dict", "eid", "hw", "norm", "skel", "sense_idx", "pid"]).to_csv(
    os.path.join(OUT_TMP, "tamil_all_senses.csv"), index=False
)

# Sanity check cosine similarity on known pairs
def cos_m2v(w1, w2):
    i1, i2 = reg_phrase(w1), reg_phrase(w2)
    if i1 >= len(emb_m2v) or i2 >= len(emb_m2v):
        v = m2v.encode([w1, w2]).astype(np.float32)
        v /= (np.linalg.norm(v, axis=1, keepdims=True) + 1e-8)
        return float(v[0] @ v[1])
    return float(emb_m2v[i1].astype(np.float32) @ emb_m2v[i2].astype(np.float32))

sanity = {
    "grain_vs_barley": round(cos_m2v("grain", "barley"), 3),
    "grain_vs_king": round(cos_m2v("grain", "king"), 3),
    "house_vs_german_haus": round(cos_m2v("house", "haus"), 3),
    "king_vs_german_koenig": round(cos_m2v("king", "könig"), 3),
}
log("Sanity cosines:", sanity)

summary = {
    "total_unique_phrases": len(all_phrases),
    "tamil_sense_rows": len(tamil_all_senses),
    "tamil_unique_phrases_bge": len(tamil_pid_set),
    "m2v_model": "minishlab/potion-multilingual-128M",
    "m2v_dim": int(emb_m2v.shape[1]),
    "bge_model": "minishlab/potion-base-32M",
    "bge_dim": int(bge_vecs.shape[1]),
    "dicts": summary_dicts,
    "sanity_cosines": sanity,
}
with open(os.path.join(OUT_REPO, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
log("Done! Summary written to work_data/dict_emb/summary.json")
