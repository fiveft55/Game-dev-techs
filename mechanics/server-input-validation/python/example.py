"""Authoritative movement command validation. Original MIT-licensed educational implementation."""

from math import hypot,isfinite

class Player:
    def __init__(self, speed=5, dt=1/60):
        if not all(isfinite(v) for v in (speed,dt)) or speed<0 or dt<=0:
            raise ValueError("invalid server tuning")
        self.x=self.y=0.0; self.sequence=-1; self.speed=speed; self.dt=dt

    def apply(self, command):
        if not isinstance(command,dict) or set(command)!={'sequence','dx','dy'}:
            return False
        seq,dx,dy=(command[k] for k in ('sequence','dx','dy'))
        if type(seq) is not int or not self.sequence<seq<=2**53-1: return False
        if any(type(v) not in (int,float) for v in (dx,dy)): return False
        try:
            if not isfinite(dx) or not isfinite(dy) or hypot(dx,dy)>1: return False
        except OverflowError:
            return False
        # Never integrate client-supplied delta time or trust client-supplied position.
        self.x+=dx*self.speed*self.dt; self.y+=dy*self.speed*self.dt
        self.sequence=seq
        return True
