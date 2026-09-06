from pathlib import Path
import re,json
CAM=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
spec='''1|shared/snapshot.json,evidence_inventory/source_manifest.json|Retained starting-state record plus explicit reconstruction provenance; no claim lost commits were recovered.
2|evidence_inventory/source_manifest.json,completion/sources/summary.json|Held inputs inventoried and documentary source recovered; no new archaeological samples.
3|shared/observations.jsonl,shared/foundation.py,completion/sources/summary.json|Raw object/face/line observations retained; witnesses supplement provenance.
4|shared/identity_groups.json,completion/sources/summary.json|Secure source namespaces retained; repeated texts do not prove physical copies.
5|shared/foundation.py,route_a/partial_observation_predictions.json|Retained permissive compatibility search is explicitly not a likelihood; new strict grammar does not silently impute partials.
6|shared/graphical_hypotheses.json,completion/sources/REPORT.md|Original drawings and codebook distinctions source-linked and reexamined.
7|route_d/outputs/linguistic_inventory.json,completion/route_d/summary.json|Held comparative forms retained; Tamil fish/star selection limits language competition.
8|completion/shared/common.py,completion/shared/masks.json|Whole objects and raw aliases excluded, including uncertain raw patterns; retrospective exposure explicit.
9|completion/shared/masks.json,completion/route_b/verification.json|Five recombination masks, explicit70/71-family mask, medium transfer; route-local evaluations separate.
10|shared/candidate_contract.json,candidate_ledger.json,completion/route_a/candidates.json|Contract retained, but final reconstruction candidates/dependencies must be consolidated.
11|completion/run_joint.py,completion/route_b/verification.json|Conditional original-channel factorization and normalized motif support; joint executions pending.
12|completion/route_a/mechanism_diagnostic.json,completion/route_d/controls.json|Constructed mechanism diagnostics, held LinearB diagnostics and renaming checks executed.
13|completion/route_a/candidates.json,route_a/composition_all_candidates.json|Multiple graphical operations and identity rivals retained; no forced mergers.
14|completion/route_a/grammar.py,completion/route_a/winner.json|Joint latent role/transitions and graphical emission fit; boundaries mean role changes, not identified words.
15|route_a/structured_alignments.json,route_a/partial_observation_predictions.json,completion/route_a/latent_segmentation_alternatives.json|Structured alignments and partial compatibility retained beside fresh latent analyses.
16|route_a/operation_context_profiles.json,route_a/graphical_family_transfer.json|Retained context-conditioned competition complements new global latent grammar; do not claim fresh context fit if not rerun.
17|completion/route_a/evaluations.json,route_a/graphical_family_transfer.json|Operation and family application predictions survive; common joint evaluation pending separately.
18|completion/route_a/grammar.py,completion/route_a/latent_segmentation_alternatives.json,completion/route_a/INTERPRETATION.md|Executable transforms and neutral latent roles, counterexamples and alternative segmentations available.
19|completion/route_b/correspondence_network.json,completion/route_b/published_copper_type_network.json,completion/sources/summary.json|Reexecuted full M77 network plus held copper typology and namespace-preserving witness layer.
20|completion/route_b/competition.json,completion/route_b/copper_referent_competition.json|Literal lookup, anonymous/production mixture, complementary/context rivals fitted; latent labels are nonidentifiable.
21|completion/route_b/matched_component_contrasts.json,completion/sources/REPORT.md,route_a/structured_alignments.json|429 independent-expression contrasts and source-grounded conditional1380/2452 argument; segmentation dependency explicit.
22|completion/route_b/competition.json,completion/route_b/published_copper_type_network.json|Observed metadata and object-form competition executed; no documented workshop identifier exists, latent relabeling acknowledged.
23|completion/route_b/frozen_358_transfer.json,completion/route_b/predictions.json|Frozen component transfer plus family/medium predictions; no supported lexical transfer.
24|completion/route_b/semantic_anchors.json,completion/route_b/candidates.json|Empty positive lexical/sound anchor set; conditional exclusions and anonymous relationships exported.
25|route_c/cup_field_records.json,completion/route_c/records.json|Neutral stroke systems and opposite-face observations retained; no assumed physical units.
26|completion/route_c/run.py,completion/route_c/program_search.json|815 finite field/value/arithmetic/categorical programs executed.
27|completion/route_c/program_search.json,completion/route_c/equal_face_counterexamples.json|Field/value/operation candidates selected jointly; front-identity failures preserved; A-expanded field alternative included.
28|completion/route_c/observational_equivalence_classes.json,route_c/relative_unit_graphs.json|Equivalent predictions grouped; scale gauge and anonymous roles remain unanchored.
29|completion/route_c/frozen_predictions.json,completion/route_c/summary.json|Held-pair and held-front comparisons executed; identical losses reflect alias masks, not two independent confirmations.
30|completion/route_c/run.py,completion/route_c/summary.json|Executable parsers and conditional arithmetic failures exported; C→D consumption requires explicit execution.
31|completion/route_d/run_completion_d.py,completion/route_d/summary.json|Tamil/Sanskrit and anonymous/nonphonetic rivals use held forms; unequal lexicon coverage explicit.
32|completion/route_d/phonetic_alternatives.json,completion/route_d/run_completion_d.py|Joint root/affix and global211 phonetic/classifier search executed; external numeric-role API not yet used in joint run.
33|completion/route_d/summary.json,completion/route_d/phonetic_alternatives.json|Actual alternating full root/affix scan and segmentation; named mappings conditional, no accepted sound assignments.
34|completion/route_b/semantic_anchors.json,completion/route_d/REPORT.md|No admissible positive B anchor exists; unanchored linguistic competition appropriate. Published fish readings cannot become independent anchors.
35|completion/route_d/controls.json,completion/route_d/summary.json|Two named languages, anonymous/nonphonetic rivals, two orders and held-script diagnostics executed.
36|completion/route_d/frozen_predictions.json,completion/route_d/phonetic_alternatives.json|Mappings frozen before excluded pair analysis; unread70 remains unread; consistency is not sound accuracy.
37|completion/route_d/phonetic_alternatives.json,completion/route_d/REPORT.md|Explicit mappings, role alternatives and dependencies exported; no pronunciation promotion.
38|claim_dependencies.json,completion/claim_dependencies.json|Retained graph exists; must refresh to identify actual reconstructed candidates and prevent circular evidence reuse.
39|completion/run_joint.py,integration/cross_route_predictions.json,completion/cross_route_roles.json|A→B/C transforms executed in joint fit; D→A lexical-prior selection pending; explicit C→D role experiment missing.
40|completion/run_joint.py,completion/joint/summary.json|Finite shared graphical candidate optimized across original channels; running, final summaries required.
41|completion/joint/summary.json,completion/joint/linguistic_coupling/summary.json|Designated held constructions provide propagation test; still running at audit.
42|completion/route_a/matched_controls.json,completion/route_d/controls.json,completion/joint/linguistic_coupling/summary.json|Graphical, language and anonymous alternatives remove pivotal assumptions; final joint summaries pending.
43|completion/sources/REPORT.md,completion/route_a/INTERPRETATION.md,completion/route_c/retained_suffix_experiment.json|Source distinction and disputed local boundary/scope inspected; fresh fits contradict unsupported repair rather than silently repairing source.
44|continuation.json,completion/continuation.json|Old queue retained, but next experiment must reflect reconstructed outcomes.
45|completion/shared/masks.json,completion/run_joint.py,completion/joint/summary.json|Masks and settings frozen before held evaluations; final fitted artifacts still running.
46|completion/route_a/matched_controls.json,completion/route_b/verification.json,completion/joint/summary.json|Six full graphical-selection controls and frozen holdouts executed; joint completion pending.
47|completion/sources/REPORT.md,completion/sources/summary.json|Load-bearing original source text and codebook reexamined; no global corpus reread substituted for inference.
48|adjudication/scientific_review.md,completion/novelty.md|Retained scholarship comparison exists, reconstructed numerical/model outcomes need updated novelty statement.
49|accepted_claims.json,completion/claim_review.json|No positive reading promoted; need final reconstructed status and predictive versus translation coverage statement.
50|completion/run_joint.py,completion/route_a/run.py,completion/route_b/run.py,completion/route_c/run.py,completion/route_d/run_completion_d.py,completion/verification.json|All route runners exist and executed; joint, reproducibility manifest and final verification pending.
51|completion/route_a/latent_segmentation_alternatives.json,completion/route_d/frozen_predictions.json,completion/WORKED_EXAMPLES.md|Route-level worked records exist; integrated original/transform/meaning/unread/counterexample presentation pending.
52|completion/task_status.json,completion/verification.json|Final consolidated current campaign, merge/persistence and cleanup pending; cannot certify from code presence.
53|completion/route_c/retained_suffix_experiment.json,completion/continuation.json|Previously queued retained-suffix experiment executed; updated exact next executable continuation still required.''' 
S={}
for line in spec.splitlines():
 n,paths,note=line.split('|',2);S[int(n)]=(paths.split(','),note)
