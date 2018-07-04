# system
import os

# fs
from fs.osfs import OSFS

# buildtools
from forge.utils.fs_utils import assertFS

def GetSrcFS(config):
    return OSFS(unicode(config["src"]))

def GetDestFS(config):
    destinations = config["dest"]

    # create list of destinations
    if not isinstance(destinations, list):
        destinations = [destinations]

    def osFilter(path):
        if os.name == "nt":
            return path[1] == ":"
        else:
            return path.startswith("/")

    filteredDestinations = filter(osFilter, destinations)

    return [assertFS(x) for x in filteredDestinations]

def buildSrc(config):
    def buildWrapper():
        srcFS = GetSrcFS(config)
        destinations = GetDestFS(config)

        if "plugins" in config.keys():
            for destFS in destinations:
                for cmd in config["plugins"]:
                    cmd(srcFS, destFS)

    return buildWrapper