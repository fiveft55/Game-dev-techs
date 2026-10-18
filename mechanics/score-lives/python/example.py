"""Score, lives, and extra lives. Original MIT-licensed educational implementation."""

class Score:
    def __init__(self, lives=3, threshold=10000):
        if type(lives) is not int or lives < 0 or type(threshold) is not int or threshold <= 0:
            raise ValueError("invalid lives or threshold")
        self.points = 0
        self.lives = lives
        self.threshold = threshold

    def award(self, points):
        if type(points) is not int or points < 0:
            raise ValueError("points must be a nonnegative integer")
        before = self.points // self.threshold
        self.points += points
        # Count every threshold crossed, rather than checking for exact equality.
        self.lives += self.points // self.threshold - before

    def lose_life(self):
        self.lives = max(0, self.lives - 1)
        return self.lives == 0
