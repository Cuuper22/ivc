import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const META = path.join(ROOT, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const MELUHHA = path.join(ROOT, 'data', 'meluhha');
const OUT_PREFIX = 'consolidated_frontier_model_20260531_1342';
const RUN_DATE = '2026-05-31T13:42:01-07:00';

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
  fs.writeFileSync(file, `${fields.join(',')}\n${body}${body ? '\n' : ''}`, 'utf8');
}

function tokens(text) {
  return String(text ?? '').match(/\d{3}/g) ?? [];
}

function norm(value, fallback = 'NA') {
  const text = String(value ?? '').trim();
  return text && text !== '-' && text !== 'None' && text !== '--' ? text : fallback;
}

function readJson(relativePath, base = REPORTS) {
  const full = path.join(base, relativePath);
  return JSON.parse(fs.readFileSync(full, 'utf8'));
}

function readMaybeJson(relativePath, base = REPORTS) {
  const full = path.join(base, relativePath);
  return fs.existsSync(full) ? JSON.parse(fs.readFileSync(full, 'utf8')) : null;
}

function objectId(row) {
  return row.cisi && row.cisi !== '-' ? row.cisi : `-:${row.id}`;
}

function carrierContext(row) {
  const type = norm(row.type);
  if (['SEAL:R', 'TAB:C'].includes(type)) return 'rect_copper_register';
  if (type === 'SEAL:S' && norm(row.symbol) === 'Bull1:W') return 'square_bull1w_icon';
  if (type === 'SEAL:S') return 'square_other_icon';
  if (['TAB:B', 'TAB:I'].includes(type)) return 'tablet_account';
  if (['SEAL:C', 'SEAL:CY'].includes(type)) return 'external_round_or_cylinder';
  return 'other';
}

function positionRole(row, sign) {
  const idx = row.signs.indexOf(sign);
  if (idx < 0) return null;
  const next = row.signs[idx + 1] ?? '<END>';
  if (idx === 0) return 'initial';
  if (next === '<END>' || next === '002') return 'boundary';
  return 'internal';
}

function positionProfile(rows, sign) {
  const profile = new Map();
  const examples = [];
  for (const row of rows) {
    if (!row.signSet.has(sign)) continue;
    for (let idx = 0; idx < row.signs.length; idx += 1) {
      if (row.signs[idx] !== sign) continue;
      const context = carrierContext(row);
      const next = row.signs[idx + 1] ?? '<END>';
      const role = idx === 0 ? 'initial' : next === '<END>' || next === '002' ? 'boundary' : 'internal';
      const key = `${context}|${role}`;
      profile.set(key, (profile.get(key) ?? 0) + 1);
      if (examples.length < 80) {
        examples.push({
          sign,
          object: objectId(row),
          site: norm(row.site),
          type: norm(row.type),
          symbol: norm(row.symbol),
          context,
          role,
          prev: row.signs[idx - 1] ?? '<START>',
          next,
          text: row.text,
        });
      }
    }
  }
  const byContext = {};
  for (const [key, count] of profile.entries()) {
    const [context, role] = key.split('|');
    byContext[context] ??= { total: 0, roles: {} };
    byContext[context].total += count;
    byContext[context].roles[role] = count;
  }
  for (const value of Object.values(byContext)) {
    value.boundary_or_final_share = (value.roles.boundary ?? 0) / value.total;
    value.internal_share = (value.roles.internal ?? 0) / value.total;
    value.initial_share = (value.roles.initial ?? 0) / value.total;
  }
  return { sign, byContext, examples };
}

