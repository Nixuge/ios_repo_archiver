import hashlib
import os
import shutil

import requests
from utils.downloaders.result import Result
from utils.downloaders.tweak._tweak_base import _TweakDownloaderBase
from utils.stringutils import random_string
from utils.vars.file import Folder, get_create_path

class TweakDownloader(_TweakDownloaderBase):
    def download(self) -> Result:
        #todo: maybe add int(time) at start & end & grab size response header
        # to make mb/s average?

        temp_filename = random_string()
        md5 = hashlib.md5()

        with requests.get(self.url, headers=self.headers, stream=True) as r:
            # r.raise_for_status()
            # we don't want to allow redirects or anything here, only 200s
            # redirect = usually paid package (see Chariz)
            if r.status_code != 200:
                return Result(status_code=r.status_code, hash_check=False, temp_filename=temp_filename)

            with open(temp_filename, 'wb') as f:
                # Files are often either very small or "very big"
                # 4KiB seems like a good middle ground
                for chunk in r.iter_content(chunk_size=4096):
                    md5.update(chunk)
                    f.write(chunk)

        md5 = md5.hexdigest()

        folder = get_create_path(Folder.debs, md5)
        full_path = f"{folder}/{md5}.deb"

        if not self._hash_match(temp_filename, md5):
            return Result(hash_check=False, temp_filename=temp_filename)

        if os.path.isfile(full_path):
            return Result(hash=full_path, temp_filename=temp_filename, already_exists=True, finished=True)


        if not os.path.exists(folder):
            os.makedirs(folder)
        
        
        shutil.move(temp_filename, full_path)

        return Result(hash=md5, finished=True)
