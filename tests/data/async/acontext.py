from contextlib import asynccontextmanager


class TestImplementation:
    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.close()

    @asynccontextmanager
    async def context_manager(self):
        return self
