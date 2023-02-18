# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

from dataclasses import dataclass
import hashlib
import os
import requests
import shutil

from utils.stringutils import random_string


@dataclass
class Result:
    status_code: int
    hash_check: bool
    already_exists: bool
    hash: str | None

    def __init__(self, status_code: int = 200, hash_check: bool = True, 
                 already_exists: bool = False, hash: str | None = None,
                 temp_filename: str | None = None):
        self.status_code = status_code
        self.hash_check = hash_check
        self.already_exists = already_exists
        self.hash = hash
        if temp_filename:
            os.system(f"rm {temp_filename}")
        

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
        if "MD5Sum" in self.hashes:
            if self.hashes["MD5Sum"] != md5:
                return False
        elif "SHA256" in self.hashes:
            sha256 = self._make_hash(filename, hashlib.sha256)
            if self.hashes["SHA256"] != sha256:
                return False
        elif "SHA512" in self.hashes:
            sha512 = self._make_hash(filename, hashlib.sha512)
            if self.hashes["SHA512"] != sha512:
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

        folder = f"debs/{md5[0]}"
        full_path = f"{folder}/{md5}.deb"

        if not self._hash_match(temp_filename, md5):
            return Result(hash_check=False, temp_filename=temp_filename)

        if os.path.isfile(full_path):
            return Result(already_exists=True, hash=full_path, temp_filename=temp_filename)


        folder = f"debs/{md5[0]}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        shutil.move(temp_filename, full_path)

        return Result(hash=md5, temp_filename=temp_filename)
