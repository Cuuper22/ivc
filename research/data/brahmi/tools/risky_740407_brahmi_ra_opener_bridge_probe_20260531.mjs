import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const FORGER = path.join(ROOT, 'data', 'brahmi', 'brahmi_real_token_impostor_forger_v3.csv');
const V2 = path.join(ROOT, 'data', 'brahmi', 'source_token_family_descent_summary_v2.csv');
const OUT_DIR = path.join(ROOT, 'data', 'brahmi');
const PREFIX = 'risky_740407_brahmi_ra_opener_bridge_probe_20260531';
const RUN_DATE = '2026-05-31';
const SIGNS = new Set(['740', '407']);

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

const forgerRows = parseCsv(fs.readFileSync(FORGER, 'utf8')).filter((row) => SIGNS.has(row.sign_id));
const v2Rows = parseCsv(fs.readFileSync(V2, 'utf8')).filter((row) => SIGNS.has(row.sign_id));

const probes = forgerRows.map((row) => {
  const v2 = v2Rows.find((candidate) => candidate.sign_id === row.sign_id && candidate.orientation_policy === row.orientation_policy) ?? {};
  const raLike =
    row.modal_brahmi_label === 'ra' ||
    row.v3_raw_modal_label === 'ra' ||
    row.v3_sha_modal_label === 'ra' ||
    row.v3_cisi_modal_label === 'ra';
  const passesAnchorGate =
    raLike &&
    num(row.original_shape_null_share) <= 0.01 &&
    num(row.original_label_null_share) <= 0.01 &&
    num(row.impostor_ge_observed_share) <= 0.01 &&
    row.v3_preflight_decision !== 'blocked_before_review' &&
    row.accepted_phonetic_anchor === 'true';
  return {
    sign_id: row.sign_id,
    orientation_policy: row.orientation_policy,
    sample_count: row.sample_count,
    modal_brahmi_label: row.modal_brahmi_label,
    v3_raw_modal_label: row.v3_raw_modal_label,
    v3_sha_modal_label: row.v3_sha_modal_label,
    v3_cisi_modal_label: row.v3_cisi_modal_label,
    v3_cisi_modal_share: row.v3_cisi_modal_share,
    ra_like: String(raLike),
    source_token_modal_share: v2.modal_share ?? '',
    original_shape_null_share: row.original_shape_null_share,
    original_label_null_share: row.original_label_null_share,
    impostor_ge_observed_share: row.impostor_ge_observed_share,
    v3_preflight_decision: row.v3_preflight_decision,
    gate_decision: row.gate_decision,
    accepted_phonetic_anchor: row.accepted_phonetic_anchor,
    blocked_reason: row.blocked_reason,
    passes_anchor_gate: String(passesAnchorGate),
  };
});

const signsWithRaPressure = new Set(probes.filter((row) => row.ra_like === 'true').map((row) => row.sign_id));
const signsPassingAnchor = new Set(probes.filter((row) => row.passes_anchor_gate === 'true').map((row) => row.sign_id));
const bestBySign = [...SIGNS].map((sign) => {
  const rows = probes.filter((row) => row.sign_id === sign);
  return rows.slice().sort((a, b) => num(a.impostor_ge_observed_share) - num(b.impostor_ge_observed_share))[0];
});
const sharedBridgeKilled =
  signsWithRaPressure.size === SIGNS.size &&
  signsPassingAnchor.size !== SIGNS.size;

const summary = {
  run_date: RUN_DATE,
  bet_id: 'V3_740407_RA_LIKE_REGISTER_OPENER_BRIDGE_20260531',
  vector: 'V3 descendant-script morphology',
  confidence_tier: 'wild shot',
  risky_bet:
    'Because the V2/V4 slot tests identify `740` and `407` as independent register openers, test a backward-Brahmi bridge bet: both openers might be a ra-like graphic/phonetic family rather than merely two unrelated administrative signs.',
  observed:
    `Ra-like pressure appears for ${signsWithRaPressure.size}/${SIGNS.size} opener signs. Best rows: ${bestBySign.map((row) => `${row.sign_id}/${row.orientation_policy}:modal=${row.modal_brahmi_label},v3=${row.v3_cisi_modal_label},shape_null=${row.original_shape_null_share},label_null=${row.original_label_null_share},impostor=${row.impostor_ge_observed_share}`).join('; ')}. Anchor-gate passes=${signsPassingAnchor.size}/${SIGNS.size}. Shared bridge verdict=${sharedBridgeKilled ? 'killed_for_phonetic_anchor' : 'not_killed'}.`,
  adversarial_test:
    'Directly tests the named 740/407 ra-like bet against source-token shape null, label null, v3 independence preflight, and real-token impostor forger v3. This does not use the contaminated v3b low-null autopsy as settled evidence.',
  false_positive_rate:
    sharedBridgeKilled
      ? 'not accepted: 407 fails real-token impostor badly and both signs fail source-token/preflight gates'
      : 'unexpected: at least one strict anchor gate passed',
  falsifier:
    'The bridge is dead as a phonetic anchor unless independent, source-checked 740 and 407 token families both return stable ra-like labels with shape-null, label-null, and impostor rates at or below 0.01 and pass independence preflight.',
  next_prediction:
    'Treat current ra-like pressure only as a search prior for future source-token crops. Do not assign 740=ra or 407=ra. The slot-grammar result remains usable without this phonetic bridge.',
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
  'orientation_policy',
  'sample_count',
  'modal_brahmi_label',
  'v3_raw_modal_label',
  'v3_sha_modal_label',
  'v3_cisi_modal_label',
  'v3_cisi_modal_share',
  'ra_like',
  'source_token_modal_share',
  'original_shape_null_share',
  'original_label_null_share',
  'impostor_ge_observed_share',
  'v3_preflight_decision',
  'gate_decision',
  'accepted_phonetic_anchor',
  'blocked_reason',
  'passes_anchor_gate',
]);

console.log(JSON.stringify(summary, null, 2));
