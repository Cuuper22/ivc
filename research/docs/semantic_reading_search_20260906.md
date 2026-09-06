# Compositional reading search — 6 September 2026

Status: unfinished decipherment research. No translation, sound value, sign meaning, or language identification is established. The requested major decipherment breakthrough has not been achieved. These are search results, not new accepted claims.

## What was actually attempted

The run searched for mechanisms that could propagate a reading across different inscriptions: a graphic modifier represented elsewhere by a separate sign; a complex glyph written as its visible parts; a short expression on one face standing for a longer expression on another; and repeated signs replaced by a count/operator plus one sign. It did not train a phonetic decipherer or assign guessed sounds.

The source is the frozen Mahadevan 1977 public concordance already in this repository. Exact strings are collapsed. All 417 publisher glyph illustrations were acquired and inspected as contact sheets; the declared graphical decompositions remain visual hypotheses, not changes to the source transcription. Parpola's copper-tablet figures were used to investigate text–image and text–text correspondences. His earlier pictorial-bilingual proposal is prior scholarship, not a discovery of this run.

## Executed searches

The input contains 2,575 eligible lines and 1,659 distinct exact strings. The tool tests 30 base/modified-glyph pairs against all 417 possible separate markers, in both orders. It additionally tests 21 declared literal-part decompositions. It constructs 167 candidate short/long correspondences from different explicitly numbered, single-line faces of the same object, and searches for those substitutions inside longer matching contexts. Finally, it searches repeated runs for alternative marker-plus-base expressions.

Faces are determined from the tens digit of the source's side/line code. Single-digit line codes are not different faces. Multi-line faces are excluded from the short/long candidate builder rather than silently reduced to one line. A preliminary 216-candidate count mixed line and face codes and partial faces; it is superseded by the corrected 167-candidate run.

## Strongest candidate, without a meaning assignment

The top graphic-modifier candidate is:

`fish with four surrounding strokes -> corresponding unmarked fish + 211`

There are six exact-string pairs spanning four fish bases and five distinct surrounding contexts:

```
171-60                 / 171-59-211
267-99-87-60           / 267-99-87-59-211
66                     / 65-211
65-68                  / 65-67-211
73                     / 72-211
73-176                 / 72-211-176
```

Only the second pair retains at least two unchanged surrounding signs. Two pairs have no surrounding signs at all. The broad graphical rule gains no corresponding multi-base support outside the fish family in this exact-context search. This does not establish equivalence, an affix, a pronunciation, or a grammatical meaning. No scholarly-priority claim is made for the fish-modifier/arrow association.

The literal-component search returns zero matches. The 167 linked-face candidates return zero longer exact-context substitution matches. Neither zero proves that the proposed relations are false; these are sparse tests with restrictive matching requirements.

The repeat search finds three alternatives to `267-99-59-59-211`, using markers 65, 87, or 104 before one fish. All three share that same frame. Since the candidates include visibly different stroke counts as well as another fish form, this result does not select a numerical value or a multiplication operator.

Every matched pair includes the source object identifiers and side/line metadata in the JSON outputs. Position profiles for marked fish are also retained: they are predominantly, but not exclusively, terminal. The outputs are retrospective exploration, not a preregistered or independently held-out test.

## External semantic routes

A separate source search examined proposed gold-assaying implements, residue studies, inscribed weights, and external contact objects as possible ways to tie an inscription to a measured quantity or named substance. No object-level join between an Indus inscription and independently measured chemical composition, contents, or an independently readable name was established. An artifact category, a shared findspot, or resemblance to a later symbol was not substituted for such a join. This source search is not an exhaustive survey of all collections.

## Reproduce the executed corpus search

From the repository root, Python 3.10 or later, standard library only:

```sh
python research/tools/semantic_transducer_search.py \
  --input research/data/mahadevan_20260905/concordance_documents.json.gz \
  --output /tmp/ivc-semantic-search
```

Preserved outputs: `research/data/semantic_search_20260906/`. These do not modify the accepted-claim ledger or merge any sign identities. They preserve the current unresolved search state; they are not presented as a completed answer to decipherment.

## Source references

Iravatham Mahadevan, *The Indus Script: Texts, Concordance and Tables* (1977), public concordance at https://indusscript.in/. The exact frozen input hash is recorded in every summary.

Asko Parpola, *Copper tablets from Mohenjo-daro and the study of the Indus script* (2008), especially Figures 1a–b and the discussion of pictorial bilinguals. Author-hosted source: https://tuhat.helsinki.fi/ws/portalfiles/portal/127257447/Parpola_A_2008._Copper_tablets_from_Mohenjo_daro._ECL_During_Caspers_Vol.pdf.

Publisher glyph illustrations: https://indusscript.in/assets/images/{id}.png. Their acquisition manifest records URLs and hashes; no new license is asserted over the source materials.