function edgeContextScope(rows, left, right) {
  const byContext = {};
  for (const row of rows) {
    const leftIdx = row.signs.indexOf(left);
    const rightIdx = row.signs.indexOf(right);
    if (leftIdx < 0 || rightIdx < 0) continue;
    const context = carrierContext(row);
    byContext[context] ??= { total: 0, left_before_right: 0, right_before_left: 0, examples: [] };
    byContext[context].total += 1;
    if (leftIdx < rightIdx) byContext[context].left_before_right += 1;
    else byContext[context].right_before_left += 1;
    if (byContext[context].examples.length < 8) byContext[context].examples.push(`${objectId(row)}:${norm(row.site)}:${norm(row.type)}:${norm(row.symbol)}:${row.text}`);
  }
  for (const value of Object.values(byContext)) {
    value.left_before_share = value.left_before_right / value.total;
  }
  return byContext;
}

function decision(id, tier, action, rank, claim, basis, weakness, nextTest, source) {
  return { id, tier, action, rank, claim, basis, weakness, next_test: nextTest, source };
}

const rawRows = parseCsv(fs.readFileSync(META, 'utf8')).map((row) => ({ ...row, signs: tokens(row.text) }));
const rows = [...new Map(rawRows.map((row) => [row.signs.join(' '), row])).values()]
  .filter((row) => row.signs.length)
  .map((row) => ({ ...row, signSet: new Set(row.signs) }));

const roleGrammar = readJson('risky_role_partial_order_grammar_20260531.json');
const headerInfo = readJson('risky_initial_header_register_information_20260531.json');
const sign400 = readJson('risky_400_tablet_account_register_forger_20260531.json');
const sign400740 = readJson('risky_400740_tablet_hierarchy_forger_20260531.json');
const sign740Hub = readJson('risky_740_precedence_hub_forger_20260531.json');
const sign002Bridge = readJson('risky_002_preterminal_bridge_forger_20260531.json');
const sign407806 = readJson('risky_407_806_register_slot_split_forger_20260531.json');
const sign405806Bull1w = readJson('risky_405806_bull1w_icon_subtype_forger_20260531.json');
const sign520Elephant = readJson('risky_520_elephant_icon_header_forger_20260531.json');
const sign741BullJl = readJson('risky_741_bull1_jl_icon_subtype_forger_20260531.json');
const terminalSplit = readJson('risky_002_terminal_allomorph_context_split_20260531.json');
const crossSiteBackbone = readMaybeJson('consolidate_backbone_cross_site_prediction_20260531_1348.json');
const familyCollapseBackbone = readMaybeJson('consolidate_backbone_family_collapse_20260531_1352.json');
const lengthStrataBackbone = readMaybeJson('consolidate_backbone_length_strata_20260531_1356.json');
const branch002390 = readMaybeJson('risky_slot_branch_class_002390_20260531.json');
const sign125Portable = readMaybeJson('risky_125_governed_crosssite_template_forger_20260531.json');
const brahmiRa = readMaybeJson('risky_740407_brahmi_ra_opener_bridge_probe_20260531.json', path.join(ROOT, 'data', 'brahmi'));
const meluhha407Uruda = readMaybeJson('risky_407_uruda_meluhha_diffuse_bridge_20260531.json', MELUHHA);
const external090091 = readMaybeJson('risky_external_090091_circular_route_split_20260531.json', MELUHHA);
const externalPrior = readMaybeJson('risky_external_register_bridge_prior_20260531.json', MELUHHA);

const profile806 = positionProfile(rows, '806');
const profile405 = positionProfile(rows, '405');
const profile741 = positionProfile(rows, '741');
const profile520 = positionProfile(rows, '520');
const edge400740Scope = edgeContextScope(rows, '400', '740');
const hardCoreEdges = ['740_before_002', '002_before_861', '002_before_820', '806_before_002'];
const scopedEdges = ['400_before_740'];
const softPeripheralEdges = ['740_before_817', '002_before_817', '740_before_820'];
const backboneConstraints = [
  ['400_before_740', '400', '740'],
  ['740_before_002', '740', '002'],
  ['740_before_861', '740', '861'],
  ['740_before_820', '740', '820'],
  ['740_before_817', '740', '817'],
  ['002_before_861', '002', '861'],
  ['002_before_820', '002', '820'],
  ['002_before_817', '002', '817'],
  ['806_before_002', '806', '002'],
];

