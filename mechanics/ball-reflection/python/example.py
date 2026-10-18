"""Ball bounce against a surface. Original MIT-licensed educational implementation."""

from math import hypot

def bounce(velocity, normal, restitution=1.0):
    if not 0 <= restitution <= 1: raise ValueError("restitution outside [0,1]")
    nx,ny=normal; length=hypot(nx,ny)
    if length == 0: raise ValueError("zero normal")
    nx/=length; ny/=length
    vx,vy=velocity; incoming=vx*nx+vy*ny
    if incoming >= 0: return (vx,vy)
    # Only the normal component loses energy; tangent velocity is preserved.
    impulse=(1+restitution)*incoming
    return vx-impulse*nx,vy-impulse*ny
