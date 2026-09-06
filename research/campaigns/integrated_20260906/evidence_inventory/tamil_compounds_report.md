# Tamil compound extraction

Extracted **all 93 category-marked entries** across the five held Appendix pages, printed pp. 279–283 / PDF indices 296–300. The JSON preserves the printed category, form transcription, printed hyphenation, gloss summary, full raw entry OCR, lexical notes/references, exact source regions, uncertainty and source hash. The extraction script executes from the repository without external retrieval.

| Source category | Headword rows | Interpretation |
|---|---:|---|
| F | 58 | Fish compound |
| S | 28 | Star compound |
| F(S) | 4 | Fish compound; only its first component has a star sense |
| SF | 3 | Both fish and star compound senses |

The **65 fish-bearing entries** match the author's reported 65. There are **31 star-bearing headword rows**, while the author reports 34 star compounds. The two star senses under `ai-m-mīṉ` and three under `cem-mīṉ` supply three additional star senses, numerically reconciling 34; this is a plausible counting explanation, not a verified statement of the author's convention. No missing entries were invented to force agreement.

Every marked row is included. Two printed F labels on p. 281 were absent from the embedded OCR and were restored from the visible source page. Paragraphs that continue into another column or page retain both source regions. Three subordinate compounds are preserved within their parent entries: `aṟu-mīṉ-kātalaṉ`, `āṟā-mīṉ-aṟa-v-ōṭṭu` and `cem-mīṉ-vayiṟam`. They are not counted as additional category-marked headwords.

**89 forms are eligible for exact-form candidate searches. Four carry explicit uncertainty:** `arakkulā-mīṉ`, `kaṭanākku-mīṉ`, `kōṉ-mīṉ` and `nāṉ-mīṉ`. They remain in the inventory with raw source text and coordinates. Their undecided diacritics or contraction must not be silently resolved to improve a phonetic fit. Definitions and citations retain their embedded OCR, which is sometimes noisy; short English gloss summaries are separately labeled as summaries. The full inventory supersedes the earlier eight-entry sampler and retains finer consonant distinctions such as `kuṟu-mīṉ`.

A useful source-supported lexical comparison is now isolated in `tamil_compounds_relations.json`:

- `kaṉ-mīṉ`: source explicitly gives `kal`, “stone,” DEDR 1298.
- `kōḻi-mīṉ`: source explicitly gives `kōḻi`, “cock, fowl,” DEDR 2248.
- `kallu-k-kōḻi-mīṉ`: source explicitly gives `kallu`, “stone,” DEDR 1298, and `kōḻi`, DEDR 2248.

The shared dictionary reference supports linking the stone components lexically. A productive rule explaining `kal → kaṉ / kallu` and the visible intervening `k` remains a separately charged grammatical hypothesis. The source does not establish an Indus sign assignment or a general phonological rule.

All entries come from Parpola's deliberately fish/star-centered appendix. They provide independent comparative-language forms quoted in decipherment scholarship; their source selection is not independent of that scholarship's hypothesis. Broader language-family exclusion cannot be inferred from failure against this finite inventory.
