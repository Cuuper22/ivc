# M-161 structural-count mismatch gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FOUR_UNIT_SEQUENCE_REJECTS_LIPI_THREE_TOKEN_STRUCTURAL_COUNT`.

## Bound sources

- CISI 1 local PDF, PDF page 84 / printed page 48, SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi row `2687.1`, object `M-161`, direction `R/L`, stored sequence `617 122 003`.
- Mayig `M-161A` at commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`, stored sequence `P268 P268 P037 P123`, raw-record SHA-256 `ACA00105AC0C3B08E0A21924E6A247B2BAB7FA50906698EDAE740F3EA33AB5DC`.

At that commit, Mayig describes `P268` as a grid, `P037` as a person with a triangular pincer, and `P123` as three adjacent half-height simple vertical strokes. Exact pinned URLs and hashes are recorded in the JSON gate.

The durable page and object panels are listed in `research/data/sign_crosswalk/source_panels/m161_mismatch/manifest.csv`.

## Visual check

Each published view separately shows the same four units:

- `M-161 A`, the impression, shows four bounded units. In normalized right-to-left reading order these are two separate grids, a person-with-pincer sign, and three short vertical strokes.
- `M-161 a`, the seal, shows the same four units in the physically mirrored order. The two grids have separate outer boundaries and remain separate on both views.

The source count is therefore `4`, not `3`. The two grids are not one indivisible graphic compound.

## Catalogue decision

The Lipi row has three tokens where the source-visible sequence has four units beginning with two separate grids. The first Lipi token is `617`, but this object does not decide whether `617` denotes a two-grid compound or whether one repeated grid is suppressed or omitted in Lipi. It is classified as `unresolved_compound_or_omission_policy`.

Consequences:

- reject Lipi's three-token sequence as a literal structural count for M-161;
- do not accept `617 = P268`;
- do not edit either corpus to force equal lengths;
- leave `122/P037` outside this bounded gate.

Despite the unresolved prefix-count discrepancy, the terminal source unit is unambiguous: terminal Lipi `003` aligns with Mayig `P123` and the three-short-stroke form at source/Mayig position 4. That is an object-bound M-161 terminal match only. It does not, by itself, accept a global `003 = P123` edge.

No sign meaning, reading, phonetic value, language identification, translation, or accepted decipherment claim is added.
