from accessor import fill_deps

class DirectAccessor(object):
    """ accessor which simply will return you the value
    it's created with when u ask
    """
    def __init__(self, key, value):
        self.key = self.name = key
        self.value = value
    def transform(self, arg):
        return self.value
DA = DirectAccessor

class Context(object):

    def __init__(self, mapping={}):
        self.mapping = mapping
        self.accessor_map = self.build_accessor_map(mapping)

    @staticmethod
    def build_accessor_map(self, mapping):
        """
        given a mapping of k/v to use in the accessor
        map create an accessor map for dep fills
        """
        return dict( ( k, DA(k, mapping[k]) ) for k in mapping )

    def create_partial(self, fn, *p_args, **p_kwargs):
        """
        returns a callable which has been wrapped
        with the passed argument

        passed arguments are added to end of resulting
        callables args
        """
        def resulting_callable(*c_args, **c_kwargs):
            # create a set of argsuments which are
            # the args passed to the this callable concat'd
            # with the one's passed to the create_partial call
            cp_args = c_args + p_args

            # update the args passed in to partial with those
            # passed to this callable
            cp_kwargs = p_kwargs.copy()
            cp_kwargs.update(c_kwargs)

            # get the args and kwargs we are going to pass
            # to our resulting
            f_args, f_kwargs = fill_deps(fn, self.accessor_map,
                                         *cp_args, **cp_kwargs)

            # call the function we're wrapping with the derived args
            return fn( *f_args, **f_kwargs )

        # return our wrapper
        return resulting_callback

    def __call__(self, fn, *args, **kwargs):
        """
        call the function within the context
        """
        return self.create_partial(fn)(*args, **kwargs)

def build_context(*context_pieces):
    context = {}
    for context_piece in context_pieces:
        # check if dict, update context w/ k/v pairs
        # todo: check if Mapping instead ?
        if hasattr(context_piece, 'items'):
            context.update( context_piece )

        # if iterator, take first two values as
        # k/v for context
        elif hasattr(context_piece, 'next'):
            for d in context_piece:
                try:
                    context[d[0]] = d[1]
                except IndexError:
                    pass

    # return our context
    return Context(context)

