# Route D: explicit phonetic systems and the assumptions that select them

No sound assignment or language identification is accepted. This run nevertheless produces explicit competing readings, a narrowly conditional `211 = ka` result, and connected Tamil morphological systems whose extra rules can be inspected and challenged. It does not substitute sign prediction for phonetic inference.

## Executed command

From the repository root:

```sh
python research/campaigns/integrated_20260906/route_d/run_all.py
```

Python standard library only. `outputs/execution_manifest.json` records the executed programs and hashes. Raw source records are unchanged. All corpus comparisons are retrospective.

## Independent linguistic material

The archived Monier–Williams XML contains **192,482 distinct alphabetic headwords**, retaining case-sensitive source transliteration, entry IDs and printed page/column references. Its digitization header credits Universität Köln, 2013. Of those, **259** have an entry explicitly matching the declared “a fish / a kind of fish” gloss filter. The filter can select a polysemous word; it does not prove that a particular Indus sign denotes its fish sense.

The held Parpola 1994 appendix supplies **93 category-marked comparative Tamil rows** over printed pages 279–283. The evidence specialist visually transcribed **89** sufficiently clearly for exact-form analysis; four remain excluded. **88** of the reliable rows end in `mīṉ`, with **86 distinct qualifier surfaces**. The inventory preserves homophones and source sense distinctions: its fish-name rows and star-name rows are not interchangeable. The appendix is selected for a fish/star investigation, not an unbiased Tamil dictionary. One unhyphenated `vīḻmīṉ` receives a declared candidate segmentation at the repeated suffix; it is not mislabeled printed hyphenation.

These are independent language facts quoted in held resources. Attaching any of them to an Indus sign is a separate hypothesis. The archived proposed `words.csv` translations, `xlits.csv` phonetics and generated Vidyut morphology are not independent pronunciation anchors. Earlier Meluhha pattern matches supply no validated object-level bilingual bridge. Route B supplies useful exclusions but no independently identified lexical referent.

## Exact shared-marker search

The initial model treats four fish bases `59,65,67,72` as lexical/logographic roots; their marked counterparts `60,66,68,73` share an added pronunciation represented separately by `211`. Both prefix and suffix realization are searched. All nonempty word splits and every eligible dictionary root participate; there is no vocabulary or string-length cutoff. The enormous assignment spaces are counted exactly by factoring the shared-marker constraint rather than enumerating every permutation.

| Declared semantic and writing assumptions | Appended-marker systems | Prepended-marker systems |
|---|---:|---:|
| Four distinct roots; no semantic anchor | 640,372,456,145,280 | 280,368,192,473,592 |
| Base 59 alone must have a fish gloss | 3,976,191,215,670 | 844,448,311,818 |
| All four bases must have fish glosses | 1,012,704 | 126,504 |
| All four bases **and all four marked forms** must have fish glosses | **360** | **0** |
| Same eight-form constraint, but homophony allowed | 1,317 | 14 |

Under the fourth row only, the marker string is uniquely **`ka`**. Six source-attested root/extension pairs survive: `cezwa→cezwaka`, `rAjIva→rAjIvaka`, `pallava→pallavaka`, `trikaRwa→trikaRwaka`, `daRqapAla→daRqapAlaka`, and `siMhatuRqa→siMhatuRqaka`. Assigning four distinct roots to four signs gives `6×5×4×3 = 360` systems. Source entry IDs, fish-sense passages and page references are in the outputs.

This is a real conditional constraint, not an independent identification of `ka`. It requires eight unestablished Indus fish-name assignments and distinct pronunciations for the bases. Allowing homophony restores **22 appended marker strings**. Requiring dictionary membership alone admits many homographic root/derived pairs whose meanings are unrelated; the eight-form semantic condition was added specifically to remove that defect.

The direct semantic-category rival is decisive about specificity. Applying the **same search** to **451 bird headwords** again yields only `ka`, now over seven root pairs. **542 tree headwords** yield `ka` over twelve pairs, plus `ja` and `pa` over four pairs each. In sixteen fixed-seed, 259-word subsets of each larger category, `ka` survives five bird subsets and five tree subsets; no other suffix survives any of those subsets. These are matched selection diagnostics, not significance probabilities. The suffix is not a fish-specific discovery; the lexicon's general word-extension structure selects it.

## Two graphical operations constrain the mixed systems

Route A supplies an actual orthographic lattice, not an invented roof sound:

```text
65  → 87–59
60  → 59–211
66  → 87–60  → 87–59–211
```

The complete `267–99` construction occurs as `267–99–66` on objects 7249, 7251, 7255, 7267 and 7269; as `267–99–87–60` on 6211; and as `267–99–87–59–211` on 1551. Exact row IDs, including side/line codes, come from the shared snapshot in `tamil_joint_worked_readings.json`. These are conditional spelling relations; they do not independently name the depicted fish, a count, or a modifier.

A literal sound-by-sign reading puts the base between the two markers, in stored order `87–59–211` or the global reverse. The full source Tamil inventory yields **zero exact concatenative two-modifier squares**, even before imposing that linear order. The 259 MW fish headwords also yield zero squares when all four nodes must independently have fish senses. These zeros apply to the held vocabularies and the tested exact-concatenation model; unattested ancient words or different graphical roles remain possible.

A separately charged mixed morphological parser can use two source lexical triangles:

- `kaṉ-mīṉ`, `kōḻi-mīṉ`, `kallu-k-kōḻi-mīṉ`: the source associates `kaṉ` with lemma `kal` and `kallu` with the same stone entry, DEDR 1298. The cock/fowl component is DEDR 2248. Treating these as one context-realized modifier family is an inference, not an established general sandhi law.
- `ney-m-mīṉ`, `vāṉ-mīṉ`, `ney-vāṉ-mīṉ`: the source preserves the intervening `m` in the simple compound. Two source entries for `vāṉ-mīṉ` supply semantic alternatives, not extra independent sound systems.

