import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_semantic_role_bets_20260531';
const checkedDate = '2026-05-31';
const focusXs = new Set(['095', '125', '530', '705']);

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

function examples(rows, n = 6) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

function objectDomain(row) {
  if (String(row.type).startsWith('SEAL')) return 'seal';
  if (String(row.type).startsWith('TAB')) return 'tablet';
  if (String(row.type).startsWith('POT')) return 'pot';
  if (String(row.type).startsWith('TAG')) return 'tag';
  return row.type || '-';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = uniqueRowsByText(
  parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
    ...row,
    object: objectId(row),
    tokens: signs(row.text),
  })),
);

const focusRows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 2; i += 1) {
    if (row.tokens[i] !== '002' || !focusXs.has(row.tokens[i + 2])) continue;
    const tail = row.tokens.slice(i + 3);
    focusRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      domain: objectDomain(row),
      shape: row.shape,
      material: row.material,
      head: row.tokens[i + 1],
      x: row.tokens[i + 2],
      tail_after_x: tail.join(' ') || '<END>',
      open: String(tail.length > 0),
      text: row.text,
    });
  }
}

const semanticRows = [...focusXs].map((x) => {
  const rowsForX = focusRows.filter((row) => row.x === x);
  return {
    checked_date: checkedDate,
    x,
    rows: String(rowsForX.length),
    domains: countBy(rowsForX, (row) => row.domain),
    sites: countBy(rowsForX, (row) => row.site),
    heads: countBy(rowsForX, (row) => row.head),
    open: ratio(rowsForX.filter((row) => row.open === 'true').length, rowsForX.length),
    tails: countBy(rowsForX, (row) => row.tail_after_x),
    examples: examples(rowsForX),
  };
});

const bets = [
  {
    checked_date: checkedDate,
    bet_id: 'SEM_095_RIGHT_EDGE_IDENTITY_LABEL',
    tier: 'wild_shot',
    risky_bet:
      '`095` marks a right-edge identity/class label in the `002-H-X` construction, closer to a seal-owner/title label than a commodity or numeral.',
    current_test:
      semanticRows.find((row) => row.x === '095')?.examples ?? '',
    destructive_prediction:
      'Pot/accounting-heavy `002-H-095` rows or continuing `002-H-095-Y` rows demote the identity-label role.',
    promotion_prediction:
      'More closed `002-H-095` rows on seals/tablets across heads promote it as a terminal identity/class label.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'SEM_125_DEPENDENT_TITLE_CHAIN',
    tier: 'wild_shot',
    risky_bet:
      '`125` opens a dependent title/name chain rather than a commodity count: it appears mainly on formal seal legends and routes into constrained tails.',
    current_test:
      semanticRows.find((row) => row.x === '125')?.examples ?? '',
    destructive_prediction:
      'Repeated `125` on pot/accounting contexts, or unconstrained arbitrary tails, kills the title-chain role.',
    promotion_prediction:
      'More seal/tablet rows with head-conditioned tails promote `125` as a dependent title/name-chain operator.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'SEM_530_GENITIVE_OR_ASSOCIATIVE_LINKER',
    tier: 'wild_shot',
    risky_bet:
      '`530` is an associative linker: `002-H-530-Y` means H is linked to exactly one dependent complement Y, roughly genitive/with/of in structural role, not lexical value.',
    current_test:
      semanticRows.find((row) => row.x === '530')?.examples ?? '',
    destructive_prediction:
      'Any `530` row with two dependent complements, or frequent direct `002-H-Y` shadows with no contrast, demotes this role.',
    promotion_prediction:
      'More one-complement `530` rows across domains promote an associative-linker function.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'SEM_705_GROUP_OR_DEFAULT_CLASS_LABEL',
    tier: 'wild_shot',
    risky_bet:
      '`705` is a default group/class label in this construction, with head `320` licensing a `125` cap; it is not itself the name/value being read.',
    current_test:
      semanticRows.find((row) => row.x === '705')?.examples ?? '',
    destructive_prediction:
      'Multiple open `705` rows under non-320 heads or source-bound `390-705-Y` continuation kills default class-label behavior.',
    promotion_prediction:
      'More closed `390/033/940-705` rows plus repeated `320-705-125` promotes the group/class exception model.',
  },
];

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'semantic_role_bets',
  rows: {
    focus_rows: focusRows.length,
    by_x: Object.fromEntries(semanticRows.map((row) => [row.x, row.rows])),
  },
  bets: bets.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

writeCsv(path.join(reportsDir, `${prefix}_semantic_rows.csv`), semanticRows, [
  'checked_date',
  'x',
  'rows',
  'domains',
  'sites',
  'heads',
  'open',
  'tails',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_target_rows.csv`), focusRows, [
  'checked_date',
  'object',
  'row_id',
  'site',
  'type',
  'domain',
  'shape',
  'material',
  'head',
  'x',
  'tail_after_x',
  'open',
  'text',
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
