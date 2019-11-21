import setuptools

import unasync

setuptools.setup(
    name="example_pkg",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A package used to test unasync",
    url="https://github.com/pypa/sampleproject",
    py_modules=["_async.some_file"],
    cmdclass={"build_py": unasync.build_py},
)
