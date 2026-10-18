"""Ability charges and cooldown refill. Original MIT-licensed educational implementation."""

from math import isfinite
import heapq

class Cooldown:
    def __init__(self, charges=1, duration=1):
        if type(charges) is not int or charges<=0 or not isfinite(duration) or duration<=0:
            raise ValueError("invalid cooldown")
        self.capacity=charges; self.duration=duration; self.pending=[]; self.now=0.0

    def available(self, now):
        if not isfinite(now) or now<self.now: raise ValueError("nonmonotonic clock")
        self.now=now
        while self.pending and self.pending[0]<=now: heapq.heappop(self.pending)
        return self.capacity-len(self.pending)

    def use(self, now):
        if self.available(now)==0: return False
        heapq.heappush(self.pending,now+self.duration)
        return True
