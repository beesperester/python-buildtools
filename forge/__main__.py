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

        forge = importlib.import_module("forge")

        if hasattr(forge, "config"):
            config = getattr(forge, "config")

            for argument in arguments:
                if hasattr(forge, argument):
                    method = getattr(forge, argument)

                    method(config)()

    except ImportError as e:
        raise e

if __name__ == '__main__':
    # main(sys.argv)
    print "hello world"