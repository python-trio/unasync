# fmt: off
# A forward-reference typed function that returns an iterator for an (a)sync iterable
def aiter1(a: "typing.Iterable[int]") -> 'typing.Iterable[int]':
	return a.__iter__()

# Same as the above but using tripple-quoted strings
def aiter2(a: """typing.Iterable[int]""") -> r'''typing.Iterable[int]''':
	return a.__iter__()

# Same as the above but without forward-references
def aiter3(a: typing.Iterable[int]) -> typing.Iterable[int]:
	return a.__iter__()
# fmt: on
