# All possible extensions (afaik):
# <no ext> (DONE)
# .bz2
# .lzma
# .xz
# .zst
# .gz (getdelta.co has only this one)

from objects.files.package import Package
from objects.files.release import Release
from utils.download import download_str

class PackagesManager:
    @staticmethod
    def _get_packages_from_file(packages_file: str) -> list[Package]:
        packages_list = []
        packages_raw = packages_file.split("\n\n")
        for pkg in packages_raw:
            pkg = Package(pkg)
            if pkg.data != {}:
                packages_list.append(pkg)
        return packages_list


    @staticmethod
    def get_packages(base_url: str, release: Release) -> list[Package]:
        # TODO: add support to remaining file extensions
        # see top of file
        if "Packages" in release.files:
            return PackagesManager._get_packages_from_file(download_str(base_url + "Packages"))
        # elif "Packages.bz2" in release.files: ...

        # IF nothing found (eg poomsmart repo), just default to "Packages"
        return PackagesManager._get_packages_from_file(download_str(base_url + "Packages"))
    