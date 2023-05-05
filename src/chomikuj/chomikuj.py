
import asyncio
import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

# TODO: move to real things once done
from chomikuj_file import ChomikujFile
from chomikuj_data import Endpoints

class ChomikujDownloader:
    last_page: int
    downloaded_pages: list[int]
    remaining_pages: list[int]
    failed_pages: list[int]

    def __init__(self) -> None:
        self._get_last_page()
        self.downloaded_pages = []
        self.remaining_pages = []
        self.failed_pages = []
    
    def _get_last_page(self) -> None:
        r = httpx.get(Endpoints.files_last_page, follow_redirects=True)
        if r.status_code != 200:
            print(f"EXCEPTION HAPPENED! code:{r.status_code} (not handling as not getting this should crash)")

        # URL redirects to same as Endpoints.last_page but with ,9999 replaced by max page num
        self.last_page = int(str(r.url).split(",")[-1])

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
        
        return ChomikujFile(
            filename=download_element.find("span").text, # type: ignore
            filepath=download_element.get("href"), # type: ignore
            filesize=size,
            date_added=date
        )

    async def get_files_from_page(self, page: int):
        endpoint = f"{Endpoints.files_page},{page}" if page > 1 else Endpoints.files_page
        print(endpoint)
        try:
            r = await httpx.AsyncClient().get(endpoint)
        except:
            print("Error grabbing page")
            self.failed_pages.append(page)
            return
        if r.status_code != 200:
            print("Error grabbing page")
            self.failed_pages.append(page)
            return
        print("done requesting")
        soup = BeautifulSoup(r.text, "lxml")
        files = self._bs_get_chomikuj_filelist_from_page(soup)
        print(len(files))


        # print(len(divEle))

async def main():
    await ChomikujDownloader().get_files_from_page(0)
    # page_html = await get_files_from_page(get_last_page())


if __name__ == "__main__":
    asyncio.run(main())
