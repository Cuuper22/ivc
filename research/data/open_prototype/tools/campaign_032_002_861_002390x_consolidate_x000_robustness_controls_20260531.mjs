import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const parseRowsPath = path.join(
  reportsDir,
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const prefix = 'campaign_032_002_861_002390x_consolidate_x000_robustness_controls_20260531';
const checkedDate = '2026-05-31';

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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
}

function rate(numerator, denominator) {
  return denominator ? numerator / denominator : 0;
}

function countMap(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return counts;
}

function countBy(items, keyFn) {
  return [...countMap(items, keyFn).entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function terminal(row) {
  return row.tail_after_x === '<END>';
}

function compare(rows, label, controlType) {
  const x000 = rows.filter((row) => row.x === '000');
  const non000 = rows.filter((row) => row.x !== '000');
  const xTerm = x000.filter(terminal);
  const nonTerm = non000.filter(terminal);
  const xRate = rate(xTerm.length, x000.length);
  const nonRate = rate(nonTerm.length, non000.length);
  return {
    checked_date: checkedDate,
    control_type: controlType,
    label,
    x000_rows: String(x000.length),
    x000_terminal: ratio(xTerm.length, x000.length),
    x000_rate: xRate.toFixed(3),
    non000_rows: String(non000.length),
    non000_terminal: ratio(nonTerm.length, non000.length),
    non000_rate: nonRate.toFixed(3),
    gap: (xRate - nonRate).toFixed(3),
    verdict:
      x000.length < 5
        ? 'too_few_x000_rows'
        : xRate >= 0.8 && xRate - nonRate >= 0.2
          ? 'survives'
          : 'damages_x000_rule',
    x000_sites: countBy(x000, (row) => row.site),
    x000_heads: countBy(x000, (row) => row.head),
    examples: x000.slice(0, 8).map((row) => `${row.object}:${row.head}-000-${row.tail_after_x}`).join(' | '),
  };
}

function groupCollapse(rows, keyFn, label) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  const collapsed = [...groups.entries()].map(([key, group]) => ({
    key,
    x: group[0].x,
    site: countBy(group, (row) => row.site),
    type: countBy(group, (row) => row.type),
    head: group[0].head,
    tail_after_x: group.some(terminal) ? '<END>' : group[0].tail_after_x,
    all_terminal: String(group.every(terminal)),
    any_terminal: String(group.some(terminal)),
    rows: String(group.length),
    examples: group.map((row) => row.object).join(';'),
  }));
  const x000 = collapsed.filter((row) => row.x === '000');
  const non000 = collapsed.filter((row) => row.x !== '000');
  const xAllTerminal = x000.filter((row) => row.all_terminal === 'true');
  const nonAllTerminal = non000.filter((row) => row.all_terminal === 'true');
  const xRate = rate(xAllTerminal.length, x000.length);
  const nonRate = rate(nonAllTerminal.length, non000.length);
  return {
    rows: collapsed,
    summary: {
      checked_date: checkedDate,
      control_type: 'collapse',
      label,
      x000_rows: String(x000.length),
      x000_terminal: ratio(xAllTerminal.length, x000.length),
      x000_rate: xRate.toFixed(3),
      non000_rows: String(non000.length),
      non000_terminal: ratio(nonAllTerminal.length, non000.length),
      non000_rate: nonRate.toFixed(3),
      gap: (xRate - nonRate).toFixed(3),
      verdict:
        x000.length < 5
          ? 'too_few_x000_rows'
          : xRate >= 0.75 && xRate - nonRate >= 0.15
            ? 'survives'
            : 'damages_x000_rule',
      x000_sites: countBy(x000, (row) => row.site),
      x000_heads: countBy(x000, (row) => row.head),
      examples: x000.slice(0, 8).map((row) => `${row.key}:${row.examples}`).join(' | '),
    },
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(parseRowsPath, 'utf8'));
const xslot = parseRows.filter((row) => row.x);
const sitesWithX000 = [...new Set(xslot.filter((row) => row.x === '000').map((row) => row.site))];
const typesWithX000 = [...new Set(xslot.filter((row) => row.x === '000').map((row) => row.type))];

const controls = [
  compare(xslot, 'all_xslot_rows', 'baseline'),
  compare(xslot.filter((row) => row.type.startsWith('SEAL')), 'seal_only', 'domain'),
  compare(xslot.filter((row) => !row.type.startsWith('SEAL')), 'non_seal_only', 'domain'),
  ...sitesWithX000.map((site) => compare(xslot.filter((row) => row.site !== site), `leave_out_site:${site}`, 'leave_one_site')),
  ...typesWithX000.map((type) => compare(xslot.filter((row) => row.type !== type), `leave_out_type:${type}`, 'leave_one_type')),
];

const byHead = groupCollapse(xslot, (row) => `${row.x}|${row.head}`, 'collapse_by_x_and_head_all_terminal');
const bySite = groupCollapse(xslot, (row) => `${row.x}|${row.site}`, 'collapse_by_x_and_site_all_terminal');
controls.push(byHead.summary, bySite.summary);

const damagingControls = controls.filter((row) => row.verdict === 'damages_x000_rule');
const seriousControls = controls.filter((row) => row.verdict !== 'too_few_x000_rows');
const survivesSerious = seriousControls.filter((row) => row.verdict === 'survives');

const decisions = [
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_X000_SURVIVES_ROBUSTNESS_CONTROLS',
    action: damagingControls.length ? 'keep_with_warning' : 'rank_up_within_candidate',
    target: 'X=000 zero-complement',
    reason: `serious_controls=${seriousControls.length}; survives=${survivesSerious.length}; damaging=${damagingControls.length}.`,
    model_effect: damagingControls.length
      ? 'Keep X=000 but downgrade robustness until damaging controls are explained.'
      : 'Keep X=000 as the strongest core subrule below acceptance.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_X000_SEAL_CONTROL',
    action: controls.find((row) => row.label === 'seal_only')?.verdict === 'survives' ? 'keep' : 'warn',
    target: 'seal-domain X=000',
    reason: `seal_only=${controls.find((row) => row.label === 'seal_only')?.x000_terminal ?? '0/0'} vs non000 ${controls.find((row) => row.label === 'seal_only')?.non000_terminal ?? '0/0'}.`,
    model_effect: 'Separates seal/formula explanation from cross-domain zero-complement behavior.',
  },
  {
    checked_date: checkedDate,
    decision_id: 'CONSOLIDATE_X000_NON_SEAL_CONTROL',
    action: controls.find((row) => row.label === 'non_seal_only')?.verdict === 'survives' ? 'keep' : 'warn',
    target: 'non-seal X=000',
    reason: `non_seal_only=${controls.find((row) => row.label === 'non_seal_only')?.x000_terminal ?? '0/0'} vs non000 ${controls.find((row) => row.label === 'non_seal_only')?.non000_terminal ?? '0/0'}.`,
    model_effect: 'If non-seal fails, X=000 becomes seal/register-biased; if it survives, grammar reading strengthens.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'x000_robustness_controls',
  controls: controls.length,
  serious_controls: seriousControls.length,
  survives: survivesSerious.length,
  damaging: damagingControls.map((row) => row.label),
  baseline: controls.find((row) => row.label === 'all_xslot_rows'),
  seal: controls.find((row) => row.label === 'seal_only'),
  non_seal: controls.find((row) => row.label === 'non_seal_only'),
  conclusion: damagingControls.length
    ? 'X=000 remains candidate but takes robustness damage.'
    : 'X=000 survives site/type/domain/head-collapse controls and remains strongest core parser subrule below acceptance.',
};

writeCsv(path.join(reportsDir, `${prefix}_controls.csv`), controls, [
  'checked_date',
  'control_type',
  'label',
  'x000_rows',
  'x000_terminal',
  'x000_rate',
  'non000_rows',
  'non000_terminal',
  'non000_rate',
  'gap',
  'verdict',
  'x000_sites',
  'x000_heads',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_collapsed_by_head.csv`), byHead.rows, [
  'key',
  'x',
  'site',
  'type',
  'head',
  'tail_after_x',
  'all_terminal',
  'any_terminal',
  'rows',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_collapsed_by_site.csv`), bySite.rows, [
  'key',
  'x',
  'site',
  'type',
  'head',
  'tail_after_x',
  'all_terminal',
  'any_terminal',
  'rows',
  'examples',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'decision_id',
  'action',
  'target',
  'reason',
  'model_effect',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
