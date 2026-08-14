# Source-Box Blind Adjudication Protocol

Date: 2026-05-29

## Purpose

This protocol scores whether the source-visible `032-002-Y` candidate survives a visual false-positive gate.

The idea is simple. If a pattern is really in the artifact photographs, blind reviewers should find it in the images that contain it and fail to find it in matched negative images that do not. Reviewers see only neutral images, with no labels and no knowledge of which rows were positive. If they "find" the pattern in negatives too, the method is generating the result, not the corpus.

The task is not to read the inscriptions. It is only to decide whether a neutral source image visibly supports a same-line adjacent `032-002-Y` packet.

## Inputs

- Packet: `data/open_prototype/reports/source_box_blind_adjudication_packet.csv`
- Neutral images: `tmp/source_box_blind_packet_v1/`
- Truth key, sealed until scoring: `data/open_prototype/reports/source_box_blind_adjudication_key.csv`

## Reviewer Rules

1. Do not open the truth key before all calls are written.
2. Use only the neutral image and packet metadata.
3. Mark `yes` only when the image itself supports a same-line adjacent `032-002-Y` packet.
4. Mark `uncertain` when the signband is visible but token identity, adjacency, or line continuity is not secure.
5. Mark `no` when the target packet is absent or the image is too weak to support the call.
6. Do not use catalog text, original filenames, route notes, or prior knowledge of which rows were positive.

## Required Review CSV

Each reviewer writes:

```text
blind_id,call_yes_no_uncertain,confidence_low_med_high,brief_visual_rationale
```

## Scoring

Run:

```powershell
node data\open_prototype\tools\score_source_box_blind_adjudication.mjs
```

The scorer computes:

- yes-only false-positive rate: `false_positive / (false_positive + true_negative)`
- conservative negative-failure rate: `(false_positive + uncertain_negative) / all negatives`
- yes-only sensitivity: `true_positive / (true_positive + false_negative)`
- conservative positive-detection-or-uncertain rate: `(true_positive + uncertain_positive) / all positives`

## Acceptance Boundary

Passing this gate would prove very little, and that is deliberate. This gate can only support the narrow source claim that the same-line `032-002-Y` packet is not trivially produced by visually similar source images.

It cannot establish a sign meaning, phonetic value, translation, language family, or general structural finding by itself.

The source-visible candidate remains unaccepted if:

- any reviewer produces a material yes-only false-positive rate,
- negatives are mostly uncertain,
- positives are not consistently recoverable,
- or the missing `negative_220_032_next_not_002` image-backed control class remains fatal for the specific `A-220-032` lane claim.
