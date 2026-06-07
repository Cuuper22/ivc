import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORTS = path.join(ROOT, 'data', 'open_prototype', 'reports');
const INPUT_ROWS = path.join(REPORTS, 'campaign_032_002_post_y_all_002_rows.csv');
const SOURCE_INDEX = path.join(REPORTS, 'effective_unicity_directionality_source_queue_source_index.csv');
const BRANCH_GAP_SOURCE_STATUS = path.join(REPORTS, 'campaign_002_y_branch_gap_public_source_status.csv');
const OUT_QUEUE = path.join(REPORTS, 'campaign_002_y_partition_source_queue.csv');
const OUT_BY_SIGN = path.join(REPORTS, 'campaign_002_y_partition_source_queue_by_sign.csv');
const OUT_SUMMARY = path.join(REPORTS, 'campaign_002_y_partition_source_queue_summary.json');

const RUN_DATE = '2026-05-29';
const CLOSURE_POLE = new Set(['817', '820']);
const BRANCH_POLE = new Set(['390', '368', '031', '220']);
const LEAKY_CLOSURE = new Set(['861']);

const QUEUE_FIELDS = [
  'rank',
  'queue_bucket',
  'partition_class',
  'y_after_002',
  'y_terminal',
  'post_y_len',
  'cisi',
  'id',
  'site',
  'type',
  'symbol',
  'material',
  'condition',
  'dir',
  'idx_002',
  'prev2_before_002',
  'prev1_before_002',
  'next1_after_y',
  'next2_after_y',
  'text',
  'source_grade',
  'source_grade_label',
  'source_hint_count',
  'best_source_rank',
  'best_source_file',
  'best_status_text',
  'best_source_url',
  'best_local_image',
  'best_sha256',
  'best_note',
  'source_files',
  'queue_reason',
];

