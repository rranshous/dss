

# auto-injected args:
#  cache_getter
#  dictionary_words
#  cache_key_computer

import packagers as p
import filters as f
import bubble as bubble
import keys
from dictionaries import dictionaries

import redis
from itertools import ifilter


def cached_possibles(letters, slots, cache_key_computer,
                     cache_getter, context):
    """
    checks cache for possible solution from cache
    """
    key = context(cache_key_computer, letters, slots)
    return context(cache_getter, key)

def cache_possibility(letters, slots, possibilities,
                      cache_key_computer, cache_setter, context):
    """
    update's cache with solution
    """
    key = context(cache_key_computer, letters, slots)
    return context(cache_setter, key)

def compute_possibles(letters, slots, dictionary_words, context):
    """
    computes possible solution words from given
    dictionary, optionally available slots

    words - iterator of all words in the dictionary
    letters - sorted list of letters on board
    slots - number of available slots

    returns - iterator of possible solution words
    """

    words = dictionary_words

    # if we have a known number of slots filter
    # our word list down to words w/ that manny letters
    if slots:
        words = ifilter(f.word_len(slots), words)

    # filter our word list down to words who's
    # letters are a subset of the given letters
    words = ifilter(f.letter_subset(letters), words)

    # we now have our final iterator of possible solutions
    return words

def get_possibles(letters, slots, compute_possibles,
                  cached_possibles, context):
    """
    returns a list of possible solution words

    letters - sorted list of letters on board
    slots - number of available letter slots

    returns - iterator of possible solution words
    """

    # check the cache
    possibles = context(cached_possibles)
    if possibles:
        return possibles

    # cache miss, we'll have to compute it ourself
    possibles = context(compute_possibles)
    return possibles

def context_application(environ, start_response,
                        letters, slots, package_response,
                        get_possibles, context):

    # get our iterator of possible words
    possibles = context(get_possibles)

    # update our context to include the possibilities
    context.update(possibles=possibles)

    # package up our possible words for returning to client
    response_package = context(package_response, possibles)

    # deliver up our response package
    return response_package

def application(environ, start_response):
    """
    wsgi application callable
    """

    # let the client know we're good to go, and sending json
    start_response('200 OK', [('Content-Type', 'application/json')])

    # break from our path the letters and # of pieces
    # path = .../letters/slots/ or .../letters/
    path = environ.get('PATH_INFO')
    path_pieces = [x.strip() for x in path.split('/') if x.strip()]
    print 'path: %s' % path
    print 'path_pieces: %s' % path_pieces
    if path_pieces[-1].isdigit():
        slots = int(path_pieces[-1])
        letters = path_pieces[-2]
    else:
        slots = None
        letters = path_pieces[-1]

    print 'letters: %s' % letters
    print 'slots: %s' % slots

    # setup redis client
    rc = redis.StrictRedis()

    # create a context for our callables
    context = bubble.build_context({
        'cached_possibles': cached_possibles,
        'compute_possibles': compute_possibles,
        'get_possibles': get_possibles,
        'package_response': p.json_dump,
        'dictionary_words': dictionaries,
        'cache_key_computer': keys.letters,
        'cache_getter': rc.smembers,
        'cache_setter': rc.sadd,
        'letters': letters,
        'slots': slots,
    })

    # wrap our application in our context
    wrapped_application = context.create_partial(context_application)

    return wrapped_application(environ, start_response)

