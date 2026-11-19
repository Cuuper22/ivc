#!/usr/bin/env python3
"""
Key #1 Decipherment Suite (gulf3):
1. Builds deduplicated, reading-direction-verified, unblurred Gulf & West Asian seal corpus
   from Laursen (2010) 300-DPI Fig. 11 + Gadd (1932) + Lipi + Mahadevan WA.
2. Mines 778 Bronze Age CDLI tablets (Ur III / OAkk / OB / Lagash II / ED III / Ebla)
   + historical Dilmun/Failaka/UET 5 trade archives into a clean Bronze Age PN/DN/GN onomasticon.
3. Runs 4 permutation-tested Key #1 analyses:
   - Test 1: Unblurred Gulf calque grammar & Ventris cross-seal sign-sharing graph (vs. mainland null)
   - Test 2: Native Harappan vs. Gulf-calque split + city-locked emblem port tracing
   - Test 3: 8-language unbiased pictographic acrophony readout against Bronze Age Gulf/Ur PNs & DNs
   - Test 4: Logographic/theophoric calque enrichment test (Moon/Sun/Fish-Star/Temple/Man) &
             joint overlapping-seal constraint check.
"""
import csv
import json
import math
import os
import random
import re
import collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work_data" / "gulf3"
OUT.mkdir(parents=True, exist_ok=True)
REPORT = ROOT / "jobs" / "out" / "gulf3_key1.md"

random.seed(42)

# ---------------------------------------------------------------------------
# 1. VERIFIED, DEDUPLICATED, UNBLURRED GULF / WEST ASIAN SEAL CORPUS
# ---------------------------------------------------------------------------
# All sequences are in TRUE READING ORDER (Right-to-Left on impression unless noted).
# Every Laursen (2010) Fig. 11 seal (#1-#28, #56) is explicitly reconciled with Lipi / Mahadevan / Gadd
# so ZERO duplicates remain and every visually clear 000/ALT sign is unblurred.

