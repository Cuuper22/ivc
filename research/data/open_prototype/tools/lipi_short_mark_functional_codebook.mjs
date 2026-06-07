import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const validationPath = path.join(reportsDir, 'lipi_multiside_mark_validation_queue.csv');

const artifactLabelsPath = path.join(reportsDir, 'lipi_short_mark_functional_codebook_artifacts.csv');
const rulesPath = path.join(reportsDir, 'lipi_short_mark_functional_codebook_rules.csv');
const predictionsPath = path.join(reportsDir, 'lipi_short_mark_functional_codebook_predictions.csv');
const summaryPath = path.join(reportsDir, 'lipi_short_mark_functional_codebook_summary.json');

const hSeries = new Set(Array.from({ length: 22 }, (_, index) => `H-${2218 + index}`));
const smoothing = 0.5;

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function toCsv(rows) {
  return `${rows
    .map((row) =>
      row
        .map((value) => {
          const text = String(value ?? '');
          return `"${text.replaceAll('"', '""')}"`;
        })
        .join(','),
    )
    .join('\n')}\n`;
}

function norm(value) {
  return String(value ?? '').trim();
}

function formatNumber(value, digits = 6) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(digits));
}

function tokens(text) {
  return norm(text).match(/\d{3}/g) ?? [];
}

function parseSideTexts(text) {
  const raw = norm(text);
  if (!raw) return [];
  return raw
    .split('|')
    .map((part) => {
      const match = part.match(/^([^:]+):(.+)$/);
      if (!match) return { side: '', text: part, tokens: tokens(part) };
      return { side: match[1], text: match[2], tokens: tokens(match[2]) };
    })
    .filter((row) => row.tokens.length);
}

function labelForSide(sideTokens) {
  const has = (token) => sideTokens.includes(token);
  if (has('700') && has('032')) return 'FRAME700_SUBTYPE032';
  if (has('700') && has('033')) return 'FRAME700_SUBTYPE033';
  if (has('700') && has('034')) return 'FRAME700_SUBTYPE034';
  if (has('861') && has('003')) return 'FRAME003_ROLE861';
  if ((has('156') || has('154')) && has('003')) return 'FRAME003_ROLE15X';
  if (has('156') && has('176')) return 'PAIR156_176';
  if (sideTokens.length === 2) return `EXACT_${sideTokens.join('_')}`;
  return `OTHER_${sideTokens.join('_')}`;
}

function add(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function setKey(values) {
  return [...values].sort((a, b) => a.localeCompare(b)).join(';');
}

function rankCandidates(candidates, target, score) {
  const ranked = candidates
    .map((candidate) => ({ candidate, score: score(candidate) }))
    .sort((a, b) => b.score - a.score || a.candidate.localeCompare(b.candidate));
  const idx = ranked.findIndex((row) => row.candidate === target);
  const rank = idx >= 0 ? idx + 1 : ranked.length + 1;
  return {
    rank,
    predicted_top1: ranked[0]?.candidate ?? '',
    top1: rank === 1,
    top3: rank <= 3,
  };
}

function countLabels(artifacts) {
  const counts = new Map();
  for (const artifact of artifacts) {
    for (const label of artifact.labels) add(counts, label);
  }
  return counts;
}

function buildCoCounts(artifacts) {
  const counts = new Map();
  const co = new Map();
  for (const artifact of artifacts) {
    for (const a of artifact.labels) {
      add(counts, a);
      for (const b of artifact.labels) {
        if (a !== b) add(co, `${a}\t${b}`);
      }
    }
  }
  return { counts, co };
}

function predictRows(artifacts, scope) {
  const out = [];
  const evaluable = artifacts.filter((artifact) => artifact.labels.length >= 2);
  for (const artifact of evaluable) {
    for (const target of artifact.labels) {
      const observed = artifact.labels.filter((label) => label !== target);
      if (!observed.length) continue;
      const train = artifacts.filter((row) => row.cisi !== artifact.cisi);
      const candidates = [...new Set(train.flatMap((row) => row.labels))].sort((a, b) => a.localeCompare(b));
      const globalCounts = countLabels(train);
      const blockTrain = train.filter(
        (row) =>
          row.type === artifact.type &&
          row.site === artifact.site &&
          row.sides === artifact.sides,
      );
      const blockCounts = countLabels(blockTrain.length ? blockTrain : train);
      const { counts, co } = buildCoCounts(train);

      const models = {
        frequency: (candidate) => globalCounts.get(candidate) ?? 0,
        type_site_sides: (candidate) => blockCounts.get(candidate) ?? 0,
        observed_role_context: (candidate) => {
          let total = Math.log(((globalCounts.get(candidate) ?? 0) + smoothing) / (train.length + smoothing * candidates.length));
          for (const obs of observed) {
            total += Math.log(((co.get(`${obs}\t${candidate}`) ?? 0) + smoothing) / ((counts.get(obs) ?? 0) + smoothing * candidates.length));
          }
          return total;
        },
      };
      for (const [model, scorer] of Object.entries(models)) {
        const rank = rankCandidates(candidates, target, scorer);
        out.push({
          scope,
          cisi: artifact.cisi,
          type: artifact.type,
          site: artifact.site,
          sides: artifact.sides,
          target,
          observed: observed.join(';'),
          model,
          rank: rank.rank,
          predicted_top1: rank.predicted_top1,
          top1: rank.top1,
          top3: rank.top3,
        });
      }
    }
  }
  return out;
}

function summarizePredictions(rows) {
  const groups = new Map();
  for (const row of rows) {
    const key = `${row.scope}\t${row.model}`;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return [...groups.entries()].map(([key, group]) => {
    const [scope, model] = key.split('\t');
    return {
      scope,
      model,
      predictions: group.length,
      top1: group.filter((row) => row.top1).length,
      top1_accuracy: formatNumber(group.filter((row) => row.top1).length / group.length),
      top3: group.filter((row) => row.top3).length,
      top3_accuracy: formatNumber(group.filter((row) => row.top3).length / group.length),
      median_rank: formatNumber(
        group
          .map((row) => Number(row.rank))
          .sort((a, b) => a - b)[Math.floor((group.length - 1) / 2)],
      ),
    };
  });
}

const rawRows = parseCsv(fs.readFileSync(validationPath, 'utf8'));
const header = rawRows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const artifacts = rawRows.slice(1).map((row) => {
  const sideRows = parseSideTexts(row[column.short_side_texts]);
  const labels = [...new Set(sideRows.map((side) => labelForSide(side.tokens)))].sort((a, b) => a.localeCompare(b));
  const exactSides = sideRows.map((side) => side.text).sort((a, b) => a.localeCompare(b));
  return {
    cisi: row[column.cisi],
    priority: row[column.priority],
    type: row[column.type],
    site: row[column.site],
    sides: row[column.sides],
    horizontal_mm: row[column.horizontal_mm],
    vertical_mm: row[column.vertical_mm],
    thickness_mm: row[column.thickness_mm],
    labels,
    exactSides,
    short_side_texts: row[column.short_side_texts],
    long_side_texts: row[column.long_side_texts],
  };
});

const labelCounts = countLabels(artifacts);
const { counts: antecedentCounts, co } = buildCoCounts(artifacts);
const rules = [];
for (const [key, count] of co.entries()) {
  const [antecedent, consequent] = key.split('\t');
  if (count < 3) continue;
  const consequentCount = labelCounts.get(consequent) ?? 0;
  rules.push({
    antecedent,
    consequent,
    cooccur_artifacts: count,
    antecedent_artifacts: antecedentCounts.get(antecedent) ?? 0,
    consequent_artifacts: consequentCount,
    confidence: count / (antecedentCounts.get(antecedent) ?? 1),
    lift: count / (antecedentCounts.get(antecedent) ?? 1) / (consequentCount / artifacts.length),
  });
}
rules.sort((a, b) => b.lift - a.lift || b.cooccur_artifacts - a.cooccur_artifacts || a.antecedent.localeCompare(b.antecedent));

const predictionRows = [
  ...predictRows(artifacts, 'all_validation_queue'),
  ...predictRows(artifacts.filter((row) => !hSeries.has(row.cisi)), 'excluding_h2218_h2239'),
];
const predictionSummary = summarizePredictions(predictionRows);

fs.writeFileSync(
  artifactLabelsPath,
  toCsv([
    [
      'cisi',
      'priority',
      'type',
      'site',
      'sides',
      'horizontal_mm',
      'vertical_mm',
      'thickness_mm',
      'functional_labels',
      'exact_short_sides',
      'short_side_texts',
      'long_side_texts',
    ],
    ...artifacts.map((row) => [
      row.cisi,
      row.priority,
      row.type,
      row.site,
      row.sides,
      row.horizontal_mm,
      row.vertical_mm,
      row.thickness_mm,
      row.labels.join(';'),
      row.exactSides.join(';'),
      row.short_side_texts,
      row.long_side_texts,
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  rulesPath,
  toCsv([
    ['antecedent', 'consequent', 'cooccur_artifacts', 'antecedent_artifacts', 'consequent_artifacts', 'confidence', 'lift'],
    ...rules.map((row) => [
      row.antecedent,
      row.consequent,
      row.cooccur_artifacts,
      row.antecedent_artifacts,
      row.consequent_artifacts,
      formatNumber(row.confidence),
      formatNumber(row.lift),
    ]),
  ]),
  'utf8',
);

fs.writeFileSync(
  predictionsPath,
  toCsv([
    ['scope', 'cisi', 'type', 'site', 'sides', 'target', 'observed', 'model', 'rank', 'predicted_top1', 'top1', 'top3'],
    ...predictionRows.map((row) => [
      row.scope,
      row.cisi,
      row.type,
      row.site,
      row.sides,
      row.target,
      row.observed,
      row.model,
      row.rank,
      row.predicted_top1,
      row.top1,
      row.top3,
    ]),
  ]),
  'utf8',
);

const summary = {
  generated_at_local: new Date().toISOString(),
  experiment: 'Lipi short-mark functional codebook attempt',
  input: 'data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv',
  validation_queue_artifacts: artifacts.length,
  artifacts_with_two_or_more_functional_labels: artifacts.filter((row) => row.labels.length >= 2).length,
  unique_functional_labels: [...labelCounts.keys()].sort((a, b) => a.localeCompare(b)),
  label_counts: Object.fromEntries([...labelCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))),
  top_rules: rules.slice(0, 20).map((row) => ({
    antecedent: row.antecedent,
    consequent: row.consequent,
    cooccur_artifacts: row.cooccur_artifacts,
    confidence: formatNumber(row.confidence),
    lift: formatNumber(row.lift),
  })),
  prediction_summary: predictionSummary,
  current_read:
    'The codebook model can test whether side-role labels predict other side-role labels, but any success is functional-grammar evidence only, not phonetic or prose translation.',
  interpretation_boundary:
    'Functional codebook attempt only. Labels such as FRAME700_SUBTYPE034 are analyst labels over sign co-occurrence; they are not accepted sign meanings, numerical values, phonetic readings, language identity, or translation.',
  outputs: [
    'data/open_prototype/reports/lipi_short_mark_functional_codebook_artifacts.csv',
    'data/open_prototype/reports/lipi_short_mark_functional_codebook_rules.csv',
    'data/open_prototype/reports/lipi_short_mark_functional_codebook_predictions.csv',
    'data/open_prototype/reports/lipi_short_mark_functional_codebook_summary.json',
  ],
};

fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
