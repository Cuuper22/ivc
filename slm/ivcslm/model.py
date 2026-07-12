from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import nn


SPECIAL_TOKENS = ("[PAD]", "[MASK]", "[BOS]", "[EOS]", "[UNK]")


@dataclass(frozen=True)
class ModelSpec:
    name: str
    d_model: int
    layers: int
    heads: int
    ffn: int
    dropout: float


class Vocabulary:
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
        values = [self.token_to_id.get(token, self.unk_id) for token in tokens]
        return [self.bos_id, *values, self.eos_id] if boundaries else values

    def decode_id(self, token_id: int) -> str:
        return self.tokens[token_id]

    def to_dict(self) -> dict[str, int]:
        return dict(self.token_to_id)


class SignTransformer(nn.Module):
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
        nn.init.normal_(self.token_embedding.weight, mean=0.0, std=0.02)
        nn.init.normal_(self.position_embedding.weight, mean=0.0, std=0.02)
        with torch.no_grad():
            self.token_embedding.weight[self.pad_id].zero_()

    def encode(self, input_ids: torch.Tensor) -> torch.Tensor:
        positions = torch.arange(input_ids.shape[1], device=input_ids.device).unsqueeze(0)
        hidden = self.token_embedding(input_ids) * math.sqrt(self.spec.d_model)
        hidden = self.embedding_dropout(self.embedding_norm(hidden + self.position_embedding(positions)))
        return self.encoder(hidden, src_key_padding_mask=input_ids.eq(self.pad_id))

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        hidden = self.encode(input_ids)
        return torch.nn.functional.linear(hidden, self.token_embedding.weight, self.output_bias)

    def replacement_logits(self, input_ids: torch.Tensor) -> torch.Tensor:
        return self.replacement_head(self.encode(input_ids)).squeeze(-1)

    def authenticity_logits(self, input_ids: torch.Tensor) -> torch.Tensor:
        hidden = self.encode(input_ids)
        mask = input_ids.ne(self.pad_id).unsqueeze(-1)
        pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
        return self.authenticity_head(pooled).squeeze(-1)

    @property
    def parameter_count(self) -> int:
        return sum(parameter.numel() for parameter in self.parameters())
