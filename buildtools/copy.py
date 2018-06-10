class MissingDestinationException(Exception):
    """Missing destination exception."""

_copyItems = []

def copySingle(src, dest):
    """Copy single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    global _copyItems

    if dest is None:
        raise MissingDestinationException()

    _copyItems.append((src, dest))

def copyMultiple(data):
    """Copy multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    global _copyItems

    for src, dest in data.iteritems():
        _copyItems.append((src, dest))

def copySrc(src, dest=None):
    if isinstance(src, basestring):
        return copySingle(src, dest)

    if isinstance(src, dict):
        return copyMultiple(src)