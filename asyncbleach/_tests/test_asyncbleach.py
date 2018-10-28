import os
import tempfile

import asyncbleach


def test_asyncbleach():
    with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory(
    ) as tmpdir2:
        with open(os.path.join(tmpdir1, "source.py"), 'w') as f:
            f.write("async def f(): return await 1 \n")

        print(os.path.join(tmpdir1, "source.py"))

        asyncbleach.bleach(
            os.path.join(tmpdir1, "source.py"), fromdir=tmpdir1, todir=tmpdir2
        )

        with open(os.path.join(tmpdir2, "source.py")) as f:

            bleached_code = f.read()
            assert bleached_code == "def f(): return 1 \n"
