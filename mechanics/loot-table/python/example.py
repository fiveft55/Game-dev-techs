"""Weighted loot selection. Original MIT-licensed educational implementation."""

def choose(table, rng):
    table=list(table)
    if not table or any(type(weight) is not int or weight<=0 for _,weight in table):
        raise ValueError("positive integer weights required")
    ticket=rng.randrange(sum(weight for _,weight in table))
    for item,weight in table:
        if ticket<weight: return item
        ticket-=weight
    raise RuntimeError("generator returned an invalid ticket")
