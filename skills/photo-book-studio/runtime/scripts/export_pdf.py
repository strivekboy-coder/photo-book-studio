"""Export the current browser layout to fixed-layout print PDFs with real bleed."""
from pathlib import Path
import argparse,json,math,subprocess
from io import BytesIO
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.generic import NameObject,NumberObject,DictionaryObject,DecodedStreamObject,RectangleObject
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from playwright.sync_api import sync_playwright
PT=72/25.4

def bleed(writer,source,mm):
 w,h=map(float,(source.mediabox.width,source.mediabox.height));b=mm*PT;e=min(PT,w,h)
 form=DecodedStreamObject();form.set_data(source.get_contents().get_data());form.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),NameObject('/FormType'):NumberObject(1),NameObject('/BBox'):RectangleObject([0,0,w,h]),NameObject('/Resources'):source['/Resources'].clone(writer)})
 ref=writer._add_object(form);page=writer.add_blank_page(width=w+2*b,height=h+2*b);page[NameObject('/Resources')]=DictionaryObject({NameObject('/XObject'):DictionaryObject({NameObject('/Artwork'):ref})})
 commands=[]
 if b:
  for x,cw,sx,tx in [(0,b,b/e,0),(b,w,1,b),(b+w,b,b/e,b+w-(w-e)*b/e)]:
   for y,ch,sy,ty in [(0,b,b/e,0),(b,h,1,b),(b+h,b,b/e,b+h-(h-e)*b/e)]:
    if x==b and y==b and cw==w and ch==h:continue
    commands.append(f'q {x-.5} {y-.5} {cw+1} {ch+1} re W n {sx} 0 0 {sy} {tx} {ty} cm /Artwork Do Q')
 commands.append(f'q 1 0 0 1 {b} {b} cm /Artwork Do Q');stream=DecodedStreamObject();stream.set_data('\n'.join(commands).encode());page[NameObject('/Contents')]=writer._add_object(stream);page.trimbox=RectangleObject([b,b,b+w,b+h]);page.bleedbox=page.mediabox;page.cropbox=page.mediabox
 return page

def raster_page(data,w,h,side=None):
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(w,h),pageCompression=1)
 if side is None:c.drawImage(ImageReader(BytesIO(data)),0,0,width=w,height=h)
 else:
  c.saveState();p=c.beginPath();p.rect(0,0,w,h);c.clipPath(p,stroke=0,fill=0);c.drawImage(ImageReader(BytesIO(data)),-side*w,0,width=2*w,height=h);c.restoreState()
 c.showPage();c.save();buf.seek(0);return PdfReader(buf).pages[0]

