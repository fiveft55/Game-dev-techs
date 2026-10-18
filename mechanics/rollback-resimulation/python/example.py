"""Deterministic rollback and resimulation. Original MIT-licensed educational implementation."""

from copy import deepcopy

class Rollback:
    def __init__(self, initial, step):
        self.states=[deepcopy(initial)]
        self.inputs=[]; self.step=step

    @property
    def current(self): return deepcopy(self.states[-1])

    def advance(self, input_value):
        next_state=self.step(deepcopy(self.states[-1]),deepcopy(input_value))
        self.inputs.append(deepcopy(input_value))
        self.states.append(deepcopy(next_state))
        return self.current

    def correct(self, tick, authoritative_state):
        if type(tick) is not int or not 0<=tick<len(self.states): raise ValueError("unknown tick")
        # Build replacement history first so a failed step leaves old state intact.
        replacement=[deepcopy(authoritative_state)]
        for input_value in self.inputs[tick:]:
            replacement.append(deepcopy(self.step(deepcopy(replacement[-1]),deepcopy(input_value))))
        self.states[tick:]=replacement
        return self.current
