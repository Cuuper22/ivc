# Corpus database (`db/`)

A single-file SQLite database that is the **system of record** for the curated
Indus-script corpus: sign systems, signs, artifacts, witnesses, crosswalk edges,
namespace gates, review events, and the claim ledger.

It is a **rebuildable artifact** generated from the CSV/JSON seeds under
`research/data/`. Its job is to make the provenance/integrity rules
*machine-enforced* instead of hand-audited — the foreign keys are the
[sign_crosswalk audit](../research/data/sign_crosswalk/README.md) done for free,
every build.

## Build

Requires **Node ≥ 22.5** (built-in `node:sqlite`; no `npm install`).

```sh
node --no-warnings db/build_db.mjs            # reads research/data/ by default
```

Outputs `db/ivc.sqlite` and `db/audit_report.json`. A clean build prints
`0 error(s), 0 warning(s)`.

## Query

```sh
sqlite3 db/ivc.sqlite "SELECT * FROM v_edge_pressure LIMIT 10;"
sqlite3 db/ivc.sqlite "SELECT * FROM v_missing_evidence;"     -- claims citing a vanished local file
sqlite3 db/ivc.sqlite "SELECT ledger_class, COUNT(*) FROM claim GROUP BY ledger_class;"
```

## Schema

See [`schema.sql`](schema.sql). Core tables: `sign_system`, `sign`, `artifact`,
`witness`, `evidence_ref`, `crosswalk_edge`, `namespace_gate`, `review_event`,
`claim` / `claim_evidence`, `data_file` (catalog of every seed file with sha256),
`audit_issue`. Views: `v_edge_pressure`, `v_open_gates`, `v_claim_provenance`,
`v_missing_evidence`.

## Integrity enforced on every build

- **No duplicate primary keys** (PK constraints).
- **No dangling references** (foreign keys + `PRAGMA foreign_key_check`) — e.g. an
  edge cannot point at a non-existent sign.
- **Evidence exists** — every `claim_evidence` local path is checked on disk;
  URLs are recorded but not fetched.
