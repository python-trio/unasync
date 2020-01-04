class AsyncLock:
    ...


class AsyncSocket:
    def __init__(self, send_lock: AsyncLock):
        ...

    async def send_all(self, data: "AsyncData"):
        ...


class AsyncData:
    ...
