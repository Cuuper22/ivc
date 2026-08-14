import fs from 'node:fs';
import path from 'node:path';

// This script builds destructive bets around two awkward single objects:
// inscription 3335.1 (which reads 032-002-390-590-032) and seal H-773 (whose
// frame is 002-390-530-741). It reads lipi/metadata_filtered.csv,
// deduplicates by sign sequence, and gathers the comparison sets each bet
// needs: every 390-590-032 chunk with its neighbors, exact
// 032-002-390-590-032 mirrors, reverse 390-590-032-002 hinges, every
// governed 002-HEAD-530-Y row with a search for "shadow" rows that use the
// same head and complement without the 530, and any direct 002-390-741 rows.
// The four bets: 3335.1 uses two different 032 roles (frame-opener versus
// formula-closer), 3335.1 imports a common formula chunk into a seal-side
// branch slot, H-773's 530 is a one-complement linker between 390 and 741,
// and that 530 is not optional because no direct 002-390-741 shadow exists.
// Writes hinge rows, 530 rows, and the bets as CSVs plus a summary JSON to
// data/open_prototype/reports.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_3335_h773_bets_20260531';
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

function containsAt(tokens, i, pattern) {
  return pattern.every((token, offset) => tokens[i + offset] === token);
}

function countBy(rows, field) {
  const counts = new Map();
  for (const row of rows) {
    const key = row[field] || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }))
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function examples(rows, n = 6) {
  return rows
    .slice(0, n)
    .map((row) => `${row.object}:${row.text}`)
    .join(' | ');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const hingeRows = [];
const pattern390590032 = ['390', '590', '032'];
const pattern032002390590032 = ['032', '002', '390', '590', '032'];
const pattern390590032002 = ['390', '590', '032', '002'];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (!containsAt(row.tokens, i, pattern390590032)) continue;
    hingeRows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      symbol: row.symbol,
      cult: row.cult,
      chunk_start_1based: String(i + 1),
      prev_before_chunk: row.tokens[i - 1] ?? '<START>',
      next_after_chunk: row.tokens[i + 3] ?? '<END>',
      has_002_before_chunk: String(row.tokens[i - 1] === '002'),
      has_002_after_chunk: String(row.tokens[i + 3] === '002'),
      is_target_3335_mirror: String(row.id === '3335.1' && containsAt(row.tokens, i - 2, pattern032002390590032)),
      text: row.text,
    });
  }
}

const target3335 = rows.find((row) => row.id === '3335.1');
const directMirrorRows = rows.filter((row) =>
  row.tokens.some((_, i) => containsAt(row.tokens, i, pattern032002390590032)),
);
const reverseHingeRows = rows.filter((row) =>
  row.tokens.some((_, i) => containsAt(row.tokens, i, pattern390590032002)),
);
const non032Target590Rows = rows.filter((row) =>
  row.tokens.some((_, i) => containsAt(row.tokens, i, ['002', '390', '590']) && row.tokens[i + 3] !== '032'),
);

const governed530Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 3; i += 1) {
    if (row.tokens[i] !== '002' || row.tokens[i + 2] !== '530') continue;
    const head = row.tokens[i + 1];
    const complement = row.tokens[i + 3] ?? '<END>';
    const directShadow = rows.filter((other) =>
      other.tokens.some((_, j) => other.tokens[j] === '002' && other.tokens[j + 1] === head && other.tokens[j + 2] === complement),
    );
    governed530Rows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      left_final: row.tokens[i - 1] ?? '<START>',
      head_after_002: head,
      complement_after_530: complement,
      tail_after_complement: row.tokens.slice(i + 4).join(' ') || '<END>',
      one_complement_only: String(row.tokens.length === i + 4),
      direct_002_head_complement_shadow_count: String(directShadow.length),
      direct_shadow_objects: directShadow.map((other) => other.object).join(';'),
      is_h773_target: String(row.object === 'H-773'),
      text: row.text,
    });
  }
}

