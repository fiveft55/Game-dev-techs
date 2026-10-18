"""Rotated grid footprint placement. Original MIT-licensed educational implementation."""

def place(occupied, footprint, anchor, width, height, turns=0):
    occupied=set(occupied); footprint=set(footprint)
    if type(width) is not int or type(height) is not int or width<=0 or height<=0 or not footprint or type(turns) is not int:
        raise ValueError("invalid footprint or grid")
    if any(type(v) is not int for point in [*occupied,*footprint,anchor] for v in point):
        raise ValueError("integer cells required")
    cells=set()
    for x,y in footprint:
        for _ in range(turns%4): x,y=-y,x
        cells.add((x+anchor[0],y+anchor[1]))
    if cells & occupied or any(not (0<=x<width and 0<=y<height) for x,y in cells): return None
    return occupied | cells
