from math import exp

def follow(current,target,rate,dt):
    if rate<0 or dt<0: raise ValueError("negative rate or dt")
    # Exact solution of first-order decay toward a constant target.
    alpha=1-exp(-rate*dt)
    return current+(target-current)*alpha
