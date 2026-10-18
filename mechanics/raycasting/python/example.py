from math import floor, inf

def cast(grid, origin, direction, limit=100):
    if not grid or not grid[0] or any(len(row)!=len(grid[0]) for row in grid):
        raise ValueError("grid must be nonempty and rectangular")
    ox,oy=origin; dx,dy=direction
    if dx==0 and dy==0: raise ValueError("zero ray")
    x,y=floor(ox),floor(oy)
    sx=1 if dx>0 else -1; sy=1 if dy>0 else -1
    tx=((x+1-ox)/dx if dx>0 else (x-ox)/dx) if dx else inf
    ty=((y+1-oy)/dy if dy>0 else (y-oy)/dy) if dy else inf
    stepx=abs(1/dx) if dx else inf; stepy=abs(1/dy) if dy else inf
    t=0.0
    for _ in range(limit):
        if not (0<=y<len(grid) and 0<=x<len(grid[0])): return None
        if grid[y][x]: return (x,y,t)
        # Step to the next grid boundary rather than sampling arbitrary distances.
        if tx<ty: t=tx; tx+=stepx; x+=sx
        else: t=ty; ty+=stepy; y+=sy
    return None
