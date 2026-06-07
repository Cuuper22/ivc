import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const CDLI_SUMMARY = path.join(ROOT, 'data', 'meluhha', 'cdli_context_lead_matched_negative_summary.csv');
const CONTEXT_407 = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_407_copper_tab_c_register_forger_20260531.json');
const REGISTER_407 = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_407_rectangular_copper_register_forger_20260531.json');
const OUT_DIR = path.join(ROOT, 'data', 'meluhha');
const PREFIX = 'risky_407_uruda_meluhha_diffuse_bridge_20260531';
const RUN_DATE = '2026-05-31';
const QUERIES = [
  'uruda me-luh-ha',
  'ma-na uruda me-luh-ha',
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

async function fetchCdliCount(query) {
  const url = `https://cdli.earth/search?atf_transliteration=${encodeURIComponent(query)}&format=json&limit=100`;
  const response = await fetch(url, { headers: { 'user-agent': 'codex-ivc-risky-407-uruda-bridge/2026-05-31' } });
  const text = await response.text();
  let parsed = [];
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = [];
  }
  const rows = Array.isArray(parsed) ? parsed : [];
  const normQuery = query.replaceAll('-', ' ');
  const lineRows = rows.map((row) => {
    const atf = row.inscription?.atf ?? '';
    const matchingLines = atf
      .split(/\r?\n/)
      .filter((line) => line.replaceAll('-', ' ').includes(normQuery))
      .join(' | ');
    return {
      query,
      artifact_id: `P${row.id}`,
      designation: row.designation ?? '',
      museum_no: row.museum_no ?? '',
      period: row.period?.period ?? row.period?.name ?? '',
      provenience: row.provenience?.provenience ?? '',
      dates_referenced: row.dates_referenced ?? '',
      genres: (row.genres ?? []).map((genre) => genre.genre ?? genre).join('|'),
      matching_lines: matchingLines,
    };
  });
  return {
    query,
    url,
    http_status: response.status,
    returned_artifacts_live: rows.length,
    artifact_ids_live: rows.map((row) => `P${row.id}`).join('|'),
    designations_live: rows.map((row) => row.designation ?? '').filter(Boolean).join('|'),
    museum_numbers_live: rows.map((row) => row.museum_no ?? '').filter(Boolean).join('|'),
    administrative_line_artifacts: lineRows.filter((row) => /ma-na/.test(row.matching_lines) && !/lexical/i.test(row.genres)).map((row) => row.artifact_id).join('|'),
    lexical_line_artifacts: lineRows.filter((row) => /lexical/i.test(row.genres) || /MSL/.test(row.designation)).map((row) => row.artifact_id).join('|'),
    line_rows: lineRows,
  };
}

const cdliRows = parseCsv(fs.readFileSync(CDLI_SUMMARY, 'utf8'));
const localQueryRows = QUERIES.map((query) => cdliRows.find((row) => row.query_text === query)).filter(Boolean);
const context407 = JSON.parse(fs.readFileSync(CONTEXT_407, 'utf8'));
const register407 = fs.existsSync(REGISTER_407) ? JSON.parse(fs.readFileSync(REGISTER_407, 'utf8')) : null;
const liveRows = [];
for (const query of QUERIES) liveRows.push(await fetchCdliCount(query));

