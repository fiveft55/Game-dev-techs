class Machine:
    def __init__(self, initial, transitions):
        self.state=initial; self.transitions=dict(transitions)
    def send(self, event):
        key=(self.state,event)
        if key not in self.transitions: return False
        # Commit one transition per event, making ordering easy to inspect.
        self.state=self.transitions[key]
        return True
