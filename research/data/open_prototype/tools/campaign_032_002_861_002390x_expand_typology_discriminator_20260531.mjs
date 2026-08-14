import fs from 'node:fs';
import path from 'node:path';

// This script steps back and asks: what KIND of writing system does our parser imply?
// Unlike its siblings it does not reread the raw corpus. It consumes two earlier report CSVs
// from reports/ — the classified 002-H-X parse rows (including the 000 null-complement class)
// and the per-domain role-switch control rows — and distills them into four typology signals:
// slot role changes sign behavior, a post-head operator inventory exists, classified rows sit
// on formal seals/tablets rather than accounting objects, and an explicit zero-complement
// class is available. Each signal records its support, what it implies, and the observation
// that would kill it. From these it stakes three bets: the parser looks like a head-plus-
// post-head-operator grammar, its core is identity/linkage rather than commodity accounting,
// and any language-family comparison must wait until the grammar survives source controls.
// Writes a signals CSV, a bets CSV, and a summary JSON to reports/.

const root = process.cwd();
const plus000Path = path.join(
  root,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_002390x_expand_x000_null_class_20260531_parse_rows_plus_000.csv',
);
const domainPath = path.join(
  root,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_002390x_expand_role_switch_domain_control_20260531_domain_rows.csv',
);
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_typology_discriminator_20260531';
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

function domain(row) {
  if (String(row.type).startsWith('SEAL')) return 'seal';
  if (String(row.type).startsWith('TAB')) return 'tablet';
  if (String(row.type).startsWith('POT')) return 'pot';
  if (String(row.type).startsWith('TAG')) return 'tag';
  return row.type || '-';
}

fs.mkdirSync(reportsDir, { recursive: true });

const parseRows = parseCsv(fs.readFileSync(plus000Path, 'utf8'));
const domainRows = parseCsv(fs.readFileSync(domainPath, 'utf8'));
const classified = parseRows.filter((row) => row.prediction_pass !== '');
const classifiedPass = classified.filter((row) => row.prediction_pass === 'true');

const typologySignals = [
  {
    checked_date: checkedDate,
    signal: 'slot_role_changes_sign_behavior',
    support:
      domainRows
        .filter((row) => row.same_domain_asymmetry === 'asymmetry_present')
        .map((row) => `${row.sign}:${row.domain}:head_open=${row.head_open}:x_open=${row.x_open}`)
        .join(';') || 'none',
    implication:
      'supports compositional slot grammar over isolated sign-value reading',
    null_attack:
      'same-domain role asymmetries disappear after more rows or source/register controls',
  },
  {
    checked_date: checkedDate,
    signal: 'post_head_operator_inventory',
    support: countBy(
      classified.filter((row) =>
        [
          'terminal_identity_or_class_label',
          'one_complement_associative_linker',
          'dependent_title_chain_operator',
          'head390_tail_menu_operator',
          'zero_complement_class',
          'zero_complement_exception',
        ].includes(row.predicted_class),
      ),
      (row) => row.predicted_class,
    ),
    implication:
      'supports a head-plus-post-head-operator grammar layer',
    null_attack:
      'operator classes collapse into object/formula families rather than head-conditioned slots',
  },
  {
    checked_date: checkedDate,
    signal: 'formal_object_bias_not_accounting_bias',
    support: countBy(classified, domain),
    implication:
      'current grammar layer is more seal/tablet identity-register compatible than commodity/accounting compatible',
    null_attack:
      'future classified rows concentrate in pots/tags or numerical/accounting-like contexts',
  },
  {
    checked_date: checkedDate,
    signal: 'zero_complement_available',
    support: countBy(classified.filter((row) => row.predicted_class.includes('zero_complement')), (row) => row.predicted_class),
    implication:
      'supports a grammar with explicit null/zero complement marking',
    null_attack:
      '000 continuations diversify into meaningful lexical tails',
  },
];

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'TYPO_HEAD_PLUS_POST_HEAD_OPERATOR_GRAMMAR',
    tier: 'candidate',
    risky_bet:
      'The current `002-H-X` parser is typologically closer to a head-plus-post-head-operator grammar than to a flat visual list: H supplies a slot head, X supplies suffix/enclitic-like class, linker, zero, or chain behavior.',
    current_test:
      `classified=${ratio(classified.length, parseRows.length)}; pass=${ratio(classifiedPass.length, classified.length)}; signals=${typologySignals.map((row) => `${row.signal}=>${row.support}`).join(' | ')}.`,
    destructive_prediction:
      'Same-domain role asymmetries vanish, operator classes collapse into source/formula families, or X roles stop predicting continuation.',
    promotion_prediction:
      'New source-strict held-out rows preserve head-plus-X role predictions across object domains.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'TYPO_NOT_COMMODITY_NUMERAL_CORE',
    tier: 'wild_shot',
    risky_bet:
      'The current live parser core is not commodity/numeral accounting grammar; it is identity/class/linkage grammar for formal seal/tablet legends.',
    current_test:
      `classified domains=${countBy(classified, domain)}; zero complement rows=${classified.filter((row) => row.predicted_class.includes('zero_complement')).length}; linker/class rows=${classified.filter((row) => /(class|linker|chain|operator)/.test(row.predicted_class)).length}.`,
    destructive_prediction:
      'Classified rows start clustering in pots/tags with quantity-like repetition or accounting object ecology.',
    promotion_prediction:
      'More classified rows remain seal/tablet-heavy with head-conditioned post-head roles.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'TYPO_LANGUAGE_FAMILY_DISCRIMINATOR_PENDING',
    tier: 'wild_shot',
    risky_bet:
      'If the head-plus-post-head-operator grammar survives source controls, language-family comparison should prioritize languages with post-head modifiers/case-like or enclitic operator behavior; if it dies, family comparison should pause.',
    current_test:
      'Internal structural precondition only; no language family accepted.',
    destructive_prediction:
      'If slot-role grammar collapses, any language-family mapping from these signs is premature.',
    promotion_prediction:
      'If source-strict role predictions survive, run family-specific morphology tests against the operator inventory.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'typology_discriminator',
  rows: {
    total_parse_rows: parseRows.length,
    classified_rows: classified.length,
    classified_pass: classifiedPass.length,
    classified_domains: countBy(classified, domain),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_signals.csv`), typologySignals, [
  'checked_date',
  'signal',
  'support',
  'implication',
  'null_attack',
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
