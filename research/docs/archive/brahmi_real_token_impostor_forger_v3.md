# Brahmi Real-Token Impostor Forger v3

Date: 2026-05-30

This is the hostile follow-up to the Brahmi v3 independence gate. Earlier nulls asked whether random abstract shape evolution could imitate an Indus-to-Brahmi match. This forger asks something narrower and nastier: it takes real Indus source-token crops from other signs and uses them as impostors. Can unrelated Indus token crops — matched by orientation, and filtered away from the same CISI, source path, and exact token hash — reproduce the apparent Brahmi modal-label agreement?

Yes, often enough to block promotion. No phonetic anchor survives.

## Artifacts

- `data/brahmi/tools/build_brahmi_real_token_impostor_forger_v3.mjs`
- `data/brahmi/brahmi_real_token_impostor_forger_v3.csv`
- `data/brahmi/brahmi_real_token_impostor_forger_iterations_v3.csv`
- `data/brahmi/brahmi_real_token_impostor_forger_v3_summary.json`

Inputs:

- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/source_token_segments_v2.csv`
- `data/brahmi/source_token_brahmi_neighbors_v2.csv`
- `data/brahmi/brahmi_independent_source_token_gate_v3.csv`

## Rule

For each v2 sign/orientation family, the forger:

- takes the observed source-token family and its top-1 Brahmi neighbor modal label,
- builds a pool of real Indus token crops from other signs under the same orientation policy,
- excludes the same CISI, same source path, same exact token hash, and same assigned sign,
- prefers impostors matched on aspect ratio and ink density when enough exist,
- samples 1,000 impostor families without replacement when the pool is large enough,
- counts an impostor as matching or beating the observed family if its modal-label count is at least the observed modal count and its mean modal distance is at most the observed mean modal distance.

The forger cannot accept a row on its own. To become a visual-review candidate, a row must also survive the v3 independence preflight and the original v2 shape/label null gates.

## Result

| Measure | Value |
| --- | ---: |
| Input v2 sign/orientation families | 83 |
| Families with full 1,000-iteration impostor runs | 82 |
| Families with insufficient impostor pool | 1 |
| Families with real-token null share > 0.01 | 61 |
| Families with real-token null share <= 0.01 | 21 |
| Review-packet eligible rows | 0 |
| Candidate-only rows | 0 |
| Accepted phonetic anchors | 0 |

## Replacement Low-Null Reaudit Added 2026-05-31

The v3 result left 21 low real-token impostor rows at or below the `0.01` threshold. The replacement branch reran the v3 impostor forger and then reaudited those rows without reading the quarantined `v3b` artifacts:

- `data/brahmi/tools/audit_brahmi_real_token_low_null_replacement_20260531.mjs`
- `data/brahmi/brahmi_real_token_low_null_reaudit_20260531.csv`
- `data/brahmi/brahmi_real_token_low_null_reaudit_20260531_summary.json`
- `docs/brahmi_real_token_low_null_reaudit_20260531.md`

Result: no low-null row is review-packet eligible. All 21 still fail the original shape-null threshold, 19 also fail the label-null threshold, 21 fail v3 preflight, 11 fail minimum source-token independence, 14 fail duplicate-collapse unanimity, and no row passes both minimum independence and duplicate-collapse unanimity. The two label-null survivors (`798` reverse and `055` reverse) are still shape-null failures and have only two CISIs. The tempting `527` order and `061` order near-misses remain one-CISI families with two token hashes and failed shape/label nulls.

Decision: low real-token impostor share alone is not a candidate gate. It is a weak negative-control fact, not a phonetic value.

The headline v2 near-misses remain blocked:

| Sign | Orientation | v2 modal | v3 CISI modal | Real-token impostor share | Decision |
| --- | --- | --- | --- | ---: | --- |
| `527` | order | `ra` | `ra` | 0.000000 | blocked by v3 independence and v2 gate |
| `527` | reverse | `o` | `o` | 0.036000 | blocked by real-token null, v3 independence, and v2 gate |
| `061` | order | `ra` | `ra` | 0.008000 | blocked by v3 independence and v2 gate |
| `061` | reverse | `ja` | `o` | 0.103000 | blocked by real-token null, v3 independence, and v2 gate |
| `817` | order | `dha` | `dha` | 0.169000 | blocked by real-token null, v3 independence, and v2 gate |
| `472` | reverse | `ra` | `ra` | 0.248000 | blocked by real-token null, v3 independence, and v2 gate |
| `817` | reverse | `dhya` | `dhya` | 0.264000 | blocked by real-token null, v3 independence, and v2 gate |
| `060` | reverse | `ka` | `ka` | 0.367000 | blocked by real-token null, v3 independence, and v2 gate |
| `472` | order | `ra` | `ra` | 0.530000 | blocked by real-token null, v3 independence, and v2 gate |
| `060` | order | `ra` | `ra` | 0.701000 | blocked by real-token null, v3 independence, and v2 gate |

The most tempting low-null rows are not promotable either. `527` order and `061` order have real-token impostor shares of `0.000000` and `0.008000`, but both are single-CISI families with only two unique token hashes and already failed the v3 independence preflight. A low impostor share cannot rescue a non-independent witness family.

## Decision

Retracted as a descendant-script phonetic anchor. The real-token impostor forger accepts zero rows and promotes zero visual-review candidates.

What this run still buys us: it closes a loophole in the Brahmi back door. Shape similarity is no longer judged only against abstract randomized shapes; it is also judged against real Indus token crops from other signs. Any future Brahmi anchor must beat v2 shape/label nulls, v3 source-token independence, and this real-token impostor null before it can count as candidate phonetic evidence.
