"""Server-side spatial interest filtering. Original MIT-licensed educational implementation."""

from math import isfinite

def relevant(entities, observer, radius, allowed):
    if not isfinite(radius) or radius<0: raise ValueError("invalid radius")
    if len(observer)!=2 or not all(isfinite(v) for v in observer): raise ValueError("invalid observer")
    result=[]
    for identifier,position in entities.items():
        if len(position)!=2 or not all(isfinite(v) for v in position): raise ValueError("invalid position")
        if allowed(identifier) and sum((a-b)**2 for a,b in zip(position,observer)) <= radius*radius:
            result.append(identifier)
    return sorted(result)
