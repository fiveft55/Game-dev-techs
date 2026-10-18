"""Rhythm timing windows. Original MIT-licensed educational implementation."""

from math import isfinite

class Note:
    def __init__(self, at, perfect=.03, good=.08):
        if not all(isfinite(v) for v in (at,perfect,good)) or not 0 <= perfect <= good:
            raise ValueError("invalid timing windows")
        self.at,self.perfect,self.good=at,perfect,good
        self.result=None

    def press(self, recorded_at, latency=0):
        if not isfinite(recorded_at) or not isfinite(latency): raise ValueError("invalid timestamp")
        if self.result is not None: return None
        error=abs(recorded_at-latency-self.at)
        if error > self.good: return None
        self.result='perfect' if error <= self.perfect else 'good'
        return self.result

    def expire(self, audio_time):
        if not isfinite(audio_time): raise ValueError("invalid timestamp")
        if self.result is None and audio_time > self.at+self.good: self.result='miss'
        return self.result
