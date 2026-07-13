# M-111 terminal wheel-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_TWO_TERMINAL_WHEELS_LIPI_821_COLLAPSES_THE_PAIR_ON_M111`.

## Question

Lipi stores six tokens for `M-111`, ending in `821`. Mayig stores seven graphemes, ending in consecutive `P378 P378`, where `P378` is defined as a six-spoked wheel. The source question was whether the repeat represented two bounded signs, one compound split into components, or a duplicated transcription.

## Direct evidence

- Lipi row `2638.1`: `+740-920-320-233-001-821+`, text length 6, signs 6.
- Mayig `M-111A`: `P324 P160 P303 P058 P121 P378 P378`, grapheme count 7.
- CISI 1 PDF page 76 / printed page 40 shows both `M-111 A` and `M-111 a`.
- Each view shows seven bounded inscription units. The terminal pair consists of two separately closed, six-spoked wheel forms with visible space between their outlines. Their order and separation mirror across the impression and seal views.

The repeated Mayig grapheme is therefore source-supported. It is neither accidental duplication nor one source-bounded compound slot.

## Object-level normalization

- Structural source-unit count for `M-111` is `7`.
- Preserve two terminal wheel positions in sign-unit analyses: `... 001, <WHEEL6>, <WHEEL6>, END`.
- Treat Lipi `821` on this object as a macro or tokenization collapse spanning the visible pair, not as one structural unit.
- Do not assign Lipi `821` separately to either wheel and do not infer a global `821 = P378 P378` crosswalk. `M-111` is the only current Lipi-Mayig overlap row containing `821`; other Lipi `821` objects remain source-unchecked here.
- A macro-token analysis may retain `821` as one catalogue token, but must label its level explicitly and must not use its token count as the source-unit count.

## Research consequence

`M-111` can re-enter source-count and stored-order analyses only with the terminal pair expanded to two units. At source-unit level, `001` precedes the first wheel, the first wheel precedes the second, and only the second wheel is terminal. Existing statistics that treat `001-821-END` as two sign-level transitions conflate catalogue-token and graphic-unit levels for this object.

This gate does not establish whether the repeated pair functions as a semantic compound, nor does it accept a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m111_terminal_wheel_pair/M-111_A_a_CISI1_pdf76_print40.png`, SHA-256 `2F3F70764CBDB0196C4ACA6E70125DDA66071FCBBE7F7EC7DE27A1174C7EDE24`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m111.json`: `05E657F04752B0D8A7EBC08493C7A8C9A3DE1361775FABFBE150A47290D2AA70`.
- Mayig `P378.json`: `4CE5F4355D600A5885EC5C5070F97C3221B2F200431E5385FD69B762E9789117`.
