"""Visible and explored fog of war. Original MIT-licensed educational implementation."""

class Fog:
    def __init__(self, width, height):
        if type(width) is not int or type(height) is not int or width<=0 or height<=0:
            raise ValueError("invalid dimensions")
        self.width,self.height=width,height
        self.visible=set(); self.explored=set()

    def update(self, observers, radius, can_see=None):
        if type(radius) is not int or radius < 0: raise ValueError("integer radius required")
        observers=list(observers)
        if any(type(v) is not int for p in observers for v in p):
            raise ValueError("integer observer cells required")
        visible=set()
        for ox,oy in observers:
            for y in range(max(0,oy-radius),min(self.height,oy+radius+1)):
                for x in range(max(0,ox-radius),min(self.width,ox+radius+1)):
                    if (x-ox)**2+(y-oy)**2 <= radius**2 and (can_see is None or can_see((ox,oy),(x,y))):
                        visible.add((x,y))
        self.visible=visible
        self.explored.update(visible)
        return set(visible)
