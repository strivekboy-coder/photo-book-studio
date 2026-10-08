"""Evidence checks for Plog delivery; not an aesthetic scorer or auto-composer."""
from collections import Counter
import json
from pathlib import Path

def template():
 return {'version':1,'planning':{'photos':[],'pages':[],'densityReason':'','expandedReason':''},'resources':{'inspiration':[],'materials':{'decision':'','reason':''},'fonts':{'mode':'','candidates':[],'actualCopy':'','reason':''}},'decoration':{'method':'','reason':''},'creativeReview':[{'route':i,'decision':'','reason':''} for i in range(1,8)],'visual':{'bookSha256':'','pages':[]}}

def problems(root,audit):
 root=Path(root);path=root/'project/plog-review.json'
 if not path.exists():return ['Missing project/plog-review.json; read references/plog-planning.md.']
 try:
  review=json.loads(path.read_text(encoding='utf-8-sig'));book=json.loads((root/'project/book.json').read_text(encoding='utf-8-sig'))
 except (ValueError,OSError) as e:return [f'Cannot read review/book: {e}']
 errors=[]
 def need(ok,message):
  if not ok:errors.append(message)
 def text(v):return isinstance(v,str) and bool(v.strip())
 planning=review.get('planning',{});photos=planning.get('photos',[]);pages=planning.get('pages',[])
 selected=set(audit['expectedOccurrences']);total=audit['pages']
 need(Counter(p.get('file') for p in photos)==Counter(selected),'Planning must describe each selected source exactly once.')
 need(all(p.get('role') in {'focus','supporting','detail','sequence'} and text(p.get('reason')) for p in photos),'Every photo role needs a source-linked reason.')
 need(Counter(p.get('page') for p in pages)==Counter(range(1,total+1)),'Planning must cover each current page exactly once.')
 for p in pages:
  i=p.get('page')
  if isinstance(i,int) and not isinstance(i,bool) and 1<=i<=total:
   actual=Counter(o['file'] for o in book['pages'][i-1].get('layers',[]) if o.get('type')=='photo')
   need(Counter(p.get('files',[]))==actual,f'Page {i} planned sources differ from actual layers.')
  need(text(p.get('reason')),'Each page needs a grouping/space reason.')
 need(text(planning.get('densityReason')),'Missing density decision.')
 if len(selected)>=6 and total>len(selected)/2:
  need(text(planning.get('expandedReason')),'Sparse Plog needs a concrete expansion reason and compact-alternative assessment.')
 resources=review.get('resources',{});cases=resources.get('inspiration',[])
 need(bool(cases) and all(text(c.get('source')) and text(c.get('observed')) and text(c.get('application')) for c in cases),'Missing inspected inspiration relationship/application; record a real case or honest fallback.')
 mat=resources.get('materials',{})
 need(mat.get('decision') in {'draw','reuse','generate','skip'} and text(mat.get('reason')),'Missing material decision/reason.')
 fonts=resources.get('fonts',{});mode=fonts.get('mode')
 need(mode in {'compare','reuse-approved','user-fixed'},'Missing font comparison or approved/user-fixed reuse decision.')
 need(text(fonts.get('actualCopy')) and text(fonts.get('reason')),'Missing actual-copy font evidence/reason.')
 if mode=='compare':need(len(set(fonts.get('candidates',[])))>=2,'Compare at least two font candidates for a new direction.')
 deco=review.get('decoration',{})
 need(deco.get('method') in {'svg','imagegen','reuse','mixed','none'} and text(deco.get('reason')),'Missing decoration method/reason; SVG is valid, imagegen is optional.')
 if deco.get('method')=='imagegen' or deco.get('generated') is True:
  records=deco.get('generations',[])
  need(bool(records) and all(text(g.get('tool')) and text(g.get('prompt')) and bool(g.get('inputs')) and bool(g.get('outputs')) and text(g.get('inspection')) for g in records),'New generated decoration needs real tool/prompt/input/output/inspection records.')
 routes=review.get('creativeReview',[])
 need(Counter(r.get('route') for r in routes)==Counter(range(1,8)),'Assess all seven creative routes exactly once.')
 need(all(r.get('decision') in {'use','skip','candidate'} and text(r.get('reason')) for r in routes),'Each creative route needs its decision and source-linked reason.')
 need(all(r.get('decision')!='candidate' or text(r.get('outcome')) for r in routes),'Resolve each remaining creative candidate before delivery.')
 visual=review.get('visual',{});views=visual.get('pages',[])
 need(visual.get('bookSha256')==audit['bookSha256'],'Visual review is stale relative to the current book.')
 need(Counter(v.get('page') for v in views)==Counter(range(1,total+1)),'Inspect every current canvas.')
 need(all(v.get('inspected') is True and v.get('phoneInspected') is True and text(v.get('notes')) for v in views),'Missing final-size/phone pixel inspection and findings.')
 return errors

def check(root,audit):
 errors=problems(root,audit)
 if errors:raise ValueError('Plog completion evidence incomplete:\n- '+'\n- '.join(errors))
 return {'workflowEvidenceComplete':True,'aestheticQualityCertified':False,'pages':audit['pages']}