function evaluateBackboneSlice(name, predicate) {
  let total = 0;
  let satisfied = 0;
  let usable = 0;
  let passed = 0;
  const details = [];
  for (const [id, left, right] of backboneConstraints) {
    let constraintTotal = 0;
    let constraintSatisfied = 0;
    for (const row of rows) {
      if (!predicate(row)) continue;
      const leftIdx = row.signs.indexOf(left);
      const rightIdx = row.signs.indexOf(right);
      if (leftIdx < 0 || rightIdx < 0) continue;
      constraintTotal += 1;
      if (leftIdx < rightIdx) constraintSatisfied += 1;
    }
    if (!constraintTotal) continue;
    usable += 1;
    total += constraintTotal;
    satisfied += constraintSatisfied;
    const share = constraintSatisfied / constraintTotal;
    const constraintPassed = constraintTotal < 5 || share >= 0.8;
    if (constraintPassed) passed += 1;
    details.push({
      id,
      satisfied: constraintSatisfied,
      total: constraintTotal,
      share,
      passed: constraintPassed,
    });
  }
  return {
    slice: name,
    usable_constraints: usable,
    passed_constraints: passed,
    satisfied_rows: satisfied,
    total_rows: total,
    satisfied_share: total ? satisfied / total : 0,
    details,
  };
}

const backboneSlices = [
  evaluateBackboneSlice('all', () => true),
  evaluateBackboneSlice('complete', (row) => norm(row.complete) === 'Y'),
  evaluateBackboneSlice('non_poor', (row) => norm(row.condition) !== 'Poor'),
  evaluateBackboneSlice('without_harappa', (row) => norm(row.site) !== 'Harappa'),
  evaluateBackboneSlice('without_mohenjo', (row) => norm(row.site) !== 'Mohenjo-daro'),
  evaluateBackboneSlice('without_harappa_and_mohenjo', (row) => !['Harappa', 'Mohenjo-daro'].includes(norm(row.site))),
  evaluateBackboneSlice('harappa_only', (row) => norm(row.site) === 'Harappa'),
  evaluateBackboneSlice('mohenjo_only', (row) => norm(row.site) === 'Mohenjo-daro'),
];

const bull1SealRows = rows.filter((row) => norm(row.type) === 'SEAL:S' && norm(row.symbol).startsWith('Bull1'));
function bull1VariantClass(row) {
  const symbol = norm(row.symbol);
  if (symbol === 'Bull1:W') return 'W';
  if (['Bull1:J', 'Bull1:L'].includes(symbol)) return 'JL';
  return 'otherBull1';
}
function has405806(row) {
  return row.signSet.has('405') || row.signSet.has('806');
}
function has741(row) {
  return row.signSet.has('741');
}
const iconDiscriminator = Object.fromEntries(['W', 'JL', 'otherBull1'].map((klass) => {
  const group = bull1SealRows.filter((row) => bull1VariantClass(row) === klass);
  return [klass, {
    rows: group.length,
    has_405_or_806: group.filter(has405806).length,
    has_741: group.filter(has741).length,
    has_both_marker_families: group.filter((row) => has405806(row) && has741(row)).length,
  }];
}));

