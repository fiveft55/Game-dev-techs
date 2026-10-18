"""Sprite animation timeline sampling. Original MIT-licensed educational implementation."""

from bisect import bisect_right
from itertools import accumulate
from math import isfinite

class Animation:
    def __init__(self, frames, durations):
        self.frames=list(frames); durations=list(durations)
        if not self.frames or len(self.frames)!=len(durations) or any(not isfinite(t) or t<=0 for t in durations):
            raise ValueError("one positive duration per frame required")
        self.ends=list(accumulate(durations)); self.total=self.ends[-1]
        if not isfinite(self.total): raise ValueError("duration overflow")

    def sample(self, elapsed, loop=True):
        if not isfinite(elapsed) or elapsed<0: raise ValueError("invalid elapsed time")
        if not loop and elapsed>=self.total: return self.frames[-1]
        time=elapsed%self.total if loop else elapsed
        return self.frames[bisect_right(self.ends,time)]
