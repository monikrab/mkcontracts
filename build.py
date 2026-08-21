# Run with:
# python3 build.py build_ext

from os import environ, path
from setuptools.command.build_ext import build_ext
from shutil import rmtree
from setuptools import setup, Extension
from Cython.Build import cythonize
from subprocess import run
from pathlib import Path


# Reduce the binary's size
environ["CFLAGS"] = environ.get("CFLAGS", "") + (
    " -Os -fomit-frame-pointer "
    " -ffunction-sections -fdata-sections "
    " -fvisibility=hidden "
    " -fno-common "
    " -DNDEBUG "
    " -DPy_LIMITED_API=0x030A0000"
)
environ["LDFLAGS"] = environ.get("LDFLAGS", "") + (
    " -s "
    " -Wl,--gc-sections "
    " -Wl,-O1 "
    " -Wl,--as-needed "
    " -Wl,--strip-all "
    " -Wl,-Bsymbolic"
)


class Build(build_ext):
    def run(self):
        self.build_lib = self.build_temp = "bin/"

        # Remove previous build objs on rebuild
        if path.exists(self.build_temp):
            rmtree(self.build_temp)

        super().run()


setup(
    ext_modules = cythonize(
        Extension("mkontracts", ["src/mkontracts.py"]),
        compiler_directives={'language_level': "3"}
    ),
    cmdclass = {'build_ext': Build}
)


run(["mv", next(Path("bin").glob("mkontracts*.so"), None), "bin/mkcontracts.so"])