const rect806 = profile806.byContext.rect_copper_register;
const bull806 = profile806.byContext.square_bull1w_icon;
const sealOther806 = profile806.byContext.square_other_icon;
const contradictionTests = [
  {
    id: '806_polyfunction_stress',
    question: 'Does Bull1:W use of 806 contradict the existing rectangular/copper closure-pivot role?',
    result: 'not_contradiction_under_boundary_pivot_model',
    evidence:
      `rect/copper 806 boundary share=${rect806.boundary_or_final_share} (${rect806.roles.boundary ?? 0}/${rect806.total}); ` +
      `Bull1:W square 806 boundary share=${bull806.boundary_or_final_share} (${bull806.roles.boundary ?? 0}/${bull806.total}); ` +
      `other square 806 boundary share=${sealOther806.boundary_or_final_share} (${sealOther806.roles.boundary ?? 0}/${sealOther806.total}).`,
    decision: 'Merge as one syntactic boundary/pivot sign selected by multiple carrier/icon contexts; do not split into two phonetic values.',
  },
  {
    id: '405_vs_806_role_split',
    question: 'Do 405 and 806 form one sign-pair formula in Bull1:W rows?',
    result: 'no_strict_pair_formula',
    evidence:
      `405/806 either on Bull1:W SEAL:S is strong (${sign405806Bull1w.key_controls.seal_s_either.target_a}/${sign405806Bull1w.key_controls.seal_s_either.context_rows}), ` +
      `but both signs co-occur in only ${rows.filter((row) => norm(row.type) === 'SEAL:S' && norm(row.symbol) === 'Bull1:W' && row.signSet.has('405') && row.signSet.has('806')).length} Bull1:W rows.`,
    decision: 'Keep as alternative subtype-marker family, not a fixed 405-806 formula.',
  },
  {
    id: '741_clean_jl_subtype_stress',
    question: 'Does 741 behave as a clean Bull1:J/L subtype marker when tested against the stronger 405/806 Bull1:W family?',
    result: 'clean_jl_subtype_killed_broad_bull_motif_survives',
    evidence:
      `Bull1 variant matrix: W rows=${iconDiscriminator.W.rows}, 405/806=${iconDiscriminator.W.has_405_or_806}, 741=${iconDiscriminator.W.has_741}; ` +
      `J/L rows=${iconDiscriminator.JL.rows}, 405/806=${iconDiscriminator.JL.has_405_or_806}, 741=${iconDiscriminator.JL.has_741}; ` +
      `other Bull1 rows=${iconDiscriminator.otherBull1.rows}, 405/806=${iconDiscriminator.otherBull1.has_405_or_806}, 741=${iconDiscriminator.otherBull1.has_741}.`,
    decision: 'Demote 741 from clean J/L subtype marker to broad Bull1 motif candidate with J/L pressure.',
  },
  {
    id: 'terminal_partner_semantics',
    question: 'Can 861/820/817 after 002 be read as context-separated terminal meanings?',
    result: 'killed',
    evidence: terminalSplit.observed,
    decision: 'Keep only as terminal partner set after 002; do not assign semantic allomorphs.',
  },
  {
    id: 'external_bridge_direction',
    question: 'Should V1 chase object-level personal names or commodity/register bridges next?',
    result: 'commodity_register_bridge_wins_current_consolidation',
    evidence:
      `${externalPrior?.observed ?? 'external prior report available'}; rejected U17649 onomastic attempt is already killed by high site-shuffle false-positive rate.`,
    decision: 'Next external tests should attack commodity/register predictions, not resurrect U17649-style personal-name readings.',
  },
];