# Final independent review: assert substantive execution records, not file presence.
verification=json.loads((CAM/'completion/verification.json').read_text())
joint=json.loads((CAM/'completion/joint/summary.json').read_text())
ling=json.loads((CAM/'completion/joint/linguistic_coupling/summary.json').read_text())
cross=json.loads((CAM/'completion/cross_route_predictions.json').read_text())
assert verification['status']=='passed' and verification['check_count']==7
assert joint['fitted_candidates']==189 and len(joint['tasks'])==7
assert ling['completed_systems']==14 and len(ling['systems'])==14
assert len(cross['C_to_D'])==35 and cross['changed_decodings']==35
assert all(r['frozen_model_before']==r['frozen_model_after'] and r['unread_spans_preserved'] for r in cross['C_to_D'])
assert not cross['B_to_D']['positive_lexical_anchors']
ledger=json.loads((CAM/'completion/candidate_ledger.json').read_text());assert ledger['new_accepted_readings']==0
pending=set()
updates={
10:(['shared/candidate_contract.json','completion/candidate_ledger.json','completion/claim_dependencies.json'],'Reconstructed candidates consolidated against retained shared contract; dependency validation passed.'),
11:(['completion/run_joint.py','completion/joint/summary.json','completion/verification.json'],'189 fitted systems use normalized original channels once, with parameter/program costs separate; seven verification checks passed.'),
30:(['completion/route_c/run.py','completion/cross_route_predictions.json'],'Executable numerical rivals exported and explicitly consumed by35 conditional C-to-D comparisons; no numerical meaning promoted.'),
32:(['completion/route_d/phonetic_alternatives.json','completion/cross_route_predictions.json'],'Root/affix segmentation and phonetic/classifier alternatives executed;35 frozen numeric-role alternatives now consumed, with unread spans preserved.'),
38:(['completion/claim_dependencies.json','completion/candidate_ledger.json','completion/verification.json'],'Actual reconstructed candidate dependencies consolidated; acyclicity and unsupported-promotion gate passed.'),
39:(['completion/cross_route_predictions.json','completion/joint/summary.json','completion/joint/linguistic_coupling/summary.json'],'A-to-B/C fitted transformations; explicit35 C-to-D role comparisons; empty admissible B anchor set;14 D-to-A prior-conditioned systems executed. These are dependent consequences, not independent confirmations.'),
40:(['completion/run_joint.py','completion/joint/summary.json'],'189 ABC fits across seven frozen tasks jointly select shared spelling and channel models; original observations counted once.'),
41:(['completion/joint/summary.json','completion/joint/linguistic_coupling/summary.json'],'Seven held construction/family/medium tasks and14 linguistic counterparts executed, including explicit unread portions.'),
42:(['completion/route_a/matched_controls.json','completion/route_d/controls.json','completion/joint/linguistic_coupling/summary.json'],'Six full graphical-selection controls plus anonymous/nonphonetic and language-prior alternatives executed; no independent reading emerges.'),
44:(['completion/experiment_queue.json','completion/continuation.json','completion/next_order_comparison.py'],'Reconstructed rival-sensitive queue selects exact next scope experiment; previously queued retained-suffix experiment executed. Next further experiment explicitly unexecuted.'),
45:(['completion/shared/masks.json','completion/run_joint.py','completion/verification.json'],'Seven masks frozen before fitting;189 ABC artifacts and14 linguistic pre/post fingerprints verified; retrospective exposure stated.'),
46:(['completion/route_a/matched_controls.json','completion/joint/summary.json','completion/route_b/verification.json'],'Six complete graphical selection controls and executed recombination/family/medium tasks; no unsearched-noise comparison promoted.'),
48:(['completion/novelty.json','adjudication/scientific_review.md'],'Prior scholarship, preserved formalizations and reconstructed results separated; novelty priority unresolved, no new translation or sound correspondence claimed.'),
49:(['accepted_claims.json','completion/candidate_ledger.json','completion/novelty.json','completion/verification.json'],'Accepted ledger preserved; zero new readings, conditional/rejected rivals accessible. Prediction is not translation coverage.'),
50:(['completion/run_completion.py','completion/README.md','completion/verification.json'],'Route and joint runners, original observations, fitted systems, settings, dependencies and verification consolidated; persistence/merge tracked in52.'),
51:(['completion/WORKED_EXAMPLES.md','completion/route_a/latent_segmentation_alternatives.json','completion/route_d/frozen_predictions.json'],'Worked raw/expanded spelling, suffix, count and conditional-language cases show retained unknowns, dependencies and strongest rivals; detailed parses linked.'),
52:(['completion/README.md','completion/audit/task_status.json','completion/verification.json'],'Scientific consolidation and shared-contract checks complete. Local research commit7bad5368 merged at3a3184ef; completed recovery branch deleted. Remote publication is separately tracked.'),
53:(['completion/route_c/retained_suffix_experiment.json','completion/continuation.json','completion/next_order_comparison.py'],'Selected retained-suffix experiment executed, active fitted models preserved, exact next executable scope diagnostic saved. Decipherment unresolved; no unattended work implied.')}
S.update(updates)

