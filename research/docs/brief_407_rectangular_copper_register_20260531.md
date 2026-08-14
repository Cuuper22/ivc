# 407 as a Rectangular/Copper Register Marker

Date: 2026-05-31

Status: promoted candidate, not accepted decipherment.

## Claim

What is sign `407` doing? In the current corpus it does not behave like a purely phonetic sign, and it does not behave like pure decoration either. The strongest current bet is that `407` marks a carrier/register class — that is, it tracks the kind of object it is written on. It concentrates on rectangular seals (`SEAL:R`) and copper tablets (`TAB:C`). The copper-tablet subset gives a plausible but diffuse external semantic bridge to the readable cuneiform expression `uruda me-luh-ha` ("Meluhha copper"). No phonetic value is assigned to `407`.

## Evidence

First we collapse canonical numeric sequences, so that repeated copies of the same text count once. After that collapse, `407` occurs in `53/444` rows of type `SEAL:R or TAB:C`, and in only `17/3059` background rows. If you scan every sign for enrichment in this context, `407` ranks `1/714`. The Bonferroni-corrected p-value — corrected for testing all the signs — is `1.26e-31`. A 3000-iteration max-stat label-shuffle forger (a null model that shuffles the labels and lets each shuffle put forward its own best candidate) produced a false-positive rate of `0`.

The result is not carried only by preservation, Mohenjo-daro, or Harappa. Remove each of those in turn and the enrichment stays:

- Complete-only rows: `40/297` register rows vs `11/1887` background, Bonferroni `1.60e-23`.
- Non-poor rows: `31/270` register rows vs `8/1463` background, Bonferroni `2.35e-16`.
- Excluding Mohenjo-daro: `14/159` register rows vs `11/1812` background, Bonferroni `3.16e-7`.
- Excluding Harappa: `46/363` register rows vs `7/1958` background, Bonferroni `2.36e-28`.

The copper subtype is strong on its own: `407` appears in `18/119` copper rows and `18/94` `TAB:C` rows, ranking `1/714` in both scans. Even within Mohenjo-daro alone, copper `TAB:C` rows give `18/92` vs `27/1440`, Bonferroni `4.97e-9`.

## External Bridge

Does anything outside the Indus corpus point the same way? Live CDLI verification on 2026-05-31 finds `uruda me-luh-ha` in `P136689` and `P228742`; the fuller `ma-na uruda me-luh-ha` occurs in `P136689`. `P136689` is the relevant administrative commodity witness: line 2 reads `6(disz) ma-na uruda me-luh-ha`. `P228742` is lexical-list support for the expression, not a trade document.

Be clear about what this bridge is: a diffuse semantic bridge only. There is no shared object, owner, seal impression, accession bridge, or bilingual inscription tying `407` to `uruda` phonetically.

## Demoters

`407` is broader than copper. A copper-only interpretation is too narrow, because rectangular seals carry most of the support. The current best reading is register/carrier class, with copper as a subtype.

The sign also appears outside `SEAL:R/TAB:C`: `10` square seals, `3` `TAB:B`, `2` pottery marks, `1` miscellaneous object, and `1` circular seal. These background rows do not kill the enrichment, but they block any categorical "means copper" claim.

## Falsifiers

The bet should be demoted if source-checked `SEAL:R` or copper `TAB:C` rows lose `407` on inspection, if unverified non-register contexts accumulate `407` at comparable rates, or if a matched control sign reaches the same enrichment under leave-site and max-stat tests.

The external bridge should be demoted if duplicate review reduces `uruda me-luh-ha` to only lexical-list evidence, or otherwise removes the administrative commodity witness.

## Prediction

If the bet is right, unverified rectangular seal rows and copper `TAB:C` rows should turn out to be enriched for `407`, including outside Mohenjo-daro. If a future object-level bilingual involving Meluhha copper ever appears, check its Indus side for `407` first — but the present result does not license a sound value.
