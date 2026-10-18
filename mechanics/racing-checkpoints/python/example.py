"""Ordered checkpoints and lap counting. Original MIT-licensed educational implementation."""

class Race:
    def __init__(self, checkpoints, laps):
        if type(checkpoints) is not int or checkpoints<=0 or type(laps) is not int or laps<=0:
            raise ValueError("positive counts required")
        self.count=checkpoints; self.target=laps
        self.next=0; self.laps=0; self.inside=set()

    @property
    def finished(self): return self.laps >= self.target

    def enter(self, checkpoint):
        if type(checkpoint) is not int or not 0 <= checkpoint < self.count:
            raise ValueError("unknown checkpoint")
        if checkpoint in self.inside: return False
        self.inside.add(checkpoint)
        if self.finished or checkpoint != self.next: return False
        self.next+=1
        if self.next == self.count:
            self.next=0; self.laps+=1
        return True

    def exit(self, checkpoint): self.inside.discard(checkpoint)
