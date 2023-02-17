# TODO:
# Handle errors (retrying, seeing if paid package)
# Allow device, unique id, firmware configuration

import os
import requests

class Downloader:
    url: str
    path: str
    headers: dict[str] = {
        "X-Machine": "iPhone10,6", # iPhone X
        "X-Unique-ID": "8843d7f92416211de9ebb963ff4ce28125932878", #from cydownload
        "X-Firmware": "14.3",
        "User-Agent": "Telesphoreo APT-HTTP/1.0.592" #from cydownload
    }

    def __init__(self, repo_url: str, url_path: str, file_path: str | None = None):
        self.url = repo_url + url_path
        
        self.path = url_path if file_path == None else file_path
        folder = os.path.dirname(self.path)
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    def download(self) -> None:
        #todo: maybe add int(time) at start & end & grab size response header
        # to make mb/s average?
        r = requests.get(self.url, headers=self.headers)

        if r.status_code != 200:
            #TODO: fix this
            print(r.status_code)
            input()

        open(self.path, "wb").write(r.content)