const h773Direct390741 = rows.filter((row) =>
  row.tokens.some((_, i) => row.tokens[i] === '002' && row.tokens[i + 1] === '390' && row.tokens[i + 2] === '741'),
);
const h773Rows = governed530Rows.filter((row) => row.is_h773_target === 'true');
const target530BadTail = governed530Rows.filter((row) => row.is_h773_target === 'true' && row.one_complement_only !== 'true');

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_3335_TWO_032_HINGE',
    tier: directMirrorRows.length === 1 && reverseHingeRows.length >= 1 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      '3335.1 uses two distinct 032 roles: left 032 opens the 002 frame, final 032 closes an imported 390-590-032 formula.',
    current_test:
      `${directMirrorRows.length} direct 032-002-390-590-032 row(s); ${reverseHingeRows.length} reverse 390-590-032-002 hinge row(s).`,
    evidence: `direct=${examples(directMirrorRows)} | reverse=${examples(reverseHingeRows)}`,
    destructive_prediction:
      'A source-bound 3335.1 without either 032, or with target 002-390-590-Y where Y is not 032, kills the hinge bet.',
    promotion_prediction:
      'A second source-bound Y-032-002-390-590-032 row or strict source validation of 3335.1 promotes the hinge bet.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_3335_REGISTER_TRANSFER',
    tier: 'wild_shot',
    risky_bet:
      '3335.1 is a register-transfer row: a common 390-590-032 chunk is imported into a seal-side 002-390 branch slot, not simply copied as a normal 390-590 formula.',
    current_test: `${hingeRows.length} 390-590-032 chunk rows across sites/types: sites=${countBy(hingeRows, 'site')}; types=${countBy(hingeRows, 'type')}.`,
    evidence: examples(hingeRows),
    destructive_prediction:
      'If the source identifies 3335.1 as an ordinary duplicate or damaged variant of an already-known 390-590-032 row, demote transfer to copied formula.',
    promotion_prediction:
      'If source binding keeps 3335.1 as an independent seal row with 032-002 before the chunk, promote to candidate.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_H773_530_COMPLEMENTIZER',
    tier: h773Rows.length === 1 && target530BadTail.length === 0 ? 'candidate' : 'wild_shot',
    risky_bet:
      'In H-773, 530 is a one-complement linker between 390 and 741, not a semantic X value by itself.',
    current_test:
      `${governed530Rows.length} governed 002-H-530-Y rows; H-773 has ${h773Rows.length}; H-773 bad-tail count ${target530BadTail.length}.`,
    evidence: examples(governed530Rows),
    destructive_prediction:
      'A cleaner source image that fuses 530 with 741/390, or adds another complement after 741, demotes the complementizer bet.',
    promotion_prediction:
      'A strict image or sign list preserving separable 390-530-741 with no further tail promotes the syntax bet.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_H773_NO_DIRECT_390741_SHADOW',
    tier: h773Direct390741.length === 0 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      'H-773 530 is not merely optional decoration before 741; if it were optional, direct 002-390-741 shadows should exist.',
    current_test: `${h773Direct390741.length} canonical 002-390-741 direct-shadow rows found.`,
    evidence: examples(h773Direct390741),
    destructive_prediction:
      'Finding a strict source-visible 002-390-741 direct shadow makes 530 optional/register-like before semantic analysis.',
    promotion_prediction:
      'Continued absence of direct 002-390-741 shadows plus strict H-773 separability strengthens 530 as a real linker.',
  },
];

writeCsv(
  path.join(reportsDir, `${prefix}_3335_hinge_rows.csv`),
  hingeRows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'shape',
    'symbol',
    'cult',
    'chunk_start_1based',
    'prev_before_chunk',
    'next_after_chunk',
    'has_002_before_chunk',
    'has_002_after_chunk',
    'is_target_3335_mirror',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_530_rows.csv`),
  governed530Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'shape',
    'left_final',
    'head_after_002',
    'complement_after_530',
    'tail_after_complement',
    'one_complement_only',
    'direct_002_head_complement_shadow_count',
    'direct_shadow_objects',
    'is_h773_target',
    'text',
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
  status: 'expand_3335_h773_bets',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    hinge_390590032_rows: hingeRows.length,
    direct_032002390590032_rows: directMirrorRows.length,
    reverse_390590032002_rows: reverseHingeRows.length,
    governed_530_rows: governed530Rows.length,
    direct_002390741_shadow_rows: h773Direct390741.length,
    non032_target_002390590_rows: non032Target590Rows.length,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
