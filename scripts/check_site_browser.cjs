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
const routeMap={landing:'index.html','exercise-doc':'docs/exercises.html',notation:'docs/notation.html'};
const tests={
'notation':`check(document.querySelectorAll('math').length>15,'rendered mathematics');check(document.querySelector('mfrac'),'native fractions');`,
'schwarz-christoffel-square':`check(Math.hypot(...squareMap([0,1]))<1e-12,'SC center');`,
'square-map':`check(document.querySelector('math'),'square formula');`,
'disk-to-halfplane':`check(document.querySelector('mfrac'),'Cayley fraction');`,
'exponential-map':`check(document.querySelector('math'),'exponential formula');`,
'object-reveal':`check(document.querySelector('math'),'logarithm formula');`,
'coplanar-waveguide':`check(document.querySelectorAll('math').length>=3,'elliptic model formulas');`,
'coplanar-sensor':`check(document.querySelector('mfrac'),'sensor formula');`,
'lunar-thesis-interactive':`document.querySelector('[data-map="log"]').click();check(document.querySelector('[data-formula-map="log"]').hidden===false,'log formula follows selection');document.querySelector('[data-map="cube"]').click();check(document.querySelector('[data-formula-map="log"]').hidden,'old formula hidden');`,
'landing':`check(document.querySelectorAll('.journeys article').length===3,'three reading routes');check(document.querySelector('.hero img').naturalWidth===880,'lunar hero image');check(document.querySelector('a[href="examples/conformal-angle.html"]'),'featured curves demo');`,
'exercise-doc':`check(document.getElementById('e1-vector-angles-and-orientation'),'E1 anchor');check(document.getElementById('e10-audit-the-historical-figure'),'E10 anchor');check(document.querySelector('a[href="exercise-solutions.html"]'),'rendered solutions link');`,
'group-p':`document.querySelector('[data-thesis="reflection"]').click();check(document.getElementById('axis').value==='30','reflection axis preset');const original=stats(points);document.getElementById('negative').checked=true;render();check(document.getElementById('m3').textContent.includes(original.angle.toFixed(2)),'negative dilation angle');check(document.getElementById('thesis-note').textContent.includes('2Î±'),'matrix convention');document.querySelector('[data-thesis="definition"]').click();check(stats(points).angle!==90,'oblique definition');document.getElementById('reset').click();`,
'conformal-angle':`byId('opening').value=60;byId('real').value=.5;byId('imag').value=.5;render();check(Math.abs(lastState.scale-Math.sqrt(2))<1e-12,'derivative scale');check(Math.abs(lastState.imageOpening-60)<1e-10,'opening preserved');byId('critical').click();check(lastState.scale===0&&lastState.imageOpening===null,'critical tangent undefined');byId('map').value='exp';render();check(lastState.scale===1&&Math.abs(lastState.imageOpening-60)<1e-10,'exp ordinary at zero');byId('reset').click();`,
'schwarz-christoffel-heat':`$('center').click();check(Math.abs(state.T-60)<1e-10,'center temperature');$('corner').click();check(state.T===100,'hot corner');set(-1,0);check(state.T===20,'cold corner');$('reset').click();`,
'peirce-atlas':`let err=0;for(const [lon,lat,x,y] of data.references){const q=PeirceMap.project(lon,lat);err=Math.max(err,Math.abs(q[0]-x),Math.abs(q[1]-y));}check(err<1e-9,'generated reference coordinates');const selected=lastState.point.slice();for(const button of document.querySelectorAll('[data-view]')){button.click();check(lastState.point.every((v,i)=>v===selected[i]),'view preserves P');}check(lastState.copies===9,'nine tile copies');$('south').click();check(lastState.relative===1&&lastState.point[0]===1&&lastState.point[1]===-1,'south pole');$('north').click();check(lastState.point.every(v=>v===0),'north pole');$('cut').click();check(!Number.isFinite(lastState.relative),'singular cut');select(-11.22,-43.30);document.querySelector('[data-view="mosaic"]').click();$('grid').checked=false;render();`,

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
for(const name of Object.keys(tests))for(const width of [1440,430]){
errors=[];remote=[];await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:false});await call('Page.navigate',{url:new URL(routeMap[name]||'examples/'+name+'.html',base).href});
let ready=false;for(let i=0;i<100;i++){const r=await call('Runtime.evaluate',{expression:"document.readyState==='complete' && [...document.images].every(i=>i.complete&&i.naturalWidth>0)",returnByValue:true});if(r.result.value){ready=true;break;}await sleep(100);}if(!ready)throw Error(name+' did not load');await sleep(100);
const expression=`(()=>{const check=(b,m)=>{if(!b)throw Error(m)};try{${tests[name]}check(document.documentElement.scrollWidth<=innerWidth+1,'horizontal page overflow');check(window.__policyEvents.length===0,'unexpected CSP violation '+window.__policyEvents);for(const m of document.querySelectorAll('math')){if(m.closest('[hidden]'))continue;check(m.getBoundingClientRect().height>0,'invisible mathematics');}return 'passed';}catch(e){return e.stack;}})()`;
const result=await call('Runtime.evaluate',{expression,returnByValue:true});if(result.result.value!=='passed'||errors.length||remote.length)throw Error(name+' '+width+': '+result.result.value+' '+errors.join(';')+' remote resources '+remote.join(';'));
if(process.env.SITE_SCREENSHOTS){const dir=path.resolve(process.env.SITE_SCREENSHOTS);fs.mkdirSync(dir,{recursive:true});const metrics=await call('Page.getLayoutMetrics'),height=Math.min(Math.ceil(metrics.cssContentSize.height),5000),shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width,height,scale:1}});fs.writeFileSync(path.join(dir,name+'-'+width+'.png'),Buffer.from(shot.data,'base64'));}
console.log(name,width,'passed');
}
await call('Runtime.evaluate',{expression:"const blocked=document.createElement('script');blocked.textContent='window.__injected=true';document.body.append(blocked);"});await sleep(100);
let result=await call('Runtime.evaluate',{expression:"window.__injected!==true && window.__policyEvents.some(d=>d.startsWith('script-src'))",returnByValue:true});if(!result.result.value)throw Error('Inline script policy did not block execution.');
await call('Runtime.evaluate',{expression:"fetch('https://example.invalid/should-not-be-sent').catch(()=>{});"});await sleep(100);result=await call('Runtime.evaluate',{expression:"window.__policyEvents.includes('connect-src')",returnByValue:true});if(!result.result.value)throw Error('Connection policy did not block the request.');
console.log('CSP probes: inline execution and outbound connections blocked');
try{await call('Browser.close');}catch{}
}catch(e){console.error(e.stack);process.exitCode=1;}finally{ws?.close();child.kill();server.close();await sleep(300);if(path.dirname(path.resolve(profile))===path.resolve(os.tmpdir())&&path.basename(profile).startsWith('pyconformal-check-')){try{fs.rmSync(profile,{recursive:true,force:true,maxRetries:3});}catch{}}}})();
