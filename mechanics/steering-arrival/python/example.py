from math import hypot

def desired_velocity(position, target, max_speed, radius):
    if radius<=0 or max_speed<0: raise ValueError("invalid tuning")
    dx=target[0]-position[0]; dy=target[1]-position[1]; distance=hypot(dx,dy)
    if distance==0: return (0.0,0.0)
    speed=max_speed*min(1.0,distance/radius)
    return dx/distance*speed,dy/distance*speed
