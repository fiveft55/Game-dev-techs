"""Original language-neutral numeric kernels and hand-authored behavioral fixtures.

The small generator translates these restricted Python function bodies into native
C, C#, Lua, GDScript, JS, and TS. Generated files do not depend on Python.
Input/output layouts are part of the documented portable API, not the legacy API.
"""
SPECS = {}


def define(slug, inputs, outputs, notes, body, cases):
    import textwrap
    SPECS[slug] = dict(inputs=inputs, outputs=outputs, notes=notes,
                       body=textwrap.dedent(body).strip(), cases=cases)


define('fixed-timestep', '[accumulator, elapsed, step, max_elapsed]', '[steps, remainder]',
       'Seconds. Negative clock values or nonpositive step return [-1]. Excess elapsed time is deliberately dropped.', '''
a = get(data, 0)
elapsed = get(data, 1)
step = get(data, 2)
cap = get(data, 3)
if a < 0 or elapsed < 0 or step <= 0 or cap < 0:
    return [-1]
a = a + minimum(elapsed, cap)
steps = floor_num((a + 0.000000000001) / step)
return [steps, maximum(0, a - steps * step)]
''', [([0,.05,.02,.25],[2,.01]), ([0,1,.1,.2],[2,0]), ([0,1,0,.2],[-1])])
define('player-movement', '[x, y, input_x, input_y, speed, dt]', '[new_x, new_y]',
       'World units and seconds. Preserve analog magnitude below one; normalize diagonal input.', '''
x = get(data, 0)
y = get(data, 1)
ix = get(data, 2)
iy = get(data, 3)
speed = get(data, 4)
dt = get(data, 5)
if speed < 0 or dt < 0:
    return [-1]
scale = maximum(1, sqrt_num(ix * ix + iy * iy))
return [x + ix / scale * speed * dt, y + iy / scale * speed * dt]
''', [([0,0,1,0,4,.5],[2,0]),([0,0,1,1,1,1],[.7071067811865476,.7071067811865476]),([0,0,.5,0,4,1],[2,0])])
define('aabb-collision', '[ax, ay, aw, ah, bx, by, bw, bh]', '[contact: 0 or 1]',
       'Touching edges count as contact. Negative dimensions return [-1].', '''
ax=get(data,0)
ay=get(data,1)
aw=get(data,2)
ah=get(data,3)
bx=get(data,4)
by=get(data,5)
bw=get(data,6)
bh=get(data,7)
if aw<0 or ah<0 or bw<0 or bh<0:
    return [-1]
if ax<=bx+bw and bx<=ax+aw and ay<=by+bh and by<=ay+ah:
    return [1]
return [0]
''', [([0,0,1,1,1,0,1,1],[1]),([0,0,1,1,2,2,1,1],[0]),([0,0,-1,1,0,0,1,1],[-1])])
define('grid-pathfinding', '[width, height, start_cell, goal_cell, ...row_major_grid]', '[...path_cell_ids] or [] if unreachable',
       'Cell ID is y*width+x; zero tiles are walkable. BFS with equal-cost four-neighbor movement.', '''
w=get(data,0)
h=get(data,1)
start=get(data,2)
goal=get(data,3)
n=w*h
if w<1 or h<1 or start<0 or goal<0 or start>=n or goal>=n or length(data)!=n+4:
    return []
if get(data,4+start)!=0 or get(data,4+goal)!=0:
    return []
parent=[]
queue=[start]
for i in range(0,n):
    push(parent,-1)
put(parent,start,start)
head=0
while head<length(queue):
    cell=get(queue,head)
    head+=1
    if cell==goal:
        break
    x=cell-w*floor_num(cell/w)
    y=floor_num(cell/w)
    for direction in range(0,4):
        nx=x
        ny=y
        if direction==0:
            nx+=1
        if direction==1:
            nx-=1
        if direction==2:
            ny+=1
        if direction==3:
            ny-=1
        other=ny*w+nx
        if nx>=0 and nx<w and ny>=0 and ny<h:
            if get(parent,other)==-1 and get(data,4+other)==0:
                put(parent,other,cell)
                push(queue,other)
if get(parent,goal)==-1:
    return []
reverse=[]
cell=goal
while cell!=start:
    push(reverse,cell)
    cell=get(parent,cell)
push(reverse,start)
out=[]
i=length(reverse)-1
while i>=0:
    push(out,get(reverse,i))
    i-=1
return out
''', [([3,2,0,2,0,1,0,0,0,0],[0,3,4,5,2]),([3,1,0,2,0,1,0],[]),([1,1,0,0,0],[0])])
define('raycasting', '[width, height, ox, oy, dx, dy, limit, ...grid]', '[cell_x, cell_y, ray_parameter] or []',
       'Grid DDA; Y wins corner ties. Direction need not have unit length. Solid tiles are nonzero.', '''
w=get(data,0)
h=get(data,1)
ox=get(data,2)
oy=get(data,3)
dx=get(data,4)
dy=get(data,5)
limit=get(data,6)
if w<1 or h<1 or length(data)!=7+w*h or (dx==0 and dy==0):
    return []
x=floor_num(ox)
y=floor_num(oy)
sx=-1
sy=-1
if dx>0:
    sx=1
if dy>0:
    sy=1
# A large sentinel replaces infinity for this bounded educational ray.
tx=1e30
ty=1e30
stepx=1e30
stepy=1e30
if dx!=0:
    tx=(x-ox)/dx
    if dx>0:
        tx=(x+1-ox)/dx
    stepx=abs_num(1/dx)
if dy!=0:
    ty=(y-oy)/dy
    if dy>0:
        ty=(y+1-oy)/dy
    stepy=abs_num(1/dy)
t=0
for i in range(0,limit):
    if x<0 or x>=w or y<0 or y>=h:
        return []
    if get(data,7+y*w+x)!=0:
        return [x,y,t]
    if tx<ty:
        t=tx
        tx+=stepx
        x+=sx
    else:
        t=ty
        ty+=stepy
        y+=sy
return []
''', [([3,1,.5,.5,1,0,10,0,0,1],[2,0,1.5]),([1,1,.5,.5,1,0,10,0],[]),([1,1,.5,.5,0,0,10,1],[])])
define('rigid-body-integration', '[x, y, vx, vy, ax, ay, dt]', '[x, y, vx, vy]',
       '2D semi-implicit Euler point mass. Seconds and consistent world units; no contacts.', '''
x=get(data,0)
y=get(data,1)
vx=get(data,2)
vy=get(data,3)
ax=get(data,4)
ay=get(data,5)
dt=get(data,6)
if dt<0:
    return [-1]
vx+=ax*dt
vy+=ay*dt
return [x+vx*dt,y+vy*dt,vx,vy]
''', [([0,0,0,0,0,-10,.1],[0,-.1,0,-1]),([1,2,3,4,0,0,0],[1,2,3,4])])
define('steering-arrival', '[x, y, target_x, target_y, max_speed, slowing_radius]', '[desired_vx, desired_vy]',
       'Desired velocity only; acceleration limits belong to a separate controller.', '''
dx=get(data,2)-get(data,0)
dy=get(data,3)-get(data,1)
speed=get(data,4)
radius=get(data,5)
if speed<0 or radius<=0:
    return [-1]
distance=sqrt_num(dx*dx+dy*dy)
if distance==0:
    return [0,0]
scaled=speed*minimum(1,distance/radius)/distance
return [dx*scaled,dy*scaled]
''', [([0,0,1,0,10,5],[2,0]),([0,0,0,0,10,5],[0,0]),([0,0,10,0,4,5],[4,0])])
define('finite-state-machine', '[initial_state, transition_count, ...[from,event,to], ...events]', '[final_state, accepted_count]',
       'Integer state/event IDs. First matching transition wins. Unknown events are ignored.', '''
state=get(data,0)
count=get(data,1)
offset=2+count*3
accepted=0
for i in range(offset,length(data)):
    event=get(data,i)
    for j in range(0,count):
        base=2+j*3
        if get(data,base)==state and get(data,base+1)==event:
            state=get(data,base+2)
            accepted+=1
            break
return [state,accepted]
''', [([0,2,0,7,1,1,8,0,99,7,8],[0,2]),([2,0,8],[2,0])])
define('inventory', '[item_id, amount, stack_cap, slot_limit, ...[item_id,count]]', '[overflow, ...[item_id,count]]',
       'Numeric item IDs. Existing positive stack counts must not exceed the cap. Preserve stack order.', '''
item=get(data,0)
amount=get(data,1)
cap=get(data,2)
slots=get(data,3)
if amount<0 or cap<=0 or slots<0 or mod_num(length(data)-4,2)!=0 or (length(data)-4)/2>slots:
    return [-1]
out=[0]
for i in range(4,length(data),2):
    kind=get(data,i)
    count=get(data,i+1)
    if count<=0 or count>cap:
        return [-1]
    if kind==item:
        taken=minimum(cap-count,amount)
        count+=taken
        amount-=taken
    push(out,kind)
    push(out,count)
while amount>0 and (length(out)-1)/2<slots:
    taken=minimum(cap,amount)
    push(out,item)
    push(out,taken)
    amount-=taken
put(out,0,amount)
return out
''', [([1,10,64,2,1,60],[0,1,64,1,6]),([1,70,64,1],[6,1,64]),([1,2,64,1,1,65],[-1])])
define('ascii-world', '[width, height, player_cell_or_minus_one, ...grid]', '[...ASCII_character_codes]',
       'Zero tiles render dot (46); one tiles render # (35); player renders @ (64); newline is 10. Decode codes with your engine UI.', '''
w=get(data,0)
h=get(data,1)
player=get(data,2)
if w<1 or h<1 or length(data)!=3+w*h:
    return [-1]
out=[]
for y in range(0,h):
    for x in range(0,w):
        cell=y*w+x
        tile=get(data,3+cell)
        if tile!=0 and tile!=1:
            return [-1]
        symbol=46
        if tile==1:
            symbol=35
        if cell==player:
            symbol=64
        push(out,symbol)
    if y<h-1:
        push(out,10)
return out
''', [([3,2,4,1,1,1,1,0,1],[35,35,35,10,35,64,35]),([1,1,-1,0],[46])])
define('procedural-maze', '[odd_width, odd_height, uint32_seed]', '[...row_major_grid]',
       'Iterative randomized depth-first carving. Portable LCG (not cryptographic) gives the same map across these six languages; it differs from Python random.Random.', '''
w=get(data,0)
h=get(data,1)
seed=get(data,2)
if w<3 or h<3 or mod_num(w,2)!=1 or mod_num(h,2)!=1 or seed<0 or seed>=4294967296:
    return [-1]
grid=[]
stack=[w+1]
for i in range(0,w*h):
    push(grid,1)
put(grid,w+1,0)
while length(stack)>0:
    cell=get(stack,length(stack)-1)
    x=mod_num(cell,w)
    y=floor_num(cell/w)
    options=[]
    for direction in range(0,4):
        nx=x
        ny=y
        if direction==0:
            nx+=2
        if direction==1:
            nx-=2
        if direction==2:
            ny+=2
        if direction==3:
            ny-=2
        if nx>0 and nx<w-1 and ny>0 and ny<h-1:
            if get(grid,ny*w+nx)==1:
                push(options,ny*w+nx)
    if length(options)==0:
        pop_value(stack)
    else:
        seed=mod_num(seed*1664525+1013904223,4294967296)
        chosen=get(options,mod_num(seed,length(options)))
        nx=mod_num(chosen,w)
        ny=floor_num(chosen/w)
        put(grid,((y+ny)/2)*w+(x+nx)/2,0)
        put(grid,chosen,0)
        push(stack,chosen)
return grid
''', [([3,3,0],[1,1,1,1,0,1,1,1,1]),([5,3,0],[1,1,1,1,1,1,0,0,0,1,1,1,1,1,1]),([4,3,0],[-1])])
define('camera-follow', '[current, target, rate, dt]', '[new_position]',
       'Exact first-order exponential smoothing toward a stationary scalar target; apply per axis.', '''
current=get(data,0)
target=get(data,1)
rate=get(data,2)
dt=get(data,3)
if rate<0 or dt<0:
    return [-1]
alpha=1-exp_num(-rate*dt)
return [current+(target-current)*alpha]
''', [([0,10,3,0],[0]),([0,10,1,1],[6.321205588285577]),([2,10,0,1],[2])])
define('spatial-hash', '[cell_size, query_x, query_y, ...[id,x,y]]', '[...candidate_ids_in_input_order]',
       'Build point-cell coordinates and query a 3x3 neighborhood. Flat buckets are scanned here for clarity; unlike the Python dictionary, this reference is O(n) per query.', '''
size=get(data,0)
if size<=0:
    return [-1]
qx=floor_num(get(data,1)/size)
qy=floor_num(get(data,2)/size)
out=[]
for i in range(3,length(data),3):
    cx=floor_num(get(data,i+1)/size)
    cy=floor_num(get(data,i+2)/size)
    if abs_num(cx-qx)<=1 and abs_num(cy-qy)<=1:
        push(out,get(data,i))
return out
''', [([1,0,0,7,-.1,0,8,10,10],[7]),([2,0,0,1,2,2,2,4,0],[1]),([0,0,0],[-1])])
define('racing-bicycle-model', '[x,y,heading,speed,steering,wheelbase,dt]', '[new_x,new_y,new_heading]',
       'Radians and seconds. Kinematic no-slip low-speed model; steering magnitude must be below pi/2.', '''
x=get(data,0)
y=get(data,1)
heading=get(data,2)
speed=get(data,3)
steering=get(data,4)
base=get(data,5)
dt=get(data,6)
if base<=0 or dt<0 or abs_num(steering)>=1.5707963267948966:
    return [-1]
return [x+speed*cos_num(heading)*dt,y+speed*sin_num(heading)*dt,heading+speed/base*tan_num(steering)*dt]
''', [([0,0,0,10,0,2,.1],[1,0,0]),([0,0,0,10,.7853981633974483,2,.1],[1,0,.5]),([0,0,0,1,0,0,1],[-1])])
define('snapshot-interpolation', '[t0,x0,y0,t1,x1,y1,render_time]', '[x,y]',
       'Clamp interpolation outside the snapshot interval. Authenticate snapshots before this calculation.', '''
t0=get(data,0)
t1=get(data,3)
if t1<=t0:
    return [-1]
alpha=maximum(0,minimum(1,(get(data,6)-t0)/(t1-t0)))
return [get(data,1)+(get(data,4)-get(data,1))*alpha,get(data,2)+(get(data,5)-get(data,2))*alpha]
''', [([0,0,0,1,10,20,.5],[5,10]),([0,0,0,1,10,20,2],[10,20]),([1,0,0,1,10,20,1],[-1])])
define('replay-window', '[window_width, ...authenticated_sequence_numbers]', '[...accepted_flags]',
       'One session per call. Explicit bounded seen-list avoids language-specific 64-bit bitmask behavior. Sequence numbers must be integers within the safe integer range. Authenticate before updating state.', '''
width=get(data,0)
if width<1:
    return [-1]
highest=-1
seen=[]
out=[]
for i in range(1,length(data)):
    seq=get(data,i)
    accept=1
    if seq<0 or floor_num(seq)!=seq or seq>9007199254740991:
        accept=0
    if seq<=highest-width:
        accept=0
    for j in range(0,length(seen)):
        if get(seen,j)==seq:
            accept=0
    if accept==1:
        highest=maximum(highest,seq)
        kept=[]
        for j in range(0,length(seen)):
            if get(seen,j)>highest-width:
                push(kept,get(seen,j))
        push(kept,seq)
        seen=kept
    push(out,accept)
return out
''', [([4,5,3,3,1,1000000000],[1,1,0,0,1]),([2,0,1,0,2,1],[1,1,0,1,0])])
define('level-editor-undo', '[width,height,...[operation,cell,value]]', '[...final_grid]',
       'Operations: 0 paint, 1 undo, 2 redo. Cell ID is y*width+x. New paint discards the redo branch. Ignored unused cell/value fields must still be supplied.', '''
w=get(data,0)
h=get(data,1)
if w<1 or h<1:
    return [-1]
grid=[]
history=[]
cursor=0
for i in range(0,w*h):
    push(grid,0)
for i in range(2,length(data),3):
    operation=get(data,i)
    cell=get(data,i+1)
    value=get(data,i+2)
    if operation==0:
        if cell<0 or cell>=w*h:
            return [-1]
        kept=[]
        for j in range(0,cursor*3):
            push(kept,get(history,j))
        history=kept
        push(history,cell)
        push(history,get(grid,cell))
        push(history,value)
        cursor+=1
        put(grid,cell,value)
    elif operation==1 and cursor>0:
        cursor-=1
        put(grid,get(history,cursor*3),get(history,cursor*3+1))
    elif operation==2 and cursor*3<length(history):
        put(grid,get(history,cursor*3),get(history,cursor*3+2))
        cursor+=1
return grid
''', [([2,1,0,0,5,1,0,0,2,0,0],[5,0]),([2,1,0,0,5,1,0,0,0,1,8,2,0,0],[0,8]),([1,1,0,3,9],[-1])])
define('cad-extrusion', '[height,...[profile_x,profile_y]]', '[vertex_count,triangle_count,...xyz_vertices,...triangle_indices]',
       'Convex simple counterclockwise profile, nonduplicate vertices. Same outward winding as the Python mesh. Not a robust CAD kernel.', '''
height=get(data,0)
n=(length(data)-1)/2
if height<=0 or n<3 or floor_num(n)!=n:
    return [-1]
out=[2*n,4*n-4]
for layer in range(0,2):
    for i in range(0,n):
        push(out,get(data,1+i*2))
        push(out,get(data,2+i*2))
        push(out,layer*height)
for i in range(1,n-1):
    push(out,0)
    push(out,i+1)
    push(out,i)
    push(out,n)
    push(out,n+i)
    push(out,n+i+1)
for i in range(0,n):
    j=mod_num(i+1,n)
    push(out,i)
    push(out,j)
    push(out,n+j)
    push(out,i)
    push(out,n+j)
    push(out,n+i)
return out
''', [([2,0,0,1,0,0,1],[6,8,0,0,0,1,0,0,0,1,0,0,0,2,1,0,2,0,1,2,0,2,1,3,4,5,0,1,4,0,4,3,1,2,5,1,5,4,2,0,3,2,3,5]),([0,0,0,1,0,0,1],[-1])])
define('score-lives', '[initial_lives, threshold, ...score_awards_or_minus_one_for_death]', '[points, lives]',
       'Integer nonnegative awards; -1 loses a life. Large awards can cross several extra-life thresholds.', '''
lives=get(data,0)
threshold=get(data,1)
if lives<0 or threshold<=0:
    return [-1]
points=0
for i in range(2,length(data)):
    award=get(data,i)
    if award==-1:
        lives=maximum(0,lives-1)
    elif award>=0:
        before=floor_num(points/threshold)
        points+=award
        lives+=floor_num(points/threshold)-before
    else:
        return [-1]
return [points,lives]
''', [([1,100,250,49,-1,-1,-1],[299,0]),([3,100,100],[100,4]),([1,100,-2],[-1])])
define('jump-controller', '[coyote_seconds, buffer_seconds, ...[time,grounded_flag,pressed_flag]]', '[...jump_flags]',
       'Monotonic finite timestamps. One consumed jump per grounded episode; collision reporting is the caller responsibility.', '''
coyote=get(data,0)
buffer=get(data,1)
if coyote<0 or buffer<0:
    return [-1]
last_ground=-1e30
last_press=-1e30
previous_time=-1e30
used=0
was_grounded=0
out=[]
for i in range(2,length(data),3):
    now=get(data,i)
    grounded=get(data,i+1)
    pressed=get(data,i+2)
    if now<previous_time:
        return [-1]
    previous_time=now
    if grounded==1:
        if was_grounded==0:
            used=0
        last_ground=now
    was_grounded=grounded
    if pressed==1:
        last_press=now
    jump=0
    if used==0 and now-last_ground<=coyote and now-last_press<=buffer:
        used=1
        last_press=-1e30
        jump=1
    push(out,jump)
return out
''', [([.1,.1,0,1,0,.05,0,1,.06,0,1],[0,1,0]),([.1,.1,0,0,1,.05,1,0],[0,1]),([.1,.1,1,0,0,0,0,0],[-1])])
define('projectile-sweep', '[start_x,start_y,end_x,end_y,rect_x,rect_y,width,height]', '[first_contact_fraction] or []',
       'Point projectile versus stationary rectangle; slab interval intersection detects tunneling. Inflate geometry separately for projectile volume.', '''
if get(data,6)<0 or get(data,7)<0:
    return [-1]
near=0
far=1
for axis in range(0,2):
    origin=get(data,axis)
    direction=get(data,axis+2)-origin
    low=get(data,axis+4)
    high=low+get(data,axis+6)
    if direction==0:
        if origin<low or origin>high:
            return []
    else:
        a=(low-origin)/direction
        b=(high-origin)/direction
        near=maximum(near,minimum(a,b))
        far=minimum(far,maximum(a,b))
        if near>far:
            return []
return [near]
''', [([0,0,10,0,4,-1,2,2],[.4]),([0,3,10,3,4,-1,2,2],[]),([5,0,5,0,4,-1,2,2],[0])])
define('combat-frames', '[startup,active,recovery,...[frame,target_id,overlap_flag]]', '[...hit_flags]',
       'At most one hit per numeric target ID per attack. Inputs use simulation frames; hitbox geometry is supplied by the caller.', '''
startup=get(data,0)
active=get(data,1)
recovery=get(data,2)
if startup<0 or active<=0 or recovery<0:
    return [-1]
hit=[]
out=[]
for i in range(3,length(data),3):
    frame=get(data,i)
    target=get(data,i+1)
    overlap=get(data,i+2)
    accepted=0
    if frame>=startup and frame<startup+active and overlap==1:
        accepted=1
        for j in range(0,length(hit)):
            if get(hit,j)==target:
                accepted=0
    if accepted==1:
        push(hit,target)
    push(out,accepted)
return out
''', [([2,2,3,1,7,1,2,7,1,3,7,1,3,8,1,4,9,1],[0,1,0,1,0]),([0,0,1],[-1])])
define('line-of-sight', '[width,height,start_x,start_y,goal_x,goal_y,...grid]', '[visible_flag]',
       'Integer tile centers; zero is transparent. Corner ties test both side cells to prevent diagonal wall leaks.', '''
w=get(data,0)
h=get(data,1)
x=get(data,2)
y=get(data,3)
gx=get(data,4)
gy=get(data,5)
if w<1 or h<1 or length(data)!=6+w*h:
    return [-1]
if x<0 or y<0 or gx<0 or gy<0 or x>=w or gx>=w or y>=h or gy>=h:
    return [0]
if get(data,6+y*w+x)!=0 or get(data,6+gy*w+gx)!=0:
    return [0]
nx=abs_num(gx-x)
ny=abs_num(gy-y)
sx=-1
sy=-1
if gx>x:
    sx=1
if gy>y:
    sy=1
ix=0
iy=0
while ix<nx or iy<ny:
    decision=(1+2*ix)*ny-(1+2*iy)*nx
    if decision==0:
        if get(data,6+y*w+x+sx)!=0 or get(data,6+(y+sy)*w+x)!=0:
            return [0]
        x+=sx
        y+=sy
        ix+=1
        iy+=1
    elif decision<0:
        x+=sx
        ix+=1
    else:
        y+=sy
        iy+=1
    if get(data,6+y*w+x)!=0:
        return [0]
return [1]
''', [([2,2,0,0,1,1,0,1,1,0],[0]),([2,2,1,1,0,0,0,0,0,0],[1]),([3,1,0,0,2,0,0,1,0],[0])])
define('rpg-progression', '[xp, attack, armor, ...strictly_increasing_level_thresholds]', '[level, damage]',
       'Thresholds begin at zero. Integer experience; damage is clamped attack minus armor.', '''
xp=get(data,0)
attack=get(data,1)
armor=get(data,2)
if xp<0 or attack<0 or armor<0 or length(data)<4 or get(data,3)!=0:
    return [-1]
level=0
last=-1
for i in range(3,length(data)):
    threshold=get(data,i)
    if threshold<=last:
        return [-1]
    last=threshold
    if xp>=threshold:
        level+=1
return [level,maximum(0,attack-armor)]
''', [([100,10,2,0,100,300],[2,8]),([99,10,12,0,100,300],[1,0]),([5,10,2,0,100,50],[-1])])
define('quest-objectives', '[objective_count,...target_counts,...[objective_index,amount]]', '[complete_flag,claim_flag,...progress]',
       'Progress clamps to target; unknown indices are ignored. One final claim per batch; persistence and atomic reward payout remain application concerns.', '''
n=get(data,0)
if n<1 or length(data)<1+n:
    return [-1]
progress=[]
for i in range(0,n):
    if get(data,1+i)<=0:
        return [-1]
    push(progress,0)
for i in range(1+n,length(data),2):
    index=get(data,i)
    amount=get(data,i+1)
    if amount<0:
        return [-1]
    if index>=0 and index<n:
        put(progress,index,minimum(get(data,1+index),get(progress,index)+amount))
complete=1
for i in range(0,n):
    if get(progress,i)<get(data,1+i):
        complete=0
out=[complete,complete]
for i in range(0,n):
    push(out,get(progress,i))
return out
''', [([2,2,1,0,99,1,1],[1,1,2,1]),([2,2,1,0,1],[0,0,1,0]),([1,2,0,-1],[-1])])
define('dialogue-graph', '[initial_node,initial_flag_mask,choice_count,...[from,event,to,requires_mask,grant_mask],...events]', '[final_node,flag_mask,accepted_choices]',
       'Numeric node/event IDs; flags use bit values 1,2,4,... up to 2^30. Event IDs select choices rather than UI list indices; first available match wins. Text/localization is separate.', '''
node=get(data,0)
flags=get(data,1)
n=get(data,2)
accepted=0
for i in range(3+n*5,length(data)):
    event=get(data,i)
    for j in range(0,n):
        base=3+j*5
        if get(data,base)==node and get(data,base+1)==event:
            requires=get(data,base+3)
            allowed=1
            power=1
            while power<=requires:
                if mod_num(floor_num(requires/power),2)==1 and mod_num(floor_num(flags/power),2)==0:
                    allowed=0
                power*=2
            if allowed==1:
                grants=get(data,base+4)
                power=1
                while power<=grants:
                    if mod_num(floor_num(grants/power),2)==1 and mod_num(floor_num(flags/power),2)==0:
                        flags+=power
                    power*=2
                node=get(data,base+2)
                accepted+=1
                break
return [node,flags,accepted]
''', [([0,0,2,0,1,0,0,1,0,2,1,1,0,2,1,2],[1,1,2]),([0,0,1,0,2,1,1,0,2],[0,0,0])])
define('turn-order', '[actor_count,...[id,initiative],...commands]', '[current_id_or_minus_one,...remaining_order]',
       'Numeric unique actor IDs >=0. Command -1 advances; a nonnegative command removes that actor. Higher initiative first, lower ID breaks ties.', '''
n=get(data,0)
if n<1:
    return [-1]
order=[]
scores=[]
for i in range(0,n):
    identifier=get(data,1+i*2)
    score=get(data,2+i*2)
    position=length(order)
    push(order,identifier)
    push(scores,score)
    while position>0:
        previous_score=get(scores,position-1)
        previous_id=get(order,position-1)
        if previous_score>score or (previous_score==score and previous_id<identifier):
            break
        put(scores,position,previous_score)
        put(order,position,previous_id)
        position-=1
    put(order,position,identifier)
    put(scores,position,score)
index=0
for i in range(1+n*2,length(data)):
    command=get(data,i)
    if length(order)>0:
        if command==-1:
            index=mod_num(index+1,length(order))
        else:
            kept=[]
            for j in range(0,length(order)):
                if get(order,j)==command:
                    if j<index:
                        index-=1
                else:
                    push(kept,get(order,j))
            order=kept
            if length(order)>0:
                index=mod_num(index,length(order))
            else:
                index=0
current=-1
if length(order)>0:
    current=get(order,index)
out=[current]
for i in range(0,length(order)):
    push(out,get(order,i))
return out
''', [([3,2,10,1,10,3,1,-1,1],[2,2,3]),([1,7,1,7],[-1]),([2,2,10,1,10],[1,1,2])])
define('resource-economy', '[resource_count,...balances,...costs,...outputs]', '[success_flag,...resulting_balances]',
       'Fixed resource indices replace dictionary keys. Integer resources; a failed purchase returns unchanged balances.', '''
n=get(data,0)
if n<1 or length(data)!=1+3*n:
    return [-1]
success=1
for i in range(0,n):
    balance=get(data,1+i)
    cost=get(data,1+n+i)
    output=get(data,1+2*n+i)
    if balance<0 or cost<0 or output<0:
        return [-1]
    if balance<cost:
        success=0
out=[success]
for i in range(0,n):
    balance=get(data,1+i)
    if success==1:
        balance+=get(data,1+2*n+i)-get(data,1+n+i)
    push(out,balance)
return out
''', [([2,5,0,3,0,0,2],[1,2,2]),([1,5,6,0],[0,5]),([1,5,-1,0],[-1])])
define('fog-of-war', '[width,height,radius,observer_count,...[x,y],...previous_explored_flags]', '[...visible_flags,...explored_flags]',
       'Radius-only 2D visibility bookkeeping; these portable kernels do not embed a caller line-of-sight callback. Compose visibility masks separately for walls.', '''
w=get(data,0)
h=get(data,1)
radius=get(data,2)
n=get(data,3)
offset=4+2*n
if w<1 or h<1 or radius<0 or n<0 or length(data)!=offset+w*h:
    return [-1]
visible=[]
explored=[]
for y in range(0,h):
    for x in range(0,w):
        seen=0
        for i in range(0,n):
            dx=x-get(data,4+2*i)
            dy=y-get(data,5+2*i)
            if dx*dx+dy*dy<=radius*radius:
                seen=1
        push(visible,seen)
        push(explored,maximum(seen,get(data,offset+y*w+x)))
for i in range(0,length(explored)):
    push(visible,get(explored,i))
return visible
''', [([3,1,1,1,0,0,0,0,1],[1,1,0,1,1,1]),([2,1,0,0,1,0],[0,0,1,0])])
define('wave-spawner', '[spawn_count,...[time,id],...monotonic_update_times]', '[...spawned_ids]',
       'Input schedule must already be sorted; simultaneous events preserve input order. All due events emitted once even after long frames.', '''
n=get(data,0)
if n<0 or length(data)<1+2*n:
    return [-1]
last=0
for i in range(0,n):
    at=get(data,1+2*i)
    if at<last:
        return [-1]
    last=at
index=0
last=0
out=[]
for i in range(1+2*n,length(data)):
    now=get(data,i)
    if now<last:
        return [-1]
    last=now
    while index<n and get(data,1+2*index)<=now:
        push(out,get(data,2+2*index))
        index+=1
return out
''', [([3,1,7,1,8,3,9,0,2,2,4],[7,8,9]),([1,2,7,1],[]),([1,2,7,2,1],[-1])])
define('event-scheduler', '[target_time,...[event_time,event_id]]', '[...due_event_ids_sorted_by_time]',
       'Schedule supplied as a batch; stable insertion sort preserves simultaneous event order. Unlike the heap-based Python service, this pure kernel has no incremental scheduling API.', '''
target=get(data,0)
if target<0:
    return [-1]
times=[]
ids=[]
for i in range(1,length(data),2):
    at=get(data,i)
    identifier=get(data,i+1)
    if at<0:
        return [-1]
    position=length(times)
    push(times,at)
    push(ids,identifier)
    while position>0 and get(times,position-1)>at:
        put(times,position,get(times,position-1))
        put(ids,position,get(ids,position-1))
        position-=1
    put(times,position,at)
    put(ids,position,identifier)
out=[]
for i in range(0,length(times)):
    if get(times,i)<=target:
        push(out,get(ids,i))
return out
''', [([2,2,7,2,8,1,9,3,10],[9,7,8]),([0,1,7],[]),([2,-1,7],[-1])])
define('racing-checkpoints', '[checkpoint_count,target_laps,...[enter_flag,checkpoint_id]]', '[laps,next_checkpoint,finished_flag]',
       'Enter=1, exit=0. Enter overlap can only count once until exit. Checkpoint order is 0..count-1.', '''
n=get(data,0)
target=get(data,1)
if n<1 or target<1:
    return [-1]
inside=[]
for i in range(0,n):
    push(inside,0)
laps=0
next_checkpoint=0
for i in range(2,length(data),2):
    entering=get(data,i)
    checkpoint=get(data,i+1)
    if checkpoint<0 or checkpoint>=n:
        return [-1]
    if entering==0:
        put(inside,checkpoint,0)
    elif get(inside,checkpoint)==0:
        put(inside,checkpoint,1)
        if laps<target and checkpoint==next_checkpoint:
            next_checkpoint+=1
            if next_checkpoint==n:
                laps+=1
                next_checkpoint=0
finished=0
if laps>=target:
    finished=1
return [laps,next_checkpoint,finished]
''', [([2,1,1,1,0,1,1,0,1,0,0,0,1,1],[1,0,1]),([1,2,1,0,1,0],[1,0,0]),([1,1,1,4],[-1])])
define('ball-reflection', '[vx,vy,normal_x,normal_y,restitution]', '[new_vx,new_vy]',
       'Normalize the surface normal; reflect only approaching velocity. Restitution in [0,1], no friction or spin.', '''
vx=get(data,0)
vy=get(data,1)
nx=get(data,2)
ny=get(data,3)
e=get(data,4)
size=sqrt_num(nx*nx+ny*ny)
if size==0 or e<0 or e>1:
    return [-1]
nx/=size
ny/=size
incoming=vx*nx+vy*ny
if incoming>=0:
    return [vx,vy]
impulse=(1+e)*incoming
return [vx-impulse*nx,vy-impulse*ny]
''', [([2,-3,0,2,1],[2,3]),([2,-3,0,1,.5],[2,1.5]),([2,3,0,1,1],[2,3]),([1,1,0,0,1],[-1])])
define('match-grid', '[width,height,minimum_run,...tiles]', '[matched_count,...collapsed_tiles]',
       'Tile -1 is empty. Detect horizontal/vertical matches, merge intersections, then apply column gravity. No random refill or cascade.', '''
w=get(data,0)
h=get(data,1)
minimum_run=get(data,2)
if w<1 or h<1 or minimum_run<2 or length(data)!=3+w*h:
    return [-1]
matched=[]
for i in range(0,w*h):
    push(matched,0)
for axis in range(0,2):
    lines=h
    span=w
    if axis==1:
        lines=w
        span=h
    for line in range(0,lines):
        start=0
        while start<span:
            cell=line*w+start
            stride=1
            if axis==1:
                cell=start*w+line
                stride=w
            tile=get(data,3+cell)
            end=start+1
            while end<span and get(data,3+cell+(end-start)*stride)==tile:
                end+=1
            if tile!=-1 and end-start>=minimum_run:
                for j in range(start,end):
                    put(matched,cell+(j-start)*stride,1)
            start=end
count=0
grid=[]
for i in range(0,w*h):
    count+=get(matched,i)
    push(grid,-1)
for x in range(0,w):
    bottom=h-1
    y=h-1
    while y>=0:
        cell=y*w+x
        if get(matched,cell)==0 and get(data,3+cell)!=-1:
            put(grid,bottom*w+x,get(data,3+cell))
            bottom-=1
        y-=1
out=[count]
for i in range(0,length(grid)):
    push(out,get(grid,i))
return out
''', [([3,3,3,1,2,3,1,1,1,1,2,3],[5,-1,-1,-1,-1,2,3,-1,2,3]),([3,1,3,-1,-1,-1],[0,-1,-1,-1])])
define('rhythm-judgement', '[note_time,perfect_window,good_window,latency,...recorded_press_times]', '[judgement_code]',
       '0 unhit, 1 perfect, 2 good. First in-window press consumes note; no expiry operation here (apply miss on audio-clock expiry in the caller).', '''
at=get(data,0)
perfect=get(data,1)
good=get(data,2)
latency=get(data,3)
if perfect<0 or good<perfect:
    return [-1]
for i in range(4,length(data)):
    error=abs_num(get(data,i)-latency-at)
    if error<=perfect:
        return [1]
    if error<=good:
        return [2]
return [0]
''', [([1,.03,.08,.1,.5,1.1],[1]),([1,.03,.08,0,1.05],[2]),([1,.03,.08,0,2],[0])])
define('crafting-recipes', '[resource_count,batches,...inventory,...ingredient_counts,...product_counts]', '[success_flag,...result_inventory]',
       'Fixed resource indices and nonnegative counts. At least one input and output; positive batches. Products cannot fund their own inputs. No inventory capacity/station constraints.', '''
n=get(data,0)
batches=get(data,1)
if n<1 or batches<1 or length(data)!=2+3*n:
    return [-1]
success=1
inputs=0
outputs=0
for i in range(0,n):
    inventory=get(data,2+i)
    cost=get(data,2+n+i)
    product=get(data,2+2*n+i)
    if inventory<0 or cost<0 or product<0:
        return [-1]
    inputs+=cost
    outputs+=product
    if inventory<cost*batches:
        success=0
if inputs==0 or outputs==0:
    return [-1]
out=[success]
for i in range(0,n):
    value=get(data,2+i)
    if success==1:
        value+=(get(data,2+2*n+i)-get(data,2+n+i))*batches
    push(out,value)
return out
''', [([2,2,5,0,2,0,0,3],[1,1,6]),([2,3,5,0,2,0,0,3],[0,5,0]),([1,1,0,1,2],[0,0])])
define('chunk-coordinates', '[world_x,world_y,chunk_size]', '[chunk_x,chunk_y,local_x,local_y]',
       'Integer world cells; floor division ensures negative cells map correctly. Join with chunk*size+local.', '''
x=get(data,0)
y=get(data,1)
size=get(data,2)
if size<1:
    return [-1]
cx=floor_num(x/size)
cy=floor_num(y/size)
return [cx,cy,x-cx*size,y-cy*size]
''', [([-1,-17,16],[-1,-2,15,15]),([16,0,16],[1,0,0,0]),([0,0,0],[-1])])
define('interest-management', '[observer_x,observer_y,radius,...[id,x,y,allowed_flag]]', '[...authorized_nearby_ids_sorted]',
       'Authorization must be decided by trusted server code. Nearby alone never grants access; no transport or field-level serializer included.', '''
ox=get(data,0)
oy=get(data,1)
radius=get(data,2)
if radius<0:
    return [-1]
out=[]
for i in range(3,length(data),4):
    dx=get(data,i+1)-ox
    dy=get(data,i+2)-oy
    if get(data,i+3)==1 and dx*dx+dy*dy<=radius*radius:
        identifier=get(data,i)
        position=length(out)
        push(out,identifier)
        while position>0 and get(out,position-1)>identifier:
            put(out,position,get(out,position-1))
            position-=1
        put(out,position,identifier)
return out
''', [([0,0,2,7,1,0,1,8,0,0,0,9,10,0,1],[7]),([0,0,0,8,0,0,1],[8]),([0,0,-1],[-1])])
define('shrinking-zone', '[start_x,start_y,end_x,end_y,start_radius,end_radius,started,duration,now,player_x,player_y,damage_rate,dt]', '[center_x,center_y,radius,damage]',
       'Linear center and radius interpolation, clamped to phase. Damage only outside; finite coordinates, seconds, nonnegative rate/dt.', '''
r0=get(data,4)
r1=get(data,5)
started=get(data,6)
duration=get(data,7)
now=get(data,8)
rate=get(data,11)
dt=get(data,12)
if duration<=0 or r1<0 or r1>r0 or rate<0 or dt<0:
    return [-1]
alpha=maximum(0,minimum(1,(now-started)/duration))
x=get(data,0)+(get(data,2)-get(data,0))*alpha
y=get(data,1)+(get(data,3)-get(data,1))*alpha
radius=r0+(r1-r0)*alpha
dx=get(data,9)-x
dy=get(data,10)-y
damage=0
if dx*dx+dy*dy>radius*radius:
    damage=rate*dt
return [x,y,radius,damage]
''', [([0,0,10,0,100,20,0,10,5,100,0,10,.5],[5,0,60,5]),([0,0,0,0,5,5,0,10,5,5,0,10,1],[0,0,5,0])])
define('ballot-resolution', '[candidate_count,voter_count,...candidate_ids,...eligible_voter_ids,...[voter_id,target_id]]', '[eliminated_id_or_minus_one]',
       'Unique nonnegative IDs; -1 is an explicit skip. Reject ineligible voters/targets and duplicate ballots. A plurality tie or skip win causes no elimination.', '''
n=get(data,0)
voters=get(data,1)
if n<0 or voters<0:
    return [-2]
counts=[]
for i in range(0,n+1):
    push(counts,0)
seen=[]
for i in range(2+n+voters,length(data),2):
    voter=get(data,i)
    target=get(data,i+1)
    eligible=0
    for j in range(0,voters):
        if get(data,2+n+j)==voter:
            eligible=1
    for j in range(0,length(seen)):
        if get(seen,j)==voter:
            eligible=0
    if eligible==0:
        return [-2]
    push(seen,voter)
    index=-1
    if target==-1:
        index=n
    for j in range(0,n):
        if get(data,2+j)==target:
            index=j
    if index<0:
        return [-2]
    put(counts,index,get(counts,index)+1)
best=0
winner=-1
tied=0
for i in range(0,n+1):
    count=get(counts,i)
    if count>best:
        best=count
        winner=i
        tied=0
    elif count==best:
        tied=1
if best==0 or tied==1 or winner==n:
    return [-1]
return [get(data,2+winner)]
''', [([2,3,1,2,1,2,3,1,2,2,2,3,-1],[2]),([2,2,1,2,1,2,1,2,2,1],[-1]),([1,1,1,1,9,1],[-2])])
define('deck-draw', '[uint32_seed,card_count,...card_ids,...operations]', '[...drawn_card_ids_or_minus_one]',
       'Operation -1 draws; nonnegative operation discards that card. Portable LCG Fisher-Yates; only server-owned decks can protect hidden cards. Not cryptographic or gambling-ready.', '''
seed=get(data,0)
n=get(data,1)
if seed<0 or seed>=4294967296 or n<0:
    return [-2]
pile=[]
discard=[]
for i in range(0,n):
    push(pile,get(data,2+i))
i=n-1
while i>0:
    seed=mod_num(seed*1664525+1013904223,4294967296)
    j=mod_num(seed,i+1)
    swap=get(pile,i)
    put(pile,i,get(pile,j))
    put(pile,j,swap)
    i-=1
out=[]
for operation_index in range(2+n,length(data)):
    operation=get(data,operation_index)
    if operation>=0:
        push(discard,operation)
    elif operation==-1:
        if length(pile)==0:
            pile=discard
            discard=[]
            i=length(pile)-1
            while i>0:
                seed=mod_num(seed*1664525+1013904223,4294967296)
                j=mod_num(seed,i+1)
                swap=get(pile,i)
                put(pile,i,get(pile,j))
                put(pile,j,swap)
                i-=1
        if length(pile)==0:
            push(out,-1)
        else:
            push(out,pop_value(pile))
    else:
        return [-2]
return out
''', [([0,1,7,-1,-1,7,-1],[7,-1,7]),([0,2,1,2,-1,-1],[2,1]),([0,0,-1],[-1])])
define('spaced-repetition', '[previous_days,correct_flag,now_seconds]', '[interval_days,next_due_seconds]',
       'Toy doubling/reset policy, not SM-2/FSRS or a validated learning intervention. Flags must be zero or one.', '''
previous=get(data,0)
correct=get(data,1)
now=get(data,2)
if previous<0 or (correct!=0 and correct!=1):
    return [-1]
days=1
if correct==1:
    days=maximum(1,previous*2)
return [days,now+days*86400]
''', [([0,1,100],[1,86500]),([4,1,0],[8,691200]),([8,0,0],[1,86400])])
define('offline-progress', '[rate,saved_at,now,cap_seconds]', '[produced]',
       'Binary64 arithmetic in these ports, unlike Python Decimal. Use integer fixed-point/server-ledger arithmetic for financial/economy precision. Client clocks remain untrusted.', '''
rate=get(data,0)
saved=get(data,1)
now=get(data,2)
cap=get(data,3)
if rate<0 or cap<0:
    return [-1]
elapsed=minimum(cap,maximum(0,now-saved))
return [rate*elapsed]
''', [([.1,0,3,28800],[.3]),([2,0,100,10],[20]),([2,100,0,10],[0]),([-1,0,1,10],[-1])])
define('save-migration', '[version,gold]', '[version_2,gold]',
       'Migration of an already decoded minimal save record; intentionally NOT a JSON parser or general inventory serializer. Engine serialization must validate keys, size, types and nonnegative integer counts before calling.', '''
version=get(data,0)
gold=get(data,1)
if (version!=1 and version!=2) or gold<0 or floor_num(gold)!=gold:
    return [-1]
return [2,gold]
''', [([1,4],[2,4]),([2,0],[2,0]),([3,0],[-1]),([2,-1],[-1])])
define('ability-cooldown', '[charge_count,duration,...attempt_times]', '[...accepted_flags]',
       'Each spent charge has its own parallel refill timer. Attempt times must be nonnegative and monotonic; equality at expiry permits reuse.', '''
capacity=get(data,0)
duration=get(data,1)
if capacity<1 or duration<=0:
    return [-1]
pending=[]
last=0
out=[]
for i in range(2,length(data)):
    now=get(data,i)
    if now<last:
        return [-1]
    last=now
    kept=[]
    for j in range(0,length(pending)):
        if get(pending,j)>now:
            push(kept,get(pending,j))
    pending=kept
    accepted=0
    if length(pending)<capacity:
        push(pending,now+duration)
        accepted=1
    push(out,accepted)
return out
''', [([2,3,0,1,2,3,4],[1,1,0,1,1]),([1,.5,0,.1,.5],[1,0,1]),([1,1,2,1],[-1])])
define('loot-table', '[ticket,...[item_id,positive_integer_weight]]', '[selected_item_id]',
       'Caller supplies a uniform integer ticket in [0,total_weight). This separates weighted selection from PRNG/security policy and permits exact boundary tests.', '''
ticket=get(data,0)
if ticket<0 or floor_num(ticket)!=ticket:
    return [-1]
total=0
for i in range(1,length(data),2):
    weight=get(data,i+1)
    if weight<=0 or floor_num(weight)!=weight:
        return [-1]
    total+=weight
if ticket>=total:
    return [-1]
for i in range(1,length(data),2):
    weight=get(data,i+1)
    if ticket<weight:
        return [get(data,i)]
    ticket-=weight
return [-1]
''', [([0,7,3,8,1],[7]),([2,7,3,8,1],[7]),([3,7,3,8,1],[8]),([4,7,3,8,1],[-1])])
define('rollback-resimulation', '[initial_state,correction_tick,authoritative_state,...integer_tick_inputs]', '[...corrected_state_history]',
       'Deterministic scalar integer movement. Tick zero is before any input. Demonstrates restore/replay without a dynamic callback, transport, bounded history, or side-effect dispatch.', '''
initial=get(data,0)
tick=get(data,1)
authority=get(data,2)
n=length(data)-3
if tick<0 or tick>n or floor_num(tick)!=tick:
    return [-1]
states=[initial]
state=initial
for i in range(0,n):
    state+=get(data,3+i)
    push(states,state)
put(states,tick,authority)
state=authority
for i in range(tick,n):
    state+=get(data,3+i)
    put(states,i+1,state)
return states
''', [([0,1,10,2,3,-1],[0,10,13,12]),([0,3,7,2,3,-1],[0,2,5,7]),([0,9,0,2],[-1])])
define('server-input-validation', '[speed,server_dt,...[sequence,dx,dy]]', '[x,y,last_sequence,...accepted_flags]',
       'Finite binary64 normalized input only, increasing integer sequence <=2^53-1. One command per server tick; caller must authenticate and rate-limit. No sockets, collision or encryption.', '''
speed=get(data,0)
dt=get(data,1)
if speed<0 or dt<=0:
    return [-1]
x=0
y=0
sequence=-1
out=[0,0,-1]
for i in range(2,length(data),3):
    seq=get(data,i)
    dx=get(data,i+1)
    dy=get(data,i+2)
    accepted=0
    if seq>sequence and seq<=9007199254740991 and floor_num(seq)==seq and dx*dx+dy*dy<=1:
        x+=dx*speed*dt
        y+=dy*speed*dt
        sequence=seq
        accepted=1
    push(out,accepted)
put(out,0,x)
put(out,1,y)
put(out,2,sequence)
return out
''', [([6,.5,0,1,0,0,1,0,1,2,0,2,0,1],[3,3,2,1,0,0,1]),([1,1,-1,0,0],[0,0,-1,0])])
define('animation-timeline', '[elapsed,loop_flag,frame_count,...durations]', '[frame_index]',
       'Positive frame durations in seconds; exact boundaries choose the next frame. No textures, skeletons, blending or event dispatch.', '''
elapsed=get(data,0)
loop=get(data,1)
n=get(data,2)
if elapsed<0 or n<1 or length(data)!=3+n:
    return [-1]
total=0
for i in range(0,n):
    duration=get(data,3+i)
    if duration<=0:
        return [-1]
    total+=duration
if loop==0 and elapsed>=total:
    return [n-1]
time=elapsed
if loop==1:
    time=mod_num(time,total)
end=0
for i in range(0,n):
    end+=get(data,3+i)
    if time<end:
        return [i]
return [n-1]
''', [([.25,1,2,.25,.75],[1]),([1,1,2,.25,.75],[0]),([2,0,2,.25,.75],[1]),([-1,1,1,1],[-1])])
define('building-placement', '[width,height,anchor_x,anchor_y,quarter_turns,footprint_count,...[dx,dy],...occupied_grid]', '[...new_occupied_grid] or [-1]',
       'Counterclockwise quarter turns in Y-up coordinates. Integer footprint offsets; out-of-bounds/occupied cells reject the whole placement before mutation.', '''
w=get(data,0)
h=get(data,1)
ax=get(data,2)
ay=get(data,3)
turns=mod_num(mod_num(get(data,4),4)+4,4)
n=get(data,5)
offset=6+2*n
if w<1 or h<1 or n<1 or length(data)!=offset+w*h:
    return [-1]
placements=[]
for i in range(0,n):
    x=get(data,6+2*i)
    y=get(data,7+2*i)
    for j in range(0,turns):
        previous_x=x
        x=-y
        y=previous_x
    x+=ax
    y+=ay
    if x<0 or x>=w or y<0 or y>=h:
        return [-1]
    cell=y*w+x
    if get(data,offset+cell)!=0:
        return [-1]
    push(placements,cell)
out=[]
for i in range(0,w*h):
    push(out,get(data,offset+i))
for i in range(0,length(placements)):
    put(out,get(placements,i),1)
return out
''', [([3,3,1,1,1,2,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,1,0]),([1,1,0,0,0,1,0,0,1],[-1]),([1,1,1,0,0,1,0,0,0],[-1])])
# Nontrivial seeded choices and multi-bit dialogue flags guard cross-runtime behavior.
SPECS['procedural-maze']['cases'].append(([5,5,0],[1,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,0,0,1,1,1,1,1,1]))
SPECS['deck-draw']['cases'].extend([
    ([1,2,1,2,-1,-1],[1,2]),
    ([0,3,1,2,3,-1,-1,-1],[2,1,3]),
])
SPECS['dialogue-graph']['cases'].append(([0,0,2,0,1,0,0,5,0,2,1,5,2,2,1,2],[1,7,2]))