| Candidate | Base 59 | Roof 87 | Ticks 211 | Doubly modified 66 |
|---|---|---|---|---|
| D-TAMIL-JOINT-00 | mīṉ | kal | kōḻi | kallukkōḻimīṉ |
| D-TAMIL-JOINT-01 | mīṉ | kōḻi | kal | kallukkōḻimīṉ |
| D-TAMIL-JOINT-02 | mīṉ | ney | vāṉ | ney vāṉ mīṉ |
| D-TAMIL-JOINT-03 | mīṉ | vāṉ | ney | ney vāṉ mīṉ |

Each system needs a fixed canonical modifier order and context-sensitive boundary realization; the stone system additionally needs the declared `kal/kaṉ/kallu` relation. The executable parser gathers typed modifiers from fused or separate signs and realizes their shared lexical state. It does **not** merely print the same answer for four hard-coded strings. Repeated unsupported operators remain unresolved. Ordinary linear phonetic concatenation fails, so the reorder and boundary rules remain explicit costs and dependencies.

Both assignments of the two modifiers survive. An anonymous classifier model and a model using `87` as a context-specific two-stroke quantity also survive as rivals. No context-specific numerical value is converted into a sound anchor.

## What actually propagates

The four mixed parsers produce worked partial readings of the three `267–99` spellings, preserving `267` and `99` as unread. These are consequences of the chosen operations and lexical premises, not three independent confirmations of a translation.

Route A's additional pair `65–70–211` on object **1380** and `87–59–71` on **2452** gives a useful new-family consequence. All four parsers produce the same abstract analysis: the known roof construction followed by a ticks-modified **unread root 70**. No pronunciation for 70 is forced. The execution is saved in `new_fish_family_propagation.json`.

A narrower bound-morpheme claim is refuted: `211` immediately follows one of the four tested fish bases in 101 strict occurrences, but not in another 93. **49 complete objects** contain `211` without any of those four base or marked fish signs. Object 2516 has separate recorded lines `86` and `211`; it is not misrepresented as an isolated one-sign object. This rejects only the global four-core-fish-bound model, not local fish compounding or use with other roots. C's independently executed layout comparison finds the same `86–211` string inline on 4474 and 4518, preserving the line-order hypothesis.

## Executed next test: does the roof write two fish?

Composing A's roof with C's one-frame `87–59 ↔ 59–59` predicts `65→59–59`, `66→59–59–211`, or, if the quantity distributes over the marked fish, `66→60–60`. The next run searched **all 123 distinct-expression occurrences of 65 and 12 of 66**, then permitted one paid context edit with at least two fixed anchors. It excluded **195 objects** in the defining `267–99` frame, including their exact-expression aliases and other faces. A separate lane used visible partial compact observations against strict target expansions.

| Composed prediction | Exact counterparts outside defining objects | One-context-edit pairs outside defining objects | Partial compatibility pairs |
|---|---:|---:|---:|
| `65→59–59` | 0 | 0 | 0 |
| `66→59–59–211` | 0 | 0 | 0 |
| `66→60–60` | 0 | 0 | 0 |

The group-scope expansion of 66 has one exact counterpart inside the original `267–99` frame. There are 39 eligible partial occurrences of 65, but none of 66 after the specified exclusions, so the latter partial zeros are absence of opportunities.

The roof spelling `65→87–59` retains two exact pairs outside the frame, six one-edit pairs and two partial compatibilities. A generic alternative `65→65–59` obtains seven one-edit pairs, demonstrating that relaxed contextual similarity alone does not identify the number two. Of the partial roof witnesses, **2275 versus 1008** retains four certain surrounding signs and only an unknown prefix; **7283 versus 4019** also retains four anchors but requires setting aside two doubtful catalogue IDs. Those are recorded separately. The stronger written-repetition interpretation earns no transfer in this bounded search; a missing counterpart remains unknown, not a negative inscription.

## Identifiability and continuation

The compact constructed control recovers a unique mapping once a supplied independent anchor is present, preserves two segmentation alternatives without it, predicts the same withheld recombination under both, handles a silent classifier, and rejects a contradictory withheld form. A full-lexicon bijective sound relabeling leaves every tested root/extension count unchanged. This proves an exact symmetry of this objective under correspondingly renamed lexical forms; it is not a claim that every possible linguistic comparison is nonidentifiable.

There are **zero independently scorable target pronunciations** in the supplied Indus evidence. Consequently sound accuracy, phonetic held-out success and deciphered-text coverage cannot be reported. The model outputs preserve candidate readings and unknown spans rather than silently supplying them.

The remaining concrete experiment is to use the existing **2275/1008** roof relation, whose retained suffix is `67–336–89–211`, as a separate construction when fitting the scope of `87` and `211`: test a local compound boundary after the roof fish against a quantity scope extending over the retained suffix. Keep 7283/4019 in a sensitivity lane because of its doubtful IDs. Freeze each scope rule before comparing the already held occurrences of `67–336–89–211` and the corresponding cross-face field roles. This asks whether the candidate operators act on a single root or a larger field; it does not pretend that either outcome alone identifies their sounds. Additional dictionary resemblance or reuse of the original six pairs cannot count as phonetic confirmation.

Steps D31–D37 were executed to the available evidence boundary. Independent phonetic validation remains specifically blocked by the absence of a grounded Indus-to-pronunciation bridge; the competing executable systems and their exact continuation state are preserved.
