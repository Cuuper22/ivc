import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const sourcePath = path.join(reportsDir, 'lipi_scope_rows.csv');
const edgeSummaryPath = path.join(reportsDir, 'lipi_edge_removed_summary.json');
const outInventory = path.join(reportsDir, 'lipi_class_robustness_inventory.csv');
const outResults = path.join(reportsDir, 'lipi_class_robustness_results.csv');
const outJson = path.join(reportsDir, 'lipi_class_robustness_summary.json');

const minStratumRows = 90;
const minLabelRows = 12;
const alpha = 1;

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

function parseTokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function bump(map, key, by = 1) {
  map.set(key, (map.get(key) ?? 0) + by);
}

function addNested(map, keyA, keyB, by = 1) {
  if (!map.has(keyA)) map.set(keyA, new Map());
  bump(map.get(keyA), keyB, by);
}

function formatNumber(value) {
  return value === null || value === undefined || Number.isNaN(value) ? null : Number(value.toFixed(6));
}

function exactFamilies(records, policy) {
  const seen = new Map();
  for (const record of records) {
    const key = record.tokens.join(' ');
    if (!seen.has(key)) {
      seen.set(key, {
        ...record,
        policy,
        duplicate_weight: 0,
        source_records: [],
        family_size: 1,
      });
    }
    const family = seen.get(key);
    family.duplicate_weight++;
    family.source_records.push(...(record.source_records ?? [record]));
  }
  return [...seen.values()].sort((a, b) => String(a.id).localeCompare(String(b.id)));
}

function majorityLabel(family, target) {
  const counts = new Map();
  for (const record of family.source_records ?? [family]) {
    const label = String(record[target] ?? '').trim();
    if (!label || label === '-' || label === 'None' || label === '??') continue;
    bump(counts, label);
  }
  if (!counts.size) return null;
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
}

function edgeFrameKey(tokens) {
  if (tokens.length <= 2) return `exact:${tokens.join(' ')}`;
  return `edge:${tokens.length}:${tokens[0]}:${tokens[tokens.length - 1]}`;
}

function collapseByKey(families, keyFn, policy) {
  const groups = new Map();
  for (const family of families) {
    const key = keyFn(family.tokens);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(family);
  }
  return collapseFamilyGroups(groups, policy);
}

class UnionFind {
  constructor(size) {
    this.parent = Array.from({ length: size }, (_, index) => index);
    this.rank = Array(size).fill(0);
  }

  find(index) {
    if (this.parent[index] !== index) this.parent[index] = this.find(this.parent[index]);
    return this.parent[index];
  }

  union(a, b) {
    const rootA = this.find(a);
    const rootB = this.find(b);
    if (rootA === rootB) return;
    if (this.rank[rootA] < this.rank[rootB]) this.parent[rootA] = rootB;
    else if (this.rank[rootA] > this.rank[rootB]) this.parent[rootB] = rootA;
    else {
      this.parent[rootB] = rootA;
      this.rank[rootA]++;
    }
  }
}

function oneEditFamilyCollapse(families, policy) {
  const uf = new UnionFind(families.length);
  const substitutionFrames = new Map();
  const deletionFrames = new Map();
  for (let i = 0; i < families.length; i++) {
    const tokens = families[i].tokens;
    for (let pos = 0; pos < tokens.length; pos++) {
      const substitutionKey = `sub:${tokens.length}:${pos}:${tokens
        .map((token, index) => (index === pos ? '*' : token))
        .join(' ')}`;
      if (substitutionFrames.has(substitutionKey)) uf.union(i, substitutionFrames.get(substitutionKey));
      else substitutionFrames.set(substitutionKey, i);

      const deleted = tokens.slice(0, pos).concat(tokens.slice(pos + 1));
      const deletionKey = `del:${deleted.length}:${deleted.join(' ')}`;
      if (deletionFrames.has(deletionKey)) uf.union(i, deletionFrames.get(deletionKey));
      else deletionFrames.set(deletionKey, i);
    }
  }

  const groups = new Map();
  for (let i = 0; i < families.length; i++) {
    const root = uf.find(i);
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push(families[i]);
  }
  return collapseFamilyGroups(groups, policy);
}

