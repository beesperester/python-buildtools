"""Eggify module."""

# system
import os
import subprocess
import re

# fs
from fs.osfs import OSFS
from fs.zipfs import ZipFS
from fs.tempfs import TempFS
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

def eggifySingle(srcFS, src, destFS, dest, config=None):
    """ Eggify single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    if dest is None:
        raise MissingDestinationException()

    if config is None:
        config = {}

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

                    eggSrcPath = distFS.getsyspath(unicode(name))
                    eggDestPath = destEggFS.getsyspath(unicode(name))

                    # create new temp filesystem
                    tempFS = TempFS()
                    eggFS = ZipFS(eggSrcPath)

                    # copy egg contents to temp filesystem
                    copy_fs(eggFS, tempFS)

                    # purge source files
                    if "purge" in config.keys() and config["purge"]:                        
                        for path in tempFS.walk.files(filter=["*.py"]):
                            tempFS.remove(path)

                    with ZipFS(eggDestPath, write=True) as destEggZipFS:
                        copy_fs(tempFS, destEggZipFS)

                    print "copied {} to {}".format(eggSrcPath, eggDestPath)

                    break

def eggifyMultiple(srcFS, data, destFS, config=None):
    """ Eggify multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    for src, dest in data.iteritems():
        eggifySingle(srcFS, src, destFS, dest, config)

def eggifySrc(src, dest=None, **kwargs):
    config = None

    if "config" in kwargs.keys():
        config = kwargs["config"]

    if isinstance(src, basestring):
        def eggifySingleWrapper(srcFS, destFS):
            eggifySingle(srcFS, src, destFS, dest, config)

        return eggifySingleWrapper

    if isinstance(src, dict):
        def eggifyMultipleWrapper(srcFS, destFS):
            eggifyMultiple(srcFS, src, destFS, config)

        return eggifyMultipleWrapper