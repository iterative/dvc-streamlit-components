import importlib.util
import os

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

# Read package meta-data from version.py
# see https://packaging.python.org/guides/single-sourcing-package-version/
pkg_dir = os.path.dirname(os.path.abspath(__file__))
version_path = os.path.join(pkg_dir, "dvc_streamlit", "version.py")
spec = importlib.util.spec_from_file_location("dvc_streamlit.version", version_path)
dvclive_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dvclive_version)
version = dvclive_version.__version__


# To achieve consistency between the build version and the one provided
# by your package during runtime, you need to **pin** the build version.
#
# This custom class will replace the version.py module with a **static**
# `__version__` that your package can read at runtime, assuring consistency.
#
# References:
#   - https://docs.python.org/3.7/distutils/extending.html
#   - https://github.com/python/mypy
class build_py(_build_py):
    def pin_version(self):
        path = os.path.join(self.build_lib, "dvc_streamlit")
        self.mkpath(path)
        with open(os.path.join(path, "version.py"), "w") as fobj:
            fobj.write("# AUTOGENERATED at build time by setup.py\n")
            fobj.write('__version__ = "{}"\n'.format(version))

    def run(self):
        self.execute(self.pin_version, ())
        _build_py.run(self)

tests_requires = [
    "pytest>=6.0.1",
    "pre-commit"
]

setup(
    name="dvc_streamlit",
    version=version,
    author="David de la Iglesia Castro",
    author_email="diglesia@iterative.ai",
    packages=find_packages(exclude="tests"),
    description="Streamlit components for DVC.",
    long_description=open("README.md", "r", encoding="UTF-8").read(),
    python_requires=">=3.7",
    extras_require={
        "tests": tests_requires,
    },
    cmdclass={"build_py": build_py},
    url="https://github.com/iterative/dvc_streamlit",
    download_url="https://github.com/iterative/dvc_streamlit",
)