from objects.packagedownload import PackageDownload
from objects.repometa import RepoMeta
from objects.sqlinfo import SQLInfo
from objects.repo import Repo

import sqlite3

from utils.file import Folder

# TODO: add tests
# TODO: add cmd line args
# TODO: add an option to re check paid packages
# TODO: support loading local repo folder
# TODO: note if other media download failed
# TODO: check httpx or smth lib for async requests


# TODO: save missing files in a json for retry later
# TODO: sometimes Headers is in moderndepiction, try to grab it there
# TODO: add settings (eg. not save headers & icons & etc)

# NOTE:
# since repo release files are pretty lightweight
# there's no need to bother with SQL
# they'll all just be saved in JSON and loaded into ram

# NOTE:
# HYI's Packages file has some UTF-8 encoding errors
# See package "IAPFree Toggle" (0x96 bytes in author field)


# Make all folders
Folder.create_all()

# Init DB
connection = sqlite3.connect("test.db")
sqlinfo = SQLInfo(connection, connection.cursor())


# TODO: read this from a json

repos: list[RepoMeta] = [
    RepoMeta("Havoc", "https://havoc.app/", "havoc_app"),
    RepoMeta("AppTapp Repository", "https://apptapp.me/repo/", "apptapp_me__repo"),
    RepoMeta("19card's Repo", "https://19card.github.io/repo/", "_19card_github_io__repo"),
    RepoMeta("PoomSmart's Repo", "https://poomsmart.github.io/repo/", "poomsmart_github_io__repo"),
    RepoMeta("Delta", "https://getdelta.co", "getdelta_co"),
    RepoMeta("Alfhaily APT", "https://apt.alfhaily.me", "apt_alfhaily_me"),
    RepoMeta("alexia's repo", "https://repo.cadoth.net", "repo_cadoth_net"),
    RepoMeta("AnthoPak's Repo", "https://repo.anthopak.dev", "repo_anthopak_dev"),
    # Pirate repo but see objects/files/package.py#68
    RepoMeta("HackYourIphone", "https://repo.hackyouriphone.org", "repo_hackyouriphone_org") 
]

# Kinda dirty repo picker for now
names = [repo.full_name for repo in repos]
print(f"Repos available: {names}")
choosen_repo = input("Choose your repo of choice: ")

choosen_repo_meta: RepoMeta = RepoMeta("", "", "")
for repometa in repos:
    if repometa.full_name == choosen_repo.strip():
        choosen_repo_meta = repometa
        break

if choosen_repo_meta.full_name == "":
    print("Select an available repo", 1 / 0)


# Init repo
repo = Repo(choosen_repo_meta.sql_name, choosen_repo_meta.url, sqlinfo)
repo.remove_existing_packages()

# Download all
for pkg in repo.packages:
    pkgdl = PackageDownload(repo, pkg, sqlinfo)
    print("===Starting DL===")
    print(f"Downloading {pkg.data['package']}")
    pkgdl.download_package_content_db()
    print("===Done with DL===")

print("Done downloading")