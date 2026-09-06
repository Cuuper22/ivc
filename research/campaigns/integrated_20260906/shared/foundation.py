#!/usr/bin/env python3
"""Lossless references, partial observations and task-local exclusion interfaces.

This extends the existing Mahadevan loader; it does not rebuild the corpus audit.
The frozen source remains authoritative. No reconstruction is used as training data.
"""
from __future__ import annotations
import collections
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'research/tools'))
from mahadevan_constraint_audit import decode, reject_reasons
from semantic_transducer_search import TICK_PAIRS, ROOF_PAIRS, PARTS, EXPECTED_SHA256


def stable(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def load_source():
    path = ROOT/'research/data/mahadevan_20260905/concordance_documents.json.gz'
    raw = gzip.decompress(path.read_bytes())
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Source differs from frozen campaign evidence')
    return json.loads(raw)


def occurrence(raw, position):
    core = raw.lstrip('*')
    result = {'slot': position, 'raw': raw, 'namespace': 'Mahadevan1977'}
    if raw == '0':
        return result | {'kind': 'unknown_span', 'sign_count': None,
                         'minimum_source_certified_length': None}
    if core.isdigit() and 1 <= int(core) <= 417:
        return result | {'kind': 'doubtful_sign' if raw.startswith('*') else 'sign',
                         'sign_id': int(core), 'certain': not raw.startswith('*'),
                         'other_identity_unresolved': raw.startswith('*')}
    return result | {'kind': 'unparsed', 'sign_count': None}


def compatible(observed, candidate, admit_doubtful=True):
    """Existential compatibility, NOT a likelihood or imputed observation.

    Unknown spans consume 0..remaining signs as an explicit permissive search
    approximation; source span length is unknown. Doubtful IDs may be respected
    or treated as an unknown single slot. Use strict results as a separate lane.
    """
    states = {0}
    for token in observed:
        next_states = set()
        for j in states:
            kind = token['kind']
            if kind in ('unknown_span', 'internal_blank', 'unparsed'):
                next_states.update(range(j, len(candidate)+1))
            elif j < len(candidate):
                if (kind == 'doubtful_sign' and admit_doubtful) or int(candidate[j]) == token['sign_id']:
                    next_states.add(j+1)
        states = next_states
    return len(candidate) in states


def load_observations():
    return [json.loads(line) for line in (HERE/'observations.jsonl').read_text().splitlines()]


def task_partition(rows, target_row_ids, related_sequences=()):
    """Remove whole target objects plus exact-expression aliases from training.

    Related expressions are explicit task choices (e.g. a withheld graphical
    family), never a transitive edit-distance family. No other catalogue is used.
    """
    targets = [r for r in rows if r['row_id'] in set(target_row_ids)]
    blocked_objects = {r['object_id'] for r in targets}
    sequences = {tuple(s) for s in related_sequences}
    sequences.update(tuple(r['tokens_stored']) for r in targets if r['strict'])
    raw_patterns = {tuple(r['raw_slots']) for r in targets if r['tokens_stored']}
    for row in rows:
        if (row['strict'] and tuple(row['tokens_stored']) in sequences) or (row['tokens_stored'] and tuple(row['raw_slots']) in raw_patterns):
            blocked_objects.add(row['object_id'])
    train = [r['row_id'] for r in rows if r['object_id'] not in blocked_objects]
    return {'target_row_ids': sorted(target_row_ids), 'train_row_ids': train,
            'excluded_object_ids': sorted(blocked_objects),
            'excluded_exact_sequences': sorted(sequences),
            'excluded_exact_raw_patterns': sorted(raw_patterns),
            'prior_exposure': 'retrospective; corpus and earlier discoveries already inspected'}


def predictive_score(log_probabilities, weights=None, parameter_bits=0, exception_bits=0, rule_bits=0):
    if weights is None:
        weights = [1.0]*len(log_probabilities)
    data_bits = -sum(w*lp/math.log(2) for w,lp in zip(weights,log_probabilities))
    return {'data_bits': data_bits, 'parameter_bits': parameter_bits,
            'exception_bits': exception_bits, 'rule_bits': rule_bits,
            'total_bits': data_bits+parameter_bits+exception_bits+rule_bits}


def build():
    rows = []
    objects = collections.defaultdict(list)
    for doc in load_source():
        raw = {k:decode(v) for k,v in doc['fields'].items()}
        slots = [str(raw.get('S'+str(i), '')) for i in range(1,15)]
        tokens = [x for x in slots if x]
        last = max((i for i,x in enumerate(slots) if x), default=-1)
        obs = [occurrence(x,i+1) if x else {'slot':i+1,'raw':'','kind':'internal_blank'}
               for i,x in enumerate(slots[:last+1])]
        code = int(raw['sideline'])
        row_id = f"M77:{raw['textnum']}:{raw['sideline']}"
        row = {'row_id': row_id, 'object_id': 'M77:'+raw['textnum'],
               'face_code': code//10, 'line_code': code%10,
               'face_definition': '0=only side; positive=numbered side',
               'line_definition': '0=only line; 1..=catalogue line number; 9=no text',
               'raw_fields': raw, 'source_record': doc['name'],
               'source_sha256': EXPECTED_SHA256,
               'raw_slots': slots, 'tokens_stored':tokens,
               'tokens_display':list(reversed(tokens)), 'observations':obs,
               'direction_code_raw':raw['dir'],
               'orientation_policy':'stored and reversed are global/task hypotheses, not free per-row choices',
               'strict': not reject_reasons(raw | {'tokens':tokens}),
               'exclusion_reasons': reject_reasons(raw | {'tokens':tokens}),
               'prior_exposure':'existing public snapshot used by prior runs'}
        row['exact_expression_key'] = stable(tokens) if row['strict'] else None
        rows.append(row)
        objects[row['object_id']].append(row)
    with (HERE/'observations.jsonl').open('w') as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False, separators=(',',':'))+'\n')
    object_records = []
    for oid, rr in sorted(objects.items()):
        faces = collections.defaultdict(list)
        for r in rr:
            faces[str(r['face_code'])].append(r['row_id'])
        signature = [(r['face_code'],r['line_code'],r['raw_slots'])
                     for r in sorted(rr,key=lambda r:(r['face_code'],r['line_code']))]
        object_records.append({'object_id':oid,'faces':dict(faces),
            'row_ids':[r['row_id'] for r in rr],
            'whole_object_text_key':stable(signature),
            'all_nonempty_lines_strict':all(r['strict'] for r in rr if r['tokens_stored']),
            'physical_copy_identity':'unresolved; exact text is not proof of common matrix',
            'line_order':'catalogue order retained; no cross-line adjacency asserted'})
    write('objects.json',object_records)
    groups = collections.defaultdict(list)
    for obj in object_records:
        groups[obj['whole_object_text_key']].append(obj['object_id'])
    write('identity_groups.json', {'same_object':'object_id',
        'whole_object_exact_text_groups':dict(groups),
        'physical_copy_groups':[], 'cross_catalogue_joins_used':[],
        'task_local_exact_expression_exclusion':'task_partition',
        'weighting':'report physical object and distinct expression/record-family results separately'})
    write('graphical_hypotheses.json', {
        'status':'prior visual hypotheses; not catalogue sign mergers or accepted operations',
        'source':'research/data/semantic_search_20260906/graphic_hypotheses.json',
        'four_strokes':TICK_PAIRS,'roof':ROOF_PAIRS,'literal_parts':PARTS,
        'long_stroke_counts':{'86':1,'87':2,'89':3,'95':4,'96':5},
        'long_stroke_semantics':'visible counts only; numerical function remains a hypothesis'})
    write('evaluation_contract.json', {
        'version':'1.0','seed':20260906,
        'exposure':'All corpus evaluations retrospective; no claim of pristine blind discovery.',
        'recombination':'withhold whole target combinations and exact copies; components may remain',
        'unseen_family':'explicit route families withheld, plus target objects and expression aliases',
        'blocked_inputs':['other catalogues of target objects','target-derived annotations',
                          'companion faces unless task explicitly permits them','other agent outputs using target'],
        'tasks':{
            'A':{'inputs':['source expression','declared graphical pairs','permitted context'],
                 'targets':['alternative written form','operation placement']},
            'B':{'inputs':['masked text component','other permitted faces','observed context'],
                 'targets':['motif or text relation excluded from inputs']},
            'C':{'inputs':['descriptor/other permitted fields','context'],
                 'targets':['observed count or alternative notation']},
            'D':{'inputs':['unmasked expressions','independent lexicon','declared conditional anchors'],
                 'targets':['recurring forms/segmentations/sound correspondences where independently scorable']}},
        'scores':'same observed targets; channel-specific predictive data cost plus rule/parameter/exception cost',
        'missing_combination':'unknown, not negative evidence by itself',
        'control_policy':'reuse published corpus outputs; compact mechanism-specific controls only',
        'partial_policy':'existential compatibility is not likelihood; never train on compatible completion',
        'fold_assignment':{k:int(k[:12],16)%5 for k in groups},
        'fold_use':'Group key alone insufficient for every task: task_partition removes exact-expression aliases.'})
    write('candidate_contract.json', {
        'required_fields':['id','route','status','claim_type','rule','namespace','context',
            'prerequisites','support','contradictions','alternatives','parameters','complexity',
            'predictions','source_paths','prior_exposure'],
        'claim_types':['graphical_equivalence','grammatical_function','operational_meaning',
                       'lexical_meaning','sound_assignment','language_identification','structural_constraint'],
        'statuses':['provisional','conditional','underdetermined','rejected','supported_scope_limited'],
        'accepted_ledger':'coordinator only; no promotion from predictive fit alone'})
    write('snapshot.json', {'starting_commit':'fcb6686c6439b1ad6fe33eafa63e99ed659a284b',
        'starting_worktree_changes':[], 'source_sha256':EXPECTED_SHA256,
        'records':len(rows),'objects':len(objects),
        'strict_rows':sum(r['strict'] for r in rows),
        'partial_nonempty_rows':sum(bool(r['tokens_stored']) and not r['strict'] for r in rows),
        'unknown_span_rows':sum(any(x['kind']=='unknown_span' for x in r['observations']) for r in rows),
        'doubtful_rows':sum(any(x['kind']=='doubtful_sign' for x in r['observations']) for r in rows),
        'multiline_objects':sum(any(sum(r['face_code']==f for r in rr)>1 for f in {r['face_code'] for r in rr})
                                for rr in objects.values()),
        'whole_object_text_groups':len(groups),
        'reused_schema':'db/schema.sql separates artifact/witness/sign/evidence; campaign JSONL adds faces, lines and spans',
        'sources_not_merged':'Lipi/Mayig/CISI identities remain in existing source-bound crosswalk, not pooled as samples'})
    print((HERE/'snapshot.json').read_text())


if __name__ == '__main__':
    build()
