import re
from collections import Counter


# A probabilistic approach to auto-correct / spellcheck
# Builds a vocab and maintains the count of each word in the corpus
# We then build a probs dict that contains the probability of every
# word in the corpus, this is called P(W)

# Now based on the vocab, given a word we find the misspelled word
# and find all the words that are 'n edit distance' away, in general
# an edit distance of 1, 2, 3 is used in auto-correct
# and based on these words we find the most probable word and replace it

def build_vocab(corpus: str, verbose=False):
    """Creates a vocab i.e list of unique words in the corpus"""
    vocab = set(re.findall(r'\w+', corpus.lower()))
    if verbose:
        print(f'Vocab contains {len(vocab)} unique words')
    return vocab


def get_probs(corpus: str):
    """Based on the vocab builds a probs dict that contains the probability of each word"""
    word_counts = Counter(re.findall(r'\w+', corpus.lower()))
    total = sum(word_counts.values())
    probs = {w: (count / total) for w, count in word_counts.items()}
    return probs


def edit_one_letter(word: str, include_switches: bool = True):
    """Returns the set of all words that are one edit distance away"""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    inserts = [L + c + R for L, R in splits for c in letters]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]

    replaces_set = set(replaces)
    replaces_set.discard(word)
    replaces = list(replaces_set)

    if include_switches:
        switches = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        return set(deletes + inserts + replaces + switches)
    return set(deletes + inserts + replaces)


def edit_two_letters(word: str, include_switches: bool = True):
    """Returns the set of all words that are two edit distance away"""
    one_edit_away = edit_one_letter(word, include_switches=include_switches)
    two_edits_away = []
    for w in one_edit_away:
        two_edits_away += edit_one_letter(w, include_switches=include_switches)
    return set(two_edits_away)


def corrected_sentence(sentence: str):
    def replace_words(words_list: list, words_to_replace, replacements):
        for i in range(len(replacements)):
            words_list[words_list.index(words_to_replace[i])] = replacements[i]
        return ' '.join(words_list)

    def get_corrections(word, vocab, probs, n=2, verbose=False):
        suggestions = []
        n_best = []

        if word in vocab:
            return word

        suggestions = list(edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
        n_best = [(s, probs[s]) for s in list(reversed(suggestions))]

        if verbose:
            print("suggestions = ", suggestions)

        n_best.sort(key=lambda x: x[1], reverse=True)
        return n_best[:n]

    with open('data.txt', 'r') as f:
        data = f.read()

    vocab = build_vocab(data)
    probs = get_probs(data)
    words_in_sentence = sentence.split(' ')
    corrections_needed = [word for word in words_in_sentence if word.lower() not in vocab]
    corrections = [get_corrections(word, vocab, probs, verbose=False)[0][0] for word in corrections_needed]

    return replace_words(words_in_sentence, corrections_needed, corrections)


print(corrected_sentence('I wanx to gx oux'))
