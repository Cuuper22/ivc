# Lipi 034 M-315 Preblind Token-2 Sort

Date: 2026-05-26

Question:

```text
After correcting the M-315 target crop for local R/L order, does the visible second-slot candidate collapse into the current M-17/M-32 non-034 controls?
```

Current answer:

```text
No clean collapse yet. M-315 stays live as a distinct stroke-bundle candidate, but this is not source-validated numeric 034.
```

## Correction

The earlier M-315 files named `m315_*_second_034_region*` are page-order crops. They show the second visible unit on the page, not necessarily token 2 in the local `R/L` transcription.

For a local `R/L` row:

```text
M-315 +390-034-002-374-228-741+
```

the token-2 candidate is the stroke-bundle adjacent to the edge `390` sign:

```text
upper face: page-right adjacent stroke bundle
lower impression: mirrored page-left adjacent stroke bundle
```

Corrected M-315 local-order candidate crops are stored in:

```text
tmp/m315_cisi1/derived/m315_local_order_candidate_manifest.csv
```

The M-315/M-17/M-32 comparison crops and contact sheet are stored in:

```text
tmp/m315_second_slot_controls/derived/preblind_token2_crops/preblind_token2_crop_manifest.csv
tmp/m315_second_slot_controls/derived/preblind_token2_crops/preblind_token2_contact_sheet.png
```

The expanded M-315/M-984/M-803/M-32/M-17/M-918 context crops are stored in:

```text
tmp/m315_second_slot_controls/new_controls/derived/m803_m918_m984_public_control_crops_manifest.csv
tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/expanded_first3_context_crop_manifest.csv
tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/expanded_first3_context_contact_sheet.png
```

## Visual Sort

M-315 corrected token-2 candidate:

```text
single stroke-bundle immediately beside the edge 390 candidate
upper/lower witnesses agree at the broad visual level after mirror correction
count/detail remains low-resolution and source-gated
```

M-32 control:

```text
shorter stroke-bundle class in the same second-slot position
visually distinct from M-315 in the current crops
local code is 003, not 034
```

M-17 control:

```text
larger/stacked stroke-bundle control in the same broad second-slot family
not a clean match to M-315, but close enough that count/allograph/transcription policy must be tested directly
local code is 016, not 034
```

M-984 control:

```text
cleanest newly acquired 004 control in the current packet
impression a shows the first-three context 390 | 004 | 002 better than the damaged face and variant impressions
local code is 004, not 034
```

M-803 control:

```text
source-visible 005 control from the same 390-X-002 frame
dark/occluded source panel makes it a weak token-2 classifier input
local code is 005, not 034
```

M-918 control:

```text
source-visible 869 control from the same 390-X-002 frame
current crop is not token2-grade because of clutter and overlap
local code is 869, not 034
```

## Decision

M-315 does not currently collapse into the M-32 `003` control or the M-17 `016` control at the coarse source-crop level. The newly acquired M-984 `004` control became the strongest public same-frame stroke-bundle comparator and was therefore included in the strict blind sort.

That strict blind sort changed the status:

```text
M-315 upper face clusters with M-984 004.
M-315 lower impression does not securely join that same cluster.
```

That keeps the M-315 second-slot test alive, but it does not upgrade M-315 to source-validated `034`. The source-visible fact is still:

```text
M-315 has a stroke-bundle candidate in local token-2 position, adjacent to the edge 390 candidate.
```

The unvalidated claim remains:

```text
that stroke-bundle candidate equals numeric Lipi 034.
```

## Next Gate

The first blind stroke-bundle/count/allograph sort is now executed and recorded in:

```text
docs/lipi_034_m315_blind_390x002_sort.md
data/open_prototype/reports/lipi_034_m315_blind_390x002_sort_review.csv
```

Required panel set:

```text
M-315 token-2 candidate
M-32 003 control
M-984 004 control
M-803 005 control
M-17 016 control
M-1833 015 control
M-918 869 control
Ai-7 and H-335 only as weak 390-034 existence controls
```

Pass condition:

```text
M-315 remains a distinct second-slot stroke-bundle class after blind orientation-normalized comparison, while the controls retain their non-034 classes.
```

Observed fail condition:

```text
M-315 upper face collapses toward M-984 004, and the two M-315 witnesses do not independently preserve a distinct 034 class.
```

Accepted translations, sign values, phonetic readings, and language assignments remain:

```text
0
```
