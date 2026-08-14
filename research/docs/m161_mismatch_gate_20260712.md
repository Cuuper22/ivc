# M-161 structural-count mismatch gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FOUR_UNIT_SEQUENCE_REJECTS_LIPI_THREE_TOKEN_STRUCTURAL_COUNT`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers one object, `M-161`, where one Lipi token sits in the place the plates give to two separate grid signs.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `617`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P268`. Here Lipi records three tokens and Mayig records four. Before either row can be used for counting or for sequence statistics, somebody has to look at the object and decide which length the surface actually supports.

Bound sources are the exact records this decision was made from, pinned by page, row, commit, and hash so that the same decision can be rechecked byte for byte later.

## Bound sources

- CISI 1 local PDF, PDF page 84 / printed page 48, SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Lipi row `2687.1`, object `M-161`, direction `R/L`, stored sequence `617 122 003`.
- Mayig `M-161A` at commit `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`, stored sequence `P268 P268 P037 P123`, raw-record SHA-256 `ACA00105AC0C3B08E0A21924E6A247B2BAB7FA50906698EDAE740F3EA33AB5DC`.

At that commit, Mayig describes `P268` as a grid, `P037` as a person with a triangular pincer, and `P123` as three adjacent half-height simple vertical strokes. Exact pinned URLs and hashes are recorded in the JSON gate.

A panel is a labeled crop rendered from the published plate and kept as a file, so anyone can recheck the reading later. The durable page and object panels are listed in `research/data/sign_crosswalk/source_panels/m161_mismatch/manifest.csv`.

## Visual check

The object is published in two views: the impression, labeled `A`, and the seal itself, labeled `a`. A seal and its impression are mirror images of each other, so agreement between the two views is a real check rather than a repetition. Each view separately shows the same four units:

- `M-161 A`, the impression, shows four bounded units. In normalized right-to-left reading order these are two separate grids, a person-with-pincer sign, and three short vertical strokes.
- `M-161 a`, the seal, shows the same four units in the physically mirrored order. The two grids have separate outer boundaries and remain separate on both views.

So the source count is `4`, not `3`. The two grids are not one indivisible graphic compound.

## Catalogue decision

The Lipi row has three tokens where the source-visible sequence has four units, beginning with two separate grids. The missing unit is at the front, where Lipi writes `617`. But this object cannot say which of two things is going on: `617` may denote a two-grid compound, or Lipi may be suppressing or omitting one of a repeated pair. Both would produce exactly what is recorded. The case is therefore classified as `unresolved_compound_or_omission_policy`.

Consequences:

- reject Lipi's three-token sequence as a literal structural count for M-161;
- do not accept `617 = P268`;
- do not edit either corpus to force equal lengths;
- leave `122/P037` outside this bounded gate.

The unresolved count at the front of the row does not spoil the back of it. The terminal source unit is unambiguous: terminal Lipi `003` aligns with Mayig `P123` and the three-short-stroke form at source/Mayig position 4. That is an object-bound M-161 terminal match only. By itself it does not accept a global `003 = P123` edge, meaning a mapping that would hold everywhere the two signs appear.

No sign meaning, reading, phonetic value, language identification, translation, or accepted decipherment claim is added.
