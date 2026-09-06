#!/usr/bin/env python3
"""Extract every visible category-marked Appendix entry from the held Parpola1994 PDF.
Coordinates come from its embedded OCR, with two missing F labels restored from page image.
Unicode headwords/gloss summaries were transcribed after viewing all five source pages.
Raw source text, exact regions and uncertainty remain separate from normalized search forms.
"""
from pathlib import Path
import fitz, json, hashlib, re, unicodedata, collections
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'evidence/tmp/parpola_1994_signlist/parpola_1994_deciphering_sindhilanguagelibrary.pdf'
DOC=fitz.open(SOURCE)
# Source order: left column top to bottom, then right column. Entries with identical
# printed form and different sense numbers remain distinct observations of the lexicon.
FORMS={
296:[
('arakkulā-mīṉ','seer-fish'),('aṟu-mīṉ','Pleiades, six stars')],
297:[
('āti-mīṉ','first nakshatra, Ashvini'),('āṟā-mīṉ','Pleiades, six stars'),('āṟṟu-mīṉ','fresh-water fish'),('āṉai-mīṉ','huge fish'),('iṭi-mīṉ','a fish'),('uttara-mīṉ','Arundhati star'),('etir-mīṉ','fish that goes against the current'),('eḻu-mīṉ','seven principal stars of Ursa Major'),('ai-m-mīṉ','thirteenth nakshatra; also fourth nakshatra'),('ōṭṭu-mīṉ','crustacean, shellfish'),('kaṭanākku-mīṉ','flat fish'),('kaṭiccai-mīṉ','a sea fish'),
('kaṭu-mīṉ','ferocious fish, such as shark'),('kaṭai-mīṉ','twenty-seventh and final nakshatra'),('kallu-k-kōḻi-mīṉ','blue sea fish, Holocanthus imperator'),('kaḻi-mīṉ','salt-water fish'),('kaṉ-mīṉ','bride-fish, Lutjanus marginatus'),('kākkāy-mīṉ','a kind of fish'),('kiḷi-mīṉ','green sea fish'),('kīrai-mīṉ','small kind of fish'),('kuttuvā-mīṉ','a herring'),('kutirai-mīṉ','a kind of fish'),('kula-mīṉ','Arundhati'),('kuḻi-mīṉ','conger eel'),('kuḷa-mīṉ','a certain star; identification disputed in source'),('kuṟu-mīṉ','a kind of fish')],
298:[
('kai-m-mīṉ','thirteenth nakshatra'),('kokku-mīṉ','long-nosed marine fish'),('koy-mīṉ','a kind of fresh-water fish'),('koḻu-mīṉ','salt-water fish'),('kōṭṭu-mīṉ','shark'),('kōṉ-mīṉ','planet'),('kōḻi-mīṉ','sturgeon, Achanthurus gahm as source spells it'),('cippi-mīṉ','oyster, cockle, shellfish'),('ciṟaki-mīṉ','flying fish'),('ciṟu-mīṉ','Arundhati; loach'),('curumpu-mīṉ','lead-coloured sea fish'),('cem-mīṉ','Arundhati; Mars; sixth nakshatra; sperm whale'),
('talappaṟṟu-mīṉ','a kind of sea fish'),('tūḷ-mīṉ','small fish'),('tūru-mīṉ','a kind of fish'),('nakara-mīṉ','fish-shaped ring worn on little toe'),('naṉ-ṉīr-mīṉ','fresh-water fish'),('nākku-mīṉ','Indian sole; flat fish'),('nāṉ-mīṉ','lunar asterism'),('nāy-mīṉ','parrot wrasse'),('ney-m-mīṉ','fourteenth nakshatra by synonym; white prawn'),('ney-vāṉ-mīṉ','fourteenth nakshatra'),('noy-m-mīṉ','small fresh-water fish'),('pacu-v-ā-mīṉ','rose-coloured sea fish'),('para-veṭṭi-mīṉ','mud-skipper'),('paṟavai-mīṉ','flying fish'),('paṉṟi-mīṉ','several large sea fish species')],
299:[
('paṉai-mīṉ','fresh-water fish; climbing fish'),('pāl-mīṉ','milk-fish'),('pittaḷai-k-kācu-mīṉ','small fresh-water fish'),('puṇar-mīṉ','pair of carp in gold or silver, an auspicious object'),('puḷi-mīṉ','fish soured with tamarind juice'),('puḷi-vār-iṭṭa mīṉ','fish soured with tamarind juice'),('pū-mīṉ-keṇṭai','mahsir'),('peru-mīṉ','large fish'),('poṭi-mīṉ','small fish'),('poṉ-mīṉ','mahsir'),('makara-mīṉ','shark'),('mañcaṭ-kōḻi-mīṉ','buff vertically banded sea fish'),('matti-mīṉ','a kind of fish'),
('maṭavā-mīṉ','grey mullet'),('maṇalai-mīṉ','purple-red sea fish'),('mayil-mīṉ','sail-fish; peacock-fish'),('mu-m-mīṉ','fifth nakshatra'),('mai-m-mīṉ','Saturn'),('mōṭṭu-mīṉ','star'),('yāṉai-mīṉ','very large fish; whale'),('rōkita-mīṉ','a kind of fish'),('vaṭa-mīṉ','Alcor/Arundhati; Arundhati personification'),('vaya-mīṉ','fourth nakshatra'),('vavvāl-mīṉ','pomfret')],
300:[
('vaṉ-mīṉ','crocodile'),('vāl-mīṉ','comet'),('vāḷ-mīṉ','swordfish'),('vāṉ-mīṉ','star'),('vāṉ-mīṉ','comet'),('viṭi-mīṉ','Venus, morning star'),('viṇ-mīṉ','star'),
('viḻu-mīṉ','meteor'),('viḻu-mīṉ','hilsa'),('vīḻmīṉ','meteor'),('veṇ-mīṉ','Venus'),('veḷḷi-mīṉ','Venus'),('veḷḷai-mīṉ','white fish'),('vaikuṟu-mīṉ','morning star')]
}
MARGINS={296:((290,302),),297:((48,55),(307,314)),298:((32,39),(289,299)),299:((46,55),(304,312)),300:((32,39),(290,297))}
# Crop limits exclude S/F labels but retain source prose. For first Appendix page only right column exists.
X={296:{1:(311,570)},297:{0:(70,291),1:(330,565)},298:{0:(52,280),1:(310,562)},299:{0:(68,293),1:(327,565)},300:{0:(52,280),1:(312,562)}}
UNSURE={'arakkulā-mīṉ':'Headword internal l/ḷ and initial r/ṟ are not fully resolved from this scan; raw crop retained, exclude from exact-phonology tests.',
'kaṭanākku-mīṉ':'Printed first component appears contracted kaṭanākku; source explicitly analyses kaṭal+nākku. Exact sandhi form needs finer reading.',
'nāṉ-mīṉ':'The nasal in the printed first component is visually less clear than source lemma nāḷ; preserve as tentative nāṉ rather than silently equating.',
'kōṉ-mīṉ':'Printed nasal appears alveolar ṉ; source lemma is kōḷ. Do not apply general sandhi rules solely from this row.'}
def get_labels(pi):
 result=[]
 for w in DOC[pi].get_text('words'):
  x,y,x1,y1,t,*_=w
  if t not in ('F','S','s','SF','F(S)'):continue
  if not any(a<x<b for a,b in MARGINS[pi]):continue
  if pi==296 and y<640:continue
  c=1 if x>285 else 0
  result.append({'column':c,'y':y,'label':'S' if t=='s' else t,'label_origin':'embedded_pdf_ocr'})
 if pi==298:
  for y in [573.9,596.9]:result.append({'column':1,'y':y,'label':'F','label_origin':'visually_restored_label_missing_from_ocr'})
 return sorted(result,key=lambda a:(a['column'],a['y']))
