import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_governed_125_template_families_20260531';

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

function countBy(items, fn) {
  const counts = new Map();
  for (const item of items) {
    const key = fn(item) || '-';
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return [...counts.entries()].sort(
    (a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), undefined, { numeric: true }),
  );
}

function topCounts(counts, n = 10) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function findGovernedHead(tokens, signIndex) {
  for (let headIndex = signIndex - 1; headIndex >= 0 && headIndex >= signIndex - 4; headIndex -= 1) {
    if (tokens[headIndex - 1] === '002') {
      return {
        governed: true,
        headIndex,
        head: tokens[headIndex],
        prevBefore002: tokens[headIndex - 2] ?? '<START>',
      };
    }
  }
  return { governed: false, headIndex: -1, head: '', prevBefore002: '' };
}

function templateClass(row) {
  if (row.template_4 === '390-125-632-032') return 'title_tail_390_125_632_032';
  if (row.template_4 === '190-125-632-032') return 'title_tail_190_125_632_032';
  if (row.template_4 === '610-125-032-<END>') return 'repeated_610_125_032_title_template';
  if (row.template_4 === '297-350-125-413') return 'repeated_297_350_125_413_title_template';
  if (['390-125-820-<END>', '405-125-820-<END>'].includes(row.template_4)) {
    return 'p086_125_820_title_template';
  }
  if (row.template_4.includes('-125-')) return 'governed_125_template_singleton';
  return 'background';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const governed125Rows = [];
for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '125') continue;
    const governed = findGovernedHead(row.tokens, i);
    if (!governed.governed) continue;
    const phrase = row.tokens.slice(governed.headIndex);
    const template4 = [
      row.tokens[i - 2] ?? '<START>',
      row.tokens[i - 1] ?? '<START>',
      row.tokens[i],
      row.tokens[i + 1] ?? '<END>',
    ].join('-');
    const headToTail4 = [
      row.tokens[governed.headIndex] ?? '<START>',
      row.tokens[governed.headIndex + 1] ?? '<END>',
      row.tokens[governed.headIndex + 2] ?? '<END>',
      row.tokens[governed.headIndex + 3] ?? '<END>',
    ].join('-');
    governed125Rows.push({
      checked_date: '2026-05-31',
      cisi: row.cisi || '-',
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      prev_before_002: governed.prevBefore002,
      governed_head: governed.head,
      phrase_from_head: phrase.join('-'),
      template_4: headToTail4,
      local_around_125: template4,
      next_after_125: row.tokens[i + 1] ?? '<END>',
      next2_after_125: row.tokens[i + 2] ?? '<END>',
      template_class: '',
      text: row.text,
    });
  }
}

for (const row of governed125Rows) {
  row.template_class = templateClass(row);
}

const families = countBy(governed125Rows, (row) => row.template_4).map(([template, count]) => {
  const members = governed125Rows.filter((row) => row.template_4 === template);
  return {
    checked_date: '2026-05-31',
    template_4: template,
    count: String(count),
    sites: topCounts(countBy(members, (row) => row.site)),
    types: topCounts(countBy(members, (row) => row.type)),
    governed_heads: topCounts(countBy(members, (row) => row.governed_head)),
    prev_before_002: topCounts(countBy(members, (row) => row.prev_before_002)),
    template_class: templateClass(members[0]),
    examples: members.map((row) => `${row.cisi}:${row.text}`).join(' | '),
  };
});

const repeatedFamilies = families.filter((row) => Number(row.count) > 1);
const promotedFamilies = families.filter((row) =>
  ['390-125-632-032', '610-125-032-<END>', '297-350-125-413'].includes(row.template_4),
);

const summary = {
  checked_date: '2026-05-31',
  status: 'governed_125_template_family_probe',
  hypothesis_tested:
    '`002-H-(modifier)-125-tail` is a governed title-template grammar, not isolated `002-390-125` behavior.',
  key_counts: {
    governed_125_rows: governed125Rows.length,
    distinct_template_4: families.length,
    repeated_template_4_families: repeatedFamilies.length,
    repeated_families: repeatedFamilies.map((row) => `${row.template_4}:${row.count}`).join(';'),
    promoted_template_candidates: promotedFamilies.map((row) => `${row.template_4}:${row.count}`).join(';'),
    governed_heads: topCounts(countBy(governed125Rows, (row) => row.governed_head)),
    next_after_125: topCounts(countBy(governed125Rows, (row) => row.next_after_125)),
  },
  decisions: [
    '`125` is promoted from a mostly 390-tail story to a broader governed title-template candidate.',
    '`610-125-032` is a candidate repeated title template across Harappa and Mohenjo-daro.',
    '`297-350-125-413` is a candidate repeated title template across Bala-kot and Nausharo.',
    '`190` stays a wild sibling-head extension: it shares `125-632-032`, but only one `190` row has that tail.',
  ],
  next_falsifier:
    'If repeated governed 125 templates collapse to duplicate/copy families or if held-out governed 125 rows do not preserve head-template structure, demote the broader grammar.',
};

writeCsv(path.join(reportsDir, `${prefix}_governed_125_rows.csv`), governed125Rows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'governed_head',
  'phrase_from_head',
  'template_4',
  'local_around_125',
  'next_after_125',
  'next2_after_125',
  'template_class',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_template_families.csv`), families, [
  'checked_date',
  'template_4',
  'count',
  'sites',
  'types',
  'governed_heads',
  'prev_before_002',
  'template_class',
  'examples',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
