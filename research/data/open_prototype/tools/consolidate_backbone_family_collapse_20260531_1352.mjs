import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'consolidate_backbone_family_collapse_20260531_1352';
const RUN_DATE = '2026-05-31T13:52:18-07:00';
const ITERATIONS = 5000;
const CORE_CONSTRAINTS = [
  ['400_before_740', '400', '740'],
  ['740_before_002', '740', '002'],
  ['740_before_861', '740', '861'],
  ['740_before_820', '740', '820'],
  ['740_before_817', '740', '817'],
  ['002_before_861', '002', '861'],
  ['002_before_820', '002', '820'],
  ['002_before_817', '002', '817'],
  ['806_before_002', '806', '002'],
];

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

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function familyKey(row, mode) {
  const fields = {
    carrier: [row.site, row.type, row.symbol, row.cult, row.material, row.shape],
    site_type: [row.site, row.type],
    icon_type: [row.type, row.symbol, row.cult],
    broad: [row.region, row.type, row.symbol],
  }[mode];
  return fields.map((value) => norm(value)).join('|');
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffleInPlace(arr, rand) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}

function familyVotes(rows, constraint, mode, shuffled = false, rand = null) {
  const [, left, right] = constraint;
  const families = new Map();
  for (const row of rows) {
    const signs = shuffled ? row.signs.slice() : row.signs;
    if (shuffled) shuffleInPlace(signs, rand);
    const li = signs.indexOf(left);
    const ri = signs.indexOf(right);
    if (li < 0 || ri < 0) continue;
    const key = familyKey(row, mode);
    const vote = li < ri ? 'satisfied' : 'violated';
    if (!families.has(key)) families.set(key, { satisfied_rows: 0, violated_rows: 0, examples: [] });
    const family = families.get(key);
    if (vote === 'satisfied') family.satisfied_rows += 1;
    else family.violated_rows += 1;
    if (family.examples.length < 5) family.examples.push(`${objectId(row)}:${norm(row.site)}:${norm(row.type)}:${norm(row.symbol)}:${row.text}`);
  }
  let satisfiedFamilies = 0;
  let violatedFamilies = 0;
  let tiedFamilies = 0;
  for (const family of families.values()) {
    if (family.satisfied_rows > family.violated_rows) satisfiedFamilies += 1;
    else if (family.violated_rows > family.satisfied_rows) violatedFamilies += 1;
    else tiedFamilies += 1;
  }
  return {
    family_count: families.size,
    satisfied_families: satisfiedFamilies,
    violated_families: violatedFamilies,
    tied_families: tiedFamilies,
    share: families.size ? satisfiedFamilies / families.size : 0,
    families,
  };
}

function rowVotes(rows, constraint) {
  const [, left, right] = constraint;
  let total = 0;
  let satisfied = 0;
  for (const row of rows) {
    const li = row.signs.indexOf(left);
    const ri = row.signs.indexOf(right);
    if (li < 0 || ri < 0) continue;
    total += 1;
    if (li < ri) satisfied += 1;
  }
  return { total, satisfied, share: total ? satisfied / total : 0 };
}

function nullForConstraint(rows, constraint, mode, observedShare, observedSatisfiedFamilies, iterations = ITERATIONS) {
  const rand = mulberry32(0xfa1352 ^ rows.length ^ mode.length ^ constraint[0].length);
  let shareGe = 0;
  let satisfiedGe = 0;
  const iterationRows = [];
  for (let iter = 0; iter < iterations; iter += 1) {
    const shuffled = familyVotes(rows, constraint, mode, true, rand);
    const shareHit = shuffled.share >= observedShare;
    const satisfiedHit = shuffled.satisfied_families >= observedSatisfiedFamilies;
    if (shareHit) shareGe += 1;
    if (satisfiedHit) satisfiedGe += 1;
    if (iter < 50 || shareHit || satisfiedHit) {
      iterationRows.push({
        iteration: iter,
        constraint_id: constraint[0],
        mode,
        shuffled_satisfied_families: shuffled.satisfied_families,
        shuffled_family_count: shuffled.family_count,
        shuffled_share: shuffled.share,
        share_ge_observed: String(shareHit),
        satisfied_ge_observed: String(satisfiedHit),
      });
    }
  }
  return {
    share_fpr: shareGe / iterations,
    satisfied_fpr: satisfiedGe / iterations,
    iterationRows,
  };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length);

const modes = ['carrier', 'site_type', 'icon_type', 'broad'];
const summaryRows = [];
const familyRows = [];
const nullRows = [];

