import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_payload_class_discriminator_20260531';
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

function containsAt(tokens, start, pattern) {
  return pattern.every((token, offset) => tokens[start + offset] === token);
}

function countBy(items, field) {
  const counts = new Map();
  for (const item of items) {
    const key = item[field] || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function examples(rows, n = 8) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

function entropy(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  const total = values.length;
  let e = 0;
  for (const value of counts.values()) {
    const p = value / total;
    e -= p * Math.log2(p);
  }
  return e;
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const sharedPrefixRows = [];
const headOccurrences = [];
const chunkRows = [];
const chunks = [
  { label: '252-840', pattern: ['252', '840'] },
  { label: '390-590-032', pattern: ['390', '590', '032'] },
  { label: '002-252-840', pattern: ['002', '252', '840'] },
  { label: '002-390-590-032', pattern: ['002', '390', '590', '032'] },
];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (containsAt(row.tokens, i, ['740', '205', '032', '002'])) {
      sharedPrefixRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        head_after_002: row.tokens[i + 4] ?? '<END>',
        payload_after_head: row.tokens.slice(i + 5).join(' ') || '<END>',
        payload_class:
          row.tokens[i + 4] === '252'
            ? 'control_closure_payload'
            : row.tokens[i + 4] === '390'
              ? 'target_open_formula_payload'
              : 'other',
        text: row.text,
      });
    }

    if (row.tokens[i] === '002' && row.tokens[i + 1]) {
      const head = row.tokens[i + 1];
      if (head === '252' || head === '390') {
        headOccurrences.push({
          checked_date: checkedDate,
          object: row.object,
          row_id: row.id,
          site: row.site,
          type: row.type,
          symbol: row.symbol,
          cult: row.cult,
          head_after_002: head,
          next_after_head: row.tokens[i + 2] ?? '<END>',
          tail_after_head: row.tokens.slice(i + 2).join(' ') || '<END>',
          terminal_after_head: String(i + 2 >= row.tokens.length),
          exact_shared_prefix: String(i >= 3 && containsAt(row.tokens, i - 3, ['740', '205', '032', '002'])),
          text: row.text,
        });
      }
    }

    for (const chunk of chunks) {
      if (!containsAt(row.tokens, i, chunk.pattern)) continue;
      chunkRows.push({
        checked_date: checkedDate,
        chunk: chunk.label,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_chunk: row.tokens[i - 1] ?? '<START>',
        next_after_chunk: row.tokens[i + chunk.pattern.length] ?? '<END>',
        terminal_after_chunk: String(i + chunk.pattern.length >= row.tokens.length),
        after_002: String(row.tokens[i - 1] === '002' || chunk.label.startsWith('002-')),
        exact_shared_prefix: String(i >= 4 && containsAt(row.tokens, i - 4, ['740', '205', '032', '002'])),
        text: row.text,
      });
    }
  }
}

const headSummary = ['252', '390'].map((head) => {
  const occurrences = headOccurrences.filter((row) => row.head_after_002 === head);
  return {
    checked_date: checkedDate,
    head_after_002: head,
    governed_rows: String(occurrences.length),
    terminal_after_head: String(occurrences.filter((row) => row.terminal_after_head === 'true').length),
    terminal_share: occurrences.length
      ? (occurrences.filter((row) => row.terminal_after_head === 'true').length / occurrences.length).toFixed(6)
      : 'NA',
    next_entropy_bits: occurrences.length ? entropy(occurrences.map((row) => row.next_after_head)).toFixed(6) : 'NA',
    top_next_after_head: countBy(occurrences, 'next_after_head'),
    sites: countBy(occurrences, 'site'),
    types: countBy(occurrences, 'type'),
    examples: examples(occurrences),
  };
});

const chunkSummary = chunks.map((chunk) => {
  const occurrences = chunkRows.filter((row) => row.chunk === chunk.label);
  return {
    checked_date: checkedDate,
    chunk: chunk.label,
    rows: String(occurrences.length),
    terminal_after_chunk: String(occurrences.filter((row) => row.terminal_after_chunk === 'true').length),
    after_002_rows: String(occurrences.filter((row) => row.after_002 === 'true').length),
    exact_shared_prefix_rows: String(occurrences.filter((row) => row.exact_shared_prefix === 'true').length),
    sites: countBy(occurrences, 'site'),
    types: countBy(occurrences, 'type'),
    examples: examples(occurrences),
  };
});

