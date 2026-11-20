/* Built-in-only smoke checks: local static server, Chromium DevTools and CSP probes. */
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),os=require('node:os');
const {spawn}=require('node:child_process');
const root=process.cwd(),site=path.join(root,'site');
const candidates=[process.env.CHROME_PATH,'/usr/bin/google-chrome','/usr/bin/chromium','C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Google/Chrome/Application/chrome.exe'].filter(Boolean);
const browser=candidates.find(p=>fs.existsSync(p));
if(!browser)throw Error('Set CHROME_PATH to a Chromium or Edge executable.');
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'pyconformal-check-'));
const flags=['--headless','--disable-gpu','--disable-dev-shm-usage','--no-first-run','--disable-background-networking','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'];
if(process.env.CI==='true'&&process.platform==='linux')flags.unshift('--no-sandbox');
const child=spawn(browser,flags,{windowsHide:true});let stderr='',ws;
child.stderr.on('data',b=>stderr+=b.toString());
child.on('error',error=>{stderr+=error.message;});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.jpg':'image/jpeg','.png':'image/png','.json':'application/json'};
const server=http.createServer((req,res)=>{try{const url=new URL(req.url,'http://localhost'),relative=decodeURIComponent(url.pathname),file=path.resolve(site,'.'+relative+(relative.endsWith('/')?'index.html':''));if(!file.startsWith(site+path.sep))throw Error('Forbidden path');if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}const body=fs.readFileSync(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(req.method==='HEAD'?undefined:body);}catch{res.writeHead(404);res.end();}});
const routeMap={landing:'index.html','landing-reduced':'index.html',gallery:'examples/index.html','sources-doc':'docs/sources-and-scope.html','exercise-doc':'docs/exercises.html',notation:'docs/notation.html'};
const tests={
'notation':`check(document.querySelectorAll('math').length>15,'rendered mathematics');check(document.querySelector('mfrac'),'native fractions');`,
'schwarz-christoffel-square':`check(Math.hypot(...squareMap([0,1]))<1e-12,'SC center');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');document.querySelector('[data-prevertex="inf"]').click();check(byId('point').textContent==='∞','infinite prevertex');byId('electrostatics').click();check(!byId('field-legend').hidden&&!byId('voltage-readout').hidden,'field view explains legend and voltage');check(Math.abs(Number.parseFloat(byId('voltage').textContent)-1)<1e-12,'top corner potential');byId('geometry').click();byId('reset').click();`,
'square-map':`check(document.querySelector('math'),'square formula');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');byId('origin').click();check(byId('scale').textContent==='0.000','critical point scale');check(byId('angles').textContent==='40° → 80°','outgoing opening doubles');byId('reset').click();check(byId('angles').textContent==='40° → 40°','ordinary opening preserved');const c=image.getContext('2d'),fill=c.fillText;let labels=[];c.fillText=function(t,...args){labels.push(t);return fill.call(this,t,...args);};render();c.fillText=fill;check(labels.includes('θ′')&&labels.includes('P′'),'image angle and point labels');const cv=source,r=cv.getBoundingClientRect(),capture=cv.setPointerCapture;cv.setPointerCapture=()=>{};cv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:42,isPrimary:true,button:0,bubbles:true}));cv.setPointerCapture=capture;check(Number(real.value)===0&&Number(imag.value)===0,'source pointer moves P');byId('reset').click();`,
'disk-to-halfplane':`check(document.querySelector('mfrac'),'Cayley fraction');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');byId('pole').click();check(byId('mapped').textContent==='∞','pole displayed as infinity');radius.value=1;angle.value=90;render();check(byId('location').textContent.includes(L('real axis','eje real')),'boundary maps to real axis');check(Math.abs(cayley(1,90)[0]-1)<1e-12,'i maps to 1');byId('reset').click();const cv=disk,r=cv.getBoundingClientRect(),capture=cv.setPointerCapture;cv.setPointerCapture=()=>{};cv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:42,isPrimary:true,button:0,bubbles:true}));cv.setPointerCapture=capture;check(Number(radius.value)===0&&Math.abs(cayley(0,0)[1]-1)<1e-12,'disk pointer selects center mapping to i');byId('reset').click();`,
'exponential-map':`check(document.querySelector('math'),'exponential formula');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');byId('wrap').click();const first=byId('mapped').textContent;byId('wrap').click();check(byId('mapped').textContent===first,'opposite strip edges have same image');check(Math.abs(Number(byId('radius').textContent)-Math.exp(Number(real.value)))<.001,'exponential radius');byId('reset').click();const cv=source,r=cv.getBoundingClientRect(),capture=cv.setPointerCapture;cv.setPointerCapture=()=>{};cv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+r.width/2,clientY:r.top+r.height/2,pointerId:42,isPrimary:true,button:0,bubbles:true}));cv.setPointerCapture=capture;check(Number(real.value)===0&&Number(angle.value)===0,'exponential source pointer');byId('reset').click();`,
'object-reveal':`check(document.querySelector('math'),'logarithm formula');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');const before=$('readout').textContent;$('position').value=150;render();check($('readout').textContent!==before,'contour selection updates');for(const j of [0,100,200,300,400]){const q=log(warped[j]);check(Math.hypot(q[0]-house[j][0],q[1]-house[j][1])<1e-12,'principal log recovers designed vertex');}const c=$('image').getContext('2d'),fill=c.fillText;let labels=[];c.fillText=function(t,...args){labels.push(t);return fill.call(this,t,...args);};render();c.fillText=fill;check(labels.includes('P′'),'recovered contour selection labeled P prime');$('position').value=0;render();const cv=$('image'),r=cv.getBoundingClientRect(),q=views[1](house[250]);cv.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+q[0],clientY:r.top+q[1],pointerId:42,button:0,bubbles:true}));check(Number($('position').value)===250,'click recovered contour selects matching sample');$('position').value=0;render();`,
'coplanar-waveguide':`check(document.querySelectorAll('math').length>=3,'elliptic model formulas');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');byId('design').click();check(Math.abs(Number.parseFloat(byId('impedance').textContent)-50)<.01,'50 ohm design');const values=[widthInput.value,gapInput.value,permittivityInput.value];widthInput.value=0;render();check(byId('impedance').textContent==='—'&&byId('status').textContent.length>0,'invalid geometry explained');[widthInput.value,gapInput.value,permittivityInput.value]=values;render();byId('show-field').checked=false;byId('show-field').dispatchEvent(new Event('change'));byId('show-field').checked=true;byId('show-field').dispatchEvent(new Event('change'));`,
'coplanar-sensor':`check(document.querySelector('mfrac'),'sensor formula');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');const values=controls.map(i=>i.value),base=Number.parseFloat(byId('total').textContent);byId('permittivity').value=Number(values[3])*2;render();check(Math.abs(Number.parseFloat(byId('total').textContent)-2*base)<.005,'uniform dielectric capacitance scales linearly');byId('width').value=0;render();check(byId('total').textContent==='—'&&byId('status').textContent.length>0,'invalid sensor geometry explained');controls.forEach((input,i)=>input.value=values[i]);render();check(Number.parseFloat(byId('double-gap').textContent)<Number.parseFloat(byId('total').textContent),'double gap lowers capacitance');`,
'lunar-thesis-interactive':`document.querySelector('[data-map="log"]').click();check(document.querySelector('[data-formula-map="log"]').hidden===false,'log formula follows selection');document.querySelector('[data-map="cube"]').click();check(document.querySelector('[data-formula-map="log"]').hidden,'old formula hidden');check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');const selected=slider.value;for(const b of maps){b.click();check(slider.value===selected,'map change preserves contour sample');}const c=image.getContext('2d'),fill=c.fillText;let labels=[];c.fillText=function(t,...args){labels.push(t);return fill.call(this,t,...args);};render();c.fillText=fill;check(labels.includes('P′'),'lunar transformed selection labeled');document.querySelector('[data-map="square"]').click();const chosen=data.markers[1],r=source.getBoundingClientRect(),q=sourceView.project(sourceView.boundary[chosen]);source.dispatchEvent(new MouseEvent('click',{clientX:r.left+q[0],clientY:r.top+q[1],bubbles:true}));check(Number(slider.value)===chosen,'lunar click selects reference vertex');marks[0].click();`,
'gallery':`check(!document.querySelector('.gallery-intro .preview-motion'),'effects control outside the introduction');check(document.querySelector('.preview-toolbar .preview-motion'),'effects control next to previews');check(document.querySelector('.preview-motion').getAttribute('aria-describedby')==='preview-effects-help','effect explanation associated with control');check(document.querySelector('footer .project-credit').textContent.includes('César Augusto Vega Penagos'),'project author explicit');check(!document.querySelector('footer').textContent.includes('Olivero'),'thesis coauthor not presented as project author');check(!document.querySelector('.purpose-audience'),'routes open to the general public');check(document.querySelectorAll('.purpose-card').length===4,'four purpose routes');check(document.querySelectorAll('.purpose-card[href]').length===4,'purpose routes link to tasks');check(document.querySelectorAll('.discovery-card').length===12,'twelve individual cases');check(document.querySelectorAll('.discovery-card svg').length===12,'visual preview for every case');check(document.querySelectorAll('.discovery-card h3').length===12,'a question for every case');const pause=document.querySelector('.preview-motion');pause.click();check(document.body.classList.contains('gallery-paused'),'preview effects paused');pause.click();check(document.querySelector('.site-header a[href="../index.html"]'),'gallery home');check(document.querySelector('a[href="../docs/reproducibility.html"]'),'reproduction route');`,
'sources-doc':`check(document.querySelector('a[href="https://doi.org/10.18273/revint.v34n1-2016002"]'),'mentor reference');check(document.querySelector('.table-scroll'),'scope comparison');`,
'landing':`
const globe=document.getElementById('globe'),square=document.getElementById('square'),button=document.getElementById('motion');
await new Promise(r=>setTimeout(r,350));
check(globe.dataset.longitude,'globe rendered');
check(Number(square.dataset.gridPaths)===55,'projected graticule rendered');
check(document.querySelector('.meridian-key')&&document.querySelector('.parallel-key'),'grid legend');check(document.querySelector('.animation-console .grid-key')&&document.querySelector('.animation-console #longitude')&&document.querySelector('.animation-console #motion'),'landing controls and legend in one block');check(document.querySelector('.views').nextElementSibling.classList.contains('animation-console'),'landing controls directly below the views');
for(const view of document.querySelectorAll('.views .view')){
 const title=view.querySelector('.view-title').getBoundingClientRect(),surface=view.querySelector('.surface').getBoundingClientRect(),legend=view.querySelector('.view-legend').getBoundingClientRect();
 check(title.bottom<=surface.top+1,'title above each animation');
 check(Math.abs((title.left+title.right-surface.left-surface.right)/2)<1,'title centered on its animation');
 check(legend.top>=surface.bottom-1,'legend below each animation');
}
const note=[...document.querySelectorAll('.scale-note-full,.scale-note-compact')].find(e=>getComputedStyle(e).display!=='none'),noteRect=note.getBoundingClientRect(),range=document.createRange();range.selectNodeContents(note);
check(range.getClientRects().length===1,'angle and scale explanation occupies one line');
check(note.scrollWidth<=note.clientWidth+1,'one-line explanation fits without clipping');
check(getComputedStyle(document.querySelector('.grid-key')).borderTopWidth==='0px','legend has no competing frame');check(parseFloat(getComputedStyle(document.getElementById('experiment-caption')).fontSize)>parseFloat(getComputedStyle(document.querySelector('.grid-key')).fontSize),'explanation has typographic priority');
check(document.querySelectorAll('.timeline li').length===3,'historical sequence');
check(document.querySelector('a[href="https://doi.org/10.2307/2369491"]'),'Peirce primary source');
check(document.querySelectorAll('header nav a[href="#cite"]').length===1,'exactly one citation navigation link');
check(document.querySelectorAll('.history-portraits img').length===3,'three historical portraits');
check(parseFloat(getComputedStyle(document.querySelector('.view p')).fontSize)>=14,'readable view captions');
check(document.querySelector('.point-key').textContent.includes('P′'),'point image legend');
check(document.querySelectorAll('.citation-card').length===2,'thesis and software citations');
let copied='';Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{copied=value;}}});
document.querySelector('[data-copy="cite-thesis"]').click();await new Promise(r=>setTimeout(r,20));
check(copied.includes('Olivero Zapata')&&copied.includes('63225bdb-dfc7-43f3-b22d-156d01277ef2'),'copy thesis and institutional URL');
check(copied.includes(L('Thesis director: Juan Pablo Yáñez Puentes.','Director de tesis: Juan Pablo Yáñez Puentes.')),'copy includes supervision credit');
document.querySelector('[data-copy="cite-software"]').click();await new Promise(r=>setTimeout(r,20));
check(copied.includes(L('Version 0.1.0a1','Versión 0.1.0a1')),'copy versioned software citation');
Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('unavailable');}}});
document.querySelector('[data-copy="cite-thesis"]').click();await new Promise(r=>setTimeout(r,20));
check(getSelection().toString().includes('Olivero Zapata'),'selectable clipboard fallback');getSelection().removeAllRanges();
document.getElementById('copy-status').textContent='';
const before=globe.dataset.longitude;
await new Promise(r=>setTimeout(r,300));check(globe.dataset.longitude!==before,'automatic movement');
button.click();const frozen=globe.dataset.longitude;
await new Promise(r=>setTimeout(r,300));check(globe.dataset.longitude===frozen,'pause freezes point');
const slider=document.getElementById('longitude');slider.value=-35;slider.dispatchEvent(new Event('input'));
const context=square.getContext('2d'),originalLabel=context.fillText;let labels=[];
context.fillText=function(text,...args){labels.push(text);return originalLabel.call(this,text,...args);};
slider.dispatchEvent(new Event('input'));context.fillText=originalLabel;
check(labels.includes('P′'),'projected canvas draws P prime');
check(Number(globe.dataset.longitude)===-35,'manual longitude');
const expected=PeirceMap.project(-35,Number(globe.dataset.latitude));
check(Math.abs(Number(square.dataset.x)-expected[0])<1e-12&&Math.abs(Number(square.dataset.y)-expected[1])<1e-12,'true Peirce correspondence');
check(button.getAttribute('aria-pressed')==='true','manual input pauses');

const globeContext=globe.getContext('2d'),globeArc=globeContext.arc,squareArc=context.arc;
const globeMarks=[],squareMarks=[];
globeContext.arc=function(x,y,r,...args){if(r===7)globeMarks.push([x,y,Number(globe.dataset.cameraLongitude)]);return globeArc.call(this,x,y,r,...args);};
context.arc=function(x,y,r,...args){if(r===7)squareMarks.push([x,y]);return squareArc.call(this,x,y,r,...args);};
for(const longitude of [-179,-90,-35,0,45,90,179]){
 slider.value=longitude;slider.dispatchEvent(new Event('input'));
 const [x,y,camera]=globeMarks.at(-1),radius=globe.width/2-5,nx=(x-globe.width/2)/radius,ny=(globe.height/2-y)/radius;
 const recoveredLongitude=camera+Math.atan2(nx,Math.sqrt(1-nx*nx-ny*ny))*180/Math.PI;
 check(Math.abs(recoveredLongitude-longitude)<1e-10,'drawn globe point recovers selected longitude');
}
const equatorPixels=globeContext.getImageData(0,globe.height/2,globe.width,1).data;
let goldenPixels=0;
for(let i=0;i<equatorPixels.length;i+=4)if(equatorPixels[i]>245&&equatorPixels[i+1]>195&&equatorPixels[i+1]<225&&equatorPixels[i+2]<150)goldenPixels++;
check(goldenPixels>globe.width*.75,'equator is visibly highlighted across the actual globe raster');
button.click();check(button.getAttribute('aria-pressed')==='false','resume control');
await new Promise(r=>setTimeout(r,420));
check(globeMarks.length>=9&&globeMarks.length===squareMarks.length,'manual and animated marker pairs captured');
let correspondenceError=0;
for(let i=0;i<globeMarks.length;i++){
 const [x,y,camera]=globeMarks[i],radius=globe.width/2-5,nx=(x-globe.width/2)/radius,ny=(globe.height/2-y)/radius;
 const lat=Math.asin(ny)*180/Math.PI,lon=camera+Math.atan2(nx,Math.sqrt(Math.max(0,1-nx*nx-ny*ny)))*180/Math.PI;
 const projected=PeirceMap.project(lon,lat),actual=[2*squareMarks[i][0]/square.width-1,1-2*squareMarks[i][1]/square.height];
 correspondenceError=Math.max(correspondenceError,Math.abs(projected[0]-actual[0]),Math.abs(projected[1]-actual[1]));
}
check(correspondenceError<1e-10,'inverse of actual globe marker projects onto actual Peirce marker');
globeContext.arc=globeArc;context.arc=squareArc;
console.log('Drawn globe-to-Peirce marker error:',correspondenceError);


for(const item of document.querySelectorAll('.grid-key span')){check(item.getBoundingClientRect().right<=document.querySelector('.grid-key').getBoundingClientRect().right+1,'legend fits translated labels');}
check(!document.querySelector('a[href*="127.0.0.1"]'),"no preview links");check(document.querySelectorAll("a[download]").length===6,"six citation downloads");`,
'landing-reduced':`
const globe=document.getElementById('globe'),button=document.getElementById('motion');
await new Promise(r=>setTimeout(r,300));check(globe.dataset.longitude,'static globe rendered');
check(button.getAttribute('aria-pressed')==='true','reduced motion initially paused');
const before=globe.dataset.longitude;await new Promise(r=>setTimeout(r,300));
check(globe.dataset.longitude===before,'reduced motion prevents autoplay');
button.click();await new Promise(r=>setTimeout(r,350));
check(globe.dataset.longitude!==before,'explicit play works with reduced motion');button.click();
`,
'exercise-doc':`check(document.getElementById('e1-vector-angles-and-orientation'),'E1 anchor');check(document.getElementById('e10-audit-the-historical-figure'),'E10 anchor');check(document.querySelector('a[href="exercise-solutions.html"]'),'rendered solutions link');`,
'group-p':`document.querySelector('[data-thesis="reflection"]').click();check(document.getElementById('axis').value==='30','reflection axis preset');const original=stats(points);document.getElementById('negative').checked=true;render();check(document.getElementById('m3').textContent.includes(original.angle.toFixed(2)),'negative dilation angle');check(document.getElementById('thesis-note').textContent.includes('2\u03b1'),'matrix convention: '+document.getElementById('thesis-note').textContent);document.querySelector('[data-thesis="definition"]').click();check(stats(points).angle!==90,'oblique definition');document.getElementById('reset').click();
check(document.querySelector('.source-panel'),'distinct interactive source');
check(document.querySelectorAll('[data-point]').length===3,'explicit point selectors');
const source=$('source'),size=source.getBoundingClientRect();
const ctx=source.getContext('2d'),originalText=ctx.fillText;let marks=[];
ctx.fillText=function(text,x,y,...args){marks.push({text,x,y});return originalText.call(this,text,x,y,...args);};
for(const preset of document.querySelectorAll('[data-thesis]')){
 marks=[];preset.click();const O=marks.find(p=>p.text==='O'),theta=marks.find(p=>p.text==='θ');
 check(O&&theta&&Math.hypot(O.x-theta.x,O.y-theta.y)>45,'vertex O separated from angle theta');
 check(preset.textContent.includes(L('Example:','Ejemplo:')),'clear preset name');
}
ctx.fillText=originalText;$('reset').click();

check(innerWidth<700||size.width>400,'larger desktop panels');
const originalPoints=points.map(p=>p.slice());
document.querySelector('[data-point="2"]').click();
source.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
check(Math.abs(points[2][0]-originalPoints[2][0]-.02)<1e-12,'selected handle moves by keyboard');
check(document.querySelector('[data-point="2"]').getAttribute('aria-pressed')==='true','selected handle identified');
check($('selected-point').textContent.includes(L('Selected: B','Selección: B')),'point selection readout');
const first=points.map(p=>p.slice()),before=sourceProjection.project(points[1]),rect=source.getBoundingClientRect();
const simulate=(type,x,y)=>source.dispatchEvent(new PointerEvent(type,{clientX:rect.left+x,clientY:rect.top+y,pointerId:42,button:0,bubbles:true,pointerType:'mouse'}));
const capture=source.setPointerCapture;source.setPointerCapture=()=>{};
simulate('pointerdown',before[0],before[1]);check(dragging&&active===1,'drag begins on handle');
const originalExtent=viewExtent,unit=sourceProjection.unit,shift=unit*.04;
simulate('pointermove',before[0]+shift,before[1]);
check(Math.abs(points[1][0]-first[1][0]-shift/unit)<1e-12,'drag follows pointer without view feedback');
check(viewExtent===originalExtent,'scale remains fixed during drag');
simulate('pointerup',before[0]+shift,before[1]);check(!dragging&&dragExtent===null,'drag ends and refits');
const frozen=JSON.stringify(points);simulate('pointerdown',2,2);check(!dragging&&JSON.stringify(points)===frozen,'empty canvas does not teleport a point');
source.setPointerCapture=capture;$('reset').click();
`,
'conformal-angle':`
byId('opening').value=60;byId('real').value=.5;byId('imag').value=.5;render();
check(Math.abs(lastState.scale-Math.sqrt(2))<1e-12,'derivative scale');
check(Math.abs(lastState.imageOpening-60)<1e-10,'opening preserved');
const originalPanel=window.plotPanel,arrows=[];
window.plotPanel=(canvas,bounds)=>{const panel=originalPanel(canvas,bounds),arrow=panel.arrow;panel.arrow=(a,b,color)=>{arrows.push({id:canvas.id,a,b});arrow(a,b,color);};return panel;};
render();check(arrows.length===4,'four tangent arrows');
for(const [j,arrow] of arrows.filter(a=>a.id==='image').entries()){
 const v=lastState.imageTangents[j],d=arrow.b.map((x,k)=>x-arrow.a[k]);
 check(Math.abs(d[0]*v[1]-d[1]*v[0])<1e-12&&d[0]*v[0]+d[1]*v[1]>0,'drawn image arrow follows analytic tangent');
}
arrows.length=0;byId('critical').click();
check(lastState.scale===0&&lastState.imageOpening===null,'critical tangent undefined');
check(arrows.length===2&&arrows.every(a=>a.id==='source'),'no misleading image arrows at critical point');
window.plotPanel=originalPanel;
let maxError=0;
for(const name of ['square','exp','rotation'])for(const z of [[.45,.3],[-.6,.2],[.01,-.02]]){
 byId('map').value=name;byId('real').value=z[0];byId('imag').value=z[1];render();
 for(let j=0;j<2;j++){
  const e=1e-6,T=lastState.tangents[j],a=maps[name].f(curvePoint(z,T,j,-e)),b=maps[name].f(curvePoint(z,T,j,e));
  const numeric=b.map((x,k)=>(x-a[k])/(2*e)),actual=lastState.imageTangents[j];
  maxError=Math.max(maxError,Math.hypot(numeric[0]-actual[0],numeric[1]-actual[1]));
 }
 check(Math.abs(lastState.imageOpening-lastState.opening)<1e-10,'ordinary tangent opening');
}
check(maxError<1e-8,'chain rule agrees with derivatives of actual mapped curves');
byId('map').value='exp';byId('critical').click();
check(lastState.scale===1&&Math.abs(lastState.imageOpening-60)<1e-10,'exp ordinary at zero');
byId('neighborhood').value=.03;render();
check(lastState.h===.03,'local neighborhood control');
check(Math.abs((lastState.extents[1][0]+lastState.extents[1][1])/2-lastState.w[0])<1e-12,'local view centered at image point');

const basePanel=window.plotPanel,drawn={source:[],image:[]},arcs={source:[],image:[]};
window.plotPanel=(canvas,bounds)=>{const panel=basePanel(canvas,bounds),fill=panel.ctx.fillText,arc=panel.ctx.arc;panel.ctx.fillText=function(text,...args){drawn[canvas.id].push(text);return fill.call(this,text,...args);};panel.ctx.arc=function(...args){arcs[canvas.id].push(args);return arc.apply(this,args);};return panel;};
for(const sign of [65,-65,0,150,-150]){
 drawn.source=[];drawn.image=[];arcs.source=[];arcs.image=[];
 byId('opening').value=sign;byId('map').value='square';byId('real').value=.45;byId('imag').value=.3;render();
 check(Math.abs(lastState.imageOpening-sign)<1e-10,'signed image opening');
 check(drawn.source.includes('θ')&&!drawn.source.includes('θ′'),'source theta label');
 check(drawn.image.includes('θ′')&&!drawn.image.includes('θ'),'image theta prime label');
 for(const id of ['source','image']){
  const sector=arcs[id].find(args=>args[2]>20);check(sector,'visible angle arc');
  check(sector[5]===(sign>=0),'arc follows signed direction');
 }
 check(byId('image-angle').textContent.includes(sign<0?L('clockwise (−)','horario (−)'):sign>0?L('counterclockwise (+)','antihorario (+)'):L('zero opening','apertura cero')),'signed image caption');
}
window.plotPanel=basePanel;byId('reset').click();
`,
'schwarz-christoffel-heat':`$('center').click();check(Math.abs(state.T-60)<1e-10,'center temperature');$('corner').click();check(state.T===100,'hot corner');set(-1,0);check(state.T===20,'cold corner');$('reset').click();check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');const c=$('image').getContext('2d'),fill=c.fillText;let labels=[];c.fillText=function(t,x,y,...args){labels.push({t,x,y});return fill.call(this,t,x,y,...args);};$('corner').click();c.fillText=fill;const P=labels.find(p=>p.t==='P′'),hot=labels.find(p=>p.t==='100°');check(P&&hot&&Math.hypot(P.x-hot.x,P.y-hot.y)>20,'corner temperature and selected point separated');$('reset').click();`,
'peirce-atlas':`let err=0;for(const [lon,lat,x,y] of data.references){const q=PeirceMap.project(lon,lat);err=Math.max(err,Math.abs(q[0]-x),Math.abs(q[1]-y));}check(err<1e-9,'generated reference coordinates');const selected=lastState.point.slice();for(const button of document.querySelectorAll('[data-view]')){button.click();check(lastState.point.every((v,i)=>v===selected[i]),'view preserves P');}check(lastState.copies===9,'nine tile copies');$('south').click();check(lastState.relative===1&&lastState.point[0]===1&&lastState.point[1]===-1,'south pole');$('north').click();check(lastState.point.every(v=>v===0),'north pole');$('cut').click();check(!Number.isFinite(lastState.relative),'singular cut');select(-11.22,-43.30);document.querySelector('[data-view="mosaic"]').click();$('grid').checked=false;render();check(document.querySelector('.example-guide ol').children.length===3,'three practical reading steps');check(document.querySelector('.example-route'),'model and reproduction route');for(const input of document.querySelectorAll('input[type="range"]'))check(input.closest('label').querySelector('.control-live'),'visible slider value');$('longitude').value='';render();check($('status').textContent.includes(L('Enter longitude','Introduce longitud')),'empty geographic input explained');$('north').click();check(lastState.lon===0&&lastState.lat===90,'geographic selection recovers');document.querySelector('[data-view="scale"]').click();check(!$('scale-key').hidden,'scale legend shown in scale mode');document.querySelector('[data-view="mosaic"]').click();check($('scale-key').hidden,'scale legend hidden in imagery mode');select(-20.08,9.62);$('grid').checked=true;render();`,

};
(async()=>{try{
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port+'/';
let endpoint;for(let i=0;i<300;i++){const match=stderr.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(match){endpoint=match[1];break;}if(child.exitCode!==null)break;await sleep(100);}if(!endpoint)throw Error('Chromium did not expose DevTools: '+stderr.slice(-4000));
const url=new URL(endpoint),pages=await(await fetch('http://'+url.host+'/json/list')).json();ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
let id=0,pending=new Map(),errors=[],remote=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text+' '+(m.params.exceptionDetails.exception?.description||''));else if(m.method==='Network.requestWillBeSent'){const u=m.params.request.url;if(/^https?:/.test(u)&&new URL(u).origin!==new URL(base).origin)remote.push(u);}};
function call(method,params={}){return new Promise((resolve,reject)=>{const n=++id,timer=setTimeout(()=>{pending.delete(n);reject(Error('CDP timeout '+method));},25000);pending.set(n,{resolve,reject,timer});ws.send(JSON.stringify({id:n,method,params}));});}
await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
await call('Page.addScriptToEvaluateOnNewDocument',{source:"window.__policyEvents=[];addEventListener('securitypolicyviolation',e=>window.__policyEvents.push(e.violatedDirective));"});
for(const language of ['es','en'])for(const name of (process.env.SITE_LANGUAGE_NAV_ONLY?[]:Object.keys(tests).filter(name=>!process.env.SITE_BROWSER_CASES||process.env.SITE_BROWSER_CASES.split(',').includes(name))))for(const width of [1440,430]){
await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:name==='landing-reduced'?'reduce':'no-preference'}]});errors=[];remote=[];await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:false});await call('Page.navigate',{url:new URL((language==='es'?'es/':'')+(routeMap[name]||'examples/'+name+'.html')+'?lang='+language,base).href});
let ready=false;for(let i=0;i<100;i++){const r=await call('Runtime.evaluate',{expression:"document.readyState==='complete' && [...document.images].filter(i=>i.loading!=='lazy').every(i=>i.complete&&i.naturalWidth>0)",returnByValue:true});if(r.result.value){ready=true;break;}await sleep(100);}if(!ready)throw Error(name+' did not load');await sleep(100);
const expression=`(async()=>{const L=(en,es)=>document.documentElement.lang==='es'?es:en;const check=(b,m)=>{if(!b)throw Error(m)};try{${tests[name]}check(document.querySelector('.language-picker a:first-child').lang==='en','English first');const picker=document.querySelector('.language-picker').getBoundingClientRect(),heading=document.querySelector('h1').getBoundingClientRect();check(picker.bottom<=heading.top+1,'language selector above the page title');check(picker.right>innerWidth*.7,'language selector aligned to the right');if(document.body.classList.contains('page-example')){check(document.querySelector('.case-purpose strong'),'concrete purpose for this case');check(!document.querySelector('.case-audience'),'case introduction open to the general public');check(document.querySelector('.case-kicker'),'highlighted introduction retained');
const workspace=document.querySelector('.interactive-workspace'),parameters=workspace.querySelector('.parameter-controls'),visual=workspace.querySelector('.visual-stage');
check(workspace&&parameters&&visual,'controls beside their visual result');
check(!document.querySelector('details,summary'),'explanations are visible subtitles');
for(const element of document.querySelectorAll('input,select,button'))check(workspace.contains(element),'parameter control belongs to the visual workspace');
check(innerWidth>760?getComputedStyle(workspace.querySelector('.parameter-rail')).position==='sticky':getComputedStyle(parameters).position==='sticky','controls remain available while examining a plot');
if(innerWidth<=760){
 const height=parameters.getBoundingClientRect().height;for(const canvas of [visual.querySelector('canvas'),[...visual.querySelectorAll('canvas')].at(-1)]){
 scrollTo(0,canvas.getBoundingClientRect().top+scrollY-height-12);
 await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
 const r=parameters.getBoundingClientRect(),c=canvas.getBoundingClientRect();
 check(r.top>=-1&&r.bottom<innerHeight,'controls visible while inspecting the canvas '+JSON.stringify({top:r.top,bottom:r.bottom,canvas:c.top,scrollY}));
 check(c.top>=r.bottom-2&&c.top<innerHeight,'canvas visible beside the pinned controls');
 }scrollTo(0,0);
}
}check(document.documentElement.scrollWidth<=innerWidth+1,'horizontal page overflow');check(window.__policyEvents.length===0,'unexpected CSP violation '+window.__policyEvents);for(const m of document.querySelectorAll('math')){if(m.closest('[hidden]'))continue;check(m.getBoundingClientRect().height>0,'invisible mathematics');}return 'passed';}catch(e){return e.stack;}})()`;
const result=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.result.value!=='passed'||errors.length||remote.length)throw Error(name+' '+width+': '+result.result.value+' '+errors.join(';')+' remote resources '+remote.join(';'));
if(process.env.SITE_SCREENSHOTS&&name==='gallery'){await call('Runtime.evaluate',{expression:"Promise.all([...document.images].map(i=>{i.loading='eager';return i.complete?Promise.resolve():new Promise((r,j)=>{i.onload=r;i.onerror=()=>j(Error('gallery image failed'));});}))",awaitPromise:true});}
if(process.env.SITE_SCREENSHOTS){const dir=path.resolve(process.env.SITE_SCREENSHOTS);fs.mkdirSync(dir,{recursive:true});const metrics=await call('Page.getLayoutMetrics'),height=Math.min(Math.ceil(metrics.cssContentSize.height),5000),shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width,height,scale:1}});fs.writeFileSync(path.join(dir,language+'-'+name+'-'+width+'.png'),Buffer.from(shot.data,'base64'));}
if(process.env.SITE_SCREENSHOTS){const focus=await call('Runtime.evaluate',{expression:"(()=>{const g=document.querySelector('.interactive-workspace')||document.querySelector('.example-guide');if(!g)return null;const r=g.getBoundingClientRect();return {y:Math.max(0,r.top+scrollY-8),height:Math.min(1500,document.documentElement.scrollHeight-r.top-scrollY)};})()",returnByValue:true});if(focus.result.value){const {y,height}=focus.result.value,shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y,width,height,scale:1}});fs.writeFileSync(path.join(path.resolve(process.env.SITE_SCREENSHOTS),language+'-'+name+'-'+width+'-focus.png'),Buffer.from(shot.data,'base64'));}}
if(process.env.SITE_SCREENSHOTS){const region=await call('Runtime.evaluate',{expression:"(()=>{const e=document.querySelector('.project-credit')?.closest('footer');if(!e)return null;const r=e.getBoundingClientRect();return {x:0,y:Math.max(0,r.top+scrollY-12),width:innerWidth,height:Math.min(280,r.height+24)};})()",returnByValue:true});if(region.result.value){const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{...region.result.value,scale:1}});fs.writeFileSync(path.join(path.resolve(process.env.SITE_SCREENSHOTS),language+'-'+name+'-'+width+'-footer.png'),Buffer.from(shot.data,'base64'));}}
console.log(language,name,width,'passed');
}

