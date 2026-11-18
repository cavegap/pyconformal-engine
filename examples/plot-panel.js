// Equal-unit canvas panels for the standalone teaching examples.
window.plotPanel = function(canvas, bounds) {
  const width = canvas.clientWidth, height = canvas.clientHeight;
  const density = window.devicePixelRatio || 1;
  canvas.width = Math.round(width * density); canvas.height = Math.round(height * density);
  const ctx = canvas.getContext('2d'); ctx.scale(density, density);
  const [left, right, bottom, top] = bounds;
  const unit = Math.min((width - 50)/(right-left), (height - 50)/(top-bottom));
  const project = ([x,y]) => [width/2 + (x-(left+right)/2)*unit, height/2 - (y-(bottom+top)/2)*unit];
  function line(points, color, weight=1.5, dash=[]) {
    ctx.save(); ctx.beginPath(); ctx.rect(8,8,width-16,height-16); ctx.clip();
    ctx.beginPath(); points.forEach((p,i) => i ? ctx.lineTo(...project(p)) : ctx.moveTo(...project(p)));
    ctx.strokeStyle=color; ctx.lineWidth=weight; ctx.setLineDash(dash); ctx.stroke(); ctx.restore();
  }
  function label(text, point, dx=9, dy=-9, color='#17374a') {
    const [x,y]=project(point); ctx.font='bold 12px system-ui'; ctx.lineWidth=4;
    ctx.strokeStyle='white'; ctx.strokeText(text,x+dx,y+dy); ctx.fillStyle=color; ctx.fillText(text,x+dx,y+dy);
  }
  function dot(point, text='', color='#ffd479') {
    const [x,y]=project(point); ctx.beginPath(); ctx.arc(x,y,5.5,0,2*Math.PI);
    ctx.fillStyle=color; ctx.fill(); ctx.strokeStyle='#17374a'; ctx.lineWidth=1.7; ctx.stroke();
    if(text)label(text,point);
  }
  function arrow(a,b,color) {
    line([a,b],color,2.2); const p=project(a),q=project(b),angle=Math.atan2(q[1]-p[1],q[0]-p[0]);
    ctx.beginPath(); ctx.moveTo(...q); ctx.lineTo(q[0]-9*Math.cos(angle-.4),q[1]-9*Math.sin(angle-.4));
    ctx.lineTo(q[0]-9*Math.cos(angle+.4),q[1]-9*Math.sin(angle+.4)); ctx.closePath(); ctx.fillStyle=color; ctx.fill();
  }
  function raster(image, extent) {
    const [l,r,b,t]=extent,[x,y]=project([l,t]); ctx.drawImage(image,x,y,(r-l)*unit,(t-b)*unit);
  }
  function grid(step=.5) {
    for(let x=Math.ceil(left/step)*step;x<=right;x+=step)line([[x,bottom],[x,top]],'#d6e3e3',.7);
    for(let y=Math.ceil(bottom/step)*step;y<=top;y+=step)line([[left,y],[right,y]],'#d6e3e3',.7);
    line([[left,0],[right,0]],'#819b9c',1); line([[0,bottom],[0,top]],'#819b9c',1);
  }
  return {ctx,project,line,label,dot,arrow,raster,grid,unit};
};
