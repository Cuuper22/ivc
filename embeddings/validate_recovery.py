#!/usr/bin/env python3
"""embeddings/validate_recovery.py — the ethos gate for image embeddings.

Tests whether image-embedding nearest-neighbors recover SAME-LABEL crops better than
a shuffled-label null. This is the falsifiable question that decides whether the
embeddings capture glyph identity *at all* before anything is built on them — and it
can come back negative. Visual similarity is NOT sign identity; a positive result here
is necessary, not sufficient (source-image validation + forger nulls still apply).

Labels come from the Brahmi neighbor table (brahmi_local_image_path -> brahmi_label),
which is the cleanest ground truth available. Reports recovery@k vs null.

  py embeddings/validate_recovery.py [-k 5]
"""
import argparse, csv, sys
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
BRAHMI_CSV = ROOT / "research/data/brahmi/source_token_brahmi_neighbors_v2.csv"


def load_images():
    f = ROOT / "embeddings" / "store_images.parquet"
    if not f.exists():
        sys.exit("no image embeddings — run: build_embeddings.py --what images")
    rows = pq.read_table(f).to_pylist()
    V = np.asarray([r["vector"] for r in rows], dtype="float32")
    V /= (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    return rows, V


def label_map():
    m = {}
    if BRAHMI_CSV.exists():
        with open(BRAHMI_CSV, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                p = (row.get("brahmi_local_image_path") or "").replace("\\", "/")
                lab = row.get("brahmi_label")
                if p and lab:
                    m[p.split("/")[-1]] = lab
    return m


def recovery_at_k(V, labels, k=5, n_null=50, seed=0):
    keep = [i for i, l in enumerate(labels) if l]
    if len(keep) < 10:
        return None
    sub = V[keep]
    subl = [labels[i] for i in keep]
    S = sub @ sub.T
    np.fill_diagonal(S, -1.0)
    topk = np.argsort(-S, axis=1)[:, :k]

    def rate(lab):
        hits = sum(any(lab[j] == lab[i] for j in topk[i]) for i in range(len(lab)))
        return hits / len(lab)

    obs = rate(subl)
    rng = np.random.default_rng(seed)
    nulls = []
    for _ in range(n_null):
        perm = list(subl)
        rng.shuffle(perm)
        nulls.append(rate(perm))
    nulls = np.asarray(nulls)
    return dict(n=len(keep), distinct_labels=len(set(subl)), k=k,
                recovery=obs, null_mean=float(nulls.mean()), null_std=float(nulls.std()),
                z=float((obs - nulls.mean()) / (nulls.std() + 1e-9)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()
    rows, V = load_images()
    lm = label_map()
    labels = [lm.get((r["source_path"] or "").split("/")[-1]) for r in rows]
    res = recovery_at_k(V, labels, k=args.k)
    if not res:
        sys.exit("not enough labeled crops to validate (need >=10 with known Brahmi labels)")
    print(f"labeled crops: {res['n']} across {res['distinct_labels']} labels")
    print(f"recovery@{res['k']}: {res['recovery']:.3f}   "
          f"null: {res['null_mean']:.3f} ± {res['null_std']:.3f}   z={res['z']:.1f}")
    verdict = ("STRONG — embeddings capture glyph identity well above chance" if res['z'] > 5
               else "WEAK/NULL — not clearly above chance; do NOT build on these embeddings" if res['z'] < 2
               else "MODEST — above chance but inspect before trusting")
    print("verdict:", verdict)
    print("\nNOTE: a positive result is necessary, not sufficient. Embedding matches remain "
          "CANDIDATES requiring source-image validation + forger nulls + skeptic review.")


if __name__ == "__main__":
    main()
