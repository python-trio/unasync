import copy
import io
import os
import shutil
import subprocess

import pytest
# Needed to get tempfile.TemporaryDirectory in Python 2
from backports import tempfile

import unasync

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ASYNC_DIR = os.path.join(TEST_DIR, "async")
SYNC_DIR = os.path.join(TEST_DIR, "sync")
TEST_FILES = sorted([f for f in os.listdir(ASYNC_DIR) if f.endswith(".py")])


@pytest.mark.parametrize("source_file", TEST_FILES)
def test_unasync(source_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        unasync.unasync_file(
            os.path.join(ASYNC_DIR, source_file), fromdir=ASYNC_DIR, todir=tmpdir
        )

        encoding = 'latin-1' if 'encoding' in source_file else 'utf-8'
        with io.open(os.path.join(SYNC_DIR, source_file), encoding=encoding) as f:
            truth = f.read()
        with io.open(os.path.join(tmpdir, source_file), encoding=encoding) as f:
            unasynced_code = f.read()
            assert unasynced_code == truth


def test_build_py():
    with tempfile.TemporaryDirectory() as tmpdir:
        source_pkg_dir = os.path.join(TEST_DIR, "example_pkg")
        pkg_dir = os.path.join(tmpdir, "example_pkg")
        shutil.copytree(source_pkg_dir, pkg_dir)

        env = copy.copy(os.environ)
        env["PYTHONPATH"] = os.path.realpath(os.path.join(TEST_DIR, ".."))
        subprocess.check_call(["python", "setup.py", "build"], cwd=pkg_dir, env=env)

        unasynced = os.path.join(pkg_dir, "build/lib/example_pkg/_sync/__init__.py")
        with open(unasynced) as f:
            unasynced_code = f.read()
            assert unasynced_code == "def f():\n    return 1\n"
