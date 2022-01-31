# wordle
A program to solve Wordle

## A word about Wordle

The game is described here: `https://www.powerlanguage.co.uk/wordle/`

The default list of five letter words comes from the Stanford University
Graph Database, however, the program can be used with any word list
provided the words are all the same length. 

## Requirements

- Python 3.8 or later.
- Pandas

## Program operation

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

The input file may be any whitespace delimited list of words. The words can be
one per line, several per line, or all on one line. You may even have blank
lines with no words. `wordle` is not fussy.

OTOH, `wordle` does not check that all your words in the list are the same
length, and if you choose an initial guess or a target that is of a different
length, then they will never be found. There is an assumption that all the 
words we are talking about are in lower case.

## Method of operation

`wordle` analyzes the word list to make its guesses based on the letter
frequencies in each ordinal position. It tries to choose a guess that 
adds the most amount of information to the clues that have already been
given.

## Sample output

```bash
[master!?][kinghenry(gflanagi):////wordle]: python wordle.py
Looking for nudes.
Round #1. The guess is pates. There are 5757 possibilities.
Round #2. The guess is lines. There are 176 possibilities.
Round #3. The guess is knees. There are 5 possibilities.
Round #4. The guess is noses. There are 3 possibilities.
Round #5. Found it. The word is nudes
```

And here is one that took a while.

```bash
[master!?][kinghenry(gflanagi):////wordle]: python wordle.py
Looking for pined.
Round #1. The guess is toads. There are 5757 possibilities.
Round #2. The guess is eider. There are 214 possibilities.
Round #3. The guess is diked. There are 31 possibilities.
Round #4. The guess is fixed. There are 22 possibilities.
Round #5. The guess is piped. There are 17 possibilities.
Round #6. The guess is piled. There are 2 possibilities.
Round #7. Found it. The word is pined
```
