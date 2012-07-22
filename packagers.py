

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
    if is_iterator(to_package):
        return iter_json_dumps(to_package)
    return json.dumps(to_package)