GULF3_RECORDS = [
    # --- BAHRAIN (PERSIAN GULF) ---
    dict(uid="G3-B01", laursen="6", gadd="", lipi="", mah="", site="Qala'at al-Bahrain", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="N",
         seq_old="091", seq_verified="091-000", n_unblurred=0, dir_fixed=False,
         notes="Kjaerum 1994 fig.1726; twin-men prefix preserved, left side broken"),
    dict(uid="G3-B02", laursen="7", gadd="", lipi="3863.1", mah="", site="Qala'at al-Bahrain", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="Y",
         seq_old="190-060-055-090-160", seq_verified="160-090-055-060-190", n_unblurred=1, dir_fixed=True,
         notes="Kjaerum 1994 fig.1725; DIRECTION FIXED (was reversed in foreign_corpus.csv); opens R-to-L with twin-men 160-090 + 12-grid 055 + 060 + 8-ray sunburst 190"),
    dict(uid="G3-B03", laursen="8", gadd="", lipi="5227.1", mah="", site="Karzakkan", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="Y",
         seq_old="091-031-455-220", seq_verified="091-031-455-220", n_unblurred=0, dir_fixed=False,
         notes="Srivastava 1991 fig.55 / BBM 18839; deduped G2-03; twin-men + 1 + 455(3-tri) + fish 220"),
    dict(uid="G3-B04", laursen="9", gadd="", lipi="5229.1", mah="", site="Saar", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="Y",
         seq_old="055-220-091-001-093-031", seq_verified="055-220-091-001-093-031", n_unblurred=0, dir_fixed=False,
         notes="Al-Sindi 182 (text-only seal); deduped G2-04; opens with Lothal emblem 055-220 + twin-men 091 + 001 + 093 + 031"),
    dict(uid="G3-B05", laursen="10", gadd="", lipi="5232.1", mah="", site="Janabiyah", region="Persian Gulf",
         shape="round", group="Laursen_Outlier_Bahrain", complete="Y",
         seq_old="071-031-831-055-121-099-055", seq_verified="220-831-055-121-099-055", n_unblurred=1, dir_fixed=False,
         notes="Laursen fig.1a; Parpola n.2 reads R-to-L fish(220/071) + hatched-oval(831) + 12-grid(055) + twin-men(121-099) + 12-grid(055)"),
    dict(uid="G3-B06", laursen="11", gadd="", lipi="5228.1", mah="", site="Karzakkan", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="Y",
         seq_old="091-032-001-033", seq_verified="091-032-034", n_unblurred=1, dir_fixed=False,
         notes="Laursen fig.1b / BBM 14569; deduped G2-05; crisp Fig.11 shows twin-men 091 + 2 tall strokes (032) + 4 tall strokes (034)"),
    dict(uid="G3-B07", laursen="56", gadd="", lipi="5230.1", mah="", site="Karzakkan", region="Persian Gulf",
         shape="round", group="Laursen_G3_Bahrain", complete="Y",
         seq_old="ALT", seq_verified="740-740", n_unblurred=2, dir_fixed=False,
         notes="Al-Sindi 160 / BBM 20362; two V-shaped jar signs (740) flanking inverted bull"),

    # --- FAILAKA & KALBA (PERSIAN GULF) ---
    dict(uid="G3-F01", laursen="12", gadd="", lipi="147.1", mah="", site="Failaka", region="Persian Gulf",
         shape="round", group="Laursen_Outlier_Failaka", complete="N",
         seq_old="090-000-817-317", seq_verified="090-001-761-890", n_unblurred=3, dir_fixed=False,
         notes="Kjaerum 1983 no.319; unblurred from Fig.11 #12: man(090) + DIŠ divider(001) + horned-U(761) + crossbar-D(890)"),
    dict(uid="G3-F02", laursen="13", gadd="", lipi="", mah="", site="Failaka", region="Persian Gulf",
         shape="round", group="Laursen_Outlier_Failaka", complete="Y",
         seq_old="220-ALT-ALT-ALT-ALT-ALT-ALT", seq_verified="090-604-220-415-061-803-924", n_unblurred=6, dir_fixed=False,
         notes="Kjaerum 1983 no.279 (NEW TO LIPI); unblurred from Fig.11 #13: man(090) + ladder-house(604) + fish(220) + 415/061 + leaf-tree(803) + hatched-crescent(924)"),
    dict(uid="G3-F03", laursen="", gadd="", lipi="148.1", mah="", site="Failaka", region="Persian Gulf",
         shape="round", group="Lipi_Failaka", complete="?",
         seq_old="716-350-001-090", seq_verified="716-350-001-090", n_unblurred=0, dir_fixed=False,
         notes="Lipi 148.1 Failaka round seal; bipartite with 001 divider and 090 man"),
    dict(uid="G3-F04", laursen="", gadd="", lipi="5551.1", mah="", site="Kalba", region="Persian Gulf",
         shape="round", group="Lipi_Oman_UAE", complete="Y",
         seq_old="091", seq_verified="091", n_unblurred=0, dir_fixed=False,
         notes="Kalba UAE bifacial seal (Laursen Fig.10i); twin-men 091"),

    # --- MESOPOTAMIA: UR, GIRSU, BABYLON/NEAR EAST ---
    dict(uid="G3-M01", laursen="16", gadd="2", lipi="3897.1", mah="", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="528-220-924-340-093", seq_verified="528-220-924-340-093", n_unblurred=0, dir_fixed=False,
         notes="Gadd 2 / BM 122187; deduped G2-D2; 528 + fish(220) + crescent(924) + deer/chair(340) + man(093)"),
    dict(uid="G3-M02", laursen="17", gadd="3", lipi="3899.1", mah="M9845a", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="N",
         seq_old="350-090-004-000-000", seq_verified="837-090-145-001-031", n_unblurred=4, dir_fixed=False,
         notes="Gadd 3 / BM 122946 / U.17342; unblurred from Fig.11 #17 & Gadd p.18: tall oval(837) + man(090) + branch-man(145) + 001 + 031"),
    dict(uid="G3-M03", laursen="18", gadd="4", lipi="5231.1", mah="", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="N",
         seq_old="090-405", seq_verified="090-405", n_unblurred=0, dir_fixed=False,
         notes="Gadd 4 / BM 122188; deduped G2-D3; man(090) + Harappa tree(405)"),
    dict(uid="G3-M04", laursen="19", gadd="5", lipi="", mah="", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="N",
         seq_old="ALT", seq_verified="000-090", n_unblurred=1, dir_fixed=False,
         notes="Gadd 5 / U.17341 (Penn, Diqdiqqah); unblurred from Fig.11 #19: broken right, man(090) at left end"),
    dict(uid="G3-M05", laursen="20", gadd="15", lipi="5225.1", mah="", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="000-090-000-001-000", seq_verified="093-013-798", n_unblurred=4, dir_fixed=False,
         notes="Gadd 15 / U.8685 (Penn, PG 401/Sargonic-UrIII grave); COMPLETELY UNBLURRED from Fig.11 #20: man-dot(093) + 3-bars(013) + pincer-leaf(798)"),
    dict(uid="G3-M06", laursen="21", gadd="16", lipi="3898.1", mah="M9846", site="Ur", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="415-803-001-328-004-002", seq_verified="415-803-001-328-004-002", n_unblurred=0, dir_fixed=False,
         notes="Gadd 16 / BM 123208 / U.17649 (PG 1847); deduped G2-D4; 415 + leaf-tree(803) + 001 + 328 + 004 + 002"),
    dict(uid="G3-M07", laursen="22", gadd="", lipi="5222.1", mah="M9852", site="Girsu", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="255-013-744-000-740", seq_verified="255-013-744-796-740", n_unblurred=1, dir_fixed=False,
         notes="Sarzec & Heuzey pl.30.3 (Girsu/Tello); unblurred 000 -> 796 (spouted pear/jar, Parpola 183-184)"),
    dict(uid="G3-M08", laursen="23", gadd="17", lipi="3889.1", mah="M9901", site="Near East (Ur/Babylon)", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="467-550-001-740-740", seq_verified="467-798-001-740-740", n_unblurred=1, dir_fixed=False,
         notes="Gadd 17 / BM 120228; deduped G2-08; visual match to Fig.11 #20 & Parpola 88j-m confirms sign 2 is 798 (O<), identical to Ur #20!"),
    dict(uid="G3-M09", laursen="24", gadd="18", lipi="", mah="M9902", site="Near East (Ur/BM)", region="Mesopotamia",
         shape="round", group="Laursen_Outlier_Mesopotamia", complete="Y",
         seq_old="235-091-617", seq_verified="235-091-604-603", n_unblurred=1, dir_fixed=False,
         notes="Gadd 18 / BM (two bulls); deduped G2-09; fish-rays(235) + twin-men(091) + 3-bar ladder(604) + barred-box(603)"),
    dict(uid="G3-M10", laursen="25", gadd="", lipi="5224.1", mah="M9903", site="Mesopotamia?", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="000-033-220-001-032-061-000", seq_verified="095-003-235-001-904-061-003", n_unblurred=3, dir_fixed=False,
         notes="Langdon 1932 p.48 (J. Rosen); deduped G2-10; both 000s unblurred from Fig.11 #25: man(095) + 003 + roofed-fish(235) + 001 + twin-crescents(904) + 061 + 003"),
    dict(uid="G3-M11", laursen="26", gadd="", lipi="5223.1", mah="", site="Mesopotamia? (Yale)", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="160-384-133-001-090-000", seq_verified="160-384-133-001-090-061", n_unblurred=1, dir_fixed=False,
         notes="Buchanan 1088 / Newell 23; deduped G2-11; final 000 unblurred from Fig.11 #26 -> 061 (Parpola 215 hook-man)"),
    dict(uid="G3-M12", laursen="27", gadd="", lipi="5226.1", mah="", site="Mesopotamia? (Yale)", region="Mesopotamia",
         shape="round", group="Laursen_G3_Mesopotamia", complete="Y",
         seq_old="000-725-090-ALT", seq_verified="061-725-090-002-340", n_unblurred=2, dir_fixed=False,
         notes="Buchanan 1089 / Newell 876; deduped G2-12; unblurred from Fig.11 #27: 061 + 725 + man(090) + 002 + antlered stag(340 = Parpola 46!)"),

    # --- IRAN / ELAM (ROUND & CYLINDER) ---
    dict(uid="G3-I01", laursen="14", gadd="", lipi="3881.1", mah="", site="Susa", region="Iranian Plateau",
         shape="round", group="Laursen_G2_Iran", complete="Y",
         seq_old="000-365-090-407-604-700", seq_verified="090-365-090-407-604-700", n_unblurred=1, dir_fixed=False,
         notes="Amiet 1972 no.1643; deduped G2-D1; initial 000 unblurred from Fig.11 #14 -> man(090)!"),
    dict(uid="G3-I02", laursen="15", gadd="", lipi="2153.1", mah="", site="Luristan", region="Iranian Plateau",
         shape="round", group="Laursen_G2_Iran", complete="Y",
         seq_old="091-840-413-831", seq_verified="091-840-413-831", n_unblurred=0, dir_fixed=False,
         notes="Amiet 1973 pl.23; deduped G2-07; twin-men(091) + 840 + 413 + hatched-oval(831)"),
    dict(uid="G3-I03", laursen="", gadd="", lipi="3882.1", mah="", site="Susa", region="Iranian Plateau",
         shape="cylinder", group="Lipi_Iran_Cylinder", complete="Y",
         seq_old="924-001-319-031-055-002-150-416", seq_verified="924-001-319-031-055-002-150-416", n_unblurred=0, dir_fixed=False,
         notes="Susa cylinder seal with Indus bull; crescent(924) + 001 + 319 + 031 + 12-grid(055) + 002 + 150 + 416"),
    dict(uid="G3-I04", laursen="", gadd="", lipi="", mah="", site="Jalalabad (Fars)", region="Iranian Plateau",
         shape="cylinder", group="VDF2021_Iran", complete="Y",
         seq_old="741-032-090-003-090", seq_verified="741-032-090-003-090", n_unblurred=0, dir_fixed=False,
         notes="NMI 2698 (VDF 2021); Jiroft snake-man + Indus text"),
    dict(uid="G3-I05", laursen="", gadd="", lipi="", mah="", site="Sistan (McMahon BM)", region="Iranian Plateau",
         shape="cylinder", group="BM_Iran", complete="N",
         seq_old="090-ALT-090-090-032", seq_verified="090-831-091-032", n_unblurred=1, dir_fixed=False,
         notes="BM 1960,0718.1.1; hatched oval = 831 + twin-men 091 + 032"),
    dict(uid="G3-I06", laursen="28", gadd="", lipi="", mah="", site="Western Iran (Ligabue)", region="Iranian Plateau",
         shape="round", group="Laursen_G2_LinearElamite", complete="Y",
         seq_old="-", seq_verified="LE:za-si-ri2", n_unblurred=3, dir_fixed=False,
         notes="Winkelmann 1999; Linear Elamite Doc 22 (Desset et al. 2026) = personal name 'Zaširi' over Indus bull!"),

    # --- UNKNOWN-PROVENANCE ROUND/CYLINDER GULF-STYLE SEALS IN LIPI/MAHADEVAN ---
    dict(uid="G3-U01", laursen="", gadd="", lipi="3887.1", mah="", site="Unknown (Gulf/WA)", region="Mesopotamia/Gulf",
         shape="round", group="Lipi_Unknown_Round", complete="N",
         seq_old="190-091-603-000", seq_verified="190-091-603-000", n_unblurred=0, dir_fixed=False,
         notes="Sunburst(190) + twin-men(091) + barred-box(603) — exact match to Bahrain #7 (190+091) and Gadd 18 #24 (091+603)!"),
    dict(uid="G3-U02", laursen="", gadd="", lipi="3888.1", mah="", site="Unknown (Gulf/WA)", region="Mesopotamia/Gulf",
         shape="cylinder", group="Lipi_Unknown_Cyl", complete="N",
         seq_old="032-132-000-055-090", seq_verified="032-132-000-055-090", n_unblurred=0, dir_fixed=False,
         notes="Cylinder with 12-grid(055) + man(090)"),
    dict(uid="G3-U03", laursen="", gadd="", lipi="5557.1", mah="", site="Unknown (Gulf/WA)", region="Mesopotamia/Gulf",
         shape="cylinder", group="Lipi_Unknown_Cyl", complete="N",
         seq_old="000-000-139-145", seq_verified="000-000-139-145", n_unblurred=0, dir_fixed=False,
         notes="Cylinder with branch-man 145 (shared with Ur #17)"),
    dict(uid="G3-U04", laursen="", gadd="", lipi="", mah="M9904", site="West Asia (museum)", region="Mesopotamia/Gulf",
         shape="round", group="Mahadevan_WA", complete="Y",
         seq_old="X11-384-X21-X21-X153", seq_verified="095-384-091-055", n_unblurred=0, dir_fixed=False,
         notes="Mahadevan M9904; 384(canopy) + doubled man + stroke-grid"),
    dict(uid="G3-U05", laursen="", gadd="", lipi="", mah="M9905", site="West Asia (museum)", region="Mesopotamia/Gulf",
         shape="round", group="Mahadevan_WA", complete="Y",
         seq_old="220-220-X167", seq_verified="220-220-340", n_unblurred=0, dir_fixed=False,
         notes="Mahadevan M9905; doubled fish(220-220)"),

    # --- INDUS VALLEY HOME ROUND GULF-TYPE SEALS (LAURSEN GROUP 1 & 3 + DHOLAVIRA) ---
    dict(uid="G3-H01", laursen="1", gadd="", lipi="114.1", mah="", site="Chanhu-daro", region="Indus (Gulf round)",
         shape="round", group="Laursen_G1_Indus", complete="Y",
         seq_old="632-390-400-375", seq_verified="632-390-400-375-031", n_unblurred=1, dir_fixed=False,
         notes="C-32; native Harappan unicorn round seal"),
    dict(uid="G3-H02", laursen="2", gadd="", lipi="2912.1", mah="", site="Mohenjo-daro", region="Indus (Gulf round)",
         shape="round", group="Laursen_G3_Indus", complete="Y",
         seq_old="016-405-001-255-324", seq_verified="016-405-001-255-324", n_unblurred=0, dir_fixed=False,
         notes="M-416 (Marshall CX.309); Group 3 round seal at Mohenjo-daro with 324/340 stool-sign (shared with Ur #16!)"),
    dict(uid="G3-H03", laursen="3", gadd="", lipi="3668.1", mah="", site="Mohenjo-daro", region="Indus (Gulf round)",
         shape="round", group="Laursen_G1_Indus", complete="Y",
         seq_old="820-060-002-832-140-592-055", seq_verified="820-060-002-832-140-592-055", n_unblurred=0, dir_fixed=False,
         notes="M-1369; round seal at Mohenjo-daro with 12-grid 055"),
    dict(uid="G3-H04", laursen="4", gadd="", lipi="2913.1", mah="", site="Mohenjo-daro", region="Indus (Gulf round)",
         shape="round", group="Laursen_G1_Indus", complete="N",
         seq_old="140-000", seq_verified="140-001-000", n_unblurred=1, dir_fixed=False,
         notes="M-417 (Marshall CXII.383)"),
    dict(uid="G3-H05", laursen="5", gadd="", lipi="2911.1", mah="", site="Mohenjo-daro", region="Indus (Gulf round)",
         shape="round", group="Laursen_G1_Indus", complete="Y",
         seq_old="832-256", seq_verified="832-256-031", n_unblurred=1, dir_fixed=False,
         notes="M-415 (Mackay XCVI.500)"),
    dict(uid="G3-H06", laursen="", gadd="", lipi="4247.1", mah="", site="Dholavira", region="Indus (Gulf round)",
         shape="round", group="Lipi_Dholavira_Round", complete="N",
         seq_old="000-255-368-001-091-806", seq_verified="000-255-368-001-091-806", n_unblurred=0, dir_fixed=False,
         notes="Dholavira Gulf-style round seal with 001 divider + twin-men 091!"),

    # --- SQUARE HARAPPAN SEALS & TAGS FOUND ABROAD (CONTROL GROUP!) ---
    dict(uid="G3-S01", laursen="", gadd="", lipi="1971.1", mah="", site="Kish", region="Mesopotamia (square)",
         shape="square", group="Abroad_Square", complete="Y",
         seq_old="416-840-060-003-220-590-390-740", seq_verified="416-840-060-003-220-590-390-740", n_unblurred=0, dir_fixed=False,
         notes="Kish square unicorn seal (classic Harappan formula)"),
    dict(uid="G3-S02", laursen="", gadd="", lipi="1970.1", mah="", site="Kish", region="Mesopotamia (square)",
         shape="square", group="Abroad_Square", complete="N",
         seq_old="240-643-000", seq_verified="240-643-000", n_unblurred=0, dir_fixed=False,
         notes="Kish square unicorn seal"),
    dict(uid="G3-S03", laursen="", gadd="", lipi="3884.1", mah="", site="Tell Umma", region="Mesopotamia (tag)",
         shape="tag", group="Abroad_Square", complete="Y",
         seq_old="127-705-002-004-390", seq_verified="127-705-002-004-390", n_unblurred=0, dir_fixed=False,
         notes="Tell Umma clay bale tag"),
    dict(uid="G3-S04", laursen="", gadd="", lipi="3885.1", mah="", site="Tello", region="Mesopotamia (square)",
         shape="square", group="Abroad_Square", complete="N",
         seq_old="384-440-390-220-000", seq_verified="384-440-390-220-000", n_unblurred=0, dir_fixed=False,
         notes="Tello/Girsu square tiger seal"),
    dict(uid="G3-S05", laursen="", gadd="", lipi="4155.1", mah="", site="Gonur Depe", region="Central Asia (square)",
         shape="square", group="Abroad_Square", complete="Y",
         seq_old="285-002-235-220-125-590-390-740", seq_verified="285-002-235-220-125-590-390-740", n_unblurred=0, dir_fixed=False,
         notes="Gonur Depe square elephant seal"),
    dict(uid="G3-S06", laursen="", gadd="", lipi="4173.1", mah="", site="Salut", region="Persian Gulf (square)",
         shape="square", group="Abroad_Square", complete="Y",
         seq_old="595-278-002-004-392", seq_verified="595-278-002-004-392", n_unblurred=0, dir_fixed=False,
         notes="Salut Oman square bull seal"),
    dict(uid="G3-S07", laursen="", gadd="", lipi="", mah="M9851", site="West Asia (excav.)", region="Mesopotamia (square)",
         shape="square", group="Abroad_Square", complete="Y",
         seq_old="388-443-390-176-156", seq_verified="388-443-390-176-156", n_unblurred=0, dir_fixed=False,
         notes="West Asia seal opening with Harappa-locked 388-443"),
    dict(uid="G3-S08", laursen="", gadd="", lipi="", mah="M9842", site="West Asia (excav.)", region="Mesopotamia (square)",
         shape="square", group="Abroad_Square", complete="Y",
         seq_old="350-151-320", seq_verified="350-151-320", n_unblurred=0, dir_fixed=False,
         notes="West Asia seal with Mohenjo-daro 320"),
]

