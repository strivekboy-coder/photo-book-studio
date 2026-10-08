(() => {
  if (new URLSearchParams(location.search).has('export')) return;
  const data = document.getElementById('plog-data');
  const initial = JSON.parse(data.textContent);
  let book = structuredClone(initial.book), selected = null, enabled = false, gesture = null;
  let past = [], future = [], beforeInput = null;
  const key = 'plog-editor-v1:' + location.pathname + ':' + initial.revision;
  const clone = v => structuredClone(v);
  const bar = document.createElement('nav'); bar.className = 'editor-bar'; bar.setAttribute('aria-label','Plog 编辑工具');
  bar.innerHTML = '<button id="edit-toggle" aria-pressed="false">微调排版</button><button id="edit-undo" disabled>撤销</button><button id="edit-redo" disabled>重做</button><button id="edit-save">保存草稿</button><details class="editor-backups"><summary>编辑备份</summary><div><button id="edit-json">备份布局 · JSON</button><button id="edit-html">备份页面 · HTML</button><small>用于继续编辑或交给 Codex 导出。最终 JPG / PNG / PDF 可直接在对话中索取。</small></div></details><button id="edit-reset">恢复初稿</button><span class="spacer"></span><span class="editor-status" role="status">点击「微调排版」开始；照片原件不会改变</span>';
  document.body.prepend(bar);
  const panel = document.createElement('aside'); panel.className = 'editor-panel'; panel.hidden = true;
  panel.innerHTML = '<strong>选中后调整</strong><label>图层（也可选中被遮挡的元素）</label><select id="edit-layer"><option value="">选择照片、文字或装饰</option></select><div id="edit-fields" hidden><div class="pair"><div><label>横向位置</label><input data-prop="x" type="number" step="1"></div><div><label>纵向位置</label><input data-prop="y" type="number" step="1"></div></div><div class="pair"><div><label>宽度</label><input data-prop="w" type="number" min="24" step="1"></div><div><label>高度</label><input data-prop="h" type="number" min="24" step="1"></div></div><label>角度 · °</label><input data-prop="rotate" type="number" step="1"><div id="edit-text-fields"><label>文字内容</label><textarea data-prop="text"></textarea><div class="pair"><div><label>字号</label><input data-prop="size" type="number" min="8" max="300"></div><div><label>颜色</label><input data-prop="color" type="color"></div></div><label>字体</label><select data-prop="font"></select></div><div class="pair" style="margin-top:12px"><button id="edit-back">后移一层</button><button id="edit-front">前移一层</button></div></div><small>拖动元素移动；右下角缩放；上方圆点旋转。照片等比缩放。方向键微移，Shift 加速。草稿保存在本浏览器；下载的页面请放回原文件夹，仍需旁边的素材。</small>';
  document.body.append(panel);
  const status = message => bar.querySelector('.editor-status').textContent = message;
  const layer = () => selected && book.pages[selected.p].layers[selected.l];
  const node = () => selected && document.querySelector(`[data-page="${selected.p+1}"] [data-layer="${selected.l+1}"]`);
  const outline = document.createElement('div'); outline.className='edit-outline';
  outline.innerHTML='<button class="resize" title="等比缩放" aria-label="缩放选中元素"></button><button class="rotate" title="旋转" aria-label="旋转选中元素"></button>';
  function validate(candidate) {
    if (candidate.pages.length !== initial.book.pages.length || JSON.stringify(candidate.fonts)!==JSON.stringify(initial.book.fonts)) return false;
    return candidate.pages.every((p,pi)=>p.layers.length===initial.book.pages[pi].layers.length && p.layers.every((o,li)=>{
      const original=initial.book.pages[pi].layers[li];
      return o.type===original.type && o.file===original.file && o.path===original.path && ['x','y','w','h'].every(k=>Number.isFinite(o[k])) && o.w>0 && o.h>0 && Number.isFinite(o.rotate||0) && Number.isFinite(o.z||0) && (o.type!=='text'||(typeof o.text==='string' && Object.hasOwn(initial.book.fonts,o.font||'default') && Number.isFinite(o.size)&&o.size>=8&&o.size<=300));
    }));
  }
  function remember(previous) {
    if(JSON.stringify(previous)===JSON.stringify(book))return;
    past.push(previous); if(past.length>80)past.shift(); future=[]; buttons(); persist();
  }
  function buttons(){document.getElementById('edit-undo').disabled=!past.length;document.getElementById('edit-redo').disabled=!future.length;}
  function persist(){try{localStorage.setItem(key,JSON.stringify(book));status('草稿已保存在本浏览器 · 可下载备份');}catch{status('浏览器无法存储草稿，请下载布局或当前页面保存');}}
  function crop(o,el){
    if(!o.sourceBox)return;
    const r=initial.inventory.find(v=>v.file===o.file);if(!r)return;
    const [sx,sy,sw,sh]=o.sourceBox,b=o.border||0,fw=o.w-2*b,fh=o.h-2*b-(o.matBottom||0),s=Math.max(fw/sw,fh/sh);
    const image=el.querySelector('img');Object.assign(image.style,{width:r.width*s+'px',height:r.height*s+'px',left:(-sx*s+(fw-sw*s)/2)+'px',top:(-sy*s+(fh-sh*s)/2)+'px'});
  }
  function draw(){
    book.pages.forEach((p,pi)=>p.layers.forEach((o,li)=>{
      const el=document.querySelector(`[data-page="${pi+1}"] [data-layer="${li+1}"]`);
      Object.assign(el.style,{left:o.x+'px',top:o.y+'px',width:o.w+'px',height:o.h+'px',transform:`rotate(${o.rotate||0}deg)`,zIndex:o.z??li+1});
      el.dataset.editable=['photo','image','text','path'].includes(o.type);
      if(o.type==='text'){el.textContent=o.text;Object.assign(el.style,{fontSize:o.size+'px',color:o.color||'#fff',fontFamily:o.font||'default'});}
      crop(o,el);
      if(o.type==='path'){
        el.querySelectorAll('.edit-hit-path').forEach(v=>v.remove());
        el.querySelectorAll('path').forEach(path=>{
          const hit=path.cloneNode();hit.classList.add('edit-hit-path');
          const view=o.viewBox||[0,0,o.w,o.h],scale=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--scale'))||1;
          hit.setAttribute('stroke','transparent');hit.setAttribute('fill','none');hit.removeAttribute('stroke-dasharray');
          hit.setAttribute('stroke-width',Math.max(view[2]/o.w,view[3]/o.h)*12/scale+(o.strokeWidth||4));el.append(hit);
        });
      }
    }));
    refreshOutline();
  }
  function refreshOutline(){
    if(!selected){outline.remove();return;}
    const o=layer(),el=node();el.closest('.canvas').append(outline);
    Object.assign(outline.style,{left:o.x+'px',top:o.y+'px',width:o.w+'px',height:o.h+'px',transform:`rotate(${o.rotate||0}deg)`});
  }
  const selector=panel.querySelector('#edit-layer');
  book.pages.forEach((p,pi)=>p.layers.forEach((o,li)=>{
    const opt=document.createElement('option');opt.value=pi+':'+li;
    const name={photo:'照片',text:'文字',image:'贴纸',paper:'纸张',path:'涂鸦'}[o.type];
    opt.textContent=`第${pi+1}页 · ${name} · ${(o.label||o.text||o.file||o.path?.split('/').pop()||li+1).toString().slice(0,24)}`;selector.append(opt);
  }));
  Object.keys(book.fonts).forEach(name=>{const opt=document.createElement('option');opt.value=name;opt.textContent={hand:'手写注释',display:'标题字体',default:'正文字体'}[name]||name;panel.querySelector('[data-prop=font]').append(opt);});
  function fields(){
    panel.querySelector('#edit-fields').hidden=!selected;
    if(!selected)return;
    const o=layer();selector.value=selected.p+':'+selected.l;
    panel.querySelector('#edit-text-fields').hidden=o.type!=='text';
    panel.querySelectorAll('[data-prop]').forEach(i=>{const k=i.dataset.prop;i.value=o[k]??({rotate:0,font:'default',color:'#ffffff'}[k]??'');if(i.type==='number')i.value=Math.round(Number(i.value)*10)/10;});
  }
  function select(p,l){selected=p==null?null:{p,l};fields();refreshOutline();}
  selector.onchange=()=>{if(!selector.value)select(null);else{const [p,l]=selector.value.split(':').map(Number);select(p,l);node().parentElement.parentElement.scrollIntoView({block:'nearest',behavior:'smooth'});}};
  document.getElementById('edit-toggle').onclick=()=>{
    enabled=!enabled;document.body.classList.toggle('editing',enabled);panel.hidden=!enabled;
    document.getElementById('edit-toggle').setAttribute('aria-pressed',String(enabled));document.getElementById('edit-toggle').textContent=enabled?'完成微调':'微调排版';
    if(!enabled)select(null);
    panel.querySelectorAll('input,textarea,select,button').forEach(el=>el.disabled=!enabled);
    panel.querySelector('strong').textContent=enabled?'选中后调整':'点击「微调排版」开始';
    fitEditor();
  };
  function fitEditor(){
    if(document.body.classList.contains('export'))return;
    const desktop=innerWidth>=900,viewer=document.querySelector('.viewer'),intro=document.querySelector('.intro');
    const room=desktop?viewer.clientWidth-40:innerWidth-48;
    // Fit the real workspace rather than subtracting a second fixed allowance.
    const top=bar.getBoundingClientRect().height+(intro?.getBoundingClientRect().height||0)+(desktop?20:72);
    const heightRoom=Math.max(100,innerHeight-top-16);
    const scale=Math.min(1,room/book.format.widthPx,desktop?heightRoom/book.format.heightPx:1);
    document.documentElement.style.setProperty('--scale',scale);
    panel.style.top=desktop?(bar.getBoundingClientRect().height+12)+'px':'';
    panel.style.maxHeight=desktop?(innerHeight-bar.getBoundingClientRect().height-24)+'px':'';
    draw();
  }
  addEventListener('resize',fitEditor);
  document.querySelectorAll('.canvas').forEach(canvas=>{
    canvas.addEventListener('pointerdown',e=>{
      if(!enabled||e.button!==0||e.target.closest('.edit-outline'))return;
      const el=e.target.closest('[data-layer]');
      if(!el||el.dataset.editable!=='true'){
        // Paper and path overlays are selected through the list. Blank canvas
        // can move them; foreground clicks always resolve the visible layer.
        if(selected&&selected.p===Number(canvas.dataset.page)-1&&['paper','path'].includes(layer().type)){start(e,'move');return;}
        select(null);return;
      }
      select(Number(canvas.dataset.page)-1,Number(el.dataset.layer)-1);start(e,'move');
    });
  });
  function start(e,mode){
    e.preventDefault();const o=clone(layer()),canvas=node().parentElement,rect=canvas.getBoundingClientRect(),scale=rect.width/book.format.widthPx;
    gesture={mode,original:o,previous:clone(book),pointer:e.pointerId,x:e.clientX,y:e.clientY,scale,cx:rect.left+(o.x+o.w/2)*scale,cy:rect.top+(o.y+o.h/2)*scale};
    gesture.startAngle=Math.atan2(e.clientY-gesture.cy,e.clientX-gesture.cx);
    e.currentTarget.setPointerCapture(e.pointerId);
  }
  outline.querySelector('.resize').onpointerdown=e=>start(e,'resize');outline.querySelector('.rotate').onpointerdown=e=>start(e,'rotate');
  // The outline body never intercepts clicks; only its handles capture input.
  addEventListener('pointermove',e=>{
    if(!gesture||gesture.pointer!==e.pointerId)return;
    const g=gesture,o=layer(),a=g.original,dx=(e.clientX-g.x)/g.scale,dy=(e.clientY-g.y)/g.scale;
    if(g.mode==='move'){o.x=Math.round(a.x+dx);o.y=Math.round(a.y+dy);}
    else if(g.mode==='rotate'){let angle=(a.rotate||0)+(Math.atan2(e.clientY-g.cy,e.clientX-g.cx)-g.startAngle)*180/Math.PI;o.rotate=Math.round((e.shiftKey?Math.round(angle/15)*15:angle)*10)/10;}
    else{
      const r=(a.rotate||0)*Math.PI/180,localX=dx*Math.cos(r)+dy*Math.sin(r),localY=-dx*Math.sin(r)+dy*Math.cos(r);
      let w=Math.max(24,a.w+localX),h=Math.max(24,a.h+localY);
      if(['photo','image'].includes(a.type)){const b=a.border||0;const s=Math.max((2*b+24)/a.w,(2*b+(a.matBottom||0)+24)/a.h,1+(localX*a.w+localY*a.h)/(a.w*a.w+a.h*a.h));w=a.w*s;h=a.h*s;}
      o.w=Math.round(w);o.h=Math.round(h);
      const dw=o.w-a.w,dh=o.h-a.h;o.x=a.x+(dw*Math.cos(r)-dh*Math.sin(r)-dw)/2;o.y=a.y+(dw*Math.sin(r)+dh*Math.cos(r)-dh)/2;
    }
    draw();fields();
  });
  function finish(e,cancel=false){if(!gesture||e.pointerId!==gesture.pointer)return;const old=gesture.previous;gesture=null;if(cancel){book=old;draw();fields();}else remember(old);}
  addEventListener('pointerup',e=>finish(e));addEventListener('pointercancel',e=>finish(e,true));
  panel.querySelectorAll('[data-prop]').forEach(input=>{
    input.onfocus=()=>beforeInput=clone(book);
    input.oninput=()=>{
      if(!selected)return;
      if(!beforeInput)beforeInput=clone(book);
      const o=layer(),k=input.dataset.prop;
      if(input.type==='number'){
        const n=Number(input.value);if(!input.value||!Number.isFinite(n)||(['w','h'].includes(k)&&n<24)||(k==='size'&&(n<8||n>300)))return;
        if(['w','h'].includes(k)&&['photo','image'].includes(o.type)){const b=o.border||0,s=n/o[k];if(o.w*s<2*b+24||o.h*s<2*b+(o.matBottom||0)+24)return;}
        if(['w','h'].includes(k)&&['photo','image'].includes(o.type)){const other=k==='w'?'h':'w';o[other]*=n/o[k];}o[k]=n;
      }else o[k]=input.value;
      draw();
    };
    input.onchange=()=>{if(beforeInput){remember(beforeInput);beforeInput=null;}fields();};
    input.onblur=()=>{if(beforeInput){remember(beforeInput);beforeInput=null;}};
  });
  function undo(){if(!past.length)return;future.push(clone(book));book=past.pop();draw();fields();buttons();persist();}
  function redo(){if(!future.length)return;past.push(clone(book));book=future.pop();draw();fields();buttons();persist();}
  document.getElementById('edit-undo').onclick=undo;document.getElementById('edit-redo').onclick=redo;
  for(const [id,direction] of [['edit-front',1],['edit-back',-1]])document.getElementById(id).onclick=()=>{
    if(!selected)return;const previous=clone(book),o=layer(),layers=book.pages[selected.p].layers;
    const ordered=layers.map((v,i)=>({v,i,z:v.z??i+1})).sort((a,b)=>a.z-b.z||a.i-b.i),index=ordered.findIndex(v=>v.i===selected.l),other=index+direction;
    if(other<0||other>=ordered.length)return;
    [ordered[index],ordered[other]]=[ordered[other],ordered[index]];ordered.forEach((entry,i)=>entry.v.z=i+1);draw();remember(previous);
  };
  document.getElementById('edit-save').onclick=persist;
  document.getElementById('edit-reset').onclick=()=>{if(!confirm('恢复 AI 初稿？当前调整可以通过撤销找回。'))return;const previous=clone(book);book=clone(initial.book);draw();fields();remember(previous);};
  function download(content,type,name){const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  document.getElementById('edit-json').onclick=()=>{download(JSON.stringify(book,null,2),'application/json','book-edited.json');status('布局已下载 · 包含文字与位置；照片原件保持不变');};
  document.getElementById('edit-html').onclick=()=>{
    const doc=document.documentElement.cloneNode(true);doc.querySelectorAll('.editor-bar,.editor-panel,.edit-outline,.edit-hit-path').forEach(el=>el.remove());doc.querySelector('body').classList.remove('editing');
    const current={...initial,book:clone(book),revision:initial.revision+'-saved-'+Date.now()};
    doc.querySelector('#plog-data').textContent=JSON.stringify(current).replaceAll('<','\\u003c');
    download('<!doctype html>\n'+doc.outerHTML,'text/html','plog-edited.html');status('页面已下载 · 放回原文件夹后打开，保留现有素材与字体');
  };
  addEventListener('keydown',e=>{
    if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName))return;
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){e.preventDefault();e.shiftKey?redo():undo();return;}
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='y'){e.preventDefault();redo();return;}
    if(!enabled||!selected)return;
    if(e.key==='Escape'){select(null);return;}
    if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();const previous=clone(book),o=layer(),step=e.shiftKey?10:1;o.x+=e.key==='ArrowRight'?step:e.key==='ArrowLeft'?-step:0;o.y+=e.key==='ArrowDown'?step:e.key==='ArrowUp'?-step:0;draw();fields();remember(previous);}
  });
  try{
    let saved=JSON.parse(localStorage.getItem(key));
    const migration=initial.book.editorMigration;
    if(!saved&&migration){
      const previous=JSON.parse(localStorage.getItem('plog-editor-v1:'+location.pathname+':'+migration.previousRevision));
      if(previous){
        saved=clone(initial.book);
        migration.layerMap.forEach((m,index)=>{
          const old=previous.pages[0].layers[m.from];if(!old)return;
          if(!m.region){saved.pages[0].layers[index]=clone(old);return;}
          const target=saved.pages[0].layers[index],r=m.region,rot=(old.rotate||0)*Math.PI/180;
          const sx=old.w/m.base[0],sy=old.h/m.base[1],dx=(r[0]+r[2]/2)*sx-old.w/2,dy=(r[1]+r[3]/2)*sy-old.h/2;
          target.w=r[2]*sx;target.h=r[3]*sy;target.x=old.x+old.w/2+dx*Math.cos(rot)-dy*Math.sin(rot)-target.w/2;
          target.y=old.y+old.h/2+dx*Math.sin(rot)+dy*Math.cos(rot)-target.h/2;target.rotate=old.rotate||0;target.z=old.z??m.from+1;
        });
      }
    }
    if(saved&&validate(saved)){book=saved;status('已恢复本浏览器草稿 · 恢复初稿可回到 AI 排版');}
  }catch{}
  panel.querySelectorAll('input,textarea,select,button').forEach(el=>el.disabled=true);
  panel.querySelector('strong').textContent='点击「微调排版」开始';
  draw();fitEditor();
})();
