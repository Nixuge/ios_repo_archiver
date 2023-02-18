import os
from database.utils import Utils
from utils.downloaders.tweak import Downloader
from objects.Repo import Repo
from objects.files.Package import Package
from objects.files.Release import Release

import sqlite3

from database.queries import Queries
from utils.file import Folder

# TODO: add tests

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

# make all folders
# actually nvm lol
# Folder().create__()

input()

repo = Repo("Chariz", "https://repo.chariz.com/")

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute(Queries.get_create_repo_table_query(repo.name))

for thing in repo.packages:
    #TODO: CHECK FOR ENTRY IN DB BEFORE DOWNLOADING
    
    if Utils.contains_md5(repo.name, thing.hashes["md5sum"], cursor):
        print("md5 already present in that repo.")
        continue

    final_args = Utils.build_args(thing)

    cursor.execute(Queries.get_insert_query(repo.name), final_args)

print("all done")
connection.commit()
print("sql done")

    # print(thing.data["Package"])
    # result = Downloader(repo.url, thing.data["Filename"], thing.hashes).download()

    # if result.status_code != 200:
    #     print("Something wrong !")
    #     #TODO: Add to diff table "paid_tweaks" if 401
    #     #or add "paid" attribute
    #     print(result.status_code)
    #     input()
    
    # elif result.already_exists:
    #     print("file already there !")
    #     # input()
    
    # elif not result.hash_check:
    #     print("invalid hash !")
    #     input()
