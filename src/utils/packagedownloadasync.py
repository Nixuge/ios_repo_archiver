from typing import Any
from database.queries import Queries
from database.utils import Utils
from objects.files.package import Package
from objects.repo import Repo
from utils.downloaders.simple.simple_async import SimpleDownloaderAsync
from utils.downloaders.tweak._tweak_base import _TweakDownloaderBase as TweakDL
from utils.downloaders.tweak.tweak_async import TweakDownloaderAsync
from utils.vars.db import DbVars
from utils.vars.file import Folder
from utils.vars.statuscodes import StatusCodes

class PackageDownloadAsync:
    repo: Repo
    package: Package
    paid: bool

    def __init__(self, repo: Repo, package: Package):
        self.repo = repo
        self.package = package
        self.paid = False
    
    async def _download_other_data(self) -> dict[str, Any]:
        other_data: dict[str, Any] = {}
        for key in ("depiction", "moderndepiction", "icon", "header"):
            if not key in self.package.data:
                other_data[key] = None
                continue
        
            value = self.package.data[key]

            result = await SimpleDownloaderAsync(value).download_async(Folder.from_name(key))

            if result.finished:
                other_data[key] = result.hash
            else:
                other_data[key] = None
                if result.valid_url:
                    print("Error @ downloading other file")
                # TODO: log all errors to file or smth
            
        return other_data

    async def download_package_content_db(self):
        result = await TweakDownloaderAsync(self.repo.url, self.package.data["filename"], self.package.hashes).download_async()
        if not result.finished:
            if result.status_code in StatusCodes.paid:
                self.paid = True
                print("Got paid package !")
            else:
                print(f"Got an error ! {result.status_code} hash:{result.hash_check} {self.repo.url}{self.package.data['filename']}")
                return None #TODO: return proper error
        
        other_keys = await self._download_other_data()

        final_args = Utils.build_args(self.package, other_keys, self.paid)

        DbVars.Queue.add_instuction(Queries.get_insert_query(self.repo.table_name), final_args)
