from objects.packagedownload import PackageDownload
from objects.sqlinfo import SQLInfo
from objects.repo import Repo

import sqlite3

from utils.file import Folder

# TODO: add tests

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

Folder.create_all()

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
sqlinfo = SQLInfo(connection, cursor)

repo = Repo("apptapp", "https://apptapp.me/repo/", sqlinfo)

repo.remove_existing_packages()

for pkg in repo.packages:
    pkgdl = PackageDownload(repo, pkg, sqlinfo)
    print("===Starting DL===")
    print(f"Downloading {pkg.data['package']}")
    pkgdl.download_package_content_db()
    print("===Done with DL===")