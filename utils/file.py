# DLF = download folder
import os
import shutil


# Class can't be made static, hence why line below it
class _Folder:
    def create_all(self):
        for folder in dir(_Folder):
            if "__" in folder or folder in ("create_all", "from_name"): 
                continue
            path = self.__getattribute__(folder)
            if not os.path.exists(path):
                os.makedirs(path)

    def from_name(self, attribute: str):
        return self.__getattribute__(attribute)

    base = "downloads/"
    temp = base + ".tmp/"
    debs = base + "debs/"
    depiction = base + "depictions/"
    moderndepiction = base + "moderndepiction/"
    icon = base + "icons/"
    header = base + "headers/"

#made for easy access (eg Folder.create())
Folder = _Folder()


def get_create_path(folder: str, hash: str) -> str:
    folder = f"{folder}/{hash[0]}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

# Unused
def save_file(temp_name: str, folder: str, hash: str, extension: str):
    get_create_path(folder, hash)
    shutil.move(Folder.temp + temp_name, f"{folder}{hash}.{extension}")
