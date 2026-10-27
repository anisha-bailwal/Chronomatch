from setuptools import setup
from Cython.Build import cythonize

setup(
    name="ChronosMatch",
    ext_modules=cythonize(
        ["src/matching_engine.py"],
        compiler_directives={"language_level": "3"},
    ),
)