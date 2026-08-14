// A "risky bet" probe (2026-05-31, wild-shot tier): is sign 820 a shape-stable
// bridge candidate into a descendant script, distinct from its terminal partners
// 817 and 861? The script reads the v2 source-token segments and the v3
// impostor-forger rows for sign 820, then summarizes each of the three signs'
// tokens: how many crops, how many distinct CISI objects and image hashes,
// and the spread of aspect ratio and ink density. The killing observation is
// independence: all of 820's token crops come from a single CISI object (M-381),
// so the apparent Brahmi ra/tha agreement could be one object counted many
// times. It writes a single JSON report recording the verdict — not promotable
// until at least 3 independently boxed 820 tokens exist — and claims no
// phonetic value for 820.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SEGMENTS = path.join(ROOT, 'data', 'brahmi', 'source_token_segments_v2.csv');
const BRAHMI_V3 = path.join(ROOT, 'data', 'brahmi', 'brahmi_real_token_impostor_forger_v3.csv');
const OUT = path.join(ROOT, 'data', 'brahmi', 'risky_820_shape_family_descent_gate_20260531.json');
const SIGNS = ['817', '820', '861'];

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

function mean(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function stats(rows, sign) {
  const subset = rows.filter((row) => row.assigned_sign === sign);
  const aspects = subset.map((row) => Number(row.aspect)).filter(Number.isFinite);
  const densities = subset.map((row) => Number(row.ink_density)).filter(Number.isFinite);
  return {
    sign,
    token_rows: subset.length,
    unique_cisis: [...new Set(subset.map((row) => row.cisi))].sort(),
    unique_sha256_count: new Set(subset.map((row) => row.sha256)).size,
    orientation_policies: [...new Set(subset.map((row) => row.orientation_policy))].sort(),
    aspect_mean: mean(aspects),
    aspect_min: aspects.length ? Math.min(...aspects) : null,
    aspect_max: aspects.length ? Math.max(...aspects) : null,
    ink_density_mean: mean(densities),
    ink_density_min: densities.length ? Math.min(...densities) : null,
    ink_density_max: densities.length ? Math.max(...densities) : null,
    example_crops: [...new Set(subset.map((row) => row.token_crop))].slice(0, 12),
  };
}

const segments = parseCsv(fs.readFileSync(SEGMENTS, 'utf8'));
const v3Rows = parseCsv(fs.readFileSync(BRAHMI_V3, 'utf8')).filter((row) => row.sign_id === '820');
const signStats = SIGNS.map((sign) => stats(segments, sign));
const sign820 = signStats.find((row) => row.sign === '820');
const report = {
  run_date: '2026-05-31T14:19:00-07:00',
  tier: 'wild shot',
  risky_bet_tested: 'Sign 820 might be a shape-stable descendant-script bridge candidate distinct from the 817/861 terminal partners.',
  verdict: 'The local Brahmi-token route is not promotable: 820 has multiple token crops but only one CISI object (M-381), so the apparent Brahmi ra/tha agreement is a one-object token-identity artifact until independent 820 source tokens are boxed.',
  positive_residue: 'The M-381-only token packet can no longer define 820 morphology. The live positive shape bet has moved to the independently source-visible rhinoceros packet, where 820 appears as a wheel/rosette terminal sign; see data/brahmi/risky_820_rosette_rhin_source_visual_gate_20260531.json.',
  terminal_partner_token_stats: signStats,
  brahmi_v3_820_rows: v3Rows,
  destructive_checks: {
    independence: `Brahmi-token route 820 unique CISI count=${sign820.unique_cisis.length}; required for phonetic/shape promotion is >=3 independent CISI objects with stable token identity.`,
    impostor_forger: 'The existing v3 rows for 820 give raw modal Brahmi labels ra/tha but both are blocked before review and fail the real-token impostor gate.',
  },
  falsifier: 'If three or more independently source-boxed 820 tokens do not preserve a coherent shape family, or if a real-token impostor repeats the same Brahmi label/distance profile at comparable rates, kill the descent bet.',
  next_prediction: 'The next useful V3 expansion is not a value claim. It is to token-box independent 820 rosette/wheel instances from M-1136/M-1137/M-1138/M-1139 and compare them against 817/861 and the M-381 token packet.',
  non_claim: 'No Brahmi phonetic value for 820 is claimed.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  tier: report.tier,
  verdict: report.verdict,
  sign820_token_rows: sign820.token_rows,
  sign820_unique_cisis: sign820.unique_cisis,
  v3_labels: v3Rows.map((row) => `${row.orientation_policy}:${row.modal_brahmi_label}:${row.gate_decision}`),
  report: OUT,
}, null, 2));
