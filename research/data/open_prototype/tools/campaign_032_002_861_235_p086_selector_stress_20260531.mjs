import fs from 'node:fs';
import path from 'node:path';

// The claim under stress: sign 235 before a 002 frame selects a later 125 — but only when
// the head after 002 belongs to the P086 family (390 or 405), not as a blanket 235 rule.
// This script tests the interaction with real statistics. It reads data/open_prototype/
// lipi/metadata_filtered.csv (deduplicated) and the open-head classifier report, tags every
// 002 frame with its predecessor, head family (P086 390/405, the wilder 392 extension,
// closure heads 817/820/861, or broad-open heads), and whether its tail contains 125, then
// runs five 2x2 contrasts scored with a one-sided Fisher exact test computed from the
// hypergeometric distribution. Key numbers: 235 + P086 head is 3/3 for 125 while 235 +
// closure heads is 0/22 (p = 0.000435), and non-P086 open heads are 0/4 — so the generic
// versions of the rule are dead while the interaction survives as candidate. The
// M-47/M-735 pair, sharing the exact left context 740-760-235-002, is kept as the minimal
// contrast. Writes all frames, 235 frames, family summaries, contrasts, minimal contrasts,
// and decisions as CSVs plus a summary JSON in reports/.

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const HEAD_CLASSES = path.join(
  ROOT,
  'data',
  'open_prototype',
  'reports',
  'campaign_032_002_861_after002_open_head_classifier_20260531_head_classes.csv',
);
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'campaign_032_002_861_235_p086_selector_stress_20260531';
const RUN_DATE = '2026-05-31';

const P086_HEADS = new Set(['390', '405']);
const P086_EXTENSION_HEADS = new Set(['390', '405', '392']);
const CLOSURE_HEADS = new Set(['817', '820', '861']);

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

function csvEscape(value) {
  const text = String(value ?? '');
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function top(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function choose(n, k) {
  if (k < 0 || k > n) return 0;
  const kk = Math.min(k, n - k);
  let out = 1;
  for (let i = 1; i <= kk; i += 1) {
    out *= (n - kk + i) / i;
  }
  return out;
}

function hypergeometricProbability({ population, successPopulation, draws, observedSuccesses }) {
  return (choose(successPopulation, observedSuccesses) * choose(population - successPopulation, draws - observedSuccesses)) / choose(population, draws);
}

function fisherGreater(a, b, c, d) {
  const population = a + b + c + d;
  const successPopulation = a + c;
  const draws = a + b;
  const max = Math.min(draws, successPopulation);
  let p = 0;
  for (let x = a; x <= max; x += 1) {
    p += hypergeometricProbability({ population, successPopulation, draws, observedSuccesses: x });
  }
  return p;
}

function tableRow({ name, groupA, groupB, interpretation }) {
  const a = groupA.filter((row) => row.tail_has_125 === 'true').length;
  const b = groupA.length - a;
  const c = groupB.filter((row) => row.tail_has_125 === 'true').length;
  const d = groupB.length - c;
  return {
    checked_date: RUN_DATE,
    contrast: name,
    group_a_rows: String(groupA.length),
    group_a_has125: String(a),
    group_a_rate: groupA.length ? (a / groupA.length).toFixed(6) : 'NA',
    group_b_rows: String(groupB.length),
    group_b_has125: String(c),
    group_b_rate: groupB.length ? (c / groupB.length).toFixed(6) : 'NA',
    fisher_greater_p: groupA.length && groupB.length ? fisherGreater(a, b, c, d).toFixed(6) : 'NA',
    group_a_objects: groupA.map((row) => `${row.object}:${row.head_after_002}:${row.tail_after_head}`).join(';'),
    group_b_objects: groupB.map((row) => `${row.object}:${row.head_after_002}:${row.tail_after_head}`).join(';'),
    interpretation,
  };
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const headClasses = new Map(
  parseCsv(fs.readFileSync(HEAD_CLASSES, 'utf8')).map((row) => [row.head_after_002, row.classifier_class]),
);

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  object: objectId(row),
  signs: tokens(row.text),
}));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()];

