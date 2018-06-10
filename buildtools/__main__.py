# system
import os
import py_compile
import sys

# fs
from fs.copy import copy_fs, copy_file
from fs.osfs import OSFS

# buildtools
from copy import _copyItems
from compile import _compileItems

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

def compileFile(src, dest):
    assertFS(os.path.dirname(dest))

    py_compile.compile(src, dest)

def main():
    cwdFS = OSFS(u".")

    try:
        # my packages
        sys.path.append(cwdFS.getsyspath(u"."))

        import build

        config = build.export()

        srcFS = OSFS(unicode(config["src"]))
        destFS = assertFS(config["dest"])

        # plugins = config["plugins"]

        # copy items
        for src, dest in _copyItems:
            if srcFS.exists(unicode(src)):
                if srcFS.isdir(unicode(src)):
                    assertFS(destFS.getsyspath(unicode(dest)))

                    copy_fs(srcFS.opendir(unicode(src)), destFS.opendir(unicode(dest)))

                if srcFS.isfile(unicode(src)):
                    assertFS(destFS.getsyspath(unicode(os.path.dirname(dest))))

                    copy_file(srcFS, unicode(src), destFS, unicode(dest))

        # compile items
        for src, dest in _compileItems:
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
    except ImportError:
        pass

if __name__ == '__main__':
    main()