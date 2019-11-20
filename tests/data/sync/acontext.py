from contextlib import contextmanager


class TestImplementation:
    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    @contextmanager
    def context_manager(self):
        return self
