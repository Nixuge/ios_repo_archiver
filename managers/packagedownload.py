from sqlite3 import Connection
from database.queries import Queries
from database.utils import Utils
from objects.files.package import Package
from objects.repo import Repo
from objects.sqlinfo import SQLInfo
from utils.downloaders.tweak import Downloader as TweakDL
from utils.downloaders.simple import Downloader as SimpleDL
from utils.file import Folder


class PackageDownloadResult:
    pass

class PackageDownload:
    repo: Repo
    package: Package
    sql: SQLInfo

    def __init__(self, repo: Repo, package: Package, sql: SQLInfo):
        self.repo = repo
        self.package = package
        self.sql = sql
    
    def _download_other_data(self) -> list[str | None]:
        other_data: list[str | None] = []
        for key in ("depiction", "sileodepiction", "icon", "header"):
            if not key in self.package.data:
                other_data.append(None)
                continue
        
            value = self.package.data[key]

            result = SimpleDL(value).download(Folder().from_name(key))

            if result.finished:
                other_data.append(result.hash)
            else:
                other_data.append(None)
                print("Error @ downloading other file")
                # TODO: log all errors to file or smth
            
        return other_data

    def download_all(self):
        result = TweakDL(self.repo.url, self.package.data["filename"], self.package.hashes).download()
        if not result.finished:
            print("Error!")
            print(result.status_code)
            return None #TODO: return proper error
        
        other_keys = self._download_other_data()

        final_args = Utils.build_args(self.package, other_keys)

        self.sql.cursor.execute(Queries.get_insert_query(self.repo.name), final_args)
        self.sql.connection.commit()
