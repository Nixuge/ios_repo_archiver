from managers.packagedownload import PackageDownload
from objects.sqlinfo import SQLInfo
from utils.downloaders.tweak import Downloader
from objects.repo import Repo
from objects.files.package import Package
from objects.files.release import Release

import sqlite3

from database.utils import Utils
from database.queries import Queries
from utils.file import Folder

# TODO: add tests

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

Folder.create_all()

repo = Repo("havoc", "https://havoc.app/")

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute(Queries.get_create_repo_table_query(repo.name))

sqldata = SQLInfo(connection, cursor)

for thing in repo.packages:
    if Utils.contains_md5(repo.name, thing.hashes["md5sum"], cursor):
        print("md5 already present in that repo.")
        continue
    
    pkgdl = PackageDownload(repo, thing, sqldata)
    print("===Starting DL===")
    pkgdl.download_all_add_db()
    print("===Done with DL===")


