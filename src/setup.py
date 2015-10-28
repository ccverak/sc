from distutils.core import setup
import py2exe

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "2.0.0",
    description = "sc",
    name = "sc",

    # targets to build
    console = ["sc.py"]
    )
