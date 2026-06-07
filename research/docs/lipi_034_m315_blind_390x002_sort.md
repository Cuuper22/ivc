# Lipi 034 M-315 Blind 390-X-002 Sort

Date: 2026-05-26

## Question

```text
Does the visible M-315 local token-2 candidate survive a blind graphic sort as a distinct second-slot class inside the 390-X-002 frame?
```

## Result

```text
No upgrade.
```

The strict blind sort does not validate M-315 as source-visible numeric `034`. The upper M-315 witness clusters with the clean M-984 `004` control, while the lower M-315 witness does not securely join that same pair. This blocks the required condition that both M-315 witnesses independently preserve a distinct local `034` class.

This is not proof that M-315 is `004`. It is proof that the current public crops do not support the cleaner claim:

```text
M-315 visibly validates a unique 034 second slot in 390-034-002.
```

## Packet

Neutral blind packet:

```text
tmp/m315_second_slot_controls/blind_390x002_sort_20260526/
```

The first reviewer packet hid object IDs and local numeric labels. It exposed one problem: some token-focus crops still contained neighboring context. Therefore the decisive packet was recut as strict token-2 crops from the first-three context images.

Strict packet and key:

```text
tmp/m315_second_slot_controls/blind_390x002_sort_20260526/strict_token2_from_context/
tmp/m315_second_slot_controls/blind_390x002_sort_20260526/strict_token2_from_context/strict_token2_from_context_key.csv
```

Review result table:

```text
data/open_prototype/reports/lipi_034_m315_blind_390x002_sort_review.csv
```

## Unblinded Strict Key

| Blind ID | Object | Witness | Local label | Decision note |
| --- | --- | --- | --- | --- |
| `S001` | `M-32` | impression `a` | `003_control` | Short separated vertical bundle; usable with caution. |
| `S002` | `M-315` | lower impression | `034_candidate` | Does not join the strongest `S003-S005` pair. |
| `S003` | `M-984` | impression `a` | `004_control` | Clean public `004` comparator. |
| `S004` | `M-17` | impression `a` | `016_control` | Composite/stacked sample; not clean isolated decision evidence. |
| `S005` | `M-315` | upper face | `034_candidate` | Clusters with `S003` across all strict reviewers. |

## Blind Reviewer Consensus

Three independent blind reviews on `S001-S005` converged on the same pressure point:

```text
S003-S005 is the strongest pair.
```

After unblinding:

```text
S003 = M-984 impression a, local 004 control
S005 = M-315 upper face, local 034 candidate
```

The other M-315 witness:

```text
S002 = M-315 lower impression
```

did not reliably cluster with `S003-S005`. Reviewers placed it with the short/separated vertical-bundle group or treated it as a separate/nearby sample. `S004` was repeatedly flagged as composite or not cleanly isolated.

## Decision Gate

Required upgrade condition:

```text
Both M-315 witnesses independently sort into a distinct second-slot class while M-32, M-984, and M-17 retain their non-034 classes.
```

Observed:

```text
M-315 upper face clusters with M-984 004.
M-315 lower impression does not securely join that same cluster.
M-17 016 is not cleanly isolated in the strict crop and should not carry the decision.
M-32 003 remains a short separated vertical-bundle comparator.
```

Decision:

```text
M-315 fails the current blind upgrade gate.
```

## Accepted And Rejected

Accepted:

```text
M-315 is source-visible in CISI Vol. 1.
M-315 remains a high-value source target because local Lipi uniquely has 390-034-002.
The current public blind sort creates direct 004-pressure on the upper M-315 witness.
The two M-315 witnesses do not currently give a stable, independent, distinct 034 class.
```

Rejected:

```text
numeric 034 source mapping for M-315
034 count value
034 sign value
function
phonetic reading
language identity
translation
```

## Next Research Consequence

M-315 should move from:

```text
live distinct 034 candidate
```

to:

```text
source-visible singleton with failed blind upgrade and upper-witness 004-pressure
```

The branch is not dead, but it now requires stronger source evidence: higher-resolution M-315 images, independent source transcription, or a cleaner face/impression orientation and segmentation basis. It cannot be used as positive `034` evidence for translation work.
