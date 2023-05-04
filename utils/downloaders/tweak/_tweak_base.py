# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import hashlib

class _TweakDownloaderBase:
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