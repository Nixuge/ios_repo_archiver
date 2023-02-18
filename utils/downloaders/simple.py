# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib
import os
import requests
import shutil

from utils.vars import DLF

class Downloader:
    url: str

    headers: dict[str, str] = {
        "X-Machine": "iPhone10,6", # iPhone X
        "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878", #from cydownload
        "X-Firmware": "14.3",
        "User-Agent": "Sileo/2.3 CoreFoundation/1770.300 Darwin/20.2.0"
    }

    def __init__(self, url: str):
        self.url = url
    

    def download(self, folder: str, extension: str) -> tuple[int, str | None]:
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            return r.status_code, None

        md5 = hashlib.md5(r.content).hexdigest()

        with open(folder + md5 + extension, 'wb') as f:
            f.write(r.content)

        return 200, md5