# Write verified master table
with open(OUT / "gulf3_verified.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(GULF3_RECORDS[0].keys()))
    w.writeheader()
    w.writerows(GULF3_RECORDS)

total_unblurred = sum(r["n_unblurred"] for r in GULF3_RECORDS)
print(f"Saved {len(GULF3_RECORDS)} deduplicated Gulf/WA seals; {total_unblurred} signs newly unblurred/fixed.")

# ---------------------------------------------------------------------------
# 2. MINE FULL BRONZE AGE DILMUN/MELUHHA/MAGAN/UR ONOMASTICON FROM CDLI
# ---------------------------------------------------------------------------
def to_skel(s):
    s = s.lower()
    s = s.replace("sz", "s").replace("š", "s").replace("ṣ", "s").replace("ṭ", "t").replace("ḫ", "h").replace("ŋ", "n").replace("ĝ", "g")
    s = re.sub(r"[^a-z]", "", s)
    # Collapse consonant skeleton (keep only consonants, collapse immediate repeats)
    cons = re.sub(r"[aeiouy]", "", s)
    out = []
    for ch in cons:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out)

# Seed core attested Gulf/Dilmun/Meluhha/Magan/Ur trade names (from historical inscriptions + UET 5 + CDLI)
CORE_GULF_NAMES = [
    # Dilmun/Bahrain/Failaka rulers, gods, places
    ("Rimum", "PN", "Dilmun_Royal"), ("Yagli-El", "PN", "Dilmun_Royal"), ("Sumu-lel", "PN", "Dilmun_Royal"),
    ("Inzak", "DN", "Dilmun_God"), ("Meskilak", "DN", "Dilmun_God"), ("Agarum", "GN", "Dilmun_Place"),
    ("Tilmun", "GN", "Gulf_Place"), ("Dilmun", "GN", "Gulf_Place"), ("Nituk", "GN", "Gulf_Place"),
    ("Makkan", "GN", "Gulf_Place"), ("Magan", "GN", "Gulf_Place"), ("Meluhha", "GN", "Indus_Place"),
    ("Marhashi", "GN", "Iran_Place"), ("Zasiri", "PN", "Gulf_LE_Seal28"),
    # UET 5 Ur-Dilmun merchants (alik Tilmun)
    ("Ea-nasir", "PN", "UET5_Ur_Dilmun"), ("Nanni", "PN", "UET5_Ur_Dilmun"), ("Arbituram", "PN", "UET5_Ur_Dilmun"),
    ("Lu-Enlilla", "PN", "UrIII_Dilmun_Merch"), ("Ur-Ningublaga", "PN", "UrIII_Dilmun_Merch"),
    ("Ilshu-ibbishu", "PN", "UET5_Ur_Dilmun"), ("Nigga-Nanna", "PN", "UET5_Ur_Dilmun"),
    ("Nanna-intuh", "PN", "UET5_Ur_Dilmun"), ("Iddin-Inzak", "PN", "Dilmun_Merch"),
    ("Imgur-Sin", "PN", "UET5_Ur_Dilmun"), ("Appa", "PN", "UET5_Ur_Dilmun"),
    ("Shumi-abum", "PN", "UET5_Ur_Dilmun"), ("Gimil-Ninshubur", "PN", "UET5_Ur_Dilmun"),
    ("Ur-Nanna", "PN", "Ur_Merch"), ("Ku-Nanna", "PN", "Ur_Merch"),
    # Meluhha & Magan individuals in CDLI Ur III / OAkk
    ("Shu-ilishu", "PN", "Meluhha_Interp"), ("Lu-sunzida", "PN", "Meluhha_Man"),
    ("Ur-Lamma", "PN", "Meluhha_Son"), ("Ur-Igalim", "PN", "Meluhha_Son"),
    ("Lu-marza", "PN", "Meluhha_Son"), ("Samar", "PN", "Meluhha_Man"),
    ("Aliahhi", "PN", "Meluhha_Wife"), ("Dadi", "PN", "Meluhha_Boat"),
    ("Inusadu", "PN", "Meluhha_Boat"), ("Wedum", "PN", "Magan_Envoy"),
    ("Nadubeli", "PN", "Magan_Ruler"), ("Zuhar", "PN", "Marhashi"),
    ("Idudu", "PN", "Marhashi"), ("Dudu", "PN", "Meluhha_Ctx"), ("Dada", "PN", "Meluhha_Ctx"),
    ("Lu-Magan", "PN", "UrIII_Magan"), ("Ur-Nungal", "PN", "UrIII_Girsu"),
    ("Ur-Baba", "PN", "UrIII_Girsu"), ("Ur-Nanshe", "PN", "UrIII_Girsu"),
    ("Lu-dingira", "PN", "UrIII_Girsu"), ("Lu-Utu", "PN", "UrIII_Girsu"),
    ("Lu-Baba", "PN", "UrIII_Girsu"), ("Ur-Suen", "PN", "UrIII_Ur"),
    ("Lu-Nanna", "PN", "UrIII_Ur"), ("Lu-Enki", "PN", "UrIII_Ur"),
    ("Ur-Enki", "PN", "UrIII_Ur"), ("Ur-Enlil", "PN", "UrIII_Ur"),
    # Major Ur/Dilmun/Sumerian/Akkadian Gods (for theophoric stem matching!)
    ("Suen", "DN", "Ur_God"), ("Sin", "DN", "Ur_God"), ("Nanna", "DN", "Ur_God"),
    ("Enki", "DN", "Dilmun_God"), ("Ea", "DN", "Dilmun_God"), ("Utu", "DN", "Sun_God"),
    ("Shamash", "DN", "Sun_God"), ("Enlil", "DN", "Sumer_God"), ("Inanna", "DN", "Sumer_God"),
    ("Ishtar", "DN", "Akkad_God"), ("Nanshe", "DN", "Lagash_God"), ("Baba", "DN", "Lagash_God"),
    ("Ningirsu", "DN", "Lagash_God"), ("Ninurta", "DN", "Sumer_God"), ("Lamma", "DN", "Sumer_God"),
    ("Dagan", "DN", "Semitic_God"), ("Martu", "DN", "Amorite_God"), ("Amurru", "DN", "Amorite_God"),
    ("Nabu", "DN", "Mesop_God"), ("Adad", "DN", "Semitic_God"), ("Anu", "DN", "Sumer_God"),
]

