"""Standalone Plog workspaces: truthful photo layers, count audit and browser export.
Does not choose photographs, captions or layouts for the user.
"""
from pathlib import Path
from collections import Counter
import argparse,json,shutil,hashlib,html,re,sys,urllib.request,urllib.parse,zipfile,io
import studio
HERE=Path(__file__).resolve().parents[1]
FONT_SOURCES={
 "yozai":{"url":"https://github.com/lxgw/yozai-font/releases/download/v0.868/Yozai-Medium.ttf","license":"https://raw.githubusercontent.com/lxgw/yozai-font/master/OFL.txt"},
 "xiaolai":{"url":"https://github.com/lxgw/kose-font/releases/download/v3.126/Xiaolai-Regular.ttf","license":"https://raw.githubusercontent.com/lxgw/kose-font/master/OFL.txt"}
}
def read(p):return studio.read(p)
def save(p,v):studio.save(p,v)
def sha(p):return studio.sha(p)
def local(root,rel):
 p=Path(rel)
 if p.is_absolute():raise ValueError(f"Use a project-relative asset path: {rel}")
 target=(root/p).resolve()
 if not target.is_relative_to(root.resolve()):raise ValueError(f"Asset leaves the workspace: {rel}")
 if not target.is_file():raise ValueError(f"Missing asset: {rel}")
 return target
def number(value,name):
 if isinstance(value,bool) or not isinstance(value,(int,float)):raise ValueError(f"{name} must be numeric")
 import math
 if not math.isfinite(value):raise ValueError(f"{name} must be finite")
 return value
def css(value):
 value=str(value)
 if any(x in value for x in [';','<','>','"',"'",'\\','url(']):raise ValueError(f"Unsupported style value: {value}")
 return value
def init(args):
 root=Path(args.workspace).resolve()
 if (root/'project/book.json').exists() or (root/'project/brief.json').exists():raise ValueError("Existing project found; initialization will not overwrite it.")
 (root/'assets/photos').mkdir(parents=True,exist_ok=True);(root/'assets/fonts').mkdir(exist_ok=True)
 for p in (HERE/'runtime/assets/fonts').iterdir():
  if p.name in {'LXGWWenKaiLite-Regular.ttf','OFL-LXGW-WenKai-Lite.txt'}:shutil.copy2(p,root/'assets/fonts'/p.name)
 shutil.copytree(HERE/'assets/plog-starter',root/'assets/plog-starter',dirs_exist_ok=True)
 save(root/'project/brief.json',{'kind':'plog','intakeComplete':False,'story':{},'output':{'value':'standalone PNGs and browser preview','source':'inferred'},'visual':{},'copy':{},'permissions':{}})
 save(root/'project/inventory.json',{'photos':[],'selected':0})
 shutil.copy2(HERE/'references/zine-policy.md',root/'project/zine-review-policy.md')
 shutil.copy2(HERE/'references/creative-prompts.md',root/'project/creative-prompts.md')
 save(root/'project/book.json',{'kind':'plog','title':args.title,'photoRoot':'assets/photos/','format':{'widthPx':1200,'heightPx':1600},'fonts':{'default':'assets/fonts/LXGWWenKaiLite-Regular.ttf'},'policy':{'allSelectedPhotosRequired':True,'authorizedOccurrences':{}},'pages':[]})
 (root/'AGENTS.md').write_text("# Standalone Plog workspace\n\nRead project/brief.json before acting. Resolve only missing story, output, style, copy and treatment preferences, record their sources, and set intakeComplete before inventory. This is not a printed book questionnaire. Keep originals read-only and every selected source once unless repeats are authorized. Record all layers in project/book.json. Use reference/material/font research before composing. Dense layouts are allowed; faces, hands, essential subjects and copy must remain readable. Mark decoration separately. Build sample.html, render every changed canvas in a real browser and inspect pixels; automated counts do not certify aesthetics. Do not publish private photographs without explicit authorization.\n",encoding='utf-8')
 print(f"Initialized {root}. Resolve and save the Plog brief before importing photos.")
