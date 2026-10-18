#include <algorithm>
#include <cassert>
#include <cmath>
#include <utility>
// Return a new position; the caller owns state and collision handling.
std::pair<double,double> move(double x,double y,double ix,double iy,double speed,double dt) {
    auto scale=std::max(1.0,std::hypot(ix,iy));
    return {x+ix/scale*speed*dt,y+iy/scale*speed*dt};
}
int main() { auto [x,y]=move(0,0,1,1,1,1); assert(std::abs(x*x+y*y-1)<1e-9); }
