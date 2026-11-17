#!/usr/bin/env python3
"""sense_embed.py -- embeds every sense phrase ONCE with google/embeddinggemma-2 (current open embedding model, Apache licence; 744M parameters,
downloaded from huggingface.co/google/embeddinggemma-2) on CPU in float32, using its 'STS' (sentence similarity) prompt, vectors normalised.
Saved as float16 .npy in the same row order as the csv. Run: /tmp/senv/bin/python sense_embed.py <senses.csv> <out.npy>"""
import sys, time, numpy as np, pandas as pd, torch
from sentence_transformers import SentenceTransformer
src, out = sys.argv[1], sys.argv[2]
SS = pd.read_csv(src).fillna('')
txt = SS.phrase.tolist(); uniq = sorted(set(txt)); print('phrases', len(txt), 'unique', len(uniq), flush=True)
torch.set_num_threads(2)
m = SentenceTransformer('/tmp/hfm/eg2', device='cpu', model_kwargs={'dtype': torch.float32})
t = time.time(); E = {}
B = 128
for i in range(0, len(uniq), B):
    e = m.encode(uniq[i:i + B], batch_size=64, prompt_name='STS', normalize_embeddings=True)
    for u, v in zip(uniq[i:i + B], e): E[u] = v
    print(f'embedded {min(i + B, len(uniq))}/{len(uniq)} ({time.time() - t:.0f}s)', flush=True)
X = np.stack([E[p] for p in txt]).astype(np.float16)
np.save(out, X); print('saved', out, X.shape, X.nbytes / 1e6, 'MB')
