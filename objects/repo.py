from database.queries import Queries
from database.utils import Utils
from utils.packagesmanager import PackagesManager
from objects.files.release import Release
from objects.files.package import Package
from objects.sqlinfo import SQLInfo

from utils.downloaders.utils import download_str

class Repo:
    sqlinfo: SQLInfo
    table_name: str
    url: str
    release: Release
    packages: list[Package]

    # in 99% of cases:
    #/Release
    #/dists/stable/main/binary-iphoneos-arm/Release
    #less common
    #or iphoneos-arm iphoneos-arm64 iphoneos-arm64-rootless
    # -> see "proxyman" on iOS

    def __init__(self, table_name: str, repo_url: str, sqlinfo: SQLInfo, subpath: str = ""):
        self.sqlinfo = sqlinfo
        self.table_name = table_name
        self.url = repo_url
        if self.url[-1] != '/':
            self.url += '/'
        #TODO: add if not starting w http/https or smth
        self.release = Release(download_str(self.url + "Release"))
        self.packages = PackagesManager(self.url, self.release).get_packages()

        sqlinfo.cursor.execute(Queries.get_create_repo_table_query(table_name))
        #TODO: use subpath

    def remove_existing_packages(self):
        new_pkges = []
        for pkg in self.packages:
            if not Utils.contains_md5(self.table_name, pkg.hashes["md5sum"], self.sqlinfo.cursor):
                new_pkges.append(pkg)
        self.packages = new_pkges
            
