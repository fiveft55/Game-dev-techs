from math import hypot

def move(x, y, ix, iy, speed, dt):
    if speed < 0 or dt < 0:
        raise ValueError("speed and dt must be nonnegative")
    # Inputs smaller than one retain analog-stick magnitude.
    scale = max(1.0, hypot(ix, iy))
    return x + ix / scale * speed * dt, y + iy / scale * speed * dt
