def add(stacks, item, amount, cap=64, slots=10):
    if amount<0 or cap<=0 or slots<0: raise ValueError("invalid capacity")
    if len(stacks)>slots or any(n<=0 or n>cap for _,n in stacks):
        raise ValueError("invalid existing stacks")
    result=list(stacks)
    for i,(kind,n) in enumerate(result):
        if kind==item:
            taken=min(cap-n,amount); result[i]=(kind,n+taken); amount-=taken
    while amount and len(result)<slots:
        taken=min(cap,amount); result.append((item,taken)); amount-=taken
    return result,amount
