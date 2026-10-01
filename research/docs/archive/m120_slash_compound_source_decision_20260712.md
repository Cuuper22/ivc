# M-120 slash-layout source correction

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SEVEN_UNITS_SLASH_IS_2D_ASSOCIATION_MAYIG_OMITS_858`.

This supersedes the earlier six-unit decision in this file. That decision counted only the six signs in the main inscription line and missed the detached diamond below it.

## What this is and why it exists

This is a source decision: a written ruling that settles one specific question against the source images, so that later analysis does not have to keep guessing. This one covers one object, `M-120`, and it corrects an earlier ruling recorded in this same file.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `858`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P324`, and each of its entries is called a grapheme. Lipi writes a slash, as in `858/740`, when two signs stand in some relation other than plain succession. The question here is what that slash records on this object, because the answer decides whether the inscription is one line of seven signs or a line of six with a separate sign set below it.

That distinction is not cosmetic. Most analyses read an inscription as a flat sequence, so anything written into the sequence gains an order relation whether or not the object has one.

## Direct evidence

Each item below is something a pinned catalogue record or a published plate actually shows.

- Lipi row `2647.1`: `+858/740-100-585-741-840-346+`, reported text length 7, signs 7, direction `R/L`.
- Mayig `M-120A`: `P324 P009 P288 P325 P349 P044`, grapheme count 6.
- Mayig defines `P363` as a diamond containing two adjacent boxes on a short internal stem and mediates it to Wells `W858`. It mediates the main-line jar `P324` to `W740`.
- CISI 1 PDF page 77 / printed page 41 publishes `M-120 A` and `M-120 a`.
- Both views show six bounded signs in the main inscription line plus the `858` diamond on a detached lower line. The diamond has clear whitespace around it and neither touches nor overlaps the `740` jar.

So the source-visible count is seven. The Lipi slash records a two-dimensional association — this sign goes with that one, positioned below it — not a fused one-sign ligature. Mayig omits the detached `858` position.

## Object-level normalization

- Preserve the six-sign main line as `740-100-585-741-840-346`.
- Preserve a separate detached `858` / `P363-like` unit associated spatially with `740`.
- Do not serialize `858/740` as either one source sign or an ordinary sequential `858-740` edge. The slash carries layout information.
- A linear-only model must either encode the detached unit and its layout relation separately or exclude M-120 from adjacency calculations; inserting it into the main line would invent an order relation.
- Normalize the Mayig object by attaching `<MISSING_DETACHED_P363_LIKE>` to the `P324` position at analysis level. Do not edit `m120.json` or either raw corpus.

## Research consequence

The queue label `slash_compound_count_policy_reconciles` is rejected for M-120. Lipi's reported count of seven is source-supported, while Mayig is incomplete for a secondary line/layout element. This is the first adjudicated case here where the fix is to preserve two-dimensional layout rather than to pick whichever catalogue offers the longer flat list. Picking the longer list would have produced a sequence the object does not have.

No global `858 = P363` edge, sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- `research/data/sign_crosswalk/source_panels/m120_slash_compound/M-120_impression_A_CISI1_pdf77_print41.png`, SHA-256 `D505326F02DEE47DF46F58C17D78B0EE609B152F00A712B779C7C2BD89DD68C4`.
- `research/data/sign_crosswalk/source_panels/m120_slash_compound/M-120_seal_a_CISI1_pdf77_print41.png`, SHA-256 `412CD6C4EFF9F3E9908412A416F86723F2AE89E3505AFA15B601BA631D6C5433`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m120.json`: `88EB3E69343B04898FE6148607178681C556CDA05F861FD953D1AAFD43BF92C7`.
- Mayig `P363.json`: `B36505090D9DCE7A2E2285DC5513DF9D7BE39030913DE56354E19397570DF5B0`.
