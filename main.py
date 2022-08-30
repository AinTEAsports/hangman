#!/usr/bin/python3

import sys
from utils import HangmanGame, get_random_word


word = get_random_word()
game = HangmanGame(word)

try:
    game.play()
except KeyboardInterrupt:
    print("\n\nGAME INTERRUPTED...\n\n")
    sys.exit(127)

