"""Make geometric fixtures for mechanics, not real-photo design evidence."""
from pathlib import Path
import argparse,json,subprocess,sys
from PIL import Image,ImageDraw
REPO=Path(__file__).resolve().parents[1]
def make(root):
 root=Path(root).resolve();subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'init',str(root),'--title','Everyday Shapes'],check=True)
 brief=json.loads((root/'project/brief.json').read_text(encoding='utf-8'));brief.update({'intakeComplete':True,'story':{'subject':{'value':'Geometric test fixtures, not photographs','source':'explicit'}},'copy':{'language':{'value':'English','source':'explicit'}}});(root/'project/brief.json').write_text(json.dumps(brief),encoding='utf-8')
 source=root/'test-input';source.mkdir()
 colors=['#779991','#b1876c','#8c9dac','#d0ae68','#ad8b96','#607f81','#91a899','#8591a8']
 for n,color in enumerate(colors):
  size=(600,800) if n%2 else (900,600);im=Image.new('RGB',size,color);draw=ImageDraw.Draw(im);w,h=size;draw.ellipse((w*.57,h*.10,w*.85,h*.10+w*.28),fill='#edd9a8');draw.polygon([(0,h),(w*.35,h*.36),(w*.7,h),(w*.85,h*.5),(w,h*.78),(w,h)],fill='#365552');draw.text((25,25),f'GEOMETRIC FIXTURE {n+1}',fill='white');im.save(source/f'fixture-{n+1:02d}.png')
 subprocess.run([sys.executable,str(REPO/'skills/photo-book-studio/scripts/studio.py'),'inventory','--workspace',str(root),'--photos',str(source)],check=True)
 def page(ids,caption,tone):
  if len(ids)==1:frames=[{'x':8,'y':6,'width':84,'height':75}]
  elif len(ids)==2:frames=[{'x':6,'y':6,'width':88,'height':37},{'x':6,'y':47,'width':88,'height':36}]
  else:frames=[{'x':6,'y':6,'width':52,'height':72},{'x':62,'y':6,'width':32,'height':33},{'x':62,'y':43,'width':32,'height':35}]
  return {'layout':'composed','family':'editorial','tone':tone,'plainBackground':True,'photos':[{'file':f'fixture-{i:02d}.png','fit':'contain','position':'50% 50%','frame':dict(frame,rotate=0,z=1)} for i,frame in zip(ids,frames)],'caption':caption,'captionStyle':'poem expressive-copy','captionPlacement':'manual','captionDesign':{'x':8,'y':85,'width':84,'font':'poem','size':'26px','align':'left','color':'#263b4b'},'stickers':[]}
 book=json.loads((root/'project/book.json').read_text(encoding='utf-8'));book['subtitle']='A functional test, made from geometric fixtures.';book['spreads']=[{'eyebrow':'FIXTURES / 01','left':page([1],'A quiet beginning.','cream'),'right':page([2,3,4],'A few little moments.','sage')},{'eyebrow':'FIXTURES / 02','left':page([5,6],'Room for two.','cream'),'right':page([7,8],'The story continues.','sky')}];book['print']={'frontText':'For the story.','backText':'To be continued.','pageIncrement':4,'frontPad':True,'backPad':True};(root/'project/book.json').write_text(json.dumps(book),encoding='utf-8');subprocess.run(['node',str(root/'scripts/build.mjs')],check=True);return root
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);make(p.parse_args().workspace)
