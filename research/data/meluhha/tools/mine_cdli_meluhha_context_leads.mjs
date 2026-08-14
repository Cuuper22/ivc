// Lead miner over the frozen CDLI line-context export (2026-05-29): what
// cuneiform words keep company with Meluhha, and which of them are worth
// chasing? It works entirely on the cuneiform side — no Indus sign value is
// claimed. Fourteen hand-seeded leads (the Shu-ilishu interpreter seal, the
// Irisagrig ration group, ship/labor contexts, carnelian and copper commodity
// formulae, patronymics like "dumu me-luh-ha", and so on) each carry
// diagnostic, anchor, and control query strings; the script counts exact and
// loose matches for every query across the deduplicated line contexts, on the
// Meluhha line itself and on adjacent lines. It also auto-mines 1-to-3-token
// n-grams from those contexts (minus stop tokens and Meluhha forms) and keeps
// the top 80 by artifact spread. Each seed lead records its own predicted
// failure mode up front. Writes leads, query-plan, and auto-token CSVs plus a
// JSON summary; leads are query plans only until they survive matched-negative
// searches.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = path.join(ROOT, 'data', 'meluhha');
const RUN_DATE = '2026-05-29';

const INPUT_CONTEXTS = path.join(OUT, 'cdli_current_line_contexts.csv');
const LEADS_OUT = path.join(OUT, 'cdli_meluhha_context_leads.csv');
const QUERY_PLAN_OUT = path.join(OUT, 'cdli_meluhha_context_lead_query_plan.csv');
const AUTO_OUT = path.join(OUT, 'cdli_meluhha_context_auto_token_leads.csv');
const SUMMARY_OUT = path.join(OUT, 'cdli_meluhha_context_lead_summary.json');

const LEAD_FIELDS = [
  'lead_id',
  'rank',
  'lead_label',
  'lead_class',
  'verified_context_count',
  'same_line_context_count',
  'adjacent_context_count',
  'artifact_count',
  'artifact_ps',
  'periods',
  'proveniences',
  'diagnostic_queries',
  'anchor_queries',
  'control_queries',
  'best_example_artifact_p',
  'best_example_source_url',
  'best_example_line',
  'best_example_previous_line',
  'best_example_following_line',
  'rationale',
  'predicted_failure_mode',
];

const QUERY_PLAN_FIELDS = [
  'query_id',
  'lead_id',
  'rank',
  'lead_label',
  'lead_class',
  'query_role',
  'query_text',
  'verified_context_count',
  'same_line_context_count',
  'adjacent_context_count',
  'artifact_count',
  'artifact_ps',
  'rationale',
  'predicted_failure_mode',
];

const AUTO_FIELDS = [
  'auto_id',
  'ngram',
  'token_count',
  'lead_class_guess',
  'context_count',
  'same_line_context_count',
  'adjacent_context_count',
  'artifact_count',
  'artifact_ps',
  'example_artifact_p',
  'example_line',
  'example_previous_line',
  'example_following_line',
];

const STOP_TOKENS = new Set([
  '',
  'x',
  'xx',
  'xxx',
  '...',
  'la2',
  'ki',
  'ta',
  'da',
  'ka',
  'ke4',
  'me',
  'sze3',
  'bi',
  'ba',
  'na',
  'ne',
  'ra',
  'e',
  'a',
  'i3',
  'sze',
  'gur',
  'gin2',
  'ma-na',
  'barig',
  'ban2',
  'asz',
  'disz',
]);

const MELUHHA_TOKENS = new Set([
  'me-luh-ha',
  'me-luh-ha{ki}',
  'me-luh-ha-ta',
  'me-luh-ha-da',
  'me-luh-ha-ka',
  'me-luh-ha-sze3',
  'me-luh-ha{ki}-me',
  'me-luh-ha{ki}-ta',
  'me-luh-ha{ki}-ka',
  'me-luh-ha{ki}-sze3',
]);

