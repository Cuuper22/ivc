import fs from 'node:fs';
import path from 'node:path';

// This script builds a prioritized "request packet": a list of CISI catalog objects whose
// end-matter records (excavation numbers, side labels, photo notes, copy/mold notes) we still
// need before the frame700 sign-034 substitution test can proceed. It reads the local corpus
// metadata (metadata_filtered.csv), groups rows by CISI object number, and starts from nine
// hand-picked anchor objects (H-771, H-789, H-1123, H-893, H-925, H-930, H-983, H-353,
// H-2211), each with a hard-coded blocker and admissibility rule. For the two family anchors
// (H-925, H-353) it adds every object sharing the exact same per-side text signature; for
// four messy anchors it adds catalog neighbors within 5 H-numbers that share at least 2 sign
// tokens, to guard against copy-family and local-batch contamination. Output is one CSV of
// requests sorted by priority (P0/P1/P2) and one JSON summary. It requests source evidence;
// it makes no decipherment claim.

const base = process.cwd();
const metadataPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_cisi31_endmatter_request_packet.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_cisi31_endmatter_request_packet_summary.json');

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (inQuotes) {
      if (char === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
    } else if (char === '"') {
      inQuotes = true;
    } else if (char === ',') {
      row.push(field);
      field = '';
    } else if (char === '\n') {
      row.push(field);
      field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else if (char !== '\r') {
      field += char;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function csvObjects(text) {
  const rows = parseCsv(text);
  const header = rows.shift() ?? [];
  return rows.map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ''])));
}

function toCsv(rows) {
  if (rows.length === 0) return '';
  const header = Object.keys(rows[0]);
  const lines = rows.map((row) =>
    header
      .map((key) => {
        const text = String(row[key] ?? '');
        return `"${text.replaceAll('"', '""')}"`;
      })
      .join(','),
  );
  return `${[header.map((key) => `"${key}"`).join(','), ...lines].join('\n')}\n`;
}

function groupBy(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return groups;
}

function cisiNumber(cisi) {
  const match = String(cisi ?? '').match(/^H-(\d+)$/);
  return match ? Number(match[1]) : null;
}

function sideIndex(id) {
  const match = String(id ?? '').match(/\.(\d+)$/);
  return match ? Number(match[1]) : 1;
}

function tokens(text) {
  return String(text ?? '')
    .replace(/^\+|\+$/g, '')
    .split(/[-/]/)
    .filter(Boolean);
}

function signatureFor(rows) {
  return rows
    .slice()
    .sort((a, b) => sideIndex(a.id) - sideIndex(b.id))
    .map((row) => `${sideIndex(row.id)}:${row.text}`)
    .join('|');
}

function compactObject(groupRows) {
  const first = groupRows[0];
  const ordered = groupRows.slice().sort((a, b) => sideIndex(a.id) - sideIndex(b.id));
  return {
    cisi: first.cisi,
    h_number: cisiNumber(first.cisi),
    ids: ordered.map((row) => row.id).join(';'),
    local_signature: signatureFor(ordered),
    texts: ordered.map((row) => row.text),
    type: first.type,
    material: first.material,
    shape: first.shape,
    cross_section: first['cross-section'],
    preservation: first.preservation,
    condition: first.condition,
    sides: Number(first.sides) || ordered.length,
    period: first.time,
    phase: first.phase,
    stratum: first.stratum,
    depth: first.depth,
    excavation_id: first['excavation-idno'],
    dimensions: `${first['horizontal(mm)'] || ''}x${first['vertical(mm)'] || ''}x${first['thickness(mm)'] || ''}`,
  };
}

function overlapScore(a, b) {
  const aTokens = new Set(a.texts.flatMap(tokens));
  const bTokens = new Set(b.texts.flatMap(tokens));
  let overlap = 0;
  for (const token of aTokens) if (bTokens.has(token)) overlap++;
  return overlap;
}

