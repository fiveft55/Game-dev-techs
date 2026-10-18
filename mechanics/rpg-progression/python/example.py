"""Experience levels and combat damage. Original MIT-licensed educational implementation."""

from bisect import bisect_right

def level_for(xp, thresholds=(0,100,300,600,1000)):
    if type(xp) is not int or xp < 0 or not thresholds or thresholds[0] != 0:
        raise ValueError("invalid experience table")
    if any(type(t) is not int for t in thresholds) or any(a >= b for a,b in zip(thresholds,thresholds[1:])):
        raise ValueError("thresholds must strictly increase")
    # bisect_right advances the level exactly at each boundary.
    return bisect_right(thresholds,xp)

def damage(attack, armor):
    if attack < 0 or armor < 0: raise ValueError("negative combat statistic")
    return max(0, attack-armor)
