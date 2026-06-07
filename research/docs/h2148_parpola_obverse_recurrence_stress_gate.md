# H-2148 Parpola Obverse Recurrence Stress Gate

Date: 2026-05-26

## Question

Does Parpola 2019's claim that the H-940 / H-2147 / H-2148 obverse text recurs on H-942, H-2240, and H-2241 support the local `+520-220-415+` companion row, or does it expose a sign-inventory problem?

## Result

It does both.

The recurrence supports the idea that the H-2148 three-sign companion row belongs to the same prior-work text family, because H-2240 has the exact local row `+520-220-415+` and H-2241 preserves a fragment ending in `415-240`.

But H-942, explicitly named by Parpola as part of the same obverse-text recurrence, is locally `+520-220-016+`, not `+520-220-415+`. That creates a real stressor:

```text
Either local `415` and `016` are being split/merged differently from Parpola's sign-list convention,
or the local row/source-side mapping for at least one object is incomplete,
or Parpola's recurrence statement tolerates a terminal variant rather than exact identity.
```

No option is accepted yet.

## Prior-Work Claim

Parpola 2019 says that for H-940, H-2147, and H-2148, the reverse has sign no. 41; the text on the obverse of these tablets occurs also on H-942, H-2240, and H-2241.

Relevant local line extraction:

```text
H-940:  +520-220-415+ / +110+
H-2148: +520-220-415+ / +110+
H-942:  +520-220-016+ / +033-700+
H-2240: +520-220-415+ / +869-575+
H-2241: ]415-240+ / ]000+
```

## Local Rows Checked

```text
481.1  H-2148  +520-220-415+
481.2  H-2148  +110+
1820.1 H-940   +520-220-415+
1820.2 H-940   +110+
1822.1 H-942   +520-220-016+
1822.2 H-942   +033-700+
816.1  H-2240  +520-220-415+
816.2  H-2240  +869-575+
639.1  H-2241  ]415-240+
639.2  H-2241  ]000+
```

## Decision

Accepted:

```text
Parpola's obverse recurrence gives independent prior-work pressure that H-2148's three-sign companion row belongs to a `520-220-X` family.
H-2240 is an exact local `+520-220-415+` recurrence.
H-942 is an explicit stress case because its local row is `+520-220-016+`.
H-2241 is fragmentary pressure only.
```

Not accepted:

```text
local `415` = local `016`
local `415` = Parpola final sign no. 189
local `016` = Parpola final sign no. 189
the H-2148 one-sign side = Parpola sign no. 41
any sign value
any phonetic value
any translation
```

## Next Gate

This creates a companion-text sign-inventory gate:

```text
Source-normalize H-942, H-2240, and H-2241 against H-940/H-2148.
Check whether Parpola's obverse recurrence maps local `415` and `016` to the same sign-list item, to different variants, or to a source/side transcription mismatch.
```

This matters because a false companion-text mapping can contaminate the same-side inference for `+110+`.

