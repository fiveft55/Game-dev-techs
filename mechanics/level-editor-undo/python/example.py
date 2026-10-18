class Editor:
    def __init__(self,width,height):
        if width<=0 or height<=0: raise ValueError("invalid dimensions")
        self.grid=[[0]*width for _ in range(height)]
        self.past=[]; self.future=[]
    def paint(self,x,y,value):
        if not (0<=y<len(self.grid) and 0<=x<len(self.grid[0])):
            raise ValueError("outside grid")
        self.past.append((x,y,self.grid[y][x],value))
        self.grid[y][x]=value; self.future.clear()
    def undo(self):
        if not self.past: return False
        x,y,old,new=self.past.pop(); self.grid[y][x]=old
        self.future.append((x,y,old,new)); return True
    def redo(self):
        if not self.future: return False
        x,y,old,new=self.future.pop(); self.grid[y][x]=new
        self.past.append((x,y,old,new)); return True
