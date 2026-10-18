"""Seeded deck shuffle, draw, and discard. Original MIT-licensed educational implementation."""

import random

class Deck:
    def __init__(self, cards, seed=0):
        self.rng=random.Random(seed)
        self.draw_pile=list(cards); self.discard_pile=[]
        self.rng.shuffle(self.draw_pile)

    def draw(self):
        if not self.draw_pile:
            self.draw_pile,self.discard_pile=self.discard_pile,[]
            self.rng.shuffle(self.draw_pile)
        return self.draw_pile.pop() if self.draw_pile else None

    def discard(self, card):
        # The game's rules must confirm that the player actually owns this card.
        self.discard_pile.append(card)
