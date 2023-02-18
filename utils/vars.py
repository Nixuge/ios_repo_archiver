import os
import types


class VARS:
    pass


# DLF = download folder
class DLF:
    def create__(self):  # cant make it static bc __getattribute__
        for folder in dir(DLF):
            if "__" in folder:
                continue
            path = self.__getattribute__(folder)
            if not os.path.exists(path):
                os.makedirs(path)

    temp = "z_tmp/"
    base = "downloads/"
    debs = base + "debs/"
    depictions = base + "depictions/"
    sileodepiction = base + "sileodepictions/"
    icon = base + "icons/"
    header = base + "headers/"
