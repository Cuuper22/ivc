# M-381 Source-Box Negative-Control Packet

Date: 2026-05-29

This note sets up a test on a single object, M-381, and states the rules the reviewer must follow.

Terms first. A "source-box" is a box drawn on a published object photograph around each sign a reviewer can see; a "token box" is one such box around one sign. A "negative control" is an object chosen because its catalog text does not contain the pattern under test, so any reviewer who finds the pattern there is producing a false positive. A "packet" is the bundle of images and instructions handed to the reviewer. "Blind" means the reviewer works without the catalog text or object identity. "Adjudication" is the scored decision that follows. A "route" is the trail from a catalog row to a real, citable source record. Numbers like `032`, `002`, and `798` are Lipi catalog sign codes, not readings. M- numbers are Mohenjo-daro artifacts.

This packet upgrades one v2 negative-control target from route inventory to adjudication queue. It does not promote a claim.

Result after blind review: failed clean-negative gate. See `docs/source_box_negative_control_v2_m381_blind_adjudication.md`.

## Files

- `data/open_prototype/reports/source_box_negative_control_v2_m381_blind_manifest.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_answer_key.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_review_template.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_packet_summary.json`
- `tmp/source_box_negative_control_v2/blind_packet/v2_neg_001_source_panel.jpg`

## Boundary

The source-status gate — the checkpoint that decides how far an object's evidence goes — says M-381 is `source_visible_ready_for_token_box_adjudication`, meaning a usable published image exists, not source-confirmed. The crop is visually usable, but the claim remains unearned until token boxes and a stage-separated review are recorded.

Accepted-claim increments: zero.

## Protocol

Stage 1 is blind tokenization:

- use only `tmp/source_box_negative_control_v2/blind_packet/v2_neg_001_source_panel.jpg`;
- do not use the CISI identifier, Lipi identifier, or catalog text;
- box every visible sign token in visual order;
- record token count, box coordinates, direction basis, and uncertainty.

Stage 2 is unblinded catalog alignment:

- use the answer key only after Stage 1 is complete;
- align the blind token boxes to `+740-055-220-032-798-002-820+`;
- decide whether a visually distinct token intervenes between catalog `032` and catalog `002`;
- record whether adjacent `032-002` is source-visible, uncertain, or visually rejected.

## Why This Exists

The first source-box blind packet failed because reviewers found plausible `032-002-Y` packets in negatives at unacceptable rates. That made the visual method invalid until harder negatives were added. M-381 is the first source-visible `negative_220_032_next_not_002` row in the v2 queue: the metadata string says `032` is followed by `798`, with `002` later. If the crop cannot support that negative visually, the visual packet method stays dead.
