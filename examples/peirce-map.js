// Same normalization and cut convention as pyconformal.cartography.
(() => {
  const radians = x => x*Math.PI/180;
  function project(longitude, latitude) {
    if(!Number.isFinite(longitude)||!Number.isFinite(latitude)||Math.abs(latitude)>90)
      throw new RangeError('Finite longitude and latitude in [-90,90] are required.');
    const angle=((longitude+45+180)%360+360)%360-180;
    let square;
    if(Math.abs(latitude)===90) square=[0,0];
    else if(latitude===0) square=SCSquare.map(angle===-180?null:[Math.abs(angle)===90?angle/90:Math.tan(radians(angle/2)),0]);
    else {
      const radius=Math.tan(radians((90-Math.abs(latitude))/2));
      const x=radius*Math.cos(radians(angle)),y=radius*Math.sin(radians(angle));
      const denominator=(1+x)**2+y*y;
      square=SCSquare.map([2*y/denominator,Math.max(0,(1-radius*radius)/denominator)]);
    }
    let [u,v]=square;
    if(latitude<0){const sector=((Math.floor(angle/90)%4)+4)%4;
      if(sector===0)v=-2-v; else if(sector===1)u=2-u; else if(sector===2)v=2-v; else u=-2-u;
    }
    return [(u-v)/2,(u+v)/2].map(x=>Math.max(-1,Math.min(1,x)));
  }
  function relativeScale(longitude,latitude) {
    const r=Math.tan(radians((90-Math.abs(latitude))/2)),a=radians(longitude+45),r4=r**4;
    const denominator=Math.sqrt(Math.hypot(1-r4*Math.cos(4*a),r4*Math.sin(4*a)));
    return denominator<1e-7?Infinity:(1+r*r)/denominator;
  }
  window.PeirceMap=Object.freeze({project,relativeScale});
})();
