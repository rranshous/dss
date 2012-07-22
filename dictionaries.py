
def iter_linux_words():
    """
    iterator of root unique words from linux dict file
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

dictionaries = iter_linux_words()
