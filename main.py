# NOTE: you have to install keyboard module to run this project
# pip install keyboard

from Game import Game

if __name__ == '__main__':
    while True:
        game = Game()
        need_to_continue = game.play()
        if not need_to_continue:
            break
