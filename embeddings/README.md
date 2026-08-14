# Multimodal embedding layer (`embeddings/`)

This layer turns items in the corpus into vectors so we can search them by similarity.
It is a **candidate-generation and search layer**: image embeddings of sign crops, plus
text embeddings of research docs, sign sequences, and signs. Everything runs on CPU with
[fastembed](https://github.com/qdrant/fastembed) (ONNX, no PyTorch). Vectors are stored
as Parquet, joinable to `db/ivc.sqlite` by `item_id`.

> **Guardrail — read this.** Embeddings are NOT evidence. **Visual similarity ≠ sign
> identity**: engraving variation, damage, and source-image quality are exactly this
> project's confounds. Anything embeddings surface is a *candidate* that must still clear
> source-image validation → forger nulls → skeptic review, per the project's claim rules.

## Status (2026-06-15)

The pipeline is complete and committed but **has not been run in the author's
environment**. The reason is network access: `huggingface.co` is blocked here (hard
connection reset), and the reachable mirror redirects model files across HF CDNs that are
only partly reachable, so a model can't be assembled reliably. Run it from a
machine/VPN/proxy with HuggingFace access, or pre-place the model files in the HF cache
(see below).

## Install

```sh
py -m pip install fastembed numpy pyarrow
# In a network-restricted environment, fastembed's downloader needs the requests-based
# hub line and (optionally) a mirror endpoint:
py -m pip install "huggingface_hub<1.0"
# export HF_ENDPOINT=https://hf-mirror.com    # only if huggingface.co is blocked AND you trust the mirror
```

Models (pinned, downloaded once, then offline & reproducible):
- text  — `BAAI/bge-small-en-v1.5` (384-d)
- image — `Qdrant/clip-ViT-B-32-vision` (512-d, CLIP)

## Build / query / validate

```sh
py embeddings/build_embeddings.py --what text                 # docs + sign-seqs + signs
py embeddings/build_embeddings.py --what images --limit 800   # sign crops (pilot cap)
py embeddings/build_embeddings.py --what images               # all configured crops

py embeddings/query_embeddings.py --text-search "terminal tail formula after 002-861"
py embeddings/query_embeddings.py --nn "img:research/data/brahmi/source_token_crops_v2/..."

py embeddings/validate_recovery.py        # THE GATE: do image-NN recover same Brahmi label vs null?
```

## What to embed (and why)

| Modality | Source | Use |
|---|---|---|
| image | sign crops (Brahmi letter images, source-token crops, Indus component crops) | crosswalk / allograph **candidate generation** — the project's manual bottleneck |
| text  | `research/docs/*.md` | semantic search over the lab notebook |
| text  | witness `sign_sequence`, sign descriptions | cluster/search formulae and signs |

## Validate before trusting (the honest first move)

Before we trust the image embeddings for anything, we test them on a question with a known
answer. `validate_recovery.py` asks: do image-embedding nearest-neighbors recover **known
labels** (Brahmi letters) better than a shuffled-label null? If they don't beat chance,
then the embeddings don't capture glyph identity in this corpus, and nothing should be
built on them. That negative result is a valid, useful outcome. The Indus-crosswalk
version of this test (does NN recover known high-support edges like `002→P122`,
`220→P050`?) is the next step once crop→sign_id labels are wired in.

## Upgrade path

CLIP is a general visual model. For line-drawing glyphs, **DINOv2** features are usually
stronger, but they need PyTorch. The store/query/validate code is model-agnostic — swap the
`IMAGE_MODEL` and rebuild. For cross-modal text→image (`query_embeddings.py --clip-search`),
also embed with `Qdrant/clip-ViT-B-32-text` so text and images share one space.