function collapseFamilyGroups(groups, policy) {
  const out = [];
  let index = 0;
  for (const [key, members] of groups.entries()) {
    index++;
    const sorted = members.slice().sort((a, b) => {
      const weightDiff = (b.duplicate_weight ?? 1) - (a.duplicate_weight ?? 1);
      return weightDiff || String(a.id).localeCompare(String(b.id));
    });
    const representative = sorted[0];
    out.push({
      ...representative,
      policy,
      family_key: String(key),
      family_index: index,
      family_size: members.length,
      family_source_weight: members.reduce((sum, member) => sum + (member.duplicate_weight ?? 1), 0),
      source_records: members.flatMap((member) => member.source_records ?? [member]),
    });
  }
  return out.sort((a, b) => String(a.id).localeCompare(String(b.id)));
}

function transformRecords(records, removedSigns, policy) {
  const remove = new Set(removedSigns);
  return records
    .map((record) => ({
      ...record,
      tokens: record.tokens.filter((token) => !remove.has(token)),
      transform_policy: policy,
      source_records: record.source_records ?? [record],
    }))
    .filter((record) => record.tokens.length > 0);
}

function buildPolicyFamilies(records, policy, topEdgeSigns) {
  const transformed =
    policy.transform === 'remove_top_10_edge_signs'
      ? transformRecords(records, topEdgeSigns, policy.transform)
      : records.map((record) => ({ ...record, source_records: record.source_records ?? [record], transform_policy: policy.transform }));
  const exact = exactFamilies(transformed, `${policy.name}_exact_source`);
  if (policy.family === 'exact_sequence') return exact.map((family) => ({ ...family, policy: policy.name }));
  if (policy.family === 'edge_frame') return collapseByKey(exact, edgeFrameKey, policy.name);
  if (policy.family === 'one_edit_neighborhood') return oneEditFamilyCollapse(exact, policy.name);
  throw new Error(`Unknown family policy ${policy.family}`);
}

function subtractLabelCount(counts, label) {
  const out = new Map(counts);
  const next = (out.get(label) ?? 0) - 1;
  if (next <= 0) out.delete(label);
  else out.set(label, next);
  return out;
}

function bestLabel(counts, labels, fallbackCounts) {
  const source = counts && counts.size ? counts : fallbackCounts;
  let best = null;
  let bestValue = -Infinity;
  for (const label of labels) {
    const value = source.get(label) ?? 0;
    if (value > bestValue || (value === bestValue && label.localeCompare(best) < 0)) {
      best = label;
      bestValue = value;
    }
  }
  return best;
}

function addConfusion(confusion, actual, predicted) {
  if (!confusion.has(actual)) confusion.set(actual, { tp: 0, fp: 0, fn: 0 });
  if (!confusion.has(predicted)) confusion.set(predicted, { tp: 0, fp: 0, fn: 0 });
  if (actual === predicted) confusion.get(actual).tp++;
  else {
    confusion.get(actual).fn++;
    confusion.get(predicted).fp++;
  }
}

function macroScores(confusion, labels) {
  const f1s = [];
  const recalls = [];
  for (const label of labels) {
    const row = confusion.get(label) ?? { tp: 0, fp: 0, fn: 0 };
    const precision = row.tp + row.fp > 0 ? row.tp / (row.tp + row.fp) : 0;
    const recall = row.tp + row.fn > 0 ? row.tp / (row.tp + row.fn) : 0;
    const f1 = precision + recall > 0 ? (2 * precision * recall) / (precision + recall) : 0;
    f1s.push(f1);
    recalls.push(recall);
  }
  return {
    macro_f1: f1s.length ? formatNumber(f1s.reduce((sum, value) => sum + value, 0) / f1s.length) : null,
    macro_recall: recalls.length ? formatNumber(recalls.reduce((sum, value) => sum + value, 0) / recalls.length) : null,
  };
}

