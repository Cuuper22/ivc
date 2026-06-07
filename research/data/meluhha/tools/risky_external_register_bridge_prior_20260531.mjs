import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const CUNEIFORM = path.join(ROOT, 'data', 'meluhha', 'cuneiform_attestations_expanded.csv');
const INDUS_407 = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_407_rectangular_copper_register_forger_20260531.json');
const SLOT_740407 = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_740_407_register_opening_model_20260531.json');
const SLOT_407806 = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_407_806_register_slot_split_forger_20260531.json');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_external_register_bridge_prior_20260531';
const RUN_DATE = '2026-05-31';

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

function classify(row) {
  const tokenType = row.token_type ?? '';
  const relation = row.meluhha_relation ?? '';
  const genre = row.genre ?? '';
  const text = `${tokenType} ${relation} ${genre}`.toLowerCase();
  if (text.includes('personal_name')) return 'onomastic';
  if (text.includes('commodity') || text.includes('object') || text.includes('route') || text.includes('ship')) return 'commodity_route_object';
  if (text.includes('ethnonym') || text.includes('title') || text.includes('origin')) return 'ethnonym_title_origin';
  if (text.includes('administrative')) return 'administrative_other';
  if (text.includes('literary')) return 'literary_toponym';
  return 'other';
}

function directness(row) {
  const relation = String(row.meluhha_relation ?? '').toLowerCase();
  const type = String(row.token_type ?? '').toLowerCase();
  if (relation.includes('direct') || type.includes('direct')) return 'direct';
  if (relation.includes('adjacent') || type.includes('adjacent')) return 'adjacent';
  return 'contextual';
}

const cuneiformRows = parseCsv(fs.readFileSync(CUNEIFORM, 'utf8'));
const uniqueRows = [...new Map(cuneiformRows.map((row) => [
  `${row.source_system}|${row.source_id}|${row.line_ref}|${row.transliteration}`,
  row,
])).values()];

const classRows = uniqueRows.map((row) => ({
  class: classify(row),
  directness: directness(row),
  source_system: row.source_system,
  source_id: row.source_id,
  line_ref: row.line_ref,
  transliteration: row.transliteration,
  token_type: row.token_type,
  meluhha_relation: row.meluhha_relation,
  period: row.period,
  provenience: row.provenience,
  genre: row.genre,
  source_url: row.source_url,
}));
const byClass = Object.entries(classRows.reduce((acc, row) => {
  acc[row.class] = (acc[row.class] ?? 0) + 1;
  return acc;
}, {})).map(([klass, count]) => ({ class: klass, count })).sort((a, b) => b.count - a.count || a.class.localeCompare(b.class));
const directByClass = Object.entries(classRows.filter((row) => row.directness === 'direct').reduce((acc, row) => {
  acc[row.class] = (acc[row.class] ?? 0) + 1;
  return acc;
}, {})).map(([klass, count]) => ({ class: klass, count })).sort((a, b) => b.count - a.count || a.class.localeCompare(b.class));

const commodityOrRegister = classRows.filter((row) => ['commodity_route_object', 'administrative_other'].includes(row.class));
const onomastic = classRows.filter((row) => row.class === 'onomastic');
const directCommodityOrRegister = classRows.filter((row) => row.directness === 'direct' && ['commodity_route_object', 'administrative_other'].includes(row.class));
const directOnomastic = classRows.filter((row) => row.directness === 'direct' && row.class === 'onomastic');

const indus407 = JSON.parse(fs.readFileSync(INDUS_407, 'utf8'));
const slot740407 = JSON.parse(fs.readFileSync(SLOT_740407, 'utf8'));
const slot407806 = JSON.parse(fs.readFileSync(SLOT_407806, 'utf8'));

const bridgeTier =
  directCommodityOrRegister.length > directOnomastic.length &&
  indus407.confidence_tier === 'promoted candidate' &&
  slot740407.confidence_tier === 'promoted candidate' &&
  ['candidate', 'promoted candidate'].includes(slot407806.confidence_tier)
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V1_EXTERNAL_REGISTER_BRIDGE_PRIOR_20260531',
  vector: 'V1 diffuse Meluhha bilingual + V4 context-to-meaning + V2 slot grammar',
  confidence_tier: bridgeTier,
  risky_bet:
    'The most promising diffuse Meluhha bridge is not an onomastic square-seal reading. It is a commodity/account register bridge: cuneiform Meluhha attestations should weight commodity/administrative/route contexts enough that the Indus-side search should prioritize SEAL:R/TAB:C rows carrying the 740/407/806 register grammar.',
  observed:
    `Cuneiform unique rows=${uniqueRows.length}. Class counts: ${byClass.map((row) => `${row.class}:${row.count}`).join(';')}. Direct class counts: ${directByClass.map((row) => `${row.class}:${row.count}`).join(';')}. Direct commodity/register=${directCommodityOrRegister.length}; direct onomastic=${directOnomastic.length}. Indus side: 407 register tier=${indus407.confidence_tier}; 740/407 opener tier=${slot740407.confidence_tier}; 407/806 slot split tier=${slot407806.confidence_tier}.`,
  adversarial_test:
    'Deduplicates cuneiform attestations by source/line/transliteration, bins them before looking at the Indus summaries, and requires the Indus-side register and slot-grammar bets to have already survived their own max-stat/forger controls. This is a search-prior bridge, not an object-level bilingual.',
  false_positive_rate:
    'not a phonetic-anchor FPR: the Indus components report 0 max-stat FPR in their own forgers; cuneiform class prior has no object-level pair and remains candidate-only',
  falsifier:
    'If deduplicated cuneiform review shows Meluhha is predominantly personal-name/owner context, or if future external Indus objects with readable cuneiform links are square animal seals without 740/407/806 register grammar, demote this bridge prior.',
  next_prediction:
    'For Ur/Gulf/Mesopotamian Indus-style objects with credible trade linkage, prioritize source-checking SEAL:R/TAB:C or rectangular/copper-like rows containing 740, 407, or 806 before attempting owner-name readings. A real object-level bridge would promote this; absence of such rows would kill it.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, by_class: byClass, direct_by_class: directByClass, class_rows: classRows }, null, 2),
  'utf8',
);
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [summary], [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'falsifier',
  'next_prediction',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_class_counts.csv`), byClass, ['class', 'count']);
writeCsv(path.join(OUT_DIR, `${PREFIX}_direct_class_counts.csv`), directByClass, ['class', 'count']);
writeCsv(path.join(OUT_DIR, `${PREFIX}_rows.csv`), classRows, [
  'class',
  'directness',
  'source_system',
  'source_id',
  'line_ref',
  'transliteration',
  'token_type',
  'meluhha_relation',
  'period',
  'provenience',
  'genre',
  'source_url',
]);

console.log(JSON.stringify(summary, null, 2));
