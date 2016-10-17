'''
    example.py

    Some examples of creating mazes, running games, collecting statistics, and opening the GUI.
'''

from __future__ import print_function

import sys
import time

from collections import defaultdict

from PyQt5.QtWidgets import QApplication

from maze import Maze, Game, game_repeater
from goodies import RandomGoody
from baddies import RandomBaddy
from goodies import OurGoody
from gui import GameViewer


EXAMPLE_MAZE = Maze(10, 10, "0001010000"
                            "0111010101"
                            "0100000011"
                            "0110100010"
                            "0000100110"
                            "1111100000"
                            "0000001000"
                            "1000111010"
                            "0010001010"
                            "1100101010")

ORIGINAL = Maze(10, 10,
"0001010000"
"0111010101"
"0100000011"
"0110100010"
"0000100110"
"1111100000"
"0000001000"
"1000111010"
"0010001010"
"1100101010") * (2, 2)

OPEN = Maze(20, 20,
"10000000000001000000"
"01000001100010000000"
"01000001000111111000"
"00100011111000000100"
"00100000000000001000"
"00100000001111100000"
"00001000000000100000"
"00110110000000100000"
"00000001110000011110"
"00000100001110000000"
"00000001000001001000"
"00001111111110110010"
"00000100000000000100"
"00011000110000001000"
"00000111000000010000"
"00000000100011100000"
"00000000011100000000"
"00000000110000000000"
"00000000100000000000"
"00000000000000000000")


TIGHT = Maze(20, 20,
"00000000000000000000"
"01111111111111111110"
"00000000110000000000"
"00110111111110011111"
"00100000000000000000"
"00111111111111110010"
"00000000000000000010"
"01001111111111001110"
"10000000000000000000"
"10111111110111011111"
"00000000000000000000"
"11111111111111111110"
"00000000000000000000"
"00000000000000000000"
"01111111111111111111"
"00100100010010010100"
"00100100000010010100"
"00100100010010010100"
"00001110011011010110"
"00000000001000000000"
)

def text_example():
    ''' Prints the state of the game to stdout after each round of turns '''

    goody0 = OurGoody()
    goody1 = RandomGoody()
    baddy = RandomBaddy()

    game = Game(EXAMPLE_MAZE * (2, 2), goody0, goody1, baddy)

    def hook(game):
        print(game, "\n")
        time.sleep(0.1)  # Max speed of 10 updates per second

    game.play(hook=hook)

def stats_example(total_games):
    ''' Plays many games, printing cumulative and final stats '''

    results = defaultdict(int)
    for game_number, game in enumerate(game_repeater(EXAMPLE_MAZE, OurGoody, OurGoody, RandomBaddy)):
        if game_number == total_games:
            break
        result, _rounds = game.play()
        results[result] += 1
        if game_number % 10 == 0:
            print(game_number, "/", total_games, ":", dict(results))

    print(dict(results))

def gui_example():
    ''' Opens a GUI, allowing games to be stepped through or quickly played one after another '''
    app = QApplication.instance() or QApplication(sys.argv)
    gv = GameViewer()
    gv.show()
    gv.set_game_generator(game_repeater(OPEN * (3, 3), OurGoody, OurGoody, RandomBaddy))
    app.exec_()

if __name__ == "__main__":
    # Uncomment whichever example you want to run
    #text_example()
    stats_example(1000)
    #gui_example()