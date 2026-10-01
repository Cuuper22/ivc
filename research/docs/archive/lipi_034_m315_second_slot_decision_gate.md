# Lipi 034 M-315 Second-Slot Decision Gate

Date: 2026-05-26

This note is a decision gate. A gate is a test a claim must pass before the project will build on it; writing the gate down in advance is what stops the standard from sliding once results come in.

The claim under test concerns seal `M-315`. Our transcription gives it the sign `034` in its second slot — a slot being one position in the sign row — inside the frame `390-X-002`, where a frame is a fixed run of surrounding signs with one position left open for comparison. If that is right, `M-315` is the only object in the corpus with that particular contrast. If it is wrong, the contrast does not exist at all.

Question:

```text
Can M-315 support a real second-slot 034 contrast in the frame 390-X-002?
```

Current answer:

```text
Not yet. M-315 is a priority source-validation target, not an accepted functional contrast.
```

## What Is Real Now

Local target:

```text
M-315 / 2833.1 / +390-034-002-374-228-741+
Mohenjo-daro, steatite square seal, one side, R/L, six signs
Local object string: VS 1190395
```

Source-visible object binding is real:

```text
CISI Vol. 1 leaf n113 / printed p. 78 labels M-315 A and M-315 a.
CISI Vol. 1 leaf n403 / printed p. 368 has the M-315 data row.
The p. 368 row reads as M-315 / 1395 / VS 1190 / ASI 63.10.117 / HU 318.
```

Stored source crops:

```text
tmp/m315_cisi1/derived/m315_page78_boxes_overlay.png
tmp/m315_cisi1/derived/m315_upper_face_signs_close_gray_autocontrast.png
tmp/m315_cisi1/derived/m315_lower_impression_signs_close_gray_autocontrast.png
tmp/m315_cisi1/derived/m315_data_page_row_context_gray_autocontrast.png
```

Do not use the old `m315_*_second_034_region*` crops as local token-2 evidence. They are page-order crops, not corrected local `R/L` token-2 crops.

Corrected local-order candidate crops are stored in:

```text
tmp/m315_cisi1/derived/m315_local_order_candidate_manifest.csv
```

The local contrast is real enough to chase:

```text
390-X-002 rows: 37
390-034-002 rows: 1
390-034 openings: 3
```

In the local Lipi data, the single extended `390-034-002` row is M-315. The other local `390-034` openings are only:

```text
Ai-7   +390-034+
H-335  +390-034+
M-315  +390-034-002-374-228-741+
```

## What Is Not Real Yet

No source page currently prints a numeric sign transcription beside M-315. So the second visible unit being `034` is still a local Lipi transcription claim, not an independently validated source fact.

Direction is unresolved. CISI shows a light face and a dark impression in mirrored order, while the local row says `R/L`. A left-to-right page view is not a linguistic order.

The object identifier is not fully reconciled. Local `VS 1190395` appears to fuse source-visible `1395` and `VS 1190`; this is a catalogue-data warning, not a fatal contradiction.

M-315 is a singleton in the exact extended frame. If the second visible unit is damage, allograph, compound oversegmentation, or a misread neighboring code such as `003`, `004`, `005`, `016`, or `415`, the whole `390-034-002` signal disappears.

## Control Packet

A control is a comparison object whose sign we are reasonably sure of. A packet is the bundle of crops and records assembled for one test. These controls exist so a reviewer's judgement can be checked against known cases.

The decision controls are stored in:

```text
data/open_prototype/reports/lipi_034_m315_second_slot_decision_controls.csv
```

Public source-panel crops for the two currently accessible non-034 controls are stored in:

```text
tmp/m315_second_slot_controls/derived/m17_m32_public_control_crops_manifest.csv
```

That manifest has collision-proof A/a filenames for Windows:

```text
M-17_face_A_* / M-17_impression_a_*
M-32_face_A_* / M-32_impression_a_*
```

These crops are useful only as control comparanda — comparison material set beside the target, nothing more. They support a blind graphic sort of M-315's second visible unit against non-034 second-position shapes; they do not validate M-315's second slot as numeric `034`.

Expanded public control crops acquired on 2026-05-26:

```text
tmp/m315_second_slot_controls/new_controls/derived/m803_m918_m984_public_control_crops_manifest.csv
tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/expanded_first3_context_crop_manifest.csv
tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/expanded_first3_context_contact_sheet.png
```

Source-page bindings:

```text
M-803: CISI Pakistan leaf n102 / printed p. 68 / MOHENJODARO 798-803 SEALS / 'unicorn' IV
M-918: CISI Pakistan leaf n122 / printed p. 88 / MOHENJO-DARO 914-922 SEALS / 'unicorn' V
M-984: CISI Pakistan leaf n130 / printed p. 96 / MOHENJO-DARO 983-990 SEALS / 'unicorn' V
```

Same-site `390-X-002` controls:

