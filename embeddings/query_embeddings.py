#!/usr/bin/env python3
"""embeddings/query_embeddings.py — query the multimodal vector layer (cosine NN).

Loads embeddings/store_*.parquet (built by build_embeddings.py) and supports:
  - nearest-neighbors of an item:   --nn "img:research/data/brahmi/..."  [-k 8]
  - text search over docs/signs:     --text-search "terminal tail formula"
  - cross-modal text->image (CLIP):  --clip-search "fish sign"   (needs CLIP-text embeddings)

item_id conventions: doc:<file>, wit:<witness_id>, sign:<sign_uid>, img:<repo-rel path>.
Brute-force cosine over normalized vectors (instant at this corpus's scale).
"""
import argparse, sys
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]


def load():
    files = sorted((ROOT / "embeddings").glob("store_*.parquet"))
    if not files:
        sys.exit("no embeddings found — run build_embeddings.py first")
    rows = []
    for f in files:
        rows += pq.read_table(f).to_pylist()
    V = np.asarray([r["vector"] for r in rows], dtype="float32")
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    return rows, V


def neighbors(qv, V, rows, k=8, modality=None, exclude=None):
    qv = qv / (np.linalg.norm(qv) + 1e-9)
    sims = V @ qv
    out = []
    for i in np.argsort(-sims):
        if exclude is not None and i == exclude:
            continue
        if modality and rows[i]["modality"] != modality:
            continue
        out.append((rows[i], float(sims[i])))
        if len(out) >= k:
            break
    return out


def embed_query(text, model_name="BAAI/bge-small-en-v1.5"):
    from fastembed import TextEmbedding
    return next(iter(TextEmbedding(model_name=model_name).embed([text])))


def show(results):
    for r, s in results:
        label = (r.get("label") or "")[:48]
        src = (r.get("source_path") or "")[:58]
        print(f"  {s:.3f}  {r['modality']:6} {r['item_type']:14} {label:48} {src}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nn", help="item_id to find neighbors of")
    ap.add_argument("--text-search", help="semantic search over text items (BGE)")
    ap.add_argument("--clip-search", help="cross-modal: text query -> images (needs CLIP-text store)")
    ap.add_argument("-k", type=int, default=8)
    args = ap.parse_args()
    rows, V = load()
    idx = {r["item_id"]: i for i, r in enumerate(rows)}

    if args.nn:
        i = idx.get(args.nn)
        if i is None:
            sys.exit(f"item_id not found: {args.nn}")
        print(f"neighbors of {args.nn}:")
        show(neighbors(V[i], V, rows, args.k, exclude=i))
    elif args.text_search:
        print(f"text search: {args.text_search!r}")
        show(neighbors(embed_query(args.text_search), V, rows, args.k, modality="text"))
    elif args.clip_search:
        print(f"cross-modal search: {args.clip_search!r}")
        qv = embed_query(args.clip_search, model_name="Qdrant/clip-ViT-B-32-text")
        show(neighbors(qv, V, rows, args.k, modality="image"))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
