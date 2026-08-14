# 520-220-X Context-Slot Null

Date: 2026-05-29

This note tests a tempting claim and finds it fails. Signs in this corpus are numeric IDs. The `520-220-X` frame is rows whose signs run `520`, `220`, then a variable third sign X. "Closure" means the row ends there; "continuation" means more follows. A "register" is the object class a row sits on — site, seal type, material, shape — and it is the rival explanation here: rows may stop where they do because of what kind of object they are on, not because of grammar.

Question:

```text
Inside the 520-220-X frame, does X predict closure versus continuation better than site/type register does?
```

This is a Vector 4 context-slot test. It is not a sign meaning, phonetic value, language identification, or translation.

## Outputs

- `data/open_prototype/tools/campaign_520_220_x_context_slot_nulls.mjs`
- `data/open_prototype/reports/campaign_520_220_x_context_slot_null_summary.json`
- `data/open_prototype/reports/campaign_520_220_x_context_slot_null_iterations.csv`
- `data/open_prototype/reports/campaign_520_220_x_context_slot_scope_rows.csv`

## Result

The tempting claim fails.

In raw clean-behavior rows, `third_slot` predicts closure/continuation at 0.687500 leave-one-out accuracy, but `site|type` predicts it at 0.812500. Leave-one-out means each row is predicted by a model fitted without it, so nothing scores well by memorizing.

After exact-text collapse, `third_slot` predicts closure/continuation at 0.781250, but `site|type` predicts it at 0.906250. The exact collapse is decisive because most short closed `415` rows are exact repetitions; once collapsed, the data are 27 continuation families and only 5 terminal-closed families.

## Forger

The forger is our adversarial tool: it builds randomized copies of the data — null models — and runs the same method on them, to see how often chance alone produces what we observed. High numbers in the columns below mean the nulls matched or beat the real result, which is bad for the real result.

5000 iterations per null model.

| Scope | Null model | Null >= observed third-slot acc. | Null >= observed gain |
| --- | --- | ---: | ---: |
| raw clean behavior | closure shuffle global | 0.014800 | 0.835400 |
| raw clean behavior | closure shuffle within site | 0.230200 | 0.248800 |
| raw clean behavior | closure shuffle within type | 0.528600 | 0.560600 |
| raw clean behavior | closure shuffle within site/type | 0.439800 | 0.439800 |
| raw clean behavior | closure shuffle within site/type/material/shape | 0.726400 | 0.726400 |
| exact-text collapsed | closure shuffle global | 0.981600 | 0.998400 |
| exact-text collapsed | closure shuffle within site | 0.989800 | 1.000000 |
| exact-text collapsed | closure shuffle within type | 0.967400 | 0.962800 |
| exact-text collapsed | closure shuffle within site/type | 0.982800 | 0.982800 |
| exact-text collapsed | closure shuffle within site/type/material/shape | 0.980200 | 0.980200 |

## Interpretation

The `520-220-X` frame is still a real structural object, but this test does not earn a context-slot meaning. The apparent closure behavior is register-shaped: Harappa tablet/tag-style repetition makes `415` look like a closure marker in the raw rows, while Mohenjo-daro carries most of the productive continuations.

The next useful test is not more raw prediction. It is source-validated same-stratum contrast:

- M-37 `+520-220-415+`
- M-1206 `+520-220-034+`
- M-1912 `+520-220-003+`
- H-942 `+520-220-016+`

Those rows test whether the terminal component is graphical/allographic/source-policy pressure, not whether `X` has a corpus-wide closure meaning.

Accepted sign meanings remain zero.
