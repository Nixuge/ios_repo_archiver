# DLF = download folder
import os
import shutil


# THIS SHOULD BE REWROTE
# IF POSSIBLE TO A STATIC WAI
# TO AVOID 50 INSTANCES
# ONLY PROBLEM RN IS __GETATTRIBUTE__ FOR THAT
class Folder:
    def create(self):  # cant make it static bc __getattribute__
        for folder in dir(Folder):
            if "__" in folder or folder in ("create", "from_name"): 
                continue
            path = self.__getattribute__(folder)
            if not os.path.exists(path):
                os.makedirs(path)

    def from_name(self, attribute: str):
        return self.__getattribute__(attribute)

    base = "downloads/"
    temp = base + "z_tmp/"
    debs = base + "debs/"
    depiction = base + "depictions/"
    moderndepiction = base + "moderndepiction/"
    icon = base + "icons/"
    header = base + "headers/"


def get_create_path(folder: str, hash: str) -> str:
    folder = f"{folder}/{hash[0]}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

# Unused
def save_file(temp_name: str, folder: str, hash: str, extension: str):
    get_create_path(folder, hash)
    shutil.move(Folder.temp + temp_name, f"{folder}{hash}.{extension}")
