from pathlib import Path
import tempfile,unittest,sys,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/photo-book-studio/scripts'))
import plog_review

class CompletionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'project').mkdir()
  self.sources=[f'source-{i}.jpg' for i in range(10)]
  self.grouped=[self.sources[:3],self.sources[3:6],self.sources[6:]]
 def tearDown(self):self.tmp.cleanup()
 def fixture(self,groups=None):
  groups=groups or self.grouped
  book={'pages':[{'layers':[{'type':'photo','file':f} for f in group]} for group in groups]}
  (self.root/'project/book.json').write_text(json.dumps(book),encoding='utf-8')
  audit={'pages':len(groups),'expectedOccurrences':dict.fromkeys(self.sources,1),'bookSha256':'current'}
  r=plog_review.template();r['version']=1;r['planning']={'photos':[{'file':f,'role':'supporting','reason':'Daily scene supporting the birthday story'} for f in self.sources],'pages':[{'page':i+1,'files':g,'reason':'Related daily fragments, readable in phone review'} for i,g in enumerate(groups)],'densityReason':'Compact social journal, three related groups','expandedReason':''}
  r['resources']={'inspiration':[{'source':'bundled concrete-case observations','observed':'Paper strip joins mixed aspect-ratio images','application':'One strip anchors the detail cluster'}],'materials':{'decision':'draw','reason':'Native tape and source-linked SVG suffice'},'fonts':{'mode':'compare','candidates':['wenkai','smiley'],'actualCopy':'生日与日常','reason':'Actual-copy specimens inspected for hierarchy'}}
  r['decoration']={'method':'svg','reason':'Draw a candle from the actual cake, linking birthday images'}
  r['creativeReview']=[{'route':i,'decision':'skip','reason':'Compact original-photo cluster already expresses this event'} for i in range(1,8)]
  r['visual']={'bookSha256':'current','pages':[{'page':i+1,'inspected':True,'phoneInspected':True,'notes':'Subjects intact, captions readable'} for i in range(len(groups))]}
  return audit,r
 def errors(self,audit,r):
  (self.root/'project/plog-review.json').write_text(json.dumps(r),encoding='utf-8')
  return plog_review.problems(self.root,audit)
 def test_compact_ten_sources_with_svg_and_no_generation_pass(self):
  a,r=self.fixture();self.assertEqual(self.errors(a,r),[])
 def test_incomplete_route_assessment_blocks_delivery(self):
  a,r=self.fixture();r['creativeReview']=r['creativeReview'][:4];self.assertTrue(any('seven' in e for e in self.errors(a,r)))
 def test_ten_sources_seven_pages_needs_reason_but_is_not_banned(self):
  groups=[[s] for s in self.sources[:6]]+[self.sources[6:]];a,r=self.fixture(groups)
  self.assertTrue(any('Sparse Plog' in e for e in self.errors(a,r)))
  r['planning']['expandedReason']='User explicitly requested six separate portrait stories; compact version would mix their long authentic captions.'
  self.assertEqual(self.errors(a,r),[])
 def test_total_equality_cannot_hide_wrong_page_identities(self):
  a,r=self.fixture();r['planning']['pages'][0]['files'][0]=self.sources[8]
  self.assertTrue(any('differ' in e for e in self.errors(a,r)))
 def test_stale_visual_review_and_missing_phone_inspection_fail(self):
  a,r=self.fixture();r['visual']['bookSha256']='previous';r['visual']['pages'][0]['phoneInspected']=False
  errors=self.errors(a,r);self.assertTrue(any('stale' in e for e in errors));self.assertTrue(any('phone' in e for e in errors))
 def test_missing_resource_research_or_single_new_font_fails(self):
  a,r=self.fixture();r['resources']['inspiration']=[];r['resources']['fonts']['candidates']=['wenkai']
  errors=self.errors(a,r);self.assertTrue(any('inspiration' in e for e in errors));self.assertTrue(any('two font' in e for e in errors))
 def test_approved_font_reuse_allowed_without_fresh_comparison(self):
  a,r=self.fixture();r['resources']['fonts'].update(mode='reuse-approved',candidates=[])
  self.assertEqual(self.errors(a,r),[])
 def test_generation_requires_actual_provenance_while_svg_does_not(self):
  a,r=self.fixture();r['decoration']['method']='imagegen'
  self.assertTrue(any('tool/prompt' in e for e in self.errors(a,r)))
  r['decoration']['generations']=[{'tool':'actual tool','prompt':'source-specific prompt','inputs':['cake.jpg'],'outputs':['stickers.png'],'inspection':'Alpha and shapes inspected'}]
  self.assertEqual(self.errors(a,r),[])

 def v2(self):
  a,r=self.fixture();r['version']=2;r['production']={'method':'native','reason':'Existing local materials and original photos suffice'};r['resources']={};r['creativeReview']=[]
  return a,r
 def test_v2_does_not_require_browsing_font_comparison_or_seven_reports(self):
  a,r=self.v2();self.assertEqual(self.errors(a,r),[])
 def test_v2_still_rejects_omitted_sources_and_stale_review(self):
  a,r=self.v2();r['planning']['photos'].pop();r['visual']['bookSha256']='old'
  errors=self.errors(a,r);self.assertTrue(any('selected source' in e for e in errors));self.assertTrue(any('stale' in e for e in errors))
 def test_v2_photo_generation_needs_actual_references_but_symbolic_does_not(self):
  a,r=self.v2();r['decoration']={'method':'imagegen','reason':'New motif','generations':[{'tool':'imagegen','prompt':'Actual motif prompt','inputs':[],'sourceFiles':[],'outputs':['assets/motif.png'],'inspection':'Alpha and shape viewed'}]}
  self.assertEqual(self.errors(a,r),[])
  r['decoration']['generations'][0]['sourceFiles']=[self.sources[0]]
  self.assertTrue(any('reference inputs' in e for e in self.errors(a,r)))
 def test_v2_artwork_mapping_needs_matching_generated_output_record(self):
  a,r=self.v2();book=json.loads((self.root/'project/book.json').read_text(encoding='utf-8'))
  book['pages'][0]['layers']=[{'type':'artwork','path':'assets/group.png','sourceFiles':self.grouped[0]}]
  (self.root/'project/book.json').write_text(json.dumps(book),encoding='utf-8')
  a['artworkMappings']=[{'path':'assets/group.png','method':'imagegen-integrated','sourceFiles':self.grouped[0]}]
  self.assertTrue(any('generation record' in e for e in self.errors(a,r)))
  r['decoration']={'method':'imagegen','reason':'Integrated group','generations':[{'tool':'imagegen','prompt':'Actual group prompt','inputs':['original references'],'sourceFiles':self.grouped[0],'outputs':['assets/group.png'],'inspection':'Compared all three originals'}]}
  self.assertEqual(self.errors(a,r),[])

 def test_v2_intermediate_inspection_is_optional_but_final_review_remains_required(self):
  a,r=self.v2();r['decoration']={'method':'imagegen','reason':'Finish the composed page','generations':[{'tool':'imagegen','prompt':'Actual finishing prompt','inputs':['finished page and original refs'],'sourceFiles':self.sources,'outputs':['assets/final.png']}]}
  self.assertEqual(self.errors(a,r),[])
  r['visual']['pages'][0]['phoneInspected']=False
  self.assertTrue(any('phone' in e for e in self.errors(a,r)))
 def test_v2_removing_intermediate_inspection_does_not_remove_real_provenance(self):
  a,r=self.v2();r['decoration']={'method':'imagegen','reason':'Finish','generations':[{'tool':'imagegen','inputs':['base page'],'sourceFiles':self.sources,'outputs':['assets/final.png']}]}
  self.assertTrue(any('prompt' in e for e in self.errors(a,r)))

if __name__=='__main__':unittest.main()
