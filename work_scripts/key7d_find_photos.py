#!/usr/bin/env python3
"""key7d_find_photos.py — Key #7D: Locate cleanest high-resolution photographs for
the 14 top unsolved holdout signs & cluster heads, generate labeled contact sheets
paired with Mahadevan 1977 drawn glyphs, and audit the Dholavira Signboard across
all local catalogues and excavation photographs.

Targets (14 signs):
  692, 585, 527, 388, 455, 384, 070, 501, 095, 645, 297, 824, 621, 611

Outputs:
  work_data/key7d/selected_photos.csv
  work_data/key7d/sheet_<sign>.png  (14 high-resolution contact sheets)
  work_data/key7d/dholavira_signboard_audit.json
  work_data/key7d/sheet_dholavira_signboard.png
"""

import csv
import json
import os
import re
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(
    ROOT,
    "evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images",
)
MAP_PATH = os.path.join(
    ROOT,
    "evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/src/assets/data/seal_id_and_image_mapping.json",
)
RAW_LIPI_PATH = os.path.join(ROOT, "evidence/tmp/lipi_current_inscriptions_20260526.csv")
OBJ_LIPI_PATH = os.path.join(ROOT, "work_data/sem/objects_lipi.csv")
SIGN_SHAPES_PATH = os.path.join(ROOT, "work_data/sign_shapes.csv")
CROSSWALK_PATH = os.path.join(ROOT, "work_data/lipi_mahadevan_crosswalk.csv")
ANATOMY_PATH = os.path.join(ROOT, "work_data/key6a/anatomy_wave4.csv")
LEXICON_PATH = os.path.join(ROOT, "work_data/key6a/master_lexicon_after_key6a.csv")
MAH_PARSED_PATH = os.path.join(ROOT, "work_data/mahadevan_parsed.csv")
MAH_GLYPH_DIR = os.path.join(ROOT, "work_data/mahadevan_glyphs")
DHOL_PDF_PATH = os.path.join(ROOT, "evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.pdf")
DHOL_TXT_PATH = os.path.join(ROOT, "evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.txt")

OUT_DIR = os.path.join(ROOT, "work_data/key7d")
os.makedirs(OUT_DIR, exist_ok=True)

TARGETS = [
    "692", "585", "527", "388", "455", "384", "070",
    "501", "095", "645", "297", "824", "621", "611",
]

