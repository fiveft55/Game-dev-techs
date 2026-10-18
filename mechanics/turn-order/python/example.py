"""Deterministic initiative order. Original MIT-licensed educational implementation."""

class Turns:
    def __init__(self, initiative):
        if not initiative or any(not isinstance(k,str) for k in initiative):
            raise ValueError("nonempty mapping with string IDs required")
        self.order=sorted(initiative,key=lambda key:(-initiative[key],key))
        self.index=0

    @property
    def current(self):
        return self.order[self.index] if self.order else None

    def advance(self):
        if self.order: self.index=(self.index+1)%len(self.order)
        return self.current

    def remove(self, actor):
        if actor not in self.order: return False
        removed=self.order.index(actor)
        self.order.pop(removed)
        if removed < self.index: self.index-=1
        # Removing the current actor leaves its successor at the same index.
        self.index=self.index%len(self.order) if self.order else 0
        return True