def padding(w,h,text,color,ink,font):
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(w,h));c.setFillColor(color);c.rect(0,0,w,h,stroke=0,fill=1);c.setFillColor(ink);c.setFont(font,14);c.drawCentredString(w/2,h/2+8*PT,text);c.showPage();c.save();buf.seek(0);return PdfReader(buf).pages[0]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True);p.add_argument('--browser',help='Installed Chromium, Edge or Chrome executable; otherwise use Playwright Chromium');p.add_argument('--dpi',type=int,default=300);args=p.parse_args();root=Path(args.workspace).resolve()
 if not 72<=args.dpi<=600:p.error('--dpi must be between 72 and 600')
 subprocess.run(['node',str(root/'scripts/build.mjs')],check=True)
 book=json.loads((root/'project/book.json').read_text(encoding='utf-8'));fmt=book['format'];w=fmt['trimWidthMm']*PT;h=fmt['trimHeightMm']*PT;b=fmt.get('bleedMm',3)
 config=book.get('print',{});increment=config.get('pageIncrement',4)
 if not isinstance(increment,int) or increment<1:p.error('print.pageIncrement must be a positive integer')
 out=root/'output/pdf';out.mkdir(parents=True,exist_ok=True);cache=root/'tmp/pdf-render';cache.mkdir(parents=True,exist_ok=True)
 fontfile=root/'assets/fonts/LXGWWenKaiLite-Regular.ttf';pdfmetrics.registerFont(TTFont('BookPad',str(fontfile)))
 reading=PdfWriter();interior=PdfWriter();cover=PdfWriter();interior_source=[];capture_records=[];text_warnings=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True,**({'executable_path':args.browser} if args.browser else {}))
  context=browser.new_context(viewport={'width':1280,'height':1000},device_scale_factor=(fmt['trimWidthMm']/25.4*args.dpi/600))
  page=context.new_page();page.goto((root/'sample.html').as_uri());page.evaluate('document.fonts.ready')
  count=page.locator('.spread').count()
  assert count==len(book['spreads'])+1,(count,len(book['spreads']))
  for i in range(count):
   page.locator('#pageInput').fill(str(i+1));page.locator('#pageJump').evaluate('(form)=>form.dispatchEvent(new Event("submit",{bubbles:true,cancelable:true}))')
   page.evaluate('async()=>{await document.fonts.ready;await Promise.all([...document.querySelectorAll(".spread.active img")].map(i=>i.decode()));}')
   layout=page.locator('.spread.active').evaluate('s=>({width:s.getBoundingClientRect().width,height:s.getBoundingClientRect().height,missing:[...s.querySelectorAll("img")].filter(i=>!i.naturalWidth).map(i=>i.src),text:[...s.querySelectorAll(".page-caption,.love-letter,.spread-date")].map(t=>({px:parseFloat(getComputedStyle(t).fontSize),text:t.textContent.slice(0,40)}))})')
   if layout['missing']:raise ValueError(f'Missing browser images on spread {i+1}: {layout["missing"]}')
   for t in layout['text']:
    physical=t['px']/600*w
    if physical<8:text_warnings.append({'viewerSpread':i+1,'typeSizePt':round(physical,1),'text':t['text']})
   data=page.locator('.spread.active').screenshot(type='png',animations='disabled');im=Image.open(BytesIO(data)).convert('RGB');buf=BytesIO();im.save(buf,format='JPEG',quality=94);jpg=buf.getvalue();(cache/f'spread-{i+1:04d}.jpg').write_bytes(jpg)
   reading.add_page(raster_page(jpg,2*w,h));capture_records.append({'viewerSpread':i+1,'pixels':list(im.size),'effectiveExportDpi':round(im.width/(2*fmt['trimWidthMm']/25.4),1)})
   for side in (0,1):
    source=raster_page(jpg,w,h,side)
    if i==0:bleed(cover,source,b)
    else:interior_source.append(source)
   print(f'Rendered spread {i+1}/{count}',flush=True)
  context.close();browser.close()
 front=1 if config.get('frontPad',True) else 0;back=1 if config.get('backPad',True) else 0
 back+=(-(front+len(interior_source)+back))%increment
 paper=config.get('padColor','#f5f0e7');ink=config.get('padInk','#0b2442')
 sources=([padding(w,h,config.get('frontText',''),paper,ink,'BookPad')]*front)+interior_source
 sources += [padding(w,h,config.get('backText',''),paper,ink,'BookPad')] if back else []
 sources += [padding(w,h,'',paper,ink,'BookPad') for _ in range(max(0,back-1))]
 for src in sources:bleed(interior,src,b)
 # Spine is exported only from a supplied printer-confirmed width and supplied artwork.
 if config.get('spineWidthMm') and book['cover'].get('spinePath'):
  spine=root/book['cover']['spinePath'];width=config['spineWidthMm']*PT
  if spine.suffix.lower()=='.pdf':
   sr=PdfReader(spine);assert len(sr.pages)==1;sp=sr.pages[0]
   if abs(float(sp.mediabox.width)-width)>.1 or abs(float(sp.mediabox.height)-h)>.1:raise ValueError('Spine artwork dimensions differ from printer specification.')
  else:
   with Image.open(spine) as im:
    if abs(im.width/im.height-width/h)>.01:raise ValueError('Spine artwork aspect ratio differs from printer specification.')
   sp=raster_page(spine.read_bytes(),width,h)
  bleed(cover,sp,b)
 files=[]
 for name,writer in [('reading',reading),('interior',interior),('cover',cover)]:
  target=out/f'{name}.pdf';writer.add_metadata({'/Title':book.get('title','Photo Book')+' - '+name});writer.write(target);check=PdfReader(target)
  assert len(check.pages)==len(writer.pages)
  assert all(p.rotation%360==0 for p in check.pages)
  files.append({'file':target.name,'pages':len(check.pages)})
 report={'files':files,'viewerSpreads':count,'interiorPages':len(sources),'originalInteriorPages':len(interior_source),'padding':{'front':front,'back':back},'trimMm':[fmt['trimWidthMm'],fmt['trimHeightMm']],'bleedMm':b,'pageIncrement':increment,'allExportRotationsZero':True,'rasterExport':True,'note':'Raster export resolution does not increase source photo or generated-art detail. Review the rendered JPEGs and final PDF at trim size. Cover wrap/hinges still require printer adaptation.','physicalTextWarnings':text_warnings,'renderedSpreads':capture_records,'printReady':False}
 (out/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'interiorPages':len(sources),'files':files,'textWarnings':len(text_warnings)}))
if __name__=='__main__':main()
