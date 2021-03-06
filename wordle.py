# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

###
# Other standard distro imports
###
import argparse
import collections
import contextlib
import enum
import random
import re
import shutil
import time

###
# Installed libraries
###
import pandas

# from urdecorators import trap

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2022'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = ['gflanagin@richmond.edu', 'me@georgeflanagin.com']
__status__ = 'in progress'
__license__ = 'MIT'

###
# A global.
###
# The one we are looking for.
theword = ""
# Does printv do anything?
verbose = False
# The size of the original population
population = 0

#@trap
def printv(s:str) -> None:
    """
    print only in verbose mode.
    """
    global verbose
    verbose and print(s)


#@trap
class SquareColor(enum.Enum):
    # We don't care about the underlying values; just the color.
    GREEN  = enum.auto()
    GREY   = enum.auto()
    YELLOW = enum.auto()


#@trap
def filter_yellow_square(words:tuple, letter:str, offset:int) -> tuple:
    """
    For example `filter_bad_location(words, 'e', 3)` will return all the 
    words that *do* contain at least one 'e', as long as it is *not* 
    in column 3. 
    """
    return tuple( word for word in words 
        if word[offset] != letter and letter in word )


#@trap
def filter_green_square(words:tuple, letter:str, offset:int) -> tuple:
    """
    Given a letter and an offset, return the words in in the list
    that have a letter in that position.  
    """ 
    return tuple( word for word in words if word[offset] == letter )


#@trap
def filter_grey_square(words:tuple, letter:str, offset:int) -> tuple:
    """
    Create shorter list of words that do not contain letter.
    NOTE: offset is not used; it is present for the signature.
    """
    return tuple( word for word in words if letter not in word )
            

filter_functions = {
    SquareColor.GREEN  : filter_green_square,
    SquareColor.GREY   : filter_grey_square,
    SquareColor.YELLOW : filter_yellow_square
    }


#@trap
def column_frequencies(words:tuple) -> tuple:
    """
    This function returns a tuple of dicts that correspond to
    the frequencies of letters in each ordinal position of the
    words in the list.
    """    
    frame = pandas.DataFrame(data=(tuple(word) for word in words))
    return tuple(collections.Counter(frame[i]) for i in range(len(words[0])))


#@trap
def compare_guess_w_target(myguess:str) -> tuple:
    """
    Provide the game's hints.
    """
    global theword

    # Set them all to GREY to start, and then change color if necessary.
    hints = [ SquareColor.GREY for _ in range (len(myguess)) ]
    for i, c in enumerate(myguess):
        if c in theword: 
            hints[i] = SquareColor.GREEN if theword[i] == c else SquareColor.YELLOW
        
    return tuple(hints)


#@trap
def eval_guess(word:str, hints:tuple, words:tuple) -> tuple:
    """
    Apply the filters based on the hints.
    """
    global filter_functions

    for i, hint in enumerate(hints):
        words = filter_functions[hint](words, word[i], i)
    
    return words


#@trap
def first_guess(words:tuple) -> str:
    """
    Some words are just good places to start. Choose one at random.
    These words have no repeated letters, the letters in each 
    position are relatively common, and relatively common in *that* 
    position.
    """
    return guess(words, no_repeats=True)


#@trap
def guess(words:tuple, depth:int=5, no_repeats:bool=False) -> str:
    """
    Choose the next word from the (already filtered?) list of words.
    This function is the core of the method for playing Wordle.
    """

    ####
    # get a list of the letter frequencies in each column.
    ####
    frequencies = column_frequencies(words)
    printv(f"{frequencies=}")

    ####
    # We are building up a regex that looks something like this one:
    #  [scbpt][aoieu][etnla][syedr][seaor]
    ####
    regex = ""
    for i in range(len(frequencies)):
        common_chars = "".join(_[0] for _ in frequencies[i].most_common(depth))
        regex += f"[{common_chars}]"

    printv(f"{regex=}")
    ####
    # Makes sense to compile it.
    ###
    regex = re.compile(regex)
    good_guesses = [word for word in words 
        if re.fullmatch(regex, word) is not None]

    if no_repeats:
        ####
        # Because we do not know any of the letters on the first guess,
        # it is a good idea to avoid any words with duplicate letters.
        ####
        better_guesses = []
        for myguess in good_guesses:
            if len(collections.Counter(myguess).most_common()) == len(myguess): 
                better_guesses.append(myguess)
        good_guesses = tuple(better_guesses)

    if not len(good_guesses):
        raise Exception("Algorithm failed. No words match.")

    return random.choice(good_guesses)


