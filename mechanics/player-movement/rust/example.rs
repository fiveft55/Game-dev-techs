// Keep ownership simple: return position, leaving world state to the caller.
fn move_player(p:(f64,f64), input:(f64,f64), speed:f64, dt:f64)->(f64,f64) {
    let scale=input.0.hypot(input.1).max(1.0);
    (p.0+input.0/scale*speed*dt,p.1+input.1/scale*speed*dt)
}
fn main() {
    let (x,y)=move_player((0.0,0.0),(1.0,1.0),1.0,1.0);
    assert!((x*x+y*y-1.0).abs()<1e-9);
}