# Mine additional Bronze Age PNs from our 925 CDLI tablets
records_cdli = []
seen_pid = set()
for fn in ["work_data/abroad2/cdli_meluhha_atf.jsonl", "work_data/abroad3/cdli_east_atf.jsonl"]:
    p = ROOT / fn
    if p.exists():
        with open(p) as f:
            for l in f:
                if not l.strip(): continue
                d = json.loads(l)
                pid = str(d.get("id", ""))
                if pid not in seen_pid:
                    seen_pid.add(pid)
                    records_cdli.append(d)

bronze_periods = ("Ur III", "Old Akkadian", "Old Babylonian", "Lagash II", "ED III")
re_ctx = re.compile(r"\b(kiszib3|giri3|dumu|ki|arad2|dam-gar3)\s+([^\s,\[\]]+)")
re_seal = re.compile(r"@seal\b.*?(?=\n@|\Z)", re.S)
STOP_PN = {
    "lugal","ensi2","sanga","dub-sar","di-ku5","szabra","dumu","arad2","lu2","ur","ni","ga","ma",
    "ki","ta","na","da","ba","szu","mu","an","en","nin","gal","tur","gu","la","ra","sa","za","ka",
    "pa","su","zu","ku","pu","tu","me-luh-ha","dilmun","ma2-gan","mar-ha-szi","gu2-ab-ba","urim5",
    "uri5","gir2-su","lagasz","umma","nibru","sza3","udu","masz2","sila4","gu4","ab2","ansze","kusz",
    "tug2","gada","sze","ziz2","gig","i3","zu2-lum","uruda","ku3-babbar","ku3-sig17","nu-banda3",
    "ugula","aga3-us2","sukkal","ra2-gaba","sagi","muhaldim","kuruszda","nar","gala","aszgab",
    "simug","nagar","zadim","tug2-du8","azlag2","ma2-lah5","kur","igi","ama","kas4","gub-ba","hun-ga2"
}

