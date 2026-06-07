import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const REPORT_DIR = path.join(ROOT, 'data', 'open_prototype', 'reports');
const OUT = path.join(REPORT_DIR, 'consolidate_expand_batch_20260531_1730.json');

function readJson(name) {
  return JSON.parse(fs.readFileSync(path.join(REPORT_DIR, name), 'utf8'));
}

const unicity = readJson('risky_terminal_governor_unicity_delta_20260531.json');
const copper = readJson('risky_copper_register_subsigns_095_845_20260531.json');
const copperPeek = readJson('risky_095_copper_subregister_source_peek_20260531.json');
const copperFamily = readJson('risky_095_copper_family_stress_20260531.json');
const bull = readJson('risky_405806_bull1w_icon_subtype_forger_20260531.json');
const damage = readJson('risky_terminal_governor_damage_source_expansion_20260531.json');
const external390 = readJson('risky_390_external_personnel_register_maxstat_20260531.json');
const blockStress = readJson('risky_terminal_governor_unicity_block_stress_20260531.json');
const frameStress = readJson('risky_740x590_filler_context_stress_20260531.json');
const bullFrameStress = readJson('risky_405806_bull1w_frame_confound_stress_20260531.json');
const bullSourcePeek = readJson('risky_806_nonharappa_bull1w_source_peek_20260531.json');
const frequencyConfound = readJson('risky_terminal_governor_frequency_confound_check_20260531.json');

function targetRow(report, target, panel = 0) {
  return report.panels[panel].target_rows.find((row) => row.target === target);
}

function liveTarget(unit) {
  return copper.live_targets.find((row) => row.unit === unit);
}

