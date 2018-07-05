"""Eggify module."""

# system
import os
import subprocess

# fs
from fs.osfs import OSFS
from fs.copy import copy_fs, copy_file

# buildtools
from forge.utils.fs_utils import assertFS, emptyFS

class MissingDestinationException(Exception):
    """Missing destination exception."""

def eggifySingle(srcFS, src, destFS, dest):
    """ Eggify single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    if dest is None:
        raise MissingDestinationException()

    if src.startswith("/"):
        head, tail = os.path.split(src)

        srcFS = OSFS(head)
        src = tail

    if srcFS.isfile(unicode(src)):
        emptyFS(destFS, dest)
        assertFS(destFS.getsyspath(unicode(dest)))

        workingDir = srcFS.getsyspath(unicode("/"))

        subprocess.check_call(["python", src, "bdist_egg"], cwd=workingDir)
    
        if srcFS.isdir(unicode("dist")):
            distFS = srcFS.opendir(unicode("dist"))

            for name in reversed(sorted(distFS.listdir("/"))):
                if name.endswith(".egg"):
                    copy_file(distFS, unicode(name), destFS, unicode("{}/{}".format(dest, name)))

                    break

def eggifyMultiple(srcFS, data, destFS):
    """ Eggify multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    for src, dest in data.iteritems():
        eggifySingle(srcFS, src, destFS, dest)

def eggifySrc(src, dest=None):
    if isinstance(src, basestring):
        def eggifySingleWrapper(srcFS, destFS):
            eggifySingle(srcFS, src, destFS, dest)

        return eggifySingleWrapper

    if isinstance(src, dict):
        def eggifyMultipleWrapper(srcFS, destFS):
            eggifyMultiple(srcFS, src, destFS)

        return eggifyMultipleWrapper