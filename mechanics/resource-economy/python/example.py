"""Atomic resource purchase. Original MIT-licensed educational implementation."""

def transact(balance, cost, output=None):
    output={} if output is None else output
    if any(type(v) is not int or v < 0 for data in (balance,cost,output) for v in data.values()):
        raise ValueError("resources must be nonnegative integers")
    if any(balance.get(key,0) < value for key,value in cost.items()):
        return None
    result=dict(balance)
    # Validate affordability before producing any side effect.
    for key,value in cost.items(): result[key]=result.get(key,0)-value
    for key,value in output.items(): result[key]=result.get(key,0)+value
    return result
