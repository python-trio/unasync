import os
import tempfile

from setuptools import sandbox

import asyncbleach


def test_asyncbleach():
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory(
    ) as tmpdir2:
        with open(os.path.join(tmpdir1, "source.py"), 'w') as f:
            f.write("async def f(): return await 1 \n")


        asyncbleach.bleach(
            os.path.join(tmpdir1, "source.py"), fromdir=tmpdir1, todir=tmpdir2
        )

        with open(os.path.join(tmpdir2, "source.py")) as f:

            bleached_code = f.read()
            assert bleached_code == "def f(): return 1 \n"



def test_bleach_build_py():
    path_to_setup_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), './example_pkg/setup.py')
    sandbox.run_setup(path_to_setup_py, ['build'])
