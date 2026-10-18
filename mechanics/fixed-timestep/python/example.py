def advance(accumulator, elapsed, step=1/60, max_elapsed=0.25):
    if step <= 0 or elapsed < 0 or accumulator < 0 or max_elapsed < 0:
        raise ValueError("invalid clock")
    # Keep fractional leftover time for interpolation between simulation states.
    accumulator += min(elapsed, max_elapsed)
    count = int((accumulator + 1e-12) / step)
    return count, max(0.0, accumulator - count * step)
