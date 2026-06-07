import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_expand_prefix530_portability_20260531';
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

function examples(items, n = 8) {
  return items
    .slice(0, n)
    .map((item) => `${item.object}:${item.text}`)
    .join(' | ');
}

function headTerminalProfile(rows, head) {
  const occurrences = [];
  for (const row of rows) {
    for (let i = 0; i < row.tokens.length - 1; i += 1) {
      if (row.tokens[i] !== '002' || row.tokens[i + 1] !== head) continue;
      occurrences.push({
        object: row.object,
        terminal: i + 2 >= row.tokens.length,
        next: row.tokens[i + 2] ?? '<END>',
        text: row.text,
      });
    }
  }
  const terminal = occurrences.filter((row) => row.terminal).length;
  return {
    governed_head_rows: occurrences.length,
    governed_head_terminal_rows: terminal,
    governed_head_terminal_share: occurrences.length ? (terminal / occurrences.length).toFixed(6) : 'NA',
    governed_head_top_next: countBy(occurrences, 'next'),
  };
}

fs.mkdirSync(reportsDir, { recursive: true });

const rawRows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  tokens: signs(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.tokens.join(' '), row])).values()];

const sharedPrefix = ['740', '205', '032', '002'];
const sharedPrefixRows = [];
const all032002Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 1; i += 1) {
    if (row.tokens[i] === '032' && row.tokens[i + 1] === '002') {
      all032002Rows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_032: row.tokens[i - 1] ?? '<START>',
        head_after_002: row.tokens[i + 2] ?? '<END>',
        tail_after_head: row.tokens.slice(i + 3).join(' ') || '<END>',
        exact_740205_prefix: String(i >= 2 && row.tokens[i - 2] === '740' && row.tokens[i - 1] === '205'),
        text: row.text,
      });
    }
    if (containsAt(row.tokens, i, sharedPrefix)) {
      sharedPrefixRows.push({
        checked_date: checkedDate,
        object: row.object,
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        material: row.material,
        shape: row.shape,
        head_after_002: row.tokens[i + 4] ?? '<END>',
        tail_after_head: row.tokens.slice(i + 5).join(' ') || '<END>',
        branch_family: row.tokens[i + 4] === '390' ? 'target_hinge_branch' : 'prefix_control_branch',
        source_readiness:
          row.object === 'M-143'
            ? 'public_panel_visible_not_token_strict'
            : row.id === '3335.1'
              ? 'metadata_unbound'
              : 'unknown',
        text: row.text,
      });
    }
  }
}

const governed530Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length - 3; i += 1) {
    if (row.tokens[i] !== '002' || row.tokens[i + 2] !== '530') continue;
    const head = row.tokens[i + 1];
    const complement = row.tokens[i + 3];
    const directShadow = rows.filter((other) =>
      other.tokens.some((_, j) => other.tokens[j] === '002' && other.tokens[j + 1] === head && other.tokens[j + 2] === complement),
    );
    const complementProfile = headTerminalProfile(rows, complement);
    governed530Rows.push({
      checked_date: checkedDate,
      object: row.object,
      row_id: row.id,
      site: row.site,
      type: row.type,
      shape: row.shape,
      head_after_002: head,
      complement_after_530: complement,
      tail_after_complement: row.tokens.slice(i + 4).join(' ') || '<END>',
      one_complement_only: String(i + 4 === row.tokens.length),
      direct_shadow_count: String(directShadow.length),
      direct_shadow_objects: directShadow.map((other) => other.object).join(';'),
      complement_governed_head_rows: String(complementProfile.governed_head_rows),
      complement_governed_head_terminal_share: complementProfile.governed_head_terminal_share,
      complement_governed_head_top_next: complementProfile.governed_head_top_next,
      portability_role:
        directShadow.length > 0
          ? 'optional_or_contrastive_linker_warning'
          : complementProfile.governed_head_rows > 0
            ? 'linker_to_known_governed_head'
            : 'linker_to_unprofiled_complement',
      text: row.text,
    });
  }
}

const directPrefixHeadCounts = countBy(sharedPrefixRows, 'head_after_002');
const all032HeadCounts = countBy(all032002Rows, 'head_after_002');
const noDirect002390741 = !rows.some((row) =>
  row.tokens.some((_, i) => row.tokens[i] === '002' && row.tokens[i + 1] === '390' && row.tokens[i + 2] === '741'),
);

