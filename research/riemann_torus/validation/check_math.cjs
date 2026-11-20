const fs=require('node:fs'),path=require('node:path');
require('../../../examples/riemann-torus-math.js');
const T=globalThis.RiemannTorus,ref=JSON.parse(fs.readFileSync(path.join(__dirname,'references.json'),'utf8'));
const dist=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));
let sphereError=0,valueError=0,periodError=0,pairError=0,derivativeError=0;
const check=(condition,message)=>{if(!condition)throw Error(message);};
for(const row of ref.rows){
 const out=T.evaluate(row.z);sphereError=Math.max(sphereError,dist(out.sphere,row.sphere));
 if(row.value)valueError=Math.max(valueError,dist(out.value,row.value)/(1+Math.hypot(...row.value)));
 check(Math.abs(Math.hypot(...out.sphere)-1)<2e-14,'unit sphere');
 pairError=Math.max(pairError,dist(out.sphere,T.evaluate(T.mate(row.z)).sphere));
}
for(const z of [[.21,.28],[.37,.09],[.49,.47],[.07,.76]]){
 const out=T.evaluate(z,false);
 for(const shift of [[1,0],[0,1],[-1,0],[0,-1]])periodError=Math.max(periodError,dist(out.sphere,T.evaluate(z.map((x,i)=>x+shift[i]),false).sphere));
 const h=1e-6,a=T.evaluate([z[0]-h,z[1]]).value,b=T.evaluate([z[0]+h,z[1]]).value;
 derivativeError=Math.max(derivativeError,dist(out.derivative,b.map((x,i)=>(x-a[i])/(2*h)))/(1+Math.hypot(...out.derivative)));
}
for(const [z,w] of [[[.5,0],1],[[0,.5],-1],[[.5,.5],0]]){
 const out=T.evaluate(z);check(dist(out.value,[w,0])<1e-12,'branch value');check(Math.hypot(...out.derivative)<1e-11,'branch derivative');check(T.branch(z),'half-period is branch point');
}
check(T.evaluate([0,0]).pole,'double pole maps to north pole');
const report={referenceDigits:70,referencePoints:ref.rows.length,sphereError,valueError,periodError,pairError,derivativeError};
console.log(report);
check(sphereError<1e-12&&valueError<1e-11&&periodError<1e-11&&pairError<1e-11&&derivativeError<1e-7,'numerical tolerances');
fs.writeFileSync(path.join(__dirname,'results.json'),JSON.stringify(report,null,2)+'\n');
