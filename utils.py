import os
import sys
import random
import requests
import subprocess
from unidecode import unidecode

import termcolor


PATH_SEPARATOR = '\\' if sys.platform.startswith("win") else '/'
SCRIPT_FULLPATH = PATH_SEPARATOR.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-1])



# This function is disgusting but I didn't found any better way to clear the screen
def clear_screen():
    """Clears the screen
    """

    print("\033c", end="")


def get_random_word() -> str:
    """Returns a random word from wordlist hosted on Github

    Returns:
        (str): a random word from T25's Github wordlist
    """

    WORDLIST_URL = "https://raw.githubusercontent.com/Tom25/Hangman/master/wordlist.txt"
    words = requests.get(WORDLIST_URL).text.split('\n')

    return random.choice(words)


class InvalidGuessNumber(Exception):
    pass


class HangmanWord:

    def __init__(self, word: str) -> None:
        """Init method

        Args:
            word (str): the word (yes)
        """

        self.__word = unidecode(word)
        self.__word_repr = [[char, '_'] for char in word]


    @property
    def word(self) -> str:
        """Returns the word

        Returns:
            (str): the word
        """

        return self.__word


    @property
    def word_repr(self) -> list[list[str, str]]:
        """The word repr

        Returns:
            (list[list[str, str]]): Returns a dictionnary where each key is each char of the word
                and if the char was found it is the char, otherwise it is '_'
        """

        return self.__word_repr


    def guess(self, char: str) -> bool:
        """If the char is right, returns True and change self.__word_repr, if
            not, returns False

        Args:
            char (str): the guess

        Returns:
            (bool): True if the char is in self.__word, otherwise False
        """

        if not char in self.__word:
            return False

        for index, t in enumerate(self.__word_repr):
            if t[0] == char:
                self.__word_repr[index][1] = char

        return True


    @property
    def list_word_repr(self) -> list[str]:
        """Returns the word representation as an array

        Returns:
            (list[str]): the word representation as an array (each element is the char if
                it has been found, otherwise it is a '_'
        """

        return [termcolor.colored(char, attrs=["underline"]) for _, char in self.__word_repr]



class HangmanGame:

    def __init__(self, word: str) -> None:
        self.__word = HangmanWord(word)
        self.__finished_game = False
        self.__lost = False
        self.__false_guess_count = 0
        self.__false_chars: list[str] = []


    def __get_draw(self, guess_number: int) -> str:
        if guess_number == 0:
            return ""

        if guess_number > 10:
            raise InvalidGuessNumber("guess number only can be between 0 and 10")

        file = f"{SCRIPT_FULLPATH}/.hangman_representations/{guess_number}.hang"

        with open(file, 'r', encoding="utf-8") as f:
            draw = f.read()

        return draw


    def play(self) -> None:
        while True:
            if self.__finished_game:
                break

            clear_screen()


            print(self.__get_draw(self.__false_guess_count) + "\n\n\n")
            print(' '.join(self.__word.list_word_repr))

            guess = input(f"\n\nFalse guesses: {' | '.join(self.__false_chars)}\nFalse guess count: {self.__false_guess_count}\nEnter your guess: ").lower()

            if len(guess) > 1:
                continue

            right_guess = self.__word.guess(guess)

            if not right_guess:
                if not guess in self.__false_chars:
                    self.__false_chars.append(guess)
                    self.__false_guess_count += 1

            # TO CORRECT
            if ''.join([char for _, char in self.__word.word_repr]) == self.__word.word:
                self.__finished_game = True

            if self.__false_guess_count == 10:
                self.__finished_game = True
                self.__lost = True


        clear_screen()

        print(self.__get_draw(self.__false_guess_count) + "\n\n\n")
        print(' '.join(self.__word.list_word_repr))
        print(f"\n\nFalse guesses: {' | '.join(self.__false_chars)}\nFalse guess count: {self.__false_guess_count}\n")

        if self.__lost:
            print(f"\nYOU LOST !\nThe word was '{self.__word.word}'")
        else:
            print(f"\nYOU WON !\nThe word was '{self.__word.word}'")


if __name__ == "__main__":
    _ = HangmanWord("test")
    print(' '.join(_.list_word_repr))

