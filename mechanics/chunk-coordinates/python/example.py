"""World-to-chunk coordinates. Original MIT-licensed educational implementation."""

def split(x, y, size=16):
    if any(type(v) is not int for v in (x,y,size)) or size<=0:
        raise ValueError("integer coordinates and positive size required")
    cx,lx=divmod(x,size); cy,ly=divmod(y,size)
    return (cx,cy),(lx,ly)

def join(chunk, local, size=16):
    if type(size) is not int or size<=0 or any(type(v) is not int for v in (*chunk,*local)):
        raise ValueError("invalid coordinates")
    if any(not 0<=v<size for v in local): raise ValueError("local coordinate outside chunk")
    return chunk[0]*size+local[0],chunk[1]*size+local[1]
