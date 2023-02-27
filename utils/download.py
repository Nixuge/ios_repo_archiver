import requests

headers: dict[str, str] = {
    "X-Machine": "iPhone10,6", # iPhone X
    "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878", #from cydownload
    "X-Firmware": "14.3",
    "User-Agent": "Telesphoreo APT-HTTP/1.0.592" #from cydownload
}

#TODO: diff functions for headers & allow redirects
def download_bytes(url: str) -> tuple[bytes, int]:
    r = requests.get(url, headers=headers, allow_redirects=False)
    return r.content, r.status_code

def download_str(url: str) -> str:
    return download_bytes(url)[0].decode()

# unused
def download_str_code(url: str) -> tuple[str, int]:
    dl, code = download_bytes(url)
    return dl.decode(), code