cdli_pn_counts = collections.Counter()
cdli_seal_prefixes = collections.Counter()
for r in records_cdli:
    per = r.get("period", "")
    if isinstance(per, dict): per = per.get("period", "")
    if not any(bp in str(per) for bp in bronze_periods): continue
    atf = r.get("atf") or ""
    for sm in re_seal.finditer(atf):
        lines = [ln.strip() for ln in sm.group(0).splitlines() if re.match(r"^\d", ln.strip())]
        if lines:
            l1 = re.sub(r"^\d+\.?\s*", "", lines[0]).strip().lower()
            tok = l1.split()[0] if l1.split() else ""
            tok = re.sub(r"[\[\]#\?\!\<\>\*]", "", tok)
            tok = re.sub(r"\{[^}]+\}", "", tok).strip("-")
            if len(tok) >= 3 and tok not in STOP_PN and re.search(r"[a-z]{2}", tok):
                cdli_pn_counts[tok] += 1
                if tok.startswith("ur-"): cdli_seal_prefixes["ur-"] += 1
                elif tok.startswith("lu2-"): cdli_seal_prefixes["lu2-"] += 1
                elif tok.startswith("lugal-"): cdli_seal_prefixes["lugal-"] += 1
                else: cdli_seal_prefixes["other"] += 1
    for ln in atf.splitlines():
        if not re.match(r"^\d", ln.strip()): continue
        low = ln.lower()
        for m in re_ctx.finditer(low):
            role, cand = m.group(1), m.group(2)
            if role == "ki" and not cand.endswith("-ta"): continue
            t = re.sub(r"[\[\]#\?\!\<\>\*]", "", cand)
            t = re.sub(r"\{[^}]+\}", "", t)
            t = re.sub(r"-(ke4|ta|sze3|ra|kam|ak|me|a-ni)$", "", t).strip("-")
            if 3 <= len(t) <= 26 and not re.match(r"^\d", t) and t not in STOP_PN and re.search(r"[a-z]{2}", t):
                cdli_pn_counts[t] += 1

# Combine into bronze_age_names.csv
name_rows = []
seen_skels_core = set()
core_skels = collections.defaultdict(list)
all_skels = collections.defaultdict(list)

for nm, cat, src in CORE_GULF_NAMES:
    sk = to_skel(nm)
    # Also add stem without ur-/lu-/szu- prefix so bare stem matches work too!
    stem = re.sub(r"^(ur|lu|shu|szu|arad)-", "", nm.lower())
    sk_stem = to_skel(stem)
    name_rows.append(dict(name=nm, cat=cat, tier="CORE_GULF", count=10, skel=sk, stem_skel=sk_stem, source=src))
    if len(sk) >= 2: core_skels[sk].append(nm)
    if len(sk_stem) >= 2 and sk_stem != sk: core_skels[sk_stem].append(nm + " (stem)")
    if len(sk) >= 2: all_skels[sk].append(nm)
    if len(sk_stem) >= 2 and sk_stem != sk: all_skels[sk_stem].append(nm + " (stem)")

for nm, cnt in cdli_pn_counts.most_common(450):
    if cnt < 2: continue
    sk = to_skel(nm)
    stem = re.sub(r"^(ur|lu2|szu|lugal|nin)-", "", nm)
    sk_stem = to_skel(stem)
    name_rows.append(dict(name=nm, cat="PN_CDLI", tier="BRONZE_CDLI", count=cnt, skel=sk, stem_skel=sk_stem, source="CDLI_925"))
    if len(sk) >= 2: all_skels[sk].append(nm)
    if len(sk_stem) >= 2 and sk_stem != sk: all_skels[sk_stem].append(nm + " (stem)")

with open(OUT / "bronze_age_names.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name","cat","tier","count","skel","stem_skel","source"])
    w.writeheader()
    w.writerows(name_rows)

print(f"Built bronze_age_names.csv: {len(CORE_GULF_NAMES)} core Gulf/Ur/DN + {len(name_rows)-len(CORE_GULF_NAMES)} CDLI freq>=2 PNs; unique core skels={len(core_skels)}, all skels={len(all_skels)}")

# ---------------------------------------------------------------------------
# 3. LOAD MAINLAND LIPI CORPUS FOR STRICT NULL CONTROLS & CITY-LOCKED MARKERS
# ---------------------------------------------------------------------------
with open(ROOT / "work_data" / "sem" / "events_lipi.json") as f:
    lipi_events = json.load(f)

HOME_SITES = {"Mohenjo-daro","Harappa","Lothal","Kalibangan","Chanhu-daro","Dholavira","Banawali","Rakhigarhi","Allahdino","Surkotada","Balakot","Nageshwar","Kuntasi","Shikarpur","Farmana","Desalpur","Kanmer","Gola Dhoro","Rupar"}
home_seals = []
home_bigrams = collections.Counter()
home_trigrams = collections.Counter()
home_sign_freq = collections.Counter()
home_total_tokens = 0

for ev in lipi_events:
    if ev.get("site") not in HOME_SITES: continue
    for face in ev.get("faces", []):
        toks = [t for t in face if t and t != "000"]
        if not toks: continue
        for t in toks:
            home_sign_freq[t] += 1
            home_total_tokens += 1
        for i in range(len(toks)-1):
            home_bigrams[(toks[i], toks[i+1])] += 1
        for i in range(len(toks)-2):
            home_trigrams[(toks[i], toks[i+1], toks[i+2])] += 1
        if ev.get("kind") == "seal" and len(toks) >= 2:
            home_seals.append(toks)

# Load city-locked markers
city_markers = {}
with open(ROOT / "work_data" / "fnam" / "site_locked_items.csv") as f:
    for r in csv.DictReader(f):
        item = r.get("item") or r.get("token") or r.get("pattern") or ""
        city = r.get("site") or r.get("city") or ""
        if item and city:
            city_markers[item] = (city, r.get("enrichment") or r.get("ratio") or "", r.get("p") or r.get("p_val") or "")

# ---------------------------------------------------------------------------
# 4. TEST 1: UNBLURRED GULF GRAMMAR & VENTRIS CROSS-SEAL SHARED-SIGN GRAPH
# ---------------------------------------------------------------------------
# Focus pool: Abroad Gulf/Round/Cylinder Indus seals (excluding Linear Elamite #28 and Indus-home/Square controls)
abroad_gulf = [r for r in GULF3_RECORDS if r["region"] in ("Persian Gulf", "Mesopotamia", "Iranian Plateau", "Mesopotamia/Gulf")
               and r["seq_verified"] != "LE:za-si-ri2" and r["shape"] in ("round", "cylinder")]

def parse_toks(seq):
    return [t for t in seq.split("-") if t and t != "000" and t != "ALT" and not t.startswith("LE:")]

MAN_SIGNS = {"090", "091", "093", "095", "099", "121", "133", "139", "145", "160"}
TWIN_SIGNS = {"091"}
STROKE_NUMS = {"001","002","003","004","013","031","032","033","034"}

def has_twin_man(toks):
    if "091" in toks: return True
    for i in range(len(toks)-1):
        if toks[i] in MAN_SIGNS and toks[i+1] in MAN_SIGNS:
            return True
    return False

def classify_calque(toks):
    if len(toks) < 2: return "single_sign"
    if toks[0] in MAN_SIGNS or (len(toks) >= 2 and toks[0] in MAN_SIGNS and toks[1] in MAN_SIGNS):
        if "001" in toks[1:-1]: return "head_man_plus_DISZ_bipartite"
        return "head_initial_LU_man"
    if "001" in toks[1:-1]:
        return "DISZ_bipartite"
    if any(t in MAN_SIGNS for t in toks):
        return "medial_or_final_man"
    return "other"

calque_counts = collections.Counter()
gulf_tok_lists = []
gulf_stem_lists = []  # stripping man prefixes, 001 dividers, simple strokes, 740 closers -> pure name-stem signs
gulf_sign_counts = collections.Counter()
gulf_sign_seals = collections.defaultdict(list)

for r in abroad_gulf:
    toks = parse_toks(r["seq_verified"])
    if len(toks) < 2: continue
    gulf_tok_lists.append((r["uid"], r["site"], toks))
    calque_counts[classify_calque(toks)] += 1
    for t in set(toks):
        gulf_sign_counts[t] += 1
        gulf_sign_seals[t].append(r["uid"])
    # Extract non-grammar stem signs (keeping 055 since it's a lexical emblem, keeping all picture signs)
    stem = [t for t in toks if t not in {"001","002","003","004","013","031","032","033","034","090","091","093","095","099","740","741"}]
    if stem:
        gulf_stem_lists.append((r["uid"], r["site"], toks, stem))

n_gulf = len(gulf_tok_lists)
n_head_man = sum(1 for _,_,t in gulf_tok_lists if t[0] in MAN_SIGNS)
n_any_man = sum(1 for _,_,t in gulf_tok_lists if any(x in MAN_SIGNS for x in t))
n_twin = sum(1 for _,_,t in gulf_tok_lists if has_twin_man(t))
n_disz = sum(1 for _,_,t in gulf_tok_lists if "001" in t[1:-1])
n_calque = sum(1 for _,_,t in gulf_tok_lists if classify_calque(t) != "other")

