# All possible extensions (afaik):
# <no ext> (DONE)
# .bz2
# .lzma
# .xz
# .zst

from objects.files.Package import Package
from objects.files.Release import Release
from downloadUtils import download_str

class PackagesManager:
    @staticmethod
    def _get_packages_from_file(packages_file: str) -> list[Package]:
        packages_list = []
        packages_raw = packages_file.split("\n\n")
        for pkg in packages_raw:
            owo = Package(pkg)
            packages_list.append(owo)
        return packages_list


    @staticmethod
    def get_packages(base_url: str, release: Release) -> list[Package] | None:
        if "Packages" in release.files:
            return PackagesManager._get_packages_from_file(download_str(base_url + "Packages"))
        
        return None
        # TODO: add support to remaining file extensions
        # see top of file