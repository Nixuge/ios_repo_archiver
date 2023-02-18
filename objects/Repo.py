from managers.packages import PackagesManager
from objects.files.Release import Release
from objects.files.Package import Package

from utils.download import download_str

class Repo:
    name: str
    url: str
    release: Release
    packages: list[Package]

    # in 99% of cases:
    #/Release
    #/dists/stable/main/binary-iphoneos-arm/Release
    #less common
    #or iphoneos-arm iphoneos-arm64 iphoneos-arm64-rootless
    # -> see "proxyman" on iOS

    def __init__(self, repo_name: str, repo_url: str, subpath: str = ""):
        self.name = repo_name
        self.url = repo_url
        self.release = Release(download_str(repo_url + "Release"))
        self.packages = PackagesManager.get_packages(repo_url, self.release)
        #TODO: use subpath