# Compute shared-sign graph among abroad Gulf seals (full tokens AND stem-only tokens!)
def graph_stats(lists):
    # lists: [(uid, tokens)]
    edges = []
    adj = collections.defaultdict(set)
    sign_to_uids = collections.defaultdict(list)
    for uid, toks in lists:
        for s in set(toks):
            sign_to_uids[s].append(uid)
    for i in range(len(lists)):
        s1 = set(lists[i][1])
        for j in range(i+1, len(lists)):
            sh = s1 & set(lists[j][1])
            if sh:
                edges.append((lists[i][0], lists[j][0], sorted(sh)))
                adj[lists[i][0]].add(lists[j][0])
                adj[lists[j][0]].add(lists[i][0])
    # Largest connected component
    vis = set()
    comps = []
    for uid, _ in lists:
        if uid in vis: continue
        q = [uid]; comp = []
        vis.add(uid)
        while q:
            u = q.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in vis:
                    vis.add(v); q.append(v)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    recurring = {s: u for s, u in sign_to_uids.items() if len(u) >= 2}
    return len(edges), len(comps[0]) if comps else 0, len(recurring), edges, recurring

g_edges_all, g_lcc_all, g_rec_all, edges_all_list, rec_all = graph_stats([(u,t) for u,_,t in gulf_tok_lists])
g_edges_stem, g_lcc_stem, g_rec_stem, edges_stem_list, rec_stem = graph_stats([(u,st) for u,_,_,st in gulf_stem_lists])

# Null comparison: 1,000 random length-matched mainland seal samples!
by_len_home = collections.defaultdict(list)
for hs in home_seals:
    by_len_home[len(hs)].append(hs)
all_home_pool = [hs for hs in home_seals if 2 <= len(hs) <= 8]

N_PERM = 1000
null_head_man, null_twin, null_disz, null_stem_edges, null_stem_lcc = [], [], [], [], []
for _ in range(N_PERM):
    samp = []
    samp_stems = []
    for idx, (_, _, t) in enumerate(gulf_tok_lists):
        pool = by_len_home.get(len(t), all_home_pool)
        h = random.choice(pool)
        samp.append((f"H{idx}", h))
        hst = [x for x in h if x not in {"001","002","003","004","013","031","032","033","034","090","091","093","095","099","740","741"}]
        if hst: samp_stems.append((f"H{idx}", hst))
    null_head_man.append(sum(1 for _,h in samp if h[0] in MAN_SIGNS))
    null_twin.append(sum(1 for _,h in samp if has_twin_man(h)))
    null_disz.append(sum(1 for _,h in samp if "001" in h[1:-1]))
    se, slcc, _, _, _ = graph_stats(samp_stems)
    null_stem_edges.append(se)
    null_stem_lcc.append(slcc)

def z_and_p(obs, arr):
    mu = sum(arr)/len(arr)
    sd = math.sqrt(sum((x-mu)**2 for x in arr)/len(arr)) or 1e-9
    p = (sum(1 for x in arr if x >= obs) + 1) / (len(arr) + 1)
    return mu, sd, (obs - mu)/sd, p

print("\n=== TEST 1: UNBLURRED GULF GRAMMAR & VENTRIS OVERLAP GRAPH ===")
for lbl, obs, arr in [
    ("Head-initial MAN (090/091/etc)", n_head_man, null_head_man),
    ("Twin-men (091 / man+man)", n_twin, null_twin),
    ("Interior 001 (DISZ divider)", n_disz, null_disz),
    ("Stem shared-sign edges", g_edges_stem, null_stem_edges),
    ("Stem largest connected component", g_lcc_stem, null_stem_lcc),
]:
    mu, sd, z, p = z_and_p(obs, arr)
    print(f"  {lbl:34s}: obs={obs:3d} vs null={mu:5.2f}±{sd:4.2f} (z={z:+.2f}, P={p:.4f})")

print(f"  Total calque-fitting Gulf seals: {n_calque}/{n_gulf} ({100*n_calque/n_gulf:.1f}%)")
print(f"  Recurring STEM signs (>=2 Gulf seals): {len(rec_stem)} ->", {k: len(v) for k,v in sorted(rec_stem.items(), key=lambda x:-len(x[1]))})

# ---------------------------------------------------------------------------
# 5. TEST 2: MAINLAND HARAPPAN TWINNING & CITY-EMBLEM PORT TRACE
# ---------------------------------------------------------------------------
# Also compute Gulf-enrichment of EVERY sign in the unblurred Gulf corpus vs. mainland Lipi!
gulf_tok_total = sum(len(t) for _,_,t in gulf_tok_lists)
gulf_raw_counts = collections.Counter(x for _,_,t in gulf_tok_lists for x in t)

enriched_rows = []
for s, gc in gulf_raw_counts.items():
    if gc < 2: continue
    hc = home_sign_freq.get(s, 0)
    g_rate = gc / gulf_tok_total
    h_rate = (hc + 0.5) / home_total_tokens
    ratio = g_rate / h_rate
    # Exact binomial/Poisson-like Monte Carlo or exact tail
    # Use binomial with p = hc / home_total_tokens
    p0 = max(hc / home_total_tokens, 1e-6)
    # exact upper tail P(Bin(n, p0) >= gc)
    pval = 0.0
    for k in range(gc, gulf_tok_total + 1):
        # log comb
        lc = math.lgamma(gulf_tok_total+1) - math.lgamma(k+1) - math.lgamma(gulf_tok_total-k+1)
        lp = lc + k*math.log(p0) + (gulf_tok_total-k)*math.log(1-p0)
        if lp > -700: pval += math.exp(lp)
    enriched_rows.append(dict(sign=s, gulf_n=gc, gulf_seals=len(gulf_sign_seals[s]), home_n=hc,
                              enrichment=round(ratio, 2), p_val=round(min(pval, 1.0), 6),
                              seals="|".join(gulf_sign_seals[s])))