const SEED_LEADS = [
  {
    rank: 1,
    label: 'Shu-ilishu interpreter seal',
    class: 'onomastic_interpreter_title',
    diagnostic: ['eme-bal me-luh-ha', 'eme-bal me-luh-ha{ki}', 'szu-i3-li2-su'],
    anchor: ['szu-i3-li2-su eme-bal'],
    control: ['eme-bal'],
    rationale: 'P525331 has `szu-i3-li2-su` adjacent to `eme-bal me-luh-ha{ki}`, the strongest readable interpreter/name configuration in the current export.',
    failure: 'Probably a singleton cylinder-seal title; the external strict target already produced no Indus pattern candidate.',
  },
  {
    rank: 2,
    label: 'Irisagrig Meluhha ration group',
    class: 'ration_group_person_cluster',
    diagnostic: ['i3-ba lu2 me-luh-ha', 'lu2 me-luh-ha{ki}-me', 'a-li-a-hi', 'a-ru-a lugal', 'sipa a-dara4'],
    anchor: ['a-li-a-hi dam-a-ni'],
    control: ['i3-ba', 'a-ru-a', 'sipa'],
    rationale: 'P453801, P516138, and P516366 preserve repeated `i3-ba lu2 me-luh-ha{ki}-me` contexts with neighboring names or role phrases.',
    failure: 'Likely a duplicate/publication cluster or a ration-list participant group rather than an Indus-facing name bridge.',
  },
  {
    rank: 3,
    label: 'Meluhha ship/work context',
    class: 'ship_labor_context',
    diagnostic: ['ma2 me-luh-ha', 'ma2 me-luh-ha-sze3', 'lu2-tukul ma2 me-luh-ha', 'gurusz ma2 me-luh-ha', 'nu-banda3 ma2 me-luh-ha'],
    anchor: ['lu2-tukul', 'gurusz', 'nu-banda3'],
    control: ['ma2', 'ma2-gan'],
    rationale: 'Several rows attach Meluhha to boats, laborers, or supervisors: `lu2-tukul`, `gurusz`, `nu-banda3`, and destination `ma2 me-luh-ha-sze3`.',
    failure: 'May be route or work vocabulary, not identity; all-distinct strings are easy to fit by length/pattern alone.',
  },
  {
    rank: 4,
    label: 'Carnelian from Meluhha',
    class: 'commodity_material_context',
    diagnostic: ['gug gi-rin-e me-luh-ha-ta', 'gug gi-rin me-luh-ha-da'],
    anchor: ['gug gi-rin', 'gug gi-rin-e'],
    control: ['gug', 'gi-rin'],
    rationale: 'Gudea material passages use `gug gi-rin(-e)` with Meluhha ablative/comitative marking.',
    failure: 'Royal/composite commodity formula; strong source-side semantics but weak as an Indus sign anchor.',
  },
  {
    rank: 5,
    label: 'Prestige-material chain',
    class: 'commodity_material_chain',
    diagnostic: ['uruda nagga lagab za-gin3-na ku3 NE gug gi-rin me-luh-ha-da', 'uruda nagga', 'za-gin3-na', 'ku3 NE gug gi-rin'],
    anchor: ['nagga', 'za-gin3-na', 'ku3', 'NE'],
    control: ['uruda', 'gug'],
    rationale: 'The long Gudea chain gives one of the richest co-material contexts around Meluhha in readable cuneiform.',
    failure: 'Probably a generic prestige-material list, and the principal witnesses may not be independent attestations.',
  },
  {
    rank: 6,
    label: 'Meluhha copper',
    class: 'commodity_material_context',
    diagnostic: ['uruda me-luh-ha', 'ma-na uruda me-luh-ha'],
    anchor: ['uruda', 'nagga uruda'],
    control: ['uruda', 'nagga'],
    rationale: 'P136689 has `6(disz) ma-na uruda me-luh-ha` near `nagga`, giving a clean material-origin lead.',
    failure: 'Commodity-origin label, not onomastic; useful as a material control more than as a phonetic bridge.',
  },
  {
    rank: 7,
    label: 'i3-dub Meluhha formula',
    class: 'administrative_formula',
    diagnostic: ['i3-dub me-luh-ha', 'i3-dub me-luh-ha-ta'],
    anchor: ['i3-dub'],
    control: ['i3-dub ma2-gan', 'i3-dub'],
    rationale: '`i3-dub` recurs across multiple Meluhha-bearing administrative entries in the current line export.',
    failure: 'Likely a broad administrative/storage/accounting formula, not a Meluhha-specific name or title.',
  },
  {
    rank: 8,
    label: 'e2-duru5 Meluhha estate',
    class: 'estate_settlement_context',
    diagnostic: ['e2-duru5 me-luh-ha', 'e2-duru5 me-luh-ha-ta', 'e2-duru5 me-luh-ha{ki}'],
    anchor: ['e2-duru5'],
    control: ['e2-duru5'],
    rationale: '`e2-duru5` appears with Meluhha locative or ablative forms and may encode an estate/settlement context.',
    failure: 'Settlement/estate language can be locally administrative rather than externally bilingual.',
  },
  {
    rank: 9,
    label: 'sons of Meluhha',
    class: 'patronymic_origin_formula',
    diagnostic: ['dumu me-luh-ha', 'ur-{d}lamma dumu me-luh-ha', 'kiszib3 ur-{d}lamma dumu me-luh-ha', 'ur-{d}ig-alim dumu me-luh-ha'],
    anchor: ['ur-{d}lamma', 'ur-{d}ig-alim', 'kiszib3 ur-{d}lamma'],
    control: ['dumu', 'ur-{d}lamma', 'kiszib3'],
    rationale: 'The current rows include `dumu me-luh-ha` and named seal-owner or patronymic-style phrases.',
    failure: '`Ur-Lamma` and `dumu` are common; this may be ordinary patronymic/origin formula rather than a Meluhhan personal name.',
  },
  {
    rank: 10,
    label: 'ugula Meluhha title',
    class: 'title_singleton',
    diagnostic: ['ugula me-luh-ha', 'ugula# me-luh-ha'],
    anchor: ['_ARAD2_ {d}nansze-me'],
    control: ['ugula'],
    rationale: 'A damaged/singleton title row has `ugula# me-luh-ha` with an adjacent personal/theophoric phrase.',
    failure: 'Damaged and singleton; likely an office/rank label if real.',
  },
  {
    rank: 11,
    label: 'Meluhha furniture/object inventory',
    class: 'object_inventory_context',
    diagnostic: ['{gesz}guzza {gesz}ab-ba me-luh-ha', '{gesz}guzza me-luh-ha'],
    anchor: ['{gesz}guzza', '{gesz}ab-ba'],
    control: ['{gesz}guzza', '{gesz}ab-ba'],
    rationale: 'A furniture/object sequence may preserve uncertain `me-luh-ha?`, useful as an object-label control if source-backed.',
    failure: 'Uncertain reading and object inventory context; should not be elevated to a phonetic anchor.',
  },
  {
    rank: 12,
    label: 'Meluhha orchard/garden',
    class: 'land_administration_context',
    diagnostic: ['{gesz}kiri6 me-luh-ha', '{gesz}kiri6 me-luh-ha {d}nin-mar{ki}'],
    anchor: ['{gesz}kiri6'],
    control: ['{gesz}kiri6'],
    rationale: 'One row places Meluhha in an orchard/garden administrative setting.',
    failure: 'Probably local institutional/land administration rather than a bilingual bridge.',
  },
  {
    rank: 13,
    label: 'Meluhha route-control lane',
    class: 'route_toponym_control',
    diagnostic: ['me-luh-ha{ki} ma2-gan{ki}', 'kur me-luh-ha{ki} ma2-gan{ki} dilmun{ki}', 'ma2-gan me-luh-ha kur-bi-ta'],
    anchor: ['ma2-gan{ki}', 'dilmun{ki}', 'gu-bi'],
    control: ['ma2-gan{ki}', 'dilmun{ki}'],
    rationale: 'Meluhha appears in the wider Magan/Dilmun route formula; this is a good control lane for overfitting Meluhha alone.',
    failure: 'Mostly literary/royal route formula, not an onomastic or object-level bridge.',
  },
  {
    rank: 14,
    label: 'Meluhha speckled dog/object',
    class: 'animal_object_modifier',
    diagnostic: ['ur gun3-a me-luh-ha', 'ur gun3-a me-luh-ha{ki}'],
    anchor: ['ur gun3-a'],
    control: ['ur gun3-a'],
    rationale: '`ur gun3-a me-luh-ha{ki}` is a potential animal/object modifier context from the expanded inventory.',
    failure: 'Object or animal tribute label; useful as modifier-control only.',
  },
];

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
      rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += ch;
    }
  }
  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ''));
    rows.push(row);
  }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1).filter((r) => r.some((v) => v !== '')).map((r) => {
    const out = {};
    header.forEach((h, i) => {
      out[h] = r[i] ?? '';
    });
    return out;
  });
}

