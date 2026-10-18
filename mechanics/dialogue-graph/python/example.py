"""Conditional branching dialogue. Original MIT-licensed educational implementation."""

from copy import deepcopy

class Dialogue:
    def __init__(self, nodes, start, flags=()):
        if start not in nodes: raise ValueError("unknown start")
        for node in nodes.values():
            for choice in node.get('choices',[]):
                if choice['next'] not in nodes: raise ValueError("unknown destination")
        self.nodes=deepcopy(nodes); self.current=start; self.flags=set(flags)

    def choices(self):
        # Return detached data so a UI cannot mutate the underlying story graph.
        return deepcopy([c for c in self.nodes[self.current].get('choices',[])
                         if set(c.get('requires',())) <= self.flags])

    def choose(self, index):
        choices=self.choices()
        if type(index) is not int or not 0 <= index < len(choices):
            raise ValueError("unavailable choice")
        choice=choices[index]
        self.flags.update(choice.get('grants',()))
        self.current=choice['next']
        return self.nodes[self.current]['text']
