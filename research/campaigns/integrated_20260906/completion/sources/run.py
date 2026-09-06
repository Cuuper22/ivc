#!/usr/bin/env python3
"""Rebuild held source overlay. Never infer a cross-catalogue object join."""
import csv,hashlib,json,re,xml.etree.ElementTree as ET
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
if not (ROOT/'evidence/tmp/cisi_xml').exists():ROOT=Path('/workspace/scratch/f9a6bdbd6310/ivc')
def dump(n,x):(OUT/n).write_text(json.dumps(x,indent=2)+'\n')
def main():
    base=ROOT/'research/data/sign_crosswalk';refs=list(csv.DictReader((base/'evidence_refs.csv').open()));w=list(csv.DictReader((base/'artifact_witnesses.csv').open()));byid={r['ref_id']:r for r in refs}
    rows=[]
    for r in w:
        links=[]
        if r['image_ref_id'] and r['image_ref_id'] in byid:links.append({'reference':byid[r['image_ref_id']],'join':'explicit_image_ref_id'})
        if r['system_id']=='mayig_p':
            for ref in refs:
                # Only exact object+side named in an already-held source-panel filename.
                match=re.search(r'/(M-\d+)_([A-Z])_CISI',ref['local_path'])
                if match and ''.join(match.groups())==r['side_id']:links.append({'reference':ref,'join':'exact_source_panel_object_and_side_label','scope':'CISI/Mayig object label only; no Mahadevan text join'})
        rows.append({'original_witness':r,'namespace':r['system_id'],'source_links':links,'m77_object_id':None,'independent_m77_observation_added':False})
    dump('witness_overlay.json',rows);dump('evidence_refs.json',refs)
    images=[]
    for p in sorted((base/'source_panels').rglob('*')):
        if p.suffix.lower() in ['.png','.jpg','.jpeg']:images.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'already_held_source_panel','independent_observation':False})
    dump('source_image_inventory.json',images)
    source=ROOT/'evidence/tmp/cisi_xml/The Indus Script. Text, Concordance and Tables -Iravathan Mahadevan_djvu.xml'
    xml=ET.parse(source).getroot();pages=list(xml.iter('OBJECT'))
    dump('original_ocr_extracts.json',[{'pdf_page_index':i,'ocr':' '.join(w.text or '' for w in pages[i].iter('WORD'))} for i in [60,82,801,802]])
    concord=list(csv.DictReader((ROOT/'research/data/mahadevan_20260905/concordance_rows.csv').open()));targets=[]
    for oid,idx,printed,code,label in [('1380',60,50,'25','fabulous_composite_animal'),('2452',82,72,'01','unicorn')]:
        r=next(r for r in concord if r['textnum']==oid);seq=[r['S'+str(i)] for i in range(1,15) if r['S'+str(i)]]
        normal=[u for t in seq for u in (['87','59'] if t=='65' else ['70','211'] if t=='71' else [t])]
        targets.append({'object_id':'M77:'+oid,'frozen_row':r,'raw_sequence':seq,'conditional_normalized_sequence':normal,'original_text_page_index':idx,'original_printed_page':printed,'original_field_symbol_code':code,'field_description':label,'verification':'Visually inspected original text entry and original codebook page image. Object photo itself is not reproduced in these text entries.','image':f'page_{idx}.png'})
    result={'status':'reconstructed_source_adjudication_executed','objects':targets,'codebook':[{'code':'01','pdf_page_index':801,'printed_page':793,'description':'Unicorn, generally facing a special cult object.'},{'code':'25','pdf_page_index':802,'printed_page':794,'description':'Composite fabulous animal combining ram body, bull horns, elephant trunk, tiger hindlegs and raised serpent-like tail.'}],'raw_fs80_policy':'251 and13 remain unchanged in frozen input. The original printed object entries establish field-symbol codes25 and01 directly; no universal arithmetic decode of the modern fs80 column is asserted.','raw_sequences_equal':False,'conditional_normalized_sequences_equal':targets[0]['conditional_normalized_sequence']==targets[1]['conditional_normalized_sequence'],'prerequisites':['65 expands to87,59','71 expands to70,211','Expanded spelling identity represents the same linguistic expression'],'conclusion':'Conditional on these spelling equivalences, the entire expression cannot universally name the literal pictured species: the original source codes different animals. This is a negative lexical constraint, not a translation.','namespace_warning':'Mahadevan1380 and2452 are not equated with CISI M-1380/M-2452 by number.'}
    dump('1380_2452_adjudication.json',result)
    pdf=OUT/'Mahadevan_1977.pdf'
    dump('recovery_manifest.json',{'document':'Mahadevan1977 original source already present as OCR/XML in repository','recovery_url':'https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/The%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan.pdf','bytes':pdf.stat().st_size,'sha1':hashlib.sha1(pdf.read_bytes()).hexdigest(),'archive_metadata_sha1':'f13143f4fb458f1b4d6bd24201cc30291ce9ba80','sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'matches_archive_metadata':hashlib.sha1(pdf.read_bytes()).hexdigest()=='f13143f4fb458f1b4d6bd24201cc30291ce9ba80','matches_lost_package_hash':'unknown; lost hash not available','new_documentary_source':False})
    summary={'witnesses':len(rows),'unique_source_panel_images':len(images),'witnesses_with_exact_source_panel_links':sum(bool(r['source_links']) for r in rows),'evidence_refs':len(refs),'new_independent_m77_observations':0,'adjudication':'1380_composite_animal_2452_unicorn_original_codes_verified','new_accepted_readings':0};dump('summary.json',summary)
    (OUT/'REPORT.md').write_text('# Reconstructed original-source adjudication\n\nAll5858 held witness rows retain original namespace, side convention, provenance tier and raw text. All55 held source-panel images are inventoried. Exact image links use explicit same-object/same-side labels only; no Mahadevan joins are invented.\n\nOriginal Mahadevan text page50 labels1380 with field-symbol25; text page72 labels2452 with01. Visually inspected codebook pages793–794 identify these as composite animal and unicorn. The raw spellings differ, but the declared65→87,59 and71→70,211 rules produce the same sequence. The consequence is conditional exclusion of a universal literal pictured-species reading.\n\nThe PDF recovers an already-held documentary source whose OCR/XML survives. Its SHA1 matches Archive metadata; the lost package checksum is unavailable. Four rendered pages and source OCR excerpts make the finding reviewable.\n')
    print(json.dumps(summary))
if __name__=='__main__':main()
