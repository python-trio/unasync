import io

from setuptools import setup, find_packages

exec(io.open("src/unasync/_version.py", encoding="utf-8").read())

LONG_DESC = io.open("README.rst", encoding="utf-8").read()

setup(
    name="unasync",
    version=__version__,
    description="The async transformation code.",
    url="https://github.com/RatanShreshtha/unasync",
    long_description=LONG_DESC,
    long_description_content_type="text/x-rst",
    author="Ratan Kulshreshtha",
    author_email="ratan.shreshtha@gmail.com",
    license="MIT -or- Apache License 2.0",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[],
    keywords=["async"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
