import setuptools

import unasync

setuptools.setup(
    name="ahip",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A package used to test customized unasync",
    url="https://github.com/pypa/sampleproject",
    packages=["ahip", "ahip.some_dir"],
    cmdclass={
        "build_py": unasync.customize_build_py(rename_dir_from_to=("ahip", "hip"))
    },
    package_dir={"": "src"},
)
