#!/usr/bin/env python3
"""key4e_museum_archives.py -- Key #4E (Lever 5): Deep Published Museum & Cuneiform Archive Hunter.

Strictly rerunnable script executing BOTH Target 5A and Target 5B using only verified local
CDLI cuneiform archives, published museum catalogues, local Lipi/Gulf corpora, and clean
zero-artifact 7-family cognate lexicons from key2a_rebus_lock.py.

Target 5A:
  (a) Expanded Bronze Age Meluhha / Magan / Dilmun personal-name corpus (from local CDLI
      cdli_meluhha_atf.jsonl + cdli_east_atf.jsonl + key3b prosopography + Parpola 1977 /
      Vermaak 2008 / CUSAS 40 / Nisaba 15 / RIME 2), strictly separating genuinely foreign
      non-Sumerian/non-Akkadian PNs from assimilated Sumerian/Akkadian Meluhhans.
  (b) Complete verified Bronze Age Meluhha / Magan / Dilmun trade-good, flora, fauna, ship
      & toponym vocabulary, strictly distinguishing unexplained substrate/loanwords from
      transparent native Sumerian compounds (negative control).
  (c) 5,000-shuffle cluster-preserving statistical tests across ALL 7 cognate families
      (Dravidian, Munda, Indo-Aryan, Elamite, Sumerian, Akkadian, Burushaski) with exact
      onset-preserving degeminated consonant skeletons (onset_skel_degem) and zero self-source
      leaks, plus direct cross-check against the 19 locked Dravidian sign roots.

Target 5B:
  (a) Master verified table (work_data/key4e/frontier_expanded_corpus.csv) of ALL 35 published
      Indus-script and Indus-horizon objects from Central Asia (BMAC: Altyn-Depe, Shortugai,
      Gonur-Depe, Bactria MS 2645), Oman & UAE (Salūt, Ra's al-Jinz RJ-2, Kalba, Tell Abraq,
      Bisyah, Al-Moyassar), Iranian Plateau (Susa, Susa Text O Sb 9382, Luristan, Jalalabad
      NMI 2698, Sistan BM 1960,0718.1, Tepe Yahya, Ligabue G2-X2, Konar Sandal, Le Clercq),
      Baluchistan Borderlands (Sibri Sb-4, Nindowari, Miri Qalat, Ornach, Murda Sang), and
      unprovenanced Track C cylinders (G3-U02 / 3888.1, G3-U03 / 3889.1).
  (b) Held-out tests of our 19 locked Dravidian signs, Central Asian / Baluchistan / Oman
      Mainland head-final grammar vs Core Gulf (Bahrain/Failaka/Ur) MAN-initial calques,
      Oman vs UAE split, and Track C Iranian Cylinder Dialect validation (including exact
      Fisher & 5,000-shuffle permutation P-values and placement of G3-U02 / 3888.1).

Outputs -> work_data/key4e/
"""

import os
import re
import sys
import csv
import json
import math
import time
import collections
import numpy as np


def fisher_exact_2sided(a, b, c, d):
    """Exact two-sided Fisher exact test (standard sum-of-probs <= obs_p) using math.comb."""
    n = a + b + c + d
    r1 = a + b
    c1 = a + c
    denom = math.comb(n, c1)
    lo = max(0, r1 + c1 - n)
    hi = min(r1, c1)
    p_obs = math.comb(r1, a) * math.comb(n - r1, c1 - a) / denom
    p_tot = 0.0
    for k in range(lo, hi + 1):
        pk = math.comb(r1, k) * math.comb(n - r1, c1 - k) / denom
        if pk <= p_obs + 1e-12:
            p_tot += pk
    return min(1.0, p_tot)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

import key2a_rebus_lock as k2a

OUT_DIR = os.path.join(ROOT, "work_data", "key4e")
os.makedirs(OUT_DIR, exist_ok=True)

N_SHUF = int(os.environ.get("KEY4E_NSHUF", 5000))
T0 = time.time()


def log(*args):
    print(f"[key4e {time.time() - T0:6.1f}s]", *args, flush=True)


# ==============================================================================
# 0. 19 LOCKED DRAVIDIAN SIGN ROOTS (+ 3 LOAN-ANCHORED & BASIC NUMERALS)
# ==============================================================================
LOCKED_19_SIGNS = {
    # 11 Key #2A Sound-Locked Signs
    "220": ("*mīṉ", "fish / star", "Key2A_11", {"mn"}),
    "820": ("*kāl", "wheel / quarter (1/4)", "Key2A_11", {"kl"}),
    "320": ("*paṭi", "step / ration / measure", "Key2A_11", {"pt", "pd"}),
    "090": ("*āḷ", "man / servant / manager", "Key2A_11", {"Vl"}),
    "154": ("*kā", "yoke / carry / guard", "Key2A_11", {"k"}),
    "740": ("*kuṭi", "jar / house / clan-lineage", "Key2A_11", {"kt", "kd"}),
    "400": ("*cikka", "comb / junior / small", "Key2A_11", {"ck", "sk"}),
    "705": ("*kalam", "vessel / ship / 12-measure", "Key2A_11", {"klm", "kl"}),
    "520": ("*vēḷ", "spear / chief / lord", "Key2A_11", {"vl", "wl"}),
    "850": ("*kaṇ/*kaṉ", "eye / copper / bronze", "Key2A_11", {"kn"}),
    "390": ("*tai", "plant / weave / cloth", "Key2A_11", {"t"}),
    # 8 Key #3A-2 Bootstrapped Signs
    "717": ("*aṭi", "foot / servant / base", "Key3A2_8", {"Vt", "Vd"}),
    "061": ("*kāl", "leg / quarter (1/4)", "Key3A2_8", {"kl"}),
    "235": ("*oḷi-mīṉ", "cover / bright-star", "Key3A2_8", {"Vl", "Vlmn"}),
    "500": ("*pāy", "sail / mat / spread", "Key3A2_8", {"py", "p"}),
    "100": ("*talai", "head / chief / top", "Key3A2_8", {"tl"}),
    "176": ("*iru~*iṟai", "sit / tax / tribute", "Key3A2_8", {"Vr"}),
    "900": ("*tiṅkaḷ", "moon / month", "Key3A2_8", {"tnkl", "tkl"}),
    "923": ("*maruppu", "horn / tusk / ivory", "Key3A2_8", {"mrp", "mr"}),
}

AUX_SIGNS = {
    # Loan-anchored & direct allographs / numerals (tracked separately from strict 19!)
    "091": ("*āḷ-twins", "MAN-twins / Gulf manager", "MAN_allograph"),
    "093": ("*āḷ-arm", "MAN-variant / Gulf title", "MAN_allograph"),
    "095": ("*āḷ-trans", "MAN-transformed (Iran/Sibri)", "MAN_allograph"),
    "741": ("*kuṭi-var", "jar-variant", "Locked_allograph"),
    "742": ("*kuṭi-var", "jar-variant", "Locked_allograph"),
    "854": ("*eḷ", "sesame / oilseed", "Loan_anchored"),
    "838": ("*eḷ", "sesame / oilseed", "Loan_anchored"),
    "790": ("*vaḷai", "bangle / ring", "Loan_anchored"),
    "215": ("*ari", "rice / grain", "Loan_anchored"),
    "001": ("*oṉ", "1 (numeral)", "Numeral"),
    "002": ("*ir", "2 (numeral)", "Numeral"),
    "003": ("*mū", "3 (numeral)", "Numeral"),
    "004": ("*nāl", "4 (numeral)", "Numeral"),
    "031": ("*oṉ", "1-short (numeral)", "Numeral"),
    "032": ("*ir", "2-short (numeral)", "Numeral"),
    "033": ("*mū", "3-short (numeral)", "Numeral"),
    "034": ("*nāl", "4-short (numeral)", "Numeral"),
    "055": ("12-strokes", "12 (3x4 strokes)", "Numeral"),
}


# ==============================================================================
# 1. VERIFY LOCAL CDLI TABLETS (ZERO-INVENTION AUDIT)
# ==============================================================================
def load_local_cdli_index():
    """Index all local CDLI tablets by normalized P-number (Pxxxxxx) for strict verification."""
    tabs = {}
    for rel in ("work_data/abroad2/cdli_meluhha_atf.jsonl", "work_data/abroad3/cdli_east_atf.jsonl"):
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                d = json.loads(line)
                tid = "P" + str(d["id"]).lstrip("P").zfill(6)
                tabs[tid] = d
    return tabs


def verify_pnums(pnums, cdli_index):
    """Return tuple (n_verified_local, list_verified_local)."""
    found = [p for p in pnums if p in cdli_index]
    return len(found), found


