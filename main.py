from objects.packagedownload import PackageDownload
from objects.sqlinfo import SQLInfo
from objects.repo import Repo

import sqlite3

from utils.file import Folder

# TODO: add tests

# TODO: save missing files in a json for retry later
# TODO: sometimes Headers is in moderndepiction, try to grab it there

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

# Make all folders
Folder.create_all()

# Init DB
connection = sqlite3.connect("test.db")
sqlinfo = SQLInfo(connection, connection.cursor())

# Init repo
repo = Repo("apptapp", "https://apptapp.me/repo/", sqlinfo)
repo.remove_existing_packages()

# Download all
for pkg in repo.packages:
    pkgdl = PackageDownload(repo, pkg, sqlinfo)
    print("===Starting DL===")
    print(f"Downloading {pkg.data['package']}")
    pkgdl.download_package_content_db()
    print("===Done with DL===")
