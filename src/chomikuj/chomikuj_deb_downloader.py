
import asyncio
import hashlib
import json
import os
from pprint import pprint
import shutil
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

from asyncio import Task
from chomikuj.async_limiter import AsyncLimiter
from chomikuj.data.chomikuj_data import DbVarsChomikuj, Endpoints, RequestData
from chomikuj.data.chomikuj_file import ChomikujFile
from chomikuj.data.chomikuj_utils import ChomikujUtils
from database.queries import QueriesChomikuj

from utils.stringutils import random_string
from utils.vars.file import Folder, get_create_path

class ChomikujDebDownloader(AsyncLimiter):
    def __init__(self) -> None:
        super().__init__(self.download_deb, max_task_count=30, polling_sleep=.05)
        # super().__init__(self.download_deb, max_task_count=1)

    def _add_to_sql(self, file: ChomikujFile, md5: str):
        if ChomikujUtils.contains_md5(md5):
            print(f"WARNING! contains md5 but file not registered ! ({file.filepath})")
            return
        
        DbVarsChomikuj.Queue.add_instuction(
            QueriesChomikuj.get_insert_query(),
            (file.bundle_id, file.version, file.filename, file.size, md5)
        )

    async def download_deb(self, file: ChomikujFile):
        if ChomikujUtils.contains_package(file):
            return True # Already downloaded

        client = httpx.AsyncClient()

        # ===== Getting the direct download URL =====
        try:
            r_post = await client.post(
                Endpoints.download,
                data={
                    "fileId": file.id, 
                    RequestData.token_key: RequestData.token_value
                },
                headers=RequestData.headers
            )
        except:
            return self.fail(file)
        if r_post.status_code != 200 or "Niestety podczas przetwarzania" in r_post.text:
            return self.fail(file)

        try:
            data_dict = json.loads(r_post.text)
            url = data_dict["redirectUrl"]
        except:
            print("Error while loading json data! Possibly unhandled error !")
            print(r_post.text)
            return self.fail(file)

        # ===== Downloading the actual file =====
        try:
            r_get = await client.get(url)
        except:
            return self.fail(file)
        if r_post.status_code != 200:
            return self.fail(file)
        
        temp_filename = random_string()
        md5 = hashlib.md5()
        with open(temp_filename, 'wb') as f:
            for chunk in r_get.iter_bytes(chunk_size=4096):
                md5.update(chunk)
                f.write(chunk)

        # ===== other checks, metadata things & moving the file =====
        md5 = md5.hexdigest()

        file.set_size(os.stat(temp_filename).st_size)

        folder = get_create_path(Folder.debs, md5)
        full_path = f"{folder}/{md5}.deb"
        
        if os.path.isfile(full_path):
            self._add_to_sql(file, md5)
            os.remove(temp_filename)
            return True
    
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        shutil.move(temp_filename, full_path)

        self._add_to_sql(file, md5)

        return True

async def main():
    dler = ChomikujDebDownloader()
    # files = await dler.get_files_from_page(0)
    # await dler.download_deb(files[0]) # type: ignore
    # page_html = await get_files_from_page(get_last_page())


if __name__ == "__main__":
    asyncio.run(main())
