from managers.Downloader import Downloader
from managers.Repo import Repo
from files.Package import Package
from files.Release import Release


repo = Repo("Chariz", "https://repo.chariz.com/")


for thing in repo.packages:
    print(thing.data["Package"])
    Downloader(repo.url, thing.data["Filename"]).download()
    # input()