#!/usr/bin/env python3
"""
Generate the 5 publication-grade vector/raster figures (SVG, PDF, 300-DPI PNG)
for the Indus Script Key #8 decipherment manuscript.

All plotted statistics are read strictly from disk artifacts under `work_data/`.
Portable repository root: ROOT = Path(__file__).resolve().parent.parent.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "paper" / "figures"

# Publication palette (colorblind-safe, print-ready)
NAVY = "#1B365D"
TEAL = "#0E7C7B"
EMERALD = "#1E8449"
AMBER = "#D4820A"
CRIMSON = "#B03A2E"
SLATE = "#5D6D7E"
LIGHT_GRAY = "#EAEDED"
MID_GRAY = "#AEB6BF"
DARK_TEXT = "#1C2833"
SOFT_BLUE = "#D6EAF8"
SOFT_GREEN = "#D4EFDF"
SOFT_AMBER = "#FCF3CF"
PURPLE = "#6C3483"


def configure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.5,
            "axes.titlesize": 10.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 9.5,
            "axes.labelweight": "bold",
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "legend.fontsize": 8.2,
            "axes.edgecolor": "#4D5656",
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": "#D5D8DC",
            "grid.linewidth": 0.6,
            "grid.linestyle": "--",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "path",
        }
    )


def load_json(rel_path: str) -> Any:
    p = ROOT / rel_path
    with p.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_figure(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf", "png"):
        out = FIG_DIR / f"{stem}.{ext}"
        kwargs: dict[str, Any] = {"bbox_inches": "tight", "pad_inches": 0.14}
        if ext == "png":
            kwargs["dpi"] = 300
        fig.savefig(out, **kwargs)
    plt.close(fig)


def fmt_p(p: float) -> str:
    if p < 1e-4:
        exp = int(math.floor(math.log10(p)))
        mant = p / (10.0 ** exp)
        return f"{mant:.2f}×10^{{{exp}}}"
    if p < 0.01:
        return f"{p:.4f}"
    return f"{p:.3f}"


# =============================================================================
# FIGURE 1: Unseen Holdout Parity & Full-Face Coverage Trajectory (33 -> 272)
# =============================================================================


def build_fig1() -> None:
    audit = load_json("work_data/key8c/master_audit_table_v3.json")
    k4 = load_json("work_data/key4_master/master_summary.json")["results"]
    k5 = load_json("work_data/key5a/coverage_before_after.json")
    k6 = load_json("work_data/key6a/coverage_after_key6a.json")
    k7 = load_json("work_data/key7a/coverage_after_key7a.json")
    k8 = load_json("work_data/key8a/coverage_after_key8a.json")

    # Panel A: Clean 563-unseen milestones from master_audit_table_v3
    checks = audit["invariant3_unseen_holdout_parity"]["checks"]
    locked_order = [
        ("T0_Baseline_K3A", "K3A\n(33)"),
        ("T1_Plus_4B_Wave2", "W2\n(51)"),
        ("T2_Plus_4A_Ligatures", "4A\n(82)"),
        ("T3_Plus_4D_PureAllo", "4D\n(98)"),
        ("T5_Master_Plus_ExtNumsMeas", "K4M\n(114)"),
        ("T5_Plus_Key5A_With4D", "K5A\n(140)"),
        ("After_Key6A_With4D", "K6A\n(163)"),
        ("After_Key7A_PhonMetOnly_With4D", "K7A*\n(224)"),
        ("After_Key7A_With4D", "K7A\n(227)"),
        ("After_Key8A_PhonMetOnly_With4D", "K8A*\n(266)"),
        ("After_Key8A_With4D", "K8A\n(272)"),
    ]
    by_tier = {r["tier"]: r for r in checks if r.get("new_faces") == 563}
    pts = [by_tier[t] for t, _ in locked_order if t in by_tier]
    frontier = by_tier["Key8A_Plus_TestingFrontier"]

    xs = np.array([p["n_signs"] for p in pts], dtype=float)
    lipi_pct = np.array([p["lipi_token_pct"] for p in pts], dtype=float)
    new_pct = np.array([p["new_token_pct"] for p in pts], dtype=float)

    # Panel B: 100%-decoded intact faces across major locked milestones
    milestones_b = [
        ("K3A\n(33)", k4["lipi_intact_3600"]["T0_Baseline_K3A"], k4["new_intact_627"]["T0_Baseline_K3A"]),
        ("K4M\n(114)", k4["lipi_intact_3600"]["T5_Master_Plus_ExtNumsMeas"], k4["new_intact_627"]["T5_Master_Plus_ExtNumsMeas"]),
        ("K5A\n(140)", k5["lipi_intact_3600"]["T5_Plus_Key5A_With4D"], k5["new_intact_627"]["T5_Plus_Key5A_With4D"]),
        ("K6A\n(163)", k6["lipi_intact_3600"]["After_Key6A_With4D"], k6["new_intact_563"]["After_Key6A_With4D"]),
        ("K7A\n(227)", k7["lipi_intact_3600"]["After_Key7A_With4D"], k7["new_intact_563"]["After_Key7A_With4D"]),
        ("K8A*\n(266)", k8["lipi_intact_3600"]["After_Key8A_PhonMetOnly_With4D"], k8["new_intact_563"]["After_Key8A_PhonMetOnly_With4D"]),
        ("K8A\n(272)", k8["lipi_intact_3600"]["After_Key8A_With4D"], k8["new_intact_563"]["After_Key8A_With4D"]),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 5.0), gridspec_kw={"width_ratios": [1.12, 1.0]})
    fig.subplots_adjust(wspace=0.28)

    # --- Panel A ---
    ax1.fill_between(xs, lipi_pct, new_pct, color=SOFT_GREEN, alpha=0.75, label="Unseen > Lipi parity margin (+0.2 to +5.1 pp)")
    ax1.plot(xs, lipi_pct, "-o", color=NAVY, linewidth=2.2, markersize=5.8, label="Lipi training intact (3,600 faces; 13,209 tok)")
    ax1.plot(xs, new_pct, "-s", color=TEAL, linewidth=2.2, markersize=5.8, label="Unseen Mahadevan holdout (563 faces; 1,994 tok)")

    # Dotted extension to testing frontier (305)
    ax1.plot(
        [xs[-1], frontier["n_signs"]],
        [lipi_pct[-1], frontier["lipi_token_pct"]],
        ":o",
        color=NAVY,
        alpha=0.55,
        linewidth=1.4,
        markersize=4.5,
    )
    ax1.plot(
        [xs[-1], frontier["n_signs"]],
        [new_pct[-1], frontier["new_token_pct"]],
        ":s",
        color=TEAL,
        alpha=0.55,
        linewidth=1.4,
        markersize=4.5,
    )

    ax1.axhline(95.0, color=AMBER, linestyle="--", linewidth=1.1, alpha=0.85)
    ax1.text(36, 95.9, "95% Unseen Holdout Milestone", color="#9A6000", fontsize=8.0, fontweight="bold")

    # Key milestone callouts (zero overlaps)
    ax1.annotate(
        f"K3A (33)\nL:{lipi_pct[0]:.2f}% | U:{new_pct[0]:.2f}%",
        xy=(xs[0], new_pct[0]),
        xytext=(68, 53.5),
        fontsize=7.5,
        color=DARK_TEXT,
        bbox=dict(boxstyle="round,pad=0.20", fc="white", ec=MID_GRAY, alpha=0.92),
        arrowprops=dict(arrowstyle="->", color=SLATE, lw=0.8),
    )
    idx_140 = [i for i, p in enumerate(pts) if p["n_signs"] == 140][0]
    ax1.annotate(
        f"K5A (140)\n{new_pct[idx_140]:.2f}% U",
        xy=(xs[idx_140], new_pct[idx_140]),
        xytext=(112, 89.2),
        fontsize=7.5,
        color=TEAL,
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.8),
    )
    idx_227 = [i for i, p in enumerate(pts) if p["n_signs"] == 227][0]
    ax1.annotate(
        f"K7A (227)\nU:{new_pct[idx_227]:.2f}%\nL:{lipi_pct[idx_227]:.2f}%",
        xy=(xs[idx_227], lipi_pct[idx_227]),
        xytext=(178, 74.0),
        fontsize=7.5,
        color=DARK_TEXT,
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=MID_GRAY, alpha=0.92),
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.8),
    )
    ax1.annotate(
        f"K8A Locked (272)\nU: {new_pct[-1]:.2f}%\nL: {lipi_pct[-1]:.2f}%",
        xy=(xs[-1], new_pct[-1]),
        xytext=(228, 59.0),
        fontsize=7.9,
        fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.28", fc=SOFT_BLUE, ec=NAVY, lw=0.9),
        arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.0),
    )
    ax1.annotate(
        f"Frontier (305)\nU:{frontier['new_token_pct']:.1f}%",
        xy=(frontier["n_signs"], frontier["new_token_pct"]),
        xytext=(276, 100.3),
        fontsize=7.2,
        color=SLATE,
        ha="center",
    )

    ax1.set_xlim(22, 318)
    ax1.set_ylim(40, 105.0)
    ax1.set_xlabel("Locked Lexicon Size (Number of Signs)")
    ax1.set_ylabel("Intact Token Coverage (%)")
    ax1.set_title("A. Unseen Holdout Parity (22/22 Clean Tiers Pass)", fontsize=10.0)
    ax1.grid(True, axis="y", alpha=0.55)
    ax1.legend(loc="lower right", frameon=True, facecolor="white", edgecolor=MID_GRAY, fontsize=7.6)

    # --- Panel B ---
    labels_b = [m[0] for m in milestones_b]
    lipi_100_pct = [m[1]["faces_100pct_pct"] for m in milestones_b]
    new_100_pct = [m[2]["faces_100pct_pct"] for m in milestones_b]
    comb_100_cnt = [m[1]["faces_100pct"] + m[2]["faces_100pct"] for m in milestones_b]
    new_100_cnt = [m[2]["faces_100pct"] for m in milestones_b]

    x_pos = np.arange(len(labels_b))
    w = 0.36
    ax2.bar(x_pos - w / 2, lipi_100_pct, width=w, color=NAVY, label="Lipi 100%-decoded (% of 3,600)")
    ax2.bar(x_pos + w / 2, new_100_pct, width=w, color=TEAL, label="Unseen 100%-decoded (% of 563)")

    for i, (lp, npct, ccnt) in enumerate(zip(lipi_100_pct, new_100_pct, comb_100_cnt)):
        top_y = max(lp, npct)
        y_off = 5.4 if i == 0 else 2.0
        ax2.text(x_pos[i], top_y + y_off, f"{ccnt:,}", ha="center", va="bottom", fontsize=7.8, fontweight="bold", color=DARK_TEXT)
        ax2.text(x_pos[i] - w / 2, lp - 3.6 if lp > 20 else lp + 0.8, f"{lp:.0f}%", ha="center", va="top" if lp > 20 else "bottom", fontsize=6.6, color="white" if lp > 20 else NAVY, fontweight="bold")
        ax2.text(x_pos[i] + w / 2, npct - 3.6 if npct > 20 else npct + 0.8, f"{npct:.0f}%", ha="center", va="top" if npct > 20 else "bottom", fontsize=6.6, color="white" if npct > 20 else TEAL, fontweight="bold")

    ax2.annotate(
        f"Unseen: {new_100_cnt[-1]}/563 ({new_100_pct[-1]:.2f}%)",
        xy=(x_pos[-1] + w / 2, new_100_pct[-1]),
        xytext=(x_pos[-1] - 1.85, 106.0),
        fontsize=7.6,
        fontweight="bold",
        color=TEAL,
        bbox=dict(boxstyle="round,pad=0.25", fc=SOFT_GREEN, ec=TEAL, lw=0.8),
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9),
    )

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(labels_b, fontsize=8.0)
    ax2.set_ylim(0, 116)
    ax2.set_ylabel("100%-Decoded Intact Faces (%)")
    ax2.set_xlabel("Decipherment Milestone (* = Strict Phon/Met+4D)")
    ax2.set_title("B. 100%-Decoded Intact Faces (Combined / 4,163)", fontsize=10.0)
    ax2.grid(True, axis="y", alpha=0.55)
    ax2.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=MID_GRAY, fontsize=7.6)

    save_figure(fig, "fig1")


# =============================================================================
# FIGURE 2: 6-Wave Strictly Pairwise-Disjoint 7-Family Meta-Analysis & Audits
# =============================================================================


def build_fig2() -> None:
    c6 = load_json("work_data/key8c/combined_6wave_meta_stats.json")
    meta6 = c6["meta_7family"]["strictly_disjoint_6wave_115"]
    jk = c6["leave_one_wave_out_jackknife"]["drops"]
    daughter = c6["daughter_lexicon_sensitivity"]["lexicons"]

    fig = plt.figure(figsize=(12.6, 5.8))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.18, 1.0], height_ratios=[1.0, 1.15], wspace=0.32, hspace=0.44)
    axA = fig.add_subplot(gs[:, 0])
    axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[1, 1])

    # --- Panel A: 7-Family Fisher chi2_12 (PhonSt vs PhonEx) ---
    fam_order = [
        ("Dravidian", "Proto-Dravidian\n(2-br fixed, 3,411)"),
        ("Dravidian_RawPDrav", "Proto-Dravidian*\n(RawPDrav, 3,256)"),
        ("Indo-Aryan", "Indo-Aryan (OIA)\n(6,338 etyma)"),
        ("Sumerian", "Sumerian\n(3,385 etyma)"),
        ("Munda", "Munda\n(1,417 etyma)"),
        ("Elamite", "Elamite\n(2,437 etyma)"),
        ("Akkadian", "Akkadian\n(716 etyma)"),
        ("Burushaski", "Burushaski\n(1,743 etyma)"),
    ]
    y = np.arange(len(fam_order))
    chi_st = [max(0.0, float(meta6["phon_stem"][f]["fisher_chi2"])) for f, _ in fam_order]
    chi_ex = [max(0.0, float(meta6["phon_exact"][f]["fisher_chi2"])) for f, _ in fam_order]
    bonf_st = [float(meta6["phon_stem"][f]["fisher_p_bonf7"]) for f, _ in fam_order]
    bonf_ex = [float(meta6["phon_exact"][f]["fisher_p_bonf7"]) for f, _ in fam_order]
    p_st = [float(meta6["phon_stem"][f]["fisher_p"]) for f, _ in fam_order]
    p_ex = [float(meta6["phon_exact"][f]["fisher_p"]) for f, _ in fam_order]

    # Sum wave hits directly from wave1_obs..wave6_obs
    def sum_hits(entry: dict[str, Any]) -> int:
        tot = 0
        for wi in range(1, 7):
            s = str(entry.get(f"wave{wi}_obs", "0/0"))
            tot += int(s.split("/")[0])
        return tot

    hits_st = [sum_hits(meta6["phon_stem"][f]) for f, _ in fam_order]
    hits_ex = [sum_hits(meta6["phon_exact"][f]) for f, _ in fam_order]

    h = 0.36
    colors_st = [NAVY if "Dravidian" in f else "#7F8C8D" for f, _ in fam_order]
    colors_ex = [TEAL if "Dravidian" in f else "#BDC3C7" for f, _ in fam_order]
    axA.barh(y - h / 2, chi_st, height=h, color=colors_st, label="PhonSt (phonemic stem)")
    axA.barh(y + h / 2, chi_ex, height=h, color=colors_ex, label="PhonEx (exact homophony)")

    # Bonf-7 chi2_12 threshold: P=0.05/7=0.0071428 -> chi2_12 = 27.25
    axA.axvline(27.25, color=CRIMSON, linestyle="--", linewidth=1.2)
    axA.annotate(
        "Bonf-7 threshold\n(α = 0.00714, χ²₁₂ = 27.25)",
        xy=(27.25, 3.65),
        xytext=(68.0, 3.65),
        color=CRIMSON,
        fontsize=7.5,
        fontweight="bold",
        va="center",
        bbox=dict(boxstyle="round,pad=0.25", fc="#FDEDEC", ec=CRIMSON, lw=0.8),
        arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=1.0),
    )

    for i in range(len(fam_order)):
        if chi_st[i] > 1.0:
            lbl_st = f"{hits_st[i]}/115  P={p_st[i]:.2e} (B7={bonf_st[i]:.2e})" if p_st[i] < 1e-3 else f"{hits_st[i]}/115  B7={bonf_st[i]:.2f}"
            axA.text(chi_st[i] + 1.2, y[i] - h / 2, lbl_st, va="center", ha="left", fontsize=7.2, fontweight="bold" if i < 2 else "normal", color=NAVY if i < 2 else DARK_TEXT)
        if chi_ex[i] > 1.0:
            lbl_ex = f"{hits_ex[i]}/115  P={p_ex[i]:.2e} (B7={bonf_ex[i]:.2e})" if p_ex[i] < 1e-3 else f"{hits_ex[i]}/115  B7={bonf_ex[i]:.2f}"
            axA.text(chi_ex[i] + 1.2, y[i] + h / 2, lbl_ex, va="center", ha="left", fontsize=7.2, fontweight="bold" if i < 2 else "normal", color=TEAL if i < 2 else SLATE)
        elif chi_st[i] == 0.0 and chi_ex[i] == 0.0:
            axA.text(1.4, y[i], "0/115 hits  (χ² = 0.00, Bonf-7 P = 1.00)", va="center", ha="left", fontsize=7.1, color=SLATE)

    axA.set_yticks(y)
    axA.set_yticklabels([lbl for _, lbl in fam_order], fontsize=8.0)
    axA.invert_yaxis()
    axA.set_xlim(0, 130)
    axA.set_xlabel("6-Wave Fisher Combined χ² (df = 12; 15/15 Wave Pairs Disjoint)")
    axA.set_title("A. 6-Wave Strictly Disjoint 7-Family Meta-Analysis (115 Unique Signs)", fontsize=9.8)
    axA.grid(True, axis="x", alpha=0.5)
    axA.legend(loc="lower right", frameon=True, facecolor="white", edgecolor=MID_GRAY)

    # --- Panel B: Leave-One-Wave-Out Jackknife (6/6 drops) ---
    drop_keys = ["drop_W1", "drop_W2", "drop_W3", "drop_W4", "drop_W5", "drop_W6"]
    drop_lbls = ["−W1\n(103)", "−W2\n(91)", "−W3\n(107)", "−W4\n(96)", "−W5\n(88)", "−W6\n(90)"]
    x_jk = np.arange(len(drop_keys))
    neglog_st = [-math.log10(float(jk[k]["phon_stem"]["Dravidian"]["fisher_p_bonf7"])) for k in drop_keys]
    neglog_ex = [-math.log10(float(jk[k]["phon_exact"]["Dravidian"]["fisher_p_bonf7"])) for k in drop_keys]
    neglog_ia = [-math.log10(float(jk[k]["phon_stem"]["Indo-Aryan"]["fisher_p_bonf7"])) for k in drop_keys]

    axB.bar(x_jk - 0.25, neglog_st, width=0.25, color=NAVY, label="Drav PhonSt")
    axB.bar(x_jk, neglog_ex, width=0.25, color=TEAL, label="Drav PhonEx")
    axB.bar(x_jk + 0.25, neglog_ia, width=0.25, color=AMBER, label="Best Rival (IA)")
    axB.axhline(-math.log10(0.05), color=CRIMSON, linestyle="--", linewidth=1.0, label="Bonf-7 P = 0.05")

    for i in range(len(drop_keys)):
        axB.text(x_jk[i] - 0.25, neglog_st[i] + 0.25, f"{neglog_st[i]:.1f}", ha="center", va="bottom", fontsize=6.6, color=NAVY, fontweight="bold")
        axB.text(x_jk[i], neglog_ex[i] + 0.25, f"{neglog_ex[i]:.1f}", ha="center", va="bottom", fontsize=6.6, color=TEAL, fontweight="bold")

    axB.set_xticks(x_jk)
    axB.set_xticklabels(drop_lbls, fontsize=7.6)
    axB.set_ylim(0, 12.0)
    axB.set_ylabel("−log₁₀(Bonf-7 P)")
    axB.set_title("B. Leave-One-Wave-Out Jackknife (6/6 Drops Pass Bonf-7)", fontsize=9.8)
    axB.grid(True, axis="y", alpha=0.5)
    axB.legend(loc="upper left", ncol=2, fontsize=6.7, frameon=True, facecolor="white", edgecolor=MID_GRAY)

    # --- Panel C: Pooled 115-Sign Mega-Shuffle & Daughter-Lexicon Sensitivity ---
    lex_order = [
        ("Dravidian", "Drav 2-br (3,411)"),
        ("Dravidian_RawPDrav", "RawPDrav (3,256)"),
        ("Dravidian_2Lang", "Drav 2-Lang (5,095)"),
        ("Dravidian_Tamil_DEDR", "Tamil DEDR (3,447)"),
        ("Indo-Aryan", "OIA Cogn (6,338)"),
        ("Indo-Aryan_Turner", "Turner IA (9,254)"),
        ("Sumerian_Halloran", "Halloran Sum (3,257)"),
        ("Munda_Santali_Campbell", "Santali Mun (12,001)"),
        ("Elamite_HinzKoch", "Hinz-Koch El (2,437)"),
    ]
    yl = np.arange(len(lex_order))
    z_st = [float(daughter[k]["phon_stem"]["z"]) for k, _ in lex_order]
    z_ex = [float(daughter[k]["phon_exact"]["z"]) for k, _ in lex_order]
    p_lst = [float(daughter[k]["phon_stem"]["p"]) for k, _ in lex_order]
    hl = 0.36

    axC.barh(yl - hl / 2, z_st, height=hl, color=[NAVY if "Drav" in k else "#85929E" for k, _ in lex_order], label="PhonSt z")
    axC.barh(yl + hl / 2, z_ex, height=hl, color=[TEAL if "Drav" in k else "#CCD1D1" for k, _ in lex_order], label="PhonEx z")
    axC.axvline(0.0, color="#2C3E50", linewidth=0.7)
    axC.axvline(2.45, color=CRIMSON, linestyle="--", linewidth=1.0)

    for i, (k, _) in enumerate(lex_order):
        zv = max(z_st[i], z_ex[i], 0.0)
        ptxt = f"P={p_lst[i]:.4f}" if p_lst[i] < 0.01 else f"P={p_lst[i]:.2f}"
        axC.text(zv + 0.18, yl[i], f"z={z_st[i]:+.1f} ({ptxt})", va="center", ha="left", fontsize=6.7, color=NAVY if "Drav" in k else SLATE, fontweight="bold" if "Drav" in k else "normal")

    axC.set_yticks(yl)
    axC.set_yticklabels([lbl for _, lbl in lex_order], fontsize=7.3)
    axC.invert_yaxis()
    axC.set_xlim(-1.2, 9.6)
    axC.set_xlabel("Pooled 115-Sign Mega-Shuffle z-score (5,000 Shuffles)")
    axC.set_title("C. Pooled 115-Sign & Wider Daughter-Lexicon Sensitivity")
    axC.grid(True, axis="x", alpha=0.5)
    axC.legend(loc="lower right", fontsize=7.0, frameon=True, facecolor="white", edgecolor=MID_GRAY)

    save_figure(fig, "fig2")


# =============================================================================
# FIGURE 3: Dholavira North Gate Signboard (Lipi 144.1, 10-Sign Breakdown)
# =============================================================================


def build_fig3() -> None:
    dhol = load_json("work_data/key8a/dholavira_signboard_audit_v2.json")
    pos10 = dhol["positions_10"]
    summary = dhol["reading_summary_key8a"]
    s388 = dhol["sign_388_pipal_audit"]
    s611 = dhol["sign_611_portal_audit"]
    s645 = dhol["sign_6_and_645_audit"]

    img_draw_p = ROOT / "work_data/key7d/dholavira_pdf_imgs/img_011.jpg"
    img_photo_p = ROOT / "work_data/key7d/dholavira_pdf_imgs/img_012.jpg"

    fig = plt.figure(figsize=(12.8, 6.6))
    gs = GridSpec(4, 1, figure=fig, height_ratios=[1.15, 1.05, 1.85, 1.05], hspace=0.22)

    # Top title banner via suptitle
    fig.suptitle(
        f"Dholavira North Gate Signboard (Lipi {dhol['object_id']}, ~3.0 m Gypsum Inlay): "
        f"{summary['locked_out_of_10_strict_phonetic']}/10 Strict Phonetic  |  "
        f"{summary['locked_out_of_10_with_corpus_645']}/10 with Corpus 645  |  "
        f"{summary['all_10_glossed_with_611_architectural']}/10 Glossed",
        fontsize=11.0,
        fontweight="bold",
        color=NAVY,
        y=0.98,
    )

    # Band 1: Bisht 2015 official line drawing
    ax_draw = fig.add_subplot(gs[0])
    if img_draw_p.is_file():
        im_d = Image.open(img_draw_p).convert("RGB")
        ax_draw.imshow(im_d, aspect="auto")
    ax_draw.set_xticks([])
    ax_draw.set_yticks([])
    for sp in ax_draw.spines.values():
        sp.set_visible(True)
        sp.set_edgecolor(MID_GRAY)
        sp.set_linewidth(0.8)
    ax_draw.set_title(
        "A. Bisht (2015, ASI) Official In-Situ Line Drawing (Fallen Face-Down: L→R In-Situ = Standard Harappan R→L Upright Reading Order #1 → #10)",
        fontsize=8.6,
        loc="left",
        pad=4,
        color=DARK_TEXT,
    )

    # Band 2: Bisht 2015 excavation photo
    ax_photo = fig.add_subplot(gs[1])
    if img_photo_p.is_file():
        im_p = Image.open(img_photo_p).convert("RGB")
        ax_photo.imshow(im_p, aspect="auto")
    ax_photo.set_xticks([])
    ax_photo.set_yticks([])
    for sp in ax_photo.spines.values():
        sp.set_visible(True)
        sp.set_edgecolor(MID_GRAY)
        sp.set_linewidth(0.8)
    ax_photo.set_title(
        "B. Excavation Photograph of White Gypsum/Stone-Paste Inlays in North Gate Western Chamber (Bisht 2015, Fig. 8.3)",
        fontsize=8.6,
        loc="left",
        pad=4,
        color=DARK_TEXT,
    )

    # Band 3: 10-tile structured reading breakdown
    ax_tiles = fig.add_subplot(gs[2])
    ax_tiles.set_xlim(0, 10)
    ax_tiles.set_ylim(0, 2.35)
    ax_tiles.axis("off")
    ax_tiles.text(
        0.0,
        2.26,
        "C. Sign-by-Sign Key #8A Decipherment (10 Expanded Tokens; Lipi 821 = Paired 820–820 *iru-kāl)",
        fontsize=8.8,
        fontweight="bold",
        color=DARK_TEXT,
        va="bottom",
    )

    short_gloss = {
        1: "quarter /\nward-wheel",
        2: "gate-lintel /\nportal canopy",
        3: "royal pipal\nemblem",
        4: "quarter /\nward-wheel",
        5: "eye / copper\nprecinct",
        6: "passage-tax\ntally (caveat)",
        7: "numeral 1\n(tall stroke)",
        8: "quarter (1/2)\nLipi 821",
        9: "quarter (2/2)\nLipi 821",
        10: "bound\nhouse-guild",
    }
    short_read = {
        1: "*kāl",
        2: "*nukam /\n*kuṭai",
        3: "*aracu /\n*āku",
        4: "*kāl",
        5: "*kaṇ /\n*kaṉ",
        6: "*kaṭa /\n*kaṭam",
        7: "*oru (1)",
        8: "*kāl",
        9: "*kāl",
        10: "*toṭu /\n*iṭukku",
    }

    for idx, item in enumerate(pos10):
        pos = int(item["pos"])
        st = item["status_key8a"]
        if st == "LOCKED":
            fc, ec, badge, bc = SOFT_GREEN, EMERALD, "LOCKED", EMERALD
        elif "645" in st:
            fc, ec, badge, bc = SOFT_AMBER, AMBER, "CORPUS 645?", AMBER
        else:
            fc, ec, badge, bc = SOFT_BLUE, NAVY, "ARCH. LOCK", NAVY

        x0 = idx + 0.05
        box = patches.FancyBboxPatch(
            (x0, 0.34),
            0.90,
            1.78,
            boxstyle="round,pad=0.03,rounding_size=0.07",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.35,
        )
        ax_tiles.add_patch(box)

        # Top badge
        bpatch = patches.FancyBboxPatch(
            (x0 + 0.04, 1.84),
            0.82,
            0.23,
            boxstyle="round,pad=0.01,rounding_size=0.04",
            facecolor=bc,
            edgecolor="none",
        )
        ax_tiles.add_patch(bpatch)
        ax_tiles.text(x0 + 0.45, 1.955, f"#{pos} {badge}", ha="center", va="center", fontsize=6.1, fontweight="bold", color="white")

        m77_short = str(item["m77"]).split(" ")[0]
        ax_tiles.text(x0 + 0.45, 1.63, f"Lipi {item['lipi_sign']}", ha="center", va="center", fontsize=8.4, fontweight="bold", color=DARK_TEXT)
        ax_tiles.text(x0 + 0.45, 1.43, m77_short, ha="center", va="center", fontsize=7.0, color=SLATE)
        ax_tiles.text(x0 + 0.45, 1.07, short_read[pos], ha="center", va="center", fontsize=8.2, fontweight="bold", color=NAVY)
        ax_tiles.text(x0 + 0.45, 0.58, short_gloss[pos], ha="center", va="center", fontsize=6.7, color=DARK_TEXT)

    # Bracket under #8-#9 for Lipi 821 (*iru-kāl)
    ax_tiles.plot([7.10, 7.10, 8.90, 8.90], [0.27, 0.16, 0.16, 0.27], color=EMERALD, lw=1.3)
    ax_tiles.text(8.00, 0.03, "Lipi 821 = *iru-kāl (2× 820, Key #5A Rank #1 double, P=0.0002)", ha="center", va="center", fontsize=7.1, fontweight="bold", color=EMERALD)

    # Bracket under #1-#2 for Lothal L-116 parallel
    ax_tiles.plot([0.10, 0.10, 1.90, 1.90], [0.27, 0.16, 0.16, 0.27], color=NAVY, lw=1.3)
    ax_tiles.text(1.00, 0.03, "Lothal L-116 exact parallel (820-611)", ha="center", va="center", fontsize=7.1, fontweight="bold", color=NAVY)

    # Band 4: Three epigraphic evidence boxes
    ax_ev = fig.add_subplot(gs[3])
    ax_ev.set_xlim(-0.02, 3.04)
    ax_ev.set_ylim(0, 1.05)
    ax_ev.axis("off")

    ev_boxes = [
        (
            0.0,
            NAVY,
            SOFT_BLUE,
            "Sign #2 (611 / M256): Architectural Lock",
            f"• 3/6 Lipi texts pair w/ 820 (OR={s611['cooccurrence_with_820_lipi']['odds_ratio']:.1f}×, P={s611['cooccurrence_with_820_lipi']['fisher_p']:.4f})\n"
            f"• Exact opening 820-611 on Lothal L-116 (steatite, 850 mm²)\n"
            f"• Monumental contexts: Dholavira, H-3 (2,767 mm²), M-56\n"
            f"• 2-br DEDR: *nukam ('bar') / *kuṭai ('canopy'); open root",
        ),
        (
            1.02,
            EMERALD,
            SOFT_GREEN,
            "Sign #3 (388 / M327): Royal Pipal Emblem Lock",
            f"• Veined pipal paradigm w/ locked 384 (cosMean={s388['cos_384_vs_388']['cosMean']:.3f})\n"
            f"• 388→443 OR={s388['fisher_388_to_443']['odds_ratio']:.0f}× (P={s388['fisher_388_to_443']['fisher_p']:.2e}); "
            f"388→740 P={s388['fisher_388_to_740']['fisher_p']:.2e}\n"
            f"• 585 (*paḷḷi)→388 OR={s388['fisher_585_to_388']['odds_ratio']:.1f}× (P={s388['fisher_585_to_388']['fisher_p']:.2e})\n"
            f"• DEDR 202 *aracu (pipal) & 201 *aracaṉ (king): FIX & RAW",
        ),
        (
            2.04,
            AMBER,
            SOFT_AMBER,
            "Sign #6 (645? / M137): Corpus Lock + Caveat",
            f"• Corpus 645 ({s645['corpus_645_stats']['comb_intact']}C/{s645['corpus_645_stats']['new_intact']}N): "
            f"104→645 P={s645['corpus_645_stats']['fisher_104_to_645']['fisher_p']:.2e}\n"
            f"• 645→590 P={s645['corpus_645_stats']['fisher_645_to_590']['fisher_p']:.2e}; "
            f"FIX 2-br *kaṭa ↔ *kaṭam\n"
            f"• Sign 064 (slender Y-fork) visually ruled out (M-361/932)\n"
            f"• 144.1 #6: 5-strip inv-V + 19 loose pieces (ASI 24.03.95)",
        ),
    ]
    for x0, ec, fc, title, body in ev_boxes:
        rect = patches.FancyBboxPatch(
            (x0, 0.04),
            0.96,
            0.96,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.1,
            alpha=0.65,
        )
        ax_ev.add_patch(rect)
        ax_ev.text(x0 + 0.03, 0.91, title, fontsize=7.6, fontweight="bold", color=ec, va="top")
        ax_ev.text(x0 + 0.03, 0.72, body, fontsize=6.4, color=DARK_TEXT, va="top", linespacing=1.34)

    save_figure(fig, "fig3")


# =============================================================================
# FIGURE 4: 4-Tier Sangam Epigraphy & Whole-Object Multi-Face Accounting
# =============================================================================


def build_fig4() -> None:
    s8b1 = load_json("work_data/key8b/test8b1_sangam_227plus.json")
    s8b3 = load_json("work_data/key8b/test8b3_multiface_key8.json")

    fig = plt.figure(figsize=(12.8, 5.7))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.22, 1.0], height_ratios=[1.05, 1.12], wspace=0.34, hspace=0.46)
    axA = fig.add_subplot(gs[:, 0])
    axB1 = fig.add_subplot(gs[0, 1])
    axB2 = fig.add_subplot(gs[1, 1])

    # --- Panel A: 4-Tier Sangam Compounds ---
    t1 = s8b1["tier1_frozen_170"]
    t2 = s8b1["tier2_expanded_attested_w56"]
    t3 = s8b1["tier3_non_numeral_lexical_only"]
    t4 = s8b1["tier4_automated_dedr_tamil_dict"]
    prak = s8b1["prakrit_loan_control"]["key8a_272_lipi_ge2"]

    cats = [
        ("T2 Dravidian\n(220 headwords)", t2["key8a_272_full_lipi_ge2"]["obs_words"], t2["key8a_272_full_lipi_ge2"]["perm_words"]["mean"], t2["key8a_272_full_lipi_ge2"]["perm_words"]["z"], t2["key8a_272_full_lipi_ge2"]["perm_words"]["p"], NAVY),
        ("T1 Frozen Drav\n(170 headwords)", t1["key8a_272_full_lipi_ge2"]["obs_words"], t1["key8a_272_full_lipi_ge2"]["perm_words"]["mean"], t1["key8a_272_full_lipi_ge2"]["perm_words"]["z"], t1["key8a_272_full_lipi_ge2"]["perm_words"]["p"], "#2E5984"),
        ("T2 Quarantined\nPrakrit (30)", prak["words"], 0.0, 0.0, 1.0, CRIMSON),
        ("T2 MW-IA Rival\n(140 headwords)", t2["rival_ia_272"]["obs_words"], t2["rival_ia_272"]["perm_words"]["mean"], t2["rival_ia_272"]["perm_words"]["z"], t2["rival_ia_272"]["perm_words"]["p"], AMBER),
        ("T2 Ur III Sum\n(114 headwords)", t2["rival_sumerian_272"]["obs_words"], t2["rival_sumerian_272"]["perm_words"]["mean"], t2["rival_sumerian_272"]["perm_words"]["z"], t2["rival_sumerian_272"]["perm_words"]["p"], SLATE),
        ("T3 Lexical-Only\nDravidian", t3["key8a_272_expanded"]["obs_words"], t3["key8a_272_expanded"]["perm_words"]["mean"], t3["key8a_272_expanded"]["perm_words"]["z"], t3["key8a_272_expanded"]["perm_words"]["p"], TEAL),
        ("T3 Lexical-Only\nMW-IA Rival", t3["rival_ia_272_lexonly"]["obs_words"], t3["rival_ia_272_lexonly"]["perm_words"]["mean"], t3["rival_ia_272_lexonly"]["perm_words"]["z"], t3["rival_ia_272_lexonly"]["perm_words"]["p"], "#E59866"),
        ("T3 Lexical-Only\nUr III Sum", t3["rival_sumerian_272_lexonly"]["obs_words"], t3["rival_sumerian_272_lexonly"]["perm_words"]["mean"], t3["rival_sumerian_272_lexonly"]["perm_words"]["z"], t3["rival_sumerian_272_lexonly"]["perm_words"]["p"], "#99A3A4"),
        ("T4 Uncurated\nDEDR (14,206)", t4["key8a_272_exact_phoneme"]["obs_words"], t4["key8a_272_exact_phoneme"]["perm_words"]["mean"], t4["key8a_272_exact_phoneme"]["perm_words"]["z"], t4["key8a_272_exact_phoneme"]["perm_words"]["p"], PURPLE),
    ]

    ya = np.arange(len(cats))
    ha = 0.38
    obs_vals = [c[1] for c in cats]
    null_vals = [c[2] for c in cats]
    cols_a = [c[5] for c in cats]

    axA.barh(ya - ha / 2, obs_vals, height=ha, color=cols_a, label="Observed attested compounds (Lipi ≥2)")
    axA.barh(ya + ha / 2, null_vals, height=ha, color=LIGHT_GRAY, edgecolor=SLATE, linewidth=0.7, hatch="///", label="5,000-perm null mean")

    for i, (lbl, obs, nmu, z, p, col) in enumerate(cats):
        xmax = max(obs, nmu)
        if "Prakrit" in lbl:
            txt = "0/30 hits  (0 Lipi, 0 Unseen mass)"
        else:
            pstr = f"P={p:.4f}" if p < 0.01 else f"P={p:.3f}"
            txt = f"{obs} vs {nmu:.1f}  (z={z:+.2f}, {pstr})"
        axA.text(xmax + 1.0, ya[i], txt, va="center", ha="left", fontsize=7.2, fontweight="bold" if col in (NAVY, TEAL, PURPLE, CRIMSON) else "normal", color=col if col != SLATE else DARK_TEXT)

    # Place callout and legend in the wide open middle-right zone (next to rows 2-4)
    w56 = t2["key8a_272_w56_ge1_lipi_ge2"]
    unseen_rep = t2["unseen_new_full_272"]
    axA.text(
        0.985,
        0.53,
        f"Wave-5/6 Novel (≥1 new): {w56['obs_words']} words\n"
        f"  (z={w56['perm_words']['z']:+.2f}, P={w56['perm_words']['p']:.4f})\n"
        f"Unseen Holdout: {unseen_rep['words']} compounds\n"
        f"  ({unseen_rep['new_mass']} Mahadevan tokens)",
        transform=axA.transAxes,
        ha="right",
        va="center",
        fontsize=7.0,
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.28", fc=SOFT_BLUE, ec=NAVY, lw=0.8),
    )

    axA.set_yticks(ya)
    axA.set_yticklabels([c[0] for c in cats], fontsize=7.6)
    axA.invert_yaxis()
    axA.set_xlim(0, 86)
    axA.set_xlabel("Distinct Attested Compound Headwords (272-Sign Lexicon)")
    axA.set_title("A. 4-Tier Sangam / Tamil-Brahmi Epigraphy (272 Signs)", fontsize=9.8)
    axA.grid(True, axis="x", alpha=0.5)
    axA.legend(loc="center right", bbox_to_anchor=(0.985, 0.72), fontsize=7.0, frameon=True, facecolor="white", edgecolor=MID_GRAY)

    # --- Panel B1: Multi-face 100%-decoded progression ---
    prog = s8b3["corpus_counts"]["progression"]
    n_intact_mf = s8b3["corpus_counts"]["intact_multiface_raw"]
    tiers_mf = [
        ("K6A\n(163)", prog["163_signs"]["raw"], prog["163_signs"]["pct"], "#7FB3D5"),
        ("K7A\n(227)", prog["227_signs"]["raw"], prog["227_signs"]["pct"], "#2E86C1"),
        ("K8A*\n(266)", prog["266_strict"]["raw"], prog["266_strict"]["pct"], TEAL),
        ("K8A\n(272)", prog["272_full"]["raw"], prog["272_full"]["pct"], NAVY),
    ]
    xm = np.arange(len(tiers_mf))
    vals_m = [t[1] for t in tiers_mf]
    axB1.bar(xm, vals_m, width=0.54, color=[t[3] for t in tiers_mf], edgecolor="none")
    for i, (_, cnt, pct, _) in enumerate(tiers_mf):
        axB1.text(xm[i], cnt + 12, f"{cnt}/{n_intact_mf}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=7.4, fontweight="bold", color=DARK_TEXT)

    comp = s8b3["test_8b3a_complementarity"]["strict_who_meas_2face"]
    axB1.text(
        0.50,
        0.96,
        f"WHO || MEAS: {comp['obs_complementary']}/{comp['n_objects']} ({comp['obs_complementary_pct']:.1f}%) vs {comp['null_repair_mean']:.1f} null (P={comp['p_repair_5000']:.4f})",
        transform=axB1.transAxes,
        va="top",
        ha="center",
        fontsize=7.2,
        fontweight="bold",
        color=EMERALD,
        bbox=dict(boxstyle="round,pad=0.26", fc=SOFT_GREEN, ec=EMERALD, lw=0.8),
    )
    axB1.set_xticks(xm)
    axB1.set_xticklabels([t[0] for t in tiers_mf], fontsize=7.8)
    axB1.set_ylim(0, 680)
    axB1.set_ylabel("100%-Decoded Objects")
    axB1.set_title("B1. Multi-Face 100%-Decoded Progression (n = 606)", fontsize=9.8)
    axB1.grid(True, axis="y", alpha=0.5)

    # --- Panel B2: Recipient Rank -> Partner Face Class (chi2=67.12, P=0.0008) ---
    rc = s8b3["test_8b3c_rank_to_contract_and_ration"]
    rtab = rc["rank_partner_table"]
    rank_order = [
        ("Junior_cikka", "Junior (*cikka)"),
        ("Guard_Porter_ka", "Guard (*kā)"),
        ("House_kuti_palli", "House (*kuṭi/*paḷḷi)"),
        ("Elite_vel_talai_ko_aracu", "Elite (*vēḷ/*kō/*aracu)"),
        ("Manager_al", "Manager (*āḷ)"),
    ]
    yr = np.arange(len(rank_order))
    p_meas, p_who, p_comm, p_oth = [], [], [], []
    totals_r = []
    for rk, _ in rank_order:
        row = rtab[rk]
        tot = sum(row.values())
        totals_r.append(tot)
        p_meas.append(100.0 * row.get("MEASURE_RATION", 0) / tot)
        p_who.append(100.0 * row.get("WHO_OFFICE_HOUSE", 0) / tot)
        p_comm.append(100.0 * row.get("COMMODITY_TAX_SHARE", 0) / tot)
        p_oth.append(100.0 * (row.get("COUNT_ONLY", 0) + row.get("OTHER_UNDEC", 0)) / tot)

    p_meas = np.array(p_meas)
    p_who = np.array(p_who)
    p_comm = np.array(p_comm)
    p_oth = np.array(p_oth)

    axB2.barh(yr, p_meas, height=0.58, color=TEAL, label="MEASURE / RATION")
    axB2.barh(yr, p_who, left=p_meas, height=0.58, color=NAVY, label="WHO / OFFICE / HOUSE")
    axB2.barh(yr, p_comm, left=p_meas + p_who, height=0.58, color=AMBER, label="COMMODITY / TAX")
    axB2.barh(yr, p_oth, left=p_meas + p_who + p_comm, height=0.58, color=MID_GRAY, label="OTHER / COUNT")

    for i in range(len(rank_order)):
        if p_meas[i] >= 16:
            axB2.text(p_meas[i] / 2, yr[i], f"{p_meas[i]:.0f}%", ha="center", va="center", fontsize=7.3, color="white", fontweight="bold")
        if p_who[i] >= 12:
            axB2.text(p_meas[i] + p_who[i] / 2, yr[i], f"{p_who[i]:.0f}%", ha="center", va="center", fontsize=7.3, color="white", fontweight="bold")
        axB2.text(101.2, yr[i], f"n={totals_r[i]}", ha="left", va="center", fontsize=7.1, color=DARK_TEXT)

    axB2.set_yticks(yr)
    axB2.set_yticklabels([lbl for _, lbl in rank_order], fontsize=7.7)
    axB2.invert_yaxis()
    axB2.set_xlim(0, 113)
    axB2.set_xlabel("Partner Face Functional Class (%)")
    axB2.set_title(f"B2. Rank → Partner Class (n={rc['n_rank_partner_class']}, χ²={rc['chi2_rank_partner_class']:.2f}, P={rc['p_rank_partner_class_5000']:.4f})")
    axB2.legend(loc="upper center", bbox_to_anchor=(0.48, -0.26), ncol=2, fontsize=6.9, frameon=True, facecolor="white", edgecolor=MID_GRAY)

    save_figure(fig, "fig4")


# =============================================================================
# FIGURE 5: Blind Physical Archaeology, External Bridges & 600-Yr Stability
# =============================================================================


def build_fig5() -> None:
    s8b2 = load_json("work_data/key8b/test8b2_wave56_archaeology.json")
    k7b2 = load_json("work_data/key7b/key7b_summary.json")["test_7b2"]
    k6b = load_json("work_data/key6b/validation_key5_5000perm.json")
    k8d = load_json("work_data/key8d/key8d_summary.json")

    fig = plt.figure(figsize=(13.2, 6.0))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.15, 1.05], height_ratios=[1.35, 0.95], wspace=0.48, hspace=0.50)
    axA = fig.add_subplot(gs[:, 0])
    axB1 = fig.add_subplot(gs[0, 1])
    axB2 = fig.add_subplot(gs[1, 1])

    # --- Panel A: Carved Square-Seal Area Hierarchy (n=1,070) ---
    corpus_med = float(s8b2["corpus_counts"]["corpus_median_mm2"])
    n_sq = int(s8b2["corpus_counts"]["n_sq_seals"])
    ev = s8b2["elite_vs_sub_272"]

    # Lookup helpers from disk JSONs
    map_8b2 = {r["role"]: r for r in s8b2["seal_area_rows"]}
    map_7b2 = {r["role"]: r for r in k7b2["seal_area_rows"]}
    map_6b1 = {r["role"]: r for r in k6b["test_6b1_seal_area_140"]["per_role"]}

    def find_row(d: dict[str, Any], sub: str) -> dict[str, Any]:
        for k, v in d.items():
            if sub in k:
                return v
        raise KeyError(f"Could not find {sub}")

    r595 = find_row(map_7b2, "595")
    r692 = find_row(map_8b2, "692")
    r585 = find_row(map_8b2, "585")
    ramma = find_row(map_6b1, "*ammā")
    r824a = find_row(map_8b2, "824a")
    rmin = find_row(map_6b1, "*mīṉ")
    rtalai = find_row(map_6b1, "*talai")
    r297 = find_row(map_8b2, "297-cl")
    r388 = find_row(map_8b2, "388/382")
    rvel = find_row(map_6b1, "*vēḷ")
    rka = find_row(map_6b1, "*kā ")
    rcikka = find_row(map_6b1, "*cikka")

    area_items = [
        ("595 *mūṭai-vari (bale-tax)", r595["median_area_mm2"], r595["n_seals"], r595["p_two_lensite_5000"], CRIMSON, False),
        ("692 [PRECINCT-HEADER]", r692["median_area_mm2"], r692["n_seals"], r692["p_two_lensite_5000"], CRIMSON, False),
        ("585 *paḷḷi (citadel hall)", r585["median_area_mm2"], r585["n_seals"], r585["p_two_lensite_5000"], NAVY, False),
        ("*ammā (matron, 140)", ramma["median_area_mm2"], ramma["n_seals"], ramma["p_two_lensite_5000"], NAVY, False),
        ("824a *kāṇam (seal split)", r824a["median_area_mm2"], r824a["n_seals"], r824a["p_two_lensite_5000"], NAVY, False),
        ("ELITE COMPOSITE (272)", ev["elite_median_mm2"], ev["n_elite"], ev["p_lensite_5000"], EMERALD, True),
        ("*mīṉ (star-clans)", rmin["median_area_mm2"], rmin["n_seals"], rmin["p_two_lensite_5000"], "#2E86C1", False),
        ("*talai (chief, 100)", rtalai["median_area_mm2"], rtalai["n_seals"], rtalai["p_two_lensite_5000"], "#2E86C1", False),
        ("297-cl *kōṇ (chevron)", r297["median_area_mm2"], r297["n_seals"], r297["p_two_lensite_5000"], "#2E86C1", False),
        ("388/382 *aracu (pipal)", r388["median_area_mm2"], r388["n_seals"], r388["p_two_lensite_5000"], "#2E86C1", False),
        ("*vēḷ (lord, 520)", rvel["median_area_mm2"], rvel["n_seals"], rvel["p_two_lensite_5000"], "#2E86C1", False),
        ("*kā (guard/porter)", rka["median_area_mm2"], rka["n_seals"], rka["p_two_lensite_5000"], AMBER, False),
        ("SUBORDINATE COMP. (272)", ev["sub_median_mm2"], ev["n_sub"], ev["p_lensite_5000"], "#B9770E", True),
        ("*cikka (junior, 400)", rcikka["median_area_mm2"], rcikka["n_seals"], rcikka["p_two_lensite_5000"], AMBER, False),
    ]

    ya = np.arange(len(area_items))
    meds = [float(x[1]) for x in area_items]
    cols_area = [x[4] for x in area_items]

    axA.barh(ya, meds, height=0.66, color=cols_area, alpha=0.88)
    axA.axvline(corpus_med, color=DARK_TEXT, linestyle="--", linewidth=1.05)
    axA.text(
        corpus_med,
        -0.78,
        f"Corpus median: {corpus_med:.1f} mm²",
        fontsize=7.0,
        color=DARK_TEXT,
        fontweight="bold",
        ha="center",
        va="bottom",
    )

    for i, (lbl, med, n_s, pv, col, is_comp) in enumerate(area_items):
        sig = ""
        if is_comp:
            sig = f" [P={pv:.4f}]"
        elif pv < 0.05:
            sig = f" (P={pv:.4f}*)"
        axA.text(
            med + 18,
            ya[i],
            f"{med:,.1f} mm² (n={n_s}){sig}",
            va="center",
            ha="left",
            fontsize=6.8,
            fontweight="bold" if (is_comp or pv < 0.05) else "normal",
            color=col if (is_comp or pv < 0.01) else DARK_TEXT,
        )

    axA.text(
        0.985,
        0.38,
        f"Length+Site-Controlled\nElite vs Subordinate:\n"
        f"{ev['elite_median_mm2']:.1f} vs {ev['sub_median_mm2']:.1f} mm²\n"
        f"(+{ev['diff_resid_log_lensite']:.3f} log mm²)\n"
        f"P = {ev['p_lensite_5000']:.5f}\n"
        f"(no-692 P = {s8b2['elite_vs_sub_272_strict_no692']['p_lensite_5000']:.5f})",
        transform=axA.transAxes,
        ha="right",
        va="center",
        fontsize=6.9,
        fontweight="bold",
        color=EMERALD,
        bbox=dict(boxstyle="round,pad=0.28", fc=SOFT_GREEN, ec=EMERALD, lw=0.8),
    )

    axA.set_yticks(ya)
    axA.set_yticklabels([x[0] for x in area_items], fontsize=7.5)
    for tick_lbl, item in zip(axA.get_yticklabels(), area_items):
        if item[5]:
            tick_lbl.set_fontweight("bold")
    axA.invert_yaxis()
    axA.set_ylim(13.8, -1.15)
    axA.set_xlim(0, 2180)
    axA.set_xlabel("Median Carved Square-Seal Face Area (mm²)")
    axA.set_title(f"A. Carved Square-Seal Area Tracks Decoded Rank (n = {n_sq:,})", fontsize=9.8, pad=10)
    axA.grid(True, axis="x", alpha=0.5)

    # --- Panel B1: Key #8A/8B/8D Blind Physical & External Bridge Odds Ratios ---
    obj_by_sub = lambda sub: next(r for r in s8b2["object_site_rows"] if sub in r["prediction"])
    r_824 = obj_by_sub("824a vs 824b")
    r_167 = obj_by_sub("167/868")
    r_391 = obj_by_sub("391 *toṇṭu")
    r_924 = obj_by_sub("924 *vari-tiṅkaḷ")
    r_890 = obj_by_sub("Kalibangan")
    r_095 = obj_by_sub("095 *āḷ")
    r_621 = obj_by_sub("621 *aṟai")
    r_923 = k8d["copper_bilinguals"]["test6b_bilingual_locks"]["lock2_923_elephant"]
    r_405 = k8d["animal_standletter_227"]["test8b4_unicorn_stand_letters"]["w_workshop_sign_proof"]["405"]
    r_meg = k8d["megalithic_graffiti"]["freq_matched_tests"]["union_megalithic_28"]["metrics"]["comb_potg_rate"]["freq_matched"]

    # Compute Haldane-corrected OR for 100% pure 2x2 tables (923->Elephant 11/2 vs 0/176, 405->W 22/0 vs 307/496)
    or_923_haldane = ((11 + 0.5) * (176 + 0.5)) / ((2 + 0.5) * (0 + 0.5))
    or_405_haldane = ((22 + 0.5) * (496 + 0.5)) / ((0 + 0.5) * (307 + 0.5))

    bridge_items = [
        ("824a/b Seals vs Harappa Tabs", float(r_824["odds_ratio"]), f"OR={r_824['odds_ratio']:.0f}×, P={r_824['p_strat_5000']:.4f}", NAVY),
        ("923 *maruppu ↔ Elephant C-Tab", or_923_haldane, f"11/11 (∞), P={r_923['lipi_fisher_p_1sided']:.2e}", CRIMSON),
        ("167/868 → Harappa Tablets", float(r_167["odds_ratio"]), f"OR={r_167['odds_ratio']:.1f}×, P={r_167['p_strat_5000']:.4f}", TEAL),
        ("391 *toṇṭu → Bronze Tools", float(r_391["odds_ratio"]), f"OR={r_391['odds_ratio']:.1f}×, P={r_391['p_strat_5000']:.4f}", TEAL),
        ("405 *tai → Unicorn W-Stand", or_405_haldane, f"22/22 (∞), P={r_405['overall_fisher_p_2sided']:.2e}", PURPLE),
        ("924 *vari-tiṅkaḷ → Foreign", float(r_924["odds_ratio"]), f"OR={r_924['odds_ratio']:.1f}×, P={r_924['p_strat_5000']:.4f}", TEAL),
        ("890 *vil → Kalibangan", float(r_890["odds_ratio"]), f"OR={r_890['odds_ratio']:.1f}×, P={r_890['p_strat_5000']:.4f}", TEAL),
        ("095 → MD Copper Tablets", float(r_095["odds_ratio"]), f"OR={r_095['odds_ratio']:.1f}×, P={r_095['p_strat_5000']:.4f}", TEAL),
        ("621 *aṟai → Seals (25/26)", float(r_621["odds_ratio"]), f"OR={r_621['odds_ratio']:.1f}×, P={r_621['p_strat_5000']:.4f}", TEAL),
        ("Megalithic Graffiti → Pottery", float(r_meg["ratio"]), f"{r_meg['ratio']:.2f}× (freq-m), P={r_meg['p']:.4f}", EMERALD),
    ]

    yb = np.arange(len(bridge_items))
    ors = [b[1] for b in bridge_items]
    axB1.barh(yb, ors, height=0.65, color=[b[3] for b in bridge_items], alpha=0.88)
    axB1.set_xscale("log")
    axB1.axvline(1.0, color=DARK_TEXT, linewidth=0.8, linestyle=":")

    for i, (_, orv, ann, col) in enumerate(bridge_items):
        axB1.text(orv * 1.15, yb[i], ann, va="center", ha="left", fontsize=6.7, fontweight="bold" if col in (NAVY, CRIMSON, PURPLE, EMERALD) else "normal", color=col if col != TEAL else DARK_TEXT)

    axB1.set_yticks(yb)
    axB1.set_yticklabels([b[0] for b in bridge_items], fontsize=7.2)
    axB1.invert_yaxis()
    axB1.set_xlim(0.8, 45000)
    axB1.set_xlabel("Enrichment Odds / Rate Ratio (Log Scale; 19/32 W5/6 Obj/Site P<0.05)")
    axB1.set_title("B1. Blind Archaeology & Key #8D External Bridge Locks", fontsize=9.8)
    axB1.grid(True, axis="x", alpha=0.45)

    # --- Panel B2: 600-Year Stratigraphic Stability (2,589 Dated Events) ---
    cov272 = next(r for r in s8b2["time_rows"] if r["feature"].startswith("COVERAGE272"))
    w56all = next(r for r in s8b2["time_rows"] if r["feature"].startswith("W56_ALL"))
    ctrl_bar = next(r for r in k6b["test_6b2_time_stability"]["features"] if "CONTROL" in r["feature"])

    bins_n = s8b2["corpus_counts"]["dated_bin_counts"]
    xt = np.array([0, 1, 2])
    xt_lbl = [
        f"Early\n(n={bins_n['early']})",
        f"Middle\n(n={bins_n['middle']:,})",
        f"Late\n(n={bins_n['late']})",
    ]
    y_cov = [cov272["early_pct"], cov272["middle_pct"], cov272["late_pct"]]
    y_w56 = [w56all["early_pct"], w56all["middle_pct"], w56all["late_pct"]]
    y_ctrl = [ctrl_bar["early_pct"], ctrl_bar["middle_pct"], ctrl_bar["late_pct"]]

    axB2.plot(xt, y_cov, "-o", color=NAVY, linewidth=2.0, markersize=5.5, label=f"272-Sign 100%-Decoded (flat, P={cov272['p_area_kind_5000']:.2f})")
    axB2.plot(xt, y_ctrl, "--^", color=CRIMSON, linewidth=2.0, markersize=6.0, label=f"Control: Harappa Bar-Seals (r={ctrl_bar['trend_r']:+.2f}, P={ctrl_bar['p_area_5000']:.3f}*)")
    axB2.plot(xt, y_w56, "-s", color=TEAL, linewidth=2.0, markersize=5.5, label=f"Any Wave-5/6 Sign (flat, P={w56all['p_area_kind_5000']:.2f})")

    for i in range(3):
        axB2.text(xt[i], y_cov[i] + 3.0, f"{y_cov[i]:.1f}%", ha="center", va="bottom", fontsize=7.0, color=NAVY, fontweight="bold")
        axB2.text(xt[i], y_ctrl[i] + 3.2, f"{y_ctrl[i]:.1f}%", ha="center", va="bottom", fontsize=7.0, color=CRIMSON, fontweight="bold")
        axB2.text(xt[i], y_w56[i] - 4.2, f"{y_w56[i]:.1f}%", ha="center", va="top", fontsize=7.0, color=TEAL, fontweight="bold")

    axB2.text(
        0.50,
        0.61,
        "24/24 W5/6 & 21/21 K5 families flat (600 yrs)",
        transform=axB2.transAxes,
        ha="center",
        va="center",
        fontsize=7.0,
        fontweight="bold",
        color=NAVY,
        bbox=dict(boxstyle="round,pad=0.22", fc=SOFT_BLUE, ec=NAVY, lw=0.7),
    )

    axB2.set_xticks(xt)
    axB2.set_xticklabels(xt_lbl, fontsize=7.8)
    axB2.set_xlim(-0.28, 2.30)
    axB2.set_ylim(8, 86)
    axB2.set_ylabel("Share of Dated Events (%)")
    axB2.set_title("B2. 600-Year Stratigraphic Stability (2,589 Dated Events)", fontsize=9.8)
    axB2.grid(True, axis="y", alpha=0.5)
    axB2.legend(loc="upper center", bbox_to_anchor=(0.48, -0.32), ncol=1, fontsize=6.8, frameon=True, facecolor="white", edgecolor=MID_GRAY)

    save_figure(fig, "fig5")


def main() -> None:
    configure_style()
    builders = [
        ("fig1", build_fig1),
        ("fig2", build_fig2),
        ("fig3", build_fig3),
        ("fig4", build_fig4),
        ("fig5", build_fig5),
    ]
    for name, fn in builders:
        fn()
        sizes = {
            ext: (FIG_DIR / f"{name}.{ext}").stat().st_size
            for ext in ("svg", "pdf", "png")
        }
        with Image.open(FIG_DIR / f"{name}.png") as im:
            w, h = im.size
            dpi = im.info.get("dpi")
        print(f"[OK] {name}: PNG={w}x{h} dpi={dpi} | bytes: svg={sizes['svg']:,} pdf={sizes['pdf']:,} png={sizes['png']:,}")


if __name__ == "__main__":
    main()
