#!/usr/bin/env python3
"""key4b_bootstrap_wave2.py -- Key #4B (Lever 2): Wave-2 Ventris Chain-Reaction Bootstrap
on the Top 30 Remaining High-Frequency Unsolved Signs + 1-Blank-Slot Constrained Decoder.

Strictly rerunnable, zero-artifact, zero-overlap pipeline:
  1. Test 4B-1 -- Zero-Overlap Wave-2 Bootstrap on the Exact Top 30 Remaining Unsolved Signs:
     - Programmatically extracts the exact Top 30 remaining high-frequency unsolved signs
       across intact Lipi (3,600 faces) + held-out unseen Mahadevan new texts (627 intact faces),
       excluding our 19 sound-locked Dravidian signs (Core 11 + Wave-1 8), 4 loan anchors, and
       numerals.
     - Extracts every sign's visual shape (`work_data/sign_shapes.csv`), empirical archaeological
       and metrological domain (`work_data/sem/sign_anchors.csv`, `work_data/reader_v3/soundfree_lexicon.csv`,
       `work_data/sem/events_lipi.json`, `work_data/sem/events_new.json`), and top locked neighbors
       from our 19 sound-locked signs.
     - Enforces STRICT PROGRAMMATIC ZERO-OVERLAP (zero shared words AND zero shared 4-char stems)
       between Domain-A (visual picture) and Domain-B (empirical archaeological/corpus function) for
       every single sign in both English and German.
     - Runs 5,000 exact derivational-cluster-preserving sound shuffles across ALL 7 cognate
       families (`Single-Headword-Only`, zero secondary-form leaks: Dravidian `pdrav_2branch_fixed`,
       Munda `pmunda_cognates`, Indo-Aryan `oia_cognates`, Elamite `elamite_roots`, Sumerian
       `sumerian_roots`, Akkadian `akkadian_roots`, Burushaski `burushaski_all`) PLUS unedited raw
       `pdrav_2branch` (`Dravidian_RawPDrav`) and `pdrav_2lang_fixed` (`Dravidian_2Lang`), on
       All-30, Strictly-Novel-24 (removing 6 allograph/echo/catalog-twin signs `741/817/920/405/151/706`
       so zero double-counting is possible!), AND the Held-Out Unseen-Replicated subset (`OR_new >= 1.5`).
     - Also runs 5,000 Domain-B permutation controls for Direct Same-Etymon Polysemy across all 7 families.

  2. Test 4B-2 -- 1-Blank-Slot Constrained Compound & Contextual Decoder (`[LOCKED] - [???] - [LOCKED]`):
     - Extracts EVERY recurring intact inscription in Lipi (3,600) + unseen new texts (627) where
       all signs EXCEPT ONE are in our 19 sound-locked signs + 4 loans + basic numerals, PLUS every
       recurring `[KNOWN_L] - X - [KNOWN_R]` sandwich and `[KNOWN] - X` / `X - [KNOWN]` frame.
     - Scores candidate Proto-Dravidian roots for each Top-30 blank sign `X` by joint evidence:
       (a) strict etymological DEDR compound with `KNOWN_L` or `KNOWN_R` (raw `dedr_entries.tsv`),
       (b) visual-picture match (Domain A),
       (c) empirical archaeological/rebus bridge (Domain B) + physical object-class replication on
           unseen Mahadevan `new texts`,
       (d) Dravidian head-final syntactic tier consistency across `[KNOWN_L] - X - [KNOWN_R]` frames.
     - Benchmarks the constrained decoder against 5,000 shuffled sound assignments (both within-known
       slot permutations AND cluster-preserving full-lexicon sound shuffles) for exact empirical P-values.

  3. Strict Epistemic Accounting & Corpus Coverage Before vs After Wave-2:
     - Classifies every one of the 30 signs strictly as `building on it`, `testing it`, or `null`.
     - Computes exact token coverage AND 100%-covered face counts across Lipi intact (3,600) and
       unseen Mahadevan intact (627) before vs after Wave-2 (strictly separating `building on it`
       from `testing it`).

Outputs -> work_data/key4b/
"""

import os
import re
import sys
import csv
import json
import math
import time
import collections
import subprocess
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

import key2a_rebus_lock as k2
import key3a_sound_sweep as k3

TMP_LEX = "/tmp/typo_lex"
OUT_DIR = os.path.join(ROOT, "work_data", "key4b")
os.makedirs(OUT_DIR, exist_ok=True)

N_SHUF = int(os.environ.get("KEY4B_NSHUF", 5000))
T0 = time.time()


def log(*args):
    print(f"[key4b {time.time() - T0:6.1f}s]", *args, flush=True)


def ensure_lexicons():
    """Ensure /tmp/typo_lex and pdrav_2branch_fixed exist for strict rerunnability."""
    needed = [
        "pdrav_2branch_fixed.tsv", "pdrav_2branch.tsv", "pdrav_2lang_fixed.tsv",
        "pmunda_cognates.tsv", "oia_cognates.tsv", "elamite_roots.tsv",
        "sumerian_roots.tsv", "akkadian_roots.tsv", "burushaski_all.tsv",
    ]
    if not all(os.path.exists(os.path.join(TMP_LEX, f)) for f in needed):
        log("Populating /tmp/typo_lex via typo_00_lexicons.py + build_fixed_pdrav_2branch()...")
        subprocess.run([sys.executable, os.path.join(ROOT, "work_scripts", "typo_00_lexicons.py")], check=True)
        k2.build_fixed_pdrav_2branch()


def p_and_z(obs, null_arr):
    null_arr = np.asarray(null_arr, dtype=np.float64)
    mu = float(null_arr.mean())
    sd = float(null_arr.std(ddof=1)) if len(null_arr) > 1 else 0.0
    z = 0.0 if sd < 1e-12 else (obs - mu) / sd
    p = float((1.0 + np.sum(null_arr >= obs - 1e-12)) / (1.0 + len(null_arr)))
    return round(mu, 4), round(sd, 4), round(z, 3), round(p, 5)


def load_single_hw_lex(fam_label, dict_name, is_de=False, single_hw=True):
    """Load CleanCognateLex and optionally restrict strictly to 1 primary headword per etymon
    (exact gold-standard Rival-1 protocol from key2a_rival_audit.py)."""
    L = k2.CleanCognateLex(fam_label, dict_name, is_de=is_de)
    if not single_hw:
        return L
    L.phons = [xs[:1] for xs in L.phons]
    L.phon_stems = [xs[:1] for xs in L.phon_stems]
    L.asciis = [xs[:1] for xs in L.asciis]
    L.ascii_stems = [xs[:1] for xs in L.ascii_stems]
    for mode, key_lists in (
        ("phon_exact", L.phons),
        ("phon_stem", L.phon_stems),
        ("ascii_exact", L.asciis),
        ("ascii_stem", L.ascii_stems),
    ):
        kmap = collections.defaultdict(list)
        for i, ks in enumerate(key_lists):
            for k in set(ks):
                kmap[k].append(i)
        L.key_maps[mode] = kmap
        us, vs = [], []
        seen_pair = set()
        for idxs in kmap.values():
            if len(idxs) < 2:
                continue
            m = len(idxs)
            for a in range(m):
                u = idxs[a]
                for b in range(a + 1, m):
                    v = idxs[b]
                    pair = (u, v) if u < v else (v, u)
                    if pair not in seen_pair:
                        seen_pair.add(pair)
                        us.append(pair[0])
                        vs.append(pair[1])
        L.edges[mode] = (np.array(us, dtype=np.int32), np.array(vs, dtype=np.int32))
    return L


# ==============================================================================
# 1. CURRENT 19 SOUND-LOCKED SIGNS + LOANS + BASIC NUMERALS
# ==============================================================================
LOCKED19_INFO = {
    # Core 11 (Key #2A)
    "220": {"roots": ["mīṉ", "miṉ"], "eids": {"4885", "4876"}, "gloss": "star / fish (*mīṉ)", "tier": 0, "wave": "Core11"},
    "820": {"roots": ["kāl"], "eids": {"1483", "1479"}, "gloss": "quarter / wheel (*kāl)", "tier": 0, "wave": "Core11"},
    "320": {"roots": ["paṭi"], "eids": {"3850", "3849"}, "gloss": "ration / step (*paṭi)", "tier": 0, "wave": "Core11"},
    "090": {"roots": ["āḷ"], "eids": {"399", "5157"}, "gloss": "manager / man (*āḷ)", "tier": 2, "wave": "Core11"},
    "154": {"roots": ["kā"], "eids": {"1417", "1416"}, "gloss": "guard / pole (*kā)", "tier": 2, "wave": "Core11"},
    "740": {"roots": ["kuṭi", "kuṭam"], "eids": {"1655", "1651"}, "gloss": "house / pot (*kuṭ-)", "tier": 1, "wave": "Core11"},
    "400": {"roots": ["cikka", "cikkam"], "eids": {"2495", "2497"}, "gloss": "junior / comb (*cikk-)", "tier": 2, "wave": "Core11"},
    "705": {"roots": ["kalam", "kaḷam"], "eids": {"1305", "1376"}, "gloss": "kalam / ship (*kalam~*kaḷam)", "tier": 0, "wave": "Core11"},
    "520": {"roots": ["vēḷ", "vēl"], "eids": {"5545", "5536"}, "gloss": "chief / spear (*vēḷ~*vēl)", "tier": 2, "wave": "Core11"},
    "850": {"roots": ["kaṉ", "kaṇ"], "eids": {"1402", "1159"}, "gloss": "copper / eye (*kaṉ~*kaṇ)", "tier": 0, "wave": "Core11"},
    "390": {"roots": ["tai"], "eids": {"3473", "3474"}, "gloss": "weave / young-tree (*tai)", "tier": 0, "wave": "Core11"},
    # Wave-1 8 (Key #3A)
    "717": {"roots": ["aṭi"], "eids": {"72"}, "gloss": "servant / foot (*aṭi)", "tier": 2, "wave": "Wave1"},
    "061": {"roots": ["kāl"], "eids": {"1479"}, "gloss": "quarter / leg (*kāl)", "tier": 0, "wave": "Wave1"},
    "235": {"roots": ["oḷi", "mīṉ"], "eids": {"1015", "1016", "4885"}, "gloss": "bright-star (*oḷi-mīṉ)", "tier": 0, "wave": "Wave1"},
    "500": {"roots": ["pāy"], "eids": {"4088"}, "gloss": "sail (*pāy)", "tier": 0, "wave": "Wave1"},
    "100": {"roots": ["talai"], "eids": {"3103"}, "gloss": "headman / head (*talai)", "tier": 2, "wave": "Wave1"},
    "176": {"roots": ["iru", "iṟu", "iṟai"], "eids": {"480", "521"}, "gloss": "tax-issuer / sit (*iru~*iṟai)", "tier": 2, "wave": "Wave1"},
    "900": {"roots": ["tiṅkaḷ"], "eids": {"3213"}, "gloss": "month / moon (*tiṅkaḷ)", "tier": 0, "wave": "Wave1"},
    "923": {"roots": ["maruppu"], "eids": {"4720"}, "gloss": "ivory-tusk / horn (*maruppu)", "tier": 0, "wave": "Wave1"},
}
LOCKED19_SET = set(LOCKED19_INFO.keys())
LOAN_SET = set(k3.LOAN_ANCHORS.keys())
BASIC_NUM_SET = set(k3.BASIC_NUMS.keys())
ALL_NUM_SET = set(k3.ALL_NUM_SIGNS)
KNOWN_INFO = {**LOCKED19_INFO, **k3.LOAN_ANCHORS, **k3.BASIC_NUMS}
KNOWN_SET = set(KNOWN_INFO.keys())

