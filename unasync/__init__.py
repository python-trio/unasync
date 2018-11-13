"""Top-level package for unasync."""

from ._version import __version__

from setuptools.command.build_py import build_py

import os
import tokenize as std_tokenize
from tokenize import NAME, NEWLINE, NL, STRING, ENCODING

ASYNC_TO_SYNC = {
    '__aenter__': '__enter__',
    '__aexit__': '__exit__',
    '__aiter__': '__iter__',
    '__anext__': '__next__',
    # TODO StopIteration is still accepted in Python 2, but the right change
    # is 'raise StopAsyncIteration' -> 'return' since we want to use unasynced
    # code in Python 3.7+
    'StopAsyncIteration': 'StopIteration',
}


def tokenize(f):
    last_end = (1, 0)
    for tok in std_tokenize.tokenize(f.readline):
        if tok.type == ENCODING:
            continue

        if last_end[0] < tok.start[0]:
            yield ('', STRING, ' \\\n')
            last_end = (tok.start[0], 0)

        space = ''
        if tok.start > last_end:
            assert tok.start[0] == last_end[0]
            space = ' ' * (tok.start[1] - last_end[1])
        yield (space, tok.type, tok.string)

        last_end = tok.end
        if tok.type in [NEWLINE, NL]:
            last_end = (tok.end[0] + 1, 0)


def unasync_tokens(tokens):
    # TODO __await__, ...?
    used_space = None
    for space, toknum, tokval in tokens:
        if tokval in ["async", "await"]:
            # When removing async or await, we want to use the whitespace that
            # was before async/await before the next token so that
            # `print(await stuff)` becomes `print(stuff)` and not
            # `print( stuff)`
            used_space = space
        else:
            if toknum == NAME and tokval in ASYNC_TO_SYNC:
                tokval = ASYNC_TO_SYNC[tokval]
            if used_space is None:
                used_space = space
            yield (used_space, tokval)
            used_space = None


def untokenize(tokens):
    return ''.join(space + tokval for space, tokval in tokens)


def unasync_file(filepath, fromdir, todir):
    with open(filepath, 'rb') as f:
        encoding, _ = std_tokenize.detect_encoding(f.readline)
        f.seek(0)
        tokens = tokenize(f)
        tokens = unasync_tokens(tokens)
        result = untokenize(tokens)
        outfilepath = filepath.replace(fromdir, todir)
        os.makedirs(os.path.dirname(outfilepath), exist_ok=True)
        with open(outfilepath, 'w', encoding=encoding) as f:
            print(result, file=f, end='')


class build_py(build_py):
    """
    Convert files in _async dir from being asynchronous to synchronous
    and saves them in _sync dir.
    """

    def run(self):
        self._updated_files = []

        # Base class code
        if self.py_modules:
            self.build_modules()
        if self.packages:
            self.build_packages()
            self.build_package_data()

        for f in self._updated_files:
            if os.sep + '_async' + os.sep in f:
                unasync_file(f, '_async', '_sync')

        # Remaining base class code
        self.byte_compile(self.get_outputs(include_bytecode=0))

    def build_module(self, module, module_file, package):
        outfile, copied = super().build_module(module, module_file, package)
        if copied:
            self._updated_files.append(outfile)
        return outfile, copied