function neighborObjects(target, objects, radius = 5) {
  return objects
    .filter(
      (object) =>
        object.cisi !== target.cisi &&
        object.h_number !== null &&
        Math.abs(object.h_number - target.h_number) <= radius &&
        overlapScore(target, object) >= 2,
    )
    .sort((a, b) => a.h_number - b.h_number);
}

const sourceFields = [
  'CISI 3.1 end-matter row',
  'excavation number',
  'museum or owner',
  'source of photograph',
  'all side labels',
  'all photo/impression labels',
  'side-order basis',
  'image or impression direction',
  'copy/mold/duplicate/family notes',
  'condition and preservation notes',
  'material/shape/dimensions',
  'findspot/period/phase/stratum/depth',
].join('; ');

const targetPlan = [
  {
    cisi: 'H-771',
    lane: 'independent_034',
    priority: 'P0',
    blocker: 'A/A bis/A ter/A quater same-side photo selection plus B',
    decision_rule:
      'Use only after one source-side node is linked to the local companion side and the B short side is separated from photo witnesses.',
  },
  {
    cisi: 'H-789',
    lane: 'independent_033_control',
    priority: 'P1',
    blocker: 'clean control; still lacks accepted subtype/direction/side-order basis',
    decision_rule:
      'Use only as calibration unless source notes independently establish side-order and direction basis.',
  },
  {
    cisi: 'H-1123',
    lane: 'independent_032',
    priority: 'P0',
    blocker: 'not page-addressable in checked IA CISI vol. 1/2 OCR',
    decision_rule:
      'Use only after source-grade side labels and all-side imagery are obtained.',
  },
  {
    cisi: 'H-893',
    lane: 'strict_local_034',
    priority: 'P0',
    blocker: 'unresolved H-893 (1) A/B object-number group',
    decision_rule:
      'Use only after base H-893 and H-893 (1) are classified as same object, copy, sub-entry, or separate artifact.',
  },
  {
    cisi: 'H-925',
    lane: 'strict_local_033_family_anchor',
    priority: 'P0',
    blocker: 'H-925 (1)/(2) A/B plus bis/ter photo witnesses and exact copy-family pressure',
    decision_rule:
      'Use only after H-326/H-924/H-925 family notes prove whether the shared 033 side is source-comparable.',
  },
  {
    cisi: 'H-930',
    lane: 'strict_local_032_control',
    priority: 'P1',
    blocker: 'clean control; local-neighborhood pressure remains non-validating',
    decision_rule:
      'Use only as calibration unless source notes establish side-order and direction basis.',
  },
  {
    cisi: 'H-983',
    lane: 'visual_local_034',
    priority: 'P0',
    blocker: 'source C-side hazard plus B/C photo witnesses',
    decision_rule:
      'Use only after C side is classified as inscriptional, iconographic, blank/edge, or intentionally excluded by source policy.',
  },
  {
    cisi: 'H-353',
    lane: 'visual_local_033_family_anchor',
    priority: 'P0',
    blocker: 'source C-side hazard inside high-repetition +400-740-176+ / +700-033+ family',
    decision_rule:
      'Use only after the repeated family notes prove which two-row packets are source-comparable and what C-side policy is being applied.',
  },
  {
    cisi: 'H-2211',
    lane: 'visual_local_032',
    priority: 'P0',
    blocker: 'CISI 3.1/archive source route pending',
    decision_rule:
      'Use only after source-normalized side labels distinguish the two 032-bearing sides and their direction basis.',
  },
];

const metadataRows = csvObjects(fs.readFileSync(metadataPath, 'utf8')).filter(
  (row) => row.cisi && row.cisi !== '-' && row.text && row.text !== '-',
);
const objects = [...groupBy(metadataRows, (row) => row.cisi).values()]
  .map(compactObject)
  .filter((object) => object.h_number !== null);
const byCisi = new Map(objects.map((object) => [object.cisi, object]));
const bySignature = groupBy(objects, (object) => object.local_signature);

