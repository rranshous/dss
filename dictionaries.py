
linux_words_buffer = None
def iter_linux_words():
    """
    iterator of root unique words from linux dict file
    """
    global linux_words_buffer
    if linux_words_buffer:
        for v in linux_words_buffer:
            yield v
    else:
        internal_buffer = []
        with open('/usr/share/dict/words','r') as fh:
            lines = fh.readlines()
            last = None
            for word in lines:
                # just root
                word = word.strip().split("'")[0]
                if word != last:
                    yield word
                last = word
                internal_buffer.append(word)
        linux_words_buffer = internal_buffer

dictionaries = iter_linux_words()
