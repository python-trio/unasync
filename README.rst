=======
unasync
=======

|documentation| |travis| |appveyor| |codecov|

.. |travis| image:: https://travis-ci.com/RatanShreshtha/unasync.svg?branch=master
    :alt: Travis Build Status
    :target: https://travis-ci.com/RatanShreshtha/unasync

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/sjw2q42mx7jvqbyp/branch/master?svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/RatanShreshtha/unasync

.. |codecov| image:: https://codecov.io/gh/RatanShreshtha/unasync/branch/master/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/RatanShreshtha/unasync

.. |documentation| image:: https://readthedocs.org/projects/unasync/badge/?version=latest
    :alt: Documentation Status
    :target: https://unasync.readthedocs.io/en/latest/?badge=latest


Welcome to `unasync <https://pypi.org/project/unasync/>`_, a project that can transform your asynchronous code into synchronous code.

Installation
============

::

    pip install unasync

Usage
=====

To use the unasync project you need to install the package and then create a **_async** where you will place the asynchronous code you want to transform into synchronous code.

And then in your :code:`setup.py` place the following code.

.. code-block:: python
    import unasync

    setuptools.setup(
        ...
        cmdclass={'build_py': unasync.build_py},
        ...
    )

And when you will build your package you will get your synchronous code in **_sync** folder.

Documentation
=============

https://unasync.readthedocs.io/en/latest/
