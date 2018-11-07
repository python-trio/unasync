class TestImplementation:
    def __iter__(self):
        return 1

    def __next__(self):
        raise StopIteration