function requestReason(anchor, object, relationship, blocker) {
  if (relationship === 'core_target') return blocker;
  if (relationship === 'exact_family') {
    return `${anchor.cisi} exact-signature family comparator; prevents treating copy-family repetition as independent substitution evidence.`;
  }
  if (relationship === 'local_neighborhood') {
    return `${anchor.cisi} H-number neighborhood comparator with token overlap ${overlapScore(anchor, object)}; tests catalog-adjacency and local-batch contamination.`;
  }
  return 'source context comparator';
}

const rowKeys = new Set();
const rows = [];

function addRow(anchorPlan, object, relationship, inheritedPriority = anchorPlan.priority) {
  if (!object) return;
  const anchor = byCisi.get(anchorPlan.cisi);
  const key = `${anchorPlan.cisi}|${relationship}|${object.cisi}`;
  if (rowKeys.has(key)) return;
  rowKeys.add(key);
  rows.push({
    checked_date: '2026-05-25',
    request_priority: inheritedPriority,
    anchor_object: anchorPlan.cisi,
    requested_object: object.cisi,
    relationship_to_anchor: relationship,
    lane: anchorPlan.lane,
    local_signature: object.local_signature,
    type: object.type,
    material: object.material,
    shape: object.shape,
    sides: object.sides,
    excavation_id: object.excavation_id,
    depth: object.depth,
    dimensions: object.dimensions,
    source_blocker_to_resolve: requestReason(anchor, object, relationship, anchorPlan.blocker),
    requested_source_fields: sourceFields,
    admissibility_decision_rule: anchorPlan.decision_rule,
    accepted_decipherment_claim: '0',
  });
}

for (const plan of targetPlan) {
  const anchor = byCisi.get(plan.cisi);
  addRow(plan, anchor, 'core_target', plan.priority);

  if (plan.cisi === 'H-925' || plan.cisi === 'H-353') {
    for (const familyObject of bySignature.get(anchor.local_signature) ?? []) {
      if (familyObject.cisi !== plan.cisi) addRow(plan, familyObject, 'exact_family', 'P1');
    }
  }

  if (['H-771', 'H-893', 'H-983', 'H-2211'].includes(plan.cisi)) {
    for (const neighbor of neighborObjects(anchor, objects)) {
      addRow(plan, neighbor, 'local_neighborhood', 'P2');
    }
  }
}

rows.sort((a, b) => {
  const priority = a.request_priority.localeCompare(b.request_priority);
  if (priority !== 0) return priority;
  const anchor = a.anchor_object.localeCompare(b.anchor_object, undefined, { numeric: true });
  if (anchor !== 0) return anchor;
  return a.requested_object.localeCompare(b.requested_object, undefined, { numeric: true });
});

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_frame700_034_cisi31_endmatter_request_packet',
  request_rows: rows.length,
  unique_requested_objects: new Set(rows.map((row) => row.requested_object)).size,
  p0_rows: rows.filter((row) => row.request_priority === 'P0').length,
  p1_rows: rows.filter((row) => row.request_priority === 'P1').length,
  p2_rows: rows.filter((row) => row.request_priority === 'P2').length,
  core_target_rows: rows.filter((row) => row.relationship_to_anchor === 'core_target').length,
  exact_family_rows: rows.filter((row) => row.relationship_to_anchor === 'exact_family').length,
  local_neighborhood_rows: rows.filter((row) => row.relationship_to_anchor === 'local_neighborhood').length,
  anchors: targetPlan.map((item) => item.cisi).join(';'),
  accepted_decipherment_claims: rows.filter((row) => row.accepted_decipherment_claim !== '0').length,
  research_conclusion:
    'The next source move is a family-aware CISI 3.1/end-matter request packet, not a translation claim. H-925 and H-353 require family notes; H-771/H-893/H-983/H-2211 require neighborhood-aware source controls; H-1123 remains object-specific.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(rows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
