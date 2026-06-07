# 032-002-861 / 002-390-X Blind Boundary Packet

Date: 2026-05-30

## Purpose

This packet tests whether the visible sign-band segmentation survives without object IDs, target/control labels, or expected sign numbers. It is an adjudication packet, not a decipherment result.

## Blind Materials

- Blind sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\blind_boundary_packet_alpha\blind_boundary_packet_alpha_blind_sheet.jpg`
- Blind manifest: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_blind_manifest.csv`
- Response form: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_response_form.csv`

The blind sheet and individual blind panels expose only neutral IDs. Readers should segment the visible marks, record boundaries in both left-to-right and right-to-left descriptions if needed, mark repeated visual clusters across panels, and reject panels that cannot be segmented.

## Separated Key

- Sealed key: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_sealed_key.csv`
- Neutral overlay manifest: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_neutral_overlay_manifest.csv`
- Neutral overlays directory: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\blind_boundary_packet_alpha\neutral_overlay_key`

The overlays preserve neutral IDs only. Object IDs, local texts, branch labels, and roles are stored only in the sealed key CSV.

## Decision Rule

The `125` branch only survives this gate if blind readers independently recover a plausible local segmentation for the two strict target panels and do not collapse the non-target controls into the same visual outcome. If the strict panels require object labels, expected sign numbers, or catalog order to become readable, then this packet demotes the visual side of the `125` branch claim.

## Current Status

No value, phonetic reading, sign meaning, language identity, or translation is accepted. The packet exists to force a blind boundary decision before the campaign treats `002-390-X` as stronger than boxed-window-compatible.
