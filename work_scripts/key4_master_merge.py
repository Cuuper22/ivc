#!/usr/bin/env python3
"""
Key #4 Stage-2 Master Merge:
Deduplicated, strictly tiered global inventory & coverage audit combining:
  - Baseline (Key #2A 11 + Key #3A 8 = 19 locked Dravidian signs + 3 trade loans + basic numerals)
  - Lever 1 (Key #4A): Diacritic operators, DEDR ligatures, and distributional allographs
  - Lever 2 (Key #4B): Wave-2 Top-30 Ventris bootstrap (+18 building on it, +8 testing it)
  - Lever 3 (Key #4C): Sangam & Tamil-Brahmi epigraphic compound validation
  - Lever 4 (Key #4D): Verified pure & workshop allograph inheritance across ALL locked signs
"""
import csv
import json
import os
from collections import Counter

ROOT = "/home/antigravity/Cuuper22/ivc"
OUT_DIR = os.path.join(ROOT, "work_data", "key4_master")
os.makedirs(OUT_DIR, exist_ok=True)


def z3(s: str) -> str:
    s = str(s).strip()
    return s.zfill(3) if s.isdigit() else s


def main():
    # 1. Baseline locked signs (strictly matching Key #3A / #4A / #4D)
    base_19 = {
        "220": ("*mīṉ", "Key2A", "fish/star"),
        "820": ("*kāl", "Key2A", "wheel/quarter"),
        "320": ("*paṭi", "Key2A", "step/ration"),
        "090": ("*āḷ", "Key2A", "man/manager"),
        "154": ("*kā", "Key2A", "pole/guard"),
        "740": ("*kuṭi/*kuṭam", "Key2A", "pot/house"),
        "400": ("*cikka/*cikkam", "Key2A", "comb/junior"),
        "705": ("*kalam/*kaḷam", "Key2A", "threshing/ship"),
        "520": ("*vēḷ/*vēl", "Key2A", "spear/chief"),
        "850": ("*kaṇ/*kaṉ", "Key2A", "eye/copper"),
        "390": ("*tai", "Key2A", "tree/weave"),
        "717": ("*aṭi", "Key3A", "footprint/servant"),
        "061": ("*kāl", "Key3A", "leg/quarter"),
        "235": ("*oḷi-mīṉ", "Key3A", "roofed-fish/bright-star"),
        "500": ("*pāy", "Key3A", "sail/sea-trip"),
        "100": ("*talai", "Key3A", "head/chief"),
        "176": ("*iṟai/*iru", "Key3A", "seated/tribute-house"),
        "900": ("*tiṅkaḷ", "Key3A", "crescent/month"),
        "923": ("*maruppu", "Key3A", "tusk/ivory"),
    }
    base_loans = {
        "854": ("*eḷ", "Key2A_Loan", "sesame (Akk. ellu)"),
        "790": ("*vaḷai", "Key2A_Loan", "bangle (Skt. valaya)"),
        "215": ("*arici", "Key2A_Loan", "rice (Gk. oryza)"),
    }
    base_nums = {
        "001": ("*oru", "Num", "1 (short)"),
        "002": ("*iru", "Num", "2 (short)"),
        "003": ("*mū", "Num", "3 (short)"),
        "004": ("*nāl", "Num", "4 (short)"),
        "015": ("*ai", "Num", "5 (short)"),
        "031": ("*oru", "Num", "1 (tall)"),
        "032": ("*iru", "Num", "2 (tall)"),
        "033": ("*mū", "Num", "3 (tall)"),
        "034": ("*nāl", "Num", "4 (tall)"),
        "035": ("*ai", "Num", "5 (tall)"),
        "055": ("*paṉṉiru", "Num", "12 (dozen)"),
    }
    all_nums_extra = {
        "006": ("*aṟu", "Num_Ext", "6 (short)"),
        "016": ("*aṟu", "Num_Ext", "6 (tall/tier)"),
        "007": ("*ēḻ", "Num_Ext", "7 (short)"),
        "017": ("*ēḻ", "Num_Ext", "7 (tier)"),
        "008": ("*eṇ", "Num_Ext", "8"),
        "027": ("*oṉpatu", "Num_Ext", "9 (photo)"),
        "028": ("*pattu", "Num_Ext", "10 (photo)"),
        "056": ("*24", "Num_Ext", "24 (photo 12+12)"),
        "711": ("*vaḷḷam", "Meas_Ext", "4-cup measure (37 L)"),
        "575": ("*kōṭṭai", "Meas_Ext", "72-cup measure (665 L)"),
    }

    # 2. Load Key #4A (Ligatures / Operators / Allographs)
    k4a_build = {}
    k4a_test = {}
    with open(os.path.join(ROOT, "work_data", "key4a", "key4a_coverage_breakdown.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = z3(r["sign"])
            tier = r["tier"].strip()
            subcat = r["subcat"].strip()
            gloss = r["reading_gloss"].strip()
            if tier.startswith("building_on_it"):
                k4a_build[s] = (gloss, f"Key4A_{subcat}", gloss)
            elif tier == "testing_it":
                k4a_test[s] = (gloss, f"Key4A_Test_{subcat}", gloss)

    # 3. Load Key #4B (Wave-2 Top-30 Bootstrap)
    k4b_build = {}
    k4b_test = {}
    with open(os.path.join(ROOT, "work_data", "key4b", "test4b1_top30_sign_table.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = z3(r["sign"])
            st = r["status"].strip()
            root = r["candidate_root"].strip()
            ev = r["evidence"].strip()
            if st == "building on it":
                k4b_build[s] = (root, "Key4B_Wave2", ev)
            elif st == "testing it":
                k4b_test[s] = (root, "Key4B_Test", ev)

    # 4. Load Key #4D (Verified Pure & Workshop Allograph Clusters)
    clusters_pure = []
    with open(os.path.join(ROOT, "work_data", "key4d", "verified_clusters_pure.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            mems = [z3(x) for x in r["members"].split("|") if x.strip()]
            clusters_pure.append((z3(r["canonical"]), mems))

    clusters_all = []
    with open(os.path.join(ROOT, "work_data", "key4d", "verified_clusters_all.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            mems = [z3(x) for x in r["members"].split("|") if x.strip()]
            clusters_all.append((z3(r["canonical"]), mems))

    # Build strictly layered cumulative sign sets
    # Tier 0: Baseline (19 + 3 loans + 11 basic nums)
    tier0 = {}
    for d in (base_19, base_loans, base_nums):
        tier0.update(d)

    # Tier 1: + Key #4B (Wave-2 strictly building on it)
    tier1 = dict(tier0)
    for s, info in k4b_build.items():
        if s not in tier1:
            tier1[s] = info

    # Tier 2: + Key #4A (Ligatures, Operators, Allographs strictly building on it)
    tier2 = dict(tier1)
    for s, info in k4a_build.items():
        if s not in tier2:
            tier2[s] = info

    # Tier 3: + Key #4D Pure Allograph Inheritance (any member of a verified PURE cluster where another member is in tier2!)
    tier3_pure = dict(tier2)
    inherited_pure = {}
    for canon, mems in clusters_pure:
        locked_parents = [m for m in mems if m in tier2]
        if locked_parents:
            parent = locked_parents[0]
            proot = tier2[parent][0]
            for m in mems:
                if m not in tier3_pure:
                    info = (proot, f"Key4D_PureAllo({parent})", f"Verified Pure allograph of {parent} ({proot})")
                    tier3_pure[m] = info
                    inherited_pure[m] = info

    # Tier 4: + Key #4D Workshop/Regional Allograph Inheritance (full verified Pure+Workshop clusters!)
    tier4_all = dict(tier3_pure)
    inherited_workshop = {}
    for canon, mems in clusters_all:
        locked_parents = [m for m in mems if m in tier3_pure]
        if locked_parents:
            parent = locked_parents[0]
            proot = tier3_pure[parent][0]
            for m in mems:
                if m not in tier4_all:
                    info = (proot, f"Key4D_WorkshopAllo({parent})", f"Verified Workshop allograph of {parent} ({proot})")
                    tier4_all[m] = info
                    inherited_workshop[m] = info

    # Tier 5: + Verified Extended Numerals & Measures (6, 7, 8, 9, 10, 24, 711, 575)
    tier5_nums = dict(tier4_all)
    for s, info in all_nums_extra.items():
        if s not in tier5_nums:
            tier5_nums[s] = info
    # And propagate pure/workshop allographs of extended nums/measures (e.g. 006/016, 007/017)
    for canon, mems in clusters_all:
        locked_parents = [m for m in mems if m in tier5_nums]
        if locked_parents:
            parent = locked_parents[0]
            proot = tier5_nums[parent][0]
            for m in mems:
                if m not in tier5_nums:
                    tier5_nums[m] = (proot, f"Key4D_AlloNum({parent})", f"Allograph of {parent}")

    # Tier 6: + Key #4A & #4B `testing it` (exploratory frontier)
    tier6_test = dict(tier5_nums)
    for d in (k4b_test, k4a_test):
        for s, info in d.items():
            if s not in tier6_test:
                tier6_test[s] = info

    # 5. Evaluate exact coverage across all corpus splits
    corpus_path = os.path.join(ROOT, "work_data", "reader_v3", "corpus_soundfree_readings.csv")
    with open(corpus_path, encoding="utf-8") as f:
        r3_rows = list(csv.DictReader(f))

    splits = {
        "lipi_intact_3600": [r for r in r3_rows if r["catalogue"] == "Lipi" and r["intact"] == "True"],
        "new_intact_627": [r for r in r3_rows if r["catalogue"] != "Lipi" and r["partnered"] == "False" and r["intact"] == "True"],
        "combined_intact_4227": [r for r in r3_rows if (r["catalogue"] == "Lipi" or r["partnered"] == "False") and r["intact"] == "True"],
        "combined_all_6862": [r for r in r3_rows if (r["catalogue"] == "Lipi" or r["partnered"] == "False")],
    }

    tiers = [
        ("T0_Baseline_K3A", tier0),
        ("T1_Plus_4B_Wave2", tier1),
        ("T2_Plus_4A_Ligatures", tier2),
        ("T3_Plus_4D_PureAllo", tier3_pure),
        ("T4_Master_BuildingOnIt", tier4_all),
        ("T5_Master_Plus_ExtNumsMeas", tier5_nums),
        ("T6_Frontier_Plus_TestingIt", tier6_test),
    ]

    results = {}
    for sname, subset in splits.items():
        results[sname] = {}
        for tname, tdict in tiers:
            tset = set(tdict.keys())
            tot_t = 0
            hit_t = 0
            f100 = 0
            f100_len3 = 0
            f50 = 0
            f75 = 0
            n_faces = 0
            for r in subset:
                toks = [z3(x) for x in r["signs"].split("-") if x.strip() and x.strip().isdigit()]
                if not toks:
                    continue
                n_faces += 1
                tot_t += len(toks)
                h = sum(1 for tk in toks if tk in tset)
                hit_t += h
                if h == len(toks):
                    f100 += 1
                    if len(toks) >= 3:
                        f100_len3 += 1
                if h >= 0.75 * len(toks):
                    f75 += 1
                if h >= 0.50 * len(toks):
                    f50 += 1
            results[sname][tname] = {
                "n_signs_in_tier": len(tset),
                "n_faces": n_faces,
                "total_tokens": tot_t,
                "covered_tokens": hit_t,
                "token_pct": round(100.0 * hit_t / tot_t, 2),
                "faces_100pct": f100,
                "faces_100pct_pct": round(100.0 * f100 / n_faces, 2),
                "faces_100pct_len3plus": f100_len3,
                "faces_75pct": f75,
                "faces_75pct_pct": round(100.0 * f75 / n_faces, 2),
                "faces_50pct": f50,
                "faces_50pct_pct": round(100.0 * f50 / n_faces, 2),
            }

    # Check top remaining UNSOLVED signs after T5_Master_Plus_ExtNumsMeas
    rem_cnt = Counter()
    all_cnt = Counter()
    for r in splits["combined_intact_4227"]:
        for x in r["signs"].split("-"):
            x = x.strip()
            if x.isdigit():
                s = z3(x)
                all_cnt[s] += 1
                if s not in tier5_nums:
                    rem_cnt[s] += 1

    # Save master lexicon CSV
    lex_rows = []
    for s, (root, src, note) in sorted(tier5_nums.items(), key=lambda kv: -all_cnt[kv[0]]):
        lex_rows.append({
            "sign": s,
            "root_or_gloss": root,
            "source_lever": src,
            "evidence_note": note,
            "intact_4227_tokens": all_cnt[s],
        })
    with open(os.path.join(OUT_DIR, "master_locked_lexicon.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sign", "root_or_gloss", "source_lever", "evidence_note", "intact_4227_tokens"])
        w.writeheader()
        w.writerows(lex_rows)

    summary = {
        "results": results,
        "cross_lever_synergy_inherited_pure": {k: v[1] for k, v in inherited_pure.items()},
        "cross_lever_synergy_inherited_workshop": {k: v[1] for k, v in inherited_workshop.items()},
        "top_15_remaining_after_T5": rem_cnt.most_common(15),
    }
    with open(os.path.join(OUT_DIR, "master_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("=== KEY #4 STAGE-2 MASTER MERGE (4,227 INTACT FACES) ===")
    for tname, _ in tiers:
        c = results["combined_intact_4227"][tname]
        l = results["lipi_intact_3600"][tname]
        n = results["new_intact_627"][tname]
        print(f"{tname:28s} | signs={c['n_signs_in_tier']:3d} | Comb={c['token_pct']:5.2f}% (100%={c['faces_100pct']:4d}/{c['faces_100pct_pct']:5.2f}%, len3+={c['faces_100pct_len3plus']:3d}, >=50%={c['faces_50pct_pct']:5.2f}%) | Lipi={l['token_pct']:5.2f}% | Unseen={n['token_pct']:5.2f}%")

    print("\nCross-lever 4D allographs inheriting NEW 4A/4B sounds:")
    for k, v in sorted(list(inherited_pure.items()) + list(inherited_workshop.items()), key=lambda kv: -all_cnt[kv[0]]):
        print(f"  {k} ({all_cnt[k]} tok) <- {v[1]}: {v[0]}")
    print("\nTop 15 remaining unsolved signs after T5:")
    for k, v in rem_cnt.most_common(15):
        print(f"  {k}: {v} tok")


if __name__ == "__main__":
    main()
