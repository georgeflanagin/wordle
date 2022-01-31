# wordle
A program to solve Wordle

## A word about Wordle

The game is described here: `https://www.powerlanguage.co.uk/wordle/`

The default list of five letter words comes from the Stanford University
Graph Database, however, the program can be used with any word list
provided the words are all the same length. 

## Program operation

The program requires the `hpclib` that is also a public repo that you
can find here: `https://github.com/georgeflanagin/hpclib`. It also
requires pandas, but almost everyone uses pandas. 

The help looks like this:

```
usage: wordle [-h] [-g GUESS] [-i INPUT] [-o OUTPUT] [-t TARGET] [-v]

What wordle does, wordle does best.

optional arguments:
  -h, --help            show this help message and exit
  -g GUESS, --guess GUESS
                        An initial guess. Default is to let the program choose one.
  -i INPUT, --input INPUT
                        Input file name with the plenum word list. Default is fiveletterwords.txt
  -o OUTPUT, --output OUTPUT
                        Output file name. If not supplied, stdout
  -t TARGET, --target TARGET
                        The target word. Default is to let the program choose one.
  -v, --verbose         Be chatty about what is taking place.
```

## Method of operation

`wordle` analyzes the word list to make its guesses based on the letter
frequencies in each ordinal position. It tries to choose a guess that 
adds the most amount of information to the clues that have already been
given.
