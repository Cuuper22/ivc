import fs from 'node:fs';
import path from 'node:path';

// Version 1 of a deliberately risky parse model for the Indus 002-390 construction, tested
// against the whole corpus at once. It reads data/open_prototype/lipi/metadata_filtered.csv
// and probes four hypotheses: 002 opens a dependency frame; 390 is an open class head under
// 002 (measured by the entropy of what follows each head); the stem 235-002 with a
// 390/405-family head selects a later 125; and unbound row 3335.1 embeds the 390-590-032
// formula bridge. The 235 test is run adversarially: the broad "any open head" version dies
// on 031/220/374/906 counterexamples, shrinking the survivor to the narrow 390/405 family,
// with an explicit warning that the family was named post hoc. Each 002-390 row also gets a
// provisional parse label (rank/title selector for 125, closure for 095, and so on) at
// candidate or wild-shot confidence. Writes head and 390-pair summaries, row parses, the
// 235 selector test, and bridge rows as CSVs plus a summary JSON in reports/.

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_002390x_risky_parse_model_v1_20260531';

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

function entropy(counts) {
  const total = Object.values(counts).reduce((sum, value) => sum + value, 0);
  return Object.values(counts).reduce((sum, value) => {
    const p = value / total;
    return sum - p * Math.log2(p);
  }, 0);
}

function topCounts(counts, n = 8) {
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], undefined, { numeric: true }))
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8'));

const after002 = new Map();
const pair390 = new Map();
const occurrences002390 = [];
const stem235Rows = [];
const formula390590032 = [];

for (const row of rows) {
  const tokens = signs(row.text);
  for (let i = 0; i < tokens.length; i += 1) {
    if (tokens[i] === '002' && tokens[i + 1]) {
      const head = tokens[i + 1];
      const next = tokens[i + 2] ?? '<END>';
      if (!after002.has(head)) {
        after002.set(head, { n: 0, next: {}, terminal: 0, examples: [] });
      }
      const bucket = after002.get(head);
      bucket.n += 1;
      bucket.next[next] = (bucket.next[next] ?? 0) + 1;
      if (next === '<END>') bucket.terminal += 1;
      if (bucket.examples.length < 6) bucket.examples.push(`${row.cisi || '-'}:${row.text}`);

      if (tokens[i - 1] === '235') {
        const tail = tokens.slice(i + 1);
        const p086HeadFamily = ['390', '405'].includes(head);
        const branchHeadFamily = p086HeadFamily || head === '392';
        const closureHead = ['817', '820', '861'].includes(head);
        stem235Rows.push({
          checked_date: '2026-05-31',
          cisi: row.cisi || '-',
          row_id: row.id,
          site: row.site,
          type: row.type,
          symbol: row.symbol,
          cult: row.cult,
          head_after_002: head,
          next_after_head: next,
          tail_after_002: tail.join('-'),
          tail_has_125: String(tail.includes('125')),
          branch_head_family_390_405_392: String(branchHeadFamily),
          p086_head_family_390_405: String(p086HeadFamily),
          closure_head_817_820_861: String(closureHead),
          model_implication: branchHeadFamily
            ? 'tests_235_selects_125_under_open_branch_head'
            : closureHead
              ? 'tests_closure_heads_do_not_select_125'
              : 'background_235_002_head',
          text: row.text,
        });
      }

      if (head === '390') {
        occurrences002390.push({
          checked_date: '2026-05-31',
          cisi: row.cisi || '-',
          row_id: row.id,
          site: row.site,
          type: row.type,
          symbol: row.symbol,
          cult: row.cult,
          prev_before_002: tokens[i - 1] ?? '<START>',
          x_slot: next,
          tail_after_390: tokens.slice(i + 2).join('-') || '<END>',
          provisional_parse: next === '125'
            ? 'rank_or_title_selector'
            : next === '095'
              ? 'administrative_closure_selector'
              : next === '705'
                ? 'remote_or_transfer_selector'
                : next === '590'
                  ? 'formula_bridge_selector'
                  : 'singleton_or_unclassified_selector',
          confidence: next === '125' || next === '590' ? 'candidate' : 'wild_shot',
          text: row.text,
        });
      }
    }

    if (tokens[i] === '390' && tokens[i + 1]) {
      const x = tokens[i + 1];
      if (!pair390.has(x)) pair390.set(x, { n: 0, after002: 0, terminal: 0, examples: [] });
      const bucket = pair390.get(x);
      bucket.n += 1;
      if (tokens[i - 1] === '002') bucket.after002 += 1;
      if (i + 1 === tokens.length - 1) bucket.terminal += 1;
      if (bucket.examples.length < 4) bucket.examples.push(`${row.cisi || '-'}:${row.text}`);
    }

    if (tokens[i] === '390' && tokens[i + 1] === '590' && tokens[i + 2] === '032') {
      formula390590032.push({
        checked_date: '2026-05-31',
        cisi: row.cisi || '-',
        row_id: row.id,
        site: row.site,
        type: row.type,
        symbol: row.symbol,
        cult: row.cult,
        prev_before_390: tokens[i - 1] ?? '<START>',
        next_after_032: tokens[i + 3] ?? '<END>',
        after_002: String(tokens[i - 1] === '002'),
        model_implication:
          tokens[i - 1] === '002'
            ? '3335_candidate_embeds_390_590_032_after_002'
            : 'analogue_for_formula_bridge',
        text: row.text,
      });
    }
  }
}

