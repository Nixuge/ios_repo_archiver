from sqlite3 import Connection
from typing import Any
from database.queries import Queries
from database.utils import Utils
from objects.files.package import Package
from objects.repo import Repo
from objects.sqlinfo import SQLInfo
from utils.downloaders.tweak import Downloader as TweakDL
from utils.downloaders.simple import Downloader as SimpleDL
from utils.file import Folder


class PackageDownload:
    repo: Repo
    package: Package
    sql: SQLInfo
    paid: bool
    paid_codes = (401, 402, 418) #unauthorized, payement required(yourepo), random (havoc)

    def __init__(self, repo: Repo, package: Package, sql: SQLInfo):
        self.repo = repo
        self.package = package
        self.sql = sql
        self.paid = False
    
    def _download_other_data(self) -> dict[str, Any]:
        other_data: dict[str, Any] = {}
        for key in ("depiction", "moderndepiction", "icon", "header"):
            if not key in self.package.data:
                other_data[key] = None
                continue
        
            value = self.package.data[key]

            result = SimpleDL(value).download(Folder.from_name(key))

            if result.finished:
                other_data[key] = result.hash
            else:
                other_data[key] = None
                print("Error @ downloading other file")
                # TODO: log all errors to file or smth
            
        return other_data

    def download_all_add_db(self):
        result = TweakDL(self.repo.url, self.package.data["filename"], self.package.hashes).download()
        if not result.finished:
            if result.status_code in self.paid_codes:
                self.paid = True
                print("Got paid package !")
            else:
                return None #TODO: return proper error
        
        other_keys = self._download_other_data()

        final_args = Utils.build_args(self.package, other_keys, self.paid)

        self.sql.cursor.execute(Queries.get_insert_query(self.repo.name), final_args)
        self.sql.connection.commit()
