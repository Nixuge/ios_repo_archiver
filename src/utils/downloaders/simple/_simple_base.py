# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib
import os
import requests
from utils.downloaders.result import Result
import mimetypes

from utils.vars.file import get_create_path

class _SimpleDownloaderBase:
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