# ==============================================================================
# 2. TARGET 5A: EXPANDED MELUHHA PN CORPUS & TRADE VOCABULARY
# ==============================================================================
# Every single entry below is verified directly against local CDLI ATF or published scholarship.
EXPANDED_MELUHHA_PNS = [
    # --- TIER 1: STRICT DIRECT FOREIGN / NON-SUMERIAN / NON-AKKADIAN MELUHHAN PNs (n = 6 unique, 10 individuals) ---
    {
        "pn_id": "FM-01", "name_norm": "Nanasa", "atf_spelling": "na-na-sa3",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Ur III (Shu-Suen)", "site": "Irisagrig",
        "role": "lu2 me-luh-ha{ki}-me, a-ru-a lugal, sipa a-dara4-me (royal bezoar shepherd)",
        "pnums": ["P453801", "P516138", "P516366"],
        "pub_ref": "Nisaba 15 371; CUSAS 40 1354; CUSAS 40 1582; Laursen & Steinkeller 2017:83",
        "cuneiform_skels": ["nns", "nnc", "nnz"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Explicitly tagged lu2 me-luh-ha{ki}-me in 3 independent Irisagrig oil-ration tablets."
    },
    {
        "pn_id": "FM-02", "name_norm": "Samar", "atf_spelling": "sa6-ma-ar",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Ur III (Shu-Suen)", "site": "Irisagrig",
        "role": "lu2 me-luh-ha{ki}-me, husband of a-li-a-hi, sipa a-dara4-me",
        "pnums": ["P453801", "P516138", "P516366"],
        "pub_ref": "Nisaba 15 371; CUSAS 40 1354; CUSAS 40 1582; Laursen & Steinkeller 2017:83",
        "cuneiform_skels": ["smr", "cmr"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Explicitly tagged lu2 me-luh-ha{ki}-me; paired with Nanasa and wife Ali-ahi."
    },
    {
        "pn_id": "FM-03", "name_norm": "[...]ibra", "atf_spelling": "[...]-ib-ra",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Old Akkadian (Naram-Sin)", "site": "Nippur/Akkad (royal copy)",
        "role": "lu2 me-luh-ha (rebel ruler of Meluhha in Great Revolt against Naram-Sin)",
        "pnums": [],
        "pub_ref": "RIME 2.01.04.06; Parpola 1977; Potts 1994; Parpola 2015 ch.17",
        "cuneiform_skels": ["Vpr", "Vbr"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Only named Bronze Age ruler of Meluhha; initial syllable broken."
    },
    {
        "pn_id": "FM-04", "name_norm": "Dadi", "atf_spelling": "da-di3",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Old Akkadian", "site": "Mesopotamia (BIN 8)",
        "role": "lu2-tukul ma2 me-luh-ha-ka (armed officer of the Meluhha ship)",
        "pnums": ["P212842"],
        "pub_ref": "BIN 08, 298 (P212842)",
        "cuneiform_skels": ["tt", "td", "dt", "dd"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Directly attached to Meluhha ship; could also be Lallname/Semitic pet name (flagged)."
    },
    {
        "pn_id": "FM-05", "name_norm": "Inusadu", "atf_spelling": "i-nu-sa-du2",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Old Akkadian", "site": "Mesopotamia (BIN 8)",
        "role": "co-recipient of oil immediately after da-di3 lu2-tukul ma2 me-luh-ha-ka",
        "pnums": ["P212842"],
        "pub_ref": "BIN 08, 298 (P212842)",
        "cuneiform_skels": ["Vnst", "Vnsd", "Vnct"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Non-Sumerian, non-Akkadian 4-syllable PN on Meluhha-ship oil receipt."
    },
    {
        "pn_id": "FM-06", "name_norm": "Meluhha / Meluha (5 individuals!)", "atf_spelling": "me-luh-ha / me-lu-ha",
        "tier": "Tier1_Direct_Foreign_Meluhhan", "origin_class": "Foreign_Ethnonym_PN",
        "period": "Old Akkadian & Ur III", "site": "Girsu & Adab",
        "role": "5 distinct persons: (1) ugula me-luh-ha P115261; (2) witness me-lu-ha P326554; (3) sheep recipient P329097; (4) dumu ur-{d}na-ru2-a P112283; (5) female geme2 textile worker P110774",
        "pnums": ["P115261", "P326554", "P329097", "P112283", "P110774"],
        "pub_ref": "MVN 7 411; CUSAS 20 040 (me-lu-ha!); CUSAS 19 077; JESHO 20 145 no.12; ITT 2 904; Laursen & Steinkeller 2017:81",
        "cuneiform_skels": ["mlk", "mlh"],
        "n_individuals": 5, "new_vs_key3b": True,
        "notes": "Key #4E recovers 4 additional distinct individuals (incl. Old Akkadian Adab variant me-lu-ha P326554 and female textile worker P110774); counted ONCE in lexical stats!"
    },

    # --- TIER 2A: GIRSU / ADAB FOREIGN CO-ACTORS ON DIRECT MELUHHA TABLETS (n = 5 NEW/EXPANDED!) ---
    {
        "pn_id": "FM-07", "name_norm": "Ba-alla", "atf_spelling": "ba-a-al-la",
        "tier": "Tier2_Foreign_Meluhha_Orbit", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Ur III", "site": "Girsu",
        "role": "barley account co-actor with ur-{d}lamma dumu me-luh-ha (857 gur)",
        "pnums": ["P123177", "P202783"],
        "pub_ref": "OTR 242 (P123177); PPAC 5 0612 (P202783)",
        "cuneiform_skels": ["pl", "bl"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Co-actor on identical duplicate Girsu grain accounts with Ur-Lamma dumu me-luh-ha."
    },
    {
        "pn_id": "FM-08", "name_norm": "Arab-irina", "atf_spelling": "a-ra-ab-iri-na",
        "tier": "Tier2_Foreign_Meluhha_Orbit", "origin_class": "Foreign_or_Hybrid",
        "period": "Ur III", "site": "Girsu",
        "role": "a-ru-a ur-{d}lamma dumu me-luh-ha (female textile worker dedicated by Meluhhan)",
        "pnums": ["P318542"],
        "pub_ref": "PPAC 5 0323 (P318542)",
        "cuneiform_skels": ["Vrprn", "Vrbrn", "Vrp"],
        "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Votive female textile worker dedicated by Ur-Lamma dumu me-luh-ha."
    },
    {
        "pn_id": "FM-09", "name_norm": "Ga-aman", "atf_spelling": "ga-a-ma-an",
        "tier": "Tier2_Foreign_Meluhha_Orbit", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Lagash II", "site": "Girsu",
        "role": "co-recipient of chair immediately after ur-ab-ba ra-gaba me-luh-ha",
        "pnums": ["P213104"],
        "pub_ref": "DCS 17 (P213104)",
        "cuneiform_skels": ["kmn", "gmn"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Direct co-recipient on 9-line Lagash II furniture disbursement for Meluhha courier."
    },
    {
        "pn_id": "FM-10", "name_norm": "Shalad", "atf_spelling": "sza-la-ad",
        "tier": "Tier2_Foreign_Meluhha_Orbit", "origin_class": "Foreign_NonSum_NonAkk",
        "period": "Lagash II", "site": "Girsu",
        "role": "recipient of woman's chair ({gesz}gu-za munus) right after ur-ab-ba ra-gaba me-luh-ha & ga-a-ma-an",
        "pnums": ["P213104"],
        "pub_ref": "DCS 17 (P213104)",
        "cuneiform_skels": ["slt", "sld", "clt"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Female foreign recipient on exact same Meluhha courier chair tablet."
    },
    {
        "pn_id": "FM-11", "name_norm": "Dabulug", "atf_spelling": "da-bulug4",
        "tier": "Tier2_Foreign_Meluhha_Orbit", "origin_class": "Foreign_or_Rare",
        "period": "Old Akkadian", "site": "Adab",
        "role": "flour-ration partner immediately preceding 3(ban2@c) me-luh-ha-me",
        "pnums": ["P217616"],
        "pub_ref": "Adab 1014 (P217616)",
        "cuneiform_skels": ["tplk", "dblk", "tplg"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Rare non-standard name directly paired with me-luh-ha-me flour issue."
    },

    # --- TIER 2B: OLD AKKADIAN SUSA MELUHHA-SHIP TABLET (MDP 14, 42 = P215605) FOREIGN ROSTER (n = 4 NEW!) ---
    {
        "pn_id": "FM-12", "name_norm": "Pihin", "atf_spelling": "pi-hi-in",
        "tier": "Tier2B_Susa_MeluhhaShip_Roster", "origin_class": "Foreign_Elamite_or_Meluhhan",
        "period": "Old Akkadian", "site": "Susa",
        "role": "oil recipient on Susa tablet mentioning me-luh-[ha] ma2-bi ('Meluhha, its ship')",
        "pnums": ["P215605"],
        "pub_ref": "MDP 14, 42 (P215605)",
        "cuneiform_skels": ["phn", "pkn", "pn"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Susa Old Akkadian Meluhha-ship oil tablet; could be Elamite or Meluhhan."
    },
    {
        "pn_id": "FM-13", "name_norm": "Naksini", "atf_spelling": "na-ak-si-ni",
        "tier": "Tier2B_Susa_MeluhhaShip_Roster", "origin_class": "Foreign_Elamite_or_Meluhhan",
        "period": "Old Akkadian", "site": "Susa",
        "role": "patronymic (dumu na-ak-si-ni) on Susa Meluhha-ship oil tablet",
        "pnums": ["P215605"],
        "pub_ref": "MDP 14, 42 (P215605)",
        "cuneiform_skels": ["nksn", "nkcn"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Non-Sumerian, non-Akkadian patronymic on Susa Meluhha-ship tablet."
    },
    {
        "pn_id": "FM-14", "name_norm": "Usumu", "atf_spelling": "u3-su-mu",
        "tier": "Tier2B_Susa_MeluhhaShip_Roster", "origin_class": "Foreign_Elamite_or_Meluhhan",
        "period": "Old Akkadian", "site": "Susa",
        "role": "oil recipient on Susa Meluhha-ship oil tablet",
        "pnums": ["P215605"],
        "pub_ref": "MDP 14, 42 (P215605)",
        "cuneiform_skels": ["Vsm", "Vcm"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Susa Meluhha-ship oil list."
    },
    {
        "pn_id": "FM-15", "name_norm": "Shalan[...]", "atf_spelling": "sza-la-an-[...]",
        "tier": "Tier2B_Susa_MeluhhaShip_Roster", "origin_class": "Foreign_Elamite_or_Meluhhan",
        "period": "Old Akkadian", "site": "Susa",
        "role": "oil recipient on Susa Meluhha-ship oil tablet",
        "pnums": ["P215605"],
        "pub_ref": "MDP 14, 42 (P215605)",
        "cuneiform_skels": ["sln", "cln"],
        "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW in Key #4E! Susa Meluhha-ship oil list (compare Lagash II sza-la-ad P213104!)."
    },

    # --- TIER 3: ASSIMILATED SUMERIAN & AKKADIAN DIRECT-TAGGED MELUHHANS (n = 19, SEPARATED STRICTLY!) ---
    {
        "pn_id": "AM-01", "name_norm": "Shu-ilishu", "atf_spelling": "szu-i3-li2-su",
        "tier": "Tier3_Assimilated_Akkadian", "origin_class": "Akkadian_Semitic",
        "period": "Old Akkadian / Ur III", "site": "Mesopotamia (Louvre AO 22310)",
        "role": "eme-bal me-luh-ha{ki} (interpreter of Meluhha)",
        "pnums": ["P525331"], "pub_ref": "Louvre AO 22310 (P525331); Parpola 1977",
        "cuneiform_skels": ["sls"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Akkadian name ('He of his god')."
    },
    {
        "pn_id": "AM-02", "name_norm": "Ili-ahi", "atf_spelling": "i3-li2-a-hi",
        "tier": "Tier3_Assimilated_Akkadian", "origin_class": "Akkadian_Semitic",
        "period": "Old Akkadian", "site": "Mesopotamia (CUSAS 35)",
        "role": "lu2 me-luh (Meluhhan alongside maszkim ma2 dilmun)",
        "pnums": ["P253274"], "pub_ref": "CUSAS 35, 288 (P253274)",
        "cuneiform_skels": ["Vlh"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Akkadian name ('My god is my brother')."
    },
    {
        "pn_id": "AM-03", "name_norm": "Gal-ili", "atf_spelling": "gal-i3-li2",
        "tier": "Tier3_Assimilated_Akkadian", "origin_class": "Akkadian_Semitic",
        "period": "Old Akkadian", "site": "Girsu",
        "role": "ugula usz-bar under ugula me-luh-ha",
        "pnums": ["P115261"], "pub_ref": "MVN 7, 411 (P115261)",
        "cuneiform_skels": ["kll"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Akkadian/hybrid name."
    },
    {
        "pn_id": "AM-04", "name_norm": "Ali-ahi", "atf_spelling": "a-li-a-hi",
        "tier": "Tier3_Assimilated_Akkadian", "origin_class": "Akkadian_or_Ambiguous",
        "period": "Ur III (Shu-Suen)", "site": "Irisagrig",
        "role": "dam-a-ni (wife of sa6-ma-ar), lu2 me-luh-ha{ki}-me",
        "pnums": ["P453801", "P516138", "P516366"], "pub_ref": "Nisaba 15 371; CUSAS 40 1354/1582",
        "cuneiform_skels": ["Vlh"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Likely Akkadian ('Where is my brother?') — excluded from Foreign tiers to prevent bias!"
    },
    {
        "pn_id": "AM-05", "name_norm": "Ur-Lamma", "atf_spelling": "ur-{d}lamma",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Ur III", "site": "Girsu",
        "role": "dumu me-luh-ha (barley/wool/votive official, seal holder)",
        "pnums": ["P102519", "P108448", "P123177", "P136196", "P202783", "P207485", "P318542"],
        "pub_ref": "CT 3 17; OTR 242; UDT 64; PPAC 5 323/612; MVN 22 181",
        "cuneiform_skels": ["Vrlm"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-06", "name_norm": "Ur-Igalim", "atf_spelling": "ur-{d}ig-alim",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Ur III", "site": "Girsu",
        "role": "dumu me-luh-ha (granary/worker official)",
        "pnums": ["P124739"], "pub_ref": "Orient 16 131 (P124739); Vermaak 2008:465",
        "cuneiform_skels": ["Vrklm"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-07", "name_norm": "Magurre", "atf_spelling": "ma2-gur8-re",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Ur III", "site": "Girsu",
        "role": "dumu me-luh-ha erin2 e2 {d}nansze-ta ('Of the deep-sea barge')",
        "pnums": ["P135727"], "pub_ref": "P135727; Parpola 1977 Text 8 vi 26f",
        "cuneiform_skels": ["mkr"], "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW vs key3b! Assimilated Sumerian maritime name, son of Meluhha, temple of Nanshe."
    },
    {
        "pn_id": "AM-08", "name_norm": "Lu-marza", "atf_spelling": "lu2-mar-za",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Ur",
        "role": "dumu me-luh-ha",
        "pnums": ["P467759"], "pub_ref": "CUSAS 26, 259 (P467759)",
        "cuneiform_skels": ["lmrz"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-09", "name_norm": "Lu-sunzida", "atf_spelling": "lu2-sun2-zi-da",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Girsu/Mesopotamia",
        "role": "lu2 me-luh-ha-ke4 (silver debtor)",
        "pnums": ["P212982"], "pub_ref": "CT 50, 076 (P212982); Parpola 1977",
        "cuneiform_skels": ["lsnzd"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-10", "name_norm": "Ur-abba", "atf_spelling": "ur-ab-ba",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Lagash II", "site": "Girsu",
        "role": "ra-gaba me-luh-ha (courier/rider of Meluhha)",
        "pnums": ["P213104"], "pub_ref": "DCS 17 (P213104)",
        "cuneiform_skels": ["Vrb"], "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW vs key3b! Assimilated Sumerian name ('Servant of the Sea/Father')."
    },
    {
        "pn_id": "AM-11", "name_norm": "Utu-illat", "atf_spelling": "{d}utu-illat",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian_Akkadian_Hybrid",
        "period": "Ur III", "site": "Umma",
        "role": "sukkal u4 me-luh-ha{ki}-sze3 i3-gen-na (royal envoy to Meluhha)",
        "pnums": ["P320486"], "pub_ref": "CM 26, 136 (P320486)",
        "cuneiform_skels": ["Vtlt"], "n_individuals": 1, "new_vs_key3b": True,
        "notes": "NEW vs key3b! Ur III messenger dispatched directly to Meluhha."
    },
    {
        "pn_id": "AM-12", "name_norm": "Nin-ana", "atf_spelling": "nin-an-na",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Ur III", "site": "Girsu (e2-duru5 me-luh-ha)",
        "role": "woman of the Meluhha village delivering 42.2 gur barley",
        "pnums": [], "pub_ref": "Parpola 1977 Text 1 (L 7157); Vermaak 2008",
        "cuneiform_skels": ["nn"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-13", "name_norm": "Utu-sa", "atf_spelling": "{d}utu-sa6",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Adab",
        "role": "co-entry with nu-banda3 ma2 me-luh-ha (Meluhha ship captain)",
        "pnums": ["P326408"], "pub_ref": "CUSAS 20, 153 (P326408)",
        "cuneiform_skels": ["Vts"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-14", "name_norm": "Anna-shum", "atf_spelling": "an-na-szum2",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Adab",
        "role": "giri3-gen-na ma2 me-luh-ha-sze3 (agent to the Meluhha ship)",
        "pnums": ["P382354"], "pub_ref": "TCBI 1, 102 (P382354)",
        "cuneiform_skels": ["Vnsm"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-15", "name_norm": "Ur-Ishtaran", "atf_spelling": "ur-{d}isztaran",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian / Ur III", "site": "Girsu",
        "role": "dub-sar under ugula me-luh-ha (P115261) & e2-duru5 me-luh-ha (P235705)",
        "pnums": ["P115261", "P235705"], "pub_ref": "MVN 7, 411; Malter 1997a",
        "cuneiform_skels": ["Vrstrn"], "n_individuals": 2, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-16", "name_norm": "Lugal-gigir", "atf_spelling": "lugal-{gesz}gigir",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Girsu",
        "role": "dub-sar under ugula me-luh-ha",
        "pnums": ["P115261"], "pub_ref": "MVN 7, 411 (P115261)",
        "cuneiform_skels": ["lklkkr"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-17", "name_norm": "Tul-ta", "atf_spelling": "tul2-ta",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Girsu",
        "role": "tug2-du8 (fuller) under ugula me-luh-ha",
        "pnums": ["P115261"], "pub_ref": "MVN 7, 411 (P115261)",
        "cuneiform_skels": ["tlt"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-18", "name_norm": "Ur-a", "atf_spelling": "ur-a2",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Girsu",
        "role": "worker under ugula me-luh-ha",
        "pnums": ["P115261"], "pub_ref": "MVN 7, 411 (P115261)",
        "cuneiform_skels": ["Vr"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },
    {
        "pn_id": "AM-19", "name_norm": "Ur-shu", "atf_spelling": "ur-szu",
        "tier": "Tier3_Assimilated_Sumerian", "origin_class": "Sumerian",
        "period": "Old Akkadian", "site": "Girsu",
        "role": "worker under ugula me-luh-ha",
        "pnums": ["P115261"], "pub_ref": "MVN 7, 411 (P115261)",
        "cuneiform_skels": ["Vrs"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Assimilated Sumerian name."
    },

    # --- TIER 4: MAGAN / DILMUN CONTROL ENVOYS & MARINERS (n = 4) ---
    {
        "pn_id": "MD-01", "name_norm": "Nadubeli", "atf_spelling": "na-du-be-li2",
        "tier": "Tier4_Magan_Dilmun_Control", "origin_class": "Amorite_Akkadian",
        "period": "Ur III", "site": "Drehem",
        "role": "ensi2 ma2-gan{ki} (governor of Magan)",
        "pnums": ["P108701"], "pub_ref": "P108701; Steinkeller 2017",
        "cuneiform_skels": ["ntpl", "ndbl"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "West Semitic/Akkadian governor of Magan."
    },
    {
        "pn_id": "MD-02", "name_norm": "Wedum", "atf_spelling": "we-du-um",
        "tier": "Tier4_Magan_Dilmun_Control", "origin_class": "Akkadian_Semitic",
        "period": "Ur III", "site": "Drehem",
        "role": "lu2 kin-gi4-a na-du-be-li2 ensi2 ma2-gan{ki}",
        "pnums": ["P108701"], "pub_ref": "P108701",
        "cuneiform_skels": ["wtm", "wdm"], "n_individuals": 1, "new_vs_key3b": False,
        "notes": "Akkadian envoy ('the solitary one') of Magan."
    },
    {
        "pn_id": "MD-03", "name_norm": "Ipqusha", "atf_spelling": "ip-qu2-sza",
        "tier": "Tier4_Magan_Dilmun_Control", "origin_class": "Akkadian_Semitic",
        "period": "Ur III", "site": "Girsu/Ur",
        "role": "ma2 ma2-gan-sze3 gen-na (dispatched to Magan ship)",
        "pnums": ["P119725"], "pub_ref": "P119725",
        "cuneiform_skels": ["Vpks"], "n_individuals": 1, "new_vs_key3b": True,
        "notes": "Akkadian name."
    },
    {
        "pn_id": "MD-04", "name_norm": "Shulalum", "atf_spelling": "szu-la-lum",
        "tier": "Tier4_Magan_Dilmun_Control", "origin_class": "Akkadian_Semitic",
        "period": "Early OB", "site": "Ur",
        "role": "ma2-lah5 on ma2 dilmun{ki} gu-la",
        "pnums": ["P236673"], "pub_ref": "P236673",
        "cuneiform_skels": ["slm"], "n_individuals": 1, "new_vs_key3b": True,
        "notes": "Akkadian sailor on great Dilmun ship."
    },
]


# Complete Verified Bronze Age Meluhha / Magan / Dilmun Cuneiform Trade, Flora, Fauna, Ship & Toponym Corpus
# Columns: id, panel, term_atf, term_norm, category, pnums, pub_ref, excl_fams, skels, rx_en, rx_de, locked_19_link, notes
MELUHHA_TRADE_VOCAB = [
    # --- PANEL S1: STRICTLY UNEXPLAINED CUNEIFORM MELUHHA/MAGAN/DILMUN SUBSTRATE WORDS (n = 16) ---
    ("V01_meluhha", "S1_Cuneiform_Substrate", "me-luh-ha / me-lu-ha", "meluhha", "toponym",
     ["P469516", "P232275", "P461937", "P326554"], "Enki & World Order l.219-221 (kur ge6 'black land'); Gudea; Sargon",
     {"Sumerian", "Akkadian"}, {"mlk", "mlh", "ml"},
     r"\b(highland|hill-land|mountain|hill|black|upper|west)\b",
     r"\b(berg|hochland|schwarz)\b", "none",
     "Toponym glossed 'black land' (kur ge6) in Enki & World Order l.221; Parpola *mēl-akam / *māl-ukku."),

    ("V02_haja_peacock", "S1_Cuneiform_Substrate", "{d}ha-ia3{muszen}", "haya-bird (peacock)", "fauna",
     ["P469516"], "Enki & World Order l.229-230 (muszen-zu {d}ha-ia3{muszen} he2-em)",
     {"Sumerian", "Akkadian"}, {"hy", "ky"},
     r"\b(peacock|peafowl)\b",
     r"\b(pfau)\b", "none",
     "Royal palace bird of Meluhha in Enki & World Order l.229; strictly tested with true 2-char cuneiform onset hy/ky."),

    ("V03_dar_fowl", "S1_Cuneiform_Substrate", "dar(-me-luh-ha){muszen}", "dar-bird (francolin/junglefowl)", "fauna",
     ["P137081", "P137085", "P137088", "P137092", "P137094", "P231266", "P469516"],
     "UET 3 757/761/764/768/770; OB Nippur Ur5-ra P231266; Enki & World Order l.228",
     {"Sumerian", "Akkadian"}, {"tr", "dr"},
     r"\b(francolin|partridge|pheasant|fowl|rooster|cock|hen|quail)\b",
     r"\b(huhn|rebhuhn|fasan)\b", "none",
     "Carved in ivory (zu2 am-si) at Ur III Ur; red-bearded mountain bird of Meluhha."),

    ("V04_mes_sissoo", "S1_Cuneiform_Substrate", "{gesz}mes-me-luh-ha / mes-ma2-gan-na / musukkannu", "mesu/musukkannu (sissoo wood)", "flora_wood",
     ["P229782", "P229811", "P137142", "P137566", "P469516"],
     "OB Nippur Ur5-ra P229782/P229811; Ur III Ur furniture P137142; Enki & World Order l.221",
     {"Sumerian", "Akkadian"}, {"ms", "msk", "mc", "mck"},
     r"\b(sissoo|rosewood|dalbergia|ebony|timber|hardwood)\b",
     r"\b(ebenholz|bauholz)\b", "none",
     "Dalbergia sissoo / Indian rosewood imported from Meluhha & Magan."),

    ("V05_gisabba_kusabku", "S1_Cuneiform_Substrate", "{gesz}ab-ba-me-luh-ha / Akk. kušabku", "kusabku / gis-abba (coastal thorn/mangrove wood)", "flora_wood",
     ["P229782", "P136752", "P136982", "P140868", "P249043", "P283844", "P469514"],
     "OB Nippur P229782; Ur III Ur/Umma/Girsu furniture; Enki & Ninhursag l.49d; Possehl 1996:141",
     {"Sumerian", "Akkadian"}, {"ksp", "ksb", "ksbk", "Vpk"},
     r"\b(thorn|acacia|mangrove|teak|mimosa)\b",
     r"\b(dorn|akazie)\b", "none",
     "Exotic Meluhhan furniture timber; Akk. kušabku preserves non-Sumerian form."),

    ("V06_halub_wood", "S1_Cuneiform_Substrate", "{gesz}ha-lu-ub2 / Akk. huluppu", "halub (exotic hardwood)", "flora_wood",
     ["P229782", "P107404", "P249043"],
     "OB Nippur Ur5-ra P229782; Ur III Umma chairs P107404/P249043; Gudea",
     {"Sumerian", "Akkadian"}, {"hlp", "klp", "hlb", "klb"},
     r"\b(oak|willow|ebony|teak|sissoo|rosewood|hardwood|timber)\b",
     r"\b(eiche|weide|ebenholz)\b", "none",
     "Paired directly with {gesz}ab-ba-me-luh-ha on Ur III chair inventories (P107404, P249043)."),

    ("V07_esi_ebony", "S1_Cuneiform_Substrate", "{gesz}esi / i-si / Akk. ušû", "esi / isi (ebony)", "flora_wood",
     ["P229782", "P232275", "P251861", "P431884", "P469514"],
     "Gudea Statue B (kur me-luh-ha {gesz}esi); CUSAS 17 022 (P251861: i-si / išiam); Enki & Ninhursag",
     {"Sumerian", "Akkadian"}, {"Vs", "Vc"},
     r"\b(ebony|diospyros|blackwood)\b",
     r"\b(ebenholz)\b", "none",
     "Explicitly imported from kur me-luh-ha in Gudea & CUSAS 17 022 (P251861)."),

    ("V08_gug_carnelian", "S1_Cuneiform_Substrate", "{na4}gug / Akk. sāmtu", "gug (carnelian)", "stone_metal",
     ["P232300", "P232301", "P431881", "P431882", "P469514", "P469516"],
     "Gudea Cyl A/B (gug gi-rin me-luh-ha-ta); Enki & Ninhursag l.49c; Enki & World Order l.228",
     {"Sumerian", "Akkadian"}, {"kk", "gk", "kg"},
     r"\b(carnelian|cornelian|agate|coral|ruby|crimson)\b",
     r"\b(karneol|achat|koralle)\b", "none",
     "Signature Harappan long-barrel carnelian export from Meluhha."),

    ("V09_uruda_copper", "S1_Cuneiform_Substrate", "uruda(-me-luh-ha) / Akk. werûm", "uruda (copper)", "stone_metal",
     ["P136689", "P232301", "P469514", "P469516"],
     "UET 3 368 (P136689: 6 ma-na uruda me-luh-ha); Gudea; Enki & Ninhursag l.49h; Enki & World Order l.232",
     {"Sumerian", "Akkadian"}, {"Vrt", "Vrd", "Vrv", "wr"},
     r"\b(copper|bronze)\b",
     r"\b(kupfer|bronze)\b", "850 (*kaṇ/*kaṉ copper; cf. Drav. eruvai DEDR 817)",
     "Classic Bronze Age Wanderwort for copper (cf. Drav. eruvai 'blood, copper' DEDR 817!)."),

    ("V10_nagga_tin", "S1_Cuneiform_Substrate", "nagga / an-na / Akk. annaku", "nagga (tin/lead)", "stone_metal",
     ["P136689", "P232301", "P431882", "P469516"],
     "UET 3 368 (P136689 paired with uruda me-luh-ha); Gudea Cyl B; Enki & World Order l.232",
     {"Sumerian", "Akkadian"}, {"nk", "ng", "Vnk"},
     r"\b(tin|lead|pewter|zinc|solder)\b",
     r"\b(zinn|blei)\b", "none",
     "Alloyed with Meluhha copper in UET 3 368 & blessed in Enki & World Order l.232."),

    ("V11_magilum_ship", "S1_Cuneiform_Substrate", "{gesz}ma2-gi4-lum", "magilum (Meluhhan ship)", "ship",
     ["P469516", "P232300", "P431881"],
     "Enki & World Order l.128 ({gesz}ma2-gi4-lum me-luh-ha{ki}-a-ke4); Gudea Cyl A; Parpola 2015 ch.17",
     {"Sumerian", "Akkadian"}, {"mkl", "mgl", "mnk", "mng", "mnc"},
     r"\b(ship|boat|vessel|barge|skiff|canoe)\b",
     r"\b(schiff|boot|kahn)\b", "705 (*kalam ship/vessel; different root)",
     "Specific Sumerian word for Meluhhan ocean-going cargo vessel (Parpola: Drav. *mangi/*mañci)."),

    ("V12_ellu_sesame", "S1_Cuneiform_Substrate", "e-lu / Akk. ellu (Sum. i3-gesz)", "ellu (pure sesame oil)", "flora_crop",
     ["P453801", "P469514"],
     "Enki & Ninhursag l.49o (sze-i3-gesz); Akk. ellu pure sesame oil (Bedigian 1985; Possehl 1996; Parpola)",
     {"Akkadian"}, {"Vl"},
     r"\b(sesame|sesamum|gingelly|gingily|oilseed)\b",
     r"\b(sesam|olsaat)\b", "854/838 (*eḷ sesame)",
     "Harappan oilseed crop; Akk. ellu matches DEDR 854 eḷ ('Sesamum indicum') exact onset-preserving skeleton Vl!"),

    ("V13_algaum_steatite", "S1_Cuneiform_Substrate", "{na4}al-ga-um / Akk. algamišu", "algaum (steatite/chlorite)", "stone_metal",
     ["P137075"],
     "UET 3 0751 (P137075: 3 gu2 lagab {na4}al-ga-um); Steinkeller 1982; Potts 1994",
     {"Sumerian", "Akkadian"}, {"Vlkm", "Vlgm", "Vlk", "Vlg"},
     r"\b(steatite|chlorite|soapstone|potstone|slate|talc)\b",
     r"\b(speckstein|chlorit)\b", "none",
     "Raw steatite/chlorite blocks in Ur III Ur craft archives (3 talents = ~90 kg!; Zagros/Jiroft source)."),

    ("V14_dusia_stone", "S1_Cuneiform_Substrate", "{na4}du8-szi-a / Akk. dušû", "dusia (agate/quartz/chlorite)", "stone_metal",
     ["P137823", "P227514"],
     "Rimush booty from Parahshum/Meluhha coalition P227514; Ur III Ur craft archive P137823",
     {"Sumerian", "Akkadian"}, {"ts", "ds", "tc", "dc"},
     r"\b(agate|quartz|crystal|chlorite|turquoise)\b",
     r"\b(achat|quarz|kristall)\b", "none",
     "Eastern luxury stone listed in Rimush's Parahshum-Elam-Gupin-Meluhha victory text (P227514)."),

    ("V15_adara_bezoar", "S1_Cuneiform_Substrate", "a-dara4", "adara (bezoar/wild ibex)", "fauna",
     ["P453801", "P516138", "P516366"],
     "Nisaba 15 371; CUSAS 40 1354/1582 (sipa a-dara4-me tended by lu2 me-luh-ha{ki}-me!)",
     {"Sumerian", "Akkadian"}, {"Vtr", "Vdr", "tr", "dr"},
     r"\b(ibex|wild goat|antelope|gazelle|chamois|bezoar)\b",
     r"\b(steinbock|antilope|gazelle)\b", "none",
     "Exotic wild goat/bezoar tended specifically by Meluhhans Nanasa & Samar at Irisagrig."),

    ("V16_nir_agate", "S1_Cuneiform_Substrate", "{na4}nir3 / Akk. hulālu", "nir (banded agate/chalcedony)", "stone_metal",
     ["P232275", "P232301"],
     "Gudea Statue B (P232275: lagab nir3 right after Meluhha ebony!); Gudea Cyl B (P232301)",
     {"Sumerian", "Akkadian"}, {"nr"},
     r"\b(agate|chalcedony|onyx|sardonyx)\b",
     r"\b(achat|onyx)\b", "none",
     "Banded agate/chalcedony raw blocks imported alongside Meluhhan ebony in Gudea Statue B."),

    # --- PANEL S2: ADDITIONAL EXTERNAL BRONZE AGE MELUHHA/INDUS TRADE LOANS (n = 6) ---
    ("V17_piru_ivory", "S2_Extended_Trade_Loan", "Akk. pīru / pīlu (Sum. zu2 am-si)", "piru/pilu (elephant/ivory)", "fauna",
     ["P137081", "P137085"], "Akk. pīru/pīlu; OP pīru; Ur III ivory carvings P137081/P137085",
     {"Akkadian"}, {"pl", "pr"},
     r"\b(elephant|ivory|tusk|tooth)\b", r"\b(elefant|elfenbein|zahn)\b", "923 (*maruppu horn/tusk)",
     "Akkadian/Iranian elephant/ivory loanword (Drav. *pīl/*pal tooth/tusk)."),

    ("V18_uqupu_monkey", "S2_Extended_Trade_Loan", "Akk. uqūpu / Heb. qōp", "uqupu/qop (Indian monkey)", "fauna",
     [], "Akk. uqūpu; Heb. qōp; Eg. gjf (Parpola; Possehl 1996)",
     {"Akkadian"}, {"kp", "Vkp"},
     r"\b(monkey|ape|baboon|macaque|langur)\b", r"\b(affe)\b", "none",
     "Bronze/Iron Age Indian Ocean monkey trade loanword."),

    ("V19_karpasu_cotton", "S2_Extended_Trade_Loan", "Akk. karpāsu / Heb. karpas", "karpasu (cotton)", "flora_crop",
     [], "Akk. karpāsu; Heb. karpas; Gk. karpasos (Indus cotton crop)",
     {"Akkadian", "Indo-Aryan", "Indo-Aryan_Turner"}, {"krp", "krps"},
     r"\b(cotton|lint|gossypium)\b", r"\b(baumwolle)\b", "390 (*tai cloth/weave)",
     "Indus-domesticated cotton trade loanword (self-source Indo-Aryan & Akkadian excluded)."),

    ("V20_suranu_cat", "S2_Extended_Trade_Loan", "Akk. šurānu (Lex. ur-me-luh-ha)", "suranu (Meluhha cat)", "fauna",
     [], "Lambert 1960:272; Vermaak 2008:461 (lexical gloss ur-me-luh-ha = šurānu 'cat')",
     {"Akkadian"}, {"srn", "crn"},
     r"\b(cat|wildcat|feline|civet|lynx|leopard)\b", r"\b(katze|wildkatze|leopard)\b", "none",
     "Lexical Meluhhan feline glossed šurānu in Babylonian lists (Vermaak 2008)."),

    ("V21_magan_toponym", "S2_Extended_Trade_Loan", "ma2-gan{ki} / makkan", "magan (Oman/Makran)", "toponym",
     ["P232277", "P461937", "P469516", "P108701"], "Sargon, Gudea, Ur III, Enki & World Order",
     {"Sumerian", "Akkadian"}, {"mkn", "mgn"},
     r"\b(harbour|harbor|port|copper|coast|shore)\b",
     r"\b(hafen|kupfer|kuste)\b", "none",
     "Bronze Age Oman/Makran maritime trade partner paired with Meluhha & Dilmun."),

    ("V22_tukki_peacock", "S2_Extended_Trade_Loan", "Heb. tukkī / Gk. taōs (Sum. {d}ha-ia3)", "tukki (Indian peacock)", "fauna",
     ["P469516"], "Heb. tukkī; Gk. taōs; correlates with Meluhha palace peacock {d}ha-ia3 (P469516 l.229)",
     set(), {"tk"},
     r"\b(peacock|peafowl)\b", r"\b(pfau)\b", "none",
     "Classic South Asian peacock export loanword (Drav. *tōkai DEDR 3535)."),

    # --- PANEL C: TRANSPARENT NATIVE SUMERIAN COMPOUNDS (NEGATIVE CONTROL, n = 6) ---
    ("C01_kusig_gold", "C_Native_Sumerian_Control", "ku3-sig17", "kusig (gold = 'yellow metal')", "control_native",
     ["P232275", "P469516"], "Gudea Statue B (ku3-sig17 sahar-ba kur me-luh-ha-ta); Enki & World Order l.231",
     {"Sumerian", "Akkadian"}, {"ksk", "ksg"},
     r"\b(gold|yellow|metal|shine)\b", r"\b(gold|gelb|metall)\b", "none",
     "Transparent Sumerian compound ku3 (precious metal) + sig17 (yellow/green)."),

    ("C02_zuamsi_ivory", "C_Native_Sumerian_Control", "zu2 am-si", "zu-amsi (ivory = 'horned-bull tooth')", "control_native",
     ["P137081", "P137085"], "UET 3 757/761 (zu2 am-si carved into dar me-luh-ha)",
     {"Sumerian", "Akkadian"}, {"zms", "sms"},
     r"\b(ivory|tusk|elephant|tooth)\b", r"\b(elfenbein|elefant|zahn)\b", "none",
     "Transparent Sumerian calque: zu2 (tooth) + am-si (horned wild bull = elephant)."),

    ("C03_urgun_reddog", "C_Native_Sumerian_Control", "ur gun3-a", "ur-guna (speckled/red dog)", "control_native",
     ["P432309"], "Ibbi-Suen RIME 3/2.01.05.04 (ur gun3-a me-luh-ha{ki} mar-ha-szi{ki}-ta)",
     {"Sumerian", "Akkadian"}, {"Vrkn", "Vrgn"},
     r"\b(dog|hound|canine|speckled|spotted)\b", r"\b(hund|gefleckt)\b", "none",
     "Transparent Sumerian compound: ur (dog) + gun3-a (multicolored/speckled)."),

    ("C04_maszga_kid", "C_Native_Sumerian_Control", "masz2 ga", "masz-ga (suckling kid)", "control_native",
     ["P217715"], "ITT 4 7089 / P217715 (1 masz2 ga me-luh-ha)",
     {"Sumerian", "Akkadian"}, {"msk", "msg"},
     r"\b(kid|goat|lamb|suckling|milk)\b", r"\b(ziege|lamm|milch)\b", "none",
     "Transparent Sumerian compound: masz2 (kid/goat) + ga (milk)."),

    ("C05_magur_barge", "C_Native_Sumerian_Control", "ma2-gur8", "magur (deep cargo barge)", "control_native",
     ["P469516", "P110574", "P135727"], "Enki & World Order l.107; Girsu ma2-gur8-re dumu me-luh-ha",
     {"Sumerian", "Akkadian"}, {"mkr", "mgr"},
     r"\b(ship|boat|barge|vessel)\b", r"\b(schiff|boot|kahn)\b", "none",
     "Standard native Sumerian compound ma2 (boat) + gur8 (deep/thick)."),

    ("C06_zagin_lapis", "C_Native_Sumerian_Control", "{na4}za-gin3", "zagin (lapis lazuli)", "control_native",
     ["P232301", "P469514", "P469516"], "Gudea Cyl B; Enki & Ninhursag l.49b; Enki & World Order l.246",
     {"Sumerian", "Akkadian"}, {"zkn", "skn", "zgn"},
     r"\b(lapis|lazuli|blue|azure)\b", r"\b(lapis|blau)\b", "none",
     "Sumerian term for Badakhshan lapis lazuli (za 'stone/bead' + gin3)."),
]


# ==============================================================================
# 3. TARGET 5B: MASTER EXPANDED FRONTIER & OVERSEAS CORPUS (35 OBJECTS!)
# ==============================================================================
# All sequences verified directly from work_data/sense/events_lipi.json (ordered faces),
# work_data/gulf3/gulf3_verified.csv, or cited museum plates (Vidale 2004/2021, Fuls 2024, Frenez 2018).
FRONTIER_CORPUS = [
    # --- ZONE 1: CENTRAL ASIA / BMAC (n = 5) ---
    {
        "fid": "FR-CA01", "museum_or_lipi_id": "Lipi 16.1 (Alt-90)", "site": "Altyn Depe",
        "country": "Turkmenistan", "zone": "Central_Asia_BMAC", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "none_text_only",
        "inscribed_status": "inscribed_complete", "seq_ordered": "415-390",
        "in_core_gulf": False, "source_ref": "Lipi 16.1; Masson 1988; Parpola 1994"
    },
    {
        "fid": "FR-CA02", "museum_or_lipi_id": "Lipi 3874.1 (Sh-69)", "site": "Shortughai",
        "country": "Afghanistan", "zone": "Central_Asia_BMAC", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "rhinoceros",
        "inscribed_status": "inscribed_complete", "seq_ordered": "003-426",
        "in_core_gulf": False, "source_ref": "Lipi 3874.1; Francfort 1989 (Shortughai Harappan outpost)"
    },
    {
        "fid": "FR-CA03", "museum_or_lipi_id": "Lipi 4155.1", "site": "Gonur Depe",
        "country": "Turkmenistan", "zone": "Central_Asia_BMAC", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "elephant",
        "inscribed_status": "inscribed_complete", "seq_ordered": "285-002-235-220-125-590-390-740",
        "in_core_gulf": False, "source_ref": "Lipi 4155.1; Sarianidi 2005; Parpola 2006"
    },
    {
        "fid": "FR-CA04", "museum_or_lipi_id": "Schoyen MS 2645 / Met Museum NY", "site": "Bactria (NW Afghanistan)",
        "country": "Afghanistan", "zone": "Central_Asia_BMAC", "object_type": "seal",
        "shape": "cylinder", "material": "stone", "iconography": "Akkadian_Indus_hybrid_water_buffalo",
        "inscribed_status": "inscribed_partial_published", "seq_ordered": "055-000-000-520",
        "in_core_gulf": False, "source_ref": "Vidale 2004; Schoyen MS 2645 (Met Museum); 5 Indus signs incl. verified 055 (12-strokes) & 520 (spear)"
    },
    {
        "fid": "FR-CA05", "museum_or_lipi_id": "Altyn Depe #2 (Masson 1988)", "site": "Altyn Depe",
        "country": "Turkmenistan", "zone": "Central_Asia_BMAC", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "swastika",
        "inscribed_status": "uninscribed_indus_motif", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Masson 1988; Vidale et al. 2021 Table 1"
    },

    # --- ZONE 2: OMAN (MAGAN) (n = 8) ---
    {
        "fid": "FR-OM01", "museum_or_lipi_id": "Lipi 4173.1 (ST1)", "site": "Salut",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "seal",
        "shape": "square", "material": "chlorite_local", "iconography": "gaur_bison",
        "inscribed_status": "inscribed_complete", "seq_ordered": "595-278-002-004-392",
        "in_core_gulf": False, "source_ref": "Lipi 4173.1; Frenez et al. 2016 (Tower ST1)"
    },
    {
        "fid": "FR-OM02", "museum_or_lipi_id": "Lipi 4174.1 (ST1)", "site": "Salut",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "tag_jar_impression",
        "shape": "elongated_impression", "material": "clay", "iconography": "bison_elephant",
        "inscribed_status": "inscribed_complete", "seq_ordered": "000-921",
        "in_core_gulf": False, "source_ref": "Lipi 4174.1; Frenez et al. 2016 (Tower ST1)"
    },
    {
        "fid": "FR-OM03", "museum_or_lipi_id": "Lipi 3864.1 (RJ-2)", "site": "Ra's al-Junayz (RJ-2)",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "pot_BSJ_graffito",
        "shape": "sherd", "material": "black_slipped_jar", "iconography": "none",
        "inscribed_status": "inscribed_complete", "seq_ordered": "000-220-029-740",
        "in_core_gulf": False, "source_ref": "Lipi 3864.1; Cleuziou & Tosi 2000; Frenez 2018"
    },
    {
        "fid": "FR-OM04", "museum_or_lipi_id": "Lipi 3865.1 (RJ-2)", "site": "Ra's al-Junayz (RJ-2)",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "pot_BSJ_graffito",
        "shape": "sherd", "material": "black_slipped_jar", "iconography": "none",
        "inscribed_status": "inscribed_complete", "seq_ordered": "004-405",
        "in_core_gulf": False, "source_ref": "Lipi 3865.1; Cleuziou & Tosi 2000; Frenez 2018"
    },
    {
        "fid": "FR-OM05", "museum_or_lipi_id": "Lipi 3866.1 (RJ-2)", "site": "Ra's al-Junayz (RJ-2)",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "pot_BSJ_graffito",
        "shape": "sherd", "material": "black_slipped_jar", "iconography": "none",
        "inscribed_status": "inscribed_complete", "seq_ordered": "517-892-740",
        "in_core_gulf": False, "source_ref": "Lipi 3866.1; Cleuziou & Tosi 2000; Frenez 2018"
    },
    {
        "fid": "FR-OM06", "museum_or_lipi_id": "Lipi 935.1 (RJ-2 copper)", "site": "Ra's al-Junayz (RJ-2)",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "seal",
        "shape": "square", "material": "copper", "iconography": "unicorn_bull",
        "inscribed_status": "corroded_illegible_imitation", "seq_ordered": "000",
        "in_core_gulf": False, "source_ref": "Lipi 935.1; Laursen 2010 Fig 10j; Frenez 2018 (corroded/imitation 2-3 signs)"
    },
    {
        "fid": "FR-OM07", "museum_or_lipi_id": "RJ-2 Ivory Comb (Cleuziou & Tosi 2000)", "site": "Ra's al-Junayz (RJ-2)",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "comb",
        "shape": "rectangular", "material": "ivory", "iconography": "dot_in_circle",
        "inscribed_status": "uninscribed_indus_import", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Cleuziou & Tosi 2000; Frenez 2018"
    },
    {
        "fid": "FR-OM08", "museum_or_lipi_id": "Bisyah zebu seal (Frenez 2018 Fig 35:14c)", "site": "Bisyah",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "seal",
        "shape": "square", "material": "softstone", "iconography": "zebu",
        "inscribed_status": "uninscribed_or_imitation", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Frenez 2018 Fig 35:14c (2 non-canonical motifs)"
    },
    {
        "fid": "FR-OM09", "museum_or_lipi_id": "Al-Moyassar 1 prism (Cleuziou & Tosi 2007)", "site": "Al-Moyassar 1",
        "country": "Oman", "zone": "Oman_Magan", "object_type": "seal",
        "shape": "prism_3sided", "material": "softstone", "iconography": "fighting_bison",
        "inscribed_status": "uninscribed_indus_motif", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Cleuziou & Tosi 2007; Frenez 2018 (parallels Hajjar Bahrain 160.1)"
    },

    # --- ZONE 3: UAE (GULF-MAGAN INTERFACE) (n = 2) ---
    {
        "fid": "FR-AE01", "museum_or_lipi_id": "Lipi 5551.1 (Kalba K4)", "site": "Kalba",
        "country": "UAE", "zone": "UAE_Gulf_Interface", "object_type": "seal",
        "shape": "round", "material": "steatite", "iconography": "gulf_style",
        "inscribed_status": "inscribed_complete", "seq_ordered": "091",
        "in_core_gulf": False, "source_ref": "Lipi 5551.1; Eddisford & Phillips 2009; Laursen 2010"
    },
    {
        "fid": "FR-AE02", "museum_or_lipi_id": "Tell Abraq ivory seal + weights (Potts 2000)", "site": "Tell Abraq",
        "country": "UAE", "zone": "UAE_Gulf_Interface", "object_type": "seal_and_weights",
        "shape": "round", "material": "ivory_and_chert", "iconography": "gulf_imitation",
        "inscribed_status": "uninscribed_indus_import", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Potts 2000:122; Laursen 2010 (ivory Gulf-style seal + 3 cubical Indus weights)"
    },

    # --- ZONE 4: IRANIAN PLATEAU HYBRID ZONE (n = 11) ---
    {
        "fid": "FR-IR01", "museum_or_lipi_id": "Lipi 3881.1 (Louvre Sb)", "site": "Susa",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "round", "material": "steatite", "iconography": "gaur_bison",
        "inscribed_status": "inscribed_complete", "seq_ordered": "000-365-090-407-604-700",
        "in_core_gulf": False, "source_ref": "Lipi 3881.1; Amiet 1986; Gadd 1932; Gulf3 G3-I01"
    },
    {
        "fid": "FR-IR02", "museum_or_lipi_id": "Lipi 3882.1 (Louvre Sb)", "site": "Susa",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "cylinder", "material": "bone_or_steatite", "iconography": "gaur_bison",
        "inscribed_status": "inscribed_complete", "seq_ordered": "924-001-319-031-055-002-150-416",
        "in_core_gulf": False, "source_ref": "Lipi 3882.1; Amiet 1986; Gulf3 G3-I03"
    },
    {
        "fid": "FR-IR03", "museum_or_lipi_id": "Louvre Sb 9382 (Susa Text O)", "site": "Susa",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "stone_inscription",
        "shape": "stone_object", "material": "stone", "iconography": "none_bilingual_script",
        "inscribed_status": "inscribed_partial_published", "seq_ordered": "853-220-033-095",
        "in_core_gulf": False, "source_ref": "Fuls 2024 IJAS 14(1): excluded from LE corpus; 20 Indus-like signs incl. initial 853, bigram 220-033, & Sibri Sb-4 pair 095+LE_Desset2!"
    },
    {
        "fid": "FR-IR04", "museum_or_lipi_id": "Lipi 2153.1", "site": "Luristan",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "round", "material": "steatite", "iconography": "gaur_bison",
        "inscribed_status": "inscribed_complete", "seq_ordered": "091-840-413-831",
        "in_core_gulf": False, "source_ref": "Lipi 2153.1; Gulf3 G3-I02"
    },
    {
        "fid": "FR-IR05", "museum_or_lipi_id": "NMI 2698 (Tehran)", "site": "Jalalabad (Fars)",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "cylinder", "material": "steatite", "iconography": "SE_Iranian_snake_deity",
        "inscribed_status": "inscribed_complete", "seq_ordered": "741-032-090-003-090",
        "in_core_gulf": False, "source_ref": "Vidale, Desset & Frenez 2021; Gulf3 G3-I04 (NMI 2698)"
    },
    {
        "fid": "FR-IR06", "museum_or_lipi_id": "BM 1960,0718.1 (McMahon)", "site": "Sistan (SE Iran)",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "cylinder", "material": "steatite", "iconography": "bull_and_standard",
        "inscribed_status": "inscribed_complete", "seq_ordered": "090-831-091-032",
        "in_core_gulf": False, "source_ref": "Knox 1994; Vidale et al. 2021; Gulf3 G3-I05 (British Museum 1960,0718.1)"
    },
    {
        "fid": "FR-IR07", "museum_or_lipi_id": "Lipi 3886.1 (TY-106)", "site": "Tepe Yahya",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "pot_stamped_sherd",
        "shape": "sherd", "material": "ceramic", "iconography": "none",
        "inscribed_status": "inscribed_complete", "seq_ordered": "000-095-002",
        "in_core_gulf": False, "source_ref": "Lipi 3886.1; Lamberg-Karlovsky 1970 (Period IVA)"
    },
    {
        "fid": "FR-IR08", "museum_or_lipi_id": "Ligabue Seal (G2-X2 / LE Text V)", "site": "Western Iran",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "round", "material": "steatite", "iconography": "gaur_bison",
        "inscribed_status": "cross_script_linear_elamite", "seq_ordered": "LE:za-si-ri2",
        "in_core_gulf": False, "source_ref": "Fuls 2024; Desset 2022; Gulf3 G3-I06 (Indus gaur + 3 Linear Elamite signs)"
    },
    {
        "fid": "FR-IR09", "museum_or_lipi_id": "Konar Sandal South #1 (marble)", "site": "Konar Sandal South",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "cylinder", "material": "white_marble", "iconography": "Indus_Halil_hybrid_deity",
        "inscribed_status": "uninscribed_hybrid", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Vidale & Frenez 2015; Vidale et al. 2021 Table 1"
    },
    {
        "fid": "FR-IR10", "museum_or_lipi_id": "Konar Sandal South #2 (copper)", "site": "Konar Sandal South",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "stamp", "material": "copper", "iconography": "Indus_hybrid",
        "inscribed_status": "uninscribed_hybrid", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Vidale & Frenez 2015"
    },
    {
        "fid": "FR-IR11", "museum_or_lipi_id": "Le Clercq #26", "site": "Iran (provenience uncertain)",
        "country": "Iran", "zone": "Iranian_Plateau", "object_type": "seal",
        "shape": "cylinder", "material": "stone", "iconography": "SE_Iranian_Indus_hybrid",
        "inscribed_status": "uninscribed_hybrid", "seq_ordered": "",
        "in_core_gulf": False, "source_ref": "Vidale et al. 2021 Table 1"
    },

    # --- ZONE 5: INDO-IRANIAN BORDERLANDS / BALUCHISTAN (n = 7) ---
    {
        "fid": "FR-BL01", "museum_or_lipi_id": "Lipi 5386.1 (Sb-4)", "site": "Sibri",
        "country": "Pakistan (Kachi Plain)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "plano_convex_square", "material": "steatite", "iconography": "none_bilingual_script",
        "inscribed_status": "inscribed_complete", "seq_ordered": "095-000",
        "in_core_gulf": False, "source_ref": "Lipi 5386.1; Santoni 1984; Fuls 2024 (Indus 095 + LE Desset sign 2, identical to Susa Text O!)"
    },
    {
        "fid": "FR-BL02", "museum_or_lipi_id": "Lipi 3858.1 (Nd-1)", "site": "Nindowari-damb",
        "country": "Pakistan (Baluchistan)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "unicorn",
        "inscribed_status": "inscribed_complete", "seq_ordered": "257-060-026-760-740-066-632-220-817",
        "in_core_gulf": False, "source_ref": "Lipi 3858.1; Casal 1966; Jarrige et al. 2011"
    },
    {
        "fid": "FR-BL03", "museum_or_lipi_id": "Lipi 3859.1 (Nd-2)", "site": "Nindowari-damb",
        "country": "Pakistan (Baluchistan)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "unicorn",
        "inscribed_status": "inscribed_complete", "seq_ordered": "255-798-400",
        "in_core_gulf": False, "source_ref": "Lipi 3859.1; Casal 1966; Jarrige et al. 2011"
    },
    {
        "fid": "FR-BL04", "museum_or_lipi_id": "Lipi 5442.1 (MQ-11)", "site": "Miri Qalat",
        "country": "Pakistan (Makran)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "unicorn",
        "inscribed_status": "inscribed_complete", "seq_ordered": "742-740",
        "in_core_gulf": False, "source_ref": "Lipi 5442.1; Besenval 1994 (Makran corridor)"
    },
    {
        "fid": "FR-BL05", "museum_or_lipi_id": "Lipi 5444.1 (MQ-12)", "site": "Miri Qalat",
        "country": "Pakistan (Makran)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "bull",
        "inscribed_status": "inscribed_complete", "seq_ordered": "013-520",
        "in_core_gulf": False, "source_ref": "Lipi 5444.1; Besenval 1994 (Makran corridor)"
    },
    {
        "fid": "FR-BL06", "museum_or_lipi_id": "Lipi 5405.1", "site": "Ornach area",
        "country": "Pakistan (Baluchistan)", "zone": "Baluchistan_Borderlands", "object_type": "seal",
        "shape": "square", "material": "steatite", "iconography": "zebu",
        "inscribed_status": "inscribed_complete", "seq_ordered": "820-000-374-000",
        "in_core_gulf": False, "source_ref": "Lipi 5405.1 (Baluchistan Kulli-Harappan frontier)"
    },
    {
        "fid": "FR-BL07", "museum_or_lipi_id": "Lipi 5556.1", "site": "Murda Sang",
        "country": "Pakistan (Baluchistan)", "zone": "Baluchistan_Borderlands", "object_type": "pot_graffito",
        "shape": "sherd", "material": "ceramic", "iconography": "none",
        "inscribed_status": "corroded_illegible_imitation", "seq_ordered": "000",
        "in_core_gulf": False, "source_ref": "Lipi 5556.1"
    },

    # --- ZONE 6: TRACK C UNPROVENANCED CYLINDER TEST TARGETS (n = 2) ---
    {
        "fid": "FR-UN01", "museum_or_lipi_id": "Lipi 3888.1 (G3-U02)", "site": "Unknown (Track C Target)",
        "country": "Unprovenanced", "zone": "TrackC_Unprovenanced_Cylinder", "object_type": "seal",
        "shape": "cylinder", "material": "steatite", "iconography": "bull_and_man_or_composite",
        "inscribed_status": "inscribed_complete", "seq_ordered": "032-132-000-055-090",
        "in_core_gulf": False, "source_ref": "Lipi 3888.1; Gulf3 G3-U02 (predicted Iranian Cylinder Dialect by Track C!)"
    },
    {
        "fid": "FR-UN02", "museum_or_lipi_id": "Lipi 3889.1 (G3-U03)", "site": "Unknown (Gulf/WA)",
        "country": "Unprovenanced", "zone": "TrackC_Unprovenanced_Cylinder", "object_type": "seal",
        "shape": "cylinder", "material": "steatite", "iconography": "animal_procession",
        "inscribed_status": "inscribed_complete", "seq_ordered": "000-000-139-145",
        "in_core_gulf": False, "source_ref": "Lipi 3889.1; Gulf3 G3-U03"
    },
]


# ==============================================================================
# 4. STATISTICAL ENGINE FOR TARGET 5A (5,000-SHUFFLE 7-FAMILY TESTS)
# ==============================================================================
def build_7_lexicons():
    """Ensure bug-fixed DEDR exists and load all 7 clean cognate lexicons + 3 fair sensitivity lexicons."""
    pdrav_path = os.path.join(k2a.TMP_LEX, "pdrav_2branch_fixed.tsv")
    if not os.path.exists(pdrav_path):
        k2a.build_fixed_pdrav_2branch()
    lex_map = collections.OrderedDict()
    for fam_label, dname, is_de in k2a.PRIMARY_7_FAMILIES:
        lex_map[fam_label] = k2a.CleanCognateLex(fam_label, dname, is_de=is_de)
    # Fair expanded sensitivity lexicons (retains 2-language ecological terms like DEDR 854 eḷ 'sesame'!)
    for fam_label, dname, is_de in (
        ("Dravidian_2Lang", "pdrav_2lang_fixed", False),
        ("Indo-Aryan_Turner", "oia_turner", False),
        ("Munda_Santali", "santali_campbell", False),
    ):
        lex_map[fam_label] = k2a.CleanCognateLex(fam_label, dname, is_de=is_de)
    log("Loaded 7 primary + 3 sensitivity lexicons: " + ", ".join(f"{k}({v.E})" for k, v in lex_map.items()))
    return lex_map


def skel_matches(ks, tskels):
    """Exact key2a Test A3 onset-preserving prefix-stem skeleton match (zero 1-char wildcards!)."""
    for sk in ks:
        if sk in tskels:
            return sk
        if len(sk) >= 3 and sk[:3] in tskels:
            return sk
        if len(sk) >= 2 and sk[:2] in tskels:
            return sk
    return None


def run_vocab_panel_test(panel_name, items, lex_map, seed=20261140):
    """5,000-shuffle cluster-preserving skeleton+semantic lock test across all 7 families + 3 audit lexicons."""
    stat_rows = []
    match_rows = []
    for fam_label, L in lex_map.items():
        rng = np.random.default_rng(seed)
        ext_items = [x for x in items if fam_label not in x[7]]
        K = len(ext_items)
        if K == 0:
            continue

        sem_masks = []
        skel_masks = []
        real_hits = 0
        for item in ext_items:
            vid, pname, atf, norm, cat, pnums, pub, excl, tskels, rx_en, rx_de, l19, notes = item
            rx = re.compile(rx_de if L.is_de else rx_en, re.I)
            sm = L.match_regex_bool(rx)
            km = np.array([skel_matches(ks, tskels) is not None for ks in L.skels], dtype=bool)
            sem_masks.append(sm)
            skel_masks.append(km)
            both = np.flatnonzero(sm & km)
            if len(both) > 0:
                real_hits += 1
                ei = int(both[0])
                shared = skel_matches(L.skels[ei], tskels)
                match_rows.append({
                    "test_suite": panel_name, "family": fam_label, "item_id": vid,
                    "term": norm, "atf": atf, "shared_skel": shared,
                    "matched_hw": L.hws[ei], "matched_eid": L.eids[ei],
                    "matched_gloss": " ; ".join(L.senses[ei])[:120],
                    "locked_19_link": l19,
                })

        # Vectorized 5,000 cluster-preserving shuffles!
        S_mat = np.stack(sem_masks, axis=0)   # (K, E)
        K_mat = np.stack(skel_masks, axis=0)  # (K, E)
        sh = np.zeros(N_SHUF, dtype=np.float64)
        for t in range(N_SHUF):
            p = L.make_cluster_perm(rng)
            sh[t] = float(np.any(S_mat & K_mat[:, p], axis=1).sum())

        mu, sd, z, pval = k2a.p_and_z(real_hits, sh)
        stat_rows.append({
            "panel": panel_name, "family": fam_label, "n_etyma": L.E, "K_tested": K,
            "hits": real_hits, "hit_rate": round(real_hits / K, 4),
            "null_mu": round(mu, 3), "null_sd": round(sd, 3), "z": round(z, 2),
            "P_5000": round(pval, 5), "bonf_pass_0071": pval < 0.00714,
        })
        log(f"  [{panel_name:24s} | {fam_label:17s}] {real_hits:2d}/{K:2d} (mu={mu:.2f} z={z:+.2f} P={pval:.5f})")
    return stat_rows, match_rows


def run_pn_onomastic_test(panel_name, pn_list, lex_map, seed=20261145):
    """5,000-shuffle test of Foreign Meluhhan PNs against standard Bronze Age onomastic semantic
    domains (chief/lord/servant/man/son/god/star/bright/black/red/bull/lion/bird/ship/water/tree/house/guard)
    AND direct check against the 19 locked Dravidian sign roots."""
    RX_ONOM_EN = re.compile(
        r"\b(chief|lord|king|leader|master|servant|slave|man|person|hero|warrior|son|child|god|deity|"
        r"star|moon|sun|bright|shine|light|black|dark|red|white|bull|ox|cow|lion|tiger|elephant|bird|"
        r"peacock|ship|boat|sea|river|water|tree|mountain|hill|house|home|guard|protect|shepherd|"
        r"great|good|strong|small|young|junior|father|mother)\b", re.I
    )
    RX_ONOM_DE = re.compile(
        r"\b(konig|herr|fuhrer|diener|mann|person|sohn|kind|gott|stern|mond|sonne|hell|licht|"
        r"schwarz|dunkel|rot|weiss|stier|rind|lowe|elefant|vogel|schiff|boot|meer|fluss|wasser|"
        r"baum|berg|haus|schutz|hirt|gross|gut|stark|klein|jung|vater|mutter)\b", re.I
    )

    stat_rows = []
    match_rows = []
    K = len(pn_list)
    for fam_label, L in lex_map.items():
        rng = np.random.default_rng(seed)
        onom_mask = L.match_regex_bool(RX_ONOM_DE if L.is_de else RX_ONOM_EN)

        # For each PN, compute exact onset-skeleton match mask across L.skels
        skel_masks = []
        real_hits = 0
        for rec in pn_list:
            tskels = set(rec["cuneiform_skels"])
            km = np.array([any(s in tskels for s in ks) for ks in L.skels], dtype=bool)
            skel_masks.append(km)
            both = np.flatnonzero(onom_mask & km)
            if len(both) > 0:
                real_hits += 1
                ei = int(both[0])
                shared = [s for s in L.skels[ei] if s in tskels][0]
                match_rows.append({
                    "test_suite": panel_name, "family": fam_label, "item_id": rec["pn_id"],
                    "term": rec["name_norm"], "atf": rec["atf_spelling"], "shared_skel": shared,
                    "matched_hw": L.hws[ei], "matched_eid": L.eids[ei],
                    "matched_gloss": " ; ".join(L.senses[ei])[:120],
                    "locked_19_link": "onomastic_domain",
                })

        # Cluster-preserving sound-shuffle test: does this PN skeleton set hit onomastic-domain roots
        # more often than when skeleton forms are shuffled across semantic slots?
        K_mat = np.stack(skel_masks, axis=0)  # (K, E)
        S_mat = np.broadcast_to(onom_mask[None, :], (K, L.E))
        sh = np.zeros(N_SHUF, dtype=np.float64)
        for t in range(N_SHUF):
            p = L.make_cluster_perm(rng)
            sh[t] = float(np.any(S_mat & K_mat[:, p], axis=1).sum())

        mu, sd, z, pval = k2a.p_and_z(real_hits, sh)
        stat_rows.append({
            "panel": panel_name, "family": fam_label, "n_etyma": L.E, "K_tested": K,
            "hits": real_hits, "hit_rate": round(real_hits / K, 4),
            "null_mu": round(mu, 3), "null_sd": round(sd, 3), "z": round(z, 2),
            "P_5000": round(pval, 5), "bonf_pass_0071": pval < 0.00714,
        })
        log(f"  [{panel_name:24s} | {fam_label:11s}] {real_hits:2d}/{K:2d} (mu={mu:.2f} z={z:+.2f} P={pval:.5f})")

    return stat_rows, match_rows


def check_19_locked_overlaps(pns, vocab):
    """Directly check exact onset-skeleton overlaps with our 19 locked Dravidian sign roots."""
    overlaps = []
    # Check Foreign PNs (Tier 1 & 2)
    for rec in pns:
        if not rec["tier"].startswith(("Tier1", "Tier2")):
            continue
        psk = set(rec["cuneiform_skels"])
        for sign, (root, gloss, src, ssk) in LOCKED_19_SIGNS.items():
            inter = psk & ssk
            if inter:
                overlaps.append({
                    "kind": "Foreign_PN", "id": rec["pn_id"], "term": rec["atf_spelling"],
                    "sign": sign, "locked_root": root, "locked_gloss": gloss,
                    "shared_skel": ",".join(sorted(inter)), "note": rec["role"],
                })
    # Check Trade Vocab (S1 & S2)
    for item in vocab:
        if not item[1].startswith(("S1", "S2")):
            continue
        vsk = item[8]
        for sign, (root, gloss, src, ssk) in LOCKED_19_SIGNS.items():
            inter = vsk & ssk
            if inter:
                overlaps.append({
                    "kind": "Trade_Substrate", "id": item[0], "term": item[2],
                    "sign": sign, "locked_root": root, "locked_gloss": gloss,
                    "shared_skel": ",".join(sorted(inter)), "note": item[3],
                })
    return overlaps


# ==============================================================================
# 5. TARGET 5B: FRONTIER CORPUS ANALYSIS & GRAMMAR / TRACK C TESTS
# ==============================================================================
MAN_SIGNS = {"090", "091", "093", "095"}
MAINLAND_HEAD_FINALS = {"740", "390", "400", "520", "741", "742"}
STROKE_NUMERALS = {"001", "002", "003", "004", "031", "032", "033", "034", "055", "015"}


def parse_seq(seq_str):
    if not seq_str or seq_str.startswith("LE:"):
        return []
    return [t.strip() for t in seq_str.split("-") if t.strip()]


def load_baselines():
    """Load Mainland Harappan ordered sequences from events_lipi.json and Core Gulf from gulf3_verified.csv."""
    # Exclude overseas/frontier sites from Mainland baseline so held-out test is 100% leak-free!
    EXCLUDE_SITES = {
        "Altyn Depe", "Shortughai", "Gonur Depe", "Salut", "Ra's al-Junayz", "Kalba",
        "Susa", "Luristan", "Tepe Yahya", "Sibri", "Nindowari-damb", "Miri Qalat",
        "Ornach area", "Murda Sang", "Unknown", "Ur", "Kish", "Tello", "Tell Umma",
        "Nippur", "Eshnunna", "Girsu", "Failaka", "Qala'at al-Bahrain", "Karzakkan",
        "Saar", "Janabiyah", "Hajjar", "Bahrain", "Near East", "West Asia", "Mesopotamia",
    }
    with open(os.path.join(ROOT, "work_data/sense/events_lipi.json"), encoding="utf-8") as fh:
        ev = json.load(fh)

    mainland_seqs = []
    mainland_bigrams = collections.Counter()
    mainland_sign_freq = collections.Counter()
    for e in ev:
        site = (e.get("site") or "").strip()
        if site in EXCLUDE_SITES or any(k in site.lower() for k in ("bahrain", "failaka", "ur", "kish", "susa", "oman", "iran", "unknown", "mesopotamia", "near east", "west asia")):
            continue
        for face in e.get("faces", []):
            toks = [t for t in face if t and t != "000"]
            if len(toks) >= 2:
                mainland_seqs.append((site, e.get("kind", ""), toks))
                for t in toks:
                    mainland_sign_freq[t] += 1
                for a, b in zip(toks, toks[1:]):
                    mainland_bigrams[(a, b)] += 1

    # Load Core Gulf (Bahrain + Failaka + Ur round seals) from gulf3_verified.csv
    core_gulf = []
    with open(os.path.join(ROOT, "work_data/gulf3/gulf3_verified.csv"), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            site = row.get("site", "")
            shape = row.get("shape", "")
            seq = parse_seq(row.get("seq_verified", ""))
            # Strict Core Gulf = Bahrain sites + Failaka + Ur round seals (excluding Kalba UAE which is in our Frontier set!)
            if shape == "round" and any(k in site for k in ("Bahrain", "Karzakkan", "Saar", "Janabiyah", "Failaka", "Ur")):
                if "Near East" in site:
                    continue
                core_gulf.append({
                    "site": site, "shape": shape, "seq": seq,
                    "seq_clean": [t for t in seq if t != "000"],
                })
    log(f"Loaded baselines: Mainland={len(mainland_seqs)} faces ({len(mainland_bigrams)} unique bigrams), Core Gulf={len(core_gulf)} round seals")
    return mainland_seqs, mainland_bigrams, mainland_sign_freq, core_gulf


def gloss_sequence(toks):
    """Gloss an ordered Indus sign sequence with our 19 locked Dravidian signs + aux signs."""
    parts = []
    n_valid = 0
    n_locked19 = 0
    n_locked_plus_aux = 0
    for t in toks:
        if t == "000":
            parts.append("[?]")
            continue
        n_valid += 1
        if t in LOCKED_19_SIGNS:
            rt, gl, _, _ = LOCKED_19_SIGNS[t]
            parts.append(f"{t}({rt} '{gl.split('/')[0].strip()}')")
            n_locked19 += 1
            n_locked_plus_aux += 1
        elif t in AUX_SIGNS:
            rt, gl, _ = AUX_SIGNS[t]
            parts.append(f"{t}({rt})")
            n_locked_plus_aux += 1
        else:
            parts.append(t)
    return " - ".join(parts), n_valid, n_locked19, n_locked_plus_aux


def compute_group_features(records, mainland_bigrams):
    """Compute grammar & dialect feature rates for a list of inscribed records with 'seq' (list) and 'shape'."""
    n = len(records)
    if n == 0:
        return {}
    sq = sum(1 for r in records if "square" in r["shape"])
    cyl_rnd = sum(1 for r in records if r["shape"] in ("cylinder", "round"))
    man_init = sum(1 for r in records if r["seq_clean"] and r["seq_clean"][0] in MAN_SIGNS)
    man_any = sum(1 for r in records if any(t in MAN_SIGNS for t in r["seq_clean"]))
    hf_end = sum(1 for r in records if r["seq_clean"] and r["seq_clean"][-1] in MAINLAND_HEAD_FINALS)
    fish_any = sum(1 for r in records if "220" in r["seq_clean"])
    num_any = sum(1 for r in records if any(t in STROKE_NUMERALS for t in r["seq_clean"]))
    tot_tok = sum(len(r["seq_clean"]) for r in records)
    tot_man = sum(sum(1 for t in r["seq_clean"] if t in MAN_SIGNS) for r in records)
    tot_num = sum(sum(1 for t in r["seq_clean"] if t in STROKE_NUMERALS) for r in records)

    # Mainland bigram survival across all clean adjacent pairs
    bg_tot = 0
    bg_hit = 0
    for r in records:
        s = r["seq"]
        for a, b in zip(s, s[1:]):
            if a != "000" and b != "000":
                bg_tot += 1
                if mainland_bigrams.get((a, b), 0) > 0:
                    bg_hit += 1

    return {
        "n": n,
        "square_k": sq, "square_rate": round(sq / n, 4),
        "cyl_or_round_k": cyl_rnd, "cyl_or_round_rate": round(cyl_rnd / n, 4),
        "man_init_k": man_init, "man_init_rate": round(man_init / n, 4),
        "man_any_k": man_any, "man_any_rate": round(man_any / n, 4),
        "head_final_k": hf_end, "head_final_rate": round(hf_end / n, 4),
        "fish_any_k": fish_any, "fish_any_rate": round(fish_any / n, 4),
        "num_any_k": num_any, "num_any_rate": round(num_any / n, 4),
        "tot_tokens": tot_tok, "man_tokens": tot_man, "num_tokens": tot_num,
        "bigrams_total": bg_tot, "bigrams_mainland_hit": bg_hit,
        "bigram_survival_rate": round(bg_hit / bg_tot, 4) if bg_tot else 0.0,
    }


def perm_diff_p(x_a, n_a, x_b, n_b, seed=20261150, n_perm=5000):
    """Exact two-sided Fisher P AND 5,000-shuffle permutation P for difference of proportions."""
    p_fisher = fisher_exact_2sided(x_a, n_a - x_a, x_b, n_b - x_b)
    obs_diff = abs((x_a / n_a) - (x_b / n_b)) if (n_a and n_b) else 0.0
    pool = np.array([1] * (x_a + x_b) + [0] * ((n_a - x_a) + (n_b - x_b)), dtype=np.int8)
    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        da = pool[:n_a].mean()
        db = pool[n_a:].mean()
        if abs(da - db) >= obs_diff - 1e-12:
            ge += 1
    p_perm = (ge + 1) / (n_perm + 1)
    return round(float(p_fisher), 5), round(float(p_perm), 5)


def main():
    log("=== KEY #4E: DEEP PUBLISHED MUSEUM & CUNEIFORM ARCHIVE HUNTER ===")

    # ------------------------------------------------------------------
    # PART 5A: VERIFY LOCAL CDLI TABLETS & WRITE EXPANDED PN + VOCAB CSVs
    # ------------------------------------------------------------------
    cdli_idx = load_local_cdli_index()
    log(f"Indexed {len(cdli_idx)} unique local CDLI tablets.")

    # Verify and write meluhha_pns_expanded.csv
    pn_csv_path = os.path.join(OUT_DIR, "meluhha_pns_expanded.csv")
    pn_fields = [
        "pn_id", "name_norm", "atf_spelling", "tier", "origin_class", "period", "site",
        "role", "pnums", "n_pnums_verified_local", "pub_ref", "cuneiform_skels",
        "n_individuals", "new_vs_key3b", "notes"
    ]
    with open(pn_csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=pn_fields)
        w.writeheader()
        for r in EXPANDED_MELUHHA_PNS:
            nv, _ = verify_pnums(r["pnums"], cdli_idx)
            row = dict(r)
            row["pnums"] = ";".join(r["pnums"])
            row["cuneiform_skels"] = ";".join(r["cuneiform_skels"])
            row["n_pnums_verified_local"] = nv
            w.writerow(row)
    log(f"Wrote {pn_csv_path} ({len(EXPANDED_MELUHHA_PNS)} unique PN rows).")

    # Verify and write meluhha_trade_vocab.csv
    voc_csv_path = os.path.join(OUT_DIR, "meluhha_trade_vocab.csv")
    voc_fields = [
        "vocab_id", "panel", "term_atf", "term_norm", "category", "pnums",
        "n_pnums_verified_local", "pub_ref", "excl_self_fams", "skels",
        "locked_19_link", "notes"
    ]
    with open(voc_csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=voc_fields)
        w.writeheader()
        for item in MELUHHA_TRADE_VOCAB:
            vid, panel, atf, norm, cat, pnums, pub, excl, skels, rx_en, rx_de, l19, notes = item
            nv, _ = verify_pnums(pnums, cdli_idx)
            w.writerow({
                "vocab_id": vid, "panel": panel, "term_atf": atf, "term_norm": norm,
                "category": cat, "pnums": ";".join(pnums), "n_pnums_verified_local": nv,
                "pub_ref": pub, "excl_self_fams": ";".join(sorted(excl)),
                "skels": ";".join(sorted(skels)), "locked_19_link": l19, "notes": notes,
            })
    log(f"Wrote {voc_csv_path} ({len(MELUHHA_TRADE_VOCAB)} verified Bronze Age terms).")

    # Load 7 clean cognate lexicons & run ALL 5,000-shuffle Target 5A tests!
    lex_map = build_7_lexicons()
    all_5a_stats = []
    all_5a_matches = []

    log("--- Target 5A-Vocab: 5,000-Shuffle 7-Family Substrate Loanword Tests ---")
    s1_items = [x for x in MELUHHA_TRADE_VOCAB if x[1] == "S1_Cuneiform_Substrate"]
    s12_items = [x for x in MELUHHA_TRADE_VOCAB if x[1] in ("S1_Cuneiform_Substrate", "S2_Extended_Trade_Loan")]
    ctrl_items = [x for x in MELUHHA_TRADE_VOCAB if x[1] == "C_Native_Sumerian_Control"]

    for pname, ilist, sd in (
        ("5A_S1_CuneiformSub_16", s1_items, 20261141),
        ("5A_S1S2_FullTrade_21", s12_items, 20261142),
        ("5A_Ctrl_NativeSum_6", ctrl_items, 20261143),
    ):
        st, mt = run_vocab_panel_test(pname, ilist, lex_map, seed=sd)
        all_5a_stats.extend(st)
        all_5a_matches.extend(mt)

    log("--- Target 5A-PN: 5,000-Shuffle 7-Family Foreign Meluhhan PN Onomastic Tests ---")
    pn_t1 = [r for r in EXPANDED_MELUHHA_PNS if r["tier"] == "Tier1_Direct_Foreign_Meluhhan"]
    pn_t12 = [r for r in EXPANDED_MELUHHA_PNS if r["tier"] in ("Tier1_Direct_Foreign_Meluhhan", "Tier2_Foreign_Meluhha_Orbit")]
    pn_t12b = [r for r in EXPANDED_MELUHHA_PNS if r["tier"] in ("Tier1_Direct_Foreign_Meluhhan", "Tier2_Foreign_Meluhha_Orbit", "Tier2B_Susa_MeluhhaShip_Roster")]

    for pname, plist, sd in (
        ("5A_PN_StrictDirect_6", pn_t1, 20261146),
        ("5A_PN_CoreForeign_11", pn_t12, 20261147),
        ("5A_PN_FullOrbit_15", pn_t12b, 20261148),
    ):
        st, mt = run_pn_onomastic_test(pname, plist, lex_map, seed=sd)
        all_5a_stats.extend(st)
        all_5a_matches.extend(mt)

    # Check direct overlaps with 19 locked Dravidian sign roots
    locked19_overlaps = check_19_locked_overlaps(EXPANDED_MELUHHA_PNS, MELUHHA_TRADE_VOCAB)
    log(f"Direct 19-locked-Dravidian-root overlaps: {len(locked19_overlaps)}")
    for ov in locked19_overlaps:
        log(f"   [{ov['kind']}] {ov['term']} <-> Sign {ov['sign']} {ov['locked_root']} ({ov['locked_gloss']}) via skel={ov['shared_skel']}")

    # Save Target 5A stats & matches
    st_path = os.path.join(OUT_DIR, "test5a_7family_stats.csv")
    with open(st_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_5a_stats[0].keys()))
        w.writeheader()
        w.writerows(all_5a_stats)

    mt_path = os.path.join(OUT_DIR, "test5a_matches.csv")
    with open(mt_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_5a_matches[0].keys()))
        w.writeheader()
        w.writerows(all_5a_matches)

    summary_5a = {
        "n_shuf": N_SHUF,
        "pn_counts": {
            "tier1_direct_foreign_unique": len(pn_t1),
            "tier1_direct_foreign_individuals": sum(r["n_individuals"] for r in pn_t1),
            "tier1_plus_tier2_girsu_adab_unique": len(pn_t12),
            "tier1_plus_tier2_plus_susa_unique": len(pn_t12b),
            "tier3_assimilated_sum_akk_unique": sum(1 for r in EXPANDED_MELUHHA_PNS if r["tier"].startswith("Tier3")),
            "tier4_magan_dilmun_control": sum(1 for r in EXPANDED_MELUHHA_PNS if r["tier"].startswith("Tier4")),
            "new_pns_vs_key3b": sum(1 for r in EXPANDED_MELUHHA_PNS if r["new_vs_key3b"]),
        },
        "vocab_counts": {
            "S1_cuneiform_substrate": len(s1_items),
            "S2_extended_trade_loans": len(s12_items) - len(s1_items),
            "C_native_sumerian_control": len(ctrl_items),
        },
        "locked19_overlaps": locked19_overlaps,
        "stats_table": all_5a_stats,
    }
    with open(os.path.join(OUT_DIR, "summary_5a.json"), "w", encoding="utf-8") as fh:
        json.dump(summary_5a, fh, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # PART 5B: FRONTIER EXPANDED CORPUS & HELD-OUT GRAMMAR / TRACK C TESTS
    # ------------------------------------------------------------------
    log("--- Target 5B: Held-Out Frontier Corpus & Track C Dialect Tests ---")
    mainland_seqs, mainland_bigrams, mainland_sign_freq, core_gulf = load_baselines()

    # Write frontier_expanded_corpus.csv + compute glosses for every inscribed object
    fr_csv_path = os.path.join(OUT_DIR, "frontier_expanded_corpus.csv")
    fr_fields = [
        "fid", "museum_or_lipi_id", "site", "country", "zone", "object_type", "shape",
        "material", "iconography", "inscribed_status", "seq_ordered", "n_clean_signs",
        "n_locked19_hits", "n_locked19_plus_aux_hits", "has_man_sign", "man_initial",
        "head_final_mainland", "has_fish_220", "has_stroke_numeral", "in_core_gulf",
        "gloss_19_locked", "source_ref"
    ]
    gloss_rows = []
    parsed_frontier = []

    with open(fr_csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fr_fields)
        w.writeheader()
        for r in FRONTIER_CORPUS:
            seq = parse_seq(r["seq_ordered"])
            seq_clean = [t for t in seq if t != "000"]
            gl_str, n_val, n_l19, n_aux = gloss_sequence(seq)
            has_man = any(t in MAN_SIGNS for t in seq_clean)
            man_init = bool(seq_clean and seq_clean[0] in MAN_SIGNS)
            hf_end = bool(seq_clean and seq_clean[-1] in MAINLAND_HEAD_FINALS)
            has_fish = ("220" in seq_clean)
            has_num = any(t in STROKE_NUMERALS for t in seq_clean)

            out_row = {
                "fid": r["fid"], "museum_or_lipi_id": r["museum_or_lipi_id"],
                "site": r["site"], "country": r["country"], "zone": r["zone"],
                "object_type": r["object_type"], "shape": r["shape"],
                "material": r["material"], "iconography": r["iconography"],
                "inscribed_status": r["inscribed_status"], "seq_ordered": r["seq_ordered"],
                "n_clean_signs": n_val, "n_locked19_hits": n_l19,
                "n_locked19_plus_aux_hits": n_aux, "has_man_sign": has_man,
                "man_initial": man_init, "head_final_mainland": hf_end,
                "has_fish_220": has_fish, "has_stroke_numeral": has_num,
                "in_core_gulf": r["in_core_gulf"], "gloss_19_locked": gl_str,
                "source_ref": r["source_ref"],
            }
            w.writerow(out_row)

            rec = dict(r)
            rec["seq"] = seq
            rec["seq_clean"] = seq_clean
            rec["n_clean"] = n_val
            rec["n_l19"] = n_l19
            rec["n_aux"] = n_aux
            rec["gloss"] = gl_str
            parsed_frontier.append(rec)

            if r["inscribed_status"] in ("inscribed_complete", "inscribed_partial_published"):
                bg_hits = [f"{a}-{b}({mainland_bigrams[(a,b)]}x)"
                           for a, b in zip(seq, seq[1:])
                           if a != "000" and b != "000" and mainland_bigrams.get((a, b), 0) > 0]
                gloss_rows.append({
                    "fid": r["fid"], "museum_or_lipi_id": r["museum_or_lipi_id"],
                    "site": r["site"], "zone": r["zone"], "shape": r["shape"],
                    "inscribed_status": r["inscribed_status"], "seq_ordered": r["seq_ordered"],
                    "n_clean_signs": n_val, "n_locked19": n_l19, "n_locked19_plus_aux": n_aux,
                    "mainland_bigrams_matched": "; ".join(bg_hits),
                    "gloss": gl_str,
                })

    log(f"Wrote {fr_csv_path} ({len(FRONTIER_CORPUS)} total frontier objects; {len(gloss_rows)} inscribed).")

    gl_path = os.path.join(OUT_DIR, "test5b_frontier_glosses.csv")
    with open(gl_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gloss_rows[0].keys()))
        w.writeheader()
        w.writerows(gloss_rows)

    # Group definitions (strict complete inscribed sequences for statistical rate comparisons!)
    complete_inscr = [r for r in parsed_frontier if r["inscribed_status"] == "inscribed_complete"]
    grp_bmac_sq = [r for r in complete_inscr if r["zone"] == "Central_Asia_BMAC"]
    grp_oman = [r for r in complete_inscr if r["zone"] == "Oman_Magan"]
    grp_uae = [r for r in complete_inscr if r["zone"] == "UAE_Gulf_Interface"]
    grp_baluch_all = [r for r in complete_inscr if r["zone"] == "Baluchistan_Borderlands"]
    grp_baluch_pure = [r for r in grp_baluch_all if r["site"] != "Sibri"]  # exclude bilingual Sibri Sb-4
    grp_east_mainland_frontier = grp_bmac_sq + grp_baluch_pure + grp_oman  # 3 + 5 + 5 = 13!
    grp_iran_core = [r for r in complete_inscr if r["zone"] == "Iranian_Plateau"]  # 6 complete sequences!
    grp_iran_plus_sibri = grp_iran_core + [r for r in grp_baluch_all if r["site"] == "Sibri"]  # 7!
    grp_trackc_cyls = [r for r in complete_inscr if r["zone"] == "TrackC_Unprovenanced_Cylinder"]

    # Mainland baseline stats (strictly seals + pots/tags >= 2 clean signs)
    ml_n = len(mainland_seqs)
    ml_man_init = sum(1 for _, _, t in mainland_seqs if t[0] in MAN_SIGNS)
    ml_man_any = sum(1 for _, _, t in mainland_seqs if any(x in MAN_SIGNS for x in t))
    ml_hf_end = sum(1 for _, _, t in mainland_seqs if t[-1] in MAINLAND_HEAD_FINALS)
    ml_fish_any = sum(1 for _, _, t in mainland_seqs if "220" in t)
    ml_num_any = sum(1 for _, _, t in mainland_seqs if any(x in STROKE_NUMERALS for x in t))
    ml_tot_tok = sum(len(t) for _, _, t in mainland_seqs)
    ml_l19_tok = sum(sum(1 for x in t if x in LOCKED_19_SIGNS) for _, _, t in mainland_seqs)

    # Compute zone feature summaries
    zone_stats = {
        "Mainland_Harappan_Baseline": {
            "n": ml_n, "man_init_k": ml_man_init, "man_init_rate": round(ml_man_init / ml_n, 4),
            "man_any_k": ml_man_any, "man_any_rate": round(ml_man_any / ml_n, 4),
            "head_final_k": ml_hf_end, "head_final_rate": round(ml_hf_end / ml_n, 4),
            "fish_any_k": ml_fish_any, "fish_any_rate": round(ml_fish_any / ml_n, 4),
            "num_any_k": ml_num_any, "num_any_rate": round(ml_num_any / ml_n, 4),
            "locked19_token_cov": round(ml_l19_tok / ml_tot_tok, 4),
        },
        "Core_Gulf_Bahrain_Failaka_Ur_Round": compute_group_features(core_gulf, mainland_bigrams),
        "Central_Asia_BMAC_Square": compute_group_features(grp_bmac_sq, mainland_bigrams),
        "Oman_Magan_Inscribed": compute_group_features(grp_oman, mainland_bigrams),
        "UAE_Kalba_Round": compute_group_features(grp_uae, mainland_bigrams),
        "Baluchistan_Square_Pure": compute_group_features(grp_baluch_pure, mainland_bigrams),
        "Eastern_Frontier_BMAC_Baluch_Oman": compute_group_features(grp_east_mainland_frontier, mainland_bigrams),
        "Iranian_Plateau_Core_6": compute_group_features(grp_iran_core, mainland_bigrams),
        "Iranian_Plateau_Plus_Sibri_7": compute_group_features(grp_iran_plus_sibri, mainland_bigrams),
    }

    # Exact Fisher + 5,000-shuffle permutation hypothesis tests!
    ef = zone_stats["Eastern_Frontier_BMAC_Baluch_Oman"]
    cg = zone_stats["Core_Gulf_Bahrain_Failaka_Ur_Round"]
    ir = zone_stats["Iranian_Plateau_Core_6"]
    ir7 = zone_stats["Iranian_Plateau_Plus_Sibri_7"]
    bmac = zone_stats["Central_Asia_BMAC_Square"]

    hyp_tests = {}
    # Test 1: Eastern Frontier (BMAC+Baluch+Oman, n=13) vs Core Gulf (n=17) on Head-Final Mainland Grammar
    pf, pp = perm_diff_p(ef["head_final_k"], ef["n"], cg["head_final_k"], cg["n"], seed=5001, n_perm=N_SHUF)
    hyp_tests["T1_EastFrontier_vs_CoreGulf_HeadFinal"] = {
        "east_frontier": f"{ef['head_final_k']}/{ef['n']} ({ef['head_final_rate']*100:.1f}%)",
        "core_gulf": f"{cg['head_final_k']}/{cg['n']} ({cg['head_final_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 2: Eastern Frontier (n=13) vs Core Gulf (n=17) on MAN-initial rate
    pf, pp = perm_diff_p(ef["man_init_k"], ef["n"], cg["man_init_k"], cg["n"], seed=5002, n_perm=N_SHUF)
    hyp_tests["T2_EastFrontier_vs_CoreGulf_MAN_Initial"] = {
        "east_frontier": f"{ef['man_init_k']}/{ef['n']} ({ef['man_init_rate']*100:.1f}%)",
        "core_gulf": f"{cg['man_init_k']}/{cg['n']} ({cg['man_init_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 3: Eastern Frontier (n=13) vs Core Gulf (n=17) on Any-MAN presence
    pf, pp = perm_diff_p(ef["man_any_k"], ef["n"], cg["man_any_k"], cg["n"], seed=5003, n_perm=N_SHUF)
    hyp_tests["T3_EastFrontier_vs_CoreGulf_MAN_Any"] = {
        "east_frontier": f"{ef['man_any_k']}/{ef['n']} ({ef['man_any_rate']*100:.1f}%)",
        "core_gulf": f"{cg['man_any_k']}/{cg['n']} ({cg['man_any_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 4: Central Asia BMAC alone (n=3) vs Core Gulf (n=17) on Head-Final & Any-MAN
    pf_hf, pp_hf = perm_diff_p(bmac["head_final_k"], bmac["n"], cg["head_final_k"], cg["n"], seed=5004, n_perm=N_SHUF)
    pf_ma, pp_ma = perm_diff_p(bmac["man_any_k"], bmac["n"], cg["man_any_k"], cg["n"], seed=5005, n_perm=N_SHUF)
    hyp_tests["T4_BMAC_Alone_vs_CoreGulf"] = {
        "bmac_head_final": f"{bmac['head_final_k']}/{bmac['n']} ({bmac['head_final_rate']*100:.1f}%)",
        "core_gulf_head_final": f"{cg['head_final_k']}/{cg['n']} ({cg['head_final_rate']*100:.1f}%)",
        "P_head_final_fisher": pf_hf, "P_head_final_perm": pp_hf,
        "bmac_man_any": f"{bmac['man_any_k']}/{bmac['n']} (0.0%)",
        "core_gulf_man_any": f"{cg['man_any_k']}/{cg['n']} ({cg['man_any_rate']*100:.1f}%)",
        "P_man_any_fisher": pf_ma, "P_man_any_perm": pp_ma,
    }
    # Test 5: Iranian Plateau Core (n=6) vs Eastern Frontier (n=13) on Any-MAN presence
    pf, pp = perm_diff_p(ir["man_any_k"], ir["n"], ef["man_any_k"], ef["n"], seed=5006, n_perm=N_SHUF)
    hyp_tests["T5_IranPlateau6_vs_EastFrontier13_MAN_Any"] = {
        "iran_6": f"{ir['man_any_k']}/{ir['n']} ({ir['man_any_rate']*100:.1f}%)",
        "east_frontier_13": f"{ef['man_any_k']}/{ef['n']} ({ef['man_any_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 6: Iranian Plateau + Sibri (n=7) vs Eastern Frontier (n=13) on Any-MAN presence
    pf, pp = perm_diff_p(ir7["man_any_k"], ir7["n"], ef["man_any_k"], ef["n"], seed=5007, n_perm=N_SHUF)
    hyp_tests["T6_IranPlusSibri7_vs_EastFrontier13_MAN_Any"] = {
        "iran_plus_sibri_7": f"{ir7['man_any_k']}/{ir7['n']} ({ir7['man_any_rate']*100:.1f}%)",
        "east_frontier_13": f"{ef['man_any_k']}/{ef['n']} ({ef['man_any_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 7: Iranian Plateau Core (n=6) vs Mainland Baseline on Any-MAN presence
    pf = fisher_exact_2sided(ir["man_any_k"], ir["n"] - ir["man_any_k"], ml_man_any, ml_n - ml_man_any)
    hyp_tests["T7_IranPlateau6_vs_Mainland_MAN_Any"] = {
        "iran_6": f"{ir['man_any_k']}/{ir['n']} ({ir['man_any_rate']*100:.1f}%)",
        "mainland": f"{ml_man_any}/{ml_n} ({ml_man_any/ml_n*100:.1f}%)",
        "P_fisher_2sided": round(float(pf), 6),
    }
    # Test 8: Eastern Frontier (n=13) vs Core Gulf (n=16) on Mainland Bigram Survival!
    pf, pp = perm_diff_p(ef["bigrams_mainland_hit"], ef["bigrams_total"],
                         cg["bigrams_mainland_hit"], cg["bigrams_total"], seed=5008, n_perm=N_SHUF)
    hyp_tests["T8_EastFrontier_vs_CoreGulf_MainlandBigrams"] = {
        "east_frontier_bigrams": f"{ef['bigrams_mainland_hit']}/{ef['bigrams_total']} ({ef['bigram_survival_rate']*100:.1f}%)",
        "core_gulf_bigrams": f"{cg['bigrams_mainland_hit']}/{cg['bigrams_total']} ({cg['bigram_survival_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }
    # Test 8b: Central Asia BMAC alone (n=3 square seals: Altyn-Depe, Shortugai, Gonur-Depe) vs Core Gulf on Mainland Bigram Survival!
    pf, pp = perm_diff_p(bmac["bigrams_mainland_hit"], bmac["bigrams_total"],
                         cg["bigrams_mainland_hit"], cg["bigrams_total"], seed=5009, n_perm=N_SHUF)
    hyp_tests["T8b_BMAC_Alone_vs_CoreGulf_MainlandBigrams"] = {
        "bmac_bigrams": f"{bmac['bigrams_mainland_hit']}/{bmac['bigrams_total']} ({bmac['bigram_survival_rate']*100:.1f}%)",
        "core_gulf_bigrams": f"{cg['bigrams_mainland_hit']}/{cg['bigrams_total']} ({cg['bigram_survival_rate']*100:.1f}%)",
        "P_fisher_2sided": pf, "P_perm_5000": pp,
    }

    # Test 9: Track C Placement of Unprovenanced Cylinder G3-U02 / 3888.1 (032-132-000-055-090)
    # Naive Bayes Laplace-smoothed log-likelihood across 5 diagnostic features:
    # (1) cylinder shape, (2) has_MAN, (3) has_stroke_numeral, (4) NO fish_220, (5) NO Mainland head-final
    u02_feats = {"cylinder": 1, "man_any": 1, "num_any": 1, "fish_any": 0, "head_final": 0}
    # Empirical group counts for those 5 features:
    iran_cyl_k = sum(1 for r in grp_iran_core if r["shape"] == "cylinder")  # 3/6
    cg_cyl_k = 0  # 0/17
    ef_cyl_k = 0  # 0/13
    ml_cyl_k = 5  # ~5 cylinders in entire >4000 Mainland corpus (conservative upper bound!)

    def nb_loglik(feat_counts, N, x):
        ll = 0.0
        for f, val in x.items():
            p = (feat_counts[f] + 0.5) / (N + 1.0)
            ll += math.log(p if val == 1 else (1.0 - p))
        return ll

    ll_iran = nb_loglik({
        "cylinder": iran_cyl_k, "man_any": ir["man_any_k"], "num_any": ir["num_any_k"],
        "fish_any": ir["fish_any_k"], "head_final": ir["head_final_k"],
    }, ir["n"], u02_feats)
    ll_gulf = nb_loglik({
        "cylinder": cg_cyl_k, "man_any": cg["man_any_k"], "num_any": cg["num_any_k"],
        "fish_any": cg["fish_any_k"], "head_final": cg["head_final_k"],
    }, cg["n"], u02_feats)
    ll_east = nb_loglik({
        "cylinder": ef_cyl_k, "man_any": ef["man_any_k"], "num_any": ef["num_any_k"],
        "fish_any": ef["fish_any_k"], "head_final": ef["head_final_k"],
    }, ef["n"], u02_feats)
    ll_main = nb_loglik({
        "cylinder": ml_cyl_k, "man_any": ml_man_any, "num_any": ml_num_any,
        "fish_any": ml_fish_any, "head_final": ml_hf_end,
    }, ml_n, u02_feats)

    mx = max(ll_iran, ll_gulf, ll_east, ll_main)
    exps = {k: math.exp(v - mx) for k, v in [("Iranian_Plateau", ll_iran), ("Core_Gulf", ll_gulf), ("Eastern_Frontier", ll_east), ("Mainland_Harappan", ll_main)]}
    Z = sum(exps.values())
    post_u02 = {k: round(v / Z, 4) for k, v in exps.items()}

    # Token coverage of 19 locked signs on ALL 23 complete held-out inscribed frontier objects
    tot_fr_clean = sum(r["n_clean"] for r in complete_inscr)
    tot_fr_l19 = sum(r["n_l19"] for r in complete_inscr)
    tot_fr_aux = sum(r["n_aux"] for r in complete_inscr)
    inscr_with_l19 = sum(1 for r in complete_inscr if r["n_l19"] > 0)
    inscr_with_aux = sum(1 for r in complete_inscr if r["n_aux"] > 0)

    stats_5b = {
        "corpus_totals": {
            "total_published_frontier_objects": len(FRONTIER_CORPUS),
            "inscribed_complete": len(complete_inscr),
            "inscribed_partial_published": sum(1 for r in parsed_frontier if r["inscribed_status"] == "inscribed_partial_published"),
            "cross_script_linear_elamite": sum(1 for r in parsed_frontier if r["inscribed_status"] == "cross_script_linear_elamite"),
            "corroded_illegible": sum(1 for r in parsed_frontier if r["inscribed_status"] == "corroded_illegible_imitation"),
            "uninscribed_indus_horizon": sum(1 for r in parsed_frontier if r["inscribed_status"].startswith("uninscribed")),
        },
        "heldout_19_locked_coverage": {
            "n_inscribed_complete": len(complete_inscr),
            "total_clean_tokens": tot_fr_clean,
            "locked19_tokens": tot_fr_l19,
            "locked19_token_rate": round(tot_fr_l19 / tot_fr_clean, 4),
            "locked19_plus_aux_tokens": tot_fr_aux,
            "locked19_plus_aux_rate": round(tot_fr_aux / tot_fr_clean, 4),
            "inscriptions_with_ge1_locked19": f"{inscr_with_l19}/{len(complete_inscr)} ({inscr_with_l19/len(complete_inscr)*100:.1f}%)",
            "inscriptions_with_ge1_locked19_or_aux": f"{inscr_with_aux}/{len(complete_inscr)} ({inscr_with_aux/len(complete_inscr)*100:.1f}%)",
            "mainland_baseline_locked19_token_rate": round(ml_l19_tok / ml_tot_tok, 4),
        },
        "zone_feature_table": zone_stats,
        "hypothesis_tests": hyp_tests,
        "trackc_u02_3888_placement": {
            "target_id": "G3-U02 / Lipi 3888.1",
            "seq": "032-132-000-055-090",
            "features": u02_feats,
            "log_likelihoods": {
                "Iranian_Plateau": round(ll_iran, 3),
                "Core_Gulf": round(ll_gulf, 3),
                "Eastern_Frontier": round(ll_east, 3),
                "Mainland_Harappan": round(ll_main, 3),
            },
            "posterior_probs_uniform_prior": post_u02,
            "bayes_factor_Iran_vs_CoreGulf": round(math.exp(ll_iran - ll_gulf), 2),
            "bayes_factor_Iran_vs_Mainland": round(math.exp(ll_iran - ll_main), 1),
        },
    }

    s5b_path = os.path.join(OUT_DIR, "test5b_frontier_stats.json")
    with open(s5b_path, "w", encoding="utf-8") as fh:
        json.dump(stats_5b, fh, indent=2, ensure_ascii=False)

    log("=== KEY 5B HEADLINE RESULTS ===")
    for k, v in hyp_tests.items():
        log(f"  {k}: {v}")
    log(f"  Held-out 19-locked coverage: {tot_fr_l19}/{tot_fr_clean} ({tot_fr_l19/tot_fr_clean*100:.1f}%) strict | {tot_fr_aux}/{tot_fr_clean} ({tot_fr_aux/tot_fr_clean*100:.1f}%) +aux | {inscr_with_l19}/{len(complete_inscr)} inscriptions")
    log(f"  Track C G3-U02 / 3888.1 placement posterior: {post_u02} (BF Iran vs Core Gulf = {math.exp(ll_iran - ll_gulf):.2f}x, vs Mainland = {math.exp(ll_iran - ll_main):.1f}x)")
    log("DONE! All outputs written to work_data/key4e/.")


if __name__ == "__main__":
    main()
