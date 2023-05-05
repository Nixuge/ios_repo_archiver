# https://github.com/Paisseon/Violyn-/Violyn/DataTypes/ChomikAPI.swift

from dataclasses import dataclass


# @dataclass
# class UrlHeaderPair:
#     url: str
#     headers: dict

class Endpoints:
    # delete = "https://chomikuj.pl/action/FileDetails/DeleteFileAction"
    download = "https://chomikuj.pl/action/License/Download"
    login = "https://chomikuj.pl/action/login/login/login"
    search = "https://chomikuj.pl/action/Files/FilesList"
    upload = "https://chomikuj.pl/action/Upload/GetUrl"
    files_page = "https://chomikuj.pl/farato/Dokumenty/debfiles"
    files_last_page = "https://chomikuj.pl/farato/Dokumenty/debfiles,99999"

class Headers:
    __RequestVerificationToken = """b%2BsiLdIH65m5AVq2Xk7B0VHudOFB%2BrddgeMKqSSaYhNNEHULqRRQbNWkLDrPB%2FT%2F2aCx0RIJUz3w5UVygR6StTykyxlNxGWo3iWYC5eIjljDNHYcM5AL9MbQagSUy6YKs%2BkyXg%3D%3D"""

# class Regexes:
