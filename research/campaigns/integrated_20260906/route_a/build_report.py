#!/usr/bin/env python3
"""Consolidate executed Route A outputs and conditional candidate records."""
import hashlib,json,math
from pathlib import Path
from run_route_a import ROOT,write

HERE=Path(__file__).parent
def read(name):return json.loads((HERE/name).read_text())

def main():
    s=read('summary.json');a=read('composition_adjudication.json');b=read('boundary_predictions.json');r=read('local_boundary_repair.json')
    common=dict(route='A',namespace='Mahadevan1977',context='Source stored sign order; strict expressions collapsed; raw observations never rewritten',
        prerequisites=['Frozen Mahadevan1977 source','Declared graphical feature hypotheses'],support=[],contradictions=[],
        alternatives=['Unrelated expressions sharing a conventional slot','Contextual category rather than synonymy','Phonetic or meaning-bearing operation not identified'],
        parameters={},complexity={},predictions=[],
        source_paths=['research/data/mahadevan_20260905/concordance_documents.json.gz','research/data/semantic_search_20260906/graphic_hypotheses.json'],
        prior_exposure='Retrospective. Corpus and prior exact relations exposed; new composed pair noticed after running frozen operations.')
    cs=[]
    cs.append(common|dict(id='A-FISH211',status='conditional',claim_type='graphical_equivalence',
        rule={'executable':'run_route_a.normalize_sequence(sequence, model="fish211")','mapping':{'60':['59','211'],'66':['65','211'],'68':['67','211'],'71':['70','211'],'73':['72','211']}},
        support={'old_exact_context_pairs':6,'one_edit_pairs_with_two_anchors':10,'structured_compact_texts':4,'structured_distinct_bases':[59,65,72],'predictions':'boundary_predictions.json'},
        contradictions=['No referent-equivalence observation independently validates this operation','Whole-line mark/211 exclusion has a direct counterexample, which does not refute a local operation'],
        complexity={'operations':1,'marker_selection_bits':math.log2(417),'operation_opcode_bits':2,'graphical_mapping':'five already declared pairs; no free per-object exception'},
        predictions=['Expand marked fish to corresponding base followed by211; then test target continuation or independently supplied referential field.'] ))
    cs.append(common|dict(id='A-GLOBAL211',status='underdetermined',claim_type='graphical_equivalence',
        rule={'executable':'run_route_a.normalize_sequence(sequence, model="global211")'},
        support={'declared_graphical_pairs':22},contradictions=['No structured211 match outside fish;342 has16 pairs across6 bases versus21111 pairs across3 fish bases'],
        complexity={'operations':1,'applicability_pairs':22},predictions=['Same expansion must explain nonfish applications if broad scope is claimed.']))
    cs.append(common|dict(id='A-BOUNDARY211',status='supported_scope_limited',claim_type='structural_constraint',
        rule='Marked fish have continuation behavior closer to an ending class than to the corresponding bare fish; no synonymy is asserted.',
        support={'target_occurrences':b['targets'],'weighted_target_mass':b['weighted_targets'],'predictive_bits':b['total_bits']},
        complexity={'ending_category_parameters':1,'training_background':'shared, train-only'},
        predictions=['Continuation distribution transfers across some fish graphical bases; do not infer that every line ends at a marked sign.']))
    cs.append(common|dict(id='A-211-EXCLUSION',status='rejected',claim_type='structural_constraint',
        rule='Marked fish and separate211 never coexist within a line.',
        contradictions=[{'row_id':'M77:1147:0','sequence':['387','66','336','89','211']}],complexity={'operations':1}))
    cs.append(common|dict(id='A-ROOF87',status='conditional',claim_type='graphical_equivalence',
        rule={'executable':'run_route_a.normalize_sequence(sequence, model="roof87")','mapping':{'65':['87','59'],'66':['87','60']}},
        support={'old_two_anchor_contexts':2,'new_marked_fish_two_anchor_contexts':1,'all_exact_expression_classes':4,
            'source_ids':['M77:1374','M77:2913','M77:2821','M77:2905','M77:2906','M77:7249','M77:7251','M77:7255','M77:7267','M77:7269','M77:6211','M77:4493','M77:4806','M77:4556'],
            'selected_marker_alternatives':'roof_lattice_predictions.json'},
        contradictions=['102-before has the same two old long-context supports; unobserved new102 counterpart is unknown','Original two roof87 pairs confound object medium; new tests do not independently prove equal referent'],
        complexity={'operations':1,'marker_selection_bits':math.log2(417),'placement_bits':1},
        predictions=['The roof addition becomes87 before the corresponding unroofed fish, including60/66 graphical lattice.']))
    cs.append(common|dict(id='A-ROOF87-TICK211',status='conditional',claim_type='graphical_equivalence',
        rule={'executable':'run_route_a.normalize_sequence(sequence, model="fish211_roof87")',
              'mapping':{'60':['59','211'],'65':['87','59'],'66':['87','59','211'],'68':['67','211'],'71':['70','211'],'73':['72','211']}},
        prerequisites=['A-FISH211','A-ROOF87','Publisher graphical square59/60/65/66'],
        support={'classes':10,'distinct_raw_expressions':21,'pairwise_relations':12,'cross_operation_pairs':2,'exclusively_cross_operation_classes':1,
            'new_pair_ids':['M77:1380:0','M77:2452:0'],'selected_program_rank':a['chosen_full_rank'],'leave70_family_rank':a['chosen_leave70_training_rank'],
            'candidate_programs':a['executable_acyclic_programs'],'comparison':'composition_adjudication.json'},
        contradictions=['Raw motif codes differ251/13 for1380/2452 although site and medium match; this is not a lexical anchor',
            'Under additional equal-face scalar assumption,4493 and4556 have conflicting cup-count outputs4/2; complementary fields remain possible'],
        alternatives=['A-ROOF102-TICK211','Roof109-before/tick211-after gives8 classes','Categorical field substitution without equal referent'],
        complexity={'operations':2,'marker_selection_bits':2*math.log2(417),'placement_bits':2,'rewriting_priority':'tick then roof; no object-specific exception'},
        predictions=[{'source_ids':['M77:1380:0','M77:2452:0'],'left':['65','70','211'],'right':['87','59','71'],'common_form':['87','59','70','211'],'phonetic_value_for70':None},
            {'source_ids':['M77:7249','M77:6211','M77:1551'],'common_form':['267','99','87','59','211']}]))
    cs.append(common|dict(id='A-ROOF102-TICK211',status='conditional',claim_type='graphical_equivalence',
        rule={'executable':'run_route_a.normalize_sequence(sequence, model="fish211_roof102")'},
        support={'normal_form_classes':8,'old_roof102_two_anchor_contexts':2},
        contradictions=['Does not connect1380/2452 under same program; this does not disprove it as a separate local convention'],
        complexity={'operations':2,'marker_selection_bits':2*math.log2(417),'placement_bits':2},predictions=['Compete on independently anchored contexts that distinguish87 and102 outputs.']))
    cs.append(common|dict(id='A-LOCAL-SUFFIX336',status='underdetermined',claim_type='structural_constraint',
        rule={'candidate_segmentation':[['387','66'],['336','89','211']]},
        support={'suffix_unique_texts':r['block_unique_texts'],'suffix_objects':r['block_object_count'],'standalone_suffix_objects':[w['object_id'] for w in r['independently_attested_suffix_witnesses']]},
        contradictions=['387–66 lacks a standalone witness','No strict211–336 adjacency observed; missing sequence is not a falsifier'],
        complexity={'new_segmentation_rules':1},predictions=['Test whether336–89 field continuations transfer across linked faces and object classes.']))
    write(HERE/'candidates.json',cs)
    report=f'''# Route A: writing-operation search, executed 6 September 2026

A two-operation candidate now connects expressions beyond the previous single-substitution fish examples. It remains a conditional orthographic analysis: no meaning, pronunciation, or equality of referents has been established.

## Strongest connected result

Use roof → separate87 before the fish, and four surrounding strokes → separate211 after the fish. The publisher drawings support the graphical square59/60/65/66; these are catalogue drawings, not independent artifact readings.

| Observation, stored order | Source objects | Conditional transformation |
|---|---|---|
|267–99–66|7249,7251,7255,7267,7269|roof removal gives267–99–87–60|
|267–99–87–60|6211|stroke removal gives267–99–87–59–211|
|267–99–87–59–211|1551|already expanded|
|65–70–211|1380|roof removal gives87–59–70–211|
|87–59–71|2452|stroke removal gives87–59–70–211|

The last pair extends the operation to fish70/71, which lacked an earlier exact single-rule counterpart. Both objects are Mohenjo-daro seals with direction code1, but their recorded picture codes differ251/13 (Route B). Site and medium alone cannot explain this particular contrast; it still may involve different referents in the same textual slot.

The roof premise came from two old contexts:65–348–342 ↔87–59–348–342 (1374/2913), and65–48–342 ↔87–59–48–342 (2821/2905/2906). Before the marked-fish transfer,87-before and102-before each had two long exact contexts. The new60/66 application has one exact context with two unchanged signs and another exact context with only176 unchanged (4493/4806 versus4556). The first two roof pairs confound medium; their repeated role across media is not itself a semantic control.

## Selected-rule rival comparison

`adjudicate_composition.py` compared every modifier/order candidate having a prior exact application:10 roof choices ×29 stroke choices =290 programs. All use the same fish features, recursive tick-then-roof grammar, and expression-collision metric.234 programs terminate;56 cyclic programs are explicitly retained as failures of this normalization mechanism.

Roof87-before plus211-after ranks first among the234 executable rivals:10 expression classes containing21 distinct raw expressions and12 pairwise relations. Roof109-before/211-after and roof102-before/211-after each give8 classes. After removing every70/71 expression, its whole objects and exact aliases,87/211 still ranks first with9 classes; the next rivals have8. Only87/211 produces the1380/2452 common form. Removing all267–99 prefix expressions leaves9 classes and preserves that pair.

Only two classes contain a pair requiring both operations. The267–99 triple is a transitive combination of single-operation edges.1380/2452 is the only class with no single-operation edge at all. These are counts of predicted equivalences, not independently observed synonymy. The comparison is restricted to prior exact modifier candidates, not the entire417² search space and not a statistical significance claim.

Both267–99 target strings had already appeared separately in the current211 alignment output before the dedicated roof test. The1380/2452 pair was noticed after the frozen composed transform produced it. All evaluations remain retrospective.

## Other executed mechanisms

The structured aligner preserves separate prefix and suffix anchors around a graphical base and permits one paid surrounding edit. It returns11 fish211 alignments, but these reduce to four compact expressions and three bases. Ten require a surrounding edit; one is the previously known exact context. Three compact expressions share267–99. A fourth,1235=150–123–65–67–73, aligns with7247=150–123–67–72–211 or4056=150–123–53–67–72–211. These edits remain explicit; they are not inferred synonyms.

Broad four-stroke →211 is not selected:342 yields16 structured pairs across six graphical bases, while211 yields11 across three fish bases. The21 literal-part hypotheses still give zero counterparts after allowing one context edit and requiring two observed anchors. Nine certain marked-fish occurrences in partial lines yield zero exact expanded visible-island counterparts; blanks, doubtful signs and unknown spans terminate an island and are never filled.

The existing graphical maps contain only one complete roof/stroke square,59/60/65/66. Every incomplete square is listed in `roof_lattice_predictions.json`; no extra base extensions were invented.

## Observable context prediction and simpler rivals

Each target graphical base is withheld with whole objects and exact-expression aliases. The task predicts the next observed sign or line boundary after a marked fish. There are50 target occurrences with44.333 total expression weight. All models use a fixed417-sign-plus-boundary alphabet and the same training-only background.

| Model | Predictive data cost, bits |
|---|---:|
|Base fish followed by211|{b['total_bits']['base_then211']:.2f}|
|One-parameter ending category|{b['total_bits']['terminal_category']:.2f}|
|Other marked fish families|{b['total_bits']['marked_other_base']:.2f}|
|All211 continuations|{b['total_bits']['all211']:.2f}|
|Marked family + catalogue-number prefix|{b['total_bits']['marked_catalogue_prefix']:.2f}|
|Marked family + object class|{b['total_bits']['marked_objectclass']:.2f}|
|Bare fish|{b['total_bits']['bare_base']:.2f}|

The6.35-bit advantage of base+211 over a simple ending category is smaller than an explicit8.70-bit charge for selecting one marker among417, before any opcode or graphical-scope charge. This is an illustrative stated code, not a unique MDL prior. Continuation prediction therefore supports an ending-role relationship much more strongly than token equivalence. An unconstrained training-family continuation search actually chooses12 or388, predicts no observed complete alternate spellings, and demonstrates why next-sign success alone cannot recover the writing operation.

## Counterexamples and route interactions

1147=387–66–336–89–211 rejects unconditional whole-line exclusion of marked fish and separate211. A local split387–66 |336–89–211 remains possible: the suffix occurs in34 unique texts on38 objects and is standalone on2575,5089,7279,2015. The left fragment is not standalone. Marked66 also precedes336–89 on1425; no strict211–336 adjacency is observed. This is an unresolved segmentation proposal, not a license for a separate grammar per object.

Root integration found a concrete failure of an additional numerical interpretation:4493=[66,176] pairs with cup count4, while4556=[87,60,176] pairs with count2. If roof87 preserves the same fixed scalar value and opposite faces are equated, this is inconsistent. It does not refute a spelling operation when opposite faces are complementary fields. Route C's existing59–59 versus87–59 example uses1551 again, so that object is never counted twice as independent confirmation. Route D may propagate the anonymous root70 through the new equality; it cannot infer a sound for70 from this alone.

## Reproduction and continuation

From the repository root:

```sh
python research/campaigns/integrated_20260906/route_a/run_route_a.py
python research/campaigns/integrated_20260906/route_a/adjudicate_composition.py
python research/campaigns/integrated_20260906/route_a/build_report.py
```

A13–18 were executed: competing decompositions; constrained transducers; structured and partial alignments; context-conditioned alternatives; recombination/family exclusions; candidate operations and counterexamples. Phonetic and semantic identification remain unresolved. `candidates.json` follows the shared contract; no accepted ledger was changed.

The next discriminating experiment is to use the already-held object sources for1380 and2452 to determine what picture-code251 versus13 actually distinguishes, and to compare that feature across all independently held witnesses of the same two component constructions. Freeze roof87/211, roof102/211 and the categorical-field rival first; exclude the defining objects and their expression aliases. Predict one specified pictorial or companion-field contrast. If source images do not identify that contrast, retain the textual operation as conditional instead of manufacturing a semantic anchor. The executable starting point is `composition_adjudication.json.target_pair`, joined to Route B's source-linked object network.
'''
    (HERE/'REPORT.md').write_text(report)
    script_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')}
    write(HERE/'execution.json',{'commands':['python research/campaigns/integrated_20260906/route_a/run_route_a.py','python research/campaigns/integrated_20260906/route_a/adjudicate_composition.py','python research/campaigns/integrated_20260906/route_a/build_report.py'],
        'source_sha256':s['input_sha256'],'script_sha256':script_hashes,'executed_outputs':['summary.json','composition_adjudication.json','roof_lattice_predictions.json','boundary_predictions.json','candidates.json','REPORT.md'],
        'task_steps':{str(i):'executed; interpretation unresolved where stated' for i in range(13,19)},
        'accepted_readings_added':0})
    print(json.dumps({'candidate_records':len(cs),'report':'REPORT.md','strongest_candidate':'A-ROOF87-TICK211'},indent=2))

if __name__=='__main__':main()
