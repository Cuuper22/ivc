import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const BRAHMI = path.join(ROOT, 'data', 'brahmi', 'brahmi_real_token_low_null_reaudit_20260531.csv');
const HEAD_SCAN = path.join(ROOT, 'data', 'open_prototype', 'reports', 'risky_002_head_branch_determinism_scan_20260531_heads.csv');
const OUT_DIR = path.join(ROOT, 'data', 'brahmi');
const PREFIX = 'risky_ra_like_branch_pair_20260531';
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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

const metadata = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const brahmi = parseCsv(fs.readFileSync(BRAHMI, 'utf8'));
const headScan = parseCsv(fs.readFileSync(HEAD_SCAN, 'utf8'));

function positionStats(sign) {
  let total = 0;
  let initial = 0;
  let terminal = 0;
  let after002Head = 0;
  for (const row of metadata) {
    row.signs.forEach((item, idx) => {
      if (item !== sign) return;
      total += 1;
      if (idx === 0) initial += 1;
      if (idx === row.signs.length - 1) terminal += 1;
      if (row.signs[idx - 1] === '002') after002Head += 1;
    });
  }
  return { sign, total, initial, terminal, terminal_rate: total ? terminal / total : 0, after002Head };
}

function bestBrahmi(sign) {
  const rows = brahmi.filter((row) => row.sign_id === sign);
  rows.sort((a, b) => Number(a.impostor_ge_observed_share) - Number(b.impostor_ge_observed_share));
  return rows[0] ?? null;
}

const signs = ['002', '861'];
const signRows = signs.map((sign) => {
  const b = bestBrahmi(sign);
  const p = positionStats(sign);
  const h = headScan.find((row) => row.head === sign);
  return {
    sign,
    modal_brahmi_label: b?.modal_brahmi_label ?? '',
    v3_cisi_modal_label: b?.v3_cisi_modal_label ?? '',
    impostor_ge_observed_share: b?.impostor_ge_observed_share ?? '',
    original_shape_null_share: b?.original_shape_null_share ?? '',
    original_label_null_share: b?.original_label_null_share ?? '',
    unique_cisi_count: b?.unique_cisi_count ?? '',
    fail_duplicate_unanimity: b?.fail_duplicate_unanimity ?? '',
    total_occurrences: p.total,
    initial_rate: p.total ? p.initial / p.total : '',
    terminal_rate: p.terminal_rate,
    after_002_head_rows: p.after002Head,
    head_branch_rows: h?.frame_rows ?? '',
    head_branch_count: h?.branch_count ?? '',
    head_determinism_p: h?.determinism_p ?? '',
    exact_text_head_determinism_p: h?.exact_text_determinism_p ?? '',
  };
});

const allRaLike = brahmi.filter((row) => row.modal_brahmi_label === 'ra' || row.v3_cisi_modal_label === 'ra');
const allLowImpostor = brahmi.filter((row) => Number(row.impostor_ge_observed_share) <= 0.001);
const bet = {
  run_date: RUN_DATE,
  bet_id: 'V3_RA_LIKE_002_861_BRANCH_PAIR_20260531',
  vector: 'V3 backward Brahmi / descendant morphology',
  confidence_tier: 'wild shot',
  risky_bet: '`002` and `861` are a ra-like graphic pair that later converges on Brahmi `ra`, and their shared branch-grammar behavior is why both surfaced in the low-impostor descent screen.',
  observed: `002 best Brahmi row: modal ${signRows[0].modal_brahmi_label}/${signRows[0].v3_cisi_modal_label}, impostor FPR ${signRows[0].impostor_ge_observed_share}, shape-null ${signRows[0].original_shape_null_share}, label-null ${signRows[0].original_label_null_share}, terminal rate ${Number(signRows[0].terminal_rate).toFixed(3)}. 861 best Brahmi row: modal ${signRows[1].modal_brahmi_label}/${signRows[1].v3_cisi_modal_label}, impostor FPR ${signRows[1].impostor_ge_observed_share}, shape-null ${signRows[1].original_shape_null_share}, label-null ${signRows[1].original_label_null_share}, terminal rate ${Number(signRows[1].terminal_rate).toFixed(3)}, 002-head determinism p ${signRows[1].head_determinism_p}. Ra-like low-impostor rows in whole screen: ${allRaLike.length}; impostor<=0.001 rows: ${allLowImpostor.length}.`,
  adversarial_test: 'Positive bet is tied to the real-token impostor screen plus corpus role. It is explicitly failed by shape-null, label-null, duplicate-unanimity, and v3 preflight, so it stays below candidate.',
  false_positive_rate: 'not_admissible_as_anchor',
  falsifier: 'Any independent source-token rerun moving either 002 or 861 away from ra-like modal labels, or showing the branch grammar is not source-stable, kills the pair. Passing duplicate collapse and shape/label nulls would be required before promotion.',
  next_prediction: 'If this wild shot is real, new source-normalized tokens for 002 and 861 should keep ra-like graphic nearest neighbors, while other deterministic heads such as 390 should not necessarily be ra-like.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({ ...bet, signs: signRows }, null, 2));
writeCsv(path.join(OUT_DIR, `${PREFIX}.csv`), [bet], [
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
writeCsv(path.join(OUT_DIR, `${PREFIX}_signs.csv`), signRows, [
  'sign',
  'modal_brahmi_label',
  'v3_cisi_modal_label',
  'impostor_ge_observed_share',
  'original_shape_null_share',
  'original_label_null_share',
  'unique_cisi_count',
  'fail_duplicate_unanimity',
  'total_occurrences',
  'initial_rate',
  'terminal_rate',
  'after_002_head_rows',
  'head_branch_rows',
  'head_branch_count',
  'head_determinism_p',
  'exact_text_head_determinism_p',
]);
console.log(JSON.stringify(bet, null, 2));