async function navigateLanguage(relative, language, suffix) {
  await call('Page.navigate',{url:new URL(relative,base).href});
  for(let i=0;i<150;i++){
    const r=await call('Runtime.evaluate',{expression:`document.readyState==='complete' && document.documentElement.lang===${JSON.stringify(language)} && location.pathname.endsWith(${JSON.stringify(suffix)})`,returnByValue:true});
    if(r.result.value)return;await sleep(80);
  }
  throw Error('Language navigation did not settle: '+relative);
}
async function assertLanguage(expression, message){
  const result=await call('Runtime.evaluate',{expression,returnByValue:true});
  if(!result.result.value)throw Error(message);
}
await call('Runtime.evaluate',{expression:"localStorage.removeItem('pyconformal-language')"});
await navigateLanguage('index.html#cite','en','/index.html');
await assertLanguage("document.querySelector('.language-picker a:first-child').lang==='en'",'English first in the selector');
await assertLanguage("document.querySelector('.language-picker a[lang=es]').getAttribute('href').endsWith('?lang=es#cite')",'language switch preserves fragment');
await call('Runtime.evaluate',{expression:"document.querySelector('.language-picker a[lang=es]').click()"});
for(let i=0;i<100;i++){const r=await call('Runtime.evaluate',{expression:"document.readyState==='complete'&&document.documentElement.lang==='es'&&location.pathname.endsWith('/es/index.html')",returnByValue:true});if(r.result.value)break;await sleep(80);}
await assertLanguage("document.documentElement.lang==='es' && localStorage.getItem('pyconformal-language')==='es' && location.hash==='#cite'",'native switch to Spanish stores preference and fragment');
await navigateLanguage('examples/index.html','es','/es/examples/index.html');
await assertLanguage("document.querySelectorAll('.discovery-card').length===12",'preference survives navigating to another page');
await navigateLanguage('examples/index.html?lang=en','en','/examples/index.html');
await assertLanguage("localStorage.getItem('pyconformal-language')==='en'",'explicit English choice overrides saved Spanish');
await call('Emulation.setScriptExecutionDisabled',{value:true});
await navigateLanguage('es/docs/notation.html','es','/es/docs/notation.html');
await assertLanguage("document.querySelector('math') && document.querySelector('.language-picker a[lang=en]').getAttribute('href').includes('docs/notation.html')",'Spanish content, mathematics and native selector work without JavaScript');
await navigateLanguage('examples/index.html','en','/examples/index.html');
await assertLanguage("document.querySelectorAll('.discovery-card svg').length===12 && document.querySelector('h1').textContent.includes('discover')",'English gallery and previews work without JavaScript');
await call('Emulation.setScriptExecutionDisabled',{value:false});
const storageBlock=await call('Page.addScriptToEvaluateOnNewDocument',{source:"Object.defineProperty(window,'localStorage',{get(){throw Error('storage blocked for test')}});"});
errors=[];
await navigateLanguage('examples/index.html','en','/examples/index.html');
await assertLanguage("document.querySelector('.language-picker a[lang=es]')!==null",'selector works with storage denied');
await navigateLanguage('examples/index.html?lang=es','es','/es/examples/index.html');
if(errors.length)throw Error('Storage fallback failed: '+errors.join(';'));
await call('Page.removeScriptToEvaluateOnNewDocument',{identifier:storageBlock.identifier});
console.log('Language navigation: default, remembered choice, fragment, explicit override, no JavaScript and blocked storage passed');
await call('Runtime.evaluate',{expression:"const blocked=document.createElement('script');blocked.textContent='window.__injected=true';document.body.append(blocked);"});await sleep(100);
let result=await call('Runtime.evaluate',{expression:"window.__injected!==true && window.__policyEvents.some(d=>d.startsWith('script-src'))",returnByValue:true});if(!result.result.value)throw Error('Inline script policy did not block execution.');
await call('Runtime.evaluate',{expression:"fetch('https://example.invalid/should-not-be-sent').catch(()=>{});"});await sleep(100);result=await call('Runtime.evaluate',{expression:"window.__policyEvents.includes('connect-src')",returnByValue:true});if(!result.result.value)throw Error('Connection policy did not block the request.');
console.log('CSP probes: inline execution and outbound connections blocked');
try{await call('Browser.close');}catch{}
}catch(e){console.error(e.stack);process.exitCode=1;}finally{ws?.close();child.kill();server.close();await sleep(300);if(path.dirname(path.resolve(profile))===path.resolve(os.tmpdir())&&path.basename(profile).startsWith('pyconformal-check-')){try{fs.rmSync(profile,{recursive:true,force:true,maxRetries:3});}catch{}}}})();