const decisions = [
  decision(
    'minimal_role_backbone',
    'promoted candidate',
    'promote_as_current_core_model',
    1,
    'The strongest current model is a split partial-order role grammar: hard-core edges 740->002, 002->{861,820}, and 806->002; carrier-scoped tablet/account edge 400->740; softer 817 terminal-partner edges; 407 as rect/copper entry into the 806 boundary zone.',
    `Partial-order grammar: ${roleGrammar.observed}; cross-site destructive check: ${crossSiteBackbone?.observed ?? 'not yet run'}; family-collapse destructive check: ${familyCollapseBackbone?.observed ?? 'not yet run'}; length-strata destructive check: ${lengthStrataBackbone?.observed ?? 'not yet run'}; header MI=${headerInfo.observed}; 400 tablet=${sign400.observed}; 400-before-740=${sign400740.observed}; 740 hub=${sign740Hub.observed}; 002 bridge=${sign002Bridge.observed}; 407/806 split=${sign407806.observed}.`,
    `No sound values, language ID, or translation; 400->002 direct edge and 407->806 direct edge are weak when isolated, so the model is backbone-level, not a complete grammar. Slice stress: without both Harappa and Mohenjo-daro ${backboneSlices.find((row) => row.slice === 'without_harappa_and_mohenjo').passed_constraints}/${backboneSlices.find((row) => row.slice === 'without_harappa_and_mohenjo').usable_constraints} constraints pass with ${backboneSlices.find((row) => row.slice === 'without_harappa_and_mohenjo').satisfied_rows}/${backboneSlices.find((row) => row.slice === 'without_harappa_and_mohenjo').total_rows} rows satisfied. 400_before_740 is carrier-scoped, not universal: tablet/account ${edge400740Scope.tablet_account?.left_before_right ?? 0}/${edge400740Scope.tablet_account?.total ?? 0}, square Bull1:W ${edge400740Scope.square_bull1w_icon?.left_before_right ?? 0}/${edge400740Scope.square_bull1w_icon?.total ?? 0}, other square ${edge400740Scope.square_other_icon?.left_before_right ?? 0}/${edge400740Scope.square_other_icon?.total ?? 0}. Family collapse confirms this: ${familyCollapseBackbone?.observed ?? 'family-collapse result missing'}. Length stress further demotes peripheral edges: ${lengthStrataBackbone?.observed ?? 'length-strata result missing'}. Hard-core edges now mean no bad length/carrier slices, not just high global row share.`,
    'In next EXPAND, predict held-out row order using hard-core edges first. Treat 400->740 only inside tablet/account contexts and use 817 edges only as soft predictions.',
    'risky_role_partial_order_grammar_20260531.json',
  ),
  decision(
    '806_boundary_context_merge',
    'promoted candidate',
    'merge_not_split',
    2,
    '806 should be treated as a boundary/pivot role sign whose distribution is carrier/icon conditioned, not as contradictory separate discoveries.',
    contradictionTests[0].evidence,
    'Bull1:W enrichment of 806 is only candidate-level because leave-Harappa weakens the icon-specific claim.',
    'Test new 806 rows by predicting boundary position first, then carrier/icon enrichment second. A run of non-boundary 806 in Bull1:W rows breaks the merge.',
    'metadata_filtered.csv + risky_405806_bull1w_icon_subtype_forger_20260531.json',
  ),
  decision(
    '405806_bull1w_subtype',
    'candidate',
    'keep_but_demote_below_backbone',
    3,
    '405/806 are a Bull1:W square-seal subtype-marker family, with 806 also participating in the backbone boundary role.',
    sign405806Bull1w.observed,
    'Overall hostile FPR is 0.025 because leave-Harappa weakens; this is probably Harappa-weighted or regional unless new non-Harappa rows strengthen it.',
    'Next EXPAND should test whether Bull1:W rows with 405/806 have a consistent sub-icon/cult/neighbor profile, and should make a held-out prediction for non-Harappa Bull1:W rows.',
    'risky_405806_bull1w_icon_subtype_forger_20260531.json',
  ),
  decision(
    '741_bull1_jl_subtype',
    'candidate',
    'demote_from_clean_subtype_to_broad_bull_motif',
    4,
    '741 remains a bull-icon motif candidate with J/L enrichment, but not a clean Bull1:J/L subtype marker.',
    sign741BullJl.observed,
    `Direct icon discriminator demotes clean subtype reading: W 741=${iconDiscriminator.W.has_741}/${iconDiscriminator.W.rows}; J/L 741=${iconDiscriminator.JL.has_741}/${iconDiscriminator.JL.rows}; other Bull1 741=${iconDiscriminator.otherBull1.has_741}/${iconDiscriminator.otherBull1.rows}. It also competes with broad square-seal/740 opener structure and is less central to the role backbone.`,
    'Next EXPAND should test whether 741 predicts a neighbor motif or terminal path, not just a Bull1 variant label.',
    'risky_741_bull1_jl_icon_subtype_forger_20260531.json',
  ),
  decision(
    'external_commodity_register_bridge',
    'candidate',
    'keep_as_v1_direction',
    5,
    'The external Meluhha direction currently favors commodity/register bridges over object-level personal-name readings.',
    `${externalPrior?.observed ?? 'external prior missing'} ${meluhha407Uruda?.observed ?? ''}`,
    'No object-level bilingual, no sign sound, and CDLI/primary source binding remains decisive.',
    'Next EXPAND should formulate one exact commodity-register prediction from cuneiform side and test it against Indus register signs before any new source-chase.',
    'risky_external_register_bridge_prior_20260531.json + risky_407_uruda_meluhha_diffuse_bridge_20260531.json',
  ),
  decision(
    'external_090091_route_split',
    'candidate',
    'keep_separate_from_core_role_backbone',
    6,
    '090/091 form a mutually exclusive external circular-seal route/register pair candidate.',
    external090091?.observed ?? 'external 090/091 report missing',
    'Small N, site clustering, and source validation prevent promotion; it should not be blended into the 400/740/002 internal role grammar yet.',
    'Next EXPAND should predict which new Gulf/Mesopotamian circular rows take 090 versus 091 before checking source rows.',
    'risky_external_090091_circular_route_split_20260531.json',
  ),
  decision(
    '002390_branch_class',
    'candidate',
    'keep_as_subgrammar',
    7,
    '002-390-X is a branch-class slot with open continuation versus closed terminal branches.',
    branch002390?.observed ?? '002390 branch report missing',
    'Several support rows are metadata-only or route-pressure, and branch 707 lacks a non-frame pool.',
    'Next EXPAND should use new 002-390-X rows as prediction tests: 125/530/590 should continue; 072/095/140/346/692/705/707 should close.',
    'risky_slot_branch_class_002390_20260531.json',
  ),
  decision(
    '520_elephant_header',
    'wild shot',
    'kill_as_candidate_keep_as_prediction_only',
    8,
    '520 as elephant-icon header is not a live semantic candidate after consolidation.',
    sign520Elephant.observed,
    'Same-type/square all-sign maxstats are bad and leave-Mohenjo FPR is 0.214.',
    'Only revive if a held-out non-Mohenjo complete elephant square seal carries 520, preferably initially.',
    'risky_520_elephant_icon_header_forger_20260531.json',
  ),
  decision(
    'terminal_861_820_817_allomorphs',
    'wild shot killed',
    'kill',
    9,
    '861/820/817 after 002 do not currently encode separable context semantics.',
    terminalSplit.observed,
    'Feature maxstat FPR is high; best apparent feature is a coincidence under null.',
    'Do not spend next EXPAND on terminal semantic labels unless a new, independent predictor is formulated first.',
    'risky_002_terminal_allomorph_context_split_20260531.json',
  ),
  decision(
    '740407_brahmi_ra_bridge',
    'wild shot killed',
    'kill_as_phonetic_anchor',
    10,
    '740/407 should not be assigned ra-like Brahmi values.',
    brahmiRa?.observed ?? 'Brahmi ra bridge report missing',
    'Brahmi bridge failed preflight/null gates; structural opener status is not a phonetic value.',
    'Next Brahmi expansion must start with shape-evolution predictions that are independent of already-known role signs.',
    'risky_740407_brahmi_ra_opener_bridge_probe_20260531.json',
  ),
  decision(
    '125_portable_governed_template',
    'wild shot killed',
    'kill_as_candidate',
    11,
    '125 as a portable governed suffix/title element is not a live candidate.',
    sign125Portable?.observed ?? '125 portable report missing',
    'Forger false-positive rates near 1 mean frequency-matched signs routinely imitate the pattern.',
    'Only revive 125 through a new constrained prediction inside the already surviving 002-390 branch class.',
    'risky_125_governed_crosssite_template_forger_20260531.json',
  ),
];

