class SyncLock:
    ...


class SyncSocket:
    def __init__(self, send_lock: SyncLock):
        ...

    def send_all(self, data: "SyncData"):
        ...


class SyncData:
    ...
