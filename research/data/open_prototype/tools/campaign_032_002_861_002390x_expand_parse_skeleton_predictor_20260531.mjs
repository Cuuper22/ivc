import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_parse_skeleton_predictor_20260531';
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

function ratio(numerator, denominator) {
  return denominator ? `${numerator}/${denominator}` : '0/0';
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

function uniqueRowsByText(rows) {
  return [...new Map(rows.map((row) => [row.tokens.join(' '), row])).values()];
}

function predictedClass(head, x, tail) {
  if (x === '095') return 'terminal_identity_or_class_label';
  if (x === '530') return 'one_complement_associative_linker';
  if (x === '125') {
    if (head === '610') return 'head610_032_tail_router';
    if (head === '390') return 'head390_tail_menu_operator';
    return 'dependent_title_chain_operator';
  }
  if (x === '705') {
    if (head === '320' && tail[0] === '125') return 'head320_705_125_cap_exception';
    return 'terminal_default_group_or_class_label';
  }
  if (x === '590') return 'head_routed_extender_bait';
  if (x === '692') return 'terminal_default_exception_bait';
  if (x === '707') return 'terminal_class_bait';
  if (['072', '140', '346'].includes(x)) return 'terminal_bait';
  return 'unclassified_x_slot';
}

function expectedContinuation(head, x) {
  if (x === '095') return 'closed';
  if (x === '530') return 'one_complement_then_closed';
  if (x === '125') {
    if (head === '610') return 'open_to_032';
    if (head === '390') return 'open_to_tail_menu';
    return 'open_or_closed_dependent_chain';
  }
  if (x === '705') {
    if (head === '320') return 'open_to_125_cap';
    return 'closed';
  }
  if (x === '590') {
    if (head === '390' || head === '798') return 'open_to_032';
    return 'head_routed_unknown';
  }
  if (x === '692') {
    if (head === '455') return 'open_to_416';
    return 'closed';
  }
  if (x === '707') return 'closed';
  if (['072', '140', '346'].includes(x)) return 'closed';
  return 'unknown';
}

function observedContinuation(tail) {
  if (!tail.length) return 'closed';
  if (tail.length === 1) return `one:${tail[0]}`;
  return `multi:${tail.join('-')}`;
}

function predictionPass(head, x, tail) {
  const expected = expectedContinuation(head, x);
  if (expected === 'closed') return tail.length === 0;
  if (expected === 'one_complement_then_closed') return tail.length === 1;
  if (expected === 'open_to_032') return tail[0] === '032';
  if (expected === 'open_to_125_cap') return tail[0] === '125';
  if (expected === 'open_to_416') return tail[0] === '416';
  if (expected === 'open_to_tail_menu') return tail.length > 0;
  if (expected === 'open_or_closed_dependent_chain') return true;
  return null;
}

function glossSkeleton(head, x, tail) {
  const cls = predictedClass(head, x, tail);
  if (cls === 'terminal_identity_or_class_label') return `FRAME(002) HEAD(${head}) IDENTITY_CLASS(${x})`;
  if (cls === 'one_complement_associative_linker') return `FRAME(002) HEAD(${head}) LINKER(${x}) COMPLEMENT(${tail[0] ?? '?'})`;
  if (cls === 'head610_032_tail_router') return `FRAME(002) HEAD(610) TITLE_CHAIN(${x}) ROUTE(032)`;
  if (cls === 'head390_tail_menu_operator') return `FRAME(002) HEAD(390) TITLE_CHAIN(${x}) TAIL(${tail.join(' ') || '?'})`;
  if (cls === 'dependent_title_chain_operator') return `FRAME(002) HEAD(${head}) DEPENDENT_CHAIN(${x}) TAIL(${tail.join(' ') || '<END>'})`;
  if (cls === 'head320_705_125_cap_exception') return `FRAME(002) HEAD(320) DEFAULT_CLASS(${x}) CAP(125)`;
  if (cls === 'terminal_default_group_or_class_label') return `FRAME(002) HEAD(${head}) DEFAULT_CLASS(${x})`;
  if (cls === 'head_routed_extender_bait') return `FRAME(002) HEAD(${head}) EXTENDER(${x}) ROUTE(${tail[0] ?? '<END>'})`;
  if (cls === 'terminal_default_exception_bait') return `FRAME(002) HEAD(${head}) BOUNDARY_BAIT(${x})`;
  if (cls === 'terminal_class_bait') return `FRAME(002) HEAD(${head}) TERMINAL_BAIT(${x})`;
  return `FRAME(002) HEAD(${head}) X(${x}) TAIL(${tail.join(' ') || '<END>'})`;
}

function failureHook(head, x) {
  if (x === '095') return 'any real continuation after 095';
  if (x === '530') return 'zero or multiple complements after 530';
  if (x === '125' && head === '610') return 'tail other than 032 after 610-125';
  if (x === '125') return 'same head repeatedly chooses incompatible tail families';
  if (x === '705' && head === '390') return 'any continuation after 390-705';
  if (x === '705' && head === '320') return '320-705 without 125';
  if (x === '590' && head === '390') return '390-590 not followed by 032';
  if (x === '692' && head === '390') return '390-692 continuation';
  if (x === '707') return '707 continuation';
  return 'unclassified row needs source/context before interpretation';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const parseRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002') continue;
    const head = row.tokens[i + 1];
    const x = row.tokens[i + 2];
    const tail = row.tokens.slice(i + 3);
    const pass = predictionPass(head, x, tail);
    parseRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      material: row.material,
      head,
      x,
      tail_after_x: tail.join(' ') || '<END>',
      observed_continuation: observedContinuation(tail),
      predicted_class: predictedClass(head, x, tail),
      expected_continuation: expectedContinuation(head, x),
      prediction_pass: pass === null ? '' : String(pass),
      gloss_skeleton: glossSkeleton(head, x, tail),
      failure_hook: failureHook(head, x),
      text: row.text,
    });
  }
}

