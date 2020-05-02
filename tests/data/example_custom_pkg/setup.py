import setuptools

import unasync

setuptools.setup(
    name="ahip",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A package used to test customized unasync",
    url="https://github.com/pypa/sampleproject",
    packages=["ahip", "ahip.some_dir", "ahip.tests"],
    cmdclass={
        "build_py": unasync.cmdclass_build_py(
            rules=[
                unasync.Rule(fromdir="/ahip/", todir="/hip/"),
                unasync.Rule(
                    fromdir="/ahip/tests/",
                    todir="/hip/tests/",
                    additional_replacements={"ahip": "hip"},
                ),
            ]
        )
    },
    package_dir={"": "src"},
)
