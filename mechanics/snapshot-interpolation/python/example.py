def interpolate(older,newer,render_time):
    t0,p0=older; t1,p1=newer
    if t1<=t0 or len(p0)!=len(p1): raise ValueError("invalid snapshots")
    alpha=max(0.0,min(1.0,(render_time-t0)/(t1-t0)))
    return tuple(a+(b-a)*alpha for a,b in zip(p0,p1))
