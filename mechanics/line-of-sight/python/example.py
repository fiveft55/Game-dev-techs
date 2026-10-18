"""Conservative grid line of sight. Original MIT-licensed educational implementation."""

def visible(grid, start, goal):
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("nonempty rectangular grid required")
    def clear(x,y):
        return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] == 0
    x,y = start
    gx,gy = goal
    if any(type(v) is not int for v in (*start,*goal)):
        raise ValueError("integer cells required")
    if not clear(x,y) or not clear(gx,gy): return False
    nx,ny = abs(gx-x),abs(gy-y)
    sx,sy = (1 if gx>x else -1),(1 if gy>y else -1)
    ix=iy=0
    while ix < nx or iy < ny:
        decision=(1+2*ix)*ny-(1+2*iy)*nx
        if decision == 0:
            # A corner touches both side cells, not just the diagonal one.
            if not clear(x+sx,y) or not clear(x,y+sy): return False
            x+=sx; y+=sy; ix+=1; iy+=1
        elif decision < 0: x+=sx; ix+=1
        else: y+=sy; iy+=1
        if not clear(x,y): return False
    return True
