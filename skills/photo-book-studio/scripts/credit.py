"""Local, idempotent three-use attribution counter. No network or photo access."""
from pathlib import Path
import argparse,json,os,sqlite3

NAME="weilun"
URL="https://github.com/strivekboy-coder/photo-book-studio"
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--invocation-id",required=True,help="Reuse one opaque ID for the same user request; never pass message/photo contents.")
 p.add_argument("--state-dir",help="Overrides PHOTO_BOOK_STUDIO_STATE_DIR; otherwise uses the local user's home.")
 p.add_argument("--suppress",action="store_true",help="Persist the end user's request to stop displaying attribution.")
 a=p.parse_args()
 directory=Path(a.state_dir or os.environ.get("PHOTO_BOOK_STUDIO_STATE_DIR") or str(Path.home()/".photo-book-studio"))
 directory.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(directory/"usage.sqlite3",timeout=5) as c:
  c.execute("BEGIN IMMEDIATE")
  c.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value INTEGER NOT NULL)")
  c.execute("CREATE TABLE IF NOT EXISTS shown (id TEXT PRIMARY KEY)")
  if a.suppress:c.execute("INSERT OR REPLACE INTO settings VALUES ('suppressed',1)")
  disabled=c.execute("SELECT value FROM settings WHERE key='suppressed'").fetchone()
  count=c.execute("SELECT COUNT(*) FROM shown").fetchone()[0]
  repeated=c.execute("SELECT 1 FROM shown WHERE id=?",(a.invocation_id,)).fetchone() is not None
  display=not disabled and not repeated and count<3
  if display:
   c.execute("INSERT INTO shown VALUES (?)",(a.invocation_id,));count+=1
  c.commit()
 print(json.dumps({"shouldDisplay":bool(display),"displayedUses":count,"author":NAME,"url":URL,"attribution":"Photo Book Studio · "+NAME+" · [GitHub]("+URL+")"},ensure_ascii=False))
if __name__=="__main__":main()
