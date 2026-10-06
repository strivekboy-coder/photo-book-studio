"""Portable project setup and photo inventory. Does not choose memories or layouts."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
from datetime import datetime,timezone
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parents[1]
EXTS={'.jpg','.jpeg','.png','.webp','.gif','.avif','.heic','.heif'}
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def init(args):
 root=Path(args.workspace).resolve()
 if (root/'project/book.json').exists():raise ValueError('Existing book found. Initialization will not overwrite it.')
 for name in ('src','scripts','assets'):shutil.copytree(HERE/'runtime'/name,root/name,dirs_exist_ok=True)
 for name in ('requirements.txt','requirements-print.txt'):shutil.copy2(HERE/'runtime'/name,root/name)
 (root/'assets/photos').mkdir(parents=True,exist_ok=True)
 (root/'assets/cover-placeholder.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200"><rect width="1200" height="1200" fill="#f5f0e7"/></svg>',encoding='utf-8')
 brief={'intakeComplete':False,'story':{},'output':{},'selection':{},'visual':{'coverTiming':{'value':'after-interior-and-whole-book-review','source':'inferred'}},'copy':{},'permissions':{}}
 save(root/'project/brief.json',brief)
 save(root/'project/book.json',{'title':args.title,'subtitle':'','photoRoot':'assets/photos/','policy':{'allSelectedPhotosRequired':True,'allowUnusedPhotos':False},'format':{'trimWidthMm':args.width,'trimHeightMm':args.height,'bleedMm':3,'safeMarginMm':10},'cover':{'path':'assets/cover-placeholder.svg','position':'50% 50%','backColor':'#f5f0e7','integratedText':False},'spreads':[]})
 save(root/'project/inventory.json',{'photos':[]})
 print(f'Initialized {root}. Resolve the intake and save brief.intakeComplete before importing photos.')
def inventory(args):
 root=Path(args.workspace).resolve();source=Path(args.photos).resolve();brief=read(root/'project/brief.json')
 if not brief.get('intakeComplete'):raise ValueError('Complete and save the first-use questionnaire before importing photos.')
 files=sorted(p for p in (source.rglob('*') if args.recursive else source.iterdir()) if p.is_file() and p.suffix.lower() in EXTS)
 if not files:raise ValueError('No supported photos found.')
 names=[p.name for p in files]
 if len(names)!=len(set(names)):raise ValueError('Duplicate basenames in upload. Separate batches or assign source IDs before importing; nothing copied.')
 previous=read(root/'project/inventory.json');records={p['file']:p for p in previous['photos']};new=[];planned=[]
 for p in files:
  digest=sha(p);target=root/'assets/photos'/p.name
  if target.exists() and sha(target)!=digest:raise ValueError(f'Source ID collision: {p.name}; existing original preserved.')
  if p.name in records and records[p.name]['sha256']!=digest:raise ValueError(f'Inventory hash mismatch: {p.name}')
  if p.name in records:continue
  with Image.open(p) as im:
   exif=im.getexif();original=im.size;orient=exif.get(274,1);capture=None
   try:sub=exif.get_ifd(34665)
   except Exception:sub={}
   raw=sub.get(36867) or exif.get(36867)
   if raw:
    try:capture=datetime.strptime(str(raw),'%Y:%m:%d %H:%M:%S').isoformat()
    except ValueError:pass
   corrected=ImageOps.exif_transpose(im);w,h=corrected.size
  record={'file':p.name,'width':w,'height':h,'storedDimensions':list(original),'exifOrientation':orient,'orientation':'portrait' if h>w else 'landscape' if w>h else 'square','capturedAt':capture,'dateSource':'exif' if capture else 'filename-fallback','sha256':digest,'bytes':p.stat().st_size}
  if p.suffix.lower() in {'.heic','.heif'}:raise ValueError(f'{p.name}: convert to JPEG/PNG before browser layout; originals remain untouched.')
  planned.append((p,target,record))
 # All files are readable and collision-free before starting writes.
 for p,target,record in planned:
  if not target.exists():shutil.copy2(p,target)
  records[p.name]=record;new.append(record)
 previous={'generatedAt':datetime.now(timezone.utc).isoformat(),'selected':len(records),'newPhotos':len(new),'photos':sorted(records.values(),key=lambda p:(p['capturedAt'] or '9999',p['file']))};save(root/'project/inventory.json',previous)
 if new:
  ordered=sorted(new,key=lambda p:(p['capturedAt'] or '9999',p['file']));columns=4;cell=(300,270);sheet=Image.new('RGB',(columns*cell[0],((len(ordered)+columns-1)//columns)*cell[1]),'#f5f0e7');draw=ImageDraw.Draw(sheet);label_font=ImageFont.truetype(str(root/'assets/fonts/LXGWWenKaiLite-Regular.ttf'),16)
  for i,p in enumerate(ordered):
   with Image.open(root/'assets/photos'/p['file']) as im:thumb=ImageOps.exif_transpose(im).convert('RGB');thumb.thumbnail((280,225))
   x=(i%columns)*cell[0];y=(i//columns)*cell[1];sheet.paste(thumb,(x+(300-thumb.width)//2,y+5+(225-thumb.height)//2));draw.text((x+8,y+235),f'{i+1:02d} {p["file"][:36]}',fill='#24201c',font=label_font)
  dest=root/'tmp/contact-sheets';dest.mkdir(parents=True,exist_ok=True);sheet.save(dest/f'batch-{len(records):04d}.jpg',quality=90)
 print(json.dumps({'selected':len(records),'newPhotos':len(new),'alreadyInventoried':len(files)-len(new)}))
def build(args):subprocess.run(['node',str(Path(args.workspace).resolve()/'scripts/build.mjs')],check=True)
def web(args):
 root=Path(args.workspace).resolve();build(args);book=read(root/'project/book.json');dest=root/'output/web-publish';dest.mkdir(parents=True,exist_ok=True)
 # References are already verified by the build. Export only referenced assets and fonts.
 paths={book['cover']['path']} if book['cover'].get('path') else {book['photoRoot']+book['cover']['photo']}
 for key in ('backPath','spinePath'):
  if book['cover'].get(key):paths.add(book['cover'][key])
 for spread in book['spreads']:
  if spread.get('backgroundPhoto'):paths.add(spread['backgroundPhoto']['path'])
  for side in ('left','right'):
   page=spread[side]
   paths.update(p.get('path') or book['photoRoot']+p['file'] for p in page.get('photos',[]))
   paths.update(s['path'] for s in page.get('stickers',[]))
   if page.get('backgroundPath'):paths.add(page['backgroundPath'])
 paths.update(str(p.relative_to(root)).replace('\\','/') for p in (root/'assets/fonts').iterdir() if p.is_file())
 for rel in paths:
  target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,target)
 shutil.copy2(root/'sample.html',dest/'index.html')
 print(f'Publish folder: {dest}. Website hosting is separate; no authentication is added by default.')
def doctor(args):
 import importlib.util
 modules=['PIL','playwright','pypdf','reportlab'];print(json.dumps({'python':sys.version.split()[0],'node':shutil.which('node'),'modules':{m:importlib.util.find_spec(m) is not None for m in modules},'printSetup':'python -m pip install -r requirements-print.txt; python -m playwright install chromium; or export with --browser pointing to installed Edge/Chrome'}))
def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('init');p.add_argument('workspace');p.add_argument('--title',default='Photo Book');p.add_argument('--width',type=float,default=210);p.add_argument('--height',type=float,default=210);p.set_defaults(func=init)
 p=sub.add_parser('inventory');p.add_argument('--workspace',required=True);p.add_argument('--photos',required=True);p.add_argument('--recursive',action='store_true');p.set_defaults(func=inventory)
 for name,func in [('build',build),('web',web)]:p=sub.add_parser(name);p.add_argument('--workspace',required=True);p.set_defaults(func=func)
 p=sub.add_parser('doctor');p.set_defaults(func=doctor)
 args=parser.parse_args()
 try:args.func(args)
 except (ValueError,OSError,subprocess.CalledProcessError) as e:parser.exit(1,f'{e}\n')
if __name__=='__main__':main()
