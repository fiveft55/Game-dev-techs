"""Swept projectile versus rectangle. Original MIT-licensed educational implementation."""

def hit_fraction(start, end, rect):
    x, y, width, height = rect
    if width < 0 or height < 0:
        raise ValueError("negative rectangle dimensions")
    near, far = 0.0, 1.0
    for origin, finish, low, high in zip(start, end, (x,y), (x+width,y+height)):
        direction = finish-origin
        if direction == 0:
            if origin < low or origin > high:
                return None
            continue
        a, b = sorted(((low-origin)/direction, (high-origin)/direction))
        # Intersect the time intervals during which both coordinates are inside.
        near, far = max(near,a), min(far,b)
        if near > far:
            return None
    return near
