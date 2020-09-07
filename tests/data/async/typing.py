import typing

typing.AsyncIterable[bytes]
typing.AsyncIterator[bytes]
typing.AsyncGenerator[bytes]

# A typed function that takes the first item of an (a)sync iterator and returns it
async def func1(a: typing.AsyncIterable[int]) -> str:
    it: typing.AsyncIterator[int] = a.__aiter__()
    b: int = await it.__anext__()
    return str(b)


# Same as the above but using old-style typings (mainly for Python 2.7 – 3.5 compatibility)
async def func2(a):  # type: (typing.AsyncIterable[int]) -> str
    it = a.__aiter__()  # type: typing.AsyncIterator[int]
    b = await it.__anext__()  # type: int
    return str(b)


# And some funky edge cases to at least cover the relevant at all in this test
a: int = 5
b: str = a  # type: ignore  # This is the actual comment and the type declaration silences the warning that would otherwise happen
c: str = a  # type: ignore2  # This is the actual comment and the declaration declares another type, both of which are wrong

# fmt: off
# And some genuine trailing whitespace (uww…)
z = a  # type: int   