const BY_SIGN_FIELDS = [
  'partition_class',
  'y_after_002',
  'rows',
  'terminal_rows',
  'terminal_rate',
  'source_index_rows',
  'source_grade_4_rows',
  'source_grade_3_rows',
  'source_grade_2_rows',
  'source_grade_1_rows',
  'source_grade_0_rows',
  'best_cisis',
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

function norm(value) {
  const text = String(value ?? '').trim();
  return text && text !== '-' ? text : 'NA';
}

function loadStrictDedupRows() {
  const seen = new Set();
  const rows = [];
  for (const row of parseCsv(fs.readFileSync(INPUT_ROWS, 'utf8'))) {
    if (row.strict_complete_closed !== 'true') continue;
    const key = [row.text_dedup_key, row.site, row.type, row.idx_002].join('\u241f');
    if (seen.has(key)) continue;
    seen.add(key);
    rows.push(row);
  }
  return rows;
}

function partitionClass(y) {
  if (CLOSURE_POLE.has(y)) return 'posthoc_closure_pole';
  if (BRANCH_POLE.has(y)) return 'posthoc_branch_pole';
  if (LEAKY_CLOSURE.has(y)) return 'leaky_861_descriptive_not_posthoc_pole';
  return 'other_y_after_002';
}

function sourceGrade(source) {
  if (!source) {
    return { grade: 0, label: 'source_dark_or_unindexed' };
  }
  const status = `${source.best_status_text ?? ''} ${source.best_source_file ?? ''}`.toLowerCase();
  const rank = Number.parseFloat(source.best_source_rank || '0');
  const hasLocal = Boolean(String(source.best_local_image ?? '').trim());
  const sourceHintCount = Number.parseInt(source.source_hint_count || '0', 10);
  if (rank >= 85 && status.includes('source_single_line:yes') && status.includes('pass')) {
    return { grade: 4, label: 'source_visible_order_window_candidate' };
  }
  if (
    rank >= 80 &&
    (
      status.includes('source_visible') ||
      status.includes('same_line_candidate') ||
      status.includes('chanhu_daro_plate_route')
    )
  ) {
    return { grade: 3, label: 'row_level_source_visible_candidate' };
  }
  if (hasLocal || rank >= 65) {
    return { grade: 2, label: 'local_image_or_public_route_candidate' };
  }
  if (sourceHintCount > 0) {
    return { grade: 1, label: 'source_hint_only' };
  }
  return { grade: 0, label: 'source_dark_or_unindexed' };
}

function sourceGradeScore(source) {
  const grade = sourceGrade(source);
  const rank = Number.parseFloat(source?.best_source_rank || '0');
  const sourceHintCount = Number.parseInt(source?.source_hint_count || '0', 10);
  return grade.grade * 100000 + rank * 100 + sourceHintCount;
}

function mergeSource(sourceByCisi, source) {
  const cisi = source?.cisi;
  if (!cisi) return;
  const current = sourceByCisi.get(cisi);
  if (!current || sourceGradeScore(source) > sourceGradeScore(current)) {
    sourceByCisi.set(cisi, source);
  }
}

function loadSupplementalBranchGapSources() {
  if (!fs.existsSync(BRANCH_GAP_SOURCE_STATUS)) return [];
  return parseCsv(fs.readFileSync(BRANCH_GAP_SOURCE_STATUS, 'utf8'))
    .filter((row) => row.source_status_rank === 'public_cisi_plate_route_candidate')
    .map((row) => ({
      cisi: row.cisi,
      source_hint_count: row.route_count || '1',
      best_source_rank: '65',
      best_source_file: 'campaign_002_y_branch_gap_public_source_status.csv',
      best_status_text:
        `${row.source_status_rank} | ${row.current_admissible_use} | ${row.blocker}`,
      best_source_url: row.best_source_url,
      best_local_image: row.best_local_artifact,
      best_sha256: row.best_artifact_sha256,
      best_note:
        `Supplemental public CISI route for branch-pole gap sign ${row.y_after_002}; not token-boxed or source-normalized.`,
      source_files:
        'campaign_002_y_branch_gap_public_routes.csv;campaign_002_y_branch_gap_public_source_status.csv;campaign_002_y_branch_gap_public_source_summary.json',
    }));
}

function queueBucket(row, grade) {
  if (row.partition_class === 'posthoc_branch_pole' && grade < 2) return 'priority_gap_branch_pole_source_dark';
  if (row.partition_class === 'posthoc_branch_pole' && grade >= 2) return 'priority_branch_pole_source_check';
  if (row.partition_class === 'posthoc_closure_pole' && grade >= 2) return 'closure_pole_source_check';
  if (row.partition_class === 'posthoc_closure_pole') return 'closure_pole_route_needed';
  if (row.partition_class.startsWith('leaky_861') && grade >= 2) return 'leaky_861_source_context';
  return 'background_context';
}

function queueReason(row, source) {
  if (row.partition_class === 'posthoc_branch_pole' && row.source_grade < 2) {
    return `Branch-pole sign ${row.y_after_002} lacks local-image/public-route coverage in the current source index; acquire source evidence before source-normalized partition testing.`;
  }
  if (row.partition_class === 'posthoc_branch_pole') {
    return `Branch-pole sign ${row.y_after_002} has existing source evidence and should be used to avoid overfitting the branch pole to metadata only.`;
  }
  if (row.partition_class === 'posthoc_closure_pole') {
    return `Closure-pole sign ${row.y_after_002} should be paired with branch-pole rows under comparable site/type/symbol/length conditions.`;
  }
  if (row.partition_class.startsWith('leaky_861')) {
    return '861 is closure-heavy but not part of the strict post-hoc pole; keep it as a leaky-background stressor, not as closure-pole support.';
  }
  if (source) return 'Background 002-Y row with some source-route pressure; useful only as a matched control.';
  return 'Background 002-Y row with no immediate source route.';
}

function sortQueue(a, b) {
  const bucketPriority = {
    priority_branch_pole_source_check: 0,
    priority_gap_branch_pole_source_dark: 1,
    closure_pole_source_check: 2,
    closure_pole_route_needed: 3,
    leaky_861_source_context: 4,
    background_context: 5,
  };
  return (
    (bucketPriority[a.queue_bucket] ?? 9) - (bucketPriority[b.queue_bucket] ?? 9) ||
    b.source_grade - a.source_grade ||
    Number(b.source_hint_count || 0) - Number(a.source_hint_count || 0) ||
    a.y_after_002.localeCompare(b.y_after_002) ||
    a.cisi.localeCompare(b.cisi)
  );
}

function summarizeBySign(rows) {
  const groups = new Map();
  for (const row of rows) {
    const key = `${row.partition_class}\t${row.y_after_002}`;
    const current = groups.get(key) ?? [];
    current.push(row);
    groups.set(key, current);
  }
  return [...groups.entries()].map(([key, members]) => {
    const [klass, y] = key.split('\t');
    const terminalRows = members.filter((row) => row.y_terminal === 'true').length;
    const gradeCount = (grade) => members.filter((row) => Number(row.source_grade) === grade).length;
    return {
      partition_class: klass,
      y_after_002: y,
      rows: members.length,
      terminal_rows: terminalRows,
      terminal_rate: members.length ? Number((terminalRows / members.length).toFixed(6)) : 0,
      source_index_rows: members.filter((row) => Number(row.source_hint_count || 0) > 0).length,
      source_grade_4_rows: gradeCount(4),
      source_grade_3_rows: gradeCount(3),
      source_grade_2_rows: gradeCount(2),
      source_grade_1_rows: gradeCount(1),
      source_grade_0_rows: gradeCount(0),
      best_cisis: members
        .slice()
        .sort((a, b) => b.source_grade - a.source_grade || Number(b.source_hint_count || 0) - Number(a.source_hint_count || 0))
        .slice(0, 10)
        .map((row) => `${row.cisi}:${row.source_grade_label}`)
        .join(';'),
    };
  }).sort((a, b) =>
    a.partition_class.localeCompare(b.partition_class) ||
    b.rows - a.rows ||
    a.y_after_002.localeCompare(b.y_after_002)
  );
}

function main() {
  const sourceRows = parseCsv(fs.readFileSync(SOURCE_INDEX, 'utf8'));
  const sourceByCisi = new Map();
  for (const row of sourceRows) mergeSource(sourceByCisi, row);
  for (const row of loadSupplementalBranchGapSources()) mergeSource(sourceByCisi, row);
  const rows = loadStrictDedupRows().map((row) => {
    const source = sourceByCisi.get(row.cisi);
    const grade = sourceGrade(source);
    const enriched = {
      partition_class: partitionClass(row.y_after_002),
      y_after_002: row.y_after_002,
      y_terminal: row.y_terminal,
      post_y_len: row.post_y_len,
      cisi: norm(row.cisi),
      id: row.id,
      site: norm(row.site),
      type: norm(row.type),
      symbol: norm(row.symbol),
      material: norm(row.material),
      condition: norm(row.condition),
      dir: norm(row.dir),
      idx_002: row.idx_002,
      prev2_before_002: row.prev2_before_002,
      prev1_before_002: row.prev1_before_002,
      next1_after_y: row.next1_after_y,
      next2_after_y: row.next2_after_y,
      text: row.text,
      source_grade: grade.grade,
      source_grade_label: grade.label,
      source_hint_count: source?.source_hint_count ?? 0,
      best_source_rank: source?.best_source_rank ?? '',
      best_source_file: source?.best_source_file ?? '',
      best_status_text: source?.best_status_text ?? '',
      best_source_url: source?.best_source_url ?? '',
      best_local_image: source?.best_local_image ?? '',
      best_sha256: source?.best_sha256 ?? '',
      best_note: source?.best_note ?? '',
      source_files: source?.source_files ?? '',
    };
    enriched.queue_bucket = queueBucket(enriched, grade.grade);
    enriched.queue_reason = queueReason(enriched, source);
    return enriched;
  }).sort(sortQueue).map((row, index) => ({ rank: index + 1, ...row }));

  const bySign = summarizeBySign(rows);
  writeCsv(OUT_QUEUE, rows, QUEUE_FIELDS);
  writeCsv(OUT_BY_SIGN, bySign, BY_SIGN_FIELDS);

  const gradeCounts = {};
  const classCounts = {};
  for (const row of rows) {
    gradeCounts[row.source_grade_label] = (gradeCounts[row.source_grade_label] ?? 0) + 1;
    classCounts[row.partition_class] = (classCounts[row.partition_class] ?? 0) + 1;
  }

  const poleRows = rows.filter((row) => row.partition_class === 'posthoc_closure_pole' || row.partition_class === 'posthoc_branch_pole');
  const branchPoleBySign = bySign.filter((row) => row.partition_class === 'posthoc_branch_pole');
  const closurePoleBySign = bySign.filter((row) => row.partition_class === 'posthoc_closure_pole');
  const summary = {
    date: RUN_DATE,
    purpose: 'Source-normalization queue for the broad all-002 post-hoc closure/branch partition.',
    input: 'data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv',
    source_index: 'data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv',
    supplemental_source_status: fs.existsSync(BRANCH_GAP_SOURCE_STATUS)
      ? 'data/open_prototype/reports/campaign_002_y_branch_gap_public_source_status.csv'
      : '',
    scope:
      'strict_complete_closed rows deduplicated by text_dedup_key + site + type + idx_002, matching the post-hoc partition forger.',
    partition: {
      closure_pole: [...CLOSURE_POLE],
      branch_pole: [...BRANCH_POLE],
      leaky_background: [...LEAKY_CLOSURE],
    },
    counts: {
      rows: rows.length,
      pole_rows: poleRows.length,
      class_counts: classCounts,
      source_grade_counts: gradeCounts,
    },
    pole_source_coverage: {
      closure_by_sign: closurePoleBySign,
      branch_by_sign: branchPoleBySign,
      blocking_gap:
        branchPoleBySign
          .filter((row) => row.source_grade_4_rows + row.source_grade_3_rows + row.source_grade_2_rows === 0).length
          ? 'Some branch-pole signs still lack local-image/public-route coverage in the current source index and supplemental public-route layer.'
          : 'Supplemental public CISI route acquisition now gives grade >= 2 route hooks for every branch-pole sign, but these are route candidates only; a source-normalized proof still needs visual token boxing, physical direction checks, and matched negatives.',
    },
    top_queue_rows: rows.slice(0, 30),
    interpretation_boundary:
      'This is acquisition infrastructure only. It does not validate source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.',
    files: {
      queue_csv: path.relative(ROOT, OUT_QUEUE).replaceAll('\\', '/'),
      by_sign_csv: path.relative(ROOT, OUT_BY_SIGN).replaceAll('\\', '/'),
      summary_json: path.relative(ROOT, OUT_SUMMARY).replaceAll('\\', '/'),
    },
  };

  fs.writeFileSync(OUT_SUMMARY, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify({
    rows: rows.length,
    class_counts: classCounts,
    closure_grade_ge2: closurePoleBySign.reduce((sum, row) => sum + row.source_grade_4_rows + row.source_grade_3_rows + row.source_grade_2_rows, 0),
    branch_grade_ge2: branchPoleBySign.reduce((sum, row) => sum + row.source_grade_4_rows + row.source_grade_3_rows + row.source_grade_2_rows, 0),
    branch_gap_signs: branchPoleBySign.filter((row) => row.source_grade_4_rows + row.source_grade_3_rows + row.source_grade_2_rows === 0).map((row) => row.y_after_002),
  }, null, 2));
}

main();
