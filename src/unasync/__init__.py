"""Top-level package for unasync."""

from __future__ import print_function

import collections
import errno
import os
import sys
import tokenize as std_tokenize

from setuptools.command import build_py as orig

from ._version import __version__  # NOQA

__all__ = [
    "Rule",
    "unasync_files",
    "cmdclass_build_py",
]


_ASYNC_TO_SYNC = {
    "__aenter__": "__enter__",
    "__aexit__": "__exit__",
    "__aiter__": "__iter__",
    "__anext__": "__next__",
    "asynccontextmanager": "contextmanager",
    "AsyncIterable": "Iterable",
    "AsyncIterator": "Iterator",
    "AsyncGenerator": "Generator",
    # TODO StopIteration is still accepted in Python 2, but the right change
    # is 'raise StopAsyncIteration' -> 'return' since we want to use unasynced
    # code in Python 3.7+
    "StopAsyncIteration": "StopIteration",
}


class Rule:
    """A single set of rules for 'unasync'ing file(s)"""

    def __init__(self, fromdir, todir, additional_replacements=None):
        self.fromdir = fromdir.replace("/", os.sep)
        self.todir = todir.replace("/", os.sep)

        # Add any additional user-defined token replacements to our list.
        self.token_replacements = _ASYNC_TO_SYNC.copy()
        for key, val in (additional_replacements or {}).items():
            self.token_replacements[key] = val

    def _match(self, filepath):
        """Determines if a Rule matches a given filepath and if so
        returns a higher comparable value if the match is more specific.
        """
        file_segments = [x for x in filepath.split(os.sep) if x]
        from_segments = [x for x in self.fromdir.split(os.sep) if x]
        len_from_segments = len(from_segments)

        if len_from_segments > len(file_segments):
            return False

        for i in range(len(file_segments) - len_from_segments + 1):
            if file_segments[i : i + len_from_segments] == from_segments:
                return len_from_segments, i

        return False

    def _unasync_file(self, filepath):
        with open(filepath, "rb") as f:
            write_kwargs = {}
            if sys.version_info[0] >= 3:
                encoding, _ = std_tokenize.detect_encoding(f.readline)
                write_kwargs["encoding"] = encoding
                f.seek(0)
            tokens = _tokenize(f)
            tokens = self._unasync_tokens(tokens)
            result = _untokenize(tokens)
            outfilepath = filepath.replace(self.fromdir, self.todir)
            _makedirs_existok(os.path.dirname(outfilepath))
            with open(outfilepath, "w", **write_kwargs) as f:
                print(result, file=f, end="")

    def _unasync_tokens(self, tokens):
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
                if toknum == std_tokenize.NAME:
                    tokval = self._unasync_name(tokval)
                elif toknum == std_tokenize.STRING:
                    left_quote, name, right_quote = tokval[0], tokval[1:-1], tokval[-1]
                    tokval = left_quote + self._unasync_name(name) + right_quote
                if used_space is None:
                    used_space = space
                yield (used_space, tokval)
                used_space = None

    def _unasync_name(self, name):
        if name in self.token_replacements:
            return self.token_replacements[name]
        # Convert classes prefixed with 'Async' into 'Sync'
        elif len(name) > 5 and name.startswith("Async") and name[5].isupper():
            return "Sync" + name[5:]
        return name


def unasync_files(fpath_list, rules):
    for f in fpath_list:
        found_rule = None
        found_weight = None

        for rule in rules:
            weight = rule._match(f)
            if weight and (found_weight is None or weight > found_weight):
                found_rule = rule
                found_weight = weight

        if found_rule:
            found_rule._unasync_file(f)


Token = collections.namedtuple("Token", ["type", "string", "start", "end", "line"])


def _get_tokens(f):
    if sys.version_info[0] == 2:
        for tok in std_tokenize.generate_tokens(f.readline):
            type_, string, start, end, line = tok
            yield Token(type_, string, start, end, line)
    else:
        for tok in std_tokenize.tokenize(f.readline):
            if tok.type == std_tokenize.ENCODING:
                continue
            yield tok


def _tokenize(f):
    last_end = (1, 0)
    for tok in _get_tokens(f):
        if last_end[0] < tok.start[0]:
            yield ("", std_tokenize.STRING, " \\\n")
            last_end = (tok.start[0], 0)

        space = ""
        if tok.start > last_end:
            assert tok.start[0] == last_end[0]
            space = " " * (tok.start[1] - last_end[1])
        yield (space, tok.type, tok.string)

        last_end = tok.end
        if tok.type in [std_tokenize.NEWLINE, std_tokenize.NL]:
            last_end = (tok.end[0] + 1, 0)


def _untokenize(tokens):
    return "".join(space + tokval for space, tokval in tokens)


def _makedirs_existok(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


_DEFAULT_RULE = Rule(fromdir="/_async/", todir="/_sync/")


class _build_py(orig.build_py):
    """
    Subclass build_py from setuptools to modify its behavior.

    Convert files in _async dir from being asynchronous to synchronous
    and saves them in _sync dir.
    """

    UNASYNC_RULES = (_DEFAULT_RULE,)

    def run(self):
        rules = self.UNASYNC_RULES

        self._updated_files = []

        # Base class code
        if self.py_modules:
            self.build_modules()
        if self.packages:
            self.build_packages()
            self.build_package_data()

        # Our modification!
        unasync_files(self._updated_files, rules)

        # Remaining base class code
        self.byte_compile(self.get_outputs(include_bytecode=0))

    def build_module(self, module, module_file, package):
        outfile, copied = orig.build_py.build_module(self, module, module_file, package)
        if copied:
            self._updated_files.append(outfile)
        return outfile, copied


def cmdclass_build_py(rules=(_DEFAULT_RULE,)):
    """Creates a 'build_py' class for use within 'cmdclass={"build_py": ...}'"""

    class _custom_build_py(_build_py):
        UNASYNC_RULES = rules

    return _custom_build_py
