import random


class Deck:
    def __init__(self):
        self._dominoes = []
        for left in range(7):
            for right in range(left, 7):
                self._dominoes.append((left, right))

    def eject_domino(self):
        value = random.choice(self._dominoes)
        self._dominoes.remove(value)
        return value

    def get_domino_count(self):
        return len(self._dominoes)

    def empty(self):
        return self.get_domino_count() == 0
