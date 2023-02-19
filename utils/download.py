import requests

def download_bytes(url: str) -> tuple[bytes, int]:
    r = requests.get(url)
    return r.content, r.status_code

def download_str(url: str) -> str:
    return download_bytes(url)[0].decode()

# unused
def download_str_code(url: str) -> tuple[str, int]:
    dl, code = download_bytes(url)
    return dl.decode(), code
