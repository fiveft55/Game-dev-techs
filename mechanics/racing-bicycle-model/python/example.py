from math import cos,sin,tan,pi

def drive(x,y,heading,speed,steering,wheelbase,dt):
    if wheelbase<=0 or dt<0 or abs(steering)>=pi/2:
        raise ValueError("invalid geometry or timestep")
    # Forward Euler is adequate for small timesteps; high speed needs substeps.
    return (x+speed*cos(heading)*dt,y+speed*sin(heading)*dt,
            heading+speed/wheelbase*tan(steering)*dt)
