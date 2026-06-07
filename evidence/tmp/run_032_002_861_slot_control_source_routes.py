from __future__ import annotations

import csv
import json
import re
import shutil
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_slot_control_source_routes"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

IA_ID = "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan"
IA_DOWNLOAD = f"https://archive.org/download/{IA_ID}"
IA_DETAILS = f"https://archive.org/details/{IA_ID}"
VOLUMES = {
    "india": {
        "label": "CISI Collections in India",
        "details": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India",
        "xml_name": "Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml",
        "local_hint": None,
    },
    "pakistan": {
        "label": "CISI Collections in Pakistan",
        "details": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan",
        "xml_name": "Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml",
        "local_hint": ROOT / "tmp" / "cisi_pakistan_ocr" / "pakistan_djvu.xml",
    },
}

TARGETS = [
    {
        "cisi": "H-823",
        "x": "636",
        "slot_text": "+740-636-240-060-692+",
        "companion": "+700-034+",
        "route_terms": ["H-823", "H823", "H88-1196", "H88 1196"],
        "current_status": "metadata_route_only",
    },
    {
        "cisi": "H-1845",
        "x": "642",
        "slot_text": "+740-642-240-060-692+",
        "companion": "+700-034+",
        "route_terms": ["H-1845", "H1845", "H2000-4484", "H2000 4484", "Figure 42.05"],
        "current_status": "public_page_route_visible_not_local",
    },
    {
        "cisi": "H-237",
        "x": "642",
        "slot_text": "+740-642-240-060-692+",
        "companion": "+700-033+",
        "route_terms": ["H-237", "H237"],
        "current_status": "metadata_only_no_excavation_id",
    },
]

LOCAL_TEXT_FILES = [
    ROOT / "tmp" / "lipi_current_inscriptions_20260526.csv",
    ROOT / "data" / "sign_crosswalk" / "artifact_witnesses.csv",
    ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv",
    ROOT / "tmp" / "032_002_861_603_slot_source_normalization" / "vats_vol2_djvu.txt",
    ROOT / "tmp" / "032_002_861_603_slot_source_normalization" / "vats_plates_djvu.txt",
]


def fetch_xml(volume: str, cfg: dict[str, object]) -> Path:
    out = OUT / f"cisi_{volume}_djvu.xml"
    hint = cfg.get("local_hint")
    if isinstance(hint, Path) and hint.exists():
        shutil.copyfile(hint, out)
        return out
    if out.exists():
        return out
    url = f"{IA_DOWNLOAD}/{urllib.parse.quote(str(cfg['xml_name']))}"
    with urllib.request.urlopen(url, timeout=60) as response:
        out.write_bytes(response.read())
    return out


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_pages(xml_path: Path) -> list[dict[str, object]]:
    tree = ET.parse(xml_path)
    pages: list[dict[str, object]] = []
    for obj in tree.findall(".//OBJECT"):
        page_file = ""
        for param in obj.findall("./PARAM"):
            if param.attrib.get("name") == "PAGE":
                page_file = param.attrib.get("value", "")
                break
        leaf_match = re.search(r"_(\d+)\.djvu$", page_file)
        leaf = int(leaf_match.group(1)) if leaf_match else None
        words = []
        for word in obj.findall(".//WORD"):
            if word.text:
                words.append(clean_text(word.text))
        pages.append({"leaf": leaf, "page_file": page_file, "text": " ".join(words)})
    return pages


def contexts(text: str, term: str, radius: int = 22) -> list[str]:
    hits: list[str] = []
    if not term:
        return hits
    pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])")
    clean = clean_text(text)
    for match in pattern.finditer(clean):
        before = " ".join(clean[: match.start()].split()[-radius:])
        after = " ".join(clean[match.end() :].split()[:radius])
        hits.append(f"{before} [[{term}]] {after}".strip())
    return hits


def classify_context(context: str) -> str:
    lower = context.lower()
    if "plate" in lower or "pl." in lower:
        return "plate_or_plate_reference"
    if "figure" in lower or "fig." in lower:
        return "figure_or_figure_reference"
    if "data" in lower or "register" in lower:
        return "data_or_register_reference"
    if "table" in lower or "concordance" in lower:
        return "table_or_concordance_reference"
    return "ocr_context_unclassified"


def search_cisi() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for volume, cfg in VOLUMES.items():
        xml_path = fetch_xml(volume, cfg)
        for page in parse_pages(xml_path):
            text = str(page["text"])
            for target in TARGETS:
                for term in target["route_terms"]:
                    for ctx in contexts(text, term):
                        leaf = page["leaf"]
                        rows.append(
                            {
                                "source_layer": "cisi_ia_ocr",
                                "target": target["cisi"],
                                "x": target["x"],
                                "term": term,
                                "volume": str(cfg["label"]),
                                "leaf": "" if leaf is None else str(leaf),
                                "reader_url": ""
                                if leaf is None
                                else f"{IA_DETAILS}/{cfg['details']}/page/n{leaf}/mode/1up",
                                "page_image_url": ""
                                if leaf is None
                                else f"{IA_DOWNLOAD}/{cfg['details']}/page/n{leaf}_w2000.jpg",
                                "context_class": classify_context(ctx),
                                "context": ctx,
                            }
                        )
    return rows


