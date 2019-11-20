from urllib3 import PoolManager


def test_redirect(self):
    with PoolManager() as http:
        r = http.request("GET", "/")
        assert r.status == 200
