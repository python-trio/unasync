from setuptools import find_packages, setup

exec(open("src/unasync/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="unasync",
    version=__version__,
    description="The async transformation code.",
    url="https://github.com/python-trio/unasync",
    long_description=LONG_DESC,
    long_description_content_type="text/x-rst",
    author="Ratan Kulshreshtha",
    author_email="ratan.shreshtha@gmail.com",
    license="MIT OR Apache-2.0",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["tokenize_rt", "setuptools"],
    keywords=["async"],
    python_requires=">=3.8",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
