"""Social deduction secret ballot resolution. Original MIT-licensed educational implementation."""

from collections import Counter

def resolve(voters, candidates, ballots):
    voters,candidates=set(voters),set(candidates)
    if None in voters or None in candidates: raise ValueError("None is reserved for skip")
    if not set(ballots)<=voters: raise ValueError("ineligible voter")
    if any(target is not None and target not in candidates for target in ballots.values()):
        raise ValueError("ineligible candidate")
    counts=Counter(ballots.values())
    if not counts: return None
    best=max(counts.values())
    winners=[target for target,count in counts.items() if count==best]
    # A missing vote is an abstention, not an implicit skip vote.
    return winners[0] if len(winners)==1 else None
