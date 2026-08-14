"""Leakage-controlled, from-scratch IVC sequence-model experiments.

`ivcslm` trains small Transformer encoders on sequences of Indus Valley
Civilization (IVC) signs and on comparator corpora, then measures how well a
trained model predicts a sign that was hidden from it. The point is to find out
whether the sequences carry order that repeats across objects, and to make it
hard for a model to fake that answer by memorizing near-duplicate rows.

The package holds the whole instrument:

- `data`: load corpora, collapse exact duplicates, group near-duplicate rows,
  and split them so that no family straddles train/validation/test.
- `model`: the vocabulary and the Transformer encoder with its three heads.
- `batching`: turn records into masked and corrupted training tensors.
- `training`: the fitting loop, early stopping, and checkpointing.
- `evaluation`: held-out scoring, baselines, and probes.
- `experiment`: the run matrix, budget guard, and immutable output directory.
- `cli`: the `ivcslm` command.

What the results can and cannot show: a model that beats the frequency
baselines is evidence of repeatable structure. It is never evidence of a
phonetic value, a sign meaning, a language family, an external anchor, or a
translation.
"""

__version__ = "0.1.0"