const classified = parseRows.filter((row) => row.prediction_pass !== '');
const passing = classified.filter((row) => row.prediction_pass === 'true');
const focus = parseRows.filter((row) => row.predicted_class !== 'unclassified_x_slot');

const ruleRows = [...new Set(parseRows.map((row) => row.predicted_class))].map((rule) => {
  const rowsForRule = parseRows.filter((row) => row.predicted_class === rule);
  const covered = rowsForRule.filter((row) => row.prediction_pass !== '');
  const pass = covered.filter((row) => row.prediction_pass === 'true');
  return {
    checked_date: checkedDate,
    predicted_class: rule,
    rows: String(rowsForRule.length),
    covered: ratio(covered.length, rowsForRule.length),
    pass: ratio(pass.length, covered.length),
    heads: countBy(rowsForRule, (row) => row.head),
    x_signs: countBy(rowsForRule, (row) => row.x),
    examples: rowsForRule
      .slice(0, 6)
      .map((row) => `${row.object}:${row.gloss_skeleton}`)
      .join(' | '),
  };
});

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PROVISIONAL_TRANSLATION_SYSTEM_SKELETON',
    tier: classified.length > 0 && passing.length / classified.length >= 0.9 ? 'candidate' : 'wild_shot',
    risky_bet:
      'A provisional non-lexical parser can assign `002-H-X` rows to slot roles and produce a gloss skeleton without accepting sign values.',
    current_test:
      `classified=${ratio(classified.length, parseRows.length)}; pass=${ratio(passing.length, classified.length)}; class_counts=${countBy(parseRows, (row) => row.predicted_class)}.`,
    destructive_prediction:
      'Held-out rows that repeatedly violate class-specific continuation predictions collapse the skeleton into a descriptive labeler.',
    promotion_prediction:
      'Source-strict held-out rows whose continuation matches predicted class promote the skeleton toward a translation-system rule layer.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_NO_LEXICAL_TRANSLATION_YET_BUT_PARSE_GLOSSES_ALLOWED',
    tier: 'candidate',
    risky_bet:
      'The system may output parse glosses like `HEAD(390) IDENTITY_CLASS(095)` before lexical values, as Egyptian-style translation analogues at the grammar layer.',
    current_test:
      focus
        .slice(0, 10)
        .map((row) => `${row.object}:${row.gloss_skeleton}`)
        .join(';'),
    destructive_prediction:
      'If parse classes fail on source-strict rows, grammar glosses are misleading and must be demoted.',
    promotion_prediction:
      'If grammar glosses predict unseen continuation and object ecology, they become the first usable translation-system layer.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'parse_skeleton_predictor',
  rows: {
    all_002_h_x_rows: parseRows.length,
    classified_rows: classified.length,
    classified_pass: passing.length,
    focus_rows: focus.length,
    class_counts: countBy(parseRows, (row) => row.predicted_class),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_parse_rows.csv`), parseRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'shape',
  'material',
  'head',
  'x',
  'tail_after_x',
  'observed_continuation',
  'predicted_class',
  'expected_continuation',
  'prediction_pass',
  'gloss_skeleton',
  'failure_hook',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_rule_rows.csv`), ruleRows, [
  'checked_date',
  'predicted_class',
  'rows',
  'covered',
  'pass',
  'heads',
  'x_signs',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_bets.csv`), bets, [
  'checked_date',
  'bet_id',
  'tier',
  'risky_bet',
  'current_test',
  'destructive_prediction',
  'promotion_prediction',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
