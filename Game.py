from Deck import Deck
from Player import Human, Computer
from Table import Table

import keyboard
import os
import time


class Game:
    def __init__(self):
        self._human = Human()
        self._computer = Computer()
        self._deck = Deck()
        self._table = Table()

        for _ in range(7):
            self._human.add_domino(self._deck.eject_domino())
            self._computer.add_domino(self._deck.eject_domino())

    def draw(self, current_player_type):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print('The current table:\n\n%s\n' % self._table.draw())
        print('The current player: %s\n' % current_player_type)
        print('You have %d dominoes\n' % self._human.get_domino_count())
        print('The computer has %d dominoes\n' % self._computer.get_domino_count())
        print('The deck has %d dominoes\n' % self._deck.get_domino_count())

    def play(self):
        current_player, next_player = self._human, self._computer
        if self._human.best_domino() < self._computer.best_domino():
            current_player, next_player = next_player, current_player

        skip_count = 0
        first_move = True
        while True:
            self.draw(current_player.get_type())
            placed = current_player.make_move(self, self._deck, self._table, first_move)
            first_move = False
            if placed:
                domino, side = placed
                # we are storing dominoes in a way that
                # left is always less than or equal to the right
                # and this is why we use this workaround
                current_player.remove_domino((min(domino), max(domino)))
                if side == 'left':
                    self._table.add_to_the_left(domino)
                else:
                    assert side == 'right', 'Side can only be left or right but it is %s' % side
                    self._table.add_to_the_right(domino)
                print('During the current move the domino %s will be added to the %s\n' % (list(domino), side))
                keyboard.wait('enter')
                time.sleep(0.1)
                skip_count = 0
            else:
                print('The current player have no valid dominoes to add so he skipped the move')
                keyboard.wait('enter')
                time.sleep(0.1)
                skip_count += 1
            if skip_count == 2:
                print('\nTwo moves in a row were skipped so the result is a fish!\n')
                human_hand, computer_hand = self._human.get_hand_score(), self._computer.get_hand_score()
                if human_hand < computer_hand:
                    print('You won!\n')
                else:
                    print('Computer owned you with a random strategy :)\n')
                keyboard.wait('enter')
                time.sleep(0.1)
                break

            if current_player.get_domino_count() == 0:
                if current_player.get_type() == 'human':
                    print('You won!\n')
                else:
                    print('Computer owned you with a random strategy :)\n')
                break
            current_player, next_player = next_player, current_player

        print('Press ESC to exit or enter to start a new game\n')
        time.sleep(0.1)
        while True:
            if keyboard.is_pressed('enter'):
                time.sleep(0.1)
                return True
            elif keyboard.is_pressed('esc'):
                time.sleep(0.1)
                return False
