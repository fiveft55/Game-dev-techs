from math import floor

def build(points,size):
    if size<=0: raise ValueError("nonpositive cell size")
    buckets={}
    for identifier,(x,y) in points.items():
        cell=(floor(x/size),floor(y/size))
        buckets.setdefault(cell,[]).append(identifier)
    return buckets

def nearby(buckets,point,size):
    if size<=0: raise ValueError("nonpositive cell size")
    x,y=(floor(v/size) for v in point)
    # Nine cells suffice only for a query radius at most one cell wide.
    return [i for dx in (-1,0,1) for dy in (-1,0,1)
            for i in buckets.get((x+dx,y+dy),[])]
