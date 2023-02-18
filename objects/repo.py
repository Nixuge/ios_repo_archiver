from database.queries import Queries
from database.utils import Utils
from managers.packages import PackagesManager
from objects.files.release import Release
from objects.files.package import Package
from objects.sqlinfo import SQLInfo

from utils.download import download_str

class Repo:
    sqlinfo: SQLInfo
    name: str
    url: str
    release: Release
    packages: list[Package]

    # in 99% of cases:
    #/Release
    #/dists/stable/main/binary-iphoneos-arm/Release
    #less common
    #or iphoneos-arm iphoneos-arm64 iphoneos-arm64-rootless
    # -> see "proxyman" on iOS

    def __init__(self, repo_name: str, repo_url: str, sqlinfo: SQLInfo, subpath: str = ""):
        self.sqlinfo = sqlinfo
        self.name = repo_name
        self.url = repo_url
        self.release = Release(download_str(repo_url + "Release"))
        self.packages = PackagesManager.get_packages(repo_url, self.release)

        sqlinfo.cursor.execute(Queries.get_create_repo_table_query(repo_name))
        #TODO: use subpath

    def remove_existing_packages(self):
        new_pkges = []
        for pkg in self.packages:
            if not Utils.contains_md5(self.name, pkg.hashes["md5sum"], self.sqlinfo.cursor):
                new_pkges.append(pkg)
        self.packages = new_pkges
            
