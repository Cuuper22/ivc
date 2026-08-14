# Replacement-Run Quarantine

Cutoff: 2026-05-31T01:04:00 America/Los_Angeles.

This directory is the evidence firewall for the replacement run. Any artifact listed in `botched_successor_after_20260531T0104_manifest.csv` is excluded from accepted-claim evidence unless it is independently re-earned under this replacement branch. The point of the firewall is simple: an artifact from a compromised run cannot support a claim, no matter how good it looks.

A quarantined artifact has exactly two allowed uses, and both are narrow:

- `read_for_autopsy_only`: inspect it to understand what happened. Do not cite it as support.
- `code_reference_only`: inspect it for implementation ideas, but rerun from verified inputs and write replacement-named outputs before using any result.

To re-earn an artifact, produce it again under a fresh name and record the command, inputs, seed policy, output hashes, forger false-positive rate, and skeptic attack notes.
