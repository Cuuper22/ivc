# Lipi FRAME700 034 Prior Research Pressure Probe

Date: 2026-05-25

## Question

What does prior work force us to do to the live `FRAME700` `034` candidate?

This is not a literature review for decoration. Each cited prior claim is converted into pressure on the current candidate: support, downgrade, kill condition, or next evidence demand.

## Outputs

```text
data/open_prototype/tools/lipi_frame700_034_prior_pressure_probe.mjs
data/open_prototype/reports/lipi_frame700_034_prior_pressure_probe.csv
data/open_prototype/reports/lipi_frame700_034_prior_pressure_summary.json
```

## Prior Work Used

- Rao et al. 2009, [Entropic Evidence for Linguistic Structure in the Indus Script](https://doi.org/10.1126/science.1170391): conditional-entropy evidence keeps sequence dependency on the table, but does not by itself read the script.
- Yadav et al. 2010, [Statistical Analysis of the Indus Script Using n-Grams](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506): ordered sign groups, directionality, and missing-sign prediction are legitimate tests; they do not license translation.
- Farmer, Sproat, and Witzel 2004, [The Collapse of the Indus-Script Thesis](https://hasp.ub.uni-heidelberg.de/journals/ejvs/article/download/620/612/1254): extreme brevity, repetition, and nonlinguistic symbol-system parallels are not annoyances. They are mandatory adversarial tests.
- Sproat 2014, [A Statistical Comparison of Written Language and Nonlinguistic Symbol Systems](https://www.cambridge.org/core/journals/language/article/abs/statistical-comparison-of-written-language-and-nonlinguistic-symbol-systems/9D2C4213767B8A8DEBEC765AB6517955): global entropy-style classification is too weak as proof.
- Meadow and Kenoyer 2000, [The Tiny Steatite Seals of Harappa](https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf), plus Kenoyer and Meadow 2010, [Inscribed Objects from Harappa Excavations 1986-2007](https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf): object context, source photos, and duplicate-family control are first-class evidence.
- Daggumati and Revesz 2021, [A method of identifying allographs in undeciphered scripts](https://doi.org/10.1057/s41599-021-00713-0): mirrored/direction-linked variants can collapse; direction must stay unresolved until source images settle it.
- Rao 2018, [The Indus Script and Economics](https://arxiv.org/abs/1812.00049): administrative use is a serious hypothesis for miniature tablets, but it remains a use-context hypothesis, not a reading.
- Nair 2026, [How Non-Linguistic Is the Indus Sign System?](https://arxiv.org/abs/2604.17828): calibrated nonlinguistic baselines are now part of the bar; this project must compare against stronger baselines as data access improves.

## Local Result

```text
pressure_rows: 8
FRAME700 rows: 353
FRAME700 rows after removing H-2218 through H-2239: 331
no-H 034 rows: 93
harsh matched-block policy: type + sides + order + context + relation
034 observed recall under dimension model: 0.677419
034 null p95 under harsh matched-block shuffle: 0.548387
p(null >= observed): 0
overall top-1 under same model: 0.435045
overall null p95: 0.425982
```

Interpretation:

The `034` branch remains alive as a distributional residue under a harsh block policy. The overall classifier is weak, but the `034` recall is still above every tested null iteration in this local run. That is not a translation. It is a reason to keep the candidate under source validation instead of dropping it.

## Pressure Outcomes

| Pressure | Local result | Effect |
| --- | --- | --- |
| Markov/order work | `034` recall `0.677419` vs null p95 `0.548387` | keep `034` alive as structure |
| N-gram direction work | all `034`: `700_first 101`, `700_last 13`; no-H: `700_first 80`, `700_last 13` | preserve order; do not normalize yet |
| FSW repetition critique | 45 of 93 triads have repeated target-family pressure; H-910 demoted to independence rank 50 | old pretty branch downgraded |
| Sproat metric critique | overall gain above frequency only `0.024169` | no global proof claim |
| Meadow/Kenoyer source context | public row hits `0`; archive-needed objects `12` | source acquisition required |
| Direction/allograph warning | direction-safe source rows `0` | no merge or reading from order alone |
| Admin-use hypothesis | no-H `034` is Harappa-only in current layer: `TAB:I 51`, `TAB:B 42` | compatible with admin-code hypothesis only |
| Synthetic-baseline pressure | no source-grade rows yet; comparator access still incomplete | keep baseline work open |

## What Changed

Before this probe, prior work was mostly background. Now it actively changes the research state:

1. The `034` candidate survives the Rao/Yadav-style sequence-dependency pressure only as a local structural residue.
2. The Farmer/Sproat/Witzel and Sproat objections are not dismissed. They demote repeated-family evidence and forbid global entropy-style confidence.
3. Kenoyer/Meadow force the next step back to object-side source images.
4. Daggumati/Revesz keep `+700-034+` versus `+034-700+` unresolved until direction and mirror status are source-checked.
5. Rao 2018 gives a plausible administrative-use lane, but the current evidence cannot yet say what `034` does.

## Boundary

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted language assignments: 0
```

The live claim is narrower:

```text
034 is a source-targeted distributional residue inside the FRAME700 tablet side-mark system.
```

It remains unvalidated until source images resolve side order, direction, allograph risk, and the H-2204/H95-2482 discrepancy.
