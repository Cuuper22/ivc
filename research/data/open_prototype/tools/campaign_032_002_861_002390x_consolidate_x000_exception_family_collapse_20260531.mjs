import fs from 'node:fs';
import path from 'node:path';

// Three inscriptions break the rule that X=000 ends a text: 4148.1 (tail
// 267-000-033), M-451 (a 000-000-000 zero chain before 906-388), and Ns-66
// (000 followed by a final 002). This script asks whether each exception is a
// one-off or a member of a family that would explain it away. For each target
// it defines a handful of probe sequences — the exact tail plus looser
// sub-patterns like "000-033 anywhere" or "any 267-000" — then scans every
// text in lipi/metadata_filtered.csv for those n-grams and records the
// surrounding two signs on each side and whether the match sits at the end of
// its text. A probe with exactly one occurrence stays a singleton the corpus
// cannot adjudicate; repeats soften the exception into a family pattern. The
// verdict encoded in the decisions: none of the three collapse locally, and
// 4148.1 remains the cleanest kill switch against new null rules. Writes
// target, sequence-summary, context, and decision CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_consolidate_x000_exception_family_collapse_20260531';
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

function signs(text) {
  return [...String(text || '').matchAll(/\d{3}/g)].map((match) => match[0]);
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, keyFn) {
  const counts = new Map();
  for (const item of items) {
    const key = keyFn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function containsSeq(tokens, seq) {
  for (let i = 0; i <= tokens.length - seq.length; i += 1) {
    if (seq.every((token, offset) => tokens[i + offset] === token)) return true;
  }
  return false;
}

function seqContexts(rows, seq, label, target = '') {
  const out = [];
  for (const row of rows) {
    const tokens = row.tokens;
    for (let i = 0; i <= tokens.length - seq.length; i += 1) {
      if (!seq.every((token, offset) => tokens[i + offset] === token)) continue;
      out.push({
        checked_date: checkedDate,
        target,
        label,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        text: row.text,
        prev2: tokens[i - 2] ?? '<START>',
        prev1: tokens[i - 1] ?? '<START>',
        sequence: seq.join(' '),
        next1: tokens[i + seq.length] ?? '<END>',
        next2: tokens[i + seq.length + 1] ?? '<END>',
        at_end: String(i + seq.length === tokens.length),
      });
    }
  }
  return out;
}

function summarizeContexts(contexts, target, label, adjudication) {
  return {
    checked_date: checkedDate,
    target,
    label,
    occurrences: String(contexts.length),
    objects: contexts.map((row) => row.object).join(';') || '-',
    sites: countBy(contexts, (row) => row.site),
    types: countBy(contexts, (row) => row.type),
    prev1: countBy(contexts, (row) => row.prev1),
    next1: countBy(contexts, (row) => row.next1),
    at_end: countBy(contexts, (row) => row.at_end),
    adjudication,
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));

const targets = [
  {
    target: '4148.1',
    object: '-:4148.1',
    row_id: '4148.1',
    sequences: [
      { label: 'exact_tail_267_000_033', seq: ['267', '000', '033'] },
      { label: 'payload_candidate_000_033', seq: ['000', '033'] },
      { label: 'head267_x000', seq: ['002', '267', '000'] },
      { label: 'same_tail_267_000_any', seq: ['267', '000'] },
    ],
  },
  {
    target: 'M-451',
    object: 'M-451',
    row_id: '2936.1',
    sequences: [
      { label: 'exact_tail_520_000_000_000_906_388', seq: ['520', '000', '000', '000', '906', '388'] },
      { label: 'zero_chain_000_000_000_906_388', seq: ['000', '000', '000', '906', '388'] },
      { label: 'payload_candidate_906_388', seq: ['906', '388'] },
      { label: 'same_head_520_000', seq: ['002', '520', '000'] },
    ],
  },
  {
    target: 'Ns-66',
    object: 'Ns-66',
    row_id: '5367.1',
    sequences: [
      { label: 'exact_tail_892_000_002', seq: ['892', '000', '002'] },
      { label: 'reset_candidate_000_002', seq: ['000', '002'] },
      { label: 'frame_002_892_000', seq: ['002', '892', '000'] },
      { label: 'terminal_002_context', seq: ['002'] },
    ],
  },
];

const contextRows = [];
const summaryRows = [];
for (const target of targets) {
  for (const item of target.sequences) {
    const contexts = seqContexts(rows, item.seq, item.label, target.target);
    contextRows.push(...contexts);
    const adjudication =
      contexts.length === 1
        ? 'singleton_local_context; source binding decides'
        : contexts.length > 1 && contexts.every((row) => row.at_end === 'true')
          ? 'repeated_terminal_boundary_pressure'
          : contexts.length > 1
            ? 'family_context_available_but_not_decisive'
            : 'no_local_family_support';
    summaryRows.push(summarizeContexts(contexts, target.target, item.label, adjudication));
  }
}

const targetRows = targets.map((target) => {
  const targetRow = rows.find((row) => row.object === target.object || row.id === target.row_id);
  const exactTextMatches = rows.filter((row) => row.tokens.join(' ') === targetRow.tokens.join(' '));
  return {
    checked_date: checkedDate,
    target: target.target,
    object: targetRow.object,
    row_id: targetRow.id,
    site: targetRow.site,
    type: targetRow.type,
    material: targetRow.material,
    shape: targetRow.shape,
    text: targetRow.text,
    tokens: targetRow.tokens.join(' '),
    exact_text_matches: exactTextMatches.map((row) => row.object).join(';'),
    exact_text_match_count: String(exactTextMatches.length),
  };
});

function targetSummary(target) {
  const rowsForTarget = summaryRows.filter((row) => row.target === target);
  const singletonCritical = rowsForTarget.filter((row) =>
    ['exact_tail_267_000_033', 'zero_chain_000_000_000_906_388', 'exact_tail_892_000_002'].includes(row.label),
  );
  return singletonCritical.every((row) => row.occurrences === '1');
}

const decisions = [
  {
    checked_date: checkedDate,
    target: '4148.1',
    decision: targetSummary('4148.1') ? 'unresolved_kill_switch' : 'family_softened',
    consequence:
      '4148.1 remains the cleanest X=000 killer unless 000-033 is shown to be boundary/segmentation rather than payload.',
    next_action:
      'In next EXPAND, source-bind 4148.1 or search exact Rakhigarhi/267-000-033 controls before adding new null rules.',
  },
  {
    checked_date: checkedDate,
    target: 'M-451',
    decision: targetSummary('M-451') ? 'zero_chain_singleton_pressure' : 'family_softened',
    consequence:
      'M-451 cannot be waved away as common formula; decide whether 906-388 is governed payload or separate zero-chain tail.',
    next_action:
      'Compare 906-388 contexts and source layout before using M-451 as either support or damage.',
  },
  {
    checked_date: checkedDate,
    target: 'Ns-66',
    decision: targetSummary('Ns-66') ? 'reset_singleton_pressure' : 'family_softened',
    consequence:
      'Ns-66 is less dangerous than 4148.1 but still tests whether final 002 can be frame reset after X=000.',
    next_action:
      'Check terminal 002 and 000-002 contexts for reset behavior before promotion.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'CONSOLIDATE',
  status: 'x000_exception_family_collapse',
  target_count: targets.length,
  sequence_tests: summaryRows.length,
  singleton_sequences: summaryRows.filter((row) => row.occurrences === '1').map((row) => `${row.target}:${row.label}`),
  local_family_softeners: summaryRows
    .filter((row) => row.adjudication !== 'singleton_local_context; source binding decides')
    .map((row) => `${row.target}:${row.label}:${row.adjudication}`),
  conclusion:
    'The three X=000 exceptions do not collapse away locally; 4148.1 remains the cleanest kill switch, M-451 and Ns-66 remain singleton pressure rather than solved exceptions.',
};

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), targetRows, [
  'checked_date',
  'target',
  'object',
  'row_id',
  'site',
  'type',
  'material',
  'shape',
  'text',
  'tokens',
  'exact_text_matches',
  'exact_text_match_count',
]);
writeCsv(path.join(reportsDir, `${prefix}_sequence_summary.csv`), summaryRows, [
  'checked_date',
  'target',
  'label',
  'occurrences',
  'objects',
  'sites',
  'types',
  'prev1',
  'next1',
  'at_end',
  'adjudication',
]);
writeCsv(path.join(reportsDir, `${prefix}_sequence_contexts.csv`), contextRows, [
  'checked_date',
  'target',
  'label',
  'object',
  'row_id',
  'site',
  'type',
  'text',
  'prev2',
  'prev1',
  'sequence',
  'next1',
  'next2',
  'at_end',
]);
writeCsv(path.join(reportsDir, `${prefix}_decisions.csv`), decisions, [
  'checked_date',
  'target',
  'decision',
  'consequence',
  'next_action',
]);
fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