const frames = [];
for (const row of rows) {
  row.signs.forEach((sign, idx) => {
    if (sign !== '002' || !row.signs[idx + 1]) return;
    const head = row.signs[idx + 1];
    const afterHead = row.signs.slice(idx + 2);
    const tailAfterHead = afterHead.join(' ') || '<END>';
    const fullTailAfter002 = row.signs.slice(idx + 1).join(' ') || '<END>';
    const prev = row.signs[idx - 1] ?? '<START>';
    const left3 = row.signs.slice(Math.max(0, idx - 3), idx).join(' ') || '<START>';
    const headClass = headClasses.get(head) ?? 'low_count_or_unclassified';
    const p086 = P086_HEADS.has(head);
    const p086Extension = P086_EXTENSION_HEADS.has(head);
    const closure = CLOSURE_HEADS.has(head);
    const broadOpen = headClass === 'open_selector_head';
    frames.push({
      checked_date: RUN_DATE,
      row_id: row.id,
      object: row.object,
      site: row.site || 'NA',
      type: row.type || 'NA',
      symbol: row.symbol || 'NA',
      cult: row.cult || 'NA',
      prev_before_002: prev,
      left3_before_002: left3,
      head_after_002: head,
      head_classifier_class: headClass,
      branch_after_head: row.signs[idx + 2] ?? '<END>',
      tail_after_head: tailAfterHead,
      full_tail_after_002: fullTailAfter002,
      terminal_after_head: afterHead.length ? 'false' : 'true',
      tail_has_125: afterHead.includes('125') ? 'true' : 'false',
      prev235: prev === '235' ? 'true' : 'false',
      p086_head_390_405: p086 ? 'true' : 'false',
      p086_extension_390_405_392: p086Extension ? 'true' : 'false',
      closure_head_817_820_861: closure ? 'true' : 'false',
      broad_open_head: broadOpen ? 'true' : 'false',
      text: row.text,
    });
  });
}

const prev235 = frames.filter((row) => row.prev235 === 'true');
const prev235P086 = prev235.filter((row) => row.p086_head_390_405 === 'true');
const prev235P086Ext = prev235.filter((row) => row.p086_extension_390_405_392 === 'true');
const prev235Closure = prev235.filter((row) => row.closure_head_817_820_861 === 'true');
const prev235BroadOpenNonP086 = prev235.filter(
  (row) => row.broad_open_head === 'true' && row.p086_head_390_405 === 'false',
);
const prev235Other = prev235.filter(
  (row) =>
    row.p086_extension_390_405_392 === 'false' &&
    row.closure_head_817_820_861 === 'false' &&
    row.broad_open_head === 'false',
);
const p086All = frames.filter((row) => row.p086_head_390_405 === 'true');
const p086Prev235 = p086All.filter((row) => row.prev235 === 'true');
const p086NotPrev235 = p086All.filter((row) => row.prev235 === 'false');
const p086ExtAll = frames.filter((row) => row.p086_extension_390_405_392 === 'true');
const p086ExtPrev235 = p086ExtAll.filter((row) => row.prev235 === 'true');
const p086ExtNotPrev235 = p086ExtAll.filter((row) => row.prev235 === 'false');

const contrastRows = [
  tableRow({
    name: 'within_235_p086_vs_closure',
    groupA: prev235P086,
    groupB: prev235Closure,
    interpretation: '`235-002-390/405` selects `125` while `235-002-817/820/861` closes without it.',
  }),
  tableRow({
    name: 'within_235_p086_vs_generic_broad_open',
    groupA: prev235P086,
    groupB: prev235BroadOpenNonP086,
    interpretation: 'Kills broad open-head version: non-P086 open heads after `235-002` do not select `125` here.',
  }),
  tableRow({
    name: 'within_p086_prev235_vs_not_prev235',
    groupA: p086Prev235,
    groupB: p086NotPrev235,
    interpretation: 'Tests whether `235` is doing work inside P086 heads rather than `390/405` generally selecting `125`.',
  }),
  tableRow({
    name: 'within_p086_extension_prev235_vs_not_prev235',
    groupA: p086ExtPrev235,
    groupB: p086ExtNotPrev235,
    interpretation: 'Same contrast if `392-590-125` is allowed as a wild P086 extension.',
  }),
  tableRow({
    name: 'within_235_p086_extension_vs_closure',
    groupA: prev235P086Ext,
    groupB: prev235Closure,
    interpretation: 'The permissive family `390/405/392` remains clean against closure heads, but `392` is not promoted.',
  }),
];

