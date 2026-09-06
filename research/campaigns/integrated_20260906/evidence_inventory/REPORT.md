# Existing evidence inventory — 6 September 2026

The available evidence supports all four route searches. The most useful recovered input is Parpola's copper-tablet classification; the largest previously overlooked independent linguistic input is the complete held Monier-Williams XML. An independent Dravidian dictionary is not held as a standalone dataset, but comparative forms and a substantial Tamil compound lexicon are present inside the held Parpola 1994 volume.

`source_manifest.json` classifies 21 resource groups and three image collections with exact file paths, availability, hashes, namespaces, source relationships and limits. `recovery_manifest.json` records 13 exact-hash recoveries. No quarantined autopsy output is used as positive evidence. This inventory does not change the accepted-claim ledger or create blind evaluation material.

## Immediately usable inputs

| Input | Actual path | What it permits |
|---|---|---|
| Copper tablets | `recovered/Parpola_2008_copper.pdf` | Figures 1a/b, PDF indices 2/3, give 46 analytical classes with text-picture and text-text relations. Exact original source hash restored. |
| Fish and marker drawings | `recovered/glyph_059.png`, `060`, `065`–`073`, `211` | Direct comparison of publisher-drawn bases/modifiers; every recovered file matches its old manifest hash. |
| Sanskrit lexicon | `evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml` | 286,539 dictionary entry keys with source headword, definition, entry number and printed-page references; 67,574,805 bytes. |
| Sanskrit roots | Same assets directory: `data.json` | 2,259 lexical root rows with source script, gloss and grammatical fields. |
| Tamil comparison | `dravidian_lexical_examples.json` | Eight source-bound, visually checked entries: fish/star **mīṉ**, plus six compounds with segmentation, gloss, printed page and lexical references. |
| Wider Tamil lexicon | Held Parpola 1994 PDF, indices 296–300, printed pp. 279–283 | Appendix quotes 34 star compounds and 65 fish compounds from Tamil Lexicon and related sources. Text extractions and page renderings preserved locally for further exact-form adjudication. |
| Comparative Dravidian table | Same PDF, index 199, printed p. 182, Table 10.1 | Fish/star/glitter forms across named Dravidian languages. OCR destroys some phonetic distinctions; the rendered table is available. |

Paths beginning `recovered/` and the lexical-example filename are relative to this evidence-inventory directory; other paths are relative to the repository root.

## Observation limits that change inference

The copper figures aggregate physical examples into **analytical reconstructions**. The author uses broken lines for tentative reconstruction and excludes uncertain type assignments. The 46 classes are not 46 new independent objects. A thick frame indicates another class with an identical inscription; the cross-reference belongs to a defined relation, not a blanket equivalence between every sign and every animal. Route B received the recovered PDF immediately.

Catalogue glyphs describe a sign-list convention. Individual artifact photographs can disagree through damage, carving differences or transcription. The repository holds 6,870 files in the third-party `public/seal_images/` cache and 63 files in the curated `sign_crosswalk/source_panels/` collection; these counts include related surfaces and derived products. Object identity must determine evidential independence.

The Sanskrit dictionary is separable independent lexical content even though it was bundled inside a proposed-decipherment implementation. In contrast, that implementation's nine-entry `lexicons.json` is selected for its readings. Its `dhatuforms_vidyut_*.json` files are generated grammatical forms, not a corpus of individually attested words. Tamil lexical facts similarly remain distinct from Parpola's proposed Indus assignments, while the fish/star emphasis in his appendix is an explicit selection bias.

The source1977 Appendix II field-symbol codebook is held in `evidence/tmp/cisi_xml/The Indus Script. Text, Concordance and Tables -Iravathan Mahadevan_djvu.txt` and `.xml`. The retained 1977 codebook does **not by itself establish how the digital `fs80` field appends variants**. No archived app asset decoding `fs80` was located. Route B was told to retain the raw code and keep any major-code lexical label conditional.

## Remaining constraints

The complete 417-glyph source set was described and hashed in prior outputs but absent from the initial checkout. Twelve needed drawings were recovered; the other 405 can be recovered using the existing manifest if they become necessary. The copper PDF's plain URL returned 403; the same URL with `?download=1` recovered the original 552,079 bytes exactly, SHA-256 `1e68a8c2cf64bece75855987572c73133d215315e8432ad3f6f61db278f41cf1`.

The held cuneiform inventory contains 16 expanded attestation rows and 96 line-context rows. These supply independent linguistic forms and source metadata, but no same-object readable bilingual join was found. Same-site Meluhha and Indus records must remain separate observations.

No whole independent Dravidian etymological dictionary was found. The available source-bound lexical excerpts are sufficient to run explicit, limited rival hypotheses without inventing forms, but their size and selection cannot justify eliminating an entire language family. Route D received the exact-form records and broader appendix references.