const urudaLocal = localQueryRows.find((row) => row.query_text === 'uruda me-luh-ha');
const manaLocal = localQueryRows.find((row) => row.query_text === 'ma-na uruda me-luh-ha');
const urudaLive = liveRows.find((row) => row.query === 'uruda me-luh-ha');
const manaLive = liveRows.find((row) => row.query === 'ma-na uruda me-luh-ha');
const tier =
  context407.confidence_tier === 'candidate' &&
  Number(urudaLive.returned_artifacts_live) >= 2 &&
  Number(urudaLocal?.query_line_anywhere_false_positive_rate ?? 1) === 0 &&
  Number(context407.false_positive_rate) <= 0.01
    ? 'candidate'
    : 'wild shot';

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V1_V4_407_URUDA_MELUHHA_DIFFUSE_BRIDGE_20260531',
  vector: 'V1 diffuse Meluhha bilingual + V4 context-to-meaning',
  confidence_tier: tier,
  risky_bet:
    '`407` is a meaning-level rectangular/copper administrative-register sign, with copper/TAB:C as the commodity-bearing subtype that converges with the readable cuneiform expression `uruda me-luh-ha`. This is a diffuse semantic bridge only: it predicts carrier/register and commodity class, not the phonetic value of 407.',
  observed:
    `Indus side broad register: ${register407 ? register407.observed : 'broad register report unavailable'}. Indus side copper subtype: ${context407.observed} Cuneiform side live CDLI: uruda me-luh-ha=${urudaLive.returned_artifacts_live} artifacts (${urudaLive.artifact_ids_live}); ma-na uruda me-luh-ha=${manaLive.returned_artifacts_live} artifact (${manaLive.artifact_ids_live}). Local CDLI negative gate for uruda me-luh-ha reports query-line false-positive ${urudaLocal?.query_line_anywhere_false_positive_rate}.`,
  adversarial_test:
    'Joined independently generated positive bets: all-sign/max-stat Indus 407 rectangular/copper register context, narrower 407 copper/TAB:C subtype, and live primary CDLI verification of the Meluhha copper phrase, with live line-context classification into administrative and lexical witnesses. No object-level Indus+cuneiform bilingual is asserted.',
  false_positive_rate: Math.max(Number(register407?.false_positive_rate ?? 0), Number(context407.false_positive_rate), Number(urudaLocal?.query_line_anywhere_false_positive_rate ?? 1)),
  indus_407_register_false_positive_rate: register407?.false_positive_rate ?? '',
  indus_407_false_positive_rate: context407.false_positive_rate,
  cdli_uruda_meluhha_query_line_false_positive_rate: urudaLocal?.query_line_anywhere_false_positive_rate ?? '',
  cdli_uruda_meluhha_live_url: urudaLive.url,
  falsifier:
    'If source-checked SEAL:R or copper/TAB:C Indus rows do not preserve 407, or if non-register contexts accumulate 407 at comparable rates under the same max-stat and leave-site controls, the semantic bridge collapses. If CDLI duplicate review reduces `uruda me-luh-ha` to a non-commodity lexical/list artifact only, the external side demotes.',
  next_prediction:
    'Unverified rectangular seal and copper/TAB:C Indus rows should be enriched for 407. A future real object-level bilingual involving Meluhha copper should be checked first for a 407-bearing Indus side, but no reading is earned yet.',
  non_claim:
    'No phonetic assignment of 407 to uruda, me-luh-ha, or any syllable is made. P136689 is an administrative commodity witness, P228742 is lexical-list support for the expression, and neither is paired with an Indus object. This is not an accepted external anchor because there is no shared object, owner, seal impression, or accession bridge.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(
  path.join(OUT_DIR, `${PREFIX}.json`),
  JSON.stringify({ ...summary, live_cdli_rows: liveRows, local_cdli_rows: localQueryRows }, null, 2),
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
  'indus_407_register_false_positive_rate',
  'indus_407_false_positive_rate',
  'cdli_uruda_meluhha_query_line_false_positive_rate',
  'cdli_uruda_meluhha_live_url',
  'falsifier',
  'next_prediction',
  'non_claim',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_live_cdli.csv`), liveRows, [
  'query',
  'url',
  'http_status',
  'returned_artifacts_live',
  'artifact_ids_live',
  'designations_live',
  'museum_numbers_live',
  'administrative_line_artifacts',
  'lexical_line_artifacts',
]);
writeCsv(path.join(OUT_DIR, `${PREFIX}_live_cdli_lines.csv`), liveRows.flatMap((row) => row.line_rows), [
  'query',
  'artifact_id',
  'designation',
  'museum_no',
  'period',
  'provenience',
  'dates_referenced',
  'genres',
  'matching_lines',
]);

console.log(JSON.stringify(summary, null, 2));