const familyRows = [
  {
    checked_date: RUN_DATE,
    family: '235-002-P086(390/405)',
    rows: String(prev235P086.length),
    has125: String(prev235P086.filter((row) => row.tail_has_125 === 'true').length),
    heads: top(countBy(prev235P086, (row) => row.head_after_002)),
    objects: prev235P086.map((row) => `${row.object}:${row.full_tail_after_002}`).join(';'),
    tier_after_test: 'candidate_strengthened',
    implication: '`235` plus P086-family head selects `125`; this is not a generic `235` rule.',
  },
  {
    checked_date: RUN_DATE,
    family: '235-002-closure(817/820/861)',
    rows: String(prev235Closure.length),
    has125: String(prev235Closure.filter((row) => row.tail_has_125 === 'true').length),
    heads: top(countBy(prev235Closure, (row) => row.head_after_002)),
    objects: prev235Closure.map((row) => `${row.object}:${row.full_tail_after_002}`).join(';'),
    tier_after_test: 'negative_control_support',
    implication: 'Closure heads are the main negative control: `235` does not force `125` by itself.',
  },
  {
    checked_date: RUN_DATE,
    family: '235-002-broad_open_nonP086',
    rows: String(prev235BroadOpenNonP086.length),
    has125: String(prev235BroadOpenNonP086.filter((row) => row.tail_has_125 === 'true').length),
    heads: top(countBy(prev235BroadOpenNonP086, (row) => row.head_after_002)),
    objects: prev235BroadOpenNonP086.map((row) => `${row.object}:${row.full_tail_after_002}`).join(';'),
    tier_after_test: 'broad_open_rule_dead',
    implication: '`125` is not selected by open-head status alone.',
  },
  {
    checked_date: RUN_DATE,
    family: '235-002-other_heads',
    rows: String(prev235Other.length),
    has125: String(prev235Other.filter((row) => row.tail_has_125 === 'true').length),
    heads: top(countBy(prev235Other, (row) => row.head_after_002)),
    objects: prev235Other.map((row) => `${row.object}:${row.full_tail_after_002}`).join(';'),
    tier_after_test: 'background',
    implication: 'Background heads do not rescue a generic `235 -> 125` rule.',
  },
];

const minimalContrastRows = [
  frames.find((row) => row.object === 'M-47' && row.prev_before_002 === '235'),
  frames.find((row) => row.object === 'M-735' && row.prev_before_002 === '235'),
  frames.find((row) => row.object === 'M-38' && row.prev_before_002 === '235'),
  frames.find((row) => row.object === 'M-41' && row.prev_before_002 === '235'),
].filter(Boolean).map((row) => ({
  checked_date: RUN_DATE,
  object: row.object,
  row_id: row.row_id,
  left3_before_002: row.left3_before_002,
  head_after_002: row.head_after_002,
  branch_after_head: row.branch_after_head,
  tail_after_head: row.tail_after_head,
  tail_has_125: row.tail_has_125,
  type: row.type,
  symbol: row.symbol,
  cult: row.cult,
  contrast_role:
    row.object === 'M-47'
      ? 'same_left_740_760_235_closure_control'
      : row.object === 'M-735'
        ? 'same_left_740_760_235_p086_positive'
        : row.head_after_002 === '405'
          ? 'p086_formula_head_positive'
          : 'p086_390_positive',
  text: row.text,
}));

