import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const framesPath = path.join(reportsDir, 'campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv');
const prefix = 'campaign_032_002_861_002390x_consolidate_same_register_null_20260531';
const focusSigns = ['125', '095', '692'];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        field += ch;
      }
    } else if (ch === '"') {
      quoted = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
      row = [];
      field = '';
    } else {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field.replace(/\r$/, ''));
    rows.push(row);
  }
  const header = rows.shift() ?? [];
  return rows
    .filter((r) => r.some((value) => value !== ''))
    .map((r) => Object.fromEntries(header.map((name, index) => [name, r[index] ?? ''])));
}

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function signs(text) {
  return text.match(/\d{3}/g) ?? [];
}

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function choose(n, k) {
  if (k < 0 || k > n) return 0;
  const kk = Math.min(k, n - k);
  let result = 1;
  for (let i = 1; i <= kk; i += 1) {
    result = (result * (n - kk + i)) / i;
  }
  return result;
}

function sourceClass(status) {
  if (status.includes('checkpoint_strict_source_visible')) return 'strict';
  if (status.includes('source_panel_acquired')) return 'panel_compatible_not_strict';
  if (status.includes('checkpoint_permissive_public_panel')) return 'panel_permissive_not_strict';
  if (status.includes('source_route')) return 'route_only';
  if (status.includes('metadata_only')) return 'metadata_only';
  if (status.includes('absent') || status.includes('secondary_icon')) return 'source_dark';
  if (status.includes('unbound')) return 'unbound';
  return 'other';
}

function decisionForSign(sign, target, outside, strictTarget) {
  const targetOpen = target.filter((row) => row.terminal_after_sign === 'False').length;
  const targetTerminal = target.filter((row) => row.terminal_after_sign === 'True').length;
  const outsideOpen = outside.filter((row) => row.terminal_after_sign === 'False').length;
  const outsideTerminal = outside.filter((row) => row.terminal_after_sign === 'True').length;
  const strictOpen = strictTarget.filter((row) => row.terminal_after_sign === 'False').length;
  const strictTerminal = strictTarget.filter((row) => row.terminal_after_sign === 'True').length;

  if (sign === '125' && target.length > 0 && targetTerminal === 0 && outsideTerminal > 0) {
    return 'keep_125_frame_open_residual; kill_intrinsic_open_value';
  }
  if (sign === '095' && outside.length === 0 && strictTerminal === 1) {
    return 'keep_m71_terminal_only; no_same_register_background_test';
  }
  if (sign === '692' && targetTerminal === target.length && outsideOpen > 0 && outsideTerminal > outsideOpen) {
    return 'keep_weak_terminal_branch; demote_as_background_terminal_biased';
  }
  if (strictOpen > 0 || strictTerminal > 0) return 'strict_target_observed_but_background_mixed';
  return 'no_load_bearing_result';
}

fs.mkdirSync(reportsDir, { recursive: true });

const metadataRows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));
const frames = parseCsv(fs.readFileSync(framesPath, 'utf8'));
const frameStatusByIdX = new Map(
  frames.map((row) => [`${row.id}|${row.branch_after_390}`, { status: row.source_status, class: sourceClass(row.source_status) }]),
);
const sameRegisterFrames = frames.filter(
  (row) =>
    row.site === 'Mohenjo-daro' &&
    row.type === 'SEAL:S' &&
    row.shape === 'square' &&
    row.material === 'Steatite',
);

const sameRegisterRows = metadataRows.filter(
  (row) =>
    row.site === 'Mohenjo-daro' &&
    row.type === 'SEAL:S' &&
    row.shape === 'square' &&
    row.material === 'Steatite',
);

const occurrences = [];
for (const row of sameRegisterRows) {
  const rowSigns = signs(row.text);
  for (let index = 0; index < rowSigns.length; index += 1) {
    const sign = rowSigns[index];
    if (!focusSigns.includes(sign)) continue;
    const targetFrame = index >= 2 && rowSigns[index - 2] === '002' && rowSigns[index - 1] === '390';
    const frameStatus = targetFrame ? frameStatusByIdX.get(`${row.id}|${sign}`) : null;
    occurrences.push({
      checked_date: '2026-05-31',
      object: row.cisi,
      id: row.id,
      sign,
      target_frame: targetFrame ? 'True' : 'False',
      source_class: frameStatus?.class ?? (targetFrame ? 'target_frame_not_in_branch_report' : 'metadata_same_register_background'),
      source_status: frameStatus?.status ?? '',
      position_1based: String(index + 1),
      text_length: String(rowSigns.length),
      prev2: rowSigns[index - 2] ?? '',
      prev: rowSigns[index - 1] ?? '',
      next: rowSigns[index + 1] ?? '',
      terminal_after_sign: index === rowSigns.length - 1 ? 'True' : 'False',
      symbol: row.symbol,
      cult: row.cult,
      complete: row.complete,
      condition: row.condition,
      text: row.text,
    });
  }
}

