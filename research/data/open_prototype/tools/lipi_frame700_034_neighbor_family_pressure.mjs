import fs from 'node:fs';
import path from 'node:path';

const base = process.cwd();
const reportsDir = path.join(base, 'data', 'open_prototype', 'reports');
const metadataPath = path.join(base, 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv');
const outCsv = path.join(reportsDir, 'lipi_frame700_034_neighbor_family_pressure.csv');
const outJson = path.join(reportsDir, 'lipi_frame700_034_neighbor_family_pressure_summary.json');

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

function classShort(texts) {
  const joined = texts.join('|');
  for (const code of ['032', '033', '034']) {
    if (joined.includes(`+700-${code}+`) || joined.includes(`+${code}-700+`)) return code;
  }
  return '';
}

function cleanJoin(items, limit = 12) {
  const unique = [...new Set(items.filter(Boolean))];
  if (unique.length <= limit) return unique.join(';');
  return `${unique.slice(0, limit).join(';')};...(+${unique.length - limit})`;
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

function signatureFor(rows) {
  return rows
    .slice()
    .sort((a, b) => sideIndex(a.id) - sideIndex(b.id))
    .map((row) => `${sideIndex(row.id)}:${row.text}`)
    .join('|');
}

function unorderedSignatureFor(rows) {
  return rows
    .map((row) => row.text)
    .sort((a, b) => a.localeCompare(b))
    .join('|');
}

function compactObject(groupRows) {
  const first = groupRows[0];
  const ordered = groupRows.slice().sort((a, b) => sideIndex(a.id) - sideIndex(b.id));
  const texts = ordered.map((row) => row.text);
  const sideCount = Number(first.sides) || ordered.length;
  return {
    cisi: first.cisi,
    h_number: cisiNumber(first.cisi),
    ids: ordered.map((row) => row.id).join(';'),
    type: first.type,
    material: first.material,
    shape: first.shape,
    cross_section: first['cross-section'],
    preservation: first.preservation,
    condition: first.condition,
    sides: sideCount,
    area: first['area-section'],
    grid: first['room-grid'],
    period: first.time,
    phase: first.phase,
    stratum: first.stratum,
    depth: first.depth,
    excavation_id: first['excavation-idno'],
    dimensions: `${first['horizontal(mm)'] || ''}x${first['vertical(mm)'] || ''}x${first['thickness(mm)'] || ''}`,
    signature: signatureFor(ordered),
    unordered_signature: unorderedSignatureFor(ordered),
    texts,
    short_class: classShort(texts),
    companion_texts: texts.filter((text) => !/^\+(700-(032|033|034)|(032|033|034)-700)\+$/.test(text)),
  };
}

const targetConfig = [
  {
    cisi: 'H-771',
    lane: 'independent_low_copy_H771_H789_H1123',
    source_blocker: 'same-side photo selection for A/A bis/A ter/A quater plus B',
  },
  {
    cisi: 'H-789',
    lane: 'independent_low_copy_H771_H789_H1123',
    source_blocker: 'clean control only; subtype and direction still unaccepted',
  },
  {
    cisi: 'H-1123',
    lane: 'independent_low_copy_H771_H789_H1123',
    source_blocker: 'source page absent in checked IA CISI vol.1/2 OCR',
  },
  {
    cisi: 'H-893',
    lane: 'strict_local_H893_H925_H930',
    source_blocker: 'unresolved H-893 (1) A/B object-number group',
  },
  {
    cisi: 'H-925',
    lane: 'strict_local_H893_H925_H930',
    source_blocker: 'unresolved H-925 (1)/(2) A/B plus bis/ter photo witnesses',
  },
  {
    cisi: 'H-930',
    lane: 'strict_local_H893_H925_H930',
    source_blocker: 'clean control only; subtype and direction still unaccepted',
  },
  {
    cisi: 'H-983',
    lane: 'visual_local_H983_H353_H2211',
    source_blocker: 'true source C-side hazard plus B/C photo witnesses',
  },
  {
    cisi: 'H-353',
    lane: 'visual_local_H983_H353_H2211',
    source_blocker: 'true source C-side hazard against local two-row packet',
  },
  {
    cisi: 'H-2211',
    lane: 'visual_local_H983_H353_H2211',
    source_blocker: 'CISI 3.1/archive source route pending',
  },
];

const metadataRows = csvObjects(fs.readFileSync(metadataPath, 'utf8')).filter(
  (row) => row.cisi && row.cisi !== '-' && row.text && row.text !== '-',
);
const objectGroups = groupBy(metadataRows, (row) => row.cisi);
const objects = [...objectGroups.values()].map(compactObject).filter((object) => object.h_number !== null);

const byCisi = new Map(objects.map((object) => [object.cisi, object]));
const byExactSignature = groupBy(objects, (object) => object.signature);
const byUnorderedSignature = groupBy(objects, (object) => object.unordered_signature);
const byCompanionText = groupBy(
  objects.flatMap((object) =>
    object.companion_texts.map((text) => ({
      cisi: object.cisi,
      text,
    })),
  ),
  (row) => row.text,
);
const byShortClass = groupBy(
  objects.filter((object) => object.short_class),
  (object) => `${object.type}|${object.shape}|${object.short_class}`,
);

function neighborObjects(target, radius = 5) {
  return objects
    .filter(
      (object) =>
        object.cisi !== target.cisi &&
        object.h_number !== null &&
        Math.abs(object.h_number - target.h_number) <= radius,
    )
    .sort((a, b) => a.h_number - b.h_number);
}

function overlapScore(a, b) {
  const aTokens = new Set(a.texts.flatMap(tokens));
  const bTokens = new Set(b.texts.flatMap(tokens));
  let overlap = 0;
  for (const token of aTokens) if (bTokens.has(token)) overlap++;
  return overlap;
}

function pressureClass({ exactFamily, unorderedFamily, companionObjects, neighborsWithOverlap }) {
  if (exactFamily.length >= 10) return 'high_repetition_family_pressure';
  if (exactFamily.length >= 3) return 'exact_copy_family_pressure';
  if (unorderedFamily.length >= 3) return 'side_order_or_copy_family_pressure';
  if (companionObjects.length >= 5) return 'companion_context_repetition_pressure';
  if (neighborsWithOverlap.length >= 3) return 'local_neighborhood_pressure';
  return 'low_copy_or_isolated_in_local_layer';
}

const rows = targetConfig.map((target) => {
  const object = byCisi.get(target.cisi);
  if (!object) {
    return {
      checked_date: '2026-05-25',
      lane: target.lane,
      cisi: target.cisi,
      local_signature: 'missing_from_metadata_filtered',
      type: '',
      material: '',
      shape: '',
      sides: '',
      depth: '',
      excavation_id: '',
      exact_signature_family_count: 0,
      exact_signature_family_objects: '',
      unordered_signature_family_count: 0,
      unordered_signature_family_objects: '',
      companion_family_objects: '',
      type_shape_short_family_count: 0,
      type_shape_short_family_objects: '',
      h_number_neighbor_overlap_objects: '',
      local_family_pressure: 'missing_target',
      source_blocker: target.source_blocker,
      source_request_implication: 'restore target row before source comparison',
      accepted_decipherment_claim: '0',
    };
  }

  const exactFamily = byExactSignature.get(object.signature) ?? [];
  const unorderedFamily = byUnorderedSignature.get(object.unordered_signature) ?? [];
  const companionObjects = [
    ...new Set(
      object.companion_texts.flatMap((text) => (byCompanionText.get(text) ?? []).map((row) => row.cisi)),
    ),
  ]
    .map((cisi) => byCisi.get(cisi))
    .filter(Boolean);
  const shortFamily = byShortClass.get(`${object.type}|${object.shape}|${object.short_class}`) ?? [];
  const neighborsWithOverlap = neighborObjects(object)
    .map((neighbor) => ({
      neighbor,
      overlap: overlapScore(object, neighbor),
    }))
    .filter(({ neighbor, overlap }) => overlap >= 2 || object.short_class === neighbor.short_class);

  const localFamilyPressure = pressureClass({
    exactFamily,
    unorderedFamily,
    companionObjects,
    neighborsWithOverlap,
  });

  let sourceRequestImplication =
    'source note still required; local repetition is not source validation';
  if (localFamilyPressure === 'high_repetition_family_pressure') {
    sourceRequestImplication =
      'treat as copy-family contaminated until source notes prove which side/panel is comparable';
  } else if (localFamilyPressure === 'exact_copy_family_pressure') {
    sourceRequestImplication =
      'request group-level source notes, not just the single target object';
  } else if (localFamilyPressure === 'low_copy_or_isolated_in_local_layer') {
    sourceRequestImplication =
      'prioritize object-specific source note because local layer gives little family rescue or cross-check';
  }

  return {
    checked_date: '2026-05-25',
    lane: target.lane,
    cisi: object.cisi,
    local_signature: object.signature,
    type: object.type,
    material: object.material,
    shape: object.shape,
    sides: object.sides,
    depth: object.depth,
    excavation_id: object.excavation_id,
    exact_signature_family_count: exactFamily.length,
    exact_signature_family_objects: cleanJoin(exactFamily.map((item) => item.cisi)),
    unordered_signature_family_count: unorderedFamily.length,
    unordered_signature_family_objects: cleanJoin(unorderedFamily.map((item) => item.cisi)),
    companion_family_objects: cleanJoin(companionObjects.map((item) => item.cisi), 20),
    type_shape_short_family_count: shortFamily.length,
    type_shape_short_family_objects: cleanJoin(shortFamily.map((item) => item.cisi), 20),
    h_number_neighbor_overlap_objects: cleanJoin(
      neighborsWithOverlap.map(({ neighbor, overlap }) => `${neighbor.cisi}(overlap_${overlap})`),
      12,
    ),
    local_family_pressure: localFamilyPressure,
    source_blocker: target.source_blocker,
    source_request_implication: sourceRequestImplication,
    accepted_decipherment_claim: '0',
  };
});

const summary = {
  checked_date: '2026-05-25',
  artifact: 'lipi_frame700_034_neighbor_family_pressure',
  target_objects: rows.length,
  exact_copy_family_pressure_objects: rows.filter(
    (row) => row.local_family_pressure === 'exact_copy_family_pressure',
  ).length,
  high_repetition_family_pressure_objects: rows.filter(
    (row) => row.local_family_pressure === 'high_repetition_family_pressure',
  ).length,
  companion_context_repetition_pressure_objects: rows.filter(
    (row) => row.local_family_pressure === 'companion_context_repetition_pressure',
  ).length,
  local_neighborhood_pressure_objects: rows.filter(
    (row) => row.local_family_pressure === 'local_neighborhood_pressure',
  ).length,
  low_copy_or_isolated_objects: rows.filter(
    (row) => row.local_family_pressure === 'low_copy_or_isolated_in_local_layer',
  ).length,
  lane_pressure: Object.fromEntries(
    [...new Set(rows.map((row) => row.lane))].map((lane) => [
      lane,
      rows
        .filter((row) => row.lane === lane)
        .map((row) => `${row.cisi}:${row.local_family_pressure}`)
        .join(';'),
    ]),
  ),
  accepted_decipherment_claims: rows.filter((row) => row.accepted_decipherment_claim !== '0')
    .length,
  research_conclusion:
    'Local metadata does not rescue any source blocker. H-925 and H-353 sit inside repeated/copy-family pressure; H-771/H-789/H-893/H-930/H-983/H-2211 show local-neighborhood pressure; only H-1123 stays low-copy/isolated. These are source-request priorities, not readings.',
};

fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(outCsv, toCsv(rows), 'utf8');
fs.writeFileSync(outJson, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(summary, null, 2));