# ==============================================================================
# 2. TOP 30 REMAINING HIGH-FREQUENCY UNSOLVED SIGNS: ZERO-OVERLAP SPECS
#    Each entry: (sign, is_strictly_novel, shape_label, words_A_en, words_B_en,
#                 words_A_de, words_B_de, expected_tier, obj_target_kind_or_zone)
# ==============================================================================
WAVE2_SPECS = [
    ("700", True, "simple U cup",
     ["cup", "bowl", "vessel", "pot", "jar", "hollow"],
     ["measure", "capacity", "grain", "ration", "allowance", "portion"],
     ["becher", "schale", "gefass", "topf", "krug", "hohl"],
     ["mass", "menge", "getreide", "ration", "lohn", "anteil"],
     0, ("kind", {"mtab"})),

    ("240", True, "fish with cheek whiskers/fins",
     ["whisker", "fin", "wing", "feather", "cheek", "bristle"],
     ["star", "bright", "shine", "glitter", "chief", "lord", "bead"],
     ["bart", "flosse", "flugel", "feder", "wange", "borste"],
     ["stern", "hell", "glanz", "leucht", "herr", "furst", "perle"],
     0, ("zone", {"chanhu_mound2_workshops"})),

    ("861", True, "diamond/eye/seed with top diamond",
     ["eye", "seed", "kernel", "bud", "lozenge", "sight"],
     ["weight", "fraction", "share", "property", "tribute", "offering"],
     ["auge", "samen", "kern", "knospe", "raute", "blick"],
     ["gewicht", "bruch", "anteil", "besitz", "tribut", "opfer"],
     0, ("kind", {"seal"})),

    ("060", True, "two strokes, second slanting/bent under first",
     ["slant", "slope", "bend", "bent", "curve", "crooked", "lean"],
     ["inside", "inner", "within", "join", "unite", "quarter", "belong"],
     ["schief", "krumm", "biegen", "gebogen", "neigen", "bogen"],
     ["innen", "innere", "innerhalb", "verbinden", "viertel", "gehoren"],
     1, ("kind", {"seal"})),

    ("590", True, "square+bar chest/basket",
     ["box", "chest", "crate", "basket", "plait", "braid"],
     ["sack", "pack", "bale", "bundle", "granary", "store", "treasury"],
     ["kasten", "truhe", "korb", "flechten", "geflecht"],
     ["sack", "pack", "ballen", "bundel", "speicher", "vorrat", "schatz"],
     0, ("kind", {"mtab", "tag"})),

    ("741", False, "jar with 1 stroke inside mouth [graphic echo of 740]",
     ["jar", "pot", "waterpot", "pitcher", "vessel"],
     ["house", "ward", "family", "abode", "lineage", "tenant"],
     ["krug", "topf", "gefass", "kanne"],
     ["haus", "familie", "wohnung", "geschlecht", "pachter"],
     1, ("kind", {"seal", "tag"})),

    ("615", True, "grid of x by y cells",
     ["grid", "net", "lattice", "mesh", "frame", "reed", "square"],
     ["field", "land", "arable", "ridge", "estate", "plot", "farm"],
     ["gitter", "netz", "rahmen", "kamm", "quadrat"],
     ["feld", "land", "acker", "furche", "gut", "grundstuck"],
     0, ("kind", {"ctab"})),

    ("817", False, "double-diamond (leaf/diamond + top diamond) [catalog twin of 861]",
     ["eye", "seed", "kernel", "bud", "lozenge", "sight"],
     ["box", "chest", "crate", "cargo", "freight", "weight", "share"],
     ["auge", "samen", "kern", "knospe", "raute", "blick"],
     ["kasten", "truhe", "fracht", "ladung", "gewicht", "anteil"],
     0, ("kind", {"tag", "seal"})),

    ("233", True, "fish with horizontal bar/split",
     ["split", "halve", "divide", "cut", "slice", "cleave", "crack"],
     ["star", "bright", "shine", "dawn", "light", "luster", "sun"],
     ["spalten", "teilen", "schneiden", "halbieren", "riss"],
     ["stern", "hell", "glanz", "leucht", "morgen", "licht", "sonne"],
     0, ("kind", {"seal", "ctab"})),

    ("415", True, "four-tine pitchfork/branch",
     ["fork", "branch", "prong", "rake", "bifurcate", "tine"],
     ["seize", "grasp", "control", "share", "rent", "chief", "lord"],
     ["gabel", "zweig", "ast", "zinke", "rechen"],
     ["greifen", "fassen", "herrschaft", "anteil", "herr", "furst"],
     0, ("kind", {"mtab", "seal"})),

    ("920", False, "crescent/right-paren with leaf [graphic echo of 900]",
     ["moon", "crescent", "lunar", "arc"],
     ["month", "season", "period", "office", "craft", "bead"],
     ["mond", "sichel", "halbmond", "bogen"],
     ["monat", "zeit", "amt", "handwerk", "perle"],
     0, ("kind", {"seal"})),

    ("405", False, "simple branching tree [thread/weave echoes 390]",
     ["tree", "branch", "bough", "twig", "shrub"],
     ["thread", "yarn", "cord", "string", "weave", "knit", "spin"],
     ["baum", "ast", "zweig", "strauch"],
     ["faden", "garn", "schnur", "weben", "stricken", "spinnen"],
     0, ("kind", {"bangle", "pot"})),

    ("407", True, "simple tree with branches (cloth-bolt copper-tab sign)",
     ["tree", "branch", "bough", "twig", "horn", "shrub"],
     ["cloth", "textile", "garment", "fabric", "dye", "weaver"],
     ["baum", "ast", "zweig", "horn", "strauch"],
     ["stoff", "tuch", "gewand", "kleid", "farbe", "weber"],
     0, ("kind", {"ctab"})),

    ("806", True, "leaf with tree/stalk at bottom",
     ["leaf", "stalk", "stem", "sprout", "shoot", "twig"],
     ["crop", "millet", "grain", "harvest", "yield", "produce", "barley"],
     ["blatt", "stiel", "halm", "spross", "trieb", "zweig"],
     ["ernte", "hirse", "getreide", "korn", "ertrag", "gerste"],
     0, ("kind", {"ctab"})),

    ("798", True, "leaf with pincers/claws",
     ["leaf", "petal", "pincer", "claw", "tongs", "crab"],
     ["house", "mansion", "courtyard", "lineage", "merchant", "heir"],
     ["blatt", "zange", "klaue", "schere", "krebs"],
     ["haus", "hof", "palast", "geschlecht", "kaufmann", "erbe"],
     0, ("zone", {"md_HR_elite"})),

    ("255", True, "asymmetric fish/animal with fins and legs",
     ["animal", "beast", "fish", "bird", "fowl", "fin"],
     ["ration", "allowance", "grain", "granary", "chief", "king", "issue"],
     ["tier", "fisch", "vogel", "huhn", "flosse"],
     ["ration", "lohn", "getreide", "speicher", "herr", "konig", "ausgabe"],
     0, ("kind", {"mtab", "ctab"})),

    ("803", True, "leaf with tree at bottom (house crest)",
     ["leaf", "leaves", "foliage", "petal"],
     ["house", "abode", "home", "family", "dwelling", "lineage"],
     ["blatt", "laub", "blutenblatt"],
     ["haus", "wohnung", "heim", "familie", "geschlecht"],
     0, ("zone", {"md_HR_elite"})),

    ("156", True, "person carrying two burdens (jar-handle head)",
     ["carry", "burden", "porter", "shoulder", "pole", "yoke"],
     ["bale", "pack", "sack", "bundle", "ration", "measure", "weight"],
     ["tragen", "last", "trager", "schulter", "stange", "joch"],
     ["ballen", "pack", "sack", "bundel", "ration", "mass", "gewicht"],
     0, ("kind", {"mtab", "tag"})),

    ("840", True, "two overlapping vertical leaves",
     ["pair", "twin", "couple", "double", "leaf", "leaves"],
     ["equal", "match", "agree", "join", "unite", "bangle", "ring", "audit"],
     ["paar", "zwilling", "doppelt", "blatt", "laub"],
     ["gleich", "passen", "verbinden", "einigen", "ring", "reif", "prufen"],
     0, ("kind", {"bangle", "mtab"})),

    ("760", True, "U with decorated branching/sprout at top",
     ["sprout", "shoot", "bud", "twig", "tendril"],
     ["child", "young", "son", "offspring", "descendant", "heir"],
     ["spross", "trieb", "knospe", "zweig", "ranke"],
     ["kind", "jung", "sohn", "nachkomme", "erbe"],
     0, ("kind", {"rod"})),

    ("368", True, "vertical stroke with triangular wing/banner",
     ["flag", "banner", "pennant", "streamer", "creeper", "wing"],
     ["give", "grant", "allot", "title", "pedigree", "grain", "ration"],
     ["fahne", "banner", "wimpel", "ranke", "flugel"],
     ["geben", "schenken", "titel", "stammbaum", "getreide", "ration"],
     1, ("zone", {"har_F_platforms_quarters", "har_F_granary"})),

    ("690", True, "two nested >> touching << (knot/tie/clasp)",
     ["knot", "tie", "bind", "fasten", "clasp", "link"],
     ["bundle", "packet", "store", "building", "ration", "grain", "pledge"],
     ["knoten", "binden", "knupfen", "schnalle", "glied"],
     ["bundel", "paket", "vorrat", "gebaude", "ration", "getreide", "pfand"],
     0, ("kind", {"mtab", "ctab"})),

    ("550", True, "opposed triangles with opening (pincer/mouth)",
     ["mouth", "jaw", "pincer", "beak", "claw", "tongs"],
     ["gate", "portal", "door", "entrance", "citadel", "fort", "precinct"],
     ["mund", "kiefer", "zange", "schnabel", "klaue"],
     ["tor", "tur", "eingang", "burg", "festung", "bezirk"],
     0, ("zone", {"lothal_acropolis_res", "md_citadel"})),

    ("892", True, "bow and arrow",
     ["bow", "arrow", "arc", "archer"],
     ["sell", "sale", "price", "cost", "value", "trade", "merchant"],
     ["bogen", "pfeil", "schutze"],
     ["verkaufen", "verkauf", "preis", "kosten", "wert", "handel", "kaufmann"],
     0, ("kind", {"tag", "mtab"})),

    ("140", True, "person with round breasts and raised arm (woman)",
     ["woman", "female", "breast", "mother", "matron", "girl"],
     ["goddess", "queen", "ruler", "chief", "sacred", "temple", "citadel"],
     ["frau", "weib", "brust", "mutter", "madchen"],
     ["gottin", "konigin", "herrscher", "herr", "heilig", "tempel", "burg"],
     0, ("zone", {"md_citadel", "md_VS_dyers"})),

    ("151", False, "person carrying two burdens [porter allograph of 154]",
     ["carry", "burden", "load", "porter", "pole", "shoulder"],
     ["guard", "protect", "watch", "shelter", "defence", "preserve"],
     ["tragen", "last", "trager", "stange", "joch"],
     ["wachter", "schutzen", "wachen", "schutz", "bewahren"],
     2, ("kind", {"seal"})),

    ("142", True, "person with staff",
     ["staff", "stick", "rod", "sceptre", "club"],
     ["king", "chief", "ruler", "lord", "sovereign", "officer"],
     ["stab", "stock", "rute", "zepter", "keule"],
     ["konig", "herr", "furst", "herrscher", "beamter"],
     1, ("kind", {"ctab"})),

    ("503", True, "tall isosceles triangle with horizontal stripes (hill)",
     ["hill", "mountain", "peak", "ridge", "mound"],
     ["garland", "necklace", "string", "bead", "shell", "dye", "estate"],
     ["berg", "hugel", "gipfel", "kamm", "hohe"],
     ["kranz", "kette", "schnur", "perle", "muschel", "farbe", "gut"],
     0, ("zone", {"md_VS_dyers", "md_VS_MN_craft"})),

    ("231", True, "fish with small vertical stroke inside body",
     ["pierce", "stab", "plant", "stick", "line", "stroke"],
     ["star", "bright", "shine", "country", "district", "estate", "bull"],
     ["stechen", "bohren", "pflanzen", "stab", "linie", "strich"],
     ["stern", "hell", "glanz", "land", "bezirk", "gut", "stier"],
     0, ("kind", {"ctab"})),

    ("706", False, "U with long vertical stroke inside [measure echo of 700]",
     ["cup", "bowl", "vessel", "pot", "jar", "hollow"],
     ["measure", "bushel", "capacity", "grain", "ivory", "elephant"],
     ["becher", "schale", "gefass", "topf", "krug", "hohl"],
     ["mass", "scheffel", "menge", "getreide", "elfenbein", "elefant"],
     0, ("kind", {"ctab"})),
]


