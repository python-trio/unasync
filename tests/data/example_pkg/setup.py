import setuptools

import unasync

setuptools.setup(
    name="example_pkg",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A package used to test unasync",
    url="https://github.com/pypa/sampleproject",
    packages=["example_pkg", "example_pkg._async", "example_pkg._async.some_dir"],
    cmdclass={"build_py": unasync.build_py},
    package_dir={"": "src"},
)
