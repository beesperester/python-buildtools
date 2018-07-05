"""Eggify module."""

# system
import os
import subprocess
import re

# fs
from fs.osfs import OSFS
from fs.copy import copy_fs, copy_file

# buildtools
from forge.utils.fs_utils import assertFS

class MissingDestinationException(Exception):
    """Missing destination exception."""

def stripNumbers(string):
    """ Strip numbers from string.

    Args:
        string (basestring)
    """

    return re.sub(r"([0-9:\.]+)", "", string)

def removeOldEggs(fs, name):
    """ Remove old eggs.
        Strip version numbers from name string
        and remove matching existing eggs.

    Args:
        fs (fs)
        name (basestring)
    """

    for destName in fs.listdir(unicode("/")):
        if destName.endswith(".egg"):
            destNameStripped = stripNumbers(destName)
            nameStripped = stripNumbers(name)
            
            if destNameStripped == nameStripped:
                fs.remove(unicode(destName))

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
        assertFS(destFS.getsyspath(unicode(dest)))

        workingDir = srcFS.getsyspath(unicode("/"))
        devnull = open(os.devnull, 'w')

        subprocess.check_call(["python", src, "bdist_egg"], cwd=workingDir, stdout=devnull, stderr=devnull)
    
        if srcFS.isdir(unicode("dist")):
            distFS = srcFS.opendir(unicode("dist"))

            for name in reversed(sorted(distFS.listdir("/"))):
                if name.endswith(".egg"):
                    destEggFS = destFS.opendir(unicode(dest))

                    # remove existing eggs
                    removeOldEggs(destEggFS, name)

                    print "copy {} to {}".format(distFS.getsyspath(unicode(name)), destEggFS.getsyspath(unicode(name)))

                    copy_file(distFS, unicode(name), destEggFS, unicode(name))

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