def verify_zero_overlap(specs):
    """Programmatically verify ZERO shared words AND ZERO shared 4-char stems between
    Domain A and Domain B for every single sign in both English and German."""
    violations = []
    for rec in specs:
        s, _, _, wAe, wBe, wAd, wBd, _, _ = rec
        for lang, wA, wB in (("EN", wAe, wBe), ("DE", wAd, wBd)):
            sA = {w.lower() for w in wA}
            sB = {w.lower() for w in wB}
            exact_ov = sA & sB
            if exact_ov:
                violations.append((s, lang, "EXACT", sorted(exact_ov)))
            pA = {w[:4].lower() for w in wA if len(w) >= 4}
            pB = {w[:4].lower() for w in wB if len(w) >= 4}
            stem_ov = pA & pB
            if stem_ov:
                violations.append((s, lang, "STEM4", sorted(stem_ov)))
            # Also check substring containment for short 3-char words
            for a in sA:
                for b in sB:
                    if len(a) >= 3 and len(b) >= 3 and (a == b or a.startswith(b) or b.startswith(a)):
                        violations.append((s, lang, "PREFIX", (a, b)))
    if violations:
        raise ValueError(f"ZERO-OVERLAP VIOLATION DETECTED: {violations}")
    log(f"Programmatic ZERO-OVERLAP verification PASSED on all {len(specs)} signs (EN + DE, 0 shared words, 0 shared 4-char stems)!")


def words_to_regex(words):
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.I)


