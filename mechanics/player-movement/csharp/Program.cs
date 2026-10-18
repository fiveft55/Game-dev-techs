using System;
// Engine-independent: pass the simulation timestep in seconds.
class Program {
    public static (double x,double y) Move(double x,double y,double ix,double iy,double speed,double dt) {
        double scale=Math.Max(1,Math.Sqrt(ix*ix+iy*iy));
        return (x+ix/scale*speed*dt,y+iy/scale*speed*dt);
    }
    static void Main() {
        var p=Move(0,0,1,1,1,1);
        if(Math.Abs(p.x*p.x+p.y*p.y-1)>=1e-9) throw new Exception("movement failed");
    }
}
