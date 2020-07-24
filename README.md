# Probabilistic-AutoCorrect
A simple probability based auto-correct / spellcheck implemented in python. This was first created by Peter Norvig in 2007.

A much detailed explanation can be found at <a href="https://norvig.com/spell-correct.html">Peter Norvig's AutoCorrect implementation</a>

## How it works ?

Based on a huge corpus we build our vocab (Set of unique words in the corpus).We then build a probs dict that contains the probability of every word in the corpus, this is called P(W).

Now based on the vocab, given a sentence we find the misspelled word and find all the words that are 'n edit distance' away, in general an edit distance of 1, 2, 3 is used in auto-correct and based on these words we find the most probable word and replace it