const betRows = [
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_3335_SHARED_PREFIX_ALTERNATION',
    tier: sharedPrefixRows.length === 2 && directPrefixHeadCounts.includes('252:1') && directPrefixHeadCounts.includes('390:1')
      ? 'candidate_edge'
      : 'wild_shot',
    risky_bet:
      'The prefix 740-205-032-002 is a real branch frame: source-visible M-143 selects 252-840, while unbound 3335.1 selects 390-590-032.',
    current_test: `${sharedPrefixRows.length} exact shared-prefix rows; heads=${directPrefixHeadCounts}.`,
    evidence: examples(sharedPrefixRows),
    destructive_prediction:
      'If 3335.1 is a duplicate/damaged M-143-like source or does not preserve 390-590-032 after the shared prefix, the alternation dies.',
    promotion_prediction:
      'If 3335.1 source-binds as an independent row, the shared-prefix pair becomes the best 032-002 head alternation witness.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_032002_HEAD_SWITCHBOARD',
    tier: all032002Rows.length >= 10 ? 'wild_shot' : 'too_small',
    risky_bet:
      '032-002 is a switchboard frame that can route into many heads; 390 is one selected lane rather than the deterministic value of 032-002.',
    current_test: `${all032002Rows.length} canonical 032-002 rows; heads=${all032HeadCounts}.`,
    evidence: examples(all032002Rows),
    destructive_prediction:
      'If source-normalized rows collapse into one or two copied templates, demote switchboard to formula residue.',
    promotion_prediction:
      'If source-visible 032-002 rows preserve head diversity across sites/forms, promote 032-002 as a frame-opening environment.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_530_PORTABLE_LINKER_WITH_OPTIONAL_WARNING',
    tier: governed530Rows.length === 4 && governed530Rows.every((row) => row.one_complement_only === 'true')
      ? 'candidate'
      : 'wild_shot',
    risky_bet:
      '530 is a portable one-complement linker across multiple heads; direct shadows mark optional/contrastive uses, not a fixed semantic value.',
    current_test:
      `${governed530Rows.length} governed 002-H-530-Y rows; all one-complement=${governed530Rows.every((row) => row.one_complement_only === 'true')}; direct-shadow rows=${governed530Rows.filter((row) => row.direct_shadow_count !== '0').length}.`,
    evidence: examples(governed530Rows),
    destructive_prediction:
      'A governed 530 row with zero/multiple complements or widespread direct shadows demotes 530 to optional register material.',
    promotion_prediction:
      'A new source-strict 002-H-530-Y row with separable one-complement structure and no direct shadow strengthens portability.',
  },
  {
    checked_date: checkedDate,
    bet_id: 'EXPAND_H773_530_NOT_OPTIONAL_BEFORE_741',
    tier: noDirect002390741 ? 'candidate_edge' : 'wild_shot',
    risky_bet:
      'Specifically in H-773, 530 is not optional before 741 because the corpus lacks direct 002-390-741 shadows.',
    current_test: `direct 002-390-741 shadow exists=${String(!noDirect002390741)}.`,
    evidence: '',
    destructive_prediction:
      'Find a source-visible direct 002-390-741 row or visual fusion of 530/741, and 530 becomes optional/register-like.',
    promotion_prediction:
      'Strict H-773 token separation plus continued absence of direct 390-741 shadows promotes 530 as real linker.',
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
    'material',
    'shape',
    'head_after_002',
    'tail_after_head',
    'branch_family',
    'source_readiness',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_032002_rows.csv`),
  all032002Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'symbol',
    'cult',
    'prev_before_032',
    'head_after_002',
    'tail_after_head',
    'exact_740205_prefix',
    'text',
  ],
);
writeCsv(
  path.join(reportsDir, `${prefix}_530_portability_rows.csv`),
  governed530Rows,
  [
    'checked_date',
    'object',
    'row_id',
    'site',
    'type',
    'shape',
    'head_after_002',
    'complement_after_530',
    'tail_after_complement',
    'one_complement_only',
    'direct_shadow_count',
    'direct_shadow_objects',
    'complement_governed_head_rows',
    'complement_governed_head_terminal_share',
    'complement_governed_head_top_next',
    'portability_role',
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
  status: 'expand_prefix530_portability',
  rows: {
    raw: rawRows.length,
    canonical_numeric_sequences: rows.length,
    exact_740205032002_prefix_rows: sharedPrefixRows.length,
    all_032002_rows: all032002Rows.length,
    governed_530_rows: governed530Rows.length,
    governed_530_direct_shadow_rows: governed530Rows.filter((row) => row.direct_shadow_count !== '0').length,
    direct_002390741_shadow_rows: noDirect002390741 ? 0 : 1,
  },
  head_counts: {
    exact_740205032002: directPrefixHeadCounts,
    all_032002: all032HeadCounts,
  },
  bets: betRows.map((row) => ({ bet_id: row.bet_id, tier: row.tier })),
};

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
