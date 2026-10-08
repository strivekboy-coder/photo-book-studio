from pathlib import Path
import unittest,tempfile,shutil,json,hashlib,argparse,importlib.util,sys,zipfile
from PIL import Image
REPO=Path(__file__).resolve().parents[1]
class PlogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory()
  cls.home=Path(cls.temp.name)
  cls.installed=cls.home/'installed/photo-book-studio'
  shutil.copytree(REPO/'skills/photo-book-studio',cls.installed)
  sys.path.insert(0,str(cls.installed/'scripts'))
  spec=importlib.util.spec_from_file_location('plog_test_module',cls.installed/'scripts/plog.py')
  cls.api=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.api)
  cls.inputs=cls.home/'input';cls.inputs.mkdir()
  Image.new('RGB',(300,500),'#53868f').save(cls.inputs/'照片.jpg')
  Image.new('RGB',(500,300),'#b68162').save(cls.inputs/'detail.png')
  cls.originals={p.name:cls.api.sha(p) for p in cls.inputs.iterdir()}
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def setUp(self):
  self.root=self.home/self._testMethodName
  self.api.init(argparse.Namespace(workspace=str(self.root),title='Plog < sample'))
  p=self.root/'project/brief.json';b=self.api.read(p);b['intakeComplete']=True;self.api.save(p,b)
  self.api.inventory(argparse.Namespace(workspace=str(self.root),photos=str(self.inputs),recursive=False))
  b=self.api.read(self.root/'project/book.json');b['pages']=[{'layers':[{'type':'photo','file':'照片.jpg','x':10,'y':10,'w':300,'h':500},{'type':'photo','file':'detail.png','x':400,'y':10,'w':500,'h':300}]}]
  self.api.save(self.root/'project/book.json',b)
 def book(self):return self.api.read(self.root/'project/book.json')
 def build(self,b):
  self.api.save(self.root/'project/book.json',b)
  return self.api.build(argparse.Namespace(workspace=str(self.root)))
 def test_copied_skill_is_self_contained_and_sources_unchanged(self):
  audit=self.build(self.book())
  self.assertEqual((audit['selected'],audit['placed'],audit['omitted']),(2,2,0))
  self.assertTrue((self.root/'assets/plog-starter/blank-ticket.svg').exists())
  self.assertTrue((self.root/'project/plog-planning.md').exists())
  self.assertEqual(len(self.api.read(self.root/'project/plog-review.json')['creativeReview']),7)
  self.assertTrue((self.root/'sample.html').exists())
  self.assertIn('Seven optional', (self.root/'project/zine-review-policy.md').read_text(encoding='utf-8'))
  self.assertTrue((self.installed/'references/creative-prompts.md').exists())
  self.assertIn('10-15', (self.root/'project/creative-prompts.md').read_text(encoding='utf-8'))
  self.assertEqual(audit['bookSha256'],self.api.sha(self.root/'project/book.json'))
  for p in self.inputs.iterdir():self.assertEqual(self.api.sha(p),self.originals[p.name])
 def test_editor_embeds_state_without_script_breakout(self):
  b=self.book();b['title']='</script><script>window.invalid=true</script>'
  self.build(b)
  page=(self.root/'sample.html').read_text(encoding='utf-8')
  import re
  state=re.search(r'<script type="application/json" id="plog-data">(.*?)</script>',page,re.S).group(1)
  self.assertNotIn('<',state)
  embedded=json.loads(state)
  self.assertEqual(embedded['book']['title'],b['title'])
  self.assertEqual(embedded['revision'],self.api.sha(self.root/'project/book.json'))
  self.assertEqual(len(embedded['inventory']),2)
  self.assertIn('微调排版',page)
  self.assertIn('pointercancel',page)
 def test_same_count_duplicate_and_omission_rejected(self):
  b=self.book();b['pages'][0]['layers'][1]['file']='照片.jpg'
  with self.assertRaisesRegex(ValueError,'Selection invariant'):self.build(b)
 def test_explicit_repeat_is_allowed_but_not_a_hidden_omission(self):
  b=self.book();b['policy']['authorizedOccurrences']={'照片.jpg':2}
  b['pages'][0]['layers'].append(dict(b['pages'][0]['layers'][0]))
  audit=self.build(b);self.assertEqual(audit['sourceOccurrences']['照片.jpg'],2);self.assertEqual(audit['sourceOccurrences']['detail.png'],1)
 def test_changed_source_hash_blocks_build(self):
  p=self.root/'assets/photos/照片.jpg';Image.new('RGB',(300,500),'red').save(p)
  with self.assertRaisesRegex(ValueError,'Source changed'):self.build(self.book())
 def test_derivative_requires_explicit_brief_path_and_keeps_source_id(self):
  p=self.root/'assets/derivative.png';Image.new('RGB',(300,500),'#77aabb').save(p)
  b=self.book();b['pages'][0]['layers'][0].update(path='assets/derivative.png',approvedDerivative=True)
  with self.assertRaisesRegex(ValueError,'explicitly approved'):self.build(b)
  brief=self.api.read(self.root/'project/brief.json');brief['permissions']['approvedDerivatives']={'照片.jpg':{'path':'assets/derivative.png','source':'explicit'}}
  self.api.save(self.root/'project/brief.json',brief)
  audit=self.build(b);self.assertEqual(audit['sourceOccurrences']['照片.jpg'],1)
 def test_missing_assets_escaping_paths_and_photo_distortion_rejected(self):
  base=self.book()
  bad=json.loads(json.dumps(base));bad['pages'][0]['layers'][0]['fit']='fill'
  with self.assertRaisesRegex(ValueError,'Unsupported image fit'):self.build(bad)
  outside=self.home/'outside.png';Image.new('RGB',(10,10),'red').save(outside)
  bad=json.loads(json.dumps(base));bad['pages'][0]['layers'].append({'type':'image','decorative':True,'path':'../outside.png','x':0,'y':0,'w':10,'h':10})
  with self.assertRaisesRegex(ValueError,'leaves the workspace'):self.build(bad)
  bad=json.loads(json.dumps(base));bad['pages'][0]['layers'].append({'type':'image','decorative':True,'path':'assets/missing.png','x':0,'y':0,'w':10,'h':10})
  with self.assertRaisesRegex(ValueError,'Missing asset'):self.build(bad)
 def test_missing_character_is_not_silent_font_fallback(self):
  b=self.book();b['pages'][0]['layers'].append({'type':'text','text':chr(0x10ffff),'font':'default','x':0,'y':0,'w':100,'h':100})
  with self.assertRaisesRegex(ValueError,'lacks characters'):self.build(b)
 def test_archive_traversal_rejected_before_writes(self):
  z=self.home/'bad.zip'
  with zipfile.ZipFile(z,'w') as f:f.writestr('../../outside.png','bad')
  with self.assertRaisesRegex(ValueError,'escapes'):self.api.install_pack(argparse.Namespace(workspace=str(self.root),archive=str(z),name='testpack',sha256=None))
  self.assertFalse((self.root/'assets/testpack').exists())
if __name__=='__main__':unittest.main()

