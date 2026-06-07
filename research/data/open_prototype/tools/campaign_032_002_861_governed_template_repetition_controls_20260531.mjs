import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const metadataPath = path.join(root, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(root, 'data', 'open_prototype', 'reports');
const prefix = 'campaign_032_002_861_governed_template_repetition_controls_20260531';

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

function topCounts(counts, n = 8) {
  return counts
    .slice(0, n)
    .map(([key, value]) => `${key}:${value}`)
    .join(';');
}

function uniqueCount(items, fn) {
  return new Set(items.map(fn)).size;
}

function templateVerdict(template, members) {
  const has125 = template.split('-').includes('125');
  if (members.length === 1) return has125 ? 'singleton_125_template_wild' : 'singleton_non125_background';
  const topExact = countBy(members, (row) => row.text)[0]?.[1] ?? 0;
  const topSite = countBy(members, (row) => row.site)[0]?.[1] ?? 0;
  const topPrev = countBy(members, (row) => row.prev_before_002)[0]?.[1] ?? 0;
  const crossSite = uniqueCount(members, (row) => row.site) > 1;
  if (template === '405-501-<END>-<END>') return 'copy_template_control';
  if (has125 && crossSite && topExact === 1) return 'survives_repetition_control_cross_site_125_template';
  if (has125 && topExact === 1) return 'survives_exact_text_control_same_site_125_template';
  if (has125) return '125_template_repeated_but_copy_pressure';
  if (topExact / members.length > 0.5) return 'copy_formula_pressure_control';
  if (topSite / members.length > 0.8 && topPrev / members.length > 0.8) return 'local_register_formula_control';
  return 'non125_repeated_template_background';
}

fs.mkdirSync(reportsDir, { recursive: true });

const rows = parseCsv(fs.readFileSync(metadataPath, 'utf8')).map((row) => ({
  ...row,
  tokens: signs(row.text),
}));

const governedRows = [];

for (const row of rows) {
  for (let i = 0; i < row.tokens.length; i += 1) {
    if (row.tokens[i] !== '002' || !row.tokens[i + 1]) continue;
    const template4 = [
      row.tokens[i + 1] ?? '<END>',
      row.tokens[i + 2] ?? '<END>',
      row.tokens[i + 3] ?? '<END>',
      row.tokens[i + 4] ?? '<END>',
    ].join('-');
    const phrase = row.tokens.slice(i + 1);
    governedRows.push({
      checked_date: '2026-05-31',
      cisi: row.cisi || '-',
      row_id: row.id,
      site: row.site,
      type: row.type,
      symbol: row.symbol,
      cult: row.cult,
      prev_before_002: row.tokens[i - 1] ?? '<START>',
      head_after_002: row.tokens[i + 1] ?? '<END>',
      template_4: template4,
      contains_125_in_template_4: String(template4.split('-').includes('125')),
      contains_125_anywhere_after_002: String(phrase.includes('125')),
      phrase_after_002: phrase.join('-'),
      text: row.text,
    });
  }
}

const templateFamilies = countBy(governedRows, (row) => row.template_4).map(([template, count]) => {
  const members = governedRows.filter((row) => row.template_4 === template);
  const exactTextCounts = countBy(members, (row) => row.text);
  const siteCount = uniqueCount(members, (row) => row.site);
  const typeCount = uniqueCount(members, (row) => row.type);
  const prevCount = uniqueCount(members, (row) => row.prev_before_002);
  return {
    checked_date: '2026-05-31',
    template_4: template,
    count: String(count),
    contains_125_in_template_4: String(template.split('-').includes('125')),
    contains_125_anywhere_after_002: String(members.some((row) => row.contains_125_anywhere_after_002 === 'true')),
    distinct_sites: String(siteCount),
    distinct_types: String(typeCount),
    distinct_prev_before_002: String(prevCount),
    top_exact_text_share: (exactTextCounts[0][1] / count).toFixed(6),
    top_exact_text: exactTextCounts[0][0],
    sites: topCounts(countBy(members, (row) => row.site)),
    types: topCounts(countBy(members, (row) => row.type)),
    prev_before_002: topCounts(countBy(members, (row) => row.prev_before_002)),
    cisi: topCounts(countBy(members, (row) => row.cisi)),
    verdict: templateVerdict(template, members),
    examples: members
      .slice(0, 10)
      .map((row) => `${row.cisi}:${row.text}`)
      .join(' | '),
  };
});

const repeatedTemplates = templateFamilies.filter((row) => Number(row.count) > 1);
const repeated125Templates = repeatedTemplates.filter((row) => row.contains_125_in_template_4 === 'true');
const repeatedNon125Templates = repeatedTemplates.filter((row) => row.contains_125_in_template_4 !== 'true');
const crossSiteRepeated = repeatedTemplates.filter((row) => Number(row.distinct_sites) > 1);
const crossSiteRepeated125 = repeated125Templates.filter((row) => Number(row.distinct_sites) > 1);
const exactTextDominated = repeatedTemplates.filter((row) => Number(row.top_exact_text_share) > 0.5);
const exactTextDominated125 = repeated125Templates.filter((row) => Number(row.top_exact_text_share) > 0.5);

templateFamilies.sort(
  (a, b) =>
    Number(b.count) - Number(a.count) ||
    Number(b.distinct_sites) - Number(a.distinct_sites) ||
    a.template_4.localeCompare(b.template_4, undefined, { numeric: true }),
);

const summary = {
  checked_date: '2026-05-31',
  status: 'governed_template_repetition_controls',
  hypothesis_tested:
    'Repeated governed `125` templates should survive better than ordinary repeated `002-H-tail` copy/register templates.',
  key_counts: {
    governed_002_occurrences: governedRows.length,
    distinct_template_4: templateFamilies.length,
    repeated_template_4_families: repeatedTemplates.length,
    repeated_125_template_4_families: repeated125Templates.length,
    repeated_non125_template_4_families: repeatedNon125Templates.length,
    cross_site_repeated_template_4_families: crossSiteRepeated.length,
    cross_site_repeated_125_template_4_families: crossSiteRepeated125.length,
    exact_text_dominated_repeated_template_4_families: exactTextDominated.length,
    exact_text_dominated_repeated_125_template_4_families: exactTextDominated125.length,
    repeated_125_templates: repeated125Templates.map((row) => `${row.template_4}:${row.count}`).join(';'),
    top_repeated_templates: repeatedTemplates.slice(0, 12).map((row) => `${row.template_4}:${row.count}`).join(';'),
  },
  decisions: [
    'The naive argument "repetition means grammar" is killed: many non-125 templates repeat, and some are obvious copy/register controls.',
    'The broader 125 grammar survives as a candidate, not accepted: repeated 125 templates are a tiny subset of all repeats but are not exact-text dominated.',
    'Cross-site repeated 125 templates remain the best risky signal: 610-125-032 and 297-350-125-413.',
    '390-125-632-032 remains useful but same-site only, so it is weaker than the cross-site templates.',
  ],
  next_falsifier:
    'Source/plate or family-collapse work should attack the cross-site 610-125-032 and 297-350-125-413 rows. If they collapse as copies or non-comparable contexts, demote broader 125 grammar.',
};

writeCsv(path.join(reportsDir, `${prefix}_governed_rows.csv`), governedRows, [
  'checked_date',
  'cisi',
  'row_id',
  'site',
  'type',
  'symbol',
  'cult',
  'prev_before_002',
  'head_after_002',
  'template_4',
  'contains_125_in_template_4',
  'contains_125_anywhere_after_002',
  'phrase_after_002',
  'text',
]);

writeCsv(path.join(reportsDir, `${prefix}_template_families.csv`), templateFamilies, [
  'checked_date',
  'template_4',
  'count',
  'contains_125_in_template_4',
  'contains_125_anywhere_after_002',
  'distinct_sites',
  'distinct_types',
  'distinct_prev_before_002',
  'top_exact_text_share',
  'top_exact_text',
  'sites',
  'types',
  'prev_before_002',
  'cisi',
  'verdict',
  'examples',
]);

fs.writeFileSync(path.join(reportsDir, `${prefix}_summary.json`), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(JSON.stringify(summary, null, 2));
