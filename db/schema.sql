-- IVC corpus relational schema (v1)
-- =================================================================
-- System of record for the curated Indus-script crosswalk + claim ledger.
-- Built by db/build_db.mjs from the data dir (default research/data/):
--   research/data/sign_crosswalk/*.csv   (sign systems, signs, witnesses, edges, gates...)
--   research/data/claim_ledger/claims.json
--
-- Foreign keys make the provenance chain machine-enforced. The builder
-- bulk-loads with foreign_keys OFF, then runs `PRAGMA foreign_key_check` so
-- dangling references are REPORTED as audit issues (matching
-- research/data/sign_crosswalk/audit_summary.json) rather than silently
-- rejected. The CSV/JSON seeds remain the source of truth; this DB is a
-- rebuildable artifact.

CREATE TABLE sign_system (
  system_id        TEXT PRIMARY KEY,
  authority        TEXT,
  namespace_prefix TEXT,
  source_version   TEXT,
  source_url       TEXT,
  local_path       TEXT,
  sha256           TEXT,
  access_status    TEXT,
  notes            TEXT
);

CREATE TABLE sign (
  sign_uid      TEXT PRIMARY KEY,
  system_id     TEXT REFERENCES sign_system(system_id),
  raw_id        TEXT,
  normalized_id TEXT,
  description   TEXT,
  feature_json  TEXT,
  visual_ref_id TEXT,
  status        TEXT
);
CREATE INDEX ix_sign_system ON sign(system_id);
CREATE INDEX ix_sign_norm   ON sign(normalized_id);

CREATE TABLE artifact (
  artifact_id TEXT PRIMARY KEY
);

CREATE TABLE witness (
  witness_id       TEXT PRIMARY KEY,
  artifact_id      TEXT REFERENCES artifact(artifact_id),
  system_id        TEXT REFERENCES sign_system(system_id),
  row_id           TEXT,
  side_id          TEXT,
  side_label_type  TEXT,
  text_raw         TEXT,
  sign_sequence    TEXT,
  direction        TEXT,
  direction_source TEXT,
  image_ref_id     TEXT,
  provenance_tier  TEXT
);
CREATE INDEX ix_witness_artifact ON witness(artifact_id);
CREATE INDEX ix_witness_system   ON witness(system_id);

CREATE TABLE evidence_ref (
  ref_id        TEXT PRIMARY KEY,
  ref_type      TEXT,
  citation      TEXT,
  url           TEXT,
  local_path    TEXT,
  page          TEXT,
  figure        TEXT,
  crop_path     TEXT,
  sha256        TEXT,
  checked_date  TEXT,
  access_status TEXT
);

CREATE TABLE crosswalk_edge (
  edge_id                  TEXT PRIMARY KEY,
  from_sign_uid            TEXT REFERENCES sign(sign_uid),
  to_sign_uid              TEXT REFERENCES sign(sign_uid),
  mapping_state            TEXT,
  evidence_types           TEXT,
  support_count            INTEGER,
  counterexample_count     INTEGER,
  aligned_positions        TEXT,
  top_share                REAL,
  example_witnesses        TEXT,
  counterexample_witnesses TEXT,
  confidence               TEXT,
  review_status            TEXT,
  accepted_for_analysis    TEXT
);
CREATE INDEX ix_edge_from ON crosswalk_edge(from_sign_uid);
CREATE INDEX ix_edge_to   ON crosswalk_edge(to_sign_uid);

CREATE TABLE namespace_gate (
  gate_id                TEXT PRIMARY KEY,
  assertion              TEXT,
  status                 TEXT,
  decision               TEXT,
  blocked_claims         TEXT,
  required_next_evidence TEXT,
  evidence_refs          TEXT
);

CREATE TABLE review_event (
  review_id          TEXT PRIMARY KEY,
  edge_id_or_gate_id TEXT,
  reviewer           TEXT,
  check_type         TEXT,
  result             TEXT,
  notes              TEXT,
  checked_date       TEXT
);

CREATE TABLE claim (
  claim_id                 TEXT PRIMARY KEY,
  ledger_class             TEXT,
  claim_type               TEXT,
  status                   TEXT,
  claim_text               TEXT,
  scope                    TEXT,
  reason_retracted         TEXT,
  retracted_date           TEXT,
  forger_tool              TEXT,
  forger_max_fpr           TEXT,
  skeptic_decision         TEXT,
  accepted_count_increment INTEGER,
  raw_json                 TEXT
);

CREATE TABLE claim_evidence (
  claim_id    TEXT REFERENCES claim(claim_id),
  idx         INTEGER,
  path        TEXT,
  summary     TEXT,
  path_exists INTEGER
);
CREATE INDEX ix_claimev_claim ON claim_evidence(claim_id);

CREATE TABLE data_file (
  path       TEXT PRIMARY KEY,
  top_dir    TEXT,
  ext        TEXT,
  size_bytes INTEGER,
  sha256     TEXT,
  csv_rows   INTEGER
);
CREATE INDEX ix_datafile_ext ON data_file(ext);
CREATE INDEX ix_datafile_top ON data_file(top_dir);

CREATE TABLE audit_issue (
  severity TEXT,
  code     TEXT,
  obj      TEXT,
  ref      TEXT,
  message  TEXT
);

-- High-support or counterexample-bearing edges to review first.
-- typeof() guards because some seed values are the literal text 'unknown'.
CREATE VIEW v_edge_pressure AS
  SELECT edge_id, from_sign_uid, to_sign_uid, support_count, counterexample_count,
         top_share, confidence, review_status, accepted_for_analysis
  FROM crosswalk_edge
  WHERE (typeof(support_count) = 'integer' AND support_count >= 2)
     OR (typeof(counterexample_count) = 'integer' AND counterexample_count > 0)
  ORDER BY (typeof(counterexample_count) = 'integer' AND counterexample_count > 0) DESC,
           CASE WHEN typeof(support_count) = 'integer' THEN support_count ELSE 0 END DESC;

CREATE VIEW v_open_gates AS
  SELECT gate_id, assertion, status, decision, required_next_evidence
  FROM namespace_gate
  WHERE status IS NULL OR LOWER(status) NOT IN ('resolved','closed','passed');

CREATE VIEW v_claim_provenance AS
  SELECT c.claim_id, c.ledger_class, c.claim_type, c.status, ce.path, ce.path_exists, ce.summary
  FROM claim c LEFT JOIN claim_evidence ce ON ce.claim_id = c.claim_id;

CREATE VIEW v_missing_evidence AS
  SELECT claim_id, path FROM claim_evidence WHERE path_exists = 0;
