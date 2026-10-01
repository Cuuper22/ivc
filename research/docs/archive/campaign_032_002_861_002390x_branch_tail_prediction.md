# 032-002-861 / 002-390-X Branch-Tail Prediction

Date: 2026-05-30

## Question

Treat `002-390-X` as a possible branch-choice slot. The question is one of prediction: does the branch chosen after `390` predict whether the inscription closes or continues?

That framing changes the linguistic object. It is no longer `125` as a heroic singleton; it is the whole `PREV -> 002-390 -> X -> TAIL` matrix.

## Input

- Matrix source: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_family_collapsed_branch_ecology_matrix_rows.csv`
- Blind alignment decision: `C:\Users\Acer\OneDrive\Documents\ivc\docs\campaign_032_002_861_002390x_blind_overlay_alignment.md`
- Machine-readable prediction table: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_branch_tail_prediction.csv`

## Branch-Tail State

| branch after `390` | rows | terminal | continues | current use |
|---:|---:|---:|---:|---|
| `125` | 4 | 0 | 4 | live continuation-branch candidate |
| `095` | 2 | 2 | 0 | live terminal non-`125` comparator |
| `705` | 2 | 2 | 0 | acquisition-hot terminal non-`125` candidate |
| `692` | 1 | 1 | 0 | strict source-visible terminal non-`125` control |
| `072` | 1 | 1 | 0 | background terminal singleton |
| `140` | 1 | 1 | 0 | background terminal singleton |
| `346` | 1 | 1 | 0 | background terminal singleton |
| `530` | 1 | 0 | 1 | background continuation singleton |
| `590` | 1 | 0 | 1 | background continuation singleton |
| `707` | 1 | 1 | 0 | background terminal singleton |

In the strict source-visible layer:

- `M-119/M-735`: `125`, both continue.
- `M-70/M-71`: non-`125` (`692/095`), both close.

In the repeated source-gated layer:

- `H-1993/M-71`: `095`, both close, but H-1993 still lacks the figure image.
- `M-1825/Dholavira 4237.1`: `705`, both close in local metadata, but M-1825 is image-dark and Dholavira item 10 is still unbound.

## Live Linguistic Hypotheses

### H1: Branch-Choice Polarity

`002-390` opens a small branch-choice slot. Some branches select closure (`095`, `692`, probably `705`), while `125` selects overt continuation.

Best current support:

- All four local `125` rows continue.
- Strict visible `M-119/M-735` continue.
- Strict visible non-`125` controls `M-70/M-71` close.
- Repeated `095` and `705` are terminal in the metadata layer.

Why this would matter for decipherment: it gives a structural contrast — not meaning, not sound, but a rule-like behavior that can constrain readings later.

### H2: Formula/Register Residue

The apparent polarity is produced by whole formulas, icon/register lanes, source routing, or copy-family cells rather than language structure.

Best current support:

- The strict visible `125` targets are both Mohenjo-daro square `SEAL:S` rows.
- `M-119/M-735` do not prove blind source windows; both are partial under blind alignment.
- `705`, the best repeated non-`125` terminal branch, is not strict source-bound.
- `530/590` show non-`125` continuation exists, even if currently source-dark/singleton.

### H3: Tail-Formula Subframe

`125` may not be a continuation marker by itself. It may be the first member of longer subframes:

- `125 -> 632 032`
- `125 -> 632 032 900 563`
- `125 -> 195`
- `125 -> 820`

Under this model, `125` carries no "continuation" meaning of its own. It is simply a branch into several fixed or semi-fixed endings.

## Decision

Promote the research object, not the sign:

`002-390-X` is a live branch-tail prediction system.

Do not promote:

- `125` as a value.
- `125` as a function.
- `125` as source-window-proven.
- `705` as strict evidence.
- Any phonetic, language-family, semantic, or translation claim.

## Next Decisive Batch

1. Bind or reject `705`.
   - If Dholavira item 10 binds to Lipi `4237.1` or M-1825 source-images as `+157-031-002-390-705+`, repeated `705` becomes the strongest non-`125` terminal comparator.
   - If both fail, `705` remains metadata pressure only.

2. Bind `H-1993`.
   - If `H96-2769 Figure 17.07` preserves `004 -> 002-390 -> 095` terminally, then `004 -> 002-390` has a real split against Sktd-1 `004 -> 002-390 -> 125 -> 820`.
   - If H-1993 fails or cannot be imaged, the `004` matched contrast remains blocked.

3. Search for matched continuation exceptions.
   - A source-bound non-`125` continuation under similar source/register conditions would demote H1.
   - A source-bound terminal `125` under similar source/register conditions would demote H1 harder.

4. Collapse by whole formula and source family before any grammar claim.
   - If branch-tail behavior survives family collapse and source binding, it becomes a genuine structural constraint.
   - If it collapses, the translation system must treat it as formula/template behavior, not grammar.

Current accepted claim:

`002-390-X` is a branch-tail prediction object worth testing at batch scale.

Rejected claims:

sign value, sign function, source-window proof, phonetic reading, language identity, sign meaning, and translation.
