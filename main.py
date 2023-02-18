import os
from managers.Downloader import Downloader
from managers.Repo import Repo
from files.Package import Package
from files.Release import Release


repo = Repo("Chariz", "https://repo.chariz.com/")


for thing in repo.packages:
    #TODO: CHECK FOR ENTRY IN DB BEFORE DOWNLOADING
    
    print(thing.data["Package"])
    result = Downloader(repo.url, thing.data["Filename"], thing.hashes).download()
    os.system("rm tmp/*")

    if result.status_code != 200:
        print("Something wrong !")
        #TODO: Add to diff table "paid_tweaks" if 401
        print(result.status_code)
        input()
    
    elif result.already_exists:
        print("file already there !")
        # input()
    
    elif not result.hash_check:
        print("invalid hash !")
        input()
