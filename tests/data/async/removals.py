# isort: skip_file
# fmt: off
from common import (
a, b , c  # these should stick around
)

# these imports should be removed
from async_only import ( # unasync: remove
    async_a, async_b,
    async_c
)

CONST = 'foo'
ASYNC_CONST = 'bar'  # unasync: remove

async def foo():
    print('this function should stick around')

async def async_only(): # unasync: remove
    print('this function will be removed entirely')


class AsyncOnly: # unasync: remove
    async def foo(self):
        print('the entire class should be removed')


class Foo:
    async def foobar(self):
        print('This method should stick around')

    async def async_only_method(self): # unasync: remove
        print('only this method should be removed')

    async def another_method(self):
        print('This line should stick around')
        await self.something("the content in this line should be removed")  # unasync: remove

# fmt: on
