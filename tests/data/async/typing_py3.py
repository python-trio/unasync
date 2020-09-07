# fmt: off
# A forward-reference typed function that returns an iterator for an (a)sync iterable
async def aiter1(a: "typing.AsyncIterable[int]") -> 'typing.AsyncIterable[int]':
	return a.__aiter__()

# Same as the above but using tripple-quoted strings
async def aiter2(a: """typing.AsyncIterable[int]""") -> r'''typing.AsyncIterable[int]''':
	return a.__aiter__()

# Same as the above but without forward-references
async def aiter3(a: typing.AsyncIterable[int]) -> typing.AsyncIterable[int]:
	return a.__aiter__()
# fmt: on