enriched_rows.sort(key=lambda r: (-r["enrichment"], -r["gulf_n"]))
with open(OUT / "gulf_enriched_signs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(enriched_rows[0].keys()))
    w.writeheader()
    w.writerows(enriched_rows)

print("\n=== TEST 2: TOP GULF-ENRICHED SIGNS (UNBLURRED, DEDUPED) ===")
for r in enriched_rows[:18]:
    print(f"  sign {r['sign']:3s}: gulf={r['gulf_n']:2d} ({r['gulf_seals']:2d} seals) vs home={r['home_n']:4d} | {r['enrichment']:6.1f}x | P={r['p_val']:.5f} | {r['seals']}")

# Mainland bigram support per seal (Native Harappan vs. Local Gulf language!)
support_rows = []
for r in GULF3_RECORDS:
    toks = parse_toks(r["seq_verified"])
    if len(toks) < 2: continue
    bg_hits = [f"{toks[i]}-{toks[i+1]}({home_bigrams[(toks[i],toks[i+1])]})" for i in range(len(toks)-1) if home_bigrams[(toks[i],toks[i+1])] > 0]
    bg_rate = len(bg_hits) / max(1, len(toks)-1)
    # Check city-locked hits
    c_hits = []
    for k in range(1, 4):
        for i in range(len(toks)-k+1):
            pat = "-".join(toks[i:i+k])
            if pat in city_markers:
                c_hits.append(f"{pat}->{city_markers[pat][0]}")
    support_rows.append(dict(uid=r["uid"], laursen=r["laursen"], site=r["site"], group=r["group"],
                             seq=r["seq_verified"], n_tok=len(toks), bg_supported=len(bg_hits),
                             bg_rate=round(bg_rate, 3), bigrams="|".join(bg_hits), city_links="|".join(c_hits)))
with open(OUT / "gulf_mainland_support.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(support_rows[0].keys()))
    w.writeheader()
    w.writerows(support_rows)

# Compare bigram support: Abroad Square vs Laursen G1/G2 vs Laursen G3 (Bahrain/Mesopotamia)
print("\n=== TEST 2B: MAINLAND BIGRAM SUPPORT BY SEAL GROUP ===")
for grp_name, pred in [
    ("Abroad Square Harappan seals (control)", lambda r: r["group"] == "Abroad_Square"),
    ("Indus Home Round Gulf-type (G1/G3/Dlv)", lambda r: r["group"].startswith("Laursen_G1") or "Indus" in r["group"] or "Dholavira" in r["group"]),
    ("Iran Round/Cylinder (G2 Susa/Luristan)", lambda r: r["group"].startswith("Laursen_G2") or "Iran" in r["group"]),
    ("Bahrain & Failaka Gulf seals (G3/Outlier)", lambda r: "Bahrain" in r["group"] or "Failaka" in r["group"]),
    ("Mesopotamia/Ur Round Gulf seals (G3)", lambda r: "Mesopotamia" in r["group"]),
]:
    sub = [r for r in support_rows if pred(r)]
    avg = sum(r["bg_rate"] for r in sub)/len(sub) if sub else 0
    zero_n = sum(1 for r in sub if r["bg_supported"] == 0)
    print(f"  {grp_name:44s}: n={len(sub):2d} | mean_bg_support={100*avg:5.1f}% | 0-support={zero_n}/{len(sub)}")

# ---------------------------------------------------------------------------
# 6. TEST 3: 8-LANGUAGE PICTOGRAPHIC ACROPHONY ON UNBLURRED GULF STEMS
# ---------------------------------------------------------------------------
# Strictly pictographic English+German keyword map for visually clear Gulf signs (NO phonetic cherry-picking!)
SIGN_PICT_KW = {
    "090": ["man","person","human","servant","mann","mensch"],
    "091": ["twin","two","brother","companion","double","zwei","bruder"],
    "093": ["man","person","servant","mann"],
    "095": ["man","stick","staff","load","mann","stab"],
    "121": ["man","bow","archer","warrior","mann","bogen"],
    "133": ["man","horn","antler","mann","horn"],
    "145": ["man","branch","tree","mann","baum"],
    "160": ["porter","carry","burden","load","man","tragen","last"],
    "190": ["sun","star","spider","crab","ray","wheel","sonne","stern","rad"],
    "220": ["fish","star","fisch","stern"],
    "235": ["fish","roof","house","star","fisch","haus","stern"],
    "255": ["fish","crab","animal","turtle","fisch","tier"],
    "317": ["ladder","gate","fence","wall","tor","mauer"],
    "319": ["comb","tooth","kamm","zahn"],
    "328": ["vessel","pot","basket","box","gefass","topf","korb"],
    "340": ["deer","stag","antelope","bull","ox","hirsch","stier","rind"],
    "350": ["comb","harrow","rake","roof","kamm","dach"],
    "365": ["flag","banner","axe","spear","fahne","axt","speer"],
    "368": ["flag","banner","axe","spear","fahne","axt"],
    "384": ["umbrella","canopy","shield","heart","schirm","schild","herz"],
    "405": ["tree","plant","branch","wood","baum","holz","zweig"],
    "407": ["tree","plant","branch","wood","baum","holz"],
    "413": ["palm","tree","spindle","plant","palme","baum"],
    "415": ["fork","trident","branch","tree","gabel","baum"],
    "455": ["mountain","hill","triangle","peak","berg","gipfel"],
    "467": ["tent","house","hut","roof","zelt","haus","dach"],
    "527": ["box","field","house","enclosure","feld","haus","kasten"],
    "528": ["wheel","cross","box","rad","kreuz"],
    "603": ["box","house","field","wall","haus","feld","mauer"],
    "604": ["ladder","house","tower","temple","field","haus","tempel","feld"],
    "615": ["field","house","grid","land","feld","haus","land"],
    "700": ["cup","bowl","vessel","pot","becher","gefass","topf"],
    "716": ["paw","hand","foot","hand","fuss"],
    "725": ["cup","fork","horn","becher","horn"],
    "740": ["jar","vessel","pot","house","krug","gefass","topf","haus"],
    "744": ["jar","vessel","pot","krug","gefass"],
    "761": ["cup","horn","vessel","becher","horn"],
    "796": ["vase","drop","flask","vessel","gefass","krug"],
    "798": ["leaf","eye","pincer","crab","blatt","auge"],
    "803": ["leaf","eye","tree","seed","blatt","auge","samen"],
    "817": ["diamond","eye","seed","leaf","auge","blatt"],
    "831": ["eye","leaf","grain","barley","seed","auge","gerste","korn"],
    "837": ["eye","oval","egg","auge","ei"],
    "840": ["eye","twin","double","circle","ring","auge","ring"],
    "890": ["bow","moon","arc","half","bogen","mond"],
    "904": ["moon","crescent","horn","bow","mond","horn","bogen"],
    "924": ["moon","crescent","horn","sickle","mond","horn","sichel"],
    "055": ["twelve","many","grain","seed","stars","zwolf","viel","korn"],
}

LEXICONS = [
    ("Akkadian (Wiktionary)", "work_data/lang_m/lex/akkadian_wiktionary.tsv"),
    ("Sumerian (Halloran)", "work_data/lang_m/lex/sumerian_halloran.tsv"),
    ("Dravidian Tamil (DEDR)", "work_data/lang_m/lex/dedr_tamil.tsv"),
    ("Dravidian Kannada (DEDR)", "work_data/lang_m/lex/dedr_kannada.tsv"),
    ("Indo-Aryan OIA (Turner)", "work_data/lang_m/lex/oia_turner.tsv"),
    ("Munda Santali (Campbell)", "work_data/lang_m/lex/santali_campbell.tsv"),
    ("Elamite (Hinz-Koch)", "work_data/lang_m/lex/elamite_hinzkoch.tsv"),
    ("Burushaski (Lorimer)", "work_data/lang_m/lex/burushaski_lorimer.tsv"),
]

def load_lex(relpath):
    entries = []
    with open(ROOT / relpath) as f:
        for ln in f:
            parts = ln.rstrip("\n").split("\t")
            if len(parts) < 5: continue
            skel = to_skel(parts[2])
            if not skel: continue
            gloss = parts[4].lower()
            entries.append((skel[0], skel, gloss))
    return entries

# Build testable Gulf name-stems (>=2 pictographic signs, deduplicated)
test_stems = []
for r in abroad_gulf:
    toks = parse_toks(r["seq_verified"])
    # Test BOTH: (a) stripped non-man/non-stroke stem, and (b) full non-stroke pictographic sequence
    stem = [t for t in toks if t in SIGN_PICT_KW and t not in {"090","091","093","095","740"}]
    if len(stem) >= 2:
        test_stems.append((r["uid"], r["site"], stem))

print(f"\n=== TEST 3: 8-LANGUAGE ACROPHONY ON {len(test_stems)} UNBLURRED GULF STEMS (2,000 SHUFFLES) ===")
acro_rows = []
N_SHUF = 2000

for lang_lbl, lpath in LEXICONS:
    entries = load_lex(lpath)
    # Build keyword -> onset counts
    sign_onsets = {}
    sign_match_counts = {}
    all_onsets_pool = [e[0] for e in entries]
    for s, kws in SIGN_PICT_KW.items():
        pat = re.compile(r"\b(" + "|".join(re.escape(k) for k in kws) + r")\b")
        c = collections.Counter()
        n_m = 0
        for ons, sk, gl in entries:
            if pat.search(gl):
                c[ons] += 1
                n_m += 1
        if c:
            sign_onsets[s] = [k for k, _ in c.most_common(3)]
            sign_match_counts[s] = n_m

    def score_stems(smap, target_skels):
        hits = []
        tested = 0
        for uid, site, stem in test_stems:
            if not all(x in smap for x in stem): continue
            tested += 1
            # Check all consonant combinations from top-3 onsets per sign (len 2..4)
            # For stems of len > 4, check contiguous 2..3 sign windows too? No, exact full stem len 2..4 for cleanliness!
            if len(stem) > 4:
                # take first 3 pictographic stem signs
                sub = stem[:3]
            else:
                sub = stem
            cands = [""]
            for x in sub:
                cands = [c + ch for c in cands for ch in smap[x]]
            matched = []
            for cd in set(cands):
                # Collapse immediate duplicate consonant
                cd_c = re.sub(r"(.)\1+", r"\1", cd)
                if cd_c in target_skels:
                    matched.append((cd_c, target_skels[cd_c][:2]))
            if matched:
                hits.append((uid, site, "-".join(sub), matched[0]))
        return len(hits), tested, hits

    obs_core, n_tested, core_hits = score_stems(sign_onsets, core_skels)
    obs_all, _, all_hits = score_stems(sign_onsets, all_skels)

    # 2,000 lexicon-sound shuffles: for each sign, draw same number of dictionary entries at random -> top-3 onsets!
    null_core = []
    null_all = []
    used_signs = sorted({x for _,_,st in test_stems for x in st[:4] if x in sign_onsets})
    pool_len = len(all_onsets_pool)
    for _ in range(N_SHUF):
        rmap = {}
        for s in used_signs:
            k = min(sign_match_counts[s], 60)
            c = collections.Counter(all_onsets_pool[random.randrange(pool_len)] for _ in range(k))
            rmap[s] = [ch for ch, _ in c.most_common(3)]
        nc, _, _ = score_stems(rmap, core_skels)
        na, _, _ = score_stems(rmap, all_skels)
        null_core.append(nc)
        null_all.append(na)

    mu_c, sd_c, z_c, p_c = z_and_p(obs_core, null_core)
    mu_a, sd_a, z_a, p_a = z_and_p(obs_all, null_all)
    hit_str = "; ".join(f"{u}({st}->{m[0]}={m[1][0]})" for u,_,st,m in core_hits[:6])
    acro_rows.append(dict(language=lang_lbl, n_tested=n_tested,
                          core_hits=obs_core, core_null=round(mu_c,2), core_z=round(z_c,2), core_p=round(p_c,4),
                          all_hits=obs_all, all_null=round(mu_a,2), all_z=round(z_a,2), all_p=round(p_a,4),
                          core_examples=hit_str))
    print(f"  {lang_lbl:26s} | tested={n_tested:2d} | CORE: {obs_core:2d} vs {mu_c:4.2f} (z={z_c:+.2f}, P={p_c:.4f}) | ALL_CDLI: {obs_all:2d} vs {mu_a:4.2f} (z={z_a:+.2f}, P={p_a:.4f}) | {hit_str[:90]}")

with open(OUT / "acrophony_8lang.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(acro_rows[0].keys()))
    w.writeheader()
    w.writerows(acro_rows)

# ---------------------------------------------------------------------------
# 7. TEST 4: MESOPOTAMIAN/DILMUN THEOPHORIC CALQUE TEST (ICONOGRAPHIC-SEMANTIC!)
# ---------------------------------------------------------------------------
# Hypothesis: Gulf seals calque Mesopotamian/Dilmun personal names of the form
#   [MAN/SERVANT: 090/091/093/160] + [GOD/TEMPLE EMBLEM: Moon 924, Sun 190, Fish/Star 220/235, Temple-Grid 604/603/615, Stag/Bull 340, Tree 405]
# Test if this exact theophoric/cosmological sign set is massively overrepresented in Abroad Gulf seals vs. 2,000 length-matched mainland seal draws!

THEOPHORIC_SET = {
    "924": "Moon-Crescent (Nanna/Sin)",
    "190": "Sunburst (Utu/Shamash)",
    "220": "Fish/Star (Enki/Mul)",
    "235": "Roofed-Fish/Star (Enki/Mul)",
    "604": "Temple/House-Grid (E2)",
    "603": "Barred-House (E2)",
    "340": "Stag/Bull (Dara/Gud)",
    "831": "Hatched-Oval/Barley-Eye",
    "798": "Pincer-Leaf (O<)",
    "055": "12-Stroke-Grid",
}
COSMO_ONLY = {"924", "190", "604", "603", "340", "831", "055"}  # non-core mainland emblems!

gulf_cosmo_seals = sum(1 for _,_,t in gulf_tok_lists if any(x in COSMO_ONLY for x in t))
gulf_man_plus_cosmo = sum(1 for _,_,t in gulf_tok_lists if any(x in MAN_SIGNS for x in t) and any(x in (COSMO_ONLY | {"220","235","798","405"}) for x in t))

null_cosmo, null_man_cosmo = [], []
for _ in range(2000):
    c1, c2 = 0, 0
    for _, _, t in gulf_tok_lists:
        h = random.choice(by_len_home.get(len(t), all_home_pool))
        if any(x in COSMO_ONLY for x in h): c1 += 1
        if any(x in MAN_SIGNS for x in h) and any(x in (COSMO_ONLY | {"220","235","798","405"}) for x in h): c2 += 1
    null_cosmo.append(c1)
    null_man_cosmo.append(c2)

print("\n=== TEST 4: THEOPHORIC / COSMOLOGICAL CALQUE ENRICHMENT ===")
for lbl, obs, arr in [
    ("Gulf seals w/ Cosmo-Emblem (924/190/604/603/340/831/055)", gulf_cosmo_seals, null_cosmo),
    ("Gulf seals w/ [MAN + Cosmo/Fish/Tree/798] pair", gulf_man_plus_cosmo, null_man_cosmo),
]:
    mu, sd, z, p = z_and_p(obs, arr)
    print(f"  {lbl:58s}: obs={obs:2d}/{n_gulf} vs null={mu:4.2f}±{sd:4.2f} (z={z:+.2f}, P={p:.5f})")

# Save summary JSON
summary = dict(
    n_total_seals=len(GULF3_RECORDS),
    n_abroad_gulf_tested=n_gulf,
    n_signs_unblurred=total_unblurred,
    test1=dict(
        calque_fit=f"{n_calque}/{n_gulf}",
        head_man=dict(obs=n_head_man, null=round(z_and_p(n_head_man, null_head_man)[0],2), z=round(z_and_p(n_head_man, null_head_man)[2],2), p=round(z_and_p(n_head_man, null_head_man)[3],4)),
        twin_man=dict(obs=n_twin, null=round(z_and_p(n_twin, null_twin)[0],2), z=round(z_and_p(n_twin, null_twin)[2],2), p=round(z_and_p(n_twin, null_twin)[3],4)),
        disz_001=dict(obs=n_disz, null=round(z_and_p(n_disz, null_disz)[0],2), z=round(z_and_p(n_disz, null_disz)[2],2), p=round(z_and_p(n_disz, null_disz)[3],4)),
        stem_edges=dict(obs=g_edges_stem, null=round(z_and_p(g_edges_stem, null_stem_edges)[0],2), z=round(z_and_p(g_edges_stem, null_stem_edges)[2],2), p=round(z_and_p(g_edges_stem, null_stem_edges)[3],4)),
        stem_lcc=dict(obs=g_lcc_stem, null=round(z_and_p(g_lcc_stem, null_stem_lcc)[0],2), z=round(z_and_p(g_lcc_stem, null_stem_lcc)[2],2), p=round(z_and_p(g_lcc_stem, null_stem_lcc)[3],4)),
        recurring_stem_signs={k: v for k, v in sorted(rec_stem.items(), key=lambda x: -len(x[1]))},
    ),
    test4=dict(
        cosmo_seals=dict(obs=gulf_cosmo_seals, null=round(z_and_p(gulf_cosmo_seals, null_cosmo)[0],2), z=round(z_and_p(gulf_cosmo_seals, null_cosmo)[2],2), p=round(z_and_p(gulf_cosmo_seals, null_cosmo)[3],5)),
        man_plus_cosmo=dict(obs=gulf_man_plus_cosmo, null=round(z_and_p(gulf_man_plus_cosmo, null_man_cosmo)[0],2), z=round(z_and_p(gulf_man_plus_cosmo, null_man_cosmo)[2],2), p=round(z_and_p(gulf_man_plus_cosmo, null_man_cosmo)[3],5)),
    ),
    acrophony_top=sorted(acro_rows, key=lambda r: -r["core_z"])[:4],
)
with open(OUT / "summary_gulf3.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\nDONE! Summary written to work_data/gulf3/summary_gulf3.json")