def inventory(args):
 root=Path(args.workspace).resolve()
 if not read(root/'project/brief.json').get('intakeComplete'):raise ValueError("Resolve the Plog brief and set intakeComplete before importing photos.")
 studio.inventory(args)
def fetch_font(args):
 root=Path(args.workspace).resolve();entry=FONT_SOURCES[args.name]
 target=root/'assets/fonts'/f'{args.name}.ttf';license_target=root/'assets/fonts'/f'{args.name}.OFL.txt'
 if target.exists() and license_target.exists():
  print(f"Using cached {args.name}");return
 raw=urllib.request.urlopen(entry['url'],timeout=60).read();license_raw=urllib.request.urlopen(entry['license'],timeout=30).read()
 if raw[:4] not in [b'\x00\x01\x00\x00',b'OTTO',b'ttcf']:raise ValueError("Font download was not a supported font file.")
 if b'OPEN FONT LICENSE' not in license_raw.upper():raise ValueError("Font license download was not the expected OFL notice.")
 target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists() and target.read_bytes()!=raw:raise ValueError("Existing font differs; choose a versioned destination instead of overwriting.")
 target.write_bytes(raw);license_target.write_bytes(license_raw)
 save(root/'project'/f'font-{args.name}.json',{'source':entry['url'],'license':entry['license'],'path':f'assets/fonts/{args.name}.ttf','sha256':sha(target)})
 print(f"Cached {args.name} and its license.")
def install_pack(args):
 root=Path(args.workspace).resolve();archive=Path(args.archive).resolve()
 if args.sha256 and sha(archive).lower()!=args.sha256.lower():raise ValueError("Material pack hash mismatch.")
 folder=root/'assets'/args.name
 if folder.exists():raise ValueError("Material pack destination exists; use a new versioned name.")
 if not re.fullmatch(r'[a-zA-Z0-9_-]+',args.name):raise ValueError("Invalid pack name.")
 with zipfile.ZipFile(archive) as z:
  if sum(i.file_size for i in z.infolist())>150_000_000:raise ValueError("Material pack is too large.")
  for info in z.infolist():
   target=(folder/info.filename).resolve()
   if not target.is_relative_to(folder.resolve()):raise ValueError("Material pack path escapes its destination.")
   if not info.is_dir() and Path(info.filename).suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.svg','.json','.txt','.md'}:raise ValueError("Unexpected material-pack file type.")
  folder.mkdir(parents=True,exist_ok=True);z.extractall(folder)
 save(root/'project'/f'material-pack-{args.name}.json',{'archive':archive.name,'sha256':sha(archive),'path':f'assets/{args.name}','licenseReview':'User/agent must record and verify provenance before using individual assets.'})
 print(f"Installed optional material pack at {folder}")
