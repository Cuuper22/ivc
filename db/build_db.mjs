#!/usr/bin/env node
// db/build_db.mjs
// =================================================================
// Build the IVC corpus SQLite database from the curated CSV/JSON seeds.
//
// Runtime: Node >= 22.5 (built-in node:sqlite — no npm install, no native build).
//
//   node --no-warnings db/build_db.mjs                      # uses research/data/
//   node --no-warnings db/build_db.mjs --data research/data --db db/ivc.sqlite
//
// Non-destructive: reads the data dir, writes only the .sqlite file and
// db/audit_report.json. The CSV/JSON seeds remain the source of truth.
//
// Loads the sign_crosswalk tables + claim ledger, derives the artifact table,
// catalogs every data file (size, sha256, csv rows), and runs an integrity audit
// (duplicate PKs, dangling foreign keys, missing claim-evidence paths) — the
// manual sign_crosswalk audit, automated.

import { DatabaseSync } from 'node:sqlite';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opt = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const ROOT = path.resolve(opt('--root', '.'));
const DATA_DIR = opt('--data', 'research/data');           // relative to ROOT
const DB_PATH = path.resolve(opt('--db', path.join(ROOT, 'db', 'ivc.sqlite')));
const SCHEMA_PATH = path.join(ROOT, 'db', 'schema.sql');

const issues = [];
const issue = (severity, code, obj, ref, message) =>
  issues.push({ severity, code, obj, ref: ref == null ? null : String(ref), message });
const rel = p => path.relative(ROOT, p).split(path.sep).join('/');
const nz = v => (v === undefined || v === '') ? null : v;

// ---- minimal RFC4180 CSV parser ----
function parseCSV(text) {
  const rows = []; let row = [], field = '', inQ = false, i = 0;
  const n = text.length;
  while (i < n) {
    const c = text[i];
    if (inQ) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i += 2; continue; } inQ = false; i++; continue; }
      field += c; i++; continue;
    }
    if (c === '"') { inQ = true; i++; continue; }
    if (c === ',') { row.push(field); field = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; i++; continue; }
    field += c; i++;
  }
  if (field.length > 0 || row.length > 0) { row.push(field); rows.push(row); }
  return rows;
}
function readCSV(file) {
  const rows = parseCSV(fs.readFileSync(file, 'utf8'));
  if (!rows.length) return { header: [], records: [] };
  return { header: rows[0], records: rows.slice(1).filter(r => r.length && !(r.length === 1 && r[0] === '')) };
}

// ---- DB setup ----
fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
for (const ext of ['', '-wal', '-shm']) if (fs.existsSync(DB_PATH + ext)) fs.rmSync(DB_PATH + ext);
const db = new DatabaseSync(DB_PATH);
db.exec('PRAGMA foreign_keys = OFF;');
db.exec(fs.readFileSync(SCHEMA_PATH, 'utf8'));
const tableCols = t => db.prepare(`PRAGMA table_info(${t})`).all().map(r => r.name);

function loadTable(table, csvName) {
  const file = path.join(ROOT, DATA_DIR, 'sign_crosswalk', csvName);
  if (!fs.existsSync(file)) { issue('warning', 'missing_seed', table, csvName, 'seed CSV not found'); return 0; }
  const { header, records } = readCSV(file);
  const tcols = tableCols(table);
  const cols = header.filter(h => tcols.includes(h));
  const idx = cols.map(c => header.indexOf(c));
  const stmt = db.prepare(`INSERT INTO ${table} (${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`);
  let ok = 0;
  db.exec('BEGIN');
  for (const rec of records) {
    const vals = idx.map(j => nz(rec[j]));
    try { stmt.run(...vals); ok++; }
    catch (e) { issue('error', String(e.message).includes('UNIQUE') ? 'duplicate_pk' : 'load_error', table, vals[0], e.message); }
  }
  db.exec('COMMIT');
  const dropped = header.filter(h => !tcols.includes(h));
  if (dropped.length) issue('info', 'unmapped_columns', table, csvName, `columns not in schema: ${dropped.join(', ')}`);
  return ok;
}

