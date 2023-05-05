
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
from chomikuj.data.chomikuj_data import Endpoints, RequestData
from chomikuj.data.chomikuj_file import ChomikujFile

from utils.stringutils import random_string
from utils.vars.file import Folder, get_create_path

class ChomikujDownloader:
    last_page: int
    tasks: list[Task]
    downloaded_pages: list[int]
    remaining_pages: list[int]
    failed_pages: list[int]
    max_tasks: int

    def __init__(self, max_tasks: int = 5) -> None:
        self._get_last_page()
        self.downloaded_pages = []
        self.remaining_pages = []
        self.failed_pages = []
        self.tasks = []
        self.max_tasks = max_tasks
    
    def _get_last_page(self) -> None:
        r = httpx.get(Endpoints.files_last_page, follow_redirects=True)
        if r.status_code != 200:
            print(f"EXCEPTION HAPPENED! code:{r.status_code} (not handling as not getting this should crash)")

        # URL redirects to same as Endpoints.last_page but with ,9999 replaced by max page num
        self.last_page = int(str(r.url).split(",")[-1])
        print(f"Max Chomikuj page number: {self.last_page}")

    def _bs_get_chomikuj_filelist_from_page(self, soup: BeautifulSoup) -> list[ChomikujFile]:
        # get the listview element to avoid grabbing other elements on the side of the page
        list_view: Tag = soup.find("div", {"id": "listView"}) # type: ignore

        # get all of the elements
        fileItemContainerList: list[Tag] = list_view.find_all("div", {"class": "fileItemContainer"})

        return [self._bs_get_chomikuj_file(fileItemContainer) for fileItemContainer in fileItemContainerList]

    @staticmethod
    def _bs_get_chomikuj_file(fileItemContainer: Tag) -> ChomikujFile:
        info_list = fileItemContainer.find("div", {"class": "fileinfo"}).find("ul") # type: ignore
        # list has 2 lis w spans inside, first is the size & second is the date
        size, date = info_list.find_all("span") # type: ignore
        
        download_element: Tag = fileItemContainer.find("a", {"class": "expanderHeader downloadAction downloadContext"}) # type: ignore
        
        path: str = download_element.get("href") # type: ignore

        return ChomikujFile(
            filename=download_element.find("span").text, # type: ignore
            filepath=path,
            filesize=size,
            date_added=date
        )

    async def get_files_from_page(self, page: int) -> list[ChomikujFile] | None:
        endpoint = f"{Endpoints.files_page},{page}" if page > 1 else Endpoints.files_page
        try:
            r = await httpx.AsyncClient().get(endpoint)
        except:
            print("Error grabbing page (httpx exception)")
            self.failed_pages.append(page)
            return
        if r.status_code != 200:
            print(f"Error grabbing page (error code: {r.status_code})")
            self.failed_pages.append(page)
            return

        soup = BeautifulSoup(r.text, "lxml")

        files = self._bs_get_chomikuj_filelist_from_page(soup)
       
        return files

    async def download_deb(self, file: ChomikujFile):
        print("Starting download...")
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
            return False
        if r_post.status_code != 200 or "Niestety podczas przetwarzania" in r_post.text:
            return False

        data_dict = json.loads(r_post.text)
        url = data_dict.get("redirectUrl")

        # ===== Downloading the actual file =====
        try:
            r_get = await client.get(url)
        except:
            return False
        if r_post.status_code != 200:
            return False
        
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
            return True
    
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        shutil.move(temp_filename, full_path)
        
        return True

async def main():
    dler = ChomikujDownloader()
    files = await dler.get_files_from_page(0)
    await dler.download_deb(files[0]) # type: ignore
    # page_html = await get_files_from_page(get_last_page())


if __name__ == "__main__":
    asyncio.run(main())
