# DLF = download folder
import os
import shutil


class Folder:
    def create__(self):  # cant make it static bc __getattribute__
        for folder in dir(Folder):
            if "__" in folder: 
                continue
            path = self.__getattribute__(folder)
            if not os.path.exists(path):
                os.makedirs(path)

    base = "downloads/"
    temp = base + "z_tmp/"
    debs = base + "debs/"
    depictions = base + "depictions/"
    sileodepiction = base + "sileodepictions/"
    icon = base + "icons/"
    header = base + "headers/"


# Unused
def save_file(temp_name: str, folder: str, hash: str, extension: str):
    folder = f"{folder}/{hash[0]}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    shutil.move(Folder.temp + temp_name, f"{folder}{hash}.{extension}")
