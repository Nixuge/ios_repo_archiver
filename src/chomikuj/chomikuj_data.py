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

class RequestData:
    token_key = "__RequestVerificationToken"
    token_value = "b+siLdIH65m5AVq2Xk7B0VHudOFB+rddgeMKqSSaYhNNEHULqRRQbNWkLDrPB/T/2aCx0RIJUz3w5UVygR6StTykyxlNxGWo3iWYC5eIjljDNHYcM5AL9MbQagSUy6YKs+kyXg=="
    cookie = "ChomikSession=d3fb23c6-430d-456c-b729-bbb72fefaf99; __RequestVerificationToken_Lw__=w8xQ4U9IcdB71uD/zSxUsJXuEQQOsI1Dogfg9d4xN3p0xxRp/wTg+oqiDdqIYGZfhEfswCKnlA47H0IBDt53LrdOy7oCNzKdOdp/lTwQAn/Zw++5skZFvLLcktKreTD7mZMZTQ==; rcid=3; guid=999f1623-f0ea-4497-8775-50832b6258df;"
