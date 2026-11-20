/* Square complex torus C/(Z+iZ). Classical theta/Jacobi formula, DLMF 20.2, 22.2, 23.6. */
(() => {
  'use strict';
  const add=([a,b],[c,d])=>[a+c,b+d],mul=([a,b],[c,d])=>[a*c-b*d,a*d+b*c];
  const scale=([a,b],t)=>[a*t,b*t],div=([a,b],[c,d])=>{const q=c*c+d*d;return [(a*c+b*d)/q,(b*c-a*d)/q];};
  const sin=([x,y])=>[Math.sin(x)*Math.cosh(y),Math.cos(x)*Math.sinh(y)];
  const cos=([x,y])=>[Math.cos(x)*Math.cosh(y),-Math.sin(x)*Math.sinh(y)];
  const centered=x=>x-Math.floor(x+.5),wrap=x=>x-Math.floor(x);
  function theta(z){
    const v=scale(z,Math.PI);let t1=[0,0],t4=[1,0],d1=[0,0],d4=[0,0];
    for(let n=0;n<9;n++){
      const a=2*(n%2?-1:1)*Math.exp(-Math.PI*(n+.5)**2),f=2*n+1;
      t1=add(t1,scale(sin(scale(v,f)),a));d1=add(d1,scale(cos(scale(v,f)),a*f*Math.PI));
      if(n){const b=2*(n%2?-1:1)*Math.exp(-Math.PI*n*n),g=2*n;
        t4=add(t4,scale(cos(scale(v,g)),b));d4=add(d4,scale(sin(scale(v,g)),-b*g*Math.PI));}
    }
    return {t1,t4,d1,d4};
  }
  function evaluate(z,reduce=true){
    if(!z.every(Number.isFinite))throw new RangeError('Finite complex coordinates are required.');
    const p=reduce?z.map(centered):z.slice(),{t1,t4,d1,d4}=theta(p);
    // F = A/B is used homogeneously on the sphere, including its double pole.
    const B=mul(t1,t1),A=add(scale(mul(t4,t4),Math.SQRT2),scale(B,-1));
    const denominator=Math.hypot(...B),pole=denominator===0;
    const value=pole?null:div(A,B);
    let derivative=null;
    if(!pole){const ratio=div(t4,t1),ratioDerivative=div(add(mul(d4,t1),scale(mul(t4,d1),-1)),B);derivative=scale(mul(ratio,ratioDerivative),2*Math.SQRT2);}
    const magnitudeA=A[0]*A[0]+A[1]*A[1],magnitudeB=B[0]*B[0]+B[1]*B[1],norm=magnitudeA+magnitudeB;
    const cross=mul(A,[B[0],-B[1]]);
    const sphere=[2*cross[0]/norm,2*cross[1]/norm,(magnitudeA-magnitudeB)/norm];
    return {value,derivative,sphere,pole};
  }
  const torus=([s,t])=>{const a=2*Math.PI*s,b=2*Math.PI*t,r=1+.38*Math.cos(b);return [r*Math.cos(a),r*Math.sin(a),.38*Math.sin(b)];};
  const mate=([s,t])=>[wrap(-s),wrap(-t)];
  const branch=z=>z.every(x=>Math.abs(2*x-Math.round(2*x))<1e-10);
  globalThis.RiemannTorus=Object.freeze({evaluate,torus,mate,branch,wrap,centered});
})();