def text_region(pi,c,y0,y1):
 x0,x1=X[pi][c]; rect=fitz.Rect(x0,y0,x1,y1)
 return {'pdf_page_index':pi,'printed_page':pi-17,'column':c,'bbox_pdf_points':[x0,round(y0,2),x1,round(y1,2)],'raw_text':DOC[pi].get_text('text',clip=rect).strip()}
records=[]
for pi,forms in FORMS.items():
 labels=get_labels(pi)
 assert len(labels)==len(forms),(pi,len(labels),len(forms))
 for j,(lab,(form,gloss)) in enumerate(zip(labels,forms)):
  nxt=next((a for a in labels[j+1:] if a['column']==lab['column']),None)
  end=nxt['y']-2 if nxt else 714
  regions=[text_region(pi,lab['column'],lab['y']-3,end)]
  # The final entry of one column/page continues before the next marked entry.
  if pi==296 and j==1:regions.append(text_region(297,0,68,103))
  if pi==298 and form=='cem-mīṉ':regions.append(text_region(298,1,66,101))
  if pi==298 and form=='paṉṟi-mīṉ':regions.append(text_region(299,0,68,101))
  if pi==299 and form=='matti-mīṉ':regions.append(text_region(299,1,68,204))
  if pi==299 and form=='vavvāl-mīṉ':regions.append(text_region(300,0,66,100))
  raw='\n\n'.join(a['raw_text'] for a in regions)
  bracket_parts=re.findall(r'\[([^\]]*)\]',raw,re.S)
  refs=[]
  # Remove spaces introduced by OCR inside the DEDR acronym only; do not normalize lexical form text.
  reftext=re.sub(r'D\s*E\s*D\s*R','DEDR',raw)
  refs=re.findall(r'DEDR\s*(?:App\.\s*)?[0-9]+[a-z]?',reftext)
  parts=re.split(r'[- ]',form)
  rec={'entry_id':f'tamil_app_{pi-17}_{j+1:02d}','language':'Tamil','entry_type':'category_marked_lexical_entry','source_category_code':lab['label'],'source_category_code_origin':lab['label_origin'],'compound_senses':['fish','star'] if lab['label']=='SF' else (['fish'] if lab['label'] in ['F','F(S)'] else ['star']),'first_component_only_star_sense':lab['label']=='F(S)','printed_form_transcription':form,'form_status':'tentative_transcription' if form in UNSURE else 'visually_transcribed','form_uncertainty':UNSURE.get(form),'segmentation_as_printed':parts if '-' in form or ' ' in form else None,'segmentation_status':'hyphenation_and_spaces_preserved_not_a_new_morphological_analysis','gloss_summary':gloss,'printed_lexical_notes_ocr':bracket_parts,'dedr_references_ocr':refs,'raw_entry_text_ocr':raw,'source_path':str(SOURCE.relative_to(ROOT)),'source_regions':regions,'phonology_test_eligible':form not in UNSURE,'evidence_class':'language_lexical_information_quoted_in_published_indus_scholarship','indus_assignment':None}
  records.append(rec)
