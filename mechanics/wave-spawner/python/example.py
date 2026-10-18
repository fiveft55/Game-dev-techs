"""Timed enemy wave spawning. Original MIT-licensed educational implementation."""

from math import isfinite

class Wave:
    def __init__(self, schedule):
        self.schedule=sorted(list(schedule),key=lambda event:event[0])
        if any(not isfinite(t) or t < 0 for t,_ in self.schedule):
            raise ValueError("invalid spawn time")
        self.index=0; self.last_time=0.0

    def update(self, now):
        if not isfinite(now) or now < self.last_time: raise ValueError("nonmonotonic time")
        self.last_time=now; due=[]
        while self.index < len(self.schedule) and self.schedule[self.index][0] <= now:
            due.append(self.schedule[self.index][1]); self.index+=1
        return due

    @property
    def finished(self):
        return self.index == len(self.schedule)
