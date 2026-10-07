from pathlib import Path
import unittest,tempfile,json,subprocess,sys,hashlib
from make_demo import make,REPO
class WorkflowTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.root=make(Path(cls.temp.name)/'book');cls.base=json.loads((cls.root/'project/book.json').read_text(encoding='utf-8'));cls.before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (cls.root/'test-input').glob('*.png')}
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def setUp(self):(self.root/'project/book.json').write_text(json.dumps(self.base),encoding='utf-8')
 def build(self,book):
  (self.root/'project/book.json').write_text(json.dumps(book),encoding='utf-8');return subprocess.run(['node',str(self.root/'scripts/build.mjs')],capture_output=True,text=True)
 def test_fresh_install_carries_runtime(self):
  result=self.build(self.base);self.assertEqual(result.returncode,0,result.stderr);audit=json.loads((self.root/'project/build-audit.json').read_text(encoding='utf-8'));self.assertEqual((audit['selected'],audit['placed'],audit['omitted']),(8,8,0))
 def test_fresh_workspace_receives_agent_contract(self):
  contract=self.root/'AGENTS.md';self.assertTrue(contract.is_file());text=contract.read_text(encoding='utf-8');self.assertIn('photo-book-studio',text);self.assertIn('project/brief.json',text)
 def test_duplicate_rejected(self):
  book=json.loads(json.dumps(self.base));book['spreads'][0]['left']['photos'].append(book['spreads'][0]['left']['photos'][0]);self.assertNotEqual(self.build(book).returncode,0)
 def test_omission_rejected(self):
  book=json.loads(json.dumps(self.base));book['spreads'][0]['left']['photos']=[];self.assertNotEqual(self.build(book).returncode,0)
 def test_missing_assets_rejected(self):
  for scope in ['cover','background','derivative']:
   book=json.loads(json.dumps(self.base))
   if scope=='cover':book['cover']['path']='assets/missing.png'
   elif scope=='background':book['spreads'][0]['left']['backgroundPath']='assets/missing.png'
   else:book['spreads'][0]['left']['photos'][0]['path']='assets/missing.png'
   self.assertNotEqual(self.build(book).returncode,0,scope)
 def test_explicit_repetition_supported(self):
  book=json.loads(json.dumps(self.base));book['policy']['authorizedOccurrences']={'fixture-01.png':2};book['spreads'][0]['left']['photos'].append(book['spreads'][0]['left']['photos'][0]);self.assertEqual(self.build(book).returncode,0)
 def test_sources_unchanged_and_reimport_idempotent(self):
  subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'inventory','--workspace',str(self.root),'--photos',str(self.root/'test-input')],check=True)
  self.assertEqual(len(json.loads((self.root/'project/inventory.json').read_text(encoding='utf-8'))['photos']),8)
  for p in (self.root/'test-input').glob('*.png'):self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),self.before[p.name])
 def test_existing_project_not_overwritten(self):
  result=subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'init',str(self.root)],capture_output=True,text=True);self.assertNotEqual(result.returncode,0)
 def test_dimensions_and_user_text_are_not_personal_defaults(self):
  book=json.loads(json.dumps(self.base));book['format'].update(trimWidthMm=180,trimHeightMm=240);book['title']='A < B';self.assertEqual(self.build(book).returncode,0);html=(self.root/'sample.html').read_text(encoding='utf-8');self.assertIn('--spread-ratio:1.5',html);self.assertIn('<title>A &lt; B</title>',html);self.assertNotIn('<audio ',html)
 def test_unicode_filename_and_exif_orientation(self):
  from PIL import Image
  root=Path(self.temp.name)/'unicode-book';subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'init',str(root)],check=True)
  brief=json.loads((root/'project/brief.json').read_text(encoding='utf-8'));brief['intakeComplete']=True;(root/'project/brief.json').write_text(json.dumps(brief),encoding='utf-8')
  inputs=root/'test-input';inputs.mkdir();im=Image.new('RGB',(640,480),'#779991');exif=im.getexif();exif[274]=6;source=inputs/'照片.jpg';im.save(source,exif=exif);before=hashlib.sha256(source.read_bytes()).hexdigest()
  subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'inventory','--workspace',str(root),'--photos',str(inputs)],check=True)
  record=json.loads((root/'project/inventory.json').read_text(encoding='utf-8'))['photos'][0];self.assertEqual((record['width'],record['height']),(480,640));self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),before)
 def test_avif_input_is_inventoried(self):
  from PIL import Image
  root=Path(self.temp.name)/'avif-book';subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'init',str(root)],check=True)
  brief=json.loads((root/'project/brief.json').read_text(encoding='utf-8'));brief['intakeComplete']=True;(root/'project/brief.json').write_text(json.dumps(brief),encoding='utf-8')
  inputs=root/'test-input';inputs.mkdir();Image.new('RGB',(480,640),'#779991').save(inputs/'photo.avif',format='AVIF')
  subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'inventory','--workspace',str(root),'--photos',str(inputs)],check=True)
  record=json.loads((root/'project/inventory.json').read_text(encoding='utf-8'))['photos'][0];self.assertEqual(record['file'],'photo.avif');self.assertEqual((record['width'],record['height']),(480,640))
if __name__=='__main__':unittest.main()