# Source explicitly states kal and kallu mean stone under same DEDR entry; it does not
# independently license the full phonological rule converting them across all contexts.
relations=[{'relation_id':'stone_cock_fish_lattice','forms':{'single_stone':'kaṉ-mīṉ','single_cock':'kōḻi-mīṉ','double':'kallu-k-kōḻi-mīṉ'},'source_lexical_equations':[{'surface_component':'kaṉ','lemma_printed':'kal','gloss':'stone','dedr':'1298','status':'source_headword_with_explicit_lemma_in_brackets','printed_page':280},{'surface_component':'kallu','lemma_printed':'kallu','gloss':'stone','dedr':'1298','status':'source_component_explicitly_glossed','printed_page':280},{'surface_component':'kōḻi','lemma_printed':'kōḻi','gloss':'cock, fowl','dedr':'2248','status':'source_component_explicitly_glossed','printed_pages':[280,281]}],'linking_segment':'k','linking_segment_status':'visible_hyphenated_component_in_double_compound; identifying_its_grammatical_function_is_analysis','permitted_candidate_inference':'Treat kal/kaṉ/kallu as one proposed lexical family with separately charged context-conditioned realization.','not_source_established':'A general productive sandhi rule or any mapping from Indus59/60/65/66/211 to these forms.'}]
counts=collections.Counter(r['source_category_code'] for r in records)
meta={'schema':'ivc.tamil_compound_inventory.v1','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_pages':[279,280,281,282,283],'source_claimed_counts':{'star_compounds':34,'fish_compounds':65},'category_marked_entries_extracted':len(records),'category_code_counts':dict(counts),'visible_category_row_coverage':'Every category-marked entry on all five source pages was included. Two OCR-absent F labels on p281 were restored from source image.','count_reconciliation':{'fish_bearing_headword_rows':65,'star_bearing_headword_rows':31,'source_reported_star_compounds':34,'possible_reconciliation':'ai-m-mīṉ has two star senses and cem-mīṉ has three; counting their additional senses adds three, reaching34. This is an inference about counting, not a verified authorial convention.','overlap_policy':'F(S) means fish compound with a star sense only for its first component; do not assign the whole compound to star. SF has both compound senses.'},'standalone_secondary_compounds':['aṟu-mīṉ-kātalaṉ','āṟā-mīṉ-aṟa-v-ōṭṭu','cem-mīṉ-vayiṟam'],'secondary_compound_coverage':'Text and sources retained within parent raw entries; not separately counted as marked fish/star headwords.','missing_category_rows':[],'normalization_limits':'Form transcription visually checked from held scan, not a new dictionary. Four uncertain forms marked ineligible for exact phonology; raw OCR of definitions/references may remain noisy. Conventional scholarly diacritics are retained; source forms are not translated into Indus values.','selection_bias':'This is Parpola\'s fish/star-centered comparative appendix, not a random or complete Tamil vocabulary.','source_supported_relations':relations,'records':records}
(OUT/'tamil_compounds.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(OUT/'tamil_compounds_relations.json').write_text(json.dumps(relations,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'entries':len(records),'category_codes':counts,'exact_form_eligible':sum(x['phonology_test_eligible'] for x in records)},ensure_ascii=False))
