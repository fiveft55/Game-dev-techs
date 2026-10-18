"""Battle royale shrinking safe zone. Original MIT-licensed educational implementation."""

from math import hypot

def zone(start_center, end_center, start_radius, end_radius, started, duration, now):
    if duration<=0 or not 0<=end_radius<=start_radius: raise ValueError("invalid shrinking phase")
    alpha=max(0.0,min(1.0,(now-started)/duration))
    center=tuple(a+(b-a)*alpha for a,b in zip(start_center,end_center))
    return center,start_radius+(end_radius-start_radius)*alpha

def damage(position, center, radius, rate, dt):
    if radius<0 or rate<0 or dt<0: raise ValueError("negative zone parameter")
    return rate*dt if hypot(position[0]-center[0],position[1]-center[1])>radius else 0.0