const minimalModel = {
  name: 'carrier-conditioned role grammar with context-selected boundary/classifier signs',
  core:
    'Rows are best modeled first as carrier/register-conditioned administrative strings. Initial/header signs carry carrier information; the global partial-order backbone splits after length/carrier stress into hard-core edges, scoped edges, and soft peripheral edges. Some signs, especially 806, are not single-context labels but role signs whose use is selected by carrier/icon contexts.',
  strongest_path:
    'hard core: 740 -> 002, 002 -> {861,820}, 806 -> 002; scoped: tablet/account 400 -> 740; soft periphery: 817 terminal-partner edges and 740 -> 820 in thin tablet slices; rectangular/copper: 407 feeds the 806 boundary zone; square-seal icon layer: Bull1:W selects 405 or boundary-role 806 at candidate level.',
  not_in_model:
    'No accepted phonetic readings, no language-family ID, no fluent translations, no 861/820/817 semantic split, no 740/407 Brahmi ra value, no U17649 personal-name bridge.',
};

const nextDestructiveTests = [
  {
    phase: 'next_expand',
    test: 'held_out_backbone_order_prediction',
    prediction: 'Rows containing two or more of {400,740,407,806,002,861,820,817} should obey the core partial order before metadata is inspected.',
    break_condition: 'A new high-quality non-Harappa/non-Mohenjo slice repeatedly reverses 002-before-terminal or 740-before-002.',
  },
  {
    phase: 'next_expand',
    test: '806_context_merge_prediction',
    prediction: 'New 806 rows in Bull1:W and rect/copper contexts should be boundary-like at comparable rates.',
    break_condition: 'Bull1:W 806 becomes mostly non-boundary while rect/copper remains boundary-like.',
  },
  {
    phase: 'next_expand',
    test: 'non_harappa_bull1w_405806',
    prediction: 'Non-Harappa Bull1:W square seals should carry 405/806 above square-seal background, but possibly below Harappa rate.',
    break_condition: 'Additional non-Harappa Bull1:W rows lack both signs while non-Bull1:W rows continue accumulating them.',
  },
  {
    phase: 'next_expand',
    test: 'external_register_not_name_bridge',
    prediction: 'External Meluhha side should align better with commodity/register signs (407/400/090/091 families) than with full personal-name readings.',
    break_condition: 'A source-bound object-level bridge gives a low-FPR name mapping without register signs.',
  },
  {
    phase: 'next_expand',
    test: '002390_branch_holdout',
    prediction: 'New 002-390-125/530/590 rows continue; new 002-390-072/095/140/346/692/705/707 rows close.',
    break_condition: 'A source-bound row flips one of these branch classes.',
  },
];

