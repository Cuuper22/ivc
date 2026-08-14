# P041 / Parpola Sign 41 Namespace Table Decision

Date: 2026-07-12

Data table: `research/data/sign_crosswalk/p041_parpola41_namespace_table_20260712.csv`

## What this is and why it exists

Five different people numbered Indus signs, and none of them agreed. A namespace is one such numbering system: Parpola's, Wells's, Mahadevan's, Mayig's `P` codes, and the project's own Lipi tokens each form one. The same digits mean different signs in different namespaces.

That sets a trap. When a Parpola sign is numbered 41 and a Mayig feature is called `P041`, they look like the same thing written twice. They are not. Reading them as the same thing is a namespace collapse, and it manufactures a sign identification out of nothing but a coincidence of digits.

This note is the table that closes the trap for the numbers `41`, `112`, and `034`. It says which label belongs to which system, and which links between them are actually supported. It is bookkeeping, deliberately: the value of it is that it prevents a claim rather than making one.

## Scope

This closes the source-available namespace annotation for the several unrelated labels containing `41`, `112`, and `034`. It distinguishes:

- Parpola 2019 article sign no. 41, sourced to Parpola 1994 Fig. 5.1 sign no. 41.
- Mayig feature `P041`.
- the `V041` value inside Mayig's `parpola_graphemes` field.
- Lipi local tokens `041`, `110`, `112`, and `034`.
- Wells `W112` and Mahadevan `M034` as cross-references asserted by Mayig.
- the M-33 overlap record and every local `110` branch witness/control.

It accepts no value, meaning, phonetic reading, language identity, or translation.

## Exact decision

The numeric labels are not portable across namespaces. Point by point:

1. Parpola 2019 explicitly uses Parpola 1994 Fig. 5.1. Its sign no. 41 is the anthropomorphic/kneeling-person-with-raised-object family visible on printed p. 70 / PDF page 88.
2. Pinned Mayig `P041` instead carries `V141`, `W112`, and `M034`. These three are recorded as Mayig metadata assertions, not independently accepted source crosswalks.
3. Pinned Mayig `V041` occurs on feature `P301`, a small hatched box, not on `P041`. It is therefore rejected as a same-number route to Parpola 1994 sign no. 41.
4. Lipi local `041` has two rows, local `110` six, local `112` two, and local `034` 182. None is equated by its digits with another system.
5. The only current Mayig `P041` occurrence is terminal in M-33A. It positionally aligns with terminal Lipi local `112` in M-33 row 2561.1. One object showing one alignment is sequence pressure — a reason to keep looking — not a crosswalk.
6. Parpola's object-specific statement places sign no. 41 on the reverse of H-940, H-2147, and H-2148. The local shorter row in all three objects contains `110`, so `local 110 <-> Parpola sign no. 41` remains a P0 same-role hypothesis: the two labels may be filling the same slot, which is a question to test, not an identity to use.
7. H-2148 is the strongest source-visible anchor, because its one-sign and three-sign panels match the two local row lengths. It still lacks a source label tying the one-sign panel to the reverse side and to local row 481.2. H-940 remains visually unresolved. H-2147 remains component-level and row-unmapped. H-2100, H-2152, and Kanmer remain mandatory source-gated controls.

## Accepted and rejected relations

Accepted as source facts:

- Parpola 2019 sign no. 41 refers to Parpola 1994 Fig. 5.1 sign no. 41.
- Mayig asserts `P041 -> V141/W112/M034`.
- Mayig attaches `V041` to `P301` in the pinned feature set.
- M-33A terminal `P041` and M-33 terminal local `112` are one positional overlap.
- H-940/H-2147/H-2148 form the article's sign-no.-41 object branch, while the local metadata places `110` in each shorter row.

Not accepted:

- `Mayig P041 = Parpola sign no. 41`.
- `Mayig V041 = Parpola sign no. 41`.
- `Lipi 041 = Mayig P041`.
- `Lipi 110 = Parpola sign no. 41`.
- `Lipi 112 = Mayig P041` or Wells `W112`.
- `Lipi 034 = Mahadevan M034`.
- independent validation of Mayig's Wells or Mahadevan cross-references.
- any value, function, phonetics, language identity, meaning, or translation.

## Completion boundary

The current source packet cannot close the P0 `local 110 <-> Parpola sign no. 41` hypothesis, and it is worth being precise about why. The missing piece is a statement nobody has made, not an image nobody has looked at closely enough. Re-cropping or re-numbering the same files cannot supply it.

Closure requires source evidence that explicitly identifies the H-2148 one-sign face as the reverse side, and ties that physical face to both local row `481.2 +110+` and Parpola sign no. 41. It also requires an independent mapped recurrence or a source-grade outside control.

Until that evidence exists, the annotation is complete at `source_available_namespace_resolved_crosswalk_unaccepted`.
