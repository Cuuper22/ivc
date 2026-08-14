# Object-Level Onomastic Value Attempts

Date: 2026-05-30

This note records the most direct attempt the project has made to assign sounds to Indus signs, and its failure.

The idea. Mesopotamian cuneiform texts mention a place called Meluhha, widely identified with the Indus region, along with names and titles attached to it. "Onomastic" means name-based. If one of those names sat on an Indus-inscribed object found in Mesopotamia, we could line the name's syllables up against the object's signs and get sound values. The "object route" is the trail from a catalog row to a real, citable object record — museum number, excavation number, publication — which is what makes an attempt worth testing at all.

This is the direct Priority A test: take cuneiform-captured Meluhha names, titles, and lexical phrases, then attempt actual sign-value assignments against the external Indus-style object rows only where the current object route makes the attempt worth testing.

No assignment survives.

## Artifacts

- `data/meluhha/tools/attempt_object_level_onomastic_values.mjs`
- `data/meluhha/object_level_onomastic_value_attempts.csv`
- `data/meluhha/object_level_onomastic_value_forger_iterations.csv`
- `data/meluhha/object_level_onomastic_value_summary.json`

## Tested Targets

The run tested 12 cuneiform-side strings:

- `me-luh-ha`
- `ma2 me-luh-ha`
- `lu2-sun2-zi-da`
- `szu-i3-li2-su`
- `e-me-bal me-luh-ha`
- `ur gun3-a me-luh-ha`
- `dar me-luh-ha`
- `ur-dlamma dumu me-luh-ha`
- `ur-digalim dumu me-luh-ha`
- `dumu me-luh-ha`
- `i3-ba lu2 me-luh-ha`
- `gug gi-rin me-luh-ha`

The focus set had 30 external Mesopotamia/Gulf objects with parseable local sign sequences. The script wrote 47 pattern-compatible candidate rows, but most are generic or site-mismatched pattern matches and are dead on arrival.

## Strongest Attempt

The only strict mapped object attempt is:

| Cuneiform target | External row | Proposed values | Decision |
| --- | --- | --- | --- |
| `ur gun3-a me-luh-ha` | `3898.1 / U17649` | `002=ur;004=gun3;328=a;001=me;803=luh;415=ha` | Retracted |

Why it was worth trying:

- `3898.1` is now mapped to `U17649` through the Gadd/Penn route.
- The local row has six distinct signs: `+002-004-328-001-803-415+`.
- The cuneiform phrase `ur gun3-a me-luh-ha` has six distinct units.
- The cuneiform source is an Ur Meluhha context.

Why it dies:

- The cuneiform phrase is from a separate text, not the same object.
- `U17649` is Indus-inscribed only in the current source surface.
- No owner, title, profession, Meluhha formula, or readable cuneiform name is attached to `U17649`.
- The match is still site plus length/pattern compatibility.

## Forger

The forger is this project's standard adversary test: build fake versions of the claimed relationship and see whether they score as well as the real one. If they do, the real one is not evidence.

The forger shuffled target source-sites across fixed cuneiform phrase patterns, then counted strict mapped Indus-only object attempts that remained same-site or Girsu/Tello-equivalent pattern matches.

| Measure | Value |
| --- | ---: |
| Iterations | 10,000 |
| Observed strict mapped same-site pattern attempts | 1 |
| Null >= observed share | 0.6857 |
| Mean null candidate count | 0.8414 |
| Max null candidate count | 2 |

This is nowhere near admissible. A forger that only gets site labels shuffled can reproduce a match at comparable or better rates most of the time.

## Decision

Retracted as an external anchor and as a phonetic-value source.

Residual value: the script is now the correct place to test future exact object bridges. If Kjaerum `279/319`, Amiet `1643`, Mitchell 1986, or Sarzec/Heuzey produces a real object-level readable-script pairing, the same harness can attempt a value and measure the false-positive rate before any claim reaches the ledger — the project's running record of accepted findings.
