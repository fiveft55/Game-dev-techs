"""Batch crafting recipes. Original MIT-licensed educational implementation."""

def craft(inventory, ingredients, products, batches=1):
    if type(batches) is not int or batches <= 0 or not ingredients or not products:
        raise ValueError("nonempty recipe and positive batches required")
    if any(type(v) is not int or v < 0 for v in inventory.values()): raise ValueError("invalid inventory")
    if any(type(v) is not int or v <= 0 for data in (ingredients,products) for v in data.values()):
        raise ValueError("recipe quantities must be positive integers")
    cost={key:value*batches for key,value in ingredients.items()}
    if any(inventory.get(key,0)<value for key,value in cost.items()): return None
    result=dict(inventory)
    for key,value in cost.items(): result[key]=result.get(key,0)-value
    for key,value in products.items(): result[key]=result.get(key,0)+value*batches
    return result
