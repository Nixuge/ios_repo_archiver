
import asyncio
from typing_extensions import override
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

from asyncio import Task
from chomikuj.async_limiter import AsyncLimiter
from chomikuj.data.chomikuj_data import Endpoints
from chomikuj.data.chomikuj_file import ChomikujFile

class ChomikujPageParser(AsyncLimiter):
    last_page: int
    files: list[ChomikujFile]

    def __init__(self) -> None:
        super().__init__(self.get_files_from_page, max_task_count=50)
        self.files = []
        self._get_last_page()
        self.remaining_elements = list(range(1, self.last_page+1))
    
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

    async def get_files_from_page(self, page: int):
        endpoint = f"{Endpoints.files_page},{page}" if page > 1 else Endpoints.files_page
        try:
            r = await httpx.AsyncClient().get(endpoint)
        except:
            print("Error grabbing page (httpx exception)")
            self.remaining_elements.append(page)
            return
        if r.status_code != 200:
            print(f"Error grabbing page (error code: {r.status_code})")
            self.remaining_elements.append(page)
            return

        soup = BeautifulSoup(r.text, "lxml")

        grabbed_files = self._bs_get_chomikuj_filelist_from_page(soup)
        for grabbed_file in grabbed_files:
            self.files.append(grabbed_file)

    # @override
    # async def grab_all(self):
    #     await super().grab_all()


async def main():
    dler = ChomikujPageParser()
    print("hello")
    await dler.grab_all()
    print(len(dler.files))
    # files = await dler.get_files_from_page(0)
    # await dler.download_deb(files[0]) # type: ignore
    # page_html = await get_files_from_page(get_last_page())


if __name__ == "__main__":
    asyncio.run(main())