const signSummary = focusSigns.map((sign) => {
  const all = occurrences.filter((row) => row.sign === sign);
  const target = all.filter((row) => row.target_frame === 'True');
  const outside = all.filter((row) => row.target_frame === 'False');
  const strictTarget = target.filter((row) => row.source_class === 'strict');
  const targetTerminal = target.filter((row) => row.terminal_after_sign === 'True').length;
  const outsideTerminal = outside.filter((row) => row.terminal_after_sign === 'True').length;
  const strictTerminal = strictTarget.filter((row) => row.terminal_after_sign === 'True').length;
  return {
    checked_date: '2026-05-31',
    sign,
    same_register_total_occurrences: String(all.length),
    target_frame_occurrences: String(target.length),
    target_frame_terminal: String(targetTerminal),
    target_frame_open: String(target.length - targetTerminal),
    target_frame_terminal_rate: ratio(targetTerminal, target.length),
    strict_target_occurrences: String(strictTarget.length),
    strict_target_terminal: String(strictTerminal),
    strict_target_open: String(strictTarget.length - strictTerminal),
    strict_target_terminal_rate: ratio(strictTerminal, strictTarget.length),
    outside_frame_occurrences: String(outside.length),
    outside_terminal: String(outsideTerminal),
    outside_open: String(outside.length - outsideTerminal),
    outside_terminal_rate: ratio(outsideTerminal, outside.length),
    decision: decisionForSign(sign, target, outside, strictTarget),
  };
});

const targetRows = occurrences.filter((row) => row.target_frame === 'True');
const outsideExamples = occurrences
  .filter((row) => row.target_frame === 'False')
  .sort((a, b) => a.sign.localeCompare(b.sign, undefined, { numeric: true }) || a.object.localeCompare(b.object, undefined, { numeric: true }));
const branchShellRows = sameRegisterFrames.map((row) => ({
  checked_date: '2026-05-31',
  object: row.object,
  id: row.id,
  left_final: row.prev_before_002,
  x: row.branch_after_390,
  x_class: row.branch_after_390 === '125' ? '125' : 'non125',
  tail_after_x: row.tail_after_branch,
  terminal_after_x: row.terminal_after_branch,
  source_class: sourceClass(row.source_status),
  source_status: row.source_status,
  symbol: row.symbol,
  cult: row.cult,
  text: row.text,
}));
const shell125 = branchShellRows.filter((row) => row.x_class === '125');
const shellNon125 = branchShellRows.filter((row) => row.x_class === 'non125');
const shell125Strict = shell125.filter((row) => row.source_class === 'strict');
const shellNon125Strict = shellNon125.filter((row) => row.source_class === 'strict');
const shell125Terminal = shell125.filter((row) => row.terminal_after_x === 'True').length;
const shellNon125Terminal = shellNon125.filter((row) => row.terminal_after_x === 'True').length;
const shell125StrictTerminal = shell125Strict.filter((row) => row.terminal_after_x === 'True').length;
const shellNon125StrictTerminal = shellNon125Strict.filter((row) => row.terminal_after_x === 'True').length;
const branchShellSummary = {
  frames: sameRegisterFrames.length,
  x125_terminal_rate: ratio(shell125Terminal, shell125.length),
  non125_terminal_rate: ratio(shellNon125Terminal, shellNon125.length),
  strict_x125_terminal_rate: ratio(shell125StrictTerminal, shell125Strict.length),
  strict_non125_terminal_rate: ratio(shellNon125StrictTerminal, shellNon125Strict.length),
  open_rows: shell125.length - shell125Terminal + shellNon125.length - shellNon125Terminal,
  exact_partition_probability_if_open_rows_random:
    shell125.length === shell125.length - shell125Terminal + shellNon125.length - shellNon125Terminal
      ? `1/${choose(sameRegisterFrames.length, shell125.length)}`
      : 'not_exact_125_partition',
  compact_rule: 'local 002-390-125 continues; local 002-390-non125 terminates',
  tier: '125 half promoted local candidate; non125 half candidate due metadata-only singleton extension',
};