#@trap
def pick_a_target(words:tuple):
    return random.choice(words)        


#@trap
def read_whitespace_file(filename:str) -> tuple:
    """
    This is a generator that returns the whitespace delimited tokens 
    in a text file, one token at a time.
    """
    if not filename: return []

    if not os.path.isfile(filename):
        sys.stderr.write(f"{filename} cannot be found.")
        return os.EX_NOINPUT

    f = open(filename)
    yield from (" ".join(f.read().lower().split('\n'))).split()
    

# @trap
def do_batch(myargs:argparse.Namespace) -> int:
    """
    Do an enormous list of comparisons
    """
    global theword
    guesses = tuple(read_whitespace_file(myargs.guess))
    targets = tuple(read_whitespace_file(myargs.target))
    for this_target in targets:
        theword = this_target
        for this_guess in guesses:
            n = solve_wordle(this_guess, targets, silent=True)
            print(f"{theword},{this_guess},{n}")

    return os.EX_OK


#@trap
def wordle_main(myargs:argparse.Namespace) -> int:
    global theword
    global population

    if myargs.batch: return do_batch(myargs)

    words       = tuple(read_whitespace_file(myargs.input))    
    t           = time.time()
    population  = len(words)

    theword     = myargs.target if myargs.target else pick_a_target(words)
    myguess = myargs.guess.lower() if myargs.guess else first_guess(words)

    print(f"Looking for {theword}.")
    return solve_wordle(myguess, words)


def solve_wordle(myguess:str, words:tuple, silent:bool=False) -> int:
    """
    Find the word by progressive approximations.
    """
    if silent: verbose=False

    i = 0
    try:
        while len(words) > 1:
            if myguess == theword: break
            i = i+1
            not silent and print(f"Round #{i}. {myguess=}. There are {len(words)} possibilities.")
            hints = compare_guess_w_target(myguess)
            newwords = eval_guess(myguess, hints, words)

            ####
            # The inner while loop deals with the situation in which
            # there are no dictionary words composed solely of the
            # N=5 most common letters in each position. In this case,
            # the letter must be one of the less common letters, os
            # we back up, and go one deeper on the search. The max
            # is set to 9.
            ####
            OK = False
            depth = 5
            while not OK and depth < 10:
                myguess = guess(newwords, depth) 
                if not myguess:
                    depth += 1
                    not silent and print(f"Backtracking ... {depth=}")
                    continue
                words = newwords
                OK = True

    except KeyboardInterrupt as e:
        print("You pressed control C")
        sys.exit(os.EX_OK)        

    if (myguess != theword): 
        raise Exception(f"This program has a bug. It found {myguess} instead of {theword}")
    
    not silent and print(f"Round #{i+1}. Found it. The word is {theword}\n")
    not silent and print(f"Elapsed time: {time.time() - t}")
    return i


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="wordle", 
        description="What wordle does, wordle does best.")

    parser.add_argument('-b', '--batch', action='store_true', 
        help="treat guess and target as files of words, and do a cross-product of them.")
    parser.add_argument('-g', '--guess', type=str, default="",
        help="An initial guess. Default is to let the program choose one.")
    parser.add_argument('-i', '--input', type=str, default="fiveletterwords.txt",
        help="Input file name with the plenum word list. Default is fiveletterwords.txt")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name. If not supplied, stdout")
    parser.add_argument('-r', '--random-start', action="store_true",
        help="Make a random guess to start the process.")
    parser.add_argument('-t', '--target', type=str, default="",
        help="The target word. Default is to let the program choose one.")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="Be chatty about what is taking place.")

    myargs = parser.parse_args()
    verbose = myargs.verbose 
    if myargs.random_start: myargs.guess = ""

    outfile = open(myargs.output, 'w') if myargs.output else sys.stdout
    with contextlib.redirect_stdout(outfile):
        try:
            sys.exit(globals()["{}_main".format(os.path.basename(__file__)[:-3])](myargs))

        except Exception as e:
            print(f"Escaped or re-raised exception: {e}")
