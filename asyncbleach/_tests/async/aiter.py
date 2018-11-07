class TestImplementation:
    async def __aiter__(self):
        return await 1

    async def __anext__(self):
        raise StopAsyncIteration
