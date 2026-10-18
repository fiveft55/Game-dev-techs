"""Capped idle-game offline production. Original MIT-licensed educational implementation."""

from decimal import Decimal

def production(rate, saved_at, now, cap_seconds=28800):
    rate,saved_at,now,cap_seconds=map(Decimal,map(str,(rate,saved_at,now,cap_seconds)))
    if not all(v.is_finite() for v in (rate,saved_at,now,cap_seconds)) or rate<0 or cap_seconds<0:
        raise ValueError("invalid offline parameters")
    elapsed=min(cap_seconds,max(Decimal(0),now-saved_at))
    return rate*elapsed