const headSummary = [...after002.entries()]
  .sort((a, b) => b[1].n - a[1].n || a[0].localeCompare(b[0], undefined, { numeric: true }))
  .map(([head, bucket]) => ({
    checked_date: '2026-05-31',
    head_after_002: head,
    frame_count: String(bucket.n),
    terminal_count: String(bucket.terminal),
    terminal_share: (bucket.terminal / bucket.n).toFixed(6),
    next_entropy_bits: entropy(bucket.next).toFixed(6),
    top_next: topCounts(bucket.next),
    examples: bucket.examples.join(' | '),
  }));

const pairSummary = [...pair390.entries()]
  .sort((a, b) => b[1].n - a[1].n || a[0].localeCompare(b[0], undefined, { numeric: true }))
  .map(([x, bucket]) => ({
    checked_date: '2026-05-31',
    sign_after_390: x,
    global_390_x_count: String(bucket.n),
    after_002_count: String(bucket.after002),
    terminal_count: String(bucket.terminal),
    after_002_share: (bucket.after002 / bucket.n).toFixed(6),
    terminal_share: (bucket.terminal / bucket.n).toFixed(6),
    examples: bucket.examples.join(' | '),
  }));

const branchFamily = stem235Rows.filter((row) => row.branch_head_family_390_405_392 === 'true');
const p086Family = stem235Rows.filter((row) => row.p086_head_family_390_405 === 'true');
const nonBranchFamily = stem235Rows.filter((row) => row.branch_head_family_390_405_392 !== 'true');
const closureFamily = stem235Rows.filter((row) => row.closure_head_817_820_861 === 'true');
const broadOpenHead = stem235Rows.filter((row) => {
  const head = after002.get(row.head_after_002);
  if (!head || head.n < 3) return false;
  return head.terminal / head.n < 0.5 && entropy(head.next) > 1;
});

const summary = {
  checked_date: '2026-05-31',
  status: 'risky_parse_model_v1_tests',
  hypotheses_tested: [
    '002 as dependency opener',
    '390 as open class head under 002',
    '235-002 branch-head family selects 125',
    '3335.1 as governed 390-590-032 bridge',
  ],
  after_002_head_390: headSummary.find((row) => row.head_after_002 === '390'),
  after_002_head_405: headSummary.find((row) => row.head_after_002 === '405'),
  stem235_test: {
    cases: stem235Rows.length,
    p086_family_390_405_cases: p086Family.length,
    p086_family_390_405_tail_has_125: p086Family.filter((row) => row.tail_has_125 === 'true').length,
    branch_family_390_405_392_cases: branchFamily.length,
    branch_family_tail_has_125: branchFamily.filter((row) => row.tail_has_125 === 'true').length,
    broad_open_head_cases: broadOpenHead.length,
    broad_open_head_tail_has_125: broadOpenHead.filter((row) => row.tail_has_125 === 'true').length,
    non_branch_family_cases: nonBranchFamily.length,
    non_branch_family_tail_has_125: nonBranchFamily.filter((row) => row.tail_has_125 === 'true').length,
    closure_family_cases: closureFamily.length,
    closure_family_tail_has_125: closureFamily.filter((row) => row.tail_has_125 === 'true').length,
    adversarial_shrink:
      'The broad open-head version fails; 031/220/374/906 cases do not carry 125. The surviving promoted candidate is narrower: 235-002 plus 390/405 P086-family head selects 125. The 392 case is retained only as a wild extension.',
    posthoc_warning: 'The 390/405 family was named from the live object and Mayig P086 pressure; treat as candidate-generating, not a confirmatory p-value.',
  },
  formula_bridge_390_590_032_rows: formula390590032.length,
  formula_bridge_after_002_rows: formula390590032.filter((row) => row.after_002 === 'true').length,
  formula_bridge_before_002_rows: formula390590032.filter((row) => row.next_after_032 === '002').length,
  confidence_changes: [
    '002 dependency opener: candidate',
    '390 open class head under 002: candidate',
    '235-002 plus 390/405 P086-family head selecting 125: promoted candidate after local null/source-pair stress',
    '235-002 broad open-head selecting 125: killed by 031/220/374/906 counterexamples',
    '392-590-125 as related extension: wild shot only',
    '125 as rank/title selector: candidate semantic interpretation of the promoted selector rule',
    '095 administrative closure: wild shot',
    '705 remote/transfer selector: wild shot',
    '3335.1 390-590-032 bridge: candidate if row source-binds as transcribed',
  ],
};

writeCsv(path.join(reportsDir, `${prefix}_after002_head_summary.csv`), headSummary, [
  'checked_date',
  'head_after_002',
  'frame_count',
  'terminal_count',
  'terminal_share',
  'next_entropy_bits',
  'top_next',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_390_x_summary.csv`), pairSummary, [
  'checked_date',
  'sign_after_390',
  'global_390_x_count',
  'after_002_count',
  'terminal_count',
  'after_002_share',
  'terminal_share',
  'examples',
]);

writeCsv(path.join(reportsDir, `${prefix}_002390_row_parses.csv`), occurrences002390, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'x_slot',
  'tail_after_390',
  'provisional_parse',
  'confidence',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_235002_selector_test.csv`), stem235Rows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'head_after_002',
  'next_after_head',
  'tail_after_002',
  'tail_has_125',
  'branch_head_family_390_405_392',
  'p086_head_family_390_405',
  'closure_head_817_820_861',
  'model_implication',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_390590032_bridge_rows.csv`), formula390590032, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_390',
  'next_after_032',
  'after_002',
  'model_implication',
  'text',
]);

fs.writeFileSync(
  path.join(reportsDir, `${prefix}_summary.json`),
  `${JSON.stringify(summary, null, 2)}\n`,
  'utf8',
);

console.log(JSON.stringify(summary, null, 2));
