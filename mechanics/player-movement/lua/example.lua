-- Normalize diagonal input; retain partial analog-stick magnitude.
local function move(x,y,ix,iy,speed,dt)
  local scale=math.max(1,math.sqrt(ix*ix+iy*iy))
  return x+ix/scale*speed*dt,y+iy/scale*speed*dt
end
local x,y=move(0,0,1,1,1,1)
assert(math.abs(x*x+y*y-1)<1e-9)
return {move=move}
