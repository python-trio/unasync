# isort: skip_file
# fmt: off
from common import (
a, b , c  # these should stick around
)

# these imports should be removed

CONST = 'foo'

def foo():
    print('this function should stick around')





class Foo:
    def foobar(self):
        print('This method should stick around')


    def another_method(self):
        print('This line should stick around')

# fmt: on