define('grid-movement',
       '[width,height,step_seconds,repeat_delay,repeat_interval,buffer_seconds,dt,direction,...9_state_values,...row_major_grid]',
       '[...9_next_state_values,visual_x,visual_y,steps_started,tiles_arrived,blocked_flag]',
       'Persistent one-update controller. Directions 0=release,1=up,2=right,3=down,4=left (Y down). State: tile_x,tile_y,target_x,target_y,progress,buffered_direction,held_direction,repeat_remaining,buffer_remaining. Keep the first nine outputs for the next call. Zero tiles are walkable. dt is 0..1 seconds; repeat delay/interval >=0.01 seconds. See README for event ordering and static-map assumptions; [-1] means invalid configuration/state.', '''
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
''', [
    # Fresh instant step, fresh smooth half-step, boundary, wall, and held repeat.
    ([3,1,0,.3,.1,.15,0,2,0,0,0,0,0,0,0,0,0,0,0,0], [1,0,1,0,0,0,2,.3,0,1,0,1,1,0]),
    ([3,1,.2,.3,.1,.15,.1,2,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,1,0,.5,0,2,.2,0,.5,0,1,0,0]),
    ([3,1,0,.3,.1,.15,0,1,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,.3,0,0,0,0,0,1]),
    ([2,1,0,.3,.1,.15,0,2,0,0,0,0,0,0,0,0,0,0,1], [0,0,0,0,0,0,2,.3,0,0,0,0,0,1]),
    ([6,1,0,.3,.1,.15,.5,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [4,0,4,0,0,0,2,.1,0,4,0,4,4,0]),
    # Change direction in transit: wait for arrival, then take the buffered turn.
    ([2,2,.2,.3,.1,.15,.1,3,0,0,1,0,.5,0,2,.2,0,0,0,0,0], [1,0,1,1,0,0,3,.2,0,1,0,1,1,0]),
    # An early turn expires; a release stops repeat but preserves an unexpired turn.
    ([2,2,.2,.3,.1,.05,.1,3,0,0,1,0,.5,0,2,.2,0,0,0,0,0], [1,0,1,0,0,0,3,.2,0,1,0,0,1,0]),
    ([2,2,.2,.3,.1,.2,.1,0,0,0,1,0,.5,3,2,.3,.2,0,0,0,0], [1,0,1,1,0,0,0,0,0,1,0,1,1,0]),
    # Exact buffer deadline is valid. Invalid direction and excessive dt are rejected.
    ([2,2,.2,.3,.1,.1,.1,3,0,0,1,0,.5,0,2,.2,0,0,0,0,0], [1,0,1,1,0,0,3,.2,0,1,0,1,1,0]),
    ([1,1,.2,.3,.1,.15,0,5,0,0,0,0,0,0,0,0,0,0], [-1]),
    ([1,1,.2,.3,.1,.15,2,0,0,0,0,0,0,0,0,0,0,0], [-1]),
])

SPECS['grid-movement']['cases'].extend([
    ([3,3,0,.3,.1,.15,0,1,1,1,1,1,0,0,0,0,0,*([0]*9)], [1,0,1,0,0,0,1,.3,0,1,0,1,1,0]),
    ([3,3,0,.3,.1,.15,0,4,1,1,1,1,0,0,0,0,0,*([0]*9)], [0,1,0,1,0,0,4,.3,0,0,1,1,1,0]),
    ([2,1,0,.3,.1,.15,0,0,0,0,1,0,.5,0,0,0,0,0,0], [-1]),
    ([1,1,.2,.3,.1,.15,0,0,0,0,0,0,0,0,0,0,0,1], [-1]),
])
