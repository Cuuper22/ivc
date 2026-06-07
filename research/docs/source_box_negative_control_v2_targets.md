# Source-Box Negative Control V2 Targets

Date: 2026-05-29

The first source-box blind packet failed. One concrete hole was that it had zero image-backed `negative_220_032_next_not_002` controls. This queue targets that hole.

Output:

- `data/open_prototype/reports/source_box_negative_control_v2_targets.csv`
- `data/open_prototype/tools/source_box_negative_control_v2_acquire.py`
- `data/open_prototype/reports/source_box_negative_control_v2_public_routes.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_public_routes_summary.json`
- `data/open_prototype/reports/source_box_negative_control_v2_panel_crops.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_source_status.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_blind_manifest.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_answer_key.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_review_template.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_packet_summary.json`
- `docs/source_box_negative_control_v2_m381_adjudication_packet.md`
- `tmp/source_box_negative_control_v2/source_box_negative_control_v2_contact_sheet.jpg`
- `tmp/source_box_negative_control_v2/source_box_negative_control_v2_panel_contact_sheet.jpg`
- `tmp/source_box_negative_control_v2/blind_packet/v2_neg_001_source_panel.jpg`

## Targets

| Priority | Row | Text | Why |
| ---: | --- | --- | --- |
| 1 | H-1678 | `+520-233-240-220-032+` | Best target-lane negative: has `240-220-032` but no following `002`. |
| 2 | M-124 | `+740-923-220-032+` | Compact Mohenjo-daro terminal `220-032`; Mayig overlap exists. |
| 3 | M-38 | `+740-690-435-255-220-032-240-235-002-390-125-632-032+` | Hard negative: `220-032` continues, but not into immediate `002`; later `002` stresses confounds. |
| 4 | M-381 | `+740-055-220-032-798-002-820+` | Tests whether later `002-820` is being mistaken for immediate `032-002`. |
| 5 | H-601 | `+740-717-233-220-032+` | Compact Harappa terminal negative against site/register overfit. |

## Public Route Acquisition

The public CISI India layer gives source-page routes for three Mohenjo-daro targets. The acquisition script generated three label-free panel crops; one is ready for token-box adjudication.

| Row | Public route | Current status |
| --- | --- | --- |
| M-381 | CISI India page `n129` / `India_0129.djvu` | strongest route; full source signband is visible and suitable for next token-box adjudication |
| M-124 | CISI India page `n139` / `India_0139.djvu` | source object is visible, but the inscription impression is tiny and low-contrast |
| M-38 | CISI India page `n55` / `India_0055.djvu` | source panel is visible, but the signband is not readable enough in the public crop |

Data-register cross-checks were also found for M-38 and M-124, but those are not source panels.

H-601 and H-1678 remain secondary-catalogue-only in this pass. The current local route is Bhaskar S1 icon catalogue text marking them as F2 / Unicorn; this is not source-grade evidence for the sign sequence.

`data/open_prototype/reports/source_box_negative_control_v2_source_status.csv` is the compact adjudication table. It has one row per target and records the best available route, the strongest local artifact/hash, the current admissible use, the blocker, and the next action. Its admissible-use split is:

| Use bucket | Rows |
| --- | --- |
| `adjudication_queue_only` | M-381 |
| `source_route_inventory_only` | M-124, M-38 |
| `not_admissible` | H-1678, H-601 |

M-381 has also been packaged as a one-item stage-separated adjudication packet. Stage 1 is blind tokenization from the anonymized source-panel crop; Stage 2 is catalog alignment against the answer key after tokenization is frozen.

The blind adjudication failed the clean-negative gate. Three independent blind reviewers returned token counts of 9, 13, and 9 against the seven-token catalog answer key, and all three flagged skip/merge risk in crowded regions. M-381 remains an ambiguity stress packet, not an admissible negative control.

## Promotion Rule

Passing these rows does not promote a crosswalk edge or structural claim. It only promotes them into a second blind negative-control packet.

Minimum evidence for each row:

- source panel or crop,
- same-line order,
- token boxes around `220` and `032`,
- immediate-next token or terminality proof,
- side/direction note.

Accepted crosswalk edges and accepted sign meanings remain zero.
