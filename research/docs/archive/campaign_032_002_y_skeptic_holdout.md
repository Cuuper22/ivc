# `032-002-Y` Skeptic Holdout

Date: 2026-05-29

## Question

This note runs the skeptic's attacks against a surviving result. Each attack tries to explain the pattern away with something other than grammar. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. A "closure" sign ends a row, a "branch" sign opens further material. A "register" is the object class a row sits on — site, seal type, icon, shape. "Family-blocked" means near-identical copies are collapsed so they cannot count as separate witnesses. The forger, referenced below, is the adversarial tool that runs our method on randomized fake corpora.

After the forger pass, does the `002-Y` closure/branch result survive hostile attacks that try to explain it as register, duplicate-family, site/type, or terminal-position artifact?

## Inputs

- `data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_branch_rows.csv`
- `data/open_prototype/tools/campaign_032_002_y_skeptic_holdout.mjs`

## Results

LOO is leave-one-out: each row is predicted by a model fitted without it, so nothing scores well by memorizing. Brier measures how well-calibrated the predicted probabilities are, and lower is better.

All-`002` strict dedup scope:

- Rows: 499.
- `y_class` LOO accuracy/Brier: 0.885772 / 0.097554.
- `site/type/symbol` register accuracy/Brier: 0.579158 / 0.248248.
- Family-blocked `y_class` accuracy/Brier: 0.885772 / 0.097540.
- Removing Mohenjo-daro `SEAL:S`: `y_class` remains 0.884298 accuracy versus register 0.611570.
- Removing `SEAL:S`: `y_class` remains 0.880952 accuracy versus register 0.690476.

Adjacent `032-002` strict dedup scope:

- Rows: 32.
- `y_class` LOO accuracy/Brier: 0.906250 / 0.106698.
- `site/type/symbol` register accuracy/Brier: 0.531250 / 0.284136.
- Family-blocked `y_class` accuracy/Brier: 0.906250 / 0.107144.
- Removing `SEAL:S` leaves only 5 rows; the signal survives numerically but is too thin for acceptance.

## Right-Edge Trap

Exact right-edge matching by `text_len` and `idx_002` is invalid for terminality. If text length and the position of `002` are fixed, the position of `Y` is fixed, so terminality is already determined. The script records this as a failed/tautological attack rather than counting it as a pass.

## Decision

The broad all-`002` closure/branch structure survives the current skeptic pass and forger pass. It is still not accepted because the remaining gate — the checkpoint before any stronger claim — is source-normalized: source boxes drawn on published photographs, side/direction checks, and family-blocked image-level rows must show the same closure/branch behavior outside the quarantined T3 metadata layer, the transcription tier set aside as unusable on its own.

The narrower adjacent `032-002` claim remains a live target but is not accepted. It is small-N and too dependent on rows still needing source acquisition.