def build(args):
 root=Path(args.workspace).resolve();book=read(root/'project/book.json');inv=read(root/'project/inventory.json')
 if book.get('kind')!='plog':raise ValueError("This renderer accepts kind: plog only.")
 if not read(root/'project/brief.json').get('intakeComplete'):raise ValueError("Plog brief is unresolved.")
 records={p['file']:p for p in inv.get('photos',[])}
 if len(records)!=len(inv.get('photos',[])):raise ValueError("Duplicate source IDs in inventory.")
 if not records:raise ValueError("No selected photographs.")
 width=number(book.get('format',{}).get('widthPx',1200),'widthPx');height=number(book.get('format',{}).get('heightPx',1600),'heightPx')
 if not 100<=width<=12000 or not 100<=height<=12000:raise ValueError("Unsupported canvas size.")
 fonts=book.get('fonts',{});font_css=[]
 for name,path in fonts.items():
  if not re.fullmatch(r'[\w-]+',name):raise ValueError("Invalid font role.")
  local(root,path);font_css.append(f"@font-face{{font-family:{name};src:url('{urllib.parse.quote(path,safe='/')}')}}")
 from fontTools.ttLib import TTFont
 font_maps={}
 for name,path in fonts.items():
  with TTFont(str(local(root,path))) as f:font_maps[name]=f.getBestCmap()
 counts=Counter();sections=[];geometry=[];paths=set(fonts.values())
 for pi,page in enumerate(book.get('pages',[]),1):
  layers=[]
  for li,obj in enumerate(page.get('layers',[]),1):
   typ=obj.get('type');x=number(obj.get('x',0),'x');y=number(obj.get('y',0),'y');w=number(obj.get('w',0),'w');h=number(obj.get('h',0),'h')
   if w<=0 or h<=0:raise ValueError(f"Page {pi} layer {li} has empty dimensions.")
   rot=number(obj.get('rotate',0),'rotate');z=number(obj.get('z',li),'z');opacity=number(obj.get('opacity',1),'opacity')
   if not 0<=opacity<=1:raise ValueError("Opacity outside 0..1.")
   style=f"left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};opacity:{opacity};"
   # Geometry is advisory: off-canvas bleed may be deliberate, subjects still need visual review.
   if x<0 or y<0 or x+w>width or y+h>height:geometry.append({'page':pi,'layer':li,'note':'Base box crosses canvas; inspect intentional bleed/crop'})
   if typ in {'photo','image'}:
    if typ=='photo':
     file=obj.get('file')
     if file not in records:raise ValueError(f"Unknown selected source: {file}")
     counts[file]+=1
     original=book.get('photoRoot','assets/photos/')+file;path=obj.get('path') or original
     if path!=original:
      approval=read(root/'project/brief.json').get('permissions',{}).get('approvedDerivatives',{}).get(file,{})
      if not obj.get('approvedDerivative') or approval.get('path')!=path or approval.get('source')!='explicit':raise ValueError(f"Derivative not explicitly approved in brief: {file}")
     source=local(root,original)
     if records[file].get('sha256') and sha(source)!=records[file]['sha256']:raise ValueError(f"Source changed: {file}")
    else:
     if obj.get('decorative') is not True:raise ValueError("Image-only layers must explicitly be decorative.")
     if obj.get('file'):raise ValueError("Decorative image cannot hide a selected source ID.")
     path=obj['path']
    local(root,path);paths.add(path)
    clip=obj.get('clip','none');clip_css={'none':'','circle':'border-radius:50%;','rounded':'border-radius:24px;','torn':'clip-path:polygon(0 1%,13% 0,27% 1%,44% 0,63% 1%,83% 0,100% 1%,99% 24%,100% 49%,99% 75%,100% 99%,83% 100%,64% 99%,43% 100%,23% 99%,0 100%,1% 73%,0 47%,1% 22%);'}
    if clip not in clip_css:raise ValueError("Unsupported photo mask.")
    border=number(obj.get('border',0),'border');mat=css(obj.get('mat','#fff7e7'));bottom=number(obj.get('matBottom',0),'matBottom')
    outer=f"padding:{border}px {border}px {border+bottom}px;background:{mat};" if border or bottom else ""
    if obj.get('shadow'):outer+="box-shadow:2px 5px 14px #0003;"
    crop=obj.get('sourceBox')
    if crop:
     if typ!='photo' or len(crop)!=4:raise ValueError("sourceBox is available for selected photographs only.")
     sx,sy,sw,sh=[number(v,'sourceBox') for v in crop];record=records[obj['file']]
     if min(sx,sy)<0 or min(sw,sh)<=0 or sx+sw>record['width']+1 or sy+sh>record['height']+1:raise ValueError("Source crop leaves the original image.")
     # One uniform scale: contain the requested region in the frame, with cover crop if needed.
     fw=w-2*border;fh=h-2*border-bottom;scale=max(fw/sw,fh/sh);iw=record['width']*scale;ih=record['height']*scale
     left=-sx*scale+(fw-sw*scale)/2;top=-sy*scale+(fh-sh*scale)/2
     img_style=f"position:absolute;width:{iw}px;height:{ih}px;left:{left}px;top:{top}px;object-fit:fill;"
    else:
     fit=obj.get('fit','cover' if typ=='photo' else 'contain')
     if fit not in ({'cover','contain'} if typ=='photo' else {'cover','contain','fill'}):raise ValueError("Unsupported image fit.")
     img_style=f"width:100%;height:100%;object-fit:{fit};object-position:{css(obj.get('position','50% 50%'))};"
    source_attr=f' data-source="{html.escape(obj["file"],quote=True)}"' if typ=='photo' else ""
    layers.append(f'<div class="layer" data-layer="{li}" style="{style}{outer}{clip_css[clip]}"><div style="position:relative;overflow:hidden;width:100%;height:100%;{clip_css[clip]}"><img{source_attr} src="{html.escape(path,quote=True)}" style="{img_style}"></div></div>')
   elif typ=='text':
    font=obj.get('font','default')
    if font not in fonts:raise ValueError(f"Undefined font role: {font}")
    missing=sorted({c for c in obj.get('text','') if not c.isspace() and ord(c) not in font_maps[font]})
    if missing:raise ValueError(f"Font {font} lacks characters: {''.join(missing)}; choose a complete font instead of silent fallback.")
    size=number(obj.get('size',36),'size');line=number(obj.get('lineHeight',1.35),'lineHeight')
    color=css(obj.get('color','#fff'));align=css(obj.get('align','left'))
    extra=f"font-family:{font};font-size:{size}px;line-height:{line};color:{color};text-align:{align};white-space:pre-wrap;"
    if obj.get('outline'):extra+=f"-webkit-text-stroke:{number(obj.get('outlineWidth',3),'outlineWidth')}px {css(obj['outline'])};paint-order:stroke fill;"
    layers.append(f'<div class="layer text" data-layer="{li}" style="{style}{extra}">{html.escape(obj.get("text",""))}</div>')
   elif typ=='paper':
    color=css(obj.get('color','#f4eedf'));pattern=obj.get('pattern','none');gap=number(obj.get('gap',28),'gap');ink=css(obj.get('ink','#adb59b55'))
    pattern_css={'none':'','grid':f'background-image:linear-gradient({ink} 1px,transparent 1px),linear-gradient(90deg,{ink} 1px,transparent 1px);background-size:{gap}px {gap}px;','ruled':f'background-image:linear-gradient({ink} 1px,transparent 1px);background-size:100% {gap}px;','dots':f'background-image:radial-gradient({ink} 1px,transparent 1px);background-size:{gap}px {gap}px;'}
    if pattern not in pattern_css:raise ValueError("Unknown paper pattern.")
    layers.append(f'<div class="layer" data-layer="{li}" style="{style}background-color:{color};{pattern_css[pattern]}"></div>')
   elif typ=='path':
    d=css(obj.get('d',''));stroke=css(obj.get('color','#fff'));stroke_width=number(obj.get('strokeWidth',4),'strokeWidth')
    fill=css(obj.get('fill','none'));dash=f' stroke-dasharray="{css(obj["dash"])}"' if obj.get('dash') else ''
    view=obj.get('viewBox',[0,0,w,h])
    if len(view)!=4:raise ValueError("SVG viewBox requires four numbers.")
    view=[number(v,'viewBox') for v in view]
    if min(view[2:])<=0:raise ValueError("SVG viewBox must have positive dimensions.")
    parts=obj.get('parts',[{'d':d,'dash':obj.get('dash')}])
    paths_html=[]
    for part in parts:
     part_dash=f' stroke-dasharray="{css(part["dash"])}"' if part.get('dash') else ''
     paths_html.append(f'<path d="{css(part.get("d",""))}"{part_dash}/>')
    layers.append(f'<svg class="layer" data-layer="{li}" style="{style}" viewBox="{" ".join(str(v) for v in view)}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">{"".join(paths_html)}</svg>')
   else:raise ValueError(f"Unsupported layer type: {typ}")
  sections.append(f'<div class="mount"><section class="canvas" id="page-{pi}" data-page="{pi}" style="background:{css(page.get("background","#f5eddd"))}"><div class="artwork">{"".join(layers)}</div></section></div>')
 expected={f:book.get('policy',{}).get('authorizedOccurrences',{}).get(f,1) for f in records}
 for f,n in expected.items():
  if not isinstance(n,int) or isinstance(n,bool) or n<1:raise ValueError("Authorized occurrences must be positive integers.")
  if counts[f]!=n:raise ValueError(f"Selection invariant failed: {f} expected {n}, placed {counts[f]}")
 if not sections:raise ValueError("No composed pages.")
 title=html.escape(book.get('title','Plog'));style=''.join(font_css)+f"""
*{{box-sizing:border-box}}body{{margin:0;background:#272d2d;color:#eee;font-family:system-ui}}.viewer{{padding:24px;max-width:{width+80}px;margin:auto}}.intro{{font-size:17px;line-height:1.7;margin-bottom:24px}}.mount{{width:calc({width}px * var(--scale));height:calc({height}px * var(--scale));margin:0 auto 26px}}.canvas{{position:relative;width:{width}px;height:{height}px;overflow:hidden;isolation:isolate;transform:scale(var(--scale));transform-origin:top left}}.layer{{position:absolute}}.layer img{{display:block}}.export .intro{{display:none}}.export .viewer{{padding:0;max-width:none}}.export .mount{{--scale:1;width:{width}px;height:{height}px;margin:0}}.export .mount:not(.active){{display:none}}
"""
 script=f"""const q=new URLSearchParams(location.search);if(q.has('export')){{document.body.classList.add('export');document.getElementById('page-'+q.get('export')).parentElement.classList.add('active')}}else{{function fit(){{document.documentElement.style.setProperty('--scale',Math.min(1,(innerWidth-32)/{width}))}}fit();addEventListener('resize',fit)}}"""
 editor_css=(HERE/'assets/plog-editor/editor.css').read_text(encoding='utf-8')
 editor_js=(HERE/'assets/plog-editor/editor.js').read_text(encoding='utf-8')
 editor_data=json.dumps({'book':book,'inventory':inv['photos'],'revision':sha(root/'project/book.json')},ensure_ascii=False).replace('<','\\u003c')
 html_text=f'<!doctype html><html lang="zh"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{style}{editor_css}</style><body><main class="viewer"><div class="intro">{title} · {len(sections)}页</div>{"".join(sections)}</main><script>{script}</script><script type="application/json" id="plog-data">{editor_data}</script><script>{editor_js}</script></body></html>'
 (root/'sample.html').write_text(html_text,encoding='utf-8')
 audit={'selected':len(records),'placed':sum(counts.values()),'omitted':0,'pages':len(sections),'sourceOccurrences':dict(counts),'expectedOccurrences':expected,'assets':sorted(paths),'geometryAdvisories':geometry,'browserInspectionRequired':True,'bookSha256':sha(root/'project/book.json')}
 save(root/'project/build-audit.json',audit);print(json.dumps({k:audit[k] for k in ['selected','placed','omitted','pages']}))
 return audit
