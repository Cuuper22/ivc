# Effective-Unicity Real-World Nonlinguistic Comparator

Date: 2026-05-29

## What This Note Is

This note tests our main structural instrument against real symbol systems that are known not to be writing. A comparator is a control corpus scored with the exact same instrument as the Indus data. Earlier comparators were synthetic — programs we wrote to fake structure. These are real: Pictish stones, kudurru deity symbols, totem poles, barn stars, Vinca symbols, weather icons. That matters, because a fake we designed is easier to dismiss than a genuine non-writing system that scores as well as our corpus.

The instrument is the masked-symbol test: hide one symbol at a time and ask a model to guess it from its neighbours. Top-1 is the share guessed exactly right; top-5 is the share where the right answer is in the first five guesses. "Max null >= observed" is the worst case across null runs — the same test on deliberately scrambled data — giving the fraction that matched or beat the real score.

## Result

The real-world comparator weakens the tempting Vector 2 overclaim. The Indus strict exact-collapsed masked top-1 score — "exact-collapsed" meaning strict dedup, where only byte-identical inscriptions are merged — is not by itself language evidence, because two real-world nonlinguistic or ambiguous symbol corpora meet or exceed it under the same masked-symbol instrument.

This does not erase the structural result. It sharpens it: the Indus working corpus has local context constraint beyond the earlier synthetic controls, but local predictability is also present in some non-writing or undeciphered emblematic systems. The surviving result is therefore an instrument and a boundary, not a decipherment.

## Input

Source bundle:

- `data/open_prototype/nonlinguistic/sproat2014/corpora.zip`
- source URL: `https://rws.xoba.com/data/non-linguistic-symbols/corpora.zip`
- SHA-256: `fb50ff5acb5221ba75e134cc7a36619e1d990b5680ad8681bcde5c447b6b8f73`

Generated artifacts:

- `data/open_prototype/tools/effective_unicity_realworld_nonlinguistic_comparator.mjs`
- `data/open_prototype/nonlinguistic/sproat2014/sproat2014_manifest.json`
- `data/open_prototype/nonlinguistic/sproat2014/sproat2014_extracted_sequences.csv`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_comparator.csv`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_realworld_nonlinguistic_null_iterations.csv`

Extraction policy: parse Sproat 2014 XML documents, read primary `<docText>` symbol titles, remove `<alternative>` blocks, filter primary sequences to lengths 2 through 8, and exact-collapse duplicate symbol sequences. This is a conservative primary-sequence extraction, but it is not a full edition of the source corpora.

## Comparator Rows

| System | Class | Rows | Tokens | Symbols | Top-1 | Top-5 | Max null >= observed |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Indus strict exact-collapsed | unread working corpus | 1,798 | 8,212 | 571 | 0.279591 | 0.534096 | 0 |
| Pictish stones | ambiguous symbol system | 187 | 684 | 78 | 0.450292 | 0.614035 | 0 |
| Mesopotamian kudurru deity symbols | known nonwriting pictorial system | 24 | 118 | 39 | 0.177966 | 0.500000 | 0 |
| Totem poles | known nonwriting emblematic system | 246 | 1,123 | 359 | 0.085485 | 0.300980 | 0.05 |
| Barn stars / hex signs | known nonwriting decorative system | 97 | 365 | 29 | 0.367123 | 0.673973 | 1 |
| Vinca symbols | ambiguous archaeological symbol system | 91 | 271 | 82 | 0.088561 | 0.276753 | 0.75 |
| Weather icons | modern nonlinguistic icon sequences | 4,018 | 20,090 | 16 | 0.265555 | 0.790543 | 0 |

Pictish stones and barn stars exceed the Indus masked top-1 reference. Weather icons sit just below Indus at top-1 while greatly exceeding it at top-5, largely because the symbol inventory is tiny and sequence conventions are highly constrained.

## Decision

Retracted interpretation: masked-sign top-1 predictability, even when it beats simple synthetic controls, is language evidence.

Surviving interpretation: the exact-collapsed Indus working corpus has measurable local context constraint, but the constraint is not specific to writing. Any language-family, phonetic, or sign-meaning claim still needs an external anchor — an independent source that fixes what at least one sign stands for — or a stronger discriminator.

No accepted claim count changes follow from this comparator.

