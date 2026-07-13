# AO 22310 Shu-ilishu source-bound contact object

Original candidate date: 2026-06-11 America/Los_Angeles
Source-binding decision: 2026-07-12 America/Los_Angeles

Status: `source_bound_contact_object_no_indus_bilingual_no_external_anchor`.

This annotation is complete. It binds the local rollout image to Louvre accession `AO 22310` and its publication route. It does not earn an external-anchor claim. Accepted external anchors remain `0`.

## Exact local binary

- Repo file: `research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.jpg`
- Dimensions: `1552 x 802`
- Bytes: `678486`
- SHA-256: `7A5C7EC00DE1F01540F05A90B8F9E7752096A74391972CAB4F8CC05533D5B670`
- SHA-1: `E699D076FE1CC066B84AD9BC7C024132A2CC043C`
- Sidecar: `research/data/meluhha/source_images/louvre_AO22310_shu_ilishu_de_clercq_plate9_no83.provenance.json`

The dimensions, byte count, and SHA-1 match the Wikimedia Commons original. Commons identifies the image source as Louis de Clercq's 1888 catalogue. The Louvre record independently identifies the same object as De Clercq plate IX, no. 83.

## Object and publication binding

1. The Louvre collections record identifies the cylinder seal as `AO 22310`, in the Department of Near Eastern Antiquities.
2. The Louvre describes the language as Akkadian and gives the inscription as “Shilishu, the interpreter of (the land of) Meluhha.”
3. The same record cites Louis de Clercq and Joachim Menant, *Collection de Clercq*, volume I (1888), plate 9, no. 83.
4. Wikimedia identifies that 1888 publication as the source of the exact local rollout image.
5. The BnF Gallica IIIF route exposes the original plate IX at canvas `f310`.
6. Gregory Possehl reports that Steve Tinney reconfirmed the reading from a fresh impression made from the original seal in 2004.

Routes checked:

- Louvre: `https://collections.louvre.fr/ark:/53355/cl010147038`
- Wikimedia original: `https://commons.wikimedia.org/wiki/File:Akkadian_cylinder_seal_with_inscription_Shu-ilishu,_interpreter_of_the_Meluhhan_language,_Louvre_Museum_AO_22310.jpg`
- De Clercq plate IX, BnF IIIF: `https://gallica.bnf.fr/iiif/ark:/12148/bpt6k927127w/canvas/f310`
- Penn Museum / Possehl: `https://www.penn.museum/sites/expedition/shu-ilishus-cylinder-seal/`

## Chronology and provenience correction

The old candidate's unqualified `~2020 BCE` is withdrawn.

- Louvre catalogue date: Akkadian period, `2340-2200 BCE`.
- Possehl/Porada stylistic discussion: Late Akkadian, `2200-2113 BCE`, possibly Ur III, `2113-2004 BCE`.
- `ca. 2020 BCE` appears only under the low chronology cited by Possehl and is not used as the object's single fixed date here.

The Louvre's `Babylonia = Sumer` entry is explicitly an attribution by style. It is not excavated provenience. Possehl states that the De Clercq collection was assembled through dealers with little or no provenience data and that AO 22310's archaeological findspot is unknown.

## Hard research boundary

- AO 22310 contains an Akkadian inscription about an interpreter of Meluhha.
- It contains no securely identified Indus text.
- It is not an Akkadian-Indus bilingual.
- It provides no Indus sign value, phonetics, reading, language-family identification, or translation.
- The reasonable association of Meluhha with the Greater Indus world is contact context, not an object-level script bridge.
- Possehl explicitly treats a true Akkadian/Meluhhan bilingual as something that might exist, not something AO 22310 already supplies.

## Decision

Decision: `COMPLETE_SOURCE_BOUND_CONTACT_OBJECT`.

Use as: a source-bound attestation that Akkadian scholarly tradition described a person as an interpreter of Meluhha.
Do not use as: an external Indus-script anchor, bilingual, phonetic constraint, sign reading, or proof of an excavated findspot.

Accepted-count changes: none.
