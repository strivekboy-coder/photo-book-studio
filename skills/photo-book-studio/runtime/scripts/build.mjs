import fs from 'node:fs';
import path from 'node:path';
const arg=process.argv.indexOf('--workspace');
const root=arg>=0?path.resolve(process.argv[arg+1]):path.resolve(import.meta.dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');
const book=JSON.parse(read('project/book.json'));
const errors=[]; const assetPaths=new Set(); const counts=new Map();
const existsSafe=rel=>{if(typeof rel!=='string'||!rel)return false;const resolved=path.resolve(root,rel);return resolved.startsWith(root+path.sep)&&fs.existsSync(resolved)&&fs.statSync(resolved).isFile();};
const inventoryPath=path.join(root,'project/inventory.json');
const inventory=fs.existsSync(inventoryPath)?JSON.parse(read('project/inventory.json')):null;
const photoRoot=book.photoRoot||'assets/photos/';
const supported=/\.(jpe?g|png|webp|gif|heic|heif)$/i;
const selected=inventory?inventory.photos.map(p=>p.file):fs.readdirSync(path.resolve(root,photoRoot)).filter(p=>supported.test(p));
if(new Set(selected).size!==selected.length)errors.push('Duplicate source IDs in inventory');
for(const spread of book.spreads||[]){
 if(spread.backgroundPhoto?.path)assetPaths.add(spread.backgroundPhoto.path);
 for(const side of ['left','right']){
  const page=spread[side];if(!page){errors.push(`Missing ${side} page`);continue;}
  for(const photo of page.photos||[]){
   if(!photo.decorative){if(!photo.file)errors.push('Selected photo missing file ID');else counts.set(photo.file,(counts.get(photo.file)||0)+1);}
   assetPaths.add(photo.path||photoRoot+photo.file);
  }
  if(page.backgroundPath)assetPaths.add(page.backgroundPath);
  for(const sticker of page.stickers||[])assetPaths.add(sticker.path);
 }
}
for(const file of selected){
 const expected=book.policy?.authorizedOccurrences?.[file]??1;
 if(!Number.isInteger(expected)||expected<0){errors.push(`Invalid authorized count: ${file}`);continue;}
 if((counts.get(file)||0)!==expected)errors.push(`Photo occurrence mismatch: ${file} expected ${expected}, placed ${counts.get(file)||0}`);
 if(!existsSafe(photoRoot+file))errors.push(`Missing original: ${file}`);
}
for(const file of counts.keys())if(!selected.includes(file))errors.push(`Unknown selected photo: ${file}`);
if(book.cover?.path)assetPaths.add(book.cover.path);else if(book.cover?.photo)assetPaths.add(photoRoot+book.cover.photo);else errors.push('Cover needs placeholder, photo or generated path');
if(book.cover?.backPath)assetPaths.add(book.cover.backPath);
if(book.cover?.spinePath)assetPaths.add(book.cover.spinePath);
for(const track of book.audio||[])assetPaths.add(track.path);
for(const rel of assetPaths)if(!existsSafe(rel))errors.push(`Missing or outside-project asset: ${rel}`);
for(const rel of ['assets/fonts/LXGWWenKaiLite-Regular.ttf','assets/fonts/SmileySans-Oblique.woff2'])if(!existsSafe(rel))errors.push(`Missing bundled font: ${rel}`);
const format=book.format||{}; const w=Number(format.trimWidthMm),h=Number(format.trimHeightMm);
if(!(w>0&&h>0))errors.push('Positive trimWidthMm and trimHeightMm required');
if(errors.length)throw Error(errors.join('\n'));
const escape=value=>String(value??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const css=read('src/styles.css')+`\n:root {--page-ratio:${w/h};--spread-ratio:${2*w/h};--print-spread-width:${2*w}mm;--print-height:${h}mm;--preview-page-height:${600*h/w}px;}\n`;
const html=read('src/template.html').replaceAll('__TITLE__',escape(book.title||'Photo Book')).replace('__STYLES__',css).replace('__BOOK__',JSON.stringify(book).replaceAll('<','\\u003c')).replace('__APP__',read('src/app.js'));
fs.writeFileSync(path.join(root,'sample.html'),html,'utf8');
const report={selected:selected.length,placed:[...counts.values()].reduce((a,b)=>a+b,0),omitted:selected.filter(f=>!(counts.get(f)>0)&&((book.policy?.authorizedOccurrences?.[f]??1)>0)).length,expectedPlacements:selected.reduce((n,f)=>n+(book.policy?.authorizedOccurrences?.[f]??1),0),sourceIdsValidated:true,assetsValidated:assetPaths.size,viewerSpreads:1+(book.spreads||[]).length,format};
fs.writeFileSync(path.join(root,'project/build-audit.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
