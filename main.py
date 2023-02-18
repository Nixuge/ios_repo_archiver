import os
from utils.Downloader import Downloader
from objects.Repo import Repo
from objects.files.Package import Package
from objects.files.Release import Release

import sqlite3

from database.queries import QUERIES

# TODO: add tests

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

repo = Repo("Chariz", "https://repo.chariz.com/")


for thing in repo.packages:
    #TODO: CHECK FOR ENTRY IN DB BEFORE DOWNLOADING
    ok = sqlite3.connect("owo3.db")
    cursor = ok.cursor()

    # args_order = ("package")


    # print(thing.data["Package"])
    # result = Downloader(repo.url, thing.data["Filename"], thing.hashes).download()
    # os.system("rm z_tmp/*")

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
