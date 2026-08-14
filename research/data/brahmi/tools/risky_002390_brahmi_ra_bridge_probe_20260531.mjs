// A "risky bet" probe (2026-05-31, wild-shot tier): does the surviving 002-390
// branch-selector frame have a "ra"-like bridge into Brahmi? The idea being
// tested is that sign 390 (the frame head) and the branch signs 125/530/590
// (open-continue) and 095/692/705/707 (close-terminal) might show consistent
// pressure toward the Brahmi letter "ra". The script reads the v3 impostor-forger
// CSV, keeps only these eight signs, tags each row with its branch role and
// whether its modal Brahmi label is "ra", and checks whether any row clears both
// the impostor null and the original shape null at 0.01. It writes a JSON bet
// record, a one-row summary CSV, and a per-probe CSV, all prefixed
// risky_002390_brahmi_ra_bridge_probe_20260531. The recorded outcome: no row
// passes both thresholds, so the ra bridge stays non-evidential.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const FORGER = path.join(ROOT, 'data', 'brahmi', 'brahmi_real_token_impostor_forger_v3.csv');
const OUT_DIR = path.join(ROOT, 'data', 'brahmi');
const PREFIX = 'risky_002390_brahmi_ra_bridge_probe_20260531';
const RUN_DATE = '2026-05-31';
const SIGNS = new Set(['390', '125', '530', '590', '095', '692', '705', '707']);

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

function num(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : NaN;
}

const rows = parseCsv(fs.readFileSync(FORGER, 'utf8')).filter((row) => SIGNS.has(row.sign_id));
const present = new Set(rows.map((row) => row.sign_id));
const missing = [...SIGNS].filter((sign) => !present.has(sign)).sort();

const probes = rows.map((row) => ({
  sign_id: row.sign_id,
  branch_role:
    row.sign_id === '390'
      ? 'frame_head'
      : ['125', '530', '590'].includes(row.sign_id)
        ? 'open_continue_branch'
        : 'close_terminal_branch',
  orientation_policy: row.orientation_policy,
  sample_count: row.sample_count,
  modal_brahmi_label: row.modal_brahmi_label,
  v3_cisi_modal_label: row.v3_cisi_modal_label,
  v3_cisi_modal_share: row.v3_cisi_modal_share,
  original_shape_null_share: row.original_shape_null_share,
  original_label_null_share: row.original_label_null_share,
  impostor_ge_observed_share: row.impostor_ge_observed_share,
  gate_decision: row.gate_decision,
  blocked_reason: row.blocked_reason,
  ra_like_modal: String(row.modal_brahmi_label === 'ra' || row.v3_cisi_modal_label === 'ra'),
}));

const raLike = probes.filter((row) => row.ra_like_modal === 'true');
const lowEnough = probes.filter((row) => num(row.impostor_ge_observed_share) <= 0.01 && num(row.original_shape_null_share) <= 0.01);
const bestRows = probes
  .slice()
  .sort((a, b) => num(a.impostor_ge_observed_share) - num(b.impostor_ge_observed_share))
  .slice(0, 5)
  .map((row) => `${row.sign_id}/${row.orientation_policy}:${row.modal_brahmi_label}->${row.v3_cisi_modal_label}:impostor=${row.impostor_ge_observed_share}`)
  .join(';');

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V3_002390_RA_LIKE_BRAHMI_BRIDGE_PROBE_20260531',
  vector: 'V3 descendant-script morphology',
  confidence_tier: 'wild shot',
  risky_bet:
    'The surviving `002-390` branch-selector frame might have a ra-like graphic/phonetic bridge: `390` as the frame head and `590` as one open branch both show ra-like Brahmi modal pressure.',
  observed:
    `Brahmi forger rows available for ${present.size}/${SIGNS.size} slot signs. Ra-like modal rows=${raLike.length}/${probes.length}; missing signs=${missing.join(';') || 'none'}. Best rows: ${bestRows}.`,
  adversarial_test:
    'Direct reuse of the real-token impostor forger v3: any bridge needs low impostor, low original shape-null, and source-token preflight. This probe only asks whether the V2 survivor has a descendant-script lead.',
  false_positive_rate:
    lowEnough.length === 0
      ? 'no row passes impostor<=0.01 and shape-null<=0.01; best impostor among slot signs remains above threshold'
      : 'unexpected_low_null_present',
  falsifier:
    'If future source-token crops for 390/590 stop returning ra-like labels, or if their real-token impostor and original shape-null rates remain high, the ra bridge stays non-evidential.',
  next_prediction:
    'A real promotion would require independent 390 and/or 590 source-token families converging on ra-like labels with impostor and shape-null rates at or below 0.01; absent that, do not assign phonetic values.',
};

fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}.json`), JSON.stringify({ ...summary, probes }, null, 2), 'utf8');
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
writeCsv(path.join(OUT_DIR, `${PREFIX}_probes.csv`), probes, [
  'sign_id',
  'branch_role',
  'orientation_policy',
  'sample_count',
  'modal_brahmi_label',
  'v3_cisi_modal_label',
  'v3_cisi_modal_share',
  'original_shape_null_share',
  'original_label_null_share',
  'impostor_ge_observed_share',
  'gate_decision',
  'blocked_reason',
  'ra_like_modal',
]);

console.log(JSON.stringify(summary, null, 2));
