# Brahmi Real-Token Low-Null Reaudit, Replacement Run

Date: 2026-05-31 America/Los_Angeles.

The `v3b` artifacts are quarantined, so this note re-earns the stopped Brahmi checkpoint from scratch, without reading them. It is a negative gate, not a phonetic result.

## Guardrail

Excluded inputs:

- `tmp/quarantine_bad_successor_20260531T0104/**`
- `data/brahmi/brahmi_real_token_low_null_autopsy_v3b.csv`
- `data/brahmi/brahmi_real_token_low_null_autopsy_v3b_summary.json`
- `docs/brahmi_real_token_low_null_autopsy_v3b.md`

Replacement outputs:

- `data/brahmi/tools/audit_brahmi_real_token_low_null_replacement_20260531.mjs`
- `data/brahmi/brahmi_real_token_low_null_reaudit_20260531.csv`
- `data/brahmi/brahmi_real_token_low_null_reaudit_20260531_summary.json`

## Result

The replacement run first reran `data/brahmi/tools/build_brahmi_real_token_impostor_forger_v3.mjs`.

Real-token impostor forger checkpoint:

| Metric | Value |
| --- | ---: |
| Brahmi family rows | 83 |
| Families with full impostor simulations | 82 |
| Rows above real-token null threshold 0.01 | 61 |
| Rows at or below real-token null threshold 0.01 | 21 |
| Accepted phonetic anchors | 0 |

Low-null reaudit:

| Metric | Value |
| --- | ---: |
| Low-null rows audited | 21 |
| Fail original shape-null threshold | 21 |
| Fail original label-null threshold | 19 |
| Fail v3 independence preflight | 21 |
| Fail minimum independence | 11 |
| Fail duplicate-collapse unanimity | 14 |
| Fail modal-label stability after collapse | 5 |
| Pass both minimum independence and duplicate-collapse unanimity | 0 |
| Review-packet eligible low-null rows | 0 |
| Accepted phonetic anchors | 0 |

What this means: the low real-token-null subset hides no Brahmi phonetic anchor. Even the rows where real Indus token impostors rarely reproduce the apparent match are still blocked by the original shape nulls and the independent-source preflight. So the strongest-looking low-null rows are failure diagnostics, not candidate values.

## Input Hashes

| Input | SHA-256 |
| --- | --- |
| `data/brahmi/brahmi_real_token_impostor_forger_v3.csv` | `4cf2baebc008f167cf2ab36583b2c19411cac52626a80605dd60645a34f06ee2` |
| `data/brahmi/brahmi_real_token_impostor_forger_v3_summary.json` | `fc03fb73f9193d44b9074464094be0ceb4cfc83b959be76d80e6f10f386e5ec1` |
| `data/brahmi/brahmi_independent_source_token_gate_v3.csv` | `b7aa8e0b7028fb243c98808beb878ea8fff22a59d0428fdd6f00459a2a6f29be` |
| `data/brahmi/source_token_family_descent_summary_v2.csv` | `22b43b8a525414f50949403bf3983fe4168885b2e23c1d181a8dc479de5e3a59` |

## Claim-Ledger Effect

No count changes.

| Claim class | Increment |
| --- | ---: |
| translations | 0 |
| phonetic_values | 0 |
| sign_meanings | 0 |
| language_identification | 0 |
| structural_findings | 0 |
| external_anchors | 0 |

This gate only supports the retraction boundary for the descendant-script lane: current Brahmi shape similarity remains inadmissible as a source of phonetic values.
