"""FS utilities module."""

# system
import os

# fs
from fs.osfs import OSFS

def assertFS(path, remainder=None):
    """Assert existence of fs.
    Step up one path segment until the directory exists, create missing directories and return filesystem.

    Args:
        path (basestring)
        remainder (basestring)

    Returns:
        fs
    
    """

    if not os.path.isdir(path):
        head, tail = os.path.split(path)

        return assertFS(head, "/".join(filter(bool, [tail, remainder])))

    fs = OSFS(path)

    if remainder is not None:
        fs.makedirs(unicode(remainder))
        
        fs = fs.opendir(unicode(remainder))

    return fs

def emptyFS(fs, path):
    """ Empty path in filesystem.

    Args:
        fs (fs)
        path (string)
    """

    if fs.isdir(unicode(path)):
        fs.removetree(unicode(path))