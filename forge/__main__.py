""" Main module. """

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

        forgeconfig = importlib.import_module("forgeconfig")

        if hasattr(forgeconfig, "config"):
            config = getattr(forgeconfig, "config")

            for argument in arguments:
                if hasattr(forgeconfig, argument):
                    method = getattr(forgeconfig, argument)

                    method(config)()

    except ImportError as e:
        raise e

if __name__ == '__main__':
    main(sys.argv)
