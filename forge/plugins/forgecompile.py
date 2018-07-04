"""Compile module."""

# system
import os
import py_compile

# fs
from fs.copy import copy_fs, copy_file

# buildtools
from forge.utils.fs_utils import assertFS

class MissingDestinationException(Exception):
    """Missing destination exception."""

def compileFile(src, dest):
    """Compile src file to dest file.

    Args:
        src (basestring)
        dest (basestring)
    """

    assertFS(os.path.dirname(dest))

    py_compile.compile(src, dest)

def compileSingle(srcFS, src, destFS, dest):
    """Copy single source to single destination.

    Args:
        src (basestring)
        dest (basestring)

    Raises:
        MissingDestinationException
    """

    if dest is None:
        raise MissingDestinationException()

    if srcFS.exists(unicode(src)):
        if srcFS.isdir(unicode(src)):
            srcModuleFS = srcFS.opendir(unicode(src))
            destModuleFS = assertFS(destFS.getsyspath(unicode(dest)))

            for path in srcModuleFS.walk.files(filter=['*.py']):
                filename, extension = os.path.splitext(path)

                compiledPath = filename + ".pyc"

                compileFile(srcModuleFS.getsyspath(unicode(path)), destModuleFS.getsyspath(unicode(compiledPath)))

        if srcFS.isfile(unicode(src)):
            compileFile(srcFS.getsyspath(unicode(src)), destFS.getsyspath(unicode(dest)))

def compileMultiple(srcFS, data, destFS):
    """Copy multiple sources to multiple destinations.

    Args:
        data (dict)
    """

    for src, dest in data.iteritems():
        compileSingle(srcFS, src, destFS, dest)

def compileSrc(src, dest=None):
    if isinstance(src, basestring):
        def compileSingleWrapper(srcFS, destFS):
            compileSingle(srcFS, src, destFS, dest)

        return compileSingleWrapper

    if isinstance(src, dict):
        def compileMultipleWrapper(srcFS, destFS):
            compileMultiple(srcFS, src, destFS)

        return compileMultipleWrapper