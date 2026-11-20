(() => {
 'use strict';
 const $=id=>document.getElementById(id),T=RiemannTorus,es=document.documentElement.lang==='es',tr=(a,b)=>es?b:a;
 const gold='#bd771b',purple='#725092',teal='#16867b',ink='#183b46';
 let periods=[0,0],lastState,dragging=false;
 function panel(id){const canvas=$(id),w=canvas.clientWidth,d=Math.min(devicePixelRatio||1,2);canvas.width=canvas.height=Math.round(w*d);const c=canvas.getContext('2d');c.scale(d,d);return {canvas,c,w};}
 function line(c,points,color,width=1,dash=[]){c.save();c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.strokeStyle=color;c.lineWidth=width;c.setLineDash(dash);c.stroke();c.restore();}
 function text(c,label,x,y,color=ink){c.save();c.font='bold 13px system-ui';x=Math.max(8,Math.min(c.canvas.clientWidth-8-c.measureText(label).width,x));y=Math.max(17,Math.min(c.canvas.clientHeight-10,y));c.lineWidth=4;c.strokeStyle='white';c.strokeText(label,x,y);c.fillStyle=color;c.fillText(label,x,y);c.restore();}
 function dot(c,p,label,color){c.beginPath();c.arc(p[0],p[1],8,0,Math.PI*2);c.fillStyle=color;c.fill();c.lineWidth=2;c.strokeStyle='white';c.stroke();c.beginPath();c.arc(p[0],p[1],11,0,Math.PI*2);c.lineWidth=1;c.strokeStyle=color;c.stroke();text(c,label,p[0]+13,p[1]-12,color);}
 const rotate=(p,yaw,pitch=.66)=>{const [x,y,z]=p,a=x*Math.cos(yaw)-y*Math.sin(yaw),b=x*Math.sin(yaw)+y*Math.cos(yaw);return [a,b*Math.cos(pitch)-z*Math.sin(pitch),b*Math.sin(pitch)+z*Math.cos(pitch)];};
 const sphereProjection=w=>p=>{const q=rotate(p,.35,-.6);return [w/2+q[0]*w*.35,w/2-q[1]*w*.35,q[2]];};
 function drawChart(p,q,ramified){
  const {c,w} =panel('chart'),margin=38,size=w-2*margin,project=([s,t])=>[margin+s*size,w-margin-t*size];
  for(let i=0;i<=10;i++){const x=i/10;line(c,[project([x,0]),project([x,1])],'#dbe8e0');line(c,[project([0,x]),project([1,x])],'#dbe8e0');}
  for(const y of [0,1]){line(c,[project([0,y]),project([1,y])],teal,3);const a=project([.43,y]),b=project([.57,y]);line(c,[a,b,[b[0]-7,b[1]-5]],teal,2);}
  for(const x of [0,1]){line(c,[project([x,0]),project([x,1])],gold,3);const a=project([x,.43]),b=project([x,.57]);line(c,[a,b,[b[0]+5,b[1]+7]],gold,2);}
  text(c,'0',margin-17,w-margin+19);text(c,'1',w-margin-4,w-margin+19);text(c,'i',margin-16,margin+4);text(c,'1+i',w-margin-15,margin-12);
  for(const z of [[0,0],[.5,0],[0,.5],[.5,.5]]){const a=project(z);c.beginPath();c.arc(...a,3,0,Math.PI*2);c.fillStyle='#776985';c.fill();}
  if(!ramified)dot(c,project(q),'Q',purple);dot(c,project(p),ramified?'P ≡ Q':'P',gold);
  return {margin,size};
 }
 function drawTorus(p,q,ramified){
  const {c,w}=panel('torus'),yaw=Number($('camera').value)*Math.PI/180;
  const project=p=>{const r=rotate(p,yaw);return [w/2+r[0]*w*.30,w/2-r[1]*w*.30,r[2]];};
  const faces=[];
  for(let i=0;i<48;i++)for(let j=0;j<20;j++){
   const vertices=[[i,j],[i+1,j],[i+1,j+1],[i,j+1]].map(([u,v])=>project(T.torus([u/48,v/20])));
   faces.push({vertices,depth:vertices.reduce((a,p)=>a+p[2],0)/4,light:.56+.22*Math.cos((j+.5)/20*2*Math.PI)+.12*Math.sin((i+.5)/48*2*Math.PI)});
  }
  faces.sort((a,b)=>a.depth-b.depth);
  for(const f of faces){c.beginPath();f.vertices.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1]));c.closePath();const l=Math.round(47+f.light*32);c.fillStyle=`hsl(157 23% ${l}%)`;c.fill();c.strokeStyle=c.fillStyle;c.lineWidth=.5;c.stroke();}
  for(let i=0;i<12;i++){
   const a=Array.from({length:121},(_,j)=>project(T.torus([j/120,i/12]))),b=Array.from({length:121},(_,j)=>project(T.torus([i/12,j/120])));
   // Split front/back pieces; a faint hidden grid makes the identification traceable.
   for(const [points,color] of [[a,teal],[b,gold]])for(let j=1;j<points.length;j++)line(c,[points[j-1].slice(0,2),points[j].slice(0,2)],points[j][2]>0?color:color+'35',.7);
  }
  if(!ramified)dot(c,project(T.torus(q)),'Q',purple);dot(c,project(T.torus(p)),ramified?'P ≡ Q':'P',gold);
 }
 function drawSphere(result){
  const {c,w}=panel('sphere'),project=sphereProjection(w),radius=w*.35;
  const gradient=c.createRadialGradient(w*.36,w*.33,w*.02,w/2,w/2,radius);gradient.addColorStop(0,'#f1f7f4');gradient.addColorStop(1,'#c3d7cf');c.beginPath();c.arc(w/2,w/2,radius,0,2*Math.PI);c.fillStyle=gradient;c.fill();c.strokeStyle='#638b7a';c.stroke();
  for(let a=0;a<12;a++){
   const points=Array.from({length:121},(_,j)=>{const lat=-Math.PI/2+j/120*Math.PI,lon=a/12*2*Math.PI;return project([Math.cos(lat)*Math.cos(lon),Math.cos(lat)*Math.sin(lon),Math.sin(lat)]);});
   for(let j=1;j<points.length;j++)line(c,[points[j-1].slice(0,2),points[j].slice(0,2)],points[j][2]>0?'#759a8d88':'#759a8d22',.8);
  }
  const values=[[[0,0,1],'∞'],[[1,0,0],'+1'],[[-1,0,0],'−1'],[[0,0,-1],'0']];
  for(const [p,label] of values){const a=project(p);c.beginPath();c.arc(a[0],a[1],3,0,2*Math.PI);c.fillStyle=ink;c.fill();text(c,label,a[0]-19,a[1]+17);}
  dot(c,project(result.sphere),'F(P) = F(Q)',gold);
 }
 const format=z=>z===null?'∞':`${Math.abs(z[0])<1e-10?'0':z[0].toFixed(5)} ${z[1]<-1e-10?'−':'+'} ${Math.abs(z[1])<1e-10?'0':Math.abs(z[1]).toFixed(5)}i`;
 function render(){
  const p=[Number($('u').value),Number($('v').value)],q=T.mate(p),result=T.evaluate(p),paired=T.evaluate(q),ramified=T.branch(p);
  const chart=drawChart(p,q,ramified);drawTorus(p,q,ramified);drawSphere(result);
  $('u-value').textContent=p[0].toFixed(3);$('v-value').textContent=p[1].toFixed(3);$('camera-value').textContent=$('camera').value+'°';
  $('lift').textContent=`z = ${format([p[0]+periods[0],p[1]+periods[1]])}`;
  $('period-note').textContent=tr('Adding 1 or i changes the coordinate representative, not the torus point or its elliptic image.','Sumar 1 o i cambia el representante, pero no el punto del toro ni su imagen elíptica.');
  $('pair').textContent=`P = ${format(p)}; Q ≡ −P = ${format(q)}`;
  $('image-value').textContent=`F(P) = F(Q) = ${format(result.value)}`;
  $('status').textContent=ramified?(result.pole?tr('Ramification over infinity: F has a double pole. The reciprocal coordinate 1/F has a double zero.','Ramificación sobre infinito: F tiene un polo doble. La coordenada recíproca 1/F tiene un cero doble.'):tr('Half-period: P and Q are the same torus point. Here F′ = 0 and the map is ramified.','Semiperíodo: P y Q son el mismo punto del toro. Aquí F′ = 0 y la aplicación está ramificada.')):tr('P and Q are distinct torus points with one elliptic image. The map is locally conformal here.','P y Q son puntos distintos del toro con una imagen elíptica común. La aplicación es localmente conforme aquí.');
  document.querySelectorAll('[data-branch]').forEach(button=>{const z=[[0,0],[.5,0],[0,.5],[.5,.5]][Number(button.dataset.branch)];button.setAttribute('aria-pressed',String(Math.hypot(T.centered(p[0]-z[0]),T.centered(p[1]-z[1]))<1e-10));});
  lastState={p,q,result,paired,ramified,periods:periods.slice(),chart};
 }
 document.querySelectorAll('input').forEach(input=>input.addEventListener('input',render));
 $('period-real').onclick=()=>{periods[0]++;render();};$('period-imag').onclick=()=>{periods[1]++;render();};
 document.querySelectorAll('[data-branch]').forEach(button=>button.onclick=()=>{const p=[[0,0],[.5,0],[0,.5],[.5,.5]][Number(button.dataset.branch)];$('u').value=p[0];$('v').value=p[1];periods=[0,0];render();});
 $('reset').onclick=()=>{$('u').value=.23;$('v').value=.31;$('camera').value=-28;periods=[0,0];render();};
 function move(event){const r=$('chart').getBoundingClientRect(),{margin,size}=lastState.chart;$('u').value=Math.max(0,Math.min(1,(event.clientX-r.left-margin)/size));$('v').value=Math.max(0,Math.min(1,1-(event.clientY-r.top-margin)/size));periods=[0,0];render();}
 $('chart').addEventListener('pointerdown',event=>{if(event.button!==0)return;dragging=true;$('chart').setPointerCapture(event.pointerId);move(event);});$('chart').addEventListener('pointermove',event=>{if(dragging)move(event);});for(const name of ['pointerup','pointercancel','lostpointercapture'])$('chart').addEventListener(name,()=>dragging=false);
 // Expose only the small review interface needed by the numerical/browser checks.
 globalThis.RiemannTorusDemo=Object.freeze({state:()=>lastState,render});
 new ResizeObserver(render).observe($('chart'));render();
})();