FACE_LETTERS = {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e"}


def load_font(size=14, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def parse_raw_text(text_str, direction):
    """Return (visual_L2R_tokens, reading_order_tokens).
    In raw Lipi CSV, `text` is stored visually left-to-right (for the impression / readable face).
    When dir. == 'R/L', standard reading order reverses the list.
    """
    cleaned = str(text_str).strip()
    cleaned = re.sub(r"^[+\]\[]+|[+\]\[]+$", "", cleaned)
    raw_toks = [t.strip() for t in cleaned.split("-") if t.strip() and t.strip().isdigit()]
    if str(direction).strip() == "R/L":
        read_toks = raw_toks[::-1]
    else:
        read_toks = raw_toks[:]
    return raw_toks, read_toks


def pick_best_image(cisi_files, face_num="1"):
    """Pick the cleanest, highest-res photo matching the face letter (default A/a for .1).
    Prefer main face impression (`_a` or `_A`), or `_a_bis`/`_A_bis` if higher res; avoid `_B`/`_C` when face_num=='1'.
    Returns (best_filename, width, height, filesize, all_matching_face_files).
    """
    letter = FACE_LETTERS.get(str(face_num), "a")
    scored = []
    for fn in cisi_files:
        fp = os.path.join(IMG_DIR, fn)
        if not os.path.exists(fp):
            continue
        try:
            with Image.open(fp) as im:
                w, h = im.size
        except Exception:
            continue
        fsize = os.path.getsize(fp)
        low = fn.lower()
        # Check face letter match: e.g., _a.jpg, _a_bis.jpg, _a_100_.jpg
        m_face = re.search(rf"_{letter}(?:[._]|$)", low)
        is_bis = "_bis" in low
        is_exact_letter = bool(m_face)
        # Penalize back/side views if face 1
        is_other_face = bool(re.search(r"_[bcdef](?:[._]|$)", low)) and letter == "a"
        # Prefer standard impression (not bis, unless bis is much larger)
        # Actually in CISI, _a is often the seal stone (mirrored) and _A is the impression, OR _a is impression and _a_bis is seal!
        # Prefer larger pixel area among exact face matches.
        score = (
            (100 if is_exact_letter else (0 if is_other_face else 40))
            + (10 if not is_bis else 8)
            + min(w * h / 50000.0, 20.0)
        )
        scored.append((score, w * h, fsize, w, h, fn, is_exact_letter))
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    best = scored[0]
    same_face = [x[5] for x in scored if x[6]]
    return best[5], best[3], best[4], best[2], same_face


def score_candidate_row(row, target_sign):
    """Score a raw Lipi row for photo inspection quality."""
    read_toks = row["read_toks"]
    n = len(read_toks)
    typ = row["type"]
    cond = row["condition"]
    comp = row["complete"]
    has_000 = "000" in read_toks

    s = 0.0
    if comp == "Y" and not has_000:
        s += 100.0
    elif not has_000:
        s += 40.0

    # Prefer square seals, then rectangular seals, then tablets
    if typ == "SEAL:S":
        s += 50.0
    elif typ == "SEAL:R":
        s += 38.0
    elif typ.startswith("SEAL"):
        s += 30.0
    elif typ in ("TAB:B", "TAB:I", "TAB:C"):
        s += 20.0
    else:
        s += 10.0

    # Prefer short 2-5 sign texts where the target sign is unmistakable
    if 2 <= n <= 5:
        s += 35.0
    elif n == 6:
        s += 25.0
    elif n == 7:
        s += 18.0
    elif n == 1:
        s += 22.0
    else:
        s += max(5.0, 20.0 - n)

    if cond == "Good":
        s += 15.0
    elif cond == "Fair":
        s += 7.0

    # Resolution bonus
    area = row["img_w"] * row["img_h"]
    s += min(area / 40000.0, 25.0)

    # Prefer face .1 so _A/_a mapping is unambiguous
    if str(row["id"]).endswith(".1"):
        s += 12.0

    # Slight bonus if target occurs cleanly once
    if read_toks.count(target_sign) == 1:
        s += 3.0

    return s


def make_contact_sheet(sign, meta_info, picked_rows, out_path):
    """Build a crisp, labeled contact sheet:
    Left column: Mahadevan 1977 drawn glyph(s) + Lipi/Wells shape_desc + Key #6A context.
    Right columns: up to 4 real photographs from seal_images/, with both full image and
    top-band zoom (for square seals) plus clear sequence labels in visual L->R and reading order.
    """
    n_imgs = len(picked_rows)
    left_w = 340
    cell_w = 400
    pad = 16
    header_h = 66
    # Show full image (max 340px tall) + zoomed top inscription strip (130px tall) for seals
    body_h = 600
    total_w = left_w + pad + n_imgs * (cell_w + pad)
    total_h = header_h + body_h + pad

    canvas = Image.new("RGB", (total_w, total_h), (250, 250, 248))
    dr = ImageDraw.Draw(canvas)
    f_title = load_font(20, bold=True)
    f_bold = load_font(13, bold=True)
    f_reg = load_font(12, bold=False)
    f_sm = load_font(11, bold=False)

    # Header bar
    dr.rectangle([0, 0, total_w, header_h], fill=(30, 42, 58))
    m77_str = meta_info.get("m77_str", "?")
    parp_str = meta_info.get("parpola", "")
    tot_str = meta_info.get("intact_total", "?")
    title = f"Key #7D Photo Audit — Lipi Sign {sign}  |  {m77_str}  {parp_str}  |  Intact tokens: {tot_str}"
    dr.text((16, 10), title, fill=(255, 255, 255), font=f_title)
    sub = f"Lipi/Wells shape_desc: {meta_info.get('shape_desc') or '[MISSING]'}"
    dr.text((16, 38), sub[:160], fill=(215, 230, 245), font=f_reg)

    # Left panel: Mahadevan drawn glyph(s) + metadata
    lx, ly = 12, header_h + 12
    dr.rectangle([lx, ly, left_w - 6, total_h - pad], fill=(255, 255, 255), outline=(190, 195, 205))
    cur_y = ly + 10
    dr.text((lx + 10, cur_y), "Mahadevan 1977 Drawn Glyph(s):", fill=(20, 30, 50), font=f_bold)
    cur_y += 22

    mah_nums = meta_info.get("mah_nums", [])
    gx = lx + 12
    max_gh = 0
    for mn, share in mah_nums[:3]:
        gpath = os.path.join(MAH_GLYPH_DIR, f"{mn}.png")
        if os.path.exists(gpath):
            try:
                gim = Image.open(gpath).convert("RGBA")
                bg = Image.new("RGB", gim.size, (255, 255, 255))
                bg.paste(gim, mask=gim.split()[3] if len(gim.split()) == 4 else None)
                bg.thumbnail((92, 92))
                canvas.paste(bg, (gx, cur_y))
                dr.rectangle([gx - 1, cur_y - 1, gx + bg.width, cur_y + bg.height], outline=(160, 165, 175))
                dr.text((gx, cur_y + bg.height + 3), f"M{mn} ({share})", fill=(40, 40, 40), font=f_sm)
                gx += 102
                max_gh = max(max_gh, bg.height + 20)
            except Exception:
                pass
    cur_y += max(max_gh, 25) + 12

    # Wrap metadata lines in left panel
    info_lines = [
        ("Key #6A Gloss:", meta_info.get("soundfree_gloss", "") or "-"),
        ("Top Anchor:", meta_info.get("top_anchor", "") or "-"),
        ("Top Left (140):", meta_info.get("top_140_L", "") or "-"),
        ("Top Right (140):", meta_info.get("top_140_R", "") or "-"),
        ("Positions:", f"init={meta_info.get('init_pct','?')}% med={meta_info.get('med_pct','?')}% fin={meta_info.get('fin_pct','?')}%"),
        ("Top Sites:", meta_info.get("top_sites_L", "") or "-"),
        ("Top Kinds:", meta_info.get("top_kinds_L", "") or "-"),
        ("4D Cluster:", meta_info.get("key4d_cluster", "") or "-"),
    ]
    for k, v in info_lines:
        dr.text((lx + 10, cur_y), k, fill=(25, 60, 110), font=f_bold)
        cur_y += 16
        # wrap text
        words = str(v).split()
        line = ""
        for w in words:
            if len(line) + len(w) + 1 > 42:
                dr.text((lx + 14, cur_y), line, fill=(35, 35, 35), font=f_sm)
                cur_y += 14
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            dr.text((lx + 14, cur_y), line, fill=(35, 35, 35), font=f_sm)
            cur_y += 16
        cur_y += 4
        if cur_y > total_h - 30:
            break

    # Right panels: real photographs
    for idx, r in enumerate(picked_rows):
        cx = left_w + pad + idx * (cell_w + pad)
        cy = header_h + 12
        dr.rectangle([cx, cy, cx + cell_w, total_h - pad], fill=(255, 255, 255), outline=(180, 185, 195))

        # Photo caption header
        cisi = r["cisi"]
        fn = r["img_file"]
        site = r["site"]
        typ = r["type"]
        direction = r["dir."]
        vis_seq = "-".join(r["vis_toks"])
        read_seq = "-".join(r["read_toks"])
        # Mark target position(s) in visual L->R sequence (1-indexed from left)
        vis_pos = [i + 1 for i, t in enumerate(r["vis_toks"]) if t == sign]
        read_pos = [i + 1 for i, t in enumerate(r["read_toks"]) if t == sign]

        dr.text((cx + 8, cy + 6), f"#{idx+1}  {cisi} ({site}, {typ}) — {fn}", fill=(15, 35, 70), font=f_bold)
        dr.text((cx + 8, cy + 23), f"Read ({direction}): {read_seq}  [pos {read_pos}]", fill=(160, 25, 25), font=f_sm)
        dr.text((cx + 8, cy + 38), f"Raw L->R: {vis_seq}  [L->R pos {vis_pos}]", fill=(50, 50, 50), font=f_sm)
        dr.text((cx + 8, cy + 52), f"Res: {r['img_w']}x{r['img_h']} | Cond: {r['condition']} | Sym: {r['symbol']}", fill=(90, 90, 90), font=f_sm)

        fp = os.path.join(IMG_DIR, fn)
        im = Image.open(fp).convert("RGB")
        # Paste full image neatly
        full_box_h = 340 if typ == "SEAL:S" else 460
        im_full = im.copy()
        im_full.thumbnail((cell_w - 16, full_box_h))
        px = cx + (cell_w - im_full.width) // 2
        py = cy + 72
        canvas.paste(im_full, (px, py))

        # For square seals, also add an enlarged crop of the top 38% inscription band!
        if typ == "SEAL:S":
            crop_h = int(im.height * 0.40)
            band = im.crop((0, 0, im.width, max(crop_h, 20)))
            scale = min((cell_w - 16) / band.width, 145 / band.height)
            band_z = band.resize((max(1, int(band.width * scale)), max(1, int(band.height * scale))), Image.Resampling.LANCZOS)
            by = cy + 72 + full_box_h + 10
            dr.text((cx + 8, by), "Zoomed top inscription band (note: stone may be mirrored vs impression):", fill=(140, 30, 30), font=f_sm)
            bx = cx + (cell_w - band_z.width) // 2
            canvas.paste(band_z, (bx, by + 16))
            dr.rectangle([bx - 1, by + 15, bx + band_z.width, by + 16 + band_z.height], outline=(180, 40, 40))

    canvas.save(out_path)


def audit_dholavira_signboard(raw_df, obj_df, lex_df):
    """Audit the Dholavira Signboard across all local catalogues and locked lexicon."""
    lex_map = {}
    for _, r in lex_df.iterrows():
        lex_map[str(r["sign"]).zfill(3)] = {
            "root_or_gloss": r["root_or_gloss"],
            "source_lever": r["source_lever"],
            "evidence_note": r["evidence_note"],
        }

    raw_sb = raw_df[raw_df["id"] == "144.1"].iloc[0].to_dict()
    obj_sb = obj_df[obj_df["stone_id"] == "144"].iloc[0].to_dict()

    # Check Mahadevan parsed corpus for any Dholavira entry
    mah_df = pd.read_csv(MAH_PARSED_PATH, dtype=str).fillna("")
    mah_dhol = mah_df[mah_df["site"].str.contains("Dhol|DLV", case=False, na=False)]

    # Check seal_images for Dholavira
    dhol_seal_imgs = sorted([f for f in os.listdir(IMG_DIR) if re.match(r"^(Dlv|Dhol|Dh-)", f, re.I)])

    # Check corpus directional statistics for 820 and 798 on intact Lipi faces
    intact_raw = raw_df[(raw_df["complete"] == "Y") & (~raw_df["text"].str.contains("000"))]
    pos_stats = {}
    for s in ["820", "798", "611", "388", "384", "850", "645", "031", "821"]:
        init_c = med_c = fin_c = tot_c = 0
        for _, r in intact_raw.iterrows():
            _, rt = parse_raw_text(r["text"], r["dir."])
            if s in rt:
                for i, tok in enumerate(rt):
                    if tok == s:
                        tot_c += 1
                        if len(rt) == 1:
                            pass
                        elif i == 0:
                            init_c += 1
                        elif i == len(rt) - 1:
                            fin_c += 1
                        else:
                            med_c += 1
        pos_stats[s] = {"total": tot_c, "init": init_c, "med": med_c, "fin": fin_c}

    # Sign-by-sign breakdown of Lipi 9-sign and expanded 10-sign (821 -> 820-820) sequences
    lipi_9 = ["820", "611", "388", "820", "850", "645", "031", "821", "798"]
    expanded_10 = ["820", "611", "388", "820", "850", "645", "031", "820", "820", "798"]

    breakdown = []
    for idx, s in enumerate(expanded_10, 1):
        locked = s in lex_map
        breakdown.append({
            "pos_reading_order": idx,
            "lipi_sign": s,
            "locked_key6a": locked,
            "reading": lex_map[s]["root_or_gloss"] if locked else "UNSOLVED",
            "lever": lex_map[s]["source_lever"] if locked else "-",
        })

    # Extract excavation photos from Bisht 2015 PDF if not already extracted
    pdf_img_dir = os.path.join(OUT_DIR, "dholavira_pdf_imgs")
    os.makedirs(pdf_img_dir, exist_ok=True)
    if os.path.exists(DHOL_PDF_PATH) and not os.listdir(pdf_img_dir):
        data = open(DHOL_PDF_PATH, "rb").read()
        idx = 0
        cnt = 0
        while True:
            s_i = data.find(b"\xff\xd8\xff", idx)
            if s_i == -1:
                break
            e_i = data.find(b"\xff\xd9", s_i + 3)
            if e_i == -1:
                break
            jpg = data[s_i:e_i + 2]
            if len(jpg) > 5000:
                cnt += 1
                open(os.path.join(pdf_img_dir, f"img_{cnt:03d}.jpg"), "wb").write(jpg)
            idx = e_i + 2

    # Build a clean signboard contact sheet combining img_011, img_012, img_014, img_015
    sb_imgs = [os.path.join(pdf_img_dir, fn) for fn in ["img_011.jpg", "img_012.jpg", "img_014.jpg", "img_015.jpg"]]
    if all(os.path.exists(p) for p in sb_imgs):
        W = 1000
        sheet = Image.new("RGB", (W, 920), (250, 250, 248))
        dr = ImageDraw.Draw(sheet)
        ft = load_font(18, bold=True)
        fb = load_font(13, bold=True)
        fs = load_font(12, bold=False)

        dr.rectangle([0, 0, W, 56], fill=(30, 42, 58))
        dr.text((14, 8), "Dholavira North Gate Signboard (Lipi 144.1, 300x37 cm gypsum inlay) — Excavation & Drawing Audit", fill=(255, 255, 255), font=ft)
        dr.text((14, 32), "Lipi reading order (9 signs -> 10 expanded): 820 - 611 - 388 - 820 - 850 - 645(?) - 031 - [820 - 820] - 798", fill=(220, 235, 250), font=fs)

        y = 66
        # Drawing (img_011)
        im11 = Image.open(sb_imgs[0]).convert("RGB")
        im11.thumbnail((W - 28, 150))
        dr.text((14, y), "1. Bisht 2015 Official Line Drawing (10 signs as found in situ, L->R = 1..10; note sign #6 is chevron/gable, NOT plain X!):", fill=(20, 40, 80), font=fb)
        y += 18
        sheet.paste(im11, (14, y))
        y += im11.height + 14

        # Full photo (img_012)
        im12 = Image.open(sb_imgs[1]).convert("RGB")
        im12.thumbnail((W - 28, 140))
        dr.text((14, y), "2. Full Excavation Photo of Fallen Gypsum Inlay Signboard (Bisht 2015):", fill=(20, 40, 80), font=fb)
        y += 18
        sheet.paste(im12, (14, y))
        y += im12.height + 16

        # Close-up (img_014) + In-situ angle (img_015) side by side
        dr.text((14, y), "3. Close-up of Signs 1-4 (820, 611, 388, 820) & Oblique In-Situ View (Bisht 2015):", fill=(20, 40, 80), font=fb)
        y += 20
        im14 = Image.open(sb_imgs[2]).convert("RGB")
        im14.thumbnail((540, 310))
        sheet.paste(im14, (14, y))

        im15 = Image.open(sb_imgs[3]).convert("RGB")
        im15.thumbnail((415, 310))
        sheet.paste(im15, (568, y))
        y += max(im14.height, im15.height) + 18

        # Text summary at bottom
        dr.text((14, y), "Key #6A Locked Status (10 expanded tokens = 7/10 tokens locked; 5/8 distinct signs locked if 821=820-820):", fill=(150, 25, 25), font=fb)
        y += 20
        row_txt = " | ".join([f"#{b['pos_reading_order']}:{b['lipi_sign']}({'LOCK:'+b['reading'] if b['locked_key6a'] else 'OPEN'})" for b in breakdown[:5]])
        row_txt2 = " | ".join([f"#{b['pos_reading_order']}:{b['lipi_sign']}({'LOCK:'+b['reading'] if b['locked_key6a'] else 'OPEN'})" for b in breakdown[5:]])
        dr.text((14, y), row_txt, fill=(30, 30, 30), font=fs)
        dr.text((14, y + 18), row_txt2, fill=(30, 30, 30), font=fs)

        sheet.save(os.path.join(OUT_DIR, "sheet_dholavira_signboard.png"))

    audit = {
        "lipi_raw_record": raw_sb,
        "objects_lipi_record": obj_sb,
        "mahadevan_1977_dholavira_count": len(mah_dhol),
        "seal_images_dholavira_files": dhol_seal_imgs,
        "bisht_pdf_extracted_signboard_photos": ["img_011.jpg", "img_012.jpg", "img_013.jpg", "img_014.jpg", "img_015.jpg", "img_016.jpg"],
        "lipi_9sign_reading_order": lipi_9,
        "expanded_10sign_reading_order": expanded_10,
        "key6a_locked_tokens_out_of_10": sum(1 for b in breakdown if b["locked_key6a"]),
        "key6a_locked_tokens_out_of_9_lipi": sum(1 for s in lipi_9 if s in lex_map),
        "sign_breakdown_10": breakdown,
        "corpus_positional_stats": pos_stats,
    }
    with open(os.path.join(OUT_DIR, "dholavira_signboard_audit.json"), "w") as f:
        json.dump(audit, f, indent=2)
    return audit


def main():
    img_map = json.load(open(MAP_PATH))
    raw_df = pd.read_csv(RAW_LIPI_PATH, dtype=str).fillna("")
    obj_df = pd.read_csv(OBJ_LIPI_PATH, dtype=str).fillna("")
    shapes_df = pd.read_csv(SIGN_SHAPES_PATH, dtype=str).fillna("")
    cw_df = pd.read_csv(CROSSWALK_PATH, dtype=str).fillna("")
    an_df = pd.read_csv(ANATOMY_PATH, dtype=str).fillna("")
    lex_df = pd.read_csv(LEXICON_PATH, dtype=str).fillna("")

    shape_map = dict(zip(shapes_df["lipi_wells_number"], shapes_df["shape_description"]))
    parp_map = dict(zip(shapes_df["lipi_wells_number"], shapes_df["mayig_code"]))
    an_map = {r["sign"]: r.to_dict() for _, r in an_df.iterrows()}

    # Parse tokens on raw_df
    vis_list, read_list = [], []
    for _, r in raw_df.iterrows():
        vt, rt = parse_raw_text(r["text"], r["dir."])
        vis_list.append(vt)
        read_list.append(rt)
    raw_df["vis_toks"] = vis_list
    raw_df["read_toks"] = read_list

    # Attach best photo for rows whose cisi is in img_map
    selected_rows = []
    for sign in TARGETS:
        sub = raw_df[raw_df["read_toks"].apply(lambda x: sign in x)].copy()
        sub = sub[sub["cisi"].isin(img_map)].copy()

        # Gather Mahadevan crosswalk numbers
        cw_sub = cw_df[cw_df["lipi"] == sign].sort_values("rank_for_lipi_sign")
        mah_nums = []
        for _, cr in cw_sub.head(3).iterrows():
            mah_nums.append((str(cr["mahadevan"]), f"{float(cr['share_of_lipi_sign'])*100:.0f}%"))
        m77_str = ", ".join([f"M{m} ({sh})" for m, sh in mah_nums]) if mah_nums else "M?"

        cand_list = []
        for _, r in sub.iterrows():
            face_num = str(r["id"]).split(".")[-1] if "." in str(r["id"]) else "1"
            picked_img = pick_best_image(img_map[r["cisi"]], face_num=face_num)
            if not picked_img:
                continue
            fn, w, h, fsize, same_face = picked_img
            rd = r.to_dict()
            rd["img_file"] = fn
            rd["img_w"] = w
            rd["img_h"] = h
            rd["img_bytes"] = fsize
            rd["same_face_files"] = "|".join(same_face)
            rd["score"] = score_candidate_row(rd, sign)
            cand_list.append(rd)

        cand_list.sort(key=lambda x: x["score"], reverse=True)

        # Pick top 3-4 distinct CISI objects, trying to include diversity of texts (unless single-formula like 501)
        picked = []
        seen_cisi = set()
        seen_texts = Counter()
        for c in cand_list:
            if c["cisi"] in seen_cisi:
                continue
            txt_key = "-".join(c["read_toks"])
            if len(picked) >= 1 and seen_texts[txt_key] >= 2 and len(cand_list) > 6:
                # Try to get a different text first unless we run out
                continue
            picked.append(c)
            seen_cisi.add(c["cisi"])
            seen_texts[txt_key] += 1
            if len(picked) >= 3:
                break
        # Fill up to 3 if skipped due to text diversity (e.g. 501)
        if len(picked) < 3:
            for c in cand_list:
                if c["cisi"] in seen_cisi:
                    continue
                picked.append(c)
                seen_cisi.add(c["cisi"])
                if len(picked) >= 3:
                    break

        # For 611, also grab M-56_a_bis.jpg if present so we can inspect both stone and impression!
        if sign == "611":
            extra_m56 = [c for c in cand_list if c["cisi"] == "M-56"]
            if extra_m56:
                c0 = dict(extra_m56[0])
                alt = [f for f in img_map["M-56"] if f != c0["img_file"]]
                if alt:
                    fp_alt = os.path.join(IMG_DIR, alt[0])
                    if os.path.exists(fp_alt):
                        with Image.open(fp_alt) as im:
                            aw, ah = im.size
                        c0["img_file"] = alt[0]
                        c0["img_w"], c0["img_h"] = aw, ah
                        c0["img_bytes"] = os.path.getsize(fp_alt)
                        picked.append(c0)

        ar = an_map.get(sign, {})
        meta_info = {
            "m77_str": m77_str,
            "mah_nums": mah_nums,
            "parpola": ar.get("parpola") or parp_map.get(sign, ""),
            "intact_total": ar.get("intact_total", str(len(raw_df[raw_df["read_toks"].apply(lambda x: sign in x)]))),
            "shape_desc": shape_map.get(sign, ar.get("shape_desc", "")),
            "soundfree_gloss": ar.get("soundfree_gloss", ""),
            "top_anchor": ar.get("top_anchor", ""),
            "top_140_L": ar.get("top_140_L", ""),
            "top_140_R": ar.get("top_140_R", ""),
            "init_pct": ar.get("init_pct", "?"),
            "med_pct": ar.get("med_pct", "?"),
            "fin_pct": ar.get("fin_pct", "?"),
            "top_sites_L": ar.get("top_sites_L", ""),
            "top_kinds_L": ar.get("top_kinds_L", ""),
            "key4d_cluster": ar.get("key4d_cluster", ""),
        }

        sheet_path = os.path.join(OUT_DIR, f"sheet_{sign}.png")
        make_contact_sheet(sign, meta_info, picked, sheet_path)

        print(f"Sign {sign} ({m77_str}): {len(cand_list)} photo candidates -> picked {len(picked)} -> {os.path.basename(sheet_path)}")
        for rank, p in enumerate(picked, 1):
            print(f"   #{rank} {p['cisi']:8s} ({p['site']:12s}, {p['type']:6s}, {p['img_w']}x{p['img_h']}) {p['img_file']:20s} | Read({p['dir.']}): {'-'.join(p['read_toks'])}")
            selected_rows.append({
                "target_sign": sign,
                "rank": rank,
                "lipi_id": p["id"],
                "cisi": p["cisi"],
                "site": p["site"],
                "type": p["type"],
                "condition": p["condition"],
                "complete": p["complete"],
                "symbol": p["symbol"],
                "dir": p["dir."],
                "reading_order_seq": "-".join(p["read_toks"]),
                "raw_L2R_seq": "-".join(p["vis_toks"]),
                "img_file": p["img_file"],
                "img_rel_path": f"seal_images/{p['img_file']}",
                "img_w": p["img_w"],
                "img_h": p["img_h"],
                "m77_crosswalk": m77_str,
                "existing_shape_desc": meta_info["shape_desc"],
                "contact_sheet": f"work_data/key7d/sheet_{sign}.png",
            })

    sel_df = pd.DataFrame(selected_rows)
    sel_df.to_csv(os.path.join(OUT_DIR, "selected_photos.csv"), index=False)

    audit = audit_dholavira_signboard(raw_df, obj_df, lex_df)
    print("\n=== DHOLAVIRA SIGNBOARD AUDIT ===")
    print("Lipi 144.1 raw text:", audit["lipi_raw_record"]["text"], "dir:", audit["lipi_raw_record"]["dir."])
    print("Lipi 9-sign reading order:", "-".join(audit["lipi_9sign_reading_order"]))
    print("Expanded 10-sign reading order:", "-".join(audit["expanded_10sign_reading_order"]))
    print(f"Locked by Key #6A: {audit['key6a_locked_tokens_out_of_10']}/10 expanded tokens ({audit['key6a_locked_tokens_out_of_9_lipi']}/9 Lipi tokens)")
    for b in audit["sign_breakdown_10"]:
        print(f"   Pos {b['pos_reading_order']:2d}: {b['lipi_sign']} -> {b['reading']} ({b['lever']})")


if __name__ == "__main__":
    main()
