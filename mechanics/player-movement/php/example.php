<?php
// The simulation owns elapsed time; do not use request duration as game dt.
function movePlayer(float $x,float $y,float $ix,float $iy,float $speed,float $dt): array {
    $scale=max(1.0,hypot($ix,$iy));
    return [$x+$ix/$scale*$speed*$dt,$y+$iy/$scale*$speed*$dt];
}
[$x,$y]=movePlayer(0,0,1,1,1,1);
if (abs($x*$x+$y*$y-1)>=1e-9) { throw new RuntimeException('movement failed'); }
