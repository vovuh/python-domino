import keyboard
from random import choice
import time


class Player:
    def __init__(self, player_type):
        self._type = player_type
        self._hand = []

    def get_type(self):
        return self._type

    def add_domino(self, domino):
        self._hand.append(domino)

    def remove_domino(self, domino):
        assert domino in self._hand, 'There is no domino %s in %s\'s hand' % (list(domino), self._type)
        self._hand.remove(domino)

    def get_domino_count(self):
        return len(self._hand)

    def get_hand_score(self):
        result = 0
        if len(self._hand) == 1:
            if self._hand[0] == (0, 0):
                result = 25
        else:
            for domino in self._hand:
                result += sum(domino)
        return result

    def best_domino(self):
        index = 28
        for value in range(1, 7):
            if (value, value) in self._hand:
                return index
            index -= 1
        # fix this
        for left in range(7):
            for right in range(left + 1, 7):
                if (left, right) in self._hand:
                    return index
            index -= 1
        assert False, 'Error: %s have no dominoes' % self._type

    def get_available_moves(self, table, first_move):
        result = set()
        for (left, right) in self._hand:
            if first_move and (left, right) == (0, 0):
                continue
            for _ in range(2):
                # not first_move is used to make  the list of
                # available dominoes during the first move a bit more clear
                # (i.e. we will only have 'right' sides during the first move)
                if not first_move and table.can_add_to_the_left((left, right)):
                    result.add(((left, right), 'left'))
                if table.can_add_to_the_right((left, right)):
                    result.add(((left, right), 'right'))
                left, right = right, left
        return list(result)

    def can_make_move(self, table, first_move):
        return len(self.get_available_moves(table, first_move)) > 0


class Human(Player):
    def __init__(self):
        super().__init__('human')

    def make_move(self, game, deck, table, first_move):
        while not self.can_make_move(table, first_move) and not deck.empty():
            game.draw('human')
            print('You have no valid dominoes so you get one domino from the deck\n')
            self.add_domino(deck.eject_domino())
            keyboard.wait('enter')

        if not self.can_make_move(table, first_move):
            return None

        moves = self.get_available_moves(table, first_move)
        position = 0

        def draw_move():
            nonlocal position
            game.draw('human')
            print('The list of valid dominoes is shown below.')
            print('Use up and down to choose domino and press enter to confirm your choice.\n')
            for i in range(len(moves)):
                domino, side = moves[i]
                line = 'Add %s to the %s' % (list(domino), side.ljust(5))
                print(line + (' <' if position == i else ''))
            print()

        draw_move()
        # each keyboard implementation library have no
        # on_release function or it is implemented in a weird way
        # so time.sleep is used to prevent too fast key presses
        while True:
            if keyboard.is_pressed('down'):
                position = min(position + 1, len(moves) - 1)
                draw_move()
                time.sleep(0.05)
            elif keyboard.is_pressed('up'):
                position = max(0, position - 1)
                draw_move()
                time.sleep(0.05)
            elif keyboard.is_pressed('enter'):
                return moves[position]


class Computer(Player):
    def __init__(self):
        super().__init__('computer')

    def make_move(self, game, deck, table, first_move):
        while not self.can_make_move(table, first_move) and not deck.empty():
            game.draw('computer')
            print('Computer has no valid dominoes so he gets one domino from the deck\n')
            self.add_domino(deck.eject_domino())
            keyboard.wait('enter')

        if not self.can_make_move(table, first_move):
            return None

        domino, side = choice(self.get_available_moves(table, first_move))

        return domino, side
