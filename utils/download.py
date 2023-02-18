import requests

def download_bytes(url: str) -> bytes:
    return requests.get(url).content

def download_str(url: str) -> str:
    return download_bytes(url).decode()