function stratumLabel(family, stratumKind) {
  if (stratumKind === 'overall') return 'all';
  if (stratumKind === 'type') return majorityLabel(family, 'type');
  if (stratumKind === 'site') return majorityLabel(family, 'site');
  if (stratumKind === 'type_site') {
    const type = majorityLabel(family, 'type');
    const site = majorityLabel(family, 'site');
    return type && site ? `${type}@${site}` : null;
  }
  throw new Error(`Unknown stratum kind: ${stratumKind}`);
}

function prepareRows(families, stratum) {
  const rows = families
    .map((family) => ({
      ...family,
      label: majorityLabel(family, 'class'),
      stratum: stratumLabel(family, stratum.stratum_kind),
    }))
    .filter((row) => row.label && row.stratum === stratum.stratum_value);
  const labelCounts = new Map();
  for (const row of rows) bump(labelCounts, row.label);
  const eligible = new Set([...labelCounts.entries()].filter(([, count]) => count >= minLabelRows).map(([label]) => label));
  return rows.filter((row) => eligible.has(row.label));
}

function discoverStrata(baseFamilies) {
  const out = [{ stratum_kind: 'overall', stratum_value: 'all' }];
  for (const stratumKind of ['site', 'type', 'type_site']) {
    const counts = new Map();
    for (const family of baseFamilies) {
      const value = stratumLabel(family, stratumKind);
      if (value) bump(counts, value);
    }
    for (const [stratumValue, count] of counts.entries()) {
      if (count < minStratumRows) continue;
      const rows = prepareRows(baseFamilies, { stratum_kind: stratumKind, stratum_value: stratumValue });
      const labelCount = new Set(rows.map((row) => row.label)).size;
      if (rows.length >= minStratumRows && labelCount >= 2) {
        out.push({ stratum_kind: stratumKind, stratum_value: stratumValue });
      }
    }
  }
  return out.sort((a, b) => a.stratum_kind.localeCompare(b.stratum_kind) || a.stratum_value.localeCompare(b.stratum_value));
}

