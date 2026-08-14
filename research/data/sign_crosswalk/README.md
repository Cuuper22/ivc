# Provenance-Tagged Sign Crosswalk

Date: 2026-05-29

This directory is the normalized crosswalk scaffold for the Indus script workspace. A crosswalk edge links a sign in one sign-list namespace to a candidate counterpart in another; the scaffold exists so every such link carries its evidence with it.

It is useful infrastructure, not an accepted decipherment artifact. Every current Lipi-Mayig candidate edge defaults to `accepted_for_analysis=false`, because the evidence behind each edge is positional alignment plus mediated feature metadata — not source-image or primary sign-list validation.

## Tables

- `sign_systems.csv`: sign-list namespaces and source status.
- `signs.csv`: signs observed or mediated through the available sources.
- `artifact_witnesses.csv`: Lipi and Mayig text witnesses with direction/provenance status.
- `crosswalk_edges.csv`: candidate sign-to-sign links and their evidence fields.
- `evidence_refs.csv`: local files and hashes supporting this scaffold.
- `namespace_gates.csv`: blocked shortcuts and unresolved namespace traps.
- `review_events.csv`: build/review events.
- `manifest.json`: counts, caveats, and file list.
- `audit_summary.json`: machine-readable hygiene audit.
- `audit_issues.csv`: audit warnings and errors.
- `edge_pressure_summary.csv`: high-support or counterexample-bearing candidate edges to review first.

## Rule

No edge in this directory is a translation, phonetic value, sign meaning, or accepted allograph merge. An edge becomes analysis-grade only after its linked evidence clears the relevant namespace gates and source-level review.

## Audit

Latest audit: 2026-05-29.

Status: `audit_passed_with_caveats`.

The audit found zero duplicate primary keys, zero dangling reference errors, zero evidence hash/path errors, and zero accepted crosswalk edges. It found eight empty Lipi witness sequences, recorded as warnings. The highest-pressure review targets are candidate edges such as `740 -> P324`, `002 -> P122`, `032 -> P145`, and the unresolved `817/861 -> P385` pressure pair.

Human-readable note: `docs/sign_crosswalk_audit.md`.
