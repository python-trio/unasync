from urllib3 import AsyncPoolManager


async def test_redirect(self):
    with AsyncPoolManager(backend="trio") as http:
        r = await http.request("GET", "/")
        assert r.status == 200