const decisions = [
  {
    checked_date: RUN_DATE,
    named_bet: '`235 + P086 head(390/405)` selects `125` rank/title branch',
    tier_after_test: 'candidate',
    evidence:
      '`235-002-390/405` is 3/3 for tails containing `125`; exact-canonical `235-002-817/820/861` is 0/22; Fisher greater p=0.000435.',
    adversary:
      '`235` alone is not enough: closure heads and generic open heads after `235-002` mostly do not take `125`.',
    falsifier_or_rescue:
      'A comparable `235-002-390/405` row without `125` demotes the rule; another strict positive outside Mohenjo-daro promotes it.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: 'Any open head after `235-002` selects `125`',
    tier_after_test: 'dead',
    evidence: 'Non-P086 open heads after `235-002` are 0/4 for `125`: heads `031`, `220`, and `374` do not carry it.',
    adversary:
      'This blocks the lazy reading that terminality/open-headedness alone explains the `125` branch.',
    falsifier_or_rescue:
      'A future broad-open non-P086 cluster selecting `125` would revive a larger open-head rule, but current evidence kills it.',
  },
  {
    checked_date: RUN_DATE,
    named_bet: '`392-590-125` is part of the P086 selector family',
    tier_after_test: 'wild_extension_only',
    evidence:
      'Allowing `392` makes `235-002-390/405/392` 4/4 for `125`, but `392` has only one row and no current P086 crosswalk support.',
    adversary:
      '`392` may simply be a separate low-count head with terminal `125`, not evidence for the same family.',
    falsifier_or_rescue:
      'A second `392` row with the same `590-125` tail or independent crosswalk evidence promotes it to candidate.',
  },
];

const summary = {
  checked_date: RUN_DATE,
  status: '235_p086_selector_stress',
  hypothesis_tested:
    '`235` selects `125` only in interaction with P086-family heads (`390/405`), not as a generic left-stem or generic open-head effect.',
  totals: {
    all_002_frames: frames.length,
    prev235_frames: prev235.length,
    prev235_p086_frames: prev235P086.length,
    prev235_closure_frames: prev235Closure.length,
    prev235_broad_open_nonp086_frames: prev235BroadOpenNonP086.length,
  },
  key_contrasts: contrastRows,
  minimal_contrast:
    'M-47 and M-735 share `740-760-235-002`; M-47 goes to closure head `861` and closes, while M-735 goes to `390-125-195` and continues.',
  decisions,
  confidence_after_test: {
    '235_p086_125_selector': 'candidate_strengthened_not_promoted',
    '235_generic_125_selector': 'dead',
    'open_head_generic_125_selector': 'dead',
    '392_p086_extension': 'wild_extension_only',
  },
};

writeCsv(path.join(OUT_DIR, `${PREFIX}_all_002_frames.csv`), frames, [
  'checked_date',
  'row_id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'left3_before_002',
  'head_after_002',
  'head_classifier_class',
  'branch_after_head',
  'tail_after_head',
  'full_tail_after_002',
  'terminal_after_head',
  'tail_has_125',
  'prev235',
  'p086_head_390_405',
  'p086_extension_390_405_392',
  'closure_head_817_820_861',
  'broad_open_head',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_235_frames.csv`), prev235, [
  'checked_date',
  'row_id',
  'object',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'left3_before_002',
  'head_after_002',
  'head_classifier_class',
  'branch_after_head',
  'tail_after_head',
  'full_tail_after_002',
  'terminal_after_head',
  'tail_has_125',
  'p086_head_390_405',
  'p086_extension_390_405_392',
  'closure_head_817_820_861',
  'broad_open_head',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_family_summary.csv`), familyRows, [
  'checked_date',
  'family',
  'rows',
  'has125',
  'heads',
  'objects',
  'tier_after_test',
  'implication',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_contrasts.csv`), contrastRows, [
  'checked_date',
  'contrast',
  'group_a_rows',
  'group_a_has125',
  'group_a_rate',
  'group_b_rows',
  'group_b_has125',
  'group_b_rate',
  'fisher_greater_p',
  'group_a_objects',
  'group_b_objects',
  'interpretation',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_minimal_contrasts.csv`), minimalContrastRows, [
  'checked_date',
  'object',
  'row_id',
  'left3_before_002',
  'head_after_002',
  'branch_after_head',
  'tail_after_head',
  'tail_has_125',
  'type',
  'symbol',
  'cult',
  'contrast_role',
  'text',
]);

writeCsv(path.join(OUT_DIR, `${PREFIX}_decisions.csv`), decisions, [
  'checked_date',
  'named_bet',
  'tier_after_test',
  'evidence',
  'adversary',
  'falsifier_or_rescue',
]);

fs.writeFileSync(path.join(OUT_DIR, `${PREFIX}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
