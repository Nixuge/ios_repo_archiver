# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib
import os
import requests
import shutil
from utils.downloaders.result import Result
from utils.file import Folder, get_create_path

from utils.stringutils import random_string


class Downloader:
    url: str
    hashes: dict[str, str]

    headers: dict[str, str] = {
        "X-Machine": "iPhone10,6", # iPhone X
        "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878", #from cydownload
        "X-Firmware": "14.3",
        "User-Agent": "Telesphoreo APT-HTTP/1.0.592" #from cydownload
    }

    def __init__(self, repo_url: str, url_path: str, hashes: dict[str, str]):
        self.url = repo_url + url_path
        self.hashes = hashes
    
    @staticmethod
    def _make_hash(filename: str, hash_method) -> str:
        hash = hash_method()
        with open(filename, "rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                hash.update(byte_block)
        return hash.hexdigest()


    def _hash_match(self, filename: str, md5: str) -> bool:
        # bit verbose but good enough for readability
        # matches md5 first then sha256 then sha512
        # if the 1st checked matches, it passes anyways
        if "md5sum" in self.hashes:
            if self.hashes["md5sum"] != md5:
                return False
        elif "sha256" in self.hashes:
            sha256 = self._make_hash(filename, hashlib.sha256)
            if self.hashes["sha256"] != sha256:
                return False
        elif "sha512" in self.hashes:
            sha512 = self._make_hash(filename, hashlib.sha512)
            if self.hashes["sha512"] != sha512:
                return False
        else:
            return False
        
        return True


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
