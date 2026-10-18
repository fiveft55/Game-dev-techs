import random

def generate(width,height,seed=0):
    if width<3 or height<3 or width%2==0 or height%2==0:
        raise ValueError("odd dimensions >= 3 required")
    rng=random.Random(seed); grid=[[1]*width for _ in range(height)]
    grid[1][1]=0; stack=[(1,1)]
    while stack:
        x,y=stack[-1]
        options=[(x+dx,y+dy) for dx,dy in ((2,0),(-2,0),(0,2),(0,-2))
                 if 0<x+dx<width-1 and 0<y+dy<height-1 and grid[y+dy][x+dx]]
        if not options: stack.pop(); continue
        nx,ny=rng.choice(options)
        # Carve the wall between adjacent maze cells.
        grid[(y+ny)//2][(x+nx)//2]=0; grid[ny][nx]=0; stack.append((nx,ny))
    return grid
