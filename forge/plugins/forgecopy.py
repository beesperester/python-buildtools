"""Copy module."""

# system
import os

# fs
from fs.copy import copy_fs, copy_file

# buildtools
from forge.utils.fs_utils import assertFS

class MissingDestinationException(Exception):
    """Missing destination exception."""

def copySingle(srcFS, src, destFS, dest):
    """Copy single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    if dest is None:
        raise MissingDestinationException()

    if srcFS.isdir(unicode(src)):
        assertFS(destFS.getsyspath(unicode(dest)))

        copy_fs(srcFS.opendir(unicode(src)), destFS.opendir(unicode(dest)))

    if srcFS.isfile(unicode(src)):
        assertFS(destFS.getsyspath(unicode(os.path.dirname(dest))))

        copy_file(srcFS, unicode(src), destFS, unicode(dest))    

def copyMultiple(srcFS, data, destFS):
    """Copy multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    for src, dest in data.iteritems():
        copySingle(srcFS, src, destFS, dest)

def copySrc(src, dest=None):
    if isinstance(src, basestring):
        def copySingleWrapper(srcFS, destFS):
            copySingle(srcFS, src, destFS, dest)

        return copySingleWrapper

    if isinstance(src, dict):
        def copyMultipleWrapper(srcFS, destFS):
            copyMultiple(srcFS, src, destFS)

        return copyMultipleWrapper