| Object | Local text | Use |
| --- | --- | --- |
| `M-32` | `+390-003-002-817+` | Best public/Mayig-overlap non-034 control. |
| `M-984` | `+390-004-002-817+` | Best new public `004` control; impression `a` is cleanest for first-three comparison, while face `A` and `a bis`/`a ter` are damaged or partial. |
| `M-803` | `+390-005-002-817+` | Source-visible public `005` control, but dark/occluded and weak for token-2 sorting. |
| `M-17` | `+390-016-002-814-560+` | Public/Mayig-overlap non-034 control. |
| `M-1833` | `+390-015-002-861+` | CISI 3.1 or equivalent source needed. |
| `M-918` | `+390-869-002-861+` | Source-visible public `869` control, but cluttered and not token2-grade in the current crop. |

Short `390-034` existence controls:

| Object | Local text | Why weak |
| --- | --- | --- |
| `Ai-7` | `+390-034+` | Different site and material; not a clean same-frame control. |
| `H-335` | `+390-034+` | Different site and object class; not a clean same-frame control. |

Mayig/Parpola overlap helps only for controls, not the target:

```text
M-17 local: 390 016 002 814 560
M-17 Mayig/Parpola: P086 P126 P122 P369 P232

M-32 local: 390 003 002 817
M-32 Mayig/Parpola: P086 P123 P122 P385
```

That supports the broad `390 -> P086` and `002 -> P122` bridge — a checked link between our sign codes and another catalogue's — in public-overlap controls, but it does not validate `M-315 034`, because current Mayig coverage stops before M-315.

## Decision Tree

Six gates in order, each with its own pass condition and its own way of failing. Each carries a status word: PASS, OPEN meaning not yet decided, or FAILED.

Gate 1: object binding.

```text
PASS: CISI p. 78 labels M-315 A/a, and p. 368 has an M-315 data row.
Scope: object/source visibility only.
```

Gate 2: direction convention.

```text
OPEN: decide face vs impression and normalize reading order before evaluating slot position.
Fail mode: the apparent second slot is a page-view artifact.
```

Gate 3: six-unit segmentation.

```text
OPEN: both M-315 witnesses look compatible with six visible graphic units.
Fail mode: the visible image is better segmented as a compound, damaged unit, or fewer/more than six signs.
```

Gate 4: second-unit identity.

```text
FAILED CURRENT PUBLIC-CROP UPGRADE: strict blind classifiers did not preserve M-315 as a distinct 034-like second unit in both witnesses.
Pass condition: both M-315 witnesses independently sort into the local-bin sequence 390 | 034 | 002 | ...
Observed fail pressure: M-315 upper face clusters with M-984 004; M-315 lower impression does not securely join that pair.
```

Gate 5: matched controls.

```text
FAILED CURRENT PUBLIC-CROP UPGRADE: M-984 004 does not stay visually separate from the M-315 upper witness in strict blind sorting.
Pass condition: M-315 is the only source-visible object that independently sorts into the local 034 second-slot bin in the matched 390-X-002 frame.
Fail condition reached for the current crop packet: M-315 upper collapses toward the 004 control.
```

Gate 6: independent 390-034 support.

```text
OPEN: Ai-7 and H-335 must be checked only as weak existence controls.
Pass condition: they confirm that 390-034 is not an M-315-only transcription accident.
Fail condition: either source check shows 034 is a local transcription artifact.
```

## Blind Sort Executed

Blind means the reviewers grouped the crops without being told which object each came from or what our labels said. The protocol below is written out step by step because the order of the steps is the safeguard: labels come off before judging and go back on only afterward.

The blind source-panel classification was run as:

```text
docs/lipi_034_m315_blind_390x002_sort.md
data/open_prototype/reports/lipi_034_m315_blind_390x002_sort_review.csv
tmp/m315_second_slot_controls/blind_390x002_sort_20260526/
```

Protocol used:

```text
1. Collect source panels for M-315 A/a, M-32, M-984, M-803, M-17, M-1833, and M-918. Current gap: M-1833 remains CISI 3.1/equivalent gated.
2. Normalize face/impression orientation before classification.
3. Hide local numeric labels from the reviewer.
4. Segment the first three visible units only: 390 | X | 002.
5. Ask whether X is the same or different across objects.
6. Reattach local labels only after the blind sort.
```

Upgrade condition:

```text
M-315 independently segments into local bins 390 | 034 | 002 in both witnesses, while same-frame controls retain 003/004/005/016/015/869 or another distinct non-034 second slot.
```

Observed strict result:

```text
M-315 upper face clusters with M-984 004 across all strict blind reviewers.
M-315 lower impression does not securely join that cluster.
M-17 016 is composite/stacked in the strict crop and should not carry decisive weight.
```

Downgrade condition reached:

```text
M-315 current public crop packet fails upgrade to source-validated 034.
```

Accepted translations, sign values, phonetic readings, and language assignments remain:

```text
0
```