const signSummaryBySign = Object.fromEntries(signSummary.map((row) => [row.sign, row]));
const contradictionChecks = [
  {
    checked_date: '2026-05-31',
    check_id: 'SAME_REGISTER_LAYOUT_NULL_EXPLAINS_ALL',
    result: 'partial_fail_keep_local_frame_residual',
    evidence:
      'same register target frames split: 125 is open in 3/3 metadata rows and 2/2 strict rows; 095 and 692 are terminal in their strict rows',
    consequence:
      'Do not collapse the entire parser into register layout; keep local frame-conditioned syntax, not script-wide grammar.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'X_INTRINSIC_POLARITY',
    result: 'pass_kill_intrinsic_values',
    evidence: `125 outside terminal=${signSummaryBySign['125'].outside_terminal_rate}; 692 outside terminal=${signSummaryBySign['692'].outside_terminal_rate}; 095 outside=${signSummaryBySign['095'].outside_frame_occurrences}`,
    consequence:
      'A sign-level reading like 125=open or 692=closed is killed; behavior is frame/context conditioned.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'FRAME_EFFECT_RESIDUAL',
    result: 'partial_candidate_125_only',
    evidence: `125 target terminal=${signSummaryBySign['125'].target_frame_terminal_rate} versus outside terminal=${signSummaryBySign['125'].outside_terminal_rate}; 692 target terminal=${signSummaryBySign['692'].target_frame_terminal_rate} versus outside terminal=${signSummaryBySign['692'].outside_terminal_rate}`,
    consequence:
      'The strongest surviving frame effect is 002-390-125 as open/continuing; 692 terminality is partly background behavior.',
  },
  {
    checked_date: '2026-05-31',
    check_id: 'SEMANTIC_READING_PRESSURE',
    result: 'pass_demote_semantics',
    evidence: 'same-register background is mixed and source status is metadata-level for most outside rows',
    consequence:
      'No rank/title/status/result/closure translation can be promoted from this test.',
  },
];

const summary = {
  checked_date: '2026-05-31',
  phase: 'CONSOLIDATE',
  status: 'same_register_null_against_local_parser',
  same_register_scope: 'Mohenjo-daro|SEAL:S|square|Steatite',
  same_register_rows: sameRegisterRows.length,
  local_branch_shell: branchShellSummary,
  signs: Object.fromEntries(
    signSummary.map((row) => [
      row.sign,
      {
        target_frame_terminal_rate: row.target_frame_terminal_rate,
        strict_target_terminal_rate: row.strict_target_terminal_rate,
        outside_terminal_rate: row.outside_terminal_rate,
        decision: row.decision,
      },
    ]),
  ),
  decisions: [
    'Keep the local Mohenjo-daro square steatite 002-390-X parser as syntax, not script grammar.',
    'Promote no semantics: same-register outside behavior is mixed and source-mixed.',
    'Make 125 the only strong residual: 002-390-125 is open/continuing inside the target frame while outside 125 can be terminal.',
    'Demote 692 closure from frame-specific to background-biased terminal sign behavior until stricter outside controls are source-checked.',
    'Leave 095 as M-71-only terminal syntax because there is no same-register outside 095 comparator.',
  ],
  contradiction_results: Object.fromEntries(contradictionChecks.map((row) => [row.check_id, row.result])),
};

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), targetRows, [
  'checked_date',
  'object',
  'id',
  'sign',
  'target_frame',
  'source_class',
  'source_status',
  'position_1based',
  'text_length',
  'prev2',
  'prev',
  'next',
  'terminal_after_sign',
  'symbol',
  'cult',
  'complete',
  'condition',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_outside_examples.csv`), outsideExamples, [
  'checked_date',
  'object',
  'id',
  'sign',
  'target_frame',
  'source_class',
  'position_1based',
  'text_length',
  'prev2',
  'prev',
  'next',
  'terminal_after_sign',
  'symbol',
  'cult',
  'complete',
  'condition',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_sign_summary.csv`), signSummary, [
  'checked_date',
  'sign',
  'same_register_total_occurrences',
  'target_frame_occurrences',
  'target_frame_terminal',
  'target_frame_open',
  'target_frame_terminal_rate',
  'strict_target_occurrences',
  'strict_target_terminal',
  'strict_target_open',
  'strict_target_terminal_rate',
  'outside_frame_occurrences',
  'outside_terminal',
  'outside_open',
  'outside_terminal_rate',
  'decision',
]);

writeCsv(path.join(reportsDir, `${prefix}_branch_shell.csv`), branchShellRows, [
  'checked_date',
  'object',
  'id',
  'left_final',
  'x',
  'x_class',
  'tail_after_x',
  'terminal_after_x',
  'source_class',
  'source_status',
  'symbol',
  'cult',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_contradiction_checks.csv`), contradictionChecks, [
  'checked_date',
  'check_id',
  'result',
  'evidence',
  'consequence',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
