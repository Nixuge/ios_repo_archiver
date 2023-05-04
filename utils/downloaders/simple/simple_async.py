import hashlib
import os

import httpx
from utils.downloaders.result import Result
from utils.downloaders.simple._simple_base import _SimpleDownloaderBase
from utils.vars.file import get_create_path


class SimpleDownloaderAsync(_SimpleDownloaderBase):
    async def download_async(self, folder: str) -> Result:
        if not self.url:
            return Result(valid_url=False)
    
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            return Result(valid_url=False)

        r: httpx.Response
        
        try:
            r = await httpx.AsyncClient().get(self.url, headers=self.headers, follow_redirects=True)
        except httpx._exceptions.ConnectError:
            return Result(valid_url=False)
        
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