function evaluateStratum(policy, stratum, families) {
  const rows = prepareRows(families, stratum);
  const labels = [...new Set(rows.map((row) => row.label))].sort((a, b) => a.localeCompare(b));
  if (labels.length < 2) return [];

  const globalLabelCounts = new Map();
  const lengthCounts = new Map();
  const edgeCounts = new Map();
  const tokenByLabel = new Map();
  const tokenTotalsByLabel = new Map();
  const vocab = new Set();

  for (const row of rows) {
    bump(globalLabelCounts, row.label);
    addNested(lengthCounts, String(row.tokens.length), row.label);
    const edgeKey = row.tokens.length <= 1 ? `single:${row.tokens[0] ?? ''}` : `${row.tokens.length}:${row.tokens[0]}:${row.tokens[row.tokens.length - 1]}`;
    addNested(edgeCounts, edgeKey, row.label);
    if (!tokenByLabel.has(row.label)) tokenByLabel.set(row.label, new Map());
    for (const token of row.tokens) {
      vocab.add(token);
      bump(tokenByLabel.get(row.label), token);
      bump(tokenTotalsByLabel, row.label);
    }
  }

  const models = {
    majority: { correct: 0, confusion: new Map() },
    length: { correct: 0, confusion: new Map() },
    edge_frame: { correct: 0, confusion: new Map() },
    token_nb: { correct: 0, confusion: new Map() },
  };

  for (const row of rows) {
    const trainLabelCounts = subtractLabelCount(globalLabelCounts, row.label);
    const lengthKey = String(row.tokens.length);
    const trainLengthCounts = subtractLabelCount(lengthCounts.get(lengthKey) ?? new Map(), row.label);
    const edgeKey = row.tokens.length <= 1 ? `single:${row.tokens[0] ?? ''}` : `${row.tokens.length}:${row.tokens[0]}:${row.tokens[row.tokens.length - 1]}`;
    const trainEdgeCounts = subtractLabelCount(edgeCounts.get(edgeKey) ?? new Map(), row.label);
    const predictions = {
      majority: bestLabel(trainLabelCounts, labels, globalLabelCounts),
      length: bestLabel(trainLengthCounts, labels, trainLabelCounts),
      edge_frame: bestLabel(trainEdgeCounts, labels, trainLengthCounts.size ? trainLengthCounts : trainLabelCounts),
      token_nb: null,
    };

    let bestNb = null;
    let bestScore = -Infinity;
    const vocabSize = Math.max(1, vocab.size);
    for (const label of labels) {
      const prior = ((trainLabelCounts.get(label) ?? 0) + alpha) / (Math.max(1, rows.length - 1) + alpha * labels.length);
      let score = Math.log(prior);
      const labelTokenCounts = new Map(tokenByLabel.get(label) ?? new Map());
      let labelTokenTotal = tokenTotalsByLabel.get(label) ?? 0;
      if (label === row.label) {
        for (const token of row.tokens) {
          const next = (labelTokenCounts.get(token) ?? 0) - 1;
          if (next <= 0) labelTokenCounts.delete(token);
          else labelTokenCounts.set(token, next);
          labelTokenTotal--;
        }
      }
      for (const token of row.tokens) {
        score += Math.log(((labelTokenCounts.get(token) ?? 0) + alpha) / (labelTokenTotal + alpha * vocabSize));
      }
      if (score > bestScore || (score === bestScore && label.localeCompare(bestNb) < 0)) {
        bestNb = label;
        bestScore = score;
      }
    }
    predictions.token_nb = bestNb;

    for (const [model, predicted] of Object.entries(predictions)) {
      if (predicted === row.label) models[model].correct++;
      addConfusion(models[model].confusion, row.label, predicted);
    }
  }

  const majorityLabelName = [...globalLabelCounts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0];
  return Object.entries(models).map(([model, result]) => {
    const macros = macroScores(result.confusion, labels);
    return {
      policy,
      stratum_kind: stratum.stratum_kind,
      stratum_value: stratum.stratum_value,
      model,
      evaluated_rows: rows.length,
      label_count: labels.length,
      labels: labels.join(';'),
      majority_label: majorityLabelName,
      majority_share: formatNumber((globalLabelCounts.get(majorityLabelName) ?? 0) / rows.length),
      accuracy: formatNumber(result.correct / rows.length),
      macro_f1: macros.macro_f1,
      macro_recall: macros.macro_recall,
    };
  });
}

function inventory(policy, families) {
  const familySizes = families.map((family) => family.family_size ?? 1);
  const sourceWeights = families.map((family) => family.family_source_weight ?? family.duplicate_weight ?? 1);
  return {
    policy,
    families: families.length,
    tokens: families.reduce((sum, family) => sum + family.tokens.length, 0),
    unique_signs: new Set(families.flatMap((family) => family.tokens)).size,
    source_weight: sourceWeights.reduce((sum, value) => sum + value, 0),
    multi_record_families: familySizes.filter((size) => size > 1).length,
    largest_family_records: familySizes.length ? Math.max(...familySizes) : 0,
    largest_source_weight: sourceWeights.length ? Math.max(...sourceWeights) : 0,
  };
}

