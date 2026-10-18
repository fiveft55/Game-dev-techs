"""Persistent grid movement. All times are seconds; tiles are unit squares.

GridMover exposes a beginner-friendly named API. _advance is the independent
numeric state machine shared conceptually with the eight native implementations.
"""
from math import floor as floor_num, isfinite

# These tiny adapters let the numeric algorithm match the native port contract.
def get(values, index):
    """Read a value by its zero-based whole-number position."""
    return values[int(index)]

length = len
minimum = min
maximum = max
abs_num = abs


def _advance(data):
    """Advance one packed state update; leave the input untouched and return new state."""
    if length(data)<18:
        return [-1]
    w=get(data,0)
    h=get(data,1)
    step_seconds=get(data,2)
    repeat_delay=get(data,3)
    repeat_interval=get(data,4)
    buffer_seconds=get(data,5)
    remaining=get(data,6)
    direction=get(data,7)
    tile_x=get(data,8)
    tile_y=get(data,9)
    target_x=get(data,10)
    target_y=get(data,11)
    progress=get(data,12)
    buffered=get(data,13)
    held=get(data,14)
    repeat_remaining=get(data,15)
    buffer_remaining=get(data,16)
    if w<1 or h<1 or floor_num(w)!=w or floor_num(h)!=h or length(data)!=17+w*h:
        return [-1]
    if step_seconds<0 or repeat_delay<0.01 or repeat_interval<0.01 or buffer_seconds<0 or remaining<0 or remaining>1:
        return [-1]
    if direction<0 or direction>4 or floor_num(direction)!=direction or held<0 or held>4 or floor_num(held)!=held or buffered<0 or buffered>4 or floor_num(buffered)!=buffered:
        return [-1]
    if tile_x<0 or tile_x>=w or tile_y<0 or tile_y>=h or target_x<0 or target_x>=w or target_y<0 or target_y>=h:
        return [-1]
    if floor_num(tile_x)!=tile_x or floor_num(tile_y)!=tile_y or floor_num(target_x)!=target_x or floor_num(target_y)!=target_y:
        return [-1]
    if progress<0 or progress>1 or repeat_remaining<0 or buffer_remaining<0 or abs_num(target_x-tile_x)+abs_num(target_y-tile_y)>1:
        return [-1]
    if (target_x==tile_x and target_y==tile_y and progress!=0) or get(data,17+tile_y*w+tile_x)!=0 or get(data,17+target_y*w+target_x)!=0:
        return [-1]
    # Instant mode cannot resume a previously unfinished smooth step.
    if step_seconds==0 and (target_x!=tile_x or target_y!=tile_y):
        return [-1]
    # A changed direction is a fresh press; a release stops repeating but keeps a live buffer.
    if direction!=held:
        held=direction
        repeat_remaining=0
        if direction!=0:
            repeat_remaining=repeat_delay
            buffered=direction
            buffer_remaining=buffer_seconds
    started=0
    arrived=0
    blocked=0
    # Process exact event boundaries so a long update does not skip repeats or overshoot tiles.
    while 1==1:
        if (target_x!=tile_x or target_y!=tile_y) and progress>=1-0.000000001:
            tile_x=target_x
            tile_y=target_y
            progress=0
            arrived+=1
        if held!=0 and repeat_remaining<=0.000000001:
            buffered=held
            buffer_remaining=buffer_seconds
            repeat_remaining+=repeat_interval
        if tile_x==target_x and tile_y==target_y and buffered!=0:
            nx=tile_x
            ny=tile_y
            if buffered==1:
                ny-=1
            if buffered==2:
                nx+=1
            if buffered==3:
                ny+=1
            if buffered==4:
                nx-=1
            # Consume each request once, including a blocked request.
            buffered=0
            buffer_remaining=0
            passable=0
            if nx>=0 and nx<w and ny>=0 and ny<h:
                if get(data,17+ny*w+nx)==0:
                    passable=1
            if passable==0:
                blocked=1
            else:
                target_x=nx
                target_y=ny
                started+=1
                if step_seconds==0:
                    tile_x=target_x
                    tile_y=target_y
                    arrived+=1
        if remaining<=0.000000001:
            break
        advance=remaining
        if held!=0:
            advance=minimum(advance,repeat_remaining)
        if tile_x!=target_x or tile_y!=target_y:
            advance=minimum(advance,(1-progress)*step_seconds)
            progress+=advance/step_seconds
        remaining=maximum(0,remaining-advance)
        if held!=0:
            repeat_remaining=maximum(0,repeat_remaining-advance)
        if buffered!=0:
            buffer_remaining-=advance
            # A buffer remains valid at its exact deadline, but expires strictly after it.
            if buffer_remaining < -0.000000001:
                buffered=0
                buffer_remaining=0
            else:
                buffer_remaining=maximum(0,buffer_remaining)
    visual_x=tile_x+(target_x-tile_x)*progress
    visual_y=tile_y+(target_y-tile_y)*progress
    return [tile_x,tile_y,target_x,target_y,progress,buffered,held,repeat_remaining,buffer_remaining,visual_x,visual_y,started,arrived,blocked]


