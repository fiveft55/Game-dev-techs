"""Buffered jump and coyote time. Original MIT-licensed educational implementation."""

from math import isfinite

class Jump:
    def __init__(self, coyote=0.1, buffer=0.1):
        if not all(isfinite(v) and v >= 0 for v in (coyote, buffer)):
            raise ValueError("invalid grace periods")
        self.coyote, self.buffer = coyote, buffer
        self.last_ground = self.last_press = float('-inf')
        self.now = float('-inf')
        self.used = False
        self.was_grounded = False

    def update(self, now, grounded, pressed):
        if not isfinite(now) or now < self.now:
            raise ValueError("clock must be finite and monotonic")
        self.now = now
        if grounded:
            if not self.was_grounded:
                self.used = False  # A new landing replenishes the jump.
            self.last_ground = now
        self.was_grounded = grounded
        if pressed:
            self.last_press = now
        if not self.used and now-self.last_ground <= self.coyote and now-self.last_press <= self.buffer:
            self.used = True
            self.last_press = float('-inf')  # Consume the buffered input exactly once.
            return True
        return False