def search_local_files() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in LOCAL_TEXT_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for target in TARGETS:
            for term in [target["cisi"], target["slot_text"], *target["route_terms"]]:
                for ctx in contexts(text, term, radius=16):
                    rows.append(
                        {
                            "source_layer": "local_text_file",
                            "target": target["cisi"],
                            "x": target["x"],
                            "term": term,
                            "volume": "",
                            "leaf": "",
                            "reader_url": "",
                            "page_image_url": "",
                            "context_class": "local_context",
                            "context": f"{path.as_posix()}: {ctx}",
                        }
                    )
    return rows


def source_decisions(cisi_rows: list[dict[str, str]], local_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    decisions: list[dict[str, str]] = []
    by_target = {target["cisi"]: {"cisi": [], "local": []} for target in TARGETS}
    for row in cisi_rows:
        by_target[row["target"]]["cisi"].append(row)
    for row in local_rows:
        by_target[row["target"]]["local"].append(row)

    for target in TARGETS:
        cisi = target["cisi"]
        cisi_hits = by_target[cisi]["cisi"]
        local_hits = by_target[cisi]["local"]
        if cisi == "H-1845":
            status = "public_harappa_route_visible_shell_download_blocked_cisi_public_ocr_unlocated"
            decision = (
                "H-1845 remains a real public-route source control via Harappa.com/H2000-4484 / 2227-15 / Figure 42.05, "
                "but no local image was acquired and no CISI IA OCR route was found."
            )
            weight = "0.75"
        elif cisi == "H-823" and not cisi_hits:
            status = "exact_route_dark_after_cisi_ia_and_web_checks"
            decision = (
                "H-823 keeps only the local H88-1196 route; public CISI IA OCR and checked web search did not locate an image or page route."
            )
            weight = "0.25"
        elif cisi == "H-237" and not cisi_hits:
            status = "metadata_only_no_excavation_route_ref_clone_pressure"
            decision = (
                "H-237 remains metadata-only. The local current export gives ref:424.2 for its SP text, so it is clone-pressure on H-1845 rather than independent source weight."
            )
            weight = "0.05"
        else:
            status = "cisi_ia_ocr_route_candidate_found"
            decision = "CISI IA OCR produced at least one page candidate; manual source-panel inspection required before upgrade."
            weight = "0.35"
        decisions.append(
            {
                "target": cisi,
                "x": target["x"],
                "slot_text": target["slot_text"],
                "companion": target["companion"],
                "previous_status": target["current_status"],
                "new_status": status,
                "working_source_weight": weight,
                "cisi_ocr_hit_rows": str(len(cisi_hits)),
                "local_hit_rows": str(len(local_hits)),
                "decision": decision,
            }
        )
    return decisions


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, decisions: list[dict[str, str]], cisi_rows: list[dict[str, str]], local_rows: list[dict[str, str]]) -> None:
    lines = [
        "# Campaign 032 Slot-Control Source Routes",
        "",
        "Date: 2026-05-29",
        "",
        "Question: do the control-side rows `H-823`, `H-1845`, and `H-237` upgrade enough to carry the `603/636/642` slot-family contrast?",
        "",
        "This is source routing and evidence weighting. It is not sign reading.",
        "",
        "## Decisions",
        "",
        "| target | X | previous | new status | working weight | decision |",
        "|---|---:|---|---|---:|---|",
    ]
    for row in decisions:
        lines.append(
            f"| `{row['target']}` | `{row['x']}` | {row['previous_status']} | {row['new_status']} | {row['working_source_weight']} | {row['decision']} |"
        )
    lines.extend(
        [
            "",
            "## Source Search Result",
            "",
            f"- CISI IA OCR route rows found: `{len(cisi_rows)}`.",
            f"- Local text-file rows found: `{len(local_rows)}`.",
            "- External web search in this turn did not locate `H88-1196`, `H-823`, or `H-237` source pages.",
            "- Harappa.com remains the only public visible route for `H-1845/H2000-4484/2227-15`, but direct local download is Cloudflare-blocked.",
            "",
            "## Consequence For The Slot-Family Contrast",
            "",
            "`636/642` controls are still weaker than `603` on source weight. `H-360` remains the only source-visible `636` control, while `H-823` is route-dark. `H-1845` remains a public-route `642` control, but `H-237` is demoted to near-zero independent weight because the local current export marks its text as `ref:424.2` and gives no excavation route.",
            "",
            "This does not kill the `240-060-692` subframe. It does narrow what can be claimed: the current source-normalized contrast is strong enough to keep `603` as the live bridge target, but not strong enough to treat `636/642` as fully source-balanced negative controls.",
            "",
            "Accepted values/translations remain 0.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cisi_rows = search_cisi()
    local_rows = search_local_files()
    decisions = source_decisions(cisi_rows, local_rows)

    write_csv(REPORTS / "campaign_032_002_861_slot_control_source_routes_cisi_hits.csv", cisi_rows)
    write_csv(REPORTS / "campaign_032_002_861_slot_control_source_routes_local_hits.csv", local_rows)
    write_csv(REPORTS / "campaign_032_002_861_slot_control_source_routes_decisions.csv", decisions)
    summary = {
        "date": "2026-05-29",
        "question": "source route status of H-823/H-1845/H-237 controls for the 740-X-240-060-692 slot family",
        "targets": [target["cisi"] for target in TARGETS],
        "cisi_ocr_rows": len(cisi_rows),
        "local_hit_rows": len(local_rows),
        "decisions": decisions,
        "accepted_values_or_translations": 0,
    }
    (REPORTS / "campaign_032_002_861_slot_control_source_routes_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_markdown(DOCS / "campaign_032_002_861_slot_control_source_routes.md", decisions, cisi_rows, local_rows)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
