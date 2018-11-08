class TestImplementation:
    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.close()
