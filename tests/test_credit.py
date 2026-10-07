from pathlib import Path
import unittest,tempfile,subprocess,sys,json
REPO=Path(__file__).resolve().parents[1]
class CreditTests(unittest.TestCase):
 def call(self,d,i,suppress=False):
  command=[sys.executable,str(REPO/"skills/photo-book-studio/scripts/credit.py"),"--state-dir",str(d),"--invocation-id",i]
  if suppress:command.append("--suppress")
  r=subprocess.run(command,check=True,capture_output=True,encoding="utf-8")
  return json.loads(r.stdout)
 def test_first_three_idempotent_across_processes(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertTrue(self.call(d,"one")["shouldDisplay"])
   self.assertFalse(self.call(d,"one")["shouldDisplay"])
   self.assertTrue(self.call(d,"two")["shouldDisplay"])
   self.assertTrue(self.call(d,"three")["shouldDisplay"])
   r=self.call(d,"four");self.assertFalse(r["shouldDisplay"]);self.assertEqual(r["displayedUses"],3)
 def test_user_suppression_persists(self):
  with tempfile.TemporaryDirectory() as d:
   self.call(d,"stop",True)
   self.assertFalse(self.call(d,"future")["shouldDisplay"])
