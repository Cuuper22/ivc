# Parpola Text No. 7 Scope / Namespace Gate

Date: 2026-05-26

## Question

This note is a gate: a recorded decision checkpoint that either lets a claim through or blocks it. It tests whether a published statement that "the same text appears on these objects" can be taken over into our own data as an exact match.

Terms first. Parpola 2019 is a published paper whose claims we test rather than trust; it numbers its texts ("text no. 7") and its signs ("sign no. 107") in its own scheme. That scheme is a separate namespace from the local Lipi sign codes (bare numbers like `220`, `415`) and from the Mayig catalog's `P###` feature ids. M- and H-numbers are Mohenjo-daro and Harappa artifacts. "Recurrence" means the same inscription turning up on more than one object. "Obverse" and "reverse" are the two faces of a tablet; the "companion" row is the other side of the same object in our catalog. "Source-dark" means no usable published image exists.

Can Parpola 2019 text no. 7 be used as the sign-number bridge explaining the H-940 / H-2147 / H-2148 obverse recurrence and M-77, or does it expose a broader sign-list and scope problem?

## Decision

It exposes a broader scope and namespace problem.

The M-77 conflict is not just one odd seal. The whole recurrence clause sits across at least three layers that are not yet source-aligned:

```text
Parpola 2019 standardized sign numbers and standardized rod drawings
Lipi / Mahadevan-style local numeric rows
Mayig Parpola-feature IDs
```

Until those are bridged object by object, Parpola text no. 7 cannot be used as a local-string identity key — a way of asserting that a published text and one of our catalog rows are the same string.

## Source Facts

Parpola 2019 says Figure 1 uses standard sign shapes, not the actual rod shapes, and tells the reader to consult CISI photos for the actual shapes.

The article then identifies text no. 7 as `M-2109` and `M-2111`. Figure 1 row 7 is visible in the stored crop:

```text
tmp/parpola_text7_scope_gate/derived/parpola2019_fig1_text_no7_m2109_m2111_crop.png
720x115
SHA256 499E8C9BE501380693030BB9ACF0C8EB0678F8F01D8892E52159A75E04C6BBD6
```

This is visual source evidence for the standardized row. It is not a prose transcription of the full Parpola sign-number sequence.

The surrounding prose gives three constraints:

```text
Text no. 7 is M-2109 / M-2111.
Parpola sign no. 107 uniquely ends text no. 7.
Without sign no. 107, the remaining part occurs on several Harappa incised tablets.
```

The later conclusion adds another constraint:

```text
Text no. 7 is not as such attested in seals.
Without the last sign no. 107, the rest forms the complete inscription of seal M-35.
```

That conclusion is important because the earlier recurrence paragraph names M-77 as a seal occurrence of the obverse text compared to text no. 7. So the article itself distinguishes at least:

```text
text no. 7 proper
text no. 7 minus final 107
the H-940/H-2147/H-2148 obverse sequence compared to text no. 7
seal parallels M-35 and M-77
```

Those cannot be collapsed into one exact local row.

## Local Rows

| Object | Local layer | Immediate result |
| --- | --- | --- |
| `M-2109` | `4042.1 +400-000-220-415+` | Local text no. 7 row has a damaged/unknown second token and does not exactly match `+520-220-415+`. |
| `M-2111` | `4044.1 +400-000-220-415+` | Same local text no. 7 row pattern as M-2109. |
| `H-2148` | `481.1 +520-220-415+`; `481.2 +110+` | H companion row is local `520-220-415`, not local `400-000-220-415`. |
| `H-940` | `1820.1 +520-220-415+`; `1820.2 +110+` | Same local companion family as H-2148. |
| `H-942` | `1822.1 +520-220-016+`; `1822.2 +033-700+` | Same frame, terminal stress. |
| `H-2240` | `816.1 +520-220-415+`; `816.2 +869-575+` | Exact local H companion recurrence but source-dark. |
| `H-2241` | `639.1 ]415-240+`; `639.2 ]000+` | Fragmentary local pressure. |
| `M-35` | `2563.1 +740-390-590-233-231-002-107+` | Named by Parpola as the seal form of text no. 7 minus final sign no. 107, but local row is seven signs and has terminal local `107`, proving numeric-label danger. |
| `M-77` | `2604.1 +832-390-803-002-861+` | Named in the recurrence paragraph, but local row is a five-sign seal string. |

## Critical Consequence

Do not equate numeric labels across systems.

The clearest warning is `107`:

```text
Parpola says sign no. 107 is the comb-like final sign of text no. 7.
Local M-35 ends in numeric token 107.
But Parpola says M-35 is text no. 7 without final sign no. 107.
```

So local `107` cannot be treated as Parpola sign no. 107 without an explicit sign-list bridge. The same caution applies to local `415`, local `016`, local `110`, and every M-77 token.

## Decision Tree

Current evidence rejects only the lazy identity path:

```text
Parpola prose recurrence -> exact local +520-220-415+ recurrence -> usable translation support
```

Surviving explanations:

```text
1. Sign-list namespace mismatch: Parpola numbers, Lipi numbers, and Mayig IDs differ.
2. Scope mismatch: M-77 may be a parallel to the H-obverse sequence compared to text no. 7, not text no. 7 itself.
3. Standardization mismatch: Parpola Figure 1 uses standardized signs while local rows encode a different transcription lineage.
4. Local-data mismatch: Lipi rows may preserve Mahadevan/local segmentation that does not reproduce Parpola's grouping.
5. Prior-work ambiguity or overreach: the prose recurrence may be broader than exact identity.
```

None is accepted yet.

## Accepted

```text
Parpola text no. 7 is source-located as M-2109 / M-2111 in Figure 1.
Parpola text no. 7 is standardized, not raw rod imagery.
Parpola sign no. 107 ends text no. 7 in Parpola's account.
Parpola separately names M-35 and M-77 in seal-parallel contexts.
Local rows do not give a direct exact match among M-2109/M-2111, H-2148/H-940/H-2240, M-35, and M-77.
The recurrence clause is now a source-critical sign-list/scope problem, not local-string evidence.
```

## Not Accepted

```text
Parpola sign no. 107 = local numeric 107
Parpola sign no. 189 = local 415 or local 016
local M-2109/M-2111 = local H-2148/H-940/H-2240 companion row
local M-35 = Parpola text no. 7 minus final sign by numeric identity
local M-77 = H companion row
any M-77 token mapping
any sign value
any phonetic value
any translation
```

## Next Action

The next useful source request is not another local row search. It is a sign-list bridge:

```text
Find or acquire the Parpola text no. 7 sign-number sequence from the article/source notes.
Find or acquire source transcription/sign-number tables for M-35 and M-77.
Only then compare to local Lipi/Mahadevan rows and Mayig feature IDs.
```

Until that bridge exists, keep the H-2148 reverse sign-no.-41 question separate from the obverse/companion recurrence problem.
