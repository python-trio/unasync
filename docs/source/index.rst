.. documentation master file, created by
   sphinx-quickstart on Sat Jan 21 19:11:14 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


=======
unasync
=======

The unasync project's goal is to produce a `permissively licensed <https://github.com/python-trio/unasync/blob/master/LICENSE>`__,
tool that gives you the ability to transform your
asynchronous code into synchronous code.

---------------------
Why are we doing it ?
---------------------

You can find the whole discussion `here <https://github.com/urllib3/urllib3/pull/1335/>`__.

In short the TLDR; version is, Unasync gives you the ability to transform your asynchronous code
placed in **_async** directory into into synchronous code and put it in directory named **_sync**  i.e

.. code-block:: python

   async def f():
      return await 1


will be transformed and placed in directory **_sync**

.. code-block:: python

   def f():
      return 1

------------
Installation
------------

::

    pip install unasync

-----
Usage
-----

To use the unasync project you need to install the package and then create a **_async** folder where you will place the asynchronous code that you want to transform into synchronous code.

And then in your :code:`setup.py` place the following code.

.. code-block:: python

    import unasync

    setuptools.setup(
        ...
        cmdclass={'build_py': unasync.build_py},
        ...
    )

Then create a file **pyproject.toml** in the root of your project and mention **unasync** as one of your build dependency.

.. code-block:: text

    [build-system]
    requires = ["setuptools>=40.6.2", "wheel", "unasync"]
    build-backend = "setuptools.build_meta"

And when you will build your package you will get your synchronous code in **_sync** folder.


.. toctree::
   :maxdepth: 2

   history.rst

====================
 Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* :ref:`glossary`