function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? '+' : '-';
  const absMinutes = Math.abs(offsetMinutes);
  const pad = (value) => String(value).padStart(2, '0');
  const offset = `${sign}${pad(Math.floor(absMinutes / 60))}:${pad(absMinutes % 60)}`;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(
    date.getHours(),
  )}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${offset}`;
}

const rows = parseCsv(fs.readFileSync(sourcePath, 'utf8'));
const header = rows[0];
const column = Object.fromEntries(header.map((name, index) => [name, index]));
const records = rows.slice(1).map((row) => ({
  id: row[column.id],
  cisi: row[column.cisi],
  region: row[column.region],
  site: row[column.site],
  type: row[column.type],
  material: row[column.material],
  complete: row[column.complete],
  direction: row[column.direction],
  class: row[column.class],
  readiness: row[column.readiness_bucket],
  tokens: parseTokens(row[column.text]),
}));

const edgeSummary = JSON.parse(fs.readFileSync(edgeSummaryPath, 'utf8'));
const top10EdgeSigns = edgeSummary.policies.find((row) => row.policy === 'remove_top_10_edge_signs').removed_signs;
const numericClean = records.filter((record) => record.readiness === 'lipi_numeric_clean_candidate');

const policies = [
  { name: 'exact_sequence_collapsed', transform: 'none', family: 'exact_sequence' },
  { name: 'edge_frame_collapsed', transform: 'none', family: 'edge_frame' },
  { name: 'one_edit_family_collapsed', transform: 'none', family: 'one_edit_neighborhood' },
  { name: 'top10_edge_removed_exact_sequence_collapsed', transform: 'remove_top_10_edge_signs', family: 'exact_sequence' },
  { name: 'top10_edge_removed_edge_frame_collapsed', transform: 'remove_top_10_edge_signs', family: 'edge_frame' },
  { name: 'top10_edge_removed_one_edit_family_collapsed', transform: 'remove_top_10_edge_signs', family: 'one_edit_neighborhood' },
];

const baseFamilies = buildPolicyFamilies(numericClean, policies[0], top10EdgeSigns);
const strata = discoverStrata(baseFamilies);
const familySets = new Map();
const inventoryRows = [];
const resultRows = [];

for (const policy of policies) {
  const families = buildPolicyFamilies(numericClean, policy, top10EdgeSigns);
  familySets.set(policy.name, families);
  inventoryRows.push(inventory(policy.name, families));
  for (const stratum of strata) {
    resultRows.push(...evaluateStratum(policy.name, stratum, families));
  }
}

const inventoryHeader = [
  'policy',
  'families',
  'tokens',
  'unique_signs',
  'source_weight',
  'multi_record_families',
  'largest_family_records',
  'largest_source_weight',
];

fs.writeFileSync(
  outInventory,
  toCsv([inventoryHeader, ...inventoryRows.map((row) => inventoryHeader.map((key) => row[key]))]),
  'utf8',
);

const resultHeader = [
  'policy',
  'stratum_kind',
  'stratum_value',
  'model',
  'evaluated_rows',
  'label_count',
  'labels',
  'majority_label',
  'majority_share',
  'accuracy',
  'macro_f1',
  'macro_recall',
];

fs.writeFileSync(
  outResults,
  toCsv([resultHeader, ...resultRows.map((row) => resultHeader.map((key) => row[key]))]),
  'utf8',
);

const summary = {
  generated_at_local: formatLocalIso(new Date()),
  source_file: 'data/open_prototype/reports/lipi_scope_rows.csv',
  source_scope: 'lipi_numeric_clean_candidate',
  source_rows: numericClean.length,
  target: 'class',
  min_stratum_rows: minStratumRows,
  min_label_rows: minLabelRows,
  top10_edge_signs: top10EdgeSigns,
  policies,
  strata,
  inventory: inventoryRows,
  results: resultRows,
  artifact_files: [
    'data/open_prototype/reports/lipi_class_robustness_inventory.csv',
    'data/open_prototype/reports/lipi_class_robustness_results.csv',
    'data/open_prototype/reports/lipi_class_robustness_summary.json',
  ],
  interpretation_boundary:
    'Class robustness scout only. Class labels come from the filtered T3 planning layer and do not create meanings, sign values, language identity, or translations.',
};

fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

console.log(
  JSON.stringify(
    {
      inventory: inventoryRows,
      token_nb_overall: resultRows.filter((row) => row.stratum_kind === 'overall' && row.model === 'token_nb'),
      token_nb_stratified_selected: resultRows.filter(
        (row) =>
          row.model === 'token_nb' &&
          ['SEAL:S', 'TAB:B', 'TAB:I', 'SEAL:S@Mohenjo-daro', 'TAB:B@Harappa', 'TAB:I@Harappa'].includes(row.stratum_value),
      ),
      wrote: summary.artifact_files,
    },
    null,
    2,
  ),
);
