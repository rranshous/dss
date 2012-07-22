
import sys
from itertools import ifilter, combinations_with_replacement
import os.path
import redis
rc = redis.StrictRedis()

words = list()
def word_iterator():
    """
    iterates up all possible words
    """
    global words
    if words:
        for word in words:
            yield word
    else:
        _words = list()
        with open('/usr/share/dict/words','r') as fh:
            lines = fh.readlines()
            last = None
            for word in lines:
                # just root
                word = word.strip().split("'")[0]
                if word != last:
                    _words.append(word)
                    yield word
                last = word
            words = _words

def report(possibles):
    for p in possibles:
        print p + ',',


def get_options(letters, spaces):
    letters = set(letters)
    return \
        ifilter(lambda w: len(w) == spaces,
                ifilter(lambda w: set(w).issubset(letters),
                        word_iterator()))

def report(writer, spaces, letters, possibles):
    """
    write to text file the data using the iterator
    """
    writer('%s:%s:' % (spaces, ''.join(letters)))
    for word in possibles:
        writer('%s,' % word)
    writer('\n')

seen = set()
def unique(i):
    """
    have we not seen these items in the list before (in any order)?
    """
    i = tuple(sorted(i))
    u =  i not in seen
    seen.add(i)
    return u

def combine_writers(*writers):
    def combo_writer(output):
        for writer in writers:
            writer(output)
    return combo_writer

if __name__ == '__main__':

    #report(possibles)
    alph = 'abcdefghijklmnopqrstuvwxyz'
    out_path = os.path.abspath('./combos.dat')
    possible_letters = 12
    fh = open(out_path, 'w')
    count = 0
    def fh_flush(*args):
        if count % 100 == 0:
            fh.flush()
    def fh_write(to_write, *args):
        fh.write(to_write)
    def stdout_write(to_write, *args):
        sys.stdout.write(to_write)
    r_buffer = ''
    def redis_write(to_write):
        global r_buffer
        r_buffer += to_write
        if r_buffer.endswith('\n'):
            r_buffer = r_buffer[:-1]
            spaces, letters, possibles = r_buffer.split(':')
            spaces = int(spaces)
            possibles = possibles.split(',')
            key = '%s:%s' % (spaces, ''.join(letters))
            pipe = rc.pipeline()
            for word in possibles:
                if word:
                    pipe.sadd(key, word)
            pipe.execute()
            r_buffer = ''
    print 'making letter combos'
    letter_combos = ( sorted(list(combo)) for combo in ifilter(unique, combinations_with_replacement(alph, possible_letters)) )
    print 'done letter combos'
    for spaces in xrange(3, 8):
        for letters in letter_combos:
            s_letters = set(letters)
            possibles = get_options(s_letters, spaces)
            report(combine_writers(sys.stdout.write, redis_write), spaces, letters, possibles)
    fh.close()

