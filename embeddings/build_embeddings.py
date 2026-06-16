#!/usr/bin/env python3
"""embeddings/build_embeddings.py — multimodal embedding builder (CPU, ONNX via fastembed).

Builds a vector layer over the IVC corpus:
  - image  : CLIP embeddings of sign crops (Brahmi letter images, source-token crops, Indus components)
  - text   : BGE embeddings of research docs + sign sequences + sign descriptions

Stores to embeddings/store_<run>.parquet (one row per item; vector as a list<float32> column),
joinable back to db/ivc.sqlite via item_id. No torch; models are pinned and run offline
after first download, so embeddings are reproducible (deterministic given model + input).

GUARDRAIL: embeddings are a candidate-generation / search layer, NOT evidence. Visual
similarity != sign identity. Every surfaced match must still clear source-image validation,
forger nulls, and skeptic review. See embeddings/README.md.

Usage:
  py embeddings/build_embeddings.py --what text                # docs + sign-seqs + signs (fast)
  py embeddings/build_embeddings.py --what images --limit 800  # sign crops (pilot cap)
  py embeddings/build_embeddings.py --what images              # all configured crops
"""
import argparse, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "ivc.sqlite"
TEXT_MODEL = "BAAI/bge-small-en-v1.5"          # 384-d
IMAGE_MODEL = "Qdrant/clip-ViT-B-32-vision"    # 512-d (CLIP)
IMAGE_DIRS = [
    "research/data/brahmi/indoskript_letter_images",
    "research/data/brahmi/indoskript_letter_images_v2",
    "research/data/brahmi/source_token_crops_v2",
]
IMAGE_GLOBS = ["evidence/**/*component*.png"]   # Indus component crops
IMG_EXT = {".png", ".jpg", ".jpeg"}


def inventory_text(limit=None):
    items = []
    docs = ROOT / "research" / "docs"
    for p in sorted(docs.glob("*.md")):
        items.append(dict(item_id="doc:" + p.name, item_type="doc", modality="text", label=p.stem,
                          source_path=str(p.relative_to(ROOT)).replace("\\", "/"),
                          text=p.read_text(encoding="utf-8", errors="ignore")[:8000]))
    if DB.exists():
        con = sqlite3.connect(DB)
        for wid, aid, seq in con.execute(
                "SELECT witness_id,artifact_id,sign_sequence FROM witness "
                "WHERE sign_sequence IS NOT NULL AND sign_sequence<>''"):
            items.append(dict(item_id="wit:" + str(wid), item_type="sign_sequence", modality="text",
                              label=str(aid or ""), source_path="", text=str(seq)))
        for uid, norm, desc in con.execute("SELECT sign_uid,normalized_id,description FROM sign"):
            items.append(dict(item_id="sign:" + str(uid), item_type="sign", modality="text",
                              label=str(norm or ""), source_path="", text=str(desc or norm or uid)))
        con.close()
    return items[:limit] if limit else items


def inventory_images(limit=None):
    cand = set()
    for d in IMAGE_DIRS:
        base = ROOT / d
        if base.exists():
            cand |= {p for p in base.rglob("*") if p.suffix.lower() in IMG_EXT}
    for g in IMAGE_GLOBS:
        cand |= {p for p in ROOT.glob(g) if p.suffix.lower() in IMG_EXT}
    items = []
    for p in sorted(cand):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        items.append(dict(item_id="img:" + rel, item_type="sign_crop", modality="image",
                          label=p.stem, source_path=rel, abspath=str(p)))
    return items[:limit] if limit else items


def write_store(rows, out):
    import numpy as np, pyarrow as pa, pyarrow.parquet as pq
    tbl = pa.table({
        "item_id":   [r["item_id"] for r in rows],
        "item_type": [r["item_type"] for r in rows],
        "modality":  [r["modality"] for r in rows],
        "model":     [r["model"] for r in rows],
        "label":     [r.get("label") for r in rows],
        "source_path": [r.get("source_path") for r in rows],
        "dim":       [len(r["vector"]) for r in rows],
        "vector":    pa.array([np.asarray(r["vector"], dtype="float32").tolist() for r in rows],
                              type=pa.list_(pa.float32())),
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(tbl, out)
    print(f"wrote {len(rows)} embeddings -> {out.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=["text", "images", "all"], default="text")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    if args.what in ("text", "all"):
        items = inventory_text(args.limit)
        print(f"text items: {len(items)} (docs/sign-seqs/signs)")
        from fastembed import TextEmbedding
        model = TextEmbedding(model_name=TEXT_MODEL)
        vecs = model.embed([it["text"] for it in items], batch_size=64)
        rows = [{**it, "model": TEXT_MODEL, "vector": v} for it, v in zip(items, vecs)]
        write_store(rows, ROOT / "embeddings" / "store_text.parquet")

    if args.what in ("images", "all"):
        items = inventory_images(args.limit)
        print(f"image items: {len(items)} (sign crops)")
        from fastembed import ImageEmbedding
        model = ImageEmbedding(model_name=IMAGE_MODEL)
        vecs = model.embed([it["abspath"] for it in items])
        rows = [{**it, "model": IMAGE_MODEL, "vector": v} for it, v in zip(items, vecs)]
        write_store(rows, ROOT / "embeddings" / "store_images.parquet")


if __name__ == "__main__":
    main()
