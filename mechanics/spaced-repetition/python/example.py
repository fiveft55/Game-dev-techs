"""Learning review scheduling. Original MIT-licensed educational implementation."""

from math import isfinite

def review(previous_days, correct, now):
    if not isfinite(previous_days) or previous_days<0 or not isfinite(now):
        raise ValueError("invalid review state")
    if type(correct) is not bool: raise ValueError("correct must be a boolean")
    days=max(1.0,previous_days*2) if correct else 1.0
    return days,now+days*86400
