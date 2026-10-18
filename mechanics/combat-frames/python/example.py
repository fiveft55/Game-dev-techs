"""Attack startup, active, and recovery frames. Original MIT-licensed educational implementation."""

class Attack:
    def __init__(self, startup, active, recovery):
        if any(type(n) is not int or n < 0 for n in (startup,active,recovery)) or active == 0:
            raise ValueError("invalid attack duration")
        self.startup, self.active, self.recovery = startup, active, recovery
        self.hit_targets = set()

    def phase(self, frame):
        if type(frame) is not int or frame < 0:
            raise ValueError("invalid frame")
        if frame < self.startup: return 'startup'
        if frame < self.startup+self.active: return 'active'
        if frame < self.startup+self.active+self.recovery: return 'recovery'
        return 'finished'

    def try_hit(self, frame, target, overlapping):
        if self.phase(frame) != 'active' or not overlapping or target in self.hit_targets:
            return False
        self.hit_targets.add(target)
        return True
