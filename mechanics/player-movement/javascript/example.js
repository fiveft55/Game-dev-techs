"use strict";
// Units: position in world units, speed in units/second, dt in seconds.
function move(x,y,ix,iy,speed,dt) {
  const scale=Math.max(1,Math.hypot(ix,iy));
  return [x+ix/scale*speed*dt,y+iy/scale*speed*dt];
}
if (require.main === module) {
  const [x,y]=move(0,0,1,1,1,1);
  require('node:assert/strict').ok(Math.abs(x*x+y*y-1)<1e-9);
}
module.exports={move};
