# M-77 Parpola Recurrence Conflict Gate

Date: 2026-05-26

## Question

This note is a gate: a recorded decision checkpoint that either lets a claim through or blocks it. The claim under test comes from published prior work.

Background terms. M-77 is a unicorn seal from Mohenjo-daro; H-numbers are Harappa artifacts. "Source-visible" means we have located the object in a published plate image, not just a catalog transcription. "Lipi" is the local sign-code catalog; "Mayig" is an independent sign-code catalog (P-numbers). Parpola 2019 is a published paper whose claims we test rather than trust.

Parpola 2019 says the obverse text of the H-940 / H-2147 / H-2148 group occurs on H-942, H-2240, H-2241, and also as the sole text of unicorn seal M-77. Does source-visible M-77 close the companion-text recurrence, or does it create a source-normalization conflict — a case where the published claim and the source evidence do not line up?

## Decision

It creates a conflict. The recurrence sentence can no longer be used as closed support for the H-2148 companion row.

Here is why. The source-visible M-77 layer is a five-sign unicorn-seal text:

```text
local Lipi:  +832-390-803-002-861+
Mayig:       P366 P086 P364 P122 P385
```

That is not the local three-sign `+520-220-415+` / `+520-220-X+` companion family being tested for H-940 / H-2147 / H-2148. M-77 therefore becomes an adversarial control on the prior-work sentence — evidence held against the claim, to stress it — not supporting evidence for an accepted local crosswalk.

## Local Matrix

| Object | Local rows | Current role |
| --- | --- | --- |
| `H-2148` | `481.1 +520-220-415+`; `481.2 +110+` | Cleanest sign-no.-41 branch target; same-side identity still pending. |
| `H-940` | `1820.1 +520-220-415+`; `1820.2 +110+` | Source-visible `110` branch witness, but public-quality split remains. |
| `H-2147` | `673.1 ]110+`; `673.2 ]220-415+` | Object-visible component-level pressure only, not clean single-sign witness. |
| `H-942` | `1822.1 +520-220-016+`; `1822.2 +033-700+` | Source-visible full-signband stress/control. |
| `H-2240` | `816.1 +520-220-415+`; `816.2 +869-575+` | Exact local recurrence, source-dark in checked public layer. |
| `H-2241` | `639.1 ]415-240+`; `639.2 ]000+` | Fragmentary local pressure, source-dark in checked public layer. |
| `M-77` | `2604.1 +832-390-803-002-861+` | Source-visible five-sign seal text; adversarial recurrence-control conflict. |

("Source-dark" means no usable public image or plate was found in the checked sources.)

## Source Evidence For M-77

M-77 is source-visible on CISI India IA leaf `n68` / printed p. 33 under the page header for Mohenjo-daro seals 75-79. (CISI is the published Corpus of Indus Seals and Inscriptions.) Both the face label `M-77 A` and impression label `M-77 a` are visible.

Source page:

```text
tmp/m77_parpola_recurrence_gate/cisi_india_n68_w1200.jpg
2398x3427
SHA256 EB7A4356C5D76844301D4B1A672D76AF675D4CDBE23BA57594AD75C6E01BA027
```

Stored crop set:

```text
tmp/m77_parpola_recurrence_gate/derived/M77_face_A_panel_v3_from_cisi_india_n68.png
790x560
SHA256 9BE8D6598EA08B41EFA2B97629BD080AC441D681CC9D84D2DF43DB3A836C4442

tmp/m77_parpola_recurrence_gate/derived/M77_face_A_signband_strict_from_cisi_india_n68.png
720x230
SHA256 308A212503B508CBB505507822FAE8E63BB2FF8DA547903D2962AE7C6F317CC2

tmp/m77_parpola_recurrence_gate/derived/M77_impression_a_panel_v3_from_cisi_india_n68.png
820x650
SHA256 68EF996CF428C79EEFF46B7210FE679BB0D3D3D73BDE8800ECCFAE4B3718BE20

tmp/m77_parpola_recurrence_gate/derived/M77_impression_a_signband_strict_from_cisi_india_n68.png
760x260
SHA256 E3ABB4E00CD3EA34AF1477F4903B7D5596DD47361E05A0C767FFD0450C5D0AA9
```

The `n33` first download in this folder is a wrong-leaf check and must not be cited as M-77 panel evidence.

## What This Does To The H-2148 Branch

It does not kill the H-2148 reverse-side sign-no.-41 branch.

It does kill the stronger shortcut:

```text
Parpola says the obverse text recurs on M-77
therefore the local H-2148 companion row is source-normalized by the named controls
therefore the H-2148 branch has a settled companion recurrence
```

That shortcut is now blocked.

The surviving H-2148 statement remains narrower:

```text
Parpola reverse sign no. 41 -> local 481.2 +110+ -> Kenoyer 2005 one-sign panel by count
```

That is still `strong_same_role_inference`, not an accepted same-side source bridge.

## Live Explanations

The M-77 conflict can mean several different things:

```text
1. We are misreading the scope of Parpola's "text no. 7" recurrence clause.
2. Parpola's sign-list / standardized text convention does not map directly onto local Lipi strings.
3. Local Lipi row mapping or segmentation for one of the controls is incomplete.
4. Parpola's recurrence is broader formula-family recurrence, not exact text identity.
5. M-77 needs a source transcription/sign-number bridge before it can be compared to H-940/H-2147/H-2148.
```

None of these is selected yet.

## Accepted

```text
M-77 is source-visible on CISI India n68 / printed p. 33.
M-77 is locally a five-sign seal string: +832-390-803-002-861+.
Mayig also records M-77A as a five-grapheme unicorn IV seal string.
M-77 does not match the local +520-220-415+ or +520-220-X companion family.
Parpola's obverse recurrence sentence is now conflict-gated, not closed support.
```

## Not Accepted

```text
local 832/390/803/002/861 maps to local 520/220/415
Mayig P366/P086/P364/P122/P385 maps to the H-2148 companion text
M-77 proves or disproves Parpola sign no. 41
H-2148 one-sign side = Parpola sign no. 41
local 415 = local 016
any sign value
any phonetic value
any translation
```

## Next Action

Acquire a source transcription or sign-number table for M-77 and Parpola text no. 7, then decide whether the conflict is a sign-list convention issue, a local-corpus mapping issue, a broader formula-family claim, or a prior-work overreach.

Until then:

```text
Use M-77 only as a source-visible adversarial control.
Keep H-2240/H-2241 in acquisition.
Keep H-942 as a source-visible full-signband stress/control.
Keep H-2148 same-side identity pending.
```