# ==============================================================================
# 3. CORPUS LOADING & TOP 30 VERIFICATION
# ==============================================================================
def load_corpora():
    with open(os.path.join(ROOT, "work_data", "reader_v3", "corpus_soundfree_readings.csv"), encoding="utf-8") as f:
        r3_rows = list(csv.DictReader(f))
    lipi_int = [r for r in r3_rows if r["catalogue"] == "Lipi" and r["intact"] == "True"]
    new_int = [r for r in r3_rows if r["catalogue"] != "Lipi" and r["partnered"] == "False" and r["intact"] == "True"]

    with open(os.path.join(ROOT, "work_data", "sem", "events_lipi.json"), encoding="utf-8") as f:
        ev_lipi = json.load(f)
    with open(os.path.join(ROOT, "work_data", "sem", "events_new.json"), encoding="utf-8") as f:
        ev_new = json.load(f)

    shapes = {}
    with open(os.path.join(ROOT, "work_data", "sign_shapes.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            shapes[r["lipi_wells_number"]] = r["shape_description"]

    anchors = collections.defaultdict(list)
    with open(os.path.join(ROOT, "work_data", "sem", "sign_anchors.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            anchors[r["sign"]].append(f"{r['anchor_tier']}: {r['pinned_domain']}")

    sf_lex = {}
    with open(os.path.join(ROOT, "work_data", "reader_v3", "soundfree_lexicon.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sf_lex[r["sign"]] = r

    # Verify our WAVE2_SPECS match the exact Top 30 remaining unsolved signs
    cnt_l, cnt_n, cnt_tot = collections.Counter(), collections.Counter(), collections.Counter()
    for r in lipi_int:
        for t in r["signs"].split("-"):
            if t and t != "000":
                cnt_l[t] += 1
                cnt_tot[t] += 1
    for r in new_int:
        for t in r["signs"].split("-"):
            if t and t != "000":
                cnt_n[t] += 1
                cnt_tot[t] += 1

    excl = LOCKED19_SET | LOAN_SET | ALL_NUM_SET
    top30_emp = [s for s, _ in cnt_tot.most_common() if s not in excl][:30]
    spec_signs = [x[0] for x in WAVE2_SPECS]
    assert set(top30_emp) == set(spec_signs), (
        f"Spec mismatch vs empirical Top 30! Missing={set(top30_emp)-set(spec_signs)}, Extra={set(spec_signs)-set(top30_emp)}"
    )
    log(f"Verified exact Top 30 remaining unsolved signs ({cnt_tot[top30_emp[0]]}x down to {cnt_tot[top30_emp[-1]]}x across {len(lipi_int)} Lipi + {len(new_int)} New intact faces)")
    return lipi_int, new_int, ev_lipi, ev_new, shapes, anchors, sf_lex, cnt_l, cnt_n, cnt_tot


# ==============================================================================
# 4. TEST 4B-1: 7-FAMILY + UNEDITED RAW PDRAV WAVE-2 BOOTSTRAP (5,000 SHUFFLES)
# ==============================================================================
def compute_replication(sign, target_spec, ev_lipi, ev_new):
    ttype, tvals = target_spec
    def is_t(e):
        if ttype == "kind":
            return e["kind"] in tvals
        return any(z in tvals for z in e.get("zones", []))
    def has_s(e):
        return any(sign in f for f in e["faces"])
    res = {}
    for tag, evs in (("lipi", ev_lipi), ("new", ev_new)):
        a = sum(1 for e in evs if has_s(e) and is_t(e))
        b = sum(1 for e in evs if has_s(e) and not is_t(e))
        c = sum(1 for e in evs if (not has_s(e)) and is_t(e))
        d = sum(1 for e in evs if (not has_s(e)) and (not is_t(e)))
        p, odds = k3.fisher_one_sided_gt(a, b, c, d)
        res[tag] = {"hits": a, "tot": a + b, "or": odds, "p": round(p, 6)}
    return res


def run_test_4b1(cnt_l, cnt_n, cnt_tot, shapes, anchors, sf_lex, ev_lipi, ev_new):
    log(f"=== TEST 4B-1: ZERO-OVERLAP WAVE-2 TOP-30 BOOTSTRAP ACROSS ALL 7 FAMILIES (N_SHUF={N_SHUF}) ===")

    # Compute locked-19 neighbors and object-class enrichments for all 30 signs
    adj19 = collections.defaultdict(collections.Counter)
    kinds_l = collections.defaultdict(collections.Counter)
    kinds_n = collections.defaultdict(collections.Counter)
    for e in ev_lipi:
        for f in e["faces"]:
            for s in f:
                if s != "000":
                    kinds_l[s][e["kind"]] += 1
            for i in range(len(f) - 1):
                a, b = f[i], f[i + 1]
                if a in LOCKED19_SET:
                    adj19[b][(a, "L")] += 1
                if b in LOCKED19_SET:
                    adj19[a][(b, "R")] += 1
    for e in ev_new:
        for f in e["faces"]:
            for s in f:
                if s != "000":
                    kinds_n[s][e["kind"]] += 1

    # Precompute held-out unseen `new texts` physical object-class replication for every sign
    rep_map = {}
    for rec in WAVE2_SPECS:
        rep_map[rec[0]] = compute_replication(rec[0], rec[8], ev_lipi, ev_new)
    unseen_rep_mask = np.array(
        [rep_map[rec[0]]["new"]["tot"] >= 1 and rep_map[rec[0]]["new"]["or"] >= 1.5 for rec in WAVE2_SPECS],
        dtype=bool,
    )
    n_unseen_rep = int(unseen_rep_mask.sum())

    # Load ALL 7 Primary Families (Single-HW) + Unedited Raw PDrav + 2-Lang Audit + Multi-HW Fixed Audit
    LEX_SPECS = [
        ("Dravidian", "pdrav_2branch_fixed", False, True, "PRIMARY_7"),
        ("Munda", "pmunda_cognates", False, True, "PRIMARY_7"),
        ("Indo-Aryan", "oia_cognates", False, True, "PRIMARY_7"),
        ("Elamite", "elamite_roots", True, True, "PRIMARY_7"),
        ("Sumerian", "sumerian_roots", False, True, "PRIMARY_7"),
        ("Akkadian", "akkadian_roots", False, True, "PRIMARY_7"),
        ("Burushaski", "burushaski_all", False, True, "PRIMARY_7"),
        ("Dravidian_RawPDrav", "pdrav_2branch", False, True, "AUDIT"),
        ("Dravidian_2Lang", "pdrav_2lang_fixed", False, True, "AUDIT"),
        ("Dravidian_MultiHW", "pdrav_2branch_fixed", False, False, "AUDIT"),
    ]

    K = len(WAVE2_SPECS)
    novel_mask = np.array([rec[1] for rec in WAVE2_SPECS], dtype=bool)
    n_novel = int(novel_mask.sum())
    log(
        f"Testing K={K} signs (All-30), Strictly-Novel N={n_novel} (excluding 6 allograph/twin signs), "
        f"AND Held-Out Unseen-Replicated N={n_unseen_rep} (OR_new >= 1.5)"
    )

    fam_summary_rows = []
    pdrav_details = None
    pdrav_raw_details = None
    pdrav_2lg_details = None
    all_fam_bridges = {}

    for fam_label, dict_name, is_de, single_hw, group_tag in LEX_SPECS:
        L = load_single_hw_lex(fam_label, dict_name, is_de=is_de, single_hw=single_hw)
        inA = np.zeros((K, L.E), dtype=bool)
        inB = np.zeros((K, L.E), dtype=bool)
        for idx, rec in enumerate(WAVE2_SPECS):
            wA = rec[5] if is_de else rec[3]
            wB = rec[6] if is_de else rec[4]
            inA[idx] = L.match_regex_bool(words_to_regex(wA))
            inB[idx] = L.match_regex_bool(words_to_regex(wB))

        rng = np.random.default_rng(20261125)

        # Precompute 5,000 cluster-preserving permutations ONCE per family so all 3 modes share identical null draws
        perms = [L.make_cluster_perm(rng) for _ in range(N_SHUF)]

        mode_out = {}
        for mode in ("phon_exact", "phon_stem", "ascii_exact"):
            real_vec = k2.eval_edges_vectorized(L, mode, inA, inB, perm=None, excl_same_flag=True)
            shuf_mat = np.zeros((N_SHUF, K), dtype=bool)
            for s_idx, perm in enumerate(perms):
                shuf_mat[s_idx] = k2.eval_edges_vectorized(L, mode, inA, inB, perm=perm, excl_same_flag=True)

            obs30 = int(real_vec.sum())
            null30 = shuf_mat.sum(axis=1)
            mu30, sd30, z30, p30 = p_and_z(obs30, null30)

            obs_nov = int(real_vec[novel_mask].sum())
            null_nov = shuf_mat[:, novel_mask].sum(axis=1)
            mu_n, sd_n, z_n, p_n = p_and_z(obs_nov, null_nov)

            obs_rep = int(real_vec[unseen_rep_mask].sum())
            null_rep = shuf_mat[:, unseen_rep_mask].sum(axis=1)
            mu_r, sd_r, z_r, p_r = p_and_z(obs_rep, null_rep)

            per_sign_p = ((1.0 + shuf_mat.sum(axis=0)) / (1.0 + N_SHUF)).tolist()
            mode_out[mode] = {
                "real_vec": real_vec.tolist(),
                "per_sign_p": [round(float(x), 5) for x in per_sign_p],
                "all30": {"obs": obs30, "null_mean": mu30, "null_sd": sd30, "z": z30, "p": p30},
                "novel24": {"obs": obs_nov, "null_mean": mu_n, "null_sd": sd_n, "z": z_n, "p": p_n},
                "unseen_rep": {"n": n_unseen_rep, "obs": obs_rep, "null_mean": mu_r, "null_sd": sd_r, "z": z_r, "p": p_r},
            }

        # Direct Same-Etymon Polysemy (5,000 Domain-B permutations across the K signs)
        direct_mat = np.zeros((K, K), dtype=bool)
        for i in range(K):
            for j in range(K):
                direct_mat[i, j] = bool(np.any(inA[i] & inB[j]))
        real_dir = np.diag(direct_mat)
        null_dir30 = np.zeros(N_SHUF, dtype=np.float64)
        null_dir_nov = np.zeros(N_SHUF, dtype=np.float64)
        nov_idxs = np.flatnonzero(novel_mask)
        for s_idx in range(N_SHUF):
            p30_d = rng.permutation(K)
            null_dir30[s_idx] = np.sum(direct_mat[np.arange(K), p30_d])
            pn_d = rng.permutation(n_novel)
            null_dir_nov[s_idx] = np.sum(direct_mat[nov_idxs, nov_idxs[pn_d]])
        d_mu30, d_sd30, d_z30, d_p30 = p_and_z(int(real_dir.sum()), null_dir30)
        d_mun, d_sdn, d_zn, d_pn = p_and_z(int(real_dir[novel_mask].sum()), null_dir_nov)
        mode_out["direct_poly"] = {
            "real_vec": real_dir.tolist(),
            "per_sign_offdiag": [round(float(x), 4) for x in direct_mat.mean(axis=1)],
            "all30": {"obs": int(real_dir.sum()), "null_mean": d_mu30, "null_sd": d_sd30, "z": d_z30, "p": d_p30},
            "novel24": {"obs": int(real_dir[novel_mask].sum()), "null_mean": d_mun, "null_sd": d_sdn, "z": d_zn, "p": d_pn},
        }

        # Extract exact audited bridges for every sign in this family
        bridges_per_sign = []
        for idx in range(K):
            s_bridges = []
            # Direct
            for ei in np.flatnonzero(inA[idx] & inB[idx]):
                s_bridges.append(("DIRECT", L.eids[ei], L.hws[ei], L.senses[ei][0][:55], "", "", ""))
            # Distinct-cluster rebus
            for ml, mk, kl in (
                ("PhonEx", "phon_exact", L.phons),
                ("PhonSt", "phon_stem", L.phon_stems),
                ("AscEx", "ascii_exact", L.asciis),
            ):
                kmap = L.key_maps[mk]
                bset = set(np.flatnonzero(inB[idx]).tolist())
                for ea in np.flatnonzero(inA[idx]):
                    ca = L.cid_int[ea]
                    for k in kl[ea]:
                        for eb in kmap.get(k, ()):
                            if eb in bset and eb != ea and L.cid_int[eb] != ca and not inA[idx, eb]:
                                s_bridges.append((
                                    ml, L.eids[ea], L.hws[ea], L.senses[ea][0][:40],
                                    L.eids[eb], L.hws[eb], L.senses[eb][0][:40],
                                ))
            bridges_per_sign.append(s_bridges)
        all_fam_bridges[fam_label] = bridges_per_sign

        row = {
            "family": fam_label,
            "group": group_tag,
            "dict": dict_name,
            "single_hw": single_hw,
            "n_etyma": L.E,
            "n_edges_phonex": len(L.edges["phon_exact"][0]),
            "n_edges_phonst": len(L.edges["phon_stem"][0]),
            "all30_phonex_obs": mode_out["phon_exact"]["all30"]["obs"],
            "all30_phonex_null": mode_out["phon_exact"]["all30"]["null_mean"],
            "all30_phonex_z": mode_out["phon_exact"]["all30"]["z"],
            "all30_phonex_p": mode_out["phon_exact"]["all30"]["p"],
            "all30_phonst_obs": mode_out["phon_stem"]["all30"]["obs"],
            "all30_phonst_null": mode_out["phon_stem"]["all30"]["null_mean"],
            "all30_phonst_z": mode_out["phon_stem"]["all30"]["z"],
            "all30_phonst_p": mode_out["phon_stem"]["all30"]["p"],
            "all30_ascex_obs": mode_out["ascii_exact"]["all30"]["obs"],
            "all30_ascex_null": mode_out["ascii_exact"]["all30"]["null_mean"],
            "all30_ascex_z": mode_out["ascii_exact"]["all30"]["z"],
            "all30_ascex_p": mode_out["ascii_exact"]["all30"]["p"],
            "all30_direct_obs": mode_out["direct_poly"]["all30"]["obs"],
            "all30_direct_null": mode_out["direct_poly"]["all30"]["null_mean"],
            "all30_direct_z": mode_out["direct_poly"]["all30"]["z"],
            "all30_direct_p": mode_out["direct_poly"]["all30"]["p"],
            "nov24_phonex_obs": mode_out["phon_exact"]["novel24"]["obs"],
            "nov24_phonex_null": mode_out["phon_exact"]["novel24"]["null_mean"],
            "nov24_phonex_z": mode_out["phon_exact"]["novel24"]["z"],
            "nov24_phonex_p": mode_out["phon_exact"]["novel24"]["p"],
            "nov24_phonst_obs": mode_out["phon_stem"]["novel24"]["obs"],
            "nov24_phonst_null": mode_out["phon_stem"]["novel24"]["null_mean"],
            "nov24_phonst_z": mode_out["phon_stem"]["novel24"]["z"],
            "nov24_phonst_p": mode_out["phon_stem"]["novel24"]["p"],
            "nov24_ascex_obs": mode_out["ascii_exact"]["novel24"]["obs"],
            "nov24_ascex_null": mode_out["ascii_exact"]["novel24"]["null_mean"],
            "nov24_ascex_z": mode_out["ascii_exact"]["novel24"]["z"],
            "nov24_ascex_p": mode_out["ascii_exact"]["novel24"]["p"],
            "nov24_direct_obs": mode_out["direct_poly"]["novel24"]["obs"],
            "nov24_direct_null": mode_out["direct_poly"]["novel24"]["null_mean"],
            "nov24_direct_z": mode_out["direct_poly"]["novel24"]["z"],
            "nov24_direct_p": mode_out["direct_poly"]["novel24"]["p"],
            "unseen_rep_n": n_unseen_rep,
            "unseen_rep_phonex_obs": mode_out["phon_exact"]["unseen_rep"]["obs"],
            "unseen_rep_phonex_null": mode_out["phon_exact"]["unseen_rep"]["null_mean"],
            "unseen_rep_phonex_z": mode_out["phon_exact"]["unseen_rep"]["z"],
            "unseen_rep_phonex_p": mode_out["phon_exact"]["unseen_rep"]["p"],
            "unseen_rep_phonst_obs": mode_out["phon_stem"]["unseen_rep"]["obs"],
            "unseen_rep_phonst_null": mode_out["phon_stem"]["unseen_rep"]["null_mean"],
            "unseen_rep_phonst_z": mode_out["phon_stem"]["unseen_rep"]["z"],
            "unseen_rep_phonst_p": mode_out["phon_stem"]["unseen_rep"]["p"],
        }
        fam_summary_rows.append(row)

        log(
            f"  [{fam_label:18s} E={L.E:4d}] All30: PhonEx={row['all30_phonex_obs']:2d}/30(mu={row['all30_phonex_null']:.2f},P={row['all30_phonex_p']:.5f}) "
            f"PhonSt={row['all30_phonst_obs']:2d}/30(mu={row['all30_phonst_null']:.2f},P={row['all30_phonst_p']:.5f}) "
            f"Dir={row['all30_direct_obs']:2d}/30(P={row['all30_direct_p']:.5f}) | "
            f"Nov24: PhonSt={row['nov24_phonst_obs']:2d}/{n_novel}(P={row['nov24_phonst_p']:.5f}) | "
            f"UnseenRep{n_unseen_rep}: PhonSt={row['unseen_rep_phonst_obs']:2d}/{n_unseen_rep}(P={row['unseen_rep_phonst_p']:.5f})"
        )

        if fam_label == "Dravidian":
            pdrav_details = (L, inA, inB, mode_out, bridges_per_sign)
        elif fam_label == "Dravidian_RawPDrav":
            pdrav_raw_details = (L, mode_out)
        elif fam_label == "Dravidian_2Lang":
            pdrav_2lg_details = (L, mode_out, bridges_per_sign)

    with open(os.path.join(OUT_DIR, "test4b1_7family_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fam_summary_rows[0].keys()))
        w.writeheader()
        w.writerows(fam_summary_rows)

    return fam_summary_rows, pdrav_details, pdrav_raw_details, pdrav_2lg_details, adj19, kinds_l, kinds_n, rep_map


# ==============================================================================
# 5. TEST 4B-2: 1-BLANK-SLOT CONSTRAINED COMPOUND & CONTEXTUAL DECODER
# ==============================================================================
def run_test_4b2(lipi_int, new_int, ev_lipi, ev_new, etyma_2br, forms_phon, eid_to_cid, pdrav_details, rep_map):
    log(f"=== TEST 4B-2: 1-BLANK-SLOT CONSTRAINED COMPOUND & CONTEXTUAL DECODER (N_SHUF={N_SHUF}) ===")
    L_pdr, inA_pdr, inB_pdr, mode_out_pdr, bridges_pdr = pdrav_details

    # 5.1 Extract ALL 1-blank intact inscriptions & [KNOWN_L] - X - [KNOWN_R] sandwiches
    one_blank_pats_l = collections.Counter()
    one_blank_pats_n = collections.Counter()
    one_blank_by_x_l = collections.Counter()
    one_blank_by_x_n = collections.Counter()
    sandwiches_l = collections.Counter()
    sandwiches_n = collections.Counter()
    adj_known_l = collections.defaultdict(collections.Counter)
    adj_known_n = collections.defaultdict(collections.Counter)
    # Distinct texts per (X, nb, side)
    adj_known_txts_l = collections.defaultdict(set)
    adj_known_txts_n = collections.defaultdict(set)

    top30_set = {rec[0] for rec in WAVE2_SPECS}

    for tag, sub in (("L", lipi_int), ("N", new_int)):
        for r in sub:
            toks = [t for t in r["signs"].split("-") if t and t != "000"]
            if len(toks) < 2:
                continue
            ft = "-".join(toks)
            unk_idxs = [i for i, t in enumerate(toks) if t not in KNOWN_SET]
            if len(unk_idxs) == 1:
                x = toks[unk_idxs[0]]
                if tag == "L":
                    one_blank_pats_l[(x, ft)] += 1
                    one_blank_by_x_l[x] += 1
                else:
                    one_blank_pats_n[(x, ft)] += 1
                    one_blank_by_x_n[x] += 1
            for i, t in enumerate(toks):
                if t in top30_set:
                    if i > 0 and toks[i - 1] in KNOWN_SET:
                        if tag == "L":
                            adj_known_l[t][(toks[i - 1], "L")] += 1
                            adj_known_txts_l[(t, toks[i - 1], "L")].add(ft)
                        else:
                            adj_known_n[t][(toks[i - 1], "L")] += 1
                            adj_known_txts_n[(t, toks[i - 1], "L")].add(ft)
                    if i + 1 < len(toks) and toks[i + 1] in KNOWN_SET:
                        if tag == "L":
                            adj_known_l[t][(toks[i + 1], "R")] += 1
                            adj_known_txts_l[(t, toks[i + 1], "R")].add(ft)
                        else:
                            adj_known_n[t][(toks[i + 1], "R")] += 1
                            adj_known_txts_n[(t, toks[i + 1], "R")].add(ft)
                if 0 < i < len(toks) - 1 and toks[i] not in KNOWN_SET and toks[i - 1] in KNOWN_SET and toks[i + 1] in KNOWN_SET:
                    if tag == "L":
                        sandwiches_l[(toks[i - 1], toks[i], toks[i + 1])] += 1
                    else:
                        sandwiches_n[(toks[i - 1], toks[i], toks[i + 1])] += 1

    # Save recurring 1-blank intact patterns & sandwiches
    pat_rows = []
    for (x, ft), cl in one_blank_pats_l.most_common():
        cn = one_blank_pats_n[(x, ft)]
        if cl >= 2 or (cl >= 1 and cn >= 1):
            pat_rows.append({
                "blank_sign": x, "in_top30": x in top30_set,
                "pattern": ft, "lipi_intact_count": cl, "new_intact_count": cn,
            })
    with open(os.path.join(OUT_DIR, "test4b2_one_blank_patterns.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(pat_rows[0].keys()))
        w.writeheader()
        w.writerows(pat_rows)

    sand_rows = []
    for (l_s, x, r_s), cl in sandwiches_l.most_common():
        cn = sandwiches_n[(l_s, x, r_s)]
        if cl >= 2 or (cl >= 1 and cn >= 1):
            sand_rows.append({
                "left_locked": l_s, "left_root": KNOWN_INFO[l_s]["roots"][0],
                "blank_sign": x, "in_top30": x in top30_set,
                "right_locked": r_s, "right_root": KNOWN_INFO[r_s]["roots"][0],
                "lipi_count": cl, "new_count": cn,
            })
    with open(os.path.join(OUT_DIR, "test4b2_sandwiches.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sand_rows[0].keys()))
        w.writeheader()
        w.writerows(sand_rows)

    # 5.3 Strict Etymological DEDR Compound Lookup between EVERY KNOWN sign and EVERY etymon in L_pdr
    # Guard against 2-char suffixal noise (-ka/-ma/-ko), inflectional suffixes, and Malayalam -kka/-uka infinitives
    BAD_COMP_ROOTS = {"mai", "kai", "avaQ", "ukkam", "ukku", "utti"}

    def is_valid_comp_rec(rec, ec, k_cids, kph, eph):
        if not ((rec["cid"] == ec or rec["cid"] in k_cids) and len(rec["phon"]) >= len(kph) + len(eph) - 1):
            return False
        if rec["lang"] == "Ma" and (rec["ascii"].endswith("kka") or rec["ascii"].endswith("uka")):
            return False
        return True

    # Map each KNOWN sign -> set of L_pdr indices that form a strict etymological DEDR compound on L or R
    known_list = sorted(KNOWN_SET)
    known_cids = {ks: {eid_to_cid.get(e, e) for e in KNOWN_INFO[ks]["eids"]} for ks in known_list}
    comp_L = {}  # ks -> dict[e_idx] = (kr, rec) where ks + X is attested
    comp_R = {}  # ks -> dict[e_idx] = (kr, rec) where X + ks is attested

    e_cids = [eid_to_cid.get(L_pdr.eids[i], L_pdr.cids[i]) for i in range(L_pdr.E)]
    for ks in known_list:
        cL = {}
        cR = {}
        k_roots = KNOWN_INFO[ks]["roots"]
        k_cids = known_cids[ks]
        for kr in k_roots:
            kph = k2.norm_phon(kr)
            if len(kph) < 2:
                continue
            for ei in range(L_pdr.E):
                eph = L_pdr.phons[ei][0]
                if len(eph) < 3 or eph in BAD_COMP_ROOTS:
                    continue
                ehw = L_pdr.hws[ei]
                ec = e_cids[ei]
                # ks (L) + X
                if ei not in cL:
                    for j in k3.dravidian_sandhi_joins(kr, ehw, "phon"):
                        recs = forms_phon.get(j)
                        if recs:
                            for rec in recs:
                                if is_valid_comp_rec(rec, ec, k_cids, kph, eph):
                                    cL[ei] = (kr, rec)
                                    break
                        if ei in cL:
                            break
                # X + ks (R)
                if ei not in cR:
                    for j in k3.dravidian_sandhi_joins(ehw, kr, "phon"):
                        recs = forms_phon.get(j)
                        if recs:
                            for rec in recs:
                                if is_valid_comp_rec(rec, ec, k_cids, kph, eph):
                                    cR[ei] = (kr, rec)
                                    break
                        if ei in cR:
                            break
        comp_L[ks] = cL
        comp_R[ks] = cR

    # For each Top-30 sign X, precompute which etyma form a DEDR compound with X's recurring (n>=2 Lipi) KNOWN neighbors
    K = len(WAVE2_SPECS)
    has_comp_mat = np.zeros((K, L_pdr.E), dtype=bool)
    comp_weight_mat = np.zeros((K, L_pdr.E), dtype=np.float64)
    comp_details = collections.defaultdict(list)  # (idx, ei) -> list of strings

    for idx, rec in enumerate(WAVE2_SPECS):
        s = rec[0]
        for (ks, side), cnt_l in adj_known_l[s].items():
            if cnt_l < 2:
                continue
            cnt_n = adj_known_n[s][(ks, side)]
            n_dist_l = len(adj_known_txts_l[(s, ks, side)])
            cmap = comp_L[ks] if side == "L" else comp_R[ks]
            for ei, (kr, drec) in cmap.items():
                has_comp_mat[idx, ei] = True
                comp_weight_mat[idx, ei] += math.log1p(n_dist_l + cnt_n)
                expr = f"{ks}({kr})+{s}({L_pdr.hws[ei]})" if side == "L" else f"{s}({L_pdr.hws[ei]})+{ks}({kr})"
                comp_details[(idx, ei)].append(
                    f"{expr}[{cnt_l}L/{cnt_n}N]->DEDR {drec['eid']} {drec['lang']}.{drec['hw']}({drec['gloss'][:32]})"
                )

    # Precompute rebus-connected etyma for each Top-30 sign (Domain-A etymon with a PhonSt rebus to Domain-B)
    rebus_A_mat = np.zeros((K, L_pdr.E), dtype=bool)
    U_st, V_st = L_pdr.edges["phon_stem"]
    diff_c = (L_pdr.cid_int[U_st] != L_pdr.cid_int[V_st])
    U_st, V_st = U_st[diff_c], V_st[diff_c]
    for idx in range(K):
        # Mark Domain-A etyma that bridge to Domain-B via distinct-cluster PhonSt OR are direct polysemy
        direct_e = inA_pdr[idx] & inB_pdr[idx]
        rebus_A_mat[idx] |= direct_e
        # Check edges
        a_u, a_v = inA_pdr[idx, U_st], inA_pdr[idx, V_st]
        b_u, b_v = inB_pdr[idx, U_st], inB_pdr[idx, V_st]
        m1 = a_u & b_v & (~a_v)
        m2 = a_v & b_u & (~a_u)
        if np.any(m1):
            rebus_A_mat[idx, U_st[m1]] = True
        if np.any(m2):
            rebus_A_mat[idx, V_st[m2]] = True

    # Observed joint metrics on Top 30:
    # (M1) Visual-Picture (inA) + Attested DEDR Compound with recurring LOCKED neighbor
    obs_vis_comp_vec = np.any(inA_pdr & has_comp_mat, axis=1)
    # (M2) Visual+Arch Bridge (Direct OR PhonSt Rebus) + Attested DEDR Compound with recurring LOCKED neighbor
    obs_triple_vec = np.any(rebus_A_mat & has_comp_mat, axis=1)
    # (M3) Head-Final Syntactic Tier Lock across ALL [LOCKED19] - X and X - [LOCKED19] bigrams!
    # Check if the 30 signs' predicted syntactic tiers (Modifier/Commodity=0, House/Slot=1, Closer/Title=2)
    # align head-finally with our 19 locked signs' tiers on BOTH Lipi and unseen New Texts!
    def compute_tier_order(tiers_30, adj_dict):
        fwd = 0
        rev = 0
        for idx, rec in enumerate(WAVE2_SPECS):
            s = rec[0]
            tx = tiers_30[idx]
            for (ks, side), cnt in adj_dict[s].items():
                if ks not in LOCKED19_INFO:
                    continue
                tk = LOCKED19_INFO[ks]["tier"]
                if tx == tk:
                    continue
                if side == "L":
                    # ks then s: head-final expects tk < tx
                    if tk < tx:
                        fwd += cnt
                    else:
                        rev += cnt
                else:
                    # s then ks: head-final expects tx < tk
                    if tx < tk:
                        fwd += cnt
                    else:
                        rev += cnt
        tot = fwd + rev
        return fwd, rev, (fwd / tot if tot > 0 else 0.0)

    real_tiers_30 = np.array([rec[7] for rec in WAVE2_SPECS], dtype=np.int32)
    hf_l_fwd, hf_l_rev, hf_l_rate = compute_tier_order(real_tiers_30, adj_known_l)
    hf_n_fwd, hf_n_rev, hf_n_rate = compute_tier_order(real_tiers_30, adj_known_n)

    # 5.4 Run 5,000-Shuffle Benchmarks for Test 4B-2!
    rng = np.random.default_rng(20261126)
    null_vis_comp = np.zeros(N_SHUF, dtype=np.float64)
    null_triple = np.zeros(N_SHUF, dtype=np.float64)
    null_hf_l = np.zeros(N_SHUF, dtype=np.float64)
    null_hf_n = np.zeros(N_SHUF, dtype=np.float64)

    # Precompute per-sign compound-active edge arrays for ultra-fast cluster-preserving shuffle!
    for s_idx in range(N_SHUF):
        perm = L_pdr.make_cluster_perm(rng)
        # Under cluster-preserving sound shuffle: etymon i gets sound of slot inv, i.e., has_comp_mat[:, perm]
        hc_shuf = has_comp_mat[:, perm]
        null_vis_comp[s_idx] = float(np.sum(np.any(inA_pdr & hc_shuf, axis=1)))
        # Recompute rebus_A_mat under perm!
        eu, ev = perm[U_st], perm[V_st]
        # Note: diff_c already holds under cluster-preserving perm because perm preserves cid strata!
        # Check if ANY sign has an etymon that is (direct OR rebus under perm) AND in hc_shuf
        # Fast exact check per sign:
        tr_hits = 0
        for idx in range(K):
            a_row = inA_pdr[idx]
            b_row = inB_pdr[idx]
            hc_row = hc_shuf[idx]
            if not np.any(hc_row & a_row):
                continue
            if np.any(a_row & b_row & hc_row):
                tr_hits += 1
                continue
            # Check rebus edges where the A-endpoint is ALSO in hc_row!
            a_u, a_v = a_row[eu], a_row[ev]
            b_u, b_v = b_row[eu], b_row[ev]
            hc_u, hc_v = hc_row[eu], hc_row[ev]
            if np.any((a_u & hc_u & b_v & (~a_v)) | (a_v & hc_v & b_u & (~a_u))):
                tr_hits += 1
        null_triple[s_idx] = tr_hits

        # Syntactic tier shuffle across the 30 signs (preserves exact tier counts!)
        tp = real_tiers_30[rng.permutation(K)]
        null_hf_l[s_idx] = compute_tier_order(tp, adj_known_l)[2]
        null_hf_n[s_idx] = compute_tier_order(tp, adj_known_n)[2]

    # Also test Within-Known-Sign Permutation (5,000x) for M1 (Visual + DEDR Compound):
    # Randomly permute which KNOWN sound root maps to which KNOWN sign!
    # Map each sign X -> list of (ks_idx, side) recurring neighbors
    ks_to_idx = {ks: i for i, ks in enumerate(known_list)}
    n_ks = len(known_list)
    # Precompute bool matrix M_L[ks_idx, k_sign] = any(inA[k_sign] & comp_L[ks])
    M_L = np.zeros((n_ks, K), dtype=bool)
    M_R = np.zeros((n_ks, K), dtype=bool)
    M_tr_L = np.zeros((n_ks, K), dtype=bool)
    M_tr_R = np.zeros((n_ks, K), dtype=bool)
    for ki, ks in enumerate(known_list):
        cL_idxs = list(comp_L[ks].keys())
        cR_idxs = list(comp_R[ks].keys())
        for idx in range(K):
            if cL_idxs:
                M_L[ki, idx] = bool(np.any(inA_pdr[idx, cL_idxs]))
                M_tr_L[ki, idx] = bool(np.any(rebus_A_mat[idx, cL_idxs]))
            if cR_idxs:
                M_R[ki, idx] = bool(np.any(inA_pdr[idx, cR_idxs]))
                M_tr_R[ki, idx] = bool(np.any(rebus_A_mat[idx, cR_idxs]))

    sign_nb_L = [[ks_to_idx[ks] for (ks, side), c in adj_known_l[rec[0]].items() if c >= 2 and side == "L"] for rec in WAVE2_SPECS]
    sign_nb_R = [[ks_to_idx[ks] for (ks, side), c in adj_known_l[rec[0]].items() if c >= 2 and side == "R"] for rec in WAVE2_SPECS]

    null_wk_vis = np.zeros(N_SHUF, dtype=np.float64)
    null_wk_tr = np.zeros(N_SHUF, dtype=np.float64)
    for s_idx in range(N_SHUF):
        kp = rng.permutation(n_ks)
        vc = 0
        tc = 0
        for idx in range(K):
            nL = sign_nb_L[idx]
            nR = sign_nb_R[idx]
            if (nL and np.any(M_L[kp[nL], idx])) or (nR and np.any(M_R[kp[nR], idx])):
                vc += 1
            if (nL and np.any(M_tr_L[kp[nL], idx])) or (nR and np.any(M_tr_R[kp[nR], idx])):
                tc += 1
        null_wk_vis[s_idx] = vc
        null_wk_tr[s_idx] = tc

    obs_vc = int(obs_vis_comp_vec.sum())
    obs_tr = int(obs_triple_vec.sum())

    # 5.5 TEST 4B-2b REDESIGN:
    # (1) Full 49-Sign (19 Locked + 30 Wave-2) Head-Final Syntactic Tier Order Lock (5,000 tier permutations)
    #     across ALL intact cross-tier bigrams in Lipi (3,600) AND held-out unseen Mahadevan new texts (627).
    all49_signs = sorted(LOCKED19_SET | top30_set)
    s49_idx = {s: i for i, s in enumerate(all49_signs)}
    tier49_real = np.array([
        LOCKED19_INFO[s]["tier"] if s in LOCKED19_INFO else WAVE2_SPECS[[r[0] for r in WAVE2_SPECS].index(s)][7]
        for s in all49_signs
    ], dtype=np.int32)

    def extract_49_bigrams(rows):
        bg = collections.Counter()
        for r in rows:
            toks = [t for t in r["signs"].split("-") if t and t != "000"]
            for i in range(len(toks) - 1):
                a, b = toks[i], toks[i + 1]
                if a in s49_idx and b in s49_idx:
                    bg[(s49_idx[a], s49_idx[b])] += 1
        if not bg:
            return np.zeros(0, dtype=np.int32), np.zeros(0, dtype=np.int32), np.zeros(0, dtype=np.int32)
        u = np.array([k[0] for k in bg], dtype=np.int32)
        v = np.array([k[1] for k in bg], dtype=np.int32)
        w = np.array(list(bg.values()), dtype=np.int32)
        return u, v, w

    def eval_49_hf(tiers, u, v, w, weighted=True):
        tu, tv = tiers[u], tiers[v]
        diff = tu != tv
        if not np.any(diff):
            return 0, 0, 0.0
        if weighted:
            fwd = int(w[diff & (tu < tv)].sum())
            rev = int(w[diff & (tu > tv)].sum())
        else:
            fwd = int(np.sum(diff & (tu < tv)))
            rev = int(np.sum(diff & (tu > tv)))
        tot = fwd + rev
        return fwd, rev, (fwd / tot if tot > 0 else 0.0)

    u49_l, v49_l, w49_l = extract_49_bigrams(lipi_int)
    u49_n, v49_n, w49_n = extract_49_bigrams(new_int)
    hf49_l_tok = eval_49_hf(tier49_real, u49_l, v49_l, w49_l, weighted=True)
    hf49_l_typ = eval_49_hf(tier49_real, u49_l, v49_l, w49_l, weighted=False)
    hf49_n_tok = eval_49_hf(tier49_real, u49_n, v49_n, w49_n, weighted=True)
    hf49_n_typ = eval_49_hf(tier49_real, u49_n, v49_n, w49_n, weighted=False)

    null_49_l_tok = np.zeros(N_SHUF, dtype=np.float64)
    null_49_l_typ = np.zeros(N_SHUF, dtype=np.float64)
    null_49_n_tok = np.zeros(N_SHUF, dtype=np.float64)
    null_49_n_typ = np.zeros(N_SHUF, dtype=np.float64)
    rng49 = np.random.default_rng(20261127)
    n49 = len(all49_signs)
    for s_idx in range(N_SHUF):
        tp49 = tier49_real[rng49.permutation(n49)]
        null_49_l_tok[s_idx] = eval_49_hf(tp49, u49_l, v49_l, w49_l, weighted=True)[2]
        null_49_l_typ[s_idx] = eval_49_hf(tp49, u49_l, v49_l, w49_l, weighted=False)[2]
        null_49_n_tok[s_idx] = eval_49_hf(tp49, u49_n, v49_n, w49_n, weighted=True)[2]
        null_49_n_typ[s_idx] = eval_49_hf(tp49, u49_n, v49_n, w49_n, weighted=False)[2]

    # (2) Held-Out Unseen `new texts` Physical Object-Class / Zone Replication Summary
    def binom_sf(k, n, p0):
        return sum(math.comb(n, i) * (p0 ** i) * ((1.0 - p0) ** (n - i)) for i in range(k, n + 1))

    new_attested = [rec[0] for rec in WAVE2_SPECS if rep_map[rec[0]]["new"]["tot"] >= 1]
    new_rep_or15 = [s for s in new_attested if rep_map[s]["new"]["or"] >= 1.5]
    new_rep_p05 = [s for s in new_attested if rep_map[s]["new"]["p"] < 0.05]
    new_rep_binom_p = binom_sf(len(new_rep_p05), len(new_attested), 0.05)

    # Build per-sign 1-blank constrained decoder table
    decoder_rows = []
    for idx, rec in enumerate(WAVE2_SPECS):
        s, is_nov, sh_lab, wAe, wBe, _, _, exp_tier, tgt = rec
        rep = rep_map[s]
        # Collect top visual+compound and triple-lock candidates
        tr_cands = []
        vc_cands = []
        for ei in np.flatnonzero(has_comp_mat[idx]):
            if rebus_A_mat[idx, ei]:
                tr_cands.append((comp_weight_mat[idx, ei], ei))
            elif inA_pdr[idx, ei]:
                vc_cands.append((comp_weight_mat[idx, ei], ei))
        tr_cands.sort(reverse=True)
        vc_cands.sort(reverse=True)
        top_sand = [
            f"{l}-{s}-{r}({cl}L/{sandwiches_n[(l,s,r)]}N)"
            for (l, x, r), cl in sandwiches_l.most_common() if x == s and cl >= 2
        ][:3]
        top_1b = [
            f"{ft}({cl}L/{one_blank_pats_n[(s,ft)]}N)"
            for (x, ft), cl in one_blank_pats_l.most_common() if x == s and cl >= 2
        ][:3]
        decoder_rows.append({
            "sign": s,
            "one_blank_lipi": one_blank_by_x_l[s],
            "one_blank_new": one_blank_by_x_n[s],
            "top_1blank_patterns": " | ".join(top_1b),
            "top_sandwiches": " | ".join(top_sand),
            "vis_comp_hit": bool(obs_vis_comp_vec[idx]),
            "triple_lock_hit": bool(obs_triple_vec[idx]),
            "triple_lock_compounds": " ; ".join(comp_details[(idx, ei)][0] for _, ei in tr_cands[:2]),
            "vis_only_compounds": " ; ".join(comp_details[(idx, ei)][0] for _, ei in vc_cands[:2]),
            "arch_target": f"{tgt[0]}:{','.join(sorted(tgt[1]))}",
            "lipi_arch_hits": f"{rep['lipi']['hits']}/{rep['lipi']['tot']}",
            "lipi_arch_or": rep["lipi"]["or"],
            "lipi_arch_p": rep["lipi"]["p"],
            "new_arch_hits": f"{rep['new']['hits']}/{rep['new']['tot']}",
            "new_arch_or": rep["new"]["or"],
            "new_arch_p": rep["new"]["p"],
        })

    with open(os.path.join(OUT_DIR, "test4b2_constrained_decoder.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(decoder_rows[0].keys()))
        w.writeheader()
        w.writerows(decoder_rows)

    summary_4b2 = {
        "n_shuf": N_SHUF,
        "total_1blank_intact_lipi": int(sum(one_blank_by_x_l.values())),
        "total_1blank_intact_new": int(sum(one_blank_by_x_n.values())),
        "top30_1blank_intact_lipi": int(sum(one_blank_by_x_l[r[0]] for r in WAVE2_SPECS)),
        "top30_1blank_intact_new": int(sum(one_blank_by_x_n[r[0]] for r in WAVE2_SPECS)),
        "test4b2a_raw_dedr_compound_honest_null": {
            "vis_plus_dedr_comp_lexshuf": {
                "obs": obs_vc, **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(obs_vc, null_vis_comp)))
            },
            "triple_lock_vis_rebus_comp_lexshuf": {
                "obs": obs_tr, **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(obs_tr, null_triple)))
            },
            "vis_plus_dedr_comp_within_known_perm": {
                "obs": obs_vc, **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(obs_vc, null_wk_vis)))
            },
            "triple_lock_within_known_perm": {
                "obs": obs_tr, **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(obs_tr, null_wk_tr)))
            },
        },
        "test4b2b_redesign_head_final_and_unseen_replication": {
            "wave2_vs_locked19_lipi": {
                "fwd": hf_l_fwd, "rev": hf_l_rev, "rate": round(hf_l_rate, 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf_l_rate, null_hf_l)))
            },
            "wave2_vs_locked19_new": {
                "fwd": hf_n_fwd, "rev": hf_n_rev, "rate": round(hf_n_rate, 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf_n_rate, null_hf_n)))
            },
            "full49_head_final_lipi_tokens": {
                "fwd": hf49_l_tok[0], "rev": hf49_l_tok[1], "rate": round(hf49_l_tok[2], 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf49_l_tok[2], null_49_l_tok)))
            },
            "full49_head_final_lipi_types": {
                "fwd": hf49_l_typ[0], "rev": hf49_l_typ[1], "rate": round(hf49_l_typ[2], 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf49_l_typ[2], null_49_l_typ)))
            },
            "full49_head_final_new_tokens": {
                "fwd": hf49_n_tok[0], "rev": hf49_n_tok[1], "rate": round(hf49_n_tok[2], 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf49_n_tok[2], null_49_n_tok)))
            },
            "full49_head_final_new_types": {
                "fwd": hf49_n_typ[0], "rev": hf49_n_typ[1], "rate": round(hf49_n_typ[2], 4),
                **dict(zip(("null_mean", "null_sd", "z", "p"), p_and_z(hf49_n_typ[2], null_49_n_typ)))
            },
            "unseen_new_physical_replication": {
                "n_attested_in_new": len(new_attested),
                "n_or_ge_1_5": len(new_rep_or15),
                "pct_or_ge_1_5": round(100.0 * len(new_rep_or15) / max(1, len(new_attested)), 1),
                "n_p_lt_005": len(new_rep_p05),
                "pct_p_lt_005": round(100.0 * len(new_rep_p05) / max(1, len(new_attested)), 1),
                "exact_binom_p_vs_5pct": float(f"{new_rep_binom_p:.3e}"),
                "replicated_p05_signs": new_rep_p05,
            },
        },
    }
    with open(os.path.join(OUT_DIR, "test4b2_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_4b2, f, indent=2, ensure_ascii=False)

    log(f"4B-2 1-Blank Intact Faces: Lipi={summary_4b2['total_1blank_intact_lipi']}/3600 (Top30={summary_4b2['top30_1blank_intact_lipi']}), "
        f"New={summary_4b2['total_1blank_intact_new']}/627 (Top30={summary_4b2['top30_1blank_intact_new']})")
    a2 = summary_4b2["test4b2a_raw_dedr_compound_honest_null"]
    b2 = summary_4b2["test4b2b_redesign_head_final_and_unseen_replication"]
    log(f"4B-2a [HONEST NULL] Vis+DEDR Comp: obs={obs_vc}/30 (LexShuf P={a2['vis_plus_dedr_comp_lexshuf']['p']}, WK P={a2['vis_plus_dedr_comp_within_known_perm']['p']}); "
        f"Triple-Lock: obs={obs_tr}/30 (LexShuf P={a2['triple_lock_vis_rebus_comp_lexshuf']['p']}, WK P={a2['triple_lock_within_known_perm']['p']})")
    log(f"4B-2b [REDESIGN] Full-49 Head-Final Tier Lock: "
        f"Lipi tok {hf49_l_tok[0]}:{hf49_l_tok[1]} ({100*hf49_l_tok[2]:.1f}%, P={b2['full49_head_final_lipi_tokens']['p']}), "
        f"Lipi types {hf49_l_typ[0]}:{hf49_l_typ[1]} ({100*hf49_l_typ[2]:.1f}%, P={b2['full49_head_final_lipi_types']['p']}) | "
        f"New tok {hf49_n_tok[0]}:{hf49_n_tok[1]} ({100*hf49_n_tok[2]:.1f}%, P={b2['full49_head_final_new_tokens']['p']}), "
        f"New types {hf49_n_typ[0]}:{hf49_n_typ[1]} ({100*hf49_n_typ[2]:.1f}%, P={b2['full49_head_final_new_types']['p']})")
    rep_s = b2["unseen_new_physical_replication"]
    log(f"4B-2b [REDESIGN] Held-Out Unseen New Physical Replication: "
        f"{rep_s['n_or_ge_1_5']}/{rep_s['n_attested_in_new']} ({rep_s['pct_or_ge_1_5']}%) at OR>=1.5; "
        f"{rep_s['n_p_lt_005']}/{rep_s['n_attested_in_new']} ({rep_s['pct_p_lt_005']}%) clear p<0.05 individually "
        f"(exact binomial P={rep_s['exact_binom_p_vs_5pct']})")
    return summary_4b2, decoder_rows


# ==============================================================================
# 6. STRICT EPISTEMIC CLASSIFICATION & COVERAGE ACCOUNTING (BEFORE VS AFTER)
# ==============================================================================
# Curated strictly from the audited zero-artifact single-headword DEDR hits (never guessing!)
AUDITED_WAVE2_TABLE = {
    # --- BUILDING ON IT (clean zero-artifact Single-HW 2-branch Proto-Dravidian lock + context lock) ---
    "892": ("*vil", "PhonEx DEDR 5422 vil ('bow') <-> 5421 vil ('to sell, sale, price') [p_shuf=0.015]; tag 2.7x, mtab 1.7x", "building on it"),
    "615": ("*accu", "PhonEx DEDR 48 accu ('weaver's reed/frame') <-> 49 accu ('field ridge, land divided') [p_shuf=0.030]; ctab 10.0x L / 4.8x N, MD VS craft 4.6x L / 2.5x N", "building on it"),
    "503": ("*malai ~ *mālai", "PhonEx DEDR 4742 malai ('hill, mountain') <-> 4827 mālai ('garland, necklace, strung beads') + 2178/2176 kō; MD VS bead/dye 5.2x L / 4.9x N, ctab 8.6x L / 4.3x N", "building on it"),
    "590": ("*mūṭai", "PhonEx DEDR 4927 muṭai ('plait/basket') <-> 5037 mūṭai ('sack-load, bale, packed bundle'); 590-390 73x cotton-bale house, har_F_granary 3.1x, tag 1.8x N", "building on it"),
    "415": ("*kavar", "PhonEx DEDR 1325 kavar ('fork, branch, prong') <-> 1326 kavar ('seize, grasp, control'); 415-220 87:0 L / 15:0 N, 415-100 43:0, 415-220-520 17x", "building on it"),
    "806": ("*kampu ~ *kāmpu", "PhonEx DEDR 1454 kāmpu ('flower-stalk, stem') <-> 1242 kampu ('bulrush/pearl millet, grain'); ctab 4.6x, bar-seal produce anchor", "building on it"),
    "233": ("*veṭi-mīṉ", "PhonEx DEDR 5473 veṭi ('crack, split') <-> 5475 veṭi ('dawn, break of day, light') + fish; 233-520 22L/1N, 235-233-705 7L/1N, ctab 3.0x", "building on it"),
    "407": ("*kōṭi", "PhonSt DEDR 2200 kōṭu ('branch of tree') <-> 2198 kōṭi ('newly purchased cloth, weaver'); ctab 13.5x, MD VS dyers 2.9x, 061-407-850 14x", "building on it"),
    "368": ("*koṭi ~ *koṭu", "PhonSt DEDR 2049 koṭi ('banner, flag') <-> 2053 koṭu ('give, grant, allow') + DIRECT 5414 virutu ('title, banner, pedigree'); har_F_granary 2.3x, 900-368 5x", "building on it"),
    "861": ("*kāṇam / *kaṇ", "PhonSt DEDR 1159 kaṇ ('eye') / 1443 kāṇ ('sight') <-> 1444 kāṇam ('ancient weight, 1/80 fraction, hereditary property'); 003-861 29x, 861-002 136L/28N", "building on it"),
    "700": ("*aḷa / *akal", "PhonSt DEDR 308 aḷai ('hollow') <-> 295 aḷa ('measure, capacity') + DIRECT 9 akal ('earthen bowl, measure of capacity'); mtab 3.5x L / 4.1x N, 410 1-blank faces", "building on it"),
    "151": ("*kā", "PhonEx DEDR 1417 kā ('pole to carry loads') <-> 1416 kā ('preserve, shelter, guard'); 83% clause-final porter allograph of 154, 740-151 8L/4N", "building on it"),
    "741": ("*oru-kuṭi", "PhonSt DEDR 1651 kuṭam ('jar') <-> 1655 kuṭi ('house, family'); graphic compound [740 jar + 1 stroke], 500-741 15L/1N, Lothal L-124", "building on it"),
    "920": ("*tiṅkaḷ", "DIRECT DEDR 3213 tiṅkaḷ ('moon' <-> 'month'); graphic variant of 900 with medial leaf, 320-920 10L/3N (5/5 New tags/seals), 920-740 13L/4N", "building on it"),
    "140": ("*ammā", "DIRECT DEDR 183 ammā ('mother, matron, lady' <-> 'goddess'); md_citadel 3.5x N, Chanhu-daro 4.0x N, 003-140-100 5x", "building on it"),
    "840": ("*iṇai", "DIRECT DEDR 457 iṇai ('pair, couple' <-> 'join, unite, agree, equality'); bangle 5.9x, multi-party audit prisms, 840-032 35L/4N", "building on it"),
    "760": ("*kuruku / *koḻuntu", "DIRECT DEDR 1791 kuruku ('sprout, shoot' <-> 'young, child') & 2149 koḻuntu ('tendril, shoot' <-> 'young'); 760-740 79L/16N, rod 2.6x L / 15.2x N", "building on it"),
    "690": ("*kaṭṭu / *piṇai", "DIRECT DEDR 1147 kaṭṭu ('tie, fasten, bind' <-> 'bundle, packet, store, building'); 690-740 42L/3N, mtab 2.1x, har_F_granary 3.3x", "building on it"),

    # --- TESTING IT (promising single-domain, graphic compound, or rival-candidate leads) ---
    "706": ("*aḷa / *kalam?", "Graphic [700 cup + 1 long stroke] 12-cup measure (~111 L); echoes 700 aḷai/aḷa & 705 kalam; 706-033-923-740 11x; zero New intact tokens", "testing it"),
    "405": ("*all- / *tai?", "PhonSt DEDR 257 alli ('tree') <-> 260 allu ('knit, weave') & 3474/3473 tai (overlaps 390); 405-740 22L/6N, needs split from 390 & 407", "testing it"),
    "803": ("*il ~ *ilai", "DEDR 497 ilai ('leaf') <-> 494 il ('house'); sub-stem len 2 (<3 stem cutoff), fails automatic PhonEx/PhonSt; strong 803-415-220 Twin-Capital stem", "testing it"),
    "231": ("*naṭu~*nāṭu / *oru-mīṉ?", "PhonEx DEDR 3583 naṭu ('plant, set up') <-> 3638 nāṭu ('country, district') + fish; ctab 4.5x, 231-520 8L/1N, 231-705 8L/2N; rival: oru-mīṉ", "testing it"),
    "060": ("*kōṭu~*kūṭu / *uḷ?", "PhonSt DEDR 2054 koṭu ('curved/bent') <-> 1882 kūṭu ('join, unite') only in multi-HW; 93% medial oblique linker, 820-060 21L/3N", "testing it"),
    "156": ("*pai / *mūṭai?", "DIRECT DEDR 4450 pai ('bag, sack') & 003-156 36x (mū+pai~Te.muppai?); shares porter silhouette w/ 151/154, needs clean split from 151 & 590", "testing it"),
    "255": ("*mā~*maṉ / *mutal?", "PhonEx DEDR 4780 mā ('animal, beast') <-> 4774 maṉ ('king, warrior'); shape uncertain ('unknown asymmetric animal?'), mtab 1.7x, 705-255-740 6x", "testing it"),
    "817": ("*kāṇam / *peṭṭi?", "Double-diamond visual twin of 861 (817-002 122x vs 861-002 136x); zero New intact tokens (catalog split artifact with 861), no clean box rebus", "testing it"),

    # --- HONEST NULLS (zero clean Single-HW 2-branch Proto-Dravidian bridge) ---
    "240": ("(open)", "HONEST NULL: zero Single-HW 2-branch rebus for whisker/fin/cheek <-> star/bright/bead; only 220+240 miṉmiṉi reduplication (needs rescue via fin/ear etymon)", "null"),
    "798": ("(open)", "HONEST NULL: zero clean leaf+pincer <-> courtyard-mansion rebus in 2-branch DEDR (confirmed null from Key #3A)", "null"),
    "550": ("(open)", "HONEST NULL: zero clean mouth/pincer <-> gate/citadel rebus in 2-branch DEDR (vāy lacks 'gate/citadel' in raw DEDR glosses)", "null"),
    "142": ("(open)", "HONEST NULL: kōl ('staff') vs kō ('king') fails -l phonology (confirmed null from Key #3A; 061-142-400-740 4x needs new visual/domain angle)", "null"),
}


def build_epistemic_and_coverage(
    lipi_int, new_int, cnt_l, cnt_n, cnt_tot, shapes, anchors, sf_lex,
    pdrav_details, pdrav_raw_details, pdrav_2lg_details, adj19, kinds_l, kinds_n, decoder_rows
):
    L_pdr, inA_pdr, inB_pdr, mode_out_pdr, bridges_pdr = pdrav_details
    _, mode_out_raw = pdrav_raw_details
    _, mode_out_2lg, bridges_2lg = pdrav_2lg_details
    dec_by_s = {r["sign"]: r for r in decoder_rows}

    per_sign_rows = []
    for idx, rec in enumerate(WAVE2_SPECS):
        s, is_nov, sh_lab, wAe, wBe, _, _, exp_tier, tgt = rec
        cand_root, cand_evid, status = AUDITED_WAVE2_TABLE[s]
        b_list = bridges_pdr[idx] if bridges_pdr[idx] else bridges_2lg[idx]
        b_strs = []
        seen_b = set()
        for b in b_list:
            k = (b[0], b[1], b[4])
            if k not in seen_b:
                seen_b.add(k)
                if b[0] == "DIRECT":
                    b_strs.append(f"DIRECT DEDR {b[1]} {b[2]} ({b[3]})")
                else:
                    b_strs.append(f"{b[0]} DEDR {b[1]} {b[2]} <-> {b[4]} {b[5]}")
                if len(seen_b) >= 3:
                    break
        dr = dec_by_s[s]
        per_sign_rows.append({
            "rank": idx + 1,
            "sign": s,
            "strictly_novel": is_nov,
            "intact_total": cnt_tot[s],
            "lipi_intact": cnt_l[s],
            "new_intact": cnt_n[s],
            "shape_desc": shapes.get(s, "")[:95],
            "soundfree_gloss": sf_lex[s]["soundfree_gloss"] if s in sf_lex else "",
            "anchor_top": anchors[s][0][:85] if s in anchors else "",
            "top_locked19_neighbors": str(adj19[s].most_common(4)),
            "domainA_en": ", ".join(wAe),
            "domainB_en": ", ".join(wBe),
            "direct_2br": mode_out_pdr["direct_poly"]["real_vec"][idx],
            "phonex_2br": mode_out_pdr["phon_exact"]["real_vec"][idx],
            "phonst_2br": mode_out_pdr["phon_stem"]["real_vec"][idx],
            "ascex_2br": mode_out_pdr["ascii_exact"]["real_vec"][idx],
            "phonst_raw": mode_out_raw["phon_stem"]["real_vec"][idx],
            "phonst_2lg": mode_out_2lg["phon_stem"]["real_vec"][idx],
            "p_shuf_phonex": mode_out_pdr["phon_exact"]["per_sign_p"][idx],
            "p_shuf_phonst": mode_out_pdr["phon_stem"]["per_sign_p"][idx],
            "one_blank_lipi": dr["one_blank_lipi"],
            "one_blank_new": dr["one_blank_new"],
            "triple_lock_hit": dr["triple_lock_hit"],
            "lipi_arch_or": dr["lipi_arch_or"],
            "new_arch_or": dr["new_arch_or"],
            "top_dedr_bridges": " | ".join(b_strs),
            "candidate_root": cand_root,
            "evidence": cand_evid,
            "status": status,
        })

    with open(os.path.join(OUT_DIR, "test4b1_top30_sign_table.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(per_sign_rows[0].keys()))
        w.writeheader()
        w.writerows(per_sign_rows)

    # Exact Before vs After Wave-2 Coverage across Lipi intact (3,600) & unseen Mahadevan intact (627)
    wave2_build = {r["sign"] for r in per_sign_rows if r["status"] == "building on it"}
    wave2_build_rebus_only = {
        r["sign"] for r in per_sign_rows
        if r["status"] == "building on it" and (r["phonex_2br"] or r["phonst_2br"])
    }
    wave2_build_novel = {
        r["sign"] for r in per_sign_rows
        if r["status"] == "building on it" and r["strictly_novel"]
    }
    wave2_test = {r["sign"] for r in per_sign_rows if r["status"] == "testing it"}

    def eval_cov(rows, sign_set):
        tot_tok = 0
        hit_tok = 0
        full_faces = 0
        one_blank_faces = 0
        for r in rows:
            toks = [t for t in r["signs"].split("-") if t and t != "000"]
            if not toks:
                continue
            tot_tok += len(toks)
            h = sum(1 for t in toks if t in sign_set)
            hit_tok += h
            if h == len(toks):
                full_faces += 1
            elif h == len(toks) - 1 and len(toks) >= 2:
                one_blank_faces += 1
        return {
            "n_faces": len(rows),
            "total_tokens": tot_tok,
            "covered_tokens": hit_tok,
            "token_pct": round(100.0 * hit_tok / max(1, tot_tok), 2),
            "faces_100pct": full_faces,
            "faces_100pct_pct": round(100.0 * full_faces / max(1, len(rows)), 2),
            "faces_1blank": one_blank_faces,
            "faces_1blank_pct": round(100.0 * one_blank_faces / max(1, len(rows)), 2),
        }

    tiers = [
        ("0_core11_only", set(k3.LOCKED11_ORDER)),
        ("1_pre_wave2_19_only", LOCKED19_SET),
        ("2_pre_wave2_19_loans_bnums", LOCKED19_SET | LOAN_SET | BASIC_NUM_SET),
        ("3_pre_wave2_19_loans_allnums", LOCKED19_SET | LOAN_SET | ALL_NUM_SET),
        ("4_post_wave2_rebus_only_bnums", LOCKED19_SET | LOAN_SET | BASIC_NUM_SET | wave2_build_rebus_only),
        ("5_post_wave2_build_bnums", LOCKED19_SET | LOAN_SET | BASIC_NUM_SET | wave2_build),
        ("6_post_wave2_build_allnums", LOCKED19_SET | LOAN_SET | ALL_NUM_SET | wave2_build),
        ("7_post_wave2_build_plus_test_bnums", LOCKED19_SET | LOAN_SET | BASIC_NUM_SET | wave2_build | wave2_test),
    ]

    cov_summary = {
        "wave2_counts": dict(collections.Counter(r["status"] for r in per_sign_rows)),
        "wave2_building_on_it_signs": sorted(wave2_build),
        "wave2_building_on_it_rebus_only": sorted(wave2_build_rebus_only),
        "wave2_building_on_it_novel": sorted(wave2_build_novel),
        "wave2_testing_it_signs": sorted(wave2_test),
        "wave2_null_signs": sorted(r["sign"] for r in per_sign_rows if r["status"] == "null"),
        "lipi_intact_3600": {},
        "new_intact_627": {},
        "combined_intact_4227": {},
    }
    comb_int = lipi_int + new_int
    for tname, sset in tiers:
        cov_summary["lipi_intact_3600"][tname] = eval_cov(lipi_int, sset)
        cov_summary["new_intact_627"][tname] = eval_cov(new_int, sset)
        cov_summary["combined_intact_4227"][tname] = eval_cov(comb_int, sset)

    # Export ALL newly 100%-decoded inscriptions (had >=1 Wave-2 building-on-it sign and 0 unknown signs post-Wave-2)
    WAVE2_SHORT_GLOSS = {
        "700": "measure (*aḷa/*akal)",
        "861": "share/weight (*kāṇam)",
        "590": "bale/sack (*mūṭai)",
        "741": "single-house (*oru-kuṭi)",
        "615": "field/plot (*accu)",
        "233": "dawn-star (*veṭi-mīṉ)",
        "415": "control/seize (*kavar)",
        "920": "month (*tiṅkaḷ)",
        "407": "new-cloth (*kōṭi)",
        "806": "millet/crop (*kampu)",
        "840": "pair/joint (*iṇai)",
        "760": "young/child (*kuruku)",
        "368": "grant/banner (*koṭu/*koṭi)",
        "690": "bundle/store (*kaṭṭu)",
        "892": "sale/price (*vil)",
        "140": "lady/mother (*ammā)",
        "151": "guard/porter (*kā)",
        "503": "garland/beads (*mālai)",
    }

    def gloss_tok(t):
        if t in WAVE2_SHORT_GLOSS:
            return f"[{WAVE2_SHORT_GLOSS[t]}]"
        if t in KNOWN_INFO:
            return KNOWN_INFO[t].get("gloss", KNOWN_INFO[t]["roots"][0])
        return t

    pre_set = LOCKED19_SET | LOAN_SET | BASIC_NUM_SET
    post_set = pre_set | wave2_build
    ul_l = collections.Counter()
    ul_n = collections.Counter()
    ul_meta = {}
    for tag, sub in (("L", lipi_int), ("N", new_int)):
        for r in sub:
            toks = [t for t in r["signs"].split("-") if t and t != "000"]
            if len(toks) < 2:
                continue
            if all(t in post_set for t in toks) and not all(t in pre_set for t in toks):
                ft = "-".join(toks)
                if tag == "L":
                    ul_l[ft] += 1
                else:
                    ul_n[ft] += 1
                if ft not in ul_meta:
                    w2_used = [t for t in toks if t in wave2_build]
                    ul_meta[ft] = (len(toks), len(w2_used), ",".join(w2_used), " — ".join(gloss_tok(t) for t in toks))

    unlocked_rows = []
    for ft in sorted(ul_meta.keys(), key=lambda k: (-(ul_l[k] + ul_n[k]), -ul_n[k], -ul_meta[k][0], k)):
        n_tok, n_w2, w2_s, gloss = ul_meta[ft]
        unlocked_rows.append({
            "pattern": ft,
            "n_signs": n_tok,
            "n_wave2_signs": n_w2,
            "wave2_signs": w2_s,
            "lipi_intact_count": ul_l[ft],
            "new_intact_count": ul_n[ft],
            "total_intact_count": ul_l[ft] + ul_n[ft],
            "sign_by_sign_reading": gloss,
        })
    with open(os.path.join(OUT_DIR, "test4b2_newly_unlocked_inscriptions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(unlocked_rows[0].keys()))
        w.writeheader()
        w.writerows(unlocked_rows)
    cov_summary["newly_unlocked_patterns_total"] = len(unlocked_rows)
    cov_summary["newly_unlocked_faces_lipi"] = int(sum(ul_l.values()))
    cov_summary["newly_unlocked_faces_new"] = int(sum(ul_n.values()))

    with open(os.path.join(OUT_DIR, "wave2_coverage_before_after.json"), "w", encoding="utf-8") as f:
        json.dump(cov_summary, f, indent=2)

    log("=== COVERAGE BEFORE VS AFTER WAVE-2 ===")
    for tname, _ in tiers:
        cl = cov_summary["lipi_intact_3600"][tname]
        cn = cov_summary["new_intact_627"][tname]
        cc = cov_summary["combined_intact_4227"][tname]
        log(
            f"  {tname:35s} | Lipi: {cl['token_pct']:5.2f}% tok, {cl['faces_100pct']:4d}/3600 ({cl['faces_100pct_pct']:5.2f}%) 100% | "
            f"New: {cn['token_pct']:5.2f}% tok, {cn['faces_100pct']:3d}/627 ({cn['faces_100pct_pct']:5.2f}%) 100% | "
            f"Comb: {cc['token_pct']:5.2f}% tok"
        )
    log(f"  Newly 100%-decoded >=2-sign inscriptions: {len(unlocked_rows)} unique texts "
        f"({cov_summary['newly_unlocked_faces_lipi']} Lipi faces + {cov_summary['newly_unlocked_faces_new']} unseen New faces)")
    return per_sign_rows, cov_summary


def main():
    log(f"Starting Key #4B Wave-2 Ventris Bootstrap + 1-Blank-Slot Constrained Decoder (N_SHUF={N_SHUF})")
    ensure_lexicons()
    verify_zero_overlap(WAVE2_SPECS)

    lipi_int, new_int, ev_lipi, ev_new, shapes, anchors, sf_lex, cnt_l, cnt_n, cnt_tot = load_corpora()
    etyma_2br, _, forms_phon, _, eid_to_cid = k3.load_clean_dedr()

    fam_rows, pdrav_det, pdrav_raw_det, pdrav_2lg_det, adj19, kinds_l, kinds_n, rep_map = run_test_4b1(
        cnt_l, cnt_n, cnt_tot, shapes, anchors, sf_lex, ev_lipi, ev_new
    )
    sum_4b2, dec_rows = run_test_4b2(
        lipi_int, new_int, ev_lipi, ev_new, etyma_2br, forms_phon, eid_to_cid, pdrav_det, rep_map
    )
    per_sign_rows, cov_summary = build_epistemic_and_coverage(
        lipi_int, new_int, cnt_l, cnt_n, cnt_tot, shapes, anchors, sf_lex,
        pdrav_det, pdrav_raw_det, pdrav_2lg_det, adj19, kinds_l, kinds_n, dec_rows
    )

    master = {
        "n_shuf": N_SHUF,
        "bonferroni_7fam": round(0.05 / 7.0, 5),
        "test4b1_7family": fam_rows,
        "test4b2_summary": sum_4b2,
        "coverage_summary": cov_summary,
    }
    with open(os.path.join(OUT_DIR, "key4b_master_summary.json"), "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    log("Key #4B pipeline finished cleanly!")


if __name__ == "__main__":
    main()
