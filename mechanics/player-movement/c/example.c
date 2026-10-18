#include <assert.h>
#include <math.h>
/* Normalize only inputs longer than one; preserve analog input strength. */
void move(double *x,double *y,double ix,double iy,double speed,double dt) {
    double scale=fmax(1.0,hypot(ix,iy));
    *x+=ix/scale*speed*dt; *y+=iy/scale*speed*dt;
}
int main(void) { double x=0,y=0; move(&x,&y,1,1,1,1); assert(fabs(x*x+y*y-1)<1e-9); }
