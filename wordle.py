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
import random

###
# Installed libraries
###
import pandas


###
# From hpclib
###
import fileutils
import linuxutils
from   urdecorators import show_exceptions_and_frames as trap

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

@trap
def build_word_map(filename:str) -> pandas.DataFrame:
    """
    Return a DataFrame of five columns, with the letters
    of each five letter word. 
    """    
    words = []
    for word in fileutils.read_whitespace_file(filename):
        words.append(tuple(word))

    return pandas.DataFrame(data=words)


@trap
def column_frequencies(word_data:list) -> tuple:
    
    words = []
    for word in word_data:
        words.append(tuple(word))

    frame = pandas.DataFrame(data=words)
    return tuple(collections.Counter(frame[i]) for i in range(5))


@trap
def remove_words_containing(words:list, chars:str) -> list:
    """
    Create shorter list of words that have none of the characters in chars.
    """
    for c in chars:
        words = [ word for word in words if c not in word ]
    return words


@trap
def filter_bad_location(words:list, letter:str, offset:int) -> list:
    """
    For example `filter_bad_location(words, 'e', 3)` will return all the 
    words that *do* contain an e, as long as it is *not* in column 3. 
    """
    return [ word for word in words if word[offset] != letter and letter in word ]


@trap
def filter_good_location(words, list, letter:str, offset:int) -> list:
    return [ word for word in words if word[offset] == letter ]


@trap
def pick_a_word(words:tuple) -> str:
        


@trap
def wordle_main(myargs:argparse.Namespace) -> int:

    words = tuple(fileutils.read_whitespace_file('fiveletterwords.txt'))    



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="wordle", 
        description="What wordle does, wordle does best.")

    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name")
    parser.add_argument('--nice', type=int, choices=range(0, 20), default=0,
        help="Niceness may affect execution time.")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="Be chatty about what is taking place")


    myargs = parser.parse_args()
    myargs.verbose and linuxutils.dump_cmdline(myargs)
    if myargs.nice: os.nice(myargs.nice)

    try:
        sys.exit(
            globals()["{}_main".format(os.path.basename(__file__)[:-3])](myargs)
            )

    except Exception as e:
        print(f"Escaped or re-raised exception: {e}")


