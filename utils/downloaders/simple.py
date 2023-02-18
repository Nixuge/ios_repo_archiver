# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib
import os
import requests
from utils.downloaders.result import Result


class Downloader:
    url: str
    extension: str

    headers: dict[str, str] = {
        "X-Machine": "iPhone10,6",  # iPhone X
        "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878",  # from cydownload
        "X-Firmware": "14.3",
        "User-Agent": "Sileo/2.3 CoreFoundation/1770.300 Darwin/20.2.0"
    }

    allowed_extensions = ("png", "jpg", "jpeg", "json", "html")

    def __init__(self, url: str):
        self.url = url
        # if HTML, only saving the actual HTML and no CSS/anything else
        if '.' not in url:
            self.extension = "html"
            return

        ext = url.split('.')[-1]

        if ext not in self.allowed_extensions:
            self.extension = "html"
            return

        self.extension = ext

    def download(self, folder: str) -> Result:
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            return Result(status_code=r.status_code)

        md5 = hashlib.md5(r.content).hexdigest()
        filename = folder + md5 + self.extension

        if os.path.isfile(filename):
            return Result(hash=md5, already_exists=True)

        with open(filename, 'wb') as f:
            f.write(r.content)

        return Result(hash=md5)
