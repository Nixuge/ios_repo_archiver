# Missing extensions
# .zst (Pretty much never used alone, won't add unless necessary)

from objects.files.package import Package
from objects.files.release import Release
from utils.download import download_bytes

import gzip
import bz2
import lzma


class PackagesManager:
    supported_packages = {
        "Packages": bytes,
        "Packages.gz": gzip.decompress,
        "Packages.bz2": bz2.decompress,
        "Packages.lzma": lzma.decompress,
        "Packages.xz": lzma.decompress
    }

    release: Release
    base_url: str

    def __init__(self, base_url: str, release: Release):
        self.release = release
        self.base_url = base_url

    @staticmethod
    def _get_packages_from_file(packages_file: str) -> list[Package]:
        packages_list = []
        packages_raw = packages_file.split("\n\n")
        for pkg in packages_raw:
            pkg = Package(pkg)
            if pkg.data != {}:
                packages_list.append(pkg)
        return packages_list

    def _get_package_filename(self) -> str | None:
        for key in self.release.files.keys():
            if key in self.supported_packages.keys():
                return key

    def _get_data(self, found_file: str | None) -> str | None:
        if found_file:
            print(f"Using packages file found in release: {found_file}")
            data, _ = download_bytes(self.base_url + found_file)
            return self.supported_packages[found_file](data).decode()

        data: bytes = b''
        found_file = None

        for file in self.supported_packages.keys():
            data, code = download_bytes(self.base_url + file)
            if code == 200:
                found_file = file
                break

        if not found_file:
            return None

        # print(found_file)

        print(f"Using found release file: {found_file}")
        return self.supported_packages[found_file](data).decode(errors="ignore")

    def get_packages(self) -> list[Package]:
        found_file = self._get_package_filename()

        packages_file = self._get_data(found_file)
        if not packages_file:
            raise Exception(f"No release file found in repo {self.base_url}")

        return PackagesManager._get_packages_from_file(packages_file)
