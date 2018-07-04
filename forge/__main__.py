# system
import sys
import importlib

# fs
from fs.osfs import OSFS

def main(arguments):
    cwdFS = OSFS(unicode("."))

    try:
        # my packages
        sys.path.append(cwdFS.getsyspath(unicode(".")))

        build = importlib.import_module("build")

        if hasattr(build, "config"):
            config = getattr(build, "config")

            for argument in arguments:
                if hasattr(build, argument):
                    method = getattr(build, argument)

                    method(config)()

    except ImportError as e:
        raise e

if __name__ == '__main__':
    # main(sys.argv)
    print "hello world"