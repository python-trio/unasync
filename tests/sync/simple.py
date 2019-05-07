class TestImplementation:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.s = "UTF-8: ❄"

    def get_a_b(self):
        s = "a is %s b is %s" % \
            (self.a,
            self.b)
        return s

    def f(self):
        return 1

def f():
    return 1