const output = {
  run_date_time: RUN_DATE,
  phase: 'CONSOLIDATE',
  minimal_model: minimalModel,
  decisions,
  contradiction_tests: contradictionTests,
  position_profiles: {
    '806': profile806.byContext,
    '405': profile405.byContext,
    '741': profile741.byContext,
    '520': profile520.byContext,
  },
  icon_discriminator: iconDiscriminator,
  edge_context_scope: {
    '400_before_740': edge400740Scope,
  },
  backbone_slice_controls: backboneSlices,
  cross_site_backbone_prediction: crossSiteBackbone ? {
    conclusion: crossSiteBackbone.conclusion,
    observed: crossSiteBackbone.observed,
    consolidation_decision: crossSiteBackbone.consolidation_decision,
    falsifier_for_next_phase: crossSiteBackbone.falsifier_for_next_phase,
  } : null,
  family_collapse_backbone: familyCollapseBackbone ? {
    conclusion: familyCollapseBackbone.conclusion,
    observed: familyCollapseBackbone.observed,
    consolidation_decision: familyCollapseBackbone.consolidation_decision,
    mode_summaries: familyCollapseBackbone.mode_summaries,
  } : null,
  length_strata_backbone: lengthStrataBackbone ? {
    conclusion: lengthStrataBackbone.conclusion,
    observed: lengthStrataBackbone.observed,
    consolidation_decision: lengthStrataBackbone.consolidation_decision,
  } : null,
  edge_status_after_consolidation: {
    hard_core_edges: hardCoreEdges,
    scoped_edges: scopedEdges,
    soft_peripheral_edges: softPeripheralEdges,
    killed_as_universal: ['400_before_740_universal'],
  },
  next_destructive_tests: nextDestructiveTests,
};

