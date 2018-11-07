import os
import shutil
import tempfile

import pytest
from setuptools import sandbox

import asyncbleach

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ASYNC_DIR = os.path.join(TEST_DIR, "async")
SYNC_DIR = os.path.join(TEST_DIR, "sync")
TEST_FILES = sorted([f for f in os.listdir(ASYNC_DIR) if f.endswith(".py")])


@pytest.mark.parametrize('source_file', TEST_FILES)
def test_asyncbleach(source_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        asyncbleach.bleach(
            os.path.join(ASYNC_DIR, source_file),
            fromdir=ASYNC_DIR,
            todir=tmpdir
        )

        with open(os.path.join(SYNC_DIR, source_file)) as f:
            truth = f.read()
        with open(os.path.join(tmpdir, source_file)) as f:
            bleached_code = f.read()
            assert bleached_code == truth


def test_bleach_build_py():
    with tempfile.TemporaryDirectory() as tmpdir:
        source_pkg_dir = os.path.join(TEST_DIR, 'example_pkg')
        pkg_dir = os.path.join(tmpdir, 'example_pkg')
        shutil.copytree(source_pkg_dir, pkg_dir)

        path_to_setup_py = os.path.join(pkg_dir, 'setup.py')
        sandbox.run_setup(path_to_setup_py, ['build'])

        bleached = os.path.join(
            pkg_dir, 'build/lib/example_pkg/_sync/__init__.py'
        )
        with open(bleached) as f:
            bleached_code = f.read()
            assert bleached_code == "def f():\n    return 1\n"
