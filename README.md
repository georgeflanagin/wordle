# wordle
A program to solve Wordle

## A word about Wordle

The game is described here: `https://www.powerlanguage.co.uk/wordle/`

The default list of five letter words comes from the Stanford University
Graph Database, however, the program can be used with any word list
provided the words are all the same length. The files `sevenletterwords.txt.gz`
and `sixletterwords.txt.gz` contain what you would think. `gunzip` them
and you are ready to go.

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

The input file may be any whitespace delimited list of words. The
words can be one per line, several per line, or all on one line.
You may even have blank lines with no words. `wordle` is not fussy.

OTOH, `wordle` does not check that all your words in the list are
the same length, and if you choose an initial guess or a target
that is of a different length, then they will never be found. There
is an assumption that all the words we are talking about are in
lower case.

## Method of operation

`wordle` analyzes the word list to make its guesses based on the
letter frequencies in each ordinal position. It tries to choose a
guess that adds the most amount of information to the clues that
have already been given.

The sample output shows the filtration process, and the next 
section explains the search method.

### Sample output

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

### Search Method

The program has two parts. The first part selects a word and provides
the information in response to the guesses, just as the Wordle game does.
The second part is the guessing. 

#### Simulator for the game, itself.

You have the option to supply the word to be guessed, but 
the program can also choose it randomly. The choice is truly random,
and is from the entire list of n-letter words, whether the words
are 5, 6, or 7 letters long. 

As the guessing engine ('the player') guesses, the game colors
the squares yellow if the letter is in the word to be guessed, but
somewhere else in the word. It goes to green if the letter is the 
correct letter in the correct position in the target word. 

The 'squares' are just a list of the offsets into the word and what
color they are to be; no squares are actually drawn.

#### The guessing engine.

Unlike a human player, the guessing engine knows all the possible
words; that is, it has a complete vocabulary. In the case of the 
5757 5-letter words, it knows them all, whereas a typical wordle
player may know 1500 or 2000 words in the sense of being able to
recall them.

Many problems in ciphers are approached with frequency analysis of
some kind, and wordle is no exception. E, T, A, O, N, ... are the
most common letters in English, but that is not specific enough to
be of use in Wordle:

1.  We are only concerned with the letter frequencies in the 5757
    5-letter words, and because they are being selected at random
    we do not care about the frequency of the words in the English language.
1.  The searching is even narrower than the first item suggests.
    Within each position of the word, say the middle character, we
    are only interested in the frequency of the letters *at that position*. 
    
For its initial guess, the engine chooses from a list of words
that have common letters at each position. As an example, `S` is a 
common letter overall, but it is not very common as the second letter because
it would only be expected as a second letter in words that start with vowels -- no English
words start with `DS` and only a handful start with `PS`.

An additional optimization on the first guess is that words with duplicate
letters are never used initially. The information gained by whittling
down the list of candidates far exceeds the chance of finding that
the target word has a double letter.

After the initial guess, the guessing engine behaves differently than
the few human players I have observed. The guessing engine always 
incorporates what it has learned so far. As an example, let's look at
the second sample output above:

```
Looking for pined.
Round #1. The guess is toads. There are 5757 possibilities.
Round #2. The guess is eider. There are 214 possibilities.
Round #3. The guess is diked. There are 31 possibilities.
```

After discovering that none of the letters in `toads` match
any of the letters in the target, `pined`, the guessing engine
eliminated all the words that have `a`, `d`, `o`, `s`, or `t` at any 
position, and selected `eider` as its next guess. 

Before selecting `eider`, it ranked the 214 words according to 
how likely it was for the letters to be in those positions just
as it looked at the whole set of 5757 words to choose the first,
blind guess. 

The answer it got after guessing `eider` was `|grey |green|grey |green|grey |`,
and all subsequent guesses were in the format `?i?e?`