for (const mode of modes) {
  for (const constraint of CORE_CONSTRAINTS) {
    const rowVote = rowVotes(rows, constraint);
    const famVote = familyVotes(rows, constraint, mode);
    const nullResult = famVote.family_count >= 5
      ? nullForConstraint(rows, constraint, mode, famVote.share, famVote.satisfied_families)
      : { share_fpr: null, satisfied_fpr: null, iterationRows: [] };
    const verdict =
      famVote.family_count >= 5 &&
      famVote.share >= 0.8 &&
      (nullResult.share_fpr === null || nullResult.share_fpr <= 0.01)
        ? 'survives_family_collapse'
        : famVote.family_count < 5
          ? 'too_few_families'
          : 'weak_after_family_collapse';
    summaryRows.push({
      mode,
      constraint_id: constraint[0],
      left: constraint[1],
      right: constraint[2],
      row_satisfied: rowVote.satisfied,
      row_total: rowVote.total,
      row_share: rowVote.share,
      family_satisfied: famVote.satisfied_families,
      family_violated: famVote.violated_families,
      family_tied: famVote.tied_families,
      family_count: famVote.family_count,
      family_share: famVote.share,
      null_share_fpr: nullResult.share_fpr,
      null_satisfied_fpr: nullResult.satisfied_fpr,
      verdict,
    });
    nullRows.push(...nullResult.iterationRows);
    for (const [key, family] of famVote.families.entries()) {
      familyRows.push({
        mode,
        constraint_id: constraint[0],
        family_key: key,
        satisfied_rows: family.satisfied_rows,
        violated_rows: family.violated_rows,
        majority: family.satisfied_rows > family.violated_rows ? 'satisfied' : family.violated_rows > family.satisfied_rows ? 'violated' : 'tied',
        examples: family.examples.join(' | '),
      });
    }
  }
}

const modeSummaries = modes.map((mode) => {
  const rowsForMode = summaryRows.filter((row) => row.mode === mode);
  return {
    mode,
    surviving_constraints: rowsForMode.filter((row) => row.verdict === 'survives_family_collapse').length,
    weak_constraints: rowsForMode.filter((row) => row.verdict === 'weak_after_family_collapse').map((row) => row.constraint_id).join(';'),
    too_few_family_constraints: rowsForMode.filter((row) => row.verdict === 'too_few_families').map((row) => row.constraint_id).join(';'),
  };
});

const hardFailures = summaryRows.filter((row) => row.mode === 'carrier' && row.verdict === 'weak_after_family_collapse');
const conclusion = hardFailures.length === 0
  ? 'backbone_survives_family_collapse'
  : 'backbone_needs_family_scoped_demotions';

const summary = {
  run_date_time: RUN_DATE,
  phase: 'CONSOLIDATE',
  bet_under_attack: 'minimal_role_backbone',
  test_type: 'metadata-family collapsed majority voting',
  conclusion,
  observed:
    `Carrier-family collapse: ${modeSummaries.find((row) => row.mode === 'carrier').surviving_constraints}/${CORE_CONSTRAINTS.length} constraints survive; weak=${modeSummaries.find((row) => row.mode === 'carrier').weak_constraints || 'none'}; too-few=${modeSummaries.find((row) => row.mode === 'carrier').too_few_family_constraints || 'none'}. ` +
    `Broad-family collapse: ${modeSummaries.find((row) => row.mode === 'broad').surviving_constraints}/${CORE_CONSTRAINTS.length} survive; weak=${modeSummaries.find((row) => row.mode === 'broad').weak_constraints || 'none'}; too-few=${modeSummaries.find((row) => row.mode === 'broad').too_few_family_constraints || 'none'}.`,
  consolidation_decision:
    conclusion === 'backbone_survives_family_collapse'
      ? 'Keep the role backbone promoted; family collapse does not expose repeated-row inflation.'
      : 'Do not promote failed constraints outside row-level support; scope or demote weak family-collapsed edges.',
  mode_summaries: modeSummaries,
  constraints: summaryRows,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${PREFIX}.json`), JSON.stringify(summary, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${PREFIX}_summary.csv`), summaryRows, [
  'mode',
  'constraint_id',
  'left',
  'right',
  'row_satisfied',
  'row_total',
  'row_share',
  'family_satisfied',
  'family_violated',
  'family_tied',
  'family_count',
  'family_share',
  'null_share_fpr',
  'null_satisfied_fpr',
  'verdict',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_mode_summaries.csv`), modeSummaries, [
  'mode',
  'surviving_constraints',
  'weak_constraints',
  'too_few_family_constraints',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_families.csv`), familyRows, [
  'mode',
  'constraint_id',
  'family_key',
  'satisfied_rows',
  'violated_rows',
  'majority',
  'examples',
]);
writeCsv(path.join(REPORTS, `${PREFIX}_forger_iterations.csv`), nullRows, [
  'iteration',
  'constraint_id',
  'mode',
  'shuffled_satisfied_families',
  'shuffled_family_count',
  'shuffled_share',
  'share_ge_observed',
  'satisfied_ge_observed',
]);

console.log(JSON.stringify(summary, null, 2));
