"""Discrete-event simulation scheduler. Original MIT-licensed educational implementation."""

import heapq
from itertools import count
from math import isfinite

class Scheduler:
    def __init__(self):
        self.now=0.0; self.queue=[]; self.serial=count()

    def schedule(self, at, event):
        if not isfinite(at) or at < self.now: raise ValueError("cannot schedule into the past")
        # A serial number prevents comparison of unrelated payload objects.
        heapq.heappush(self.queue,(at,next(self.serial),event))

    def advance(self, target):
        if not isfinite(target) or target < self.now: raise ValueError("nonmonotonic target")
        result=[]
        while self.queue and self.queue[0][0] <= target:
            at,_,event=heapq.heappop(self.queue)
            result.append((at,event))
        self.now=target
        return result