original=(CAM/'EXECUTION_PLAN.md').read_text();out=[]
for match in re.finditer(r'^- \[ \] \*\*(\d+)\. (.*?)\*\* (.*)$',original,re.M):
 n=int(match[1]);paths,note=S[n];clauses=re.split(r'(?<=[.!?])\s+(?=[A-Z])',match[3]);refs=[{'path':p,'exists':(CAM/p).exists(),'origin':'reconstructed' if p.startswith('completion/') else 'retained_checkpoint'} for p in paths]
 out.append(dict(task=n,title=match[2],status='pending_reconstruction_closure' if n in pending else 'executed_with_scientific_limits',assessment=note,evidence=refs,clauses=[dict(clause=i+1,text=c,status='pending_task_closure' if n in pending else 'executed_within_stated_scope',evidence_paths=paths,assessment=note) for i,c in enumerate(clauses)]))
packet=dict(audit_status='final_scientific_audit_executed',tasks=out,task_count=len(out),clause_count=sum(len(x['clauses']) for x in out),executed_tasks=[x['task'] for x in out if x['task'] not in pending],pending_tasks=sorted(pending),important='Completion means listed finite research actions, not decipherment. Reconstructed executions are not exact recovery of lost bytes. Zero new readings were accepted; remote publication remains separately tracked.')
(HERE/'task_status.json').write_text(json.dumps(packet,indent=2)+'\n')
lines=['# Independent reconstruction completion audit','',f'{len(out)} original tasks and217 clauses reviewed.All53 tasks are executed within stated scientific scope; local consolidation merged at3a3184ef. Seven ABC evaluations contain189 fitted candidates;14 linguistic systems and35 frozen C-to-D comparisons are complete.','', 'The identified C-to-D consumption gap is closed:35 explicit conditional comparisons changed decoded analyses without changing frozen model fingerprints. No positive lexical anchor or numerical meaning was promoted.','', 'Final provenance, dependency graph, queue, novelty, worked examples and continuation now describe the newly executed results. Seven verification gates passed. The further scope diagnostic is explicitly saved for next execution, not falsely reported as run.','', '| Task | Status | Assessment |','|---|---|---|']
for x in out:lines.append(f"| {x['task']:02} | {x['status']} | {x['assessment']} |")
(HERE/'REPORT.md').write_text('\n'.join(lines)+'\n')
print(len(out),packet['clause_count'],sorted(pending))
