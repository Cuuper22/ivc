"""The sign vocabulary and the Transformer encoder trained on sign sequences.

The model is an encoder, not a generator. It sees a whole sequence at once with
some positions hidden, and predicts what belongs in the hidden positions from
the signs on both sides. That is the right shape for this evidence: the
sequences are short, and the question is whether a sign is constrained by its
neighbours, not whether text can be continued.

The encoder carries three heads, each answering a different question:

- the tied output projection scores which sign belongs in a masked slot;
- `replacement_head` marks, per position, whether that sign was swapped out;
- `authenticity_head` scores a whole sequence as stored-order or corrupted.

Sizes are small on purpose. See the branch README for why capacity is matched
to roughly eight thousand observed sign tokens rather than to a parameter
ceiling.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import nn


# Reserved ids that are not signs: padding, the hidden slot, sequence
# boundaries, and a fallback for a token outside the vocabulary.
SPECIAL_TOKENS = ("[PAD]", "[MASK]", "[BOS]", "[EOS]", "[UNK]")


@dataclass(frozen=True)
class ModelSpec:
    """One point on the capacity curve: the shape of a single model size."""

    name: str
    d_model: int
    layers: int
    heads: int
    ffn: int
    dropout: float


class Vocabulary:
    """Maps sign labels to integer ids, with the special tokens ranked first.

    Keeping every special token below `first_sign_id` means evaluation can slice
    them off and score only real signs, so the model never wins by predicting
    padding or a boundary marker.
    """

    def __init__(self, tokens: list[str]) -> None:
        unique = sorted(set(tokens))
        self.tokens = list(SPECIAL_TOKENS) + [token for token in unique if token not in SPECIAL_TOKENS]
        self.token_to_id = {token: index for index, token in enumerate(self.tokens)}
        self.pad_id = self.token_to_id["[PAD]"]
        self.mask_id = self.token_to_id["[MASK]"]
        self.bos_id = self.token_to_id["[BOS]"]
        self.eos_id = self.token_to_id["[EOS]"]
        self.unk_id = self.token_to_id["[UNK]"]
        self.first_sign_id = len(SPECIAL_TOKENS)

    def __len__(self) -> int:
        return len(self.tokens)

    def encode(self, tokens: tuple[str, ...] | list[str], boundaries: bool = True) -> list[int]:
        """Turn sign labels into ids, optionally wrapped in start/end markers."""
        values = [self.token_to_id.get(token, self.unk_id) for token in tokens]
        return [self.bos_id, *values, self.eos_id] if boundaries else values

    def decode_id(self, token_id: int) -> str:
        return self.tokens[token_id]

    def to_dict(self) -> dict[str, int]:
        return dict(self.token_to_id)


class SignTransformer(nn.Module):
    """A bidirectional Transformer encoder over one sequence of signs.

    `norm_first` layers are used because they train stably at these small sizes
    without a long warmup. The output projection reuses the token embedding
    matrix (weight tying), which keeps the parameter count honest on a corpus
    this small.
    """

    def __init__(self, vocab_size: int, max_length: int, spec: ModelSpec, pad_id: int) -> None:
        super().__init__()
        self.spec = spec
        self.pad_id = pad_id
        self.token_embedding = nn.Embedding(vocab_size, spec.d_model, padding_idx=pad_id)
        self.position_embedding = nn.Embedding(max_length, spec.d_model)
        self.embedding_norm = nn.LayerNorm(spec.d_model)
        self.embedding_dropout = nn.Dropout(spec.dropout)
        layer = nn.TransformerEncoderLayer(
            d_model=spec.d_model,
            nhead=spec.heads,
            dim_feedforward=spec.ffn,
            dropout=spec.dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=spec.layers, norm=nn.LayerNorm(spec.d_model))
        self.output_bias = nn.Parameter(torch.zeros(vocab_size))
        self.replacement_head = nn.Linear(spec.d_model, 1)
        self.authenticity_head = nn.Sequential(
            nn.Linear(spec.d_model, spec.d_model), nn.GELU(), nn.Dropout(spec.dropout), nn.Linear(spec.d_model, 1)
        )
        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Draw small random embeddings and zero the padding row."""
        nn.init.normal_(self.token_embedding.weight, mean=0.0, std=0.02)
        nn.init.normal_(self.position_embedding.weight, mean=0.0, std=0.02)
        with torch.no_grad():
            self.token_embedding.weight[self.pad_id].zero_()

    def encode(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Return one contextual vector per position; padding is masked out."""
        positions = torch.arange(input_ids.shape[1], device=input_ids.device).unsqueeze(0)
        hidden = self.token_embedding(input_ids) * math.sqrt(self.spec.d_model)
        hidden = self.embedding_dropout(self.embedding_norm(hidden + self.position_embedding(positions)))
        return self.encoder(hidden, src_key_padding_mask=input_ids.eq(self.pad_id))

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Score every sign at every position, using the tied embedding matrix."""
        hidden = self.encode(input_ids)
        return torch.nn.functional.linear(hidden, self.token_embedding.weight, self.output_bias)

    def replacement_logits(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Per position, score whether this sign was swapped in by corruption."""
        return self.replacement_head(self.encode(input_ids)).squeeze(-1)

    def authenticity_logits(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Score a whole sequence by averaging its non-padding positions.

        This head is explicitly trained to separate stored order from
        corruptions, so a high score is generalization of a trained task, not
        independent evidence about direction.
        """
        hidden = self.encode(input_ids)
        mask = input_ids.ne(self.pad_id).unsqueeze(-1)
        pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
        return self.authenticity_head(pooled).squeeze(-1)

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())