function loadClaims() {
  const file = path.join(ROOT, DATA_DIR, 'claim_ledger', 'claims.json');
  if (!fs.existsSync(file)) { issue('warning', 'missing_seed', 'claim', 'claims.json', 'not found'); return { claims: 0, ev: 0 }; }
  const d = JSON.parse(fs.readFileSync(file, 'utf8'));
  const cstmt = db.prepare(`INSERT INTO claim
    (claim_id,ledger_class,claim_type,status,claim_text,scope,reason_retracted,retracted_date,
     forger_tool,forger_max_fpr,skeptic_decision,accepted_count_increment,raw_json)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)`);
  const estmt = db.prepare(`INSERT INTO claim_evidence (claim_id,idx,path,summary,path_exists) VALUES (?,?,?,?,?)`);
  let nc = 0, ne = 0;
  db.exec('BEGIN');
  for (const [cls, arr] of [['accepted', d.accepted_claims], ['candidate', d.candidate_claims], ['retracted', d.retracted_candidates]]) {
    for (const c of (arr || [])) {
      const fr = c.forger_record || {}, sr = c.skeptic_record || {};
      const inc = c.accepted_count_increment === true ? 1 : (typeof c.accepted_count_increment === 'number' ? c.accepted_count_increment : 0);
      try {
        cstmt.run(c.claim_id, cls, nz(c.claim_type), nz(c.status), nz(c.claim), nz(c.scope), nz(c.reason_retracted),
          nz(c.retracted_date), nz(fr.tool), fr.max_recorded_fpr != null ? String(fr.max_recorded_fpr) : null, nz(sr.decision), inc, JSON.stringify(c));
        nc++;
      } catch (e) { issue('error', String(e.message).includes('UNIQUE') ? 'duplicate_pk' : 'load_error', 'claim', c.claim_id, e.message); continue; }
      const ev = Array.isArray(c.primary_evidence) ? c.primary_evidence : (Array.isArray(c.evidence) ? c.evidence : []);
      ev.forEach((it, k) => {
        const p = (it && typeof it === 'object') ? (it.path || null) : (typeof it === 'string' ? it : null);
        const s = (it && typeof it === 'object') ? (it.summary || null) : null;
        const isUrl = p ? /^[a-z][a-z0-9+.-]*:\/\//i.test(p) : false;
        let exists = null;
        if (p && !isUrl) {
          exists = fs.existsSync(path.join(ROOT, p)) ? 1 : 0;
          // claim paths predate the data/ -> research/data/ reorg; resolve that too
          if (!exists && p.startsWith('data/')) exists = fs.existsSync(path.join(ROOT, DATA_DIR, p.slice(5))) ? 1 : 0;
        }
        estmt.run(c.claim_id, k, nz(p), nz(s), exists); ne++;
      });
    }
  }
  db.exec('COMMIT');
  return { claims: nc, ev: ne };
}

function walk(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const fp = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(fp)); else out.push(fp);
  }
  return out;
}
function catalogData() {
  const base = path.join(ROOT, DATA_DIR);
  if (!fs.existsSync(base)) return 0;
  const stmt = db.prepare(`INSERT OR REPLACE INTO data_file (path,top_dir,ext,size_bytes,sha256,csv_rows) VALUES (?,?,?,?,?,?)`);
  let n = 0;
  db.exec('BEGIN');
  for (const fp of walk(base)) {
    const r = rel(fp);
    const sub = path.relative(base, fp).split(path.sep).join('/');
    const top = sub.split('/')[0] || null;
    const ext = path.extname(fp).toLowerCase();
    const buf = fs.readFileSync(fp);
    const sha = createHash('sha256').update(buf).digest('hex');
    let rows = null;
    if (ext === '.csv') { let c = 0; for (let i = 0; i < buf.length; i++) if (buf[i] === 10) c++; rows = Math.max(0, c - (buf.length && buf[buf.length - 1] !== 10 ? 0 : 1)); }
    stmt.run(r, top, ext, buf.length, sha, rows); n++;
  }
  db.exec('COMMIT');
  return n;
}

