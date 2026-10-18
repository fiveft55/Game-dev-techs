def integrate(position, velocity, acceleration, dt):
    if dt < 0: raise ValueError("negative dt")
    if not len(position)==len(velocity)==len(acceleration):
        raise ValueError("dimension mismatch")
    # Updating velocity first is more stable for many game systems than explicit Euler.
    velocity=tuple(v+a*dt for v,a in zip(velocity,acceleration))
    position=tuple(p+v*dt for p,v in zip(position,velocity))
    return position,velocity
