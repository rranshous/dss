import sys
from itertools import ifilter

def word_iterator():
    """
    iterates up all possible words
    """
    with open('/usr/share/dict/words','r') as fh:
        lines = fh.readlines()
        last = None
        for word in lines:
            # just root
            word = word.strip().split("'")[0]
            if word != last:
                yield word
            last = word

def report(possibles):
    for p in possibles:
        print p + ',',


def get_options(letters, spaces):
    return \
        ifilter(lambda w: len(w) == spaces,
                ifilter(lambda w: set(w).issubset(letters),
                        word_iterator()))

def save_convo(writer, spaces, letters, possibles):
    """
    write to text file the data using the iterator
    """
    writer('%s:%s:' % spaces, letters)
    for word in possibles:
        writer('%s,' % word)

if __name__ == '__main__':

    letters, spaces = sys.argv[1:]
    spaces = int(spaces)
    letters = set(letters)
    possibles = get_options(letters, spaces)

    report(possibles)
