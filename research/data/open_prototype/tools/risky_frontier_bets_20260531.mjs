// Runs four independent "frontier bets" — risky, falsifiable claims at the
// edge of what the corpus supports — and scores each with its own Monte Carlo
// null (100000 iterations). The bets: (1) 002-390-X is a polarity slot where
// sign 125 opens continuation and 095/692/705 close the phrase; (2) the sign
// after 806 classifies icon context (806-465 predicts plant iconography,
// 806-468 predicts symbol-free seals); (3) sign 090 marks a west-contact
// circular-seal route on external sites like Failaka and Susa; (4) Indus 002
// descends into the Brahmi ra-line and behaves as a connector, checked
// against a precomputed Brahmi low-null CSV. Reads the filtered corpus
// metadata, assigns each bet a tier (candidate / wild shot / killed) with
// falsifiers and next predictions, and writes one JSON detail file plus a
// one-row-per-bet summary CSV.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const BRAHMI_LOW_NULL = path.join(ROOT, 'data', 'brahmi', 'brahmi_real_token_low_null_reaudit_20260531.csv');
const OUT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const PREFIX = 'risky_frontier_bets_20260531';
const RUN_DATE = '2026-05-31';
const ITERATIONS = 100000;

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

function writeCsv(file, rows, fields) {
  const esc = (value) => {
    const text = String(value ?? '');
    return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  const body = rows.map((row) => fields.map((field) => esc(row[field])).join(',')).join('\n');
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`);
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' ? text : fallback;
}

function mulberry32(seed) {
  return function rand() {
    let t = (seed += 0x6D2B79F5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function choose(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

function hasBigram(signs, a, b) {
  return signs.some((sign, idx) => sign === a && signs[idx + 1] === b);
}

function contextKey(row) {
  return [
    norm(row.site),
    norm(row.type),
    norm(row.symbol),
    norm(row.cult),
    norm(row.material),
    norm(row.shape),
  ].join('|');
}

function rowBrief(row) {
  return [
    objectId(row),
    norm(row.site),
    norm(row.type),
    norm(row.symbol),
    norm(row.cult),
    row.text,
  ].join('/');
}

function fisherRightTail(a, b, c, d) {
  const logFact = [0];
  const n = a + b + c + d;
  for (let i = 1; i <= n; i += 1) logFact[i] = logFact[i - 1] + Math.log(i);
  const logChoose = (nn, kk) => logFact[nn] - logFact[kk] - logFact[nn - kk];
  const row1 = a + b;
  const row2 = c + d;
  const col1 = a + c;
  const min = Math.max(0, col1 - row2);
  const max = Math.min(row1, col1);
  const logDen = logChoose(n, col1);
  let p = 0;
  for (let x = a; x <= max; x += 1) {
    const lp = logChoose(row1, x) + logChoose(row2, col1 - x) - logDen;
    p += Math.exp(lp);
  }
  return Math.max(0, Math.min(1, p));
}

const rows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({
  ...row,
  signs: tokens(row.text),
}));

function bet002390Polarity() {
  const openSigns = new Set(['125']);
  const closeSigns = new Set(['095', '692', '705']);
  const focusSigns = new Set([...openSigns, ...closeSigns]);
  const frames = [];
  const nonFrameBySign = new Map();

  for (const row of rows) {
    const signs = row.signs;
    for (let i = 0; i < signs.length; i += 1) {
      const sign = signs[i];
      if (!focusSigns.has(sign)) continue;
      const after002390 = signs[i - 2] === '002' && signs[i - 1] === '390';
      const terminal = i === signs.length - 1;
      if (after002390) {
        frames.push({
          row,
          sign,
          terminal,
          hit: openSigns.has(sign) ? !terminal : terminal,
        });
      } else {
        if (!nonFrameBySign.has(sign)) nonFrameBySign.set(sign, []);
        nonFrameBySign.get(sign).push(terminal);
      }
    }
  }

  const targetFrames = frames.filter((frame) => focusSigns.has(frame.sign));
  const observedHits = targetFrames.filter((frame) => frame.hit).length;
  const exactTextCollapsed = [...new Map(targetFrames.map((frame) => [frame.row.text, frame])).values()];
  const exactHits = exactTextCollapsed.filter((frame) => frame.hit).length;
  const strictObjects = new Set(['M-70', 'M-71', 'M-119', 'M-735']);
  const strictFrames = targetFrames.filter((frame) => strictObjects.has(objectId(frame.row)));
  const strictHits = strictFrames.filter((frame) => frame.hit).length;
  const frameContinuing = targetFrames.filter((frame) => !frame.terminal).length;
  const openFrameCount = targetFrames.filter((frame) => openSigns.has(frame.sign)).length;
  const frameInternalPermutationFpr =
    observedHits === targetFrames.length && openFrameCount === frameContinuing
      ? 1 / binomial(targetFrames.length, openFrameCount)
      : 1;
  const mohenjoFrames = targetFrames.filter((frame) => norm(frame.row.site) === 'Mohenjo-daro');
  const nonMohenjoFrames = targetFrames.filter((frame) => norm(frame.row.site) !== 'Mohenjo-daro');
  const mohenjoHits = mohenjoFrames.filter((frame) => frame.hit).length;
  const nonMohenjoHits = nonMohenjoFrames.filter((frame) => frame.hit).length;
  const rand = mulberry32(0x2390);
  let geObserved = 0;
  let geStrict = 0;

  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    let score = 0;
    for (const frame of targetFrames) {
      const terminal = choose(rand, nonFrameBySign.get(frame.sign));
      const hit = openSigns.has(frame.sign) ? !terminal : terminal;
      if (hit) score += 1;
    }
    if (score >= observedHits) geObserved += 1;

    let strictScore = 0;
    for (const frame of strictFrames) {
      const terminal = choose(rand, nonFrameBySign.get(frame.sign));
      const hit = openSigns.has(frame.sign) ? !terminal : terminal;
      if (hit) strictScore += 1;
    }
    if (strictScore >= strictHits) geStrict += 1;
  }

  const bySign = {};
  for (const sign of focusSigns) {
    const pool = nonFrameBySign.get(sign) ?? [];
    bySign[sign] = {
      nonframe_pool: pool.length,
      nonframe_terminal: pool.filter(Boolean).length,
      nonframe_continuing: pool.filter((value) => !value).length,
      frame_rows: targetFrames.filter((frame) => frame.sign === sign).length,
      frame_hits: targetFrames.filter((frame) => frame.sign === sign && frame.hit).length,
    };
  }

  return {
    bet_id: 'V2_SLOT_002390_BRANCH_POLARITY_20260531',
    vector: 'V2 effective-unicity / slot grammar',
    confidence_tier: geObserved / ITERATIONS <= 0.01 && geStrict / ITERATIONS > 0.01 ? 'candidate' : 'wild shot',
    risky_bet: '`002-390-X` is a branch-polarity slot: `125` opens continuation, while `095`, `692`, and `705` close the phrase in this frame.',
    falsifier: 'A source-bound terminal `002-390-125`, or source-bound continuing `002-390-095/692/705`, or a sign-specific non-frame null reproducing the full polarity split at ordinary rates.',
    observed: `${observedHits}/${targetFrames.length} frame rows match the polarity bet; exact-text collapse ${exactHits}/${exactTextCollapsed.length}; Mohenjo-daro ${mohenjoHits}/${mohenjoFrames.length}; non-Mohenjo-daro ${nonMohenjoHits}/${nonMohenjoFrames.length}; strict visual subset ${strictHits}/${strictFrames.length}; frame-internal permutation FPR ${frameInternalPermutationFpr.toFixed(6)}.`,
    adversarial_test: `Monte Carlo sign-specific non-frame terminality null, ${ITERATIONS} iterations; frame-internal open/closed label permutation preserving terminality counts.`,
    false_positive_rate: geObserved / ITERATIONS,
    strict_subset_false_positive_rate: geStrict / ITERATIONS,
    frame_internal_permutation_false_positive_rate: frameInternalPermutationFpr,
    support_objects: targetFrames.map((frame) => rowBrief(frame.row)).join(' | '),
    by_sign: bySign,
    next_prediction: 'H-1993 should source-bind as terminal `002-390-095`; Dholavira 4237.1 or M-1825 should source-bind as terminal `002-390-705`; any contrary source-bound row demotes the bet immediately.',
  };
}

function bet806SuffixIconClassifier() {
  const rows806465 = rows.filter((row) => hasBigram(row.signs, '806', '465'));
  const rows806468 = rows.filter((row) => hasBigram(row.signs, '806', '468'));
  const exactTexts806465 = [...new Set(rows806465.map((row) => row.text))];
  const exactTexts806468 = [...new Set(rows806468.map((row) => row.text))];
  const isPhyt = (row) => norm(row.symbol) === 'Phyt';
  const isNoSymbolSeal = (row) => norm(row.symbol) === 'NA' && String(row.type).startsWith('SEAL');
  const observedScore = rows806465.filter(isPhyt).length + rows806468.filter(isNoSymbolSeal).length;
  const maxScore = rows806465.length + rows806468.length;

  const all806SuffixRows = rows.filter((row) => {
    const signs = row.signs;
    return signs.some((sign, idx) => sign === '806' && signs[idx + 1]);
  });

  const contextPool = all806SuffixRows.map((row) => ({
    phyt: isPhyt(row),
    noSymbolSeal: isNoSymbolSeal(row),
  }));
  const rand = mulberry32(0x806465);
  let geObserved = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    let score = 0;
    for (let i = 0; i < rows806465.length; i += 1) if (choose(rand, contextPool).phyt) score += 1;
    for (let i = 0; i < rows806468.length; i += 1) if (choose(rand, contextPool).noSymbolSeal) score += 1;
    if (score >= observedScore) geObserved += 1;
  }

  const matchedPools = new Map();
  for (const row of rows) {
    const key = `${norm(row.site)}|${norm(row.type)}`;
    if (!matchedPools.has(key)) matchedPools.set(key, []);
    matchedPools.get(key).push(row);
  }
  let geSiteType = 0;
  for (let iter = 0; iter < ITERATIONS; iter += 1) {
    let score = 0;
    for (const row of rows806465) {
      const sample = choose(rand, matchedPools.get(`${norm(row.site)}|${norm(row.type)}`));
      if (isPhyt(sample)) score += 1;
    }
    for (const row of rows806468) {
      const sample = choose(rand, matchedPools.get(`${norm(row.site)}|${norm(row.type)}`));
      if (isNoSymbolSeal(sample)) score += 1;
    }
    if (score >= observedScore) geSiteType += 1;
  }

  return {
    bet_id: 'V4_CONTEXT_806_SUFFIX_ICON_CLASSIFIER_20260531',
    vector: 'V4 context-to-meaning',
    confidence_tier:
      geObserved / ITERATIONS <= 0.01
      && geSiteType / ITERATIONS <= 0.05
      && exactTexts806465.length >= 2
      && exactTexts806468.length >= 2
        ? 'candidate'
        : 'wild shot',
    risky_bet: '`806` is not the semantic class alone; the following sign is an icon-context classifier. Specifically `806-465` predicts plant iconography, while `806-468` predicts aniconic/no-symbol seal contexts.',
    falsifier: 'Find several source-bound `806-465` rows without plant iconography, or `806-468` rows with animal/plant iconography, or a suffix-shuffle/site-type null that reproduces the split.',
    observed: `806-465: ${rows806465.filter(isPhyt).length}/${rows806465.length} Phyt but ${exactTexts806465.length} exact text family. 806-468: ${rows806468.filter(isNoSymbolSeal).length}/${rows806468.length} no-symbol seals across ${exactTexts806468.length} exact text families. Joint score ${observedScore}/${maxScore}.`,
    adversarial_test: `Two nulls, ${ITERATIONS} iterations each: shuffle context labels among all 806-suffix rows; sample matched site/type rows.`,
    false_positive_rate: geObserved / ITERATIONS,
    site_type_false_positive_rate: geSiteType / ITERATIONS,
    copy_family_warning: exactTexts806465.length === 1
      ? 'The plant side is one exact formula repeated five times, so the semantic claim is not a suffix-family claim yet.'
      : '',
    support_objects: [
      `806-465 => ${rows806465.map(rowBrief).join(' | ')}`,
      `806-468 => ${rows806468.map(rowBrief).join(' | ')}`,
    ].join(' || '),
    exact_texts_806_465: exactTexts806465.join(' | '),
    exact_texts_806_468: exactTexts806468.join(' | '),
    next_prediction: 'Other `806-X` suffix families should separate icon classes better than raw artifact type; the next kill test is leave-one-object and exact-text-family collapse before any semantic promotion.',
  };
}

function betExternal090CircularRoute() {
  const externalSites = new Set(['Failaka', 'Susa', 'Tell Umma', 'Tepe Yahya', 'Gonur Depe']);
  const externalRows = rows.filter((row) => externalSites.has(norm(row.site)));
  const isCircular = (row) => norm(row.shape) === 'circular' || norm(row.type) === 'SEAL:C';
  const has090 = (row) => row.signs.includes('090');
  const circularExternal = externalRows.filter(isCircular);
  const nonCircularExternal = externalRows.filter((row) => !isCircular(row));
  const circularWith090 = circularExternal.filter(has090).length;
  const nonCircularWith090 = nonCircularExternal.filter(has090).length;
  const observedPerfectSplit = circularWith090 === circularExternal.length && nonCircularWith090 === 0;
  const pExternalPermutation = observedPerfectSplit
    ? 1 / binomial(externalRows.length, circularExternal.length)
    : 1;

  const allCircular = rows.filter(isCircular);
  const allNonCircular = rows.filter((row) => !isCircular(row));
  const fisherP = fisherRightTail(
    circularExternal.filter(has090).length,
    circularExternal.filter((row) => !has090(row)).length,
    allCircular.filter((row) => !externalSites.has(norm(row.site)) && has090(row)).length,
    allCircular.filter((row) => !externalSites.has(norm(row.site)) && !has090(row)).length,
  );

  return {
    bet_id: 'V1_EXTERNAL_090_CIRCULAR_ROUTE_MARKER_20260531',
    vector: 'V1 diffuse Meluhha/Gulf external bridge',
    confidence_tier: circularExternal.length >= 3 && observedPerfectSplit ? 'wild shot' : 'killed',
    risky_bet: '`090` is a west-contact circular-seal route/formula marker, not a generic foreign sign. It should mark the Failaka/Susa circular-seal lane and fail on non-circular external objects.',
    falsifier: 'A source-bound Failaka/Susa circular-seal row without `090`, several local circular seals with the same `090` pattern, or a non-circular external object with the same sign in the same slot.',
    observed: `External circular rows with 090: ${circularWith090}/${circularExternal.length}; external non-circular rows with 090: ${nonCircularWith090}/${nonCircularExternal.length}.`,
    adversarial_test: 'Small-n exact external-row permutation plus global circular-seal Fisher right-tail check.',
    false_positive_rate: pExternalPermutation,
    circular_global_fisher_p: fisherP,
    support_objects: externalRows.map(rowBrief).join(' | '),
    next_prediction: 'Kjaerum/Failaka source pages for rows 147.1 and 148.1 should preserve a `090`-bearing circular-seal formula; if either binds to a different sign band, this bet dies.',
  };
}

function betBrahmi002RaLine() {
  const lowNullRows = fs.existsSync(BRAHMI_LOW_NULL)
    ? parseCsv(fs.readFileSync(BRAHMI_LOW_NULL, 'utf8'))
    : [];
  const row002 = lowNullRows.find((row) => row.sign_id === '002' && row.orientation_policy === 'visual_ltr_catalog_order');
  const signCounts = new Map();
  for (const row of rows) {
    row.signs.forEach((sign, idx) => {
      if (!signCounts.has(sign)) signCounts.set(sign, { n: 0, terminal: 0, initial: 0 });
      const c = signCounts.get(sign);
      c.n += 1;
      if (idx === row.signs.length - 1) c.terminal += 1;
      if (idx === 0) c.initial += 1;
    });
  }
  const c002 = signCounts.get('002') ?? { n: 0, terminal: 0, initial: 0 };
  const commonSigns = [...signCounts.entries()]
    .filter(([, c]) => c.n >= 50)
    .map(([sign, c]) => ({
      sign,
      n: c.n,
      terminal_rate: c.terminal / c.n,
      initial_rate: c.initial / c.n,
    }));
  const terminalRankLow = commonSigns
    .filter((item) => item.terminal_rate <= c002.terminal / c002.n)
    .length;

  return {
    bet_id: 'V3_BRAHMI_002_RA_LINE_WILDSHOT_20260531',
    vector: 'V3 backward Brahmi / descendant morphology',
    confidence_tier: 'wild shot',
    risky_bet: 'Indus `002` is a real ra-line shape descendant candidate, and its script-internal role is a high-frequency connector/linker rather than an object noun.',
    falsifier: 'Independent source tokens move the modal Brahmi label away from `ra`, duplicate collapse keeps failing, or `002` behaves like an ordinary terminal/content sign under matched position tests.',
    observed: row002
      ? `Brahmi low-null row: modal=${row002.modal_brahmi_label}, v3_modal=${row002.v3_cisi_modal_label}, sample=${row002.sample_count}, impostor FPR=${row002.impostor_ge_observed_share}, shape-null=${row002.original_shape_null_share}, label-null=${row002.original_label_null_share}, unique CISI=${row002.unique_cisi_count}. Metadata position: 002 terminal ${c002.terminal}/${c002.n} (${(c002.terminal / c002.n).toFixed(3)}), initial ${c002.initial}/${c002.n} (${(c002.initial / c002.n).toFixed(3)}), low-terminal rank ${terminalRankLow}/${commonSigns.length} among signs with >=50 occurrences.`
      : 'No replacement low-null row for 002 found; bet cannot be tested in this run.',
    adversarial_test: 'Directly tied to the positive bet: real-token impostor row plus a corpus-position sanity check for connector-like behavior.',
    false_positive_rate: row002 ? Number(row002.impostor_ge_observed_share) : 1,
    secondary_false_positive_rate: row002 ? Number(row002.original_shape_null_share) : 1,
    support_objects: 'Uses family-level Brahmi token evidence and all metadata occurrences of sign 002; no phonetic value is accepted.',
    next_prediction: '`002` should remain nonterminal/internal in held-out source-bound rows and should preferentially appear before branch/closure heads such as `390` and `861`; if future independent source tokens stop looking ra-like, the descent bet dies.',
  };
}

function binomial(n, k) {
  if (k < 0 || k > n) return 0;
  k = Math.min(k, n - k);
  let out = 1;
  for (let i = 1; i <= k; i += 1) out = (out * (n - k + i)) / i;
  return out;
}

const bets = [
  bet002390Polarity(),
  bet806SuffixIconClassifier(),
  betExternal090CircularRoute(),
  betBrahmi002RaLine(),
];

const summaryRows = bets.map((bet) => ({
  run_date: RUN_DATE,
  bet_id: bet.bet_id,
  vector: bet.vector,
  confidence_tier: bet.confidence_tier,
  risky_bet: bet.risky_bet,
  observed: bet.observed,
  adversarial_test: bet.adversarial_test,
  false_positive_rate: bet.false_positive_rate,
  secondary_false_positive_rate:
    bet.strict_subset_false_positive_rate
    ?? bet.site_type_false_positive_rate
    ?? bet.circular_global_fisher_p
    ?? bet.secondary_false_positive_rate
    ?? bet.frame_internal_permutation_false_positive_rate
    ?? '',
  falsifier: bet.falsifier,
  next_prediction: bet.next_prediction,
}));

const detailPath = path.join(OUT_DIR, `${PREFIX}.json`);
const summaryPath = path.join(OUT_DIR, `${PREFIX}.csv`);
fs.writeFileSync(detailPath, `${JSON.stringify({ run_date: RUN_DATE, iterations: ITERATIONS, bets }, null, 2)}\n`);
writeCsv(summaryPath, summaryRows, [
  'run_date',
  'bet_id',
  'vector',
  'confidence_tier',
  'risky_bet',
  'observed',
  'adversarial_test',
  'false_positive_rate',
  'secondary_false_positive_rate',
  'falsifier',
  'next_prediction',
]);

console.log(JSON.stringify({
  run_date: RUN_DATE,
  iterations: ITERATIONS,
  outputs: {
    detail: path.relative(ROOT, detailPath).replaceAll('\\', '/'),
    summary: path.relative(ROOT, summaryPath).replaceAll('\\', '/'),
  },
  bets: summaryRows,
}, null, 2));