def render(args):
 root=Path(args.workspace).resolve();audit=build(args)
 from playwright.sync_api import sync_playwright
 book=read(root/'project/book.json');w=int(book['format']['widthPx']);h=int(book['format']['heightPx'])
 selected=args.page or list(range(1,audit['pages']+1))
 if any(p<1 or p>audit['pages'] for p in selected):raise ValueError("Requested page not found.")
 out=root/'output/plog';out.mkdir(parents=True,exist_ok=True);reports=[]
 with sync_playwright() as p:
  kwargs={'headless':True}
  if args.browser:kwargs['executable_path']=args.browser
  browser=p.chromium.launch(**kwargs);pg=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  for pi in selected:
   pg.goto((root/'sample.html').as_uri()+f'?export={pi}');pg.evaluate('document.fonts.ready')
   pg.wait_for_function('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
   pg.locator(f'#page-{pi}').screenshot(path=str(out/f'page-{pi:02}.png'))
   count=pg.locator(f'#page-{pi} [data-source]').count();reports.append({'page':pi,'photoOccurrences':count,'png':f'output/plog/page-{pi:02}.png','visualStatus':'requires inspection'})
  pg.set_viewport_size({'width':400,'height':850});pg.goto((root/'sample.html').as_uri());pg.evaluate('document.fonts.ready');pg.wait_for_function('Array.from(document.images).every(i=>i.complete)')
  for pi in selected:pg.locator(f'#page-{pi}').screenshot(path=str(out/f'page-{pi:02}-phone.png'))
  browser.close()
 deliveries=[]
 if getattr(args,'jpg',False) or getattr(args,'pdf',False):
  from PIL import Image
  images=[]
  try:
   for pi in selected:
    with Image.open(out/f'page-{pi:02}.png') as source:
     if source.mode=='RGBA':
      canvas=Image.new('RGB',source.size,'white');canvas.paste(source,mask=source.getchannel('A'))
     else:canvas=source.convert('RGB')
    if getattr(args,'jpg',False):
     target=out/f'page-{pi:02}.jpg';canvas.save(target,quality=95,subsampling=0);deliveries.append(f'output/plog/{target.name}')
    images.append(canvas)
   if getattr(args,'pdf',False) and images:
    # A reading PDF, with a consistent 144 dpi page size; no print bleed claim.
    suffix='' if selected==list(range(1,audit['pages']+1)) else '-pages-'+'-'.join(str(v) for v in selected)
    target=out/f'plog{suffix}.pdf';images[0].save(target,'PDF',save_all=True,append_images=images[1:],resolution=144.0,title=book.get('title','Plog'))
    deliveries.append(f'output/plog/{target.name}')
  finally:
   for image in images:image.close()
 save(root/'project/render-report.json',{'pages':reports,'deliverables':deliveries,'pdfPurpose':'reading, not print preflight' if getattr(args,'pdf',False) else None,'phonePreviews':True,'notAestheticApproval':True,'bookSha256':audit['bookSha256']});print(f"Rendered {len(selected)} page(s); inspect full and phone PNGs before approval.")
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 q=sub.add_parser('init');q.add_argument('workspace');q.add_argument('--title',default='Plog');q.set_defaults(func=init)
 q=sub.add_parser('inventory');q.add_argument('--workspace',required=True);q.add_argument('--photos',required=True);q.add_argument('--recursive',action='store_true');q.set_defaults(func=inventory)
 q=sub.add_parser('font');q.add_argument('--workspace',required=True);q.add_argument('--name',choices=FONT_SOURCES,required=True);q.set_defaults(func=fetch_font)
 q=sub.add_parser('material-pack');q.add_argument('--workspace',required=True);q.add_argument('--archive',required=True);q.add_argument('--name',required=True);q.add_argument('--sha256');q.set_defaults(func=install_pack)
 q=sub.add_parser('build');q.add_argument('--workspace',required=True);q.set_defaults(func=build)
 q=sub.add_parser('render');q.add_argument('--workspace',required=True);q.add_argument('--browser');q.add_argument('--page',type=int,action='append');q.add_argument('--jpg',action='store_true',help='Also export high-quality sharing JPGs');q.add_argument('--pdf',action='store_true',help='Also export the rendered pages as a reading PDF');q.set_defaults(func=render)
 args=p.parse_args()
 try:args.func(args)
 except (ValueError,OSError,RuntimeError,ImportError) as e:p.exit(1,f'{e}\n')
if __name__=='__main__':main()

