from collections import deque

def path(grid, start, goal):
    height = len(grid)
    width = len(grid[0]) if height else 0
    if any(len(row) != width for row in grid):
        raise ValueError("ragged grid")
    def valid(p):
        x,y=p
        return 0<=x<width and 0<=y<height and grid[y][x] == 0
    if not valid(start) or not valid(goal): return []
    queue=deque([start]); parent={start: None}
    while queue:
        p=queue.popleft()
        if p == goal:
            result=[]
            while p is not None:
                result.append(p); p=parent[p]
            return result[::-1]
        x,y=p
        for q in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if valid(q) and q not in parent:
                # Mark on enqueue so each cell enters the queue once.
                parent[q]=p; queue.append(q)
    return []