class GridMover:
    """Walk one adjacent tile at a time; keep position and timers between updates."""

    DIRECTIONS = {None: 0, 'up': 1, 'right': 2, 'down': 3, 'left': 4}

    def __init__(self, grid, start=(0, 0), step_seconds=0.2,
                 repeat_delay=0.3, repeat_interval=0.1, buffer_seconds=0.15):
        """Copy a binary tile map and start on an unblocked integer tile."""
        rows = tuple(tuple(row) for row in grid)
        if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError('grid must be nonempty and rectangular')
        if any(type(tile) is not int or tile not in (0, 1) for row in rows for tile in row):
            raise ValueError('tiles must be integer zero (floor) or one (wall)')
        if len(start) != 2 or any(type(v) is not int for v in start):
            raise ValueError('start must contain two integer tile coordinates')
        x, y = start
        if not (0 <= y < len(rows) and 0 <= x < len(rows[0])) or rows[y][x] != 0:
            raise ValueError('start must be an unblocked tile inside the map')
        values = (step_seconds, repeat_delay, repeat_interval, buffer_seconds)
        if any(type(v) not in (int, float) or not isfinite(v) for v in values):
            raise ValueError('timing parameters must be finite numbers')
        if step_seconds < 0 or repeat_delay < .01 or repeat_interval < .01 or buffer_seconds < 0:
            raise ValueError('invalid timing parameters; repeat times must be >= 0.01')
        self._config = [len(rows[0]), len(rows), *values]
        self._grid = [tile for row in rows for tile in row]
        self._state = [x, y, x, y, 0, 0, 0, 0, 0]

    @property
    def tile(self):
        """The last square fully reached, used for tile-based game rules."""
        return tuple(int(v) for v in self._state[:2])

    @property
    def target(self):
        """The reserved destination of the current step."""
        return tuple(int(v) for v in self._state[2:4])

    @property
    def position(self):
        """Drawing position: slide between the source and destination squares."""
        x, y, tx, ty, progress = self._state[:5]
        return x + (tx-x)*progress, y + (ty-y)*progress

    @property
    def moving(self):
        """Whether there is an unfinished tile step."""
        return self.tile != self.target

    def update(self, dt, direction=None):
        """Apply the held direction at interval start, then advance by dt seconds."""
        if type(dt) not in (int, float) or not isfinite(dt) or not 0 <= dt <= 1:
            raise ValueError('dt must be a finite number between zero and one second')
        if direction is not None and (not isinstance(direction, str) or direction not in self.DIRECTIONS):
            raise ValueError('direction must be up, right, down, left or None')
        result = _advance([*self._config, dt, self.DIRECTIONS[direction], *self._state, *self._grid])
        if result == [-1]:
            raise ValueError('invalid controller state')
        self._state = result[:9]
        return {'position': self.position, 'tile': self.tile,
                'started': int(result[11]), 'arrived': int(result[12]),
                'blocked': bool(result[13])}