fs.mkdirSync(REPORTS, { recursive: true });
fs.writeFileSync(path.join(REPORTS, `${OUT_PREFIX}.json`), JSON.stringify(output, null, 2), 'utf8');
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_decisions.csv`), decisions, [
  'rank',
  'id',
  'tier',
  'action',
  'claim',
  'basis',
  'weakness',
  'next_test',
  'source',
]);
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_contradiction_tests.csv`), contradictionTests, [
  'id',
  'question',
  'result',
  'evidence',
  'decision',
]);
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_next_destructive_tests.csv`), nextDestructiveTests, [
  'phase',
  'test',
  'prediction',
  'break_condition',
]);
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_backbone_slice_controls.csv`), backboneSlices.map((row) => ({
  slice: row.slice,
  usable_constraints: row.usable_constraints,
  passed_constraints: row.passed_constraints,
  satisfied_rows: row.satisfied_rows,
  total_rows: row.total_rows,
  satisfied_share: row.satisfied_share,
  failing_constraints: row.details.filter((detail) => !detail.passed).map((detail) => `${detail.id}:${detail.satisfied}/${detail.total}`).join(';'),
})), [
  'slice',
  'usable_constraints',
  'passed_constraints',
  'satisfied_rows',
  'total_rows',
  'satisfied_share',
  'failing_constraints',
]);
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_400740_context_scope.csv`), Object.entries(edge400740Scope).map(([context, row]) => ({
  context,
  total: row.total,
  left_before_right: row.left_before_right,
  right_before_left: row.right_before_left,
  left_before_share: row.left_before_share,
  examples: row.examples.join(' | '),
})), [
  'context',
  'total',
  'left_before_right',
  'right_before_left',
  'left_before_share',
  'examples',
]);
writeCsv(path.join(REPORTS, `${OUT_PREFIX}_806_examples.csv`), profile806.examples, [
  'sign',
  'object',
  'site',
  'type',
  'symbol',
  'context',
  'role',
  'prev',
  'next',
  'text',
]);

console.log(JSON.stringify({
  run_date_time: output.run_date_time,
  phase: output.phase,
  minimal_model: output.minimal_model,
  top_decisions: decisions.slice(0, 8),
  cross_site_backbone_prediction: output.cross_site_backbone_prediction,
  family_collapse_backbone: output.family_collapse_backbone,
  length_strata_backbone: output.length_strata_backbone,
  edge_status_after_consolidation: output.edge_status_after_consolidation,
  backbone_slice_controls: backboneSlices.map((row) => ({
    slice: row.slice,
    usable_constraints: row.usable_constraints,
    passed_constraints: row.passed_constraints,
    satisfied_rows: row.satisfied_rows,
    total_rows: row.total_rows,
    satisfied_share: row.satisfied_share,
    failing_constraints: row.details.filter((detail) => !detail.passed).map((detail) => `${detail.id}:${detail.satisfied}/${detail.total}`),
  })),
  contradiction_tests: contradictionTests,
  next_destructive_tests: nextDestructiveTests,
}, null, 2));
