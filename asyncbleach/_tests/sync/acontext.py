class TestImplementation:
    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
