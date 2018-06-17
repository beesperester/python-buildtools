# fs
from fs.osfs import OSFS

# buildtools
from utils.fs_utils import assertFS

def GetSrcFS(config):
    return OSFS(unicode(config["src"]))

def GetDestFS(config):
    return assertFS(config["dest"])

def buildSrc(config):
    def buildWrapper():
        srcFS = GetSrcFS(config)
        destFS = GetDestFS(config)

        if "plugins" in config.keys():
            for cmd in config["plugins"]:
                cmd(srcFS, destFS)

    return buildWrapper