// ============================ build ============================
console.log(`Building ${rel(DB_PATH)} from ${DATA_DIR}/ ...\n`);
loadTable('sign_system', 'sign_systems.csv');
loadTable('sign', 'signs.csv');
loadTable('evidence_ref', 'evidence_refs.csv');
loadTable('namespace_gate', 'namespace_gates.csv');
loadTable('review_event', 'review_events.csv');
loadTable('witness', 'artifact_witnesses.csv');
loadTable('crosswalk_edge', 'crosswalk_edges.csv');
db.exec(`INSERT OR IGNORE INTO artifact(artifact_id) SELECT DISTINCT artifact_id FROM witness WHERE artifact_id IS NOT NULL AND artifact_id <> ''`);
loadClaims();
const nfiles = catalogData();

// ============================ audit ============================
db.exec('PRAGMA foreign_keys = ON;');
for (const v of db.prepare('PRAGMA foreign_key_check').all())
  issue('error', 'dangling_fk', v.table, v.rowid, `references missing parent in ${v.parent} (fkid ${v.fkid})`);
for (const [col, tbl] of [['image_ref_id', 'witness'], ['visual_ref_id', 'sign']]) {
  const n = db.prepare(`SELECT COUNT(*) n FROM ${tbl} WHERE ${col} IS NOT NULL AND ${col} <> '' AND ${col} NOT IN (SELECT ref_id FROM evidence_ref)`).get().n;
  if (n) issue('info', 'soft_ref_unresolved', `${tbl}.${col}`, null, `${n} rows reference an evidence_ref ref_id not loaded yet`);
}
for (const r of db.prepare(`SELECT ref_id, local_path, crop_path FROM evidence_ref`).all())
  for (const [f, val] of [['local_path', r.local_path], ['crop_path', r.crop_path]])
    if (val && !fs.existsSync(path.join(ROOT, val))) issue('warning', 'evidence_path_missing', 'evidence_ref', r.ref_id, `${f}=${val} not found`);
const missEv = db.prepare(`SELECT COUNT(*) n FROM claim_evidence WHERE path_exists = 0`).get().n;
if (missEv) issue('warning', 'claim_evidence_missing', 'claim_evidence', null, `${missEv} local claim-evidence path(s) do not exist on disk`);
const urlEv = db.prepare(`SELECT COUNT(*) n FROM claim_evidence WHERE path LIKE 'http%://%'`).get().n;
if (urlEv) issue('info', 'url_evidence', 'claim_evidence', null, `${urlEv} claim-evidence entries are URLs (not checked)`);

const ast = db.prepare(`INSERT INTO audit_issue (severity,code,obj,ref,message) VALUES (?,?,?,?,?)`);
db.exec('BEGIN'); for (const it of issues) ast.run(it.severity, it.code, it.obj, it.ref, it.message); db.exec('COMMIT');

// ============================ report ============================
const tables = ['sign_system', 'sign', 'artifact', 'witness', 'evidence_ref', 'crosswalk_edge', 'namespace_gate', 'review_event', 'claim', 'claim_evidence', 'data_file'];
const counts = Object.fromEntries(tables.map(t => [t, db.prepare(`SELECT COUNT(*) n FROM ${t}`).get().n]));
console.log('Row counts:');
for (const t of tables) console.log(`  ${t.padEnd(16)} ${String(counts[t]).padStart(7)}`);
const errs = issues.filter(i => i.severity === 'error'), warns = issues.filter(i => i.severity === 'warning');
console.log(`\nAudit: ${errs.length} error(s), ${warns.length} warning(s), ${issues.length - errs.length - warns.length} info`);
for (const it of [...errs, ...warns].slice(0, 20)) console.log(`  [${it.severity}] ${it.code} ${it.obj ?? ''} ${it.ref ?? ''} — ${it.message}`);
fs.writeFileSync(path.join(ROOT, 'db', 'audit_report.json'), JSON.stringify({ db: rel(DB_PATH), data_dir: DATA_DIR, data_files_cataloged: nfiles, counts, issues }, null, 2));
db.close();
console.log(`\nWrote ${rel(DB_PATH)} and db/audit_report.json`);
