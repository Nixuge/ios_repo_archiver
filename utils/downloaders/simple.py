# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib
import os
import requests
from utils.downloaders.result import Result
import mimetypes

from utils.file import get_create_path

class Downloader:
    url: str | None
    extension: str

    headers: dict[str, str] = {
        "X-Machine": "iPhone10,6",  # iPhone X
        "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878",  # from cydownload
        "X-Firmware": "14.3",
        "User-Agent": "Sileo/2.3 CoreFoundation/1770.300 Darwin/20.2.0"
    }

    default_extension: str = ".html"

    def __init__(self, url: str):
        self.url = url if url.startswith("https://") or url.startswith("http://") else None
        # if HTML, only saving the actual HTML and no CSS/anything else
        # TODO: download E V E R Y T H I N G

    # extension grabbing verbose
    # because otherwise it's buggy
    def _grab_ext_from_mime(self, content_type: str | None) -> str:
        if not content_type:
            return self.default_extension
        
        ext = mimetypes.guess_extension(content_type)

        return ext if ext != None else self.default_extension

    def _grab_ext(self, folder: str, content_type: str | None) -> str:
        if "moderndepiction" in folder:
            ext = ".json"
        elif "depiction" in folder:
            ext = ".html"
        else:
            ext = self._grab_ext_from_mime(content_type)
        return ext

    def download(self, folder: str) -> Result:
        if not self.url:
            return Result(valid_url=False)
    
        r = requests.get(self.url, headers=self.headers)
        if r.status_code != 200:
            return Result(status_code=r.status_code)

        ext = self._grab_ext(folder, r.headers.get("content-type"))

        md5 = hashlib.md5(r.content).hexdigest()

        folder = get_create_path(folder, md5)
        filename = folder + md5 + ext

        if os.path.isfile(filename):
            return Result(hash=md5, already_exists=True, finished=True)

        with open(filename, 'wb') as f:
            f.write(r.content)

        return Result(hash=md5, finished=True)
