def extrude(profile,height):
    if len(profile)<3 or height<=0: raise ValueError("invalid extrusion")
    n=len(profile)
    vertices=[(x,y,z) for z in (0,height) for x,y in profile]
    faces=[]
    for i in range(1,n-1):
        # Bottom faces point down, top faces point up.
        faces.extend([(0,i+1,i),(n,n+i,n+i+1)])
    for i in range(n):
        j=(i+1)%n
        faces.extend([(i,j,n+j),(i,n+j,n+i)])
    return vertices,faces
