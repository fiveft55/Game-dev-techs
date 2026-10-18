"""Quest objective tracking. Original MIT-licensed educational implementation."""

class Quest:
    def __init__(self, targets):
        if not targets or any(type(v) is not int or v <= 0 for v in targets.values()):
            raise ValueError("positive objective targets required")
        self.targets=dict(targets)
        self.progress={key:0 for key in targets}
        self.claimed=False

    def record(self, event, amount=1):
        if type(amount) is not int or amount < 0: raise ValueError("invalid amount")
        if event in self.targets:
            self.progress[event]=min(self.targets[event], self.progress[event]+amount)

    @property
    def complete(self):
        return self.progress == self.targets

    def claim(self):
        if self.claimed or not self.complete: return False
        self.claimed=True
        return True