function csvEscape(value) {
  const text = String(value ?? '');
  if (/[",\n\r]/.test(text)) return `"${text.replaceAll('"', '""')}"`;
  return text;
}

function writeCsv(file, rows, fields) {
  const lines = [fields.join(',')];
  for (const row of rows) lines.push(fields.map((field) => csvEscape(row[field])).join(','));
  fs.writeFileSync(file, `${lines.join('\n')}\n`, 'utf8');
}

function stableId(parts) {
  return crypto.createHash('sha1').update(parts.join('\u241f'), 'utf8').digest('hex').slice(0, 16);
}

function cleanLineNumber(text) {
  return String(text ?? '').replace(/^\s*\d+'?\.?\s*/, '').trim();
}

function normalizeAtf(text) {
  return cleanLineNumber(text)
    .toLowerCase()
    .replace(/[#?!]/g, '')
    .replace(/\[[^\]]*?\]/g, '')
    .replace(/[.,;:]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeForLooseContains(text) {
  return normalizeAtf(text)
    .replace(/[{()}]/g, '')
    .replace(/_/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function queryAppearsIn(text, query) {
  const normalizedText = normalizeAtf(text);
  const normalizedQuery = normalizeAtf(query);
  if (normalizedText.includes(normalizedQuery)) return true;
  return normalizeForLooseContains(text).includes(normalizeForLooseContains(query));
}

function cleanToken(token) {
  return String(token ?? '')
    .toLowerCase()
    .replace(/^\d+'?\.\s*/, '')
    .replace(/[#?!\[\],.;:]/g, '')
    .replace(/^_+|_+$/g, '')
    .trim();
}

function tokenize(text) {
  return normalizeAtf(text)
    .split(/\s+/)
    .map(cleanToken)
    .filter((token) => token && !STOP_TOKENS.has(token))
    .filter((token) => !MELUHHA_TOKENS.has(token))
    .filter((token) => !/^\d/.test(token))
    .filter((token) => token !== 'me-luh-ha' && !token.startsWith('me-luh-ha'));
}

function classifyNgram(ngram) {
  if (/(ur-\{d\}|szu-i3|a-li-a-hi|a-ru-a|dumu|kiszib3)/.test(ngram)) return 'onomastic_or_patronymic';
  if (/(ma2|gurusz|nu-banda3|lu2-tukul)/.test(ngram)) return 'ship_labor';
  if (/(uruda|nagga|za-gin3|gug|gi-rin|ku3|ne)/.test(ngram)) return 'commodity_material';
  if (/(e2-duru5|\{gesz\}kiri6)/.test(ngram)) return 'estate_land';
  if (/(ugula|eme-bal|lu2)/.test(ngram)) return 'title_role';
  return 'unclassified_context';
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function contextHaystack(row) {
  return [row.previous_line, row.line_text, row.following_line].filter(Boolean).join(' | ');
}

function scoreQuery(rows, query) {
  const contexts = [];
  for (const row of rows) {
    const same = queryAppearsIn(row.line_text, query);
    const previous = queryAppearsIn(row.previous_line, query);
    const following = queryAppearsIn(row.following_line, query);
    if (!same && !previous && !following) continue;
    contexts.push({ row, same, adjacent: !same && (previous || following) });
  }
  const artifactPs = uniqueSorted(contexts.map((ctx) => ctx.row.artifact_p));
  return {
    contexts,
    verifiedContextCount: contexts.length,
    sameLineContextCount: contexts.filter((ctx) => ctx.same).length,
    adjacentContextCount: contexts.filter((ctx) => ctx.adjacent).length,
    artifactPs,
    periods: uniqueSorted(contexts.map((ctx) => ctx.row.period)),
    proveniences: uniqueSorted(contexts.map((ctx) => ctx.row.provenience)),
    bestExample: contexts[0]?.row ?? null,
  };
}

function summarizeSeed(seed, rows) {
  const allQueries = [...seed.diagnostic, ...seed.anchor, ...seed.control];
  const queryScores = allQueries.map((query) => ({ query, score: scoreQuery(rows, query) }));
  const contexts = queryScores.flatMap((entry) => entry.score.contexts.map((ctx) => ctx.row));
  const artifactPs = uniqueSorted(contexts.map((row) => row.artifact_p));
  const periods = uniqueSorted(contexts.map((row) => row.period));
  const proveniences = uniqueSorted(contexts.map((row) => row.provenience));
  const bestExample = contexts.find((row) => seed.diagnostic.some((query) => queryAppearsIn(row.line_text, query)))
    ?? contexts[0]
    ?? null;
  return {
    queryScores,
    verifiedContextCount: contexts.length,
    sameLineContextCount: queryScores.reduce((sum, entry) => sum + entry.score.sameLineContextCount, 0),
    adjacentContextCount: queryScores.reduce((sum, entry) => sum + entry.score.adjacentContextCount, 0),
    artifactPs,
    periods,
    proveniences,
    bestExample,
  };
}

function buildAutoTokenLeads(rows) {
  const byNgram = new Map();
  for (const row of rows) {
    const fields = [
      { scope: 'previous', text: row.previous_line, same: false, adjacent: true },
      { scope: 'line', text: row.line_text, same: true, adjacent: false },
      { scope: 'following', text: row.following_line, same: false, adjacent: true },
    ];
    for (const field of fields) {
      const tokens = tokenize(field.text);
      for (let n = 1; n <= Math.min(3, tokens.length); n += 1) {
        for (let i = 0; i <= tokens.length - n; i += 1) {
          const ngram = tokens.slice(i, i + n).join(' ');
          if (!ngram || STOP_TOKENS.has(ngram)) continue;
          if (ngram.length < 3) continue;
          const item = byNgram.get(ngram) ?? {
            ngram,
            token_count: n,
            contexts: [],
          };
          item.contexts.push({ row, same: field.same, adjacent: field.adjacent, scope: field.scope });
          byNgram.set(ngram, item);
        }
      }
    }
  }

  return [...byNgram.values()]
    .map((item) => {
      const artifactPs = uniqueSorted(item.contexts.map((ctx) => ctx.row.artifact_p));
      const example = item.contexts[0]?.row ?? {};
      return {
        auto_id: `auto_${stableId([item.ngram])}`,
        ngram: item.ngram,
        token_count: item.token_count,
        lead_class_guess: classifyNgram(item.ngram),
        context_count: item.contexts.length,
        same_line_context_count: item.contexts.filter((ctx) => ctx.same).length,
        adjacent_context_count: item.contexts.filter((ctx) => ctx.adjacent).length,
        artifact_count: artifactPs.length,
        artifact_ps: artifactPs.join('|'),
        example_artifact_p: example.artifact_p ?? '',
        example_line: example.line_text ?? '',
        example_previous_line: example.previous_line ?? '',
        example_following_line: example.following_line ?? '',
      };
    })
    .filter((row) => row.artifact_count >= 1)
    .sort((a, b) => {
      const scoreA = Number(a.artifact_count) * 10 + Number(a.context_count) + Number(a.token_count);
      const scoreB = Number(b.artifact_count) * 10 + Number(b.context_count) + Number(b.token_count);
      return scoreB - scoreA || a.ngram.localeCompare(b.ngram);
    })
    .slice(0, 80);
}

function main() {
  const contexts = parseCsv(fs.readFileSync(INPUT_CONTEXTS, 'utf8'));
  const uniqueContexts = [...new Map(contexts.map((row) => [
    [row.artifact_p, row.line_index, row.line_text, row.previous_line, row.following_line].join('\u241f'),
    row,
  ])).values()];

  const leadRows = [];
  const queryPlanRows = [];

  for (const seed of SEED_LEADS) {
    const leadId = `lead_${String(seed.rank).padStart(2, '0')}_${stableId([seed.label])}`;
    const summary = summarizeSeed(seed, uniqueContexts);
    leadRows.push({
      lead_id: leadId,
      rank: seed.rank,
      lead_label: seed.label,
      lead_class: seed.class,
      verified_context_count: summary.verifiedContextCount,
      same_line_context_count: summary.sameLineContextCount,
      adjacent_context_count: summary.adjacentContextCount,
      artifact_count: summary.artifactPs.length,
      artifact_ps: summary.artifactPs.join('|'),
      periods: summary.periods.join('|'),
      proveniences: summary.proveniences.join('|'),
      diagnostic_queries: seed.diagnostic.join('|'),
      anchor_queries: seed.anchor.join('|'),
      control_queries: seed.control.join('|'),
      best_example_artifact_p: summary.bestExample?.artifact_p ?? '',
      best_example_source_url: summary.bestExample?.source_url ?? '',
      best_example_line: summary.bestExample?.line_text ?? '',
      best_example_previous_line: summary.bestExample?.previous_line ?? '',
      best_example_following_line: summary.bestExample?.following_line ?? '',
      rationale: seed.rationale,
      predicted_failure_mode: seed.failure,
    });

    for (const [role, queries] of [['diagnostic', seed.diagnostic], ['anchor', seed.anchor], ['control', seed.control]]) {
      for (const query of queries) {
        const score = scoreQuery(uniqueContexts, query);
        queryPlanRows.push({
          query_id: `query_${stableId([leadId, role, query])}`,
          lead_id: leadId,
          rank: seed.rank,
          lead_label: seed.label,
          lead_class: seed.class,
          query_role: role,
          query_text: query,
          verified_context_count: score.verifiedContextCount,
          same_line_context_count: score.sameLineContextCount,
          adjacent_context_count: score.adjacentContextCount,
          artifact_count: score.artifactPs.length,
          artifact_ps: score.artifactPs.join('|'),
          rationale: seed.rationale,
          predicted_failure_mode: seed.failure,
        });
      }
    }
  }

  const autoRows = buildAutoTokenLeads(uniqueContexts);

  const summary = {
    run_date: RUN_DATE,
    input_contexts: path.relative(ROOT, INPUT_CONTEXTS).replaceAll('\\', '/'),
    unique_line_contexts: uniqueContexts.length,
    lead_count: leadRows.length,
    query_plan_count: queryPlanRows.length,
    auto_token_lead_count: autoRows.length,
    outputs: {
      leads: path.relative(ROOT, LEADS_OUT).replaceAll('\\', '/'),
      query_plan: path.relative(ROOT, QUERY_PLAN_OUT).replaceAll('\\', '/'),
      auto_token_leads: path.relative(ROOT, AUTO_OUT).replaceAll('\\', '/'),
    },
    caveats: [
      'This is a cuneiform-side lead miner over current CDLI line-context exports; it does not claim any Indus sign value.',
      'Seed leads are admitted only as query plans and must survive matched-negative CDLI searches before being used downstream.',
      'Verified context counts are exact phrase/context scans over exported lines, not comprehensive Assyriological attestation counts.',
    ],
  };

  writeCsv(LEADS_OUT, leadRows, LEAD_FIELDS);
  writeCsv(QUERY_PLAN_OUT, queryPlanRows, QUERY_PLAN_FIELDS);
  writeCsv(AUTO_OUT, autoRows, AUTO_FIELDS);
  fs.writeFileSync(SUMMARY_OUT, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
}

main();