const governed252 = headOccurrences.filter((row) => row.head_after_002 === '252');
const governed390 = headOccurrences.filter((row) => row.head_after_002 === '390');
const chunk252840 = chunkRows.filter((row) => row.chunk === '252-840');
const chunk390590032 = chunkRows.filter((row) => row.chunk === '390-590-032');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_PAYLOAD_HEAD_CLASS_ALTERNATION',
    tier: sharedPrefixRows.length === 2 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      'The exact prefix 740-205-032-002 licenses different payload head classes: M-143 uses 252-840 as closure payload, while 3335.1 uses 390-590-032 as open/formula payload.',
    current_test:
      `${sharedPrefixRows.length} exact shared-prefix rows; payload classes=${countBy(sharedPrefixRows, 'payload_class')}.`,
    evidence: examples(sharedPrefixRows),
    destructive_prediction:
      'If 3335.1 does not source-bind or collapses into a copied 390-590-032 object unrelated to the shared prefix, demote alternation.',
    promotion_prediction:
      'If 3335.1 source-binds independently, the M-143/3335 pair becomes a head-class minimal pair under a shared prefix.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_252840_CLOSURE_PAYLOAD',
    tier: chunk252840.length === 1 && governed252.length === 1 ? 'wild_shot' : 'too_dirty',
    risky_bet:
      'M-143 252-840 is a closure-like payload under 032-002, not a productive branch family like 390.',
    current_test:
      `002-252 rows=${governed252.length}; 252-840 chunk rows=${chunk252840.length}; terminal 252 head share=${headSummary.find((row) => row.head_after_002 === '252').terminal_share}.`,
    evidence: examples(governed252),
    destructive_prediction:
      'More 002-252-Y diversity or nonterminal 252-840 continuations would kill closure-payload status.',
    promotion_prediction:
      'A source-visible M-143 token reading plus more terminal 002-252-840-like rows would promote the closure-payload parse.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_390_AS_OPEN_PAYLOAD_HEAD',
    tier: governed390.length >= 10 ? 'candidate' : 'wild_shot',
    risky_bet:
      'Under 032-002, choosing 390 means choosing an open payload head rather than a closure head.',
    current_test:
      `002-390 rows=${governed390.length}; next entropy=${headSummary.find((row) => row.head_after_002 === '390').next_entropy_bits}; 390-590-032 chunk rows=${chunk390590032.length}.`,
    evidence: examples(governed390),
    destructive_prediction:
      'If source-normalized 002-390 rows collapse into copied formulae, demote open payload head.',
    promotion_prediction:
      'If source-visible 002-390 rows keep diverse X choices while exact-prefix 3335 binds, promote 390 as open payload head.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_FORMULA_PAYLOAD_VS_CLOSURE_PAYLOAD',
    tier: 'wild_shot',
    risky_bet:
      'The M-143/3335 contrast is semantic-class-like: 252-840 closes the prefix locally; 390-590-032 imports a portable formula payload.',
    current_test:
      `252-840 rows=${chunk252840.length}; 390-590-032 rows=${chunk390590032.length}; 390-590-032 sites=${countBy(chunk390590032, 'site')}.`,
    evidence: `252=${examples(chunk252840)} | 390=${examples(chunk390590032)}`,
    destructive_prediction:
      'If 390-590-032 source rows collapse to duplicates or 252-840 has hidden formula ecology, demote semantic-class contrast.',
    promotion_prediction:
      'If 3335.1 binds and 390-590-032 remains portable across independent source-visible rows, promote formula-payload contrast.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_shared_prefix_rows.csv`),
  sharedPrefixRows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'head_after_002',
    'payload_after_head',
    'payload_class',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_head_summary.csv`),
  headSummary,
  [
    'checked_date',
    'head_after_002',
    'governed_rows',
    'terminal_after_head',
    'terminal_share',
    'next_entropy_bits',
    'top_next_after_head',
    'sites',
    'types',
    'examples',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_chunk_summary.csv`),
  chunkSummary,
  [
    'checked_date',
    'chunk',
    'rows',
    'terminal_after_chunk',
    'after_002_rows',
    'exact_shared_prefix_rows',
    'sites',
    'types',
    'examples',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_bets.csv`),
  betRows,
  [
    'checked_date',
    'bet_id',
    'tier',
    'risky_bet',
    'current_test',
    'evidence',
    'destructive_prediction',
    'promotion_prediction',
  ],
);

const summary = {
  checked_date: checkedDate,
  phase: 'EXPAND',
  status: 'expand_payload_class_discriminator',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    exact_740205032002_prefix_rows: sharedPrefixRows.length,
    governed_002252_rows: governed252.length,
    governed_002390_rows: governed390.length,
    chunk_252840_rows: chunk252840.length,
    chunk_390590032_rows: chunk390590032.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
