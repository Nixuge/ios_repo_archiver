#!/bin/python3

from config.argparser import ArgsParser
from config.config import Config
from utils.packagedownload import PackageDownload
from objects.repometa import RepoMeta
from objects.sqlinfo import SQLInfo
from objects.repo import Repo

import sqlite3
from utils.prints import print_same_line

from utils.vars.file import Folder

# TODO: add tests
# TODO: support loading local repo folder
# TODO: note if other media download failed
# TODO: check httpx or smth lib for async requests

# TODO: (eventually) add way to see data from the db

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


ArgsParser().get_repos()


# repos: list[RepoMeta] = [
#     RepoMeta("Havoc", "https://havoc.app/"),
#     RepoMeta("AppTapp Repository", "https://apptapp.me/repo/"),
#     RepoMeta("19card's Repo", "https://19card.github.io/repo/",),
#     RepoMeta("PoomSmart's Repo", "https://poomsmart.github.io/repo/"),
#     RepoMeta("Delta", "https://getdelta.co"),
#     RepoMeta("Alfhaily APT", "https://apt.alfhaily.me"),
#     RepoMeta("alexia's repo", "https://repo.cadoth.net"),
#     RepoMeta("AnthoPak's Repo", "https://repo.anthopak.dev"),
#     RepoMeta("HackYourIphone", "https://repo.hackyouriphone.org") 
# ]
repos: list[RepoMeta] = [
    RepoMeta("https://havoc.app/"),
    RepoMeta("https://apptapp.me/repo/"),
    RepoMeta("https://19card.github.io/repo/",),
    RepoMeta("https://poomsmart.github.io/repo/"),
    RepoMeta("https://getdelta.co"),
    RepoMeta("https://apt.alfhaily.me"),
    RepoMeta("https://repo.cadoth.net"),
    RepoMeta("https://repo.anthopak.dev"),
    # Pirate repo but see objects/files/package.py#68
    RepoMeta("https://repo.hackyouriphone.org") 
]



# Kinda dirty repo picker for now
names = [repo.url for repo in repos]
print(f"Repos available: {names}")
choosen_repo = input("Choose your repo of choice: ")

choosen_repo_meta: RepoMeta = RepoMeta("invalid.fr")
for repometa in repos:
    if repometa.url == choosen_repo.strip():
        choosen_repo_meta = repometa
        break

if choosen_repo_meta.url == "invalid.fr":
    print("Select an available repo", 1 / 0)


# Init repo
repo = Repo(choosen_repo_meta.sql_name, choosen_repo_meta.url, sqlinfo)

if choosen_repo_meta.config.print_progress:
    print(f"Full packages: {len(repo.packages)}")

repo.remove_existing_packages()

if choosen_repo_meta.config.print_progress:
    print(f"Stripped packages: {len(repo.packages)}")

# Download all
for index, pkg in enumerate(repo.packages):
    pkgdl = PackageDownload(repo, pkg, sqlinfo)
    if choosen_repo_meta.config.print_progress:
        print_same_line(f"Downloading package {index+1}/{len(repo.packages)} ({pkg.data['package']})")
    pkgdl.download_package_content_db()

if choosen_repo_meta.config.print_progress:
    print("Done downloading")
