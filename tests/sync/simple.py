class TestImplementation:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.s = "UTF-8: ❄"

    def get_a_b(self):
        # fmt: off
        s = "a is %s b is %s" % \
            (self.a,
             self.b)
        # fmt: on
        return s

    def f(self):
        return 1


def f():
    return 1
