class MissingDestinationException(Exception):
    """Missing destination exception."""

_compileItems = []

def compileSingle(src, dest):
    """Copy single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    global _compileItems

    if dest is None:
        raise MissingDestinationException()

    _compileItems.append((src, dest))

def compileMultiple(data):
    """Copy multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    global _compileItems

    for src, dest in data.iteritems():
        _compileItems.append((src, dest))

def compileSrc(src, dest=None):
    if isinstance(src, basestring):
        return compileSingle(src, dest)

    if isinstance(src, dict):
        return compileMultiple(src)