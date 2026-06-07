# Brahmi Real-Token Low-Null Autopsy v3b

Date: 2026-05-31

This is the follow-up gate for the remaining low-null rows from the Brahmi real-token impostor forger. The previous v3 impostor run found 21 sign/orientation families where unrelated real Indus token crops did not reproduce the observed Brahmi modal-label match above the `0.01` threshold. This audit asks whether any of those 21 rows actually becomes a review candidate after joining the v2 shape/label nulls, the v3 independence preflight, and duplicate-collapse checks.

No. The low-null rows are not survivors.

## Artifacts

- `data/brahmi/tools/audit_brahmi_real_token_low_null_rows_v3b.mjs`
- `data/brahmi/brahmi_real_token_low_null_autopsy_v3b.csv`
- `data/brahmi/brahmi_real_token_low_null_autopsy_v3b_summary.json`

Inputs:

- `data/brahmi/brahmi_real_token_impostor_forger_v3.csv`
- `data/brahmi/brahmi_independent_source_token_gate_v3.csv`
- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/source_token_segments_v2.csv`

## Result

| Measure within low-null rows | Count |
| --- | ---: |
| Low real-token impostor rows (`<= 0.01`) | 21 |
| Pass original shape-null threshold (`<= 0.01`) | 0 |
| Pass original label-null threshold (`<= 0.01`) | 2 |
| Pass minimum source-token independence | 10 |
| Pass duplicate-collapse unanimity | 7 |
| Pass both minimum independence and duplicate-collapse unanimity | 0 |
| Review-packet eligible rows | 0 |

Every low-null row still fails the original shape-null gate. Nineteen of the 21 also fail the original label-null gate. Eleven fail minimum source-token independence. The remaining independence-pass rows are not duplicate-collapse unanimous, so they are broad-family modal artifacts, not stable sign-value candidates.

The two rows that pass the label-null threshold still die:

| Sign | Orientation | Modal label | Impostor share | Shape-null share | Independence blocker |
| --- | --- | --- | ---: | ---: | --- |
| `798` | reverse | `ra` | `0.000000` | `0.100000` | only two CISIs |
| `055` | reverse | `ra` | `0.002000` | `0.097727` | only two CISIs |

The strongest v2 near-miss rows stay blocked:

| Sign | Orientation | Modal label | Impostor share | Shape-null share | Label-null share | Blocker |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `527` | order | `ra` | `0.000000` | `0.035000` | `0.031000` | two token hashes, one CISI, shape+label fail |
| `061` | order | `ra` | `0.008000` | `0.047500` | `0.020000` | two token hashes, one CISI, shape+label fail |

## Decision

Retracted as a descendant-script phonetic anchor. The low-null subset adds no candidate-only rows and no visual-review rows. It only says the real-token impostor forger is not the binding objection for those 21 rows; the binding objections are the original shape null, the original label null, and source-token independence/duplicate-collapse instability.

Next Brahmi gate, if pursued, needs new independent source-token data before any rerun. Reusing these 21 rows cannot create a value, sound, language identification, or translation.
