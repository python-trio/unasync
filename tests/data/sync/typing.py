import typing

typing.Iterable[bytes]
typing.Iterator[bytes]
typing.Generator[bytes]

# A typed function that takes the first item of an (a)sync iterator and returns it
def func1(a: typing.Iterable[int]) -> str:
    it: typing.Iterator[int] = a.__iter__()
    b: int = it.__next__()
    return str(b)


# Same as the above but using old-style typings (mainly for Python 2.7 – 3.5 compatibility)
def func2(a):  # type: (typing.Iterable[int]) -> str
    it = a.__iter__()  # type: typing.Iterator[int]
    b = it.__next__()  # type: int
    return str(b)


# And some funky edge cases to at least cover the relevant at all in this test
a: int = 5
b: str = a  # type: ignore  # This is the actual comment and the type declaration silences the warning that would otherwise happen
c: str = a  # type: ignore2  # This is the actual comment and the declaration declares another type, both of which are wrong

# fmt: off
# And some genuine trailing whitespace (uww…)
z = a  # type: int   
