
def word_len(length):
    """
    returns callable which returns true if it's
    argument's len is the same as our passed length
    """
    def match_len(w):
        return length == len(w)
    return match_len

def letter_subset(letters):
    """
    returns callable which returns true if
    it's argument is a subset of our passed arg
    """
    s_letters = set(letters)
    def match_subset(w):
        return set(w).issubset(s_letters)
    return match_subset
