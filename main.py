import sys
from utils import HangmanGame


game = HangmanGame("prout")

try:
    game.play()
except KeyboardInterrupt:
	print("\n\nGAME INTERRUPTED...\n\n")
	sys.exit(127)