const report = {
  date: '2026-05-31',
  phase: 'CONSOLIDATE',
  wall_clock: '2026-05-31 17:30 America/Los_Angeles',
  candidate_id: 'consolidate_expand_batch_20260531_1730',
  smallest_model: {
    tier: 'promoted candidate cluster, not accepted',
    statement:
      'The live model is a register grammar, not a phonetic reading: 002/060 act as terminal governors whose final closures create real local unicity pressure; 095 marks a fragile independent copper TAB:C subregister; 405/806 mark a Bull1:W square-seal subtype with a Harappa-weighted distribution. The 740-X-590 frame is now demoted to repeated syntax only; its attempted semantic filler split failed.',
    carried_bets: [
      'terminal_governor_unicity_pressure',
      '095_independent_copper_subregister',
      '405806_bull1w_square_seal_subtype',
      '740_X_590_register_slot_frame_wild_shot',
    ],
    excluded_bets: [
      '390_external_personnel_or_title_register',
      '055_to_brahmi_ra_descent',
      'damaged_002000_terminal_resolution',
    ],
  },
  ranked_survivors: [
    {
      rank: 1,
      tier: 'candidate strengthening promoted terminal-governor model',
      bet: '002/060 terminal governors create effective-unicity pressure in the final slot.',
      evidence: {
        leave_site_text_family_rows: unicity.evaluation.observed_target_governors.evaluated_rows,
        target_top1_accuracy: unicity.evaluation.observed_target_governors.top1_accuracy,
        target_top3_accuracy: unicity.evaluation.observed_target_governors.top3_accuracy,
        non_target_top3_accuracy: unicity.evaluation.observed_non_target_penults.top3_accuracy,
        target_mean_effective_candidates: unicity.evaluation.observed_target_governors.mean_effective_candidates,
        non_target_mean_effective_candidates: unicity.evaluation.observed_non_target_penults.mean_effective_candidates,
        final_label_shuffle: {
          iterations: unicity.final_label_shuffle_null.iterations,
          p_ge_top1: unicity.final_label_shuffle_null.p_ge_target_top1_accuracy,
          p_ge_top3: unicity.final_label_shuffle_null.p_ge_target_top3_accuracy,
          p_le_effective_candidates: unicity.final_label_shuffle_null.p_le_target_mean_effective_candidates,
          p_ge_surprisal_delta: unicity.final_label_shuffle_null.p_ge_target_mean_surprisal_delta_bits,
        },
        block_stress: {
          decision: blockStress.decision,
          panels: blockStress.panels.map((panel) => ({
            id: panel.id,
            target_rows: panel.target.evaluated_rows,
            target_top3: panel.target.top3_accuracy,
            target_effective_candidates: panel.target.mean_effective_candidates,
            non_target_top3: panel.non_target.top3_accuracy,
            null_iterations: panel.final_label_shuffle_null.iterations,
            p_ge_target_top3: panel.final_label_shuffle_null.p_ge_target_top3_accuracy,
          })),
        },
        frequency_confound_check: {
          decision: frequencyConfound.decision,
          high_support_non_targets: frequencyConfound.high_support_non_target_penults,
          low_support_warning: frequencyConfound.low_support_warning,
        },
      },
      decision: 'keep as live Vector 2 structural candidate; no phonetic/language-family claim',
      next_destructive_test:
        'Rerun block stress at higher iterations and add source-family collapse; demote if top3/effective-candidate advantage disappears after source-token boxing.',
    },
    {
      rank: 2,
      tier: 'candidate',
      bet: '095 is an independent copper TAB:C subregister sign, not merely a 407 passenger.',
      evidence: {
        total_095: liveTarget('095')?.unit_rows,
        copper_tab_c_095: liveTarget('095')?.support,
        without_407_support: liveTarget('095')?.without_407?.support,
        without_407_total_095: liveTarget('095')?.without_407?.unit_rows,
        source_visible_non407_witnesses: copperPeek.source_peek?.length ?? 0,
        family_stress: {
          decision: copperFamily.decision,
          non407_object_rows: copperFamily.support.non407_count,
          non407_exact_text_families: copperFamily.support.non407_exact_text_family_count,
          non407_prefix_families: copperFamily.support.non407_prefix_family_count,
          non407_local_families: copperFamily.support.non407_local_family_count,
        },
        decision: copperPeek.decision,
      },
      decision: 'keep within candidate tier but mark fragile; keep 845 as 407-dependent',
      next_destructive_test:
        'Source-family collapse of the 617-142-001-595-095 cluster; if M-519/M-520/M-1470 are one source family and M-599 is the only independent frame, demote 095 to frame-local variant.',
    },
    {
      rank: 3,
      tier: 'candidate, Harappa-weighted',
      bet: '405/806 mark a Bull1:W square-seal subtype/register.',
      evidence: {
        summary: bull.observed,
        skeptic_verdict: bull.skeptic_verdict,
        frame_confound_stress: {
          decision: bullFrameStress.decision,
          panels: bullFrameStress.panels.map((panel) => ({
            id: panel.id,
            rows: panel.rows,
            bull1w_rows: panel.bull1w_rows,
            sign405: panel.stats['405'],
            sign806: panel.stats['806'],
            either: panel.stats.either,
          })),
        },
        nonharappa_806_source_peek: {
          decision: bullSourcePeek.decision,
          checked_rows: bullSourcePeek.support_rows_from_metadata.filter((row) => row.image_path).length,
          unrouted_or_unusable_rows: bullSourcePeek.support_rows_from_metadata.filter((row) => !row.image_path || row.source_status.includes('poor/incomplete')).length,
          skeptic_note: bullSourcePeek.skeptic_note,
        },
      },
      decision:
        'keep as candidate but split strength: 806 carries the hardest non-Harappa/frame survival; 405 remains a weaker partner',
      next_destructive_test:
        'Source-verify non-Harappa Bull1:W square seals carrying 806 and matched non-Bull1:W square controls; demote 405 first if source checks or harder controls keep it below maxstat threshold.',
    },
    {
      rank: 4,
      tier: 'wild shot demoted',
      bet: '740-X-590 is a repeated syntactic slot frame; the stronger claim that X cleanly selects the predicted semantic context class is not supported.',
      evidence: {
        frame_stress_decision: frameStress.decision,
        exact_text_counts: frameStress.counts,
        top_390_contexts: frameStress.filler_context_stats['390']?.slice(0, 5),
        top_405_contexts: frameStress.filler_context_stats['405']?.slice(0, 5),
        top_407_contexts: frameStress.filler_context_stats['407']?.slice(0, 5),
        external_390_note:
          'The external-personnel version of 390 failed max-stat, so 390 may remain only as an internal frame filler until retested.',
      },
      decision: 'demote semantic/context-sorted version; carry only as syntax-frequency wild shot',
      next_destructive_test:
        'Only reopen if a stricter syntactic test shows the frame predicts neighboring signs or terminal closures better than matched 740/590 controls.',
    },
  ],
  killed_or_demoted_this_window: [
    {
      bet: '390 is an external Meluhha personnel/title register marker.',
      prior_tier: 'wild shot',
      decision: 'killed as external bridge; optionally reusable only as an internal 740-X-590 filler',
      evidence: {
        main_390: targetRow(external390, '390'),
        leave_kish_390: targetRow(external390, '390', 1),
        leave_gonur_390: targetRow(external390, '390', 2),
        main_740390: targetRow(external390, '740-390'),
        main_390590: targetRow(external390, '390-590'),
      },
      reason:
        'Raw enrichment loses under all-feature max-stat and leaves no robust Kish/Gonur-independent external signal.',
    },
    {
      bet: '055 descends to Brahmi ra.',
      prior_tier: 'wild shot',
      decision: 'killed',
      evidence:
        'Subagent source audit: 11/11 nearest-neighbor ra was a high-collision vertical-stroke attractor; shape-null 0.097727 and only two object families.',
      reason:
        'Fails the <=0.01 shape-null bar and is orientation/source-support sensitive.',
    },
    {
      bet: 'Damaged 002-000 rows adjudicate terminal closure predictions now.',
      prior_tier: 'wild shot unresolved',
      decision: damage.decision,
      evidence: 'No checked damaged source image gave a clean terminal-slot assignment without over-reading.',
      reason: 'No promotion or demotion; keep the model unchanged.',
    },
    {
      bet: '845 is an independent copper subregister marker.',
      prior_tier: 'candidate screen',
      decision: 'demoted to 407-dependent passenger',
      evidence: {
        total_845: liveTarget('845')?.unit_rows,
        copper_tab_c_845: liveTarget('845')?.support,
        without_407_support: liveTarget('845')?.without_407?.support,
        without_407_total_845: liveTarget('845')?.without_407?.unit_rows,
      },
      reason: 'The signal vanishes when 407 rows are removed.',
    },
  ],
  contradictions_to_resolve: [
    {
      contradiction:
        '405 is both part of the Bull1:W subtype candidate and a filler in the 740-X-590 frame.',
      resolution_for_now:
        'Do not use the frame to support the Bull1:W candidate. The frame-internal 405 context skew is SEAL:R/None, not Bull1:W; this forces a split between standalone 405/806 icon-subtype behavior and 740-405-590 frame behavior.',
    },
    {
      contradiction:
        '390 failed external-personnel max-stat but is the most common 740-X-590 filler.',
      resolution_for_now:
        'Kill the external/personnel semantics. The frame stress says 390 is mostly square/SEAL:S inside this frame, not a readable Meluhha title bridge.',
    },
    {
      contradiction:
        'Terminal-governor unicity is strong but non-target penults show larger mean surprisal delta.',
      resolution_for_now:
        'Use top-k accuracy and effective-candidate collapse as the carried signal, not surprisal delta alone; rerun source-family and leave-block stress before promotion.',
    },
  ],
  next_expand_tests: [
    'Reopen 740-X-590 only with a syntactic-neighbor prediction test; the semantic filler-context version is demoted.',
    'Rerun terminal-governor unicity block stress at higher iterations, then add source-family/source-token collapse.',
    'Run 095 source-family collapse and duplicate-family stress over the three non-407 witnesses.',
    'Run non-Harappa source audit for 405/806 Bull1:W square seals and matched controls.',
  ],
  acceptance_status:
    'No new accepted claim. The strongest newly promoted object is a candidate-level structural/effective-unicity result local to terminal governors.',
};

fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
  candidate_id: report.candidate_id,
  smallest_model: report.smallest_model.statement,
  ranked_survivors: report.ranked_survivors.map((row) => ({
    rank: row.rank,
    tier: row.tier,
    bet: row.bet,
    decision: row.decision,
  })),
  killed_or_demoted: report.killed_or_demoted_this_window.map((row) => ({
    bet: row.bet,
    decision: row.decision,
  })),
}, null, 2));
