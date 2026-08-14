// Many bas-relief and incised tablets (types TAB:B and TAB:I) carry text on
// several faces, recorded as row ids like `1234.1`, `1234.2` — the suffix is the
// face number. The bet: sign `400` marks the primary heading face (face 1), not
// just tablet inscriptions in general. The script reads metadata_filtered.csv,
// keeps complete TAB:B/TAB:I rows with numbered faces, groups them by physical
// object, and keeps multi-face objects where at least one face carries 400. It then
// counts how often the 400-bearing faces are face 1. The null keeps each object's
// face count and its number of 400-bearing faces fixed, and shuffles which faces
// carry 400, 10,000 times — pricing both the total primary-face hits and the number
// of objects where every 400 face is primary. Writes a witnesses CSV and a JSON
// summary to the reports directory.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_400_primary_face_heading_forger_20260531';
const RUN_DATE = '2026-05-31';
const TARGET = '400';
const ITERATIONS = 10000;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        cell += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        cell += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(cell);
      cell = '';
    } else if (ch === '\n') {
      row.push(cell.replace(/\r$/, ''));
      if (row.some((value) => value.length)) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    if (row.some((value) => value.length)) rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((cols) => Object.fromEntries(header.map((name, idx) => [name, cols[idx] ?? ''])));
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function sideIndex(id) {
  const m = String(id ?? '').match(/\.(\d+)$/);
  return m ? Number(m[1]) : null;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : String(row.id).replace(/\.\d+$/, '');
}

function esc(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function chooseK(n, k) {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = 0; i < k; i += 1) {
    const j = i + Math.floor(Math.random() * (n - i));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return new Set(arr.slice(0, k));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8'))
  .map((row) => ({
    ...row,
    object: objectId(row),
    side: sideIndex(row.id),
    toks: tokens(row.text),
  }))
  .filter((row) => row.complete === 'Y')
  .filter((row) => row.type === 'TAB:B' || row.type === 'TAB:I')
  .filter((row) => row.side !== null);

const groups = new Map();
for (const row of rows) {
  if (!groups.has(row.object)) groups.set(row.object, []);
  groups.get(row.object).push(row);
}

const scopeGroups = [...groups.values()]
  .map((group) => group.sort((a, b) => a.side - b.side))
  .filter((group) => group.length >= 2)
  .filter((group) => group.some((row) => row.toks.includes(TARGET)));

const witnessRows = scopeGroups.flatMap((group) => group);
const targetRows = witnessRows.filter((row) => row.toks.includes(TARGET));
const nonTargetRows = witnessRows.filter((row) => !row.toks.includes(TARGET));
const primaryTarget = targetRows.filter((row) => row.side === 1).length;
const primaryNonTarget = nonTargetRows.filter((row) => row.side === 1).length;

let targetPrimaryGe = 0;
let targetPrimaryMean = 0;
let allPrimaryGe = 0;
let allPrimaryMean = 0;
const observedAllPrimary = scopeGroups.filter((group) =>
  group.filter((row) => row.toks.includes(TARGET)).every((row) => row.side === 1)
).length;

for (let iter = 0; iter < ITERATIONS; iter += 1) {
  let simPrimary = 0;
  let simAllPrimary = 0;
  for (const group of scopeGroups) {
    const k = group.filter((row) => row.toks.includes(TARGET)).length;
    const chosen = chooseK(group.length, k);
    let groupAllPrimary = true;
    for (const idx of chosen) {
      if (group[idx].side === 1) simPrimary += 1;
      else groupAllPrimary = false;
    }
    if (groupAllPrimary) simAllPrimary += 1;
  }
  targetPrimaryMean += simPrimary;
  allPrimaryMean += simAllPrimary;
  if (simPrimary >= primaryTarget) targetPrimaryGe += 1;
  if (simAllPrimary >= observedAllPrimary) allPrimaryGe += 1;
}

targetPrimaryMean /= ITERATIONS;
allPrimaryMean /= ITERATIONS;

const witnesses = targetRows.map((row) => ({
  object: row.object,
  row_id: row.id,
  cisi: row.cisi,
  site: row.site,
  type: row.type,
  side: row.side,
  text: row.text,
  primary_side: row.side === 1 ? 'yes' : 'no',
}));

const summary = {
  date: RUN_DATE,
  candidate_id: PREFIX,
  tier: 'wild_shot',
  bet: '400 marks the primary heading face of multi-row TAB:B/I account tablets rather than merely belonging to the tablet register.',
  scope: {
    complete_tab_b_i_rows_with_numbered_sides: rows.length,
    multirow_artifact_groups_with_400: scopeGroups.length,
    rows_inside_scope_groups: witnessRows.length,
    target_400_rows_inside_scope: targetRows.length,
  },
  observed: {
    primary_400_rows: primaryTarget,
    nonprimary_400_rows: targetRows.length - primaryTarget,
    primary_non400_rows_in_same_artifacts: primaryNonTarget,
    nonprimary_non400_rows_in_same_artifacts: nonTargetRows.length - primaryNonTarget,
    groups_where_all_400_rows_are_primary: observedAllPrimary,
  },
  within_artifact_side_shuffle_null: {
    iterations: ITERATIONS,
    preserves: 'artifact group size and number of 400-bearing rows per artifact; only side assignment is shuffled',
    mean_primary_400_rows: Number(targetPrimaryMean.toFixed(6)),
    p_ge_observed_primary_400_rows: targetPrimaryGe / ITERATIONS,
    mean_groups_all_400_primary: Number(allPrimaryMean.toFixed(6)),
    p_ge_observed_groups_all_400_primary: allPrimaryGe / ITERATIONS,
  },
  decision: null,
};

summary.decision = summary.within_artifact_side_shuffle_null.p_ge_observed_primary_400_rows <= 0.01
  ? 'candidate_survives_first_adversary'
  : 'wild_shot_demoted_or_killed';

fs.mkdirSync(OUT_DIR, { recursive: true });
writeCsv(path.join(OUT_DIR, `${PREFIX}_witnesses.csv`), witnesses, [
  'object', 'row_id', 'cisi', 'site', 'type', 'side', 'primary_side', 'text',
]);
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
