from chomikuj.chomikuj_deb_downloader import ChomikujDebDownloader
from chomikuj.chomikuj_page_parser import ChomikujPageParser
from chomikuj.data.chomikuj_data import DbVarsChomikuj
from database.queries import QueriesChomikuj

# chomikuj is kinda separated from the whole thing
# as it's not really a repo
# Still has its place here as it holds tweaks

async def chomikuj_main():
    DbVarsChomikuj.Queue.add_important_instruction(QueriesChomikuj.get_create_repo_table_query())

    page_parser = ChomikujPageParser()
    print("Starting page parser")
    await page_parser.grab_all()
    print(f"Parsed {len(page_parser.files)} files.")

    elements_shared_list = list(page_parser.files) 

    deb_downloader = ChomikujDebDownloader()
    deb_downloader.remaining_elements = elements_shared_list
    await deb_downloader.grab_all()
    # files = await dler.get_files_from_page(0)
    # await dler.download_deb(files[0]) # type: ignore
    # page_html = await get_files_from_page(get_last_page())
