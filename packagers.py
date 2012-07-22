import json

def is_iterator(i):
    """
    return True if passed arg is iterator
    """
    # TODO: better
    return callable(i)

def json_dump(to_package):
    """
    takes a dictionary or iterator
    and packages it in json

    returns - json string
    """
    try:
        to_package = iter(to_package)
        to_package = [p for p in to_package]
    except TypeError:
        pass
    package = json.dumps(to_package)
    return package
